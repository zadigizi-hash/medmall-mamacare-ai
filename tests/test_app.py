"""Basic functional tests for the local MamaCare AI proof of concept."""
import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen

from app import Handler, answer_question, detect_red_flag, retrieve_articles


class KnowledgeTests(unittest.TestCase):
    def test_antenatal_question_retrieves_source_material(self):
        results = retrieve_articles("What should I ask at an antenatal appointment?")
        self.assertTrue(results)
        self.assertEqual(results[0]["id"], "antenatal-care")

    def test_unmatched_question_does_not_invent_answer(self):
        result = answer_question("Explain quantum chromodynamics and the Andromeda galaxy.")
        self.assertIn("not have enough information", result["answer"])
        self.assertEqual(result["status"], "no_match_not_a_safety_clearance")

    def test_urgent_phrase_triggers_care_message(self):
        result = answer_question("I have heavy bleeding")
        self.assertEqual(result["status"], "urgent_language_detected")
        self.assertIn("immediate assessment", result["answer"])

    def test_non_trigger_is_not_labelled_safe(self):
        result = answer_question("I have a mild question about pregnancy")
        self.assertNotEqual(result["status"], "safe")
        self.assertIn("not_a_safety_clearance", result["status"])

    def test_red_flag_match_is_case_insensitive(self):
        self.assertIsNotNone(detect_red_flag("SEVERE HEADACHE and blurred vision"))


class ApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f"http://127.0.0.1:{cls.server.server_port}"

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join(timeout=2)

    def test_health_endpoint_discloses_unvalidated_status(self):
        with urlopen(self.base + "/api/health") as response:
            body = json.loads(response.read())
        self.assertEqual(body["status"], "ok")
        self.assertEqual(body["clinical_review"], "pending")
        self.assertFalse(body["ai_connected"])

    def test_articles_endpoint_returns_source_links(self):
        with urlopen(self.base + "/api/articles") as response:
            body = json.loads(response.read())
        self.assertGreaterEqual(len(body["articles"]), 1)
        self.assertTrue(body["articles"][0]["url"].startswith("https://"))

    def test_ask_endpoint_accepts_question(self):
        data = json.dumps({"question": "What is antenatal care?", "stage": "pregnancy"}).encode()
        request = Request(self.base + "/api/ask", data=data,
                          headers={"Content-Type": "application/json"})
        with urlopen(request) as response:
            body = json.loads(response.read())
        self.assertIn("answer", body)
        self.assertIn("sources", body)


if __name__ == "__main__":
    unittest.main()

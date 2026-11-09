#!/usr/bin/env python3
"""MedMall MamaCare AI - early local proof of concept.

Run: python app.py
Open: http://127.0.0.1:8000

This is not a medical device, diagnostic system, or validated triage tool.
Clinical content and safety rules require qualified maternal-health review.
"""
from __future__ import annotations

import json
import os
import re
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from typing import Any
from urllib.parse import urlparse

HOST = os.environ.get("HOST", "127.0.0.1")
PORT = int(os.environ.get("PORT", "8000"))
MAX_BODY = 8000

ARTICLES = [
    {
        "id": "antenatal-care",
        "title": "Antenatal care and preparing for appointments",
        "tags": ["pregnancy", "antenatal", "appointment", "checkup", "midwife", "doctor"],
        "content": "Antenatal care gives a pregnant woman opportunities to receive health checks, information, counselling and support from a skilled health worker. Keep a record of questions and concerns to discuss at each visit, and follow the care schedule provided by your own healthcare team. Ask your care team where to seek help if a concern arises.",
        "source": "WHO - Getting the health services you need during pregnancy",
        "url": "https://www.who.int/tools/your-life-your-health/life-phase/pregnancy--birth-and-after-childbirth/getting-the-health-services-you-need-during-pregnancy"
    },
    {
        "id": "postnatal-care",
        "title": "Postnatal care and follow-up",
        "tags": ["postnatal", "after birth", "new mother", "newborn", "follow up", "recovery", "baby"],
        "content": "Postnatal care supports the health and wellbeing of both the mother and newborn after childbirth. The timing and content of follow-up contacts should be agreed with a qualified health worker and adapted to the mother's and baby's needs. Keep the contact details of the facility or provider responsible for follow-up.",
        "source": "WHO - Getting the health services you need after childbirth",
        "url": "https://www.who.int/tools/your-life-your-health/life-phase/pregnancy--birth-and-after-childbirth/getting-the-health-services-you-need-after-childbirth"
    },
    {
        "id": "maternal-warning-signs",
        "title": "When to seek urgent maternal care",
        "tags": ["danger signs", "warning signs", "bleeding", "seizure", "headache", "blurred vision", "fever", "pain", "breathing"],
        "content": "Some symptoms during pregnancy or after childbirth require urgent professional assessment. Examples include heavy vaginal bleeding, convulsions or seizures, severe headache with vision changes, severe abdominal pain, fever with marked illness, or difficulty breathing. Do not rely on an online tool to decide that a symptom is safe. Seek urgent assessment at a health facility or contact local emergency services.",
        "source": "WHO - Pregnancy, childbirth and after childbirth health information",
        "url": "https://www.who.int/health-topics/maternal-health"
    },
    {
        "id": "maternal-wellbeing",
        "title": "Emotional wellbeing during and after pregnancy",
        "tags": ["mental health", "psychological", "emotional", "sad", "anxious", "stress", "postpartum", "wellbeing"],
        "content": "Emotional wellbeing is part of health during pregnancy and after childbirth. If worry, sadness, anxiety, exhaustion or difficulty coping is affecting daily life, consider speaking with a qualified health worker. If you feel at immediate risk of harming yourself or someone else, seek urgent help from a qualified professional or local emergency service now. This tool does not screen for or diagnose a mental health condition.",
        "source": "WHO - Keeping well during pregnancy and after childbirth",
        "url": "https://www.who.int/health-topics/mental-health"
    }
]

URGENT_TERMS = [
    "heavy bleeding", "severe bleeding", "bleeding heavily", "seizure", "convulsion",
    "cannot breathe", "difficulty breathing", "trouble breathing", "severe headache",
    "blurred vision", "vision changes", "severe abdominal pain", "severe stomach pain",
    "high fever", "fever and very weak", "baby is not breathing", "baby cannot breathe",
    "want to harm myself", "suicide", "kill myself"
]

def detect_red_flag(question: str) -> str | None:
    text = re.sub(r"\s+", " ", question.casefold())
    for term in URGENT_TERMS:
        if term in text:
            return term
    return None

def retrieve_articles(question: str, limit: int = 3) -> list[dict[str, Any]]:
    words = set(re.findall(r"[a-z0-9]+", question.casefold()))
    stop = {"the", "and", "for", "with", "what", "when", "how", "can", "does", "should",
            "about", "from", "your", "are", "is", "my", "me", "i", "to", "of", "in", "on"}
    words = {w for w in words if len(w) > 2 and w not in stop}
    ranked = []
    for article in ARTICLES:
        searchable = " ".join([article["title"], article["content"], " ".join(article["tags"])])
        score = len(words & set(re.findall(r"[a-z0-9]+", searchable.casefold())))
        if score:
            ranked.append((score, article))
    ranked.sort(key=lambda item: item[0], reverse=True)
    return [a for _, a in ranked[:limit]]

def answer_question(question: str, stage: str = "general") -> dict[str, Any]:
    trigger = detect_red_flag(question)
    if trigger:
        return {
            "answer": "Your message contains a phrase that may describe an urgent warning sign. Please seek immediate assessment at the nearest health facility or contact local emergency services now. Do not wait for an online response. This prototype cannot assess your condition.",
            "status": "urgent_language_detected",
            "mode": "illustrative local safety rules",
            "sources": []
        }
    matches = retrieve_articles(question)
    if not matches:
        return {
            "answer": "I do not have enough information in this prototype to answer reliably. Please discuss your question with a qualified healthcare professional. This tool cannot assess personal symptoms or replace clinical care.",
            "status": "no_match_not_a_safety_clearance",
            "mode": "local knowledge demo",
            "sources": []
        }
    return {
        "answer": matches[0]["content"] + "\n\nThis is general demonstration information, not a personal assessment. The content is awaiting formal clinical review by MedMall. Please confirm care decisions with a qualified healthcare professional.",
        "status": "no_urgent_phrase_detected_not_a_safety_clearance",
        "mode": "local knowledge retrieval",
        "sources": [{"title": a["source"], "url": a["url"]} for a in matches]
    }

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>MedMall MamaCare AI</title>
<style>
:root{--ink:#173a35;--muted:#64736e;--green:#1e6555;--mint:#e9f3ee;--paper:#f7f8f5;--line:#dce5df;--white:#fff;--rose:#fff0ed}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.55 Arial,sans-serif}
header{background:var(--white);border-bottom:1px solid var(--line);padding:16px max(5vw,20px);display:flex;justify-content:space-between;align-items:center}
.brand{font-weight:800;font-size:18px;color:var(--green)}.tag{font-size:12px;color:var(--muted)}
main{max-width:1100px;margin:36px auto;padding:0 20px}.hero{background:var(--mint);border-radius:18px;padding:34px;margin-bottom:22px}
h1{font-size:clamp(28px,4vw,43px);line-height:1.1;margin:0 0 12px;max-width:720px}
p{margin:8px 0;color:var(--muted)}.pill{display:inline-block;background:#d3e7dc;padding:5px 10px;border-radius:20px;font-size:12px;font-weight:700;margin-bottom:12px}
.grid{display:grid;grid-template-columns:1.2fr .8fr;gap:20px}.card{background:var(--white);border:1px solid var(--line);border-radius:16px;padding:22px;margin-bottom:18px}
h2{font-size:20px;margin:0 0 12px}label{font-size:13px;font-weight:700;display:block;margin:12px 0 6px}
input,textarea,select{width:100%;padding:12px;border:1px solid #cbd8d0;border-radius:9px;font:inherit;background:#fff;color:var(--ink)}
textarea{min-height:100px;resize:vertical}button{background:var(--green);color:white;border:0;border-radius:9px;padding:12px 17px;font-weight:700;cursor:pointer;margin-top:12px}
button.secondary{background:#e7efe9;color:var(--green)}button:disabled{opacity:.5;cursor:wait}
.notice{background:#fff8e7;border:1px solid #f0dfb3;border-radius:10px;padding:12px;font-size:13px;color:#614d20}
.result{margin-top:15px;padding:15px;background:#f3f7f4;border-radius:10px;white-space:pre-wrap}.urgent{background:var(--rose);border:1px solid #f1c5bc}
.resource{padding:12px 0;border-bottom:1px solid var(--line)}.resource a{color:var(--green);font-size:13px}
ul{padding-left:20px;color:var(--muted)}.item{display:flex;justify-content:space-between;gap:10px;padding:10px 0;border-bottom:1px solid var(--line)}
small,footer{color:var(--muted);font-size:12px}footer{text-align:center;padding:25px}
@media(max-width:760px){.grid{grid-template-columns:1fr}header{align-items:flex-start;gap:8px;flex-direction:column}.hero{padding:25px}}
</style></head>
<body>
<header><div><div class="brand">MedMall <span style="color:#b17a54">MamaCare AI</span></div><div class="tag">Maternal health information and care continuity</div></div><div class="tag">Early prototype · Not for clinical decision-making</div></header>
<main>
<section class="hero"><span class="pill">PREGNANCY · POSTNATAL · EARLY CHILDHOOD</span><h1>Care information and support, connected.</h1><p>MamaCare AI is a developing digital experience for maternal-health information, follow-up planning and navigation to professional care.</p></section>
<div class="notice"><strong>Important:</strong> This is an early demonstration. Its information and safety rules have not been clinically approved. It cannot diagnose, triage or replace a qualified healthcare professional. For a medical emergency, seek immediate care.</div>
<div class="grid" style="margin-top:20px">
<section>
<div class="card"><h2>Ask MamaCare</h2><p>Ask a general question. The demo retrieves information from a small source-linked starter library.</p>
<label for="stage">Your care stage</label><select id="stage"><option value="pregnancy">Pregnancy</option><option value="postpartum">After childbirth</option><option value="child_under_two">Child under two</option><option value="general">General</option></select>
<label for="question">Your question</label><textarea id="question" maxlength="2000" placeholder="Example: What should I discuss at an antenatal appointment?"></textarea>
<button id="ask">Find information</button><div id="result" class="result" hidden></div><div id="sources"></div></div>
<div class="card"><h2>Information library</h2><div id="articles"><p>Loading topics…</p></div></div>
</section>
<aside>
<div class="card"><h2>Care reminders</h2><p>Save a personal reminder on this device. This demo does not send SMS, email or push notifications.</p>
<label for="reminderTitle">Reminder</label><input id="reminderTitle" maxlength="100" placeholder="e.g. Antenatal appointment">
<label for="reminderDate">Date</label><input id="reminderDate" type="date">
<button id="saveReminder">Save reminder</button><div id="reminders"></div></div>
<div class="card"><h2>What this prototype does</h2><ul><li>Retrieves general information from linked sources.</li><li>Flags selected urgent phrases for immediate professional assessment.</li><li>Saves reminders locally in your browser.</li><li>Displays the current development and clinical-review status.</li></ul><small>No account, clinical record, provider directory or external AI connection is configured.</small></div>
</aside></div></main>
<footer>MedMall Digital Health Nigeria Ltd. · MamaCare AI v0.1.0 · Clinical review pending</footer>
<script>
const $=id=>document.getElementById(id);
async function loadArticles(){try{const r=await fetch('/api/articles');const d=await r.json();$('articles').innerHTML=d.articles.map(a=>'<div class="resource"><strong>'+escapeHtml(a.title)+'</strong><br><a href="'+a.url+'" target="_blank" rel="noopener">Read source material</a></div>').join('')}catch(e){$('articles').textContent='Unable to load topics.'}}
function escapeHtml(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
$('ask').onclick=async()=>{const q=$('question').value.trim();if(!q){$('question').focus();return}$('ask').disabled=true;$('result').hidden=false;$('result').className='result';$('result').textContent='Searching the starter library…';$('sources').innerHTML='';try{const r=await fetch('/api/ask',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({question:q,stage:$('stage').value})});const d=await r.json();$('result').className='result'+(d.status==='urgent_language_detected'?' urgent':'');$('result').textContent=d.answer; $('sources').innerHTML=(d.sources||[]).map(s=>'<div class="resource"><a target="_blank" rel="noopener" href="'+s.url+'">'+escapeHtml(s.title)+'</a></div>').join('')}catch(e){$('result').textContent='Unable to reach the local server. Please try again.'}finally{$('ask').disabled=false}};
function readReminders(){try{return JSON.parse(localStorage.getItem('mam acare-reminders')||'[]')}catch(e){return []}}
function renderReminders(){const a=readReminders();$('reminders').innerHTML=a.length?a.sort((x,y)=>x.date.localeCompare(y.date)).map((x,i)=>'<div class="item"><span><strong>'+escapeHtml(x.title)+'</strong><br><small>'+escapeHtml(x.date)+'</small></span><button class="secondary" data-remove="'+i+'">Remove</button></div>').join(''):'<p>No reminders saved on this device.</p>'}
$('saveReminder').onclick=()=>{const title=$('reminderTitle').value.trim(),date=$('reminderDate').value;if(!title||!date){alert('Enter a reminder and date.');return}const a=readReminders();a.push({title,date});localStorage.setItem('mam acare-reminders',JSON.stringify(a));$('reminderTitle').value='';$('reminderDate').value='';renderReminders()};
$('reminders').onclick=e=>{const i=e.target.getAttribute('data-remove');if(i===null)return;const a=readReminders();a.splice(Number(i),1);localStorage.setItem('mam acare-reminders',JSON.stringify(a));renderReminders()};
loadArticles();renderReminders();
</script></body></html>'''

class Handler(BaseHTTPRequestHandler):
    server_version = "MamaCarePrototype/0.1"

    def headers(self, kind: str = "application/json; charset=utf-8") -> None:
        self.send_header("Content-Type", kind)
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("X-Frame-Options", "DENY")
        self.send_header("Referrer-Policy", "strict-origin-when-cross-origin")
        self.send_header("Cache-Control", "no-store")

    def respond(self, payload: Any, status: int = 200) -> None:
        raw = json.dumps(payload, ensure_ascii=False).encode()
        self.send_response(status)
        self.headers()
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def do_GET(self) -> None:
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            raw = PAGE.encode()
            self.send_response(200)
            self.headers("text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(raw)))
            self.end_headers()
            self.wfile.write(raw)
        elif path == "/api/health":
            self.respond({"status": "ok", "product": "MedMall MamaCare AI", "version": "0.1.0",
                          "ai_connected": False, "clinical_review": "pending",
                          "pilot_status": "not piloted"})
        elif path == "/api/articles":
            self.respond({"articles": [{"id": a["id"], "title": a["title"], "url": a["url"],
                                        "source": a["source"]} for a in ARTICLES]})
        else:
            self.respond({"error": "Not found"}, 404)

    def do_POST(self) -> None:
        if urlparse(self.path).path != "/api/ask":
            self.respond({"error": "Not found"}, 404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
        except ValueError:
            self.respond({"error": "Invalid request length"}, 400)
            return
        if length <= 0 or length > MAX_BODY:
            self.respond({"error": "Request body must be between 1 byte and 8 KB"}, 413)
            return
        try:
            body = json.loads(self.rfile.read(length).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError):
            self.respond({"error": "Invalid JSON"}, 400)
            return
        question = str(body.get("question", "")).strip()
        if not question or len(question) > 2000:
            self.respond({"error": "Enter a question of 1–2,000 characters"}, 400)
            return
        self.respond(answer_question(question, str(body.get("stage", "general"))))

    def log_message(self, fmt: str, *args: Any) -> None:
        if self.path.startswith("/api/ask"):
            return
        super().log_message(fmt, *args)

def main() -> None:
    server = ThreadingHTTPServer((HOST, PORT), Handler)
    print(f"MamaCare AI prototype running at http://{HOST}:{PORT}")
    print("Demonstration only; clinical review pending; do not use for medical decisions.")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()

if __name__ == "__main__":
    main()

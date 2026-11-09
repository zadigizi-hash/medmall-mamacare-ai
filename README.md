# MedMall MamaCare AI

Early-stage proof-of-concept for maternal-health information, continuity-of-care reminders, and safety-oriented referral navigation in Nigeria.

> **Development and safety status:** This is an early software prototype. It is not clinically validated, has not undergone a user pilot, and must not be used to diagnose, triage, or treat medical conditions. Clinical content and escalation rules require review and approval by appropriately qualified maternal-health professionals before any user-facing pilot.

## Prototype features

- Browser-based maternal-care interface.
- Local knowledge-base retrieval for selected maternal-health topics.
- Demonstration safety phrase detection and escalation messaging.
- Appointment/reminder planning stored locally in the user's browser.
- Python HTTP API and static web frontend.
- Automated tests for knowledge retrieval and safety rules.
- Optional model integration scaffold; no live model credentials are included.

## Run locally

Requirements: Python 3.10 or newer.

```bash
python -m venv .venv
# macOS/Linux
source .venv/bin/activate
# Windows PowerShell
# .venv\Scripts\Activate.ps1

pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:8000.

Run tests:

```bash
python -m unittest discover -s tests -v
```

## Project structure

- `app.py` — application server and API routes
- `mamacare/` — knowledge retrieval and safety demonstration logic
- `data/knowledge_base.json` — starter knowledge records (requires clinical review)
- `static/` — browser interface, styles and client-side behaviour
- `tests/` — automated tests
- `docs/CLINICAL_REVIEW_CHECKLIST.md` — clinical review requirements
- `docs/PILOT_READINESS.md` — pilot readiness checklist
- `SECURITY.md` — security reporting and data handling notes

## Before any pilot

1. Have a named, appropriately qualified maternal-health clinician review and approve every clinical content item and escalation pathway.
2. Conduct a documented clinical safety assessment and test urgent scenarios, false reassurance and out-of-scope requests.
3. Complete privacy impact assessment, consent wording, retention policy and security review.
4. Validate referral providers, contact details and service availability.
5. Obtain applicable ethics and regulatory approvals.
6. Conduct usability testing with informed consent and documented safeguarding arrangements.

## AI integration

The current default assistant uses local retrieval from the included starter knowledge base. The optional generative AI integration is not configured by default. Do not add API keys to source control. Use environment variables and review the model provider's data-processing terms before processing any sensitive information.

## Open-source

This repository is released under the MIT License. Clinical content may have separate source/licensing requirements; check attribution and permissions before reuse.

## Project contact

MedMall Digital Health Nigeria Ltd. — https://www.medmall.com.ng/

# MedMall MamaCare AI

An early-stage, locally runnable proof of concept for maternal-health information, care-continuity reminders, and safety-oriented referral navigation in Nigeria.

> **Development and safety status:** This repository contains a demonstration prototype only. MamaCare AI has not been clinically validated or piloted with users. The built-in educational content and phrase-matching safety rules are illustrative and require formal review and approval by appropriately qualified maternal-health professionals before any patient-facing pilot. This software must not be used to diagnose, triage, or treat medical conditions.

## What is included

- Browser-based maternal-care information experience served by the Python application.
- Source-linked starter information on antenatal care, postnatal care, selected warning signs and emotional wellbeing.
- Local retrieval of relevant starter information.
- Demonstration phrase detection that displays an urgent-care message for selected phrases. It is not a comprehensive triage engine.
- Appointment reminder planning saved in the user's browser.
- Python HTTP API with health and knowledge endpoints.
- No user accounts, electronic health records, live referral directory, SMS/email notification service or live AI model connection are configured.

## Run locally

Requirements: Python 3.10 or newer. The prototype uses Python's standard library.

```bash
python app.py
```

Open http://127.0.0.1:8000.

Optional configuration:

```bash
HOST=127.0.0.1 PORT=8000 python app.py
```

## API endpoints

- `GET /api/health` — reports prototype, AI and clinical-review status.
- `GET /api/articles` — returns starter information titles and source links.
- `POST /api/ask` — accepts JSON containing `question` and optional `stage`.

Example:

```bash
curl -X POST http://127.0.0.1:8000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"What should I discuss at an antenatal appointment?","stage":"pregnancy"}'
```

## Automated tests

The repository includes unit and local API tests. Run them with:

```bash
python -m unittest discover -s tests -v
```

A GitHub Actions workflow runs this test suite on pushes and pull requests to `main`. These software tests do not establish clinical accuracy, clinical safety, or pilot readiness.

## Clinical and safeguarding requirements before a pilot

1. Appoint a named, appropriately qualified maternal-health clinician to review every content item and escalation pathway against current Nigerian guidance and relevant WHO guidance.
2. Develop a clinician-reviewed test set covering routine, ambiguous, urgent and out-of-scope questions.
3. Evaluate false negatives, false reassurance, unsafe outputs, language variation and usability; document issues and corrective actions.
4. Complete privacy impact, security, consent, retention and incident-response reviews.
5. Validate actual referral providers, contact details, availability and emergency pathways for the pilot location.
6. Obtain required ethical, regulatory and safeguarding approvals before recruiting participants.
7. Define stop/go criteria and require clinical sign-off before participant-facing deployment.

See `docs/CLINICAL_REVIEW_CHECKLIST.md` and `docs/PILOT_READINESS.md`.

## Privacy and security

Do not enter real patient details or identifiable health information. Do not commit API keys, passwords, credentials or production data. Appointment reminders are stored in the browser's local storage on that device; they are not sent to a provider and are not synced to a server. See `SECURITY.md`.

## Open-source and content licensing

The source code is released under the MIT License. Starter clinical information links to external sources; source terms and attribution requirements should be checked before reuse. Clinical content is not approved for clinical use.

## Project

MedMall Digital Health Nigeria Ltd. — https://www.medmall.com.ng/

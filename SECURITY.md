# Security and data-handling notes

This repository is an early local demonstration, not a production deployment.

## Do not submit sensitive data
- Do not enter names, phone numbers, addresses, medical record numbers or identifiable patient details.
- Do not upload real patient records or clinical datasets to this repository.
- Do not commit API keys, passwords, tokens or production credentials.
- Appointment reminders are kept in the local browser storage of the device used; they are not encrypted, synchronized or sent to MedMall.

## Current technical limitations
- No user authentication or role-based access control.
- No server-side patient record storage.
- No encrypted clinical data store.
- No verified referral-provider directory.
- No production AI model is configured.
- The phrase-matching safety demonstration is incomplete and must not be used as a clinical triage system.

## Before production or pilot deployment
Complete a threat model, privacy impact assessment, security testing, secure hosting configuration, access-control design, incident-response process, data-retention policy, consent materials and independent review. Obtain applicable legal, regulatory and ethics advice.

## Reporting a vulnerability
Do not include patient data or secrets in a public issue. Contact MedMall through its verified organizational channel and provide a concise description and reproducible steps.

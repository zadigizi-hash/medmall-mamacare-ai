# Pilot readiness and evidence plan

## Current prototype status

- Browser experience: implemented for local demonstration.
- API: implemented using Python standard-library HTTP server.
- Maternal information: small source-linked starter library; MedMall clinical review is pending.
- Safety: illustrative phrase-matching only; not a comprehensive triage system.
- Reminders: saved to browser local storage; no SMS, email or push notifications.
- AI: no live generative AI provider is configured in this repository.
- Accounts, cloud sync, facility directory, payment, pharmacy orders, telemedicine booking and EHR integration: not implemented.
- Clinical pilot: not conducted.

## Minimum evidence before a controlled pilot

1. Functional tests for every intended workflow.
2. Clinician-reviewed evaluation set with version, expected response and expected safe action.
3. Sensitivity and false-negative analysis for critical warning-sign scenarios.
4. Accuracy, source-grounding and unsupported-answer assessment.
5. Usability testing with intended users, informed consent and safeguarding.
6. Accessibility and low-bandwidth testing.
7. Privacy impact assessment, threat model, retention policy and incident-response procedure.
8. Verified local referral directory and emergency instructions.
9. Ethics approval or formal determination, regulatory review and consent materials as applicable.
10. Documented clinical safety sign-off and stop/go acceptance criteria.

## Proposed engineering gates (targets, not achieved results)

- 100% correct escalation on a predefined critical-scenario test set before pilot sign-off.
- At least 95% of answers meeting clinician-defined acceptability and source-grounding criteria on an approved evaluation set.
- At least 80% successful completion of defined core tasks in usability testing.
- Document every safety failure and close or formally accept each issue before deployment.

These are proposed engineering gates, not clinical outcome claims. They must be confirmed by the clinical lead and evaluator. Passing software unit tests does not demonstrate clinical safety or effectiveness.

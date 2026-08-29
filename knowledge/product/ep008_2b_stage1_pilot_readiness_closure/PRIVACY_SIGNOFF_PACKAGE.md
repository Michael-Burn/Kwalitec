# EP-008.2B — Privacy Sign-Off Package (OR-01)

**Programme:** EP-008.2B — Stage 1 Pilot Readiness Closure  
**Date:** 2026-07-26  
**Status:** Package **COMPLETE** — Founder Reviews **SIGNED** (2026-07-26) — Stage 1 enrollment **HOLD** (OR-02 open)  
**Closes documentation for:** OR-01 (Privacy Review)  
**Does not:** Authorise Stage 1 invites until OR-02 dry-run / kill-switch evidence and enrollment clearance are complete  
**Governance:** GP-001 Founder Governance Model — `../gp001_founder_governance_model/`  
**Authorities:** Vision Data Principles · PRD-001 §7–§8 · EP-003 Private Beta Protocol §3 · `private_beta/PRIVACY_REVIEW.md` · EP-002 Privacy Operations Guide  

---



## 1. Purpose

Provide a single, Board-auditable privacy package for Stage 1 invite-only enrolment (5–10 external participants), so the Founder can complete Product Owner and Privacy Owner Founder Reviews — or explicitly refuse — before first invitation.

**Claim allowed:** Privacy documentation and operational controls for Stage 1 are assembled; Founder Reviews (Product Owner + Privacy Owner) are **SIGNED** (2026-07-26).  
**Claim forbidden:** “Stage 1 GO”; “GDPR certified”; “DPA complete for all jurisdictions”; “OR-02 closed” without §E evidence.

---



## 2. Scope of processing (Stage 1)


| Dimension                      | Scope                                                                                            |
| ------------------------------ | ------------------------------------------------------------------------------------------------ |
| Population                     | Invite-only external pilots `BETA-PIL-001`…`010` (+ Stage 0 internal remains separate)           |
| Purpose                        | Private-beta product validation and educational effectiveness measurement (directional M-series) |
| Legal / policy basis (product) | Invite-only account + presented privacy notice + measurement consent for KPI inclusion           |
| Not in purpose                 | Advertising, resale, opaque vendor profiling, marketing analytics, public registration           |
| Analytics flag                 | Remains **OFF** until Pilot go-live evidence + activation log (OR-02 / OR-06)                    |
| Educational algorithms         | Unchanged — analytics observe only                                                               |


**Jurisdiction posture:** Stage 1 prefers a **single primary privacy regime** (EP-007.3 / EP-004 cohort design). Multi-country DPA automation is **out of scope** and remains a Version 1 Commercial residual.

---



## 3. Data inventory



### 3.1 Account / identity (product domain — not analytics store)


| Field / class            | Example          | Lawful / product purpose                        | Stored where                                            | Stage 1 note                                      |
| ------------------------ | ---------------- | ----------------------------------------------- | ------------------------------------------------------- | ------------------------------------------------- |
| Email                    | login identity   | Authentication; invite delivery                 | User account (ORM)                                      | Ops map private; **never** in knowledge artefacts |
| Password hash            | credential       | Authentication                                  | User account                                            | Standard auth                                     |
| Display name (if any)    | optional         | Account UX                                      | User account                                            | Minimise                                          |
| Subject / exam proximity | CM2, exam window | Cohort eligibility; M8/M9 interpretation        | Ops store / registry fields (pseudonymous in knowledge) | Required for Stage 1 selection                    |
| Pseudonymous pilot ID    | `BETA-PIL-003`   | Research / scorecard linkage without PII in git | `BETA_COHORT.md` + private ops map                      | Knowledge = pseudonymous only                     |




### 3.2 Educational domain (learning product — existing)


| Class                            | Purpose                  | Analytics store?                                                  |
| -------------------------------- | ------------------------ | ----------------------------------------------------------------- |
| Session / mission / plan records | Deliver study experience | No — domain authority                                             |
| Reflection body text             | Learning reflection UX   | **Forbidden** in analytics events                                 |
| Educational State / Twin beliefs | Runtime A authorities    | **Forbidden** as analytics payload; hash+metadata only if emit ON |
| History / Home projections       | Student experience       | No third-party analytics                                          |




### 3.3 First-party learning analytics events (when `ANALYTICS_EVENTS_V1=true`)

Per PRD-001 §7.4 allowlist only. No page views, keystrokes, reflection free-text, or exam PII.


| Event                           | Fields (allowlist)                                                                                                  | Lawful / product purpose                                                   |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| `session.started`               | `event_id`, `event_type`, `user_id`, `session_id`, `mission_id`, `occurred_at`, `idempotency_key`, `schema_version` | Measure activation / starts (M-series support)                             |
| `session.completed`             | As started + `started_at`, `completion_status`                                                                      | Productive completion / duration derive (O2 / M4)                          |
| `reflection.completed`          | ids, `required_flag`, `quality_flag`, timestamps, schema — **no body**                                              | Reflection completion (M3) without content                                 |
| `journey.milestone_reached`     | journey/milestone ids + metadata                                                                                    | Progress engagement (M5; may stay provisional)                             |
| `educational_state.snapshot`    | snapshot id + `content_hash` + metadata                                                                             | Observe ESS change; **no ESS payload**                                     |
| `twin.evolved`                  | twin ids/version, `reason_code`, `content_hash`, metadata                                                           | Observe Twin evolution; **no Twin payload**                                |
| Observational commitment events | `commitment_confirmed` / `_deferred` / `_completed` (research)                                                      | Observational research only — **not** ranking / readiness / Twin authority |




### 3.4 Support / research / ops


| Class                      | Purpose                                | Retention / handling                                                |
| -------------------------- | -------------------------------------- | ------------------------------------------------------------------- |
| Support tickets            | P0–P3 triage                           | Minimise PII; tag `private-beta`                                    |
| Check-in / interview notes | Qualitative research                   | Interview + quote consent gates; coded themes in knowledge (no PII) |
| Consent capture log        | Measurement / interview / quote        | Ops store; registry status only in knowledge                        |
| Analytics audit log        | Deletion, export, purge, emit failures | **36 months** (PRD-001 §9)                                          |




### 3.5 Explicitly not collected (Stage 1)

- Third-party analytics SDKs / advertising IDs  
- Reflection free-text in analytics tables  
- Exam results / pass-fail as analytics fields  
- Public self-registration profiles  
- Marketing email tracking pixels

---



## 4. Lawful purpose summary (per collection class)


| Collection class           | Purpose                             | Basis (product posture)                   | KPI use                                       |
| -------------------------- | ----------------------------------- | ----------------------------------------- | --------------------------------------------- |
| Account identity           | Provide invite-only study access    | Contract / invite relationship + notice   | Not in M numerators                           |
| Educational domain records | Deliver learning product            | Same                                      | Domain truth for study                        |
| Analytics events (flag ON) | Product validation / release health | Invite-only + privacy notice (PRD-001 §8) | Supports M when consented                     |
| Measurement aggregates     | Effectiveness directional evidence  | Separate **measurement consent**          | M1–M9 numerators                              |
| Interview themes           | Qualitative validation              | Optional **interview consent**            | Q-coded support                               |
| Anonymous quotes           | Internal reports only               | Optional **quote consent**                | Never public marketing without further review |


**Purpose limitation:** No advertising, resale, or opaque vendor profiling. `flask analytics-verify-consent --marketing-use` must **deny**.

---



## 5. Consent wording (Stage 1 — operator script)

Use calm, honest language. Do **not** promise pass rates or “exam ready.”

### 5.1 Privacy notice acknowledgement (required for external study access)

> I have read the Kwalitec Stage 1 Privacy Notice. I understand that Kwalitec is an invite-only study companion; that my account and study records are stored to provide the product; and that first-party learning analytics (metadata and cryptographic hashes — not my reflection text) may be collected for product validation when analytics are enabled. I understand I can request export or deletion as described in the notice.



### 5.2 Measurement consent (required for KPI numerators)

> I agree that Kwalitec may include my study activity in aggregate educational metrics (for example weekly active study, session completion, consistency) and anonymised interview themes to improve the product. I can withdraw this measurement consent and still keep studying; after withdrawal I will be excluded from metric numerators. Withdrawal does not by itself delete my account unless I also request deletion.



### 5.3 Interview consent (optional)

> I optionally agree to a short (~30 minute) structured interview about my experience. Declining does not remove my study access.



### 5.4 Quote consent (optional, separate)

> I optionally agree that anonymous quotes from my interview or feedback may appear in internal product reports. Quotes will not be published publicly without a further request. Declining does not remove study access or interview participation (if interview consented).



### 5.5 Withdrawal script (operator)

> You can withdraw measurement consent at any time by contacting support. You may still study. If you want your analytics events deleted, or a copy of your analytics export, say so and we will follow the export (≤14 days) / delete (≤30 days) path.

---



## 6. Participant information sheet (Stage 1)

**Title:** Kwalitec Stage 1 Private Pilot — Participant Information  

**What is this?**  
A small invite-only pilot (about 5–10 students) of Kwalitec, a study companion for professional exam preparation (IFoA in-scope subjects). This is **not** a public launch.

**What will I do?**  
Log in with your invite account, complete any in-product onboarding/calibration, use Home and Today’s Session, complete Sessions and Reflections when prompted, and optionally join check-ins / a short interview.

**What is being studied?**  
Whether the product helps you study in a clear, honest way — activation, consistency, session completion, reflection usefulness, and trust in recommendations. We do **not** claim the pilot proves exam pass rates.

**What data is used?**  
Account data needed to log in; study records needed to run the product; and, when analytics are on, first-party event metadata and hashes (not reflection body text). See Privacy Notice.

**Risks:**  
Software bugs may occur. Educational guidance is deterministic and explainable where shipped, but may still feel incomplete (orientation gaps). Support is founder-operated for this small pilot.

**Benefits:**  
Early access to the study companion; ability to give feedback that shapes the product; clear export/delete rights for analytics data.

**Voluntary:**  
Participation is voluntary. You may stop studying, withdraw measurement consent, or request deletion. Declining interview/quote consent does not remove study access.

**Contact:**  
Support channel named in your invite pack (P0 security / data = immediate; P1 cannot-study = same day).

---



## 7. Privacy notice (finalized Stage 1 text — attach to invites)

**Kwalitec Stage 1 Privacy Notice**  
**Version:** 2026-07-26 · **Audience:** Invite-only Stage 1 pilot participants  

### Who we are

Kwalitec provides an invite-only exam-focused study companion for professional exam preparation. There is **no public self-registration** for this pilot.

### What we store

1. **Account data** — email and credentials needed to authenticate your invite account.
2. **Study data** — sessions, plans, progress, and reflections as needed to provide the learning product. Reflection text is part of your study experience; it is **not** copied into the analytics event store.
3. **First-party learning analytics** (only when the analytics feature is enabled on the pilot environment) — structured event metadata such as session start/completion identifiers and timestamps, reflection *completion* flags (not reflection body), journey milestone identifiers, and cryptographic hashes of educational/twin snapshots. Hashes are not reversible to Twin beliefs or Educational State payloads.
4. **Support and research notes** — if you contact support or consent to interview, notes needed to help you or improve the product (minimised).



### Why we process data

To provide the study product, support you during the pilot, validate product health, and (with measurement consent) compute aggregate educational metrics for product decisions. We do **not** use this data for advertising, resale, or third-party advertising profiles. No third-party analytics SDK is used for Stage 1.

### Retention

- Analytics raw events: up to **18 months** from event time, or until account/analytics deletion (whichever sooner).  
- Analytics audit log (operational): up to **36 months**.  
- Educational account/study data: retained while your account is active; deletion follows support/account workflow plus analytics cascade when requested.



### Your choices

- **Measurement consent** — required for inclusion in aggregate KPI numerators; withdrawable while keeping study access.  
- **Interview / quote consent** — optional.  
- **Export** — request a JSON export of your analytics events (beta SLA: **14 days**).  
- **Delete analytics** — request cascade deletion of analytics events/outbox for your user (beta SLA: **30 days** after verified request).  
- **Full withdrawal** — leave the product; ops follow export/delete as applicable.



### Who can access

Authenticated system writes for events. Raw analytics read: you (via export) or Founder/Admin with console capability for support/compliance. Cohort aggregates: Founder/Admin only. Operators are trained not to share your educational data broadly in chat/email threads.

### Contact for privacy requests

Use the support channel in your invite pack. Identity will be verified before export/delete.

### Changes

Expanding beyond invite-only Stage 1, adding countries/jurisdictions, or enabling marketing use requires an updated Privacy Review and notice.

---



## 8. Data retention schedule


| Data class                                           | Retention                                                   | Enforcement                                                      |
| ---------------------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------- |
| Analytics raw events / snapshots / twin evolved rows | **18 months** from `occurred_at`, or earlier on deletion    | `flask analytics-retention --execute` (daily when Pilot flag ON) |
| User-keyed analytics aggregates                      | Per PRD / delete cascade                                    | Delete path + retention job                                      |
| Analytics audit log                                  | **36 months**                                               | Documented; purge not fully automated in EP-002                  |
| Consent / privacy request tickets                    | Per support practice; enough to evidence fulfilment         | Support tracker                                                  |
| Interview notes (consented)                          | Pilot research window + Board evidence needs; minimise      | Ops store; coded themes may enter knowledge without PII          |
| Account / educational domain                         | While account active; deletion via account/support workflow | Existing support path + analytics cascade                        |


---



## 9. Export process


| Step | Action                                                                  | Owner            |
| ---- | ----------------------------------------------------------------------- | ---------------- |
| 1    | Receive request via support; verify identity                            | Beta operator    |
| 2    | Confirm requester is the account holder (or authorised)                 | Export SLA owner |
| 3    | `flask analytics-export-user <user_id> --output student.json`           | Export SLA owner |
| 4    | Deliver securely; **do not** include other users; do not reverse hashes | Export SLA owner |
| 5    | Record fulfilment (ticket + optional audit)                             | Export SLA owner |
| 6    | Optional: `flask analytics-export-audit` for security investigations    | Security / ops   |


**SLA (beta):** ≤ **14 days**. Guide: `../analytics/ep002/PRIVACY_OPERATIONS_GUIDE.md`.

**Aggregate research packs** (Board/measurement) follow EP-008.2A `DATA_COLLECTION_PLAN.md` §6 — pseudonymous; separate from per-student export.

---



## 10. Deletion process


| Step | Action                                                                                 | Owner              |
| ---- | -------------------------------------------------------------------------------------- | ------------------ |
| 1    | Receive verified deletion / analytics-delete request                                   | Beta operator      |
| 2    | Confirm scope: analytics-only vs full account withdrawal                               | Deletion SLA owner |
| 3    | `flask analytics-delete-user <user_id> --yes --requested-by support`                   | Deletion SLA owner |
| 4    | Confirm audit action `analytics.user_deleted`                                          | Deletion SLA owner |
| 5    | Educational domain deletion via existing account/support workflow (not redefined here) | Beta operator      |
| 6    | If measurement-only withdrawal: exclude from KPI numerators; study may continue        | Beta operator      |


**SLA (beta):** ≤ **30 days** for analytics cascade after verified request.  
**Scheduled purge:** retention cron when Pilot analytics ON.

---



## 11. Named operational owners (Stage 1 designation)

Role designations for Stage 1 N≤10 (founder-operated accepted under invite-only / PR-015). **Names must be confirmed on the activation / Rollout log before first invite — blank confirmation ≠ signed Privacy Review.**


| Role                                            | Designated role holder        | Confirmation on activation log          |
| ----------------------------------------------- | ----------------------------- | --------------------------------------- |
| Beta operator / triage (P0–P3)                  | Founder / Product             | Required before invites                 |
| Export SLA owner (≤14 days)                     | Founder / Product             | Required before Pilot ON / first invite |
| Deletion SLA owner (≤30 days)                   | Founder / Product             | Required before Pilot ON / first invite |
| Analytics kill-switch on-call                   | Founder / Product (same rota) | Required before Pilot ON                |
| Privacy Review — Founder Review (Product Owner) | **Signed** — Courage T Shumba (2026-07-26) | Recorded in §14 |
| Privacy Review — Founder Review (Privacy Owner) | **Signed** — Courage T Shumba (2026-07-26) | Recorded in §14 |


---



## 12. Privacy Review checklist (executable)

Maps to `../private_beta/PRIVACY_REVIEW.md` and closes OR-01. Checklist rows 1–13 mean **documented / verified in repo**. Founder Reviews are recorded in §14 (SIGNED 2026-07-26).


| #   | Item                                                            | Doc status                       | Evidence                                               |
| --- | --------------------------------------------------------------- | -------------------------------- | ------------------------------------------------------ |
| 1   | No public registration; invite-only                             | **Ready**                        | Auth posture; DR-034; cohort design                    |
| 2   | Auth cookies / HTTPS / production `SECRET_KEY` validated        | **Ready (ops verify at deploy)** | Factory validation; Stage 0 posture                    |
| 3   | Support access minimised / logged where feasible                | **Ready**                        | Support workflow; audit export                         |
| 4   | Feedback storage excludes unnecessary PII                       | **Ready**                        | Protocol; feedback system                              |
| 5   | Analytics follows Product Analytics Architecture; no new vendor | **Ready**                        | PRD-001; first-party only                              |
| 6   | Export/delete path documented                                   | **Ready**                        | This package §§9–10; Privacy Ops Guide                 |
| 7   | CSP / third-party scripts reviewed for beta                     | **Ready with residual**          | G10 / PR-023 accepted residual for Stage 1 claim class |
| 8   | Operators trained not to share student educational data broadly | **Ready**                        | Operator rule in this package + runbook                |
| 9   | Privacy notice text reviewed for honesty                        | **Ready**                        | §7 finalized text                                      |
| 10  | Data inventory + purpose per field                              | **Ready**                        | §§3–4                                                  |
| 11  | Consent wording + participant sheet                             | **Ready**                        | §§5–6                                                  |
| 12  | Retention schedule                                              | **Ready**                        | §8                                                     |
| 13  | Named owners designated                                         | **Ready (confirmation open)**    | §11                                                    |




### Open items (do not guess)


| Item                                    | Status                                                                                                   |
| --------------------------------------- | -------------------------------------------------------------------------------------------------------- |
| Formal multi-country DPA programme      | **Deferred** — not required to start single-regime Stage 1; required before multi-jurisdiction expansion |
| Automated self-serve export UI          | **Deferred** — manual CLI fulfilment accepted for beta                                                   |
| Founder Review — Product Owner capacity | **SIGNED** — Courage T Shumba · 2026-07-26 · Approve (§14 S1) |
| Founder Review — Privacy Owner capacity | **SIGNED** — Courage T Shumba · 2026-07-26 · Approve (§14 S2) |


---



## 13. External / additional approvals required


| Approval                                                                 | Required to close OR-01?                                                                                                                                                                                                                                | Notes                                                           |
| ------------------------------------------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- |
| **Founder Review — Product Owner** on this package / `PRIVACY_REVIEW.md` | **Yes — SIGNED** (Courage T Shumba · 2026-07-26 · Approve) | See §14 S1 / OR-01 product accuracy |
| **Founder Review — Privacy Owner**                                       | **Yes — SIGNED** (Courage T Shumba · 2026-07-26 · Approve) | See §14 S2 / OR-01 participant protection |
| External legal counsel / DPO sign-off                                    | **Not mandatory for package completeness** if Founder accepts Stage 1 single-regime invite-only risk under both capacities; **recommended** if privacy competence is insufficient or processing expands (new country, marketing, third-party processor) |                                                                 |
| Data Protection Authority filing                                         | **Not claimed / not performed by this programme**                                                                                                                                                                                                       | Jurisdiction-dependent; do not invent                           |
| Participant signatures / acks                                            | **Required per invitee before measurement inclusion**                                                                                                                                                                                                   | Captured in ops consent log (OR-04) — not git                   |


Founder Review rows below are filled with Approve (2026-07-26). **OR-01 Founder Review layer is SIGNED.** Stage 1 enrollment remains **HOLD** until OR-02 evidence and enrollment clearance.

---



## 14. Founder Review checklist (human — SIGNED 2026-07-26)


| #   | Gate                                                       | Capacity         | Reviewer         | Date         | Decision | Notes |
| --- | ---------------------------------------------------------- | ---------------- | ---------------- | ------------ | -------- | ----- |
| S1  | Privacy package accurate for Stage 1                       | Product Owner    | Courage T Shumba | 26 July 2026 | Approve  |       |
| S2  | Privacy / security controls adequate for invite-only pilot | Privacy Owner    | Courage T Shumba | 26 July 2026 | Approve  |       |
| S3  | Privacy notice §7 attached to invite pack                  | Product Owner    | Courage T Shumba | 26 July 2026 | Confirm  |       |
| S4  | Export / delete owners confirmed                           | Operations Owner | Courage T Shumba | 26 July 2026 | Confirm  |       |
| S5  | No marketing / third-party analytics in Stage 1            | Product Owner    | Courage T Shumba | 26 July 2026 | Confirm  |       |


**Master record also mirrored in:** `../private_beta/PRIVACY_REVIEW.md` (Founder Review table).  
**Authority:** `../gp001_founder_governance_model/UPDATED_APPROVAL_MATRIX.md`


| Founder Review                 | Reviewer         | Date         | Capacity      | Decision | Notes |
| ------------------------------ | ---------------- | ------------ | ------------- | -------- | ----- |
| OR-01 — product accuracy       | Courage T Shumba | 26 July 2026 | Product Owner | Approve  |       |
| OR-01 — participant protection | Courage T Shumba | 26 July 2026 | Privacy Owner | Approve  |       |


---



## 15. OR-01 closure status


| Layer                                           | Status                                                               |
| ----------------------------------------------- | -------------------------------------------------------------------- |
| Documentation package                           | **COMPLETE**                                                         |
| Founder Reviews (Product Owner + Privacy Owner) | **SIGNED** (2026-07-26)                                              |
| Enrollment implication                          | **HOLD** — do not invite until OR-02 evidence / enrollment clearance |


**Successor action:** OR-01 Founder Reviews signed. Next: complete OR-02 dry-runs and kill-switch rehearsal (`GO_LIVE_CHECKLIST.md` §E); confirm owners on activation log; choose C1/C2; then enrollment clearance before any external invite.

---

**End of PRIVACY_SIGNOFF_PACKAGE**
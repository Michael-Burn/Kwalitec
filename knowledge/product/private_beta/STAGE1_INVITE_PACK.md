# Stage 1 Invite Pack (OR-03)

**Programme:** EP-008.2B / EP-004 Stage 1  
**Version:** 2026-07-26  
**Status:** **READY TO SEND** — assemble per invite; do not put emails/names in git  
**Canonical privacy text:** [`../ep008_2b_stage1_pilot_readiness_closure/PRIVACY_SIGNOFF_PACKAGE.md`](../ep008_2b_stage1_pilot_readiness_closure/PRIVACY_SIGNOFF_PACKAGE.md) §§5–7  
**Onboarding outline:** [`BETA_ONBOARDING.md`](BETA_ONBOARDING.md)  
**Support:** [`SUPPORT_WORKFLOW.md`](SUPPORT_WORKFLOW.md) · [`ISSUE_REPORTING.md`](ISSUE_REPORTING.md)  
**Closes documentation for:** OR-03 (notice attached to invite pack artefact)  
**Does not:** Send invites; fill enrollment clearance; enable analytics  

---

## 1. How to use (operator)

For each `BETA-PIL-00N` invitee:

1. Provision invite-only account (admin / controlled creation).  
2. Copy **§2–§7** below into the invite email (or secure attachment).  
3. Fill **Support channel** with the live reply address / link for this send.  
4. Capture consents in the **ops consent log** (template: [`../ep008_2b_stage1_pilot_readiness_closure/CONSENT_CAPTURE_LOG_TEMPLATE.md`](../ep008_2b_stage1_pilot_readiness_closure/CONSENT_CAPTURE_LOG_TEMPLATE.md)) — **not** in git.  
5. Update [`../ep004_private_beta/BETA_COHORT.md`](../ep004_private_beta/BETA_COHORT.md) with pseudonymous status only.  
6. Send only after enrollment clearance (Stage 1 checklist §B + Rollout Go).

---

## 2. Welcome note

Hello,

You are invited to a **small, invite-only Stage 1 pilot** of **Kwalitec** — an exam-focused study companion for professional exam preparation (IFoA in-scope subjects).

Kwalitec is built to help you study with clarity and honesty. The north star is learning that supports exam readiness over time — **not** a question bank, gamification app, or a promise of pass rates.

**What to do first**

1. Log in with the account credentials in this invite.  
2. Complete any in-product onboarding / calibration.  
3. Start **Today’s Session** from Home.  
4. Use Journey, History, Revision, and Reflection when prompted.  

Bugs may occur in a pilot. Prefer honest feedback over polish. See support details below.

---

## 3. Support channel (fill per send)

| Item | Value |
|---|---|
| Support contact | _[operator: reply-to email or private channel]_ |
| P0 Security / data | Immediate |
| P1 Cannot study | Same day |
| How to report | Reply to this invite **or** use the linked issue/feedback path in-product / ops pack |
| Tag | `private-beta` |

Operators: do not share student educational data broadly in chat/email threads.

---

## 4. Participant information sheet

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
Support channel named in this invite pack (P0 security / data = immediate; P1 cannot-study = same day).

---

## 5. Privacy notice (OR-03 — finalized text attached)

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

## 6. Consent requests (reply or ops form)

Please reply to this invite (or complete the ops form) with **Yes / No** for each:

### 6.1 Privacy notice acknowledgement — **required** for study access

> I have read the Kwalitec Stage 1 Privacy Notice. I understand that Kwalitec is an invite-only study companion; that my account and study records are stored to provide the product; and that first-party learning analytics (metadata and cryptographic hashes — not my reflection text) may be collected for product validation when analytics are enabled. I understand I can request export or deletion as described in the notice.

**Your answer:** Yes / No  

### 6.2 Measurement consent — **required** for KPI numerators

> I agree that Kwalitec may include my study activity in aggregate educational metrics (for example weekly active study, session completion, consistency) and anonymised interview themes to improve the product. I can withdraw this measurement consent and still keep studying; after withdrawal I will be excluded from metric numerators. Withdrawal does not by itself delete my account unless I also request deletion.

**Your answer:** Yes / No  

### 6.3 Interview consent — **optional**

> I optionally agree to a short (~30 minute) structured interview about my experience. Declining does not remove my study access.

**Your answer:** Yes / No / Prefer not  

### 6.4 Quote consent — **optional**

> I optionally agree that anonymous quotes from my interview or feedback may appear in internal product reports. Quotes will not be published publicly without a further request. Declining does not remove study access or interview participation (if interview consented).

**Your answer:** Yes / No / Prefer not  

### 6.5 Withdrawal (for later — operator script)

> You can withdraw measurement consent at any time by contacting support. You may still study. If you want your analytics events deleted, or a copy of your analytics export, say so and we will follow the export (≤14 days) / delete (≤30 days) path.

---

## 7. Operator checklist (per invite)

- [ ] Pseudonymous ID assigned (`BETA-PIL-00N`)  
- [ ] Account provisioned (invite-only)  
- [ ] Support channel filled in §3  
- [ ] §§2–6 included in send  
- [ ] Consent answers logged in **ops store** (not git)  
- [ ] `BETA_COHORT.md` Consent / Onboarding columns updated (pseudonymous only)  
- [ ] Enrollment clearance already filed before first send  

---

## 8. OR-03 closure record

| Field | Value |
|---|---|
| Artefact | This invite pack (`private_beta/STAGE1_INVITE_PACK.md`) |
| Privacy notice source | Privacy Sign-off Package §7 (verbatim) |
| Attached | **Yes** — §5 of this pack |
| Date | 2026-07-26 |
| Operator | Courage T Shumba |
| First external send | **Authorized** under Stage 1 Go (C2) — execute after OR-07 candidate selection |

---

**End of STAGE1_INVITE_PACK**

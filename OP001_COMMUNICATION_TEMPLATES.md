# OP-001 — Communication Templates

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `STAGE1_INVITE_PACK.md` · Privacy Review (OR-01) · claim discipline (no marketing / pass guarantees)

**Templates only.** Replace bracketed fields in the ops mailer. Do **not** commit filled emails with recipient PII to git. Attach or link Stage 1 Privacy Notice + consent prompts from the invite pack when sending invitations.

---

## Global copy rules

- Name the product **Kwalitec** clearly.  
- State invite-only Early Access / closed pilot — **not** a public launch.  
- **No** exam pass-rate promises; **no** “Version 1 released” / production-ready claims.  
- Bugs may occur; honest feedback is welcome.  
- Support SLAs: security/privacy immediate; cannot-study same business day.

---

## 1. Invitation email

**Subject:** Invitation to Kwalitec Early Access (closed pilot)

```text
Hello [FIRST_NAME],

You are invited to a small, invite-only Early Access pilot of Kwalitec — a study companion for professional exam preparation.

This is not a public launch. Participation is voluntary.

What Kwalitec is for
Kwalitec is built to help you study with clarity and honesty. It is a learning companion for exam preparation over time — not a question bank, not a gamification app, and not a promise of pass rates.

How to start
1. Log in with the account details below (or the secure link provided).
2. Complete any in-product onboarding or calibration you are shown.
3. Open Home and start Today’s Session when you are ready to study.

Account
- Login URL: [LOGIN_URL]
- Email / username: [ACCOUNT_EMAIL]
- Temporary password: [TEMP_PASSWORD]  (please change after first login)

Privacy and consent
Please read the Privacy Notice in this email / attachment. Reply with Yes/No to the consent prompts (privacy acknowledgement and measurement consent are required before we include your activity in aggregate study metrics). Interview and quote consent are optional and do not affect your access.

Support
Reply to this email. Security or data issues: treat as urgent — we respond immediately. If you cannot study (login or session broken): same business day.

Expectations
Bugs may occur. Prefer honest feedback over polish. There is no guarantee of exam results.

If you accept, reply “I accept” (or complete the ops form) and log in within a few days.

Thank you,
[OPERATOR_NAME]
Kwalitec Early Access
```

Include Stage 1 Privacy Notice + consent Yes/No block from `STAGE1_INVITE_PACK.md` §5–§6 (or equivalent current pack) when sending.

---

## 2. Reminder email

**Subject:** Reminder — Kwalitec Early Access invitation

```text
Hello [FIRST_NAME],

This is a short reminder about your invitation to the Kwalitec Early Access pilot.

We have not yet recorded your acceptance / first login.

If you still wish to join:
1. Reply “I accept” if you have not already.
2. Log in: [LOGIN_URL]
3. Complete onboarding and try Today’s Session when ready.

If this is no longer a good time, reply “decline” — no problem at all.

Support: reply to this email.

Thank you,
[OPERATOR_NAME]
Kwalitec Early Access
```

Use for: invite not accepted, or accepted but never-activated approaching day 7.

---

## 3. Acceptance email

**Subject:** You’re in — Kwalitec Early Access

```text
Hello [FIRST_NAME],

Thank you — we have recorded your acceptance for the Kwalitec Early Access pilot ([PSEUDONYMOUS_ID]).

Next steps
1. Log in if you have not already: [LOGIN_URL]
2. Complete any onboarding / calibration prompts.
3. Start Today’s Session from Home when you are ready to study.
4. Keep an eye on Reflections when the product asks for them.

Consents on file (ops)
- Privacy acknowledgement: [YES/NO]
- Measurement consent: [YES/NO]
- Interview consent (optional): [YES/NO/PENDING]
- Quote consent (optional): [YES/NO/PENDING]

If any consent is still pending, please reply so we can complete it. Measurement consent is required before inclusion in aggregate metrics; you can withdraw later and still keep studying.

Support: reply to this email (cannot-study = same business day; security/privacy = immediate).

Welcome,
[OPERATOR_NAME]
Kwalitec Early Access
```

---

## 4. Welcome email

**Subject:** Welcome to Kwalitec Early Access — orientation

```text
Hello [FIRST_NAME],

Welcome. Here is a short orientation for Early Access.

What to do first
- Log in and finish any in-product onboarding.
- Use Home to see what to do now.
- Start Today’s Session and complete a Session when you can.
- Use Reflection when prompted.

What this pilot is
A closed study companion pilot for professional exam preparation. Packages for this wave are stable. We are observing real study use — we are not asking you to “perform” for metrics.

What we will not claim
We do not guarantee exam passes. This is not a public marketing launch.

How to get help
Reply to this email. Tell us what you tried, what you expected, and what happened.

Optional later
Around week 4 of your personal start, we may invite you to a ~30-minute structured interview. Declining the interview does not remove your access.

Thank you for studying with us,
[OPERATOR_NAME]
Kwalitec Early Access
```

---

## 5. Interview invitation

**Subject:** Optional interview — Kwalitec Early Access (~30 minutes)

```text
Hello [FIRST_NAME],

Thank you for taking part in Kwalitec Early Access.

We would like to invite you to an optional ~30-minute structured conversation about how you have been studying with the product. This helps us understand usefulness honestly — including what we should not claim.

- Mode: [CALL_OR_EQUIVALENT]
- Proposed times: [TIME_OPTIONS]
- Recording: only with your explicit consent (optional)

Interview consent on file: [YES/NO/PLEASE CONFIRM]

You may decline without losing access. If you prefer written answers instead of a call, say so.

To schedule, reply with a time that works or “decline”.

Thank you,
[OPERATOR_NAME]
Kwalitec Early Access
```

Interview questions follow KSI-002 fixed instrument (operator uses protocol; do not paste leading probes into student email).

---

## 6. Completion thank-you

**Subject:** Thank you — Kwalitec Early Access

```text
Hello [FIRST_NAME],

Thank you for completing the planned Early Access / observation window with Kwalitec.

Your time and honest feedback matter. This pilot does not guarantee exam outcomes; it exists to learn whether the companion helps real study.

If you have anything we should not claim based on your experience, you are welcome to reply — including after any interview.

Optional: if interview is still open and you consented, we will confirm scheduling separately.

With appreciation,
[OPERATOR_NAME]
Kwalitec Early Access
```

---

## 7. Withdrawal acknowledgement

**Subject:** Withdrawal confirmed — Kwalitec Early Access

```text
Hello [FIRST_NAME],

This confirms we have recorded your withdrawal from Kwalitec Early Access as:

Type: [MEASUREMENT_ONLY / FULL_STUDY_OR_ACCOUNT / OTHER]
Effective: [ISO_DATE]

What this means
- [MEASUREMENT_ONLY: You may keep studying; you will be excluded from aggregate metric numerators going forward.]
- [FULL: Access will be closed / account handled per your request; data handling follows our Privacy Notice.]
- Interview/quote-only withdrawal does not remove study access.

If you also want data export or deletion, reply with that request. We verify identity before fulfilling privacy requests (export target 14 days; analytics deletion target 30 days after verified request).

Thank you for your time,
[OPERATOR_NAME]
Kwalitec Early Access
```

---

## 8. Optional light week check-in (not mandated by brief; available)

**Subject:** Kwalitec Early Access — quick check-in

```text
Hello [FIRST_NAME],

Quick check-in only — no need for a long reply.

Are you able to study with Kwalitec this week? Anything blocking you (login, confusion, bugs)?

Reply with a sentence, or ignore if all is fine.

Thanks,
[OPERATOR_NAME]
```

---

## STOP

Do not send templates to external participants until Founder authorises invitations.

Signed: OP-001 Communication Templates · 2026-08-04

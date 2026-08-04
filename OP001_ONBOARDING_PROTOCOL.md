# OP-001 — Onboarding Protocol

**Programme:** OP-001 — Early Access Operations  
**Version:** 1.0  
**Status:** OPERATIONAL PACKAGE COMPLETE — AWAITING FOUNDER APPROVAL  
**Effective:** 2026-08-04  
**Authority:** `OP001_EARLY_ACCESS_PLAN.md` · `KSI002_PARTICIPANT_PROTOCOL.md` · `BETA_ONBOARDING.md` · `STAGE1_INVITE_PACK.md` · Privacy Review (OR-01)

**Defines ops onboarding.** Does not redesign in-product UX. Uses existing student onboarding / Home / Session surfaces as-is.

---

## 1. Purpose

Ensure every accepted Early Access participant can: create/receive an account, complete first login, understand what to do next, know how to get support, and pass **consent checkpoints** before KPI inclusion.

**Ops success of onboarding:** ≥1 productive Session within **7 days** of invite acceptance (KSI-002 never-activated definition).

---

## 2. Preconditions (before first invite of the wave)

| Check | Required |
|-------|----------|
| Founder approval of OP-001 package | Yes |
| Founder authorisation to **send invites** | Yes (separate) |
| Privacy Review signed (OR-01) | Yes |
| Support channel live | Yes |
| Consent capture log ready (ops store) | Yes |
| Communication templates ready | Yes |
| Dashboard counting definitions understood | Yes |

---

## 3. Account creation

1. Operator creates **invite-only** student account via approved admin / controlled provisioning path.  
2. Assign pseudonymous study ID; map ID ↔ account only in ops store.  
3. Generate temporary credentials or invite link per existing admin practice — **never** commit credentials to git.  
4. Record dashboard state **Invited** when invite email is sent (not when account is merely provisioned).  
5. If provisioning fails: log as ops defect; do **not** count toward accepted N.

**Out of scope:** Public registration, self-serve signup funnels, OAuth marketing flows.

---

## 4. First login

1. Participant receives invitation email (`OP001_COMMUNICATION_TEMPLATES.md` — Invitation).  
2. Participant signs in with provided credentials.  
3. If login fails: treat as **P1** support (`OP001_STUDENT_SUPPORT_PROTOCOL.md`); do not blame the student.  
4. On success, operator may mark ops note “first login observed” (manual); dashboard **Activated** is reserved for productive Session (see §8).  
5. Encourage password change if temporary credentials were used (security hygiene — existing product behaviour).

---

## 5. Welcome flow (ops)

Send **Welcome email** after acceptance / first successful login (whichever Founder ops chooses as trigger — default: on acceptance reply + confirmed account access).

Welcome must include:

- Purpose of Early Access (closed pilot; not public launch)  
- What Kwalitec is / is not (study companion; **no** pass guarantee)  
- First actions: complete any in-product onboarding/calibration; open Home; start Today’s Session  
- Support contact and bug-reporting path  
- Reminder of consent status and how to withdraw  
- Link or pointer to study expectations (§7)

**Do not** redesign the in-app welcome UX in this programme.

---

## 6. Orientation (checklist for participant)

Operator shares this checklist (email or short call). Participant ticks as they go:

| Step | Action |
|------|--------|
| 1 | Log in successfully |
| 2 | Complete in-product onboarding / subject calibration if prompted |
| 3 | Find **Home** — what to do now |
| 4 | Start **Today’s Session** (or equivalent primary study action) |
| 5 | Complete at least one Session when ready |
| 6 | Complete Reflection when prompted |
| 7 | Note where Journey / Progress / History live (existing surfaces) |
| 8 | Know how to contact support |

Orientation is **ops guidance**, not a new product feature.

---

## 7. Study expectations

| Topic | Expectation |
|-------|-------------|
| Cadence | Ordinary personal study rhythm; consistency valued over activity vanity |
| Duration | ≥4 weeks of use preferred for later study evaluation |
| Honesty | Prefer reporting confusion over pretending understanding |
| Bugs | Expected in Early Access; report via support protocol |
| Interviews | Optional ~week 4 structured interview per KSI-002 instrument |
| Claims | No marketing pass-rate language; packages frozen for this wave |
| Metrics | Measurement consent required for inclusion in aggregate KPIs |

---

## 8. Dashboard state transitions (onboarding-related)

| State | Definition (ops) |
|-------|------------------|
| Invited | Invite email sent |
| Accepted | Participant accepts invite + account reachable (acceptance timestamp) |
| Activated | ≥1 productive Session completed after acceptance |
| Never-activated | Accepted but no productive Session within **7 days** — chase per checklist |
| Withdrawn | Consent/study/account withdrawal logged |

Week 1–4 and Completed are **cohort timeline** states — see `OP001_OPERATIONS_DASHBOARD.md`.

---

## 9. Support contacts

| Contact | Use |
|---------|-----|
| Primary Early Access support channel | Named in invite/welcome (email or Founder-designated inbox) |
| P0 security / privacy | Immediate escalation to Founder |
| Do not use | Public social DMs as official support of record |

Exact addresses live in ops store / invite pack — **not** hard-coded with personal emails in this protocol if avoidable; use role labels in git docs.

---

## 10. Consent checkpoints

| Checkpoint | When | Required for |
|------------|------|----------------|
| **C1 Privacy notice acknowledgement** | Before or at invite acceptance | Any external participation |
| **C2 Measurement consent** | Before KPI inclusion | M1–M9 / effectiveness numerators |
| **C3 Interview consent** | Before structured interview | Interview archive |
| **C4 Quote consent** | Before publishing anonymous quotes | Quote use |

**Rules:**

- Decline of C3/C4 **must not** remove study access.  
- Withdrawal of C2 excludes from numerators; access may continue.  
- Capture in ops consent log; file only pseudonymous completeness flags in git evidence if needed.  
- Align wording with `STAGE1_INVITE_PACK.md` §6.

**No KPI counting** until C1 + C2 recorded.

---

## 11. Operator day-0 / day-7 actions

| Day | Action |
|-----|--------|
| 0 (acceptance) | Confirm consents; send welcome; orientation checklist |
| 1–2 | Soft check if no first login |
| 7 | If never-activated: send Reminder; offer support; log chase |
| 14 | If dormant after prior activation: light check-in (optional) |

---

## 12. STOP

Do not onboard external participants until Founder authorises invite send.  
Do not invent activation events.

Signed: OP-001 Onboarding Protocol · 2026-08-04

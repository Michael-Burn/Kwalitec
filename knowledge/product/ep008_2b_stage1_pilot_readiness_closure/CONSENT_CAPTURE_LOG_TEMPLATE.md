# Stage 1 Consent Capture Log — Template (OR-04)

**Programme:** EP-008.2B / EP-004 Stage 1  
**Version:** 2026-07-26  
**Status:** Process **READY** — live rows start at first invite (N=0 today)  
**Authority:** Privacy Sign-off Package §5 · `BETA_COHORT.md` §3 · Private Beta Protocol §3  
**Privacy rule:** Copy this template to a **private ops store**. Do **not** commit filled rows with emails, names, or other PII to git. Knowledge repo mirrors **pseudonymous status only** in `BETA_COHORT.md`.

---

## 1. Purpose

Operationalise capture of:

1. Privacy notice acknowledgement (required for external study access)  
2. Measurement consent (required for M-series / KPI numerators)  
3. Interview consent (optional)  
4. Quote consent (optional)  

Withdrawal of measurement consent → exclude from KPI numerators; study may continue. Decline of interview/quote → keep study access.

---

## 2. Operator process

```text
Send invite pack (STAGE1_INVITE_PACK.md)
        ↓
Receive Yes/No answers (email reply or form)
        ↓
Verify identity matches provisioned account
        ↓
Record row in THIS ops log (private store)
        ↓
Update BETA_COHORT.md Consent column (pseudonymous only)
        ↓
Only then include in measurement numerators (if measurement = Yes)
```

**Hard gate:** Cannot / will not acknowledge privacy notice → do not grant productive study access as Stage 1 external. Do not pressure.

**CLI assist (technical, not a substitute for human capture):**

```bash
flask analytics-verify-consent <user_id>
flask analytics-verify-consent <user_id> --marketing-use   # must deny
```

---

## 3. Field definitions

| Field | Allowed values | Notes |
|---|---|---|
| Pilot ID | `BETA-PIL-001` … `010` | Pseudonymous — OK to mirror in git |
| User id | integer | Ops only |
| Privacy ack | Yes / No | Required Yes for access |
| Measurement | Yes / No | Required Yes for KPI numerators |
| Interview | Yes / No / Prefer not | Optional |
| Quote | Yes / No / Prefer not | Optional |
| Captured at | ISO date-time | |
| Captured by | Operator name | |
| Channel | email / form / call | |
| Withdrawal | blank / measurement withdrawn + date | Exclude from KPI if set |
| Notes | free text | No unnecessary PII |

---

## 4. Log table (ops store — leave blank in git)

| Pilot ID | User id | Privacy ack | Measurement | Interview | Quote | Captured at | Captured by | Channel | Withdrawal | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
| | | | | | | | | | | |

---

## 5. Registry mirror (git-safe)

After each capture, update `../ep004_private_beta/BETA_COHORT.md` Consent column, e.g.:

| Consent value | Meaning |
|---|---|
| `Pending` | Invite not sent or consents not returned |
| `Privacy+Measure` | Privacy ack Yes + Measurement Yes |
| `Privacy only` | May study; **exclude** from KPI numerators |
| `Withdrawn measure` | Measurement withdrawn; may still study |
| `Declined` | Ineligible / not enrolled |

Never write email or legal name in the cohort register.

---

## 6. OR-04 readiness record

| Item | Status |
|---|---|
| Consent wording | **READY** — Privacy Sign-off Package §5 / Invite Pack §6 |
| Capture process | **READY** — this template + operator steps |
| Optional interview / quote paths | **READY** — decline ≠ lose access |
| Live filled log | **OPEN** — starts at first invite (N=0) |
| Date process ready | 2026-07-26 |
| Operator | Courage T Shumba |

---

**End of CONSENT_CAPTURE_LOG_TEMPLATE**

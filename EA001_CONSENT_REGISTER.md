# EA-001 — Consent Register

**Programme:** EA-001 — Early Access Cohort 1 Recruitment  
**Wave:** `EA-COHORT-1`  
**As of:** 2026-08-04  
**Authority:** `OP001_ONBOARDING_PROTOCOL.md` §10 · EP-008.2B `CONSENT_CAPTURE_LOG_TEMPLATE.md` · OR-01 Privacy Review (SIGNED)  
**Privacy:** Pseudonymous completeness flags only in git. Full capture (including any PII) stays in the **ops consent log**.

---

## 1. Consent layers

| Code | Layer | Required for |
|------|-------|----------------|
| **C1** | Privacy notice acknowledgement | Any external participation |
| **C2** | Measurement consent | KPI / M1–M9 numerators |
| **C3** | Interview consent | Structured interview archive |
| **C4** | Quote consent | Anonymous quote publication |

**Hard rule:** No KPI counting until **C1 + C2** recorded. Decline of C3/C4 must not remove study access.

---

## 2. Pseudonymous completeness (git-safe)

| ID | Status | C1 | C2 | C3 | C4 | Captured at | Notes |
|----|--------|----|----|----|----|-------------|-------|
| BETA-PIL-001 | Selected — not yet invited | — | — | — | — | — | Awaiting invite + capture |
| BETA-PIL-002 | Selected — not yet invited | — | — | — | — | — | Awaiting invite + capture |
| BETA-PIL-003 | Selected — not yet invited | — | — | — | — | — | Awaiting invite + capture |
| BETA-EA-004…012 | Open slots | — | — | — | — | — | Screen then invite |

**Legend:** `Y` = recorded Yes · `N` = recorded No · `—` = not yet asked · `W` = withdrawn

---

## 3. Aggregate

| Metric | N |
|--------|--:|
| Participants with C1+C2 complete | **0** |
| C3 Yes | **0** |
| C4 Yes | **0** |
| Measurement withdrawn | **0** |

---

## 4. Ops store pointer

| Item | Location |
|------|----------|
| Live consent capture log | Ops store (copy of EP-008.2B template) — **outside git** |
| Privacy Notice version | Stage 1 invite pack / OR-01 package |
| Git mirror | This file + `knowledge/evidence/releases/EA001/registers/consent/` |

Do **not** commit emails, names, or raw consent reply text.

---

## 5. Withdrawal log (empty)

| ID | Type | Date | Effect |
|----|------|------|--------|
| — | — | — | None yet |

Signed: EA-001 Consent Register · 2026-08-04

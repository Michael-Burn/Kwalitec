# EDUCATIONAL_TRUST_RELEASE_DECISION.md

**Programme:** VERSION1-RC2 — Sprint D — Educational Trust Release Decision  
**Authority:** EF-001 · EC-001 PASS · RC2 Sprint C1 PASS · Sprint D LIVE verification  
**Classification:** PI-S1  
**Date:** 2026-08-01  
**LIVE tip:** `94e02f57669831ff6af4e6f6bf87a727ca0cfe38`  
**Host:** https://kwalitec.onrender.com  

---

## Decision

# **GO — Close PB-001 Findings F1 and F2; authorise full PB-001 rerun**

The LIVE application on the Sprint C1 tip demonstrably delivers the certified EC-001 educational experience on published Reading activities. The prior claim-breaking failure mode (empty / non-directed Reading shell on Study 1.1 and undeployed partnership copy) is cleared on the production host for published packages.

This decision does **not** declare Version 1 production-ready, does **not** reopen EF-001, and does **not** claim the full adversarial PB-001 trust claim is re-proven — that requires the authorised complete PB-001 rerun.

---

## Findings closure

| Finding | Prior status | Sprint D status | Justification |
|---------|--------------|-----------------|---------------|
| **PB-001 F1** — No CMP direction (S1 · EC) | Open | **CLOSED** | LIVE Reading on published topics 1.1 / 1.2 / 2.1 / 4.2 includes explicit CMP open/reference and partnership framing (EC-001). Evidence: `PB001A_LIVE_VERIFICATION_REPORT.md`; HTML under `knowledge/evidence/releases/RC2_SPRINT_D/html/`. |
| **PB-001 F2** — Empty Reading activity (S1 · EC) | Open | **CLOSED** | Same paths deliver certified Guided Reading bodies (not LO-only fallback shells). Control 4.1 correctly remains fallback. |

EF-001 operational classification remains **EC** (content/publication), resolved by EC-001 remediation + Sprint C1 publication activation + Sprint D deploy — **without** modifying frozen Educational Framework law.

---

## Preconditions satisfied

| Precondition | Evidence |
|--------------|----------|
| Sprint C1 packages on tip | `afa0010` / tip `94e02f5` |
| Tip on `origin/main` | Push `d8670d5..94e02f5` |
| Render deploy live | `dep-d9ms5o6417fc73c3v1h0` |
| Fingerprint match | `/health.commit` == `94e02f5…` |
| Migrations current | `202607310002` |
| Health PASS | `/health`, `/health/live`, `/health/ready` |
| Fresh-student Reading PASS | `PB001A_LIVE_VERIFICATION_REPORT.md` |

---

## Authorisation — PB-001 complete rerun

**Authorised immediately:** re-run PB-001 Adversarial Educational Validation across the full simulated student population against LIVE tip `94e02f57669831ff6af4e6f6bf87a727ca0cfe38`.

### Bound conditions

1. Target host remains https://kwalitec.onrender.com with fingerprint match to `94e02f5…` (or a successor tip that preserves the Sprint C1 publication set and EC-001 Reading bodies).  
2. Simulation remains black-box / defect-non-remediating during the run (same PB-001 method).  
3. Success is judged against the educational trust claim, not against this Sprint D gate alone.  
4. Residual known issues **out of F1/F2 closure** must not be silently treated as PASS:  
   - **KI-H4** shared `topic_code` first-match for 1.2 / 2.1 sibling days  
   - Campaign revision days `CA-R1` / `CB-R1` (loader-live; not Baseline-seeded in Sprint D)

### Not authorised by this decision

- Declaring Version 1 production-ready  
- Unfreezing EF-001  
- Changing Runtime, SCI, recommendation engines, or educational content under Sprint D  
- Closing KI-H4 or volume marketing `released` status claims

---

## Success criterion (Sprint D)

> The LIVE application demonstrably delivers the certified EC-001 educational experience to real students, allowing the full adversarial PB-001 simulation to resume against the canonical production system.

**Met.**

---

## Sign-off artefacts

| Artefact | Path |
|----------|------|
| Deployment report | `RC2_SPRINT_D_DEPLOYMENT_REPORT.md` |
| LIVE verification | `PB001A_LIVE_VERIFICATION_REPORT.md` |
| Evidence pack | `knowledge/evidence/releases/RC2_SPRINT_D/` |
| This decision | `EDUCATIONAL_TRUST_RELEASE_DECISION.md` |

---

## Stop

Educational trust release decision recorded. Proceed to complete PB-001 rerun under a separate mission ID. Do not modify Educational Framework, Runtime, SCI, or recommendation engines under Sprint D.

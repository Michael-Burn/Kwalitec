# Current Release Position

**Programme:** P-003.8 — Version 1 Exit Criteria  
**As of:** 2026-07-26  
**Claim window:** W-PROD  
**Status:** Freeze-date snapshot (synthesis only)  
**Does not:** Change DR-041, gates, risks, or runtime  

---

## Can Version 1 be released today?

# NO

**Board recommendation:** **NO GO** (DR-041)

---

## Scoreboard

| Dimension | State | Source |
|---|---|---|
| Validated KSI | **62** (Medium) | EP-007.2; DR-051 |
| Target | ≥ **80** | PSF; DR-025; G1.1 |
| Gap | **18** | — |
| Gate G1 | **FAIL** | G1.1, G1.9; G1.7 HOLD; G1.5 PASS |
| K8 (G1.5) | **70** PASS | EP-006.3; DR-042 |
| K1 / K2 / K3 | **72** / **55** / **65** | EP-007.2 / EP-005.1 chain / EP-006.5 |
| Educational effectiveness | **NO-GO / PENDING EVIDENCE** | EP-003; EP-007.3 G1.9 |
| External cohort N | **0** | Privacy unsigned; Stage 1 ops not started |
| Private beta | **GO WITH CONDITIONS** (Stage 0) | DR-040; EP-004 |
| Public registration | Not exposed | DR-034 |
| Twin / personalisation / feedback defaults | **OFF** | DR-009, DR-039, DR-038 |
| Evidence package G1–G12 | Incomplete (G1 slice only) | P-002.1 evidence folder; PR-019 |
| Release Readiness maturity | Level 2 / Red | P-003.6 (context; not a gate) |
| Version 1 production-ready | **Not declared** | P-002.1; dossier §11 |

---

## Exit criteria at a glance

| ID | Criterion | Status | Blocks GO? |
|---|---|---|---|
| XC-G1 | Validated KSI | **FAIL** | **Yes** |
| XC-G2 | Constitutional / EVF | IN PROGRESS | Yes |
| XC-G3 | Explainability | Partially met | Yes |
| XC-G4 | Recommendation Quality | Partially met | Yes |
| XC-G5 | Planning Quality | Partially met | Yes |
| XC-G6 | Readiness Quality | Partially met | Yes |
| XC-G7 | Performance | IN PROGRESS | Yes / HOLD path |
| XC-G8 | Reliability | IN PROGRESS | Yes / HOLD path |
| XC-G9 | Telemetry | COMPLETE (flag OFF)* | No if claims honest |
| XC-G10 | Security / privacy | IN PROGRESS | Yes for claim class |
| XC-G11 | Tests | IN PROGRESS | Yes for RC tag |
| XC-G12 | Feature flags | Not scored | Yes for matrix / ON defaults |
| XC-PKG | Evidence Package | Incomplete | **Yes** |
| XC-REC | Signed Board record | NO GO posture | **Yes** |

\* PASS only with honest OFF / claim alignment (DR-047).

---

## Why NO GO (evidence-bound)

1. **Hard Gate G1 FAIL** — Validated KSI **62** &lt; **80** (G1.1).  
2. **Hard Gate G1.9 FAIL** — Effectiveness **NO-GO**; `N_external = 0`.  
3. **Incomplete Evidence Package** — G2–G12 declaration boards not assembled.  
4. **P-002.1 decision rule** — Any hard-gate FAIL → overall **NO GO** (DR-031).

References: `../p003_1_version1_release_dossier/Version_1_RELEASE_DOSSIER.md` §11; `Release_Gates.md`; `Version1_State.md`.

---

## What NO GO allows

- Continue Stage 0 invite-only private beta under EP-004 / DR-040.  
- Continue remediation and evidence programmes toward G1.1 / G1.9.  
- Maintain claim freezes (recommendation-effectiveness, Exam Ready, public launch).

## What NO GO forbids

- Declaring “Kwalitec Version 1 is production-ready.”  
- Public registration / marketing launch.  
- Claiming measurable educational effectiveness or exam pass-rate lift from current evidence.

---

## Minimum path before a future declaration board

(Restatement of dossier / Version1_State — **not** a commitment to GO.)

1. Privacy Review signed → Stage 1 cohort ops → M1–M9 + interviews → effectiveness verdict update (**G1.9** / XC-G1).  
2. Further validated KSI to ≥ **80** with Medium/High confidence (**G1.1**) + **G1.7** formality.  
3. Assemble complete G1–G12 Evidence Package (**XC-PKG**); score PASS/HOLD per P-002.1.  
4. Product Board signed go/no-go (**XC-REC**) under existing matrix.

Until those conditions are evidenced, recommendation remains **NO GO**.

---

## Pointers

| Need | Document |
|---|---|
| Full exit criteria | [`VERSION1_EXIT_CRITERIA.md`](VERSION1_EXIT_CRITERIA.md) |
| Meeting checklist | [`BOARD_RELEASE_CHECKLIST.md`](BOARD_RELEASE_CHECKLIST.md) |
| Outcome definitions | [`GO_NO_GO_MATRIX.md`](GO_NO_GO_MATRIX.md) |
| Traceability | [`EXIT_TRACEABILITY.md`](EXIT_TRACEABILITY.md) |
| Dossier | `../p003_1_version1_release_dossier/` |
| Gate law | `../p002_1_version_1_release_framework/` |
| Tracker | `knowledge/VERSION_1_READINESS.md` |

---

**End of CURRENT_RELEASE_POSITION**

# P-004.1 — KSI Gap Analysis & Improvement Roadmap

**Programme:** P-004.1  
**Date:** 2026-07-26  
**Status:** Complete — analysis and planning only  
**Authority board:** Validated KSI **62** (Medium) · Target **≥ 80** · Gap **18** · Board **NO GO** (DR-041)  
**Does not:** Change runtime, services, governance law, architecture, decisions, risks, assumptions, evidence, or release gates  
**Commits:** None (programme constraint)

---

## Purpose

Answer the Product Board’s educational improvement questions:

1. **Why is validated KSI currently 62 instead of 80?**
2. **What are the highest-leverage product improvements?**
3. **Which improvements do *not* matter (or would harm honesty)?**
4. **Which engineering programmes should run first to maximise the probability of reaching KSI 80?**

This programme designs **no new features**. It identifies the **smallest set of improvements** most likely to raise validated educational value under the Product Success Framework.

---

## Board reading order (30 minutes)

| Order | Document | Question answered |
|---|---|---|
| 1 | [`KSI_GAP_ANALYSIS.md`](KSI_GAP_ANALYSIS.md) | Why 62? What closed? What remains? |
| 2 | [`KSI_DIMENSION_BREAKDOWN.md`](KSI_DIMENSION_BREAKDOWN.md) | Per-category scores, gaps, confidence, evidence |
| 3 | [`STUDENT_PAIN_POINTS.md`](STUDENT_PAIN_POINTS.md) | Journey friction catalogue |
| 4 | [`HIGH_LEVERAGE_IMPROVEMENTS.md`](HIGH_LEVERAGE_IMPROVEMENTS.md) | Improvement catalogue + prioritisation matrix |
| 5 | [`EXPECTED_KSI_IMPACT.md`](EXPECTED_KSI_IMPACT.md) | Portfolio path from 62 → 80 (planning only) |
| 6 | [`ENGINEERING_PRIORITIES.md`](ENGINEERING_PRIORITIES.md) | Recommended next EP programmes |
| 7 | [`ROADMAP.md`](ROADMAP.md) | Quick wins · medium-term · post-V1 |
| 8 | [`STUDENT_IMPACT_ASSESSMENT.md`](STUDENT_IMPACT_ASSESSMENT.md) | Student-value framing for this analysis |
| 9 | [`COMPLETION_REPORT.md`](COMPLETION_REPORT.md) | Programme exit package |

---

## Scoreboard (freeze)

| Measure | Value | Source |
|---|---|---|
| Validated KSI (W-PROD) | **62** | EP-007.2; DR-051 |
| Version 1 target | **≥ 80** | PSF; DR-025 |
| Gap | **18** | — |
| K1 / K2 / K3 / K4 | **72 / 55 / 65 / 55** | EP-007.2 board |
| K5 / K6 / K7 / K8 | **63 / 50 / 58 / 70** | EP-007.2 board |
| G1.5 (K8 ≥ 70) | **PASS** | EP-006.3; DR-042 |
| G1.1 (KSI ≥ 80) | **FAIL** | PR-002 |
| G1.9 (effectiveness) | **FAIL** | EP-007.3; N_external=0 |
| Board recommendation | **NO GO** | DR-041 |

---

## One-sentence verdict

Perception remediation (MES + readiness + sole-runtime journey) raised validated KSI from **59 → 62** and cleared the explainability floor; the remaining **18-point** gap is dominated by **recommendation trust (K2)**, **flag-OFF personalisation/analytics (K4/K6)**, **revision depth (K7)**, and the absence of **external cohort evidence** needed for Strong-band scores and effectiveness GO — not by missing algorithms or opaque AI.

---

## Explicit non-goals

- New Runtime A ranking / Twin / second educational brain
- Speculative LLM coach features
- Stacking estimated ΔKSI into a fake “current” score
- Flipping personalisation flags without dogfood + G12
- Declaring Version 1 production-ready
- Amending gates, decisions, risks, or assumptions

---

## Upstream authorities (read-only)

| Artefact | Path |
|---|---|
| Product Success Framework | `../p001_1_ksi_baseline/PRODUCT_SUCCESS_FRAMEWORK.md` |
| Validated evolution | `../p003_1_version1_release_dossier/KSI_Evolution.md` |
| Current release position | `../p003_8_version1_exit_criteria/CURRENT_RELEASE_POSITION.md` |
| Prior gap analysis (KSI 59) | `../ep005_2_educational_experience_validation/KSI_GAP_ANALYSIS.md` |
| Decision / risk / assumption registers | `../p003_2_*` · `../p003_3_*` · `../p003_4_*` |

---

**End of README**

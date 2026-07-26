# EP-006.3 — MES Perception Report

**Programme:** EP-006.3 — MES Perception Validation (Tier B)  
**Date:** 2026-07-26  
**Status:** Complete (evidence-only)  
**Method:** [`PERCEPTION_METHODOLOGY.md`](PERCEPTION_METHODOLOGY.md)  
**Surfaces judged:** [`STUDENT_SURFACE_PACK.md`](STUDENT_SURFACE_PACK.md)  
**Tier B archive:** [`tier_b_reviews/`](tier_b_reviews/) (N=9)  
**Baseline perception:** EP-004 corpus + Meta Analysis V2 (Coach opacity Near-Universal)  
**Does not:** Change runtime, UI, or educational reasoning  

---

## 1. Executive verdict

Post–EP-006.2 MES delivery **measurably improves student perception of explainability on the schema-complete Home/Coach path**. The pre-change Near-Universal theme — Coach restating “highest-value / learning evidence” without working — is **cleared to a minority residual** for schema-complete sessions.

Cold-start / incomplete-schema nights remain weakly explained. Home readiness **drivers** are still absent. Dual-home / duration frictions continue to tax trust but are outside MES delivery scope.

| Dimension | Baseline (pre-MES presentation) | Post–EP-006.2 Tier B | Meaningful change? |
|---|---|---|---|
| Explanation visibility | Poor on canonical Home | **Strong** when schema-complete | **Yes** |
| Explanation comprehension | Opacity Near-Universal | **Majority can restate why** | **Yes** |
| Explanation trust | Weak (Coach distrust) | **Conditional Pass** majority | **Yes (bounded)** |
| Explanation usefulness | Mission restatement | **Pass** majority (adds content) | **Yes** |
| Next-action clarity | Often missing | **Pass** ≥80% schema-complete | **Yes** |
| Review-point usefulness | Unbound / unseen | **Pass** when shown | **Yes** |
| Confidence understanding | Thin / overclaim risk | **Pass** on Suggested + basis | **Yes (bounded)** |

**Unsupported claims:** “Explainability cured for all nights”; “Home readiness fully unpackable”; “KSI ≥ 80”; “educational effectiveness GO”; “dual-home trust cured.”

---

## 2. Cohort and method

| Item | Detail |
|---|---|
| Tier B personas | SV-003, 005, 008, 010, 011, 012, 013, 014, 015 |
| N | **9** (≥8 methodology floor) |
| Focus | Trust / explainability / feedback / adaptation / calibration / decision support |
| Judgement basis | Live student-facing Home renders after EP-006.2 + Mission/Analytics binding inventory |
| Baseline contrast | EP-004 SV corpus; EV-EXP-003 Coach opacity Near-Universal |

Reviews are archived under this programme so the EP-004 baseline corpus remains intact for longitudinal comparison.

---

## 3. Dimension findings

### 3.1 Explanation visibility

**Pass for schema-complete Home.** L1 why + next appear without expand; L2 evidence / confidence / review point reachable in one disclosure (`explanation_card`). Automated EP-006.2 contract tests align with Tier B observation.

**Fail / residual:** Cold-start Home shows why without next or disclosure. Home `readiness_drivers` remain empty in production `home_vm`.

### 3.2 Explanation comprehension

**Majority Pass.** Reviewers (esp. SV-005, SV-014, SV-015) could restate soft-recall + practice evidence + syllabus position in their own words. SV-012 still had to *infer* adaptation linkage after a shock assessment.

Opacity theme status: **not Near-Universal** on schema-complete path → **minority residual** (cold-start + adaptation explicitness).

### 3.3 Explanation trust

**Conditional Pass (majority).** Schema-complete evidence-backed speech earned cautious trust (SV-005, SV-014, SV-013, SV-015). SV-003 respected honesty but rejected product value. SV-008 / SV-010 remained limited by emotional / navigation residuals unrelated to MES fields.

Trust is **not** unconditional blind follow-through — consistent with Product Constitution (advice advisory).

### 3.4 Explanation usefulness

**Pass (majority).** Why adds instructional content beyond the mission title when schema-complete. Cold-start “educational return” remains low-usefulness speech (different failure mode than false learning-evidence claims).

### 3.5 Next-action clarity

**Pass.** ≥8/9 reviewers affirmed clear next action on schema-complete Home (explicit “Next” line). Meets EP-006.1 ≥80% target for that path.

### 3.6 Review-point usefulness

**Pass when shown.** Reviewers noticed and valued reassessment cues (SV-005, SV-011, SV-013, SV-012). Secondary for some decision-focused users (SV-015) relative to Next.

### 3.7 Confidence understanding

**Pass (bounded).** “Suggested” + basis read as provisional (SV-013 calibration Pass). Residual risk: readiness **percentage** on Home without named drivers can still feel over-precise.

---

## 4. Baseline vs post-implementation

| Theme (Meta Analysis V2) | Baseline frequency | Tier B post-MES |
|---|---|---|
| Coach restates mission without working | Near Universal | **Minority** on schema-complete (Coach carries authored why/next) |
| “Learning evidence” claim with empty history | Strong | **Cleared** on schema-complete; cold-start no longer uses that phrase in capture |
| Inspectable Learning Mode rule | Emerging positive | Still present on Workspace path; Home now has parallel inspectable practice-gap why |
| Dual homes / 30 vs 90 | Universal | **Unchanged** (out of MES scope) |

Statistically, this is a **qualitative cohort shift** (N=9 persona re-reviews), not an external RCT. Under EP-005.1 methodology it is sufficient Tier B to support category re-score with **Medium** confidence — not High, and not Stage 1 product-decision KPIs.

---

## 5. Unsupported claims log

| Claim | Status |
|---|---|
| Validated K8 ≥ 70 from checklist Pass alone | **Unsupported** (requires this Tier B — now supplied) |
| Explainability Excellent / mid-Strong (75+) | **Unsupported** — residuals remain |
| Home readiness drivers student-visible | **Unsupported** — `readiness_drivers=()` on Home VM |
| Cold-start explainability cured | **Unsupported** |
| Dual-home trust cured by MES | **Unsupported** |
| Composite KSI ≥ 80 | **Unsupported** |
| Recommendation effectiveness marketing clear | **Unsupported** |

---

## 6. Remediation required (perception residuals)

| ID | Residual | Severity for K8/G1.5 | Suggested owner |
|---|---|---|---|
| PERC-01 | Home readiness drivers still empty | Medium (caps K3 unpackability; mild K8) | Presentation follow-up (MES-05 residual) |
| PERC-02 | Cold-start generic “educational return” speech | Medium (minority opacity) | Copy / incomplete-schema UX (no ranking change) |
| PERC-03 | Adaptation after failure not explicit | Medium for K2/K6 perception | Future experience programme (not MES delivery) |
| PERC-04 | Dual-home / duration mismatch | High for K1/trust; not G1.5 blocker alone | EP-005.2 REM-02 / REM-03 |
| PERC-05 | `V1_REVIEW_PACKAGE` stale Coach description | Low (process) | Refresh review package screens/copy |
| PERC-06 | External N=0 | Caps confidence at Medium | Stage 1 cohort |

**G1.5 path:** PERC-01/02 are improvements after bare-floor clear; they do not by themselves reverse a K8 ≥ 70 claim if schema-complete majority Pass holds.

---

## 7. Evidence index

| ID | Artefact |
|---|---|
| EV-MES-TB-001 | This report |
| EV-MES-TB-002 | `tier_b_reviews/SV-*.md` (N=9) |
| EV-MES-TB-003 | `STUDENT_SURFACE_PACK.md` + `_capture/` |
| EV-MES-TB-004 | EP-006.2 contract / template / parity tests |
| EV-MES-TB-005 | EP-004 baseline corpus (contrast only) |

---

## References

- [`K8_REVALIDATION.md`](K8_REVALIDATION.md)  
- [`G1_5_STATUS.md`](G1_5_STATUS.md)  
- [`EVIDENCE_CONFIDENCE_UPDATE.md`](EVIDENCE_CONFIDENCE_UPDATE.md)  
- `../ep006_1_mes_end_to_end_delivery/MES_DELIVERY_SPECIFICATION.md` §6  
- `../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`  

---

**End of MES_PERCEPTION_REPORT**

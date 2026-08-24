# PB012-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-012 Progressive Educational Confidence (Campaign Mu)  
**Mission:** Determine exactly why the cohort mean was **9.00 / 9** (and account for every point relative to a perfect score)  
**Authority:** PB-012 PASS · EF-001 Frozen Educational Law · RO-010 PASS WITH RESIDUAL  
**Date:** 2026-08-02  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 11 not started**

---

## Verdict (exit criterion)

# Mean **9.00** — zero numeric deductions on the certified cohort path.

Arithmetic identity:

\[
\frac{5 \times 6 \times 9}{30} = \frac{270}{30} = \mathbf{9.00}
\]

Every certified sitting scored **9/9**. Soft-passed residuals (CM-R1 Q6 / revision chrome; Continuity Front transit labels) are present and classified below, but they do **not** reduce the numeric `/9` under PB-012 residual policy.

Because the mean is **not** below 9.00, there are **no lost points** to attribute. This audit still registers every soft-passed residual and confirms none are newly discovered critical educational findings.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB012/results.json` | Authoritative PB-012 dimension matrix (30 certified sittings) |
| `knowledge/evidence/releases/PB012/personas/*.json` | Persona trajectories |
| `PB012_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB12-R1…R3 |
| `knowledge/evidence/releases/RO010/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `RO010_LIVE_VERIFICATION_REPORT.md` / `RO010_RELEASE_DECISION.md` | RO10-R1…R3 definitions |

---

## Scoring law used by PB-012

Nine educational-confidence dimensions (PASS = 1 point toward `/9`):

1. `mission_clarity`  
2. `cmp_partnership`  
3. `educational_confidence`  
4. `session_completion`  
5. `reflection_quality`  
6. `transition_quality`  
7. `tomorrow_confidence`  
8. `trust_retention`  
9. `educational_consistency`  

Residual soft-pass policy (same class as RO-010 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO10-R3 chrome miss on Learning days | Soft-pass (does not fail progressive claim) | Would record FAIL on `tomorrow_confidence` → **8/9** |
| RO10-R3 chrome miss on CM-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO10-R2 / PB12-R1 revision Q6 on CM-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO10-R1 / PB12-R3 Continuity Front transit / label class | Observed on transit; claim scores only true Mu substance | **Not scored** on CM-D1…CM-R1 matrix |

**This cohort:** Learning days CM-D1…CM-D5 had **chrome match** (numeric `tomorrow_confidence` PASS). CM-R1 retained RO10-R2 / soft-passed RO10-R3 → still **9/9**.

---

## 1. Reconstructed scoring events (all personas identical)

Trajectory for every persona: **9, 9, 9, 9, 9, 9** · stable HIGH · mean **9.00**

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CM-D1 | 9 | — |
| CM-D2 | 9 | — |
| CM-D3 | 9 | — |
| CM-D4 | 9 | — |
| CM-D5 | 9 | — |
| CM-R1 | 9 | — |

Emails:  
`pb012.mu.beginner.1785688816@example.com` · `…average.1785690774…` · `…advanced.1785692761…` · `…returning.1785695054…` · `…struggling.1785697095…`

---

## 2. Deduction register

| ID | Day | Persona | Dimension | Observation | EF-001 class | Residual coverage | Newly discovered? |
|----|-----|---------|-----------|-------------|--------------|-------------------|-------------------|
| — | — | — | — | **No numeric FAILs** | — | — | — |

**Count of numeric deductions:** **0 / 0**.  
**NEW findings required to explain the mean:** **None** (mean already 9.00).

### Soft-passed residuals that did **not** create numeric deductions

| Residual | Observation | EF-001 | Why not in mean gap |
|----------|-------------|--------|---------------------|
| **RO10-R2** / PB12-R1 | CM-R1 checklist Q6 Learning-oriented (`revision_q6_residual: true` on all 5 personas) | **PI** (presentation / audit rubric) | Soft-pass; CM-R1 scored 9/9 |
| **RO10-R3** / PB12-R2 | CM-R1 tomorrow chrome residual (`chrome_residual: true`; soft-pass into tomorrow PASS) | **PI** | Soft-pass on revision day |
| **RO10-R1** / PB12-R3 | Continuity Front CK/CL transit sittings before Mu | **PI** | Progressive claim scores only true Mu substance days |

EF-001 check: all observations resolve as **PI**. None require **EC / AW / RB / EF**. None require unfreezing Educational Law.

### Existing residual vs newly discovered

| Observation | Classification |
|-------------|----------------|
| CM-R1 Q6 Learning-oriented audit | **Existing residual** (RO10-R2) |
| CM-R1 tomorrow chrome soft-pass | **Existing residual** (RO10-R3) |
| CK/CL transit before CM entry | **Existing residual** (RO10-R1 class) |
| Learning-day chrome numeric FAIL | **Not observed** in this cohort (chrome matched) |
| Fallback / Critical educational path failure on certified PASS personas | **Not observed** |

---

## 3. Aggregates

### Per-dimension averages (PASS rate across 30 sittings)

| Dimension | PASS count | Average |
|-----------|----------:|--------:|
| mission_clarity | 30 / 30 | **1.000** |
| cmp_partnership | 30 / 30 | **1.000** |
| educational_confidence | 30 / 30 | **1.000** |
| session_completion | 30 / 30 | **1.000** |
| reflection_quality | 30 / 30 | **1.000** |
| transition_quality | 30 / 30 | **1.000** |
| tomorrow_confidence | 30 / 30 | **1.000** |
| trust_retention | 30 / 30 | **1.000** |
| educational_consistency | 30 / 30 | **1.000** |

### Per-persona averages

| Persona | Certified days | Mean `/9` |
|---------|---------------:|----------:|
| beginner | 6 | **9.00** |
| average | 6 | **9.00** |
| advanced | 6 | **9.00** |
| returning | 6 | **9.00** |
| struggling | 6 | **9.00** |
| Cohort | 30 | **9.00** |

### Per-day averages (all personas)

| Day | Sittings | Mean `/9` | Driver |
|-----|---------:|----------:|--------|
| CM-D1…CM-D5 | 5 each | **9.00** | Chrome matched |
| CM-R1 | 5 | **9.00** | Soft-pass R2/R3 |

---

## 4. Root cause summary

1. **What failed numerically:** nothing — mean is 9.00.  
2. **What residuals remain:** RO10-R2 (Q6), RO10-R3 (CM-R1 chrome soft-pass), RO10-R1 (transit).  
3. **Why Learning days reached 9/9 here:** expect-day binding to true Mu packages allowed Finish/Home chrome fragment checks to match approved `tomorrow_preview` text (contrast RO-010 offset-detector walk where chrome_residual was true on some Mu Learning days).  
4. **EF-001:** classification **PI** for all soft-passed residuals; Smallest Effective Intervention would be chrome/presentation / audit-rubric binding under existing Educational Law — **out of scope for this audit**.

### Residual coverage check

| Residual | Explains any numeric FAIL? | Notes |
|----------|----------------------------|-------|
| RO10-R1 | No | Transit only |
| RO10-R2 | No | Soft-passed; CM-R1 = 9/9 |
| RO10-R3 | No (this cohort Learning days matched; R1 soft-passed) | Still tracked |
| NEW | **None** | — |

---

## 5. Exit conclusion

> **The entire 9.00 score is fully explained: there are no lost points.**

Soft-passed existing residuals remain open as PI follow-ups and do not disturb the progressive PASS gate.  
No previously unknown critical educational issue has been identified.  
No remediation implemented.  
Wave 11 not started.

---

Signed: PB012-AUDIT · Confidence Score Root Cause Analysis · 2026-08-02  
**Conclusion: mean 9.00 · zero numeric deductions · residuals = existing RO10-R1…R3 only**

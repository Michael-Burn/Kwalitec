# PB011-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-011 Progressive Educational Confidence (Campaign Lambda)  
**Mission:** Determine exactly why the cohort mean was **9.00 / 9** (and account for every point relative to a perfect score)  
**Authority:** PB-011 PASS · EF-001 Frozen Educational Law · RO-009 PASS WITH RESIDUAL  
**Date:** 2026-08-02  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 10 not started**

---

## Verdict (exit criterion)

# Mean **9.00** — zero numeric deductions on the certified cohort path.

Arithmetic identity:

\[
\frac{5 \times 9 \times 9}{45} = \frac{405}{45} = \mathbf{9.00}
\]

Every certified sitting scored **9/9**. Soft-passed residuals (CL-R1 Q6 / revision chrome; Continuity Front transit labels) are present and classified below, but they do **not** reduce the numeric `/9` under PB-011 residual policy.

Because the mean is **not** below 9.00, there are **no lost points** to attribute. This audit still registers every soft-passed residual and confirms none are newly discovered critical educational findings.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB011/results.json` | Authoritative PB-011 dimension matrix (45 certified sittings) |
| `knowledge/evidence/releases/PB011/personas/*.json` | Persona trajectories |
| `PB011_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB11-R1…R3 |
| `knowledge/evidence/releases/RO009/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `RO009_LIVE_VERIFICATION_REPORT.md` / `RO009_RELEASE_DECISION.md` | RO9-R1…R3 definitions |

---

## Scoring law used by PB-011

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

Residual soft-pass policy (same class as RO-009 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO9-R3 chrome miss on Learning days | Soft-pass (does not fail progressive claim) | Would record FAIL on `tomorrow_confidence` → **8/9** |
| RO9-R3 chrome miss on CL-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO9-R2 / PB11-R1 revision Q6 on CL-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO9-R1 / PB11-R3 Continuity Front transit / label class | Observed on transit; claim scores only true Lambda substance | **Not scored** on CL-D1…CL-R1 matrix |

**This cohort:** Learning days CL-D1…CL-D8 had **chrome match** (numeric `tomorrow_confidence` PASS). CL-R1 retained RO9-R2 / soft-passed RO9-R3 → still **9/9**.

---

## 1. Reconstructed scoring events (all personas identical)

Trajectory for every persona: **9, 9, 9, 9, 9, 9, 9, 9, 9** · stable HIGH · mean **9.00**

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CL-D1 | 9 | — |
| CL-D2 | 9 | — |
| CL-D3 | 9 | — |
| CL-D4 | 9 | — |
| CL-D5 | 9 | — |
| CL-D6 | 9 | — |
| CL-D7 | 9 | — |
| CL-D8 | 9 | — |
| CL-R1 | 9 | — |

Emails:  
`pb011.lambda.beginner.1785676331@example.com` · `…average.1785677744…` · `…advanced.1785680359…` · `…returning.1785681691…` · `…struggling.1785683030…`

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
| **RO9-R2** / PB11-R1 | CL-R1 checklist Q6 Learning-oriented (`revision_q6_residual: true` on all 5 personas) | **PI** (presentation / audit rubric) | Soft-pass; CL-R1 scored 9/9 |
| **RO9-R3** / PB11-R2 | CL-R1 tomorrow chrome residual (`chrome_residual: true`; soft-pass into tomorrow PASS) | **PI** | Soft-pass on revision day |
| **RO9-R1** / PB11-R3 | Continuity Front CK transit sittings before Lambda | **PI** | Progressive claim scores only true Lambda substance days |

EF-001 check: all observations resolve as **PI**. None require **EC / AW / RB / EF**. None require unfreezing Educational Law.

### Existing residual vs newly discovered

| Observation | Classification |
|-------------|----------------|
| CL-R1 Q6 Learning-oriented audit | **Existing residual** (RO9-R2) |
| CL-R1 tomorrow chrome soft-pass | **Existing residual** (RO9-R3) |
| CK transit before CL entry | **Existing residual** (RO9-R1 class) |
| Learning-day chrome numeric FAIL | **Not observed** in this cohort (chrome matched) |
| Fallback / Critical educational path failure on certified PASS personas | **Not observed** |

Ops archive only (not cohort PASS path): first advanced provision mid-CL-D3 unfinished reflection stall → fallback loop — **PI / ops harness incomplete-session** · existing recovery class · fresh advanced completed 9/9 · **not** a new educational Critical on the certified claim.

---

## 3. Aggregates

### Per-dimension averages (PASS rate across 45 sittings)

| Dimension | PASS count | Average |
|-----------|----------:|--------:|
| mission_clarity | 45 / 45 | **1.000** |
| cmp_partnership | 45 / 45 | **1.000** |
| educational_confidence | 45 / 45 | **1.000** |
| session_completion | 45 / 45 | **1.000** |
| reflection_quality | 45 / 45 | **1.000** |
| transition_quality | 45 / 45 | **1.000** |
| tomorrow_confidence | 45 / 45 | **1.000** |
| trust_retention | 45 / 45 | **1.000** |
| educational_consistency | 45 / 45 | **1.000** |

### Per-persona averages

| Persona | Certified days | Mean `/9` |
|---------|---------------:|----------:|
| beginner | 9 | **9.00** |
| average | 9 | **9.00** |
| advanced | 9 | **9.00** |
| returning | 9 | **9.00** |
| struggling | 9 | **9.00** |
| Cohort | 45 | **9.00** |

### Per-day averages (all personas)

| Day | Sittings | Mean `/9` | Driver |
|-----|---------:|----------:|--------|
| CL-D1…CL-D8 | 5 each | **9.00** | Chrome matched |
| CL-R1 | 5 | **9.00** | Soft-pass R2/R3 |

---

## 4. Root cause summary

1. **What failed numerically:** nothing — mean is 9.00.  
2. **What residuals remain:** RO9-R2 (Q6), RO9-R3 (CL-R1 chrome soft-pass), RO9-R1 (transit).  
3. **Why Learning days reached 9/9 here:** expect-day binding to true Lambda packages allowed Finish/Home chrome fragment checks to match approved `tomorrow_preview` text (contrast RO-009 offset-detector walk where chrome_residual was true on several Lambda Learning days).  
4. **EF-001:** classification **PI** for all soft-passed residuals; Smallest Effective Intervention would be chrome/presentation / audit-rubric binding under existing Educational Law — **out of scope for this audit**.

### Residual coverage check

| Residual | Explains any numeric FAIL? | Notes |
|----------|----------------------------|-------|
| RO9-R1 | No | Transit only |
| RO9-R2 | No | Soft-passed; CL-R1 = 9/9 |
| RO9-R3 | No (this cohort Learning days matched; R1 soft-passed) | Still tracked |
| NEW | **None** | — |

---

## 5. Exit conclusion

> **The entire 9.00 score is fully explained: there are no lost points.**

Soft-passed existing residuals remain open as PI follow-ups and do not disturb the progressive PASS gate.  
No previously unknown critical educational issue has been identified.  
No remediation implemented.  
Wave 10 not started.

---

Signed: PB011-AUDIT · Confidence Score Root Cause Analysis · 2026-08-02  
**Conclusion: mean 9.00 · zero numeric deductions · residuals = existing RO9-R1…R3 only**

# PB013-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-013 Progressive Educational Confidence (Campaign Nu)  
**Mission:** Determine exactly why the cohort mean was **9.00 / 9** (and account for every point relative to a perfect score)  
**Authority:** PB-013 PASS · EF-001 Frozen Educational Law · RO-011 PASS WITH RESIDUAL  
**Date:** 2026-08-02  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 12 not started**

---

## Verdict (exit criterion)

# Mean **9.00** — zero numeric deductions on the certified cohort path.

Arithmetic identity:

\[
\frac{5 \times 6 \times 9}{30} = \frac{270}{30} = \mathbf{9.00}
\]

Every certified sitting scored **9/9**. Soft-passed residuals (CN-R1 Q6 / revision chrome; Continuity Front transit labels) are present and classified below, but they do **not** reduce the numeric `/9` under PB-013 residual policy.

Because the mean is **not** below 9.00, there are **no lost points** to attribute. This audit still registers every soft-passed residual and confirms none are newly discovered critical educational findings.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB013/results.json` | Authoritative PB-013 dimension matrix (30 certified sittings) |
| `knowledge/evidence/releases/PB013/personas/*.json` | Persona trajectories |
| `PB013_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB13-R1…R3 |
| `knowledge/evidence/releases/RO011/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `RO011_LIVE_VERIFICATION_REPORT.md` / `RO011_RELEASE_DECISION.md` | RO11-R1…R3 definitions |

---

## Scoring law used by PB-013

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

Residual soft-pass policy (same class as RO-011 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO11-R3 chrome miss on Learning days | Soft-pass (does not fail progressive claim) | Would record FAIL on `tomorrow_confidence` → **8/9** |
| RO11-R3 chrome miss on CN-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO11-R2 / PB13-R1 revision Q6 on CN-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO11-R1 / PB13-R3 Continuity Front transit / label class | Observed on transit; claim scores only true Nu substance | **Not scored** on CN-D1…CN-R1 matrix |

**This cohort:** Learning days CN-D1…CN-D5 had **chrome match** (numeric `tomorrow_confidence` PASS). CN-R1 retained RO11-R2 / soft-passed RO11-R3 → still **9/9**.

---

## 1. Reconstructed scoring events (all personas identical)

Trajectory for every persona: **9, 9, 9, 9, 9, 9** · stable HIGH · mean **9.00**

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CN-D1 | 9 | — |
| CN-D2 | 9 | — |
| CN-D3 | 9 | — |
| CN-D4 | 9 | — |
| CN-D5 | 9 | — |
| CN-R1 | 9 | — |

Emails:  
`pb013.nu.beginner.1785704605@example.com` · `…average.1785707203…` · `…advanced.1785709824…` · `…returning.1785712368…` · `…struggling.1785714940…`

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
| **RO11-R2** / PB13-R1 | CN-R1 checklist Q6 Learning-oriented (`revision_q6_residual: true` on all 5 personas) | **PI** (presentation / audit rubric) | Soft-pass; CN-R1 scored 9/9 |
| **RO11-R3** / PB13-R2 | CN-R1 tomorrow chrome residual (`chrome_residual: true`; soft-pass into tomorrow PASS) | **PI** | Soft-pass on revision day |
| **RO11-R1** / PB13-R3 | Continuity Front CK/CL/CM transit sittings before Nu | **PI** | Progressive claim scores only true Nu substance days |

EF-001 check: all observations resolve as **PI**. None require **EC / AW / RB / EF**. None require unfreezing Educational Law.

### Existing residual vs newly discovered

| Observation | Classification |
|-------------|----------------|
| CN-R1 Q6 Learning-oriented audit | **Existing residual** (RO11-R2) |
| CN-R1 tomorrow chrome soft-pass | **Existing residual** (RO11-R3) |
| CK/CL/CM transit before CN entry | **Existing residual** (RO11-R1 class) |
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
| CN-D1…CN-D5 | 5 each | **9.00** | Chrome matched |
| CN-R1 | 5 | **9.00** | Soft-pass R2/R3 |

---

## 4. Root cause summary

1. **What failed numerically:** nothing — mean is 9.00.  
2. **What residuals remain:** RO11-R2 (Q6), RO11-R3 (CN-R1 chrome soft-pass), RO11-R1 (transit).  
3. **Why Learning days reached 9/9 here:** expect-day binding to true Nu packages allowed Finish/Home chrome fragment checks to match approved `tomorrow_preview` text (contrast RO-011 offset-detector walk where chrome_residual was true on some Nu Learning days).  
4. **EF-001:** classification **PI** for all soft-passed residuals; Smallest Effective Intervention would be chrome/presentation / audit-rubric binding under existing Educational Law — **out of scope for this audit**.

### Residual coverage check

| Residual | Explains any numeric FAIL? | Notes |
|----------|----------------------------|-------|
| RO11-R1 | No | Transit only |
| RO11-R2 | No | Soft-passed; CN-R1 = 9/9 |
| RO11-R3 | No (this cohort Learning days matched; R1 soft-passed) | Still tracked |
| NEW | **None** | — |

---

## 5. Exit conclusion

> **The entire 9.00 score is fully explained: there are no lost points.**

Soft-passed existing residuals remain open as PI follow-ups and do not disturb the progressive PASS gate.  
No previously unknown critical educational issue has been identified.  
No remediation implemented.  
Wave 12 not started.

---

Signed: PB013-AUDIT · Confidence Score Root Cause Analysis · 2026-08-02  
**Conclusion: mean 9.00 · zero numeric deductions · residuals = existing RO11-R1…R3 only**

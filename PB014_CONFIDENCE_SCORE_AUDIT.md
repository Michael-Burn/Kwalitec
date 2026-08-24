# PB014-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-014 Progressive Educational Confidence (Campaign Xi)  
**Mission:** Determine exactly why the cohort mean was **9.00 / 9** (and account for every point relative to a perfect score)  
**Authority:** PB-014 PASS · EF-001 Frozen Educational Law · RO-012 PASS WITH RESIDUAL  
**Date:** 2026-08-03  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 13 / EP-013 not started**

---

## Verdict (exit criterion)

# Mean **9.00** — zero numeric deductions on the certified cohort path.

Arithmetic identity:

\[
\frac{5 \times 11 \times 9}{55} = \frac{495}{55} = \mathbf{9.00}
\]

Every certified sitting scored **9/9**. Soft-passed residuals (CX-R1 Q6 / revision chrome; Continuity Front transit labels) are present and classified below, but they do **not** reduce the numeric `/9` under PB-014 residual policy.

Because the mean is **not** below 9.00, there are **no lost points** to attribute. This audit still registers every soft-passed residual and confirms none are newly discovered critical educational findings.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB014/results.json` | Authoritative PB-014 dimension matrix (55 certified sittings) |
| `knowledge/evidence/releases/PB014/personas/*.json` | Persona trajectories |
| `knowledge/evidence/releases/PB014/checkpoints/` | Continuation Protocol resume evidence |
| `PB014_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB14-R1…R3 |
| `knowledge/evidence/releases/RO012/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `RO012_LIVE_VERIFICATION_REPORT.md` / `RO012_RELEASE_DECISION.md` | RO12-R1…R3 definitions |

---

## Scoring law used by PB-014

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

Residual soft-pass policy (same class as RO-012 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO12-R3 chrome miss on Learning days | Soft-pass (does not fail progressive claim) | Would record FAIL on `tomorrow_confidence` → **8/9** |
| RO12-R3 chrome miss on CX-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO12-R2 / PB14-R1 revision Q6 on CX-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO12-R1 / PB14-R3 Continuity Front transit / label class | Observed on transit; claim scores only true Xi substance | **Not scored** on CX-D1…CX-R1 matrix |

**This cohort:** Learning days CX-D1…CX-D10 had **chrome match** (numeric `tomorrow_confidence` PASS). CX-R1 retained RO12-R2 / soft-passed RO12-R3 → still **9/9**.

---

## 1. Reconstructed scoring events (all personas identical)

Trajectory for every persona: **9 × 11** · stable HIGH · mean **9.00**

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CX-D1 | 9 | — |
| CX-D2 | 9 | — |
| CX-D3 | 9 | — |
| CX-D4 | 9 | — |
| CX-D5 | 9 | — |
| CX-D6 | 9 | — |
| CX-D7 | 9 | — |
| CX-D8 | 9 | — |
| CX-D9 | 9 | — |
| CX-D10 | 9 | — |
| CX-R1 | 9 | — |

Emails:  
`pb014.xi.beginner.1785742189@example.com` · `…average.1785750939…` · `…advanced.1785742269…` · `…returning.1785742311…` · `…struggling.1785749071…`

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
| **RO12-R2** / PB14-R1 | CX-R1 checklist Q6 Learning-oriented (`revision_q6_residual: true` on all 5 personas) | **PI** (presentation / audit rubric) | Soft-pass; CX-R1 scored 9/9 |
| **RO12-R3** / PB14-R2 | CX-R1 tomorrow chrome residual (`chrome_residual: true`; soft-pass into tomorrow PASS) | **PI** | Soft-pass on revision day |
| **RO12-R1** / PB14-R3 | Continuity Front CK/CL/CM/CN transit sittings before Xi | **PI** | Progressive claim scores only true Xi substance days |

---

## 3. Infrastructure events (explicitly out of scoring)

Per Continuation Protocol and EF-001 operational review class **PI / ops**:

- HTTP / SSL timeouts under parallel LIVE load  
- Render cold starts / temporary disconnects  
- Checkpoint pause + resume for `average` and `struggling`  
- Relogin / browser session restarts  
- Local disk pressure and `/tmp` harness restore  

These **must not** be mapped to Critical / Major / Minor educational findings and do **not** appear in the deduction register. See `PB014_SIMULATION_REPORT.md` § Operational Reliability Notes.

---

## 4. Mean gap statement

| Quantity | Value |
|----------|------:|
| Perfect cohort sum | 495 |
| Observed cohort sum | 495 |
| Mean | **9.00** |
| Points lost | **0** |
| Points requiring EF-001 Critical/Major explanation | **0** |

---

## 5. Exit

Score audit complete. Mean **9.00** fully explained by zero numeric deductions + documented soft-pass residuals RO12-R1…R3. No remediation authorised. EP-013 not started.

---

Signed: PB014-AUDIT · Confidence Score Root Cause Analysis · 2026-08-03

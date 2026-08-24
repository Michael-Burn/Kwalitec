# PB016-AUDIT — Confidence Score Root Cause Analysis

**Programme:** PB-016 Progressive Educational Confidence (Campaign Pi)  
**Mission:** Determine exactly why the cohort mean was **8.90 / 9** (and account for every point relative to a perfect score)  
**Authority:** PB-016 PASS · EF-001 Frozen Educational Law · RO-014 PASS WITH RESIDUAL  
**Date:** 2026-08-04  
**Scope:** Reconstruct scoring events only — **no remediation · Wave 15 / EP-015 not started**

---

## Verdict (exit criterion)

# Mean **8.90** — five numeric deductions on the certified cohort path, all accounted.

Arithmetic identity:

\[
\frac{5 \times (9\times9 + 8)}{50} = \frac{445}{50} = \mathbf{8.90}
\]

Equivalent: maximum \(50 \times 9 = 450\); **5** lost points → \(450 - 5 = 445\); \(445 / 50 = 8.90\).

Every certified sitting scored **9/9** except **CP-D8**, which scored **8/9** for all five personas (failing dimension: `tomorrow_confidence`). Soft-passed residuals (CP-R1 Q6; CP-R1 chrome) are present and classified below, but they do **not** reduce the numeric `/9` under PB-016 residual policy.

Because the mean is **below 9.00**, every lost point is attributed below under EF-001.

---

## Evidence corpus

| Artefact | Role |
|----------|------|
| `knowledge/evidence/releases/PB016/results.json` | Authoritative PB-016 dimension matrix (50 certified sittings) |
| `knowledge/evidence/releases/PB016/personas/*.json` | Persona trajectories |
| `knowledge/evidence/releases/PB016/checkpoints/` | Continuation Protocol resume evidence |
| `PB016_CONFIDENCE_REPORT.md` | Residual soft-pass policy; residual register PB16-R1…R4 |
| `knowledge/evidence/releases/RO014/results.json` | Supporting LIVE verify chrome / Q6 residuals |
| `RO014_LIVE_VERIFICATION_REPORT.md` / `RO014_RELEASE_DECISION.md` | RO14-R1…R4 definitions |

---

## Scoring law used by PB-016

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

Residual soft-pass policy (same class as RO-014 / prior PB programmes):

| Residual | Effect on **progressive PASS gate** | Effect on **numeric `/9` score** |
|----------|--------------------------------------|----------------------------------|
| RO14-R1 chrome miss on Learning days | Soft-pass (does not fail progressive claim if score ≥ 8) | Records FAIL on `tomorrow_confidence` → **8/9** |
| RO14-R1 chrome miss on CP-R1 | Soft-pass | Soft-passed into **PASS** on `tomorrow_confidence` → contributes to **9/9** |
| RO14-R3 / PB16-R2 revision Q6 on CP-R1 | Soft-pass | No dimension FAIL (revision audit-rubric class) |
| RO14-R2 / PB16-R4 Memory Front label / title soft-match | Observed; claim scores only true Pi substance | **Not scored** as separate numeric FAIL when package path holds |

**This cohort:** Learning days CP-D1…CP-D7 and CP-D9 had **chrome match** (9/9). **CP-D8** had chrome miss on all 5 personas → **8/9**. CP-R1 retained RO14-R3 (`revision_q6_residual: true`) with chrome soft-pass → still **9/9**.

---

## 1. Reconstructed scoring events (all personas identical shape)

Trajectory for every persona: **9,9,9,9,9,9,9,8,9,9** · stable HIGH · mean **8.90**

| Day | Score | Failing dimension(s) |
|-----|------:|----------------------|
| CP-D1 | 9 | — |
| CP-D2 | 9 | — |
| CP-D3 | 9 | — |
| CP-D4 | 9 | — |
| CP-D5 | 9 | — |
| CP-D6 | 9 | — |
| CP-D7 | 9 | — |
| CP-D8 | **8** | `tomorrow_confidence` |
| CP-D9 | 9 | — |
| CP-R1 | 9 | — |

Emails:  
`pb016.cp.beginner.1785837986@example.com` · `…average.1785839808…` · `…advanced.1785841553…` · `…returning.1785843445…` · `…struggling.1785847680…`

---

## 2. Deduction register

| ID | Day | Persona | Dimension | Observation | EF-001 class | Residual coverage | Newly discovered? |
|----|-----|---------|-----------|-------------|--------------|-------------------|-------------------|
| D1 | CP-D8 | beginner | `tomorrow_confidence` | Tomorrow chrome fragments not matched on Finish/Home after `…-CP-4.1-LINEAR-REGRESSION` | **PI** | RO14-R1 / PB16-R1 | **No** — known RO-014 chrome class |
| D2 | CP-D8 | average | `tomorrow_confidence` | Same | **PI** | RO14-R1 / PB16-R1 | **No** |
| D3 | CP-D8 | advanced | `tomorrow_confidence` | Same | **PI** | RO14-R1 / PB16-R1 | **No** |
| D4 | CP-D8 | returning | `tomorrow_confidence` | Same | **PI** | RO14-R1 / PB16-R1 | **No** |
| D5 | CP-D8 | struggling | `tomorrow_confidence` | Same | **PI** | RO14-R1 / PB16-R1 | **No** |

**Count of numeric deductions:** **5 / 5**.  
**Points lost:** **5**.  
**Mean gap to 9.00:** \(9.00 - 8.90 = 0.10 = 5/50\).  
**NEW critical educational findings required to explain the mean:** **None**.

### Soft-passed residuals that did **not** create numeric deductions

| Residual | Observation | EF-001 | Why not in mean gap |
|----------|-------------|--------|---------------------|
| **RO14-R3** / PB16-R2 | CP-R1 checklist Q6 Learning-oriented (`revision_q6_residual: true` on all 5 personas) | **PI** (presentation / audit rubric) | Soft-pass; CP-R1 scored 9/9 |
| **RO14-R1** / PB16-R3 | CP-R1 chrome residual soft-passed into `tomorrow_confidence` PASS | **PI** | Soft-pass on revision day |
| **RO14-R2** / PB16-R4 | Memory Front title / label soft-match class (e.g. Opening Front chrome soft-match while package path delivers Pi) | **PI** | Progressive claim scores package-path substance; not a separate `/9` FAIL when finished + CMP + no fallback |

---

## 3. Infrastructure events (explicitly out of scoring)

Per Continuation Protocol and EF-001 operational review class **PI / ops**:

- Detached launcher process exits mid-create-user (relaunch via managed shell)  
- Struggling v1 Continue Session `lsr-5001eaaa166d` → **500 Internal Server Error** on all session routes; account abandoned (`ops/struggling_abandoned_500/`)  
- Fresh struggling Internal Alpha provision completing CP-D1…CP-R1 without replaying prior certified days of the abandoned account  
- Render / API job latency on create-user and backdates  
- Relogin / session restarts  

These **must not** be mapped to Critical / Major / Minor educational findings and do **not** appear in the deduction register. See `PB016_SIMULATION_REPORT.md` § Operational Reliability Notes.

---

## 4. Proof of deduction completeness

For each of 50 certified sittings, dimension fields in `knowledge/evidence/releases/PB016/personas/*.json` show:

- **45** sittings: all nine dimensions `"PASS"`  
- **5** sittings (CP-D8 × 5 personas): exactly one `"FAIL"` on `tomorrow_confidence`; eight `"PASS"`  

Cohort aggregator reports `mean_score_over_9: 8.9` with `fingerprint_ok: true` against tip `4ff8c95…`. No unexplained gap remains between observed mean and perfect 9.00.

---

## EF-001 classification summary

| Finding | Class | Severity | Smallest intervention (out of PB-016 scope) |
|---------|-------|----------|-----------------------------------------------|
| CP-D8 tomorrow chrome miss | **PI** | S3 | Presentation / chrome alignment under existing law — not EF unfreeze |
| CP-R1 Q6 Learning-oriented residual | **PI** | S3 | Audit rubric / presentation — not EF unfreeze |
| Continue Session 500 | Ops / PI | — | Ops recovery only; not educational scoring |

**EF-001 Check:** Resolvable without modifying the frozen Educational Framework — **YES**.

---

Signed: PB016-AUDIT · mean 8.90 · 5 numeric deductions (all RO14-R1 / CP-D8) · 2026-08-04

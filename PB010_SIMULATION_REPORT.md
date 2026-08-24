# PB-010 — Simulation Report (Campaign Kappa)

**Programme:** PB-010 — Progressive Confidence  
**Volume:** CS1-010 · Campaign Kappa (`CK-D1…CK-R1`)  
**Authority:** EF-001 · RO-008 LIVE-complete · HR-008 APPROVED · RO008 Release Decision (PB-010 authorised)  
**Host:** https://kwalitec.onrender.com  
**LIVE tip:** `28a06b176cd1ca1249cc74de0726e5d8c46f5982` (fingerprint match)  
**Date:** 2026-08-02  
**Evidence:** `knowledge/evidence/releases/PB010/`  
**Suite:** `knowledge/evidence/releases/PB010/suite/run_pb010.py`  
**Method:** Black-box LIVE simulation — diligent students obey missions and CMP; defects not remediated during simulation · syllabus / Wave 9 untouched  

---

## Verdict (simulation gate)

# **PASS — 5 / 5 personas completed CK-D1…CK-R1**

All five diverse Internal Alpha personas completed the LIVE-certified Campaign Kappa arc with package-path fidelity. No Critical or Major defects. Minor residuals match RO-008 (chrome / Q6).

---

## Evaluation suite

| Component | Detail |
|-----------|--------|
| Harness | RO-008 LIVE browserless walker + PB-009 progressive scoring law |
| Entry | Baseline `continue_topic` + `curriculum_topic_code=3` (Continuity Front into Topic 3.1) |
| Detection | Syllabus `3.1.N` / Campaign Kappa revision markers (not ops label alone) |
| Scoring | 9 educational-confidence dimensions + 6 programme metrics |
| Regression baseline | `knowledge/evidence/releases/RO008/results.json` (Campaign Kappa outputs) |
| Constraint | No syllabus edits · no Wave 9 · observation only |

---

## Personas

| Slug | Label | Profile | Email | Verdict | Mean /9 |
|------|-------|---------|-------|---------|--------:|
| `beginner` | Beginner candidate | never sitting · very_low confidence · novice answers | `pb010.kappa.beginner.1785669720@example.com` | **PASS** | 8.29 |
| `average` | Average candidate | never · medium · mixed | `pb010.kappa.average.1785670376@example.com` | **PASS** | 8.29 |
| `advanced` | Advanced candidate | never · high · strong | `pb010.kappa.advanced.1785670936@example.com` | **PASS** | 8.29 |
| `returning` | Returning / repeat | previous sitting · medium · strong | `pb010.kappa.returning.1785671502@example.com` | **PASS** | 8.29 |
| `struggling` | Struggling candidate | never · low · weak answers | `pb010.kappa.struggling.1785672079@example.com` | **PASS** | 8.29 |

Each persona enrolled as a brand-new Internal Alpha student (no Founder privileges), followed Kwalitec missions exactly, used the CMP as directed, and completed Reading → activities → Reflection → Finish with ops `mission_date` backdating between sittings.

---

## Journey results (LIVE-certified Kappa only)

| Day | Package | Finish | CMP | Fallback | Typical score | Programme metrics |
|-----|---------|:------:|:---:|:--------:|:-------------:|:-----------------:|
| CK-D1 | `…-3.1-METHOD-OF-MOMENTS` | 5/5 | PASS | No | **9/9** | 6/6 |
| CK-D2 | `…-3.1-MAXIMUM-LIKELIHOOD` | 5/5 | PASS | No | **8/9** | 6/6 |
| CK-D3 | `…-3.1-EFFICIENCY-BIAS-CONSISTENCY-MSE` | 5/5 | PASS | No | **8/9** | 6/6 |
| CK-D4 | `…-3.1-COMPARISON-MSE` | 5/5 | PASS | No | **8/9** | 6/6 |
| CK-D5 | `…-3.1-ASYMPTOTIC-MLE` | 5/5 | PASS | No | **8/9** | 6/6 |
| CK-D6 | `…-3.1-BOOTSTRAP-ESTIMATOR` | 5/5 | PASS | No | **8/9** | 6/6 |
| CK-R1 | `…-REV-ESTIMATORS` | 5/5 | PASS | No | **9/9** | 6/6 |

**Certified day-observations:** 35 (5 × 7).  
**Natural sequence:** CK-D1 → CK-D2 → CK-D3 → CK-D4 → CK-D5 → CK-D6 → CK-R1 on every persona.

---

## Six programme metrics (35 sittings)

| Metric | Pass rate | Result |
|--------|----------:|--------|
| Recommendation consistency | 35 / 35 | **PASS** |
| Weak-area identification accuracy | 35 / 35 | **PASS** |
| Mission sequencing quality | 35 / 35 | **PASS** |
| Continuity between syllabus sections | 35 / 35 | **PASS** |
| Confidence calibration | 35 / 35 | **PASS** |
| Explanation usefulness | 35 / 35 | **PASS** |

**Continuity note:** Kappa Revision stop copy includes “do not begin syllabus 3.2”. The suite treats that honest stop as anti-leak (not a Critical leak).

---

## Defect classification

| Severity | Count (unique) | IDs |
|----------|---------------:|-----|
| Critical | **0** | — |
| Major | **0** | — |
| Minor | **7** | PB10-MINOR-CHROME (CK-D2…CK-D6, CK-R1) · PB10-MINOR-Q6 (CK-R1) |
| Cosmetic | **0** | — |

All Minors map to known RO-008 residuals **RO8-R3** (tomorrow chrome) and **RO8-R2** (revision Q6). No new defect classes.

---

## Regression vs Campaign Kappa (RO-008)

| Check | Result |
|-------|--------|
| Kappa days observed | CK-D1…CK-R1 — match |
| Package IDs | Match RO-008 / HR-008 inventory |
| Cross-persona sequence | Identical on all 5 personas |
| New Critical / Major | **None** |
| Known residual classes only | **Yes** (RO8-R2 / RO8-R3) |
| Regression detected | **No** |

---

## Qualitative findings

1. Persona diversity (beginner → struggling) did **not** change package selection, sequencing, or CMP partnership on the certified Kappa path.  
2. CK-D1 Finish/Home tomorrow chrome matched approved text in this cohort (9/9); CK-D2…CK-D6 retained RO8-R3 chrome miss (8/9) — same PI class as prior Waves.  
3. CK-R1 correctly retrieves estimator hinges and honestly stops before 3.2.  
4. Returning / struggling profiles completed the arc without fallback or sequence break.

---

## Evidence

- `knowledge/evidence/releases/PB010/results.json`  
- `knowledge/evidence/releases/PB010/personas/*.json`  
- `knowledge/evidence/releases/PB010/suite/run_pb010.py`  
- Supporting: `knowledge/evidence/releases/RO008/`

---

Signed: Private Beta · PB-010 Simulation · 2026-08-02  
**Simulation:** **PASS** · Wave 9 **not started**

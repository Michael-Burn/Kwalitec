# Success Measures — Adaptive Assessment

**Programme:** ILE-001 — Adaptive Assessment Experience  
**Version:** 1.0  
**Status:** Design  
**Effective:** 2026-07-28  

---

## Purpose

Define **product success metrics** for Adaptive Assessment: learner outcomes and trust.

Avoid implementation metrics (latency, item-bank size, code coverage) as definitions of product success. Those may be engineering health signals only.

Align with ILE-000 `SUCCESS_METRICS.md`, KSI categories, and Educational Philosophy (assessment as evidence, not vanity scores).

---

## Success thesis

Adaptive Assessment succeeds when students:

1. Feel checks are **useful and non-punitive**.  
2. **Understand why** a check appeared and what changed afterward.  
3. Show **better-calibrated confidence** over time.  
4. Experience **more accurate daily guidance** because evidence improved — without being flooded with questions.

---

## Primary measures (learner outcomes & trust)

### 1. Anxiety safety & framing comprehension

| Measure | Intent | Evidence type |
|---|---|---|
| **Felt tested vs supported** | Students describe checks as learning support, not exams | Blind review / survey / interview |
| **Why-comprehension** | Can state why the check existed in one sentence | Perception task / post-check prompt |
| **Voluntary completion quality** | Starts that finish without distress drop-off attributable to exam chrome | Cohort qualitative + completion with exit reasons |

**Pass signal:** Majority of reviewed students say the check helped them know what to study next *without* feeling examined.

---

### 2. Explainability & trust

| Measure | Intent | Evidence type |
|---|---|---|
| **What / why / next / uncertain** | Post-check, student can answer all four | Structured perception |
| **Trust in plan honesty** | Belief that answers inform the plan without hidden grading | Trust survey items |
| **No dual truth** | Post-check next action matches Home Mission story | Scenario audit / review |

Related: K8 explainability; P-001.2 reviews when surfaces ship.

---

### 3. Evidence usefulness (learner-facing consequence)

| Measure | Intent | Evidence type |
|---|---|---|
| **Visible effect on next study** | Student perceives that checks change tomorrow’s focus appropriately | Journey interviews; Decision Journal where used |
| **Uncertainty honesty** | Students recognise when the product remains unsure | Perception + copy audit |
| **Recovery dignity** | Return-after-gap and incomplete paths preserve willingness to continue | Qualitative |

**Note:** Underlying Twin “thin evidence” reduction may be monitored operationally, but product success is whether students experience honest, useful adaptation — not raw observation counts alone.

---

### 4. Calibration

| Measure | Intent | Evidence type |
|---|---|---|
| **Confidence calibration** | Self-confidence vs evidence-backed estimates move toward alignment | Confidence Check analytics + survey |
| **Overconfidence reduction (leading)** | Fewer “sure but weak evidence” patterns on revisited topics | Longitudinal cohort (privacy-safe) |
| **Underconfidence support** | Students with strong evidence + low confidence report less unjustified anxiety over time | Qualitative / survey |

Avoid optimising for “higher confidence scores.”

---

### 5. Sustainable use (not engagement maximisation)

| Measure | Intent | Evidence type |
|---|---|---|
| **Check acceptance without fatigue** | Framed checks accepted when offered; density complaints low | Offer/accept/defer rates + qualitative |
| **Session completion quality** | Assessment steps that complete *and* produce qualifying evidence | Align EP-003 session quality ideas |
| **Study-day consistency** | Checks support return to the daily loop rather than burn out | Retention / consistency metrics |

---

### 6. Readiness honesty (Readiness Check)

| Measure | Intent | Evidence type |
|---|---|---|
| **Focus usefulness** | Pre-exam check yields actionable last-mile focus | Perception |
| **Non-guarantee comprehension** | Students understand it does not predict pass/fail | Explicit comprehension item |
| **No false reassurance complaints** | Trust incidents related to overclaim | Support / review themes |

---

## Secondary / leading operational signals (not vanity KPIs)

Use as health diagnostics, not north-star optimisation targets:

| Signal | Healthy use |
|---|---|
| Observation yield via lawful pipeline | Engineering + educational integrity |
| Over-assessment deferral rate | Gate working as designed |
| Pause/resume success | Failure recovery health |
| Tutor “explain result” use | Depth-on-request working |

---

## Anti-metrics (do not optimise)

- Maximise questions answered  
- Maximise average “score”  
- Maximise time in assessment UI  
- Maximise push-into-check notifications  
- Maximise forced retries after misses  
- Inflate completion by hiding uncertainty or lowering educational standards  
- Competitive percentiles or leaderboards  

---

## KSI mapping (indicative)

| KSI area | How ILE-001 may contribute when validated |
|---|---|
| K2 Recommendation quality | Better evidence → more trustworthy next actions |
| K5 Feedback / loop quality | Attempt → interpretation → next guidance visible |
| K7 Revision | Revision Checks support durable revisit behaviour |
| K8 Explainability | Why-check and uncertainty UX |

Estimated ΔKSI for this **design-only** milestone: **0** (no student-visible production change). Implementation slices claim ΔKSI only with evidence.

---

## Measurement cadence

| Phase | Focus |
|---|---|
| ILE-001.B–D | Anxiety safety, why-comprehension, feedback four-questions |
| ILE-001.E–F | Recovery dignity, calibration comprehension |
| ILE-001.G | Readiness non-guarantee comprehension |
| ILE-001.I | Full perception pack; trust themes |
| Later Stage / KSI | Validated category movement — not declared from design docs |

---

## Declaration rule

Do not claim “Adaptive Assessment works” from implementation metrics alone.

Claim product success only when **learner outcome and trust measures** above show improvement (or strong qualitative pass) without anti-metric gaming.

---

**End of SUCCESS_MEASURES**

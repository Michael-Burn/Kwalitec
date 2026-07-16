# Version 1 Educational State Refinement

**Capability ID:** EIP-006  
**Programme:** Educational Integrity Programme  
**Classification:** Educational Product Refinement — subordinate to Constitution, Registry, Lifecycle, and Knowledge & Mastery Educational Model  
**Status:** IMPLEMENTED — awaiting Architecture Review  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This document records the Version 1 educational-state refinement delivered under EIP-006.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001)  
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (EGI-002) — especially EL-001, EL-006, EL-007, EL-008, EL-010  
3. `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md` (EIP-004 lineage)  
4. `KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` (EIP-006-DESIGN)  

Authority order for this subject:

> The Constitution and Knowledge & Mastery Model define educational meanings.  
> **This Refinement governs which of those meanings Version 1 may lawfully *expose to students*.**

This document does **not** redesign the Digital Twin, Educational Evidence, or Educational Intelligence.

---

## 1. Educational Principle

Version 1 must expose only educational states that it can objectively support.

| Version 1 student-facing educational state | Educational question |
|--------------------------------------------|----------------------|
| **Study Progress** | What have I studied? |
| **Estimated Knowledge** | How well do I currently understand this? |
| **Educational Guidance** | What optional coaching is suggested, and why? |

**Competence** and **Mastery** remain binding educational constructs in the Knowledge & Mastery Educational Model and the Constitution. They are **not** Version 1 student-facing educational states.

---

## 2. Audit Method

Every material use of the following was classified:

- `mastery` / `mastery_score`  
- stage or confidence value `Mastered`  
- student label **Estimated Mastery**  

Classification for each usage:

1. **Educational understanding (Knowledge)** — provisional grasp from lawful practice/assessment evidence; Version 1 may surface as **Estimated Knowledge**.  
2. **True Mastery** — sustained demonstrated competence over time (EL-007); Version 1 must **not** claim this as a student educational state.  

Internal storage names and Twin research types were evaluated but not redesigned.

---

## 3. Classification Summary

| Surface / artefact | Prior speech or name | Educational meaning | Version 1 decision |
|--------------------|----------------------|---------------------|--------------------|
| `TopicProgress.mastery_score` | Internal scalar | Evidence-backed understanding posture when `average_accuracy` present | **Keep field.** Student meaning: **Estimated Knowledge**. Not Estimated Mastery. |
| `TopicProgress.has_estimated_mastery` | Estimate gate | Evidence gate for estimate visibility | Prefer **`has_estimated_knowledge`**; retain alias for compatibility. |
| Stage `Mastered` | Internal journey stage | High estimated understanding from formula thresholds | **Keep internally.** Student label remains **Strong estimated knowledge** (EL-010 / EIP-003). |
| Form confidence value `"Mastered"` | Felt confidence storage | Soft Observation only (EIP-002) | **Keep as storage value.** UI continues to show **Very Confident**. Never authors estimates alone. |
| Study Plan roadmap metric | “Estimated Mastery” | Same scalar as understanding | Relabel **Estimated Knowledge**. |
| Dashboard / Analytics topic badges | Tooltip “Estimated Mastery…” | Same | Relabel **Estimated Knowledge**. |
| Analytics chart title | “Estimated Mastery Over Time” | Time series of the same scalar | Relabel **Estimated Knowledge Over Time**. |
| Mission / wizard / explainability contrast | “not Estimated Mastery” | Study Progress ≠ understanding | Name Version 1 estimate: **not Estimated Knowledge**. |
| Settings progress export | “Average Estimated Mastery” | Composite factor from scalar mean | Relabel **Average Estimated Knowledge**. |
| Recommendation / readiness advisory copy | Mixed | Educational Guidance | **Unchanged** in behaviour; Mastery claims removed where they named the V1 scalar. |
| Digital Twin `TopicMasteryRecord` | Twin research type | Twin-owned knowledge posture | **Not redesigned** (out of scope). |
| Adaptive calculation method names | `calculate_mastery_score`, etc. | Estimation machinery | **Not renamed.** Docstrings clarify V1 meaning is Estimated Knowledge. |

---

## 4. Version 1 Student Educational Story

One coherent story across Mission, Dashboard, Study Plan, Analytics, and Recommendations:

1. **Study Progress** — coverage of the syllabus (Observed / Derived Fact). Completing studying never implies understanding or mastery.  
2. **Estimated Knowledge** — provisional understanding when authorised practice results exist. Always an estimate. Honest absence when evidence is thin.  
3. **Educational Guidance** — optional coaching that supports Learning Mode and does not replace Today’s Mission.  

Forbidden Version 1 student claims:

- Absolute **Mastered** as a Study Progress badge or checkbox.  
- **Estimated Mastery** as the label for the practice-backed scalar.  
- **Competence** as a shipped, governed student metric.  
- Any implication that Study Progress authors Estimated Knowledge.

---

## 5. Why “Estimated Mastery” Was Removed from Version 1 Student Surfaces

The Knowledge & Mastery Educational Model (and Constitution Article IV.8 / EL-007) define Estimated Mastery as longer-horizon, evidence-dense confidence of sustained competence.

Version 1’s live estimate path:

- writes a **single** scalar from authorised Structured Question Results;  
- does **not** maintain a separate, denser Mastery warrant than Knowledge;  
- historically presented that scalar under both Knowledge and Mastery speech (FINDING-012).

Under EIP-006 educational principle:

> Version 1 must expose only educational states it can objectively support.

Therefore the same scalar is presented solely as **Estimated Knowledge**. Mastery remains defined and reserved — not invented, not student-claimed.

This tightens student visibility relative to the Model’s earlier “Partial — Estimated Mastery only” aspiration for Version 1. Educational meaning of Mastery is unchanged; product exposure is deferred until evidence architecture can lawfully separate Knowledge from Mastery without synonym theatre.

---

## 6. What Intentionally Did Not Change

| Area | Reason |
|------|--------|
| Educational Guidance / Learning Mode mission authority | EIP-003 / EIP-001 behaviour; guidance disclosure unchanged |
| Educational Evidence Authority gates | EIP-002; no redesign |
| Digital Twin schemas / succession | Out of scope |
| Educational Intelligence ranking | Out of scope |
| Database column `mastery_score` | Persistence compatibility; meaning documented here |
| Alembic migrations | None required |
| Curriculum V1/V2 traversal | Untouched |

---

## 7. Regression Protection

| Class | Coverage |
|-------|----------|
| Negative | Student surfaces must not emit “Estimated Mastery”; coverage without accuracy must not gate Estimated Knowledge; internal `Mastered` stage must not appear as student “Mastered”. |
| Positive | Evidence gates `has_estimated_knowledge`; Mission / Dashboard / Analytics / Roadmap use Estimated Knowledge / Study Progress story; coverage readiness contrasts against Estimated Knowledge. |

Automated tests: `tests/test_eip006_version1_educational_state_refinement.py` (plus updated EIP-003 / services assertions).

---

## 8. Cross References

| Document | Role |
|----------|------|
| `KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` | Ladder Study Progress ≠ Knowledge ≠ Competence ≠ Mastery |
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Article IV states; Article VII language |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-001, EL-006, EL-007, EL-010 |
| `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md` | Knowledge vs Mastery sibling relationship |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Ownership / writers |
| `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | Student claim honesty |
| `EDUCATIONAL_GOVERNANCE_RECERTIFICATION.md` | FINDING-012 residual closed at presentation layer |

---

## Closing

Version 1 educational states match what Version 1 can truthfully support:

> **Study Progress · Estimated Knowledge · Educational Guidance**

Mastery and Competence remain educationally real. Version 1 does not pretend to measure them as student-facing states.

**Status:** Awaiting Architecture Review.  
**Next:** Do not begin EIP-007 until Architecture Review returns.

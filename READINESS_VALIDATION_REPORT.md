# READINESS_VALIDATION_REPORT.md

**Programme:** VERSION1-RC2 — Sprint B  
**Date:** 2026-08-01  
**Service:** `ReadinessService` (+ explainability / quality contracts)

---

## Verdict

**PASS** — every composite component is explainable, traceable, and evidence-based under Version 1 Educational Law.

---

## Composite model (unchanged weights, corrected inputs)

| Component | Weight | Input (post Sprint B) | Evidence basis |
|-----------|-------:|----------------------|----------------|
| Syllabus coverage / Study Progress | 50% | `completed` leaf topics ÷ plan-scoped leaf total | Study Progress (Observed / Derived Fact) |
| Average Estimated Knowledge | 30% | Mean `mastery_score` where `has_estimated_knowledge` | Authorised practice results only |
| Review discipline | 20% | Mission completion rate | Mission status counts |

Score = `0.5·coverage + 0.3·avg_EK + 0.2·review`.

---

## Traceability

| Claim | Trace |
|-------|-------|
| Coverage % | `_study_progress_metrics` → `TopicProgress.completed` on `_leaf_topics_for_user` |
| Plan scope | Active plan `curriculum_id` via `StudyPlanService` + `CurriculumService.get_ordered_topics`; fail-open to global leaves if unbound |
| EK average | Rows with `average_accuracy is not None` (`has_estimated_knowledge`) — never coverage-minted |
| Review discipline | `Mission.status == Completed` / total missions |
| Student narrative | `EducationalExplainabilityService.explain_composite_readiness` cites Study Progress, EK, review |
| Driver schema | `readiness_quality` drivers: “Study Progress — completed syllabus topics”, “Average Estimated Knowledge from recorded practice”, “Recent review / mission completion” |

---

## Honesty checks

| Check | Result |
|-------|--------|
| Completion alone mints EK? | **No** (EIP-001 / EIP-006 preserved) |
| Revision-only sessions inflate coverage? | **No** (requires `completed`) |
| Estimate labelled as estimate? | **Yes** (`is_estimate=True` on composite narrative) |
| Drivers disclose weights? | **Yes** (50% / 30% / 20%) |
| Separated from Study Progress readiness? | **Yes** — `calculate_readiness` remains coverage-only weighted narrative (“not Estimated Knowledge”) |

---

## Validation evidence

```text
python3 -m pytest \
  tests/test_rc2_educational_trust_consistency.py \
  tests/services/test_readiness_quality_ep003_2.py \
  tests/test_eip003_educational_explainability.py::TestNegativeEstimateAsFact \
  tests/test_services.py::TestReadinessService -q
# → PASS
```

Architecture Guardian: **40/100** (pre-existing debt); Blueprint Separation **PASS**.

---

## Residual

LIVE readiness numbers for Founder student `ctshumba01` must be re-sampled after Sprint C deploy; this report certifies **calculation law**, not LIVE fingerprints.

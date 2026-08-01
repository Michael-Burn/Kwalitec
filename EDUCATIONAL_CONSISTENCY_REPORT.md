# EDUCATIONAL_CONSISTENCY_REPORT.md

**Programme:** VERSION1-RC2 — Sprint B  
**Date:** 2026-08-01  
**Question:** Do Dashboard, Analytics, Readiness, Topic Status, Estimated Knowledge, and Learning Objectives tell one coherent educational story?

---

## Verdict

**PASS (local code authority)** — coverage, knowledge, and topic-state presentation now share Study Progress / EIP evidence rules. LIVE confirmation deferred to Sprint C.

---

## 1. Coverage authority

### Before

| Consumer | Definition |
|----------|------------|
| Dashboard Study Progress | `TopicProgress.completed` (weighted) |
| Analytics / Readiness / Exam timeline | `revision_count > 0` over **global** leaf topics |

Same student could see different “coverage %” on one journey.

### After

| Consumer | Definition |
|----------|------------|
| `ReadinessService.get_curriculum_coverage` | Plan-scoped leaf topics; **`completed`** |
| `ReadinessService.get_overall_readiness` coverage leg | Same `_study_progress_metrics` helper |
| `CurriculumService.get_curriculum_progress` | Same `completed` semantics (parity asserted in tests) |
| Twin readiness CLS fallback | Prefers `completed` only (no `revision_count` inflation) |

**Result:** Dashboard / Analytics / Readiness coverage derive from the **same authoritative calculation**.

---

## 2. Recorded practice → state

| Update | Writer | Gate |
|--------|--------|------|
| Estimated Knowledge (`mastery_score`, `average_accuracy`, stage) | `AdaptiveLearningService.update_mastery_after_attempt` | Authorised structured question results (EIP-002) |
| Study Progress (`completed`) | Mission completion path | Separate from EK (EIP-001) |
| Readiness inputs | Read-only composite of coverage + EK + review discipline | No second formula |

Practice with authorised results updates EK and stage; completion updates coverage; readiness reads both consistently.

---

## 3. Topic status vs Estimated Knowledge

**Educational model:** Practice-backed Estimated Knowledge **may** exist before Study Progress marks a topic completed (coverage ≠ understanding).

**UI rule (Study Plan roadmap):**

| Condition | Badge |
|-----------|-------|
| `completed` | Completed |
| Current learning pointer | Learning |
| Next incomplete | Next |
| `has_estimated_knowledge` and not completed | **Practised** + basis copy that EK can precede completion |
| Otherwise | Not Started / stage label |

**Contradiction eliminated:** “Not Started” + 70% EK no longer appears without explanation.

---

## 4. Learning objectives

| Surface | Behaviour |
|---------|-----------|
| Study Plan roadmap | Renders imported active LOs per topic, ordered by `LearningObjective.order` |
| Empty curriculum | Honest “Not available yet” placeholder only when no LOs exist |
| Curriculum Map | LO status inherits parent Study Progress; children sorted by syllabus code |
| Non-syllabus titles | Filtered via `is_non_syllabus_title` (address / publisher noise) |

---

## 5. Workflow agreement (local / unit)

Fresh-student HTTP journey was **not** re-executed on LIVE (no deploy). Local parity tests confirm:

```
completed topics → identical coverage_pct on get_overall_readiness
                 → identical coverage_percentage on get_curriculum_coverage
                 → identical completion_percentage on get_curriculum_progress

revision_count-only practice → coverage stays 0%; EK average still reflects practice
```

---

## Tests

| Suite | Result |
|-------|--------|
| `tests/test_rc2_educational_trust_consistency.py` | PASS |
| `tests/test_ptp003_honest_product_communication.py` | PASS |
| `tests/services/test_readiness_quality_ep003_2.py` | PASS |
| `tests/test_services.py::TestReadinessService` | PASS |

---

## Known residual

- Pedagogy placeholders / empty reading (EV-001 TB-001/007) require LIVE package validation.  
- Two pre-existing EIP-006 tests hard-code `topic_id=1` without creating a Topic (FK IntegrityError) — unrelated to this remediation.

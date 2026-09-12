# Study Progress Ownership — Phases 1–3

**Status:** Implemented (data-model / ownership correction)  
**Date:** 2026-09-12  
**Scope:** Canonical Study Progress ownership, coverage ≠ mastery, prior-knowledge claims distinct from verified coverage.  
**Non-goals:** Progression Readiness evaluator, mastery gate, Twin EK / Policy V1 / OEA / Spacing / VP-001 / arbitration, student-facing template rewrites.

## Canonical owner

**Sole owner** of live Study Progress for the Education OS: the Runtime C immutable event stream (`runtime_educational_events`), derived only via domain `derive_progress` / Progress Engine / `EducationalRuntimeEngineService.get_study_progress`.

Stage A `TopicProgress.completed` remains a historical/legacy write path (wizard, edit, remap) but is **not** an independent OR-able source of truth when a Runtime C enrolment exists. `CompositeStudyProgressReader` uses Runtime C only when enrolled; Stage A only as legacy fallback when there is no Runtime C enrolment.

## Coverage vs evidence / mastery

**Verified coverage** (`TOPIC_COMPLETED` from an authorised completion path) is a plain historical fact: the product recorded that the topic was completed in the learning loop. It is **not** Estimated Knowledge, mastery, or evidence density.

## Prior-knowledge claims

| Mechanism | Role |
|-----------|------|
| `PRIOR_KNOWLEDGE_CLAIM` event | Written by `seed_declared_position` for baseline continue-from priors |
| Legacy `TOPIC_COMPLETED` with `source=baseline_self_declared` or `warrant=thin_self_declared` | Reclassified as claims on read (no Alembic rewrite) |
| `verified_completed_topic_ids` | Genuine non-baseline `TOPIC_COMPLETED` only |
| `prior_knowledge_claimed_topic_ids` | Claims (new + legacy reclassified) |
| `progressed_topic_ids` / `completed_topic_ids` (alias) | Union used for continue-from / `current_topic_id` / back-compat presentation numbers |
| `verified_coverage_ratio` | Verified-only ratio |
| `coverage_ratio` | Progressed ratio (unchanged numeric behaviour for continue-from this increment) |

Claims may influence where the product positions the student. They must never be written or classified as Kwalitec-verified coverage.

## Finding for a later pass

Honest Progress / Stats still surface a single `coverage_ratio` (progressed) without a student-visible “claimed vs verified” label. The data model now exposes the split; presentation honesty is out of scope for this increment.

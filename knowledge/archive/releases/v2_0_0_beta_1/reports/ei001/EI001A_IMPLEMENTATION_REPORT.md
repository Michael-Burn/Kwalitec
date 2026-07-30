# EI-001A — Implementation Report

**Programme:** Curriculum Intelligence Engine · Phase A  
**Status:** PHASE A COMPLETE  
**Date:** 2026-07-30  
**Authority:** `EI001_CURRICULUM_INTELLIGENCE_ENGINE.md` §12 Phase A  
**Scope:** Domain contracts + Generation Store + Orchestrator foundation only  

---

## Summary

EI-001A delivers the architectural foundation of the Curriculum Intelligence Engine
without educational optimisation logic. Immutable generation snapshots, append-only
Curriculum Memory lineage, an append-only Generation Store (in-memory + SQLAlchemy),
a sequential `GenerationOrchestrator` with mock runners, a `RegressionGuard`
comparison framework, and Certification / Calibration **interfaces** are in place.
The existing CIP pipeline remains functional and was re-verified.

---

## Architecture implemented

```
Presentation / Studio          (unchanged — out of scope)
        ↓
Application
  GenerationOrchestrator
  RegressionGuard
  MockGenerationRunners (G1–G7 placeholders)
  InMemoryGenerationStore
  Ports: GenerationStorePort · CertificationEngine · CalibrationRouter
        ↓
Domain
  Generation · CurriculumGenerationSnapshot · EducationalNode
  LineageRecord / LineageOperation · QualitySnapshot · RegressionPolicy
  CertificationDecision · CalibrationProfile
  ProvenanceRecord / ConfidenceRecord (CIP-002 atoms, extended subject kind)
        ↓
Infrastructure
  SqlAlchemyGenerationStore → ei_* tables
```

Laws preserved:

- Snapshots are write-once; only lifecycle `status` may change.
- Rejected ≠ deleted (`active=False` + rejection reason retained).
- Application orchestrator depends on `GenerationStorePort` (no infra import).
- No LLM; mock runners are deterministic placeholders.
- CIP ingress / Studio egress untouched; no Student Runtime changes.

---

## Domain contracts

| Contract | Role |
|---|---|
| `Generation` | One educational purpose within a chain (`generation_index` 1..7) |
| `CurriculumGenerationSnapshot` | Immutable checkpoint: nodes, rejected nodes, metrics, status |
| `EducationalNode` | Stable `node_id` + confidence + provenance + lineage + `active` |
| `RejectedNode` | Soft-deleted node retained for comparison |
| `LineageRecord` / `LineageOperation` | Append-only Curriculum Memory operations |
| `QualitySnapshot` | Six-metric quality vector (coverage, hierarchy, duplicates, noise, granularity, confidence) |
| `RegressionPolicy` / `RegressionReport` | Gate ε values + durable accept/reject record |
| `CertificationDecision` | Gen 7 outcome enum + score fields (no scoring yet) |
| `CalibrationProfile` | Founder style dimensions (granularity, hierarchy, density, difficulty) |

`ProvenanceSubjectKind.EDUCATIONAL_NODE` added for CIP-002 provenance integration.

---

## Persistence model

Alembic revision `202607300001` (revises `202607290001`):

| Table | Purpose |
|---|---|
| `ei_generation_chains` | Chain scope + **active snapshot pointer** |
| `ei_generations` | Generation metadata |
| `ei_generation_snapshots` | Immutable snapshot root + metrics JSON + status |
| `ei_educational_nodes` | Snapshot-frozen nodes (inactive when rejected) |
| `ei_lineage_operations` | Append-only Curriculum Memory log |
| `ei_regression_reports` | Regression accept/reject history |
| `ei_certification_records` | Certification decisions |
| `ei_calibration_profiles` | Founder calibration profiles |

Adapters:

- `InMemoryGenerationStore` — tests / process-local
- `SqlAlchemyGenerationStore` — durable ORM adapter

---

## Orchestrator / regression / interfaces

| Component | Phase A behaviour |
|---|---|
| `GenerationOrchestrator` | Runs G1…Gn sequentially; stores snapshots; calls RegressionGuard for G≥2; activates accepted; leaves active pointer on last accepted when rejected (rollback) |
| `RegressionGuard` | Lexicographic hard gates on coverage / noise / hierarchy; soft notes for granularity / confidence; no educational scoring |
| `MockRawGraphRunner` / `MockPassThroughRunner` | Deterministic placeholder graphs; Gen 2 can soft-reject `front_matter` |
| `CertificationEngine` | Interface + `UnimplementedCertificationEngine` stub |
| `CalibrationRouter` | Interface + `DefaultCalibrationRouter` mapping (§8.3) — no UI / no regen execution |

---

## Files Created

- `app/domain/curriculum_intelligence/generation.py`
- `app/application/curriculum_intelligence/ports/generation_store_port.py`
- `app/application/curriculum_intelligence/ports/certification_engine_port.py`
- `app/application/curriculum_intelligence/ports/calibration_router_port.py`
- `app/application/curriculum_intelligence/in_memory_generation_store.py`
- `app/application/curriculum_intelligence/regression_guard.py`
- `app/application/curriculum_intelligence/mock_generation_runners.py`
- `app/application/curriculum_intelligence/generation_orchestrator.py`
- `app/models/curriculum_generation.py`
- `app/infrastructure/adapters/curriculum_intelligence/generation_store.py`
- `migrations/versions/202607300001_ei001a_generation_store.py`
- `tests/application/curriculum_intelligence/test_ei001a_generation_engine.py`
- `knowledge/engineering/ei001_curriculum_intelligence_engine/EI001A_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/domain/curriculum_intelligence/__init__.py` — EI-001 exports
- `app/domain/curriculum_intelligence/provenance.py` — `EDUCATIONAL_NODE` subject kind
- `app/application/curriculum_intelligence/exceptions.py` — snapshot / lineage errors
- `app/application/curriculum_intelligence/ports/__init__.py` — port exports
- `app/infrastructure/adapters/curriculum_intelligence/__init__.py` — store export
- `app/models/__init__.py` — register `Ei*` models
- `app/__init__.py` — import `Ei*` models for metadata registration

---

## Tests Executed

```bash
python -m pytest tests/application/curriculum_intelligence/test_ei001a_generation_engine.py -v
# 8 passed

python -m pytest tests/application/curriculum_intelligence/test_pipeline.py \
  tests/application/curriculum_intelligence/test_validation_provenance.py -q
# 28 passed

ruff check <EI-001A modules>
# All checks passed
```

Coverage exercised:

- Snapshot immutability
- Generation ordering / orchestrator sequencing
- Rollback behaviour (active pointer retained)
- Append-only lineage + stable node identity
- SQLAlchemy Generation Store persistence
- Regression API / quality-vector gates
- Certification + Calibration interfaces

---

## Migration Impact

Additive Alembic revision `202607300001` creating `ei_*` tables only.  
No CIP table alterations. No Student Runtime / curriculum engine schema changes.  
V1/V2 curriculum JSON loadability unaffected.

---

## Architecture Compliance

- Layering Presentation → Application → Domain → Infra preserved.
- Application orchestrator uses `GenerationStorePort`; SQLAlchemy lives in infrastructure.
- Curriculum V1/V2 traversal/import compatibility: **preserved (untouched)**.
- CIP pipeline stages remain the document spine; EI-001 generations are additive and **not yet wired** into `PipelineCoordinator` (Phase B+ migration shim).
- No LLM in educational decisions.

---

## Technical Debt

- Mock runners only — real Gen 1–7 educational logic deferred.
- `RegressionGuard` uses placeholder metric values from mocks; educational scoring not implemented.
- CIP dual-read / coordinator adapter period (EI-001 §10.3) not started.
- Snapshot node rows store confidence/lineage/provenance as JSON for Phase A speed; may normalise further if query patterns demand it.
- `CipPersistenceService` still imports ORM directly (pre-existing CIP pattern); EI store follows the cleaner port pattern.

---

## Known Limitations

- No topic consolidation, hierarchy optimisation, or educational intelligence.
- No Founder UI, Student Runtime, publication, or parser modifications.
- CertificationEngine raises `NotImplementedError` (Phase D).
- CalibrationRouter selects generations only — does not execute partial regen (Phase E).
- Review Pack emitter not started (Phase D).

---

## Remaining work

| Item | Phase |
|---|---|
| Gen 1 raw educational graph (retain-all) | B |
| Gen 2 noise elimination (lift EQ-001 classifier) | B |
| Gen 3 hierarchy construction (syllabus-first) | B |
| RegressionGuard online with real EQ-001 metrics | B |
| Gen 4–6 optimisation / reconciliation | C |
| CertificationEngine + Review Pack | D |
| Studio structure prep reads certified snapshot | D |
| Calibration partial regen + Founder controls | E |
| Live CS1 republish dogfood | F |

---

## Phase B prerequisites

1. **Domain + store stable** — delivered by this phase; Gen runners consume `CurriculumGenerationSnapshot`.
2. **EQ-001 assets available to lift** — `ContentClassificationService`, front-matter gates, depth-aware parse, syllabus-first prep, reconciliation/audit services (already in tree).
3. **CS1 fixtures** — syllabus + CMP extracts / review-pack baseline under `knowledge/engineering/eq001_educational_quality/`.
4. **Regression metrics wiring** — map EQ-001 audit outputs into `QualitySnapshot` fields.
5. **Do not wire Founder UI yet** — keep CIP stages as UI milestones until Gen 1–3 reproduce the 5/15/73 syllabus-first shape with lineage.

Exit criterion for Phase B (from EI-001): CS1 syllabus path reproduces EQ-001 **5 / 15 / 73** shape with lineage.

---

## FINAL DECISION

# PHASE A COMPLETE

Immutable generation snapshots, append-only lineage, stable node identity,
working Generation Store (memory + SQLAlchemy), orchestrator with mock
generations, rollback framework, regression comparison API, and
Certification / Calibration interfaces are operational. Existing CIP
pipeline tests remain green. Educational optimisation remains out of scope
and is deferred to EI-001B.

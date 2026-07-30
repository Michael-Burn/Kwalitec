# EI-001B — Implementation Report

**Programme:** Curriculum Intelligence Engine · Phase B  
**Status:** PHASE B COMPLETE  
**Date:** 2026-07-30  
**Authority:** `EI001_CURRICULUM_INTELLIGENCE_ENGINE.md` §12 Phase B  
**Scope:** Generations 1–3 + Agent framework + real RegressionGuard metrics  

---

## Summary

EI-001B introduces the distinction between **immutable Generations** (curriculum
snapshots) and **executable Agents** (educational transformers). Three Agents —
`RawGraphAgent`, `NoiseEliminationAgent`, and `HierarchyConstructionAgent` —
produce Generations 1–3. EQ-001 classification and syllabus-first hierarchy logic
are lifted into Agents. Every snapshot receives a deterministic Generation Hash.
`RegressionGuard` now operates on real EQ-001-derived `QualitySnapshot` metrics.
No educational optimisation beyond Generation 3 was implemented. The existing CIP
pipeline remains functional.

---

## Implemented agents

| Agent | ID | Gen | Purpose | Deterministic | Rollback |
|---|---|---:|---|---|---|
| `RawGraphAgent` | `raw_graph_agent` | 1 | Retain-all raw educational graph | ✓ | ✓ |
| `NoiseEliminationAgent` | `noise_elimination_agent` | 2 | Soft-reject non-curriculum noise | ✓ | ✓ |
| `HierarchyConstructionAgent` | `hierarchy_construction_agent` | 3 | Syllabus-first hierarchy | ✓ | ✓ |

Every Agent exposes the required descriptor fields:

Agent ID · Name · Purpose · Consumes · Produces · Dependencies · Version ·
Deterministic flag · Supports rollback · Quality metrics produced.

Agents implement `CurriculumIntelligenceAgent`, which is also a
`GenerationRunner`, so `GenerationOrchestrator` executes them unchanged.

---

## Generation hashes

Every `CurriculumGenerationSnapshot` carries a SHA-256 `generation_hash` derived
from:

1. Source document ids  
2. Parent snapshot hash  
3. Calibration profile id  
4. Agent id + version  
5. Generation index  
6. Stable node fingerprints (title, kind, role, parent, active, confidence, attributes)

Content-derived ids (not chain-scoped) ensure **independent runs with identical
inputs produce identical hashes**.

Fixture run (`fixed_created_at_iso=2026-07-30T12:00:00Z`, mini CS1 syllabus):

| Gen | Agent | Hash prefix |
|---:|---|---|
| 1 | `raw_graph_agent` | `8d6507495946142d…` |
| 2 | `noise_elimination_agent` | `e909ad9fb474199a…` |
| 3 | `hierarchy_construction_agent` | `69a8203958b917b8…` |

---

## Generation metrics

Real `QualitySnapshot` values from the same fixture (not Phase A placeholders):

| Metric | Gen 1 | Gen 2 | Gen 3 |
|---|---:|---:|---:|
| coverage | 0.4062 | 0.6500 | 0.6780 |
| hierarchy | 0.0000 | 0.0000 | 0.6900 |
| noise | 0.3750 | 0.0000 | 0.0000 |
| confidence | 0.8250 | 0.8700 | 0.9240 |
| chapters | 0 | 0 | 2 |
| topics | 0 | 0 | 3 |
| objectives | 0 | 0 | 4 |
| active nodes | 16 | 10 | 10 |
| rejected | 0 | 6 | 7 |

Observed monotonic educational improvement on hard gates: noise ↓ (G1→G2),
hierarchy ↑ (G2→G3), coverage non-decreasing. Full CS1 5/15/73 shape remains the
dogfood exit when live syllabus PDFs are supplied (fixture is a 2-chapter mini
syllabus).

---

## Migration of EQ-001 logic

| EQ-001 asset | EI-001B home |
|---|---|
| `ContentClassificationService` | Gen 1 labels roles (retain-all); Gen 2 rejects via `NON_CURRICULUM_ROLES` |
| Front-matter / chrome roles | Soft-reject with reason + confidence + evidence |
| `DocumentNormalizationService` + `StructuralParserService` | Gen 3 hierarchy construction |
| `CurriculumMappingService` syllabus-first mapping | Gen 3 Subject→Chapter→Section→Topic→LO |
| `EducationalQualityAuditService` intent | `generation_quality.compute_quality_snapshot` |

Rejected ≠ deleted: inactive nodes remain in Curriculum Memory with lineage
`REJECTED` operations. CIP one-pass parse/map path is unchanged for Studio.

---

## Architecture changes

```
GenerationOrchestrator
        ↓ executes Agents (GenerationRunner)
RawGraphAgent → NoiseEliminationAgent → HierarchyConstructionAgent
        ↓ immutable snapshots + generation_hash
GenerationStore (memory / SQLAlchemy)
        ↓
RegressionGuard (real QualitySnapshot gates)
```

Laws preserved:

- Snapshots write-once; only lifecycle `status` may change  
- Agents transform; Generations are immutable checkpoints  
- No LLM; deterministic content hashes  
- No optimisation beyond Gen 3  
- CIP ingress / Studio egress untouched  

Curriculum Memory on every `EducationalNode`:

- `created_generation` / `current_generation` (lineage accessors)  
- evidence (`provenance`)  
- confidence  
- role  
- active status  

---

## Files Created

- `app/domain/curriculum_intelligence/agent.py`
- `app/application/curriculum_intelligence/agents/__init__.py`
- `app/application/curriculum_intelligence/agents/base.py`
- `app/application/curriculum_intelligence/agents/raw_graph_agent.py`
- `app/application/curriculum_intelligence/agents/noise_elimination_agent.py`
- `app/application/curriculum_intelligence/agents/hierarchy_construction_agent.py`
- `app/application/curriculum_intelligence/generation_hash.py`
- `app/application/curriculum_intelligence/generation_quality.py`
- `migrations/versions/202607300002_ei001b_generation_hash.py`
- `tests/application/curriculum_intelligence/test_ei001b_generation_agents.py`
- `knowledge/engineering/ei001_curriculum_intelligence_engine/EI001B_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/domain/curriculum_intelligence/generation.py` — hash fields; Curriculum Memory accessors; shape counts on `QualitySnapshot`
- `app/domain/curriculum_intelligence/__init__.py` — AgentDescriptor exports
- `app/application/curriculum_intelligence/generation_orchestrator.py` — source documents + agent context
- `app/application/curriculum_intelligence/regression_guard.py` — real-metric framing
- `app/application/curriculum_intelligence/mock_generation_runners.py` — extended context + hashes
- `app/models/curriculum_generation.py` — `generation_hash` / `agent_id` / `agent_version`
- `app/infrastructure/adapters/curriculum_intelligence/generation_store.py` — persist/hydrate hash fields

---

## Tests Executed

```bash
python3 -m pytest tests/application/curriculum_intelligence/test_ei001b_generation_agents.py \
  tests/application/curriculum_intelligence/test_ei001a_generation_engine.py -q
# 17 passed

python3 -m pytest tests/application/curriculum_intelligence/test_educational_quality.py \
  tests/application/curriculum_intelligence/test_pipeline.py -q
# 21 passed (CIP + EQ-001 regression)

ruff check <EI-001B modules>
# All checks passed
```

Coverage exercised:

- Agent descriptor contract  
- Generation reproducibility / stable hashes  
- Agent execution order  
- Snapshot immutability  
- Noise rejection (inactive, not deleted)  
- Hierarchy correctness (syllabus-first)  
- Real regression metrics  
- Rollback to last accepted  

---

## Migration Impact

Additive Alembic revision `202607300002` adds nullable-safe columns on
`ei_generation_snapshots`:

- `generation_hash`  
- `agent_id`  
- `agent_version`  

No CIP table alterations. No Student Runtime / curriculum engine schema changes.
V1/V2 curriculum JSON loadability unaffected.

---

## Architecture Compliance

- Layering Presentation → Application → Domain → Infra preserved.  
- Agents live in application; descriptors in domain; SQLAlchemy in infrastructure.  
- Curriculum V1/V2 traversal/import compatibility: **preserved (untouched)**.  
- CIP pipeline stages remain the document spine; EI Agents are additive and not
  yet wired into `PipelineCoordinator` (Phase C+ shim).  
- No LLM in educational decisions.  

---

## Technical Debt

- Structural parser / mapper still allocate UUID entity ids internally; Gen 3
  node ids are content-hashed to restore reproducibility.  
- Gen 3 rebuilds hierarchy from sources rather than reparenting Gen 2 candidates
  in place — unmatched Gen 2 actives are soft-superseded (`hierarchy:not_promoted`).  
- Full CS1 5/15/73 dogfood against live PDFs deferred to Phase F evidence pack.  
- CIP dual-read / coordinator adapter period (EI-001 §10.3) not started.  

---

## Known Limitations

- No Topic Consolidation (Gen 4), Objective Intelligence (Gen 5), Reconciliation
  (Gen 6), or Certification (Gen 7).  
- No Founder Calibration UI.  
- No Student Runtime changes.  
- Mini syllabus fixtures validate shape rules; live CMP coherence remains EQ-001
  residual debt (Gen 4).  

---

## Remaining work

| Item | Phase |
|---|---|
| Gen 4 topic consolidation (CMP ~936) | C |
| Gen 5 objective intelligence | C |
| Gen 6 educational reconciliation | C |
| CertificationEngine + Review Pack | D |
| Studio structure prep reads certified snapshot | D |
| Calibration partial regen + Founder controls | E |
| Live CS1 republish dogfood (5/15/73 evidence) | F |

---

## FINAL DECISION

# PHASE B COMPLETE

Agent framework is operational. Generations 1–3 are implemented via specialised
Agents. EQ-001 classification and syllabus-first hierarchy logic are migrated
into Agents. RegressionGuard uses real educational metrics. Generation hashes
are deterministic. Immutable snapshots and rollback are preserved. Existing CIP
pipeline tests remain green. Educational optimisation beyond Generation 3 was
not attempted and remains deferred to EI-001C+.

# EI-002A — Implementation Report

**Programme:** Educational Intelligence Integration · Phase A · Founder Integration  
**Status:** EI-002A COMPLETE  
**Date:** 2026-07-30  
**Authority:** Programme brief EI-002A + `EI001_CURRICULUM_INTELLIGENCE_ENGINE.md` §8 / §10 / §12 Phases E–F  
**Scope:** Certified curriculum pipeline wiring into Curriculum Studio, Founder calibration, publication, and Student Runtime  

---

## Summary

EI-002A makes the completed Curriculum Intelligence Engine (EI-001) the
authoritative curriculum source for Founder publish workflows. Every Curriculum
Studio workspace binds to exactly one active Generation Chain. CIP completion
triggers the Generation Orchestrator. Founder calibration adjusts style
dimensions (granularity, hierarchy, topic density, difficulty bias) via
`CalibrationRouter` + partial regeneration. Publication and Foundation Ready
packages prefer certified snapshots; legacy CIP mapping remains migration-only
fallback. Student Runtime accepts certified (and legacy-migration) published
packages — never raw parser outputs.

---

## Workspace integration

```
Upload → CIP → GenerationIntegrationBridge → G1…G7
  → Certification → Review Pack
  → WorkspaceGenerationService.sync (facts + metadata + projection columns)
  → [Optional] FounderCalibrationService.apply
  → Preview (certified dual-read)
  → Approve → Publish (certified gate)
  → Foundation package + Student Runtime
```

| Workspace stores | Mechanism |
|---|---|
| Active Chain | `ei_generation_chains.workspace_id` + metadata `ei_chain_id` + projection `active_chain_id` |
| Current Certified Snapshot | metadata `ei_certified_snapshot_id` + projection column |
| Calibration Profile | `ei_calibration_profiles` + metadata `ei_calibration_profile_id` |
| Certification Status | metadata / projection `certification_status` |
| Review Pack | metadata `ei_review_pack_ref` |

Publication facts (FV-001A additive):

- `intelligence_certified` — Gen 7 CERTIFIED / CERTIFIED_WITH_WARNINGS  
- `calibration_applied` — Founder saved a CalibrationProfile (optional)  
- `legacy_publish_fallback` — migration-only CIP publish allowance  

`READY_TO_PUBLISH` requires the original eight facts **plus** intelligence
satisfaction (`intelligence_certified` **or** `legacy_publish_fallback`).
Calibration is checklist-visible but not a hard gate.

---

## Calibration integration

`FounderCalibrationService`:

1. Loads previous `CalibrationProfile` (if any)  
2. `DefaultCalibrationRouter.select_generations(profile, previous=…)`  
3. `GenerationOrchestrator.run_from(start, …)` through Gen 7  
4. Syncs `calibration_applied` + re-certification facts  

| Setting change | Regen start |
|---|---|
| Hierarchy style | Gen 3 |
| Granularity / Topic Density | Gen 4 |
| Difficulty Bias | Gen 5 |

Founder never edits curriculum nodes — only style dimensions.

---

## Publication integration

1. `PublicationService.assert_ready` / publish gate requires certified **or**
   legacy fallback.  
2. `PublicationBridgeService._ensure_structure` prefers certified dual-read;
   rejects CIP-only structure unless legacy fallback is set.  
3. Foundation `publish_curriculum` writes `package["certification"]` provenance.  
4. `PublishedCurriculumAuthority` accepts certified / legacy / pre-EI packages;
   rejects explicit raw-parser authority.

Legacy mapping path is retained **only** as migration fallback.

---

## Migration progress

| Deliverable | Status |
|---|---|
| Alembic `202607300004` binding columns on `studio_workspace_projections` | Done |
| Store `ensure_chain` / `get_chain_id_for_workspace` | Done |
| CLI `flask ei-migrate-workspaces` | Done |
| Legacy fallback marking for uncertified workspaces | Done |
| Optional `--run-engine` reprocess | Done (best-effort) |
| Live CS1 republish dogfood evidence pack | Remaining (EI-002B / Phase F) |

---

## Runtime

Student Runtime continues to consume `PublishedCurriculumPackage` only.
Packages now carry certification provenance when published through the
certified pipeline. Raw CIP / parser outputs are not exposed through
`PublishedCurriculumAuthority`.

---

## Files Created

- `app/domain/curriculum_intelligence/workspace_binding.py`
- `app/application/curriculum_intelligence/workspace_generation_service.py`
- `app/application/curriculum_intelligence/calibration_service.py`
- `app/application/curriculum_intelligence/generation_integration_bridge.py`
- `app/application/curriculum_intelligence/migration_tooling.py`
- `app/infrastructure/adapters/curriculum_intelligence/certified_snapshot_loader.py`
- `migrations/versions/202607300004_ei002a_workspace_chain_binding.py`
- `tests/application/curriculum_intelligence/test_ei002a_founder_integration.py`
- `knowledge/engineering/ei001_curriculum_intelligence_engine/EI002A_IMPLEMENTATION_REPORT.md`

## Files Modified

- `app/domain/curriculum_studio/publication_checklist.py` — EI facts + readiness
- `app/application/curriculum_studio/fact_updates.py`
- `app/application/curriculum_studio/publication_service.py` — certified gate
- `app/application/curriculum_studio/curriculum_studio_service.py` — soft reconcile
- `app/application/curriculum_studio/structure_preparation_service.py` — source in dict
- `app/application/curriculum_studio/{preview,workspace,version_history,document_upload,management_reconciliation}_service.py` — preserve EI facts
- `app/application/curriculum_intelligence/ports/generation_store_port.py`
- `app/application/curriculum_intelligence/in_memory_generation_store.py`
- `app/infrastructure/adapters/curriculum_intelligence/generation_store.py`
- `app/infrastructure/adapters/curriculum_intelligence/pipeline_processing.py`
- `app/infrastructure/adapters/curriculum_studio_workspace_persistence.py`
- `app/application/platform_integration/publication_bridge.py`
- `app/application/curriculum_studio_foundation/service.py`
- `app/application/curriculum_studio_foundation/authority.py`
- `app/models/curriculum_studio_foundation.py`
- `app/presentation/curriculum_studio/factory.py`
- `app/__init__.py` — CLI registration
- Curriculum Studio / domain test helpers and readiness matrices

---

## Tests Executed

```bash
python3 -m pytest \
  tests/application/curriculum_intelligence/test_ei002a_founder_integration.py \
  tests/application/curriculum_intelligence/test_ei001d_educational_certification.py \
  tests/application/curriculum_studio/test_services.py \
  tests/application/curriculum_studio/test_use_cases.py \
  tests/domain/curriculum_studio/ \
  -q
# 767+ related passed (EI-002A suite 10/10)

ruff check <EI-002A modules>
# All checks passed
```

Coverage exercised:

- Workspace ↔ Generation Chain binding  
- Calibration partial regen (Topic Density → Gen 4+)  
- Certified preview loader projection  
- Certified publication gate + legacy fallback  
- Runtime package authority filter  
- Migration legacy marking  
- Checklist / readiness fact matrices  

---

## Migration Impact

Alembic revision `202607300004` (revises `202607300003`):

- Adds to `studio_workspace_projections`: `active_chain_id`,
  `certified_snapshot_id`, `calibration_profile_id`, `certification_status`,
  `review_pack_ref`  
- Index on chain/workspace active pointer  

No CIP table drops. V1/V2 curriculum JSON loadability unaffected.

---

## Architecture Compliance

- Layering Presentation → Application → Domain → Infra preserved.  
- No LLM in educational decisions.  
- CIP remains ingress; EI Engine is authoritative for certified curriculum.  
- Curriculum V1/V2 traversal/import compatibility: **preserved**.  
- Founder calibrates style; does not edit nodes.  

---

## Technical Debt

- Full CIP→EI bridge on every document may re-run chains aggressively; future
  debounce / “syllabus+CMP both ready” gate recommended.  
- Founder Calibration UI controls not added (service + facts ready; console
  surface can bind next).  
- Live CS1 republish dogfood + evidence pack deferred.  

---

## Known Limitations

- Calibration UI is service-level; no new Founder template yet.  
- `--run-engine` migration reprocess needs source documents present.  
- Cross-diet CERTIFIED_WITH_WARNINGS behaviour inherits EI-001D limits.  

---

## Remaining work

| Item | Next |
|---|---|
| Founder Calibration console controls | EI-002B / UX |
| Live CS1 certified republish dogfood | EI-002B / Phase F |
| Remove dual-read CIP fallback after all workspaces certified | Post-migration |
| Debounce GenerationIntegrationBridge per workspace | Hardening |

---

## FINAL DECISION

# EI-002A COMPLETE

Founder publish path uses the certified curriculum pipeline. Workspaces bind to
Generation Chains. Calibration is operational via CalibrationRouter partial
regen. Publication consumes certified snapshots (legacy CIP retained only as
migration fallback). Student Runtime consumes published packages with
certification provenance — never raw parser outputs. Migration tooling and
schema binding are in place. Remaining work is UI polish and live republish
evidence, not integration architecture.

# V1S-002 — Curriculum Authority Cutover & Runtime Simplification

**Programme:** V1S-002 · Version 1 Stabilisation  
**Phase:** Curriculum authority cutover + mission runtime ownership  
**Date:** 2026-07-31  
**Nature:** Consolidation only — **no new educational capabilities**  
**Authority:** V1S-001 · KWP-015 · KWP-014 · `PRODUCT_BLUEPRINT.md` · `V1_RELEASE_CRITERIA.md`

---

## Executive Summary

V1S-002 closed the dogfood dual-curriculum gap for CS1 / CB2 / CM1: when Runtime C enrolment is enabled and an active published package exists, platform routing selects **PublishedCurriculumAuthority** as the sole student curriculum authority (including legacy IFoA catalogue selections). A single mission spine is documented and surfaced on the Founder Version 1 Readiness dashboard: **EducationalRuntimeEngine + CertifiedMissionEngine + StudentRuntimeCoordinator**. Unwired MissionEngine / MissionEngineV2 / MissionAdapter packages are marked **DEPRECATED / ARCHIVE** with explicit owners; package deletion is scheduled behind extraction and independence-test gates rather than blind delete.

**Verdict:** **DOGFOOD GO WITH CONDITIONS.** Every dogfood subject follows one curriculum authority and one mission runtime when founder-published packages are active. Runtime A substrate and Progress singularity remain owned residual debt — not falsely claimed removed.

---

## Implementation Audit

| Capability | Classification | Owner | Notes |
|---|---|---|---|
| CurriculumRepository.load_auto | **EXISTING** | `app/curriculum/repository` | Loader singularity unchanged |
| CurriculumService import/traversal | **EXISTING** | `app/services/curriculum_service` | Substrate for JSON / historical plans |
| PublishedCurriculumAuthority | **EXISTING** | curriculum_studio_foundation | **Dogfood student authority** |
| Certified packages / CertifiedMissionEngine | **EXISTING** | curriculum_intelligence | Selection on Runtime C spine |
| Founder → Student bridge flags | **MODIFIED** | platform_integration.flags | Dogfood allowlist union |
| RuntimeRoutingService | **MODIFIED** | platform_integration.routing | Reason `dogfood_curriculum_cutover` |
| EducationalRuntimeEngine | **EXISTING** | educational_runtime_engine | Mission instance authority |
| StudentRuntimeCoordinator | **EXISTING** | student_runtime | Session spine glue |
| EducationalExperienceService | **EXISTING** | educational_experience | Runtime C Home projection |
| MissionEngine (application shell) | **TECHNICAL DEBT** → DEPRECATED | mission_engine | Marked off student spine |
| MissionEngineV2 | **REMOVE** → ARCHIVE | mission_engine_v2 | Unwired; tests-only |
| MissionAdapter (migration router) | **REMOVE** → ARCHIVE | mission_adapter | Unwired; tests-only |
| MissionIntelligence (domain) | **EXISTING** | domain.mission | Orchestrator flag-gated OFF |
| MissionPlanningService | **EXISTING** | mission_engine.planning | Founder/EI only — extract later |
| PlanningService / MissionService | **TECHNICAL DEBT** | services | Runtime A until RI-002 |
| Runtime ownership registry | **NEW** | `runtime_ownership.py` | Code-backed matrices |
| Founder V1 Readiness | **MODIFIED** | v1_readiness_dashboard + template | Authority / Mission / Ownership |
| Learning Runtime / Evidence / Progress / Strategy / Diagnostics / Difficulty / Intervention / Memory / Forecast / KA / Authoring / Adaptive Workspace | **EXISTING** — not redesigned | KWP owners | Out of scope |

---

## Runtime Ownership Matrix

Canonical code: `app/services/runtime_ownership.py` → `RUNTIME_OWNERSHIP_MATRIX`.

| Capability | Owner | Status |
|---|---|---|
| Educational Runtime (journey) | `EducationalRuntimeEngineService` | ACTIVE |
| Learning Session Runtime | `LearningSessionRuntime` | ACTIVE |
| Student Runtime Coordinator | `StudentRuntimeCoordinator` | ACTIVE |
| Evidence | `EducationalEvidenceAuthority` | ACTIVE |
| Progress | `ProgressEngine` | ACTIVE (singularity residuals scheduled elsewhere) |
| Strategy → Authoring + Adaptive Workspace | KWP-007…015 | ACTIVE — consumed, not reimplemented |

---

## Curriculum Authority Matrix

Canonical code: `CURRICULUM_AUTHORITY_MATRIX` + cutover helper.

| Capability | Owner | Status |
|---|---|---|
| Student curriculum (dogfood) | `PublishedCurriculumAuthority` | ACTIVE |
| On-disk syllabus loader | `CurriculumRepository.load_auto` | SUBSTRATE |
| DB import / traversal | `CurriculumService` | SUBSTRATE |
| Certified package intelligence | CertifiedLearning / CertifiedMissionEngine | ACTIVE |

### Dogfood cutover rule (V1S-002)

```
Runtime C enrolment ON
  + active PublishedCurriculumPackage for CS1|CB2|CM1
  → PUBLISHED_CURRICULUM (even from IFoA catalogue)
  reason: dogfood_curriculum_cutover

else (no package or enrolment OFF)
  → JSON_BUNDLED (single authority for that subject)
```

Effective allowlist = explicit `RUNTIME_C_SUBJECT_ALLOWLIST` ∪ `{CS1, CB2, CM1}` when enrolment is enabled.

---

## Mission Runtime Review

| Component | Disposition | Evidence |
|---|---|---|
| EducationalRuntimeEngineService | **Active** | Home Runtime C path |
| CertifiedMissionEngine | **Active** | ERE `_select_certified_mission` |
| StudentRuntimeCoordinator | **Active** | Accept ≡ LSR start |
| EducationalExperienceService | **Active** | Runtime C snapshots |
| MissionEngine shell | **Deprecated** | `V1S002_DISPOSITION=DEPRECATED` |
| MissionEngineV2 | **Archive** | Zero app/ presentation/services consumers |
| MissionAdapter | **Archive** | Tests-only |
| MissionIntelligence | **Scheduled** | Orchestrator default OFF |
| PlanningService missions | **Scheduled** | RI-002 retirement |

### Single mission spine

```
PublishedCurriculumPackage
  → PublishedCurriculumAuthority.get_active
  → EducationalEngineFoundationService.derive
  → EducationalRuntimeEngineService.generate_daily_mission
  → CertifiedMissionEngine.generate (selection)
  → EducationalExperienceService.load_for_user
  → StudentHomeService + compose_adaptive_workspace
  → StudentRuntimeCoordinator.accept_and_start_session
  → LearningSessionRuntime
```

---

## Technical Debt Removed

| Item | Action |
|---|---|
| Dual student authority for dogfood CS1/CB2/CM1 (when published) | **Closed** via effective allowlist cutover |
| Undocumented bridge env vars | **Documented** in `.env.example` |
| Unowned MissionEngineV2 / MissionAdapter / ME shell | **Owned** — ARCHIVE / DEPRECATED with gates |
| Undocumented mission spine | **Documented** in registry + Founder UI + this report |
| A3 HOLD for dogfood cohort | **PASS** (conditional on published packages) |

No large package trees deleted from `app/` in this programme — independence suites still exercise archived packages; disposition is explicit so nothing remains without an owner.

---

## Technical Debt Remaining

| Item | Severity | Owner | Gate |
|---|---|---|---|
| Physically archive/delete MissionEngineV2 + MissionAdapter | High | Mission consolidation follow-up | Migrate or drop independence tests |
| Extract MissionPlanningService; delete ME shell | High | V1S follow-up | New `mission_planning/` package |
| Runtime A PlanningService.generate_today_mission | High | RI-002 | Retirement gates PASS |
| Progress singularity residuals | High | Progress programme | Out of V1S-002 |
| Domain CurriculumRepository port | Low | Curriculum housekeeping | Rename or wire |
| seed.py vs import_curricula | Low | Curriculum housekeeping | Prefer import; seed documented |
| Opaque Phase-I demo bridges | Medium | Runtime hygiene | Fail closed first |

---

## Architecture Compliance

- Layering preserved: routing/flags + founder observability + ownership registry only.  
- No redesign of Learning Runtime, Evidence, Progress, Strategy, Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory, Forecast, Knowledge Architecture, Educational Authoring, or Adaptive Workspace.  
- Curriculum V1/V2 **format** compatibility preserved (ADR-003); `load_auto` remains the sole format detector.  
- Curriculum **student authority** singularity achieved for the dogfood cohort under published + enrolment conditions.  
- Runtime A not hard-deleted (RI-002 still applies).

---

## Tests

```
python3 -m pytest tests/test_v1s002_curriculum_authority_cutover.py \
  tests/application/platform_integration/test_bridge.py -q
```

Outcome: **27 passed**.

Ruff clean on touched modules after import sort.

Coverage includes:

- Dogfood allowlist union  
- CS1 IFoA → `dogfood_curriculum_cutover` → PUBLISHED_CURRICULUM  
- Non-dogfood published subject still defaults to Runtime A from IFoA  
- Dogfood without package → JSON_BUNDLED  
- ARCHIVE/DEPRECATED package markers  
- Static guard: student presentation does not import archived mission engines  
- Founder readiness snapshot ownership sections  

---

## Known Limitations

1. Without an active founder-published package, dogfood subjects still enrol on JSON_BUNDLED (one authority, but not published).  
2. MissionEngineV2 / MissionAdapter source trees remain in the repo pending archive deletion.  
3. Runtime A paths remain for non-cohort subjects and historical study plans.  
4. Progress singularity unfinished (out of scope).  
5. Does not claim P-002.1 production-ready / Gate G1.  
6. Does not add new educational intelligence.

---

## Recommendation

1. **Before dogfood enrol:** founder-publish active certified packages for CS1, CB2, and CM1.  
2. Keep Runtime C enrolment enabled for dogfood (development default or `KWALITEC_FOUNDER_STUDENT_BRIDGE=1`).  
3. Use `/founder/v1-readiness` as the ownership board (Curriculum Authority, Mission Runtime, Runtime Ownership, debt register).  
4. Next programmes:  
   - Archive delete MissionEngineV2 + MissionAdapter after test migration  
   - Extract MissionPlanningService; retire ME shell  
   - Progress singularity completion  
   - RI-002 Runtime A hard removal when gates pass  
5. Do **not** re-wire MissionEngine / MissionEngineV2 onto student Home.

---

## Files Created

- `app/services/runtime_ownership.py`  
- `tests/test_v1s002_curriculum_authority_cutover.py`  
- `V1S002_IMPLEMENTATION_REPORT.md`  

## Files Modified

- `app/application/platform_integration/flags.py`  
- `app/application/platform_integration/routing.py`  
- `app/application/educational_runtime_engine/coexistence.py`  
- `app/application/mission_engine/__init__.py`  
- `app/application/mission_engine_v2/__init__.py`  
- `app/application/mission_adapter/__init__.py`  
- `app/curriculum/seed.py`  
- `app/services/v1_readiness_dashboard.py`  
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`  
- `app/founder/dashboard/routes.py`  
- `.env.example`  
- `V1_RELEASE_CRITERIA.md`  

## Migration Impact

**None** — no Alembic / schema changes.

## Success criteria

| Criterion | Result |
|---|---|
| One curriculum authority per dogfood subject (when published) | **PASS** |
| Remove student-facing dependence on legacy pathways for dogfood | **PASS** (routing cutover) |
| Single mission spine documented | **PASS** |
| Runtime ownership simplified / owned | **PASS** |
| No duplicated runtime responsibility without owner | **PASS** |
| No new educational capabilities | **PASS** |

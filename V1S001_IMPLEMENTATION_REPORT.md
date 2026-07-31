# V1S-001 — Version 1 Release Readiness & Architecture Consolidation

**Programme:** V1S-001 · Version 1 Stabilisation  
**Phase:** Internal dogfooding preparation  
**Date:** 2026-07-31  
**Nature:** Consolidation, polish, debt catalogue — **not new educational intelligence**  
**Authority:** KWP-015 · KWP-014 · KWP-013 · KWP-012 · KWP-011 · KWP-010 · KWP-009 · KWP-008 · KWP-007 · `PRODUCT_BLUEPRINT.md`

---

## Executive Summary

V1S-001 audited the post-KWP educational stack and polished student-facing coherence for internal dogfooding. Educational authorities from Strategy through Educational Authoring are cleanly owned and consumed by Adaptive Study Workspace without reimplementation. Presentation language was aligned to the Product Language Guide (Tomorrow Preview, Extra Study, Curriculum Map, Readiness Forecast, Confirm today's Mission). A Founder **Version 1 Readiness** dashboard and checkable `V1_RELEASE_CRITERIA.md` now frame go/no-go.

**Verdict:** **DOGFOOD GO WITH CONDITIONS.** The product can feel release-quality on a single enrolled curriculum authority. It is **not** Version 1 production-ready: dual curriculum runtime authority, Mission orchestration duplication, and P-002.1 Gate G1 (validated KSI) remain open.

---

## Architecture Discovery

### Requested capability inventory

| Capability | Classification | Owner | Notes |
|---|---|---|---|
| Curriculum V2 bundled syllabi | **EXISTING** | `app/curriculum/` + `CurriculumService` | CS1/CB2/CM1 V2 JSON only on disk |
| Curriculum load_auto singularity | **EXISTING** | `CurriculumRepository.load_auto` | Canonical V1/V2 detection |
| Published curriculum (Runtime C) | **EXISTING** · **TECHNICAL DEBT** vs singularity | `PublishedCurriculumAuthority` | Second student authority — coexistence by policy |
| Educational Runtime (journey) | **EXISTING** | `educational_runtime_engine` | Enrolment / mission lifecycle |
| Learning Session Runtime | **EXISTING** | `learning_session` | Sitting FSM / evidence candidates |
| Student Runtime Coordinator | **EXISTING** | `student_runtime` | Spine glue only |
| Evidence Authority | **EXISTING** | `EducationalEvidenceAuthority` | CLEAN |
| Progress Engine | **EXISTING** · **TECHNICAL DEBT** | `progress_engine` | Parallel certified + Runtime A mastery |
| Learning Strategy | **EXISTING** | `learning_strategy` | CLEAN |
| Learning Diagnostics | **EXISTING** | `learning_diagnostics` | CLEAN |
| Learning Difficulty | **EXISTING** | `learning_difficulty` | CLEAN |
| Intervention Effectiveness | **EXISTING** | `intervention_effectiveness` | CLEAN |
| Educational Memory | **EXISTING** | `educational_memory` | CLEAN |
| Readiness Forecast | **EXISTING** | `readiness_forecast` | CLEAN |
| Knowledge Architecture | **EXISTING** | `knowledge_architecture` | CLEAN |
| Educational Authoring | **EXISTING** | `educational_authoring` | KWP-015; composition only |
| Adaptive Study Workspace | **MODIFIED** | `adaptive_workspace` + Home templates | Terminology polish |
| Mission Runtime (student spine) | **EXISTING** · **TECHNICAL DEBT** | ERE + `CertifiedMissionEngine` | Parallel ME / ME v2 / MissionIntelligence |
| Product language | **MODIFIED** | `product_language.py` + surfaces | Rejected synonym CTA removed from UI |
| Founder V1 Readiness | **NEW** | `/founder/v1-readiness` | Dogfooding dashboard |
| V1 Release Criteria | **NEW** | `V1_RELEASE_CRITERIA.md` | Checkable gates |

### System shape (dogfood path)

```
Curriculum (bundled V2 OR published package — pick one per subject)
        │
        ▼
 Educational Runtime / Certified Mission
        │
        ▼
 Student Runtime Coordinator → Learning Session Runtime
        │
        ▼
 Educational Authoring (episodes) + KWP engines (strategy…forecast, KA)
        │
        ▼
 Adaptive Study Workspace (Home)
        │
        ▼
 Student
```

---

## Implementation Audit

### EXISTING (reused — no parallel rebuild)

- All KWP-007…015 engines and Adaptive Workspace composer  
- Curriculum engine `load_auto` chain and DB import via `CurriculumService`  
- Session Experience as HTTP/navigation adapter  
- Founder Platform Intelligence metrics pattern  

### MODIFIED (V1S-001)

- Student Home / Journey / Learning Journey / readiness card copy  
- Adaptive Workspace quick-action labels  
- Runtime C rollback CTA → **Confirm today's Mission**  
- `CurriculumEngineService.load_curriculum` docstring (prefer `load_auto`)  
- Founder nav + Version 1 Readiness route  

### NEW

- `app/services/v1_readiness_dashboard.py`  
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`  
- `V1_RELEASE_CRITERIA.md`  
- `V1S001_IMPLEMENTATION_REPORT.md`  

### REMOVE (recommended — not executed this programme)

Structural removals deferred to dedicated cutover milestones to avoid breaking independence / regression suites:

| Item | Reason deferred |
|---|---|
| `app/application/mission_engine_v2/` full delete | Large test surface; documented V2 package — retire via Mission consolidation programme |
| V1 format loaders | ADR-003 requires format coexistence for historical DB rows |
| Opaque demo bridges | Need explicit “unavailable” path before stub deletion |
| Latent student component templates | Wire-or-delete pass recommended next |

---

## Items Removed

**None from the application tree in V1S-001.** Removals are catalogued under Technical Debt with retirement gates. Presentation **wording** removed/replaced (developer CTAs and engine nouns) rather than package deletion.

---

## Items Consolidated

| Consolidation | Action |
|---|---|
| Workspace section titles | Aligned to product language (Tomorrow Preview, Extra Study, From your learning story) |
| Curriculum Map naming | Journey button + Home quick action use **Curriculum Map** (not Knowledge Map) |
| Forecast link text | **View Readiness Forecast** on Home and workspace actions |
| Mission confirm CTA | Rejected “Mark mission complete” replaced with **Confirm today's Mission** |
| Loader guidance | `load_curriculum` documented as legacy; `load_auto` canonical |

---

## Items Modified

### Presentation

- `app/templates/student/home.html`  
- `app/templates/student/learning_journey.html`  
- `app/templates/student/journey.html`  
- `app/templates/student/components/readiness_card.html`  
- `app/presentation/student/adaptive_workspace.py`  
- `app/presentation/student/educational_view_models.py`  
- `app/presentation/student/forms.py`  
- `app/presentation/student/services/student_home_service.py`  

### Curriculum / Founder

- `app/services/curriculum_engine_service.py`  
- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/routes.py`  

### Tests

- `tests/certification/test_pr001b_student_pilot.py`  
- `tests/test_dx006b_student_home.py`  
- `tests/test_sr002_session_spine.py`  

---

## Technical Debt

| Debt | Severity | Recommendation |
|---|---|---|
| Dual curriculum authority (JSON_BUNDLED + PUBLISHED) | **Blocker** for singularity | Subject-by-subject Runtime C cutover; retire JSON student authority |
| MissionEngine / MissionEngineV2 / MissionIntelligence coexistence | **High** | Declare ERE+Certified as Runtime C owner; archive unwired packages |
| Progress singularity incomplete | **High** | Retire CertifiedProgressEngine + Runtime A mastery writes when gated |
| Opaque Phase-I demo bridges | **Medium** | Fail closed instead of demo payloads |
| Latent templates (`educational_experience.html`, `recommendation_card.html`, …) | **Medium** | Delete or wire in one pass |
| Unused briefing/health CSS selectors | **Low** | Prune `design_system.css` orphans |
| Domain `CurriculumRepository` port unimplemented | **Low** | Rename port or wire adapter |
| `seed_curricula` vs `import_curricula` | **Low** | Align bootstrap or remove seed |
| Substance planner vs Educational Authoring | **Medium** | Converge composition layers when LXP/KWP merge |
| Journey dual mental model | **Medium** | Cross-link copy + dogfood education |
| Triple Home projection (VM + service + workspace) | **Medium** | Document ownership; merge later |

---

## Presentation Audit

| Surface | Verdict | V1S-001 action |
|---|---|---|
| Home / Adaptive Workspace | Coherent visual system; terminology drift fixed | Titles + links aligned |
| History | Strong empty states | No change |
| Journey (syllabus) | Curriculum Map CTA fixed | Knowledge Map → Curriculum Map |
| My Learning Journey | Engine nouns removed from archive blurb | Learner language |
| Forecast | Link text unified | View Readiness Forecast |
| Revision | Mission primacy policy intact | No change |
| Workspace sections | Morning Brief → Mission → Focus → Episode → Tomorrow → Extra → Forecast → Journey | Operates as one experience visually |

**Product language:** No lorem/TODO in student templates. Rejected “Mark mission complete” removed from live CTA paths.

---

## Mission Quality Audit

Educational Authoring (`writing.py` / `episode.py`) enforces:

| Check | Status |
|---|---|
| No CMP copy | **PASS** — `looks_like_cmp_dump` + scrub |
| No objective concatenation | **PASS** — single composed objective |
| Clear educational context | **PASS** — foundation / successor / recent narratives |
| Clear objectives | **PASS** — verb-led or “Strengthen {topic}…” |
| Meaningful success criteria | **PASS** — explain / solve / complete |
| Natural transitions | **PASS** — mission composition arc |
| Tomorrow continuity | **PASS** — `compose_connection` + Tomorrow Preview |

**Residual:** Live quality still depends on certified package metadata richness; dogfooders should flag thin episodes for Curriculum Studio follow-up.

---

## Curriculum Audit

| Gate | Result | Evidence |
|---|---|---|
| One canonical on-disk loader | **PASS** | `load_auto` + anti-duplication tests |
| No shipped V1 JSON | **PASS** | Only V2 files under `app/curriculum/data/` |
| Exactly one student curriculum authority | **FAIL / HOLD** | `RuntimeAuthority` JSON vs published coexistence |
| No duplicate repositories (name collision) | **DEBT** | Engine repo vs unimplemented domain port |
| No orphan curriculum services | **PARTIAL** | `seed.py` low-use; studio/intelligence intentional parallel lifecycles |

**Dogfood rule:** Enrol each dogfood subject on **one** authority only.

---

## Authority Ownership Matrix

| Authority | Owner package | Entry point | Status |
|---|---|---|---|
| Runtime (journey) | `educational_runtime_engine` | `EducationalRuntimeEngineService` | **DEBT** (split + coexistence) |
| Runtime (session) | `learning_session` | `LearningSessionRuntime` | **CLEAN** (with coordinator) |
| Evidence | `educational_evidence_authority` | `EducationalEvidenceAuthority` | **CLEAN** |
| Progress | `progress_engine` | `ProgressEngine` | **DEBT** |
| Strategy | `learning_strategy` | `LearningStrategyEngine` | **CLEAN** |
| Diagnostics | `learning_diagnostics` | `LearningDiagnosticsEngine` | **CLEAN** |
| Difficulty | `learning_difficulty` | `LearningDifficultyEngine` | **CLEAN** |
| Effectiveness | `intervention_effectiveness` | `InterventionEffectivenessEngine` | **CLEAN** |
| Memory | `educational_memory` | `EducationalMemoryService` | **CLEAN** |
| Forecast | `readiness_forecast` | `ReadinessForecastEngine` | **CLEAN** |
| Knowledge Architecture | `knowledge_architecture` | `KnowledgeArchitectureEngine` | **CLEAN** |
| Educational Authoring | `educational_authoring` | `EducationalAuthoringEngine` | **CLEAN** |
| Adaptive Workspace | `presentation/student/adaptive_workspace` | `compose_adaptive_workspace` | **CLEAN** |
| Mission Runtime | ERE + `CertifiedMissionEngine` | accept/defer/complete + selection | **DUPLICATE** residuals |

---

## Performance Review

| Surface | Finding | Action |
|---|---|---|
| Home / Workspace | Multiple engine evaluates per request; failures fail quiet | Acceptable for dogfood; optional cache later (F1 HOLD) |
| Knowledge Graph | Certified learner graph + KA overlay | Prefer package graph — **PASS** pattern |
| Educational Authoring | Scoped to mission context | **PASS** |
| Founder V1 Readiness | Static snapshot, no DB fan-out | **PASS** |
| Founder Platform Intelligence | Metrics aggregations remain request-scoped | Monitor; not changed in V1S-001 |

---

## Release Criteria

Canonical checklist: [`V1_RELEASE_CRITERIA.md`](V1_RELEASE_CRITERIA.md).

Founder UI: `/founder/v1-readiness`.

Provisional dimension scores (not validated KSI/CRI):

| Dimension | Score | Status |
|---|---|---|
| Architecture completeness | 78 | HOLD |
| Technical debt | 62 | IN_PROGRESS |
| Presentation quality | 84 | PASS |
| Educational completeness | 80 | HOLD |
| Commercial readiness | 55 | HOLD |
| Risk assessment | 70 | HOLD |

---

## Known Limitations

1. Does **not** retire Runtime A JSON curriculum authority.  
2. Does **not** delete Mission Engine packages.  
3. Does **not** claim Gate G1 / production-ready.  
4. Does **not** add new educational intelligence.  
5. Journey naming dual-surface remains by design (syllabus vs story) with clearer labels only.  
6. Latent templates / unused CSS not deleted in this pass.  
7. Progress singularity unfinished.

---

## Recommendation

1. **Start founder/internal dogfooding** on Adaptive Study Workspace with one curriculum authority per subject.  
2. Treat `/founder/v1-readiness` + `V1_RELEASE_CRITERIA.md` as the weekly readiness board.  
3. Next programmes (suggested order):  
   - **Curriculum authority cutover** (close A3)  
   - **Mission Runtime consolidation** (retire unwired ME packages)  
   - **Progress singularity completion**  
   - **Latent template / CSS prune**  
4. Do **not** market or declare Version 1 production-ready until P-002.1 G1–G12 and Launch criteria pass.

---

## Files Created

- `V1_RELEASE_CRITERIA.md`  
- `V1S001_IMPLEMENTATION_REPORT.md`  
- `app/services/v1_readiness_dashboard.py`  
- `app/founder/dashboard/templates/founder_dashboard/v1_readiness.html`  

## Files Modified

- Student templates and presentation modules listed above  
- `app/services/curriculum_engine_service.py`  
- `app/founder/dashboard/nav.py`  
- `app/founder/dashboard/routes.py`  
- Related certification / DX / SR tests  

## Tests Executed

```
python3 -m pytest tests/test_dx006b_student_home.py \
  tests/test_sr002_session_spine.py \
  tests/certification/test_pr001b_student_pilot.py \
  tests/test_kwp002_student_value_activation.py -q
```

Outcome: **57 passed**. Ruff clean on touched Python modules.

Also fixed latent defects uncovered during polish:

- Premature `{% endif %}` on Home that severed Tomorrow Preview from the non-empty branch
- History template referencing undefined `history` before `page.history` set
- Diagnostics guidance leaking “practice evidence” into student Current Focus

## Migration Impact

**None** — no Alembic / schema changes.

## Architecture Compliance

- Layering preserved: presentation polish + founder observability only; no educational law rewrite.  
- Curriculum V1/V2 **format** compatibility preserved (ADR-003).  
- Curriculum **authority** singularity intentionally HOLD — documented, not falsely claimed.

## Technical Debt

See Technical Debt table above (honest residual).

---

## Success criteria (programme)

| Criterion | Result |
|---|---|
| One curriculum (loader) | PASS |
| One curriculum (student authority) | HOLD |
| One educational architecture (KWP owners) | PASS with Mission/Progress debt |
| One presentation philosophy | PASS (workspace system + language polish) |
| One product language | PASS on audited surfaces |
| One commercial identity | HOLD — dogfoodable, not launch-ready |

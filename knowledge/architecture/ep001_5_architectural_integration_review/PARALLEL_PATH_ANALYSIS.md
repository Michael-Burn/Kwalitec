# EP-001.5 — Parallel Path Analysis

**Milestone:** EP-001.5  
**Review area:** Legacy paths, duplicate consumers, compatibility layers  
**Date:** 2026-07-26

Legend: **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Twin stacks (coexistence)

| Stack | Path | EP-001 role | Removal recommendation |
|---|---|---|---|
| MS-004 + EP-001.1 Foundation | `app/infrastructure/adapters/digital_twin/` | **Active substrate** | Keep |
| ExperienceTwinAdapter | `app/infrastructure/adapters/student_twin/experience_adapter.py` | Default UX TwinPort | Keep until Authority soak |
| StudentTwinProjectionPort (T5) | `digital_twin/experience_projection.py` | Additive DI; not `composition.twin` | Keep; do not confuse with Authority |
| Epic Twin | `app/domain/twin/` | Constitutional aggregate vocabulary | Keep as domain reference |
| V2 StudentTwinEngine | `app/domain/student_twin/`, `app/application/student_twin/` | Parallel non-authority | Do **not** promote; eventual quarantine/docs-only |
| EOS Educational Digital Twin | `src/domain/education/digital_twin/` | Education OS; not Flask Runtime A SoT | Keep isolated; no merge into EP-001 |
| StudentTwinAdapter (orchestrator) | `student_twin/adapter.py` | Learning Orchestrator TwinPort | Out of EP-001 scope |

**C:** EP-001 correctly extended MS-004 and did **not** introduce a fourth Twin domain. Parallel stacks remain inventory debt, not integration failure.

---

## 2. Planning / readiness / recommendation dual paths

| Domain | Legacy (production HTTP) | EP-001 path | Callers of EP-001 path |
|---|---|---|---|
| Planning | `PlanningService.generate_today_mission` | `build_daily_study_plan` | Internal weak-label + readiness/insight resolvers + tests; MissionOptimizer |
| Mission balancing | (legacy AdaptiveLearning in MissionOptimizer) | `MissionOptimizer._from_canonical_plan` | **No production callers** of `generate_balanced_mission` |
| Readiness | `get_overall_readiness` (+ weak/strong) | `build_readiness_intelligence` | Insight resolver + tests |
| Recommendations | `generate_recommendations` | `build_study_insights` | **Tests only** |
| Explainability | `EducationalExplainabilityService` | Insight layer (presentation) | Parallel |

**E:** HTTP routes under `app/dashboard/routes.py`, `app/mission/routes.py`, `app/analytics/routes.py`, `app/settings/routes.py` call legacy APIs.  
**E:** Grep for `build_study_insights` / `build_readiness_intelligence` / `build_daily_study_plan` in `app/` shows service + adapter usage only — no routes.

---

## 3. Temporary compatibility layers

| Layer | Purpose | Temporary? | Remove when |
|---|---|---|---|
| Twin OFF → `build_*` returns `None` | Fail-open to legacy | Yes (until cutover) | After HTTP cutover soak |
| Authority fallback to ExperienceTwinAdapter | Safe Experience cutover | Yes | After Authority soak removes demo-seed risk |
| Legacy getters for `ReadinessCollector` | Avoid Foundation recursion | **Long-lived** | Only after collector refactor |
| MissionOptimizer canonical branch | Optional balanced mission | Orphaned | Wire or delete in a follow-up chore |
| Partial insight limitation codes | Honest incomplete guidance | Permanent pattern | Keep |

---

## 4. Recommended removals / consolidations

| Priority | Action | Risk |
|---|---|---|
| P1 | Do **not** remove legacy HTTP paths yet | High if premature |
| P2 | Decide fate of `MissionOptimizer.generate_balanced_mission` (wire to a caller or mark dead) | Low |
| P3 | Quarantine / document V2 student_twin as non-runtime for Flask product | Medium (confusion) |
| P4 | Plan cutover of dashboard recommendations → `build_study_insights` behind Twin | Medium |
| P5 | Consolidate `EducationalExplainabilityService` vs EP-001.4 as single presentation SoT | Medium |
| P6 | Align Shadow/Adaptive-input docs with bundled Twin flag | Low |

**C:** Parallel paths are **expected** at this assurance stage. Premature removal would violate fail-open design. The primary consolidation opportunity is **product surface cutover**, not package deletion.

# EP-002.8 — UI Surface Inventory

**Milestone:** EP-002.8  
**Date:** 2026-07-26

## Runtime A surfaces in scope

| Surface | Route | Template | Twin cutover | Narration (post-EP-002.8) |
|---|---|---|---|---|
| Student Dashboard | `dashboard.index` `/dashboard/` | `dashboard/index.html` | Insights + Readiness + Daily Plan | `RuntimeAPresentationAdapter` |
| Analytics | `analytics.index` `/analytics/` | `analytics/index.html` | Readiness | Adapter (readiness + topics) |
| Today's Mission | `mission.missions` `/missions/` | `mission/index.html` | Daily Plan | Adapter (mission narrative) |
| Explainability macro | — | `partials/educational_explainability.html` | Shared | Unchanged macro |
| Mission session start | `mission.start_study_session` | `mission/session.html` | None (ORM) | EIP-003 direct |
| Practice outcome | mission practice routes | `session_practice_outcome.html` | None | Form / service |
| Session recorded | feedback | `session_recorded.html` | None | EIP-003 via StudySessionService |

## Out of inventory (explicit)

| Surface | Reason |
|---|---|
| `/student/*` Experience Home | SOLE_RUNTIME / Experience stack |
| Curriculum Studio | Unrelated product surface |
| Founder dashboard | Admin |
| Education OS `src/presentation/` | Separate stack |

## Projection DTOs consumed

| DTO producer | Marker | Consumers |
|---|---|---|
| `project_study_insights_to_recommendations` | `source_authority=study_insights` | Dashboard recommendations |
| `project_readiness_intelligence_to_surface` | `source_authority=readiness_intelligence` | Dashboard + Analytics |
| `project_daily_plan_to_mission_surface` | `source_authority=daily_study_plan` | Dashboard + Mission |
| Legacy service surfaces | `source_authority=legacy` | All of the above (fail-open) |

## Duplicate components removed / centralised

| Component | Before | After |
|---|---|---|
| Recommendation enrich branch | Inline dashboard | Adapter |
| Topic enrich branch | Dashboard + Analytics | Adapter |
| Readiness composite | Dashboard + Analytics always EIP-003 | Adapter selects Twin vs EIP-003 |
| Mission Twin/legacy branch | Dashboard + Mission duplicated | Adapter |
| Twin `SimpleNamespace` | Ad-hoc | `MissionNarrative` |

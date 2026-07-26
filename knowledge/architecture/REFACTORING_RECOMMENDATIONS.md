# MS-001 — Refactoring Recommendations

**Milestone:** MS-001 — Foundational Trust  
**Status:** Architecture Investigation (read-only)  
**Constraint:** This document recommends; it does **not** implement.

Investigation companions: `NAVIGATION_AUDIT.md`, `NAVIGATION_GRAPH.md`, `SESSION_LIFECYCLE.md`, `SOURCE_OF_TRUTH_ANALYSIS.md`, `SERVICE_DEPENDENCY_MAP.md`, `UI_INVENTORY.md`.

---

## Final summary

### 1. Current architecture strengths

- Clear **layering intent**: thin presentation → application facades → ports/adapters; legacy blueprints → services → models/curriculum.  
- **Deterministic** legacy planning and recommendations (no opaque LLM in core path).  
- **Canonical topic traversal** concentrated in `CurriculumService.get_next_incomplete_topic` / ordered helpers.  
- **Sole-runtime gate** is centralized (`consolidation.redirect_if_sole_runtime`) rather than ad-hoc per template.  
- Canonical session **resume** is explicit (`SessionWorkspace.active_surface` + `resume_redirect_if_needed`) — better than URL-only.  
- Evidence Authority on legacy mastery updates protects educational integrity.  
- Student/Session Experience facades correctly refuse educational ownership (projection-only), which is the right seam for a future bridge.

### 2. Current architecture weaknesses

- **Two live study stacks** with independent session identities.  
- **Sole runtime switches chrome, not truth** — default V2 Home is demo-seeded.  
- **Two “next” producers** on legacy (Planning mission vs Recommendation card) already disagree by design.  
- **In-memory** session/experience stores by default → resume loss across workers/restarts.  
- **Fat routes** (dashboard/mission) compose many services.  
- **Circular** Planning ↔ StudyPlan (lazy import papering).  
- **Unwired** MissionEngine / MissionEngineV2 / underfed AdaptiveDecisionEngine add cognitive load.  
- Calibration/onboarding still target `dashboard.index` (double-hop under sole runtime).  
- Welcome modal still points at legacy missions.

### 3. Sources of duplication

| Duplicate | Instances |
|---|---|
| Start-study UX | Dashboard CTA, Mission hub, Student Home, Revision begin |
| Session lifecycle | Mission.status + StudySessionService vs SessionWorkspace + ExperienceMissionAdapter |
| Next-action logic | PlanningService, RecommendationService, Adaptive demo / AdaptiveDecisionEngine |
| Topic sequencing | Leaf incomplete order vs Kahn week-plan sequence |
| Readiness display | ReadinessService/TopicProgress vs Twin opaque readiness |
| Nav trees | Legacy vs canonical branches in `sidebar.html` |
| Mission domain packages | SQL MissionService vs Experience adapter vs MissionEngine* |

### 4. Technical risks

| Risk | Severity | Why |
|---|---|---|
| Enabling `SOLE_RUNTIME` without SQL bridge | **Critical** | Students study fabricated content; real Mission/TopicProgress diverge |
| Multi-worker deploy with in-memory SessionWorkspace | **High** | Resume redirects wrong or session “missing” |
| Retiring legacy finish before Evidence parity | **High** | Mastery updates stop; readiness freezes |
| Unifying recommendation + mission without product rules | **Medium** | Behaviour change students notice |
| Import-cycle cleanup without tests | **Medium** | Startup / circular import regressions |
| Deleting MissionEngine* prematurely | **Low–Medium** | May be intended future; confirm product intent |

### 5. Recommended refactoring order (safest first)

1. **Document + test the contract** — freeze “authoritative next” and “authoritative session” as product decisions (this investigation).  
2. **Bridge adapters (read path)** — `MissionPort.get_todays_session` and Twin/Adaptive ports read real `PlanningService` / `Mission` / `TopicProgress` / `RecommendationService` (or one chosen authority). Keep writes on legacy first.  
3. **Disable or gate demo seeding** in non-demo environments (`SEED_DEMO_LEARNERS=false` when bridged).  
4. **Bridge adapters (write path)** — canonical `start_session` / `complete_session` / practice outcomes mutate SQL Mission + Evidence/TopicProgress.  
5. **Enable durable stores** for SessionWorkspace / projections in any multi-instance deploy.  
6. **Retarget shared flows** — calibration, onboarding, welcome modal → `student.home` when sole runtime.  
7. **Collapse dual “next”** on legacy — Recommendation card consumes mission topic or vice versa under one policy.  
8. **Extract topic label helper** from Planning private methods.  
9. **Break Planning ↔ StudyPlan cycle** via shared module or unidirectional API.  
10. **Sole runtime as default** only after bridge E2E proofs.  
11. **Remove legacy UI** (mission templates, study_session.js, sidebar legacy branch) behind flag.  
12. **Archive or wire** MissionEngine* / decide AdaptiveDecisionEngine vs RecommendationService.

### 6. Highest priority improvements

1. **Production bridge from Experience ports → legacy SQL educational services** (read then write).  
2. **Do not treat SOLE_RUNTIME as done** until Home CTA starts the student’s real today’s mission.  
3. **Durable session resume store** before sole-runtime production.  
4. **Single navigation entry** for “Start studying” (Home CTA) with all other CTAs redirecting to it.  
5. **Parity for practice outcome / mastery** on the canonical complete path.

### 7. Risks of refactoring

| Change | Risk if done carelessly |
|---|---|
| Bridge write-through | Double-start sessions; status desync; IDOR if ownership checks diverge |
| Kill RecommendationService early | Dashboard/analytics narratives empty; Decision journal unused |
| Force AdaptiveDecisionEngine | Different priority policy than students know; exam timeline rules may shift |
| Delete legacy mission UI before write bridge | Loss of Evidence-gated outcome capture UX |
| Enable durable store without migration | Empty projections; students appear “new” |
| Big-bang sole runtime | Support burden; beta evidence invalidation |

### 8. Estimated implementation complexity

| Workstream | Complexity | Rough effort (eng) |
|---|---|---|
| Read-only bridge adapters + flags | **M** | 3–8 days |
| Write-through start/complete + tests | **L** | 1–2 weeks |
| Practice outcome / Evidence parity on Session complete | **L–XL** | 2–4 weeks |
| Durable store hardening + multi-worker verification | **M** | 3–5 days |
| Shared flow retargets (calibration/onboarding/welcome) | **S** | 1–2 days |
| Unify recommendation vs mission policy | **M** | 3–7 days (product + eng) |
| Legacy UI removal under flag | **S–M** | 2–5 days |
| Planning/StudyPlan cycle + label extraction | **S** | 1–3 days |
| MissionEngine archive or wire decision | **S** (archive) / **XL** (wire) | decision-dependent |

**Overall MS-001 implementation (Foundational Trust end-state):** **L–XL**, dominated by write-path + Evidence parity — not by deleting templates.

---

## Components: remain vs remove

### Remain (canonical product surface)

- `student` + `session` blueprints and templates  
- `CurriculumService` traversal as topic-order SoT  
- Evidence Authority + TopicProgress as mastery SoT (until a migrated replacement exists)  
- Study Plan + Calibration as setup workflow  
- Sole-runtime consolidation helper  

### Remain (temporarily, as system of record)

- `PlanningService` / `MissionService` / `StudySessionService` until write bridge complete  
- Legacy finish/outcome templates until canonical Evidence parity  

### Remove (after bridge + sole-runtime proof)

- Legacy sidebar branch; dashboard as student home  
- Mission study UI + `study_session.js`  
- Demo seeding in production paths  
- Dead presentation links to `/missions/` for study start  

### Decide explicitly (do not silently delete)

- `RecommendationService` vs AdaptiveDecisionEngine  
- `app/application/mission_engine*` packages  

---

## Success criteria checklist (investigation)

| Criterion | Status |
|---|---|
| Where every study session begins | Documented in `NAVIGATION_AUDIT.md` |
| Who owns every navigation decision | Documented (flag / Planning / ports / workspace) |
| Whether there is a single source of truth | **No** — `SOURCE_OF_TRUTH_ANALYSIS.md` |
| Where duplication exists | Catalogued above + SoT doc |
| Which components should remain | This section + `UI_INVENTORY.md` |
| Which components should be removed | This section + `UI_INVENTORY.md` |
| Safest refactoring order | §5 above |

---

## Stop condition

Investigation complete. **No production code was modified** under this directive.

# EP-002.8 — Architecture Discovery Report

**Milestone:** EP-002.8 — Presentation Consolidation  
**Date:** 2026-07-26  
**Nature:** Mandatory discovery before implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Scope of discovery

Reviewed:

| Artefact | Path / location |
|---|---|
| Programme Constitutional Review (EP-002.7A) | **Not present in repo** — EP-002.7 constitutional pack used as surrogate |
| EP-001.5 Architectural Integration Review | `knowledge/architecture/ep001_5_architectural_integration_review/` |
| EP-002 Programme Brief | `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md` |
| EP-002.1–7 Completion Reports | `knowledge/architecture/ep002_* /COMPLETION_REPORT.md` |
| Architecture Constitution | `docs/ARCHITECTURE_CONSTITUTION.md` |
| EIP-003 Educational Explainability | `knowledge/educational/EDUCATIONAL_EXPLAINABILITY_STANDARD.md` |
| Explainability boundaries | `knowledge/explainability/EXPLAINABILITY_BOUNDARIES.md` |
| Dashboard / Analytics / Mission routes | `app/dashboard/routes.py`, `app/analytics/routes.py`, `app/mission/routes.py` |
| EducationalExplainability | `app/services/educational_explainability_service.py` |
| Consumer Chain cutovers | `app/infrastructure/adapters/consumer_chain/{cutover,readiness_cutover,daily_plan_cutover}.py` |
| Feature flags | `app/application/config/v2_flags.py`, `.env.example` |
| Presentation layer | `app/presentation/` |
| Templates | `app/templates/{dashboard,analytics,mission}/`, `partials/educational_explainability.html` |

**O:** No `EP-002.7A` / “Programme Constitutional Review” artefact exists.  
**E:** Repo-wide search returns zero matches for `EP-002.7A`.  
**C:** Discovery proceeds on EP-002.7 constitutional impact/gap + EP-001.5 authority matrix + Architecture Constitution.  
**R:** Document absence in Constitutional Drift Register; do not invent EP-002.7A findings.

---

## 2. Programme expectation for EP-002.8

**O:** EP-002.8 is WS7 — Presentation consolidation under Phase P5.  
**E:** `PROGRAMME_BRIEF.md` objective O5: “Collapse dual presentation **without inventing a third narrator**”; dependency gate WS4→WS5→WS6→WS7→WS8.  
**E:** EP-002.7 health gate `ready_for_ep002_8_presentation`; recommendation: plan EP-002.8 after staging soak.  
**C:** This milestone consolidates presentation selection/routing — not planning, readiness maths, or insight generation.  
**R:** Implement a presentation facade that selects communication by `source_authority`; keep cutover flags and fail-open unchanged.

---

## 3. Authority matrix (binding)

| Concern | Owner | Must not |
|---|---|---|
| Presentation / template shaping | Presentation layer (`app/presentation/`, blueprints) | Own evaluation / planning / insight maths |
| Student guidance copy (Twin ON + Insights cutover) | `RecommendationService` + EP-001.4 Insight | Re-narrate via EIP-003 when Twin owns communication |
| Readiness evaluation | `ReadinessService` + EP-001.3 | Migrate evaluation into templates or presentation |
| Daily planning | `PlanningService` + EP-001.2 | Migrate planning into presentation |
| Consumer Chain | Orchestration / dual-run / cutover / telemetry | Invent educational authority |
| Legacy ORM narration (fail-open) | `EducationalExplainabilityService` (EIP-003) | Recalculate scores or invent certainty |
| EI Stage A card | `EducationalDashboardComposer` / `RecommendationCardBuilder` | Claim EP-002 Runtime A authority |

**O:** Partial `source_authority` skips already exist in routes (EP-002.5–7).  
**E:** `dashboard/routes.py` skips enrich for `study_insights` / `readiness_intelligence` topic rows / `daily_study_plan` mission narrative; still always calls `explain_composite_readiness`.  
**C:** Residual dual-narration is concentrated in readiness composite narrative (TD-RI-02) and duplicated mission-branching across dashboard + mission routes.  
**R:** Centralise selection; complete Twin readiness narrative mapping; deduplicate mission narrative helper.

---

## 4. Presentation duplication inventory

| ID | Duplication | Locations | Severity |
|---|---|---|---|
| D1 | Insight vs EducationalExplainability on recommendations | Dashboard (partial skip) | Residual — selection logic duplicated in route |
| D2 | Readiness composite always EIP-003 | Dashboard + Analytics | **TD-RI-02 — open** |
| D3 | Mission narrative Twin/legacy branch copied twice | `dashboard/routes.py`, `mission/routes.py` | Ownership-safe but DRY debt |
| D4 | Ad-hoc Twin `SimpleNamespace` mission narrator | Same two routes | Third ad-hoc shape vs `MissionNarrative` |
| D5 | EI card vs Runtime A rec lists | Dashboard mutual exclusion | **TD-CO-02** — orthogonal Stage A |
| D6 | Topic-row enrich skip duplicated | Dashboard + Analytics | DRY debt |
| D7 | Student Experience `ExplanationService` | `/student/*` | Out of Runtime A cutover scope (SOLE_RUNTIME separate) |

**O:** Session sub-routes always use `EducationalExplainabilityService.build_mission_narrative` for a concrete ORM mission.  
**E:** `mission/routes.py` `_session_context_for_mission`.  
**C:** Correct — session pages operate on persisted Mission ORM, not Twin display overlay. Leave as legacy adapter.  
**R:** Do not force Twin authority onto session start/feedback.

---

## 5. Feature flags (unchanged by this milestone)

| Env | Flag | Default | Role |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | Required for Twin paths |
| `KWALITEC_STUDY_INSIGHTS_CUTOVER` | `ENABLE_STUDY_INSIGHTS_CUTOVER` | OFF | Dashboard recommendations Twin |
| `KWALITEC_READINESS_INTELLIGENCE_CUTOVER` | `ENABLE_READINESS_INTELLIGENCE_CUTOVER` | OFF | Dashboard + Analytics readiness Twin |
| `KWALITEC_DAILY_PLAN_CUTOVER` | `ENABLE_DAILY_PLAN_CUTOVER` | OFF | Dashboard + Mission Twin plan |
| `KWALITEC_V2_SOLE_RUNTIME` | `SOLE_RUNTIME` | OFF | Redirects to `/student/*` |
| EI orchestrator flags | Stage A | OFF | EI recommendation card |

**C / R:** EP-002.8 must not add production-wide activation or new domain engines. No new cutover flag required — consolidation is presentation selection only.

---

## 6. EducationalExplainability constitutional role

**O:** EIP-003 binds presentation/coaching copy only; does not own evaluation.  
**E:** `EDUCATIONAL_EXPLAINABILITY_STANDARD.md`; service docstring.  
**O:** EP-001.4 Insight owns Twin-path student guidance communication.  
**E:** Authority matrix AD-03; Programme O5.  
**C:** Outcome **B** — EducationalExplainability becomes the **legacy presentation adapter** invoked when `source_authority == legacy` (and for coverage/session paths that remain ORM-backed). Not deprecated (C) while fail-open exists; not a parallel peer SoT (A) for Twin-served surfaces.  
**R:** Route all Runtime A surface narration through one presentation facade that delegates to EIP-003 or Twin projection fields.

---

## 7. Constitutional conflict check

| Potential conflict | Found? | Disposition |
|---|---|---|
| Presentation owns evaluation | No | Adapter maps fields only |
| Insight invents readiness/plans | No | Out of scope; untouched |
| Third narrator invented | Avoided | Selection facade ≠ new speech engine |
| Delete legacy fail-open | No | Legacy path retained |
| MissionOptimizer un-quarantine | No | Out of scope |
| Schema / persistence change | No | Presentation-only |
| EP-002.7A missing | Yes (artefact gap) | Document; not a STOP for consolidation |

**C:** **No STOP condition.** Safe to implement consolidation design.

---

## 8. Discovery recommendations (binding for implementation)

1. Introduce `app/presentation/intelligence_surface/` with `RuntimeAPresentationAdapter`.
2. Select communication by `source_authority` for readiness, recommendations, mission, topic rows.
3. Map Twin readiness surface fields → `ReadinessNarrative` (close TD-RI-02).
4. Return `MissionNarrative` for Twin mission path (retire ad-hoc `SimpleNamespace`).
5. Keep EducationalExplainability as legacy adapter; update docstring.
6. Preserve EI mutual exclusion; document TD-CO-02 as Stage A residual (not Runtime A dual narrator).
7. No flag defaults changed; no production activation; no migrations.
8. Add presentation regression / flag / fallback / a11y tests.

---

## 9. Explicit non-claims

- Not Twin Ready (T7)
- Not production cutover ON
- Not retirement of `/student/*` Experience narrators
- Not redesign of EP-001.1–4 contracts
- Not MissionOptimizer reactivation

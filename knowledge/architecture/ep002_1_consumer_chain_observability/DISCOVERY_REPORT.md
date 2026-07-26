# EP-002.1 — Architecture Discovery Report

**Milestone:** EP-002.1 — Consumer-Chain Observability & Twin Quarantine  
**Date:** 2026-07-26  
**Nature:** Mandatory discovery before implementation  
**Legend:** **O** = observation · **E** = evidence · **C** = conclusion · **R** = recommendation

---

## 1. Scope of discovery

Reviewed:

| Artefact | Path / location |
|---|---|
| EP-001.5 Architectural Integration Review | `knowledge/architecture/ep001_5_architectural_integration_review/` |
| EP-002 Programme Brief | `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md` |
| Student Digital Twin Architecture | `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md` |
| Digital Twin Interface Spec | `knowledge/architecture/DIGITAL_TWIN_INTERFACE_SPECIFICATION.md` |
| Feature flag review (EP-001.5) | `FEATURE_FLAG_REVIEW.md` |
| Runtime A RecommendationService | `app/services/recommendation_service.py` |
| PlanningService | `app/services/planning_service.py` |
| ReadinessService | `app/services/readiness_service.py` |
| MS-004 Foundation package | `app/infrastructure/adapters/digital_twin/` |
| V2 flags | `app/application/config/v2_flags.py` |
| Existing telemetry / diagnostics | `app/infrastructure/diagnostics/`, `*/telemetry.py`, `events/` |

---

## 2. Consumer-chain entry points

| API | Host service | Package(s) | Twin gate |
|---|---|---|---|
| `build_daily_study_plan` | `PlanningService` | `adaptive_study_planner/` | `ENABLE_DIGITAL_TWIN`; returns `None` when OFF / unavailable |
| `build_readiness_intelligence` | `ReadinessService` | `readiness_intelligence/` | Same |
| `build_study_insights` | `RecommendationService` | `insight_recommendation/` | Same |

**O:** Nested resolve — Insight may call Readiness which may call Planner; each reassembles Foundation unless injected.

**E:** No HTTP route callers of `build_*` (EP-001.5 IF-06 / TD-OPS-01). Legacy HTTP still uses `generate_today_mission`, `get_overall_readiness`, `generate_recommendations`.

**C:** Observability must wrap Runtime A `build_*` hosts — not invent HTTP cutover.

---

## 3. Existing logging

| Location | Behaviour |
|---|---|
| Module `logging.getLogger(__name__)` in the three services | Info/debug on missing plan / unavailable CLS; exception debug on Foundation resolve failure |
| HTTP observability | `http_observability.py` — correlation + duration at Flask boundary |
| Experience diagnostics | StructuredLogger + optional EventRegistry (P2-MS007) |

**C:** Service-level `build_*` has only ad-hoc debug/info logs — no structured outcome / latency / limitation matrix.

---

## 4. Existing telemetry / metrics

| Infrastructure | Role | Reuse for EP-002.1? |
|---|---|---|
| `StructuredLogger` + `CorrelationContext` | Operational structured fields | **Yes — primary log sink** |
| `EventRegistry` + `IntegrationEvent` | In-process observational events | **Yes — optional publish** |
| `*/shadow_telemetry.py`, bridge `*_telemetry.py` | Domain observational emitters | Pattern to mirror |
| `PipelineMetrics` / `AdapterDiagnostics` | Generic counters | Optional secondary; do not fork |
| `PresentationTelemetryService` | Product-surface DB events | **No** — product analytics; out of scope |
| Twin Shadow (`TWIN_SHADOW_*`) | Twin assemble observational | Related but not consumer-chain `build_*` |

**R:** Extend existing diagnostics + events catalogue. Do **not** add a second framework or analytics event catalogue.

---

## 5. Feature flags (implemented)

| Env | Flag | Default | Affects `build_*`? |
|---|---|---|---|
| `KWALITEC_DIGITAL_TWIN` | `ENABLE_DIGITAL_TWIN` | OFF | **Yes** — Foundation DI + `build_*` availability |
| `KWALITEC_DIGITAL_TWIN_AUTHORITY` | `ENABLE_DIGITAL_TWIN_AUTHORITY` | OFF (requires Twin ON) | **No** — Experience TwinPort only |

**O / E:** Docs still mention separate `KWALITEC_DIGITAL_TWIN_SHADOW` and `KWALITEC_DIGITAL_TWIN_ADAPTIVE_INPUT`. Code bundles Shadow + Adaptive TwinInput under Twin ON (EP-001.5 TD-ARCH-06).

**C:** No new feature flag is required for observability. Dual-run diagnostics can gate on Twin ON + non-production `APP_ENV`.

---

## 6. Twin stack inventory (quarantine need)

| Stack | Status | Authority for Runtime A product path? |
|---|---|---|
| MS-004 + EP-001.1 Foundation | Active substrate | **Yes — extend** |
| ExperienceTwinAdapter | Default Experience TwinPort | UX default until Authority soak |
| Epic `app/domain/twin` | Domain vocabulary | Historical / reference |
| V2 `student_twin` | Parallel bounded context | Experimental / non-authority |
| EOS `src/domain/education/digital_twin` | Education OS | Isolated; non-authority for Flask Runtime A |

**R:** Publish quarantine note (TD-ARCH-01) as part of this milestone.

---

## 7. Gap analysis (discovery → objectives)

| Engineer question | Current answerability | Gap |
|---|---|---|
| Was the API called? | Partial (ad-hoc logs) | Structured invocation event |
| How long did it take? | No | Latency field |
| Did it succeed? | No structured outcome | Outcome categories |
| Returned None? | Inferable only | Explicit availability flag |
| Limitation codes? | In payload only | Extracted into observability fields |
| Which flags active? | Not on `build_*` path | Twin + Authority in payload |

---

## 8. Implementation constraints (binding)

1. No business-logic / recommendation / readiness / planner algorithm changes.  
2. No HTTP route changes; no student-facing behaviour changes.  
3. No schema / migrations / new Twin / new planner / readiness / recommender.  
4. No new feature flags unless proven necessary — **not necessary**.  
5. Twin remains OFF by default; no production Authority flip.  
6. Dual-run comparison is diagnostic only — never alters returned payloads.  
7. Prefer fingerprint comparison helper over auto-invoking legacy writers inside `build_*`.

---

## 9. Discovery conclusions

| Question | Answer |
|---|---|
| Where to emit? | Wrap `PlanningService.build_daily_study_plan`, `ReadinessService.build_readiness_intelligence`, `RecommendationService.build_study_insights` |
| How to emit? | Shared `consumer_chain` observability module using `StructuredLogger` + optional `EventRegistry` + new `CONSUMER_CHAIN_*` event types |
| Dual-run? | Optional diagnostic helper; eligible when Twin ON and `APP_ENV` ≠ production; log fingerprints only |
| Docs? | Twin quarantine note + align Shadow/Adaptive TwinInput docs with bundled Twin flag |
| Ready to implement? | **Yes** |

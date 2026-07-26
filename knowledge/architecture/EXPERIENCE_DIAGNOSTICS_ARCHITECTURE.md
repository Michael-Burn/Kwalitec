# Programme II — Experience Observability & Diagnostics Architecture

**Milestone:** P2-MS007 — Experience Observability & Diagnostics  
**Directive:** Engineering Directive 001 (Experience Observability & Diagnostics)  
**Status:** Implemented  
**Package:** `app/infrastructure/adapters/experience_observation/`  
**Feature flag:** `KWALITEC_EXPERIENCE_DIAGNOSTICS` → `ENABLE_EXPERIENCE_DIAGNOSTICS` (**default OFF**)  
**Contract version:** `p2.ms007.1`  
**Companions:** `EXPERIENCE_OBSERVATION_ARCHITECTURE.md`, `UNIFIED_STUDENT_JOURNEY_ARCHITECTURE.md`, `LEARNING_EVIDENCE_PLATFORM_ARCHITECTURE.md`

---

## 0. Purpose

Provide **operational visibility** into the Unified Student Journey and Experience Observation pipeline.

> Every journey event and observation should be traceable from creation to Evidence intake.  
> Operators diagnose failures quickly while preserving student privacy and architectural boundaries.

This is an **Infrastructure and Experience Operations** milestone.

| In scope | Out of scope |
|---|---|
| Immutable `JourneyTrace` | Behavioural adaptation |
| Observation diagnostics counters | Evidence interpretation |
| Pipeline health checks | Runtime A / Strategy / Adaptive / Twin changes |
| Structured operational logging | Persistence / repositories |
| Internal diagnostics dashboard DTOs | Student-facing UI / analytics dashboards |
| `ENABLE_EXPERIENCE_DIAGNOSTICS` | Educational authority |

**Stop condition:** Stop after Experience Observability & Diagnostics. Await architecture review before introducing any Evidence-driven behavioural adaptation.

---

## 1. Components

| Component | Location | Responsibility | Non-responsibility |
|---|---|---|---|
| `JourneyTrace` | `journey_trace.py` | Immutable operational pipeline step | Student PII, educational conclusions |
| `JourneyTraceStore` | `journey_trace.py` | Bounded in-memory ring buffer | Persistence |
| `ObservationDiagnosticsService` | `diagnostics.py` | Counters, traces, dashboard aggregation | Educational scoring |
| `PipelineHealthChecker` | `health.py` | Publisher / Evidence / flags / DI checks | Student UX gates |
| `ExperienceDiagnosticsLogger` | `telemetry.py` | Structured logs + IntegrationEvents | Mastery / recommendation logs |
| `ExperienceDiagnosticsDashboard` | `dashboard.py` | Internal-only presentation DTO | Student templates / public APIs |
| DI helper | `build_experience_observation_diagnostics` | Construct when flag ON | Auto-enable observation publish |

---

## 2. Trace lifecycle

```
JourneyEvent (presentation)
        │
        ▼
record_journey_event  → JourneyTrace (pipeline_stage=journey_event, status=pending)
        │
        ▼
ObservationAssembler  → ExperienceObservation
        │
        ▼
JourneyTrace (pipeline_stage=assembled, status=pending)
        │
        ▼
ExperienceObservationPublisher.publish
        │
        ├─ skip paths → JourneyTrace (pipeline_stage=skipped)
        │
        ▼
JourneyTrace (pipeline_stage=publish_attempted)   ← Evidence collect_event timed
        │
        ├─ accepted → JourneyTrace (pipeline_stage=evidence_ack, status=published)
        └─ rejected → JourneyTrace (pipeline_stage=failed, status=failed)
```

### Suggested fields (directive)

| Field | Role |
|---|---|
| `trace_id` | Deterministic hash of operational material fields (`jtrace-…`) |
| `correlation_id` | Request / pipeline linkage (`CorrelationContext` or explicit) |
| `journey_stage` | Presentation stage (e.g. `daily_mission`) |
| `experience_event` | Presentation event (e.g. `session_started`) |
| `observation_status` | `pending` / `published` / `skipped` / `failed` |
| `timestamp` | Explicit ISO timestamp from caller (no wall-clock invent) |
| `pipeline_stage` | `journey_event` / `assembled` / `publish_attempted` / `evidence_ack` / `skipped` / `failed` |

Optional operational refs (still non-PII): `observation_id`, `evidence_id`, `reason`, `latency_ms`.

**Privacy invariant:** `JourneyTrace` never stores `student_id`, email, or user identifiers.

---

## 3. Correlation strategy

1. Callers pass `correlation_id` into `publish_journey_event` / session / reflection helpers.
2. When omitted, publisher falls back to `CorrelationContext.get_correlation_id()` (HTTP hooks bind `X-Correlation-ID` / `X-Request-ID`).
3. Every `JourneyTrace` and structured log record carries the same correlation id for lineage queries via `ObservationDiagnosticsService.traces_for(correlation_id)`.
4. IntegrationEvents published by diagnostics also inherit `CorrelationContext`.

Correlation links **operational** artefacts only. It does not grant educational authority.

---

## 4. Observation diagnostics

`ObservationDiagnosticsService` exposes:

| Metric | Meaning |
|---|---|
| `observations_published` | Successful Evidence intakes |
| `observations_accepted` | Alias of published (Evidence ack received) |
| `observations_rejected` | Evidence intake raised / failed |
| `observations_skipped` | Flag off / not observable / Evidence unavailable |
| `journey_events_traced` | JourneyEvent entries recorded |
| Feature flag state | Diagnostics / Observation / Evidence / Unified Journey |
| Intake latency | `perf_counter` around `collect_event` (when measurable) |
| Publisher health | Availability, enabled, Evidence binding |

All counters are process-local and resettable for tests. No student-identifying fields.

---

## 5. Health model

`PipelineHealthChecker` evaluates four checks:

| Check | OK when |
|---|---|
| `observation_publisher` | Observation flag ON and publisher injected + enabled |
| `evidence_intake` | Evidence flag ON and adapter exposes `collect_event` |
| `feature_flag_consistency` | Diagnostics flag ON (independent matrix is valid) |
| `dependency_injection_wiring` | Publisher ↔ Evidence sink matches flag matrix |

Overall status: `ok` / `degraded` / `unavailable`.

Health never blocks student presentation flows — it is ops-facing only.

---

## 6. Logging conventions

Structured messages (via `StructuredLogger` + optional `EventRegistry`):

| Message | IntegrationEvent | Required fields |
|---|---|---|
| `experience_diagnostics.journey_event` | `EXPERIENCE_DIAG_JOURNEY_EVENT` | `correlation_id`, `journey_stage`, `experience_event` |
| `experience_diagnostics.observation_published` | `EXPERIENCE_DIAG_OBSERVATION_PUBLISHED` | `correlation_id`, `observation_status`, `experience_event` |
| `experience_diagnostics.evidence_ack` | `EXPERIENCE_DIAG_EVIDENCE_ACK` | `correlation_id`, `observation_status`, `evidence_id` (when accepted) |

Hard invariants on every record:

- `influences_student: false`
- No `student_id` / `email` / `user_id`
- No mastery, scores, recommendations, or educational conclusions

Publisher instrumentation is fail-safe: diagnostics exceptions are logged and swallowed so Experience controls continue.

---

## 7. Diagnostic dashboard model

`ExperienceDiagnosticsDashboard` is a **presentation-ready DTO for internal ops only**.

```
audience = "internal_ops"
influences_student = false
```

Contains: feature flags, counters, publisher health, pipeline health, recent traces.

**Must not** be exposed on student Experience routes, templates, or public APIs. Founder / ops tooling may consume `to_canonical_dict()` later; this milestone ships the model only.

---

## 8. Feature flags

| Environment | Resolved field | Default |
|---|---|---|
| `KWALITEC_EXPERIENCE_DIAGNOSTICS` | `ENABLE_EXPERIENCE_DIAGNOSTICS` | OFF |
| `KWALITEC_EXPERIENCE_OBSERVATION` | `ENABLE_EXPERIENCE_OBSERVATION` | OFF (independent) |
| `KWALITEC_EVIDENCE_PLATFORM` | `ENABLE_EVIDENCE_PLATFORM` | OFF (independent) |
| `KWALITEC_UNIFIED_JOURNEY` | `ENABLE_UNIFIED_JOURNEY` | OFF (independent) |

Behaviour matrix (illustrative):

| Diagnostics | Observation | Evidence | Result |
|---|---|---|---|
| OFF | * | * | No diagnostics service (`None`) |
| ON | OFF | * | Diagnostics reports publisher unavailable; no publish instrumentation |
| ON | ON | OFF | Publisher bound; publish skips; traces still record skip path |
| ON | ON | ON | Full JourneyTrace lifecycle + latency |

Dual-run ops field: `DualRunStatus.experience_diagnostics`.

---

## 9. Failure modes

| Condition | Diagnostics behaviour | Student impact |
|---|---|---|
| Diagnostics flag OFF | Service not constructed; publisher has no hooks | None |
| Observation publish skipped | Trace `skipped` + counter increment | None |
| Evidence intake rejects | Trace `failed` + rejected counter + warning log | None (publisher already fail-safe) |
| Diagnostics record throws | Warning logged; publish result still returned | None |
| Trace store at capacity | Oldest traces dropped (ring buffer) | None |

---

## 10. Operational responsibilities

| Role | Owns |
|---|---|
| Platform / SRE | Enable diagnostics in non-prod / canary; watch health + reject rates |
| Experience eng | Keep publisher instrumentation fail-safe; never put PII in traces |
| Evidence eng | Ensure public `collect_event` remains the only intake surface |
| Product / education | **No authority** — diagnostics never drive adaptation |

Operators may query:

```python
composition.experience_diagnostics.dashboard()
composition.experience_diagnostics.traces_for(correlation_id)
composition.experience_diagnostics.pipeline_health()
```

---

## 11. Composition / DI

`build_production_experience()` constructs diagnostics when `ENABLE_EXPERIENCE_DIAGNOSTICS` is ON, then late-binds it onto the publisher when present:

```python
experience_diagnostics = build_experience_observation_diagnostics(
    enabled=True,
    observation_flag=...,
    evidence_flag=...,
    publisher=experience_observation,
    evidence=evidence_platform,
    events=events,
)
if experience_observation is not None:
    experience_observation.bind_diagnostics(experience_diagnostics)
```

Stored on composition as `composition.experience_diagnostics`.

---

## 12. Tests

| Suite | Coverage |
|---|---|
| `test_journey_trace.py` | Immutability, deterministic ids, store / correlation |
| `test_diagnostics.py` | Health checks, counter aggregation, dashboard, DI helper |
| `test_diagnostics_logging_flags.py` | Logging contracts, PII exclusion, flag isolation, composition |
| `tests/application/config/test_v2_flags.py` | Flag default OFF + dual-run field |

---

## 13. Explicit non-goals (binding)

- Behavioural adaptation
- Evidence interpretation / scoring
- Runtime A changes
- Strategy / Adaptive / Digital Twin changes
- Persistence changes
- Student-facing UI
- Analytics dashboards
- Educational authority of any kind

# MIG-001 — Analytics Feature Status (PRD-001)

**Investigation date:** 2026-07-27  
**Scope:** Determine whether PRD-001 / analytics event infrastructure was cancelled, superseded, merged, abandoned, or still planned.

---

## Executive status

| Dimension | Status | Evidence |
|---|---|---|
| PRD | **Approved** v1.1 | `knowledge/prd/PRD-001_LEARNING_ANALYTICS_PHASE1.md` |
| Persistence ADR | **Accepted** | `docs/adr/ADR-025-analytics-event-infrastructure.md` |
| Phase A–E instrumentation | **Shipped** | `knowledge/product/analytics/README.md`; phase implementation reports |
| EP-002 operational readiness | **Shipped** | `knowledge/product/analytics/ep002/` |
| Feature flag | **OFF by default** | `ANALYTICS_EVENTS_V1` / `KWALITEC_ANALYTICS_EVENTS_V1` |
| Version 1 readiness row | **COMPLETE (ops ready; flag OFF)** | `knowledge/VERSION_1_READINESS.md` |
| Journey production emit | **Deferred** (not cancelled) | ADR-026 |
| Cancelled / abandoned / superseded schema | **No evidence** | Searches below |

**Conclusion:** PRD-001 is **not cancelled**. Implementation **merged into the codebase** and remains **planned for staged activation** behind the kill switch. Schema migration `202607240001` is part of that shipped contract.

---

## Programme timeline (evidence)

| When | What | Evidence |
|---|---|---|
| 2026-07-24 | PRD Approved v1.1 | PRD header |
| 2026-07-24 | Phase A commit + migration + ADR-025 | `0cf8541` |
| 2026-07-24+ | Phases B–E reports + ADR-026 | `knowledge/product/analytics/PHASE_*`, ADR-026 |
| EP-002 | Ops runbooks, privacy, worker, metrics | `knowledge/product/analytics/ep002/` |
| EP-003 / EP-004 / EP-008.2x | Treat analytics as prerequisite ops surface; flag remains OFF until go-live steps | Private beta / pilot docs |
| 2026-07-27 | RC1 commit includes later dual-head migration (commitments), not analytics removal | `65cb380` |

---

## Search results: cancelled / superseded / abandoned

Repository searches covered `knowledge/`, `docs/`, ADR, README, programme reports, and application code for cancel/abandon/supersede language around PRD-001 analytics tables.

Findings:

1. **No document declares PRD-001 cancelled or abandoned.**
2. **“Superseded” appears only for Journey event naming** (`journey.milestone_reached` → `journey.progressed` in ADR-026) — not for the analytics tables or Phase A migration.
3. **“Deferred”** applies to:
   - Journey *production* emit (ADR-026 / EVENT_CATALOGUE)
   - Some validation outcomes (O3/O8) out of PRD-001 scope
   - Flag-on production activation until go-live checklists complete
4. Older EP-001 README line saying “impl milestone not started” is **stale relative to later COMPLETE status** in `VERSION_1_READINESS.md` and analytics README “shipped”. Prefer the later COMPLETE evidence.

---

## What shipped with the migration

From `202607240001` + ADR-025 + Phase A report:

- `analytics_events` — append-only durable store
- `analytics_outbox` — fail-open enqueue / retry
- `analytics_audit_log` — purge / deletion / export / emit-failure audit (36-month policy)

Explicit non-goals preserved: does not alter Twin / EducationalState / Evidence / educational schema.

---

## Activation posture

| Item | Posture | Evidence |
|---|---|---|
| Default runtime writes | None (dispatcher no-op) | `feature_flag.py`; ADR-025 §6 |
| Emit call sites | Present (Session, Reflection, ESS, Twin, Journey helper) | `app/services/study_session_service.py`, `reflection_manager.py`, `educational_state`, twin/journey observation modules |
| Ops CLI | Registered | `app/__init__.py` imports `app.infrastructure.analytics.cli` |
| Pilot activation | Checklisted; not claimed production-ON in investigated docs | EP-002 / EP-008.2B go-live checklists |

Empty tables under flag OFF are **intentional capacity**, not unused accidental schema.

---

## Relationship to EP-008.3A

EP-008.3A (`recommendation_commitments`) is a **separate product surface** (preference/intent commitment). It does not replace analytics. Its migration `202607260001` is the other head and is orthogonal in schema (different tables). Dual heads are a **graph parenting error**, not a feature replacement.

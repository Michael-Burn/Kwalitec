# EP-002.8 — Presentation Consolidation Design

**Milestone:** EP-002.8  
**Date:** 2026-07-26  
**Status:** Binding for implementation

---

## 1. Design principle

> Presentation owns presentation. Insight owns communication (Twin path). Readiness owns evaluation. Planning owns planning. Consumer Chain owns orchestration.

Consolidation means **one selection facade**, not one speech engine that invents content.

---

## 2. Component

| Module | Role |
|---|---|
| `app/presentation/intelligence_surface/adapter.py` | `RuntimeAPresentationAdapter` — selects + shapes |
| `app/presentation/intelligence_surface/__init__.py` | Public exports |
| `EducationalExplainabilityService` | Legacy presentation adapter (EIP-003) |
| Consumer Chain projectors | Twin → surface DTOs (unchanged) |
| Templates | Consume narrative DTOs only (unchanged contracts) |

---

## 3. Selection matrix

| Input `source_authority` | Recommendations | Topic rows | Readiness narrative | Mission narrative |
|---|---|---|---|---|
| `legacy` | EIP-003 enrich | EIP-003 enrich | EIP-003 composite | EIP-003 mission |
| `study_insights` | Pass-through (Insight fields) | n/a | n/a | n/a |
| `readiness_intelligence` | n/a | Pass-through | Twin→`ReadinessNarrative` | n/a |
| `daily_study_plan` | n/a | n/a | n/a | Twin slot→`MissionNarrative` |

---

## 4. Twin readiness narrative mapping (presentation only)

From readiness surface DTO:

| Twin field | Narrative field |
|---|---|
| `readiness.score` | `percentage` (rounded display) |
| ProductCommunication labels | `label` (“Estimated readiness”) |
| `readiness_drivers` (id/value) | `evidence_basis` summary |
| `confidence_level` | Appended to `evidence_basis` |
| `recommended_next_actions` | Soft `explanation` continuation |
| Always | `is_estimate=True`, `can_estimate` from score presence |

Never recalculate score. Never invent driver values.

---

## 5. Twin mission narrative mapping

| Source | Narrative field |
|---|---|
| Display mission title | `next_action`, `topic_title` |
| Primary slot `reason` | `reason_for_selection`, `educational_purpose` |
| Slot topic ids / titles | `observed_facts` |
| Empty / honest defaults | `estimates` empty unless confidence present |
| Fallback copy | Only when reason missing (existing EP-002.7 strings) |

---

## 6. EducationalExplainability decision

**Outcome B — presentation adapter (legacy).**

- Remains for fail-open, coverage, session feedback, and any non-Twin surface.
- Invoked only through `RuntimeAPresentationAdapter` for Runtime A dashboard/analytics/mission index surfaces (coverage/session may call EIP-003 directly as ORM-only paths).
- Not deprecated while fail-open exists.
- EIP-003 speech rules remain the standard for legacy cohorts.

---

## 7. EI Stage A (TD-CO-02)

When `ENABLE_EDUCATIONAL_ORCHESTRATOR` produces a recommendation card:

- Runtime A recommendation lists remain hidden (existing mutual exclusion).
- EP-002.8 does **not** merge EI into Insight (different product stage / ownership).
- Residual accepted; tracked for post-programme product decision.

---

## 8. Rollback

Disable Twin and/or cutover flags → `source_authority=legacy` → facade delegates entirely to EIP-003. No code rollback required for behaviour restoration. No data/schema migration.

---

## 9. Out of scope (explicit)

- Foundation / Twin assemble changes
- Planning algorithms / MissionOptimizer
- Readiness calculations
- Study Insight generation
- Consumer Chain orchestration logic
- `/student/*` ExplanationService consolidation
- Production flag activation

# EP-001.1 — Implementation Plan

**Milestone:** EP-001.1 — Student Digital Twin Foundation  
**Phase:** 4 — Implementation Plan

---

## Goals

1. Establish a **canonical Student Digital Twin foundation read model**.
2. Cover: study state, topic mastery, topic progress, learning evidence, practice performance, mock performance (honest unavailable), study behaviour, study consistency, streaks, mission completion.
3. Prefer **extend / integrate** — reuse MS-004 collectors and evidence bag.
4. Keep Runtime A as transactional write SoT; Twin Foundation as consumer-facing learner-state SoT.
5. Add `ENABLE_DIGITAL_TWIN_AUTHORITY` (default OFF).

---

## Non-goals

- Redesign constitutional Twin philosophy
- Replace TopicProgress / Mission / StudyAttempt write paths
- Alembic schema for Foundation (recompute from Runtime A)
- Delete V2 or EOS Twin packages
- Flip Authority ON by default / declare MS-004 Twin Ready (T7)
- Invent mastery or mock scores

---

## Work packages

### WP1 — Documentation (Phases 1–3 artefacts)

Discovery, review, gap, plan under this folder.

### WP2 — Foundation contracts + assembler

| Module | Responsibility |
|---|---|
| `foundation.py` | `CanonicalLearnerState` + `StudentDigitalTwinFoundation` |
| Reuse | `TwinFacetAssembler` / `TwinRuntimeEvidence` / facet builders |

Assemble dimensions as **Runtime A pass-through** (+ MS-004 facet labels for behaviour/consistency). Never estimate missing values.

### WP3 — Streak pass-through

Extend `ReadinessCollector` payload with `current_streak` / `longest_streak` from `ReadinessService` (existing methods).

### WP4 — Authority seam

| Piece | Behaviour |
|---|---|
| Flag | `KWALITEC_DIGITAL_TWIN_AUTHORITY` → `ENABLE_DIGITAL_TWIN_AUTHORITY` |
| `authority.py` | `StudentTwinFoundationAuthorityPort` implements `StudentTwinPort` |
| Composition | When Twin + Authority ON → `composition.twin` = Authority port; disable demo Twin seeding |
| Fallback | On assemble failure → prior `ExperienceTwinAdapter` |

### WP5 — Tests

- Foundation unit: determinism, pass-through, unavailable mock
- Authority unit: flag isolation, fallback
- Flag resolution tests

### WP6 — Doc updates

README, architecture cross-links, `.env.example`.

---

## Success criteria mapping

| Criterion | How met |
|---|---|
| Single canonical Twin for consumers | `StudentDigitalTwinFoundation.assemble` + Authority port |
| Extend not replace | Builds on MS-004; no new domain package |
| Constitutional compliance | Evidence-only; honest unavailable; no Runtime A writes |
| Future subsystems read Twin | Documented Foundation API + optional Authority cutover |

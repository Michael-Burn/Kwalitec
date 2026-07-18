# Version 2 Migration Strategy

**Document ID:** V2-001-MIGRATE  
**Milestone:** V2-001 — Learning Journey Domain Architecture  
**Status:** Architectural migration map  
**Nature:** Concept mapping only — no database implementation  

**Parent:** [`VERSION2_ARCHITECTURE.md`](VERSION2_ARCHITECTURE.md)  
**Continuity law:** [`EDUCATIONAL_CONTINUITY_STANDARD.md`](../educational/EDUCATIONAL_CONTINUITY_STANDARD.md)

This document explains how Version 1 educational concepts evolve into Version 2 Learning Journey concepts. It does not prescribe Alembic revisions, ORM classes, dual-write code, or cutover flags.

---

## 1. Migration Philosophy

1. **Evolve, do not erase.** Version 1 learners keep working during coexistence.
2. **Learner history survives.** Plans and missions are containers; evidence and coverage belong to the learner.
3. **Map meanings before tables.** Wrong concept mapping cannot be fixed by clever SQL.
4. **No silent equivalence.** Where V1 data cannot objectively map, retain history and mark uncertainty.
5. **Behaviour cutover is a later milestone.** V2-001 changes documentation only.

---

## 2. Primary Concept Map

```
Study Plan                 →    Planning context + Journey portfolio constraints
                                      (not the journey itself)

Daily Mission              →    Journey Recommendation
                                      (daily commitment derived from journeys)

Study Session              →    Learning Session
                                      (bounded work inside a journey)

Topic Progress (coverage)  →    JourneyProgress + Topic Complete outcome

Current Learning Topic     →    Active Learning Journey pointer

Study Attempt / Evidence   →    JourneyEvidence (attributed) + global Evidence Model

Mission Review / feedback  →    JourneyReflection (generalised, required)
```

---

## 3. Study Plan → Learning Journey (clarified)

### What people might wrongly assume

That each Study Plan becomes one Learning Journey.

### Correct mapping

| Version 1 | Version 2 |
|-----------|-----------|
| Study Plan | Disposable **planning container**: exam date, availability, active curriculum, scheduling |
| Week plans / day slots | Capacity and calendar projections that **schedule** journey sessions |
| Active plan | Context that authorises which journeys may be recommended under Learning Mode |
| Topic within plan scope | Candidate for a **Learning Journey** instance |

A student with one Study Plan will have **many** Learning Journeys (typically one per topic engaged).

### Continuity

Plan delete/recreate must not destroy journeys, evidence, or coverage (already Version 1 law). Version 2 makes journeys the explicit surviving educational aggregate.

---

## 4. Daily Mission → Journey Recommendation

| Version 1 Mission | Version 2 Journey Recommendation |
|-------------------|----------------------------------|
| “What should I do today?” | Same job |
| Bound to plan + Current Learning Topic | Bound to active / recommended **journey** + session intent |
| Optimizer output | Decision/Mission Engine 2.0 output |
| Completion advances coverage (when lawful) | Realising recommendation → Learning Session; coverage only via journey rules |
| Can feel like topic unit of work | Explicitly **not** the topic unit of work |

### Migration stance

- Missions remain valid Version 1 runtime objects until Mission Engine 2.0 (V2-004).
- Conceptually, treat each mission as a **recommendation to perform a session** on a topic journey.
- Historical missions become ancestry references on Learning Sessions / JourneyHistory after a future data migration milestone.

### Authority warning

Recommendations must continue to respect Learning Mode focus. Migration must not use “smarter recommendations” as a pretext to bypass Current Learning / active journey authority without disclosed mode change.

---

## 5. Study Session → Learning Session

| Version 1 | Version 2 |
|-----------|-----------|
| LXP-002 Study Session | Learning Session |
| Start / Pause / Resume / Finish | SessionState machine |
| Practice outcome capture | JourneyEvidence contributions |
| Optional notes / review | JourneyReflection (required in V2 principles) |
| Mission-scoped | Journey-scoped (mission/recommendation optional link) |

### Migration stance

- Session UX patterns can be reused.
- Attribution upgrades from mission-id-primary to journey-id-primary.
- In-flight Version 1 sessions at cutover need an explicit handoff policy (open question for V2-005).

---

## 6. Coverage and Completion

| Version 1 | Version 2 |
|-----------|-----------|
| TopicProgress.completed (Study Progress) | Topic Complete via journey `COMPLETED` |
| Mission complete → may advance coverage | Session complete → never alone; journey criteria + confirm |
| Risk: mastery formula side-effects | Explicitly forbidden as completion drivers |

### Migration stance

Existing Study Progress rows remain authoritative coverage history. Future journey completion must **reconcile with** that history, not invent a second coverage truth.

---

## 7. Twin and Evidence

| Version 1 / Epic 0 | Version 2 |
|--------------------|-----------|
| Student Digital Twin | Twin 2.0 consumes journey-attributed evidence (V2-006) |
| Learning Evidence Model | Unchanged catalogue; add journey/session attribution fields conceptually |
| Evidence Authority gates | Remain mandatory |

Journeys do not replace Twin domains (Knowledge, Memory, Behaviour, etc.). They improve the quality and attribution of inputs.

---

## 8. Curriculum Structures

| Engine / ADR language | Version 2 educational language |
|-----------------------|--------------------------------|
| Curriculum | Curriculum |
| (implicit paper) | Subject |
| Section | Chapter |
| Topic | Topic |
| Learning Objective / Outcome | Learning Objective |

Migration must preserve ADR-003 coexistence: flat curricula without sections still traverse and still grow journeys per topic.

---

## 9. Phased Evolution (Architectural)

```
Phase A — Architecture (V2-001)
  Documents only; V1 runtime unchanged

Phase B — Curriculum Graph (V2-002)
  Formalise Subject/Chapter/Topic/edges; still no journey runtime required

Phase C — Journey Engine (V2-003)
  Create journey aggregates; dual-run with TopicProgress

Phase D — Mission Engine 2.0 (V2-004)
  Emit JourneyRecommendations; may wrap or replace Daily Mission generation

Phase E — Session Engine (V2-005)
  Learning Sessions write journey evidence + required reflection

Phase F — Twin 2.0 (V2-006)
  Prefer journey-attributed evidence in belief updates

Phase G+ — Revision / Analytics / Founder / Alpha (V2-007–010)
  Build on stable journey meanings
```

No phase may rewrite educational meanings defined in V2-001.

---

## 10. Data Migration Principles (Future Implementation)

When a later milestone implements persistence:

1. **Map by official topic identity**, not by title fuzzy match.
2. **Prefer additive tables/columns** over destructive rewrites.
3. **Backfill journeys** for topics with existing progress/attempts as `ACTIVE` or `COMPLETED` according to explicit rules reviewed against the Constitution.
4. **Never drop** Study Attempts or Evidence to “simplify” journey backfill.
5. **Record migration events** in JourneyHistory / system evidence.
6. **Feature activation** must be explicit; documentation is not activation.

Schema design is out of scope for V2-001.

---

## 11. Non-Migration (Explicit)

The following do **not** map into Learning Journeys:

- Founder Operational State / Founder Recommendations
- Brand / auth / billing artefacts
- Internal Alpha pipeline tickets
- UI layout preferences

---

## 12. Closing

Version 1 Study Plan / Mission / Session remain the live educational path until later milestones implement this map. The map exists so those milestones do not renegotiate what Version 2 means.

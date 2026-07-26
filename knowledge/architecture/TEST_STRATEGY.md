# MS-001 — Educational Runtime Bridge Test Strategy

**Milestone:** MS-001 — Foundational Trust  
**Directive:** Engineering Directive 002  
**Status:** Architecture Design (tests designed — **do not implement** under this directive)  
**Parent:** `EDUCATIONAL_RUNTIME_BRIDGE.md`  
**Interfaces:** `BRIDGE_INTERFACE_SPECIFICATION.md`

---

## Goals

Prove the Bridge:

1. Preserves educational behaviour (AC-8).  
2. Unifies Experience consumption onto Runtime A (AC-1…AC-6).  
3. Gates mastery through Evidence Authority (AC-7).  
4. Eliminates `seeded_demo_*` authority when Bridge on (AC-3).  
5. Remains rollback-safe per phase.

---

## Test pyramid

```
Internal Alpha validation
        ↑
   End-to-end (HTTP)
        ↑
   Regression (golden educational)
        ↑
   Contract (port ↔ bridge ↔ service)
        ↑
   Integration (bridge + DB)
        ↑
   Unit (mappers, alignment, flags)
```

---

## 1. Unit tests (design)

| Suite | Asserts |
|---|---|
| Mission projection mapper | SQL Mission + tasks → OpaqueDict fields; status enum map |
| Session id map | MissionId ↔ ExperienceSessionId bijection |
| Recommendation alignment | Primary label/topic forced to mission when present |
| Failure code mapping | Service exceptions → bridge codes |
| Flag composition | Bridge on ⇒ seed path unreachable; Bridge off ⇒ prior adapters |
| Ownership guard helpers | Foreign mission → FORBIDDEN |

**Do not** re-test Planning topic math in Bridge unit tests — call through to service integration/golden instead.

---

## 2. Integration tests (design)

| Suite | Setup | Asserts |
|---|---|---|
| PlanningBridge ensure | User + active StudyPlan + TopicProgress | `generate_today_mission` idempotent; projection matches DB |
| MissionLifecycle start | Pending Mission | Status In Progress; event emitted |
| MissionLifecycle start owned | Other user’s mission id | FORBIDDEN; no status change |
| LearningStateBridge | Known TopicProgress | Readiness/lifecycle labels match ReadinessService / Lifecycle |
| EvidenceParity | Controlled outcome payload | TopicProgress delta == legacy StudySessionService path |
| Evidence reject | Authority reject fixture | No mastery write; code `EVIDENCE_REJECTED` |

Use existing pytest app/db fixtures; no schema changes.

---

## 3. Contract tests (design)

Port-level contracts Experience already relies on:

| Contract | Consumer | Provider under Bridge |
|---|---|---|
| `MissionPort.get_todays_session` | HomeService / EducationalStateService | PlanningBridge adapter |
| `MissionPort.start_session` | StudentExperienceService | MissionLifecycleBridge |
| `AdaptiveDecisionPort.get_todays_recommendation` | HomeService | RecommendationBridge |
| Twin summary port | EducationalStateService | LearningStateBridge |

**Assert:** For each method — inputs/outputs/failure modes match `BRIDGE_INTERFACE_SPECIFICATION.md`.  
**Assert:** `authority` fields never equal demo seed authorities when Bridge on.

Suggested location (future): `tests/architecture/` or `tests/infrastructure/adapters/bridge/`.

---

## 4. Regression / golden educational tests (design)

Freeze Runtime A outputs for fixtures:

| Fixture ID | Scenario | Golden fields |
|---|---|---|
| G1 | No study plan | No mission; CTA disabled |
| G2 | Learning stage, incomplete leaves | Mission topic == `CurriculumService.get_next_incomplete_topic` path |
| G3 | Revision stage | Revision template / weak-topic policy match Planning |
| G4 | Mission In Progress | Resume status; no second ensure creating divergent topic |
| G5 | After legacy finish | TopicProgress snapshot |

**Bridge regression:** With Bridge on, Experience projections’ educational fields **equal** golden (formatting tolerance documented).

**Forbidden:** Changing Planning/Recommendation algorithms to make Bridge tests pass.

---

## 5. End-to-end tests (design)

HTTP flows (Flask test client):

| Flow | Steps | Asserts |
|---|---|---|
| Start Study | Login → Home GET → Start POST → Overview | Redirect; SQL In Progress; topic on Overview |
| Resume Study | In Progress mission + workspace → deep link | Lands on `active_surface`; ownership OK |
| Load Home | GET `/student/` | Cards from SQL; no demo strings (e.g. fabricated “Core methods” when not in syllabus state) |
| Complete Session | Start → … → Complete POST | Mission Completed; Evidence path invoked |
| Recommendation | GET Home | `mission_aligned`; topic equality |

Also: sole runtime on + Bridge on smoke (optional until P7).

---

## 6. Negative / security tests (design)

| Case | Expect |
|---|---|
| session_id for another user | 403/404 |
| Bridge on, seed flag on | Composition refuses seed **or** test fails AC-3 (define one policy) |
| Complete without outcome when required | INVALID_STATE |
| DB down / service raise | UNAVAILABLE; fallback telemetry; no demo invent |

---

## 7. Performance / ops smoke (design)

| Check | Notes |
|---|---|
| Home parallel reads | Latency budget vs legacy Dashboard |
| `bridge.call` metrics present | Diagnostics |
| Multi-worker resume | After P6 only |

---

## 8. Internal Alpha validation (design)

Manual / operator checklist (extends `knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md` conceptually):

| Step | Pass criteria |
|---|---|
| A1 | Bridge flags on; seed off; sole runtime **off** initially |
| A2 | Create/activate plan via existing wizard |
| A3 | Legacy Dashboard mission topic recorded |
| A4 | Experience Home shows **same** topic |
| A5 | Start from Home → same mission In Progress in DB |
| A6 | Resume after refresh works |
| A7 | Complete updates progress equivalently to a legacy finish for same outcome |
| A8 | Recommendation card matches mission topic |
| A9 | Journey/History not demo fabrications |
| A10 | Rollback drill: disable write flag → Start fail closed; legacy still works |
| A11 | Re-enable; re-verify A4–A8 |
| A12 | Optional: sole runtime on smoke **only after** A1–A11 |

Sign-off artefact: short Alpha report linking AC-1…AC-10.

---

## 9. Phase exit test gates

| Phase | Minimum tests before release |
|---|---|
| P1 | Integration PlanningBridge + Home contract; seed unreachable |
| P2 | Alignment property + recommendation E2E |
| P3 | Start/resume E2E + ownership negatives |
| P4 | Evidence parity integration + complete E2E |
| P5 | Journey/History/Revision contract + no demo |
| P6 | Multi-worker resume smoke |
| P7 | Full Alpha checklist + rollback drill |

---

## 10. Explicit non-goals (this directive)

- Do **not** implement the suites above under Directive 002.  
- Do **not** weaken architecture CI gates unrelated to Bridge.  
- Do **not** add LLM-based “fuzzy” educational assertions.

---

## Stop condition

Test strategy documented. Implementation of tests is a later engineering milestone.

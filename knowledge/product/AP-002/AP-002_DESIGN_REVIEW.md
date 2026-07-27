# AP-002 — Design Review

**Programme:** AP-002 — Educational Assessment Engine  
**Document:** `AP-002_DESIGN_REVIEW.md`  
**Status:** Design review (documentation milestone)  
**Date:** 2026-07-27  

---

## 1. Educational consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Assessments improve learning, not grade theatre | **Pass** | Philosophy explicit across pack |
| Evidence over marks | **Pass** | Scoring model reframed as evidence dimensions |
| Soft signals cannot alone author mastery | **Pass** | Aligned with EIP-002 / Evidence Model |
| Anxiety-safe UX | **Pass** | UX principles reject exam chrome by default |
| Distinction vs Quiz/Practice/Mission/Revision/Exam | **Pass** | Educational Model defines boundaries |
| Mastery remains Twin/Reasoning inference | **Pass** | Repeated invariant |

**Residual educational risk:** Student perception may still read any check as “test” if copy/visuals regress during implementation — UX acceptance tests required in AP-002B/E.

---

## 2. Architecture consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Twin sole learner SoT | **Pass** | Digital Twin integration |
| Reasoning sole inference | **Pass** | Evidence Model ownership matrix |
| Mission consumes decisions | **Pass** | Mission integration |
| Tutor explains, never grades | **Pass** | Tutor integration |
| Graph relates only | **Pass** | Chain documented |
| Retrieval-only curriculum evidence | **Pass** | Question Model content authority |
| Assessment produces observations | **Pass** | Matches invariant §7; AP-001 retained as ingress |
| No architecture redesign | **Pass** | Additive Engine beside Pipeline |
| Determinism / no LLM in Reasoning | **Pass** | Explicit throughout |

**Residual architecture risk:** Pressure to “just update mastery in the Engine for speed” during implementation — must be blocked by architecture tests and code review checklist.

---

## 3. Engineering consistency

| Criterion | Verdict | Notes |
|---|---|---|
| Layering Blueprints → Services → Domain | **Pass** (planned) | Matches CIP/SDT/AME/AP-001 pattern |
| Independently releasable milestones | **Pass** | AP-002A…F |
| Additive migrations intent | **Pass** | Implementation Plan |
| V1/V2 curriculum compatibility | **Pass / N/A** | Design does not alter traversal; Retrieval remains interface |
| Idempotent observation emission | **Pass** (designed) | Lifecycle idempotency section |
| Coexistence with LXP practice + AP-001 | **Pass** | Explicit non-cutover |

**Residual engineering risk:** ObservationKind may prove insufficient for concept-linking / rich free text — requires coordinated Twin additive change, not Engine-only fork.

---

## 4. Risks

| Risk | Severity | Mitigation |
|---|---|---|
| Exam anxiety leaks into UI | High | UX principles + blind review on student copy |
| Over-assessment fatigue | High | Mission eligibility density gates |
| Evidence noise overwhelms Reasoning | Medium | Evidence strength bands; selection for Twin unknowns |
| Duplicate scoring paths (Engine vs Tutor vs legacy) | High | Single evaluation in Engine; Tutor narrates only |
| Premature mastery language | High | EIP-002 gates; no direct Twin writes |
| Scope creep into mock exams | Medium | Out-of-scope + deferred non-milestones |
| Schema sprawl vs AP-001 tables | Medium | Prefer Pipeline events; Engine tables for instruments/sessions only |

---

## 5. Future extensibility

The design intentionally leaves room for:

- Additional item types (worked solutions, concept linking) without rewriting Twin SoT
- New assessment intents without new authorities
- Reasoning rule evolution consuming richer metadata
- Optional Retrieval profile for assessment authoring/grounding
- Later exam-simulation programme *beside* formative Engine (not inside it)
- LLM Tutor prose still behind `TutorGenerationPort` only

Extension forbidden without ADR:

- LLM as mastery authority
- Assessment-owned learner state store
- Mission prioritisation that re-implements Reasoning

---

## 6. Open questions

1. **ObservationKind extension:** Add kinds for concept linking / structured free text in Twin, or overload metadata on `question_answered`?
2. **Authoring workflow:** Do Founders author items in Curriculum Studio, a new Assessment Studio, or import packs?
3. **Cutover from LXP-003 / StudyAttempt:** When does Engine become canonical practice evidence ingress?
4. **Numeric evidence strength thresholds:** Own in Reasoning policy registry or Assessment config?
5. **Student identity wiring:** Ensure Engine sessions key off the same Twin `student_id` as Tutor Home (known TUTOR-001 debt).
6. **Feature flag strategy:** Per-subject rollout vs global flag for AP-002B?
7. **Reflection coding:** Closed taxonomy vs free text stored as uncoded soft signal only?
8. **Time pressure:** Any formative contexts where gentle timers are educationally justified?

---

## 7. Recommendations

1. Implement **AP-002A → AP-002B (narrow)** first; prove observation yield before adaptive triggers.
2. Keep **AP-001 as sole Reasoning trigger path** from assessment activity.
3. Add architecture tests early: Engine must not import Twin mastery writers.
4. Run a short **educational copy review** (blind or founder) before AP-002B student release.
5. Coordinate any Reasoning rule changes as an explicit sub-task under AP-002D — do not smuggle policy into delivery UI.
6. Treat Founder analytics (AP-002F) as evidence-density health, never ranking.
7. Update `ARCHITECTURE.md` / `PROJECT_CONTEXT.md` only when implementation milestones land — not in this design-only pack (unless a docs cross-link is desired later).

---

## 8. Design milestone verdict

**APPROVED FOR IMPLEMENTATION PLANNING** — educational and architectural consistency hold; no production code required or produced by this pack.

Implementation must not start by violating “Assessment observes; Reasoning infers.”

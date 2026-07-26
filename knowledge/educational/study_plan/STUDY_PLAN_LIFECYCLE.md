# Study Plan Lifecycle

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Educational lifecycle specification for Canonical Study Plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **educational lifecycle** of a Canonical Study Plan — what each state means for the student’s preparation journey, and which transitions are educationally lawful.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `CANONICAL_STUDY_PLAN.md`
3. `../EDUCATIONAL_CONTINUITY_STANDARD.md` (EIP-005)
4. `../EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`
5. `../EDUCATIONAL_LOGIC_REGISTRY.md` (EL-011)
6. `../scheduling/RESCHEDULING_POLICY.md`
7. `STUDY_PLAN_VALIDATION.md`

Lifecycle states describe **educational meaning**. They are not merely database enums, UI badges, or workflow tickets.

> **Lifecycle names how the plan lives.  
> Continuity names what survives when the plan changes.  
> Neither invents educational structure.**

---

## 1. Purpose

A Study Plan is a living educational promise for a sitting — not a static PDF.

Students miss weeks, recover, finish early, change sittings, or replace a plan that no longer fits. Coaching systems need a shared vocabulary for those postures so narration, missions, and advisory layers do not invent conflicting stories.

This document records educational state meaning so Runtime A and future Master Planner consumers share one lifecycle contract.

---

## 2. Lifecycle Principles

1. **Educational meaning first.** Each state answers *what is true of the preparation frame now?*
2. **Derivation preserved.** State changes do not licence inventing phases, intensity, or revision law.
3. **Continuity preserved.** Learner-owned history survives ordinary plan change (EIP-005).
4. **Adaptation ≠ replan.** Local timetable moves may yield Adapted / Recovered plans; educational envelope changes require upstream re-package / re-blueprint / re-allocate and typically Superseded + new plan.
5. **One active preparation frame.** At most one Canonical Study Plan is Active for a given student × sitting context unless product rules explicitly disclose multi-plan comparison (comparison plans are not Active coaching authority).
6. **Speakable transitions.** Material lifecycle changes require explainability (`STUDY_PLAN_EXPLAINABILITY.md`).
7. **Validation gates publication.** Draft may exist before full validation; Active coaching consumption requires validation success (`STUDY_PLAN_VALIDATION.md`).
8. **Disposable container.** Archived / Superseded plans dispose planning authority; they do not erase Study Progress.

---

## 3. Lifecycle State Catalogue

Identifiers (SPL-XX) exist for traceability. Educational meaning is binding.

| ID | State | Educational meaning |
|----|-------|---------------------|
| SPL-01 | **Draft** | The plan is being assembled from Scheduling Engine output but is not yet an educational promise to the student |
| SPL-02 | **Approved** | The plan has passed educational validation and is authorised as a complete coaching contract — not yet the lived daily frame, or awaiting activation |
| SPL-03 | **Active** | The plan is the student’s current authorised preparation frame for the sitting |
| SPL-04 | **Adapted** | The plan remains the same educational journey, but placement has lawfully changed after divergence (buffers used, sessions moved) |
| SPL-05 | **Recovered** | The plan has absorbed disruption through authorised recovery capacity / lighter load and remains educationally continuous |
| SPL-06 | **Completed** | The sitting journey under this plan has reached its educational end (sitting arrived / planned horizon finished) without requiring a replacement plan |
| SPL-07 | **Superseded** | A new educational plan (new timetable / blueprint / package) has replaced this one as coaching authority |
| SPL-08 | **Archived** | The plan is retained for history / audit / student reference but is not coaching authority |

### 3.1 State posture notes

| State | Is coaching authority? | May invent structure? | Continuity duty |
|-------|------------------------|-----------------------|-----------------|
| Draft | No | No | N/A (not yet published promise) |
| Approved | Ready, not yet lived | No | Preserve any seeded Study Progress declarations |
| Active | Yes | No | Full EIP-005 |
| Adapted | Yes (same plan identity) | No — placement only | Full EIP-005 |
| Recovered | Yes (same plan identity) | No — recovery already authorised | Full EIP-005 |
| Completed | No (historical) | No | History retained |
| Superseded | No | No | History retained; new plan continues learner assets |
| Archived | No | No | History retained |

---

## 4. State Specifications

### SPL-01 — Draft

**Educational meaning:** The Scheduling Engine has produced (or is producing) output, and the Canonical Study Plan representation is incomplete, unvalidated, or not yet shown as a student promise.

**May:** assemble sections; attach traces; fail validation openly.  
**Must not:** be narrated as “your plan” for daily coaching; hide known overflow; claim completeness.

### SPL-02 — Approved

**Educational meaning:** Validation has succeeded. The artefact is a lawful educational contract ready for activation.

**May:** be presented for student confirmation / activation; serve as the frozen baseline before lived divergence.  
**Must not:** skip validation; approve infeasible theatre; approve plans that invent structure beyond the timetable.

### SPL-03 — Active

**Educational meaning:** This plan is the student’s current authorised preparation frame. Missions, sessions, and plan narration bind to it.

**May:** guide daily coaching within envelopes; surface upcoming phases, revision windows, and commitments.  
**Must not:** silently coexist with another Active plan for the same sitting context; redefine Learning Mode topic authority.

### SPL-04 — Adapted

**Educational meaning:** Reality diverged; the timetable moved under MS006 rescheduling **without** changing educational envelopes. The journey mission remains the same; the diary changed.

**Typical causes:** missed sessions, availability change, leave correction, buffer consumption, session re-seating (RD-01…RD-08 family as allocation events).  
**May:** update session inventory and explain “what changed.”  
**Must not:** steal protected revision; invent new first-pass ambition; pretend nothing moved.

**Relationship to Active:** Adapted is an Active-class posture (still coaching authority) with disclosed placement change. Product surfaces may show “Active (adapted)” language; educationally the state is Adapted.

### SPL-05 — Recovered

**Educational meaning:** Disruption was absorbed through authorised recovery capacity / lighter load. The plan remains continuous and coaching-authoritative, with recovery posture disclosed.

**Typical causes:** illness, dense shock after mocks, authorised recovery insertion (RD-07 and related).  
**May:** temporarily emphasise lighter sessions already warranted by BC-06 / recovery cells.  
**Must not:** convert recovery into punishment catch-up; invent recovery pedagogy absent from the blueprint.

**Relationship to Adapted:** Recovery is a specialised adaptation emphasising authorised lighter load. A plan may be Recovered after illness even if few calendar cells moved, provided recovery capacity was engaged and explained.

### SPL-06 — Completed

**Educational meaning:** The preparation frame under this plan has reached its natural educational end for the sitting — e.g. exam date arrived, or the planned horizon finished under this contract.

**May:** remain visible as the plan the student prepared under; support post-sitting reflection without inventing new first-pass.  
**Must not:** continue generating forward first-pass ambition past the sitting without a new plan; erase history.

Completion is **not** a pass claim. Completing the plan is not passing the exam.

### SPL-07 — Superseded

**Educational meaning:** Upstream educational law or allocation authority changed enough that a **new** Canonical Study Plan is now coaching authority (new package / blueprint / timetable, or sitting change requiring replan).

**Typical causes:** RD-09 sitting date change; RD-10 blueprint superseded; feasibility failure requiring re-package; student elects a replacement plan.  
**May:** retain superseded plan for audit and student history.  
**Must not:** keep superseded plan as silent Active authority; wipe Study Progress because the container was replaced.

### SPL-08 — Archived

**Educational meaning:** The plan is intentionally retained without coaching authority — e.g. after completion, after supersession cleanup, or after student archive of an unused approved plan.

**May:** support review, comparison, or support tooling.  
**Must not:** drive today’s mission; invent discontinuity in learner history.

---

## 5. Lawful Transitions

```
                    ┌────────────┐
                    │   Draft    │
                    └─────┬──────┘
                          │ validate success
                          ▼
                    ┌────────────┐
                    │  Approved  │
                    └─────┬──────┘
                          │ activate
                          ▼
              ┌───────────────────────┐
              │        Active         │◄──────────────┐
              └───────────┬───────────┘               │
        divergence│       │ recovery engaged          │ further local moves
                  ▼       ▼                           │
           ┌──────────┐ ┌───────────┐                 │
           │ Adapted  │ │ Recovered │─────────────────┘
           └────┬─────┘ └─────┬─────┘
                │             │
                └──────┬──────┘
                       │ sitting / horizon end
                       ▼
                 ┌───────────┐
                 │ Completed │──────► Archived
                 └───────────┘

        Active / Adapted / Recovered / Approved / Draft
                       │ upstream replan or replacement
                       ▼
                 ┌────────────┐
                 │ Superseded │──────► Archived
                 └────────────┘
```

### 5.1 Transition rules

| From | To | Educational warrant |
|------|----|---------------------|
| Draft → Approved | Validation success (`STUDY_PLAN_VALIDATION.md`) |
| Draft → Archived | Abandoned before approval; no coaching authority ever granted |
| Approved → Active | Explicit activation as the student’s preparation frame |
| Approved → Superseded / Archived | Replaced or withdrawn before activation |
| Active → Adapted | Lawful MS006 rescheduling preserving blueprint intent |
| Active → Recovered | Authorised recovery capacity engaged after disruption |
| Adapted → Adapted | Further lawful placement moves |
| Adapted → Recovered | Recovery capacity engaged after further disruption |
| Recovered → Adapted / Active-class | Recovery window ends; remaining journey continues under same envelopes |
| Active / Adapted / Recovered → Completed | Sitting / planned horizon educationally ends |
| Active / Adapted / Recovered / Approved / Draft → Superseded | New Canonical Study Plan becomes authority |
| Completed / Superseded → Archived | Retention without coaching authority |
| Any → Draft | **Forbidden** as a way to silently rewrite an Active promise; create a new Draft plan instead and supersede |

### 5.2 Forbidden transitions / postures

- Active without validation success
- Adapted / Recovered that invent new educational envelopes
- Completed used as a pass certificate
- Superseded plan still driving missions
- Archive / delete that erases learner-owned Study Progress
- Dual Active plans for the same sitting without disclosure

---

## 6. Relationship to Scheduling Reschedule Events

| MS006 divergence / event | Typical Study Plan lifecycle effect |
|--------------------------|-------------------------------------|
| Local missed sessions / availability tweak (RD-01, RD-03…RD-06, RD-08) | Active → Adapted (if material) |
| Illness / recovery insertion (RD-07) | Active / Adapted → Recovered |
| Extra time within envelopes (RD-04, RD-05) | Adapted (placement), not new ambition |
| Sitting date change / blueprint superseded (RD-09, RD-10) | → Superseded; new plan Draft→Approved→Active |
| Escalation to re-package / re-blueprint | → Superseded when new plan published |

The Study Plan lifecycle **represents** scheduling adaptation. It does not perform packing.

---

## 7. Continuity Across Lifecycle Change

Binding continuity rules (EIP-005):

1. Educational history belongs to the learner, not the Study Plan container.
2. Adapted / Recovered plans continue the same learner history under the same plan identity.
3. Superseded / Archived / deleted planning containers dispose schedule authority only.
4. A new Active plan for the same syllabus units continues existing Study Progress — no false cold-start.
5. Current Learning and missions resynchronise from preserved inputs after lawful plan change.

Lifecycle language must never imply that “starting a new plan” means “you have studied nothing.”

---

## 8. Student-Facing Meaning (Plain Language)

| State | Student-facing sense (examples) |
|-------|----------------------------------|
| Draft | “We’re preparing your plan — not ready to follow yet.” |
| Approved | “Your plan is ready. Activate it when you want it to guide daily study.” |
| Active | “This is the plan you’re following now.” |
| Adapted | “Your plan’s dates moved after [missed study / leave / availability change]. The educational journey is the same.” |
| Recovered | “We’ve used recovery capacity after [illness / dense stretch]. Lighter load for a while — not punishment.” |
| Completed | “This plan’s preparation window has ended.” |
| Superseded | “A new plan replaced this one.” |
| Archived | “Kept for your records — not guiding today.” |

Internal IDs (SPL-XX) must not appear as student jargon.

---

## 9. Out of Scope

- Database state machines or ORM enums
- UI badge design
- Soft-delete mechanics beyond educational continuity rules
- New scheduling or recovery algorithms

---

## 10. Cross References

- `CANONICAL_STUDY_PLAN.md` — overall contract
- `STUDY_PLAN_COMPONENTS.md` — what lives inside each state
- `STUDY_PLAN_VALIDATION.md` — gate for Approved / Active
- `STUDY_PLAN_EXPLAINABILITY.md` — how transitions are explained
- `../scheduling/RESCHEDULING_POLICY.md` — allocation adaptation law
- `../EDUCATIONAL_CONTINUITY_STANDARD.md` — history survival

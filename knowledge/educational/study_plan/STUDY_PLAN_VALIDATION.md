# Study Plan Validation

**Programme:** VI — Master Planner  
**Milestone:** MS007 — Canonical Study Plan Model  
**Classification:** Educational validity gates for Canonical Study Plans  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **what makes a Study Plan educationally valid** — the gates a completed plan must pass before it may become an Approved or Active coaching contract.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `CANONICAL_STUDY_PLAN.md`
3. `STUDY_PLAN_COMPONENTS.md`
4. `STUDY_PLAN_LIFECYCLE.md`
5. `../scheduling/SCHEDULING_ENGINE.md`
6. `../scheduling/SCHEDULING_CONSTRAINTS.md`
7. `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`
8. `../strategy/EDUCATIONAL_STRATEGY_FRAMEWORK.md`
9. `../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`
10. `../EDUCATIONAL_CONTINUITY_STANDARD.md`

Validation checks **educational integrity of the represented artefact**. It does not run new scheduling algorithms and does not invent educational structure to “make validation pass.”

> **Valid means educationally lawful and complete as a coaching contract.  
> Valid does not mean the student will pass.**

---

## 1. Purpose

Downstream coaching must not consume an incomplete, invented, or dishonest plan.

An expert IFoA tutor refuses to present a diary that:

- invents revision from leftovers,
- contradicts the agreed strategy,
- ignores the student’s diagnosed starting point,
- hides impossibility,
- or cannot explain itself.

This document records those refusal rules as educational validation gates.

---

## 2. Validation Principles

1. **Derivation first.** Invalid if material elements lack Scheduling Engine warrant.
2. **No invention to pass.** Failed gates escalate upstream; they do not authorise silent repair by inventing structure.
3. **All gates material.** A plan may not be Approved while any hard gate fails.
4. **Soft gates speak.** Warnings (thin evidence, fragile capacity) must be named in assumptions / explainability — they do not mint false certainty.
5. **Deterministic posture.** Same complete timetable + same validation rules → same pass/fail posture.
6. **Continuity-aware.** Validation must not require erasing learner history to “clean” a plan.
7. **Claim-type humility.** Validation never certifies mastery or exam success.

---

## 3. Hard Validation Gates

Identifiers (SPV-XX) name gates. Educational meaning is binding.

| ID | Gate | Pass condition |
|----|------|----------------|
| SPV-01 | **Timetable derivation** | Every material plan element traces to Scheduling Engine output |
| SPV-02 | **Blueprint traceability** | Every material phase/session/protection traces through the timetable to Planning Blueprint elements |
| SPV-03 | **Protected revision** | Where the blueprint reserved revision, the plan presents a protected revision window — not cannibalised first-pass theatre |
| SPV-04 | **Constraint respect** | Educational and allocation constraints already settled upstream are not violated by the plan representation |
| SPV-05 | **Educational coherence** | Phase order, sequencing, and component meanings form one coherent journey story consistent with the blueprint |
| SPV-06 | **Strategy consistency** | The plan remains consistent with the Educational Strategy bound on the package / blueprint / timetable |
| SPV-07 | **Profile alignment** | The plan remains consistent with the Student Educational Profile postures carried upstream (no cold-start theatre against known coverage / constraints) |
| SPV-08 | **Capacity honesty** | No normal load packed into leave / zero-capacity regions; intensity envelopes respected as allocated |
| SPV-09 | **Protection honesty** | Buffers, recovery, and rest capacity authorised upstream appear as first-class elements (or explicit lawful absence) |
| SPV-10 | **Feasibility honesty** | Infeasible or overflow outcomes are explicit; complete plan theatre over infeasible upstream posture fails |
| SPV-11 | **Required sections present** | All required Canonical Study Plan sections exist (`CANONICAL_STUDY_PLAN.md` §8) |
| SPV-12 | **Explainability present** | Plan-level explainability attachments exist for material structure (`STUDY_PLAN_EXPLAINABILITY.md`) |
| SPV-13 | **Non-invention** | No educational objectives, phases, intensity, or recovery law appear beyond timetable / blueprint / package warrants |
| SPV-14 | **Continuity posture** | Plan validation does not depend on erasing rightful learner history; continuity notice present |
| SPV-15 | **Mode humility** | Plan does not claim authority to silently override Learning Mode topic selection |

A Canonical Study Plan is **educationally valid** only when **all hard gates pass**.

---

## 4. Gate Specifications

### SPV-01 — Timetable derivation

**Fails when:** sessions, phases, or commitments exist with no Scheduling Engine warrant; or the plan silently “improves” packing.

**Remediation:** rebuild representation from timetable; do not invent missing cells.

### SPV-02 — Blueprint traceability

**Fails when:** plan elements cannot cite blueprint phase/component IDs (BP-XX / BC-XX) via the timetable.

**Remediation:** escalate if timetable itself lacks traces; scheduling layer must be fixed first.

### SPV-03 — Protected revision

**Fails when:** blueprint reserved revision, but the plan shows first-pass consuming that region; or revision window is absent/hidden.

**Remediation:** refuse approval; escalate to scheduling / upstream — never “borrow” revision in the plan layer.

### SPV-04 — Constraint respect

**Fails when:** known educational constraints (prerequisites, sequencing, leave, rest, intensity) are violated in the represented plan.

**Examples:** prerequisite topics after dependents; study on declared leave; weekly load above envelope.

### SPV-05 — Educational coherence

**Fails when:** journey story contradicts itself — e.g. final-preparation freeze alongside new first-pass ambition; practice before any authorised learning of the topic; recovery narrated as punishment grind.

### SPV-06 — Strategy consistency

**Fails when:** plan commitments contradict the bound strategy (e.g. strategy privileges protected revision while plan speech treats revision as optional leftover).

Validation does **not** re-select strategy. It checks consistency with the strategy already chosen.

### SPV-07 — Profile alignment

**Fails when:** plan assumes a cold-start student despite Profile / Study Progress showing completed studying; or ignores named constraints already in the Profile (e.g. known leave, sitting pressure) that the timetable already embodied — and the plan representation drops them.

Validation does **not** re-diagnose. It checks alignment with Profile postures already carried upstream.

### SPV-08 — Capacity honesty

**Fails when:** availability fiction, leave packing, or envelope breach appears in the plan as normal commitment.

### SPV-09 — Protection honesty

**Fails when:** buffers/recovery/rest authorised upstream are deleted, hidden, or rebranded as ordinary study to make the plan look denser.

### SPV-10 — Feasibility honesty

**Fails when:** upstream feasibility was incomplete/infeasible, or timetable recorded mandatory overflow, yet the plan presents as complete and ready without disclosure.

**Pass requires:** either clean placement with explicit “no overflow,” or Draft-only / refused publication with overflow named — never Approved completeness theatre.

### SPV-11 — Required sections present

**Fails when:** identity binding, phases, sessions, protections, assumptions, commitments, lifecycle posture, validation posture, explainability, traceability, change conditions, or continuity notice are missing.

### SPV-12 — Explainability present

**Fails when:** the plan cannot answer why it exists, why it is structured this way, what it commits to, and when it will change (see `STUDY_PLAN_EXPLAINABILITY.md`).

### SPV-13 — Non-invention

**Fails when:** any educational reasoning appears that is not already present in Scheduling Engine output and its upstream traces.

### SPV-14 — Continuity posture

**Fails when:** activation/approval path requires wiping Study Progress; or continuity notice is absent such that supersession would be narrated as educational amnesia.

### SPV-15 — Mode humility

**Fails when:** plan claims that schedule phase emphasis alone reassigns Today’s Mission topic contrary to Learning Mode / Current Learning Topic law without disclosure.

---

## 5. Soft Validation Warnings

Soft warnings do **not** block Approved by themselves, but must appear in SPC-09 assumptions and explainability when material:

| ID | Warning | Educational duty |
|----|---------|------------------|
| SPW-01 | Thin evidence / Profile defaults used upstream | Name uncertainty; avoid confident readiness speech |
| SPW-02 | Fragile capacity (minimal buffers) | Warn that small slip may force escalation |
| SPW-03 | Short runway / risk-protection posture | Keep risk-protection speech visible |
| SPW-04 | Heavy reliance on recovery capacity already | Disclose sustainability strain |
| SPW-05 | Extra time absorbed without envelope change | Confirm no invented new first-pass ambition |

Hiding soft warnings to make the plan feel “confident” is an explainability failure (SPV-12).

---

## 6. Validation Outcomes

| Outcome | Meaning | Lifecycle effect |
|---------|---------|------------------|
| **Valid** | All hard gates pass | Draft may become Approved |
| **Invalid — representation** | Plan misrepresents a lawful timetable | Fix representation; re-validate |
| **Invalid — upstream** | Timetable / blueprint / package itself fails integrity | Refuse plan approval; escalate to MS006 / MS005 / MS004 as appropriate |
| **Incomplete** | Required sections or placements missing | Remain Draft; do not activate |

### 6.1 No silent repair

| Lawful | Unlawful |
|--------|----------|
| Refuse approval and escalate | Steal revision to make SPV-03 pass |
| Keep Draft while overflow is named | Hide overflow to pass SPV-10 |
| Rebuild representation from timetable | Invent sessions to fill gaps |
| Request upstream replan | Re-diagnose Profile inside validation |

---

## 7. When Validation Must Re-Run

Re-validate before treating the plan as Approved/Active after:

1. Any material timetable change (Adapted / Recovered candidates)
2. Upstream package / blueprint replacement
3. Sitting / exam date change
4. Material correction to capacity assumptions (leave, holidays, availability)
5. Discovery that explainability or continuity notice was missing

Cosmetic display changes without educational meaning do not require re-validation.

Adapted / Recovered plans must pass the same hard gates after representation updates. Adaptation is not a licence to weaken protections.

---

## 8. Relationship to Coaching Consumption

| Consumer action | Requires |
|-----------------|----------|
| Student sees “your plan is ready” | Valid → Approved (minimum) |
| Missions / sessions bind to plan as daily frame | Valid → Active (or Active-class Adapted / Recovered) |
| Advisory within envelopes | Active-class plan still Valid after latest material change |
| Historical review of old plan | Completed / Superseded / Archived may be invalid *as current authority* but retained as historical artefacts |

---

## 9. Out of Scope

- Automated test harnesses or CI wiring
- Numeric scoring of “plan quality”
- ML classifiers of adherence risk
- Database constraint definitions
- Re-running scheduling inside the validator

---

## 10. Cross References

- `CANONICAL_STUDY_PLAN.md` — required sections and guarantees
- `STUDY_PLAN_COMPONENTS.md` — compositional completeness
- `STUDY_PLAN_LIFECYCLE.md` — Approved / Active gates
- `STUDY_PLAN_EXPLAINABILITY.md` — SPV-12 content
- `../scheduling/SCHEDULING_CONSTRAINTS.md` — allocation hard constraints
- `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md` — blueprint completeness

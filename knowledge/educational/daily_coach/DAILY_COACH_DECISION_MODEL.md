# Daily Coach Decision Model

**Programme:** VI — Workstream 2 — Daily Coach  
**Milestone:** MS001 — Daily Coaching Model  
**Classification:** Educational decision rules for today’s priority under a Canonical Study Plan  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how an expert tutor decides what today’s priority should be**.

It is subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `EDUCATIONAL_LOGIC_REGISTRY.md` (especially EL-002, EL-003, EL-008, EL-009, EL-011)
3. `DAILY_COACH_MODEL.md`
4. `DAILY_COACH_OBJECTIVES.md`
5. `../study_plan/CANONICAL_STUDY_PLAN.md`
6. `../study_plan/STUDY_PLAN_LIFECYCLE.md`
7. `../scheduling/RESCHEDULING_POLICY.md` (when divergence requires allocation change)
8. `../EDUCATIONAL_EVIDENCE_MODEL.md`

> **Preserve the educational commitments of the Canonical Study Plan unless there is sufficient evidence to justify deviation.  
> Deviation means disclosed adaptation within envelopes, or escalation — never silent rewrite.**

---

## 1. Purpose

Daily coaching is a sequence of educational judgements:

1. Is there a lawful plan to coach against?
2. What educational job does the plan authorise for today?
3. What does today’s real capacity allow?
4. Does recovery or continuity repair take precedence?
5. What single primary objective follows?
6. What optional secondary advice may be offered?
7. Has the situation outgrown Daily Coach authority?

This Decision Model records that tutor reasoning without prescribing algorithms, scores, or code.

Identifiers (DCD-XX) exist for traceability. Educational meaning is binding; implementation field names are out of scope.

---

## 2. Decision Principles

1. **Plan before improvisation.** Start from Canonical Study Plan sessions / phase emphasis for today.
2. **One primary priority.** Rank; do not present equal competing “musts.”
3. **Capacity truth.** Never recommend more than today’s available study time and plan intensity envelopes allow.
4. **Protection precedence.** Protected revision, recovery, buffers, and rest beat invented first-pass ambition.
5. **Mode respect.** Learning Mode topic authority is not silently overridden by advisory preference.
6. **Evidence humility.** Recent evidence may shift emphasis inside envelopes; it may not mint mastery or invent new plan law.
7. **Consistency over heroics.** Prefer sustainable authorised work over punishment catch-up.
8. **Escalate, don’t rewrite.** When educational envelopes must change, identify rescheduling / replanning need.
9. **Explain every material choice.** See `DAILY_COACH_EXPLAINABILITY.md`.
10. **Deterministic posture.** Same inputs → same priority class and escalation posture.

---

## 3. Priority Ordering (Today’s Educational Job)

When multiple authorised jobs could claim today, apply this **priority ladder** (highest first):

| Rank | Priority class | Educational meaning |
|------|----------------|---------------------|
| P1 | **Safety / zero-capacity day** | Leave, illness day with no capacity, or explicit rest / freshness cell — coach rest or minimal continuity only |
| P2 | **Active recovery posture** | Plan is Recovered or SPC-05 recovery capacity is today’s authorised job — lighter load, not catch-up |
| P3 | **Protected revision window** | SPC-04 / revision-phase emphasis for today — revision job beats new first-pass theatre |
| P4 | **Authorised checkpoint / mock emphasis** | SPC-06 / SPC-13 when placed for today — honour exam-craft or check quality as planned |
| P5 | **Authorised practice / consolidation commitment** | SPC-11 / SPC-12 due today or urgently warranted inside envelopes |
| P6 | **Planned study session (phase-default job)** | SPC-03 for today under current phase emphasis (often first-pass learning) |
| P7 | **Continuity repair within envelopes** | Recent missed planned work — resume next lawful plan job; do not invent overload |
| P8 | **Optional advisory enrichment** | EL-008 secondary suggestions — never primary unless no higher class applies and plan allows |

### 3.1 Notes on the ladder

- **P1–P4** are protection- and posture-heavy: violating them for “more topics” is unlawful Daily Coach behaviour.
- **P5–P7** operate inside the plan’s ordinary educational rhythm.
- **P8** is advice. It must be labelled as optional and must not redefine Today’s Mission topic under Learning Mode.
- If the plan places a concrete SPC-03 session for today, that session’s **work type** determines which ladder rung applies (learning vs practice vs revision vs recovery vs rest).

---

## 4. Decision Pipeline (Educational)

```
DCD-01  Plan authority gate
   ↓
DCD-02  Today’s capacity & interruption gate
   ↓
DCD-03  Recovery / protection gate
   ↓
DCD-04  Authorised job resolution (from plan + mode)
   ↓
DCD-05  Recent evidence modulation (within envelopes)
   ↓
DCD-06  Primary objective selection
   ↓
DCD-07  Secondary advice (optional)
   ↓
DCD-08  Escalation check
   ↓
DCD-09  Explainability attachment
```

### DCD-01 — Plan authority gate

| Aspect | Rule |
|--------|------|
| **If** | Active-class Canonical Study Plan exists (Active / Adapted / Recovered) and is educationally valid for coaching |
| **Then** | Proceed with plan-faithful daily coaching |
| **Else if** | Draft / incomplete / invalid / Archived / Superseded / no plan |
| **Then** | Refuse plan-based daily coaching theatre; speak honestly (e.g. activate a plan, or limited Learning Mode continuity if constitutionally available without inventing a plan) |
| **Must not** | Invent a shadow Study Plan for the day |

### DCD-02 — Today’s capacity & interruption gate

| Aspect | Rule |
|--------|------|
| **Inputs** | Available study time today; planned interruptions; leave; intensity envelope |
| **Then** | Cap recommended blocks to true capacity |
| **If** | Capacity is zero or rest is authorised |
| **Then** | Primary objective becomes rest / continuity-only (P1) |
| **Must not** | Recommend heroic load “because the plan shows a session” when capacity was declared unavailable |

### DCD-03 — Recovery / protection gate

| Aspect | Rule |
|--------|------|
| **If** | Recovered lifecycle, SPC-05 engaged, or SPC-08 rest/freshness for today |
| **Then** | Prefer P2 (or P1); refuse punishment catch-up |
| **If** | Protected revision window for today |
| **Then** | Prefer P3; refuse first-pass cannibalisation |
| **Must not** | Steal revision or recovery “just for today” without escalation pathway |

### DCD-04 — Authorised job resolution

| Aspect | Rule |
|--------|------|
| **Resolve** | Today’s plan session / phase emphasis → educational work type |
| **Align** | If work type is first-pass learning under Learning Mode, primary topic follows Current Learning Topic (EL-002 / EL-003) |
| **Disclose** | If work type is revision / recovery / practice emphasis, say so; do not silently present a different Learning Mode Mission as if the plan job did not exist |
| **Must not** | Let advisory weak-topic widgets become undeclared primary objectives |

### DCD-05 — Recent evidence modulation

| Aspect | Rule |
|--------|------|
| **May** | Prefer authorised consolidation / practice return after weak recent practice *when evidence quality permits and plan envelopes allow* |
| **May** | Prefer continuing planned next job after solid completion of yesterday’s authorised work |
| **Must not** | Treat mission completion as mastery; invent weakness theatre from missing soft signals alone; change phase meaning |
| **If** | Evidence is thin / cold start |
| **Then** | Understate estimates; keep guidance plan-led and provisional in speech |

### DCD-06 — Primary objective selection

| Aspect | Rule |
|--------|------|
| **Output** | Exactly one primary educational objective for today (see `DAILY_COACH_OUTPUTS.md`) |
| **Selection** | Highest applicable priority class (§3) that fits capacity |
| **Shape** | Named educational job + syllabus / plan warrant + intended work type + realistic scope for today’s time |
| **Must not** | Emit multiple equal primaries; emit a primary without plan or mode warrant |

### DCD-07 — Secondary advice

| Aspect | Rule |
|--------|------|
| **May** | Offer 0–2 optional secondary recommendations (practice focus, short reflection, confidence support) |
| **Must** | Label as Educational Advice; rank below primary |
| **Must not** | Compete with Mission topic authority; invent new first-pass ambition beyond the plan |

### DCD-08 — Escalation check

See §6. If escalation triggers fire, attach an escalation output rather than inventing unlawful daily load.

### DCD-09 — Explainability attachment

Every material primary (and material secondary) recommendation must carry educational rationale under `DAILY_COACH_EXPLAINABILITY.md`.

---

## 5. Conflict Handling

### 5.1 Common conflicts

| Conflict | Lawful resolution |
|----------|-------------------|
| Plan session vs short available time | Shrink scope inside envelopes; prefer complete smaller authorised job over unfinished heroic load |
| First-pass desire vs protected revision today | Revision wins (P3); first-pass waits or becomes optional advice only if plan permits |
| Missed backlog vs recovery posture | Recovery wins (P2); resume continuity after recovery — do not punish |
| Advisory weak topic vs Learning Mode Current Learning Topic | Learning Mode Mission topic wins for learning days; weak topic may be optional advice with disclosure |
| Extra free time vs plan envelopes | Do not invent new first-pass ambition beyond blueprint/plan; may deepen authorised practice/consolidation or move only via lawful reschedule pathways |
| Confidence low vs plan asks for mocks/checkpoints | Honour plan checkpoint if capacity and recovery allow; otherwise escalate or use authorised lighter preparation — do not invent mastery repair theatre |
| Two plan sessions same day | Follow plan ordering / phase rules; if infeasible under capacity, escalate to rescheduling rather than silent drop of protections |

### 5.2 Conflict resolution order

When objectives and protections collide, resolve in this order:

1. Zero-capacity / rest honesty  
2. Recovery protection  
3. Revision / buffer / freshness protection  
4. Mode authority (Learning Mode topic for learning jobs)  
5. Planned session work type for today  
6. Recent evidence modulation within envelopes  
7. Consistency / sustainable scope  
8. Optional advisory enrichment  

This matches `DAILY_COACH_OBJECTIVES.md` §4 and must not be weakened by local product preferences.

---

## 6. Recovery Decisions

### 6.1 What “recovery” means for Daily Coach

Recovery is **authorised lighter-load coaching** after illness, dense shock, disruption, or engagement of SPC-05 — as already warranted by the Canonical Study Plan / rescheduling posture.

It is **not**:

- a new educational philosophy invented by the Daily Coach;
- a licence to skip protected revision permanently;
- punishment deferred until tomorrow;
- mastery repair claims.

### 6.2 Recovery decision rules

| Situation | Daily Coach decision |
|-----------|----------------------|
| Plan lifecycle **Recovered** | Primary objective emphasises lighter authorised work; explain recovery as intentional |
| Today is an SPC-05 / recovery cell | Coach the recovery job; refuse catch-up doubles |
| Recent illness (RD-07 family) already absorbed into Recovered / Adapted plan | Follow updated plan; do not re-litigate allocation |
| Student feels depleted but plan still shows dense session and no recovery capacity remains | Prefer sustainable scope reduction within envelopes; if still infeasible, **escalate** rather than invent recovery pedagogy |
| Missed days without recovery warrant | Continuity repair (P7): resume next lawful job; escalate if backlog threatens envelopes |

### 6.3 Forbidden recovery behaviours

- Shame language or “you fell behind” as the primary educational reason  
- Invented overload to “get back on track” in one day  
- Silent consumption of protected revision to clear first-pass backlog  
- Claiming understanding was “restored” by rest alone  

---

## 7. Adaptation Boundaries

The Daily Coach may adapt **today’s emphasis** within these boundaries:

| Lawful adaptation | Unlawful adaptation |
|-------------------|---------------------|
| Reduce scope to fit today’s capacity | Change phase order or sitting ambition |
| Prefer authorised consolidation after weak recent practice | Invent a new revision phase |
| Honour Adapted / Recovered plan posture already published | Silently rewrite Active plan commitments |
| Offer optional secondary advice | Replace Learning Mode Mission topic without disclosure / authority |
| Recommend rest when capacity is zero | Pack study into declared leave |
| Flag need to reschedule missed sessions | Perform calendar packing itself (MS006 ownership) |

**Adaptation boundary (binding):**

> Daily Coach adapts *interpretation and today’s scope*.  
> Master Planner / Scheduling adapt *placement*.  
> Upstream planning adapts *educational envelopes*.  
> The Daily Coach owns only the first of these.

---

## 8. Escalation to Rescheduling or Replanning

### 8.1 Escalation principle

When significant deviation from Canonical Study Plan educational commitments is required, the Daily Coach must **identify that a rescheduling or replanning process is needed** rather than independently changing long-term educational intent.

| Escalation class | When | Who owns next step |
|------------------|------|--------------------|
| **E1 — Reschedule (allocation)** | Lived divergence can be absorbed by moving placements while preserving blueprint / plan educational envelopes | Scheduling Engine / Rescheduling Policy (MS006) → plan becomes Adapted / Recovered |
| **E2 — Replan (educational envelopes)** | Remaining work cannot fit; protections would be stolen; strategy / phase meaning must change; sitting date / blueprint superseded | Upstream Master Planner (re-package / re-blueprint / new Canonical Study Plan) |

### 8.2 Triggers that require escalation (not Daily Coach improvisation)

| Trigger | Typical class |
|---------|---------------|
| Multiple missed sessions such that today’s catch-up would breach intensity envelopes | E1 first; E2 if still infeasible |
| Ongoing capacity reduction that invalidates remaining plan feasibility | E1 / E2 per MS006 → upstream |
| Desire to consume protected revision for unfinished first-pass | E2 (educational envelope change) — Daily Coach must refuse silent steal |
| Sitting / exam date change | E2 |
| Blueprint / strategy superseded | E2 |
| Recovery needed but no recovery capacity remains and lighter load still infeasible | E1 / E2 |
| Plan invalid, draft-only, or superseded while surfaces still request “today’s plan coaching” | Refuse + E2 / activation path |

### 8.3 What escalation output looks like (educational)

Escalation is an educational output (see `DAILY_COACH_OUTPUTS.md`):

- **What happened** (capacity / missed work / protection conflict) as fact;
- **What Daily Coach will not do** (invent overload / steal revision / rewrite plan);
- **What should happen next** (reschedule remaining sessions / request replan);
- **What the student should do today meanwhile** (lawful interim primary objective under remaining authority — often continuity-safe lighter work or rest — never fake completeness).

---

## 9. Decision Classes

| Class | Meaning | Examples |
|-------|---------|----------|
| **Mandatory** | Must occur for lawful Daily Coach behaviour | Plan authority gate; single primary; protection honesty; explainability; escalation when triggers fire |
| **Adaptive** | May vary with context inside envelopes | Scope sizing; evidence modulation; secondary advice presence |
| **Forbidden** | Never lawful | Silent plan rewrite; mastery minting from completion; punishment catch-up; revision cannibalisation; Learning Mode commandeering without disclosure |

---

## 10. Worked Tutor Scenarios (Normative Illustrations)

### Scenario A — Ordinary learning evening

Plan shows a first-pass study session; Learning Mode Current Learning Topic is Topic X; two hours available; no recovery posture.

**Decision:** Primary = learn Topic X under Learning Mode (P6). Optional secondary = short practice on X if plan practice density allows. No escalation.

### Scenario B — Revision window day

Plan shows protected revision; student asks to “push ahead” on new topics.

**Decision:** Primary = revision job (P3). New topics may be optional advice only if they do not displace revision. No silent first-pass replacement.

### Scenario C — Post-illness recovery

Plan lifecycle Recovered; lighter sessions placed.

**Decision:** Primary = authorised lighter work (P2). Refuse double-speed catch-up. Explain recovery as intentional.

### Scenario D — Short window, planned long session

Plan shows 3-hour session; student has 40 minutes.

**Decision:** Shrink to a complete smaller authorised fragment of today’s job; do not invent a different curriculum. If repeated shortfalls accumulate, escalate E1.

### Scenario E — Backlog threatens revision

Many missed first-pass sessions; only way to “finish” before exam is to study through protected revision.

**Decision:** Refuse silent revision steal. Escalate E2 (replan) / E1 as policy requires. Today’s interim objective stays envelope-honest.

---

## 11. Cross References

| Document | Relationship |
|----------|----------------|
| [`DAILY_COACH_OBJECTIVES.md`](DAILY_COACH_OBJECTIVES.md) | Objectives this model pursues |
| [`DAILY_COACH_INPUTS.md`](DAILY_COACH_INPUTS.md) | Inputs consumed by DCD-01…DCD-05 |
| [`DAILY_COACH_OUTPUTS.md`](DAILY_COACH_OUTPUTS.md) | Primary, secondary, and escalation outputs |
| [`../scheduling/RESCHEDULING_POLICY.md`](../scheduling/RESCHEDULING_POLICY.md) | E1 allocation adaptation ownership |
| [`../study_plan/STUDY_PLAN_LIFECYCLE.md`](../study_plan/STUDY_PLAN_LIFECYCLE.md) | Active / Adapted / Recovered coaching authority |

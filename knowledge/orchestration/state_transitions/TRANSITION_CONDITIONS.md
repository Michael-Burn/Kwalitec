# Transition Conditions

**Programme:** VII — Workstream 4 — Educational State Engine  
**Milestone:** MS002 — Educational State Transition Framework  
**Classification:** Constitutional conditions that permit contextual state transitions  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **constitutional conditions** that must hold before a catalogue transition (CST-xx) may occur.

It is subordinate to:

1. [`EDUCATIONAL_STATE_TRANSITION_FRAMEWORK.md`](EDUCATIONAL_STATE_TRANSITION_FRAMEWORK.md)
2. [`TRANSITION_TYPES.md`](TRANSITION_TYPES.md)
3. [`TRANSITION_BOUNDARIES.md`](TRANSITION_BOUNDARIES.md)
4. [`../state/STATE_TYPES.md`](../state/STATE_TYPES.md)
5. [`../state/STATE_BOUNDARIES.md`](../state/STATE_BOUNDARIES.md)
6. [`../workflows/`](../workflows/), [`../workflow_transitions/`](../workflow_transitions/), [`../workflow_completion/`](../workflow_completion/) — published orchestration rules that may be *referenced*
7. [`../authority/`](../authority/), [`../conflict_resolution/`](../conflict_resolution/) — constitutional authority and disposition facts
8. Programme VI models for availability of educational warrants (without redefining those models)

> **Conditions permit contextual representation updates.  
> Conditions do not invent educational recommendations, execute workflows, or transfer authority.**

---

## 1. Purpose

Transitions without conditions become product convenience. Conditions without a catalogue become unenforceable folklore.

This document states **what must be true** — in contextual, authority, and orchestration terms — for each CST-xx move. It introduces **no runtime evaluation algorithms, scores, timers-as-tutors, or scheduling logic**.

---

## 2. Condition Families

Every permitting check is expressed using one or more of these families:

| Family | Meaning | Asks |
|--------|---------|------|
| **C-CONTEXT** | Contextual evidence | Which EST is primary now? Do MS001 entry/exit warrants hold for origin and destination? |
| **C-FLOW** | Lawful workflow progression | Has published WS1 progression / pause / resume / conclude / complete fact occurred that this succession may *reference*? |
| **C-AUTH** | Constitutional authority | Whose educational question is primary? Is ownership preserved? Is mutation forbidden? |
| **C-RULE** | Published orchestration / state rules | Is the move a named CST? Do MS001 catalogue, WS1 transition/completion law, and WS2 disposition law permit the cited facts? |

Optional supporting family (never a substitute for the four above):

| Family | Meaning |
|--------|---------|
| **C-CONT** | Continuity preservation — prior context history remains speakable; EIP-005 not violated by the move |

Conditions are **qualitative constitutional facts**, not computed rankings.

### 2.1 Binding reading of C-FLOW

**C-FLOW may cite** lawful workflow progression or completion as *evidence that a context change is warranted*.

**C-FLOW must never mean** that the Educational State Engine executed the workflow, advanced WT stages, or judged educational success.

---

## 3. Global Preconditions (All Transitions)

Before **any** CST-xx transition (including CST-13 refuse/remain documentation):

| # | Condition | Family |
|---|-----------|--------|
| G1 | The proposed move is a named catalogue transition (CST-01…CST-13) | C-RULE |
| G2 | Origin and destination EST types are published in MS001 (EST-01…EST-12), or CST-13 keeps origin unchanged | C-CONTEXT / C-RULE |
| G3 | The move does not require redefining Programme VI coach / planner meaning | C-AUTH |
| G4 | The move does not transfer, absorb, or invent Authority Model domains | C-AUTH |
| G5 | The move does not create, rank, or assemble educational recommendations | C-AUTH / C-RULE |
| G6 | The move does not execute educational workflows or educational actions | C-FLOW / C-AUTH |
| G7 | The move does not mutate Canonical Study Plan educational intent or Article IV states | C-AUTH |
| G8 | The move does not reinterpret Educational Evidence or mint mastery / success / workflow-completion claims from succession alone | C-AUTH / C-CONTEXT |
| G9 | At most one primary EST remains after the move (unless documented parallel-read) | C-CONTEXT / C-RULE |
| G10 | Learner-owned educational history is preserved (EIP-005) | C-CONT |

Failure of any global precondition ⇒ **transition refused** (prefer CST-13); remain in current primary context and explain.

---

## 4. Conditions by Transition

### CST-01 — Warranted primary succession

| # | Condition | Family |
|---|-----------|--------|
| 01.1 | Current primary is EST-xx; proposed destination is a distinct published EST-yy | C-CONTEXT |
| 01.2 | MS001 exit conditions for EST-xx hold, or a documented supersede path applies | C-CONTEXT / C-RULE |
| 01.3 | MS001 entry conditions for EST-yy hold | C-CONTEXT / C-RULE |
| 01.4 | A more specialised CST (02–12) does not exclusively own this succession shape — or CST-01 is explicitly used as the general class with specialised conditions also satisfied | C-RULE |
| 01.5 | Any cited WS1 progression / completion fact is a published lawful fact, not inventing stage movement | C-FLOW / C-RULE |
| 01.6 | Primary Programme VI / WS2 owner for the destination question is identifiable and unchanged in ownership map | C-AUTH |

**Fails when:** destination EST entry unmet; exit of prior required but unmet; move would invent a tip or rewrite ownership; product wants a “fresh mode” without warrant.

---

### CST-02 — Nested context open

| # | Condition | Family |
|---|-----------|--------|
| 02.1 | Origin primary is EST-03 (or other published nest-capable parent warrant) | C-CONTEXT |
| 02.2 | Destination is EST-04 or EST-05 | C-CONTEXT |
| 02.3 | MS001 entry for Session / Reflection holds (lawful session start or reflection warrant) | C-CONTEXT / C-RULE |
| 02.4 | Active-class Canonical Study Plan (or other published nest support) remains available as constraint | C-CONTEXT / C-AUTH |
| 02.5 | If a WS1 session / reflection workflow progression is cited, it is a published lawful fact — not executed by this transition | C-FLOW / C-RULE |
| 02.6 | Nest open does not claim day question concluded or mission mastered | C-AUTH / C-CONTEXT |

**Fails when:** no lawful session/reflection warrant; attempt to open EST-04 from EST-01 without plan; tip invention mid-open.

---

### CST-03 — Nested context return

| # | Condition | Family |
|---|-----------|--------|
| 03.1 | Origin primary is EST-04 and/or EST-05 | C-CONTEXT |
| 03.2 | MS001 exit for Session / Reflection holds (ended, abandoned, interrupted, or reflection concluded / deferred under published law) | C-CONTEXT / C-RULE |
| 03.3 | Destination EST-03 / EST-12 / other primary has MS001 entry satisfied | C-CONTEXT |
| 03.4 | Prior nest remains narratable (continuity); history not erased | C-CONT |
| 03.5 | Any cited WS1 session-completion / reflection-completion fact is published and lawful — not judged as learner mastery | C-FLOW / C-AUTH |

**Fails when:** nest still live under MS001; destination entry unmet; return used to mint mastery or Study Progress.

---

### CST-04 — Absent-plan enter

| # | Condition | Family |
|---|-----------|--------|
| 04.1 | No Active-class Canonical Study Plan remains for the learner’s study context (never existed, or lawfully ended/archived) | C-CONTEXT / C-AUTH |
| 04.2 | Destination EST-01 entry conditions hold | C-CONTEXT / C-RULE |
| 04.3 | Prior primary exit (if any) is recorded; plan absence is not smuggled as “exam mode” | C-CONTEXT / C-RULE |
| 04.4 | No independent Programme VII tip is created to “cover” absence | C-AUTH |

**Fails when:** Active plan still exists; EST-09 forced by calendar alone; tips invented for empty plan.

---

### CST-05 — Plan-contract succession

| # | Condition | Family |
|---|-----------|--------|
| 05.1 | Origin primary is EST-01 | C-CONTEXT |
| 05.2 | An Active-class Canonical Study Plan has been lawfully published / activated under Master Planner / Scheduling authority | C-AUTH / C-CONTEXT |
| 05.3 | Destination EST-02 / EST-03 / EST-12 entry conditions hold as warrants dictate | C-CONTEXT / C-RULE |
| 05.4 | Plan activation is not treated as syllabus mastery or educational success | C-AUTH |
| 05.5 | If WS1 structural workflow progression is cited, it remains a referenced fact — State Engine does not publish the plan | C-FLOW / C-AUTH |

**Fails when:** no Active plan yet; destination forced to EST-03 while structural work is still primary without warrant; mastery theatre.

---

### CST-06 — Structural focus open / close

| # | Condition | Family |
|---|-----------|--------|
| 06.1 | **Open:** structural educational question is primary; Master Planner (or Scheduling under plan authority) is the invited primary owner | C-AUTH / C-CONTEXT |
| 06.2 | **Open:** destination EST-02 entry holds; prior primary exits or supersedes under MS001 / WS1 conflict law | C-CONTEXT / C-RULE |
| 06.3 | **Close:** EST-02 exit holds (plan published/updated/refused under plan law, or supersession) | C-CONTEXT / C-AUTH |
| 06.4 | **Close:** successor destination entry holds | C-CONTEXT |
| 06.5 | Canonical Study Plan is not rewritten by the CST act itself | C-AUTH |
| 06.6 | Cited WS1 escalate / structural progression facts are published lawful references only | C-FLOW / C-RULE |

**Fails when:** day coach absorbs structural ownership; CST used to mutate plan cells; calendar anxiety forces EST-02 without plan authority warrant.

---

### CST-07 — Coach-focus succession

| # | Condition | Family |
|---|-----------|--------|
| 07.1 | Origin and destination are distinct members of {EST-03, EST-06, EST-07, EST-08, EST-09} | C-CONTEXT |
| 07.2 | Origin MS001 exit (or supersede) holds; destination MS001 entry holds | C-CONTEXT / C-RULE |
| 07.3 | Destination coach domain remains the WS2 owner of that educational question — ownership map unchanged by CST | C-AUTH |
| 07.4 | Destination warrant is the Programme VI warrant for that coach (disruption for recovery, revision law for revision, exam law for exam, etc.) — not UI preference alone | C-CONTEXT / C-AUTH |
| 07.5 | No mega-context merge of multiple coach primaries | C-RULE / C-AUTH |
| 07.6 | Any cited WS1 handoff / supersede progression is a published fact, not coach blending by State Engine | C-FLOW / C-RULE |

**Fails when:** revision used as first-learning disguise; recovery exit narrated as “you succeeded”; exam context from calendar alone; tip minted by State Engine.

---

### CST-08 — Conflict-await enter

| # | Condition | Family |
|---|-----------|--------|
| 08.1 | Concurrent valid recommendation set recognised under Conflict Resolution law | C-AUTH / C-RULE |
| 08.2 | Disposition pending or disposition speech is the live coordination focus | C-CONTEXT / C-AUTH |
| 08.3 | Destination EST-10 entry conditions hold | C-CONTEXT / C-RULE |
| 08.4 | State Engine does not rank or invent a merged tip | C-AUTH |
| 08.5 | Published WS2 conflict rules are the cited C-RULE basis — not ad-hoc product ranking | C-RULE |

**Fails when:** single tip already settled as primary focus; attempt to use EST-10 to transfer ownership; Evidence rewrite “to resolve conflict.”

---

### CST-09 — Conflict-await exit

| # | Condition | Family |
|---|-----------|--------|
| 09.1 | Origin primary is EST-10 | C-CONTEXT |
| 09.2 | Lawful RO disposition applied **or** concurrency cleared under Conflict Resolution law | C-AUTH / C-RULE |
| 09.3 | Destination primary EST entry holds | C-CONTEXT |
| 09.4 | Disposition was performed by WS2 Conflict Resolution — not by CST label | C-AUTH |
| 09.5 | Continuity of conflict narration preserved when material | C-CONT |

**Fails when:** exit without disposition or cleared concurrency; State Engine claims to have “picked the winner.”

---

### CST-10 — Escalation-await enter

| # | Condition | Family |
|---|-----------|--------|
| 10.1 | Workflow / orchestration authorises escalate / await outcome under published WS1 law | C-FLOW / C-RULE |
| 10.2 | Structural or ownership question exceeds current coach envelope; tip invention refused | C-AUTH / C-CONTEXT |
| 10.3 | Destination EST-11 entry conditions hold | C-CONTEXT / C-RULE |
| 10.4 | No independent Programme VII tip is created while awaiting | C-AUTH |

**Fails when:** await used as motivational tip theatre; EST-11 entered without escalate/await authorisation; ownership rewritten.

---

### CST-11 — Escalation-await exit

| # | Condition | Family |
|---|-----------|--------|
| 11.1 | Origin primary is EST-11 | C-CONTEXT |
| 11.2 | Escalation target concluded, refuse remains, **or** a new primary warrant lawfully supersedes under published rules | C-AUTH / C-RULE / C-FLOW |
| 11.3 | Destination EST entry holds (often EST-02) | C-CONTEXT |
| 11.4 | Exit does not mint tips or mutate the plan via CST | C-AUTH |

**Fails when:** impatience forces day tips while structural question unresolved; exit narrated as educational success.

---

### CST-12 — Continuity hold enter / exit

| # | Condition | Family |
|---|-----------|--------|
| 12.1 | **Enter:** Active-class Canonical Study Plan present; no primary day / learning / recovery / revision / exam / structural / conflict / escalation warrant currently constitutive — **or** prior primary exited without immediate successor | C-CONTEXT / C-RULE |
| 12.2 | **Enter:** destination EST-12 entry holds | C-CONTEXT |
| 12.3 | **Exit:** a classified educational event / warrant makes another EST type primary; destination entry holds | C-CONTEXT / C-RULE |
| 12.4 | Holding is not treated as workflow completion or student failure | C-AUTH / C-CONTEXT |
| 12.5 | Continuity of prior educational history preserved | C-CONT |

**Fails when:** inventing focus to avoid “empty” UI; treating hold as mastery plateau; erasing prior focus history.

---

### CST-13 — Refuse / remain

| # | Condition | Family |
|---|-----------|--------|
| 13.1 | A proposed succession was evaluated against CST-01…CST-12 and failed one or more required conditions **or** global preconditions | C-RULE / C-CONTEXT |
| 13.2 | Primary EST remains the current published primary | C-CONTEXT |
| 13.3 | Refusal is recorded as the lawful outcome — not a soft/silent transition | C-RULE |
| 13.4 | Explanation remains available (why succession was refused) | C-RULE / C-CONT |

**Fails when:** product silently changes EST anyway; refuse used to invent an undocumented mode.

---

## 5. Condition Evidence vs Educational Evidence

| May cite as contextual / orchestration evidence | Must not treat as |
|-------------------------------------------------|-------------------|
| Active vs absent plan class | Estimated Mastery |
| Programme VI warrant IDs / coach-question primacy | Educational Evidence of understanding (EIP-002 rewrite) |
| Published WT progression / completion facts | Proof the State Engine executed the workflow |
| WS2 RO disposition records | Tip authored by State Engine |
| Continuity hold / prior EST history | Erasure licence |

---

## 6. Binding Summary

Contextual state transitions are permitted only when **C-CONTEXT**, **C-FLOW** (when progression is material), **C-AUTH**, and **C-RULE** facts hold — plus **C-CONT** continuity preservation. Conditions never authorise algorithms, tip invention, ownership transfer, meaning rewrite, or workflow execution by the Educational State Engine.

# EV-001A — Educational Evidence Contract

**Programme:** EV-001A · Educational Evidence Contract  
**Date:** 2026-07-30  
**Nature:** P4 Foundation — constitutional definition only  
**Authority:** SR-001 · SR-001A · LXP-003 · LXP-004A  
**Predecessor:** LXP-004A (P3 Educational Session Substance)  
**Successor (implementation):** EV-001B (Evidence Before Completion)  
**Constraint:** No application code modified. This programme defines **what** educational evidence is. It does **not** implement Evidence Before Completion, Twin writes, progress advancement, mission completion, or readiness mutation.

---

## Executive Summary

The Student Runtime now supports a continuous educational loop:

```
Mission → Study Session → Learning Objectives → Reading → Worked Example
  → Practice → Reflection → Finish Review
```

SR-001 requires **Evidence Before Completion**: Twin updates, lawful progress, and mission completion must follow evidence — not coverage theatre, Mark-complete alone, or session duration.

Before EV-001B wires that gate, this contract establishes the constitutional answer to:

> What does the Student Runtime recognise as educational evidence, and what may each kind of evidence lawfully do?

**Verdict of this programme:** Evidence is a ranked, attributable observation of educationally meaningful happenings. Activity is not evidence. Participation is not understanding. Session completion is not mastery. Reflection and confidence are soft signals. Only graded, accepted evidence may advance progress, update the Twin, complete missions, or contribute to readiness — and only within the authority matrix defined here.

This document becomes the **constitutional reference** for every future Evidence, Progress, Twin, and Readiness implementation on the Student Runtime path. It specialises EIP-002 (`EDUCATIONAL_EVIDENCE_MODEL.md`, `EDUCATIONAL_EVIDENCE_AUTHORITY.md`) for the Mission → Session daily loop without amending the Educational Constitution.

---

## Evidence Philosophy

### Why evidence exists

Kwalitec coaches students for demanding professional examinations. Trust collapses when the platform narrates *knowing*, *mastery*, or *readiness* from administrative convenience: a button click, a finished timer, a reading page view, or a Home “Mark mission complete.”

Educational evidence exists so that material claims about learning rest on **observed educational happenings**, ranked by epistemic strength, and consumed only by systems authorised to act on that rank.

### Seven distinctions that must never collapse

| Concept | Definition | Primary question | Lawful role on Student Runtime |
|---|---|---|---|
| **Activity** | Something the student or system did or scheduled (open session, open reading, submit form, pause, navigate). | What happened as an action? | May drive UX and session FSM. Is not, by itself, understanding. |
| **Participation** | Attributable engagement with a planned learning stage (student entered and interacted with Read / Example / Practice / Reflect). | Did the student engage with the planned stage? | May support Behavioural evidence and Finish Review honesty. Does not prove comprehension. |
| **Completion** | A bounded commitment finished under its contract (activity submitted, session closed with Finish Review, mission lifecycle Completed). | Was the planned unit finished? | May close session / mission **only** under this contract’s authority columns. Never equals mastery. |
| **Understanding** | Demonstrated or strongly supported grasp of syllabus-bound objectives (practice outcomes, assessments). | What observations support claims about grasp? | Requires Educational-grade (or higher) accepted evidence. |
| **Mastery** | Accumulated, warranted competence estimate over time — Twin-owned Estimated Mastery / Knowledge State. | How well is this understood as an estimate? | Requires Mastery- or Constitutional-grade evidence; never a single Finish Review Yes. |
| **Confidence** | Student-felt self-assessment of how sure they feel. | How confident does the student feel? | Soft signal only. Never authors progress, Twin estimates, or mastery speech alone. |
| **Reflection** | Deliberate metacognitive report (what was hard, clear, unfinished; insights; gaps). | What does the student notice about their learning? | Soft Educational Observation / Informational–Behavioural. Skip allowed (LXP-004A). Never scores Twin alone (SR-001 stage contract). |

### Succession law (Student Runtime)

```
Activity
   ↓  (only when the activity yields a qualifying observation)
Educational Observation
   ↓  (validation + grade + authority)
Authorised Educational Evidence
   ↓  (interpretation; never invention)
Inference (Twin / Readiness / Progress derivation)
   ↓
Mission Complete → Tomorrow
```

Activity without a qualifying observation does not enter the Evidence domain.  
Inference without Evidence is educational fiction.  
Knowledge without Evidence succession is unconstitutional certainty.

### Relationship to coverage

| Question | Owner | Must not be confused with |
|---|---|---|
| What have I studied? | Progress Engine (Study Progress / coverage) | Understanding |
| What observations support understanding claims? | Evidence Pipeline + Twin | Coverage checkboxes |
| Did today’s planned study occur? | Finish Review + session completion | Mastery |
| What should I do next? | Mission composition (Progress + Twin + curriculum) | Evidence itself |

A student may lawfully have session history while Educational Evidence for understanding remains empty. In that case Kwalitec may narrate honesty and must withhold mastery certainty.

### Alignment with prior authority

| Source | Binding contribution |
|---|---|
| SR-001 | One Evidence Pipeline; Evidence Before Completion; Twin after evidence; Study ≠ understanding |
| SR-001A P4 | Session complete blocked unless Evidence Authority accepts **or** explicit Partial/No recorded; coverage only under Evidence contract |
| LXP-003 | Finish Review Yes / Partially / No; session close ≠ mission complete; `progress_advanced=False` until P4 |
| LXP-004A | Continuous Read → Example → Practice → Reflect; reflection skip allowed; no Twin scoring from reflection alone |
| EIP-002 Model / Authority | Global meaning of Educational Evidence; V1.0 Twin-authorised catalogue (structured question / reserved assessment results) |
| Digital Twin Philosophy | Evidence before inference; Twin observes, does not teach |

**EV-001A does not replace EIP-002.** It binds the Student Runtime daily loop to those principles with stage-specific types, grades, and consumer permissions required by SR-001.

---

## Evidence Taxonomy

Every evidence type below is a **named observation class**. Types may be *generated* by LearningSessionRuntime (or adapters) but are **authoritative only after** lifecycle Validated → Accepted (see Evidence Lifecycle). Until EV-001B, generation may remain stubbed (`evidence_emitted=False`); meaning is still fixed by this contract.

### A. Stage evidence (educational flow)

| ID | Evidence type | Educational meaning | Typical grade | Notes |
|---|---|---|---|---|
| **EV-RT-01** | Learning objectives presented | Student was shown syllabus-bound objectives for the sitting | Informational | Presentation fact; not participation |
| **EV-RT-02** | Reading started | Student opened the reading stage | Informational | Navigation / activity |
| **EV-RT-03** | Reading completed | Student submitted / advanced past reading with attributable engagement | Behavioural | Exposure; **not** understanding |
| **EV-RT-04** | Worked example started | Student opened worked-example stage | Informational | |
| **EV-RT-05** | Worked example completed | Student finished the method walkthrough stage | Behavioural | Method exposure; not demonstrated application |
| **EV-RT-06** | Practice attempted | Student submitted a practice response (outcome may be unknown / unscored) | Behavioural → Educational* | *Educational only when outcome is attributable and scorable |
| **EV-RT-07** | Practice correct | Practice response scored correct against authorised criteria | Educational (→ Mastery with accumulation) | Strongest in-session understanding signal on daily loop |
| **EV-RT-08** | Practice incorrect | Practice response scored incorrect | Educational | Lawful negative signal; still evidence of attempt quality |
| **EV-RT-09** | Practice partial / unscored | Response recorded without authorised scoring | Behavioural | History only until scoring exists |
| **EV-RT-10** | Reflection submitted | Student recorded structured or free reflection | Behavioural (soft) | Never Twin-scoring alone |
| **EV-RT-11** | Reflection skipped | Student used lawful skip | Informational | Lawful (LXP-004A); not a negative mastery claim |
| **EV-RT-12** | Confidence reported | Felt confidence captured on reflection or review | Informational (soft) | Never sole Twin / progress writer |

### B. Session lifecycle evidence

| ID | Evidence type | Educational meaning | Typical grade | Notes |
|---|---|---|---|---|
| **EV-RT-20** | Session started | LearningSessionRuntime entered ACTIVE for a mission | Informational | Spine fact |
| **EV-RT-21** | Session paused | Student paused; progress surface retained | Informational | Recovery, not learning proof |
| **EV-RT-22** | Session resumed | Student returned to same `session_id` | Informational | |
| **EV-RT-23** | Finish review — Yes | Student asserts today’s planned study was engaged | Behavioural | Session-completion candidate; **not** mastery |
| **EV-RT-24** | Finish review — Partially | Student asserts partial engagement | Behavioural | Explicit Partial under G-Evidence |
| **EV-RT-25** | Finish review — No | Student asserts planned study did not occur | Behavioural | Explicit No under G-Evidence; blocks Twin-grade claims |
| **EV-RT-26** | Session completed | Session FSM reached COMPLETED under policy | Behavioural | Requires Finish Review when product flag ON (LXP-003) |
| **EV-RT-27** | Skipped activity | Student advanced past an optional or unavailable stage (e.g. no worked example) | Informational / Behavioural | Must not invent substance |
| **EV-RT-28** | Partial completion | Sitting closed with incomplete planned stages + Partial review | Behavioural | Honest understatement |
| **EV-RT-29** | Abandoned session | Session left without Finish Review / completion (timeout, crash, quiet leave without pause contract) | Informational | Must not auto-complete mission |

### C. Mission & progress evidence (pipeline outcomes)

| ID | Evidence type | Educational meaning | Typical grade | Notes |
|---|---|---|---|---|
| **EV-RT-30** | Mission accepted | Mission Accepted ≡ session start (SR-002) | Informational | Not completion |
| **EV-RT-31** | Mission deferred | ILE-004 defer; no session | Informational | No TOPIC_COMPLETED |
| **EV-RT-32** | Mission completed (lifecycle) | Mission lifecycle Completed after lawful evidence contract | Behavioural / Educational† | †Educational only when backed by accepted Educational+ evidence or Board-defined coverage contract — never Mark-complete theatre |
| **EV-RT-33** | Topic coverage advanced | Progress Engine records coverage / `TOPIC_COMPLETED` | Behavioural (coverage) | **Not** understanding Evidence; never Twin-grade alone |
| **EV-RT-34** | Mark-complete (pilot) | Offline / pilot confirm without session evidence path | Informational / forbidden for Twin | Flag-gated; non-default; **cannot** claim Twin-grade or unscoped mastery (SR-001A) |

### D. Assessment-class evidence (EIP-002 V1.0 catalogue — reserved on daily loop)

These remain the **only** V1.0 sources authorised to enter Twin-owned Estimated Knowledge / Mastery under EIP-002 Authority. The Student Runtime practice path becomes Educational-grade when it produces equivalent attributable scored outcomes; until then, silence is preferred.

| ID | Evidence type | Typical grade | Status on Student Runtime daily loop |
|---|---|---|---|
| **EV-RT-40** | Structured question results | Educational / Mastery | Live interim pathway (EIP-002); wire when session practice yields accuracies |
| **EV-RT-41** | Quiz results | Educational / Mastery | Reserved — silence |
| **EV-RT-42** | Mission assessment results | Educational / Mastery | Reserved — silence |
| **EV-RT-43** | Mock examination results | Mastery / Constitutional | Reserved — silence |
| **EV-RT-44** | Official examination results | Constitutional | Reserved — silence |

### E. Telemetry that is not educational evidence of understanding

| ID | Observation | Grade if retained | Rule |
|---|---|---|---|
| **EV-RT-90** | Session duration / time-on-task | Informational | Workload analytics only |
| **EV-RT-91** | Button clicks / navigation | Informational | UX telemetry; never Evidence domain for understanding |
| **EV-RT-92** | Checklist ticks alone | Informational | UI state; not mastery |
| **EV-RT-93** | Recommendation accept / dismiss | Informational | Decision Journal preference — not understanding |

---

## Authority

Authority answers five consumer questions for each evidence type. Values:

- **Yes** — lawful when evidence is Accepted at the stated grade  
- **No** — never, even if Accepted  
- **Conditional** — only under explicit subordinate rule (noted)  
- **Contribute** — may inform a composite; never sole warrant for the claim

### Authority matrix — stage & session evidence

| Evidence type | Advance Progress? | Update Twin? | Satisfy session completion? | Satisfy mission completion? | Contribute to readiness? |
|---|---|---|---|---|---|
| Learning objectives presented | No | No | No | No | No |
| Reading started | No | No | No | No | No |
| Reading completed | No | No | Contribute‡ | No | No |
| Worked example completed | No | No | Contribute‡ | No | No |
| Practice attempted (unscored) | No | No | Contribute‡ | No | Contribute (weak) |
| Practice correct | Conditional§ | Conditional¶ | Contribute‡ | Conditional§ | Contribute |
| Practice incorrect | Conditional§ | Conditional¶ | Contribute‡ | Conditional§ | Contribute |
| Reflection submitted | No | No | Contribute‡ | No | Contribute (weak calibration) |
| Reflection skipped | No | No | Contribute‡ | No | No |
| Confidence reported | No | No | No | No | Contribute (weak calibration) |
| Finish review — Yes | No alone | No | **Yes** | Conditional# | Contribute (coverage honesty) |
| Finish review — Partially | No alone | No | **Yes** | Conditional# | Contribute (understatement) |
| Finish review — No | No | No | **Yes** | Conditional# (typically blocks advancement) | No (blocks Twin-grade readiness claims) |
| Session completed | No alone | No | — (is the session close) | Conditional# | Contribute |
| Skipped activity | No | No | Contribute‡ | No | No |
| Partial completion | No alone | No | **Yes** (with Partial review) | Conditional# | Contribute (understatement) |
| Abandoned session | No | No | No | No | No |
| Mission completed (lifecycle) | Conditional§ | No alone | — | — (is the mission close) | Contribute |
| Topic coverage advanced | — (is progress) | No | — | — | Contribute as coverage fact only |
| Mark-complete (pilot) | Conditional (Board residual only) | **No** | N/A (bypasses session) | Conditional (non-product) | **No** Twin-grade |
| Structured question / assessment results | Conditional§ | **Yes** (EIP-002) | Contribute | Conditional§ | **Yes** (estimate path) |
| Session duration / clicks | No | No | No | No | No |

‡ **Session completion:** When `SR_SESSION_COMPLETION_PRODUCT` is ON, session close requires Finish Review (Yes / Partially / No). Stage evidence supports honesty and future gates but does not replace Finish Review.  
§ **Progress / mission:** Only after Evidence Authority accepts a completion package under EV-001B; coverage may advance when the Board-defined completion contract for that topic is met — never from reading-only or reflection-only packages.  
¶ **Twin:** Only when the observation is Accepted as Educational-grade or higher **and** matches an EIP-002 authorised source (or successor catalogue amendment). Practice correct/incorrect updates Twin only when scored outcomes are authorised Structured Question (or reserved) results.  
# **Mission completion:** SR-001A G-Evidence — blocked unless EducationalEvidenceAuthority accepts **or** explicit Partial/No is recorded. Partial/No may close the sitting honestly without Twin-grade or unscoped `TOPIC_COMPLETED` mastery claims.

### Authority summary law

1. **Session completion** may be satisfied by Finish Review alone (LXP-003 product contract).  
2. **Mission completion** and **Progress advancement** require the Evidence Before Completion gate (EV-001B), not Finish Review Yes alone as understanding.  
3. **Twin** updates only after Accepted Educational / Mastery / Constitutional evidence on an authorised source.  
4. **Readiness** may consume Twin estimates and coverage facts; it must not mint understanding from Informational telemetry.

---

## Evidence Grades

Grades are epistemic classes. They determine **claim lawfulness**, not UI chrome. They align with EIP-002 Quality Levels / Constitution Article V ranks without renaming that corpus.

| Grade | Epistemic class | What it may support | What it must never support alone |
|---|---|---|---|
| **Informational** | System or navigation fact | Debugging, analytics counts, recovery, founder observability | Progress, Twin, understanding, mastery, readiness as competence |
| **Behavioural** | Attributable participation / completion of planned activity | Session honesty, Finish Review context, workload patterns, coverage *when* Board contract says coverage is behavioural | Twin-owned Estimated Knowledge / Mastery; “student understands X” |
| **Educational** | Attributable performance outcome on syllabus-bound practice/assessment | Understanding estimates; mission/progress under Evidence contract; readiness contribution | Lasting Mastered-stage speech from a single observation |
| **Mastery** | Accumulated Educational evidence meeting density / spacing rules | Twin Estimated Mastery / Knowledge State evolution; stronger readiness speech | Certainty theatre; single-sitting mastery certificates |
| **Constitutional** | Highest-warrant outcomes (e.g. official examination results under catalogue) | Strongest lawful estimates and institutional claims under Constitution | Invention; use as daily-loop substitute for missing practice evidence |

### Grade assignment rules

1. Grade is assigned at **Validation**, not by the emitting UI label.  
2. A type has a **ceiling grade** (taxonomy “Typical grade”); Validation may only lower, never inflate.  
3. Soft signals (reflection, confidence, duration) have ceiling **Informational** or **Behavioural** — never Educational+ for understanding claims.  
4. Finish Review is ceiling **Behavioural**.  
5. Scored practice / structured questions may reach **Educational**; **Mastery** requires accumulation (EIP-002 `MIN_AUTHORISED_OBSERVATIONS_FOR_HIGH_MASTERY` and EL-007).  
6. Absence of evidence is **uncertainty**, not weak mastery as fact.

### Mapping to EIP-002 (informative)

| EV-001A grade | EIP-002 Quality Level (approx.) |
|---|---|
| Informational | Level 0 — Administrative / telemetry |
| Behavioural | Level 1 — Engagement |
| Educational | Level 2–3 — Performance / structured outcome |
| Mastery | Level 3 with accumulation |
| Constitutional | Level 4 — examination-class |

---

## Evidence Lifecycle

Evidence is not instantaneous truth. Every observation traverses a defined lifecycle. Consumers may act **only** on states lawful for their purpose.

```
Generated → Validated → Accepted → Persisted → Consumed → Archived
                ↘ Rejected
```

| State | Meaning | Who owns the transition | Consumer rule |
|---|---|---|---|
| **Generated** | Candidate observation emitted from session/activity/telemetry | LearningSessionRuntime / collectors (EV-001B) | Must not advance Progress, Twin, mission, or readiness |
| **Validated** | Schema, attribution (student, enrolment, session, topic), and grade ceiling checked | EducationalEvidenceAuthority (+ policies) | Still not consumable for Twin/progress |
| **Accepted** | Authority admits the observation into the Evidence domain at a grade | EducationalEvidenceAuthority | May be Persisted; eligible for Consumed per authority matrix |
| **Rejected** | Fails validation, fails catalogue, or is non-authoritative for claimed grade | EducationalEvidenceAuthority | May retain as Informational history; must not inflate claims |
| **Persisted** | Durable record retained (no silent rewrite) | Evidence / learning-evidence persistence | History of truth; expiry only by named educational rules |
| **Consumed** | Downstream system applied Accepted evidence under matrix permissions | Progress, Twin, Readiness, Mission, Journal, Analytics | Must record consumer identity; idempotent where possible |
| **Archived** | Retained for audit; no longer active for live inference | Retention / founder audit paths | May not silently re-activate as fresh Mastery evidence |

### Lifecycle invariants

1. **Generated ≠ Accepted.** Emitting `evidence_emitted` stubs without Authority is not acceptance.  
2. **Rejected evidence is not failure of the student** — it is refusal of an unlawful claim.  
3. **Partial/No Finish Review** may be Accepted as Behavioural session evidence while Twin/Mastery claims remain Rejected.  
4. Rollback of EV-001B flags must **not delete** Persisted rows (SR-001A).  
5. Inference may revise estimates as history grows; it may not mint new Accepted evidence by renaming recommendations as observations.

---

## Consumer Matrix

| Consumer | Consumes | May write from evidence? | Forbidden |
|---|---|---|---|
| **Progress Engine** | Accepted Behavioural+ under completion contract; coverage events | Coverage / Study Progress only when matrix allows | Treating coverage as Twin mastery; dual writers disagreeing on topic |
| **Student Digital Twin** | Accepted Educational+ on EIP-002 authorised sources | Estimated Knowledge / Mastery / Knowledge State after evidence succeeds | Updates from Mark-complete, reading-only, reflection-only, duration, Finish Review alone |
| **Readiness** | Twin estimates + coverage facts + Educational outcomes | Readiness projections / narratives | Inventing competence from Informational telemetry; one scalar pretending two constructs without warrant |
| **Mission Engine / EducationalRuntimeEngine** | Session + Evidence gate outcomes | Mission lifecycle Completed; next composition inputs | Completing mission from Home Mark-complete as product Primary; TOPIC_COMPLETED without contract |
| **Decision Journal** | Reflection / commitment / preference observations | Memory-grade reflective records when REF-001 warrants | Scoring Twin from Journal alone; using Journal as Progress writer |
| **Analytics** | Persisted observations at any grade (labelled) | Aggregate metrics, cohort honesty | Student-facing mastery speech from Informational series |
| **Founder dashboards / Feedback Hub** | Ops projections of pipeline health, gates, residual risks | Operator visibility | Becoming a second student Progress or Twin writer |

### Presentation rule

Student-facing surfaces prefer plain language (practice results, how you did, study check). Internal domains retain the constitutional term **Educational Evidence**. Founder surfaces may show grades and gate status; they must not author student educational state.

---

## Non-Authoritative Evidence

The following must **NEVER**:

- advance Progress (Study Progress / `TOPIC_COMPLETED`),  
- update Twin-owned estimates, or  
- claim understanding or mastery  

even when Persisted as history.

| Observation | Why non-authoritative for those claims |
|---|---|
| **Reading only** (EV-RT-03 alone) | Exposure ≠ comprehension |
| **Worked example only** | Method viewing ≠ demonstrated application |
| **Reflection only** (EV-RT-10) | Metacognition ≠ validated knowledge; SR-001 forbids Twin scoring from reflection alone |
| **Confidence only** (EV-RT-12) | Felt confidence is student-owned soft signal |
| **Session duration / time-on-task** (EV-RT-90) | Effort ≠ understanding |
| **Button clicks / navigation** (EV-RT-91) | Telemetry ≠ educational outcome |
| **Checklist ticks alone** (EV-RT-92) | UI state ≠ evidence |
| **Finish Review Yes alone** | Planned study occurred ≠ mastery or Twin warrant |
| **Mission completed / Mark-complete alone** | Coverage theatre; EIP-002 unauthorised for Twin |
| **Recommendation accept/dismiss** | Preference ≠ performance |
| **Abandoned session** | Incomplete sitting; no auto-complete |
| **Learning objectives presented** | Presentation fact only |

**Package rule:** A completion package composed solely of non-authoritative observations must be **Rejected** for Progress advancement, Twin update, and understanding claims. It may still support session completion via Finish Review (Behavioural honesty).

---

## Constitutional Rules

Future programmes — including EV-001B, SDT-004, SR-003, and readiness work — **may never violate** the following.

### C1 — Evidence Before Completion

No default product path may complete a Mission or advance Twin-grade progress without Accepted evidence under this contract **or** an explicit Finish Review Partial/No recorded for honest non-advancement (SR-001 gate G-Evidence).

### C2 — Study ≠ understanding

Coverage, session completion, and Finish Review Yes are not understanding. Student speech and founder metrics must keep the distinction.

### C3 — Twin after evidence

The Student Digital Twin updates only after EducationalEvidenceAuthority success on authorised Educational+ evidence. Twin observes; it does not teach; it does not invent evidence.

### C4 — One Evidence Pipeline

Presentation, Session Experience adapters, Unified Journey chrome, and Founder tools must not become second evidence authorities. LearningSessionRuntime emits candidates; EducationalEvidenceAuthority accepts or rejects.

### C5 — Grade ceilings are binding

No consumer may treat Informational or Behavioural evidence as Educational or Mastery by renaming, aggregation theatre, or UI emphasis.

### C6 — Reflection and confidence are soft

Reflection may be skipped. Reflection and confidence must not alone update Twin estimates, advance Progress, or author Mastered-stage language.

### C7 — Silence over fiction

Where authorised Educational+ pathways do not yet exist for a sitting, the system leaves Twin-owned educational states unchanged. Correct silence beats artificial certainty.

### C8 — Non-authoritative package rejection

Reading-only, reflection-only, duration-only, click-only, or Mark-complete-only packages cannot satisfy Progress advancement, Twin update, or understanding claims.

### C9 — Explicit Partial/No is lawful honesty

Finish Review Partially / No must be recordable, Persisted, and must not be coerced into Yes. They satisfy session-completion honesty; they do not mint mastery.

### C10 — Idempotent persistence

Evidence rows are not deleted on feature-flag rollback. Estimates may freeze; history remains.

### C11 — Curriculum identity

Evidence attribution must bind to syllabus-bound topic / objective identity coherent with Mission briefing (MISSION-002 / P0). No `node-*` leakage into student-facing evidence speech.

### C12 — No dual educational state

Evidence consumers must not create a second current topic, second Twin, or second Progress writer that disagrees with the One Educational State singularity (SR-001).

---

## Future Integration

### Pipeline position (normative)

```
Mission Brief
  → Study Session (LearningSessionRuntime AUTHORITY)
  → Read → Worked Example → Practice → Reflect
  → Finish Review (LXP-003)
  → Evidence Pipeline (this contract → EV-001B gate)
  → Student Digital Twin (SDT-004; after Accepted Educational+)
  → Progress Engine (lawful coverage only)
  → Mission Complete
  → Tomorrow
```

### Flag expectation (SR-001A)

| Flag | Phase | Role |
|---|---|---|
| `SR_SESSION_PRIMARY` | P1 | Spine |
| `SR_SESSION_COMPLETION_PRODUCT` | P2 | Finish Review |
| `SR_SESSION_SUBSTANCE` | P3 | Educational flow |
| `SR_EVIDENCE_GATE` | P4 | Evidence Before Completion (EV-001B) |

### Existing code authorities (do not invent parallels)

| Concern | Authority path |
|---|---|
| Evidence gate | `app/services/educational_evidence_authority.py` |
| Evidence model | `knowledge/educational/EDUCATIONAL_EVIDENCE_MODEL.md` |
| Session emission (future) | LearningSessionRuntime evidence collector / VP-001 bridges |
| Twin observation | Student Digital Twin + learner lifecycle orchestrator |
| Session FSM | `LearningSessionRuntime` |
| HTTP | Session Experience `/session/*` (ADAPTER only) |

### What EV-001A deliberately leaves unimplemented

- Evidence Authority wiring on `/session/*` complete  
- Mission completion from session evidence  
- Progress `TOPIC_COMPLETED` from evidence packages  
- Twin birth/update on published path  
- Readiness formula changes  
- Decision Journal memory-grade reflection writes (REF-001)

---

## Recommendation for EV-001B

**EV-001B — Evidence Before Completion** should implement the gate, not redefine meaning.

### Scope (recommended)

1. Emit candidate evidence from LearningSessionRuntime stage outcomes + Finish Review into the Evidence Pipeline.  
2. Validate and Accept/Reject per this contract’s taxonomy, grades, and authority matrix.  
3. Enforce `SR_EVIDENCE_GATE`: session → mission complete blocked unless Authority accepts **or** explicit Partial/No recorded.  
4. Allow Progress / mission lifecycle writes only for Accepted packages that are not non-authoritative.  
5. Keep Twin writes **off** until SDT-004 (P5), but ensure EV-001B never emits Twin-grade claims from Behavioural-only packages.  
6. Regression suite: complete without evidence rejected; Partial/No recorded without Twin-grade mastery; Mark-complete pilot cannot bypass Twin-grade rules; reflection-only does not update Twin.

### Exit criteria (from SR-001A, restated)

- Gate **G-Evidence** green.  
- Automated tests for accept/reject and Partial/No honesty.  
- Home Mark-complete (if flag ON) cannot emit Twin-grade or unscoped `TOPIC_COMPLETED` without evidence adapter.  
- Prefer keeping gate ON and rolling back Twin (P5) rather than deleting evidence rows.

### Sequencing

Do **not** start SDT-004 Twin activation until EV-001B accepts Educational+ evidence on the daily loop (or Board records residual risk in writing). Prefer P3 substance (`SR_SESSION_SUBSTANCE`) enabled in dogfood so Accepted evidence is educationally meaningful.

---

## Document Control

| Item | Value |
|---|---|
| Status | **Constitutional reference** — binding for Student Runtime evidence programmes |
| Application code modified | **None** |
| Migration impact | **None** |
| Supersedes | Nothing; specialises EIP-002 for SR daily loop |
| Amended by | Future Board-accepted EV / EIP amendments only |

### Architecture compliance

- Preserves LearningSessionRuntime as session AUTHORITY and Session Experience as HTTP ADAPTER.  
- Preserves EducationalEvidenceAuthority as sole evidence gate.  
- Preserves curriculum V1/V2 loadability (no curriculum changes).  
- Aligns with SR-001 singularities: One Evidence Pipeline, Evidence before Twin, Study ≠ understanding.

### Technical debt / known limitations

- EIP-002 V1.0 Twin catalogue is narrower than the full Student Runtime taxonomy; EV-001B must not widen Twin writers without catalogue amendment.  
- Package activity substance may lack scored practice accuracies until LXP-005 / assessment wiring — Educational+ silence remains lawful.  
- This document does not assign numeric weights or half-lives; subordinate architectures may, if constitutionally authorised.

---

**End of EV-001A.**

Until superseded by a Board-accepted amendment:

1. No Student Runtime programme may invent evidence meaning absent from this contract.  
2. No programme may treat non-authoritative observations as Progress, Twin, or understanding warrant.  
3. EV-001B and successors implement gates and wiring; they do not dilute grade ceilings or authority columns.

# Educational Logic Registry

**Capability ID:** EGI-002  
**Programme:** Educational Governance Initiative  
**Classification:** Operational Educational Authority  
**Status:** APPROVED — governing (subordinate to Constitution)  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This Registry is the authoritative operational description of every educational decision currently performed by Kwalitec.

It is subordinate only to:

> **KWALITEC_EDUCATIONAL_CONSTITUTION.md** (EGI-001)

Authority order:

1. Educational Constitution — defines **WHAT** educational truth and meaning are;
2. This Educational Logic Registry — defines **HOW** educational decisions behave;
3. Specialised architectures, policies, and Internal Alpha doctrines — design compliant systems;
4. Implementation — realises governed behaviour.

**No implementation may introduce educational logic that is not first represented in this Registry.**

This document contains no code, no algorithms, and no mathematical formulae. It specifies educational behaviour, ownership, visibility, constraints, and the relationship of each logic to the Constitution.

Where current product behaviour differs from constitutional intent, the difference is recorded explicitly under **Current Implementation Status**. Differences are not silently reconciled.

---

## Table of Contents

1. [EL-001 — Study Progress](#el-001--study-progress)
2. [EL-002 — Current Learning Topic](#el-002--current-learning-topic)
3. [EL-003 — Today's Mission](#el-003--todays-mission)
4. [EL-004 — Mission Completion](#el-004--mission-completion)
5. [EL-005 — Educational Evidence](#el-005--educational-evidence)
6. [EL-006 — Estimated Knowledge](#el-006--estimated-knowledge)
7. [EL-007 — Estimated Mastery](#el-007--estimated-mastery)
8. [EL-008 — Recommendations](#el-008--recommendations)
9. [EL-009 — Learning Mode](#el-009--learning-mode)
10. [EL-010 — Educational Messaging](#el-010--educational-messaging)
11. [EL-011 — Study Plan](#el-011--study-plan)
12. [EL-012 — Digital Twin Boundary](#el-012--digital-twin-boundary)
13. [Educational Decision Dependency Map](#educational-decision-dependency-map)
14. [Educational State Ownership Matrix](#educational-state-ownership-matrix)
15. [Future Educational Logic](#future-educational-logic)
16. [Cross References](#cross-references)

---

## EL-001 — Study Progress

### Educational Logic ID

EL-001

### Purpose

Answer the student question:

> **What have I completed studying?**

Study Progress records syllabus coverage — which units the student has marked or earned as studied — without asserting competence, knowledge, or mastery.

### Educational Principle

Study is not the same as understanding. Students may declare what they have studied. Study Progress must never be presented or treated as mastery (Constitution Articles II, III §5, IV.1, VIII.1, VIII.6).

### Inputs

- Student declarations that a syllabus unit has been completed studying (study-plan wizard, edit surfaces);
- Lawful session or mission completion that advances coverage for the unit that was studied;
- Active study context (curriculum / Study Plan scope) that identifies which syllabus units are in play;
- Official syllabus structure (unit identity and order).

### Outputs

- Per-unit Study Progress state: incomplete or completed studying;
- Signals that allow Learning Progress and Current Learning Topic to advance;
- Student-visible coverage narration (“Completed”, “Completed studying”, Study Progress metrics).

### Single Source of Truth

The application’s Study Progress record for the student within the relevant study context (conceptually: per-topic coverage state owned by the Study Progress / Topic Progress domain).  
Study Progress is not Twin Knowledge State and is not Estimated Mastery.

### State Owner

- **Student** owns declarations of study completion;
- **Application** owns recording, consistency, presentation, and lawful coverage advancement from completed study activity.

Students never own Estimated Mastery. The Twin never owns Study Progress declarations as verified knowledge.

### Student Visibility

Highly visible. Students see and edit Study Progress as completed / not completed studying on study-plan and related coverage surfaces. Dashboards may summarise Study Progress / Learning Progress as journey metrics.

### Dependencies

- Official syllabus structure (curriculum spine);
- Active Study Plan / study context (EL-011);
- Mission completion may update Study Progress (EL-004) when the completed work is study coverage of a unit;
- Current Learning Topic (EL-002) depends on Study Progress.

Does **not** depend on Estimated Mastery or Digital Twin belief to exist as coverage truth.

### Decision Process

1. Begin with units incomplete for the active study context.
2. Permit Study Progress to become **completed studying** when:
   - the student explicitly declares completion studying for that unit; or
   - a lawful mission/session completion advances coverage for that unit.
3. Retain Study Progress as coverage even if later evidence revises knowledge estimates.
4. Prohibited updates:
   - writing Study Progress as a synonym for Mastery, Known, or Strong Topic;
   - inventing Study Progress solely from Estimated Mastery formulae or recommendation artefacts;
   - treating Twin Knowledge State as Study Progress.
5. Relationship to Completion (EL-004 / Constitution IV.14): Completion of a *coverage* unit of work may update Study Progress. Completion of an attempt or estimate update does not, by itself, redefine Study Progress meaning.

### Educational Justification

Professional syllabuses are long. Students need an honest answer to “what have I covered?” so that learning can advance in syllabus order. Conflating coverage with mastery trains false confidence and collapses trust.

### Constraints

- Completion ≠ Mastery.
- Declaration ≠ Belief (Study Progress does not author Knowledge State).
- Study Progress checkboxes alone are not Educational Evidence of understanding (Constitution Article V §2).
- Language: “Completed studying”, never “Mastered” as a Study Progress badge.

### Future Evolution

Preserve coverage meaning if storage relocates. Future modes must not rewrite Study Progress when introducing review, revision, or adaptive interruption. Continuity of rightful Study Progress across plan changes remains constitutional and is operationalised by EIP-005 / `EDUCATIONAL_CONTINUITY_STANDARD.md`.

### Current Implementation Status

**Aligned (Intent ↔ Product direction after IA-004 / EIP-005):**

- Student study-plan surfaces ask which topics are already **completed studying**;
- Mission completion records Study Progress (`completed`) and does **not** invent mastery score from completion alone;
- Estimated Mastery display is gated separately from completion badges;
- Deleting a Study Plan preserves Study Progress (learner-owned continuity); planning metadata and week schedules are disposable.

**Documented divergence / residual risk:**

- Product still co-locates estimate fields on the same progress record as coverage flags; constitutionally they remain distinct meanings;
- Residual paths may auto-mark coverage from estimate thresholds or write felt-confidence labels onto progress rows — these behaviours conflict with full constitutional separation and must not be treated as Registry-authorised educational meaning.

### Related Constitution Articles

Article II §§1–2 (incl. §1.8); Article III §5; Article IV.1 (Study Progress), IV.2 (Learning Progress), IV.14 (Completion); Article V §2, §4; Article VII §§2–4; Article VIII rules 1, 6, 14–16; Article IX §4.

---

## EL-002 — Current Learning Topic

### Educational Logic ID

EL-002

### Purpose

Answer the student question:

> **What am I learning now?**

Provide a stable, authorised next learning focus under Learning Mode.

### Educational Principle

Learning is normally sequential. Current Learning Topic is the syllabus unit Learning Mode treats as the student’s authorised next learning focus — ordinarily the next incomplete unit in official order within the active study context (Constitution Articles II §1.1, IV.3, VI).

### Inputs

- Official syllabus order within the active curriculum / Study Plan;
- Study Progress for units in that context (EL-001);
- Active study context changes (plan switch, curriculum scope change).

### Outputs

- The Current Learning Topic (syllabus unit identity and educational title);
- Authoritative topic for Today’s Mission under Learning Mode (EL-003, EL-009);
- Student narration of sequence (“continue learning …”).

### Single Source of Truth

Canonical syllabus traversal combined with Study Progress for the active study context. No advisory recommendation, Digital Twin field, or review signal is the source of truth for Current Learning Topic in Version 1.0 Learning Mode.

### State Owner

**Application**, subordinate to official syllabus order and Study Progress.  
Students do not freely invent Current Learning Topic outside Study Progress and syllabus order. Educational Intelligence does not own Current Learning Topic under Learning Mode.

### Student Visibility

Highly visible as today’s learning focus under Learning Mode (mission and related educational surfaces).

### Dependencies

- Study Progress (EL-001);
- Study Plan / active study context (EL-011);
- Learning Mode (EL-009) as the Version 1.0 mode that privileges this topic for mission selection;
- Curriculum primacy (official syllabus).

### Decision Process

1. Within the active Study Plan’s curriculum scope, walk official syllabus order.
2. Select the first syllabus leaf (or authorised unit) whose Study Progress is not completed studying.
3. Advance Current Learning Topic when Study Progress completes the current unit.
4. Resynchronise when the active study context lawfully changes.
5. What **cannot** change Current Learning Topic under Learning Mode Version 1.0:
   - Advisory recommendations;
   - Review-due or weak-topic signals acting silently;
   - Educational Intelligence Decision artefacts without mode disclosure and Article VI authority;
   - Randomness or opportunistic optimisation.

### Educational Justification

Students need continuity. If “what I am learning now” jumps without explanation to reviewed or weak topics, the coach feels arbitrary and trust collapses.

### Constraints

- Learning Mode Mission topic must track Current Learning Topic (EL-003, EL-009).
- Advisory systems must not silently replace Current Learning Topic.
- Adaptive interruption of this selection is deferred (Article VI §3).

### Future Evolution

Revision Mode, Diagnostic Mode, and Adaptive Mode may lawfully redirect primary focus only when activated, disclosed, and constitutionally authorised. Until then, Current Learning Topic remains Learning Mode’s sole mission topic authority input.

### Current Implementation Status

**Aligned (IA-004 Learning Mode):**

- Today’s Mission topic selection follows the next incomplete syllabus unit within the active Study Plan;
- Review and weak-topic preemption are deferred from mission topic authority.

**Documented divergence / residual risk:**

- Advisory dashboard surfaces may still *name* a different topic while the mission follows Current Learning Topic — educationally confusing if not labelled as non-mission advice (see EL-008);
- Historical pre–IA-004 selection cascaded review → weak → next incomplete; that cascade is **not** authorised Learning Mode behaviour and must not return without Constitution / Registry amendment.

### Related Constitution Articles

Article II §1.1, §2; Article IV.3; Article VI §§1–3; Article VIII rule 13.

---

## EL-003 — Today's Mission

### Educational Logic ID

EL-003

### Purpose

Provide the student’s authorised daily (or session) educational commitment — one concrete focus and set of tasks for study now — that reduces daily decision burden and reinforces learning along the authorised path.

### Educational Principle

Reduce decisions. Increase learning. Missions translate educational state into actionable study work. They are not an arbitrary task queue, and must not silently commandeer Learning Mode (Constitution Articles I, IV.4, VI).

### Inputs

- Under Learning Mode Version 1.0: Current Learning Topic (EL-002) and active Study Plan context (EL-011);
- Learning Mode as active primary mode (EL-009);
- Student actions to start, complete, abandon, or supersede a mission under explicit product rules.

### Outputs

- Today’s Mission (or equivalent plain language: today’s focus / today’s session);
- Mission lifecycle state (generated, in progress, completed, abandoned, superseded);
- Opportunity for Mission Completion to update Study Progress (EL-004) and later Educational Evidence (EL-005).

### Single Source of Truth

The application’s persisted mission for the student and active Study Plan for the study day/session under Learning Mode.  
Mission topic authority under Version 1.0 is Learning Mode → Current Learning Topic, not advisory recommendations.

### State Owner

**Application** for the product learning path.  
Educational Intelligence may propose mission artefacts only under constitutional Decision Hierarchy authority (not Version 1.0 silent override).

### Student Visibility

Primary daily surface. Students experience Today’s Mission as the main study commitment.

### Dependencies

- Learning Mode (EL-009);
- Current Learning Topic (EL-002);
- Study Plan binding (EL-011; plan-scoped integrity);
- Educational Messaging (EL-010) for honest why-copy;
- Recommendations (EL-008) may advise but must not redefine the mission topic silently.

### Decision Process

**Why it exists**

- Convert syllabus continuity into one daily commitment;
- Reduce topic choice burden;
- Honour Learning Mode rather than optimisation theatre.

**Selection (Version 1.0 Learning Mode)**

1. Resolve active Study Plan.
2. Resolve Current Learning Topic from Study Progress + syllabus order.
3. Generate or retrieve the plan-bound mission for today focusing on that topic.
4. Present mission title and tasks from the mission itself (single display authority).

**Lifecycle**

1. Generated for a study day or session;
2. Started by the student;
3. Completed, abandoned, or superseded under explicit rules;
4. Completion may update Study Progress for covered units (EL-004);
5. Completion creates opportunity for reflection / performance observation (EL-005) — it does not imply mastery.

**Relationship to Learning Mode**

While Learning Mode governs: Mission always follows Learning Mode. Review suggestions remain advisory.

### Educational Justification

Scarce daily study time must be spent on the authorised next learning step. Missions exist so students do not renegotiate the entire syllabus every morning.

### Constraints

- Must not be a covert mastery exam without disclosure;
- Must not present advisory weak/review topics as Today’s Mission under Learning Mode;
- Must remain bound to the active Study Plan so plan switches do not resurrect foreign missions;
- Calls to action must not imply acceptance of a contradictory topic as the learning mission.

### Future Evolution

Revision Mode / Adaptive Mode may lawfully own mission focus when activated and disclosed. Domain Mission Intelligence may become product authority only when subordinated to Article VI and this Registry.

### Current Implementation Status

**Aligned (IA-001 + IA-004):**

- Product missions are plan-scoped;
- Learning Mode selects Current Learning Topic for today’s mission;
- Mission surfaces explain Learning Mode / Study Progress vs Estimated Mastery.

**Documented divergence / residual risk:**

- Educational Intelligence Mission path exists but is not the live student mission authority under Internal Alpha flags; dual stacks remain;
- Competing “mission-shaped” advisory widgets can dilute clarity if not labelled as non–Learning Mode advice.

### Related Constitution Articles

Article I; Article IV.4; Article VI §§1–2, §4; Article VII §2; Article VIII rules 8, 9, 13.

---

## EL-004 — Mission Completion

### Educational Logic ID

EL-004

### Purpose

Close a bounded daily study commitment honestly: honour finished work, update only the educational states that completion lawfully supports, and never over-claim mastery from finishing a mission.

### Educational Principle

Completion ≠ Mastery. Attempt ≠ Success. Completing a mission answers that the commitment was finished and may advance Study Progress — it does not prove understanding (Constitution Articles IV.14, VIII.1–2).

### Inputs

- Student confirmation that the mission (or defined session) is complete;
- Mission identity and its focal syllabus unit(s);
- Active Study Progress row for those units;
- Optional post-mission reflection or attempt outcomes (separate from the mere completion flag).

### Outputs

**What changes (lawfully):**

- Mission lifecycle → completed;
- Study Progress for covered unit(s) may become completed studying when the mission was coverage work for that unit (EL-001);
- Opportunity to record Educational Evidence observations from the session (EL-005), if gathered;
- UX closure, flash, and planning continuity (next Current Learning Topic may advance after Study Progress updates).

**What does NOT change:**

- Estimated Mastery solely because the mission was completed;
- Knowledge State / Twin belief solely because the mission was completed;
- Validation that the student “knows” or has “mastered” the topic;
- Learning Mode authority (completion does not hand mission authority to Adaptive Mode).

**Explicit constitutional statement:**

> **Mission completion does not imply mastery.**

### Single Source of Truth

Completion of the mission object is owned by Application records. Downstream estimates remain owned by Twin / authorised estimation paths and may update only from Educational Evidence — not from the completion checkbox alone.

### State Owner

Student initiates or confirms completion where required; Application records mission closure and permitted Study Progress updates.

### Student Visibility

Visible as mission / session finished and, when applicable, topic marked completed studying. Must never display “Mastered” as a synonym for mission completion.

### Dependencies

- Today’s Mission (EL-003);
- Study Progress (EL-001);
- Educational Evidence (EL-005) for optional post-completion observations;
- Estimated Mastery (EL-007) must **not** treat this event alone as warrant for high mastery language.

### Decision Process

1. Student completes mission.
2. Application closes the mission unit of work.
3. If the mission was study coverage of the Current Learning Topic (or named unit), update Study Progress only.
4. Optionally gather reflective / performance observations as Educational Evidence.
5. Do not floor, invent, or certify Estimated Mastery from completion alone.
6. Advance Current Learning Topic only via Study Progress rules (EL-002), not via mastery stage names.

### Educational Justification

Students must trust that finishing today’s work means progress in the journey — not a fake certificate of competence. Honesty about completion protects long-horizon exam preparation.

### Constraints

- Forbidden: equating Completion with Mastery, Known, or Strong Topic;
- Forbidden: using mission completion alone as Rank-A epistemic warrant;
- Preferred language: Completed / Completed studying / session finished.

### Future Evolution

Richer end-of-session Evidence contracts may attach observations more consistently. Mastery estimation may deepen without ever letting completion become mastery by fiat.

### Current Implementation Status

**Aligned (IA-004):**

- Mission completion updates Study Progress completion and does not invent mastery score from completion alone;
- Student messaging states that Estimated Mastery grows from study evidence over time.

**Documented divergence / residual risk:**

- Progress rows may still receive felt-confidence labels at completion that can be misread as understanding;
- Separate attempt-based estimate paths may still rise aggressively from sparse evidence (see EL-007);
- These residuals do not amend the Registry rule: completion ≠ mastery.

### Related Constitution Articles

Article III §§2–5; Article IV.1, IV.4, IV.14; Article V §4 (mission score / completion distinctions); Article VII §§2–4; Article VIII rules 1, 2, 10–12.

---

## EL-005 — Educational Evidence

### Educational Logic ID

EL-005

### Purpose

Define the only lawful observational basis from which knowledge-oriented beliefs and estimates may evolve. Educational Evidence records what happened educationally — not what to do next.

### Educational Principle

Objective Educational Evidence precedes educational inference. Inference may interpret evidence; inference may not invent evidence. Evidence accumulates over time (Constitution Articles III, V, VIII.10–11).

### Inputs

Observations arising from lawful study activity or assessment, attributable to a student and educational context (topic, curriculum, session, or equivalent).

### Outputs

Durable observational history that may inform:

- Knowledge State / Estimated Knowledge (EL-006);
- Estimated Mastery (EL-007);
- Readiness judgements (future specialised logic);
- Explainable recommendation factors (EL-008) — as inputs to advice, never as advice itself.

Evidence itself does not schedule missions or declare mastery as a checkbox.

### Single Source of Truth

The Educational Evidence domain / educational memory authority (conceptual). Application may record; intelligence may consume. Evidence must not be silently rewritten to fit a desired conclusion.

### State Owner

Educational Evidence domain (conceptual). Student performs activities that yield observations; Application records; Twin / estimation paths interpret.

### Student Visibility

Students experience practice results, study checks, reflection, and closure in plain language. They need not see the term “evidence”. Internal domains may retain the constitutional term Educational Evidence.

### Dependencies

- Attempt and completion events (missions, quizzes, assessments);
- Does not depend on Recommendations or Decisions (those are not evidence — Article V §2; VIII.7);
- Twin boundary (EL-012) consumes evidence interpretation, not student UI cargo.

### Decision Process

**Evidence types (current constitutional catalogue)**

| Type | Role |
|------|------|
| Official assessment outcomes | High-stakes objective performance |
| Mission scores / assessed mission outcomes | Structured objective practice |
| Quizzes | Structured objective practice |
| Mock examinations | High / structured performance |
| Past papers | Structured objective practice |
| Self-reflection | Reflective / subjective signal |
| Confidence ratings | Soft / calibrated subjective signal |
| Time spent | Exposure / engagement — weak alone |
| Reading completion | Exposure — coverage sometimes, knowledge never alone |
| Student self-report of study | Study Progress declaration when that is its meaning — not validated knowledge |

**Quality hierarchy (epistemic weight for knowledge/mastery claims)**

| Rank | Class | Typical weight |
|------|--------|----------------|
| A | High-stakes objective performance | Highest |
| B | Structured objective practice | High |
| C | Guided performance with partial objectivity | Medium |
| D | Reflective and subjective signals | Low for strong claims |
| E | Exposure and engagement signals | Lowest; never sole basis for strong knowledge/mastery claims |

**Who produces evidence**

- Students produce performance and declarations through study and assessment;
- Application observes and retains;
- Systems may structure scores — they do not invent educational observations by renaming recommendations as evidence.

**What evidence may influence**

- Knowledge State, Estimated Knowledge, Estimated Mastery (with quality ranking respected);
- Readiness factors cautiously;
- Soft calibration inputs when weighted carefully.

**What evidence may never influence (or never alone)**

- Mere navigation / clicks without educational outcome → not Educational Evidence;
- Recommendations, Decisions, mission artefacts → not Educational Evidence of knowledge;
- Study Progress checkbox alone → not understanding;
- Time spent alone → not mastery;
- Self-report alone → not validated mastery;
- Engineering metadata, warrant theatre labels, entity identifiers → not Educational Evidence for student knowledge claims.

### Educational Justification

Without ranked observational memory, the platform would either claim certainty from coverage or invent mastery from coaching rhetoric. Evidence is the honesty backbone of Estimated Knowledge and Estimated Mastery.

### Constraints

- Accumulation rule: one favourable observation does not constitutionalise lasting mastery;
- Lower ranks alone must not manufacture high certainty;
- Student language prefers “practice results”, “study checks”, “how you did” over “evidence” jargon.

### Future Evolution

Immutable Educational Evidence Contract and Twin mapping architectures may strengthen consistency of observation handoff. Evidence types may be refined by subordinate architecture without inventing new constitutional meaning here. Algorithms remain out of this Registry.

### Current Implementation Status

**Aligned direction:**

- Constitution and specialised Evidence architectures define observation vs conclusion separation;
- Product separates mission completion from mastery estimate inventiveness;
- Internal Alpha messaging discourages engineering “evidence_creating” leakage.

**Documented divergence / residual risk:**

- Full immutable Evidence → Twin succession may be architecturally specified ahead of Universal product enforcement;
- Presentation-facing estimate stores (attempt averages) may act as interim knowledge proxies while Twin Progress surfaces remain gated;
- Residual student copy may still say “study evidence” where plainer language is preferred;
- These gaps do not authorise treating recommendations or completion checkboxes as Educational Evidence of mastery.

### Related Constitution Articles

Article III; Article IV.5, IV.13; Article V (entire); Article VII §3; Article VIII rules 4–7, 10–12.

---

## EL-006 — Estimated Knowledge

### Educational Logic ID

EL-006

### Purpose

Communicate a provisional estimate of current understanding for a syllabus unit or domain — answering “How well do I currently understand this?” without claiming certified knowledge.

### Educational Principle

Estimates must be identified as estimates. Knowledge State is Twin-owned understanding posture derived from Educational Evidence — never from Study Progress alone (Constitution Articles III §4, IV.6–7, VIII.12, VIII.14).

### Inputs

- Knowledge State successive from Educational Evidence (EL-005);
- Authorised estimation paths that preserve the same educational meaning while Twin surfaces mature.

### Outputs

- Estimated Knowledge (student-facing or intermediate), always marked as estimated when material;
- Inputs to coaching, analytics honesty, and readiness factors;
- Never a verified “Known” certificate.

### Single Source of Truth

Digital Twin Knowledge State (and authorised estimation services that serve the same meaning). Application owns presentation mapping only.

### State Owner

Digital Twin / authorised estimation services; Application for presentation. Students never edit Estimated Knowledge as verified truth.

### Student Visibility

Visible when material, **always as an estimate**. Twin mechanics remain invisible (EL-012). Preferred markers: *Estimated Knowledge*, provisional understanding language.

### Dependencies

- Educational Evidence (EL-005);
- Knowledge State / Twin boundary (EL-012);
- Distinct from Study Progress (EL-001) and Learning Progress.

**Relationship to Twin**

Estimated Knowledge is the student-lawful expression of Twin understanding posture. Students experience the estimate (or coaching derived from it), not Twin schemas, succession language, or research infrastructure names.

### Decision Process

1. Require Educational Evidence interpretation — Study Progress alone is insufficient.
2. Present only with estimate framing when shown.
3. Allow estimates to refine or regress as evidence accumulates.
4. Prefer understatement under cold start, thin history, or conflicting signals.
5. Forbid presentation as verified “known”.

### Educational Justification

Students benefit from provisional understanding signals for long-horizon preparation, but only if language preserves doubt where warrant is thin. False certainty is educationally worse than honest provisionality.

### Constraints

- Forbidden: “Known” as fact without strong objective warrant;
- Forbidden: conflating Study Plan coverage with Estimated Knowledge;
- Limitations: thin evidence ⇒ understate or hide strong language rather than invent confidence.

### Future Evolution

As Twin Progress activates for students, Estimated Knowledge may become more consistently Twin-sourced. Registry will require amendment only if meaning — not storage — changes.

### Current Implementation Status

**Partial product surface:**

- Constitutional concept is clear; student UX historically emphasises **Estimated Mastery** labels more than a separate Estimated Knowledge ribbon;
- Dual stores may exist (product estimate fields vs Twin knowledge domains) with Internal Alpha Progress flags gating Twin-facing student depth;
- Messaging must still use estimate honesty wherever understanding is claimed.

**Documented divergence:**

- Where product shows coverage-derived averages under “progress” wording that sounds like understanding, that conflicts with EL-006 / EL-001 separation and is recorded as residual blur, not as authorised meaning.

### Related Constitution Articles

Article III §§3–5; Article IV.6–7; Article VII §§2–4; Article VIII rules 11–12, 14.

---

## EL-007 — Estimated Mastery

### Educational Logic ID

EL-007

### Purpose

Support long-horizon preparation judgement with a provisional estimate of how confidently the student has mastered a syllabus unit — without allowing checkbox mastery or completion-as-mastery.

### Educational Principle

Mastery is estimated, never self-certified as fact. Only accumulated Educational Evidence may raise mastery confidence. Estimates remain estimates until warrant justifies stronger speech (Constitution Articles II §1.3, III, IV.8, VIII).

### Inputs

- Accumulated Educational Evidence of sufficient quality (EL-005), especially objective practice and assessment;
- Knowledge-oriented estimation under Twin / authorised services;
- Explicit **minimum evidence**: Estimated Mastery should be absent until sufficient attempt or assessment evidence exists — completion alone is never enough.

### Outputs

- Estimated Mastery when an estimate exists;
- Honest absence of Estimated Mastery when evidence is insufficient;
- Inputs to review suggestions and future adaptive explanations — never student-editable mastery facts.

### Single Source of Truth

Digital Twin / authorised estimation services. Students never own edit rights to declare mastery as fact.

### State Owner

Digital Twin / authorised estimation services. Application maps to student language. Study Progress owners must not write mastery as coverage side-effect.

### Student Visibility

Visible **only when estimate exists**; labelled Estimated Mastery (or equivalent honest language).  
**When estimates must be hidden:** no attempt/assessment warrant; cold start; thin or conflicting signals where certainty cannot be justified; any surface that would otherwise imply mastery from Study Progress alone.

### Dependencies

- Educational Evidence (EL-005);
- Estimated Knowledge / Knowledge State (EL-006);
- Twin boundary (EL-012);
- Must not be authored by Mission Completion alone (EL-004) or Study Progress alone (EL-001).

### Decision Process

1. Require minimum objective attempt/assessment evidence before showing Estimated Mastery.
2. Update only through evidence-derived estimation — rise and fall with evidence density and outcomes.
3. Prefer Estimated Mastery language over “Mastered” badges.
4. Why estimates exist: exam preparation needs provisional competence signals without pretending certainty.
5. Forbid: student checkbox “Mastered”; treating mission completion as mastery; self-report alone as validated mastery.

### Educational Justification

High-stakes professional exams punish false confidence. Estimated Mastery exists to guide review and readiness without converting honesty of coverage into a counterfeit certificate.

### Constraints

- High stages require accumulation, not theatre;
- Self-report may be soft input only — never sole path to “Mastered”;
- Recommendations are not mastery evidence (VIII.7).

### Future Evolution

Evidence-density thresholds, spacing, and Twin-native mastery posture may strengthen honesty. Adaptive / Revision modes may consume Estimated Mastery for explained interruption — never silently in Version 1.0 Learning Mode.

### Current Implementation Status

**Aligned:**

- Students cannot tick Mastery on study-plan coverage checklists;
- Estimated Mastery UI gated on attempt-derived estimate presence;
- Mission completion does not invent mastery score from completion alone.

**Documented divergence / residual risk (explicit):**

- Student confidence instruments may still use internal values named like mastery / “Very Confident”, weighted into estimate computation — this tensions with “self-report alone must not drive validated mastery”;
- Sparse attempt history may still yield high estimate stages — below constitutional accumulation ideal;
- Product estimate store coexists with Twin belief paths; Twin Progress may be gated for students while product estimates display.

These residuals are **not** Registry amendments; they are compliance gaps for Architecture Review and subsequent capabilities.

### Related Constitution Articles

Article II §1.3, §1.6–7; Article III; Article IV.8, IV.10; Article V §§3–5; Article VII §§2–4; Article VIII rules 1, 3, 6, 10–12.

---

## EL-008 — Recommendations

### Educational Logic ID

EL-008

### Purpose

Advise the student on useful next educational actions in plain, explainable language — reducing decision burden without silently commandeering the authorised learning journey.

### Educational Principle

Intelligence advises; it does not silently override. Guidance must be explainable: what to do, why, and what happens next (Constitution Articles II §1.4, §1.9; VI §4; VII).

### Inputs

- Educational state: Study Progress, Learning Progress, Current Learning Topic, plan/time context;
- Educational Evidence–informed estimates when available (EL-005–EL-007);
- Readiness posture when available (future specialised logic);
- Learning Mode authority for what may *not* be rewritten.

### Outputs

- Advisory recommendations (suggested / recommended actions);
- Explanations in educational language (EL-010);
- Optional review or practice suggestions labelled honestly when not today’s learning mission.

Recommendations are **not** Educational Evidence (Article V §2; VIII.7).

### Single Source of Truth

Advisory surfaces project recommendations; mission persistence remains Learning Mode authority under Version 1.0 (EL-003, EL-009). Divergence, if shown, must be labelled (e.g. optional review — not today’s learning).

### State Owner

Educational Intelligence / authorised recommendation services for advisory artefacts; Application for presentation. Students may later accept/dismiss (coaching consent) without mutating mastery.

### Student Visibility

Visible as Suggested / Recommended guidance. Must not impersonate Today’s Mission when naming a different topic.

### Dependencies

- Educational Evidence and estimates inform quality of advice;
- Learning Mode / Today’s Mission define the non-advisory commitment;
- Educational Messaging governs wording;
- Relationship to missions: recommendations may point toward starting today’s session or suggest optional alternatives — they must not silently mutate Learning Mode mission topic.

### Decision Process

1. Form advice from lawful educational inputs.
2. Explain in plain language (what / why / next).
3. Keep advisory role: do not rewrite Current Learning Topic or Today’s Mission under Learning Mode without Article VI activation.
4. Treat recommendation artefacts as judgements/actions — never as observations of student knowledge.
5. Prefer truthful continuity over opaque optimisation when advice and Learning Mode diverge.

### Educational Justification

Students need coaching, not a dictator. Recommendations exist to surface useful options (including future review) while Learning Mode preserves sequential trust.

### Constraints

- Forbidden: silent override of Learning Mode mission topic;
- Forbidden: student-facing engineering vocabulary (entity ids, intent enums, Twin names);
- Forbidden: presenting recommendation text as proof of mastery or evidence.

### Future Evolution

Accept/dismiss/defer product loops; explained adaptive interruption; Founder Intelligence integration as operator insight — without converting recommendations into evidence or silent mission law.

### Current Implementation Status

**Aligned:**

- EI recommendation projection is presentation-only under Internal Alpha mission flags (does not rewrite ORM Learning Mode mission topic);
- IA-003 remapped student recommendation copy away from engineering leakage.

**Documented divergence / residual risk:**

- Dual advisory paths (EI card vs legacy lists / mission-shaped widgets) may still *name* topics other than Current Learning Topic without always labelling “optional review (not today’s learning)”;
- Deep explainability and warrant honesty may be suppressed; Why copy may be family-generic;
- Accept/dismiss coaching consent may be incomplete in product HTTP flows.

### Related Constitution Articles

Article II §1.4, §1.9; Article V §2; Article VI §4; Article VII; Article VIII rules 7–9, 13, 15.

---

## EL-009 — Learning Mode

### Educational Logic ID

EL-009

### Purpose

Define Version 1.0’s default educational operating mode: the student’s primary daily commitment follows Current Learning Topic in official syllabus order within the active study context.

### Educational Principle

Learning is normally sequential. Learning Mode is the Version 1.0 authority for Today’s Mission topic selection. Adaptive interruption is deferred (Constitution Article VI).

### Inputs

- Active Study Plan and curriculum (EL-011);
- Study Progress (EL-001);
- Official syllabus order;
- Mode activation state (Learning Mode active vs future modes).

### Outputs

- Mission topic authority → Current Learning Topic (EL-002, EL-003);
- Student-visible Learning Mode behaviour and why-copy;
- Explicit non-authority of review/weak signals over mission topic while Learning Mode governs.

### Single Source of Truth

Decision Hierarchy Article VI: Learning Mode is the Version 1.0 primary mode for mission topic selection. No feature flag may silently rename Adaptive behaviour as Learning Mode (Article IX §3).

### State Owner

Application mode authority (product learning path). Educational Intelligence advises within mode rules; it does not silently replace Learning Mode in Version 1.0.

### Student Visibility

Students experience Learning Mode as “today’s mission follows your Current Learning Topic” and sequential Continue Learning — not as an engineering mode switch panel (unless future UX explicitly offers disclosed mode choice).

### Dependencies

- Study Plan (EL-011);
- Study Progress (EL-001);
- Current Learning Topic (EL-002);
- Today’s Mission (EL-003);
- Recommendations remain advisory (EL-008);
- Future Revision Mode is related but distinct and deferred for primary mission authority.

### Decision Process

**Version 1.0 behaviour**

1. Learning Mode is active by default for mission topic selection.
2. Mission always follows Learning Mode while it is the active primary mode.
3. Review and weak-topic signals may appear as recommendations only.
4. Adaptive / Revision interruption must not silently steal mission authority.

**Relationship to Study Plan**

Learning Mode operates within the active Study Plan’s syllabus scope and schedule context.

**Relationship to Mission**

Today’s Mission topic = Current Learning Topic under Learning Mode.

**Relationship to future Revision Mode**

Revision Mode consolidates previously studied material when activated and disclosed. It is not silent Learning Mode substitution. Until activated under Constitution / Registry amendment, Revision Mode does not own Version 1.0 mission topic selection.

### Educational Justification

Sequential syllabuses underpin professional exam preparation. Version 1.0 must earn trust through continuity before optimisation is allowed to interrupt.

### Constraints

- No silent Adaptive Mode as if already primary authority;
- Advisory divergence must be labelled honestly;
- Mode changes that alter Article VI require constitutional amendment before implementation meaning shifts.

### Future Evolution

Revision Mode, Diagnostic Mode, Adaptive Mode placeholders (see Future Educational Logic). Phase gating and student-visible explanation are prerequisites for interruption authority.

### Current Implementation Status

**Aligned (IA-004):**

- Product mission generation uses Learning Mode (next incomplete unit);
- Copy explains Learning Mode vs Estimated Mastery.

**Residual:**

- Advisory dual-display can still feel like mode conflict if poorly labelled — integrity of *persistence* is Learning Mode; integrity of *narration* remains a trust risk.

### Related Constitution Articles

Article II §1.1, §1.9; Article IV.3–4; Article VI (entire); Article VIII rule 13; Article IX §3; Article X §1.3, §1.6.

---

## EL-010 — Educational Messaging

### Educational Logic ID

EL-010

### Purpose

Govern how educational language is chosen on student-facing surfaces so that speech remains plain, truthful, actionable, and free of engineering theatre.

### Educational Principle

Student-facing language is educational speech. It must answer what / why / next where relevant. Estimates must be named as estimates. Twin and pipeline jargon must not appear (Constitution Articles III §4, VII, VIII.11–12, VIII.15).

### Inputs

- Educational concept being communicated (Study Progress, Mission, Recommendation, Estimate, …);
- Warrant honesty posture (when known internally);
- Presentation mapping from internal domain vocabulary to student vocabulary.

### Outputs

- Student-visible titles, subtitles, reasons, badges, empty states, settings labels;
- Honest estimate wording and recommended advisory wording;
- Suppression or remapping of forbidden wording.

### Single Source of Truth

Constitution Article VII for permitted and forbidden families; this Registry for operational application to product messages. Domain may retain precise internal vocabulary; Presentation must map before render.

### State Owner

Application / presentation layer for student speech; domain for internal terms. Educational specialists and Architecture review govern vocabulary discipline.

### Student Visibility

All student-facing surfaces are within this logic’s scope. Operator-only surfaces may use more precise terms if not student-exposed.

### Dependencies

- Every student-visible educational logic (EL-001–EL-009, EL-011–EL-012);
- Recommendations (EL-008) especially sensitive to leakage;
- Twin Boundary (EL-012) for invisibility in speech.

### Decision Process

**How language is chosen**

1. Identify the educational concept (coverage vs estimate vs advice vs mission).
2. Select permitted family language from the Constitution.
3. Map internal enums/ids/warrant tags to plain educational phrases.
4. Prefer understatement when warrant is thin.

**Truthfulness requirements**

- Assert only what educational states and evidence support;
- Name estimates as estimates;
- Do not convert Study Progress into mastery rhetoric;
- Do not dump entity identifiers or ActionIntent-like enums.

**Estimate wording (required style)**

- Estimated Knowledge / Estimated Mastery / Suggested / Recommended / provisional phrases.

**Recommended wording (preferred families)**

| Concept | Prefer |
|---------|--------|
| Coverage | Completed studying, Study Progress, Learning Progress |
| Daily commitment | Today’s Mission / today’s focus |
| Advice | Suggested, Recommended, optional review (not today’s learning) |
| Checks | Practice, study check, short check |
| Continuity | Continue Learning |

**Forbidden wording (student-facing)**

- Engineering / intelligence jargon: evidence_creating, pipeline, warrant tags, cold_start, thin_warrant, entity identifiers, Digital Twin (named as such), mission generation as engineering, classification enums;
- False attainment from coverage: Mastered, Fully Learned, Finished Learning Forever as Study Progress labels;
- Unsupported factual strength: Known, Strong Topic, Weak Topic as bare fact under thin/no objective evidence;
- Composite/system theatre without educational meaning.

### Educational Justification

Week-one Internal Alpha trust collapse demonstrated that engineering language and false attainment labels destroy the coach relationship. Messaging is educational integrity made audible.

### Constraints

- Internal domains may keep precise terms; students must not see them unmapped;
- Feature flags must not circumvent vocabulary rules by renaming.

### Future Evolution

Deeper explainability may introduce richer student-safe reasons — still without warrant tags or Twin names. Amendment required before relaxing forbidden attainment language.

### Current Implementation Status

**Aligned (IA-003):**

- Recommendation cards remapped to educational family titles/subtitles/reasons;
- Settings use Learning profile status rather than Digital Twin naming;
- Regression tests guard forbidden vocabulary on key surfaces.

**Documented divergence / residual risk:**

- Residual phrases such as “study evidence” may remain where “practice results” is preferred;
- Some legacy readiness/recommendation copy may still assert strong outcomes without estimate markers;
- Estimate honesty is uneven outside mastery labels.

### Related Constitution Articles

Article III §§3–5; Article VII (entire); Article VIII rules 11–12, 15; Article IX §3.

---

## EL-011 — Study Plan

### Educational Logic ID

EL-011

### Purpose

Provide the student’s authorised study context — which curriculum/examination track is active, what schedule and scope bound daily learning — so that syllabus order, Study Progress, and Learning Mode have a coherent home.

### Educational Principle

Curriculum primacy: official syllabus structure is the educational spine. The Study Plan situates that spine in the student’s preparation journey. Study Plan coverage must never be mixed with Digital Twin understanding (Constitution Articles II §2, IV, VIII.14).

### Inputs

- Student choices: create/edit plan, select curriculum, mark initial Study Progress, set schedule/preferences;
- Official syllabus imported through curriculum services;
- Active plan selection.

### Outputs

- Active Study Plan context for mission generation, progress narration, and learning sequence;
- Scope for Current Learning Topic and Study Progress;
- Plan-bound mission integrity.

### Single Source of Truth

The Application’s Study Plan for the student (active plan selection + associated progress scope). Twin Knowledge State is not the Study Plan.

### State Owner

Student owns plan creation, editing intent, and Study Progress declarations within the plan. Application owns persistence, active-plan resolution, and consistency with curriculum.

### Student Visibility

Highly visible: plan creation wizard, plan view/edit, active plan in settings, roadmap of completed studying vs later estimates.

### Dependencies

- Curriculum / syllabus;
- Study Progress (EL-001);
- Current Learning Topic and Learning Mode (EL-002, EL-009);
- Today’s Mission plan binding (EL-003).

**Relationship to Current Learning**

Current Learning Topic is derived inside the active Study Plan’s syllabus scope from Study Progress.

**Relationship to Study Progress**

Study Progress is a learner educational history asset scoped to syllabus units. Completing studying within an active Study Plan advances Learning Mode. The Study Plan does not ontologically own Study Progress for deletion purposes (EIP-005).

**What Study Plan never represents**

- Estimated Mastery or certified knowledge;
- Digital Twin belief;
- Educational Evidence itself;
- A permission to declare Mastered by covering topics;
- Readiness proof by schedule alone;
- Ownership of educational history that may be wiped when the plan row is deleted.

### Decision Process

1. Student establishes or activates a Study Plan for a curriculum.
2. Initial Study Progress declarations may seed coverage without seeding mastery as fact.
3. Learning Mode uses the active plan’s incomplete syllabus units for Current Learning Topic.
4. Missions bind to the active plan so foreign plans cannot masquerade as today.
5. Changing active plan resynchronises mission and learning focus lawfully — without inventing educational discontinuity.
6. Deleting a Study Plan disposes planning artefacts only; Study Progress and related educational history remain with the learner.

### Educational Justification

Without a Study Plan as study context, daily missions and progress narration cannot stay syllabus-accountable. The plan is the student’s authorised preparation frame — not an understanding model and not the delete-owner of rightful coverage memory.

### Constraints

- Do not mix Study Plan metrics with Twin understanding narration;
- Do not destroy rightful Study Progress on ordinary plan delete/archive (EIP-005);
- Advisory lists should remain scoped to active plan curriculum where integrity requires it.

### Future Evolution

Richer phase planning (revision season) may interact with Revision Mode. Continuity rules are strengthened under `EDUCATIONAL_CONTINUITY_STANDARD.md` for multi-plan and archive semantics.

### Current Implementation Status

**Aligned (IA-001 / IA-004 / EIP-005):**

- Missions store study plan binding;
- Wizard/edit use completed-studying language;
- Learning Mode scoped to active plan curriculum;
- Plan delete preserves Study Progress, Attempts, Evidence posture, and Twin estimates; week plans and mission plan pointers are cleared.

**Documented divergence / residual risk:**

- Some advisory lists may remain user-global rather than active-plan scoped;
- Progress storage may still carry estimate fields beside coverage flags (meaning separation mandatory regardless of column co-location);
- Curriculum remapping across editions uses objective topic codes only — unmapped units remain historical without inventing equivalence.

### Related Constitution Articles

Article II §1.8, §2; Article IV.1–4; Article VI §1; Article VIII rules 14–16; Article IX §4.

---

## EL-012 — Digital Twin Boundary

### Educational Logic ID

EL-012

### Purpose

Define what belongs inside the Digital Twin, what must never leak into student UI, and how students experience Twin-powered understanding as guidance and estimates — not implementation theatre.

### Educational Principle

Internal systems remain invisible. Twin holds understanding posture; Study Plan holds coverage journey. Students experience guidance, not Twin schemas (Constitution Articles II §1.10, IV.6–8, VII §5, VIII.14).

### Inputs

- Educational Evidence interpretations (EL-005);
- Authorised Twin update / succession pathways (architecture subordinates — not specified here as algorithms).

### Outputs

- Knowledge State and related estimates feeding Estimated Knowledge / Estimated Mastery presentation (EL-006, EL-007);
- Internal warrant/confidence for intelligence — not student engineering displays;
- Optional operator presence signals remapped to “Learning profile status” language when shown.

### Single Source of Truth

Digital Twin for understanding meaning. Study Progress / Study Plan remain separate sources for coverage. Presentation must not invent Twin contents as Study Plan metrics.

### State Owner

Digital Twin (and authorised estimation paths serving the same meaning). Students never edit Twin belief as verified truth.

### Student Visibility

**Twin mechanics: invisible.**  
Students may see Estimated Knowledge / Estimated Mastery / readiness language / coaching when material. Students must not see Twin schemas, succession language, warrant tags, research infrastructure names, or “Digital Twin” labelling on ordinary student surfaces.

### Dependencies

- Educational Evidence (EL-005);
- Estimated Knowledge / Estimated Mastery (EL-006, EL-007);
- Educational Messaging for invisibility (EL-010);
- Forbidden coupling to Study Progress ownership (EL-001) and Study Plan meaning (EL-011).

### Decision Process

**What belongs inside**

- Knowledge State and related understanding beliefs;
- Evidence-driven succession of those beliefs;
- Educational confidence / warrant about estimates and recommendations (distinct from student-felt confidence).

**What never leaks into UI**

- Twin type names and entity graphs as educational guidance;
- Succession / pipeline / warrant posture enums as student copy;
- Raw Twin research fields;
- Mixing Twin understanding into Study Plan coverage badges.

**Student visibility rule**

Experience guidance and honest estimates; never Twin implementation.

### Educational Justification

Exposing Twin invites score gaming, confuses product with research, and undermines the coach metaphor. Invisibility protects trust and educational clarity.

### Constraints

- Article VII §5 Twin invisibility in speech;
- Article VIII.14 Study Plan vs Twin separation;
- Feature flags enabling Progress/Explainability must preserve mapping discipline.

### Future Evolution

Twin Progress and Explainability may deepen student-facing estimates and reasons without naming Twin. Adaptive modes may consume Twin estimates with disclosure. Algorithms and Twin update strategies remain outside this Registry’s scope.

### Current Implementation Status

**Aligned (EP-008 / IA-003):**

- Student templates avoid “Digital Twin” naming;
- Settings use Learning profile status presence labels when Twin presence is material for Internal Alpha;
- Twin retrieval remains behind application/orchestration providers, not student theatre.

**Documented divergence / residual risk:**

- Dual estimate stores (product mastery scores vs Twin domains) require careful presentation until Twin is the sole student-ready understanding authority;
- Enabling EI Progress/Explainability without mapping would risk leakage — currently gated, which preserves invisibility at the cost of depth.

### Related Constitution Articles

Article II §1.10; Article IV.6–8, IV.10; Article VII §5; Article VIII rule 14; Article IX §4.

---

## Educational Decision Dependency Map

Educational decisions form a lawful dependency chain. Downstream decisions must not invent upstream meaning.

```
Official Syllabus Structure
        ↓
Study Plan (EL-011) — active study context
        ↓
Study Progress (EL-001) — what has been completed studying
        ↓
Current Learning Topic (EL-002)
        ↓
Learning Mode (EL-009) — Version 1.0 mission authority
        ↓
Today's Mission (EL-003)
        ↓
Mission Completion (EL-004) ──► may update Study Progress only
        │
        └──► may yield Educational Evidence observations (EL-005)

Educational Evidence (EL-005)
        ↓
Digital Twin / Knowledge State (EL-012 boundary)
        ↓
Estimated Knowledge (EL-006)
        ↓
Estimated Mastery (EL-007)
        ↓
Educational Intelligence advisory judgement
        ↓
Recommendations (EL-008) — advice, not evidence, not silent mission law
        ↓
Student Guidance via Educational Messaging (EL-010)
```

**Parallel integrity rules on the map**

- Recommendations must not write Study Progress, Knowledge State, or Mission topic under Learning Mode.
- Mission Completion must not write Estimated Mastery.
- Estimated Mastery must not redefine Study Progress meaning.
- Educational Messaging binds every student-visible edge of the map.

**Short form (programme example)**

```
Study Progress
↓
Educational Evidence
↓
Estimated Knowledge
↓
Estimated Mastery
↓
Educational Intelligence
↓
Recommendations
↓
Student Guidance
```

Learning Mode / Mission / Study Plan run as the **journey spine** alongside the **understanding spine**. They meet in student experience but remain distinct in meaning.

---

## Educational State Ownership Matrix

| Educational Concept | Owner | Persistence | Student Editable | Evidence Required | Displayed to Student |
|---------------------|-------|-------------|------------------|-------------------|----------------------|
| Study Progress | Student (declare) + Application (record) | Persistent coverage state | Yes (declarations); mission may lawfully advance | No for coverage declaration; understanding evidence not required | Yes — completed studying |
| Learning Progress | Application (derived) | Derived / recomputed | No | No (derived from Study Progress + scope) | Yes — journey progress, non-mastery labels |
| Current Learning Topic | Application (syllabus + Study Progress) | Derived for active context | Indirectly via Study Progress / plan only | No | Yes — learning focus |
| Today's Mission | Application (Learning Mode authority) | Persistent mission records (plan-bound) | Start / complete / tasks; not free topic hijack under Learning Mode | No for selection under Learning Mode | Yes — primary daily surface |
| Mission Completion | Student confirm + Application record | Persistent closed mission | Yes (confirm closure) | No for completion flag; evidence optional afterward | Yes — finished work |
| Educational Evidence | Evidence domain (conceptual) | Persistent observational history | Student produces via activity; does not rewrite history | N/A (it *is* the evidence) | Indirect — practice results / checks, not jargon |
| Knowledge State | Digital Twin | Twin persistence | No | Yes — evidence-driven only | No as Twin; yes as estimates |
| Estimated Knowledge | Twin / authorised estimation; App presents | Derived estimate | No as verified truth | Yes | Yes when material, as estimate |
| Estimated Mastery | Twin / authorised estimation | Derived estimate | Never as fact checkbox | Yes — minimum attempt/assessment evidence | Yes only when estimate exists |
| Recommendations | EI / recommendation services; App presents | Advisory artefacts / projections | Future accept/dismiss; not mastery edits | Prefer evidence-informed; not themselves evidence | Yes — suggested / recommended |
| Learning Mode | Application mode authority | Mode policy (Version 1.0 default) | Not a casual student rewrite of constitution | N/A | Experienced via mission behaviour / copy |
| Study Plan | Student intent + Application persistence | Persistent plans | Yes (create/edit/activate) | No for plan existence | Yes |
| Digital Twin (internals) | Twin authority | Twin persistence | No | Evidence for belief succession | No — invisible; estimates/guidance only |
| Readiness *(future specialised)* | Readiness authority within EI | Derived judgement | No as fact theatre | Prefer warranted signals | Plain readiness summaries when shown |
| Student-felt Confidence | Student | Attempt/reflection records | Yes (self-report) | N/A | Collected in plain language; ≠ understanding |

**Operational authority matrix (mutation rights):** see `knowledge/educational/EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` (EIP-001). That document supersedes informal write-path ambiguity for implementation and regression protection.

---

## Future Educational Logic

The following logics are **reserved placeholders**. They are recognised constitutional trajectories but are **not** fully specified as Version 1.0 operational decisions in this Registry. No algorithms are defined here. Implementation that elevates them to primary mission authority requires Constitution Article X amendment and Registry expansion.

### FEL-001 — Revision Mode

**Reserved.** Mode oriented toward consolidating and revising previously studied material, typically as examinations approach or when the student explicitly enters revision posture. May guide primary focus only when activated and disclosed — never as silent Learning Mode substitution.

### FEL-002 — Diagnostic Mode

**Reserved.** Mode that prioritises creating clarifying Educational Evidence when knowledge warrant is thin or next-step uncertainty is high. May propose diagnostics and short checks. Must not masquerade as mastery certification or silently steal Learning Mode mission authority.

### FEL-003 — Adaptive Learning (Adaptive Mode)

**Reserved / deferred.** Explained adaptive interruption (review, weak-topic focus, spaced reinforcement) may temporarily redirect primary focus according to evidence-informed need — only with Phase gating and student-visible explanation. Not Version 1.0 mission authority.

### FEL-004 — Readiness

**Reserved for specialised operational expansion.** Explainable preparedness posture relative to exam goals, coverage, pace, and related signals. Informs Decision and advisory surfaces; must not silently become Today’s Mission without Decision Hierarchy compliance. Article IV.9 defines meaning; full operational section awaits a dedicated capability.

### FEL-005 — Founder Intelligence Integration

**Reserved.** Operator/founder educational insight overlays that consume governed educational state for product stewardship. Must not redefine student-facing educational meaning, invent mastery, or bypass Twin invisibility and messaging rules. Integration details are out of Version 1.0 Learning Mode scope.

---

## Cross References

**Supreme authority**

- `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` (EGI-001)

**Subordinate / diagnostic (do not override this Registry or the Constitution)**

- Internal Alpha: IA-001 Mission Recommendation Integrity; IA-003 Student-Centred Educational Messaging; IA-004 Truthful Learning Progress;
- `knowledge/product/EDUCATIONAL_PHILOSOPHY_AUDIT.md` (diagnostic relative to educational law);
- Educational Intelligence and Digital Twin architectures under `docs/architecture/` and Twin constitutions;
- Knowledge educational subtree folders: philosophy, policies, recommendation, digital_twin.

---

## Closing

This Registry makes educational behaviour explicit so that developers, educational specialists, and future architects share one operational map.

The Constitution defines **what** learning truth is.  
This Registry defines **how** Kwalitec currently decides educationally.

No new educational logic may appear in code before it appears here.

**End of Educational Logic Registry — Version 1.0**

# Kwalitec Educational Constitution

**Capability ID:** EGI-001  
**Programme:** Educational Governance Initiative  
**Classification:** Highest Educational Authority  
**Status:** APPROVED — governing  
**Version:** 1.0  

---

## Authority

This Constitution is the highest educational authority in the Kwalitec repository.

Every educational feature, recommendation, mission, dashboard, Educational Intelligence capability, Digital Twin capability, and future implementation must comply with this Constitution.

If a proposed implementation would contradict this Constitution, the Constitution must be amended first under Article X.

**The Constitution governs implementation.  
Implementation never governs the Constitution.**

This document is not an implementation specification, not an architecture design, and not a product requirements document. It defines educational philosophy, truth, governance, ownership, terminology, and integrity for the whole platform.

---

## PREAMBLE

Kwalitec exists so that candidates for demanding professional examinations may study with clarity, honesty, and continuity.

Professional syllabuses are long. Daily study time is scarce. Trust is fragile. Students who are told they have mastered what they have only studied, or who are steered without explanation away from their planned learning path, lose faith in the coach that was meant to serve them.

Therefore Kwalitec binds itself to educational truth before educational optimisation; to evidence before certainty; to syllabus order before opportunistic interruption; and to language that a student can understand and believe.

This Constitution records those obligations so that product, architecture, and intelligence may evolve without silently redefining what learning means.

---

## ARTICLE I — Educational Purpose

### Section 1. Why Kwalitec Exists

Kwalitec exists to help students prepare for official professional examinations by reducing daily decision burden and increasing productive learning.

Its central promise is:

> **Reduce decisions. Increase learning.**

### Section 2. What Kwalitec Is

Kwalitec is an educational coach grounded in:

1. Official syllabus structure as the primary organising truth of study;
2. Deterministic, explainable guidance from the student’s own educational state;
3. Accumulated educational evidence as the only lawful basis for claims about knowledge and mastery.

### Section 3. What Kwalitec Is Not

Kwalitec is not:

1. A generic calendar or task list divorced from syllabus meaning;
2. A black-box tutor whose suggestions cannot be traced to educational grounds;
3. A system that permits students to declare mastery by assertion alone;
4. A surface that exposes internal machinery as if it were educational guidance.

### Section 4. Beneficiaries

The primary beneficiary is the student. Educational design, messaging, and decision behaviour must serve student comprehension, trust, and learning continuity above internal convenience.

---

## ARTICLE II — Educational Philosophy

### Section 1. Beliefs Governing Learning

Kwalitec holds the following beliefs as binding:

1. **Learning is normally sequential.** Students advance through official syllabus order unless a later, constitutionally authorised mode explicitly and transparently interrupts that order.
2. **Study is not the same as understanding.** Declaring that a topic has been studied answers coverage, not competence.
3. **Mastery is estimated, never self-certified as fact.** Only accumulated educational evidence may raise confidence that a topic is mastered.
4. **Guidance must be explainable.** Every material recommendation should answer what to do, why it is suggested, and what happens next — in plain educational language.
5. **Trust precedes optimisation.** Opaque or contradictory guidance is educationally worse than simpler, truthful guidance.
6. **Evidence accumulates over time.** A single completion, attempt, or session does not prove mastery.
7. **Uncertainty must be named.** Where certainty cannot be justified by evidence, Kwalitec speaks of estimates, suggestions, and readiness judgements — not validated truth.
8. **The student’s learning journey is continuous.** Changing study context must not invent educational discontinuity or silently erase rightful progress without clear educational justification. Educational history — Study Progress, Study Attempts, Educational Evidence posture, and Twin-owned estimates — belongs to the learner. A Study Plan is a disposable planning container and must not silently destroy that history when deleted, replaced, or migrated (see `EDUCATIONAL_CONTINUITY_STANDARD.md`).
9. **Intelligence advises; it does not silently commandeer.** Educational Intelligence and related systems may advise. They must not override the student’s authorised learning path without disclosure and constitutional authority for that mode.
10. **Internal systems remain invisible.** Mechanisms such as the Digital Twin may underpin understanding; students experience guidance, not implementation theatre.

### Section 2. Curriculum Primacy

Official syllabus structure is the educational spine of the platform. Planning, missions, progress narration, and recommendations must remain accountable to that spine.

### Section 3. Determinism of Educational Cores

Core educational judgements that shape the student’s journey must be reproducible from the same educational inputs. Randomness and opaque generative substitution are forbidden in those cores.

---

## ARTICLE III — Educational Truth

### Section 1. Principle of Lawful Claim

Kwalitec may assert only what its educational states and evidence lawfully support. Presentation, analytics, coaching copy, and intelligence outputs are bound by this Article equally.

### Section 2. Objective Evidence Before Inference

1. Objective educational evidence precedes educational inference.
2. Inference may interpret evidence; inference may not invent evidence.
3. Absence of evidence is not evidence of mastery, readiness, or weakness stated as fact.

### Section 3. Certainty Requires Support

1. Kwalitec shall never communicate educational certainty that is unsupported by evidence.
2. Strong language of attainment (“mastered”, “known”, “strong”, “weak” as factual labels) is permitted only when warrant from objective evidence justifies it — and even then should prefer estimated or provisional framing where doubt remains material.
3. Cold start, thin history, and conflicting signals require honest understatement, not confident theatre.

### Section 4. Estimates Must Be Identified as Estimates

1. Educational estimates shall always be identified as estimates in student-facing communication when they represent inferred knowledge, mastery, readiness, or similar.
2. Preferred markers include *Estimated*, *Suggested*, *Recommended*, and equivalent plain language that does not pretend validated proof.
3. Internal scores may exist for computation; student language must map them to truthful educational wording.

### Section 5. Separation of Declaration and Belief

1. Students may declare what they have studied.
2. Kwalitec may estimate what they know.
3. Neither student declaration nor system convenience may convert Study Progress into Mastery by fiat.

---

## ARTICLE IV — Educational State Model

Each state below is a constitutional educational concept. Implementation may store or derive them differently over time, but must not redefine their meaning without amending this Constitution.

---

### 1. Study Progress

| Aspect | Provision |
|--------|-----------|
| **Definition** | The record of what the student has marked or earned as studied for a syllabus unit (typically a topic), answering “What have I studied?” |
| **Purpose** | Honour honest coverage of the syllabus without claiming competence. |
| **Owner** | Student for declarations of study completion; Application for recording and presenting those declarations consistently. |
| **Source** | Student study-plan actions; lawful session/mission completion that advances coverage — never mastery formulae alone disguised as coverage truth. |
| **Lifecycle** | Begins incomplete; may become completed for a unit; remains Study Progress even when later evidence revises knowledge estimates. |
| **Student Visibility** | Highly visible as completed / not completed studying. |
| **Permitted Uses** | Drive Current Learning Topic advancement; pace learning sequence; narrate coverage. Must not be presented as mastery. |

---

### 2. Learning Progress

| Aspect | Provision |
|--------|-----------|
| **Definition** | Derived measure of how far the student has advanced through the authorised syllabus learning sequence for the active study context. |
| **Purpose** | Answer “How far through the syllabus have I progressed?” as a journey metric, distinct from knowledge quality. |
| **Owner** | Application (derived). |
| **Source** | Study Progress relative to official syllabus order and scope of the active plan or curriculum context. |
| **Lifecycle** | Recalculated as Study Progress and plan context change. |
| **Student Visibility** | Visible as overall or journey progress, labelled without mastery rhetoric. |
| **Permitted Uses** | Dashboards, plan overviews, motivational continuity. Must not be labelled or treated as Estimated Mastery. |

---

### 3. Current Learning Topic

| Aspect | Provision |
|--------|-----------|
| **Definition** | The syllabus unit that Learning Mode treats as the student’s authorised next learning focus — ordinarily the next incomplete unit in official order within the active study context. |
| **Purpose** | Give the student a stable answer to “What am I learning now?” |
| **Owner** | Application, subordinate to official syllabus order and Study Progress. |
| **Source** | Canonical syllabus traversal combined with Study Progress. |
| **Lifecycle** | Advances when Study Progress completes the current unit; resets or resynchronises when active study context lawfully changes. |
| **Student Visibility** | Highly visible as today’s learning focus under Learning Mode. |
| **Permitted Uses** | Authority for Today’s Mission topic under Learning Mode; student narration of sequence. Advisory systems must not silently replace it. |

---

### 4. Mission

| Aspect | Provision |
|--------|-----------|
| **Definition** | The student’s authorised daily (or session) educational commitment — the concrete focus and tasks for study now. |
| **Purpose** | Translate educational state into one actionable study commitment that reinforces learning. |
| **Owner** | Application for the product learning path; Educational Intelligence may propose mission artefacts only under constitutional Decision Hierarchy authority. |
| **Source** | In Version 1.0 Learning Mode: Current Learning Topic and plan context. Later modes may lawfully interrupt only under Article VI. |
| **Lifecycle** | Generated for a study day or session; completed, abandoned, or superseded under explicit rules; completion may update Study Progress for covered units. |
| **Student Visibility** | Primary daily surface (“Today’s Mission” or equivalent plain language). |
| **Permitted Uses** | Direct learning action. Must not be an arbitrary task queue, nor a covert mastery exam disguised as a mission without disclosure. |

---

### 5. Educational Evidence

| Aspect | Provision |
|--------|-----------|
| **Definition** | An immutable educational observation arising from lawful study activity or assessment — a record of what happened educationally, not a prescription of what to do next. |
| **Purpose** | Supply the only lawful observational input from which knowledge-oriented beliefs and estimates may evolve. |
| **Owner** | Educational Evidence domain / educational memory authority (conceptual); Application may record; intelligence may consume. |
| **Source** | Study sessions, assessments, reflections, and related lawful observations as classified in Article V. |
| **Lifecycle** | Created upon observation; retained as history; may be interpreted repeatedly; must not be silently rewritten to fit a desired conclusion. |
| **Student Visibility** | Students should experience reflection and closure; they need not see “evidence” jargon. Underlying observations may power Estimated Knowledge and Estimated Mastery. |
| **Permitted Uses** | Evolve Knowledge State and related estimates; inform Readiness and recommendations. Must not itself schedule missions or declare mastery as a checkbox. |

---

### 6. Knowledge State

| Aspect | Provision |
|--------|-----------|
| **Definition** | The platform’s structured representation of how well the student currently understands syllabus elements — the educational understanding posture, distinct from study coverage. |
| **Purpose** | Answer “How well do I currently understand this?” at the system level of belief. |
| **Owner** | Digital Twin (and authorised estimation paths that serve the same educational meaning until Twin surfaces fully). |
| **Source** | Interpretation of Educational Evidence over time — never Study Progress alone. |
| **Lifecycle** | Born thin or empty; evolves only through lawful evidence-driven succession; never student-edited as verified truth. |
| **Student Visibility** | Twin mechanics remain invisible; understanding appears as Estimated Knowledge / Estimated Mastery / readiness language. |
| **Permitted Uses** | Inform readiness, recommendations, analytics honesty. Must never be conflated with Study Plan coverage. |

---

### 7. Estimated Knowledge

| Aspect | Provision |
|--------|-----------|
| **Definition** | A student-facing or intermediate estimate of current understanding for a unit or domain, explicitly marked as estimated. |
| **Purpose** | Communicate provisional understanding without claiming certified knowledge. |
| **Owner** | Digital Twin / authorised estimation services; Application for presentation. |
| **Source** | Knowledge State derived from Educational Evidence. |
| **Lifecycle** | Updates as evidence accumulates; may regress or refine; remains provisional until objective warrant justifies stronger language. |
| **Student Visibility** | Visible when material, always as an estimate. |
| **Permitted Uses** | Coaching, analytics, explainable factors. Forbidden: presentation as verified “known”. |

---

### 8. Estimated Mastery

| Aspect | Provision |
|--------|-----------|
| **Definition** | The platform’s estimate of how confidently the student has mastered a syllabus unit, always provisional and evidence-derived. |
| **Purpose** | Support long-horizon preparation judgement without allowing checkbox mastery. |
| **Owner** | Digital Twin / authorised estimation services. Students never own edit rights to declare mastery as fact. |
| **Source** | Accumulated Educational Evidence interpreted through lawful estimation — not completion alone, not a single self-report alone. |
| **Lifecycle** | Absent until sufficient attempt or assessment evidence exists; rises and falls with evidence density and outcomes; high stages require accumulation, not theatre. |
| **Student Visibility** | Visible only when estimate exists; labelled Estimated Mastery (or equivalent honest language). |
| **Permitted Uses** | Review suggestions, analytics, future adaptive interruption explanations. Forbidden: student checkbox “Mastered”; treating mission completion as mastery. |

---

### 9. Readiness

| Aspect | Provision |
|--------|-----------|
| **Definition** | An explainable judgement of preparedness relative to exam goals, coverage, pace, and related educational signals — a preparedness posture, not a next-action engine. |
| **Purpose** | Answer “How prepared am I becoming?” honestly. |
| **Owner** | Readiness authority within Educational Intelligence / authorised readiness services. |
| **Source** | Progress, evidence-informed estimates, plan and time context, and related factors with warrant. |
| **Lifecycle** | Continuously revised; may be not-yet-knowable under thin evidence. |
| **Student Visibility** | Visible as readiness summaries in plain language; uncertainty disclosed when warrant is thin. |
| **Permitted Uses** | Inform Decision and advisory surfaces. Must not silently become Today’s Mission without Decision Hierarchy compliance. |

---

### 10. Confidence

| Aspect | Provision |
|--------|-----------|
| **Definition** | A family of related but distinct concepts: (a) student-felt confidence (self-report); (b) educational estimate confidence / warrant about knowledge or recommendations. These must not be collapsed into one dial. |
| **Purpose** | Capture subjective feeling separately from educational warrant. |
| **Owner** | Student owns felt confidence reports; Educational Intelligence / Twin own educational confidence and warrant. |
| **Source** | Self-report instruments; evidence density and estimation quality respectively. |
| **Lifecycle** | Felt confidence may change per attempt; educational confidence grows with warrant, not with rhetoric. |
| **Student Visibility** | Felt confidence may be collected in plain language; educational confidence appears as estimated or warrant-honest language — never engineering jargon. |
| **Permitted Uses** | Calibration inputs (weighted carefully); honesty about certainty. Forbidden: treating self-report alone as mastery; writing system stage labels that imply mastery from completion. |

---

### 11. Review

| Aspect | Provision |
|--------|-----------|
| **Definition** | Educational activity that returns to previously studied material to reinforce retention or address decay — distinct from first-pass learning of the Current Learning Topic. |
| **Purpose** | Protect long-term retention without pretending review is the same as advancing the learning frontier. |
| **Owner** | Application and, when authorised, Educational Intelligence advisory or Phase-gated adaptive modes. |
| **Source** | Scheduling signals, Estimated Mastery / knowledge concerns, spaced-retention logic, student choice. |
| **Lifecycle** | Suggested, accepted, completed, or deferred. |
| **Student Visibility** | Visible as review or practice suggestions when shown; must be labelled as review when it is not Current Learning Topic work. |
| **Permitted Uses** | Advisory recommendations; future Adaptive Mode interruption only with disclosure. Forbidden: silent replacement of Learning Mode missions in Version 1.0. |

---

### 12. Revision

| Aspect | Provision |
|--------|-----------|
| **Definition** | Deliberate reworking of material — often exam-oriented consolidation — overlapping with but not identical to Review; oriented toward fixing gaps and consolidating for assessment. |
| **Purpose** | Support preparation intensity as exams approach without redefining Study Progress as mastery. |
| **Owner** | Application / Educational Intelligence when mode-authorised. |
| **Source** | Plan phase, readiness posture, evidence of gaps, student intent. |
| **Lifecycle** | Planned, suggested, undertaken, completed. |
| **Student Visibility** | Plain language (“revise”, “consolidate”) when appropriate. |
| **Permitted Uses** | Exam-season strategies and advisory guidance under Article VI. |

---

### 13. Attempt

| Aspect | Provision |
|--------|-----------|
| **Definition** | A discrete performance or practice episode against educational material (questions, checks, papers, structured exercises) that may yield Educational Evidence. |
| **Purpose** | Produce observable outcomes from which estimates may update. |
| **Owner** | Student performs; Application records; Evidence domain captures observation. |
| **Source** | Missions, quizzes, assessments, past-paper practice, diagnostics. |
| **Lifecycle** | Started, submitted/completed, recorded; outcomes feed evidence history. |
| **Student Visibility** | Visible as practice results, scores, and feedback — not as automatic mastery certificates. |
| **Permitted Uses** | Update Educational Evidence and, when quality warrants, Estimated Knowledge / Estimated Mastery. Attempt alone is not success, completion of syllabus study, or mastery. |

---

### 14. Completion

| Aspect | Provision |
|--------|-----------|
| **Definition** | The closing of a defined educational unit of work: a mission, session, attempt, or Study Progress mark for a topic — context determines which educational state updates. |
| **Purpose** | Honour finished work without over-claiming its meaning. |
| **Owner** | Student initiates or confirms where required; Application records. |
| **Source** | Explicit student action or lawful automatic closure of a bounded activity. |
| **Lifecycle** | Incomplete → completed for that unit of work; does not automatically imply mastery or readiness. |
| **Student Visibility** | “Completed”, “Completed studying”, session finished — never “Mastered” as a synonym for completion. |
| **Permitted Uses** | Advance Study Progress when the completed object is study coverage; close missions; create opportunity for reflection evidence. Forbidden: equating Completion with Mastery, Known, or Strong Topic. |

---

## ARTICLE V — Educational Evidence Constitution

### Section 1. What Is Educational Evidence?

Educational Evidence is a durable observation of educationally meaningful activity or assessment outcome that may lawfully inform knowledge-oriented belief.

Qualifying characteristics:

1. It records something that occurred in learning or assessment;
2. It is attributable to a student and an educational context (topic, curriculum, session, or equivalent);
3. It is retained as observation rather than rewritten as a desired recommendation;
4. Its quality and weight are ranked before it moves strong claims.

### Section 2. What Is Not Educational Evidence?

The following are not Educational Evidence for the purpose of updating Knowledge State or Estimated Mastery, though some may still update Study Progress or UX state:

1. Mere navigation, page views, or clicks without educational outcome;
2. System-generated recommendations, decisions, or mission artefacts (these are judgements/actions, not observations of student knowledge);
3. Engineering metadata, entitiy identifiers, warrants as display theatre, or pipeline labels;
4. Uncorroborated marketing claims or coaching rhetoric;
5. A Study Progress checkbox taken alone as proof of understanding;
6. Time spent alone, unaccompanied by educational outcome of recognised quality;
7. Student self-report alone treated as validated mastery.

### Section 3. Evidence Quality Ranking

From higher to lower typical epistemic weight for knowledge and mastery claims (illustrative hierarchy; finer calibration belongs to specialised architectures subordinate to this Constitution):

| Rank | Class | Examples |
|------|--------|----------|
| A | High-stakes objective performance | Official assessment outcomes; mock examinations under exam-like conditions; marked past papers with reliable scoring |
| B | Structured objective practice | Mission scores from assessed tasks; quizzes with known keys; timed practice sets with measured accuracy |
| C | Guided performance with partial objectivity | Supervised drills; partly scored exercises; mixed practice with outcome records |
| D | Reflective and subjective signals | Self-reflection; confidence ratings; student self-report of understanding |
| E | Exposure and engagement signals | Reading completion; time spent; session length |

Higher ranks may more readily justify updates to Knowledge and Estimated Mastery. Lower ranks alone must not manufacture high certainty.

### Section 4. Evidence Types and Permitted Updates

| Evidence type | May update Study Progress? | May update Knowledge? | May update Estimated Mastery? | May update Readiness? |
|---------------|----------------------------|------------------------|-------------------------------|------------------------|
| Official assessment | Yes, when coverage credit is educationally warranted | Yes | Yes | Yes |
| Mission score (assessed outcomes) | Yes for coverage when mission completes study of a unit; score itself is not mastery by decree | Yes, as observation of performance | Yes, as contributing evidence over time | Yes, as a factor among others |
| Quiz | Sometimes (if the product treats the quiz as completing a study obligation); otherwise no | Yes | Yes | Yes |
| Mock examination | Sometimes for coverage credit of examined units if so designed | Yes | Yes | Yes |
| Past paper | Sometimes under the same coverage rules as quizzes/mocks | Yes | Yes | Yes |
| Self reflection | No (unless separately accompanied by an explicit Study Progress action) | Only weakly; must not alone drive strong knowledge claims | Only weakly; must not alone drive high Estimated Mastery | Yes, cautiously as soft signal |
| Time spent | No | No as sole basis | No as sole basis | Yes, cautiously (pace/workload), never as mastery proof |
| Reading completion | Yes when reading is the defined study obligation for a unit | No as sole basis for strong knowledge claims | No as sole basis | Limited (coverage/pace signals only) |
| Confidence rating | No | Only as calibrated soft input | Only as calibrated soft input; never sole path to “Mastered” | Limited |
| Student self-report | Yes only when the report *is* a Study Progress declaration (“I have studied this”) | No as validated knowledge | No as validated mastery | Limited |

### Section 5. Accumulation Rule

Evidence accumulates. Interpreters may revise Estimated Knowledge and Estimated Mastery as history grows. One favourable observation does not constitutionalise lasting mastery.

### Section 6. Student Language for Evidence

Student-facing surfaces should prefer plain phrases (practice results, study checks, how you did) over the term “evidence”, unless educational clarity truly requires it. Internal domains may retain the constitutional term Educational Evidence.

---

## ARTICLE VI — Educational Decision Hierarchy

### Section 1. Modes

Kwalitec recognises educational operating modes. Only authorised modes may determine how missions and primary daily focus are chosen.

#### 1. Learning Mode

**Definition.** The default mode in which the student’s primary daily educational commitment follows the Current Learning Topic in official syllabus order within the active study context.

**Authority.** Learning Mode is the Version 1.0 authority for Today’s Mission topic selection.

**Rule.** Mission always follows Learning Mode while Learning Mode is the active primary mode.

#### 2. Revision Mode

**Definition.** A mode oriented toward consolidating and revising previously studied material, typically as examinations approach or when the student explicitly enters revision posture.

**Authority.** May guide primary focus only when constitutionally activated and disclosed to the student as revision — not as silent substitution for Learning Mode.

#### 3. Diagnostic Mode

**Definition.** A mode that prioritises creating clarifying Educational Evidence when knowledge warrant is thin or next-step uncertainty is high.

**Authority.** May propose diagnostics and short checks. Must not masquerade as mastery certification. Must not silently steal Learning Mode’s mission authority without disclosure and mode activation rules.

#### 4. Future Adaptive Mode

**Definition.** A later mode in which explained adaptive interruption (review, weak-topic focus, spaced reinforcement) may temporarily redirect primary focus according to evidence-informed need.

**Authority.** Deferred until Educational Intelligence Phase gating and student-visible explanation exist. Adaptive interruption is not Version 1.0 mission authority.

### Section 2. Mission Follows Learning Mode

While Learning Mode governs:

1. Today’s Mission tracks Current Learning Topic;
2. Review and weak-topic signals may appear as advisory recommendations;
3. Advisory surfaces must not present themselves as Today’s Mission when they name a different topic;
4. Calls to action must not imply acceptance of a contradictory topic as the learning mission.

### Section 3. Adaptive Interruption Deferred

Adaptive interruption of Learning Mode is deferred. No implementation may silently introduce Adaptive Mode behaviour as if it were already constitutional primary authority.

### Section 4. Advice Versus Command

Educational Intelligence should advise. It must not silently override the student’s authorised learning journey. Divergence between advisory recommendation and Learning Mode mission, if shown, must be labelled honestly (for example, optional review that is not today’s learning).

---

## ARTICLE VII — Student Communication Principles

### Section 1. Purpose of Language

Student-facing language is educational speech. It must be plain, truthful, and actionable. It must answer, where relevant:

1. What should I do?
2. Why should I do it?
3. What happens next?

### Section 2. Permitted Educational Language

The following families of language are generally permitted when used honestly:

| Language | Typical lawful use |
|----------|--------------------|
| Completed / Completed studying | Study Progress and finished sessions |
| Continue Learning | Advance along Current Learning Topic |
| Study Progress | Coverage narration |
| Learning Progress | Syllabus journey narration |
| Estimated Knowledge | Provisional understanding |
| Estimated Mastery | Provisional mastery estimate when evidence exists |
| Suggested / Recommended | Advisory guidance |
| Today’s Mission / today’s focus | Authorised commitment under Article VI |
| Practice / study check / short check | Diagnostics and evidence-creating activities without engineering jargon |
| Optional review (not today’s learning) | Non-mission advisory review |

### Section 3. Forbidden Educational Language

The following are forbidden on student-facing surfaces unless a future constitutional amendment and truthful warrant explicitly allow a carefully bounded exception:

1. Engineering and intelligence jargon: evidence_creating, pipeline, warrant tags, cold_start, thin_warrant, entity identifiers, Digital Twin (named as such), mission generation, classification enums, and similar;
2. False attainment from coverage alone: Mastered, Fully Learned, Finished Learning Forever as labels for Study Progress completion;
3. Factual strength labels without support: Known, Strong Topic, Weak Topic stated as fact when only thin or no objective evidence exists;
4. Composite or system jargon that students cannot act on (for example, composite score theatre without educational meaning).

Internal domains may retain precise engineering vocabulary. Presentation must map before render.

### Section 4. Vocabulary Discipline for Attainment

| Term | Rule |
|------|------|
| Mastered | Avoid as student checkbox or completion badge. Prefer Estimated Mastery when an estimate exists. |
| Known | Avoid as fact without strong objective evidence. Prefer Estimated Knowledge. |
| Strong Topic / Weak Topic | Avoid as bare fact; prefer estimated or suggested practice language with reasons. |
| Completed | Prefer for Study Progress and finished work. |

### Section 5. Twin Invisibility in Speech

Students experience guidance, learning profile status if needed for operators, and estimates — not Twin schemas, succession language, or research infrastructure names.

---

## ARTICLE VIII — Educational Integrity Rules

The following rules are immutable under this Constitution unless amended under Article X. They bind product, presentation, Educational Intelligence, and Digital Twin behaviours alike.

1. **Completion ≠ Mastery.** Completing study, a mission, or an attempt does not equate to mastery.
2. **Attempt ≠ Success.** An attempt is observation opportunity; outcome quality is separate.
3. **Confidence ≠ Understanding.** Student-felt confidence is not Educational Knowledge.
4. **Reading ≠ Retention.** Exposure is not proof that knowledge endures.
5. **Time ≠ Learning.** Duration alone does not establish understanding.
6. **Declaration ≠ Belief.** Student Study Progress declarations do not author Knowledge State.
7. **Recommendation ≠ Evidence.** Advice is not an observation of student knowledge.
8. **Readiness ≠ Next Action.** Preparedness judgement does not by itself schedule the mission.
9. **Decision ≠ Mission.** Choosing an educational intent does not automatically redefine Learning Mode authority.
10. **Evidence accumulates.** Strong mastery language requires sufficient history, not a single fortunate moment.
11. **Educational certainty requires objective evidence.** Rhetoric cannot manufacture warrant.
12. **Estimates remain estimates** until evidence and governance justify stronger speech.
13. **Learning Mode missions are not silently interrupted** while Adaptive Mode remains deferred.
14. **Study Plan coverage and Digital Twin understanding must never be mixed** in meaning or student narration.
15. **Trust is more important than optimisation.** When in conflict, prefer truthful continuity over clever diversion.
16. **Study Plan disposal must not erase learner educational history.** Deleting planning artefacts may clear schedules and temporary pointers; it must not silently destroy Study Progress, Attempts, Evidence posture, or Twin estimates without explicit informed educational reset.

---

## ARTICLE IX — Educational Governance

### Section 1. Mandatory Reference

Every future educational capability — including but not limited to Educational Intelligence work, Digital Twin work, missions, dashboards, analytics, study planning, and student messaging — must reference this Constitution before implementation begins.

### Section 2. Order of Authority

1. This Constitution;
2. Explicit amendments under Article X;
3. Subordinate educational policies and specialised architectures that comply with this Constitution;
4. Implementation.

Where subordinate documents conflict with this Constitution, this Constitution prevails until amended.

### Section 3. Non-Circumvention

No feature flag, experiment, advisory surface, or intermediate estimate store may circumvent Articles III, VI, VII, or VIII by renaming forbidden behaviour.

### Section 4. Ownership of Meaning

Educational concept ownership defined in Article IV is binding. Implementations may relocate storage or computation, but must preserve constitutional meaning and student-visible honesty.

Educational history persistence belongs to the learner. Study Plan rows may authorise Learning Mode context and receive coverage declarations, but deleting or replacing a Study Plan must not silently redefine or erase Study Progress, Study Attempts, Educational Evidence posture, Estimated Knowledge, or Estimated Mastery. Continuity rules are specialised under `EDUCATIONAL_CONTINUITY_STANDARD.md` and `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md`.

### Section 5. Programme Relationship

The Educational Governance Initiative exists to protect and evolve this Constitution. Capabilities that implement algorithms remain subordinate to governance.

---

## ARTICLE X — Amendment Process

### Section 1. When Amendment Is Required

An amendment is required before any change that would:

1. Redefine an Article IV educational state;
2. Alter evidence quality permissions in Article V;
3. Change Decision Hierarchy mode authority (Article VI);
4. Relax integrity rules (Article VIII);
5. Authorise previously forbidden student language as factual attainment;
6. Elevate Adaptive Mode or other modes to primary mission authority.

### Section 2. Amendment Principles

1. Amendments must be explicit, versioned, and recorded in this document (or a formal successor identified as the highest educational authority).
2. Implementation must never silently redefine educational concepts through code behaviour, copy changes, or telemetry reinterpretation.
3. Empirical learning from Internal Alpha and later programmes may motivate amendment; data does not itself amend the Constitution.
4. Architecture and product review should scrutinise amendments for student trust impact.

### Section 3. Compatibility of Subordinates

After amendment, subordinate policies and architectures must be brought into compliance. Until they are, this Constitution’s amended text remains controlling for educational meaning.

### Section 4. Continuity

Version identifiers and amendment notes shall preserve the trail of educational law so that future custodians understand why meaning shifted.

---

## Cross References

This Constitution stands above and informs:

- Educational Intelligence architectures and product flows (subordinate);
- Digital Twin constitutions and twin-update architectures (subordinate);
- Internal Alpha stabilisation doctrine (IA-001 through IA-004 and successors), especially truthful Learning Progress, Learning Mode, and student-centred messaging;
- Educational Philosophy Audit findings (diagnostic relative to this law);
- Product thesis in project orientation documents;
- Knowledge base educational subtree (philosophy, policies, recommendation, digital twin folders).

Subordinate documents explain *how* compliant systems may be designed. They do not redefine *what* educational truth is.

---

## Closing

Kwalitec’s educational law is now written.

Let every syllabus sequence, every mission, every estimate, and every word spoken to a student remain answerable to this Constitution.

**End of Constitution — Version 1.0**

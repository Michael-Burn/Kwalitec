# Knowledge & Mastery Educational Model

**Capability ID:** EIP-006-DESIGN  
**Programme:** Educational Integrity Programme  
**Classification:** Educational Model — subordinate specialised architecture  
**Status:** APPROVED — design; awaiting Architecture Review before implementation  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This document defines the educational meanings of **Study Progress**, **Knowledge**, **Competence**, and **Mastery** for Kwalitec.

It is subordinate to:

1. **KWALITEC_EDUCATIONAL_CONSTITUTION.md** (EGI-001) — highest educational authority  
2. **EDUCATIONAL_LOGIC_REGISTRY.md** (EGI-002) — operational educational behaviour  
3. **EDUCATIONAL_STATE_AUTHORITY_MATRIX.md** (EIP-001) — ownership and lawful writers  
4. **EDUCATIONAL_EVIDENCE_MODEL.md** / **EDUCATIONAL_EVIDENCE_AUTHORITY.md** (EIP-002) — evidence meaning  

Authority order for this subject:

> Constitution defines *that* study is not understanding and mastery requires accumulated evidence.  
> The Evidence Model defines *what* observations may lawfully support understanding claims.  
> **This Model defines the educational ladder that separates coverage, understanding, application, and mastery.**

This document:

- defines educational concepts and their lawful relationships;
- does **not** implement code, algorithms, or scoring mathematics;
- does **not** redesign the Constitution, Digital Twin, Educational Intelligence, Adaptive Learning, or Revision Mode;
- does **not** authorise product behaviour that collapses these concepts.

**This Model governs future Knowledge / Competence / Mastery implementation.  
Implementation never invents educational meaning absent from this Model.**

---

## Table of Contents

1. [Educational Philosophy](#1-educational-philosophy)
2. [Educational Definitions](#2-educational-definitions)
3. [Educational Relationships](#3-educational-relationships)
4. [Educational Evidence](#4-educational-evidence)
5. [Student Communication](#5-student-communication)
6. [Version 1 Scope](#6-version-1-scope)
7. [Future Evolution](#7-future-evolution)
8. [Cross References](#8-cross-references)

---

## 1. Educational Philosophy

### 1.1 Why This Ladder Exists

Professional examination preparation fails educationally when the platform treats finishing work as proof of learning.

A student may mark a topic complete, feel confident, and still be unable to reason under exam conditions. Conversely, a student may perform well once on a practice set and later forget under pressure. Educational truth therefore requires distinct answers to four different questions:

| Question | Concept |
|----------|---------|
| What have I studied? | **Study Progress** |
| How well do I currently understand this? | **Knowledge** |
| Can I apply this reliably when asked? | **Competence** |
| Have I shown lasting, exam-credible command over time? | **Mastery** |

These are separate educational concepts. Collapsing any two of them produces false readiness theatre — the precise trust failure Educational Integrity Programme work is designed to prevent.

### 1.2 Learning Progression Is Not Identical to Understanding

**Study Progress** answers coverage: whether the student has honestly covered a syllabus unit through declaration or lawful study completion.

Coverage is necessary for sequential learning. It is not sufficient for educational belief about understanding.

Reasons:

1. Studying can be incomplete, shallow, or poorly retained.  
2. A declaration of “I have studied this” is a coverage claim, not a performance observation.  
3. Mission or session completion closes work; it does not measure comprehension.  
4. Journey metrics (how far through the syllabus) narrate progress along order — not quality of understanding.

Therefore: **completing studying never implies Knowledge.**

Constitutional grounding: Article II §1.2 (“Study is not the same as understanding”); Article III §5; Article IV.1 vs IV.6–7.

### 1.3 Understanding Is Not Identical to Application

**Knowledge** answers understanding: a provisional estimate of how well the student currently comprehends a syllabus element.

Understanding is necessary for competent performance. It is not sufficient to claim competence.

Reasons:

1. A student may recognise concepts in familiar wording and still fail when the question form changes.  
2. Near-term recall after study differs from applying principles under novel or timed conditions.  
3. Estimated Knowledge may rise from recent practice that has not yet generalised.  
4. Soft signals (reflection, felt confidence) may accompany understanding estimates weakly; they do not prove transferable skill.

Therefore: **having Knowledge never implies Competence.**

Constitutional grounding: Article IV.6–7 (Knowledge State / Estimated Knowledge as understanding posture); Article V (evidence ranking and accumulation).

### 1.4 Application Is Not Identical to Mastery

**Competence** answers application: whether the student can perform correctly and usefully with the material when asked — typically under practice or assessment conditions attributable to syllabus scope.

Competence is necessary for Mastery. It is not sufficient to claim Mastery.

Reasons:

1. One successful attempt shows that application was possible *once*; it does not show durability.  
2. Performance under guided practice can exceed performance under exam-like pressure.  
3. Competence may decay without review; Mastery concerns sustained command.  
4. High confidence or high recent accuracy without accumulation still fails constitutional Mastery warrant.

**Mastery** is sustained demonstrated competence — longer-horizon, evidence-dense confidence that the student has durable command suitable for exam preparation judgement — always provisional when stated by the platform.

Therefore: **having Competence never implies Mastery.**  
**Mastery implies sustained demonstrated Competence, not merely high understanding.**

Constitutional grounding: Article II §1.3, §1.6; Article IV.8; Article V §5 (accumulation).

### 1.5 Binding Educational Doctrine for This Model

1. Coverage, understanding, application, and mastery answer different educational questions.  
2. Later concepts may depend on evidence that often accompanies earlier concepts, but must never be inferred from earlier concepts by fiat.  
3. Absence of a later concept is honest emptiness, not failure of Study Progress.  
4. Student trust requires naming estimates as estimates and refusing attainment language without warrant.  
5. Implementation storage, score sharing, or UI co-location never redefine meaning.

---

## 2. Educational Definitions

For each concept, this Model defines Purpose, Educational Meaning, Evidence Required, Student Visibility, and Relationship to the Constitution.

---

### 2.1 Study Progress

| Aspect | Definition |
|--------|------------|
| **Purpose** | Honour honest syllabus coverage without claiming understanding, application, or mastery. |
| **Educational meaning** | The record of what the student has marked or earned as studied for a syllabus unit (typically a topic). Answers: **“What have I studied?”** It is a coverage state on the Learning Mode spine. |
| **Evidence required** | Coverage evidence only: explicit student study-completion declaration, or lawful mission/session completion that advances coverage for that unit. No performance score is required. Understanding Evidence is not required for Study Progress to become completed studying. |
| **Student visibility** | Highly visible. Students see and may declare completed / not completed studying. Dashboards may summarise journey progress derived from Study Progress. Must never appear as “Mastered”, “Known”, or “Strong” from coverage alone. |
| **Relationship to the Constitution** | Article IV.1 (Study Progress); Article IV.2 / IV.3 (Learning Progress and Current Learning Topic depend on it); Article IV.14 (Completion may update coverage when the completed object is study coverage); Article VIII rules separating coverage from mastery; EL-001. |

**Educational boundary.** Study Progress remains Study Progress even when later Knowledge, Competence, or Mastery estimates change. Revision of understanding never silently erases rightful coverage without explicit educational authorisation (Educational Continuity).

---

### 2.2 Knowledge

| Aspect | Definition |
|--------|------------|
| **Purpose** | Represent provisional current understanding of a syllabus element without claiming certified knowledge or exam success. |
| **Educational meaning** | The understanding posture for a unit or domain. Internally this is Knowledge State; student-facingly it is **Estimated Knowledge**. Answers: **“How well do I currently understand this?”** It concerns comprehension and near-term grasp, not durable exam command. |
| **Evidence required** | Lawful Educational Evidence interpreted over time (Evidence Model / Authority). Study Progress alone is insufficient. Soft signals alone must not author strong Knowledge language. Thin history requires honest understatement or absence. |
| **Student visibility** | Visible when material, **always as an estimate**. Twin mechanics remain invisible. Prefer “Estimated knowledge”, “how well you seem to understand…”, or equivalent provisional language. Forbidden: “Known” as fact without strong objective warrant. |
| **Relationship to the Constitution** | Article IV.6 (Knowledge State); Article IV.7 (Estimated Knowledge); Article III §§3–5 (certainty and estimate framing); EL-006; EL-012 (Twin boundary). |

**Educational boundary.** Knowledge is not Study Progress renamed. Knowledge is not Competence. Knowledge is not Mastery. Product may presently co-locate presentation with mastery scalars; constitutionally the meaning remains distinct (documented presentation debt does not amend this Model).

---

### 2.3 Competence

| Aspect | Definition |
|--------|------------|
| **Purpose** | Name the educational capacity to apply understanding under attributable practice or assessment conditions — the bridge between knowing and lasting mastery. |
| **Educational meaning** | Demonstrated ability to use syllabus knowledge correctly when asked: solving, selecting, explaining, or performing within the scope of attributed material. Answers: **“Can I apply this when it matters in practice?”** Competence is performance-oriented application, not coverage and not mere recognition. |
| **Evidence required** | Objective or structured performance observations of sufficient quality (typically Evidence Quality Levels 2–4): question outcomes, quizzes, mocks, past-paper practice, or mission assessments when authorised. One weak engagement signal is insufficient. Self-report alone is insufficient. Study Progressive completion alone is forbidden as Competence proof. |
| **Student visibility** | When surfaced, must use plain application language (“practice shows you can apply…”, “assessment results suggest…”) and remain provisional where warrant is thin. Version 1 scope (§6) defers a distinct student-facing Competence construct; until then, Competence must not be implied by Study Progress badges or interchangeable “mastery” wording. |
| **Relationship to the Constitution** | Not a separately numbered Article IV state today; this Model introduces Competence as an **educational semantic layer** between Estimated Knowledge (IV.7) and Estimated Mastery (IV.8), consistent with Article II philosophy (study ≠ understanding ≠ lasting command) and Article V performance Evidence. It must not contradict the Constitution. Any future student-facing Competence state requires Registry and, if needed, constitutional Article IV amendment before implementation claims the label. |

**Educational boundary.** Competence may exist with incomplete Study Progress only in exceptional diagnostic or prior-learning contexts — and even then must not invent coverage. Competence without Mastery is the normal educational condition for many units during first-pass learning.

---

### 2.4 Mastery

| Aspect | Definition |
|--------|------------|
| **Purpose** | Support long-horizon preparation judgement with a provisional estimate of durable command — never checkbox mastery. |
| **Educational meaning** | Sustained demonstrated competence for a syllabus unit: evidence-dense confidence that the student can apply the material reliably over time, under conditions relevant to examination preparation. Answers: **“How confidently can we treat this as mastered for long-horizon preparation?”** Student-facingly: **Estimated Mastery**, always provisional. |
| **Evidence required** | Accumulated Educational Evidence of competence quality — density and outcomes over time, not a single favourable observation. High Mastery language requires higher warrant than Knowledge. Completion, elapsed time, and self-report alone are forbidden authors. Absent sufficient Attempt/Assessment Evidence, Estimated Mastery should be absent, not invented. |
| **Student visibility** | Visible **only when an estimate exists**; labelled Estimated Mastery (or equivalent honest language). Never a Study Progress checkbox. Never a synonym for “completed studying”. Prefer estimate framing over absolute “Mastered”. |
| **Relationship to the Constitution** | Article IV.8 (Estimated Mastery); Article II §1.3, §1.6–7; Article III §§3–5; Article V §§3–5; EL-007. |

**Educational boundary.** Mastery implies sustained Competence. Mastery does not imply that Study Progress was authored by estimates. Mastery does not convert Learning Progress into understanding quality.

---

### 2.5 Definition Summary

| Concept | Primary question | Educational class | Typical student framing |
|---------|------------------|-------------------|-------------------------|
| **Study Progress** | What have I studied? | Coverage (Observed / Derived Fact) | Completed studying |
| **Knowledge** | How well do I understand this now? | Understanding estimate | Estimated knowledge |
| **Competence** | Can I apply this when asked? | Application capacity | Practice / assessment application (when surfaced) |
| **Mastery** | Do I show lasting, exam-credible command? | Long-horizon estimate | Estimated mastery |

---

## 3. Educational Relationships

### 3.1 Relationship Diagram (Educational, Not Algorithmic)

```
Study Progress ──────────────────────────────► Learning Mode spine
   (coverage)                                  (Current Learning Topic / Mission)

Educational Evidence (understanding / performance)
         │
         ├──────────────► Knowledge
         │                 (current understanding estimate)
         │
         ├──────────────► Competence
         │                 (demonstrated application capacity)
         │
         └──────────────► Mastery
                            (sustained demonstrated competence;
                             denser / longer-horizon warrant)
```

Study Progress and the understanding ladder are **siblings of different kinds**, not a pipeline:

- Study Progress is not an input that creates Knowledge by succession.  
- Knowledge does not create Competence by renaming.  
- Competence does not become Mastery by a single high score.  
- Mastery never writes Study Progress.

### 3.2 Dependencies

| Concept | May depend upon | Must never depend upon as sole author |
|---------|-----------------|----------------------------------------|
| **Study Progress** | Student declaration; lawful coverage completion; syllabus order / active study context | Estimated Knowledge; Competence; Estimated Mastery; recommendations; Twin belief |
| **Knowledge** | Accumulated Educational Evidence of understanding quality | Study Progress alone; Completion alone; Confidence alone; Mission artefact alone |
| **Competence** | Performance Evidence that demonstrates application | Study Progress alone; Knowledge estimate alone without application Evidence; Confidence alone |
| **Mastery** | Accumulated Competence-quality Evidence over time; often co-informed by Knowledge posture | Study Progress alone; single attempt alone; Knowledge high score alone; Confidence alone; Completion alone |

### 3.3 Independence Rules

Which concepts may exist independently:

1. **Study Progress without Knowledge** — common and lawful. A student may complete studying with no performance Evidence yet.  
2. **Knowledge without Competence** — lawful. Understanding estimates may exist from soft or early practice Evidence before reliable application is shown.  
3. **Competence without Mastery** — expected during preparation. Application demonstrated once or sparsely is not lasting Mastery.  
4. **Knowledge without Study Progress** — exceptional (e.g. prior learning / diagnostic Evidence). Must not invent coverage. Study Progress remains coverage-owned.  
5. **Mastery without Study Progress** — educationally unstable for Learning Mode narration. Mastery estimates must not mint coverage to “repair” the story. Prefer advisory review language over rewriting Study Progress.

### 3.4 Forbidden Implications

The following implications are educationally unlawful:

| Unlawful implication | Why forbidden |
|----------------------|---------------|
| Study Progress ⇒ Knowledge | Coverage is not understanding. |
| Study Progress ⇒ Competence | Coverage is not application. |
| Study Progress ⇒ Mastery | Coverage is not mastery. |
| Knowledge ⇒ Competence | Understanding is not proven application. |
| Knowledge ⇒ Mastery | High understanding is not sustained competence. |
| Competence ⇒ Mastery | Application once is not mastery. |
| Mastery ⇒ Study Progress | Estimates must never author coverage truth. |
| Completion ⇒ Mastery | Closing work is not attainment. |
| Confidence ⇒ Mastery | Felt confidence is soft signal only. |
| Time spent ⇒ Mastery | Exposure duration is not competence. |

### 3.5 Lawful Positive Implications

| Lawful relation | Educational meaning |
|-----------------|---------------------|
| Mastery ⇒ sustained Competence (as educational claim posture) | Mastery language is only warranted when Competence-quality Evidence has accumulated. |
| Competence Evidence may support Knowledge updates | Application performance often revises understanding estimates. |
| Knowledge thinness may advise against Mastery speech | Without understanding warrant, Mastery language is theatre. |
| Study Progress may coexist with any understanding state | Coverage and estimates evolve independently under separate owners. |

### 3.6 Illustrative Educational Cases

**Case A — Complete studying without Knowledge**  
A student marks three topics completed studying after reading and mission coverage. No scored attempt Evidence exists. Study Progress is complete. Knowledge is absent or thin. This is honest.

**Case B — Have Knowledge without Competence**  
Evidence shows the student can recall definitions in familiar items. Under varied question forms, performance fails. Estimated Knowledge may be modestly present; Competence remains unsupported. Mastery must remain absent.

**Case C — Have Competence without Mastery**  
A quiz and a practice set show strong application on one week. Weeks later, no further attributable performance exists. Competence was demonstrated; Mastery is not yet warranted.

**Case D — Mastery as sustained Competence**  
Multiple assessment-quality Observations across time show stable application under exam-like conditions. Estimated Mastery may become visible as an estimate. Study Progress remains whatever coverage truth already held; estimates did not invent it.

---

## 4. Educational Evidence

This section maps each concept to Required Evidence, Insufficient Evidence, and Forbidden Assumptions. Quality Levels refer to the Educational Evidence Model; they define claim lawfulness, not numerical weights.

---

### 4.1 Study Progress

**Required evidence**

- Explicit student declaration of study completion for the unit; **or**  
- Lawful mission/session completion that advances coverage for that unit under Learning Mode / Study Progress rules.

**Insufficient evidence**

- Mere navigation or page views without a coverage declaration or lawful coverage completion;  
- High Estimated Knowledge or Estimated Mastery without a coverage event;  
- Recommendation acceptance;  
- Felt confidence reported alone.

**Forbidden assumptions**

- That completing studying means the student understands the topic;  
- That completing studying means the student can apply the topic;  
- That completing studying means the topic is mastered;  
- That mastery thresholds may mark Study Progress complete.

---

### 4.2 Knowledge

**Required evidence**

- One or more lawful Educational Evidence Observations interpreted as understanding signals (commonly Levels 1–4 contributory; strong Knowledge speech requires denser/higher-quality Evidence under Constitution Articles III and V).

**Insufficient evidence**

- Study Progress completion alone (Level 0 for understanding);  
- Mission completion alone;  
- Elapsed time alone;  
- Self-reported confidence alone for strong Knowledge claims;  
- A single weak engagement event for confident “known” language.

**Forbidden assumptions**

- That Estimated Knowledge is verified Knowledge;  
- That Study Progress and Knowledge may share one student meaning;  
- That recommendations observing the student create Knowledge Evidence;  
- That absence of Knowledge Evidence means the student is “weak” as factual label without warrant.

---

### 4.3 Competence

**Required evidence**

- Performance Observations demonstrating application within attributable syllabus scope (typically Levels 2–4): scored attempts, quizzes, mocks, past-paper practice, authorised mission assessments.

**Insufficient evidence**

- Study Progress alone;  
- Reading completion alone;  
- Felt confidence alone;  
- Estimated Knowledge high solely from recognition-style soft Evidence;  
- One ambiguous partial attempt without interpretable outcome.

**Forbidden assumptions**

- That Competence equals Mastery;  
- That Competence may be declared by the student as certified fact;  
- That Competence authorises rewriting Study Progress;  
- That Version 1 product scalars labelled “mastery” already constitute a governed Competence construct (see §6).

---

### 4.4 Mastery

**Required evidence**

- Accumulated Competence-quality Educational Evidence over time, with density and outcomes sufficient for long-horizon provisional judgement;  
- Minimum attempt/assessment warrant before any Estimated Mastery is shown (honest absence preferred over early Mastered theatre).

**Insufficient evidence**

- One favourable Observation;  
- Mission completion alone;  
- Study Progress alone;  
- High Estimated Knowledge alone;  
- Sparse history even with high recent accuracy;  
- Self-report alone (including “Very Confident”).

**Forbidden assumptions**

- That Mastery is a checkbox the student may tick;  
- That Mastery is permanent once shown;  
- That Mastery implies the platform has certified examination success;  
- That Mastery may auto-complete Study Progress;  
- That “Mastered” stage language from thin history is educationally lawful.

---

### 4.5 Evidence Ladder Summary

| Evidence posture | May support Study Progress | May support Knowledge | May support Competence | May support Mastery |
|------------------|----------------------------|-----------------------|------------------------|---------------------|
| Coverage declaration / coverage completion | Yes | No | No | No |
| Engagement / soft signals | No alone | Weakly / provisional | No alone | No alone |
| Structured practice outcomes | No alone | Contributory | Contributory / Yes | Contributory only with accumulation |
| Assessment / exam-like outcomes | Sometimes (if also coverage rules) | Contributory / Yes | Yes | Contributory toward accumulation |
| Accumulated Competence-quality history | No (coverage separate) | Yes | Yes | Yes (when density warrants) |

---

## 5. Student Communication

Communication must remain plain, truthful, and free of engineering jargon (Constitution Article VII; Educational Explainability Standard).

### 5.1 How to Explain Each Concept

| Concept | Student explanation (plain language) |
|---------|--------------------------------------|
| **Study Progress** | “This shows which topics you have finished studying — not how well you know them yet.” |
| **Knowledge** | “This is our estimate of how well you currently understand a topic. It can change as you practise.” |
| **Competence** | “This means you have shown you can apply the topic in practice or checks — using it, not only recognising it.” |
| **Mastery** | “This is our estimate that your ability to apply the topic looks lasting enough for long-term exam preparation. It is still an estimate, and it needs practice over time.” |

### 5.2 Language Rules

1. Prefer **Completed studying** for Study Progress.  
2. Prefer **Estimated knowledge** / provisional understanding language for Knowledge.  
3. Prefer **practice shows / assessment shows you can apply** for Competence when surfaced.  
4. Prefer **Estimated mastery** for Mastery; avoid absolute **Mastered** as a coverage badge.  
5. Never use one label for two concepts on the same surface without clear separation.  
6. When evidence is thin: say what is unknown, or hide the estimate — do not invent confidence.

### 5.3 Forbidden Student Phrases (Representative)

- “You’ve mastered this” after only completing a mission.  
- “You know this” solely because Study Progress is complete.  
- “Strong topic” from coverage or confidence alone.  
- Any sentence that makes Estimated Mastery sound like a certified result.

### 5.4 Good Student Phrases (Representative)

- “You’ve completed studying this topic. Practice will help us estimate how well you understand it.”  
- “Estimated knowledge is based on your practice results so far.”  
- “Your recent checks suggest you can apply this. We’ll need more practice over time before treating it as lasting mastery.”  
- “No mastery estimate yet — not enough practice evidence.”

---

## 6. Version 1 Scope

This section separates what Version 1 may truthfully claim to measure from what remains educational aspiration.

### 6.1 Version 1 Truly Measures (Educational Claims Allowed)

| Concept | Version 1 posture |
|---------|-------------------|
| **Study Progress** | **Yes — core measured construct.** Coverage declarations and lawful coverage completions are Version 1 educational truth for the Learning Mode spine. |
| **Knowledge** | **Partial — Estimated Knowledge as educational meaning.** Version 1 may surface provisional understanding language when lawful Evidence pathways exist (including interim authorised Study Attempt structured results). Distinct storage / fully separated Twin Knowledge State presentation may remain incomplete; meaning must still follow this Model and EL-006. |
| **Mastery** | **Partial — Estimated Mastery only.** Version 1 may show Estimated Mastery when minimum Evidence warrant exists, with estimate framing and honest absence when thin. High mastery language requires accumulation rules already constitutional. Absolute Mastery-as-fact is out of scope. |
| **Competence** | **Deferred as a distinct Version 1 student-facing construct.** |

### 6.2 Explicit Deferral: Competence Beyond Version 1

**Competence is deferred beyond Version 1 as a separately owned, student-visible educational state.**

Reasons:

1. Version 1’s stable educational spine is coverage honesty + evidence-bound estimates (Knowledge / Mastery meanings), not a four-state attainment UI.  
2. Premature Competence labelling would likely collapse into existing mastery scalars and recreate FINDING-012-style synonym theatre.  
3. Competence semantics in this Model remain binding for **interpretation and future design**, so implementation may not invent Competence theatre under another name.  
4. Until Competence is Registry-registered (and Constitution-aligned if added as Article IV state), product speech must not claim “Competence measured.”

Operational consequence for Version 1:

- Practice and assessment Evidence may update Estimated Knowledge and Estimated Mastery under EIP-002 authority;  
- Those updates must respect that Mastery requires sustained Competence-quality Evidence;  
- Surfaces must not introduce a third attainment badge called Competence in Version 1 without Architecture-approved Registry amendment.

### 6.3 Version 1 Aspirations (Not Claimed Complete)

| Aspiration | Status |
|------------|--------|
| Fully separated Knowledge vs Mastery persistence and presentation | Future clarification / productisation |
| Distinct Competence state with own ownership, writers, and student ribbon | Deferred beyond Version 1 |
| Full authorised Evidence catalogue (quiz, mock, official exam) live | Reserved / partial |
| Adaptive Learning Mode primary authority | Deferred (Constitution Article VI) |
| Revision Mode as primary mission authority | Deferred until disclosed mode activation |
| Digital Twin as fully student-visible understanding engine | Reserved; Twin remains invisible; meaning Twin-owned |
| Educational Intelligence redesign | Out of scope for this Model |

### 6.4 Version 1 Non-Claims

Version 1 must not claim:

1. That Study Progress measures Knowledge, Competence, or Mastery.  
2. That Estimated Mastery is certified Mastery.  
3. That Competence is a shipped, governed student metric.  
4. That shared internal scalars prove educational equivalence of Knowledge and Mastery.

---

## 7. Future Evolution

This Model reserves space for later educational capabilities without redesigning them here.

### 7.1 Adaptive Learning

Future Adaptive Mode may use Knowledge, Competence, and Mastery estimates to explain temporary interruption of Learning Mode. Interruption remains mode-gated, disclosed, and constitutionally authorised. Adaptive Learning must consume these concepts; it must not redefine them.

### 7.2 Revision Mode

Revision Mode may prioritise units with Competence gaps or Mastery decay concerns while preserving Study Progress as coverage history. Revision must be labelled as revision — not as silent replacement of first-pass Learning Mode.

### 7.3 Digital Twin

The Digital Twin remains the conceptual owner of understanding posture (Knowledge State) and authorised mastery estimates. Twin implementation evolution may refine storage and succession. Twin naming stays invisible to students. This Model does not redesign Twin architecture.

### 7.4 Educational Intelligence

Educational Intelligence may advise using Knowledge / Competence / Mastery distinctions (for example, optional review when Competence is thin despite completed studying). Intelligence advises; it does not commandeer Learning Mode without disclosure and mode authority. This Model does not redesign Educational Intelligence.

### 7.5 Possible Future Constitution / Registry Work

If Competence becomes a student-facing educational state:

1. Amend or extend Article IV (or accept this Model + Registry entry as specialised architecture under Constitution philosophy);  
2. Register ownership and writers in the State Authority Matrix;  
3. Add Educational Logic for Competence succession;  
4. Re-certify messaging under Explainability and Governance Review.

Until then, Competence remains a **binding semantic distinction** for design and evidence interpretation, not a Version 1 product claim.

---

## 8. Cross References

| Document | Role |
|----------|------|
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Highest educational authority; Article IV state meanings; Article V evidence; Article VII language |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-001 Study Progress; EL-006 Estimated Knowledge; EL-007 Estimated Mastery |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Ownership / writers for coverage and estimate states |
| `EDUCATIONAL_EVIDENCE_MODEL.md` | Activity ≠ Evidence ≠ Inference ≠ Knowledge; quality levels |
| `EDUCATIONAL_EVIDENCE_AUTHORITY.md` | Version 1 authorised evidence pathways |
| `EDUCATIONAL_STATE_LIFECYCLE_ARCHITECTURE.md` | Lifecycle chain; Knowledge vs Mastery sibling relationship |
| `EDUCATIONAL_EXPLAINABILITY_STANDARD.md` | Student-facing claim honesty |
| `EDUCATIONAL_CONTINUITY_STANDARD.md` | Study Progress and estimate history belong to the learner |
| `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | Programme sequencing toward Version 1 readiness |

---

## Closing

This Model establishes the educational ladder that Kwalitec must respect:

> **Study Progress ≠ Knowledge ≠ Competence ≠ Mastery.**

Learning progression measures coverage. Understanding measures provisional grasp. Competence measures demonstrated application. Mastery measures sustained demonstrated competence.

No implementation may collapse these meanings for convenience.

**Status:** Awaiting Architecture Review.  
**Next:** Do not begin EIP-006 implementation until Architecture Review returns.

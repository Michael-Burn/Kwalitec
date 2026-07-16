# Educational Evidence Model

**Capability ID:** EIP-002-DESIGN  
**Programme:** Educational Integrity Programme  
**Classification:** Educational Model — subordinate specialised architecture  
**Status:** APPROVED — design; awaiting Architecture Review before implementation  
**Version:** 1.0  
**Date:** 2026-07-15  

---

## Authority

This document defines the educational meaning of **Educational Evidence** for Kwalitec.

It is subordinate to:

1. **KWALITEC_EDUCATIONAL_CONSTITUTION.md** (EGI-001) — highest educational authority  
2. **EDUCATIONAL_LOGIC_REGISTRY.md** (EGI-002) — operational educational behaviour  
3. **EDUCATIONAL_STATE_AUTHORITY_MATRIX.md** (EIP-001) — ownership and lawful writers  

Authority order for this subject:

> Constitution defines *that* objective evidence is required.  
> The Logic Registry names Educational Evidence as the only authority capable of updating Twin-owned educational states.  
> **This Model defines what Educational Evidence actually is.**

This document:

- defines educational concepts and claim lawfulness;
- does **not** implement code, algorithms, or scoring mathematics;
- does **not** redesign the Constitution, the Digital Twin, or Educational Intelligence;
- does **not** authorise product behaviour that contradicts the Constitution or Registry.

**The Educational Evidence Model governs EIP-002 implementation.  
Implementation never invents evidence meaning absent from this Model.**

---

## Table of Contents

1. [Purpose](#1-purpose)
2. [Educational Evidence Principles](#2-educational-evidence-principles)
3. [Educational Evidence Hierarchy](#3-educational-evidence-hierarchy)
4. [Evidence Quality Levels](#4-evidence-quality-levels)
5. [Educational Inference Rules](#5-educational-inference-rules)
6. [Future Evolution](#6-future-evolution)
7. [Cross References](#7-cross-references)

---

## 1. Purpose

### 1.1 Why Educational Evidence Exists

Kwalitec coaches students for demanding professional examinations. Trust collapses when the platform claims that a student *knows* or *has mastered* material on grounds that are merely administrative, declarative, or optimistically inferred.

Educational Evidence exists so that every material claim about understanding rests on **observed educational happenings**, not on convenience, rhetoric, or coverage theatre.

Without Educational Evidence:

- Study Progress would be mistaken for competence;
- Mission completion would be mistaken for mastery;
- Self-reported confidence would be mistaken for validated knowledge;
- Recommendations would be mistaken for observations of learning.

With Educational Evidence:

- inference may interpret history;
- estimates may rise, fall, or remain thin;
- student-facing language may stay honest under cold start and sparse history.

Educational Evidence is therefore the honesty backbone of Estimated Knowledge, Estimated Mastery, and every educational claim that pretends to describe understanding.

### 1.2 Four Distinct Concepts

The following four concepts must never be collapsed.

| Concept | Definition | Primary question | Constitutional role |
|---------|------------|------------------|---------------------|
| **Activity** | Something the student or system did or scheduled (navigate, open a topic, start a mission, mark coverage, accept advice). | What happened as an action? | May update Study Progress or UX state when lawful; is not, by itself, knowledge. |
| **Evidence** | A durable, attributable observation of educationally meaningful outcome or performance — a record of what happened educationally. | What was observed? | Sole lawful observational input that may evolve Twin-owned understanding states. |
| **Inference** | Interpretation of accumulated Evidence into provisional beliefs (estimates, readiness judgements, advisory factors). | What may we believe, provisionally? | May interpret Evidence; may not invent Evidence. |
| **Knowledge** | The educational understanding posture — internally Knowledge State; student-facingly Estimated Knowledge / Estimated Mastery. | How well is this understood (as estimate)? | Twin-owned; evolves only through lawful evidence-driven succession. |

**Succession law (educational, not algorithmic):**

```
Activity
   ↓  (only when the activity yields a qualifying observation)
Educational Evidence
   ↓  (interpretation; never invention)
Inference
   ↓
Knowledge (Estimated Knowledge / Estimated Mastery / Knowledge State)
```

Activity without a qualifying observation does not enter the Evidence domain.  
Inference without Evidence is educational fiction.  
Knowledge without Evidence succession is unconstitutional certainty.

### 1.3 Relationship to Coverage

Study Progress answers: *What have I studied?*  
Educational Evidence and Knowledge answer: *What observations support claims about understanding?*

A student may lawfully complete Study Progress for a unit while Educational Evidence for that unit remains empty. In that case Kwalitec may narrate coverage and must withhold knowledge and mastery certainty.

---

## 2. Educational Evidence Principles

These principles bind all future EIP-002 implementation and all educational speech about evidence. They refine Constitution Articles III and V; they do not amend them.

### 2.1 Evidence Is Observed

Educational Evidence records something that occurred in learning or assessment. It is an observation, not a plan, not a recommendation, and not a desired conclusion written backwards into history.

### 2.2 Evidence Is Objective in Claim Law

“Objective” here means **epistemically accountable**: attributable to a student and educational context, retained as observation, and ranked by quality before it supports strong claims.

Subjective signals (reflection, felt confidence) may exist as low-quality evidence or soft calibration inputs. They do not become high certainty by repetition of wording alone.

### 2.3 Evidence Accumulates

Evidence accumulates over time. Interpreters may revise estimates as history grows. One favourable observation does not constitutionalise lasting mastery. Conflicting observations require honest understatement, not selective theatre.

### 2.4 Evidence Has Quality

Not all observations carry equal epistemic weight. Quality Levels (Section 4) determine what educational conclusions an observation may support. Lower quality alone must not manufacture high certainty.

### 2.5 Evidence Expires Only by Defined Educational Rules

Observations are retained as history. They are not silently rewritten to fit a preferred estimate. Educational decay, supersession, or reduced weight may occur only under **explicit educational rules** defined in subordinate architectures authorised by the Constitution — never by informal product convenience or silence.

This Model does not define numerical half-lives. It asserts only that expiry or de-weighting, if any, must be educationally named and lawfully authorised.

### 2.6 Activity Alone Is Not Knowledge

Completing a mission, marking a topic studied, spending time, or feeling confident is activity (and sometimes coverage). It is not knowledge. Knowledge arises only when qualifying Evidence is recorded and lawfully interpreted.

### 2.7 Inference May Not Invent Evidence

Inference interprets Evidence. Inference may not mint Evidence by renaming recommendations, decisions, mastery formulae, or marketing language as observations of student knowledge.

### 2.8 Absence of Evidence Is Uncertainty, Not Weakness as Fact

Absence of Evidence is not Evidence of mastery, readiness, or weakness stated as fact. Thin history requires understatement.

### 2.9 Students Experience Outcomes; Domains Retain the Term Evidence

Student-facing surfaces prefer plain phrases (practice results, study checks, how you did). Internal domains may retain the constitutional term Educational Evidence.

---

## 3. Educational Evidence Hierarchy

### 3.1 How to Read This Hierarchy

Every evidence **source** below is classified by educational meaning. For each source:

| Field | Meaning |
|-------|---------|
| **Purpose** | Why this observation exists educationally |
| **Reliability** | Typical epistemic trustworthiness for understanding claims |
| **Educational Meaning** | What the observation lawfully says |
| **May update Study Progress?** | Coverage advancement (EL-001) |
| **May update Educational Evidence?** | Whether a durable evidence observation may be recorded |
| **May update Estimated Knowledge?** | Twin-facing understanding estimate (EL-006), never by this source alone unless Level permits |
| **May update Estimated Mastery?** | Twin-facing mastery estimate (EL-007), subject to accumulation and Level |

**Key distinctions:**

- **May update Educational Evidence?** asks whether the source may *enter* the Evidence domain as a retained observation. Entering the domain is necessary but not sufficient for strong knowledge claims.
- Update permissions for Estimated Knowledge and Estimated Mastery always require: (1) lawful Evidence recording where applicable; (2) Quality Level warrant (Section 4); (3) Twin / authorised estimation as sole writer (State Authority Matrix). No source below writes those estimates directly by fiat.
- “Weakly / contributory” means the source may inform interpretation only as a soft or partial signal and **must not alone** drive strong knowledge or high mastery language.

### 3.2 Source Catalogue

#### EV-01 — Reading a Topic

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record that the student engaged with instructional content for a syllabus unit. |
| **Reliability** | Low for understanding; may be high for honest coverage when reading *is* the defined study obligation. |
| **Educational Meaning** | Exposure / engagement. Shows contact with material, not demonstrated comprehension. |
| **Quality Level** | Level 1 — Engagement (typically) |
| **May update Study Progress?** | Yes, when reading is the defined study obligation for that unit; otherwise no. |
| **May update Educational Evidence?** | Yes, as engagement / exposure observation. |
| **May update Estimated Knowledge?** | No as sole basis for strong claims; contributory only at Level 1 limits. |
| **May update Estimated Mastery?** | No as sole basis. |

---

#### EV-02 — Completing a Mission (Completion Event Alone)

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Honour that a bounded study commitment was finished. |
| **Reliability** | High for activity closure and often for coverage; **none** for mastery by itself. |
| **Educational Meaning** | Completion / Activity. Closing a unit of work. Not an assessment outcome unless scored performance is separately recorded. |
| **Quality Level** | Level 0 — Administrative for understanding claims; may accompany Level 1+ observations if outcomes are captured. |
| **May update Study Progress?** | Yes, when the completed work is study coverage of a unit (EL-004). |
| **May update Educational Evidence?** | No from the completion checkbox alone. Yes only for accompanying lawful observations (scores, attempts, reflections) recorded as distinct evidence items. |
| **May update Estimated Knowledge?** | No from completion alone. |
| **May update Estimated Mastery?** | No from completion alone. |

---

#### EV-03 — Question Attempts

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record that the student undertook discrete performance episodes against educational items. |
| **Reliability** | Medium when outcomes are recorded; low if attempt existence alone is kept without result. |
| **Educational Meaning** | Attempt (Constitution IV.13). Performance episode that *may* yield Evidence; the attempt event is not success, coverage completion, or mastery. |
| **Quality Level** | Level 2 — Practice when outcomes exist; Level 0 if only “started” without educational outcome. |
| **May update Study Progress?** | No by attempt alone; only if product rules treat a completed assessed set as fulfilling a study obligation (then via Completion / Study Progress rules, not via attempt identity). |
| **May update Educational Evidence?** | Yes when an educational outcome (submission, score, correctness pattern, or structured result) is observed. |
| **May update Estimated Knowledge?** | Contributory when outcomes exist; subject to Level 2–3 rules and accumulation. |
| **May update Estimated Mastery?** | Contributory when outcomes exist and accumulate; never from a single attempt alone as lasting mastery. |

---

#### EV-04 — Question Scores

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record measured correctness or performance quality on attempted items. |
| **Reliability** | Medium to high depending on item quality, key reliability, and conditions. |
| **Educational Meaning** | Structured objective practice outcome (or guided partial objectivity if scoring is partial). Observation of performance, not a mastery certificate. |
| **Quality Level** | Level 2 — Practice (partial / light keys) or Level 3 — Assessment (known keys, measured accuracy). |
| **May update Study Progress?** | No from score alone. |
| **May update Educational Evidence?** | Yes. |
| **May update Estimated Knowledge?** | Yes, as contributing evidence; strength limited by Level and accumulation. |
| **May update Estimated Mastery?** | Yes, as contributing evidence over time; not as instant high-certainty mastery from one score. |

---

#### EV-05 — Quiz Results

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record outcomes of a bounded, keyed check of understanding. |
| **Reliability** | High among practice contexts when keys and scope are educationally sound. |
| **Educational Meaning** | Structured objective practice / assessment observation for the examined syllabus scope. |
| **Quality Level** | Level 3 — Assessment (typical). |
| **May update Study Progress?** | Sometimes — only if the product treats the quiz as completing a defined study obligation for covered units; otherwise no. |
| **May update Educational Evidence?** | Yes. |
| **May update Estimated Knowledge?** | Yes, as contributing evidence. |
| **May update Estimated Mastery?** | Yes, as contributing evidence; accumulation still required for high language. |

---

#### EV-06 — Mock Examinations

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record performance under exam-like or whole-paper practice conditions. |
| **Reliability** | High when conditions, marking, and scope approximate the target examination; otherwise Level 3. |
| **Educational Meaning** | High or structured performance observation across examined domains — strong warrant for preparedness interpretation, never checkbox mastery of every micro-topic unless outcomes attribute accordingly. |
| **Quality Level** | Level 3 — Assessment, or Level 4 when exam-like reliability criteria are met. |
| **May update Study Progress?** | Sometimes for coverage credit of examined units if so designed. |
| **May update Educational Evidence?** | Yes. |
| **May update Estimated Knowledge?** | Yes. |
| **May update Estimated Mastery?** | Yes, as strong contributing evidence; still cumulative and provisional. |

---

#### EV-07 — Official Examinations

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record outcomes from formal, externally authoritative assessment. |
| **Reliability** | Highest typical reliability among performance classes when authenticity is established. |
| **Educational Meaning** | High-stakes objective performance. Strongest constitutional warrant for knowledge- and mastery-oriented estimates for attributable scope. |
| **Quality Level** | Level 4 — High-confidence Assessment. |
| **May update Study Progress?** | Yes when coverage credit is educationally warranted for attributable units. |
| **May update Educational Evidence?** | Yes. |
| **May update Estimated Knowledge?** | Yes. |
| **May update Estimated Mastery?** | Yes — strongest class of contributing evidence; estimates remain estimates unless and until communication rules allow stronger speech with warrant. |

---

#### EV-08 — Reflection

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Capture the student’s considered self-view of what was hard, clear, or unfinished after study or practice. |
| **Reliability** | Low for validated understanding; useful for coaching honesty and calibration. |
| **Educational Meaning** | Reflective / subjective signal. Soft observation of metacognition — not proof of knowledge. |
| **Quality Level** | Level 1 — Engagement (epistemic class: subjective soft signal). |
| **May update Study Progress?** | No, unless separately accompanied by an explicit Study Progress action. |
| **May update Educational Evidence?** | Yes, as Rank-D / soft reflective evidence. |
| **May update Estimated Knowledge?** | Only weakly; must not alone drive strong knowledge claims. |
| **May update Estimated Mastery?** | Only weakly; must not alone drive high Estimated Mastery. |

---

#### EV-09 — Self-Reported Confidence

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Capture felt confidence separately from educational warrant. |
| **Reliability** | Low for attainment; may assist calibration when carefully weighted. |
| **Educational Meaning** | Student-felt confidence (Constitution IV.10). Soft signal. Never verified mastery. |
| **Quality Level** | Level 1 — Engagement (subjective soft signal). |
| **May update Study Progress?** | No. |
| **May update Educational Evidence?** | Yes only as soft confidence observation — never as understanding Evidence of Level 3+. |
| **May update Estimated Knowledge?** | Only as calibrated soft input; never sole path. |
| **May update Estimated Mastery?** | Only as calibrated soft input; never sole path to high mastery language or “Mastered”. |

**Ownership note:** Students own felt-confidence reports. Twin owns educational warrant. Confidence must not co-write Study Progress or impersonate assessment Evidence.

---

#### EV-10 — Time Spent Studying

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record exposure duration or session length as a workload / pace signal. |
| **Reliability** | Lowest for understanding claims. |
| **Educational Meaning** | Engagement / exposure. Effort indication — not comprehension. |
| **Quality Level** | Level 1 — Engagement; Level 0 if mere timer noise without educational attribution. |
| **May update Study Progress?** | No. |
| **May update Educational Evidence?** | Yes as weak engagement observation when attributable; otherwise administrative telemetry only (not Evidence of understanding). |
| **May update Estimated Knowledge?** | No as sole basis. |
| **May update Estimated Mastery?** | No as sole basis. |

---

#### EV-11 — Past-Paper Practice (Attributed)

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Record performance on authentic or near-authentic examination items. |
| **Reliability** | High when scoring is reliable; approaches Level 4 under exam-like conditions. |
| **Educational Meaning** | Structured objective practice / high-stakes practice for attributable syllabus scope. |
| **Quality Level** | Level 3 typical; Level 4 when conditions justify. |
| **May update Study Progress?** | Sometimes under the same coverage rules as quizzes/mocks. |
| **May update Educational Evidence?** | Yes. |
| **May update Estimated Knowledge?** | Yes. |
| **May update Estimated Mastery?** | Yes, as contributing evidence over time. |

---

#### EV-12 — Student Self-Report of Study (“I Have Studied This”)

| Aspect | Provision |
|--------|-----------|
| **Purpose** | Allow honest declaration of syllabus coverage. |
| **Reliability** | High for *declared coverage intent*; none for validated knowledge. |
| **Educational Meaning** | Study Progress declaration — Activity / Coverage, not understanding Evidence. |
| **Quality Level** | Level 0 — Administrative for knowledge claims. |
| **May update Study Progress?** | Yes — when the report *is* a Study Progress declaration. |
| **May update Educational Evidence?** | No as Educational Evidence of understanding. |
| **May update Estimated Knowledge?** | No as validated knowledge. |
| **May update Estimated Mastery?** | No as validated mastery. |

---

### 3.3 What Never Enters Educational Evidence of Understanding

The following are **not** Educational Evidence for Knowledge State, Estimated Knowledge, or Estimated Mastery (Constitution Article V §2), even if logged for product or UX reasons:

1. Mere navigation, page views, or clicks without educational outcome;  
2. System-generated recommendations, decisions, or mission artefacts (judgements/actions, not observations of knowledge);  
3. Engineering metadata, entity identifiers, warrant-display theatre, or pipeline labels;  
4. Uncorroborated marketing or coaching rhetoric;  
5. A Study Progress checkbox taken alone as proof of understanding;  
6. Time spent alone as mastery proof;  
7. Self-report alone treated as validated mastery;  
8. Mission completion alone treated as mastery or Estimated Knowledge write.

### 3.4 Hierarchy Summary Matrix

| Source | Typical Level | Study Progress | Educational Evidence (understanding) | Estimated Knowledge | Estimated Mastery |
|--------|---------------|----------------|--------------------------------------|---------------------|-------------------|
| Reading a topic | 1 | Sometimes | Yes (engagement) | Not alone | Not alone |
| Mission completion alone | 0 | Yes (coverage) | No | No | No |
| Question attempts (with outcome) | 2–3 | No alone | Yes | Contributory | Contributory |
| Question scores | 2–3 | No | Yes | Contributory | Contributory |
| Quiz results | 3 | Sometimes | Yes | Yes (contrib.) | Yes (contrib.) |
| Mock examinations | 3–4 | Sometimes | Yes | Yes | Yes (contrib.) |
| Official examinations | 4 | Sometimes | Yes | Yes | Yes (contrib.) |
| Reflection | 1 | No alone | Yes (soft) | Weakly | Weakly |
| Self-reported confidence | 1 | No | Soft only | Soft only | Soft only / never sole |
| Time spent | 0–1 | No | Weak / often no | Not alone | Not alone |
| Past-paper practice | 3–4 | Sometimes | Yes | Yes | Yes (contrib.) |
| Self-report “I studied this” | 0 | Yes | No | No | No |

---

## 4. Evidence Quality Levels

Quality Levels translate Constitution Article V §3 ranks into an implementation-independent ladder of **what educational conclusions may be supported**. They define claim lawfulness, not numerical weights.

| This Model | Constitutional Rank (EGI-001 Art. V §3) | Epistemic class |
|------------|------------------------------------------|-----------------|
| Level 0 — Administrative | Beneath Rank E / non-evidence for understanding | Action, coverage, telemetry |
| Level 1 — Engagement | Rank E (and Rank D soft signals) | Exposure, engagement, subjective soft |
| Level 2 — Practice | Rank C (guided / partial objectivity) | Guided performance, light outcome records |
| Level 3 — Assessment | Rank B | Structured objective practice |
| Level 4 — High-confidence Assessment | Rank A | High-stakes / exam-like objective performance |

### Level 0 — Administrative

**Nature.** Closing of work, declarations of coverage, scheduling artefacts, and non-outcome telemetry.

**May support:**

- Study Progress and Learning Progress narration;  
- Mission lifecycle status;  
- UX continuity and next-step planning under Learning Mode.

**Must not support:**

- Estimated Knowledge as validated understanding;  
- Estimated Mastery or “Mastered” language;  
- Factual Known / Strong / Weak topic labels from this level alone.

### Level 1 — Engagement

**Nature.** Reading completion, attributable time-on-task, session length, reflection, felt confidence, and similar exposure or subjective soft signals.

**May support:**

- Weak Evidence entries that document engagement or metacognition;  
- Cautious readiness / pace factors;  
- Soft calibration inputs when estimation is already Evidence-grounded at higher levels;  
- Advisory honesty (“you have spent time here”; “you reported low confidence”).

**Must not support:**

- High Estimated Mastery language;  
- Strong factual attainment claims;  
- Sole succession into Knowledge State as if assessment had occurred.

### Level 2 — Practice

**Nature.** Guided drills, partially scored exercises, attempt outcomes with incomplete objectivity, mixed practice with outcome records.

**May support:**

- Provisional Estimated Knowledge refinements framed as estimates;  
- Early, cautious Estimated Mastery appearance only after **accumulation** of practice outcomes (still provisional);  
- Explainable practice-based factors in advice.

**Must not support:**

- Lasting high-certainty mastery from a single practice bout;  
- Treating guided practice as official examination equivalence;  
- Overwriting Study Progress meaning with competence language.

### Level 3 — Assessment

**Nature.** Quizzes with known keys, scored mission assessments, timed practice sets with measured accuracy, structured mock segments under reliable scoring.

**May support:**

- Material updates to Estimated Knowledge (as estimate);  
- Meaningful contribution to Estimated Mastery over accumulated assessments;  
- Readiness factors grounded in performance;  
- Honest “how you did” student language.

**Must not support:**

- Instant permanent mastery certification from one quiz;  
- Silent conversion of a passed quiz into Study Progress *unless* coverage rules explicitly say so;  
- Presentation of Level 3 results as Twin engineering theatre to the student.

### Level 4 — High-confidence Assessment

**Nature.** Official examination outcomes; mock examinations under exam-like conditions; marked past papers with reliable scoring and authentic conditions.

**May support:**

- Strongest lawful contribution to Estimated Knowledge and Estimated Mastery for attributable scope;  
- Strong readiness interpretation when combined with plan and coverage context;  
- Highest warrant for provisional strength language — still prefer estimate framing where doubt remains material.

**Must not support:**

- Blanket mastery of unattributable syllabus units;  
- Erasure of conflicting Evidence without educational rule;  
- Student checkbox “Mastered” as substitute for this Evidence.

### 4.1 Accumulation Across Levels

Higher Levels more readily justify estimate movement. Lower Levels accumulate as history but do not, by stacking engagement alone, become Level 4 warrant. Cross-level interpretation is permitted; **promotion of claim strength without higher-level Evidence is forbidden**.

### 4.2 Density Before High Language

High Estimated Mastery language requires:

1. Lawful Educational Evidence;  
2. Sufficient **quality** (typically Level 3–4 contribution);  
3. Sufficient **accumulation** over time;

not a single favourable observation, not completion, and not confidence alone.

This Model states the educational requirement. It does not define numerical thresholds.

---

## 5. Educational Inference Rules

Inference is the interpretation of Evidence into provisional educational claims. For every Quality Level, the following claim permissions bind Educational Intelligence, Twin estimation, analytics, and student-facing messaging.

### 5.1 Level 0 — Administrative

**Permitted educational claims**

- The student completed a defined unit of work (mission, session, declaration).  
- Study Progress may be complete / incomplete for a unit.  
- Today’s Mission may be finished, abandoned, or due.  
- The platform may suggest continuing learning along Current Learning Topic.

**Forbidden educational claims**

- The student knows or has mastered the topic because work was completed.  
- Estimated Knowledge or Estimated Mastery changed because of completion alone.  
- Strength labels (Known, Strong, Weak as fact) derived from administrative events.  
- Recommendations or Decisions presented as Evidence of knowledge.

### 5.2 Level 1 — Engagement

**Permitted educational claims**

- The student engaged with material (read, spent time, reflected, reported confidence).  
- Soft, explicitly subjective statements (“you reported low confidence”).  
- Cautious pace or workload observations.  
- Advice framed as suggestion, not as validated competence.

**Forbidden educational claims**

- Validated knowledge or mastery from engagement or confidence alone.  
- High Estimated Mastery language from Rank-D / Level 1 soft signals alone.  
- Absence of Engagement Evidence framed as proven weakness.  
- Time spent narrated as proof of understanding.

### 5.3 Level 2 — Practice

**Permitted educational claims**

- Provisional Estimated Knowledge informed by practice outcomes, labelled as estimate.  
- Cautious practice-performance summaries (“how you did on this drill”).  
- Early Estimated Mastery only when accumulation rules are met, still provisional.  
- Recommendations that cite practice results as factors.

**Forbidden educational claims**

- Lasting mastery certified from one guided practice episode.  
- Equating partial objectivity with official examination proof.  
- Using practice inference to invent Study Progress without coverage rules.  
- Stating factual Strong/Weak topic competence from thin Level 2 history.

### 5.4 Level 3 — Assessment

**Permitted educational claims**

- Estimated Knowledge updates grounded in structured objective results.  
- Accumulating Estimated Mastery contributions from quizzes / scored assessments.  
- Readiness factors that cite assessment performance among other lawful inputs.  
- Plain-language result narration with estimate framing for competence claims.

**Forbidden educational claims**

- Permanent mastery from a single quiz result.  
- Treating mission *completion* (Level 0) as if it were the mission *score* (Level 3).  
- Suppressing conflicting Evidence to preserve a preferred estimate narrative.  
- Student-editable “Mastered” as the store of Level 3 inference.

### 5.5 Level 4 — High-confidence Assessment

**Permitted educational claims**

- Strongest provisional understanding and mastery estimates for attributable scope.  
- Exam-oriented readiness interpretation when Evidence, coverage, and plan context agree.  
- Careful strength language only when warrant remains clear and estimates stay provisional where doubt is material.

**Forbidden educational claims**

- Transferring Level 4 warrant to topics outside attributable scope.  
- Absolute, lifelong “Finished Learning Forever” speech from one official result.  
- Using Level 4 outcomes to rewrite Study Progress history dishonestly or to erase Evidence.  
- Naming Digital Twin or pipeline internals as the student’s educational explanation.

### 5.6 Universal Inference Constraints (All Levels)

1. Inference interprets Evidence; inference does not invent Evidence.  
2. Absence of Evidence ⇒ leave Twin estimates unchanged; disclose uncertainty; do not fill with fiction.  
3. Soft signals may inform advice; they do not author verified attainment.  
4. Study Progress and Estimated Mastery remain distinct meanings forever.  
5. Educational Evidence is the only authority capable of updating Twin-owned educational states (Registry EL-005; State Authority Matrix).

---

## 6. Future Evolution

The following evidence sources are **reserved**. They may enter the hierarchy by refining this Model under constitutional process. This section does **not** define implementation, schemas, algorithms, or product timelines.

| Reserved source | Anticipated educational role (non-binding sketch) | Likely Level band |
|-----------------|---------------------------------------------------|-------------------|
| **Adaptive diagnostics** | Short checks that create clarifying Evidence when warrant is thin (Diagnostic Mode). | Typically Level 2–3 |
| **Spaced repetition** | Retention-oriented practice outcomes and schedule adherence as engagement / practice Evidence. | Typically Level 1–2 (outcomes may reach Level 3) |
| **External LMS** | Imported activity and scored results when provenance and reliability are educationally attested. | Level depends on attestation; must not default to Level 4 |
| **Question banks** | Item-level attempts and scores as structured practice Evidence. | Typically Level 2–3 |
| **Peer learning** | Collaborative study observations; ordinarily soft unless objectively scored. | Typically Level 1; rarely higher without objective scoring |
| **Tutor assessments** | Human-marked judgements; reliability depends on rubric and independence. | Typically Level 3; Level 4 only if educationally equivalent to high-stakes marking |

**Reserved-source rules:**

1. New sources must be classified into Quality Levels before they may update Estimated Knowledge or Estimated Mastery.  
2. Import and adaptive systems must not bypass Evidence → Inference → Knowledge succession.  
3. Diagnostic Mode may *create* Evidence; it must not masquerade as mastery certification or silently steal Learning Mode mission authority (Constitution Article VI).  
4. Algorithms remain out of this Model.

---

## 7. Cross References

| Document | Relationship |
|----------|----------------|
| `KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Articles III, IV.5–14, V (Evidence Constitution), VII, VIII — governing meaning |
| `EDUCATIONAL_LOGIC_REGISTRY.md` | EL-004, EL-005, EL-006, EL-007, EL-012 — operational behaviour |
| `EDUCATIONAL_STATE_AUTHORITY_MATRIX.md` | Educational Evidence as sole authority for Twin estimate updates |
| `EDUCATIONAL_INTEGRITY_PROGRAMME_BLUEPRINT.md` | EIP-002 Evidence Integrity — this Model is the design precursor |
| `EDUCATIONAL_GOVERNANCE_REVIEW_STANDARD.md` | Categories A, B, D (and related) for later verification |

---

## Document Control

| Field | Value |
|-------|-------|
| Capability | EIP-002-DESIGN |
| Next authorised step | Architecture Review |
| Forbidden next step | EIP-002 implementation without Architecture Review approval |
| Implementation status | EIP-002 operational gate: `EDUCATIONAL_EVIDENCE_AUTHORITY.md` |

**Stop.** Do not begin EIP-002 implementation from this document alone.

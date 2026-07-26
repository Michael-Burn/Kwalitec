# Obstacle Catalogue

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS002 — Learning Obstacle Model  
**Classification:** Categories of educational obstacles for IFoA preparation  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines the **catalogue of educational obstacles** Kwalitec may diagnose when genuine learning progression is blocked, stalled, uneven, or misleading.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `LEARNING_OBSTACLE_MODEL.md`
3. `../learning_coach/LEARNING_PROGRESSION_MODEL.md`
4. `../learning_coach/LEARNING_OBJECTIVES.md`
5. `../KNOWLEDGE_AND_MASTERY_EDUCATIONAL_MODEL.md` (EIP-006)
6. `../EDUCATIONAL_EVIDENCE_MODEL.md` (EIP-002)

Catalogue entries are educational meanings — not database enums, UI badges, optimiser modes, or numeric severity bands. Implementations may map storage labels onto these meanings; they may not redefine the meanings in code.

> **Obstacles are educational causes.  
> They are developed from educational principles, not implementation convenience.  
> Listing an obstacle does not author an intervention.**

---

## 1. Purpose

An expert IFoA tutor carries a mental catalogue of *why* actuarial students stop progressing: missing foundations, recognising without recalling, holding a wrong method firmly, studying in fits and starts, drowning in volume, using passive strategies, misjudging confidence, practising too little, neglecting revision, or failing exam technique.

This catalogue records those educational causes so Learning Coach diagnosis, explainability, and (downstream) interventions share one vocabulary.

---

## 2. Catalogue Principles

1. **Educational first.** Categories come from learning science and IFoA tutoring practice — not from which UI widget is easiest to build.
2. **Causes, not symptoms.** “Wrong answers” is not a catalogue entry; the *reason* wrong answers persist may be.
3. **Objective-aware.** Each obstacle typically blocks specific Learning Objectives (LO-01…LO-07); it must not collapse the ladder.
4. **Non-exclusive.** A student may face more than one obstacle on different scopes — or stacked obstacles on one scope. Prefer a **primary** diagnosis in speech.
5. **Reversible.** Obstacles are provisional; they clear or change as evidence evolves.
6. **Non-punitive.** Names describe barriers — never character.
7. **Syllabus-faithful.** Prerequisite talk must respect official curriculum order; folk “shortcuts” that invent syllabus content are unlawful.
8. **No severity scores.** Qualitative language only (mild / material / pervasive as speech cues if needed — never numeric ranks as educational law).

---

## 3. Framework Logic (Before Labels)

Before naming an obstacle, the tutor asks, in order:

| Order | Tutor question | If unclear |
|-------|----------------|------------|
| 1 | Which learning objective is failing to advance? | Withhold strong cause; stay at symptom + evidence gathering |
| 2 | Is the barrier knowledge structure (foundations / misconception) or performance form (retrieval / application / exam technique)? | Prefer structural checks before volume advice |
| 3 | Is the barrier process (strategy, cadence, overload) rather than content? | Diagnose process obstacles without inventing content gaps |
| 4 | Could soft confidence be misleading the story? | Keep confidence mismatch distinct from competence obstacles |
| 5 | Is warrant dense enough to name a cause? | Explicit insufficient warrant — not a guessed LOB |

Examples such as “Prerequisite Gap” are **illustrative names** for causes produced by this logic. Binding meanings are the definitions below.

---

## 4. Obstacle Catalogue

Each entry records: educational meaning, typical symptoms (not the diagnosis), primary objectives blocked, what it is not, and a constructive speech cue.

IDs (`LOB-XX`) exist for audit and cross-reference. They must not appear as student-facing jargon.

---

### LOB-01 — Prerequisite Gap

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Earlier syllabus foundations required for the current scope are missing, fragile, or never lawfully covered — so current understanding or application cannot advance honestly. |
| **Typical symptoms** | Persistent failure on advanced items; Reflection “I don’t know where to start”; errors that replay earlier topics; stall after jumping ahead of curriculum order. |
| **Primarily blocks** | LO-03 Understanding and LO-05 Application on the *current* scope; may also block LO-07 synthesis. |
| **Does not mean** | The student is incapable; current-topic coverage never happened; every wrong answer is a foundation gap. |
| **Speech cue** | “This topic depends on earlier ideas that still need rebuilding.” |

**Educational principle.** Professional syllabi are ordered. Teaching advanced CM1/CS1 technique on missing algebra, probability, or earlier CMP units manufactures false struggle.

---

### LOB-02 — Weak Retrieval

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | The student recognises or understands material with prompts / notes / recent study, but cannot reliably recall or reconstruct it unaided. |
| **Typical symptoms** | Strong recognition, weak closed-book production; success immediately after reading that collapses without cues; “I knew it when I saw the answer.” |
| **Primarily blocks** | LO-04 Retrieval ability; undermines LO-06 Durable retention and exam-condition LO-05/LO-07. |
| **Does not mean** | Absence of all understanding (LO-03 may still be emerging); permanent inability to learn the topic. |
| **Speech cue** | “You recognise this with support, but it isn’t coming back cleanly without prompts.” |

**Educational principle.** Exams reward production under reduced cues. Recognition theatre is not retrieval.

---

### LOB-03 — Misconception

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | A specific, stable misunderstanding of a concept or method is actively producing wrong performance — more practice without repair rehearses the error. |
| **Typical symptoms** | Repeated identical wrong method; confident wrong answers; Reflection naming a wrong rule; errors that cohere around one false idea. |
| **Primarily blocks** | Quality of LO-03 Understanding; unlocks LO-05 only after repair. |
| **Does not mean** | Random careless slips; thin exposure without a stable wrong model; every error pattern. |
| **Speech cue** | “There’s a specific misunderstanding to correct before more practice will help.” |

**Educational principle.** Volume on a wrong schema strengthens the wrong schema. Diagnosis must name the idea when warrant exists.

---

### LOB-04 — Inconsistent Study

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Study cadence is irregular enough that accumulation, spacing, and skill formation cannot establish — progress is interrupted by patternless gaps rather than planned recovery. |
| **Typical symptoms** | Bursts of coverage then long silence; Reflection about lost rhythm; Profile planning-reliability concerns; decay readings after unplanned gaps. |
| **Primarily blocks** | Sustainable LO-01→LO-05 progression; LO-06 spacing design; plan faithfulness. |
| **Does not mean** | Lawful recovery after a named interruption (see Continuity / recovery posture); one missed day as a moral failure. |
| **Speech cue** | “Your study rhythm is too uneven for learning to settle — we’ll stabilise cadence first.” |

**Educational principle.** Learning compounds through return. Chaotic contact produces familiarity theatre without durable growth.

---

### LOB-05 — Cognitive Overload

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | The educational demand of the current sitting or day exceeds what the student can process productively — too much novelty, simultaneous goals, or intensity — so learning quality collapses even when effort is present. |
| **Typical symptoms** | Rapid fatigue; many unfinished threads; Reflection “everything at once”; declining accuracy as session complexity rises; plan intensity mismatched to Profile capacity. |
| **Primarily blocks** | Efficient LO-03/LO-05 growth in-session; may masquerade as LOB-08 or LOB-03. |
| **Does not mean** | The syllabus is “too hard forever”; ordinary productive struggle on a well-scoped objective. |
| **Speech cue** | “We’re asking for too much at once — we’ll narrow the focus so understanding can form.” |

**Educational principle.** Working memory is limited. Overload produces activity without encoding.

---

### LOB-06 — Ineffective Study Strategies

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | The student invests effort in study methods that poorly match the educational objective — typically passive re-reading, highlighting, or recognition review when retrieval, worked-example fading, or exam-form practice is required. |
| **Typical symptoms** | High time-on-task with thin EC-C gains; “I studied for hours” without application improvement; preference for notes over production; LPS-S despite session volume. |
| **Primarily blocks** | Conversion of LO-01/LO-02 into LO-04/LO-05. |
| **Does not mean** | Laziness; absence of all strategy forever; that every re-read is useless (early familiarity may warrant light contact). |
| **Speech cue** | “Your effort is there — the study method isn’t producing the kind of learning the exam needs.” |

**Educational principle.** Desirable difficulties (retrieval, generation, spacing) outperform comfort strategies for professional exams.

---

### LOB-07 — Confidence Mismatch

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Felt confidence systematically diverges from performance evidence — overconfidence (false readiness) or underconfidence (warranted skill unseen by the student). |
| **Typical symptoms** | Soft “I know this” with weak EC-C; or strong EC-C with persistent “I can’t do this”; LPS-I confidence-vs-performance conflict. |
| **Primarily blocks** | Honest self-regulation toward LO-03–LO-07; elevates false LO-07 risk when overconfident. |
| **Does not mean** | Soft signals are worthless (they remain Level-1 calibration); competence is defined by confidence. |
| **Speech cue** | “Your confidence and your practice results don’t match yet — we’ll align them with evidence.” |

**Educational principle.** Calibration protects exam decisions. Confidence is not competence; despair is not diagnosis of incapacity.

---

### LOB-08 — Insufficient Practice

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Coverage or familiarity has advanced, but attributable practice volume or variety on the target scope is too thin for application evidence to accumulate. |
| **Typical symptoms** | Rising LO-01 with empty EC-C; “I understand when I read” without question trails; LPS-1 stuck when practice was expected; Reflection avoiding questions. |
| **Primarily blocks** | LO-05 Application; supporting LO-03 warrant. |
| **Does not mean** | Foundations are sound (check LOB-01/LOB-03 first when error patterns suggest structure); more volume cures misconception. |
| **Speech cue** | “You’ve covered the ideas — we don’t yet have enough practice evidence on them.” |

**Educational principle.** Actuarial competence is shown in performance. Reading alone rarely authorises application claims.

---

### LOB-09 — Revision Neglect

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Earlier scope that once showed promise is not being returned to — spacing and revision are absent or chronically deferred — so durable retention and exam synthesis cannot form. |
| **Typical symptoms** | Coverage-heavy, spacing-light trails; approaching sitting with thin EC-E; LPS-5 without return tests; protected revision windows repeatedly skipped. |
| **Primarily blocks** | LO-06 Durable retention; contributes to unlawful LO-07 speech risk. |
| **Does not mean** | First-pass learning should stop forever; one delayed return equals permanent loss. |
| **Speech cue** | “We’re moving forward without returning — knowledge needs revisiting to hold for the exam.” |

**Educational principle.** Durability is tested by return. Neglect of revision produces brittle preparation.

---

### LOB-10 — Exam Technique Deficiencies

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Topic knowledge may be emerging, but performance under exam-like conditions fails for process reasons: timing, structure, notation discipline, question selection, or multi-topic switching — not primarily missing content. |
| **Typical symptoms** | Untimed success, timed collapse; incomplete papers; method marks lost despite correct idea; EC-D weakness with fair EC-C on isolated items. |
| **Primarily blocks** | LO-07 Exam readiness contributions; stress-tests LO-05 under exam form. |
| **Does not mean** | All mock difficulty is technique (content gaps may co-exist); a single hard mock brands permanent failure. |
| **Speech cue** | “The ideas are starting to show — exam technique still needs deliberate practice.” |

**Educational principle.** IFoA sittings reward method, time, and paper craft. Content-only coaching leaves technique debt unpaid.

---

### LOB-11 — Fragile Durability (Spacing Failure)

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Same-day or short-delay performance is acceptable, but command weakens materially on spaced return — learning is present yet not durable. |
| **Typical symptoms** | Strong EC-C soon after study; weak EC-E after delay; LPS-I immediate-vs-spaced; Reflection “I had it last week.” |
| **Primarily blocks** | LO-06 Durable retention; warns against overstating LO-03–LO-05. |
| **Does not mean** | The student never understood; permanent amnesia; equivalent to LOB-09 when returns were never scheduled (neglect vs failed return when scheduled). |
| **Speech cue** | “It works soon after study, but it fades on return — we’ll rebuild so it holds.” |

**Educational principle.** Spacing is the durability test. Immediate success without return cannot claim lasting knowledge.

**Relation to LOB-09.** Revision Neglect is *absence of return design*. Fragile Durability is *failed or weak outcome when return occurs*. They may co-occur; diagnosis must say which.

---

### LOB-12 — Coverage Ahead of Understanding

| Aspect | Provision |
|--------|-----------|
| **Educational meaning** | Syllabus contact is advancing faster than comprehension and application warrant — coverage theatre outruns genuine learning, creating false readiness risk. |
| **Typical symptoms** | Rapid LO-01 with empty/thin LO-03–LO-05; LPS-1 accelerating; plan pressure to “finish the notes”; soft confidence from having “seen it all.” |
| **Primarily blocks** | Honest conversion into LO-03/LO-05; elevates false LO-07 risk. |
| **Does not mean** | Coverage is worthless; the student should never first-pass; every fast reader has this obstacle. |
| **Speech cue** | “Coverage is ahead of understanding — we’ll consolidate before covering more.” |

**Educational principle.** Finishing the CMP is not finishing the learning. Pace must serve understanding, not calendar theatre alone.

---

## 5. Catalogue Map to Learning Objectives

| Obstacle | LO-01 | LO-02 | LO-03 | LO-04 | LO-05 | LO-06 | LO-07 |
|----------|-------|-------|-------|-------|-------|-------|-------|
| LOB-01 Prerequisite Gap | may need rebuild | — | **blocks** | — | **blocks** | — | risk |
| LOB-02 Weak Retrieval | — | often intact | may be emerging | **blocks** | weakens | weakens | weakens |
| LOB-03 Misconception | — | — | **blocks quality** | — | **blocks** | — | risk |
| LOB-04 Inconsistent Study | unstable | thin | delayed | delayed | delayed | delayed | risk |
| LOB-05 Cognitive Overload | noisy | — | **blocks efficiency** | — | **blocks efficiency** | — | — |
| LOB-06 Ineffective Strategies | effort without gain | inflated | delayed | **blocks** | **blocks** | — | — |
| LOB-07 Confidence Mismatch | — | miscalibrated | speech risk | — | speech risk | — | **false readiness risk** |
| LOB-08 Insufficient Practice | may be fine | may be fine | thin warrant | thin | **blocks** | — | — |
| LOB-09 Revision Neglect | may look complete | — | overstated | untested | overstated | **blocks** | **risk** |
| LOB-10 Exam Technique | — | — | may be OK | — | form-limited | — | **blocks** |
| LOB-11 Fragile Durability | — | — | overstated | weak return | overstated | **blocks** | risk |
| LOB-12 Coverage Ahead | **advancing** | inflated | **lags** | lags | **lags** | — | **risk** |

“Blocks” / “risk” are educational readings — not scores.

---

## 6. Downstream Intervention Traceability (Non-Collapsing Map)

Interventions remain a **separate layer**. This table is traceability guidance only — it does not author automatic selection or redefine LI meanings.

| Primary obstacle | Typical first-line interventions (MS003) |
|------------------|------------------------------------------|
| Insufficient warrant / Conflicting | LI-00 Evidence Gathering |
| LOB-01 Prerequisite Gap | LI-04 Prerequisite Rebuilding; sometimes LI-07 |
| LOB-02 Weak Retrieval | LI-03 Retrieval Reinforcement; LI-06 Spacing Adjustment |
| LOB-03 Misconception | LI-07 Misconception Correction; then LI-01 / LI-13 |
| LOB-04 Inconsistent Study | LI-10 when recovering; else cadence via Daily Coach / LI-12 if envelopes break |
| LOB-05 Cognitive Overload | LI-09 Consolidation; narrower session design; LI-10 if recovery |
| LOB-06 Ineffective Strategies | LI-08 Method / Strategy Coaching (incl. worked-example emphasis) |
| LOB-07 Confidence Mismatch | LI-11 Confidence Recalibration; LI-02/LI-03 as evidence anchors |
| LOB-08 Insufficient Practice | LI-02 Targeted Question Practice; LI-01 / LI-13 as support |
| LOB-09 Revision Neglect | LI-06 Spacing Adjustment; LI-14 Revision Restructuring; LI-09 if first-pass must pause |
| LOB-10 Exam Technique | LI-08 Method Coaching; LI-13; LI-05 careful challenge under exam form |
| LOB-11 Fragile Durability | LI-06 + LI-03; LI-14 if return design is poor |
| LOB-12 Coverage Ahead | LI-09 Consolidation Before Progression; LI-01/LI-03 |

If no LOB can be named, the lawful response is evidence gathering (LI-00) — not picking an LI “because something must be recommended.”

---

## 7. What This Catalogue Explicitly Excludes

Not educational obstacles in this Model’s sense (may be real life factors, but are not LOB diagnoses here):

- character judgements (“lazy”, “not cut out for actuarial work”);
- opaque “low engagement scores”;
- product bugs or UX friction (operational — escalate separately);
- syllabus dislike as a substitute for educational cause;
- sitting date proximity as itself an obstacle (calendar pressure may *reveal* false readiness; it is not LOB-10 by itself).

---

## 8. Cross References

| Document | Relationship |
|----------|--------------|
| `LEARNING_OBSTACLE_MODEL.md` | Constitutional doctrine |
| `OBSTACLE_DIAGNOSIS.md` | How to choose among catalogue entries |
| `OBSTACLE_EVIDENCE.md` | Evidence that supports each diagnosis |
| `OBSTACLE_EXPLAINABILITY.md` | How to speak catalogue meanings |
| `../learning_coach/LEARNING_OBJECTIVES.md` | Objectives blocked |
| `../learning_interventions/INTERVENTION_CATALOGUE.md` | Downstream responses (MS003 governing) |
| `../learning_coach/LEARNING_INTERVENTIONS.md` | Compatibility pointer to MS003 |
| `../learning_coach/LEARNING_PROGRESSION_STATES.md` | Postures that invite diagnosis |

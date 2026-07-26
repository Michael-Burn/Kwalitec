# Obstacle Diagnosis

**Programme:** VI — Workstream 3 — Learning Coach  
**Milestone:** MS002 — Learning Obstacle Model  
**Classification:** How an expert tutor differentiates educational causes from symptoms  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how Kwalitec differentiates among educational causes** when diagnosing learning obstacles.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `LEARNING_OBSTACLE_MODEL.md`
3. `OBSTACLE_CATALOGUE.md`
4. `OBSTACLE_EVIDENCE.md`
5. `../learning_coach/LEARNING_EVIDENCE_MODEL.md`
6. `../learning_coach/LEARNING_PROGRESSION_STATES.md`
7. `../EDUCATIONAL_EVIDENCE_MODEL.md` (EIP-002)
8. `../student_profile/STUDENT_EDUCATIONAL_PROFILE.md`

> **Diagnosis interprets evidence.  
> It does not invent evidence.  
> It does not author interventions.  
> No numerical diagnostic scoring is defined here.**

---

## 1. Purpose

An expert IFoA tutor faced with struggle does not pick the first plausible label. The tutor asks what was observed, what else could explain it, how confident the explanation is, and what further evidence would settle the question.

This document records that differentiation discipline so Learning Coach obstacle diagnoses remain educationally honest.

---

## 2. Diagnosis Principles

1. **Symptom first, cause second.** Record what is observable before naming a LOB.
2. **One primary cause in speech.** Multiple obstacles may exist; student-facing diagnosis prefers a primary with optional secondary.
3. **Alternative explanations are mandatory.** Every diagnosis must survive at least one rival reading.
4. **Confidence is qualitative.** Use postures in §4 — never percentages or point scores.
5. **Silence beats stretch.** Prefer insufficient warrant over a fashionable LOB.
6. **Objective specificity.** Name which Learning Objective is failing; do not diagnose “bad at CM1” as a cause.
7. **Structure before volume.** When patterns suggest foundations or misconception, do not default to “more practice.”
8. **Process vs content.** Cadence, strategy, overload, and exam technique are distinct from missing ideas.
9. **Non-punitive.** Diagnostic language describes barriers — never character.
10. **Intervention stays downstream.** Completing diagnosis authorises — but does not itself select — an LI response.

---

## 3. Diagnostic Procedure (Educational)

The tutor follows this order. Implementations may later encode equivalents; they may not skip educational steps.

| Step | Action | Output |
|------|--------|--------|
| 1 | Establish syllabus **scope** | Topic / unit / domain under concern |
| 2 | Read **progression posture** (LPS) | Stall, inconsistency, decay, thin warrant, false readiness, etc. |
| 3 | Name **symptoms** (observable patterns) | What is going wrong on the surface |
| 4 | Identify which **learning objectives** are not advancing | LO-01…LO-07 mapping |
| 5 | List **candidate obstacles** from the Catalogue | Shortlist of LOB-XX |
| 6 | For each candidate, test **observable evidence**, **alternatives**, and **confidence** | Per §5 profiles |
| 7 | Select **primary diagnosis** or **insufficient warrant** | Explicit LOB or gather-evidence posture |
| 8 | Only then allow **intervention** recommendation | Downstream LI layer |

Skipping from step 2 or 3 directly to an intervention is unlawful.

---

## 4. Diagnostic Confidence Postures (Non-Numeric)

| Posture | Educational meaning | Lawful speech |
|---------|---------------------|---------------|
| **Insufficient warrant** | Trail too thin or too ambiguous to name a cause | “Too early to diagnose the barrier — we need clearer evidence.” |
| **Provisional** | Plausible primary cause; alternatives still live | “The leading explanation looks like… — still provisional.” |
| **Supported** | Multiple agreeing observations; rivals weakened | “Evidence consistently points to…” |
| **Conflicting** | Rival causes remain similarly plausible | “Two explanations still fit — we’ll gather evidence that distinguishes them.” |

Rules:

- Never convert these postures into scores, weights, or traffic-light maths in this Model.
- **Supported** still remains provisional in the constitutional sense (estimates, not eternal facts).
- **Conflicting** forbids picking a LOB for coaching convenience; evidence gathering or dual-hypothesis speech is required.
- Soft signals alone may colour **Provisional** at most — they may not author **Supported** for content/structure obstacles.

---

## 5. Per-Obstacle Differentiation Profiles

For each catalogue obstacle: observable evidence that *suggests* it, strong alternative explanations, when confidence may rise, and when additional evidence is required.

---

### LOB-01 — Prerequisite Gap

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Errors that replay earlier syllabus ideas; inability to begin multi-step items; Reflection that early topics feel foreign; curriculum-order jump in lived study; stall on advanced scope after thin earlier EC-C. |
| **Alternative explanations** | LOB-03 Misconception on *current* idea (not earlier); LOB-08 Insufficient Practice on current scope; LOB-05 Overload; LOB-10 Exam technique under time; LOB-11 after a break (rust vs never-learned). |
| **Confidence may become Supported when** | Patterned foundation errors recur across sessions **and** targeted earlier-scope checks are weak **and** current-scope teaching without foundations repeatedly fails. |
| **Require additional evidence when** | Only one hard sitting exists; errors are mixed/random; earlier scope was never returned to after a long break (test rust vs gap); soft “I never got Chapter X” without performance trail. |

**Differentiation cue.** If rebuilding the earlier topic unlocks the current one in tutor reasoning, prefer LOB-01. If the earlier topic is sound but a wrong *current* rule repeats, prefer LOB-03.

---

### LOB-02 — Weak Retrieval

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Open-book / prompted success with closed-book failure; recognition quizzes better than production; collapse when cues removed; “I knew it when I saw the solution.” |
| **Alternative explanations** | LOB-03 (wrong schema produced fluently); LOB-08 (almost no production attempts); LOB-11 (retrieval OK same-day, fails after spacing — durability, not cue-dependence alone); LOB-06 (never practised retrieval). |
| **Confidence may become Supported when** | Multiple sessions show the prompt-vs-production gap on the same scope with fair contact history. |
| **Require additional evidence when** | Student has never attempted unaided recall; only recognition items exist; fatigue/overload confounds a single closed-book try. |

**Differentiation cue.** Weak retrieval is about **cues**. Fragile durability (LOB-11) is about **time**. Both can co-exist; say which the trail emphasises.

---

### LOB-03 — Misconception

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Repeated identical wrong method; coherent false rule across items; confident incorrect answers; Reflection articulating the wrong idea; repair attempts that only work after explicit correction. |
| **Alternative explanations** | Careless slips / LOB-05 overload; LOB-01 missing foundation that *looks* like a wrong rule; LOB-10 notation/method-mark process without conceptual error; LOB-08 thin sampling that looks patterned by chance. |
| **Confidence may become Supported when** | The same false idea appears across different item surface forms **and** the student can state the wrong rule **or** performance flips after conceptual repair (as later evidence). |
| **Require additional evidence when** | Errors are heterogeneous; only one item failed; tutor cannot name the putative misconception; soft self-blame without a stable wrong model. |

**Differentiation cue.** Misconception is a **stable wrong model**. Random error is not. Missing prerequisite is an **absent** model for earlier ideas.

---

### LOB-04 — Inconsistent Study

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Irregular session cadence; long unplanned gaps; burst-then-silence coverage; Profile planning-reliability concerns; Continuity notes of disrupted rhythm without a single recovery plan. |
| **Alternative explanations** | Lawful recovery after named interruption (not LOB-04); LOB-05 overload causing abandoned sessions; LOB-09 revision neglect inside otherwise steady first-pass; LOB-07 despair reducing appearance. |
| **Confidence may become Supported when** | Multiple cycles of burst/gap appear **and** progression stalls despite occasional intense effort **and** gaps are unplanned rather than Continuity-governed recovery. |
| **Require additional evidence when** | One missed week after illness (prefer Continuity / LOB-11 rust); calendar was always unrealistic (may escalate plan — not solely LOB-04). |

**Differentiation cue.** Inconsistency is about **rhythm**. Revision neglect is about **not returning to prior scope** even when cadence exists. Recovery-respecting rebuild is lawful after a named break.

---

### LOB-05 — Cognitive Overload

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Performance decline as simultaneous goals rise; unfinished multi-thread sessions; Reflection “too much at once”; accuracy worse on stacked novelty; intensity mismatched to Profile capacity. |
| **Alternative explanations** | LOB-01/LOB-03 content barriers misread as overload; LOB-06 passive methods causing fatigue without encoding; LOB-04 abandoned sessions for life reasons; ordinary productive struggle on a well-scoped hard item. |
| **Confidence may become Supported when** | Narrowing scope restores learning quality across sittings **or** the day plan repeatedly stacks incompatible objectives against Profile limits. |
| **Require additional evidence when** | Only preference for easier work is voiced; single tough mock without process data; content gaps explain the same failures. |

**Differentiation cue.** Overload improves when **demand is reduced**. Content obstacles improve when **ideas are repaired**, even at moderate demand.

---

### LOB-06 — Ineffective Study Strategies

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | High time-on-task with thin EC-C gains; predominant re-reading/highlighting/recognition; avoidance of production; LPS-S despite session volume; Reflection describing passive methods. |
| **Alternative explanations** | LOB-08 (strategy OK but absolute practice still thin); LOB-03 (active practice rehearsing a wrong method); LOB-05 (method secondary to overload); LOB-01 (foundations block any method). |
| **Confidence may become Supported when** | Method description is clear **and** comparable peers/scope would expect gains **and** production-shaped sessions have barely been tried. |
| **Require additional evidence when** | Practice volume is already high and patterned errors suggest LOB-03/LOB-01; student cannot yet describe how they study. |

**Differentiation cue.** Strategy obstacles respond to **changing how**; insufficient practice responds to **doing attributable practice at all**; misconception responds to **repairing what**.

---

### LOB-07 — Confidence Mismatch

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Persistent EC-B vs EC-C conflict; soft certainty with weak outcomes (overconfidence); strong outcomes with persistent incapacity narrative (underconfidence); false readiness speech near sitting. |
| **Alternative explanations** | True LOB-02/LOB-11 (confidence correctly low); true competence with temporary nerves (not chronic mismatch); LOB-10 (confidence about content OK, exam form fails). |
| **Confidence may become Supported when** | Divergence repeats across sessions after feedback **and** soft signals dominate the student’s story relative to performance trail. |
| **Require additional evidence when** | One emotional day; soft signal only with no performance trail (cannot claim overconfidence about untested skill); cultural hedging in Reflection language. |

**Differentiation cue.** Mismatch is about **calibration**. Do not “fix” underconfidence by inventing mastery speech; do not “fix” overconfidence by shaming — align with evidence.

---

### LOB-08 — Insufficient Practice

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Adequate or rising coverage (EC-A) with sparse EC-C; familiarity without question trails; Reflection avoidance of questions; LPS-1 when practice was educationally expected. |
| **Alternative explanations** | LOB-06 (some practice exists but wrong kind); LOB-01/LOB-03 (practice exists but foundations/misconceptions block gains — not a volume problem); LOB-05 (practice abandoned mid-set); LOB-12 (coverage racing ahead). |
| **Confidence may become Supported when** | Contact history is honest **and** attributable practice observations remain thin **and** structural rivals are weakened. |
| **Require additional evidence when** | Practice was attempted and failed patterned ways (investigate LOB-01/03 first); “I did questions” without recorded outcomes (observation gap, not proven volume). |

**Differentiation cue.** Ask: *Is practice missing, mistyped, or blocked by structure?* Only the first is LOB-08 as primary.

---

### LOB-09 — Revision Neglect

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Forward coverage without scheduled returns; thin EC-E by design; skipped revision windows; approaching sitting with spacing-light trail; LPS-5 without return tests. |
| **Alternative explanations** | LOB-11 (returns happened and failed); LOB-04 (no stable cadence for anything); LOB-12 (first-pass rush); plan that lawfully deferred revision (temporary — re-check later). |
| **Confidence may become Supported when** | Multiple earlier scopes lack any return design **and** exam horizon makes retention claims material. |
| **Require additional evidence when** | Returns exist but outcomes are weak (LOB-11); student is still early first-pass with plan-protected later revision. |

**Differentiation cue.** Neglect = **no return**. Fragile durability = **return failed**.

---

### LOB-10 — Exam Technique Deficiencies

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Untimed/isolated success vs timed/paper collapse; incomplete scripts; lost method marks with right idea; poor question selection; multi-topic switching failures; EC-D weakness with fair item-level EC-C. |
| **Alternative explanations** | LOB-01/LOB-03 content gaps exposed by mocks; LOB-02 retrieval collapse under stress; LOB-05 overload in exam conditions; LOB-07 panic narrative without process data. |
| **Confidence may become Supported when** | Process faults are identifiable across exam-like sittings **and** content checks on the same ideas are comparatively stronger outside exam form. |
| **Require additional evidence when** | Only one difficult mock exists; content and technique failures are entangled; no exam-like observations at all (cannot diagnose technique from notes study). |

**Differentiation cue.** Technique is **how the paper is taken**. Content obstacles are **what cannot be produced even with time and calm**.

---

### LOB-11 — Fragile Durability (Spacing Failure)

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Acceptable near-study EC-C; materially weaker EC-E after delay; LPS-I immediate-vs-spaced; Reflection “I had it last week.” |
| **Alternative explanations** | LOB-09 (never returned — cannot claim failure of return); LOB-02 (cueing issue more than time); LOB-04 long gap with total rust; LOB-01 never solid initially (immediate “success” was recognition). |
| **Confidence may become Supported when** | At least one deliberate spaced return shows decay **and** near-study performance had been encouraging on the same scope. |
| **Require additional evidence when** | No spaced return has occurred; immediate success was recognition-only; break was Continuity-governed (prefer recovery reading before branding fragility). |

---

### LOB-12 — Coverage Ahead of Understanding

| Aspect | Provision |
|--------|-----------|
| **Observable evidence** | Rapid LO-01 advance; thin LO-03–LO-05 trail; soft “I’ve seen it all”; calendar-driven note completion; LPS-1 accelerating without EC-C. |
| **Alternative explanations** | LOB-08 as pure volume (related — often co-primary); LOB-06 passive coverage methods; LOB-07 overconfidence from coverage; efficient student who *does* have practice (must not force LOB-12). |
| **Confidence may become Supported when** | Coverage metrics/activity rise while understanding/application evidence stays empty **across** recent weeks. |
| **Require additional evidence when** | Early first-pass by plan with practice scheduled next (may be lawful sequence — watch, don’t over-diagnose); practice exists and is simply unrecorded. |

---

## 6. Symptom → Cause Quick Reference

| Common symptom | Prefer investigating first | Common misdiagnosis to avoid |
|----------------|----------------------------|------------------------------|
| Getting questions wrong | Pattern → LOB-03 or LOB-01; else LOB-08/06 | “Do more questions” as diagnosis |
| “I understood it yesterday” | LOB-11 or LOB-02 | Character forgetfulness |
| Finished the notes, still can’t apply | LOB-12 + LOB-08; check LOB-06 | Instant LO-07 readiness |
| Studies for hours, no gain | LOB-06; rule out LOB-03/01 | Laziness |
| Skips days in bursts | LOB-04 vs Continuity recovery | Shame narrative |
| Panic before mocks | LOB-07 + check LOB-10/content | “Not exam material” as fact |
| Timed paper collapse | LOB-10 vs content LOBs | One mock as permanent brand |
| Feels fine, scores weak | LOB-07 overconfidence; check LOB-02/11 | Ignore soft signals entirely |
| Feels doomed, scores OK | LOB-07 underconfidence | Invent incapacity |

---

## 7. Conditions Requiring Additional Evidence (Global)

Regardless of candidate LOB, require further evidence when any of the following hold:

1. **Cold start / LPS-0** — withhold Supported diagnoses for LO-03–LO-07 barriers.
2. **Single-session trail** — Reflection may hypothesise; longitudinal LOB Supported is premature.
3. **Conflict between soft and hard signals** — prefer Conflicting or Provisional; do not let soft author Supported content causes.
4. **Entangled failures** — mock that mixes content, retrieval, and timing → Conflicting until separated.
5. **Profile contradiction** — obstacle speech that denies Profile dimensions → re-consult Profile before Supported.
6. **Missing observation class** — cannot diagnose LOB-10 without exam-like observations; cannot diagnose LOB-11 without a return; cannot diagnose LOB-08 if practice outcomes were never recorded (observation gap).

Lawful output in these cases: **Insufficient warrant** or **Conflicting**, with an explicit evidence-gathering next step — not a guessed intervention cure.

---

## 8. Diagnosis Record (Educational Minimum)

A complete educational diagnosis states:

1. **Scope** — syllabus area concerned.
2. **Symptoms observed** — surface patterns.
3. **Primary obstacle** — LOB meaning (or insufficient warrant).
4. **Objectives blocked** — which LO-01…LO-07.
5. **Confidence posture** — insufficient / provisional / supported / conflicting.
6. **Alternatives considered** — at least one rival.
7. **Evidence basis** — classes/patterns (see `OBSTACLE_EVIDENCE.md`).
8. **Intervention gate** — whether an LI recommendation is now lawful.

Omitting (3) or (8) while recommending an intervention is unlawful.

---

## 9. Integrity Boundaries

| Boundary | Lawful | Unlawful |
|----------|--------|----------|
| Differentiation | Test alternatives | First-label diagnosis |
| Confidence | Qualitative postures | Numeric diagnostic scores |
| Thin history | Insufficient warrant | Invented LOB for coaching energy |
| Intervention | After explicit diagnosis | Generic tip without LOB |
| Shame | Barrier language | Character language |
| Evidence | Cite accumulation patterns | Mint observations via diagnosis |

---

## 10. Cross References

| Document | Relationship |
|----------|--------------|
| `OBSTACLE_CATALOGUE.md` | Meanings being chosen among |
| `OBSTACLE_EVIDENCE.md` | How evidence supports/weakens each diagnosis |
| `OBSTACLE_EXPLAINABILITY.md` | How diagnosis is spoken |
| `../learning_coach/LEARNING_PROGRESSION_STATES.md` | Postures that invite diagnosis |
| `../learning_interventions/INTERVENTION_CATALOGUE.md` | Downstream after gate opens (MS003) |
| `../learning_coach/LEARNING_INTERVENTIONS.md` | Compatibility pointer to MS003 |
| `../reflection/REFLECTION_INTERPRETATION.md` | Session-level hypotheses feeding longitudinal diagnosis |

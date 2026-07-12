# Capability 3.6.2 — Student Calibration Educational Analysis

**Status:** Educational analysis only — no implementation  
**Epic:** Epic 3 — Product Integration & Experience  
**Capability:** 3.6.2 Student Calibration Educational Analysis (educational implications of Twin-birth priors preceding any Application construction)  
**Governing ADR:** [`ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md`](ADR-002-EDUCATIONAL-INTELLIGENCE-ARCHITECTURE.md)  
**Governing architecture:** [`EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md`](EDUCATIONAL_INTELLIGENCE_ARCHITECTURE.md)  
**Upstream Calibration architecture:** [`CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md`](CAPABILITY_3_6_1_STUDENT_CALIBRATION_ARCHITECTURE.md)  
**Twin law:** [`STUDENT_DIGITAL_TWIN.md`](../../STUDENT_DIGITAL_TWIN.md)  
**Companions:** [`CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_7_READINESS_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_8_DECISION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_9_RECOMMENDATION_ENGINE_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md`](CAPABILITY_2_10_MISSION_INTELLIGENCE_EDUCATIONAL_ANALYSIS.md), [`CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md`](CAPABILITY_3_2_EDUCATIONAL_EXPERIENCE_CONTRACT.md)  
**Scope:** Educational implications of Initial Student Calibration priors — **no Application Layer design, Flask, persistence, UI, algorithms, readiness calculation, confidence assignment, mastery inference, or ADR-002 redesign**

---

## Document purpose

Capability 3.6.1 established that Initial Student Calibration creates the initial Digital Twin from self-declared educational history, and that Calibration produces **structural priors only**.

This milestone analyses the **educational** meaning of those priors.

It answers:

> What is the minimum educational information required to initialise a truthful Digital Twin while preserving Educational Intelligence integrity?

It protects the binding principle:

> **Self-report establishes priors. Evidence establishes truth.**

Architectural restatement from 3.6.1 remains binding here:

> **Calibration captures history. It never reasons. Priors are not truth.**

**Non-goals of this document**

- Implementation, pseudocode, services, dataclasses, or package layouts  
- Flask routes, forms, templates, wizard UX, or copy  
- Database schemas, Alembic migrations, ORM, or Twin Persistence design  
- Redesign of ADR-002, Readiness, Decision, Recommendation, Mission, or Evidence  
- Inventing educational algorithms, readiness scores, confidence values, or mastery beliefs  
- Diagnostic assessment design (assessed baseline is a separate Evidence path)

---

# 1. Educational problem

## 1.1 Why beginner-assumption is educationally incorrect

Treating every new Study Plan as if the student is a beginner is not a harmless default. It is an educational falsehood.

A beginner-assumption Twin says, by silence:

- this student has never engaged this syllabus;  
- foundations are the only honest starting place;  
- prior exam attempts, Core Reading, and syllabus coverage do not exist;  
- the first recommendation may safely restart the journey from zero.

That may be true for some students. It is false for many actuarial candidates who:

- completed Core Reading outside the product;  
- previously sat the paper;  
- are revising after a pass/fail or deferred sitting;  
- return after a long gap with real prior exposure and uncertain retention.

Educational Intelligence that begins from an implicit zero-knowledge birth therefore:

1. **Misrepresents the learner** — the Twin denies known educational history.  
2. **Misdirects the first recommendation** — foundations-first guidance can contradict declared reality.  
3. **Erodes trust** — returning candidates recognise “start from scratch” as product ignorance, not educational care.  
4. **Creates pressure to fake Mid readiness** — the wrong fix for cold start is inventing preparedness theatre rather than capturing honest priors.

The educational problem is therefore not “missing a feature.” It is **dishonest Twin birth**.

Cold-start honesty about *absence of Evidence* remains correct. Beginner-assumption about *known history* does not.

## 1.2 Four learner postures that require different initial Twins

Calibration must distinguish educational *posture at birth*. These are not readiness bands. They are different prior structures — different answers to “what history and objective did this student declare?”

### First-time learner

**Educational meaning:** The student declares they are beginning this paper / syllabus for the first time — little or no prior study of this scope.

**Initial Twin character:**

- Empty or near-empty educational-history priors.  
- Explicit beginner / first-time declared posture.  
- Goals anchored to first sit (or equivalent first-attempt objective).  
- Belief domains that Calibration does not initialise remain empty.

**Why distinct:** Foundations-first guidance is educationally coherent *when declared*. The Twin must record that coherence as declared posture, not as inventing Mid mastery later “to feel personalised.”

### Returning learner

**Educational meaning:** The student declares prior study of this paper / syllabus without necessarily framing the present work as revision-only or as a repeat exam attempt. Exposure exists; Evidence does not yet exist inside the product.

**Initial Twin character:**

- Non-empty exposure / coverage priors where declared (previous study, Core Reading, completed sections).  
- Returning / history-declared posture.  
- Empty Memory, Behaviour, Predictions — retention and habits are unknown.  
- Thin warrant on every history prior.

**Why distinct:** Absolute beginner assumptions falsify declared exposure. Equally, treating declared exposure as mastery falsifies educational truth. The Twin must hold *declared history without assessed belief*.

### Revision student

**Educational meaning:** The student declares that Core Reading (or equivalent coverage) is largely complete and the present objective is revision, consolidation, or finishing remaining sections — not first exposure.

**Initial Twin character:**

- Stronger declared coverage priors (Core Reading / completed sections) than a generic returning learner.  
- Goals posture oriented to revision / remaining gaps — still not readiness.  
- No mastery map, no retention schedule, no weak-topic list invented from declaration.

**Why distinct:** Revision is an *objective posture*, not a preparedness claim. A revision Twin that still forces “learn foundations as if unread” contradicts declared coverage. A revision Twin that skips diagnostics because “they said they finished Core Reading” converts self-report into mastery. Both fail Educational Intelligence integrity.

### Repeat exam candidate

**Educational meaning:** The student declares one or more previous attempts at the sitting / paper. The educational past includes attempt history; the present objective is typically re-sit or another attempt.

**Initial Twin character:**

- Attempt-history priors (count / sitting labels / declared outcome only if stated as history).  
- Goals anchored to intended sitting and re-attempt objective.  
- No invented mock scores, pass probabilities, or Performance summaries from declaration alone.  
- Prior attempt history must not erase the need for Evidence about current strength and weakness.

**Why distinct:** Attempt history changes educational framing (re-sit urgency, prior exam-condition exposure as *declared fact*) without proving current readiness. A Twin that ignores attempts treats a re-sitter as a first-timer. A Twin that invents Performance beliefs from “I sat before” pretends observation occurred.

## 1.3 Why all four require different initial Twins

| Posture | Educational starting claim | Wrong Twin if collapsed into beginner | Wrong Twin if collapsed into “ready” |
|---|---|---|---|
| First-time learner | Declared empty history | (Correct empty-history path) | Fabricated Mid theatre |
| Returning learner | Declared exposure without assessed mastery | Foundations-only falsehood | Coverage → mastery collapse |
| Revision student | Declared coverage + revision objective | Re-teaching unread material as default truth | Skipping Evidence because “revision” |
| Repeat exam candidate | Declared attempt history + re-sit objective | Ignoring attempt lineage | Attempt → Performance / pass-probability invention |

Different initial Twins are required because Educational Intelligence’s first lawful inputs differ:

- what history was declared;  
- what objective frames the Goal;  
- which priors exist under thin warrant;  
- which unknowns remain deliberately empty.

They do **not** differ because Calibration computed four readiness levels. Posture is structural honesty at birth — not educational judgement.

Governing restatement:

> **One beginner default for everyone is educationally false. Four postures with the same Evidence-backed beliefs would also be false. Different priors, same warrant humility.**

---

# 2. Educational philosophy

## 2.1 Self-declared history vs observed educational evidence

| | Self-declared history | Observed educational evidence |
|---|---|---|
| **Source** | What the student claims about their past and objective | What the product observes in study / assessment events |
| **Authority** | Calibration at Twin birth | Learning Evidence → Twin Update Pipeline |
| **Epistemic status** | Prior / claim | Observed fact (within measurement limits) |
| **Warrant** | Thin / `self_declared` | Densifies with repeated, syllabus-mapped Evidence |
| **May initialise** | Identity / Goals anchors + history prior markers | Knowledge, Memory, Behaviour, Performance beliefs |
| **May not become** | Mastery, readiness, predicted marks | Fabricated by Calibration |

These are fundamentally different because they answer different educational questions:

- Self-declaration answers: *What does the student say happened before we met?*  
- Evidence answers: *What did we observe while they studied with us?*

A truthful educational system may begin from the first. It may only *believe* with warrant from the second.

## 2.2 Why they are fundamentally different

1. **Agency of observation** — Self-report is the student’s narrative. Evidence is the product’s observation of learning events. Narratives can be incomplete, optimistic, forgotten, or strategically framed. Observation can be sparse, noisy, or narrow — but it is still observation, not autobiography.

2. **Falsifiability inside the product** — Declared Core Reading cannot be verified by Calibration. Quiz outcomes, mission completions, and mocks can be recorded as Evidence and later contradicted by further Evidence. Educational truth inside Kwalitec is Evidence-sovereign precisely because it can evolve under observation.

3. **Audit spine** — Learning Evidence is append-only educational history the system can defend. Calibration provenance is lineage of *claims*. Collapsing claims into Evidence falsifies the audit spine and teaches every downstream domain that sparse declaration equals assessed Performance.

4. **Educational function** — Priors prevent dishonest beginner assumptions. Evidence enables belief evolution. Using either for the other’s job breaks integrity: Evidence alone cannot know off-product history; priors alone cannot certify mastery.

## 2.3 Why self-report should never imply mastery

Mastery is an educational belief about what the student can *do now* with a curriculum entity. It is uncertain, evidence-weighted, and supersedable.

Self-report of history answers a different question: *Did the student declare prior engagement?*

Therefore:

- “I completed Core Reading for Section X” ≠ mastery of Section X.  
- “I finished these syllabus sections” ≠ weighted coverage score or mastery map.  
- “I studied this paper before” ≠ durable Knowledge belief.  
- “I sat previously” ≠ current exam-condition Performance.  
- “I am revising” ≠ High readiness.

Equating declaration with mastery creates four educational failures:

1. **False certainty** — thin warrant is presented as dense belief.  
2. **Decision corruption** — next actions skip foundations or diagnostics without Evidence authority.  
3. **Readiness theatre** — preparedness narratives claim Mid/High from autobiography.  
4. **Irrecoverable trust debt** — when Evidence later contradicts declaration, the product appears to have lied rather than to have held an honest prior.

Governing principle (binding for this analysis):

> **Self-report establishes priors. Evidence establishes truth.**

Extended:

> **Priors may change where Educational Intelligence *starts looking*. Only Evidence may change what Educational Intelligence *believes*.**

---

# 3. Minimum calibration information

## 3.1 What “minimum closed information set” means

Before Educational Intelligence can make its **first recommendation** without beginner-assumption falsehood, Calibration must supply the smallest closed set of self-declared facts that:

1. scopes the Twin to a real syllabus / exam;  
2. records whether history is empty or non-empty;  
3. records the educational objective posture;  
4. anchors the intended sitting / Goal;  
5. attaches thin-warrant provenance to every history prior;  
6. leaves mastery, readiness, and related unknowns intentionally empty.

“Minimum” is educational, not commercial: collect enough to stop lying about history; collect nothing that pretends to be judgement.

## 3.2 Required minimum set

| Item | Educational necessity | Lawful prior meaning |
|---|---|---|
| **Authorised student identity + curriculum / exam scope** | Without these, no Twin birth is educationally meaningful | Identity anchors — not beliefs |
| **Previous study (coarse)** | Distinguishes first-time vs returning exposure | Exposure prior — not mastery |
| **Core Reading completed (declared)** | Distinguishes unread vs declared coverage for actuarial papers | Coverage prior — not retention or readiness |
| **Previous attempts** | Distinguishes first sit vs repeat candidate | Attempt-history prior — not Performance summary |
| **Completed syllabus sections (canonical ids)** | Locates declared syllabus position without free-text invention | Declared-complete markers — not mastery map |
| **Study objective** | Distinguishes first sit / revise / re-sit / finish remaining | Goals posture — not preparedness |
| **Intended sitting** | Makes Goals and later Readiness sitting-relative | Sitting anchor — not completion forecast |
| **Beginner declaration (when history is empty)** | Makes empty-history posture explicit rather than silent | Explicit empty priors — not Mid empty theatre |

These items align with the closed educational-history field set in Capability 3.6.1 §4.2. This analysis does not expand that set. It confirms educational necessity of the closed set for truthful Twin birth.

Optional product sitting facts already collected by Study Plan (e.g. declared study capacity) may structurally inform Goals capacity. They are not required to establish educational-history honesty, and must not become Behaviour adherence or burnout judgement.

## 3.3 How the minimum set enables the first recommendation

Educational Intelligence’s first recommendation remains owned by Decision → Recommendation. Calibration does not select it.

What Calibration enables is a **truthful input Twin**:

- first-time empty-history Twin → first recommendation may honestly favour foundations / evidence-creating actions under cold-start warrant;  
- returning / revision / repeat Twin → first recommendation must not assume unread syllabus when coverage or attempts were declared — yet must still respect thin warrant and prefer Evidence creation where beliefs are empty.

Without the minimum set, the first recommendation can only choose between:

- beginner falsehood, or  
- invented Mid preparedness.

Both violate Educational Intelligence integrity.

## 3.4 What should NOT be collected at Calibration

| Must not collect (as Calibration authority) | Why |
|---|---|
| Mastery percentages / topic mastery ratings treated as birth truth | Implies mastery from self-report |
| Readiness %, preparedness bands, “how ready do you feel?” as readiness | Readiness is Educational Intelligence judgement; self-report Confidence is separable and not this capability |
| Predicted marks / pass probability / “chance of passing” | Predictions / forecasting — not history capture |
| Detailed weak-topic lists invented by the student as assessed truth | Weaknesses are Evidence-discovered; free-form weakness claims risk mastery-by-another-name |
| Confidence ratings smuggled as Calibration history | Confidence calibration domain is deferred / separable; not Initial Student Calibration |
| Fabricated Learning Evidence “seed” events | Poisons Evidence sovereignty |
| LLM-inferred syllabus completion from free text without explicit confirmation of the closed field set | Opaque inference; breaks explainability and self-report discipline |
| Legacy TopicProgress / heuristic composites as birth authority | Dual-truth debt — not Calibration truth |
| Diagnostic scores inside Calibration | Diagnostics produce Evidence; different educational path |
| Retention estimates, learning-speed claims, burnout self-diagnosis as Twin beliefs | Memory / Behaviour / Predictions must remain empty at birth |

### Collection invariant

> **If answering the question requires educational judgement, do not collect it at Calibration. If the student did not declare it in the closed field set, do not invent it.**

---

# 4. Unknowns

## 4.1 What must intentionally remain unknown after Calibration

After a lawful Calibration, the Twin may be non-empty in structure and still **unknown** in educational belief. The following must remain unknown (empty or explicitly unwarranted) until Evidence and Educational Intelligence discover them:

| Unknown | Why it must remain unknown | Who discovers it later |
|---|---|---|
| **Mastery** | Declaration is exposure/coverage, not assessed can-do | Knowledge beliefs via Evidence → Twin Update Pipeline |
| **Confidence** (self-report feel) | Not part of Calibration history; separable domain | Confidence channel / later Confidence work — never inferred from Core Reading claims |
| **Retention / Memory strength** | Completing reading does not prove durable memory | Memory domain from spaced Evidence and time |
| **Readiness / preparedness** | Sitting preparedness is derived judgement, not autobiography | Readiness Aggregation under thin-then-densifying warrant |
| **Weaknesses** | Declared incomplete sections ≠ assessed weakness map | Performance + Knowledge from assessed Evidence; Decision risk-framing |
| **Predicted marks / pass probability** | Forecasting requires models + Evidence density | Predictions domain / later calibrated forecasting |
| **Learning speed** | Rate of belief change is observed over time | Longitudinal Evidence patterns — never a birth field |
| **Behaviour reliability / adherence** | Declared hours ≠ how the student actually studies | Behaviour domain from session Evidence |
| **Exam-condition Performance** | Prior attempt declaration ≠ current mock-grade belief | Performance from assessed Evidence under exam conditions |

Empty Memory, Behaviour, and Predictions after Calibration are **educationally correct**, not product incompleteness.

## 4.2 Why Educational Intelligence must discover these later

1. **Integrity** — Discovering unknowns through Evidence preserves the distinction between prior and truth.  
2. **Explainability** — “We believe X because of Evidence Y” is defensible. “We believe X because you said so at signup” is not mastery explainability.  
3. **Correction** — Students misremember, overstate, or understate history. Only an Evidence path can revise beliefs without rewriting autobiography as gospel.  
4. **Authority boundaries** — Readiness, Decision, Recommendation, and Mission remain owners of judgement, selection, packaging, and composition. Calibration must not pre-answer their questions.  
5. **Cold-start honesty** — Thin warrant after Calibration is still cold start for belief density. Product language may acknowledge declared history without claiming Mid/High preparedness.

Governing restatement:

> **Calibration reduces beginner falsehood. It must not reduce educational humility. Unknowns after Calibration are a feature of truthful intelligence.**

---

# 5. Interaction with Educational Intelligence

Calibration affects Educational Intelligence by changing the **birth Twin** those domains consume. It does not replace their authority.

## 5.1 Readiness

| Calibration may | Calibration must not |
|---|---|
| Supply Identity / Goals sitting anchors and declared posture | Emit readiness bands, overall %, or “on track” claims |
| Leave Knowledge/Performance belief density thin while priors exist | Coerce returning posture into Mid/High preparedness |
| Make cold-start narratives historically honest (“declared Core Reading; Evidence still thin”) | Treat declared coverage as Knowledge Strength |

**Educational effect:** Readiness starts from a Twin that may include declared history under thin warrant, instead of an implicit beginner void. Readiness still owns preparedness judgement. Uncertainty remains mandatory until Evidence densifies.

## 5.2 Decision

| Calibration may | Calibration must not |
|---|---|
| Change the structural starting point Decision reasons over | Select the next action |
| Make absolute “start at topic 1 as unread” assumptions educationally contestable when coverage was declared | Grant permission to skip foundations as policy inside Calibration |
| Preserve attempt-history priors as lineage Decision may risk-frame later | Invent Performance weakness/strength from attempts alone |

**Educational effect:** Decision’s first selections should respect declared posture without confusing thin priors for dense beliefs. Evidence-creating actions remain appropriate when mastery, retention, and Performance are unknown. Decision remains sole next-action authority.

## 5.3 Recommendation

| Calibration may | Calibration must not |
|---|---|
| Indirectly shape what Decision selected (via Twin inputs) | Package, title, or urgency-copy a suggestion |
| Require honesty language that priors are self-declared when surfaced | Present recommendations as mastery-certified because Calibration occurred |

**Educational effect:** Recommendation remains a projection of Decision. Calibration must not become a parallel “setup recommendation” engine that tells the student what to study based on a questionnaire.

## 5.4 Mission

| Calibration may | Calibration must not |
|---|---|
| Influence mission composition only through Twin + Decision inputs | Compose missions, filler tasks, or week plans |
| Avoid forcing beginner mission templates when returning priors exist | Treat “revision student” as a mission template that skips Evidence |

**Educational effect:** Mission Intelligence still composes today’s task set from Decisions under constraints. Calibration is not a mission factory.

### Authority invariant

```
Calibration → birth Twin (priors)
        ↓
TwinProvider retrieves Twin
        ↓
Readiness judges preparedness (thin warrant)
        ↓
Decision selects next action
        ↓
Recommendation packages
        ↓
Mission composes
```

Governing restatement:

> **Calibration changes the Twin Educational Intelligence reads. It never becomes Educational Intelligence.**

---

# 6. Educational risks

## 6.1 Over-trusting self-report

**Failure mode:** Declared Core Reading / completed sections / prior attempts are treated as mastery, readiness, or Performance.

**Educational harm:** Foundations and diagnostics are skipped; Mid/High theatre appears; Evidence cannot easily correct inflated beliefs if priors were written as truth.

**Protective principle:** Thin warrant always; Evidence dominates conflicting priors for judgement; never write `mastery_belief` from declaration.

## 6.2 Under-trusting self-report

**Failure mode:** Calibration is collected then ignored; product still assumes beginner for planning, Decision, and missions.

**Educational harm:** Returning / revision / repeat candidates receive foundations-first falsehood; Calibration becomes questionnaire theatre; trust erodes.

**Protective principle:** Declared posture must change Twin structure and cold-start narrative; beginner assumption survives only when beginner is declared (or Calibration is absent and Twin is empty/absent — still not Mid fabrication).

## 6.3 Confirmation bias

**Failure mode:** Product and student both seek actions that confirm the declaration (“I’m revising, so only mocks”) and discount contradictory Evidence.

**Educational harm:** Weak foundations remain hidden; Performance Evidence is explained away; Decision loses independence.

**Protective principle:** Evidence sovereignty; Decision may prefer evidence-creating actions when warrant is thin even if objective is “revision”; explanations must show prior vs Evidence poles when they conflict.

## 6.4 False confidence

**Failure mode:** Completing Calibration feels like an assessment. Student and product language imply the Twin “knows” the learner.

**Educational harm:** Psychological readiness without Evidence; dismissal of early diagnostics; Confidence conflated with Calibration.

**Protective principle:** Product honesty — Calibration records history claims; it does not measure the student. Confidence remains separable and out of Calibration scope.

## 6.5 Repeated calibration

**Failure mode:** Students casually re-edit history; Twin oscillates; priors are silently rewritten into beliefs; lineage disappears.

**Educational harm:** Unstable educational state; audit confusion; Calibration used to “fix” bad recommendations instead of studying into Evidence.

**Protective principle:** Re-calibration is an explicit history-correction event with retained provenance — not a daily lever, not a belief overwrite, not a substitute for Evidence.

## 6.6 Recommendation theatre

**Failure mode:** Calibration questionnaire results are mapped directly into “recommended study path” without Decision authority — or Decision is coerced to echo declarations for UX polish.

**Educational harm:** Parallel intelligence; ADR-002 chain broken; explainability becomes “because you said so”; Mission becomes content filler matching the form.

**Protective principle:** No recommendations from Calibration. Decision sole next-action authority. Recommendation packages Decisions only. Experience Contract honesty preserved.

### Risk restatement

The primary educational danger is not missing Calibration. It is **Calibration that starts reasoning** — or **Calibration that is ignored**. Over-trust creates overconfidence. Under-trust recreates beginner falsehood. Both destroy the prior/truth distinction.

---

# 7. Version 1.0 recommendations

Recommend the educationally safest behaviour for Internal Alpha and Version 1.0.

## 7.1 Internal Alpha

1. **Prefer honest emptiness over invented Mid.** Until Calibration + Persistence exist end-to-end, empty / thin Twins and `TwinAbsent` honesty remain safer than fabricated returning-student theatre.  
2. **Do not simulate Calibration by writing mastery or readiness.** Alpha cold-start sources may supply Identity + empty domains; they must not invent calibrated beliefs.  
3. **If collecting any history questions early, treat answers as non-authoritative UX research** — not Twin truth — until the 3.6.1 prior-mapping contract is implemented with provenance.  
4. **Keep language cold-start honest.** Do not tell students they are Mid/High ready after a questionnaire.  
5. **Do not seed fake Evidence** to make intelligence look dense.

## 7.2 Version 1.0 (educationally safest shipping posture)

1. **Collect only the closed minimum set** (§3.2 / 3.6.1 §4.2). Refuse mastery, readiness, predicted marks, and confidence-as-calibration fields.  
2. **Map declarations to structural priors with explicit `self_declared` provenance.** Never to mastery beliefs.  
3. **Distinguish the four postures** (first-time, returning, revision, repeat) as declared prior/objective structure — not as readiness bands.  
4. **Leave mastery, confidence, retention, readiness, weaknesses, predicted marks, learning speed, and Behaviour unknown** until Evidence and Educational Intelligence discover them.  
5. **Teach Readiness / Decision to consume priors under thin warrant only.** Declared coverage may prevent absolute beginner falsehood; it must not authorise exam-rehearsal-only paths without Evidence.  
6. **Prefer evidence-creating early actions** when belief density is thin — including for revision and repeat postures.  
7. **Preserve Evidence sovereignty.** Calibration never authors Learning Evidence. Evidence dominates conflicting priors for educational judgement.  
8. **Make re-calibration rare and explicit.** History correction is not recommendation repair.  
9. **Keep V1/V2 curriculum-safe.** Declared sections resolve only through canonical curriculum identities.  
10. **Separate diagnostics.** If Version 1.0 later adds assessed baselines, they are Evidence paths — not Calibration expansions.  
11. **Preserve Experience Contract honesty.** After Calibration, product may say the Twin includes self-declared history. It must not claim measured mastery or Mid/High preparedness from Calibration alone.

### Version 1.0 educational motto

> **Ask little. Record priors. Discover truth through Evidence. Never let the questionnaire become the coach.**

---

# 8. Analysis Compliance Summary

| Invariant | Status under this analysis |
|---|---|
| Self-report establishes priors; Evidence establishes truth | Affirmed throughout |
| Calibration does not reason educationally | Affirmed — analysis only; no algorithms |
| No mastery / readiness / confidence inference | Affirmed — unknowns intentional |
| Readiness / Decision / Recommendation / Mission authority preserved | Affirmed — Calibration affects Twin inputs only |
| ADR-002 not redesigned | Honoured |
| No Application Layer / Flask / persistence / UI | Honoured — educational analysis only |
| Closed minimum information set | Affirmed; aligned with 3.6.1; expansions rejected |
| Curriculum V1/V2 safety | Required for declared sections |

---

# 9. STOP

This document defines **Student Calibration educational analysis only**.

It does **not** authorise:

- Implementation  
- Application Layer construction  
- Flask routes or forms  
- Database tables or migrations  
- UI / wizard steps  
- Twin Persistence implementation  
- Evidence seeding  
- Educational Intelligence redesign  
- ADR-002 changes  

**STOP.**

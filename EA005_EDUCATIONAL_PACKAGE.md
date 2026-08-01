# EA-005 — Educational Package (Golden Pilot)

**Programme:** Educational Excellence Programme EA-005 — Educational Package Pilot  
**Package ID:** `CS1-EA005-PKG-4.2-GLM-STRUCTURE`  
**Subject:** CS1 — Actuarial Statistics (2026)  
**Syllabus node:** `4.2` — Understand and use generalised linear models  
**Mode:** Learning (first-pass Learning Mode day on GLM structure)  
**Nature:** One complete educational package (Mission → Session → Reading Guidance → Knowledge Checks → Reflection → Tomorrow Preview)  
**Status:** Certified Golden Educational Package (reference / author-training); **not** wired into live application code  
**Authority:** EA-001 PASS · EA-002 PASS · EA-003 PASS · EA-004 PASS · EV-001  
**Schema:** `kwalitec.mission.blueprint` 1.0.0 · EA-004 Session Blueprint  
**CMP edition pin:** IFoA CS1 Core Reading / CMP aligned to 2026 syllabus (locus by syllabus §4.2; no CMP prose reproduced)  
**Package version:** `ea005-pilot-1.0.0`  
**Author ID:** `ea005-educational-author`  
**Created:** 2026-08-01  
**Updated:** 2026-08-01 (Revision R2 — post multi-review)  

---

## 0. Package selection

### Topic chosen

**CS1 · 4.2 — Understand and use generalised linear models**  
(Topic ID: `CS1-D-T02`; Section: Regression theory and applications)

### Why this topic

| Criterion | Fit |
|-----------|-----|
| **Has prerequisites** | Requires first-pass fluency from **4.1** linear regression (response/explanatory variables, linear predictor form, least-squares intuition). Cold start on 4.2 would be educationally unsafe. |
| **Introduces a meaningful new concept** | Extends the linear machine to non-Normal responses via **exponential family → linear predictor → link**. This is a genuine conceptual leap, not a re-labelling of 4.1. |
| **Naturally leads to another topic** | Lawful next syllabus node is **5.1** Bayesian foundations — likelihood / distribution thinking carries forward without unlock theatre. |
| **Exercises Reading Guidance** | Dense CMP chapter; selective open/stop/out-of-scope is mandatory (EP-04). Perfect stress test of EA-004 Reading Guidance Architecture. |
| **Exercises Reflection** | Known sticky misconceptions (link vs linear predictor; “GLM = just software”) yield topic-specific residual harvest (EP-07). |
| **Exercises Tomorrow continuity** | Clean skill bridge into Bayesian priors/posteriors without assigning heavy new teaching after Reflection (Gate TP). |
| **EV-001 counter-example value** | EV-001 audited live CS1 **4.2** and recorded Mission/Session FAIL (TB-001, TB-002, TB-007). This pilot authors the premium remedy pack for the same node — without rewriting the running app. |

### Explicit non-goals of selection

- Not a CS1 subject rewrite.  
- Not publication into the live student path (no application code).  
- Not a full multi-day coverage of all 4.2 LOs — **one deliberate day** on GLM structure (4.2.1–4.2.3 centre).  

---

## 1. Package arc (student-facing story)

```text
Mission: Extend linear models into GLM structure
        ↓
Session: Guide → CMP study → return → checks → reflect → tomorrow
        ↓
CMP Reading Guidance: Extract exponential family → η → link
        ↓
Knowledge Checks: Closed-book chain + canonical-link identification
        ↓
Reflection: Where the chain still sticks
        ↓
Tomorrow Preview: Bayesian foundations (5.1) — likelihood thinking carries forward
```

---

## 2. Mission authoring pack

### 2.1 Identity

| Field | Value |
|-------|-------|
| `mission_id` | `msn-ea005-cs1-4.2-glm-structure` |
| `schema_version` | `1.0.0` |
| `subject_id` | `CS1` |
| `package_version` | `ea005-pilot-1.0.0` |
| `topic_code` | `4.2` |
| `topic_title` | Understand and use generalised linear models |
| `mode` | `learning` |
| `display_title` | Extend linear models into GLM structure |
| `author_id` | `ea005-educational-author` |
| `created_at` | `2026-08-01T08:00:00Z` |
| `updated_at` | `2026-08-01T16:00:00Z` |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |
| `status` | `certified` |

### 2.2 Blueprint

**`mission_purpose`**  
Today’s Mission exists to extend yesterday’s linear-model fluency into GLM structure so you can choose a response family and link with intent — not by software habit.

**`educational_intent`**  
Produce a cognitive move from “linear regression assumes Normal errors” to “a GLM joins an exponential-family response, a linear predictor, and a link,” with enough clarity that you can justify one non-identity link closed-book.

**`tutor_intent`** *(internal — mandatory)*  
Today I will force the candidate to name the exponential-family → linear predictor → link chain aloud before reading deep, so they enter the CMP with a mental map instead of page-turning — and I will refuse to let “fit a glm()” substitute for that structure.

**`learning_objective`**  
Explain how a GLM joins an exponential-family response, a linear predictor, and a link for a non-Normal outcome.

**`cmp_reading_scope`**

| Subfield | Value |
|----------|-------|
| `open_point` | CMP material for Syllabus **4.2** — GLM setup: exponential family, mean/variance structure, linear predictor, link / canonical link (centred on LOs **4.2.1–4.2.3**) |
| `stop_condition` | Through the first worked GLM setup example that shows a non-identity link (or equivalent first full structural walkthrough in your CMP edition) |
| `out_of_scope_today` | Full deviance diagnostics; exhaustive factor/interaction design; multi-model comparison theatre; CS1B coding marathon; Bayesian material (5.1) |
| `materials_authority` | `cmp` |

**`syllabus_coverage`**

| Subfield | Value |
|----------|-------|
| `topic_code` | `4.2` |
| `topic_title` | Understand and use generalised linear models |
| `coverage_claim` | First-pass **progress** on GLM structure (exponential family, linear predictor, link). Not Topic Complete. Not Estimated Mastery. |
| `first_pass` | `true` |
| `weight_cue` | Regression / GLM questions commonly require justifying the response family and link — today’s success check targets that examiner move |

**`prerequisite_knowledge`**

1. CS1 **4.1** — response vs explanatory variables; simple/multiple linear regression form.  
2. Ability to write a linear predictor η = Xβ in ordinary language.  
3. Comfort that Normal linear models are a special case, not the only modelling world.  

**`concept_focus`**  
Exponential family → linear predictor → link (GLM structure chain).

**`common_misconceptions`**

| Statement | Corrective move |
|-----------|-----------------|
| “A GLM is just linear regression with fancy software.” | Force the three-part chain; Normal + identity link is the special case, not the definition. |
| “The link function is the same thing as the linear predictor.” | In Knowledge Checks: define η separately from g(μ); name one canonical link for a named family. |
| “Any link works equally — choice does not matter.” | Require one exam-style justification for a canonical (or clearly motivated) link on a count or binary response. |

**`study_strategy`**

| Subfield | Value |
|----------|-------|
| `method_summary` | Selective Guided Reading with a pre-drawn mental map, then closed-book retrieval of the GLM chain and one canonical-link identification |
| `session_structure` | Mission Orientation → Reading Preparation → Guided Reading (CMP) → Knowledge Checks (Active Recall + Checkpoint) → Reflection → Confidence → Wrap-up → Tomorrow Preparation |
| `active_demands` | annotate · extract · attempt-before-reveal · explain · identify · justify · reflect |

**`reflection_goal`**  
Harvest the single stickiest point in the GLM chain (family, η, or link) and one concrete CMP sentence or example step still unclear — fuel for revision and tomorrow’s likelihood bridge.

**`success_criteria`**

1. Closed-book, explain the GLM chain (exponential-family response → linear predictor → link) in your own words.  
2. Name one non-Normal response family and its canonical (or clearly justified) link.  
3. Point to where that structure appears in today’s CMP example (page/section cue from your notes).  

**`tomorrow_bridge`**

| Subfield | Value |
|----------|-------|
| `known` | `true` |
| `next_topic_code` | `5.1` |
| `next_topic_title` | Explain fundamental concepts of Bayesian statistics and use these concepts to calculate Bayesian estimators |
| `continuity_line` | Today you practised thinking in distributions and likelihood-shaped structure; tomorrow that thinking opens Bayesian priors and posteriors. |
| `light_prep_cue` | Optional skim: CMP heading for Bayes’ theorem / prior–posterior (Syllabus 5.1.1–5.1.2) — titles only, no deep study tonight |

**`estimated_cognitive_load`**  
`heavy`

**`cognitive_load_rationale`**  
New abstraction density (family + η + link) on top of 4.1; calculation load light today, conceptual load high.

**`estimated_study_time_minutes`**  
`{min: 50, max: 70}`

**`revision_signals`**

| Signal | Path |
|--------|------|
| Weak closed-book chain explanation | Soft revision flag: rework GLM structure (not whole chapter) |
| Confuses link with linear predictor | Named misconception hit → targeted recall card |
| Reflection residual on canonical links | Feed Revision workspace when warranted by evidence |

**`why_now`**  
4.1 is complete enough to extend; 4.2 is the next lawful Learning Mode node; examiners frequently ask you to choose and justify a link for a non-Normal response — structure first, software second.

**`expected_benefit`**  
A usable mental map of GLM structure and one justified link choice you can defend — Study Progress evidence for today’s Session, not mastery of all of 4.2.

**`explainability`**  
Assigned because you finished classical linear models (4.1); the exam skill gap now is extending the linear predictor to exponential-family responses via a link — not re-reading least squares.

### 2.3 Continuity bundle

| Field | Value |
|-------|-------|
| `prior_bridge` | Yesterday you finished classical linear models (4.1) — response, explanatory variables, and the linear predictor in the Normal world. Today that same linear machinery expands to responses that are not Normal. |
| `prior_mission_id` | `msn-ea005-cs1-4.1-prior-assumed` *(assumed prior / pilot continuity; not a live app ID)* |
| `prior_topic_code` | `4.1` |
| `cold_start` | `false` |
| `continuity_bundle_complete` | `true` |

### 2.4 Execution / dependencies

| Field | Value |
|-------|-------|
| `session_intent` | Orientation · Reading Preparation · Guided Reading · Knowledge Checks · Reflection · Confidence · Wrap-up · Tomorrow Preparation · Completion |
| `linked_session_id` | `ssn-ea005-cs1-4.2-glm-structure` |
| `linked_episode_ids` | `lep-ea005-4.2-gr-01` · `lep-ea005-4.2-ar-01` · `lep-ea005-4.2-cp-01` |
| `dependencies` | prior topic 4.1; Session `ssn-ea005-cs1-4.2-glm-structure`; Episodes above; curriculum package CS1 2026; CMP edition pin as identity; twin inputs assumed: none required beyond Learning Mode order |

### 2.5 Quality self-check

| Field | Value |
|-------|-------|
| `voice_self_check` | `true` |
| `style_self_check` | `true` |
| `prohibited_patterns_denied` | P1, P2, P3, P4, P5, P6, P7, P8, P9, P10, P11, P12 |
| `principle_citations` | EP-01, EP-02, EP-03, EP-04, EP-05, EP-06, EP-07, EP-08, EP-09, EP-10 |
| `ev001_regression_denied` | TB-001, TB-002, TB-004, TB-007, TB-008, TB-009 |

### 2.6 Student-facing Mission brief (composed)

> **Mission:** Extend linear models into GLM structure  
> **Topic:** 4.2 — Understand and use generalised linear models  
> **Objective:** Explain how a GLM joins an exponential-family response, a linear predictor, and a link for a non-Normal outcome.  
> **Bridge:** Yesterday you finished classical linear models (4.1). Today that same linear machinery expands to responses that are not Normal.  
> **Why now:** Next lawful Learning Mode step after 4.1; exam questions often require choosing and justifying a link.  
> **Focus:** Exponential family → linear predictor → link.  
> **Success today:** Closed-book, name the GLM chain; give one non-Normal family with its canonical (or justified) link; note where it sits in the CMP example.  
> **Materials:** CMP for Syllabus 4.2 (GLM setup) through the first worked structural example. Not today: full deviance diagnostics or Bayesian material.  
> **How:** Guided Reading → Knowledge Checks → Reflection.  
> **Benefit:** A mental map you can defend — Study Progress, not mastery of all of 4.2.  
> **Tomorrow:** Bayesian foundations (5.1) — distribution and likelihood thinking carry forward.

---

## 3. Session authoring pack

### 3.1 Identity / metadata

| Field | Value |
|-------|-------|
| `session_id` | `ssn-ea005-cs1-4.2-glm-structure` |
| `parent_mission_id` | `msn-ea005-cs1-4.2-glm-structure` |
| `subject_id` | `CS1` |
| `package_version` | `ea005-pilot-1.0.0` |
| `topic_code` | `4.2` |
| `topic_title` | Understand and use generalised linear models |
| `learning_objective` | Explain how a GLM joins an exponential-family response, a linear predictor, and a link for a non-Normal outcome. |
| `concept_focus` | Exponential family → linear predictor → link |
| `cognitive_load` | Heavy |
| `duration_budget` | 50–70 minutes |
| `interruption_budget` | 2 Reading Pause Points maximum |
| `status` | `certified` |
| `cmp_edition` | IFoA CS1 Core Reading / CMP · 2026 syllabus alignment |

### 3.2 Permanent Session specification

**`session_educational_purpose`**  
This Session exists to execute today’s Mission: build and stress-test a closed-book GLM structure chain using selective CMP reading and retrieval — not to survey the whole of 4.2.

**`session_tutor_purpose`** *(internal — mandatory)*  
In this hour I will set three focus questions, exit while the candidate works the first GLM structural example alone, then force a closed-book linear-predictor-and-link explanation — so today’s Mission success criteria are stress-tested, not merely claimed. I will not narrate the CMP page-by-page.

**`student_actions`**

1. Confirm ready to begin with real topic 4.2 bound.  
2. Absorb one short Mission orientation.  
3. Write the GLM chain skeleton in notes before opening CMP.  
4. Open CMP at the GLM setup locus; hunt answers to focus questions.  
5. At Pause Point 1: write own-words definition of the linear predictor η.  
6. Attempt the middle step of the first worked example before reading the solution.  
7. Stop at stop condition; return to Kwalitec.  
8. Complete closed-book Active Recall + Checkpoint.  
9. Author Reflection residuals.  
10. Soft confidence rating with warrant.  
11. Receive Wrap-up + Tomorrow Preview; close Session.

**`cmp_interaction`**

| Element | Specification |
|---------|---------------|
| Open | CMP · Syllabus 4.2 GLM setup (exponential family, mean/variance, η, link) |
| Stop | After first worked structural example with a non-identity link (or equivalent) |
| Out of scope | Deviance deep-dive; factor/interaction catalogue; Bayesian chapter |
| Exit into reading | After Reading Guidance packet delivered |
| Re-entry | Student returns when stop met → Knowledge Checks (no Mission restack) |
| Pause points | 2 designed (see §4) |

**`expected_outputs`**

- Pre-reading chain skeleton (3 labelled parts)  
- Own-words η note (Pause 1)  
- Attempt mark on example middle step (Pause 2)  
- Answers to Active Recall + Checkpoint  
- Reflection text (clarity + residual)  
- Confidence mark (1–5) with one-line warrant  

**`success_evidence`**  
Closed-book / reduced-cue performance on Knowledge Checks aligned to Mission success criteria, plus student-authored Reflection. Reading completion alone is **not** success evidence.

**`reflection_evidence`**  
Implements Mission `reflection_goal`: stickiest chain element + one unclear CMP locus; student-authored; required before educational close.

**`session_revision_signals`**  
Aligns to Mission: weak chain check; link/η confusion; Reflection residual on canonical links.

**`continuity_evidence`**  
Orientation carries 4.1 → 4.2 bridge; Tomorrow Preparation agrees with Mission tomorrow_bridge (5.1); completion language = Session complete / Study Progress only.

**`unavailable_policy`**  
If topic 4.2 or CMP locus cannot resolve: refuse Session open; honest message — never “Today’s topic” placeholders.

### 3.3 Stage plan

| # | Stage | Episode type | Educational job |
|---|-------|--------------|-----------------|
| 1 | Session Entry | — | Bind Mission `msn-ea005-cs1-4.2-glm-structure` + topic 4.2 |
| 2 | Mission Orientation | — | One short brief; Begin |
| 3 | Reading Preparation | — | Focus questions, misconceptions, duration |
| 4 | CMP Reading Guidance | Guided Reading `lep-ea005-4.2-gr-01` | Exit packet → uninterrupted CMP |
| 5 | Reading Pause Points | (inside Guided Reading) | 2 sparse pauses |
| 6 | Knowledge Checks | Active Recall `lep-ea005-4.2-ar-01` + Checkpoint `lep-ea005-4.2-cp-01` | Retrieval + identify/justify |
| 7 | Reflection | — | Topic-specific harvest |
| 8 | Confidence Assessment | — | Soft probe |
| 9 | Session Wrap-up | — | Truthful Study Progress close |
| 10 | Tomorrow Preparation | — | 5.1 continuity |
| 11 | Session Completion | — | Lawful close |

**Advertised activity count:** Guided Reading · Active Recall · Checkpoint = **3 of 3** (all reachable).

---

## 4. CMP Reading Guidance (instance)

*Conforms to `EA004_READING_GUIDANCE_ARCHITECTURE.md`.*

### 4.1 Reading lead line

Extract how a GLM joins an exponential-family response, a linear predictor, and a link — then stop after the first structural worked example.

### 4.2 Reading objectives / focus questions (2–4)

1. Where is the **linear predictor** η defined for a GLM? Write it in your own words.  
2. Which distributions in today’s reading sit in the **exponential family**, and what mean/variance language does the CMP use?  
3. Which example shows a **non-identity link**? Attempt the middle modelling step before reading the solution.  
4. *(Success link)* You will later explain, closed-book, the family → η → link chain and name one canonical link.

### 4.3 Misconception watch-list (before exit)

- Watch for treating “GLM” as “linear regression with a package name.”  
- Watch for calling the link function the linear predictor.  
- Watch for “any link is fine” without justification.

### 4.4 Attention directives

| Type | Directive |
|------|-----------|
| Open point | CMP · Syllabus 4.2 GLM setup (4.2.1–4.2.3 centre) |
| Hunt targets | Exponential-family statement; definition of η; link / canonical link; first worked non-identity link example |
| Ignore today | Full deviance diagnostics; long factor/interaction catalogues; Bayesian sections |
| Annotation task | Before deep reading: sketch Family / η / Link as three boxes in notes |
| Attempt-before-reveal | At the first worked example, cover the solution and attempt the middle step |
| Stop condition | End of that first structural worked example |

### 4.5 Exit packet (mandatory)

- Open locus ✓  
- Focus questions ✓  
- Stop condition ✓  
- Return cue: **Come back to Kwalitec when you have finished the first structural worked example.**  
- Annotation / attempt instruction ✓  
- Misconception watch-list ✓  

**Exit line (student-facing):**  
> Open your CMP at the GLM setup for Syllabus 4.2. Work with the three focus questions above. I will stay quiet while you study. Come back here when you reach the end of the first structural worked example.

### 4.6 Reading Pause Points (budget: 2)

| ID | Placement | Cue | Student action | Re-exit |
|----|-----------|-----|----------------|---------|
| PP1 | After η definition | “Pause — write η in your own words (one sentence).” | Annotate | Return to CMP |
| PP2 | Before solution reveal of first worked example | “Attempt the middle step before you uncover the solution.” | Attempt | Return to CMP until stop |

### 4.7 Re-entry after reading

1. Acknowledge return without fluff.  
2. Do **not** re-brief the Mission.  
3. Move to Knowledge Checks.  
4. Feedback + advance.  
5. Carry residuals into Reflection.

**Re-entry line:**  
> Welcome back. Keep your CMP closed for the next few minutes. We will check what the reading fixed in memory.

### 4.8 Forbidden behaviours denied

RG-X01 … RG-X12 denied (empty shell, placeholders, CMP paste, continuous interruption, chatbot narration, no stop/return, mastery-from-reading, Mission restack, unresolved locus open, mechanical fragments, Reflection-as-only-activity, platform jargon).

---

## 5. Knowledge Checks

### 5.1 Episode A — Active Recall (`lep-ea005-4.2-ar-01`)

| Field | Value |
|-------|-------|
| Type | Active Recall |
| Objective | Retrieve the GLM structure chain without CMP open |
| Demand | Explain (closed-book) |
| Duration cue | ~8–10 minutes |

**Prompt:**  
> Closed-book. In your own words, explain how a generalised linear model joins (1) an exponential-family response, (2) a linear predictor, and (3) a link function. One short paragraph is enough.

**Success criteria (Episode):**

1. All three parts named in a coherent order.  
2. Linear predictor distinguished from the link.  
3. At least one phrase showing non-Normal responses are in scope.

**Feedback design:**  
- If η and link conflated → corrective note + optional 2-minute CMP re-open at link definition only, then re-attempt.  
- If software-only answer → reject as insufficient; demand structure.  
- Advance only after attempt recorded and feedback shown (no “answer recorded” dead-end).

### 5.2 Episode B — Checkpoint (`lep-ea005-4.2-cp-01`)

| Field | Value |
|-------|-------|
| Type | Checkpoint |
| Objective | Identify and justify one canonical (or clearly motivated) link |
| Demand | Identify + justify |
| Duration cue | ~8–12 minutes |

**Prompt:**  
> Name one non-Normal response family used in GLMs (e.g. Poisson or binomial). State its canonical link (or a clearly justified link). In one sentence, why is that link a sensible default for that family?

**Success criteria (Episode):**

1. Family named correctly.  
2. Link named correctly for that family (canonical preferred).  
3. Justification is distributional / mean-range aware — not “because R defaults to it.”

**Feedback design:**  
- Correct family/wrong link → show the target pairing pattern without pasting CMP paragraphs; invite one re-attempt.  
- “Software default” justification → fail criterion 3; ask for mean/support reasoning.  
- Advance to Reflection after feedback.

---

## 6. Reflection

**Implements:** Mission `reflection_goal` · EP-07 · Gate SS-04  

**Framing (student-facing):**  
> Do not summarise the whole chapter. Harvest what still wobbles in the GLM chain.

**Prompts (student-authored):**

1. Which part of the chain is stickiest right now — **family**, **linear predictor η**, or **link** — and why?  
2. Quote or paraphrase the single CMP sentence or example step that is still unclear (your words; no need for a long extract).  
3. If you had five minutes tomorrow before Bayesian work, what one GLM structure move would you rework?

**Rules:**

- Student writes the answers (or structured choices + free text).  
- System must not write Reflection and attribute it to the student.  
- Required before Session Completion.  
- Feeds `session_revision_signals` and tomorrow continuity (likelihood comfort).

---

## 7. Confidence Assessment

| Field | Value |
|-------|-------|
| Type | Soft metacognitive probe |
| Scale | 1–5 confidence on today’s success criteria |
| Warrant | One sentence: “I can / cannot yet explain the chain closed-book because…” |
| Must not | Claim Estimated Mastery, Topic Complete, or readiness ±N% from this mark alone |

**Prompt:**  
> How confident are you that you could explain the GLM chain closed-book tomorrow morning? Rate 1–5 and give one honest warrant.

---

## 8. Session Wrap-up

**Student-facing close:**  
> Session complete for **Extend linear models into GLM structure**. You practiced selective CMP reading on Syllabus 4.2 setup and stress-tested the family → η → link chain. This is **Study Progress** for today’s block — not mastery of all of 4.2, and not Topic Complete by itself.

**Must not:** Invent completion of LOs not attempted; mastery theatre; contradict History inputs.

---

## 9. Tomorrow Preview (Gate TP)

| Field | Value |
|-------|-------|
| Next topic | **5.1** — Explain fundamental concepts of Bayesian statistics… |
| Continuity line | Today you practised thinking in distributions and likelihood-shaped structure; tomorrow that thinking opens Bayesian priors and posteriors. |
| Light prep | Optional: skim CMP headings for Bayes’ theorem / prior–posterior (5.1.1–5.1.2) only — no deep study tonight |
| Honesty | Lawful next syllabus node; agrees with Mission `tomorrow_bridge` |
| Load | No heavy new teaching after Reflection |

**Student-facing Tomorrow Preview:**  
> **Tomorrow:** Bayesian foundations (5.1).  
> Today’s GLM work trained distribution-and-likelihood thinking; tomorrow that carries into priors and posteriors.  
> Optional light prep: skim the CMP headings for Bayes’ theorem and prior–posterior — titles only tonight.

---

## 10. Learning Episode packs (Gate LE)

### 10.1 `lep-ea005-4.2-gr-01` — Guided Reading

| LE check | Evidence |
|----------|----------|
| LE-01 Objective | Extract GLM structure (family → η → link) from CMP setup |
| LE-02 Coherence | Parent Mission 4.2 / concept focus |
| LE-03 Teachable instruction | Full Reading Guidance §4 |
| LE-04 CMP vs Kwalitec | Guides into CMP; no CMP paste |
| LE-05 Active demand | Annotate + attempt-before-reveal |
| LE-06 Success criteria | Focus questions answered in notes; stop condition met; return |
| LE-07 Not templated | Topic-specific GLM language throughout |
| LE-08 Transitions | Stage 1 of 3 → advances to Active Recall |
| LE-09 Accuracy | Standard IFoA GLM structure claims; no false maths |
| LE-10 Depth vs duration | ~25–35 min CMP block inside 50–70 min Session |

### 10.2 `lep-ea005-4.2-ar-01` — Active Recall

See §5.1 — LE-01–LE-10 satisfied (closed-book explain; feedback; advance).

### 10.3 `lep-ea005-4.2-cp-01` — Checkpoint

See §5.2 — LE-01–LE-10 satisfied (identify + justify; feedback; advance to Reflection).

---

## 11. Joint publication note

This package is certified as a **Golden Educational Package** under EA-005 for reference and future author training.

| Live student exposure | Status |
|-----------------------|--------|
| Application wiring | **Not in scope** — no app/Runtime/SCI changes in EA-005 |
| Publication Approval for production CS1 | Deferred to a successor publication programme that may adopt this pack verbatim or by adaptation |
| Honest unavailable | N/A for this documentation pilot |

---

## 12. Closing

> This package is the first complete exemplar produced under EA-001 through EA-004.  
> It teaches one CS1 day well — and, more importantly, defines the quality bar every future Kwalitec educational package must match.

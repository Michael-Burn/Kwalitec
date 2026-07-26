# Explainability Standard

**Programme:** P-001.2 — Explainability Standard  
**Version:** 1.0  
**Status:** Active — permanent product explainability authority for student-facing intelligence  
**Effective:** 2026-07-26  
**Authority:** Product explainability law  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

This standard defines **how every recommendation, prediction, planning decision, and readiness assessment must explain itself to students**.

It exists so that:

- students can trust guidance because they can see the working;
- recommendation effectiveness is not blocked by opaque “highest-value” speech;
- confidence and uncertainty are communicated honestly;
- every student-facing intelligence change can be reviewed against one permanent contract;
- Version 1 can close the K8 Explainability gap (baseline **55** → floor **≥ 70**).

**Explainability improves understanding of decisions already authorised.  
It never invents educational certainty, mastery, or a second educational brain.**

---

## 2. Guiding principles

| # | Principle | Rule |
|---|---|---|
| P1 | Every guidance product explains itself | Silent steering is forbidden. If it cannot be explained, it is not ready to show. |
| P2 | Evidence before opinion | Supporting evidence must be identifiable (facts, practice results, syllabus position). Vague authority language (“because learning evidence says so”) is non-compliant. |
| P3 | Confidence is speakable | Confidence / uncertainty must match evidence strength. Thin history requires understatement or “cannot yet be estimated.” |
| P4 | One clear next action | Guidance reduces decision burden. Students must know what to do now. |
| P5 | Educational language only | Twin, Adaptive Engine, warrants, pipelines, entity ids, and internal enums stay invisible on student surfaces. |
| P6 | Facts ≠ estimates ≠ advice | Observed / derived facts, evidence-backed estimates, and educational advice remain distinguishable (EIP-003 hierarchy). |
| P7 | Consistent across Runtime A | The same decision class must produce consistent explanation structure across Dashboard, Coach, Insights, Plan, Readiness, and Journey surfaces. |
| P8 | Length fits the level | Level 1 stays short; Level 3 is opt-in or diagnostic. Do not dump diagnostics into daily coaching. |
| P9 | No AI-authored educational truth | AI may enrich wording of already-decided explanations; it must not invent reasons, evidence, or confidence. |
| P10 | Agency preserved | Advice does not commandeer Learning Mode / Today’s Mission. Advisory divergence must be labelled as advice. |

---

## 3. Educational objectives

Explainability serves learning, not theatre.

| Objective | Student outcome |
|---|---|
| Trust | The student believes the coach is working from their syllabus and practice — not guessing. |
| Decision quality | The student can choose to follow, defer, or question guidance with enough context. |
| Learning transfer | Reasons emphasise syllabus progress, weak-topic repair, revision timing, and exam readiness — not activity vanity. |
| Honesty under uncertainty | Cold start and thin evidence produce humble speech, not false precision. |
| Consistency habit | Clear “what / why / next” reduces friction so serious candidates keep studying. |
| Professional formation | Explanations model how professionals justify study priorities with evidence. |

**Final Test alignment:** Explanations that help students become better professionals pass. Explanations that inflate confidence, hide uncertainty, or reward clicks fail.

---

## 4. Relationship to Product Constitution

| Product authority | Relationship |
|---|---|
| Vision 2030 | Highest product-philosophy authority. Explainability supports Vision design questions (“What should I do now?”, “What is stopping me?”, “What happens next?”) and the Final Test. |
| Product Blueprint | Strategy and roadmap consume this standard when shipping student-facing intelligence. |
| Product Success Framework (KSI) | K8 Explainability is measured against this standard. Version 1 criterion **V1-K3** requires K8 ≥ **70**. |
| Student Impact Assessment | Programmes that change student-facing intelligence must cite this standard and complete the [Explainability Review Checklist](EXPLAINABILITY_REVIEW_CHECKLIST.md). |

This standard does **not** replace Vision 2030 or invent a second north star. It operationalises product trust for guidance surfaces.

---

## 5. Relationship to existing Architecture / Educational Constitutions

Authority order for student-facing explanation speech:

```
Vision 2030 (philosophy)
        ↓
Educational Constitution + EIP (educational truth, claim honesty)
        ↓
EIP-003 Educational Explainability Standard (four-question educational speech contract)
        ↓
Architecture Constitution Art. IV (structural explainability law)
        ↓
Digital Twin / Adaptive / Runtime constitutions (who may decide; provenance)
        ↓
THIS STANDARD (product levels, mandatory schema, patterns, quality, review gate)
        ↓
Runtime A presentation / Coach / Insights / Plan / Readiness copy
```

| Authority | Owns | This standard’s role |
|---|---|---|
| Educational Constitution | Lawful educational meaning | Consumes — never soft-amends mastery, coverage, or evidence law |
| EIP-003 Educational Explainability Standard | Four-question framework; claim types; language bans | **Specialises** into product levels, schema fields, patterns, and review checklist |
| Architecture Constitution Art. IV | “Unexplainable guidance is incomplete guidance” | Implements product acceptance criteria for that law |
| Digital Twin Constitution | Twin authority / honesty | Explanations may cite Twin-derived estimates only when lawfully labelled as estimates |
| Constitutional Explainability Architecture | How completed constitutional audits become constitutional explanations | Orthogonal — product narration remains subordinate; does not re-decide education |
| Runtime A | One educational runtime implementation | Must present consistent explanation contracts across surfaces |

**Conflict rule:** If this document appears to conflict with EIP-003 or Architecture Art. IV → **STOP**, document, amend the higher authority first. Product patterns may never invent educational certainty.

---

## 6. Explanation levels

Every student-facing intelligence surface chooses a **default level**. Deeper levels may be offered via progressive disclosure (e.g. “Why this?” / “Show details”), never by dumping Level 3 into the primary daily path.

### Level 1 — Simple

| Attribute | Definition |
|---|---|
| **Audience** | Everyday student at the point of action (Dashboard, start session, Coach tip, mission card) |
| **Maximum recommended length** | **≤ 40 words** for the primary explanation block (excluding the recommendation title itself) |
| **Required information** | Recommendation; Why (one reason); Suggested next action. Confidence may be implicit (“Suggested”) if evidence is thin and language is humble. |
| **Appropriate use cases** | Daily plan headline; Today’s Mission reason line; short Coach nudge; positive reinforcement toast; missed-session recovery one-liner |
| **Must not** | Expose diagnostics, multi-factor score dumps, or engineering vocabulary |

### Level 2 — Detailed

| Attribute | Definition |
|---|---|
| **Audience** | Student who wants to understand the working before committing time (Insights, readiness panel, plan detail, revision recommendation) |
| **Maximum recommended length** | **≤ 120 words** for the primary explanation narrative, or equivalent structured fields that a student can scan in **≤ 45 seconds** |
| **Required information** | Full [Mandatory Explanation Schema](#7-mandatory-explanation-schema) except Review point (include Review point when a reassessment is material) |
| **Appropriate use cases** | Readiness assessment detail; topic prioritisation rationale; revision recommendation; study warning with evidence; plan day breakdown |
| **Must not** | Replace Learning Mode authority silently; present estimates as facts |

### Level 3 — Diagnostic

| Attribute | Definition |
|---|---|
| **Audience** | Support, educational review, power users opting into “show working,” dogfood, and operator audit — not the default daily path |
| **Maximum recommended length** | **≤ 250 words** student-safe narrative **or** structured diagnostic packet; internal operator views may add non-student fields behind operator auth |
| **Required information** | Full Mandatory Explanation Schema + evidence lineage (what inputs, what decision class, what confidence basis) + explicit uncertainty / missing-data notes |
| **Appropriate use cases** | “Why am I seeing this?” expanded drawer; educational governance review; dual-run / shadow comparison narration; support investigation |
| **Must not** | Leak internal ids, warrant tags, pipeline names, or Twin machinery into default student chrome; invent precision the inputs do not support |

### Level selection rules

1. Default daily coaching and mission start → **Level 1**.
2. Surfaces whose job is judgement (readiness, prioritisation, revision advice) → **Level 2** by default.
3. Level 3 only via explicit expand / operator path / review artefact.
4. Progressive disclosure: Level 1 summary must remain true when Level 2/3 is opened (no bait-and-switch reasons).

---

## 7. Mandatory Explanation Schema

Every **student-facing recommendation** (and, by extension, every material prediction, planning decision, and readiness assessment shown as guidance) must specify the following fields. Surfaces may render fields as labelled sections or as an equivalent coherent narrative that still contains each required element at the chosen level.

| Field | Definition | Level 1 | Level 2 | Level 3 |
|---|---|---|---|---|
| **Recommendation** | What the system suggests or decides for the student (topic, session, plan, readiness posture, recovery action) | Required | Required | Required |
| **Why it is recommended** | One primary educational reason in plain language | Required (one sentence) | Required | Required (+ secondary factors allowed if ranked) |
| **Supporting evidence** | Identifiable inputs: syllabus position, completed study, practice results, missed sessions, time-to-exam, prior outcomes | Optional short cue | Required | Required with lineage |
| **Confidence level** | Honest strength of the judgement (see §7.1) | Recommended (may be lexical: Suggested / Estimated) | Required | Required + basis |
| **Expected benefit** | What following the guidance is meant to improve (coverage, weak-topic repair, readiness honesty, revision timing) | Optional short cue | Required | Required |
| **Suggested next action** | One clear thing to do now | Required | Required | Required |
| **Review point** | When the judgement should be reconsidered (after N sessions, after next practice, on plan refresh) | When applicable | When applicable | Required when judgement is provisional |

### 7.1 Confidence levels (student-safe)

| Label | Meaning | When to use |
|---|---|---|
| **High confidence** | Multiple consistent evidence sources; decision is stable under small input changes | Dense practice history + clear syllabus signal |
| **Moderate confidence** | Useful guidance with incomplete or mixed evidence | Typical mid-journey state |
| **Low confidence / Suggested** | Thin history, cold start, or conflicting signals — follow with caution | New users; sparse practice; conflicting topic signals |
| **Cannot yet be estimated** | Lawful refusal to invent a score or ranking | Empty readiness; insufficient history |

Lexical alternatives (“Suggested”, “Estimated”, “Optional”) are compliant when they communicate the same honesty as the labels above.

### 7.2 Mapping to EIP-003 four questions

| Schema field | EIP-003 question |
|---|---|
| Supporting evidence (facts) | Q1 — What do we objectively know? |
| Confidence / estimates | Q2 — What do we estimate? |
| Why + Recommendation + Expected benefit | Q3 — Why are we recommending this? |
| Suggested next action (+ Review point) | Q4 — What should the student do next? |

Compliant product explanations satisfy **both** this schema and EIP-003.

### 7.3 Non-recommendation guidance

For **predictions**, **planning decisions**, and **readiness assessments** that are not framed as a tip:

- Map **Recommendation** → the stated judgement (e.g. “Estimated readiness: building”, “Today’s plan: Topic X then Y”).
- Keep Why, Evidence, Confidence, Benefit, Next action, and Review point as above.
- Never present a readiness percentage or composite without Level 2 access to Why + Evidence + Confidence.

---

## 8. Explanation Quality Guidelines

### 8.1 Plain language principles

1. Write for a serious exam candidate, not an engineer or data scientist.
2. Prefer short sentences and concrete nouns (topic names, “practice results”, “today’s mission”).
3. One primary reason per explanation; secondary factors belong in Level 2/3 only, ranked.
4. Replace jargon with EIP-003 student language (Completed studying, Estimated readiness, Suggested, Today’s Mission).
5. Never use unexplained percentages as the only reason.

### 8.2 Reading time targets

| Level | Target reading time | Hard stop |
|---|---|---|
| Level 1 | ≤ **10 seconds** | If longer, cut or move detail to Level 2 |
| Level 2 | ≤ **45 seconds** | If longer, structure as scanable fields |
| Level 3 | ≤ **2 minutes** student-safe | Operator diagnostics may exceed with auth |

### 8.3 Maximum complexity

| Constraint | Rule |
|---|---|
| Primary reasons at Level 1 | Exactly **one** |
| Factors named at Level 2 | At most **three**, ordered |
| Numeric composites | Must unpack into student-meaningful parts at Level 2 |
| Parallel metaphors | Forbidden if they conflict with Learning Mode / Today’s Mission |
| Dual “today” speech | Forbidden — one authorised today story across Runtime A surfaces |

### 8.4 Educational terminology standards

| Prefer (student-facing) | Avoid (student-facing) |
|---|---|
| Today’s Mission / today’s focus | Recommended Mission theatre that replaces Learning Mode |
| Completed studying / Study Progress | Mastered / mastery (unless authorised Educational Evidence) |
| Estimated Knowledge / Estimated readiness | Bare “Known / Strong / Weak” as facts under thin evidence |
| Practice results / study checks | Warrant, cold_start, thin_warrant, evidence_creating |
| Suggested / Recommended / Optional | Digital Twin, Educational Intelligence, pipeline, entity ids |
| Syllabus / exam topic names | Internal curriculum keys as primary labels |

Internal domains retain precise vocabulary; presentation maps before render.

### 8.5 Accessibility considerations

1. Meaning must not depend on colour alone (confidence, warnings, positive reinforcement).
2. Explanation structure must remain understandable when CSS/layout is simplified (logical heading / field order).
3. Interactive “Why this?” controls must be keyboard-operable and announce expanded content to assistive tech when implemented.
4. Warnings must state the issue and the next action in text — icons are secondary.
5. Reading level: aim for clear professional English; avoid idioms that obscure the educational reason.
6. Do not rely on hover-only explanations for mandatory schema fields on primary paths.

---

## 9. Consistency across Runtime A

Runtime A is the single educational runtime implementation. Product explanations must be **structurally consistent** across its student surfaces:

| Surface family | Consistency rule |
|---|---|
| Dashboard / Learning Workspace | Level 1 mission + plan reasons align with session start |
| Coach / Insights | Same decision class → same Why + Evidence story (wording may vary; reasons must not conflict) |
| Daily plan | Topic order reasons match prioritisation / readiness inputs cited elsewhere that day |
| Readiness | Composite unpacking matches Insight / Coach language for the same inputs |
| Journey / analytics | Progress speech does not contradict mission authority or readiness honesty |
| Warnings / recovery | Recovery actions do not invent a second “today” that fights Learning Mode |

**Inconsistency is a defect**, even when each surface is locally fluent.

---

## 10. Patterns and review

| Artefact | Use |
|---|---|
| [`EXPLANATION_PATTERNS.md`](EXPLANATION_PATTERNS.md) | Copy-ready templates for common guidance types |
| [`EXPLAINABILITY_REVIEW_CHECKLIST.md`](EXPLAINABILITY_REVIEW_CHECKLIST.md) | Mandatory review for EP/P programmes affecting student-facing intelligence |
| [`../ep006_1_mes_end_to_end_delivery/MES_DELIVERY_SPECIFICATION.md`](../ep006_1_mes_end_to_end_delivery/MES_DELIVERY_SPECIFICATION.md) | Student-visible MES delivery contract (M/D/O + progressive disclosure) |
| [`../ep006_2_mes_delivery_implementation/`](../ep006_2_mes_delivery_implementation/) | Presentation implementation — Home/Coach pass-through of authored MES |

---

## 11. Explicit non-goals

This standard does **not**:

- change Twin, Adaptive, planning, or readiness algorithms;
- authorise new educational scores;
- require UI implementation in this programme;
- replace EIP-003 or Architecture Article IV;
- lift EP-001 / EP-003 recommendation-effectiveness marketing freezes.

---

## 12. Amendment

Amendments require Product + Educational governance review when claim honesty or educational language may change. Version bumps record date and rationale. Lower documents (PRDs, copy decks, UI specs) must not contradict this standard.

---

**End of EXPLAINABILITY_STANDARD**

# Product Success Framework

**Programme:** P-001.1 — KSI Baseline & Version 1 Success Framework  
**Version:** 1.1  
**Status:** Active — permanent product success measurement authority  
**Effective:** 2026-07-26  
**Amended:** 2026-07-26 — §5.6 validated vs estimated (EP-005.1); weights unchanged  
**Authority:** Product measurement law (subordinate to Vision 2030; complementary to Educational Constitution and Architecture Constitution)  
**Does not:** Change runtime behaviour, Twin algorithms, UI, or APIs  

---

## 1. Purpose

This framework defines **how Kwalitec measures educational usefulness** and **what Version 1 product success means**.

It exists so that:

- every future programme can estimate its contribution to student value;
- prioritisation is driven by educational usefulness gaps, not feature count;
- Version 1 release claims are tied to a published threshold;
- product roadmaps remain accountable to the Product Constitution’s Final Test.

**KSI is not a second north star.** The Vision north star remains: students who consistently use Kwalitec should have a materially higher probability of passing their examinations. KSI is the **operational usefulness index** that measures whether the product is educationally useful enough to support that outcome.

---

## 2. Version 1 objective

### 2.1 Objective statement

**Version 1 product success** requires the platform to achieve:

> **Kwalitec Student Index (KSI) ≥ 80**

out of 100, under the scoring methodology in this document.

### 2.2 Baseline and gap

| Measure | Value | Authority |
|---|---|---|
| Current estimated KSI | **~58** | Previous product evaluation (formalised in [`BASELINE_KSI_ASSESSMENT.md`](BASELINE_KSI_ASSESSMENT.md)) |
| Version 1 target KSI | **≥ 80** | This framework |
| Gap to close | **~22 points** | Baseline − target |

### 2.3 What Version 1 success is not

Version 1 success under this framework is **not**:

- operational GA alone (already certified separately);
- Twin Ready / production cutover claims;
- exam pass-rate proof in a live population (north-star outcome; measured later);
- recommendation-effectiveness marketing without approved evidence (EP-001 / EP-003 freeze still applies until lifted).

KSI ≥ 80 is the **educational usefulness bar** for Version 1 product readiness claims. It complements — and does not replace — EP-003 Go / No-Go educational release gates, EVF educational quality gates, and the Version 1 Release Framework (P-002.1) production-ready declaration gates.

---

## 3. Definition — Kwalitec Student Index (KSI)

### 3.1 Formal definition

The **Kwalitec Student Index (KSI)** is a weighted composite score (0–100) that estimates **how educationally useful Kwalitec is for a serious professional-exam candidate** across eight student-value categories.

KSI answers:

> If a serious student used Kwalitec as their primary study companion, how useful would it be for learning — not merely for activity, navigation, or feature presence?

### 3.2 Design principles

| Principle | Rule |
|---|---|
| Learning over activity | Scores reward learning outcomes and decision quality, not clicks, time-on-site, or vanity engagement |
| Student lens | Categories are judged from what a student can perceive and use |
| Evidence-bound | Category scores require cited evidence (interviews, blind reviews, KPIs, dogfood, support) |
| Explainable | Every category score must state why it was assigned |
| Constitution-aligned | Scores must not reward opaque AI, mastery theatre, or dual educational truths |
| Reproducible judgement | Same evidence package → same KSI within review tolerance (±3 points declared) |

### 3.3 Relationship to existing measurement systems

| System | Owns | Relationship to KSI |
|---|---|---|
| Vision 2030 Success Metrics | Long-term product outcomes | KSI categories map to Vision metrics; north star remains pass probability |
| EP-003 Educational Metrics (M1–M9) | Operational KPI formulae | Primary quantitative evidence sources for category scores |
| EP-003 Product Scorecard | Cohort decision board | Feeds KSI recalculations; does not replace KSI |
| EP-004 Blind Reviews | Student-only qualitative corpus | Primary qualitative evidence for baseline and re-scores |
| EVF Release Gate | Educational quality to release | May require KSI evidence; EVF still owns release trust law |
| Architecture / GA certification | Structural & operational readiness | Orthogonal — required but insufficient for KSI |

---

## 4. KSI categories and weightings

Weights sum to **100**. Initial weights reflect Version 1 educational priorities: the daily study loop (plan → recommend → readiness), trust (explainability), then supporting capabilities.

| ID | Category | Weight |
|---|---|---:|
| K1 | Planning usefulness | 15 |
| K2 | Recommendation usefulness | 15 |
| K3 | Readiness usefulness | 12 |
| K4 | Personalisation | 12 |
| K5 | Motivation | 10 |
| K6 | Learning analytics | 10 |
| K7 | Revision support | 12 |
| K8 | Explainability | 14 |
| | **Total** | **100** |

Weight changes require an explicit Product amendment to this document (version bump + rationale). Do not silently re-weight to greenwash a score.

---

### K1 — Planning usefulness (15%)

**Definition:** The product reliably helps the student decide *what to study now* within scarce daily time, with one coherent plan that respects syllabus structure and available study duration.

**Why it matters:** Professional exams are failed for lack of structure and consistency. Planning usefulness is the daily expression of the Vision design question: “What is the highest-value thing this student should do next?”

**Proposed measurement approach:**

- Qualitative: blind-review / interview themes on “what to study tonight,” dual-home friction, duration trust.
- Quantitative: Session start rate from plan surfaces; plan adherence / completion (M2, M4); time-to-first-Session.
- Integrity: no conflicting durations or competing “today” directives on the same day.

**Example evidence sources:** EP-004 blind reviews (Learning Workspace director; duration mismatch); M2 / M4; private-beta feedback (EDU / Session); dogfood notes.

---

### K2 — Recommendation usefulness (15%)

**Definition:** Guidance about *what to do next* (topics, missions, practice focus) is accepted as educationally helpful, evidence-based, and non-conflicting with the student’s authorised plan — without requiring the student to reverse-engineer the system.

**Why it matters:** Recommendations are how planning becomes adaptive. Useless or opaque recommendations destroy trust and revert students to external stacks (notes, Anki, CMP).

**Proposed measurement approach:**

- Qualitative: trust in guidance; conflict with Today’s Session; “would you follow this?”
- Quantitative: recommendation acceptance / follow-through (when instrumented under approved PRD); support tickets for contradictory guidance.
- Governance: effectiveness marketing remains frozen until EP-001 O8 / approved PRD evidence exists — KSI may still **score** usefulness from qualitative evidence without marketing claims.

**Example evidence sources:** Coach / Insight interview codes; EP-001 recommendation validation framework; IA-001 integrity lessons; future acceptance KPIs; product Recommendation Quality Standard + Decision Framework + Scorecard + Review Checklist (`knowledge/product/p001_3_recommendation_quality_standard/`).

**Product law:** Student-facing quality principles, dimensions, prioritisation, scorecard metrics, and the EP/P review gate live in P-001.3 (`RECOMMENDATION_QUALITY_STANDARD.md`). K2 improvement claims require checklist Pass per `knowledge/GOVERNANCE.md` §4.3. Complementary to P-001.2 Explainability Standard (selection/priority vs speech).

---

### K3 — Readiness usefulness (12%)

**Definition:** Readiness and progress signals help the student understand whether they are prepared, what is unknown, and what blocks progress — without false certainty or mastery theatre.

**Why it matters:** Students need objective feedback. Inflated readiness harms pass probability; empty or unpackable readiness fails the “how am I progressing?” design question.

**Proposed measurement approach:**

- Qualitative: honesty of empty states; interpretability of composites; overconfidence risk (resitter personas).
- Quantitative: M8 time-to-readiness (exploratory until calibrated); readiness claim-safety incidents; Twin explainability interview codes.
- Integrity: absence of evidence must remain unknown; no Exam Ready marketing without gates.

**Example evidence sources:** EP-003 Version 1 Educational Review (Twin / Journey); EP-004 readiness themes; Go / No-Go readiness gates; Twin authority soak evidence (architectural honesty, not student claim).

---

### K4 — Personalisation (12%)

**Definition:** The study experience adapts to the student’s exam, progress, available time, and evidenced strengths/weaknesses — rather than presenting a generic one-size path dressed as personal.

**Why it matters:** Professional candidates have scarce, irregular time and non-identical gaps. Personalisation that is merely cosmetic fails Educational Constitution obligations to evidence-based guidance.

**Proposed measurement approach:**

- Qualitative: “did it feel like *my* plan?”; adaptation after poor practice / missed days.
- Quantitative: plan/topic diversity vs syllabus coverage; recovery after abandon; Twin-driven surface eligibility honesty.
- Integrity: personalisation must cite evidence; must not invent student state.

**Example evidence sources:** Blind-review adaptation / recoverability personas; Digital Twin provenance; Session objective specificity.

---

### K5 — Motivation (10%)

**Definition:** The product sustains consistent study behaviour through clarity, honest encouragement, and recoverable restarts — without gamification that rewards activity over learning, and without shaming.

**Why it matters:** Consistency is a Vision success metric and Educational Principle. Motivation that creates busywork or false confidence violates the Never-Build list.

**Proposed measurement approach:**

- Qualitative: return after missed days; tone trust (honest vs hype); overwhelm vs guided.
- Quantitative: M6 study consistency; M7 learning continuity; retention / WAL.
- Integrity: no artificial streak pressure that encourages unhealthy habits.

**Example evidence sources:** EP-003 scorecard retention rows; EP-004 habit / motivation personas; support friction.

---

### K6 — Learning analytics (10%)

**Definition:** Students (and operators, where appropriate) can see learning-relevant progress signals that improve decisions — not vanity dashboards that reward activity.

**Why it matters:** Analytics without educational meaning creates the illusion of progress. Vision philosophy: measure learning, not activity.

**Proposed measurement approach:**

- Qualitative: can the student explain progress in one sentence after using Journey / analytics surfaces?
- Quantitative: M5 curriculum progress velocity (label provisional where emit deferred); reflection completion M3; founder scorecard use.
- Integrity: analytics must not invent educational scores; privacy and Educational State boundaries preserved.

**Example evidence sources:** EP-002 / product analytics architecture constraints; Journey usefulness review; EVENT_CATALOGUE; private-beta feedback on Analytics.

---

### K7 — Revision support (12%)

**Definition:** The product helps students revise intelligently — prioritising weak or exam-critical material, supporting spaced return, and connecting revision to evidenced gaps rather than random re-reading.

**Why it matters:** Professional exams are won in revision as much as first-pass learning. Weak revision support leaves candidates in external tools and breaks the companion promise.

**Proposed measurement approach:**

- Qualitative: revision workspace usefulness; “did revision change what I practised?”
- Quantitative: revision adherence (Vision metric); return-to-topic after weak evidence; Revision Workspace completion patterns.
- Integrity: revision prompts must not contradict Learning Mode / Current Learning Topic law without authority.

**Example evidence sources:** Product Blueprint Revision Workspace scope; Vision revision adherence; future revision KPIs; blind-review deliberate-practice themes.

---

### K8 — Explainability (14%)

**Definition:** Every material guidance product (plan, recommendation, readiness, coach narrative) can be understood in plain language from identifiable inputs — what the system knows, what it estimates, why it recommends, and what happens next.

**Why it matters:** Architecture Constitution Article IV and Vision AI philosophy forbid opaque recommendations. Blind-review corpus shows near-universal distrust when Coach restates “highest-value” language without showing working.

**Proposed measurement approach:**

- Qualitative: “did you understand *why*?”; unpackability of readiness/coach; conflict detection.
- Quantitative: trust-in-guidance interview rates (scorecard §2.8); educational honesty incidents; explainability support tickets.
- Integrity: if it cannot be explained, it must not be shown as educational guidance.

**Example evidence sources:** Architecture Constitution Art. IV; EP-004 Coach themes; EducationalExplainability / Insight presentation consolidation; interview trust codes; product Explainability Standard + Review Checklist (`knowledge/product/p001_2_explainability_standard/`).

**Product law:** Student-facing levels, Mandatory Explanation Schema, patterns, and the EP/P review gate live in P-001.2 (`EXPLAINABILITY_STANDARD.md`). K8 improvement claims require checklist Pass per `knowledge/GOVERNANCE.md` §4.2.

---

## 5. Scoring methodology

### 5.1 Category score scale (0–100)

Each category receives an integer score **0–100**:

| Band | Score | Meaning |
|---|---|---|
| Absent / harmful | 0–24 | Missing, contradictory, or actively misleading for learning |
| Weak | 25–49 | Present but unreliable, untrusted, or frequently unused |
| Partial | 50–69 | Helpful in some contexts; material gaps remain |
| Strong | 70–84 | Consistently useful for most serious students in scope |
| Excellent | 85–100 | Dependably useful; residual gaps are edge cases |

Mid-band scores (e.g. 58) are allowed when evidence is mixed. Prefer the **lower** score when evidence conflicts (honesty before optimism).

### 5.2 Composite formula

\[
\mathrm{KSI} = \sum_{i \in \{K1..K8\}} \left( \frac{w_i}{100} \times s_i \right)
\]

Where \(w_i\) is the category weight and \(s_i\) is the category score (0–100).

Round the published KSI to the nearest integer. Retain one decimal in working papers if useful.

### 5.3 Evidence requirements per score

A category score is **valid** only if the assessment records:

1. **Evidence package ID / paths** (reviews, scorecards, interviews, dogfood).
2. **Scoring rationale** (2–6 sentences).
3. **Confidence** — High / Medium / Low.
4. **Limitations** (sample size, provisional metrics, excluded claims).

Scores without evidence are forbidden. Placeholder “TBD = 70” is forbidden.

### 5.4 Recalculation cadence

| Trigger | Action |
|---|---|
| End of private-beta review window | Recalculate KSI from scorecard + interviews |
| Major EP/P programme exit that claims student-visible educational change | Update affected category scores; recompute KSI |
| Weight / methodology amendment | Version bump; restate baseline comparability |
| Marketing or V1 educational claim | Require current KSI assessment ≤ 90 days old |

### 5.5 Tolerance and dispute

Independent re-score of the same evidence package should agree within **±3 KSI points**. Larger divergence → STOP, document disagreement, escalate to Product owner before publishing.

### 5.6 Validated vs estimated assessments

| Kind | Role | May satisfy Gate G1 / V1-K1? |
|---|---|---|
| **Estimated** programme ΔKSI | Planning and prioritisation at EP/P entry/exit | **No** |
| **Validated** KSI assessment | Evidence-bound re-score of current claim window (paths, rationales, confidence, limitations) | **Yes** — when current (≤ 90 days) and methodology-compliant |

**Rule:** Do not sum overlapping programme estimates into a composite “current KSI.” De-duplicate category lifts, separate production-default vs flag-gated claim windows, and prefer the lower score when structural eligibility and student-perception evidence conflict.

**Current validated assessment (W-PROD):** [`../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`](../ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md) (assembled 2026-07-26; methodology in the same folder). This pointer does not change category weights or the ≥ 80 threshold.

---

## 6. Target threshold

| Threshold | Meaning |
|---|---|
| **KSI ≥ 80** | Version 1 educational usefulness target met |
| **70 ≤ KSI < 80** | Approaching Version 1; ship only with explicit holds and no overclaim |
| **KSI < 70** | Not Version 1 educationally useful enough for success claims |
| **KSI < baseline − 5** | Regression — investigate before further feature expansion |

The **≥ 80** threshold is binding for Version 1 product-success claims under this framework.

---

## 7. Version 1 release criteria (KSI lens)

Version 1 may be declared **educationally successful under P-001** only when all of the following hold:

| # | Criterion |
|---|---|
| V1-K1 | Published KSI ≥ 80 with High or Medium confidence |
| V1-K2 | No category scored below **50** (no critical weak pillar) |
| V1-K3 | K8 Explainability ≥ **70** (constitutional explainability floor) |
| V1-K4 | Student Impact Assessments filed for all material EP/P programmes since this framework’s effective date |
| V1-K5 | EP-003 / EP-004 educational Go / No-Go not in **NO-GO** for the same claim window |
| V1-K6 | No active educational honesty incident unresolved (dual truth, false readiness marketing, opaque AI guidance shipped as fact) |
| V1-K7 | Claim language distinguishes KSI usefulness from exam pass-rate proof |

Operational GA and architecture certification remain necessary but are **not sufficient**.

### 7.1 Relationship to Version 1 Release Framework (P-002.1)

V1-K1…V1-K7 are the **KSI-lens** criteria. They are necessary for educational usefulness claims and are embedded as Gate **G1** (plus cross-links in G2–G4) of the permanent Version 1 Release Framework:

| Artefact | Path |
|---|---|
| Version 1 Release Framework | `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md` |
| Acceptance Checklist | `…/VERSION_1_ACCEPTANCE_CHECKLIST.md` |
| Go / No-Go Guide | `…/VERSION_1_GO_NO_GO_GUIDE.md` |
| Evidence Requirements | `…/VERSION_1_EVIDENCE_REQUIREMENTS.md` |

**Rule:** Estimated programme ΔKSI does **not** satisfy V1-K1 for a Version 1 production-ready declaration. Gate G1 requires a **validated** KSI assessment (evidence-bound re-score ≤ 90 days old).  

**Rule:** Satisfying V1-K1…V1-K7 alone does **not** authorise “Version 1 production-ready.” P-002.1 also requires constitutional, quality-contract, performance, reliability, telemetry, security, test, and feature-flag gates.  

**Authority split:** This framework owns *how useful is educational enough*. P-002.1 owns *when Version 1 may be declared production-ready*. Vision 2030 remains the Product Constitution; EVF remains educational trust-to-release law.

---

## 8. Relationship between KSI and future product roadmaps

### 8.1 Prioritisation rule

Roadmap items and EP/P programmes must be ordered primarily by **expected KSI contribution** toward closing the gap from baseline (~58) to target (80), subject to constitutional and architectural constraints.

When two initiatives have similar cost/risk, prefer the one with higher estimated positive impact on the **lowest-scoring material categories**.

### 8.2 Programme entry gate

Before authorising a material EP or P programme:

1. Complete a draft [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md) (may be preliminary).
2. State **Estimated KSI contribution** (category deltas and net KSI points).
3. Cite which baseline gaps the work attacks.
4. Pass Vision Final Test.

Programmes that cannot articulate student/KSI benefit should not start (exceptions: pure security, pure compliance, pure docs/governance, pure operational reliability with no educational claim).

### 8.3 Programme exit gate

Every future **EP** or **P** programme completion report must include:

| Required section | Content |
|---|---|
| Student Impact Assessment | Completed template (or link to filled assessment) |
| Estimated KSI contribution | Category deltas + net points (can be 0 for infra-only) |
| Evidence collected | Paths to tests, reviews, metrics, dogfood |
| Lessons learned for student value | What the work taught about usefulness |

See [`knowledge/GOVERNANCE.md`](../../GOVERNANCE.md) and `.cursor/rules/07-reporting.mdc`.

### 8.4 Roadmap tiers (illustrative)

| Tier | Use when |
|---|---|
| **KSI-critical** | Directly raises K1–K8 scores that block V1-K1 / V1-K2 / V1-K3 |
| **KSI-supporting** | Improves evidence quality, measurement, or integrity without large score lifts |
| **Non-KSI** | Necessary engineering with explicit zero student-usefulness claim |

Non-KSI work is allowed; it must not be marketed as educational usefulness progress.

### 8.5 Compatibility with Product Blueprint roadmap

Blueprint Version 1 / Version 2 epic framing remains the strategic capability map. **KSI governs whether capability work actually improved usefulness.** Blueprint says what exists; KSI says how useful it is.

---

## 9. Alignment with constitutions

| Constitution | Alignment obligation |
|---|---|
| Product Vision 2030 | KSI serves north star + Final Test; never replaces them; Never-Build list constrains motivational scoring |
| Educational Constitution | Evidence before certainty; syllabus order; lawful educational meaning |
| Architecture Constitution | Determinism, explainability, no invented educational truth; presentation ≠ authority |
| EVF | KSI informs quality judgement; EVF still owns educational release gate |

If KSI scoring would reward a constitutionally forbidden behaviour (e.g. opaque AI, mastery theatre), the score must be reduced — constitutions win.

---

## 10. Amendment

Amendments require:

1. Product owner approval.
2. Version bump on this document.
3. Note on baseline comparability (re-score required or not).
4. Update to [`BASELINE_KSI_ASSESSMENT.md`](BASELINE_KSI_ASSESSMENT.md) if weights change.

---

## References

- [`BASELINE_KSI_ASSESSMENT.md`](BASELINE_KSI_ASSESSMENT.md)
- [`STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md`](STUDENT_IMPACT_ASSESSMENT_TEMPLATE.md)
- `knowledge/product/ep005_1_ksi_validation_evidence/VALIDATED_KSI_REPORT.md`
- `knowledge/product/vision/PRODUCT_VISION_2030.md`
- `PRODUCT_BLUEPRINT.md`
- `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`
- `docs/ARCHITECTURE_CONSTITUTION.md`
- `knowledge/product/ep003_educational_effectiveness/`
- `knowledge/product/ep004_private_beta/`
- `knowledge/product/p002_1_version_1_release_framework/VERSION_1_RELEASE_FRAMEWORK.md`

---

**End of PRODUCT_SUCCESS_FRAMEWORK**

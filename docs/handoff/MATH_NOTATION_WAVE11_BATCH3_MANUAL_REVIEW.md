# Wave 11 Mathematical Notation - Manual-Review Proposals (Batch 3)

**Status:** Proposal only (not applied)  
**Date:** 2026-09-08  
**Scope:** Batch 3 of the catalogue-wide `correctly_excluded` + `needs_manual_review` population (62 of the 115 still pending after Batches 1–2)  
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md` (semantic-role test)  
**Ledger:** `docs/content/math_notation_inventory.json` (fingerprint `66ad0532050967bb82c1b07573d832825118b5247afd4f4086aea32ca111e4c9`, generated `2026-09-08T07:05:34Z`)  
**Prior batches:** `docs/handoff/MATH_NOTATION_WAVE11_MANUAL_REVIEW.md` (Batch 1: 64 of original 239); `docs/handoff/MATH_NOTATION_WAVE11_BATCH2_MANUAL_REVIEW.md` (Batch 2: 60 of the 175 remaining after Batch 1)

## Confirmed remaining population

Query on the live ledger:

- `category` = `correctly_excluded`
- `needs_manual_review` = `true`
- `migration_status` = `pending`

**Count: 115** (matches Batch 2 remainder tracker: 239 − 64 − 60 = 115; also matches ledger `totals.needs_manual_review` and `limits_of_automation.needs_manual_review_count`).

**Reason mix (115):** `isolated_symbol_in_narrative_ambiguous` 92 · `mathish_role_unclear` 23.

**Order:** syllabus / package-filename order (same rule as Batches 1–2), **not** raw ledger `packages` list order. First remaining package is `4.2.4-factors-interactions-cs1014.json`; last is `revision-sampling-distributions-cs1009.json` (**33** packages). Package set and per-package counts match Batch 2’s remainder table exactly.

Reusable distinctions (unchanged from Waves 1–10 and Batches 1–2):

- A symbol naming a topic or category in the abstract (mission chrome, schematic paths, metalinguistic gloss) is prose.
- The same symbol inside a concrete equation, pivot, or instruction to compute a real value is mathematics.
- A function or statistic name used to warn against a shallow reading is prose; the same characters forming a real expression the student works with are mathematics.
- Mostly-English definitional statements get only their genuine symbolic content wrapped (migrate partial).
- Numeric `±` / `×` constructions in attempt cues are live evaluation objects (migrate), matching Wave 10 / Batches 1–2.
- Standard §3.2 (“unbiased for μ” style naming in explanatory prose) stays exclude.
- `η forms` / `Family → η → link` style syllabus-path naming in mission / out-of-scope chrome excludes (Waves 3, 6, 7; Batch 2).
- Fit-measure / GOF-test topic naming in schematic titles / concept paths / expected-benefit skill lists excludes; the same statistic as a step target, sum target, or decision object migrates (partial) (Wave 4 / Wave 7 / Batch 2).
- Credibility weight `Z`, `X̄`, `μ`, and `1 − Z` as live premium structure migrate (Wave 6 / Wave 7); the same letters only as deferred-theory chrome may exclude (verify each instance).

---

## Batch 3 selection

**Selection rule:** continue syllabus / package-filename order from `4.2.4-factors-interactions-cs1014.json` through `5.1.6-credibility-premium-cs1003.json` inclusive.

**Why this cut:**

1. Coherent topic arc (factors twin close-out → linear predictor → deviance / model choice → GOF → prior/posterior → loss → credible intervals → first credibility-premium twin), so one reviewer can hold a stable set of distinctions.
2. Lands on **62** items without splitting a package mid-board (**14** packages), within the requested ~60 band (stopping after `5.1.5` would yield 55; adding the cs1015 credibility twin would jump to 69).
3. Mirrors Batch 2’s twin split (ended at `4.2.4-…-cs1003`, left `4.2.4-…-cs1014` for Batch 3): Batch 3 takes `5.1.6-…-cs1003` and leaves `5.1.6-…-cs1015` for Batch 4.
4. Leaves a clean remainder tracker: **53** items in **19** packages starting at `5.1.6-credibility-premium-cs1015.json`.

**Batch 3 reason mix:** `isolated_symbol_in_narrative_ambiguous` 57 · `mathish_role_unclear` 5.

**Batch 3 packages (14):**

| Package | N |
|---|---:|
| `4.2.4-factors-interactions-cs1014.json` | 4 |
| `4.2.5-linear-predictor-cs1003.json` | 11 |
| `4.2.5-linear-predictor-cs1014.json` | 8 |
| `4.2.6-deviance-estimation-cs1014.json` | 1 |
| `4.2.7-model-choice-cs1003.json` | 2 |
| `4.2.7-model-choice-cs1014.json` | 1 |
| `4.2.9-goodness-tests-cs1003.json` | 5 |
| `4.2.9-goodness-tests-cs1014.json` | 7 |
| `5.1.2-prior-posterior-cs1003.json` | 4 |
| `5.1.2-prior-posterior-cs1015.json` | 4 |
| `5.1.3-posterior-simple-cs1015.json` | 1 |
| `5.1.4-loss-estimators-cs1015.json` | 1 |
| `5.1.5-credible-intervals-cs1015.json` | 6 |
| `5.1.6-credibility-premium-cs1003.json` | 7 |

**Remainder for later batches (not reviewed here):** packages from `5.1.6-credibility-premium-cs1015.json` through `revision-sampling-distributions-cs1009.json` (53 strings).

Note: some Batch 3 *packages* appeared in earlier wave leftover docs for **different** field paths (e.g. Wave 6 on `4.2.4-cs1014` / `4.2.5` mission and worked-example equations; Wave 4 / Wave 7 on GOF and credibility fields already migrated; Wave 9–10 on prior/posterior and credible-interval twins). Those prior proposals do not cover these ledger rows; each string below is first-pass review for this population. Where the **same term** recurs (η, χ² / X², θ, Z, α/β), each instance is classified from its own field role, not copied from a sibling.

---

## Proposed classifications

### 1. `4.2.4-factors-interactions-cs1014.json` · `mission.success_criteria[2]`

**Original:** Refuse one 'I wrote η, so I finished today's LO' claim.

**Why flagged:** Success-criterion chrome with Greek η (`isolated_symbol_in_narrative_ambiguous`).

**Proposal: exclude.** η sits inside a shallow-completion slogan the student must refuse. Metalinguistic warning about LO finish, not a live predictor to evaluate. Parallel to Wave 6 “refuse treating η-form writing as today's LO” and Batch 2 shallow-reading exclusions.

---

### 2. `4.2.4-factors-interactions-cs1014.json` · `mission.task_descriptions[2]`

**Original:** Closed-book Knowledge Checks: factors + refuse η swallow.

**Why flagged:** Task-description chrome with η.

**Proposal: exclude.** “refuse η swallow” names a shallow-reading refusal in KC task chrome, not an equation board. Matches the reusable “warn against shallow reading → exclude” distinction.

---

### 3. `4.2.4-factors-interactions-cs1014.json` · `reading_guidance.misconception_watch[1]`

**Original:** Watch for jumping to full η polynomial forms (4.2.5) as today's finish.

**Why flagged:** Misconception-watch with η.

**Proposal: exclude.** “η polynomial forms (4.2.5)” names a deferred syllabus object / premature-finish path (Wave 6 / Batch 2 out-of-scope and why-now η-forms exclusions), not a live polynomial predictor to write today.

---

### 4. `4.2.4-factors-interactions-cs1014.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Plug the factor indicators into η, remembering the interaction is zero unless both factors equal 1.

**Why flagged:** Attempt-before-reveal with η.

**Proposal: migrate (partial).** η is the live linear-predictor object the student must plug indicators into before reveal (twin of Batch 2 item 60 on `4.2.4-…-cs1003`: “Plug indicator patterns into η…”). “CMP closed”, “Plug the factor indicators into …, remembering the interaction is zero unless both factors equal 1” stays framing prose around that object.

---

### 5. `4.2.5-linear-predictor-cs1003.json` · `mission.mission_purpose`

**Original:** Today's Mission exists to define the linear predictor and write its form for simple models including polynomials and factors. So η is concrete.

**Why flagged:** Mission-purpose chrome with η.

**Proposal: exclude.** “So η is concrete” is pedagogical literacy chrome naming the day’s object class, not posing η = … or another live expression (contrast Wave 6 migrate-partial of mission chrome that embeds η = Xβ).

---

### 6. `4.2.5-linear-predictor-cs1003.json` · `mission.educational_intent`

**Original:** Produce concrete η literacy.

**Why flagged:** Educational-intent chrome with η.

**Proposal: exclude.** “η literacy” is a metalinguistic learning-goal label, not a live predictor equation.

---

### 7. `4.2.5-linear-predictor-cs1003.json` · `mission.expected_benefit`

**Original:** Study Progress for η forms. Not deviance estimation as primary.

**Why flagged:** Expected-benefit chrome with η forms.

**Proposal: exclude.** “η forms” is syllabus/topic naming of Study Progress scope (Waves 3, 6; Batch 2), with deviance deferred as out-of-primary. No live expression.

---

### 8. `4.2.5-linear-predictor-cs1003.json` · `mission.success_criteria[0]`

**Original:** Closed-book, write η for a simple continuous model and a factor model.

**Why flagged:** Success criterion requiring writing η.

**Proposal: migrate (partial).** η is the live linear-predictor object the criterion requires the student to produce for two model types (distinct from “η forms” activity naming in chrome). “Closed-book, write … for a simple continuous model and a factor model” stays criterion framing.

---

### 9. `4.2.5-linear-predictor-cs1003.json` · `mission.success_criteria[2]`

**Original:** Refuse conflating η with the link.

**Why flagged:** Success-criterion refuse clause with η.

**Proposal: exclude.** “conflating η with the link” is a discrimination / shallow-reading refusal in success chrome (parallel to Wave 6 “Refuse η/link conflation” prose and Batch 2 refuse-η exclusions), not a live g(μ)=η board in this field.

---

### 10. `4.2.5-linear-predictor-cs1003.json` · `mission.task_descriptions[0]`

**Original:** Write two η sketches before CMP.

**Why flagged:** Task description with η.

**Proposal: exclude.** “η sketches” names the pre-CMP activity genre (same family as “η forms” topic/activity naming in Wave 6 prior-bridge and Batch 2), not a concrete η = … expression.

---

### 11. `4.2.5-linear-predictor-cs1003.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Compute x² first, then form η before exponentiating.

**Why flagged:** Attempt-before-reveal with x² and η.

**Proposal: migrate (partial).** x² and η are the live constructed-covariate and linear-predictor objects the student must form before the inverse link. “CMP closed”, “Compute … first, then form … before exponentiating” stays framing.

---

### 12. `4.2.5-linear-predictor-cs1003.json` · `worked_example.steps[0].explanation`

**Original:** The linear predictor is linear in the parameters even when it includes x² as a constructed covariate.

**Why flagged:** Step explanation with x² (`mathish_role_unclear`).

**Proposal: migrate (partial).** x² is the live constructed covariate named inside the linearity-in-parameters claim (genuine symbolic content in mostly-English definitional prose). Surrounding “The linear predictor is linear in the parameters even when it includes … as a constructed covariate” stays instructional prose.

---

### 13. `4.2.5-linear-predictor-cs1003.json` · `worked_example.steps[2].attempt_cue`

**Original:** State what η is versus μ.

**Why flagged:** Attempt cue contrasting η and μ.

**Proposal: migrate (partial).** η and μ are the live link-scale vs response-scale objects this step asks the student to distinguish (parallel to Batch 2 migrate-partial of “Link maps μ to η”). “State what … is versus …” stays cue framing. Distinct from mission “refuse conflating η with the link” chrome (item 9), which never poses the two objects as a board contrast.

---

### 14. `4.2.5-linear-predictor-cs1003.json` · `worked_example.steps[2].explanation`

**Original:** η is the linear predictor on the link scale; μ is the mean on the response scale after the inverse link.

**Why flagged:** Step explanation defining η vs μ.

**Proposal: migrate (partial).** η and μ are the live scale objects in the definition (Batch 2 / Wave 7 link-definition migrate-partial pattern). The English scale/link clauses stay instructional prose around those objects.

---

### 15. `4.2.5-linear-predictor-cs1003.json` · `worked_example.common_pitfall`

**Original:** Reporting η as the mean severity, or dropping the quadratic term when x² is part of the specified linear predictor.

**Why flagged:** Common-pitfall with η and x².

**Proposal: migrate (partial).** η (misreported as mean) and x² (dropped term) are the live wrong-path objects. “Reporting … as the mean severity, or dropping the quadratic term when … is part of the specified linear predictor” stays pitfall prose.

---

### 16. `4.2.5-linear-predictor-cs1014.json` · `mission.tutor_intent`

**Original:** Today I will force η-form writing for simple GLM structures and refuse treating deviance as today's LO.

**Why flagged:** Tutor-intent chrome with η-form.

**Proposal: exclude.** “η-form writing” is metalinguistic activity naming (Wave 6 twin package tutor-intent exclude on factors; Batch 2 “write η forms” tutor chrome exclude). Deviance clause is deferred-LO chrome.

---

### 17. `4.2.5-linear-predictor-cs1014.json` · `mission.why_now`

**Original:** 4.2.5 is contiguous after factors. Without η forms, deviance and software fit lack structure.

**Why flagged:** Why-now chrome with η forms.

**Proposal: exclude.** “η forms” names the syllabus hinge object in sequencing prose (Wave 6 why-now η-forms exclusions), not a live predictor to evaluate here.

---

### 18. `4.2.5-linear-predictor-cs1014.json` · `mission.success_criteria[0]`

**Original:** Closed-book, define the linear predictor η.

**Why flagged:** Success criterion naming η.

**Proposal: migrate (partial).** η is the live object the criterion requires defining (same role family as item 8’s “write η …”, not “η forms” chrome). “Closed-book, define the linear predictor” stays framing.

---

### 19. `4.2.5-linear-predictor-cs1014.json` · `mission.task_descriptions[0]`

**Original:** Sketch η forms before CMP.

**Why flagged:** Task description with η forms.

**Proposal: exclude.** “η forms” is pre-CMP activity/topic naming (item 10 parallel), not a concrete expression board.

---

### 20. `4.2.5-linear-predictor-cs1014.json` · `mission.task_descriptions[2]`

**Original:** Closed-book Knowledge Checks: η forms + refuse deviance swallow.

**Why flagged:** Task-description chrome with η forms.

**Proposal: exclude.** η forms + refuse-deviance is KC chrome naming today’s literacy vs deferred LO, not live math.

---

### 21. `4.2.5-linear-predictor-cs1014.json` · `reading_guidance.misconception_watch[0]`

**Original:** Watch for equating η with μ without the link.

**Why flagged:** Misconception-watch with η and μ.

**Proposal: migrate (partial).** η and μ are the live objects of the forbidden identification (student must keep them distinct via the link). “Watch for equating … with … without the link” stays watch framing. Distinct from item 9’s mission refuse chrome, which never pairs the two symbols as a board contrast; here both symbols are the discrimination payload.

---

### 22. `4.2.5-linear-predictor-cs1014.json` · `knowledge_checks[1].explanation`

**Original:** Specified eta includes x, x squared, and cover indicator. Link maps μ to η; they are distinct objects.

**Why flagged:** KC explanation with μ / η (and English “eta”).

**Proposal: migrate (partial).** μ and η are the live link-mapping objects (Batch 2 twin wording on link packages). English “eta”, “x”, “x squared”, and “cover indicator” stay covariate-list / warning prose unless separately treated; the μ↔η distinction is the symbolic payload.

---

### 23. `4.2.5-linear-predictor-cs1014.json` · `worked_example.steps[0].label`

**Original:** Write η as xᵀβ

**Why flagged:** Step label with η / xᵀβ.

**Proposal: migrate (partial).** η as xᵀβ (i.e. the live η = xᵀβ form) is the step’s writing target (Wave 6 migrate-partial of η = xᵀβ in this package family). “Write” stays label framing.

---

### 24. `4.2.6-deviance-estimation-cs1014.json` · `mission.educational_intent`

**Original:** Produce a cognitive move from η forms to lawful deviance and parameter estimation under CMP.

**Why flagged:** Educational-intent chrome with η forms.

**Proposal: exclude.** “η forms” names the prior literacy stage in a pedagogical trajectory, not a live predictor equation on this deviance mission.

---

### 25. `4.2.7-model-choice-cs1003.json` · `mission.task_descriptions[2]`

**Original:** Knowledge Checks: Δ deviance + refuse kitchen-sink.

**Why flagged:** Task description with Δ deviance.

**Proposal: exclude.** “Δ deviance” is English topic/activity naming for the KC (not the live ΔD = D_R − D_F identity). “refuse kitchen-sink” is shallow-reading chrome. Contrast Wave 7 migrate of explicit ΔD equations elsewhere on model-choice boards.

---

### 26. `4.2.7-model-choice-cs1003.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Form ΔD before comparing to the chi-square critical value.

**Why flagged:** Attempt-before-reveal with ΔD.

**Proposal: migrate (partial).** ΔD is the live nested-deviance difference the student must form before reveal (Wave 7 “Form ΔD = …” family). “CMP closed”, “Form … before comparing to the chi-square critical value” stays framing (English “chi-square” as critical-value name, not a typeset χ² expression in this field).

---

### 27. `4.2.7-model-choice-cs1014.json` · `worked_example.steps[1].explanation`

**Original:** Reject the reduced model when ΔD exceeds the χ² critical value.

**Why flagged:** Step explanation with ΔD and χ².

**Proposal: migrate (partial).** ΔD and χ² are the live decision objects for the nested-model reject call (Wave 7 migrate-partial of ΔD vs χ² critical comparisons). “Reject the reduced model when … exceeds the … critical value” stays decision-rule prose.

---

### 28. `4.2.9-goodness-tests-cs1003.json` · `mission.concept_focus`

**Original:** Fitted GLM → Pearson χ² acceptability test → likelihood-ratio test.

**Why flagged:** Concept-focus schematic path with χ².

**Proposal: exclude.** Pearson χ² here names the GOF-test topic in a schematic path (Wave 4 CMP/syllabus Pearson χ² topic-name exclude; Wave 7 / Batch 2 schematic-path exclusions), not a live sum-to-χ² calculation.

---

### 29. `4.2.9-goodness-tests-cs1003.json` · `mission.expected_benefit`

**Original:** You will be able to apply Pearson's χ² and likelihood-ratio tests to judge acceptability of a fitted GLM.

**Why flagged:** Expected-benefit skill statement with χ².

**Proposal: exclude.** Pearson's χ² names the test type in a skill/outcome sentence, not a live statistic evaluation on a board. Same topic-naming role as item 28, different surface.

---

### 30. `4.2.9-goodness-tests-cs1003.json` · `mission.success_criteria[0]`

**Original:** Closed-book, name Pearson χ² and likelihood-ratio tests in GLM context.

**Why flagged:** Success criterion asking to name χ² tests.

**Proposal: exclude.** The verb is “name … tests”: metalinguistic recall of test labels, not computing or selecting on a live X² / χ² value. Distinct from step labels that target the live statistic (item 32).

---

### 31. `4.2.9-goodness-tests-cs1003.json` · `reading_guidance.open_point`

**Original:** CMP · Syllabus 4.2.9 Pearson χ² and likelihood-ratio tests

**Why flagged:** Open-point CMP path with χ².

**Proposal: exclude.** Exact Wave 4 syllabus-path exclusion pattern: Pearson χ² names the CMP topic in a reading open line.

---

### 32. `4.2.9-goodness-tests-cs1003.json` · `worked_example.steps[0].label`

**Original:** Pearson X²

**Why flagged:** Step label with X² (`mathish_role_unclear`).

**Proposal: migrate (partial).** X² is the live Pearson GOF statistic this step produces (Batch 2 “Pearson χ²” / “Sum to χ²” migrate-partial; Wave 4 Pearson X² as live aggregate check). “Pearson” names the statistic type around that object.

---

### 33. `4.2.9-goodness-tests-cs1014.json` · `mission.tutor_intent`

**Original:** Today I will force χ² vs LRT acceptability discrimination and refuse treating full software interpretation as today's LO.

**Why flagged:** Tutor-intent chrome with χ².

**Proposal: exclude.** “χ² vs LRT acceptability discrimination” names the pedagogical discrimination topic in tutor chrome, not a live GOF sum. Software-interpretation clause is deferred-LO refuse.

---

### 34. `4.2.9-goodness-tests-cs1014.json` · `mission.concept_focus`

**Original:** Fitted GLM → Pearson χ² acceptability test → likelihood-ratio test.

**Why flagged:** Same wording / role as item 28 on the twin.

**Proposal: exclude.** Same schematic-path topic naming as item 28.

---

### 35. `4.2.9-goodness-tests-cs1014.json` · `mission.expected_benefit`

**Original:** You will be able to apply Pearson's χ² and likelihood-ratio tests to judge acceptability of a fitted GLM.

**Why flagged:** Same wording / role as item 29 on the twin.

**Proposal: exclude.** Same skill-list topic naming as item 29.

---

### 36. `4.2.9-goodness-tests-cs1014.json` · `mission.task_descriptions[0]`

**Original:** Sketch χ² vs LRT before CMP.

**Why flagged:** Task description with χ² vs LRT.

**Proposal: exclude.** “Sketch χ² vs LRT” names a pre-CMP discrimination sketch (activity/topic chrome), parallel to “Sketch η forms before CMP” excludes, not a live X² evaluation.

---

### 37. `4.2.9-goodness-tests-cs1014.json` · `reading_guidance.misconception_watch[0]`

**Original:** Watch for treating a non-significant χ² as automatic model perfection.

**Why flagged:** Misconception-watch with χ².

**Proposal: migrate (partial).** χ² is the live GOF statistic being over-read (Wave 4 pitfall migrated non-significant X² as a live mathematical over-read object). “Watch for treating a non-significant … as automatic model perfection” stays watch prose. Distinct from items 28–31 / 33–36, where χ² only labels the syllabus test family.

---

### 38. `4.2.9-goodness-tests-cs1014.json` · `worked_example.steps[1].attempt_cue`

**Original:** Sum to X² and compare with 5.991.

**Why flagged:** Attempt cue with X² (`mathish_role_unclear`).

**Proposal: migrate (partial).** X² and 5.991 are the live sum target and critical value for this step (Batch 2 “Sum to χ²”; Wave 4 sum-to-Pearson cues). “Sum to … and compare with …” stays cue framing.

---

### 39. `4.2.9-goodness-tests-cs1014.json` · `worked_example.steps[1].explanation`

**Original:** Large X² rejects aggregate adequacy of the fitted means.

**Why flagged:** Step explanation with X² (`mathish_role_unclear`).

**Proposal: migrate (partial).** X² is the live decision statistic (Wave 4 “when X² is below the critical value” migrate family). “Large … rejects aggregate adequacy of the fitted means” stays decision-rule prose.

---

### 40. `5.1.2-prior-posterior-cs1003.json` · `worked_example.given[0].note`

**Original:** conjugate prior for θ

**Why flagged:** Given note with θ.

**Proposal: migrate (partial).** θ is the live prior parameter on this board’s given row (Wave 10 “posterior for θ” migrate-partial twin pattern). “conjugate prior for” stays framing.

---

### 41. `5.1.2-prior-posterior-cs1003.json` · `worked_example.steps[1].attempt_cue`

**Original:** Update α and β with the Binomial counts.

**Why flagged:** Attempt cue with α and β.

**Proposal: migrate (partial).** α and β are the live Beta hyperparameters the student must update (Wave 9 / Wave 10 Beta-update cues). “Update … with the Binomial counts” stays instructional framing.

---

### 42. `5.1.2-prior-posterior-cs1003.json` · `worked_example.steps[1].explanation`

**Original:** Conjugacy adds successes to α and failures to β.

**Why flagged:** Step explanation with α and β.

**Proposal: migrate (partial).** α and β are the live update targets in the conjugacy rule. “Conjugacy adds successes to … and failures to …” stays explanatory prose around those objects.

---

### 43. `5.1.2-prior-posterior-cs1003.json` · `worked_example.common_pitfall`

**Original:** Updating as Beta(α+n, β+s) or forgetting to add failures n − s to β.

**Why flagged:** Common-pitfall with Beta(α+n, β+s) and n − s (`isolated_symbol_in_narrative_ambiguous`).

**Proposal: migrate (partial).** Beta(α+n, β+s), n − s, and β are the live wrong/right update objects (Wave 10 Beta(α, β) pitfall migrate-partial). “Updating as … or forgetting to add failures … to …” stays pitfall prose.

---

### 44. `5.1.2-prior-posterior-cs1015.json` · `worked_example.given[0].note`

**Original:** prior for θ

**Why flagged:** Given note with θ.

**Proposal: migrate (partial).** θ is the live prior parameter on the given row (same role as item 40 / Wave 10). “prior for” stays framing.

---

### 45. `5.1.2-prior-posterior-cs1015.json` · `worked_example.steps[0].explanation`

**Original:** The prior is the distribution of θ before seeing the new sample.

**Why flagged:** Step explanation naming θ.

**Proposal: exclude.** θ is named only inside a definitional “what a prior is” sentence (Standard §3.2), with no live update expression in this field. Distinct from items 40/44 (given-row parameter tags) and item 46 (numeric Beta update).

---

### 46. `5.1.2-prior-posterior-cs1015.json` · `worked_example.steps[1].attempt_cue`

**Original:** Update to Beta(2+3, 8+10−3).

**Why flagged:** Attempt cue with Beta(…) and Unicode minus (`isolated_symbol_in_narrative_ambiguous`).

**Proposal: migrate.** Beta(2+3, 8+10−3) is the live numeric posterior-update expression for this step. “Update to” stays cue framing.

---

### 47. `5.1.2-prior-posterior-cs1015.json` · `worked_example.steps[2].explanation`

**Original:** The posterior is the distribution of θ after combining prior and likelihood.

**Why flagged:** Step explanation naming θ.

**Proposal: exclude.** Same §3.2 definitional naming of θ as item 45 (posterior definition), not a live density board. Distinct from item 49’s pure π(θ|data) notation.

---

### 48. `5.1.3-posterior-simple-cs1015.json` · `worked_example.given[0].note`

**Original:** shape-rate prior for λ

**Why flagged:** Given note with λ.

**Proposal: migrate (partial).** λ is the live rate parameter tagged on the given row (Wave 10 given-note parameter migrate-partial). “shape-rate prior for” stays framing.

---

### 49. `5.1.4-loss-estimators-cs1015.json` · `worked_example.given[1].note`

**Original:** π(θ|data)

**Why flagged:** Given note that is posterior-density notation.

**Proposal: migrate.** π(θ|data) is itself the live posterior object on the given row, not a prose gloss.

---

### 50. `5.1.5-credible-intervals-cs1015.json` · `knowledge_checks[0].explanation`

**Original:** Credible interval is posterior probability for θ. Repeated-sampling coverage slogan is the frequentist confidence interval reading unless carefully distinguished.

**Why flagged:** KC explanation naming θ.

**Proposal: exclude.** θ is named inside a definitional / contrast slogan about credible vs frequentist readings (Wave 10 exclude of “posterior probability statement about θ” style explanations). No live interval arithmetic in this field.

---

### 51. `5.1.5-credible-intervals-cs1015.json` · `worked_example.given[0].note`

**Original:** posterior for θ

**Why flagged:** Given note with θ.

**Proposal: migrate (partial).** Same Wave 10 twin-package given-note role: θ is the live posterior parameter on the given row. “posterior for” stays framing.

---

### 52. `5.1.5-credible-intervals-cs1015.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Form mean ± 1.96 × posterior SD, and phrase it as a posterior probability statement.

**Why flagged:** Attempt-before-reveal with ± / ×.

**Proposal: migrate (partial).** mean ± 1.96 × posterior SD is the live central credible-interval construction (Wave 10 twin migrate-partial). “CMP closed” and “phrase it as a posterior probability statement” stay framing.

---

### 53. `5.1.5-credible-intervals-cs1015.json` · `worked_example.steps[0].attempt_cue`

**Original:** Compute 100 ± 1.96 × 5.

**Why flagged:** Attempt cue with numeric ± / ×.

**Proposal: migrate.** 100 ± 1.96 × 5 is the live numeric interval evaluation (Wave 10 / Batches 1–2 numeric ± × cues). “Compute” stays cue prose.

---

### 54. `5.1.5-credible-intervals-cs1015.json` · `worked_example.steps[1].explanation`

**Original:** Unlike a frequentist CI, the credible interval places probability on θ given the data and prior.

**Why flagged:** Step explanation naming θ.

**Proposal: exclude.** θ is named in conceptual contrast prose (Wave 10 twin excludes for “statement about θ” / “treat θ as random”). No live interval expression here (that sits in items 52–53).

---

### 55. `5.1.5-credible-intervals-cs1015.json` · `worked_example.common_pitfall`

**Original:** Interpreting (90.2, 109.8) as a frequentist confidence interval ('95% of samples cover θ') instead of a posterior probability statement for θ.

**Why flagged:** Common-pitfall with numeric interval and θ.

**Proposal: migrate (partial).** (90.2, 109.8) is the live interval object being misread. The θ mentions inside the frequentist-slogan vs posterior-statement contrast stay instructional prose (same θ role as items 50/54). Distinct from Wave 10’s ± sd template pitfall: here the payload is the numeric interval endpoints.

---

### 56. `5.1.6-credibility-premium-cs1003.json` · `knowledge_checks[1].hints[0]`

**Original:** Compute 1 - Z first, then blend X̄ and μ.

**Why flagged:** KC hint with Z / X̄ / μ.

**Proposal: migrate (partial).** 1 - Z, X̄, and μ are the live credibility-premium ingredients (Wave 6 / Wave 7 credibility structure). “Compute … first, then blend …” stays hint framing. Verified against Wave 7’s already-migrated numeric premium explanation on this package: those rows posed full P = … arithmetic; this hint is a separate field still pending, with the same live-object role.

---

### 57. `5.1.6-credibility-premium-cs1003.json` · `knowledge_checks[1].hints[1]`

**Original:** Z weights the individual experience X̄.

**Why flagged:** KC hint with Z and X̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** Z and X̄ are the live weight and experience objects in the premium structure (Wave 7 “Z = 0.55 weights individual experience”). “weights the individual experience” stays hint prose around those objects. Not mere topic naming of “credibility weight”.

---

### 58. `5.1.6-credibility-premium-cs1003.json` · `knowledge_checks[1].success_criteria[1]`

**Original:** Uses Z on X̄ and (1 - Z) on μ.

**Why flagged:** Success criterion with Z / X̄ / μ.

**Proposal: migrate (partial).** Z, X̄, (1 - Z), and μ are the live correct weighting structure the criterion checks (Wave 6 / Wave 7 premium formula family). “Uses … on … and … on …” stays criterion framing.

---

### 59. `5.1.6-credibility-premium-cs1003.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Form the convex combination with weights Z and 1 − Z.

**Why flagged:** Attempt-before-reveal with Z and 1 − Z.

**Proposal: migrate (partial).** Z and 1 − Z are the live credibility weights the student must form (Wave 6 twin “Write P = Z X̄ + (1 − Z)μ” migrate; this field names the weights without restating the full product sum). “CMP closed” and “Form the convex combination with weights …” stays framing.

---

### 60. `5.1.6-credibility-premium-cs1003.json` · `worked_example.steps[0].attempt_cue`

**Original:** Compute 1 − Z.

**Why flagged:** Attempt cue with 1 − Z.

**Proposal: migrate.** 1 − Z is the live complementary-weight evaluation for this step. “Compute” stays cue prose.

---

### 61. `5.1.6-credibility-premium-cs1003.json` · `worked_example.steps[1].attempt_cue`

**Original:** Compute Z X̄ + (1 − Z)μ.

**Why flagged:** Attempt cue with the full premium expression.

**Proposal: migrate.** Z X̄ + (1 − Z)μ is the live credibility-premium formula (Wave 6 twin migrate of the same structure). “Compute” stays cue prose.

---

### 62. `5.1.6-credibility-premium-cs1003.json` · `worked_example.steps[2].explanation`

**Original:** Z is the weight on the risk's own experience X̄; 1 − Z weights the class hypothetical mean.

**Why flagged:** Step explanation with Z / X̄ / 1 − Z.

**Proposal: migrate (partial).** Z, X̄, and 1 − Z are the live premium-structure objects being glossed after the computation (Wave 7 KC explanation migrate of Z and (1 - Z) with short “weights …” clauses). Surrounding “is the weight on the risk's own experience” / “weights the class hypothetical mean” stays instructional prose. Distinct from mission chrome that only names “credibility” as a theory topic without posing Z.

---

## Summary of Batch 3 proposals

| Proposal | Count |
|---|---:|
| migrate | 5 |
| migrate (partial) | 31 |
| exclude (confirm exclude) | 26 |
| genuinely uncertain | 0 |
| **Batch 3 total** | **62** |

### Recurring-term check (same symbol, different roles in this batch)

| Term | Exclude instances (topic / shallow / §3.2) | Migrate / migrate-partial instances (live object) |
|---|---|---|
| η / η forms | Mission chrome, refuse slogans, η-forms / η-sketches task naming (items 1–3, 5–7, 9–10, 16–17, 19–20, 24) | Plug/form/write/define η; η vs μ board contrasts; η as xᵀβ; pitfall η / x² (items 4, 8, 11, 13–15, 18, 21–23) |
| χ² / X² / Pearson | Schematic path, expected benefit, “name … tests”, CMP open, tutor χ² vs LRT, sketch χ² vs LRT (items 28–31, 33–36) | Step label Pearson X²; watch non-significant χ²; sum to X²; large X² rejects (items 32, 37–39) |
| Δ / ΔD | “Δ deviance” KC topic label (item 25) | Form ΔD; ΔD vs χ² reject rule (items 26–27) |
| θ | Definitional prior/posterior / credible prose (items 45, 47, 50, 54; θ slogans in item 55) | Given-row prior/posterior for θ; π(θ\|data) (items 40, 44, 49, 51) |
| α, β / Beta(…) | — | Update cues, conjugacy explanation, wrong Beta(α+n, β+s) pitfall, numeric Beta(2+3, …) (items 41–43, 46) |
| Z, X̄, μ, 1−Z | — | All seven `5.1.6-cs1003` pending rows are live premium structure (items 56–62); no topic-only Z row in this batch |

---

## Remainder tracker (for later Wave 11 batches)

- **Original Wave 11 population:** 239  
- **Batch 1 (prior document):** 64  
- **Batch 2 (prior document):** 60  
- **Reviewed in this document:** 62  
- **Still pending human review after Batches 1–3:** 53 / 239  
- **Next cut suggestion:** continue syllabus order from `5.1.6-credibility-premium-cs1015.json` (through Bayesian credibility / EB / Bayes-vs-EB / CP / CR / revision packages), again aiming ~60 per batch without splitting packages (53 remaining fits a single final Batch 4).

**Remainder packages (19; 53 strings):**

| Package | N | isol. | mathish |
|---|---:|---:|---:|
| `5.1.6-credibility-premium-cs1015.json` | 7 | 5 | 2 |
| `5.1.7-bayesian-credibility-cs1003.json` | 2 | 2 | 0 |
| `5.1.7-bayesian-credibility-cs1015.json` | 2 | 2 | 0 |
| `5.1.8-empirical-bayes-cs1003.json` | 1 | 1 | 0 |
| `5.1.8-empirical-bayes-cs1015.json` | 2 | 2 | 0 |
| `5.1.9-bayes-vs-eb-cs1003.json` | 2 | 1 | 1 |
| `5.1.9-bayes-vs-eb-cs1015.json` | 3 | 3 | 0 |
| `cp-3.1.1-estimators-cs1016.json` | 3 | 2 | 1 |
| `cp-3.2.1-ci-sample-cs1016.json` | 3 | 2 | 1 |
| `cp-3.3.1-hypothesis-testing-cs1016.json` | 2 | 0 | 2 |
| `cr-1.2.2-correlation-cs1017.json` | 1 | 1 | 0 |
| `cr-2.1.2-continuous-cs1017.json` | 1 | 1 | 0 |
| `revision-confidence-intervals-cs1011.json` | 3 | 3 | 0 |
| `revision-distributions-generation-cs1004.json` | 3 | 3 | 0 |
| `revision-glm-cs1014.json` | 1 | 1 | 0 |
| `revision-linear-models-cs1003.json` | 5 | 1 | 4 |
| `revision-linear-regression-cs1013.json` | 6 | 0 | 6 |
| `revision-regression-glm-cs1003.json` | 3 | 3 | 0 |
| `revision-sampling-distributions-cs1009.json` | 3 | 2 | 1 |
| **Total** | **53** | **35** | **18** |

## Application status

**Applied.** Package JSON migrations, `_MANUAL_PROSE_EXCLUSIONS` registrations, ledger refresh, and Wave 11 batch 3 tests landed in the content commit that follows human acceptance of these proposals.

**Per-item classification counts (authoritative):** migrate 5 · migrate (partial) 31 · exclude 26 · total 62. (The summary table above had an off-by-one in the exclude/partial split; each numbered proposal was applied as written.)

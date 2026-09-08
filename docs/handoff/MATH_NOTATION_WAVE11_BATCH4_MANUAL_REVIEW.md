# Wave 11 Mathematical Notation - Manual-Review Proposals (Batch 4 / Final)

**Status:** Applied (Wave 11 final batch closed)  
**Date:** 2026-09-08  
**Scope:** Final batch of the catalogue-wide `correctly_excluded` + `needs_manual_review` population (all **53** remaining after Batches 1–3; closes the original **239**)  
**Standard:** `docs/content/MATHEMATICAL_NOTATION_STANDARD.md` (semantic-role test)  
**Ledger:** `docs/content/math_notation_inventory.json` (refreshed on application)  
**Prior batches:** `docs/handoff/MATH_NOTATION_WAVE11_MANUAL_REVIEW.md` (Batch 1: 64); `docs/handoff/MATH_NOTATION_WAVE11_BATCH2_MANUAL_REVIEW.md` (Batch 2: 60); `docs/handoff/MATH_NOTATION_WAVE11_BATCH3_MANUAL_REVIEW.md` (Batch 3: 62)

## Confirmed remaining population

Query on the live ledger:

- `category` = `correctly_excluded`
- `needs_manual_review` = `true`
- `migration_status` = `pending`

**Count: 53** (matches Batch 3 remainder tracker: 239 − 64 − 60 − 62 = 53; also matches ledger `totals.needs_manual_review` and `limits_of_automation.needs_manual_review_count`).

**Catalogue-wide check:** every `needs_manual_review=true` row in the ledger is exactly this set (53 × `correctly_excluded` + `pending`). There are no other NMR rows in any category or status. This is the entire remaining population, not a sample.

**Reason mix (53):** `isolated_symbol_in_narrative_ambiguous` 35 · `mathish_role_unclear` 18.

**Order:** syllabus / package-filename order (same rule as Batches 1–3), **not** raw ledger `packages` list order. First remaining package is `5.1.6-credibility-premium-cs1015.json`; last is `revision-sampling-distributions-cs1009.json` (**19** packages). Package set and per-package counts match Batch 3’s remainder table exactly.

Reusable distinctions (unchanged from Waves 1–10 and Batches 1–3):

- A symbol naming a topic or category in the abstract (mission chrome, schematic paths, metalinguistic gloss) is prose.
- The same symbol inside a concrete equation, pivot, or instruction to compute a real value is mathematics.
- A function or statistic name used to warn against a shallow reading is prose; the same characters forming a real expression the student works with are mathematics.
- Mostly-English definitional statements get only their genuine symbolic content wrapped (migrate partial).
- Numeric `±` / `×` constructions in attempt cues are live evaluation objects (migrate), matching Wave 10 / Batches 1–3.
- Standard §3.2 (“unbiased for μ” style naming in explanatory prose) stays exclude.
- `η forms` / `Family → η → link` style syllabus-path naming in mission / out-of-scope chrome excludes (Waves 3, 6, 7; Batches 2–3).
- Fit-measure / GOF-test topic naming in schematic titles / concept paths / expected-benefit skill lists excludes; the same statistic as a step target, sum target, or decision object migrates (partial) (Wave 4 / Wave 7 / Batch 2). Shallow “high R² clears diagnostics” refuse chrome excludes (Batch 2 'best R²' pattern).
- Credibility weight `Z`, `X̄`, `μ`, and `1 − Z` as live premium structure migrate (Wave 6 / Wave 7 / Batch 3); the same letters only as deferred-theory chrome or §3.2 structural naming in contrast prose may exclude (verify each instance).

---

## Batch 4 selection

**Selection rule:** continue syllabus / package-filename order from `5.1.6-credibility-premium-cs1015.json` through `revision-sampling-distributions-cs1009.json` inclusive (the entire remainder).

**Why this cut (no further split):**

1. Batch 3 already left this exact remainder as the natural final cut.
2. **53** items in **19** packages is within one coherent review pass; splitting would only delay close-out of the Wave 11 population.
3. Topic arc is coherent enough for one reviewer: credibility-premium twin → Bayesian credibility → EB → Bayes-vs-EB → CP estimators / CI / HT → CR twins → revision packages.

**Batch 4 reason mix:** `isolated_symbol_in_narrative_ambiguous` 35 · `mathish_role_unclear` 18.

**Batch 4 packages (19):**

| Package | N |
|---|---:|
| `5.1.6-credibility-premium-cs1015.json` | 7 |
| `5.1.7-bayesian-credibility-cs1003.json` | 2 |
| `5.1.7-bayesian-credibility-cs1015.json` | 2 |
| `5.1.8-empirical-bayes-cs1003.json` | 1 |
| `5.1.8-empirical-bayes-cs1015.json` | 2 |
| `5.1.9-bayes-vs-eb-cs1003.json` | 2 |
| `5.1.9-bayes-vs-eb-cs1015.json` | 3 |
| `cp-3.1.1-estimators-cs1016.json` | 3 |
| `cp-3.2.1-ci-sample-cs1016.json` | 3 |
| `cp-3.3.1-hypothesis-testing-cs1016.json` | 2 |
| `cr-1.2.2-correlation-cs1017.json` | 1 |
| `cr-2.1.2-continuous-cs1017.json` | 1 |
| `revision-confidence-intervals-cs1011.json` | 3 |
| `revision-distributions-generation-cs1004.json` | 3 |
| `revision-glm-cs1014.json` | 1 |
| `revision-linear-models-cs1003.json` | 5 |
| `revision-linear-regression-cs1013.json` | 6 |
| `revision-regression-glm-cs1003.json` | 3 |
| `revision-sampling-distributions-cs1009.json` | 3 |

**Remainder after this batch:** none (0 strings), if applied as proposed.

Note: `5.1.6-…-cs1015` is the twin of Batch 3’s `5.1.6-…-cs1003` (items 56–62 there). `cr-1.2.2` / `cr-2.1.2` reuse wording already reviewed on earlier syllabus twins in Batch 1 (`1.2.2-eda-association-ep001`, `2.1.2-continuous-cs1002`). Prior twin proposals do not auto-apply: each string below is classified from its own field role. Where the **same term** recurs (Z, X̄, μ, R², η, H₀, θ, λ), each instance is checked on its own role.

---

## Proposed classifications

### 1. `5.1.6-credibility-premium-cs1015.json` · `knowledge_checks[1].hints[0]`

**Original:** Compute 1 - Z first, then blend X̄ and μ.

**Why flagged:** KC hint with Z / X̄ / μ (`isolated_symbol_in_narrative_ambiguous`).

**Proposal: migrate (partial).** 1 - Z, X̄, and μ are the live credibility-premium ingredients (Wave 6 / Wave 7 / Batch 3 twin item 56 on `5.1.6-…-cs1003`). “Compute … first, then blend …” stays hint framing.

---

### 2. `5.1.6-credibility-premium-cs1015.json` · `knowledge_checks[1].hints[1]`

**Original:** Z weights the individual experience X̄.

**Why flagged:** KC hint with Z and X̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** Z and X̄ are the live weight and experience objects in the premium structure (Batch 3 twin item 57). “weights the individual experience” stays hint prose around those objects. Not mere topic naming of “credibility weight”.

---

### 3. `5.1.6-credibility-premium-cs1015.json` · `knowledge_checks[1].success_criteria[1]`

**Original:** Uses Z on X̄ and (1 - Z) on μ.

**Why flagged:** Success criterion with Z / X̄ / μ.

**Proposal: migrate (partial).** Z, X̄, (1 - Z), and μ are the live correct weighting structure the criterion checks (Batch 3 twin item 58). “Uses … on … and … on …” stays criterion framing.

---

### 4. `5.1.6-credibility-premium-cs1015.json` · `worked_example.steps[0].attempt_cue`

**Original:** Compute 1 − Z.

**Why flagged:** Attempt cue with 1 − Z.

**Proposal: migrate.** 1 − Z is the live complementary-weight evaluation for this step (Batch 3 twin item 60). “Compute” stays cue prose.

---

### 5. `5.1.6-credibility-premium-cs1015.json` · `worked_example.steps[1].attempt_cue`

**Original:** Evaluate Z X̄ + (1 − Z)μ.

**Why flagged:** Attempt cue with the full premium expression.

**Proposal: migrate.** Z X̄ + (1 − Z)μ is the live credibility-premium formula (Wave 6 / Batch 3 twin migrate). “Evaluate” stays cue prose.

---

### 6. `5.1.6-credibility-premium-cs1015.json` · `worked_example.steps[1].explanation`

**Original:** Z weights the individual mean; (1 − Z) weights the class mean.

**Why flagged:** Step explanation with Z / 1 − Z.

**Proposal: migrate (partial).** Z and (1 − Z) are the live premium-structure weights being glossed after the evaluation (Batch 3 item 62 / Wave 7 “weights …” gloss pattern). Surrounding “weights the individual mean” / “weights the class mean” stays instructional prose.

---

### 7. `5.1.6-credibility-premium-cs1015.json` · `worked_example.steps[2].explanation`

**Original:** Larger Z places more weight on the risk's own experience X̄.

**Why flagged:** Step explanation with Z and X̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** Z and X̄ remain live premium-structure objects in the comparative-weight gloss (same family as items 2 and 6; Batch 3 item 57). “Larger … places more weight on the risk's own experience” stays instructional prose around those objects. Distinct from mission chrome that only names “credibility” without posing Z.

---

### 8. `5.1.7-bayesian-credibility-cs1003.json` · `knowledge_checks[0].explanation`

**Original:** Bayesian credibility requires prior-to-posterior structure that justifies μ and Z. Empty formula or EB conflation are wrong.

**Why flagged:** KC explanation naming μ and Z.

**Proposal: exclude.** μ and Z are named only as the quantities a Bayesian warrant must justify, inside conceptual KC explanation prose (Standard §3.2 / Batch 1 coverage-about-μ exclusions). The live blend formula already sits in the migrated model answer / choices on this check; this field does not pose Z X̄ + (1 − Z)μ.

---

### 9. `5.1.7-bayesian-credibility-cs1003.json` · `worked_example.steps[1].attempt_cue`

**Original:** Compute Z X̄ + (1 − Z)μ.

**Why flagged:** Attempt cue with the full premium expression.

**Proposal: migrate.** Z X̄ + (1 − Z)μ is the live credibility-premium evaluation for this step (Wave 6 / Batch 3 migrate of the same structure). “Compute” stays cue prose.

---

### 10. `5.1.7-bayesian-credibility-cs1015.json` · `worked_example.steps[2].attempt_cue`

**Original:** Evaluate Z X̄ + (1 − Z)μ.

**Why flagged:** Attempt cue with the full premium expression.

**Proposal: migrate.** Same live premium formula as item 9 / Batch 3 twin migrate. “Evaluate” stays cue prose.

---

### 11. `5.1.7-bayesian-credibility-cs1015.json` · `worked_example.steps[2].explanation`

**Original:** The premium blends experience with the prior mean μ.

**Why flagged:** Step explanation naming μ.

**Proposal: exclude.** μ is named only as the prior mean in explanatory blend prose (Standard §3.2), without posing Z X̄ + (1 − Z)μ in this field (that live expression is item 10 / the sibling calculation). Parallel to Batch 2’s exclude of μ as mean-recipient in GLM prose.

---

### 12. `5.1.8-empirical-bayes-cs1003.json` · `worked_example.steps[1].explanation`

**Original:** The premium uses estimated μ and k in place of known prior structurals.

**Why flagged:** Step explanation with μ and k.

**Proposal: exclude.** μ and k are named as estimated structurals in contrast prose after the (already migrated) EB premium cue. Standard §3.2 structural naming, not a live formula board in this field.

---

### 13. `5.1.8-empirical-bayes-cs1015.json` · `worked_example.steps[1].explanation`

**Original:** The premium formula matches classical credibility, with estimated Z and μ.

**Why flagged:** Step explanation with Z and μ.

**Proposal: exclude.** Z and μ are named as the estimated classical-credibility ingredients in explanatory prose. The live EB premium expression sits in the sibling attempt cue (already migrated). Same §3.2 structural-naming role as item 12.

---

### 14. `5.1.8-empirical-bayes-cs1015.json` · `worked_example.steps[2].explanation`

**Original:** EB estimates μ and k from data; a fully Bayesian analysis would take them from an explicit prior structure.

**Why flagged:** Step explanation with μ and k.

**Proposal: exclude.** μ and k name the structurals whose source (data estimate vs prior) is being contrasted. Conceptual EB-versus-Bayes chrome, not a live premium evaluation. Verified separately from items 12–13: same letters, same exclude role (source naming), still no expression board here.

---

### 15. `5.1.9-bayes-vs-eb-cs1003.json` · `worked_example.common_pitfall`

**Original:** Forcing the two premiums to match by reusing one Z for both structural pairs, or claiming EB and Bayes must always agree for the same X̄.

**Why flagged:** Common-pitfall with Z and X̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** Z is the live weight being incorrectly reused across structural pairs; X̄ is the shared experience wrongly treated as forcing agreement (Wave 7 credibility pitfall migrate-partial of Z / X̄ wrong-path objects). Surrounding “Forcing the two premiums to match by…” / “or claiming EB and Bayes must always agree for…” stays pitfall prose.

---

### 16. `5.1.9-bayes-vs-eb-cs1003.json` · `worked_example.steps[2].explanation`

**Original:** Same risk experience can produce different premiums when (μ, k) differ because Bayes uses specified prior structurals while EB uses estimated ones.

**Why flagged:** Step explanation with (μ, k).

**Proposal: migrate (partial).** (μ, k) are the live structural pair whose difference drives the premium gap on this contrast step (sibling calculation already treats Different (μ, k) pairs as the math object). Surrounding Bayes-specified vs EB-estimated English stays instructional prose. Distinct from items 12–14, which only name structurals as “estimated” without posing them as the contrast cause of different premiums.

---

### 17. `5.1.9-bayes-vs-eb-cs1015.json` · `worked_example.common_pitfall`

**Original:** Assuming the two approaches must produce identical premiums whenever X̄ and n match, or mixing Bayes μ with EB k̂ in one formula.

**Why flagged:** Common-pitfall with X̄ / n / μ / k̂.

**Proposal: migrate (partial).** X̄ and n are the live shared-experience / sample-size objects in the false-identity assumption; Bayes μ and EB k̂ are the live wrong-path mix in one formula (Wave 7 credibility pitfall pattern). Surrounding “Assuming… must produce identical premiums whenever…” / “or mixing … in one formula” stays pitfall prose.

---

### 18. `5.1.9-bayes-vs-eb-cs1015.json` · `worked_example.steps[0].explanation`

**Original:** Bayes uses prior-specified μ and k.

**Why flagged:** Step explanation with μ and k.

**Proposal: exclude.** Short §3.2 naming of the prior-specified structurals after a numeric Bayes premium step. Live Z / P arithmetic sits in the sibling attempt cue / calculation. Same structural-naming exclude role as items 12–13; verified on this field alone (not copied from those rows).

---

### 19. `5.1.9-bayes-vs-eb-cs1015.json` · `worked_example.steps[2].explanation`

**Original:** Bayes assumes a specified prior structure; EB estimates structurals from collective data. Different (μ, k) pairs produce different Z and different blends, so premiums need not match.

**Why flagged:** Step explanation with (μ, k) and Z.

**Proposal: migrate (partial).** (μ, k) and Z are the live structural / weight objects in the causal claim that different pairs produce different blends (parallel to item 16, with Z explicit). The opening Bayes-vs-EB assumption sentence stays instructional prose around those objects.

---

### 20. `cp-3.1.1-estimators-cs1016.json` · `knowledge_checks[1].success_criteria[1]`

**Original:** Uses the sample mean as MoM for the Poisson mean λ.

**Why flagged:** Success criterion naming λ.

**Proposal: exclude.** λ names the Poisson mean parameter in a scoring criterion (“MoM for the Poisson mean”), without posing λ̂ = x̄ or another live expression here. Parallel to Batch 1 exclude of “Uses the Exponential CDF with mean θ”.

---

### 21. `cp-3.1.1-estimators-cs1016.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Equate the Poisson mean λ to the sample mean before computing.

**Why flagged:** Attempt-before-reveal with λ.

**Proposal: migrate (partial).** λ is the live MoM matching object the student must equate to the sample mean (Batch 1 migrate-partial of “write the first population moment in terms of μ”). “CMP closed”, “Equate the Poisson mean … to the sample mean before computing” stays framing prose around that object.

---

### 22. `cp-3.1.1-estimators-cs1016.json` · `worked_example.steps[1].explanation`

**Original:** Substitute the observed counts into x̄.

**Why flagged:** Step explanation with x̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** x̄ is the live sample-mean object formed on this evaluation step. “Substitute the observed counts into” stays instructional framing. Distinct from item 20’s criterion naming of λ without posing x̄.

---

### 23. `cp-3.2.1-ci-sample-cs1016.json` · `knowledge_checks[1].explanation`

**Original:** Coverage is about μ and the procedure. Prediction readings and 'midpoint probability' misstate frequentist CIs; HT is a related but distinct task.

**Why flagged:** KC explanation naming μ.

**Proposal: exclude.** μ is named inside coverage-interpretation / misconception-refusal prose (Batch 1 coverage-about-μ / coverage-contrast exclusions). No live interval expression in this field.

---

### 24. `cp-3.2.1-ci-sample-cs1016.json` · `worked_example.steps[1].attempt_cue`

**Original:** Compute 450 ± 1.96 × 5.

**Why flagged:** Attempt cue with numeric ± / ×.

**Proposal: migrate.** 450 ± 1.96 × 5 is the live numeric interval evaluation (Wave 10 / Batches 1–3 numeric ± × cues). “Compute” stays cue prose.

---

### 25. `cp-3.2.1-ci-sample-cs1016.json` · `worked_example.steps[1].explanation`

**Original:** 95% z-interval centres at x̄.

**Why flagged:** Step explanation with x̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** x̄ is the live interval centre (Batch 1 migrate-partial of “Centre at the observed” / “centres at x̄” family). “95% z-interval centres at” stays instructional framing around that object.

---

### 26. `cp-3.3.1-hypothesis-testing-cs1016.json` · `worked_example.steps[0].explanation`

**Original:** Type I error is a false rejection of H₀. With H₀: clean, that is flagging a clean claim as fraud.

**Why flagged:** Step explanation with H₀ (`mathish_role_unclear`).

**Proposal: exclude.** H₀ is named inside Type I error definitional prose and as the “clean” null label (Batch 2 exclude of H₀ as framing-note null label; Standard §3.2 HT vocabulary). No live p ≤ α decision board here (rates are computed in the sibling calculation without posing H₀ as an expression).

---

### 27. `cp-3.3.1-hypothesis-testing-cs1016.json` · `worked_example.steps[1].explanation`

**Original:** Type II error is failing to reject H₀ when the claim is fraudulent (H₀ false).

**Why flagged:** Step explanation with H₀ (`mathish_role_unclear`).

**Proposal: exclude.** Same definitional Type II / H₀-false naming role as item 26. Verified on this field alone: still vocabulary in error-type explanation, not a live hypothesis expression.

---

### 28. `cr-1.2.2-correlation-cs1017.json` · `worked_example.steps[1].attempt_cue`

**Original:** Compare |r| and |ρ| in light of the scatter.

**Why flagged:** Attempt cue with |r| / |ρ|.

**Proposal: migrate (partial).** |r| and |ρ| are the live correlation magnitudes the student must compare (Batch 1 twin on `1.2.2-eda-association-ep001`, same wording and role). “Compare … in light of the scatter” stays cue prose. Rechecked on this CR package: still a comparison board, not topic chrome.

---

### 29. `cr-2.1.2-continuous-cs1017.json` · `worked_example.given[0].note`

**Original:** continuous support on (0, ∞)

**Why flagged:** Given note with (0, ∞).

**Proposal: migrate (partial).** (0, ∞) is the live support interval (Batch 1 twin on `2.1.2-continuous-cs1002`). “continuous support on” stays framing prose. Rechecked: same support-object role on this CR twin.

---

### 30. `revision-confidence-intervals-cs1011.json` · `worked_example.common_pitfall`

**Original:** Saying that given these data, θ has probability 0.95 of lying in the calculated interval, which swaps a frequentist coverage statement for a posterior probability reading.

**Why flagged:** Common-pitfall naming θ.

**Proposal: exclude.** θ appears only inside the wrong posterior-probability reading of a frequentist interval (Batch 1 / Batch 3 coverage-θ exclude pattern). No numeric interval endpoints are posed as objects in this field (contrast Batch 3 item 55, which migrated the numeric (90.2, 109.8) and left θ prose).

---

### 31. `revision-confidence-intervals-cs1011.json` · `worked_example.steps[0].explanation`

**Original:** The construction procedure covers the fixed parameter θ in 95% of repeated samples under the model. It does not assign posterior probability 0.95 to θ given these data.

**Why flagged:** Step explanation naming θ.

**Proposal: exclude.** θ is named in coverage-interpretation contrast prose (Batch 1 / Batch 3 θ coverage excludes). No live X̄ ± … expression here (that is item 32).

---

### 32. `revision-confidence-intervals-cs1011.json` · `worked_example.steps[2].attempt_cue`

**Original:** Compute X̄ ± 1.96 SE.

**Why flagged:** Attempt cue with X̄ ± … SE.

**Proposal: migrate.** X̄ ± 1.96 SE is the live interval form this step evaluates (Wave 10 / Batches 1–3 ± cue family; symbolic rather than fully numeric, still a live evaluation object). “Compute” stays cue prose.

---

### 33. `revision-distributions-generation-cs1004.json` · `worked_example.common_pitfall`

**Original:** Generating Exponential draws by applying the CDF to U instead of the inverse CDF, or multiplying by λ instead of dividing by λ in the quantile formula.

**Why flagged:** Common-pitfall with U and λ.

**Proposal: migrate (partial).** U and λ are the live wrong-path objects in the inverse-transform mistake (CDF-on-U; multiply-vs-divide by λ). Surrounding “Generating Exponential draws by…” / “in the quantile formula” stays pitfall prose.

---

### 34. `revision-distributions-generation-cs1004.json` · `worked_example.steps[0].attempt_cue`

**Original:** Write X in terms of U and λ.

**Why flagged:** Attempt cue with X / U / λ.

**Proposal: migrate (partial).** X, U, and λ are the live inverse-transform constituents the student must write (sibling explanation already has X = −ln(1−U)/λ migrated). “Write … in terms of” stays cue framing.

---

### 35. `revision-distributions-generation-cs1004.json` · `worked_example.steps[2].explanation`

**Original:** Applying the CDF rather than its inverse does not produce an Exponential(λ) draw. The method maps Uniform probability through the quantile function.

**Why flagged:** Step explanation with Exponential(λ).

**Proposal: exclude.** Exponential(λ) names the target law inside refuse-explanation prose (distribution naming / Standard §3.2), without posing the inverse-transform formula in this field. Distinct from item 34’s live Write-X cue and from Batch 1 migrate of Normal(400, 400²) as an accept/refuse distributional claim on a histogram board.

---

### 36. `revision-glm-cs1014.json` · `reading_guidance.focus_questions[1]`

**Original:** Can you state family → link → η → deviance → residuals → tests → fit?

**Why flagged:** Focus question with η in a schematic path.

**Proposal: exclude.** “family → link → η → …” is syllabus-path / retrieval-outline chrome (Waves 3, 6, 7; Batches 2–3 Family → η → link exclusions). No live g(μ)=η or η = Xβ equation here.

---

### 37. `revision-linear-models-cs1003.json` · `worked_example.common_pitfall`

**Original:** Confusing OLS with minimising fitted values, or treating a large R² as proof that a funnel-shaped residual plot can be ignored.

**Why flagged:** Common-pitfall with R² (`mathish_role_unclear`).

**Proposal: exclude.** “a large R²” is a shallow-reading warning phrase (statistic name used to refuse a bad heuristic), not a live fit value to compute or select on (Batch 2 exclude of 'best R²' shallow warnings; contrast Wave 7 migrate-partial when raw R² = 0.58 is a numeric wrong-path comparison).

---

### 38. `revision-linear-models-cs1003.json` · `worked_example.steps[0].explanation`

**Original:** Y is the response; columns of X are explanatory variables; OLS chooses β to minimise the sum of squared residuals.

**Why flagged:** Step explanation with Y / X / β.

**Proposal: migrate (partial).** Y, X, and β are the live model objects being retrieved on this roles/OLS step (Wave 9 / Batch 2 definitional migrate-partial pattern). Surrounding “is the response”, “are explanatory variables”, “OLS chooses … to minimise the sum of squared residuals” stays instructional prose.

---

### 39. `revision-linear-models-cs1003.json` · `worked_example.steps[2].attempt_cue`

**Original:** Can high R² dismiss the residual pattern?

**Why flagged:** Attempt cue with R² (`mathish_role_unclear`).

**Proposal: exclude.** R² is named inside a refuse-probe cue (shallow diagnostics substitute), not as a live selection or substitution object. Parallel to Batch 2 'best R²' / shallow-reading exclusions; distinct from Wave 7 “Write R²_adj … do not select on raw R² alone”, where the student must form the fit measures.

---

### 40. `revision-linear-models-cs1003.json` · `worked_example.steps[2].explanation`

**Original:** A large R² does not repair a clear residual funnel. Diagnostics remain required.

**Why flagged:** Step explanation with R² (`mathish_role_unclear`).

**Proposal: exclude.** Same shallow-reading refuse role as items 37 and 39: R² named as the inadequate diagnostic substitute in explanatory prose. Verified on this field: no numeric R² and no selection formula.

---

### 41. `revision-linear-models-cs1003.json` · `worked_example.steps[2].label`

**Original:** Refuse R²-as-diagnostics

**Why flagged:** Step label with R² (`mathish_role_unclear`).

**Proposal: exclude.** Metalinguistic refuse-path naming in a step label (Batch 2/3 refuse-slogan / shallow-reading exclusions). No live R² expression.

---

### 42. `revision-linear-regression-cs1013.json` · `worked_example.attempt_before_reveal`

**Original:** CMP closed. Retrieve the residual-sum-of-squares criterion, then interpret curvature despite high R².

**Why flagged:** Attempt-before-reveal with R² (`mathish_role_unclear`).

**Proposal: exclude.** “high R²” is shallow-adequacy framing inside ABR chrome (same refuse family as items 37–41), not a live fit object to write. “CMP closed. Retrieve the residual-sum-of-squares criterion, then interpret curvature despite…” stays pedagogical framing.

---

### 43. `revision-linear-regression-cs1013.json` · `worked_example.common_pitfall`

**Original:** Minimising the sum of fitted values instead of squared residuals, or treating high R² from automated selection as proof that a curved residual plot can be ignored.

**Why flagged:** Common-pitfall with R² (`mathish_role_unclear`).

**Proposal: exclude.** Same shallow R²-as-adequacy warning role as item 37 on the linear-models twin. Rechecked: still refuse prose, not a numeric R² comparison board.

---

### 44. `revision-linear-regression-cs1013.json` · `worked_example.steps[2].attempt_cue`

**Original:** Does high R² clear the curvature?

**Why flagged:** Attempt cue with R² (`mathish_role_unclear`).

**Proposal: exclude.** Same refuse-probe role as item 39. Verified independently on this twin: still shallow-adequacy cue, not a live selection object.

---

### 45. `revision-linear-regression-cs1013.json` · `worked_example.steps[2].explanation`

**Original:** High R² and automated selection do not establish adequacy when residuals show clear curvature. Reconsider justified transformations or nonlinear terms and validate.

**Why flagged:** Step explanation with R² (`mathish_role_unclear`).

**Proposal: exclude.** Same shallow-adequacy refuse explanation role as item 40.

---

### 46. `revision-linear-regression-cs1013.json` · `worked_example.steps[2].label`

**Original:** Refuse R²-as-adequacy

**Why flagged:** Step label with R² (`mathish_role_unclear`).

**Proposal: exclude.** Metalinguistic refuse-path label naming (parallel to item 41).

---

### 47. `revision-linear-regression-cs1013.json` · `worked_example.title`

**Original:** Retrieve OLS criterion and refuse R²-clears-curvature

**Why flagged:** Title with R² (`mathish_role_unclear`).

**Proposal: exclude.** Title chrome naming the retrieval + refuse path (Batch 2 exclude of adjusted R² topic naming in titles / schematic paths). No live defining equation in the title itself.

---

### 48. `revision-regression-glm-cs1003.json` · `mission.success_criteria[1]`

**Original:** Retrieve Family → η → link.

**Why flagged:** Mission success criterion with η in a schematic path.

**Proposal: exclude.** “Family → η → link” is pedagogical path / retrieval chrome (Batches 2–3 / Waves 6–7). No live link equation in this criterion.

---

### 49. `revision-regression-glm-cs1003.json` · `worked_example.steps[0].label`

**Original:** Retrieve Family → η → link

**Why flagged:** Step label with η in a schematic path.

**Proposal: exclude.** Same Family → η → link path-naming role as item 48, now as a step label. Verified separately: still chrome, not g(μ)=η (that live object is item 50).

---

### 50. `revision-regression-glm-cs1003.json` · `worked_example.steps[1].attempt_cue`

**Original:** State g(μ) for Poisson.

**Why flagged:** Attempt cue with g(μ).

**Proposal: migrate (partial).** g(μ) is the live link-function object the student must state for Poisson (Wave 9 / Wave 7 migrate of g(μ)=η; Batch 2/3 link-object migrate-partial). “State … for Poisson” stays cue framing. Distinct from items 48–49’s path naming of η without posing g(μ).

---

### 51. `revision-sampling-distributions-cs1009.json` · `worked_example.steps[0].attempt_cue`

**Original:** What distribution does X̄ have across repeated samples?

**Why flagged:** Attempt cue with X̄ (`mathish_role_unclear`).

**Proposal: migrate (partial).** X̄ is the live statistic whose sampling distribution this step retrieves (Batch 1 migrate-partial of “Name the Normal parameters for X̄” / “Sampling distribution of X̄” label; contrast Batch 1 exclude of X̄ only inside a finished definitional explanation or mission chrome). “What distribution does … have across repeated samples?” stays cue framing around that object.

---

### 52. `revision-sampling-distributions-cs1009.json` · `worked_example.steps[1].attempt_cue`

**Original:** Write T when σ is estimated by S.

**Why flagged:** Attempt cue with T / σ / S.

**Proposal: migrate (partial).** T, σ, and S are the live pivot objects the student must write under estimated scale (Batch 1 migrate-partial of σ/s substitution and t-under-H₀ distributional statements). “Write … when … is estimated by …” stays cue framing.

---

### 53. `revision-sampling-distributions-cs1009.json` · `worked_example.steps[2].explanation`

**Original:** Replacing σ by S without switching to t ignores the extra uncertainty from estimating the variance.

**Why flagged:** Step explanation with σ and S.

**Proposal: migrate (partial).** σ and S are the live wrong-path substitution pair in the refuse explanation (Batch 1 migrate-partial of “With σ unknown, replace σ by s…”; contrast Batch 1 exclude when σ only names the unknown-scale syllabus condition). “Replacing … without switching to t ignores the extra uncertainty…” stays instructional prose around those objects.

---

## Summary of Batch 4 proposals

Counted by walking items 1–53 above (not estimated):

| Proposal | Count | Item numbers |
|---|---:|---|
| migrate | 6 | 4, 5, 9, 10, 24, 32 |
| migrate (partial) | 21 | 1–3, 6–7, 15–17, 19, 21–22, 25, 28–29, 33–34, 38, 50–53 |
| exclude (confirm exclude) | 26 | 8, 11–14, 18, 20, 23, 26–27, 30–31, 35–37, 39–49 |
| genuinely uncertain | 0 | — |
| **Batch 4 total** | **53** | 6 + 21 + 26 = 53 |

### Recurring-term check (same symbol, different roles in this batch)

| Term | Exclude instances (topic / shallow / §3.2) | Migrate / migrate-partial instances (live object) |
|---|---|---|
| Z, X̄, μ, 1−Z | KC warrant-for-μ-and-Z; prior-mean μ gloss; estimated μ/k/Z structural naming (items 8, 11–14, 18) | Premium hints/criteria/cues/glosses; full Z X̄+(1−Z)μ cues; Bayes-vs-EB pitfalls and (μ,k)/Z contrast (items 1–7, 9–10, 15–17, 19) |
| λ / x̄ (MoM) | Success criterion “MoM for … λ” (item 20) | Equate λ; substitute into x̄ (items 21–22) |
| μ (CI coverage) | Coverage-is-about-μ KC prose (item 23) | — (live interval is numeric ± cue item 24 / centre x̄ item 25) |
| H₀ | Type I / Type II definitional naming (items 26–27) | — |
| \|r\|, \|ρ\|, (0, ∞) | — | CR twin comparison / support (items 28–29) |
| θ | Coverage / posterior-misread prose (items 30–31) | — (live form is X̄ ± 1.96 SE, item 32) |
| U, λ, X, Exponential(λ) | Exponential(λ) as named target law in refuse prose (item 35) | Pitfall U/λ; Write X in terms of U and λ (items 33–34) |
| η / Family → η → link | Focus-question path; mission criterion; step label (items 36, 48–49) | — |
| g(μ) | — | State g(μ) for Poisson (item 50) |
| R² | All shallow refuse / title / ABR / pitfall / label / cue / explanation rows on the two revision twins (items 37, 39–47) | — |
| Y, X, β | — | Roles / OLS explanation (item 38) |
| X̄, T, σ, S (sampling) | — | Distribution-of-X̄ cue; Write T when σ by S; Replacing σ by S refuse (items 51–53) |

---

## Final Wave 11 cross-batch summary

Verified by summing Batch 1–3 document proposal tables plus the Batch 4 per-item count above (Batch 3 uses the authoritative per-item counts from its application note: migrate 5 · partial 31 · exclude 26).

| Batch | Reviewed | migrate | migrate (partial) | exclude | uncertain |
|---|---:|---:|---:|---:|---:|
| Batch 1 | 64 | 9 | 30 | 25 | 0 |
| Batch 2 | 60 | 7 | 34 | 19 | 0 |
| Batch 3 | 62 | 5 | 31 | 26 | 0 |
| Batch 4 (this doc) | 53 | 6 | 21 | 26 | 0 |
| **Wave 11 total** | **239** | **27** | **116** | **96** | **0** |

Cross-checks:

- 64 + 60 + 62 + 53 = **239** (original population).
- 27 + 116 + 96 = **239** (classification partition).
- Migrated (full + partial) across all batches: **27 + 116 = 143**.
- Confirmed excluded across all batches: **96**.
- After this batch is applied (package migrations + `_MANUAL_PROSE_EXCLUSIONS` + ledger refresh), catalogue-wide `needs_manual_review` must reach **exactly 0** (current ledger already shows only these 53 NMR rows remain).

---

## Remainder tracker

- **Original Wave 11 population:** 239  
- **Batch 1:** 64  
- **Batch 2:** 60  
- **Batch 3:** 62  
- **Reviewed in this document:** 53  
- **Still pending human review after Batches 1–4 proposals:** 0 / 239 (once applied)

## Application status

**Applied.** Package migrations, `_MANUAL_PROSE_EXCLUSIONS`, and ledger refresh completed for all 53 items (6 full migrate, 21 partial migrate, 26 confirm exclude). Catalogue-wide `needs_manual_review` is **0**.

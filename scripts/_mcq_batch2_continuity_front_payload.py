#!/usr/bin/env python3
"""Batch 2 MCQ conversion payload for Continuity Front (checkpoint Batch B file set).

Applies deterministic MCQ rewrites to Active Recall + Checkpoint items for:
  - Campaign Nu CS1-013 (4.1.1 through 4.1.5)
  - Campaign Xi CS1-014 (4.2.1 through 4.2.10)
  - Campaign Omicron CS1-015 (5.1.1 through 5.1.9)

Does not touch revision packages or other campaigns.
"""
from __future__ import annotations

from typing import Any

# Inventory filename -> {ar: {...}, cp: {...}}
# Each item supplies fields that replace short_structured scoring content.

Choice = dict[str, str]


def _item(
    *,
    prompt: str,
    body: str,
    choices: list[Choice],
    correct: str,
    explanation: str,
    model_answer: str,
    common_mistake: str,
    hints: list[str] | None = None,
    success_criteria: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "prompt": prompt,
        "response_type": "mcq",
        "body": body,
        "hints": hints
        or [
            "Select the single best statement.",
            "Use the concept from this learning objective only.",
        ],
        "accepted_keywords": [],
        "choices": choices,
        "correct_choice_id": correct,
        "explanation": explanation,
        "model_answer": model_answer,
        "common_mistake": common_mistake,
        "success_criteria": success_criteria
        or [
            "Selects the correct choice.",
            "Rejects the named misconception distractors.",
        ],
    }


def c(cid: str, label: str, tag: str = "") -> Choice:
    return {"id": cid, "label": label, "misconception_tag": tag}


CONVERSIONS: dict[str, dict[str, dict[str, Any]]] = {
    # ------------------------------------------------------------------
    # 4.1.1 Response and explanatory variables
    # ------------------------------------------------------------------
    "4.1.1-response-explanatory-cs1013.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly assigns response and "
                "explanatory roles in a regression modelling question?"
            ),
            body="Select the statement that names Y, X, and an actuarial pair.",
            choices=[
                c(
                    "a",
                    "The response variable Y is the outcome being modelled or "
                    "predicted; explanatory variables X are the predictors "
                    "thought to help explain or predict Y. Example: claim "
                    "severity (Y) with age and sum insured as X variables.",
                ),
                c(
                    "b",
                    "Every numeric column in a data set is automatically an "
                    "explanatory variable; the response is whichever column "
                    "has the largest variance.",
                    "column_soup",
                ),
                c(
                    "c",
                    "Claim count is always an explanatory variable when "
                    "modelling claim severity, because both are numeric "
                    "policy fields.",
                    "claim_count_as_x",
                ),
                c(
                    "d",
                    "Response and explanatory roles are defined only after "
                    "writing a simple versus multiple linear model equation; "
                    "variable roles cannot be stated before model form.",
                    "model_form_first",
                ),
            ],
            correct="a",
            explanation=(
                "Y is the outcome for the modelling question; X variables are "
                "predictors with a warrant. Putting every numeric column on "
                "the right-hand side, or treating claim count as automatically "
                "an X for severity, ignores the modelling question."
            ),
            model_answer=(
                "Response is the outcome modelled; explanatory variables are "
                "predictors. Example: claim severity (Y) vs age and sum insured."
            ),
            common_mistake=(
                "Column-soup modelling, or treating claim count as automatically "
                "an explanatory variable for severity."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Motor book: you want to model claim severity. "
                "Columns include age, sum insured, claim amount, NCD discount, "
                "and claim count. Which statement is correct?"
            ),
            body="Name Y and warranted X variables; refuse column-soup.",
            choices=[
                c(
                    "a",
                    "Response Y = claim amount (severity, the outcome to explain). "
                    "Explanatory examples: age and sum insured (predictors of "
                    "severity with a one-sentence warrant each). Claim count is "
                    "a frequency outcome, not automatically an X for severity. "
                    "Putting every numeric column on the right-hand side is not "
                    "variable-role modelling.",
                ),
                c(
                    "b",
                    "Response Y = claim count; explanatory variables are claim "
                    "amount, age, sum insured, and NCD because all numeric "
                    "columns belong on the right-hand side.",
                    "column_soup",
                ),
                c(
                    "c",
                    "Response Y = claim amount; claim count must also be an "
                    "explanatory variable because it appears in the same policy "
                    "record as severity.",
                    "claim_count_as_x",
                ),
                c(
                    "d",
                    "No response can be named until a multiple regression "
                    "equation is fully written; severity modelling starts with "
                    "equation form, not Y versus X.",
                    "model_form_first",
                ),
            ],
            correct="a",
            explanation=(
                "For severity modelling, claim amount is Y. Age and sum insured "
                "are plausible X's with warrants. Claim count is a different "
                "outcome type. Column-soup is not role assignment."
            ),
            model_answer=(
                "Y = claim amount (severity). X examples: age, sum insured. "
                "Refuse column-soup."
            ),
            common_mistake=(
                "Accepting column-soup or treating claim count as automatically "
                "an X for severity."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.1.2 Simple and multiple linear models
    # ------------------------------------------------------------------
    "4.1.2-simple-multiple-cs1013.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly contrasts simple and "
                "multiple linear regression model forms?"
            ),
            body="Select the statement that names one X versus several X's.",
            choices=[
                c(
                    "a",
                    "A simple linear model has one explanatory variable; a "
                    "multiple linear model has several explanatory variables "
                    "entering jointly. Multiple regression can hold additional "
                    "predictors simultaneously that a simple model cannot.",
                ),
                c(
                    "b",
                    "Simple and multiple linear models differ only in how "
                    "least-squares estimates are computed; stating Y = β₀ "
                    "+ β₁ x + ε is already least squares.",
                    "least_squares_finishes",
                ),
                c(
                    "c",
                    "A multiple linear model must always include interaction "
                    "terms; a simple model never includes an intercept.",
                    "interaction_required",
                ),
                c(
                    "d",
                    "Simple linear regression applies only to claim frequency; "
                    "multiple linear regression applies only to claim severity.",
                    "frequency_severity_swap",
                ),
            ],
            correct="a",
            explanation=(
                "Simple versus multiple is about how many explanatory variables "
                "enter the linear form. Least squares is a separate estimation "
                "criterion applied after the model is stated."
            ),
            model_answer=(
                "Simple: one X; multiple: several X's jointly. Least squares "
                "estimation is a separate criterion from model-form statement."
            ),
            common_mistake=(
                "Collapsing model-form statement into least-squares estimation."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Claim severity Y with predictors age (x1) and "
                "sum insured (x2). Which statement is correct?"
            ),
            body="Write simple versus multiple forms; refuse OLS-as-form.",
            choices=[
                c(
                    "a",
                    "Simple: Y = β₀ + β₁ age + ε. Multiple: "
                    "Y = β₀ + β₁ age + β₂ sum_insured + ε. "
                    "Writing least-squares formulae for β̂ is estimation, "
                    "not stating the simple versus multiple linear model forms.",
                ),
                c(
                    "b",
                    "Simple: Y = β₀ + β₁ age + β₂ sum_insured + "
                    "ε. Multiple: Y = β₀ + β₁ age + ε, "
                    "because multiple means more parameters in the criterion.",
                    "forms_swapped",
                ),
                c(
                    "c",
                    "Both forms are Y = β̂₀ + β̂₁ x + ε "
                    "where β̂ comes from minimising sum of squared "
                    "residuals; stating the model is the same as clicking Fit.",
                    "least_squares_finishes",
                ),
                c(
                    "d",
                    "Simple and multiple models are identical here because age "
                    "and sum insured are both continuous; the distinction "
                    "applies only when one predictor is categorical.",
                    "continuous_collapse",
                ),
            ],
            correct="a",
            explanation=(
                "Simple uses one predictor; multiple uses both. Closed-form "
                "least squares is estimation, not the act of naming the model "
                "forms."
            ),
            model_answer=(
                "Simple: Y = β₀ + β₁ age + ε. Multiple adds "
                "β₂ sum_insured. Refuse OLS-as-form."
            ),
            common_mistake=(
                "Treating least-squares estimation as finishing model-form "
                "statement."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.1.3 Least squares
    # ------------------------------------------------------------------
    "4.1.3-least-squares-cs1013.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the "
                "least-squares criterion, parameters estimated in simple "
                "linear regression, and a residual?"
            ),
            body="Select the OLS foundation statement.",
            choices=[
                c(
                    "a",
                    "Least squares minimises the sum of squared residuals. "
                    "In the simple linear model, slope and intercept are "
                    "estimated. A residual is observed minus fitted value.",
                ),
                c(
                    "b",
                    "Least squares means clicking Fit in software; the "
                    "criterion is whatever the package minimises internally "
                    "without a closed-form expression.",
                    "fit_as_criterion",
                ),
                c(
                    "c",
                    "The ordinary least-squares slope equals the correlation "
                    "Corr(X, Y); correlation is therefore the slope "
                    "estimate by definition.",
                    "corr_as_slope",
                ),
                c(
                    "d",
                    "Least squares minimises the sum of absolute residuals; "
                    "the intercept alone is estimated while the slope is "
                    "fixed at the sample correlation.",
                    "lad_as_ols",
                ),
            ],
            correct="a",
            explanation=(
                "OLS minimises sum of squared residuals and estimates slope "
                "and intercept. Correlation is dimensionless association, not "
                "the OLS slope (which scales by SD ratios)."
            ),
            model_answer=(
                "Minimise sum of squared residuals; estimate slope and "
                "intercept; residual = observed minus fitted."
            ),
            common_mistake=(
                "Treating software Fit as the criterion, or equating OLS "
                "slope with correlation."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Simple linear model Y = β₀ + β₁ x + "
                "ε with data pairs (xi, yi). Which statement is correct?"
            ),
            body="State the criterion and slope; refuse Fit-as-criterion.",
            choices=[
                c(
                    "a",
                    "Choose β₀, β₁ to minimise sum (yi minus β₀ minus "
                    "β₁ xi) squared. Slope β̂₁ = sum (xi minus "
                    "x-bar)(yi minus ȳ) / sum (xi minus x̄) squared = "
                    "Cov̂(X, Y) / Var̂(X); intercept β̂₀ = "
                    "ȳ minus β̂₁ x̄. Fit implements OLS but is "
                    "not the criterion; Corr(X, Y) is not the OLS slope.",
                ),
                c(
                    "b",
                    "Least squares is clicking Fit; the closed-form slope "
                    "formula is optional once software returns β̂.",
                    "fit_as_criterion",
                ),
                c(
                    "c",
                    "The OLS slope equals Corr(X, Y) because both measure "
                    "linear association on the same scale.",
                    "corr_as_slope",
                ),
                c(
                    "d",
                    "Minimise sum |yi minus β₀ minus β₁ xi|; the "
                    "resulting slope is Cov̂(X, Y) / Var̂(X) for "
                    "simple linear regression.",
                    "lad_as_ols",
                ),
            ],
            correct="a",
            explanation=(
                "The criterion is sum of squared residuals. The slope formula "
                "uses covariance over variance. Correlation lacks the SD "
                "scaling of the OLS slope."
            ),
            model_answer=(
                "Minimise sum squared residuals; β̂₁ = Cov̂/Var̂; "
                "refuse Fit-as-criterion and Corr-as-slope."
            ),
            common_mistake=(
                "Accepting Fit as the criterion or Corr(X, Y) as the OLS slope."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.1.4 Software fit and inference
    # ------------------------------------------------------------------
    "4.1.4-software-fit-cs1013.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes slope "
                "inference, goodness-of-fit use, mean versus individual "
                "prediction limits, and residual checks after a linear fit?"
            ),
            body="Select the post-fit inference statement.",
            choices=[
                c(
                    "a",
                    "Report the slope estimate with its standard error and "
                    "inference under the model. Goodness-of-fit summarises how "
                    "well the linear relationship describes the data. A "
                    "prediction interval for a new observation is typically "
                    "wider than a mean-response interval because it adds "
                    "residual variance. Residuals check suitability and "
                    "validity of the linear model.",
                ),
                c(
                    "b",
                    "After a significant slope, residual plots are optional "
                    "because significance already proves the model is valid.",
                    "residuals_optional",
                ),
                c(
                    "c",
                    "Mean-response and individual-response intervals are "
                    "identical for a new x-star because both target E[Y | "
                    "x-star].",
                    "intervals_identical",
                ),
                c(
                    "d",
                    "Goodness-of-fit means adjusted R-squared alone; slope "
                    "inference and prediction limits are not part of software "
                    "fit output.",
                    "gof_r2_only",
                ),
            ],
            correct="a",
            explanation=(
                "Slope inference, GOF, prediction limits, and residual checks "
                "are all required after a fit. Residuals are not optional after "
                "significance, and the two interval types differ in width."
            ),
            model_answer=(
                "Slope SE and inference; GOF; prediction wider than mean "
                "interval; residuals check validity."
            ),
            common_mistake=(
                "Treating residuals as optional or collapsing GOF to R-squared "
                "alone."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. After fitting Y = β₀ + β₁ x in software "
                "you see β̂₁, SE(β̂₁), R-squared, and residual "
                "plots. For a new x-star, which statement is correct?"
            ),
            body="Distinguish mean versus individual prediction; refuse selection.",
            choices=[
                c(
                    "a",
                    "A mean-response interval covers E[Y | x-star]; a "
                    "prediction interval covers a new observation and is "
                    "typically wider (adds residual variance). Running "
                    "best-subset selection is separate from post-fit inference; "
                    "slope "
                    "inference, GOF, prediction limits, and residual checks "
                    "are all required after a fit.",
                ),
                c(
                    "b",
                    "Running best-subset variable selection finishes software "
                    "fit and inference for this model.",
                    "variable_selection_finishes",
                ),
                c(
                    "c",
                    "Because the slope is significant, residual plots are "
                    "optional diagnostic theatre.",
                    "residuals_optional",
                ),
                c(
                    "d",
                    "The mean-response interval and prediction interval for "
                    "x-star are the same width because both estimate E[Y | "
                    "x-star] only.",
                    "intervals_identical",
                ),
            ],
            correct="a",
            explanation=(
                "Mean interval targets the conditional mean; prediction adds "
                "observation noise. Variable selection and optional residuals "
                "are misconceptions."
            ),
            model_answer=(
                "Mean interval for E[Y | x-star]; prediction wider; refuse "
                "selection-as-fit and optional residuals."
            ),
            common_mistake=(
                "Accepting variable selection as finishing fit, or treating "
                "residuals as optional after significance."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.1.5 Variable selection
    # ------------------------------------------------------------------
    "4.1.5-variable-selection-cs1013.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the "
                "variable-selection decision and the role of model-fit "
                "measures?"
            ),
            body="Select the explanatory-set selection statement.",
            choices=[
                c(
                    "a",
                    "Select an appropriate set of explanatory variables using "
                    "fit measures that reward fit while penalising unnecessary "
                    "complexity. More explanatory variables is not "
                    "automatically better because overfitting and diluted "
                    "interpretation can worsen the model.",
                ),
                c(
                    "b",
                    "Keep every term with p less than 0.05; that mechanical "
                    "rule completes explanatory-variable selection.",
                    "p_value_chopping",
                ),
                c(
                    "c",
                    "Variable selection for linear models is the same task as "
                    "choosing a GLM link function; both are finished by raw "
                    "R-squared alone.",
                    "glm_finishes",
                ),
                c(
                    "d",
                    "The best explanatory set always contains every available "
                    "numeric column because unused columns waste information.",
                    "more_variables_always",
                ),
            ],
            correct="a",
            explanation=(
                "Selection compares candidate explanatory sets using fit "
                "measures with complexity penalties. Mechanical p-value "
                "chopping and GLM conflation are wrong tasks."
            ),
            model_answer=(
                "Select explanatory set via fit measures; more variables is "
                "not automatically better."
            ),
            common_mistake=(
                "Mechanical p-value chopping or conflating linear selection "
                "with GLM link-and-family modelling."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Two nested linear models for claim severity: M1 "
                "uses age only; M2 adds sum insured and NCD. Which statement "
                "is correct?"
            ),
            body="Name fit measures; refuse p-chopping and GLM conflation.",
            choices=[
                c(
                    "a",
                    "Examples: adjusted R-squared (rewards fit while adjusting "
                    "for unused complexity versus raw R-squared); AIC or BIC "
                    "(likelihood fit with a parameter-count penalty). Mechanical "
                    "p-value chopping is not a complete selection warrant; GLM "
                    "uses links and exponential-family responses, not linear "
                    "explanatory selection alone.",
                ),
                c(
                    "b",
                    "Keep every term with p less than 0.05 in M2 and "
                    "selection is done; no fit measure comparison is needed.",
                    "p_value_chopping",
                ),
                c(
                    "c",
                    "Variable selection finishes GLM modelling because both "
                    "choose predictors using software output.",
                    "glm_finishes",
                ),
                c(
                    "d",
                    "Raw R-squared alone decides between M1 and M2 because "
                    "it never increases when variables are added.",
                    "raw_r2_penalty",
                ),
            ],
            correct="a",
            explanation=(
                "Adjusted R-squared and AIC/BIC penalise complexity. p-value "
                "chopping and GLM conflation do not finish linear explanatory "
                "selection."
            ),
            model_answer=(
                "Adjusted R-squared; AIC/BIC. Refuse p-chopping and GLM "
                "conflation."
            ),
            common_mistake=(
                "Accepting p-value chopping or treating selection as finishing "
                "GLM."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.1 Exponential family
    # ------------------------------------------------------------------
    "4.2.1-exponential-family-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly lists exponential-"
                "family GLM response distributions and identifies the Normal "
                "special case?"
            ),
            body="Select the GLM response-family statement.",
            choices=[
                c(
                    "a",
                    "Binomial, Poisson, exponential, gamma, and Normal are "
                    "named exponential-family GLM responses. Normal with "
                    "identity link is a special case inside the family list, "
                    "not the definition of every GLM.",
                ),
                c(
                    "b",
                    "GLM is ordinary linear regression with a different "
                    "software package name; no response distribution family "
                    "is required.",
                    "glm_is_ols",
                ),
                c(
                    "c",
                    "Only Normal responses belong in a GLM; Poisson and "
                    "binomial models are separate non-GLM procedures.",
                    "normal_only_glm",
                ),
                c(
                    "d",
                    "Any continuous response is automatically in the "
                    "exponential family because the density can be written "
                    "with an exp() somewhere.",
                    "exp_anywhere",
                ),
            ],
            correct="a",
            explanation=(
                "GLM responses sit in named exponential families. Package "
                "name or presence of exp() does not make a GLM. Normal is "
                "one family member, not the universal definition."
            ),
            model_answer=(
                "Binomial, Poisson, exponential, gamma, Normal. Normal is "
                "the special case, not the GLM definition."
            ),
            common_mistake=(
                "Treating GLM as renamed OLS or requiring only Normal "
                "responses."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Name three of binomial, Poisson, exponential, "
                "gamma, Normal as GLM responses. Which statement is correct?"
            ),
            body="Warrant family membership; refuse package-name GLM.",
            choices=[
                c(
                    "a",
                    "Example: Poisson (counts with E[Y]=Var[Y]=μ); binomial "
                    "(bounded proportion or count responses); Normal "
                    "(continuous responses with constant variance). Each has "
                    "an exponential-family density usable as a GLM response. "
                    "Package name is not GLM; a GLM response sits in an "
                    "exponential family with later eta and link.",
                ),
                c(
                    "b",
                    "GLM is just ordinary linear regression with a different "
                    "software package name; family membership is marketing.",
                    "glm_is_ols",
                ),
                c(
                    "c",
                    "Only Normal belongs in the exponential family for GLM; "
                    "Poisson and binomial are non-GLM legacy procedures.",
                    "normal_only_glm",
                ),
                c(
                    "d",
                    "Poisson belongs because the pmf contains exp(); that "
                    "single algebraic feature is the family definition without "
                    "mean-variance structure.",
                    "exp_anywhere",
                ),
            ],
            correct="a",
            explanation=(
                "Family membership needs the exponential-family form tied to "
                "the response structure, not software branding or exp() "
                "alone."
            ),
            model_answer=(
                "Poisson, binomial, Normal with one-line warrants. Refuse "
                "package-name GLM."
            ),
            common_mistake=(
                "Accepting package-name GLM or Normal-only family membership."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.2 Mean, variance, variance function, scale
    # ------------------------------------------------------------------
    "4.2.2-mean-variance-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly names the four "
                "quantities handled for a GLM response family and gives a "
                "Poisson example?"
            ),
            body="Select mean, variance, variance function, scale.",
            choices=[
                c(
                    "a",
                    "Mean, variance, variance function V(mu), and scale "
                    "(dispersion). Example: Poisson with mean lambda has "
                    "E[Y]=Var[Y]=lambda and V(μ)=μ with scale often 1.",
                ),
                c(
                    "b",
                    "Choosing the logit link finishes stating mean, variance, "
                    "variance function, and scale for any family.",
                    "link_finishes_mean_variance",
                ),
                c(
                    "c",
                    "For every GLM response, Var[Y] equals σ² "
                    "constant independent of mu; V(μ)=1 always.",
                    "constant_variance_all",
                ),
                c(
                    "d",
                    "Mean and variance are defined only after writing the "
                    "linear predictor η; family structure is secondary.",
                    "eta_first",
                ),
            ],
            correct="a",
            explanation=(
                "Family structure specifies mean, variance, V(mu), and scale. "
                "The link maps μ to η and is a separate object from the "
                "response variance structure."
            ),
            model_answer=(
                "Mean, variance, V(mu), scale. Poisson: E[Y]=Var[Y]=lambda."
            ),
            common_mistake=(
                "Letting link choice substitute for family mean-variance "
                "structure."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. For Poisson and Normal GLM responses, which "
                "statement is correct?"
            ),
            body="State E[Y], Var[Y], V(mu); refuse link-as-structure.",
            choices=[
                c(
                    "a",
                    "Poisson: E[Y]=μ, Var[Y]=μ, V(μ)=μ (scale typically 1). "
                    "Normal: E[Y]=μ, Var[Y]=σ², V(μ)=1 with scale "
                    "σ². The link maps μ to η; this question "
                    "requires the mean, variance, and scale structure of the "
                    "response family.",
                ),
                c(
                    "b",
                    "Choosing the logit link finishes stating E[Y], Var[Y], "
                    "V(mu), and scale for Poisson and Normal.",
                    "link_finishes_mean_variance",
                ),
                c(
                    "c",
                    "Poisson: E[Y]=μ, Var[Y]=σ² constant; Normal: "
                    "E[Y]=μ, Var[Y]=μ because both GLM families share the "
                    "same variance function.",
                    "families_collapsed",
                ),
                c(
                    "d",
                    "V(mu) is always mu for every exponential-family response; "
                    "Normal and Poisson therefore share Var[Y]=μ.",
                    "v_mu_universal",
                ),
            ],
            correct="a",
            explanation=(
                "Poisson has mean-variance equality; Normal has constant "
                "variance with scale σ². Link choice does not "
                "replace these family facts."
            ),
            model_answer=(
                "Poisson V(μ)=μ; Normal V(μ)=1, scale σ². Refuse "
                "link-as-structure."
            ),
            common_mistake=(
                "Accepting link choice as finishing mean-variance structure."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.3 Link and canonical link
    # ------------------------------------------------------------------
    "4.2.3-link-canonical-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines a link "
                "function, a canonical link, and canonical links for binomial "
                "and Poisson responses?"
            ),
            body="Select the link and canonical-link statement.",
            choices=[
                c(
                    "a",
                    "A link function connects the mean response mu to the "
                    "linear predictor η. A canonical link is the natural "
                    "family link equating eta with the natural parameter. "
                    "Binomial: logit; Poisson: log.",
                ),
                c(
                    "b",
                    "Whatever link the software defaults to is automatically "
                    "the canonical link for that response family.",
                    "software_default_canonical",
                ),
                c(
                    "c",
                    "Canonical link means identity for every family; logit and "
                    "log are non-canonical alternatives only.",
                    "identity_canonical_all",
                ),
                c(
                    "d",
                    "The link function is the same object as the linear "
                    "predictor eta; g(mu)=eta means eta equals X beta by "
                    "definition of link.",
                    "link_is_eta",
                ),
            ],
            correct="a",
            explanation=(
                "Link maps μ to η; canonical is family-specific natural "
                "parameter link. Software default needs a warrant, and link "
                "is not eta itself."
            ),
            model_answer=(
                "Link maps μ to η; canonical examples logit (binomial), "
                "log (Poisson)."
            ),
            common_mistake=(
                "Treating software default as canonical or equating link with "
                "eta."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. For binomial and gamma responses, which "
                "statement correctly names the canonical link and justifies it "
                "from the mean's natural range?"
            ),
            body="Name canonical links; refuse GUI default.",
            choices=[
                c(
                    "a",
                    "Binomial: logit (μ in (0,1) and logit maps to the real "
                    "line for eta). Gamma: reciprocal (negative-reciprocal "
                    "canonical form as in CMP) because μ greater than 0 maps "
                    "the positive mean onto the η scale for the gamma "
                    "exponential-family form. A software default needs a "
                    "warrant; canonical means the link equating eta with the "
                    "natural parameter.",
                ),
                c(
                    "b",
                    "Binomial: identity; gamma: log, because software defaults "
                    "are canonical by definition.",
                    "software_default_canonical",
                ),
                c(
                    "c",
                    "Binomial and gamma both use logit as canonical because "
                    "logit handles bounded means only.",
                    "logit_for_gamma",
                ),
                c(
                    "d",
                    "Canonical link is whichever link minimises deviance in the "
                    "fitted sample; it is an empirical choice, not a family "
                    "definition.",
                    "deviance_picks_link",
                ),
            ],
            correct="a",
            explanation=(
                "Logit matches binomial (0,1) mean range; gamma canonical is "
                "reciprocal form for positive mean. GUI default or deviance "
                "minimisation does not define canonical."
            ),
            model_answer=(
                "Binomial logit; gamma reciprocal canonical. Refuse default "
                "as canonical."
            ),
            common_mistake=(
                "Accepting software default as canonical or mis-assigning "
                "logit to gamma."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.4 Factors and interactions
    # ------------------------------------------------------------------
    "4.2.4-factors-interactions-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines a factor and "
                "an interaction term in a GLM?"
            ),
            body="Select the categorical factor and interaction statement.",
            choices=[
                c(
                    "a",
                    "A factor represents categorical levels with indicator "
                    "or contrast coding. An interaction term allows the effect "
                    "of one variable to depend on the level of another, "
                    "beyond main effects alone.",
                ),
                c(
                    "b",
                    "An interaction is just another main-effect slope on a "
                    "continuous variable; it never changes slope by level.",
                    "interaction_as_main",
                ),
                c(
                    "c",
                    "Factors apply only to linear regression outside GLMs; "
                    "GLMs use only continuous covariates.",
                    "factors_not_glm",
                ),
                c(
                    "d",
                    "Writing η = β₀ + β₁ x with no factor indicators "
                    "already explains categorical region levels completely.",
                    "no_factors_finishes",
                ),
            ],
            correct="a",
            explanation=(
                "Factors encode categorical levels; interactions modify joint "
                "effects. A continuous-only eta does not encode region levels, "
                "and interaction is not merely another main slope."
            ),
            model_answer=(
                "Factor: categorical levels; interaction: joint level effects "
                "beyond mains."
            ),
            common_mistake=(
                "Treating interaction as another main effect or omitting factor "
                "indicators."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Rating: continuous age x and factor region "
                "(levels North/South). Which statement is correct?"
            ),
            body="Write eta with factor and interaction; refuse no-factor eta.",
            choices=[
                c(
                    "a",
                    "η = β₀ + β₁ x + β₂ I_South + β₃ x times "
                    "I_South with North baseline. Factors encode categorical "
                    "levels; an interaction changes the age slope by region. "
                    "It is not merely another additive main effect.",
                ),
                c(
                    "b",
                    "η = β₀ + β₁ x finishes explaining factors and "
                    "interactions because region is known to the modeller.",
                    "no_factors_finishes",
                ),
                c(
                    "c",
                    "η = β₀ + β₁ x + β₂ I_South only; the "
                    "interaction is unnecessary because South adds a constant "
                    "shift equal to an interaction.",
                    "interaction_as_main",
                ),
                c(
                    "d",
                    "Region enters as numeric 1 for North and 2 for South on "
                    "the same slope as age; that is the GLM factor definition.",
                    "numeric_levels",
                ),
            ],
            correct="a",
            explanation=(
                "Factor indicator plus age-by-region interaction encodes level "
                "effects and slope change. Constant shift alone is not a full "
                "interaction story."
            ),
            model_answer=(
                "η = β₀ + β₁ x + β₂ I_South + β₃ x I_South. "
                "Refuse no-factor eta and interaction-as-main."
            ),
            common_mistake=(
                "Accepting η = β₀ + β₁ x only or treating interaction "
                "as another main effect."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.5 Linear predictor
    # ------------------------------------------------------------------
    "4.2.5-linear-predictor-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines the linear "
                "predictor eta and gives simple and factor or polynomial "
                "examples?"
            ),
            body="Select the linear predictor statement.",
            choices=[
                c(
                    "a",
                    "The linear predictor η is typically X beta on the "
                    "scale linked to the mean. Example simple: η = β₀ + "
                    "β₁ x. Example with structure: eta includes factor "
                    "indicators or polynomial powers such as x squared.",
                ),
                c(
                    "b",
                    "The link function is the linear predictor; g(mu)=eta "
                    "means eta and link are the same object.",
                    "link_is_eta",
                ),
                c(
                    "c",
                    "eta equals mu for every GLM because the linear predictor "
                    "always models the mean directly without a link.",
                    "eta_equals_mu",
                ),
                c(
                    "d",
                    "Polynomial terms belong only in Normal linear models; "
                    "Poisson GLMs forbid x squared in eta.",
                    "poly_normal_only",
                ),
            ],
            correct="a",
            explanation=(
                "η = Xβ is the linear predictor; the link maps mu to "
                "eta. Polynomial and factor terms can enter eta in GLMs when "
                "specified."
            ),
            model_answer=(
                "η = X beta; examples with x and with factor or polynomial "
                "terms."
            ),
            common_mistake=(
                "Equating link with eta or forbidding polynomial terms in GLM "
                "eta."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Poisson claim counts with log link, continuous "
                "exposure score x and two-level factor cover (Standard/Plus). "
                "Which statement is correct?"
            ),
            body="Write eta; refuse link-as-eta.",
            choices=[
                c(
                    "a",
                    "η = β₀ + β₁ x + β₂ x squared + β₃ I_Plus "
                    "with Standard baseline. η = Xβ is the linear "
                    "predictor; the link g maps mean μ to η (for example "
                    "log(μ)=η for Poisson log link).",
                ),
                c(
                    "b",
                    "The link function is the linear predictor, so log(mu) "
                    "means mu equals eta without further structure.",
                    "link_is_eta",
                ),
                c(
                    "c",
                    "η = log(mu) = β₀ + β₁ x only; quadratic and "
                    "factor terms belong in mu, not in eta.",
                    "structure_in_mu",
                ),
                c(
                    "d",
                    "η = β₀ + β₁ x + β₂ I_Plus only because "
                    "quadratic terms cannot appear in a Poisson GLM linear "
                    "predictor.",
                    "poly_normal_only",
                ),
            ],
            correct="a",
            explanation=(
                "Specified eta includes x, x squared, and cover indicator. "
                "Link maps μ to η; they are distinct objects."
            ),
            model_answer=(
                "η = β₀ + β₁ x + β₂ x^2 + β₃ I_Plus. Link maps "
                "μ to η."
            ),
            common_mistake=(
                "Treating link as eta or placing polynomial terms only in mu."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.6 Deviance and estimation
    # ------------------------------------------------------------------
    "4.2.6-deviance-estimation-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines deviance, "
                "scaled deviance, and what is estimated in a GLM?"
            ),
            body="Select the deviance and estimation statement.",
            choices=[
                c(
                    "a",
                    "Deviance compares the fitted model log-likelihood to a "
                    "saturated model. Scaled deviance divides by dispersion "
                    "or scale when relevant. GLM parameters are typically "
                    "estimated by maximum likelihood (often via IWLS).",
                ),
                c(
                    "b",
                    "Deleting insignificant terms until p-values look nice "
                    "defines deviance and finishes GLM estimation.",
                    "p_value_chopping_finishes",
                ),
                c(
                    "c",
                    "Deviance equals the sum of Pearson residuals by "
                    "definition; scaled deviance is always the same number "
                    "without dividing by scale.",
                    "pearson_is_deviance",
                ),
                c(
                    "d",
                    "GLM parameters are estimated by equating sample moments to "
                    "population moments; deviance is an optional display label.",
                    "mom_not_mle",
                ),
            ],
            correct="a",
            explanation=(
                "Deviance is a likelihood comparison to saturated fit. "
                "Mechanical p-value deletion is model choice, not deviance "
                "definition. GLM estimation is typically MLE/IWLS."
            ),
            model_answer=(
                "Deviance compares to saturated; scaled divides by scale; "
                "estimate by MLE/IWLS."
            ),
            common_mistake=(
                "Treating p-value chopping as deviance definition or moment "
                "matching as GLM estimation."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly defines deviance and "
                "scaled deviance and names the usual GLM estimation principle?"
            ),
            body="One sentence each; refuse p-value chopping.",
            choices=[
                c(
                    "a",
                    "Deviance compares the fitted model's log-likelihood to a "
                    "saturated model (2 times ℓ_sat minus ℓ_model). Scaled "
                    "deviance divides by dispersion or scale when relevant. "
                    "Parameters are typically estimated by maximum likelihood "
                    "(often via IWLS). Mechanical p-value chopping is model-"
                    "choice behaviour, not deviance definition.",
                ),
                c(
                    "b",
                    "Deviance is the difference in AIC between nested models; "
                    "scaled deviance is AIC divided by n. Estimation means "
                    "dropping terms with p greater than 0.10.",
                    "p_value_chopping_finishes",
                ),
                c(
                    "c",
                    "Deviance equals sum (y minus μ̂) squared; scaled "
                    "deviance adds sigma hat. GLM parameters are always OLS "
                    "slopes on the link scale.",
                    "ols_on_link",
                ),
                c(
                    "d",
                    "Deviance and scaled deviance are identical for Poisson "
                    "and binomial because scale is always 1 with no further "
                    "definition.",
                    "no_scaled_definition",
                ),
            ],
            correct="a",
            explanation=(
                "Deviance is twice the log-likelihood drop to saturated. "
                "Scale enters scaled deviance when dispersion matters. p-value "
                "chopping is not estimation."
            ),
            model_answer=(
                "Deviance 2(ℓ_sat - ℓ_model); scaled divides by scale; "
                "MLE/IWLS. Refuse p-chopping."
            ),
            common_mistake=(
                "Accepting p-value chopping as deviance or estimation definition."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.7 Model choice
    # ------------------------------------------------------------------
    "4.2.7-model-choice-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes analysis "
                "of deviance and the role of parameter significance in nested "
                "GLM choice?"
            ),
            body="Select nested model comparison statement.",
            choices=[
                c(
                    "a",
                    "Analysis of deviance compares nested models via deviance "
                    "differences (likelihood-ratio style). Parameter "
                    "significance checks support whether added terms are "
                    "statistically and scientifically warranted.",
                ),
                c(
                    "b",
                    "Plotting Pearson residuals finishes model choice via "
                    "analysis of deviance because large residuals imply the "
                    "full model wins.",
                    "residuals_finishes_model_choice",
                ),
                c(
                    "c",
                    "Non-nested models are always compared by raw R-squared on "
                    "the link scale; deviance differences apply only to Normal "
                    "GLMs.",
                    "r2_non_nested",
                ),
                c(
                    "d",
                    "Parameter significance alone replaces deviance comparison; "
                    "if every p-value is below 0.05, deviance difference is "
                    "unnecessary.",
                    "p_only_choice",
                ),
            ],
            correct="a",
            explanation=(
                "Nested comparison uses deviance difference with reference "
                "distribution. Residual plots are diagnostics, a different "
                "task from analysis of deviance."
            ),
            model_answer=(
                "Deviance difference for nested models; significance supports "
                "inclusion."
            ),
            common_mistake=(
                "Treating residual plots as finishing analysis of deviance."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Nested GLMs M_reduced subset M_full. Which "
                "statement is correct?"
            ),
            body="Outline deviance difference choice; refuse residual plot.",
            choices=[
                c(
                    "a",
                    "Compare deviance (or −2Δℓ) between nested "
                    "models against a chi-squared reference on the degrees-of-"
                    "freedom difference; also inspect whether added parameters "
                    "are statistically and scientifically warranted. Residual "
                    "plots are diagnostics, not nested model comparison. Model "
                    "choice here uses analysis of deviance and parameter "
                    "significance.",
                ),
                c(
                    "b",
                    "Plotting Pearson residuals finishes model choice via "
                    "analysis of deviance.",
                    "residuals_finishes_model_choice",
                ),
                c(
                    "c",
                    "Choose M_full whenever any single added p-value is below "
                    "0.05; deviance difference is redundant if significance "
                    "exists.",
                    "p_only_choice",
                ),
                c(
                    "d",
                    "Analysis of deviance applies only when both models use "
                    "Normal identity GLMs; Poisson models require raw AIC "
                    "only.",
                    "normal_only_aod",
                ),
            ],
            correct="a",
            explanation=(
                "Deviance difference with chi-squared reference compares nested "
                "GLMs. Residual plotting and p-only rules do not replace "
                "analysis of deviance."
            ),
            model_answer=(
                "Deviance difference plus parameter warrants. Residual plots "
                "are diagnostics, not model choice here."
            ),
            common_mistake=(
                "Accepting residual plots as finishing analysis of deviance."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.8 Residuals
    # ------------------------------------------------------------------
    "4.2.8-residuals-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes Pearson "
                "and deviance residuals and one diagnostic use?"
            ),
            body="Select residual definition statement.",
            choices=[
                c(
                    "a",
                    "Pearson residual uses observed minus fitted scaled by the "
                    "variance structure: (y minus μ̂) over sqrt(Var̂(Y)). "
                    "Deviance residual comes from the signed contribution of "
                    "observation i to deviance. Both help check fit, outliers, "
                    "and patterns.",
                ),
                c(
                    "b",
                    "Running a likelihood-ratio test finishes explaining "
                    "Pearson and deviance residuals because LRT and residuals "
                    "are the same diagnostic object.",
                    "lrt_finishes_residuals",
                ),
                c(
                    "c",
                    "Pearson and deviance residuals equal (y minus μ̂) "
                    "with no variance scaling in GLMs.",
                    "raw_only_residual",
                ),
                c(
                    "d",
                    "Deviance residuals apply only to Normal GLMs; Poisson and "
                    "binomial models use Pearson residuals exclusively by "
                    "definition.",
                    "deviance_normal_only",
                ),
            ],
            correct="a",
            explanation=(
                "Pearson scales by fitted variance; deviance residual comes "
                "from deviance contributions. LRT is a formal test, not the "
                "residual definition."
            ),
            model_answer=(
                "Pearson: standardised (y-μ̂)/sqrt(Var); deviance: signed "
                "deviance contribution."
            ),
            common_mistake=(
                "Collapsing residuals into LRT or omitting variance scaling."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly states the idea of a "
                "Pearson residual and a deviance residual for a GLM "
                "observation?"
            ),
            body="Define residuals; refuse LRT-as-residual.",
            choices=[
                c(
                    "a",
                    "Pearson residual: (y minus μ̂) over sqrt(Var̂(Y)), "
                    "a standardised discrepancy. Deviance residual: the signed "
                    "contribution of observation i to the deviance. Both help "
                    "check fit, outliers, and patterns. An LRT is a formal "
                    "acceptability or model-comparison test, different from "
                    "defining and using residual diagnostics.",
                ),
                c(
                    "b",
                    "Running a likelihood-ratio test finishes explaining "
                    "Pearson and deviance residuals.",
                    "lrt_finishes_residuals",
                ),
                c(
                    "c",
                    "Pearson residual equals y minus μ̂; deviance residual "
                    "equals log(y/μ̂) with no further definition.",
                    "raw_only_residual",
                ),
                c(
                    "d",
                    "Both residuals are defined only after acceptability tests "
                    "pass; before that, residuals are undefined.",
                    "residuals_after_tests",
                ),
            ],
            correct="a",
            explanation=(
                "Residuals standardise or decompose deviance at observation "
                "level. LRT compares models or assesses acceptability, a "
                "separate object."
            ),
            model_answer=(
                "Pearson standardised discrepancy; deviance signed contribution. "
                "LRT is different."
            ),
            common_mistake=(
                "Accepting LRT as finishing residual explanation."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.9 Goodness-of-fit tests
    # ------------------------------------------------------------------
    "4.2.9-goodness-tests-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly names the two "
                "acceptability tests in formal GLM goodness-of-fit checking "
                "and the question each addresses?"
            ),
            body="Select Pearson chi-square and LRT statement.",
            choices=[
                c(
                    "a",
                    "Pearson's chi-square test aggregates squared Pearson "
                    "residuals against a chi-squared reference to assess "
                    "adequacy of fit. The likelihood-ratio test compares "
                    "likelihood or deviance of the fitted model to a relevant "
                    "nested or saturated alternative.",
                ),
                c(
                    "b",
                    "Interpreting every coefficient in software output is the "
                    "Pearson chi-square test; R-squared is the likelihood-ratio "
                    "test.",
                    "coefficient_interpretation_finishes",
                ),
                c(
                    "c",
                    "Pearson chi-square and LRT are identical for GLMs with "
                    "large samples; the names differ only by software vendor.",
                    "tests_identical",
                ),
                c(
                    "d",
                    "Acceptability tests apply only before fitting; after Fit "
                    "clicks, formal tests are unnecessary.",
                    "tests_pre_fit_only",
                ),
            ],
            correct="a",
            explanation=(
                "Pearson chi-square and LRT are formal acceptability tests "
                "with distinct comparisons. Coefficient interpretation is "
                "separate from aggregate acceptability testing."
            ),
            model_answer=(
                "Pearson chi-square for aggregate adequacy; LRT for "
                "likelihood or deviance comparison."
            ),
            common_mistake=(
                "Treating coefficient interpretation as finishing acceptability "
                "tests."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You have a fitted GLM and want to judge "
                "acceptability. Which statement is correct?"
            ),
            body="Outline what each test compares; refuse coefficient-only.",
            choices=[
                c(
                    "a",
                    "Pearson chi-square: aggregate squared Pearson residuals "
                    "against a chi-squared reference (adequacy of fit). LRT: "
                    "compares likelihood or deviance of the fitted model to a "
                    "relevant nested or saturated alternative. Coefficient "
                    "interpretation is separate from acceptability "
                    "testing; this question requires applying the formal "
                    "acceptability tests.",
                ),
                c(
                    "b",
                    "Interpreting every coefficient in the software output "
                    "finishes applying acceptability tests.",
                    "coefficient_interpretation_finishes",
                ),
                c(
                    "c",
                    "Pearson chi-square equals the deviance difference between "
                    "M_full and M_reduced; LRT equals the sum of squared "
                    "Pearson residuals only.",
                    "tests_swapped",
                ),
                c(
                    "d",
                    "Acceptability is judged only by residual plots; Pearson "
                    "chi-square and LRT are optional labels for the same plot.",
                    "plots_are_tests",
                ),
            ],
            correct="a",
            explanation=(
                "Each test has a defined comparison object. Coefficient "
                "reading or residual plots alone do not replace formal "
                "acceptability tests."
            ),
            model_answer=(
                "Pearson chi-square aggregate adequacy; LRT deviance or "
                "likelihood comparison. Refuse coefficient-only."
            ),
            common_mistake=(
                "Accepting coefficient interpretation as finishing "
                "acceptability tests."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 4.2.10 Fit and interpret
    # ------------------------------------------------------------------
    "4.2.10-fit-interpret-cs1014.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes what is "
                "required beyond clicking Fit for a GLM and names three "
                "output elements to interpret?"
            ),
            body="Select fit-and-interpret requirement statement.",
            choices=[
                c(
                    "a",
                    "Fit and interpret: coefficients on the link scale, fit "
                    "measures such as deviance or AIC as warranted, and "
                    "residual or diagnostic checks. Clicking Fit alone is "
                    "incomplete without interpretation and diagnostics.",
                ),
                c(
                    "b",
                    "Clicking Fit finishes interpretation and diagnostics "
                    "because software displays all required actuarial "
                    "conclusions automatically.",
                    "fit_without_interpret",
                ),
                c(
                    "c",
                    "Fitting a GLM finishes Bayesian credibility work because "
                    "both use statistical software output.",
                    "glm_finishes_bayesian",
                ),
                c(
                    "d",
                    "Interpretation requires only the intercept; factor "
                    "coefficients and diagnostics are optional extras.",
                    "intercept_only",
                ),
            ],
            correct="a",
            explanation=(
                "GLM work includes coefficient interpretation, fit assessment, "
                "and diagnostics. Fit click alone or Bayesian conflation misses "
                "the requirement."
            ),
            model_answer=(
                "Interpret coefficients, fit measures, diagnostics; Fit alone "
                "is incomplete."
            ),
            common_mistake=(
                "Treating Fit as finishing interpretation or conflating GLM with "
                "Bayesian modelling."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You fit a Poisson log-link GLM for claim counts "
                "with factor rating class. A coefficient of 0.20 on class High "
                "vs baseline is reported. Which statement is correct?"
            ),
            body="Interpret log-link coefficient; refuse Fit-only.",
            choices=[
                c(
                    "a",
                    "Under log link, β̂ = 0.20 means the fitted mean for "
                    "High is e^{0.20} ≈ 1.22 times the baseline "
                    "class mean (multiplicative effect), other terms held fixed. "
                    "Fit without interpretation or diagnostics is incomplete; "
                    "Bayesian credibility uses prior-posterior updating, not "
                    "GLM log-link coefficient reading alone.",
                ),
                c(
                    "b",
                    "Clicking Fit finishes interpretation and diagnostics; "
                    "0.20 is read directly as a 0.20 claim count increase on "
                    "the original scale.",
                    "fit_without_interpret",
                ),
                c(
                    "c",
                    "β̂ = 0.20 means High has mean 0.20 claims because "
                    "log-link coefficients are means on the count scale.",
                    "coeff_as_mean",
                ),
                c(
                    "d",
                    "Fitting this GLM finishes Bayesian credibility premium "
                    "calculation because both use Poisson counts.",
                    "glm_finishes_bayesian",
                ),
            ],
            correct="a",
            explanation=(
                "Log-link coefficient multiplies baseline mean by exp(0.20) "
                "≈ 1.22. Additive reading on count scale is wrong. "
                "Bayesian credibility is separate."
            ),
            model_answer=(
                "exp(0.20) ≈ 1.22 times baseline mean. Refuse Fit-only "
                "and Bayesian conflation."
            ),
            common_mistake=(
                "Additive reading of log-link coefficient or Fit-only "
                "completion."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.1 Bayes' theorem
    # ------------------------------------------------------------------
    "5.1.1-bayes-theorem-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly states Bayes' "
                "theorem for events and names what a simple conditional "
                "probability update requires?"
            ),
            body="Select Bayes theorem foundation statement.",
            choices=[
                c(
                    "a",
                    "Bayes' theorem updates P(A|B) from P(B|A), P(A), and "
                    "P(B): posterior equals prior times likelihood divided by "
                    "evidence. A simple conditional update requires the "
                    "likelihood, prior, and normalising evidence, not "
                    "confusing posterior with likelihood alone.",
                ),
                c(
                    "b",
                    "P(A|B) always equals P(B|A) because conditioning is "
                    "symmetric for any events A and B.",
                    "posterior_equals_likelihood",
                ),
                c(
                    "c",
                    "Bayes' theorem means posterior equals likelihood; the "
                    "base rate P(A) never enters a flagged-claim update.",
                    "ignore_base_rate",
                ),
                c(
                    "d",
                    "Updating a conditional requires only the prior; "
                    "likelihood and evidence are optional labels.",
                    "prior_only_update",
                ),
            ],
            correct="a",
            explanation=(
                "Bayes combines prior, likelihood, and evidence. Equating "
                "P(A|B) with P(B|A) or ignoring the base rate reverses or "
                "drops required pieces."
            ),
            model_answer=(
                "P(A|B) proportional to P(B|A)P(A); normalise by P(B)."
            ),
            common_mistake=(
                "Equating posterior with likelihood or ignoring base rate."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Fraud screen: P(fraud)=0.02, P(flag|fraud)=0.90, "
                "P(flag|genuine)=0.05. A claim is flagged. Which statement is "
                "correct?"
            ),
            body="Compute P(fraud|flag); refuse likelihood-as-posterior.",
            choices=[
                c(
                    "a",
                    "P(flag)=0.90 times 0.02 + 0.05 times 0.98 = 0.018 + 0.049 "
                    "= 0.067. P(fraud|flag)=0.018/0.067 ≈ 0.269. "
                    "That equating posterior with P(flag|fraud)=0.90 ignores the "
                    "base rate; Bayes multiplies prior times likelihood and "
                    "normalises.",
                ),
                c(
                    "b",
                    "P(fraud|flag)=P(flag|fraud)=0.90 because the flag was "
                    "observed and the screen is accurate for fraud.",
                    "posterior_equals_likelihood",
                ),
                c(
                    "c",
                    "P(fraud|flag)=0.02 because the prior is the answer once "
                    "a claim is flagged.",
                    "prior_only_update",
                ),
                c(
                    "d",
                    "P(fraud|flag)=0.05 because P(flag|genuine)=0.05 dominates "
                    "the update for flagged claims.",
                    "genuine_rate_as_posterior",
                ),
            ],
            correct="a",
            explanation=(
                "Evidence P(flag)=0.067 and posterior 0.018/0.067 ≈ 0.269. "
                "Likelihood 0.90 is not the posterior. Prior alone or genuine "
                "false-flag rate alone is wrong."
            ),
            model_answer=(
                "P(flag)=0.067; P(fraud|flag) ≈ 0.269. Refuse posterior "
                "equals likelihood."
            ),
            common_mistake=(
                "Taking P(fraud|flag)=0.90 or ignoring base rate normalisation."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.2 Prior and posterior
    # ------------------------------------------------------------------
    "5.1.2-prior-posterior-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines prior, "
                "posterior, and conjugate prior, and contrasts naming "
                "conjugate with obtaining a posterior?"
            ),
            body="Select prior-posterior-conjugate statement.",
            choices=[
                c(
                    "a",
                    "Prior encodes belief about θ before data; posterior "
                    "is the updated belief after data. Conjugate prior: a "
                    "prior family closed under updating so the posterior stays "
                    "in the same family. Naming conjugate structures the update "
                    "but still requires obtaining the posterior from prior plus "
                    "data.",
                ),
                c(
                    "b",
                    "Naming a conjugate pair such as Beta-Binomial automatically "
                    "delivers the numerical posterior parameters without further "
                    "calculation from data.",
                    "conjugate_finishes_posterior",
                ),
                c(
                    "c",
                    "Prior and posterior are the same object; conjugate means "
                    "the prior equals the maximum likelihood estimate.",
                    "prior_equals_posterior",
                ),
                c(
                    "d",
                    "Conjugate prior means any prior on (0,1) for a proportion; "
                    "closure under updating is optional.",
                    "any_prior_conjugate",
                ),
            ],
            correct="a",
            explanation=(
                "Prior and posterior are distinct stages. Conjugate family "
                "closure simplifies algebra but does not replace calculating "
                "posterior parameters from data."
            ),
            model_answer=(
                "Prior before data; posterior after; conjugate keeps family. "
                "Naming is not calculating."
            ),
            common_mistake=(
                "Treating conjugate naming as finishing posterior calculation."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly defines prior, "
                "posterior, and conjugate prior and names one actuarial "
                "conjugate pair?"
            ),
            body="Define terms; refuse conjugate-as-finished.",
            choices=[
                c(
                    "a",
                    "Prior: belief about θ before data. Posterior: updated "
                    "belief after data. Conjugate: prior family closed under "
                    "updating so posterior stays in the same family. Example: "
                    "Beta-Binomial or Gamma-Poisson. Conjugate language "
                    "structures the update; you still must obtain the actual "
                    "posterior parameters from prior plus data.",
                ),
                c(
                    "b",
                    "Naming Beta-Binomial finishes obtaining the numerical "
                    "posterior for a parameter; no prior-plus-data calculation "
                    "is required.",
                    "conjugate_finishes_posterior",
                ),
                c(
                    "c",
                    "Prior equals the sample mean; posterior equals the prior "
                    "because conjugate updating leaves parameters unchanged.",
                    "prior_equals_posterior",
                ),
                c(
                    "d",
                    "Conjugate pair means prior and likelihood are independent "
                    "objects that never combine into a posterior.",
                    "no_combination",
                ),
            ],
            correct="a",
            explanation=(
                "Definitions plus example pair. Conjugate naming does not "
                "replace posterior calculation from observed data."
            ),
            model_answer=(
                "Prior, posterior, conjugate definitions; Beta-Binomial example. "
                "Refuse naming as calculating."
            ),
            common_mistake=(
                "Accepting conjugate naming as finishing posterior numerics."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.3 Simple posterior
    # ------------------------------------------------------------------
    "5.1.3-posterior-simple-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the inputs "
                "and output object for a simple posterior calculation?"
            ),
            body="Select prior-plus-likelihood to posterior statement.",
            choices=[
                c(
                    "a",
                    "Prior and likelihood together yield a posterior "
                    "distribution for the parameter. A loss-based point "
                    "estimator is a further step summarising that posterior "
                    "under a chosen loss function.",
                ),
                c(
                    "b",
                    "Having the posterior distribution automatically finishes "
                    "choosing the Bayesian point estimator under squared-error "
                    "loss; no further step exists.",
                    "posterior_finishes_loss_estimator",
                ),
                c(
                    "c",
                    "Simple posterior means the prior alone; likelihood enters "
                    "only in frequentist confidence intervals.",
                    "prior_only_posterior",
                ),
                c(
                    "d",
                    "The output object is always a credible interval; a full "
                    "posterior distribution is unnecessary once data are observed.",
                    "interval_only_output",
                ),
            ],
            correct="a",
            explanation=(
                "Posterior is the updated distribution. Point estimators under "
                "loss and intervals are subsequent summaries, not automatic "
                "byproducts of writing posterior."
            ),
            model_answer=(
                "Prior plus likelihood give posterior distribution. Loss-based "
                "point estimate is a further step."
            ),
            common_mistake=(
                "Treating posterior as automatically delivering loss-based point "
                "estimator."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Binomial n=10 with x=3 successes and Beta(2,2) "
                "prior. Which statement is correct?"
            ),
            body="State posterior parameters; refuse loss-as-automatic.",
            choices=[
                c(
                    "a",
                    "Posterior Beta(2+3, 2+7) = Beta(5,9). The posterior is the "
                    "full distribution; a loss-based point estimator (for example "
                    "posterior mean under squared-error loss) is a further step.",
                ),
                c(
                    "b",
                    "Posterior Beta(2,2) because the prior dominates with n=10 "
                    "small; successes add nothing to the parameters.",
                    "prior_unchanged",
                ),
                c(
                    "c",
                    "Posterior mean 3/10 = 0.3 is the posterior distribution; "
                    "Beta(5,9) is optional notation.",
                    "mean_is_posterior",
                ),
                c(
                    "d",
                    "Having Beta(5,9) finishes choosing the Bayesian point "
                    "estimator under squared-error loss without calculation.",
                    "posterior_finishes_loss_estimator",
                ),
            ],
            correct="a",
            explanation=(
                "Conjugate update adds successes to first shape and failures to "
                "second: Beta(5,9). Posterior mean under squared-error loss is a "
                "separate summary step."
            ),
            model_answer=(
                "Posterior Beta(5,9). Refuse posterior as automatic loss "
                "estimator."
            ),
            common_mistake=(
                "Stopping at prior, sample proportion, or treating posterior as "
                "automatic point estimator."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.4 Loss-based estimators
    # ------------------------------------------------------------------
    "5.1.4-loss-estimators-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly pairs simple loss "
                "functions with the Bayesian point estimators they typically "
                "justify?"
            ),
            body="Select squared-error and absolute-error pairing.",
            choices=[
                c(
                    "a",
                    "Squared-error loss typically justifies the posterior mean "
                    "as the Bayesian point estimator. Absolute-error loss "
                    "typically justifies the posterior median.",
                ),
                c(
                    "b",
                    "The Bayesian point estimator under any loss function is "
                    "the same object as a credible interval; both summarise "
                    "posterior uncertainty identically.",
                    "point_estimator_is_interval",
                ),
                c(
                    "c",
                    "Absolute-error loss justifies the posterior mean; squared-"
                    "error loss justifies the posterior median.",
                    "losses_swapped",
                ),
                c(
                    "d",
                    "Loss-based estimators always equal the maximum likelihood "
                    "estimate regardless of the posterior.",
                    "mle_not_posterior",
                ),
            ],
            correct="a",
            explanation=(
                "Squared error maps to posterior mean; absolute error to "
                "median. Credible interval is a set probability statement, not "
                "the same object as a point estimator."
            ),
            model_answer=(
                "Squared-error: posterior mean; absolute-error: posterior median."
            ),
            common_mistake=(
                "Collapsing point estimator into credible interval or swapping "
                "mean and median losses."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Posterior for θ is available. Which "
                "statement is correct?"
            ),
            body="Name estimators under losses; refuse interval collapse.",
            choices=[
                c(
                    "a",
                    "Under squared-error loss, use the posterior mean as the "
                    "Bayesian point estimator; under absolute-error loss, use "
                    "the posterior median. A point estimator summarises the "
                    "posterior under a loss; a credible interval is a posterior "
                    "probability set for θ. Different objects.",
                ),
                c(
                    "b",
                    "The Bayesian point estimator under loss is the same object "
                    "as a credible interval.",
                    "point_estimator_is_interval",
                ),
                c(
                    "c",
                    "Under squared-error loss, use the posterior median; under "
                    "absolute-error loss, use the posterior mean.",
                    "losses_swapped",
                ),
                c(
                    "d",
                    "Both losses justify the posterior mode only; mean and "
                    "median are frequentist labels.",
                    "mode_only",
                ),
            ],
            correct="a",
            explanation=(
                "Mean under squared error, median under absolute error. "
                "Interval and point estimator answer different questions."
            ),
            model_answer=(
                "Squared-error: mean; absolute-error: median. Refuse interval "
                "collapse."
            ),
            common_mistake=(
                "Equating point estimator with credible interval or swapping "
                "loss pairings."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.5 Credible intervals
    # ------------------------------------------------------------------
    "5.1.5-credible-intervals-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes what a "
                "credible interval says and which posterior object it uses?"
            ),
            body="Select Bayesian interval reading statement.",
            choices=[
                c(
                    "a",
                    "A credible interval is a posterior probability statement "
                    "about the parameter θ given the observed data, typically "
                    "constructed from the posterior distribution (for example "
                    "equal-tailed quantiles).",
                ),
                c(
                    "b",
                    "A 95% credible interval means that in repeated samples the "
                    "random interval covers theta 95% of the time without any "
                    "Bayesian reading.",
                    "frequentist_reading",
                ),
                c(
                    "c",
                    "Credible intervals use only the prior; the likelihood "
                    "enters credible intervals only in credibility premium "
                    "formulas.",
                    "prior_only_interval",
                ),
                c(
                    "d",
                    "A credible interval is the same object as a confidence "
                    "interval; the adjective is interchangeable in all readings.",
                    "ci_cr_collapsed",
                ),
            ],
            correct="a",
            explanation=(
                "Credible interval is posterior probability for θ. "
                "Repeated-sampling coverage slogan is the frequentist confidence "
                "interval reading unless carefully distinguished."
            ),
            model_answer=(
                "Posterior probability statement for θ using posterior "
                "distribution."
            ),
            common_mistake=(
                "Reading credible interval with frequentist repeated-coverage "
                "language only."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Posterior for risk parameter θ is Normal(0.10, "
                "0.02 squared). Which statement is correct?"
            ),
            body="Construct 95% equal-tailed interval; refuse frequentist reading.",
            choices=[
                c(
                    "a",
                    "Approximate 95% equal-tailed credible interval: 0.10 plus "
                    "or minus 1.96 times 0.02 gives about (0.0608, 0.1392). "
                    "That frequentist repeated-sampling coverage slogan is the "
                    "confidence-interval reading; a credible interval is a "
                    "posterior probability statement about θ given the data.",
                ),
                c(
                    "b",
                    "95% credible interval (0.10, 0.10) because theta equals "
                    "the posterior mean with probability 1.",
                    "degenerate_interval",
                ),
                c(
                    "c",
                    "Approximate interval (0.08, 0.12) using plus or minus one "
                    "posterior standard deviation only, which is always the "
                    "95% equal-tailed rule.",
                    "one_sd_rule",
                ),
                c(
                    "d",
                    "A 95% credible interval means that in repeated samples the "
                    "random interval covers theta 95% of the time; no Bayesian "
                    "reading is needed.",
                    "frequentist_reading",
                ),
            ],
            correct="a",
            explanation=(
                "Normal(0.10, 0.02^2) gives equal-tailed interval ≈ "
                "(0.0608, 0.1392). Frequentist coverage language misstates "
                "credible intervals."
            ),
            model_answer=(
                "Approx (0.0608, 0.1392). Credible is posterior probability for "
                "theta."
            ),
            common_mistake=(
                "Using frequentist coverage reading or wrong interval width rule."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.6 Credibility premium
    # ------------------------------------------------------------------
    "5.1.6-credibility-premium-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly writes the "
                "credibility premium with Z and states what Z weights?"
            ),
            body="Select credibility premium formula statement.",
            choices=[
                c(
                    "a",
                    "Credibility premium = Z times X̄ + (1 minus Z) times μ, "
                    "where Z weights the individual experience X̄ versus the "
                    "collateral or manual mean μ.",
                ),
                c(
                    "b",
                    "Always use full credibility Z = 1 regardless of sample "
                    "size or data quality.",
                    "full_credibility_always",
                ),
                c(
                    "c",
                    "Z weights the collateral mean only; the individual "
                    "experience enters with weight (1 minus Z) always.",
                    "z_weights_collateral",
                ),
                c(
                    "d",
                    "Credibility premium equals mu alone because collateral "
                    "information dominates individual experience by definition.",
                    "collateral_only",
                ),
            ],
            correct="a",
            explanation=(
                "Standard form blends individual and collateral means with Z on "
                "individual experience. Full credibility always or reversed "
                "weights are wrong."
            ),
            model_answer=(
                "Premium = Z X̄ + (1-Z) mu; Z weights individual experience."
            ),
            common_mistake=(
                "Always taking Z=1 or reversing weights on individual versus "
                "collateral."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Individual mean claim X̄ = 1200, collateral or "
                "manual mean μ = 1000, credibility factor Z = 0.4. Which "
                "statement is correct?"
            ),
            body="Compute premium; refuse full credibility always.",
            choices=[
                c(
                    "a",
                    "Premium = Z times X̄ + (1 minus Z) times μ = 0.4 times "
                    "1200 + 0.6 times 1000 = 480 + 600 = 1080. Z is the weight "
                    "on the individual experience versus the collateral mean. "
                    "With limited or noisy data, Z less than 1 shrinks toward the "
                    "collateral or manual mean.",
                ),
                c(
                    "b",
                    "Premium = 1200 because individual experience must always "
                    "receive full credibility Z = 1.",
                    "full_credibility_always",
                ),
                c(
                    "c",
                    "Premium = 0.4 times 1000 + 0.6 times 1200 = 1120 because Z "
                    "weights the collateral mean.",
                    "z_weights_collateral",
                ),
                c(
                    "d",
                    "Premium = 1000 because collateral mean mu is the credibility "
                    "premium by definition.",
                    "collateral_only",
                ),
            ],
            correct="a",
            explanation=(
                "Arithmetic gives 1080. Z=0.4 on individual experience pulls "
                "toward mu. Full credibility or reversed weights misapply the "
                "formula."
            ),
            model_answer=(
                "Premium = 1080; Z weights individual experience."
            ),
            common_mistake=(
                "Always using Z=1 or swapping weights to collateral."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.7 Bayesian credibility approach
    # ------------------------------------------------------------------
    "5.1.7-bayesian-credibility-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly distinguishes the "
                "Bayesian credibility approach in simple cases and names the "
                "premium object calculated?"
            ),
            body="Select Bayesian credibility approach statement.",
            choices=[
                c(
                    "a",
                    "Bayesian credibility uses an explicit prior or structural "
                    "distribution for risk parameters. The premium object is "
                    "Z times X̄ + (1 minus Z) times μ with Z and mu determined "
                    "theoretically from the prior structure in simple cases.",
                ),
                c(
                    "b",
                    "Applying Bayesian credibility finishes the Empirical Bayes "
                    "approach because both yield a numeric premium.",
                    "bayesian_finishes_eb",
                ),
                c(
                    "c",
                    "Bayesian credibility never supplies mu or Z; only Empirical "
                    "Bayes defines those quantities.",
                    "eb_only_supplies",
                ),
                c(
                    "d",
                    "The premium object is the posterior mean only; Z and mu "
                    "never appear in Bayesian credibility.",
                    "posterior_mean_only",
                ),
            ],
            correct="a",
            explanation=(
                "Bayesian approach treats structural parameters as known from "
                "prior structure. Empirical Bayes estimates them from data, a "
                "different approach."
            ),
            model_answer=(
                "Explicit prior structure supplies mu and Z; premium Z X̄ + "
                "(1-Z) mu."
            ),
            common_mistake=(
                "Collapsing Bayesian credibility into Empirical Bayes."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. In a simple Bayesian credibility setup with known "
                "structural parameters, the credibility premium takes the form "
                "Z times X̄ + (1 minus Z) times μ. Which statement is "
                "correct?"
            ),
            body="State what prior supplies; refuse EB conflation.",
            choices=[
                c(
                    "a",
                    "The prior or known structural distribution supplies the "
                    "overall mean and variance components so mu and Z are "
                    "determined theoretically, then combined with observed "
                    "X̄. Empirical Bayes estimates those structural parameters "
                    "from data; a different approach from treating them as known "
                    "in the Bayesian calculation.",
                ),
                c(
                    "b",
                    "Applying Bayesian credibility finishes the Empirical Bayes "
                    "approach.",
                    "bayesian_finishes_eb",
                ),
                c(
                    "c",
                    "mu and Z must be estimated from collective data even in "
                    "the fully Bayesian setup; prior structure supplies nothing.",
                    "eb_only_supplies",
                ),
                c(
                    "d",
                    "Structural parameters are always user-chosen constants "
                    "unrelated to any prior; Z equals 1 by definition.",
                    "arbitrary_z",
                ),
            ],
            correct="a",
            explanation=(
                "Known structural parameters from prior theory yield mu and Z. "
                "EB estimates structural parameters from collective experience."
            ),
            model_answer=(
                "Prior supplies mean and variance components for mu and Z. EB "
                "estimates structurals from data."
            ),
            common_mistake=(
                "Accepting Bayesian credibility as finishing Empirical Bayes."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.8 Empirical Bayes
    # ------------------------------------------------------------------
    "5.1.8-empirical-bayes-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes how "
                "Empirical Bayes obtains structural parameters differently "
                "from a fully specified Bayesian prior and names the premium "
                "derived?"
            ),
            body="Select Empirical Bayes move statement.",
            choices=[
                c(
                    "a",
                    "Empirical Bayes estimates structural parameters from "
                    "collective data rather than treating them as fully specified "
                    "by a prior alone. The credibility premium Ẑ times X̄ "
                    "+ (1 minus Ẑ) times μ-hat follows after plugging "
                    "estimated structural parameters into the credibility formula.",
                ),
                c(
                    "b",
                    "Empirical Bayes and fully Bayesian credibility always use "
                    "identical assumptions for structural parameters.",
                    "same_assumptions",
                ),
                c(
                    "c",
                    "Empirical Bayes obtains the premium only by applying Bayes' "
                    "theorem to a single claim; collective data never enter.",
                    "single_claim_only",
                ),
                c(
                    "d",
                    "Empirical Bayes means choosing Z = 1 always because data "
                    "estimate full credibility automatically.",
                    "full_credibility_eb",
                ),
            ],
            correct="a",
            explanation=(
                "EB estimates overall mean and process variance components from "
                "collective experience, then forms credibility premium. Same "
                "assumptions as fully Bayesian is incorrect."
            ),
            model_answer=(
                "Estimate structurals from collective data; premium Ẑ X̄ "
                "+ (1-Ẑ) μ̂."
            ),
            common_mistake=(
                "Treating EB as identical assumptions or single-claim update."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly outlines the Empirical "
                "Bayes move to obtain a credibility premium when structural "
                "parameters are unknown?"
            ),
            body="Outline EB premium; refuse contrast-as-finished.",
            choices=[
                c(
                    "a",
                    "Estimate structural parameters (for example overall mean "
                    "and process or variance components) from the collective "
                    "data, plug them into the credibility formula to get Ẑ "
                    "and μ̂, then form Ẑ times X̄ + (1 minus Ẑ) "
                    "times μ-hat for the risk. Computing one EB premium is not "
                    "the same task as contrasting assumption sets of Bayes versus "
                    "EB.",
                ),
                c(
                    "b",
                    "Computing one EB premium finishes explaining how Bayesian "
                    "and Empirical Bayes differ in assumptions.",
                    "eb_premium_finishes_contrast",
                ),
                c(
                    "c",
                    "Empirical Bayes requires a fully specified prior before any "
                    "data; collective estimation is unnecessary.",
                    "prior_required_first",
                ),
                c(
                    "d",
                    "Structural parameters are set to sample proportions only; "
                    "no credibility formula is used afterward.",
                    "no_credibility_formula",
                ),
            ],
            correct="a",
            explanation=(
                "EB pipeline: estimate structurals, plug into credibility form, "
                "compute premium. That calculation differs from the contrast LO "
                "about assumptions."
            ),
            model_answer=(
                "Estimate structurals from collective data; plug into Z and mu; "
                "form premium."
            ),
            common_mistake=(
                "Treating one EB premium calculation as finishing Bayes versus "
                "EB contrast."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 5.1.9 Bayesian vs Empirical Bayes
    # ------------------------------------------------------------------
    "5.1.9-bayes-vs-eb-cs1015.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly names assumption "
                "differences between fully Bayesian credibility and Empirical "
                "Bayes and explains why premiums may differ?"
            ),
            body="Select Bayes versus EB contrast statement.",
            choices=[
                c(
                    "a",
                    "Fully Bayesian credibility treats structural or prior "
                    "parameters as specified within a prior model. Empirical "
                    "Bayes estimates those structural parameters from observed "
                    "collective data. Different assumptions about structural "
                    "knowledge can yield different premiums.",
                ),
                c(
                    "b",
                    "Bayesian and Empirical Bayes are the same method with "
                    "different names; premiums must always agree.",
                    "same_method",
                ),
                c(
                    "c",
                    "Premiums differ only because software packages differ; "
                    "assumptions about structural parameters are identical.",
                    "software_only_difference",
                ),
                c(
                    "d",
                    "Empirical Bayes always uses a specified prior; fully "
                    "Bayesian credibility never uses prior structure.",
                    "assumptions_reversed",
                ),
            ],
            correct="a",
            explanation=(
                "Key contrast is specified structural knowledge versus "
                "estimated from collective data. Same method or software-only "
                "differences misstate the approaches."
            ),
            model_answer=(
                "Bayes: specified prior structure; EB: estimated structurals. "
                "Premiums can differ."
            ),
            common_mistake=(
                "Treating Bayes and EB as identical or reversing who specifies "
                "structure."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly states one key "
                "assumption difference between a fully Bayesian credibility "
                "approach and Empirical Bayes?"
            ),
            body="Contrast assumptions; refuse same-method claim.",
            choices=[
                c(
                    "a",
                    "Bayesian treats structural or prior parameters as specified "
                    "within a prior model; Empirical Bayes estimates those "
                    "structural parameters from the observed collective data. They "
                    "differ in how structural knowledge enters; contrasting them "
                    "does not replace separate posterior, interval, and "
                    "premium calculations.",
                ),
                c(
                    "b",
                    "Bayesian and Empirical Bayes are the same method with "
                    "different names.",
                    "same_method",
                ),
                c(
                    "c",
                    "Contrasting them means every prior calculation, posterior, "
                    "loss estimator, and premium formula is already finished.",
                    "contrast_finishes_all",
                ),
                c(
                    "d",
                    "Empirical Bayes specifies all structural parameters in "
                    "advance; Bayesian credibility estimates them only from "
                    "collective data.",
                    "assumptions_reversed",
                ),
            ],
            correct="a",
            explanation=(
                "Specified versus estimated structural parameters is the core "
                "difference. Same-method and all-formulas-finished claims are "
                "misconceptions."
            ),
            model_answer=(
                "Specified prior structure vs estimated structurals from "
                "collective data."
            ),
            common_mistake=(
                "Accepting same-method claim or reversed assumption roles."
            ),
        ),
    },
}

# Inventory filename -> campaign twin relative path under educational_campaigns/cs1/
CAMPAIGN_TWINS: dict[str, str] = {
    "4.1.1-response-explanatory-cs1013.json": "campaign-nu-cs1013/packages/4.1.1-response-explanatory-cs1013.json",
    "4.1.2-simple-multiple-cs1013.json": "campaign-nu-cs1013/packages/4.1.2-simple-multiple-cs1013.json",
    "4.1.3-least-squares-cs1013.json": "campaign-nu-cs1013/packages/4.1.3-least-squares-cs1013.json",
    "4.1.4-software-fit-cs1013.json": "campaign-nu-cs1013/packages/4.1.4-software-fit-cs1013.json",
    "4.1.5-variable-selection-cs1013.json": "campaign-nu-cs1013/packages/4.1.5-variable-selection-cs1013.json",
    "4.2.1-exponential-family-cs1014.json": "campaign-xi-cs1014/packages/4.2.1-exponential-family-cs1014.json",
    "4.2.2-mean-variance-cs1014.json": "campaign-xi-cs1014/packages/4.2.2-mean-variance-cs1014.json",
    "4.2.3-link-canonical-cs1014.json": "campaign-xi-cs1014/packages/4.2.3-link-canonical-cs1014.json",
    "4.2.4-factors-interactions-cs1014.json": "campaign-xi-cs1014/packages/4.2.4-factors-interactions-cs1014.json",
    "4.2.5-linear-predictor-cs1014.json": "campaign-xi-cs1014/packages/4.2.5-linear-predictor-cs1014.json",
    "4.2.6-deviance-estimation-cs1014.json": "campaign-xi-cs1014/packages/4.2.6-deviance-estimation-cs1014.json",
    "4.2.7-model-choice-cs1014.json": "campaign-xi-cs1014/packages/4.2.7-model-choice-cs1014.json",
    "4.2.8-residuals-cs1014.json": "campaign-xi-cs1014/packages/4.2.8-residuals-cs1014.json",
    "4.2.9-goodness-tests-cs1014.json": "campaign-xi-cs1014/packages/4.2.9-goodness-tests-cs1014.json",
    "4.2.10-fit-interpret-cs1014.json": "campaign-xi-cs1014/packages/4.2.10-fit-interpret-cs1014.json",
    "5.1.1-bayes-theorem-cs1015.json": "campaign-omicron-cs1015/packages/5.1.1-bayes-theorem-cs1015.json",
    "5.1.2-prior-posterior-cs1015.json": "campaign-omicron-cs1015/packages/5.1.2-prior-posterior-cs1015.json",
    "5.1.3-posterior-simple-cs1015.json": "campaign-omicron-cs1015/packages/5.1.3-posterior-simple-cs1015.json",
    "5.1.4-loss-estimators-cs1015.json": "campaign-omicron-cs1015/packages/5.1.4-loss-estimators-cs1015.json",
    "5.1.5-credible-intervals-cs1015.json": "campaign-omicron-cs1015/packages/5.1.5-credible-intervals-cs1015.json",
    "5.1.6-credibility-premium-cs1015.json": "campaign-omicron-cs1015/packages/5.1.6-credibility-premium-cs1015.json",
    "5.1.7-bayesian-credibility-cs1015.json": "campaign-omicron-cs1015/packages/5.1.7-bayesian-credibility-cs1015.json",
    "5.1.8-empirical-bayes-cs1015.json": "campaign-omicron-cs1015/packages/5.1.8-empirical-bayes-cs1015.json",
    "5.1.9-bayes-vs-eb-cs1015.json": "campaign-omicron-cs1015/packages/5.1.9-bayes-vs-eb-cs1015.json",
}


# Campaign package stem (filename without .json) -> inventory conversion key
STEM_TO_INVENTORY: dict[str, str] = {
    "4.1.1-response-explanatory-cs1013": "4.1.1-response-explanatory-cs1013.json",
    "4.1.2-simple-multiple-cs1013": "4.1.2-simple-multiple-cs1013.json",
    "4.1.3-least-squares-cs1013": "4.1.3-least-squares-cs1013.json",
    "4.1.4-software-fit-cs1013": "4.1.4-software-fit-cs1013.json",
    "4.1.5-variable-selection-cs1013": "4.1.5-variable-selection-cs1013.json",
    "4.2.1-exponential-family-cs1014": "4.2.1-exponential-family-cs1014.json",
    "4.2.2-mean-variance-cs1014": "4.2.2-mean-variance-cs1014.json",
    "4.2.3-link-canonical-cs1014": "4.2.3-link-canonical-cs1014.json",
    "4.2.4-factors-interactions-cs1014": "4.2.4-factors-interactions-cs1014.json",
    "4.2.5-linear-predictor-cs1014": "4.2.5-linear-predictor-cs1014.json",
    "4.2.6-deviance-estimation-cs1014": "4.2.6-deviance-estimation-cs1014.json",
    "4.2.7-model-choice-cs1014": "4.2.7-model-choice-cs1014.json",
    "4.2.8-residuals-cs1014": "4.2.8-residuals-cs1014.json",
    "4.2.9-goodness-tests-cs1014": "4.2.9-goodness-tests-cs1014.json",
    "4.2.10-fit-interpret-cs1014": "4.2.10-fit-interpret-cs1014.json",
    "5.1.1-bayes-theorem-cs1015": "5.1.1-bayes-theorem-cs1015.json",
    "5.1.2-prior-posterior-cs1015": "5.1.2-prior-posterior-cs1015.json",
    "5.1.3-posterior-simple-cs1015": "5.1.3-posterior-simple-cs1015.json",
    "5.1.4-loss-estimators-cs1015": "5.1.4-loss-estimators-cs1015.json",
    "5.1.5-credible-intervals-cs1015": "5.1.5-credible-intervals-cs1015.json",
    "5.1.6-credibility-premium-cs1015": "5.1.6-credibility-premium-cs1015.json",
    "5.1.7-bayesian-credibility-cs1015": "5.1.7-bayesian-credibility-cs1015.json",
    "5.1.8-empirical-bayes-cs1015": "5.1.8-empirical-bayes-cs1015.json",
    "5.1.9-bayes-vs-eb-cs1015": "5.1.9-bayes-vs-eb-cs1015.json",
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace AR/CP knowledge_checks with Batch 2 MCQ content when stem is in scope."""
    inv_key = STEM_TO_INVENTORY.get(stem)
    if not inv_key:
        return pkg
    parts = CONVERSIONS[inv_key]
    new_checks: list[dict[str, Any]] = []
    for check in pkg.get("knowledge_checks") or []:
        kind = check.get("kind")
        if kind == "active_recall":
            updated = dict(check)
            updated.update(parts["ar"])
            new_checks.append(updated)
        elif kind == "checkpoint":
            updated = dict(check)
            updated.update(parts["cp"])
            new_checks.append(updated)
        else:
            new_checks.append(check)
    pkg["knowledge_checks"] = new_checks
    return pkg

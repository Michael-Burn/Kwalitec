#!/usr/bin/env python3
"""Batch 3 MCQ conversion payload for Memory Front + Publication Front (Batch C).

Applies deterministic MCQ rewrites to Active Recall + Checkpoint items for:
  - Campaign Pi CS1-016 remaining Memory Front (2.1.3, 2.2.1, 2.5.1, 2.6.1, 4.1.1, 5.1.1)
  - Campaign Rho CS1-017 Publication Front (1.1.1 through 2.1.2)

Section 3 Pi packages (3.1.1, 3.2.1, 3.3.1) remain in Batch 1 payload.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

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
    # Pi Memory Front (remaining 6)
    # ------------------------------------------------------------------
    "cp-2.1.3-prob-quantiles-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes probability and "
                "quantile evaluation for a named univariate distribution?"
            ),
            body="Select the probability/quantile retrieval move.",
            choices=[
                c(
                    "a",
                    "For a placed univariate family, evaluate a probability such as "
                    "P(X > x) from the CDF or survival function, and evaluate a quantile "
                    "by inverting the CDF to solve F(x) = p for x.",
                ),
                c(
                    "b",
                    "Naming the distribution family (for example Exponential) completes "
                    "probability and quantile evaluation; no calculation is required once "
                    "the family is recognised.",
                    "recognition_as_evaluation",
                ),
                c(
                    "c",
                    "A quantile is always the sample mean of the distribution; "
                    "probabilities are read directly from a joint table of (X, Y).",
                    "quantile_as_mean",
                ),
                c(
                    "d",
                    "Probability evaluation for univariate X requires first obtaining "
                    "marginals by summing out Y from a joint distribution.",
                    "joint_required_for_univariate",
                ),
            ],
            correct="a",
            explanation=(
                "Univariate probability and quantile work uses the one-dimensional "
                "CDF or survival function. Recognition alone is not evaluation, and "
                "joint machinery is not the primary move for a single named univariate "
                "family."
            ),
            model_answer=(
                "Use CDF/survival for probabilities; invert CDF for quantiles on a "
                "named univariate family."
            ),
            common_mistake=(
                "Treating family recognition as finished evaluation, or pulling joint "
                "steps into a univariate task."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Claim sizes are Exponential with mean θ = 1000. Which "
                "statement is correct?"
            ),
            body="Compute P(X > 2000) and the 90th percentile; refuse recognition-as-evaluation.",
            choices=[
                c(
                    "a",
                    "P(X > 2000) = e^{-2} ≈ 0.135. The 90th percentile solves "
                    "1 − e^{-x/1000} = 0.9, giving x = 1000 ln(10) ≈ 2302.6. Naming "
                    "Exponential does not replace these calculations.",
                ),
                c(
                    "b",
                    "P(X > 2000) = 0.5 because the threshold 2000 is twice the mean "
                    "1000, so the tail probability is one half.",
                    "mean_ratio_as_probability",
                ),
                c(
                    "c",
                    "The 90th percentile is 900 because 0.9 × 1000 = 900 for any "
                    "Exponential with mean θ.",
                    "percentile_times_mean",
                ),
                c(
                    "d",
                    "Once the model is Exponential(θ = 1000), probability and quantile "
                    "questions are answered by naming the family; numeric evaluation is "
                    "optional decoration.",
                    "recognition_as_evaluation",
                ),
            ],
            correct="a",
            explanation=(
                "Survival gives e^{-2000/1000}. Quantile inversion gives 1000 ln(10). "
                "Halving by mean ratio, scaling the mean by 0.9, or stopping at "
                "recognition are all wrong."
            ),
            model_answer=(
                "P(X > 2000) ≈ 0.135; 90th percentile ≈ 2302.6; refuse recognition-only."
            ),
            common_mistake=(
                "Heuristic mean ratios, linear scaling of the mean for quantiles, or "
                "recognition without calculation."
            ),
        ),
    },
    "cp-2.2.1-marginal-conditional-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes how marginals and "
                "conditionals are obtained from a joint distribution?"
            ),
            body="Select marginal vs conditional construction.",
            choices=[
                c(
                    "a",
                    "A marginal sums or integrates the joint over the other variable(s). "
                    "A conditional renormalises the joint on the given condition, "
                    "dividing by the marginal probability of that condition.",
                ),
                c(
                    "b",
                    "Marginal and conditional distributions are optional decorations "
                    "once the joint table or density is written; the joint already "
                    "contains all required information without extraction.",
                    "joint_as_margins_done",
                ),
                c(
                    "c",
                    "A conditional P(Y | X = x) equals the joint entry P(X = x, Y) "
                    "with no division by P(X = x).",
                    "conditional_without_normalise",
                ),
                c(
                    "d",
                    "A marginal distribution is obtained by dividing each joint cell "
                    "by the grand total of all cells; conditionals use the same rule.",
                    "grand_total_only",
                ),
            ],
            correct="a",
            explanation=(
                "Marginals sum/integrate out partners; conditionals divide the joint "
                "by the conditioning event's probability. Skipping extraction or "
                "omitting normalisation confuses joint with margin or conditional."
            ),
            model_answer=(
                "Marginal: sum/integrate joint; conditional: joint divided by "
                "P(condition)."
            ),
            common_mistake=(
                "Treating the joint as sufficient without marginals/conditionals, or "
                "forgetting to divide by P(X = x)."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Joint PMF of (X, Y): P(0,0)=0.10, P(0,1)=0.20, "
                "P(1,0)=0.30, P(1,1)=0.40. Which statement is correct?"
            ),
            body="Compute P(X=1) and P(Y=1 | X=1); refuse joint-as-margins-done.",
            choices=[
                c(
                    "a",
                    "P(X=1) = 0.30 + 0.40 = 0.70. P(Y=1 | X=1) = 0.40 / 0.70 ≈ 0.571. "
                    "The joint table is not interchangeable with its margins or "
                    "conditionals without these moves.",
                ),
                c(
                    "b",
                    "P(X=1) = 0.40 because P(1,1) is the largest cell, so X = 1 is "
                    "identified with that cell alone.",
                    "largest_cell_as_marginal",
                ),
                c(
                    "c",
                    "P(Y=1 | X=1) = 0.40 because the conditional equals the joint "
                    "entry P(1,1) with no further normalisation.",
                    "conditional_without_normalise",
                ),
                c(
                    "d",
                    "P(X=1) = 0.70 and P(Y=1 | X=1) = 0.60 because (0.30 + 0.40) and "
                    "(0.20 + 0.40) are both needed for the conditional numerator.",
                    "wrong_conditional_numerator",
                ),
            ],
            correct="a",
            explanation=(
                "Marginal sums the X = 1 row. Conditional divides 0.40 by 0.70. "
                "Using one cell as the marginal, skipping division, or wrong numerator "
                "are standard joint-table errors."
            ),
            model_answer=(
                "P(X=1)=0.70; P(Y=1|X=1)≈0.571; refuse joint-as-margins-done."
            ),
            common_mistake=(
                "Largest-cell shortcut, conditional without normalising, or wrong "
                "numerator for P(Y=1|X=1)."
            ),
        ),
    },
    "cp-2.5.1-clt-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly states the central limit "
                "theorem for an IID sequence and what it approximates?"
            ),
            body="Select the CLT statement and its target object.",
            choices=[
                c(
                    "a",
                    "For an IID sequence with finite mean and variance, the "
                    "distribution of the sample mean X̄ (equivalently a standardised "
                    "X̄) approaches Normal as n grows, giving a Normal approximation "
                    "for sample-mean probabilities under stated conditions.",
                ),
                c(
                    "b",
                    "The CLT says every insurance quantity is Normal, so any routine "
                    "Normal model needs no theorem statement or IID conditions.",
                    "normal_everywhere",
                ),
                c(
                    "c",
                    "The CLT approximates the distribution of a single observation X₁ "
                    "as Normal whenever the population has a finite mean, regardless of "
                    "sample size.",
                    "clt_on_single_observation",
                ),
                c(
                    "d",
                    "The CLT applies only when the population is already Normal; for "
                    "non-Normal populations the sample mean cannot be approximated.",
                    "population_must_be_normal",
                ),
            ],
            correct="a",
            explanation=(
                "CLT targets the sample mean (or its standardised form) under IID "
                "with finite variance. Casual Normal habit, single-X claims, or "
                "requiring a Normal population misstate the theorem."
            ),
            model_answer=(
                "IID, finite mean/variance → sample mean ≈ Normal for large n."
            ),
            common_mistake=(
                "Normal-by-habit, CLT on one observation, or population must be "
                "Normal."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Claim sizes are iid with mean μ = 500 and sd σ = 200; "
                "n = 100. Using the CLT, which statement about P(X̄ > 540) is correct? "
                "(Use Φ(2) ≈ 0.977.)"
            ),
            body="Approximate distribution of X̄, standardise, and refuse Normal-by-habit.",
            choices=[
                c(
                    "a",
                    "X̄ ≈ Normal(μ = 500, sd = σ/√n = 20). z = (540 − 500)/20 = 2, so "
                    "P(X̄ > 540) ≈ 1 − Φ(2) ≈ 0.023. Casual Normal use without stating "
                    "IID CLT conditions is not the same skill.",
                ),
                c(
                    "b",
                    "X̄ ≈ Normal(500, 200) because σ = 200 is the population sd, so "
                    "P(X̄ > 540) ≈ 1 − Φ(0.2) without dividing by √n.",
                    "forget_sqrt_n",
                ),
                c(
                    "c",
                    "P(X̄ > 540) ≈ 0.5 because 540 exceeds the mean 500, so the sample "
                    "mean is above average.",
                    "above_mean_half",
                ),
                c(
                    "d",
                    "P(X̄ > 540) ≈ 0.977 because z = 2 and Φ(2) ≈ 0.977 is the "
                    "upper-tail probability directly.",
                    "phi_as_upper_tail",
                ),
            ],
            correct="a",
            explanation=(
                "Standard error is 200/10 = 20. z = 2 gives upper tail 0.023. Using σ "
                "instead of σ/√n, a 0.5 heuristic, or reading Φ(2) as the upper tail "
                "are common errors."
            ),
            model_answer=(
                "X̄ ≈ N(500, 20); z = 2; P ≈ 0.023; refuse Normal-by-habit."
            ),
            common_mistake=(
                "Forgetting √n in the standard error, heuristic 0.5, or misreading Φ."
            ),
        ),
    },
    "cp-2.6.1-random-samples-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines a random sample from "
                "a population and why sampling precedes estimator construction?"
            ),
            body="Select the sampling warrant and inference ordering.",
            choices=[
                c(
                    "a",
                    "A random sample is drawn so observations follow the population "
                    "distribution under a stated sampling model (for example iid draws). "
                    "Estimator and interval procedures require this warrant; a pile of "
                    "observations is not automatically a random sample.",
                ),
                c(
                    "b",
                    "Any n observations collected in practice constitute a random sample "
                    "because having data is sufficient for inference formulas to apply.",
                    "n_observations_as_sample",
                ),
                c(
                    "c",
                    "A random sample means the sample mean equals the population mean; "
                    "once that equality holds, the sampling model is verified.",
                    "sample_mean_equals_population",
                ),
                c(
                    "d",
                    "Sampling vocabulary is optional because estimator formulas can be "
                    "applied to any spreadsheet column without a population model.",
                    "estimators_without_sampling",
                ),
            ],
            correct="a",
            explanation=(
                "Random sample is about how data relate to a population model, not "
                "merely count or accidental equality of means. Estimators presuppose "
                "a sampling story."
            ),
            model_answer=(
                "Lawful draw from population model; observations alone are not enough."
            ),
            common_mistake=(
                "Equating n observations with a random sample, or skipping the sampling "
                "warrant before estimators."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. An analyst takes the 40 most recent claims from one "
                "large commercial client and treats them as a random sample from the "
                "whole motor book. Which statement is correct?"
            ),
            body="Judge sampling warrant; refuse n-observations-as-random-sample.",
            choices=[
                c(
                    "a",
                    "Consecutive claims from one client are clustered and not an iid "
                    "draw from the portfolio population; dependence and selection bias "
                    "break the random-sample warrant. Having n = 40 observations does "
                    "not by itself create a random sample.",
                ),
                c(
                    "b",
                    "Because n = 40 exceeds a common rule-of-thumb threshold, the "
                    "extract is a random sample of the motor book regardless of how "
                    "it was selected.",
                    "n_observations_as_sample",
                ),
                c(
                    "c",
                    "If the sample mean claim size is close to the book average, the "
                    "selection mechanism is validated and the extract counts as a "
                    "random sample.",
                    "sample_mean_equals_population",
                ),
                c(
                    "d",
                    "Random-sample language applies only after an estimator is chosen; "
                    "until then any claims file may be treated as a population draw.",
                    "estimators_without_sampling",
                ),
            ],
            correct="a",
            explanation=(
                "Selection from one client breaks portfolio-level iid sampling. Large "
                "n, similar means, or deferred vocabulary do not repair the warrant."
            ),
            model_answer=(
                "Selection bias breaks random sample; n alone is insufficient."
            ),
            common_mistake=(
                "Large-n rule, mean-match validation, or treating sampling as optional."
            ),
        ),
    },
    "cp-4.1.1-linear-regression-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly assigns response and "
                "explanatory roles in a linear regression modelling question?"
            ),
            body="Select Y, X, and the modelling warrant.",
            choices=[
                c(
                    "a",
                    "The response variable Y is the outcome being modelled or predicted; "
                    "explanatory variables X are predictors thought to help explain or "
                    "predict Y, each with a modelling warrant for the stated question.",
                ),
                c(
                    "b",
                    "Every numeric column in a data set is automatically an explanatory "
                    "variable; the response is whichever column has the largest variance.",
                    "column_soup",
                ),
                c(
                    "c",
                    "Response and explanatory roles are defined only after writing the "
                    "full multiple regression equation; roles cannot be stated before "
                    "model form.",
                    "model_form_first",
                ),
                c(
                    "d",
                    "The response is always the column entered last in the software "
                    "formula because estimation order defines Y.",
                    "software_order_defines_y",
                ),
            ],
            correct="a",
            explanation=(
                "Y is the outcome for the modelling question; X variables are chosen "
                "with warrants. Column-soup, equation-first, or software order do not "
                "replace role assignment."
            ),
            model_answer=(
                "Y = outcome modelled; X = predictors with warrants."
            ),
            common_mistake=(
                "Column-soup, delaying roles until equation form, or software-order "
                "rules."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Household contents book: model renewal premium. Columns "
                "include renewal premium, sum insured, bedrooms, previous claims count, "
                "and postcode band. Which statement is correct?"
            ),
            body="Name Y and warranted X variables; refuse column-soup and role-swap.",
            choices=[
                c(
                    "a",
                    "Response Y = renewal premium (outcome to explain). Explanatory "
                    "examples: sum insured and bedrooms as predictors of premium level; "
                    "previous claims count may also warrant as an X. Putting every "
                    "numeric column on the right-hand side is not role modelling, and "
                    "treating premium as an X for sum insured answers a different "
                    "question.",
                ),
                c(
                    "b",
                    "Response Y = sum insured; renewal premium, bedrooms, and claims "
                    "count are explanatory because all numeric fields belong on the "
                    "right-hand side.",
                    "column_soup",
                ),
                c(
                    "c",
                    "Response Y = renewal premium; premium must also be an explanatory "
                    "variable for bedrooms because both appear in the same policy record.",
                    "role_swap",
                ),
                c(
                    "d",
                    "No response can be named until a regression equation is fully "
                    "written; premium modelling starts with equation form, not Y versus X.",
                    "model_form_first",
                ),
            ],
            correct="a",
            explanation=(
                "Premium is the outcome for this question. Sum insured and bedrooms "
                "are plausible X's. Column-soup, self-prediction, or equation-first "
                "delay are wrong."
            ),
            model_answer=(
                "Y = renewal premium; X examples: sum insured, bedrooms; refuse "
                "column-soup."
            ),
            common_mistake=(
                "Column-soup, swapping Y and X, or requiring equation before roles."
            ),
        ),
    },
    "cp-5.1.1-bayes-theorem-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly states Bayes' theorem for a "
                "simple conditional probability update?"
            ),
            body="Select the Bayes update with prior, likelihood, and evidence.",
            choices=[
                c(
                    "a",
                    "Bayes' theorem updates P(A|B) from P(B|A), P(A), and P(B): "
                    "posterior equals prior times likelihood divided by evidence. A "
                    "simple update requires all three pieces, not confusing posterior "
                    "with likelihood alone.",
                ),
                c(
                    "b",
                    "P(A|B) always equals P(B|A) because conditioning is symmetric "
                    "for any events A and B.",
                    "posterior_equals_likelihood",
                ),
                c(
                    "c",
                    "Bayes' theorem means posterior equals likelihood; the base rate "
                    "P(A) never enters a positive-test update.",
                    "ignore_base_rate",
                ),
                c(
                    "d",
                    "Updating a conditional requires only the prior P(A); likelihood "
                    "and normalising evidence are optional labels.",
                    "prior_only_update",
                ),
            ],
            correct="a",
            explanation=(
                "Bayes combines prior, likelihood, and evidence. Equating P(A|B) with "
                "P(B|A) or dropping the base rate reverses or omits required pieces."
            ),
            model_answer=(
                "P(A|B) ∝ P(B|A)P(A); normalise by P(B)."
            ),
            common_mistake=(
                "Equating posterior with likelihood or ignoring the base rate."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Screening: P(D) = 0.01, P(+|D) = 0.95, P(+|not D) = 0.10. "
                "A case tests positive. Which statement is correct?"
            ),
            body="Compute P(D|+) via Bayes; refuse P(D|+) = P(+|D).",
            choices=[
                c(
                    "a",
                    "P(+) = 0.95×0.01 + 0.10×0.99 = 0.1085. P(D|+) = 0.0095/0.1085 ≈ "
                    "0.0876. Equating P(D|+) with P(+|D) = 0.95 ignores the base rate; "
                    "Bayes multiplies prior by likelihood and normalises.",
                ),
                c(
                    "b",
                    "P(D|+) = P(+|D) = 0.95 because the test is accurate when disease "
                    "is present, so the positive predictive value equals the sensitivity.",
                    "posterior_equals_likelihood",
                ),
                c(
                    "c",
                    "P(D|+) = 0.01 because the prior prevalence is the answer once a "
                    "case tests positive.",
                    "prior_only_update",
                ),
                c(
                    "d",
                    "P(D|+) = 0.10 because P(+|not D) = 0.10 dominates the update for "
                    "any positive screen.",
                    "false_positive_rate_as_posterior",
                ),
            ],
            correct="a",
            explanation=(
                "Evidence P(+) = 0.1085 and posterior ≈ 0.0876. Sensitivity 0.95 is "
                "not the posterior. Prior alone or the false-positive rate alone is "
                "wrong."
            ),
            model_answer=(
                "P(+)=0.1085; P(D|+)≈0.0876; refuse posterior equals likelihood."
            ),
            common_mistake=(
                "Taking P(D|+) = 0.95 or ignoring base-rate normalisation."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # Rho Publication Front (9)
    # ------------------------------------------------------------------
    "cr-1.1.1-aims-analysis-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly distinguishes descriptive, "
                "inferential, and predictive analysis aims?"
            ),
            body="Select the three aim types and one separating warrant.",
            choices=[
                c(
                    "a",
                    "Descriptive analysis summarises observed data; inferential analysis "
                    "generalises from sample evidence to population quantities; "
                    "predictive analysis forecasts future outcomes. Inferential targets "
                    "parameters under uncertainty; predictive targets future values.",
                ),
                c(
                    "b",
                    "Descriptive, inferential, and predictive are interchangeable labels "
                    "for any exploratory data analysis; the aim is always EDA.",
                    "eda_as_everything",
                ),
                c(
                    "c",
                    "Inferential analysis always means building a forecasting model for "
                    "next year; descriptive analysis always means hypothesis testing.",
                    "aims_swapped",
                ),
                c(
                    "d",
                    "Predictive analysis summarises last year's data; inferential "
                    "analysis plots histograms only.",
                    "aims_reversed",
                ),
            ],
            correct="a",
            explanation=(
                "Each aim has a distinct target. Collapsing all into EDA or swapping "
                "inferential/predictive roles misclassifies tasks."
            ),
            model_answer=(
                "Descriptive = summarise; inferential = generalise; predictive = forecast."
            ),
            common_mistake=(
                "Treating all aims as EDA, or swapping inferential and predictive."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Motor pricing review tasks: (A) histogram of last year's "
                "claim severities; (B) confidence interval for mean severity; (C) model "
                "forecasting next year's severity. Which statement is correct?"
            ),
            body="Classify each aim; refuse EDA-as-everything.",
            choices=[
                c(
                    "a",
                    "A is descriptive (summarise observed severities); B is inferential "
                    "(generalise to a parameter); C is predictive (forecast future "
                    "severity). Calling all three 'just EDA' collapses distinct aims.",
                ),
                c(
                    "b",
                    "All three are descriptive because each uses historical claim data "
                    "from the motor book.",
                    "eda_as_everything",
                ),
                c(
                    "c",
                    "A is predictive, B is descriptive, and C is inferential because "
                    "forecasting is exploratory and intervals are summaries only.",
                    "aims_swapped",
                ),
                c(
                    "d",
                    "B and C are both inferential; only A is descriptive, because any "
                    "model or interval is automatically inference.",
                    "interval_and_model_same",
                ),
            ],
            correct="a",
            explanation=(
                "Histogram summarises; CI targets a parameter; forecast targets future "
                "severity. Historical data alone does not make every task descriptive."
            ),
            model_answer=(
                "A descriptive; B inferential; C predictive; refuse EDA collapse."
            ),
            common_mistake=(
                "EDA-as-everything or mislabelling forecast/interval tasks."
            ),
        ),
    },
    "cr-1.1.2-stages-tools-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly orders analysis stages and "
                "pairs a stage with a suitable tool class?"
            ),
            body="Select staged analysis path and tool pairing.",
            choices=[
                c(
                    "a",
                    "A sensible path runs from defining the aim through obtaining data, "
                    "cleaning/exploring, analysing (infer or predict), to communicating "
                    "results. Exploratory work sits in clean/explore and pairs with "
                    "summary statistics and exploratory visualisations (or data-wrangling "
                    "scripts).",
                ),
                c(
                    "b",
                    "Analysis stages are finished once a notebook is opened and packages "
                    "loaded; tool choice replaces staged planning.",
                    "tools_without_stages",
                ),
                c(
                    "c",
                    "Communicate results first, then obtain data, then define the aim "
                    "so stakeholders see output early.",
                    "stages_reversed",
                ),
                c(
                    "d",
                    "Clean/explore and final inference are the same stage because any "
                    "plot automatically completes both.",
                    "eda_equals_inference",
                ),
            ],
            correct="a",
            explanation=(
                "Stages structure the workflow; tools serve named stages. Opening "
                "software, reversing order, or collapsing explore with inference "
                "skips staged analysis."
            ),
            model_answer=(
                "Aim → data → clean/explore → analyse → communicate; EDA tools in "
                "explore."
            ),
            common_mistake=(
                "Tool-shopping without stages, reversed order, or EDA equals inference."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You are running a reserves data analysis. Which "
                "statement is correct?"
            ),
            body="Order stages, place EDA, pair a tool; refuse tools-without-stages.",
            choices=[
                c(
                    "a",
                    "Main stages: define aim → obtain data → clean/explore → analyse → "
                    "communicate; exploratory work sits in clean/explore. That stage "
                    "pairs with summary statistics and exploratory visualisations. "
                    "Opening a notebook and loading packages does not finish the staged "
                    "path.",
                ),
                c(
                    "b",
                    "Reserves analysis begins and ends in clean/explore because once "
                    "plots are drawn the inference stage is complete.",
                    "eda_equals_inference",
                ),
                c(
                    "c",
                    "The analysis is complete when R or Python packages load successfully; "
                    "stage order is optional after that.",
                    "tools_without_stages",
                ),
                c(
                    "d",
                    "Communicate findings before defining the aim so reserves output "
                    "reaches stakeholders without delay.",
                    "stages_reversed",
                ),
            ],
            correct="a",
            explanation=(
                "EDA sits inside clean/explore with appropriate tools. Package load or "
                "plots alone do not complete inference or communication stages."
            ),
            model_answer=(
                "Ordered stages with EDA in explore; tools serve stages."
            ),
            common_mistake=(
                "Equating package load or plots with finished staged analysis."
            ),
        ),
    },
    "cr-1.1.3-data-sources-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly contrasts data source types "
                "and one large-set characteristic that affects analysis?"
            ),
            body="Select source characteristics and scale constraint.",
            choices=[
                c(
                    "a",
                    "Sources differ in origin and quality (for example administrative "
                    "records versus voluntary surveys bring different bias and coverage "
                    "risks). Extremely large sets add scale constraints such as storage, "
                    "compute limits, or need for sampling despite volume.",
                ),
                c(
                    "b",
                    "A larger file is automatically better data because volume implies "
                    "representativeness and removes selection concerns.",
                    "bigger_is_better",
                ),
                c(
                    "c",
                    "Source characteristics matter only after modelling is complete; "
                    "during exploration all files may be treated as equally trustworthy.",
                    "trust_after_modelling",
                ),
                c(
                    "d",
                    "Extremely large data sets always remove the need for sampling or "
                    "distributed tooling because every row can always be processed "
                    "locally without constraint.",
                    "scale_no_constraint",
                ),
            ],
            correct="a",
            explanation=(
                "Quality and bias depend on source design, not size alone. Large scale "
                "can add engineering constraints rather than remove them."
            ),
            model_answer=(
                "Source quality varies; large volume does not auto-imply fitness."
            ),
            common_mistake=(
                "Bigger-is-better, deferred trust checks, or ignoring scale limits."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Compare an administrative claims extract with a voluntary "
                "customer survey, both used for the same pricing question. Which "
                "statement is correct?"
            ),
            body="Name trust characteristics and a large-set constraint; refuse bigger-is-better.",
            choices=[
                c(
                    "a",
                    "Examples: selection or response bias (survey versus administrative "
                    "coverage), completeness or granularity of fields, measurement error. "
                    "Large scale may still require sampling or distributed tooling and "
                    "does not fix representativeness by itself. Volume alone is not "
                    "automatically better data.",
                ),
                c(
                    "b",
                    "The administrative extract is always superior because it has more "
                    "rows, so source characteristics need not be compared.",
                    "bigger_is_better",
                ),
                c(
                    "c",
                    "Both sources are equally trustworthy during EDA because trust is "
                    "assessed only after the final model is chosen.",
                    "trust_after_modelling",
                ),
                c(
                    "d",
                    "Extremely large survey files remove bias automatically because "
                    "every respondent row is included in the analysis file.",
                    "volume_fixes_bias",
                ),
            ],
            correct="a",
            explanation=(
                "Bias and coverage differ by source mechanism. Row count does not "
                "replace representativeness or remove scale work."
            ),
            model_answer=(
                "Compare bias/coverage; large n does not imply better data."
            ),
            common_mistake=(
                "Row-count superiority, deferred trust, or volume cures bias."
            ),
        ),
    },
    "cr-1.1.4-reproducible-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines reproducible research "
                "and names required elements?"
            ),
            body="Select reproducibility meaning and element list.",
            choices=[
                c(
                    "a",
                    "Reproducible research lets others (or a future you) reconstruct "
                    "the same analysis results from stated inputs and steps. Required "
                    "elements include versioned or clearly identified data, scripted "
                    "code paths, and documented environment and decisions.",
                ),
                c(
                    "b",
                    "Reproducibility means re-running one notebook cell once on a local "
                    "laptop; shared data, code, and documentation are optional.",
                    "one_off_rerun",
                ),
                c(
                    "c",
                    "An analysis is reproducible if the author remembers the steps; "
                    "formal versioning and scripts are bureaucracy only.",
                    "memory_as_reproducible",
                ),
                c(
                    "d",
                    "Reproducibility applies only to published papers, not to internal "
                    "pricing or reserves work.",
                    "papers_only",
                ),
            ],
            correct="a",
            explanation=(
                "Reconstruction from shared artefacts is the core. One local rerun, "
                "memory, or papers-only scope misstates reproducibility."
            ),
            model_answer=(
                "Others can reconstruct results; data, code, documentation required."
            ),
            common_mistake=(
                "One-off rerun, memory-only, or excluding internal analyses."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. A colleague says their pricing analysis is reproducible "
                "because they can re-run one notebook cell on their laptop. Which "
                "statement is correct?"
            ),
            body="Define reproducibility; name elements; refuse one-off rerun claim.",
            choices=[
                c(
                    "a",
                    "Reproducible research means others can reconstruct the same results "
                    "from stated inputs and steps. Examples of required elements: "
                    "versioned data or clear extract identity, scripted code, documented "
                    "environment/parameters. A one-off local re-run without shared "
                    "artefacts is not reproducibility.",
                ),
                c(
                    "b",
                    "Re-running the last cell proves reproducibility because the output "
                    "appeared twice on the same machine.",
                    "one_off_rerun",
                ),
                c(
                    "c",
                    "Documentation is unnecessary if the colleague wrote detailed comments "
                    "in email about what they did.",
                    "email_as_documentation",
                ),
                c(
                    "d",
                    "Reproducibility is satisfied when the notebook filename includes the "
                    "analysis date; data versioning is optional.",
                    "filename_as_version",
                ),
            ],
            correct="a",
            explanation=(
                "Shared data, code, and environment documentation enable reconstruction. "
                "Duplicate local output, email notes, or dated filenames alone fail."
            ),
            model_answer=(
                "Reconstruct from shared artefacts; refuse one-off rerun."
            ),
            common_mistake=(
                "Equating reproducibility with a single local re-run or weak versioning."
            ),
        ),
    },
    "cr-1.2.1-eda-summaries-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly pairs summary tools and "
                "exploratory visualisations with variable type and analysis aim?"
            ),
            body="Select EDA tool choice aligned to aim.",
            choices=[
                c(
                    "a",
                    "Tool choice depends on variable type and the exploratory question: "
                    "for example counts may use bar charts or histograms to reveal mass "
                    "and tail behaviour; means alone can hide zero-inflation or skew.",
                ),
                c(
                    "b",
                    "EDA always uses the sample mean and a pie chart regardless of "
                    "variable type because any numeric column is continuous.",
                    "mean_and_pie_always",
                ),
                c(
                    "c",
                    "Exploratory visualisation is optional once correlation coefficients "
                    "are computed because numbers replace plots.",
                    "correlation_replaces_eda",
                ),
                c(
                    "d",
                    "Pie charts are the default for any frequency exploration because "
                    "they show part-to-whole structure for every count variable.",
                    "pie_default",
                ),
            ],
            correct="a",
            explanation=(
                "Summaries and plots should match type and question. Mean-only, pie "
                "defaults, or skipping plots for correlations mis-serve EDA."
            ),
            model_answer=(
                "Match summary/plot to type and aim; means can hide shape."
            ),
            common_mistake=(
                "Mean-only tables, pie misuse, or correlation without visual checks."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Claim counts per policy-year: many zeros, a long right "
                "tail of large counts. Aim: explore frequency shape before modelling. "
                "Which statement is correct?"
            ),
            body="Choose visualisation and refuse misuse for zero-inflated counts.",
            choices=[
                c(
                    "a",
                    "Use a bar chart or histogram of counts (or a zero-aware frequency "
                    "plot) to reveal mass at zero and the right tail. Refuse a pie chart "
                    "of policies or a mean-only summary that hides zero-inflation and "
                    "tail behaviour.",
                ),
                c(
                    "b",
                    "Use the sample mean count alone because one number summarises the "
                    "distribution for modelling decisions.",
                    "mean_only",
                ),
                c(
                    "c",
                    "Use a pie chart of policy segments because part-to-whole display "
                    "always shows zero-inflation clearly.",
                    "pie_default",
                ),
                c(
                    "d",
                    "Skip visual exploration and proceed directly to correlation with "
                    "premium because coefficients replace shape diagnostics.",
                    "correlation_replaces_eda",
                ),
            ],
            correct="a",
            explanation=(
                "Zero mass and tail need shape plots. Mean-only, pie charts, or jumping "
                "to correlation without shape checks miss the stated aim."
            ),
            model_answer=(
                "Histogram/bar for zero and tail; refuse mean-only or pie."
            ),
            common_mistake=(
                "Mean-only summary, pie misuse, or correlation without EDA."
            ),
        ),
    },
    "cr-1.2.2-correlation-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly distinguishes Pearson, "
                "Spearman, and Kendall correlation measures?"
            ),
            body="Select measure definitions and one inference caution.",
            choices=[
                c(
                    "a",
                    "Pearson measures linear association; Spearman and Kendall use "
                    "ranks and suit monotone but nonlinear patterns and outlier resistance "
                    "better in many skewed cases. A large coefficient does not prove "
                    "causation.",
                ),
                c(
                    "b",
                    "Pearson, Spearman, and Kendall always give identical values because "
                    "they are three names for the same formula.",
                    "all_same_measure",
                ),
                c(
                    "c",
                    "A significant Pearson correlation proves that changing X causes Y "
                    "to change in the observed direction.",
                    "correlation_is_causation",
                ),
                c(
                    "d",
                    "Kendall is used only for PCA inputs; Pearson is used only after "
                    "PCA scores are constructed.",
                    "pca_confusion",
                ),
            ],
            correct="a",
            explanation=(
                "Measures differ in what association they capture. Identity claims, "
                "causal proof, or PCA confusion are wrong."
            ),
            model_answer=(
                "Pearson linear; Spearman/Kendall rank; correlation ≠ causation."
            ),
            common_mistake=(
                "Treating measures as identical or reading causation from r."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Years licensed vs claim frequency: frequency is skewed "
                "with outliers; scatter looks roughly decreasing but nonlinear. Which "
                "statement is correct?"
            ),
            body="Choose correlation measure and state one limit of a large coefficient.",
            choices=[
                c(
                    "a",
                    "Prefer Spearman (or Kendall) because the relationship looks monotone "
                    "but nonlinear and outliers can distort Pearson. A large coefficient "
                    "still does not prove that changing years licensed causes frequency "
                    "to change.",
                ),
                c(
                    "b",
                    "Use Pearson only because linear correlation is required whenever "
                    "a scatter plot is drawn.",
                    "pearson_only",
                ),
                c(
                    "c",
                    "A strong negative Spearman correlation proves that reducing years "
                    "licensed will reduce claim frequency.",
                    "correlation_is_causation",
                ),
                c(
                    "d",
                    "Use Kendall because it measures variance explained by PC1, which "
                    "is the correct bivariate association measure here.",
                    "pca_confusion",
                ),
            ],
            correct="a",
            explanation=(
                "Rank measures suit monotone nonlinear patterns with outliers. Neither "
                "Pearson-only nor causal claims follow from association alone."
            ),
            model_answer=(
                "Spearman/Kendall preferred; refuse causation from correlation."
            ),
            common_mistake=(
                "Pearson by default, causal inference from r, or PCA confusion."
            ),
        ),
    },
    "cr-1.2.3-pca-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes PCA for "
                "dimensionality reduction?"
            ),
            body="Select PCA purpose and what a component represents.",
            choices=[
                c(
                    "a",
                    "PCA reduces dimensionality by constructing orthogonal components "
                    "that capture major patterns of variation in correlated variables; "
                    "a principal component is a weighted combination summarising shared "
                    "variation, not by itself a proven causal driver.",
                ),
                c(
                    "b",
                    "PCA selects the single causal factor behind all rating variables and "
                    "proves which factor drives claims.",
                    "pc_as_causal",
                ),
                c(
                    "c",
                    "PCA replaces the need for correlation analysis because components "
                    "are always interpretable causal scores.",
                    "pca_replaces_correlation",
                ),
                c(
                    "d",
                    "The first principal component always equals the sample mean vector "
                    "of the original variables.",
                    "pc1_is_mean",
                ),
            ],
            correct="a",
            explanation=(
                "PCA summarises variation for exploration or compression. Causal proof, "
                "correlation replacement, or mean-vector confusion misread components."
            ),
            model_answer=(
                "Components capture variation structure; not automatic causal drivers."
            ),
            common_mistake=(
                "Treating PC1 as causal or equating it with the mean vector."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. A colleague says: 'PC1 from our rating factors is the "
                "true underlying risk score, so we can treat it as a causal driver and "
                "auto-decline on PC1 alone.' Which statement is correct?"
            ),
            body="State exploratory use of PC1; refuse causal auto-decline claim.",
            choices=[
                c(
                    "a",
                    "PC1 may summarise major shared variation among correlated rating "
                    "factors for exploration or visualisation. It does not by itself "
                    "prove a causal risk driver or justify auto-decline without external "
                    "subject-matter and decision warrants.",
                ),
                c(
                    "b",
                    "PC1 is the true latent risk score by construction, so auto-decline "
                    "on PC1 alone is statistically justified.",
                    "pc_as_causal",
                ),
                c(
                    "c",
                    "Because PC1 explains the largest variance, it replaces correlation "
                    "analysis and hypothesis testing for rating factors.",
                    "pca_replaces_correlation",
                ),
                c(
                    "d",
                    "PC1 equals the average of standardised rating factors, so it is "
                    "the same as the portfolio mean premium.",
                    "pc1_is_mean",
                ),
            ],
            correct="a",
            explanation=(
                "Exploratory summarisation differs from causal underwriting policy. "
                "Variance rank or averaging does not create a validated risk driver."
            ),
            model_answer=(
                "PC1 may summarise variation; refuse causal auto-decline."
            ),
            common_mistake=(
                "Treating PC1 as proven causal score or portfolio mean."
            ),
        ),
    },
    "cr-2.1.1-discrete-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly contrasts named discrete "
                "distribution families on a finite or countable support?"
            ),
            body="Select family distinguishing warrants.",
            choices=[
                c(
                    "a",
                    "Named discrete families (geometric, binomial, negative binomial, "
                    "hypergeometric, Poisson, uniform discrete) share discrete support "
                    "but differ in generative stories: for example Poisson counts rare "
                    "events in a fixed interval under a constant rate; binomial counts "
                    "successes in fixed independent trials.",
                ),
                c(
                    "b",
                    "All discrete count data should be modelled as Normal because the "
                    "Normal is the default family for any numeric column.",
                    "normal_for_counts",
                ),
                c(
                    "c",
                    "Hypergeometric and Poisson are interchangeable whenever counts are "
                    "non-negative integers.",
                    "families_interchangeable",
                ),
                c(
                    "d",
                    "Discrete families apply only after continuous models fail; integer "
                    "support alone determines Poisson regardless of generating mechanism.",
                    "integer_implies_poisson",
                ),
            ],
            correct="a",
            explanation=(
                "Family choice follows the data-generating story, not integer typing "
                "alone. Normal-for-counts or interchangeable families are mismatches."
            ),
            model_answer=(
                "Match generative story to family; discrete ≠ interchangeable."
            ),
            common_mistake=(
                "Normal for counts, ignoring without-replacement structure, or integer "
                "implies Poisson."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. For a single policy, model the number of claims in a "
                "fixed year with a constant rare-event rate and independent increments. "
                "Which statement is correct?"
            ),
            body="Place Poisson; refuse habitual mismatch.",
            choices=[
                c(
                    "a",
                    "Poisson fits: counts of rare events in a fixed interval under a "
                    "constant rate / independent-increments story. Refuse Normal for a "
                    "non-negative integer count or hypergeometric when there is no "
                    "without-replacement draw from a finite success/failure population.",
                ),
                c(
                    "b",
                    "Normal(μ, σ²) fits best because the sample mean and variance can "
                    "always be matched for any count variable.",
                    "normal_for_counts",
                ),
                c(
                    "c",
                    "Hypergeometric is required because every insurance count problem "
                    "draws without replacement from a finite population of policies.",
                    "hypergeometric_always",
                ),
                c(
                    "d",
                    "Binomial is mandatory because there is one policy, so n = 1 trial "
                    "always defines a binomial count model for annual claims.",
                    "binomial_n_one",
                ),
            ],
            correct="a",
            explanation=(
                "Poisson matches rare events in fixed time with constant rate. Normal, "
                "automatic hypergeometric, or forced binomial n = 1 are mismatches."
            ),
            model_answer=(
                "Poisson for rare events; refuse Normal/hypergeometric mismatch."
            ),
            common_mistake=(
                "Normal-by-default or wrong discrete family for the story."
            ),
        ),
    },
    "cr-2.1.2-continuous-cs1017.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly contrasts named continuous "
                "distribution families on an interval support?"
            ),
            body="Select continuous family distinguishing warrants.",
            choices=[
                c(
                    "a",
                    "Named continuous families (Normal, lognormal, exponential, gamma, "
                    "chi-square, t, F, beta, uniform continuous) share continuous support "
                    "but differ in shape and scale stories: for example exponential models "
                    "positive memoryless waiting times under constant hazard.",
                ),
                c(
                    "b",
                    "Normal is the default family for any positive quantity because "
                    "symmetric all-real support is always adequate after standardisation.",
                    "normal_by_default",
                ),
                c(
                    "c",
                    "Exponential and Normal are interchangeable for waiting times because "
                    "both have a single numeric parameter.",
                    "families_interchangeable",
                ),
                c(
                    "d",
                    "Continuous families apply only to variables already transformed to "
                    "z-scores; raw positive data must first be declared Normal.",
                    "zscore_first",
                ),
            ],
            correct="a",
            explanation=(
                "Support and generative story guide family choice. Normal-by-default "
                "or interchangeable families ignore positive support and hazard shape."
            ),
            model_answer=(
                "Match support/shape story; exponential for memoryless waiting times."
            ),
            common_mistake=(
                "Normal-by-default or treating distinct continuous families as "
                "interchangeable."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Inter-claim waiting times are strictly positive and, "
                "under a constant hazard story, memoryless. Which statement is correct?"
            ),
            body="Place exponential; refuse Normal-by-default.",
            choices=[
                c(
                    "a",
                    "Exponential fits first: positive support and memoryless waiting "
                    "times under constant hazard. Refuse Normal-by-default because a "
                    "symmetric all-real support model mismatches strictly positive "
                    "waiting times.",
                ),
                c(
                    "b",
                    "Normal(μ, σ²) is appropriate because the central limit theorem "
                    "always makes waiting times Normal regardless of support.",
                    "clt_on_waiting_times",
                ),
                c(
                    "c",
                    "Beta distribution is required because waiting times are bounded "
                    "between zero and one.",
                    "beta_mismatch",
                ),
                c(
                    "d",
                    "Lognormal is ruled out for any waiting-time problem because "
                    "memoryless property implies exponential only when data are discrete.",
                    "lognormal_ruled_out",
                ),
            ],
            correct="a",
            explanation=(
                "Memoryless positive waiting aligns with exponential. Normal CLT "
                "misuse, beta on unbounded times, or false lognormal exclusion are "
                "wrong."
            ),
            model_answer=(
                "Exponential for memoryless waiting; refuse Normal-by-default."
            ),
            common_mistake=(
                "Normal-by-default or misplacing beta/lognormal for the stated story."
            ),
        ),
    },
}

CAMPAIGN_TWINS: dict[str, str] = {
    "cp-2.1.3-prob-quantiles-cs1016.json": (
        "campaign-pi-cs1016/packages/2.1.3-prob-quantiles-cs1016.json"
    ),
    "cp-2.2.1-marginal-conditional-cs1016.json": (
        "campaign-pi-cs1016/packages/2.2.1-marginal-conditional-cs1016.json"
    ),
    "cp-2.5.1-clt-cs1016.json": "campaign-pi-cs1016/packages/2.5.1-clt-cs1016.json",
    "cp-2.6.1-random-samples-cs1016.json": (
        "campaign-pi-cs1016/packages/2.6.1-random-samples-cs1016.json"
    ),
    "cp-4.1.1-linear-regression-cs1016.json": (
        "campaign-pi-cs1016/packages/4.1.1-linear-regression-cs1016.json"
    ),
    "cp-5.1.1-bayes-theorem-cs1016.json": (
        "campaign-pi-cs1016/packages/5.1.1-bayes-theorem-cs1016.json"
    ),
    "cr-1.1.1-aims-analysis-cs1017.json": (
        "campaign-rho-cs1017/packages/1.1.1-aims-analysis-cs1017.json"
    ),
    "cr-1.1.2-stages-tools-cs1017.json": (
        "campaign-rho-cs1017/packages/1.1.2-stages-tools-cs1017.json"
    ),
    "cr-1.1.3-data-sources-cs1017.json": (
        "campaign-rho-cs1017/packages/1.1.3-data-sources-cs1017.json"
    ),
    "cr-1.1.4-reproducible-cs1017.json": (
        "campaign-rho-cs1017/packages/1.1.4-reproducible-cs1017.json"
    ),
    "cr-1.2.1-eda-summaries-cs1017.json": (
        "campaign-rho-cs1017/packages/1.2.1-eda-summaries-cs1017.json"
    ),
    "cr-1.2.2-correlation-cs1017.json": (
        "campaign-rho-cs1017/packages/1.2.2-correlation-cs1017.json"
    ),
    "cr-1.2.3-pca-cs1017.json": "campaign-rho-cs1017/packages/1.2.3-pca-cs1017.json",
    "cr-2.1.1-discrete-cs1017.json": (
        "campaign-rho-cs1017/packages/2.1.1-discrete-cs1017.json"
    ),
    "cr-2.1.2-continuous-cs1017.json": (
        "campaign-rho-cs1017/packages/2.1.2-continuous-cs1017.json"
    ),
}

STEM_TO_INVENTORY: dict[str, str] = {
    "2.1.3-prob-quantiles-cs1016": "cp-2.1.3-prob-quantiles-cs1016.json",
    "2.2.1-marginal-conditional-cs1016": "cp-2.2.1-marginal-conditional-cs1016.json",
    "2.5.1-clt-cs1016": "cp-2.5.1-clt-cs1016.json",
    "2.6.1-random-samples-cs1016": "cp-2.6.1-random-samples-cs1016.json",
    "4.1.1-linear-regression-cs1016": "cp-4.1.1-linear-regression-cs1016.json",
    "5.1.1-bayes-theorem-cs1016": "cp-5.1.1-bayes-theorem-cs1016.json",
    "1.1.1-aims-analysis-cs1017": "cr-1.1.1-aims-analysis-cs1017.json",
    "1.1.2-stages-tools-cs1017": "cr-1.1.2-stages-tools-cs1017.json",
    "1.1.3-data-sources-cs1017": "cr-1.1.3-data-sources-cs1017.json",
    "1.1.4-reproducible-cs1017": "cr-1.1.4-reproducible-cs1017.json",
    "1.2.1-eda-summaries-cs1017": "cr-1.2.1-eda-summaries-cs1017.json",
    "1.2.2-correlation-cs1017": "cr-1.2.2-correlation-cs1017.json",
    "1.2.3-pca-cs1017": "cr-1.2.3-pca-cs1017.json",
    "2.1.1-discrete-cs1017": "cr-2.1.1-discrete-cs1017.json",
    "2.1.2-continuous-cs1017": "cr-2.1.2-continuous-cs1017.json",
}


INVENTORY_TO_STEM: dict[str, str] = {v: k for k, v in STEM_TO_INVENTORY.items()}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace AR/CP knowledge_checks with Batch 3 MCQ content when stem is in scope."""
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


def sync_catalogue_twins(root: Path | None = None) -> int:
    """Patch live educational_packages twins with Batch 3 MCQ knowledge_checks."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key in CONVERSIONS:
        cat_path = catalogue_dir / inv_key
        if not cat_path.exists():
            continue
        pkg = json.loads(cat_path.read_text(encoding="utf-8"))
        stem = INVENTORY_TO_STEM[inv_key]
        patched = apply_mcq_overlay(pkg, stem)
        cat_path.write_text(
            json.dumps(patched, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        updated += 1
    return updated


if __name__ == "__main__":
    count = sync_catalogue_twins()
    print(f"Synced {count} catalogue twins with Batch 3 MCQ knowledge_checks.")

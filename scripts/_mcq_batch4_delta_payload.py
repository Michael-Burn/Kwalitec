#!/usr/bin/env python3
"""Batch 4 MCQ conversion payload for Campaign Delta CS1-003 (Batch D file set).

Applies deterministic MCQ rewrites to Active Recall + Checkpoint items for
18 Delta learning packages (-cs1003 suffix). Excludes 4.2.3, 4.2.5, 5.1.1,
and 5.1.5 (STRONG / untouched in original content-quality audit; Batch 6).

Content is adapted from Batch 2 Continuity Front conversions with cs1003-specific
stem alignment where prompts differ materially.
"""
from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

from _mcq_batch2_continuity_front_payload import CONVERSIONS as B2
from _mcq_batch2_continuity_front_payload import _item, c

# Batch 2 inventory key -> Batch 4 (cs1003) inventory key
B2_TO_CS1003: dict[str, str] = {
    "4.1.1-response-explanatory-cs1013.json": "4.1.1-response-explanatory-cs1003.json",
    "4.1.2-simple-multiple-cs1013.json": "4.1.2-simple-multiple-cs1003.json",
    "4.1.3-least-squares-cs1013.json": "4.1.3-least-squares-cs1003.json",
    "4.1.4-software-fit-cs1013.json": "4.1.4-software-inference-cs1003.json",
    "4.1.5-variable-selection-cs1013.json": "4.1.5-variable-selection-cs1003.json",
    "4.2.1-exponential-family-cs1014.json": "4.2.1-exponential-family-cs1003.json",
    "4.2.2-mean-variance-cs1014.json": "4.2.2-mean-variance-cs1003.json",
    "4.2.4-factors-interactions-cs1014.json": "4.2.4-factors-interactions-cs1003.json",
    "4.2.6-deviance-estimation-cs1014.json": "4.2.6-deviance-estimation-cs1003.json",
    "4.2.7-model-choice-cs1014.json": "4.2.7-model-choice-cs1003.json",
    "4.2.8-residuals-cs1014.json": "4.2.8-residuals-cs1003.json",
    "4.2.9-goodness-tests-cs1014.json": "4.2.9-goodness-tests-cs1003.json",
    "5.1.2-prior-posterior-cs1015.json": "5.1.2-prior-posterior-cs1003.json",
    "5.1.3-posterior-simple-cs1015.json": "5.1.3-posterior-simple-cs1003.json",
    "5.1.4-loss-estimators-cs1015.json": "5.1.4-loss-estimators-cs1003.json",
    "5.1.6-credibility-premium-cs1015.json": "5.1.6-credibility-premium-cs1003.json",
    "5.1.7-bayesian-credibility-cs1015.json": "5.1.7-bayesian-credibility-cs1003.json",
    "5.1.8-empirical-bayes-cs1015.json": "5.1.8-empirical-bayes-cs1003.json",
}

CONVERSIONS: dict[str, dict[str, dict[str, Any]]] = {
    cs1003_key: copy.deepcopy(B2[b2_key]) for b2_key, cs1003_key in B2_TO_CS1003.items()
}

# cs1003-specific overrides (stem alignment + refusal targets from Delta prompts)
CONVERSIONS["4.1.1-response-explanatory-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. For a portfolio with claim frequency as Y and age and "
        "territory as X, which statement correctly assigns response and "
        "explanatory roles with a one-sentence justification?"
    ),
    body="Select Y, X, and actuarial warrant for a frequency model.",
    choices=[
        c(
            "a",
            "Response Y = claim frequency (the outcome to model). Explanatory "
            "variables X = age and territory (rating factors thought to explain "
            "or predict frequency). Justification: we model frequency as the "
            "outcome explained by rating factors.",
        ),
        c(
            "b",
            "Response Y = age; explanatory variables are claim frequency and "
            "territory because every column in the portfolio table is a predictor.",
            "column_soup",
        ),
        c(
            "c",
            "Age and territory are both response variables; frequency is an "
            "explanatory variable because it is numeric.",
            "roles_reversed",
        ),
        c(
            "d",
            "Response and explanatory roles cannot be named until a multiple "
            "regression equation is written; the portfolio sketch is insufficient.",
            "model_form_first",
        ),
    ],
    correct="a",
    explanation=(
        "For frequency modelling, claim frequency is Y and rating factors such "
        "as age and territory are X. Column-soup or reversed roles ignore the "
        "modelling question."
    ),
    model_answer=(
        "Response = claim frequency (Y). Explanatory = age, territory (X). "
        "Justification: model frequency as outcome explained by rating factors."
    ),
    common_mistake=(
        "Column-soup modelling or treating every numeric field as an explanatory "
        "variable without naming Y first."
    ),
)

CONVERSIONS["4.1.2-simple-multiple-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. Which statement correctly writes a simple linear model "
        "for Y on X1 and a multiple linear model for Y on X1 and X2 using "
        "β notation?"
    ),
    body="Select the simple versus multiple LM equations.",
    choices=[
        c(
            "a",
            "Simple: Y = β0 + β1 X1 + ε. Multiple: Y = β0 + β1 X1 + β2 X2 + ε "
            "(or equivalent β notation).",
        ),
        c(
            "b",
            "Simple: Y = β0 + β1 X1 + β2 X2 + ε. Multiple: Y = β0 + β1 X1 + ε, "
            "because multiple means more parameters in the least-squares criterion.",
            "forms_swapped",
        ),
        c(
            "c",
            "Both forms are Y = β̂0 + β̂1 x + ε where β̂ comes from minimising "
            "sum of squared residuals; stating the model is the same as "
            "OLS estimation.",
            "least_squares_finishes",
        ),
        c(
            "d",
            "Simple and multiple models differ only in software menu choice; "
            "the equation Y = β0 + β1 X1 + ε covers both one and two predictors.",
            "software_only",
        ),
    ],
    correct="a",
    explanation=(
        "Simple uses one X; multiple adds a second X term. OLS estimation is a "
        "separate step from stating the model forms."
    ),
    model_answer=(
        "Simple: Y = β0 + β1 X1 + ε. Multiple: Y = β0 + β1 X1 + β2 X2 + ε."
    ),
    common_mistake=(
        "Swapping simple and multiple forms or treating OLS as finishing model-form "
        "statement."
    ),
)

CONVERSIONS["4.1.3-least-squares-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. Which statement correctly states what least squares "
        "minimises and what the slope estimate means for Y versus X?"
    ),
    body="Select the OLS criterion and slope interpretation.",
    choices=[
        c(
            "a",
            "Least squares minimises the sum of squared residuals. The slope "
            "estimate is the change in mean Y per unit change in X in the "
            "simple linear model frame.",
        ),
        c(
            "b",
            "Least squares minimises the sum of absolute residuals; the slope "
            "equals the sample correlation Corr(X, Y) by definition.",
            "lad_as_ols",
        ),
        c(
            "c",
            "Least squares means clicking Fit in software; no closed-form "
            "criterion need be stated once β̂ is printed.",
            "fit_as_criterion",
        ),
        c(
            "d",
            "The slope estimate is the ratio of standard deviations SD(Y)/SD(X) "
            "with no intercept adjustment; least squares minimises R-squared.",
            "corr_as_slope",
        ),
    ],
    correct="a",
    explanation=(
        "OLS minimises sum of squared residuals. Slope is change in mean Y per "
        "unit X. Correlation and LAD are different objects."
    ),
    model_answer=(
        "Minimises sum of squared residuals. Slope: change in mean Y per unit X."
    ),
    common_mistake=(
        "Equating OLS with software Fit or confusing slope with correlation."
    ),
)

_cp_414 = copy.deepcopy(CONVERSIONS["4.1.4-software-inference-cs1003.json"]["cp"])
for ch in _cp_414["choices"]:
    if ch["id"] == "a":
        ch["label"] = (
            "A mean-response interval covers E[Y | x*]; a prediction interval "
            "covers a new observation and is typically wider (adds residual "
            "variance). Fit alone is not enough: slope inference, goodness-of-fit, "
            "prediction limits, and residual checks are all required before "
            "trusting the fit."
        )
    if ch["id"] == "b":
        ch["label"] = (
            "I fitted the model so I am done; residual plots are optional after "
            "a significant slope."
        )
        ch["misconception_tag"] = "fit_finishes_inference"
_cp_414["model_answer"] = (
    "Mean interval for E[Y | x*]; prediction wider; refuse fit-only "
    "and optional residuals."
)
_cp_414["common_mistake"] = (
    "Accepting fit as finishing inference, or treating residuals as "
    "optional after significance."
)
_cp_414["explanation"] = (
    "Mean interval targets the conditional mean; prediction adds observation noise. "
    "Fit-only and optional residuals are misconceptions."
)
CONVERSIONS["4.1.4-software-inference-cs1003.json"]["cp"] = _cp_414

CONVERSIONS["4.1.4-software-inference-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. Which statement correctly lists in order the post-fit "
        "moves after fitting a linear model in software?"
    ),
    body="Select fit, slope inference, prediction limits, residual check.",
    choices=[
        c(
            "a",
            "Fit the model in software, then check slope inference (estimate, "
            "standard error, test or confidence interval), then use prediction "
            "with confidence or prediction limits, then inspect residuals to "
            "check suitability and validity of the linear model.",
        ),
        c(
            "b",
            "Fit the model, then run variable selection, then declare the model "
            "valid without residual checks because R-squared is displayed.",
            "selection_finishes",
        ),
        c(
            "c",
            "Fit the model and read the slope sign only; prediction limits and "
            "residual checks belong to GLM diagnostics, not linear regression.",
            "glm_only_diagnostics",
        ),
        c(
            "d",
            "Inspect residuals first, then fit the model, then skip slope "
            "inference because significance is automatic from the fit command.",
            "residuals_before_fit",
        ),
    ],
    correct="a",
    explanation=(
        "The chain is fit, slope inference, prediction with limits, residual "
        "checks. Skipping inference or residuals after fit is menu tourism."
    ),
    model_answer=(
        "Fit, slope inference, prediction with limits, residual checks for "
        "suitability."
    ),
    common_mistake=(
        "Stopping at fitted coefficients without prediction limits or residual "
        "checks."
    ),
)

CONVERSIONS["4.2.4-factors-interactions-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. Which statement gives one continuous explanatory example, "
        "one categorical factor example, and states what an interaction term "
        "allows?"
    ),
    body="Select continuous, factor, and interaction warrant.",
    choices=[
        c(
            "a",
            "Continuous example: policyholder age. Categorical factor example: "
            "region with levels North/South. An interaction term allows the "
            "effect of one variable (for example age) to depend on the level of "
            "another (for example region), beyond main effects alone.",
        ),
        c(
            "b",
            "Continuous example: region North/South. Categorical factor example: "
            "age in years. An interaction is always unnecessary because main "
            "effects fully encode categories.",
            "roles_swapped",
        ),
        c(
            "c",
            "Continuous and factor variables are the same object in GLMs; an "
            "interaction term is just another main-effect slope on a continuous "
            "covariate.",
            "interaction_as_main",
        ),
        c(
            "d",
            "Factors apply only outside GLMs; GLM linear predictors use only "
            "continuous covariates with no level coding.",
            "factors_not_glm",
        ),
    ],
    correct="a",
    explanation=(
        "Age is continuous; region is a factor with levels. Interaction allows "
        "joint level-dependent effects beyond additive mains."
    ),
    model_answer=(
        "Continuous: age. Factor: region. Interaction: effect depends on level "
        "beyond mains."
    ),
    common_mistake=(
        "Treating interaction as another main effect or omitting factor level coding."
    ),
)

CONVERSIONS["4.2.7-model-choice-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. For nested models A subset B, which statement correctly "
        "describes what analysis of deviance compares and what a large "
        "improvement suggests?"
    ),
    body="Select nested deviance comparison statement.",
    choices=[
        c(
            "a",
            "Compare deviance of A versus B (deviance difference or related "
            "likelihood-ratio test). A large improvement supports the richer "
            "model B if added parameters are statistically and scientifically "
            "warranted.",
        ),
        c(
            "b",
            "Plot Pearson residuals to finish analysis of deviance; a large "
            "residual implies the full model wins automatically.",
            "residuals_finishes_model_choice",
        ),
        c(
            "c",
            "Analysis of deviance compares raw R-squared on the link scale only; "
            "deviance differences apply exclusively to Normal identity GLMs.",
            "r2_non_nested",
        ),
        c(
            "d",
            "If every p-value in B is below 0.05, deviance comparison is "
            "unnecessary because significance alone selects the model.",
            "p_only_choice",
        ),
    ],
    correct="a",
    explanation=(
        "Nested comparison uses deviance difference. Residual plots are "
        "diagnostics, not a substitute for analysis of deviance."
    ),
    model_answer=(
        "Compare deviance A vs B; large improvement supports richer model if "
        "parameters warranted."
    ),
    common_mistake=(
        "Treating residual plots as finishing analysis of deviance."
    ),
)

CONVERSIONS["5.1.2-prior-posterior-cs1003.json"]["cp"] = _item(
    prompt=(
        "Closed-book. Which statement correctly defines prior, posterior, and "
        "conjugate prior and names one actuarial conjugate pair?"
    ),
    body="Define terms; refuse prior-as-sample and conjugate-as-finished.",
    choices=[
        c(
            "a",
            "Prior: belief about θ before data. Posterior: updated belief after "
            "data. Conjugate: prior family closed under updating so posterior "
            "stays in the same family. Example: Beta-Binomial or Gamma-Poisson. "
            "The prior is not the last sample; conjugate language structures the "
            "update but you still obtain the posterior from prior plus data.",
        ),
        c(
            "b",
            "The prior is just the last observed sample; conjugate updating "
            "copies that sample into the posterior without a separate prior object.",
            "prior_is_sample",
        ),
        c(
            "c",
            "Naming Beta-Binomial finishes obtaining the numerical posterior "
            "for a parameter; no prior-plus-data calculation is required.",
            "conjugate_finishes_posterior",
        ),
        c(
            "d",
            "Prior and posterior are identical once data arrive; conjugate means "
            "the prior equals the maximum likelihood estimate.",
            "prior_equals_posterior",
        ),
    ],
    correct="a",
    explanation=(
        "Prior and posterior are distinct stages. Conjugate naming does not "
        "replace calculating posterior parameters from data."
    ),
    model_answer=(
        "Prior, posterior, conjugate definitions; Beta-Binomial example. "
        "Refuse prior-as-sample and naming-as-calculating."
    ),
    common_mistake=(
        "Treating the prior as the sample or conjugate naming as finishing "
        "posterior numerics."
    ),
)

CONVERSIONS["5.1.3-posterior-simple-cs1003.json"]["cp"] = _item(
    prompt=(
        "Closed-book. Binomial n=10 with x=3 successes and Beta(2,2) prior. "
        "Which statement is correct?"
    ),
    body="State posterior parameters; refuse slogan-Bayes and loss-as-automatic.",
    choices=[
        c(
            "a",
            "Posterior Beta(2+3, 2+7) = Beta(5,9). Bayesian work requires an "
            "actual posterior distribution, not a slogan. The posterior is the "
            "full distribution; a loss-based point estimator under squared-error "
            "loss is a further step.",
        ),
        c(
            "b",
            "Bayesian means I believe in Bayes; no posterior distribution is "
            "required once the prior is named Beta(2,2).",
            "slogan_bayes",
        ),
        c(
            "c",
            "Posterior Beta(2,2) because the prior dominates with n=10 small; "
            "successes add nothing to the parameters.",
            "prior_unchanged",
        ),
        c(
            "d",
            "Having Beta(5,9) finishes choosing the Bayesian point estimator "
            "under squared-error loss without further calculation.",
            "posterior_finishes_loss_estimator",
        ),
    ],
    correct="a",
    explanation=(
        "Conjugate update gives Beta(5,9). Slogan-Bayes and automatic loss "
        "estimators are refusals from the checkpoint stem."
    ),
    model_answer=(
        "Posterior Beta(5,9). Refuse slogan-Bayes; loss estimator is a further step."
    ),
    common_mistake=(
        "Slogan-Bayes without a posterior or treating posterior as automatic "
        "point estimator."
    ),
)

CONVERSIONS["5.1.4-loss-estimators-cs1003.json"]["cp"] = _item(
    prompt=(
        "Closed-book. Posterior for θ is available. Which statement is correct?"
    ),
    body="Name estimators under losses; refuse mode-default and interval collapse.",
    choices=[
        c(
            "a",
            "Under squared-error loss, use the posterior mean as the Bayesian "
            "point estimator; under absolute-error loss, use the posterior median. "
            "Just taking the posterior mode always is not warranted without an "
            "explicit loss. A point estimator summarises the posterior under a "
            "loss; a credible interval is a posterior probability set for θ. "
            "Different objects.",
        ),
        c(
            "b",
            "Just take the posterior mode always; mean and median are frequentist "
            "labels unrelated to loss.",
            "mode_always",
        ),
        c(
            "c",
            "The Bayesian point estimator under loss is the same object as a "
            "credible interval.",
            "point_estimator_is_interval",
        ),
        c(
            "d",
            "Under squared-error loss, use the posterior median; under absolute-"
            "error loss, use the posterior mean.",
            "losses_swapped",
        ),
    ],
    correct="a",
    explanation=(
        "Mean under squared error, median under absolute error. Mode without "
        "loss and interval collapse are checkpoint refusals."
    ),
    model_answer=(
        "Squared-error: mean; absolute-error: median. Refuse mode-default and "
        "interval collapse."
    ),
    common_mistake=(
        "Defaulting to the mode without a loss or conflating point estimator "
        "with credible interval."
    ),
)

CONVERSIONS["5.1.7-bayesian-credibility-cs1003.json"]["ar"] = _item(
    prompt=(
        "Closed-book. Which statement correctly outlines how a Bayesian "
        "credibility approach uses prior and data to produce a credibility "
        "premium in a simple case?"
    ),
    body="Select prior-to-posterior-to-premium chain.",
    choices=[
        c(
            "a",
            "Specify a prior or structural distribution for risk parameters; "
            "update with data to a posterior; in a simple case the credibility "
            "premium takes the form Z times X̄ + (1 minus Z) times μ with Z and "
            "μ determined from the prior structure.",
        ),
        c(
            "b",
            "Write Z times X̄ + (1 minus Z) times μ with no Bayesian story; "
            "the blend formula alone defines Bayesian credibility.",
            "empty_formula",
        ),
        c(
            "c",
            "Applying Bayesian credibility finishes the Empirical Bayes approach "
            "because both yield a numeric premium.",
            "bayesian_finishes_eb",
        ),
        c(
            "d",
            "Bayesian credibility uses only the sample mean X̄ with Z = 1 always; "
            "the prior enters only in Empirical Bayes.",
            "full_credibility_always",
        ),
    ],
    correct="a",
    explanation=(
        "Bayesian credibility requires prior-to-posterior structure that "
        "justifies μ and Z. Empty formula or EB conflation are wrong."
    ),
    model_answer=(
        "Prior, update to posterior, credibility premium Z X̄ + (1-Z) μ from "
        "structure."
    ),
    common_mistake=(
        "Writing the blend formula without a Bayesian warrant or collapsing into "
        "Empirical Bayes."
    ),
)

CONVERSIONS["5.1.8-empirical-bayes-cs1003.json"]["cp"] = _item(
    prompt=(
        "Closed-book. Which statement correctly outlines the Empirical Bayes "
        "move to obtain a credibility premium when structural parameters are "
        "unknown?"
    ),
    body="Outline EB premium; refuse EB-as-Bayesian identity.",
    choices=[
        c(
            "a",
            "Estimate structural parameters (for example overall mean and "
            "process or variance components) from collective data, plug them "
            "into the credibility formula to get Ẑ and μ̂, then form "
            "Ẑ times X̄ + (1 minus Ẑ) times μ̂ for the risk. Empirical Bayes "
            "is not just another name for fully Bayesian credibility; assumptions "
            "about structural parameters differ.",
        ),
        c(
            "b",
            "Empirical Bayes is just another name for Bayesian credibility; "
            "both treat the prior as fully specified before any data.",
            "eb_is_bayesian",
        ),
        c(
            "c",
            "Computing one EB premium finishes explaining how Bayesian and "
            "Empirical Bayes differ in assumptions.",
            "eb_premium_finishes_contrast",
        ),
        c(
            "d",
            "Empirical Bayes requires a fully specified prior before any data; "
            "collective estimation is unnecessary.",
            "prior_required_first",
        ),
    ],
    correct="a",
    explanation=(
        "EB estimates structural parameters from collective experience. It is "
        "not identical to full Bayes with a given prior."
    ),
    model_answer=(
        "Estimate structurals from collective data; plug into credibility form. "
        "EB differs from full Bayes in assumptions."
    ),
    common_mistake=(
        "Equating EB with full Bayes or stopping at one premium without noting "
        "assumption difference."
    ),
)

# Campaign package stem (filename without .json) -> inventory conversion key
STEM_TO_INVENTORY: dict[str, str] = {
    inv_key.replace(".json", ""): inv_key for inv_key in CONVERSIONS
}

INVENTORY_TO_STEM: dict[str, str] = {v: k for k, v in STEM_TO_INVENTORY.items()}

CAMPAIGN_TWINS: dict[str, str] = {
    inv_key: f"campaign-delta-cs1003/packages/{inv_key.replace('.json', '')}.json"
    for inv_key in CONVERSIONS
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace AR/CP knowledge_checks with Batch 4 MCQ content when stem is in scope."""
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
    """Patch live educational_packages twins with Batch 4 MCQ knowledge_checks."""
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


def sync_campaign_twins(root: Path | None = None) -> int:
    """Patch campaign-delta-cs1003 package twins with Batch 4 MCQ knowledge_checks."""
    repo = root or Path(__file__).resolve().parents[1]
    campaigns_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        camp_path = campaigns_dir / rel_path
        if not camp_path.exists():
            continue
        pkg = json.loads(camp_path.read_text(encoding="utf-8"))
        stem = INVENTORY_TO_STEM[inv_key]
        patched = apply_mcq_overlay(pkg, stem)
        camp_path.write_text(
            json.dumps(patched, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        updated += 1
    return updated


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    """Scan touched files for duplicate words, em dashes, and meta language."""
    import re

    repo = root or Path(__file__).resolve().parents[1]
    defects: list[str] = []
    dup_word = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
    meta_patterns = [
        re.compile(p, re.IGNORECASE)
        for p in [
            r"\bcampaign\b",
            r"\bjourney\b",
            r"Batch \d",
            r"Wave \d",
            r"Isolated Golden Day",
        ]
    ]
    paths: list[Path] = []
    cat = repo / "app/curriculum/data/educational_packages/cs1"
    for inv_key in CONVERSIONS:
        paths.append(cat / inv_key)
        camp_root = repo / "app/curriculum/data/educational_campaigns/cs1"
        paths.append(camp_root / CAMPAIGN_TWINS[inv_key])

    for path in paths:
        if not path.exists():
            defects.append(f"MISSING: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        pkg = json.loads(text)
        for kc in pkg.get("knowledge_checks", []):
            if kc.get("response_type") != "mcq":
                defects.append(f"{path.name} {kc.get('kind')}: not mcq")
                continue
            blob = json.dumps(kc, ensure_ascii=False)
            if "\u2014" in blob or "—" in blob:
                defects.append(f"{path.name} {kc.get('kind')}: em dash found")
            for m in dup_word.finditer(blob):
                word = m.group(1).lower()
                skip = {"that", "the", "a", "an", "or", "and", "to", "in", "is"}
                if word not in skip:
                    defects.append(
                        f"{path.name} {kc.get('kind')}: duplicate word '{m.group(1)}'"
                    )
            for mp in meta_patterns:
                if mp.search(blob):
                    defects.append(
                        f"{path.name} {kc.get('kind')}: meta language '{mp.pattern}'"
                    )
            if len(kc.get("choices", [])) != 4:
                defects.append(f"{path.name} {kc.get('kind')}: not 4 choices")
            if kc.get("correct_choice_id") not in {"a", "b", "c", "d"}:
                defects.append(f"{path.name} {kc.get('kind')}: bad correct_choice_id")
    return defects


if __name__ == "__main__":
    cat = sync_catalogue_twins()
    camp = sync_campaign_twins()
    defects = mechanical_defect_scan()
    print(f"Synced {cat} catalogue + {camp} campaign twins.")
    if defects:
        print("DEFECTS:")
        for d in defects:
            print(" ", d)
    else:
        print("Mechanical defect scan: PASS (0 issues)")

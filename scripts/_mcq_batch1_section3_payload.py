#!/usr/bin/env python3
"""Batch 1 MCQ conversion payload for Section 3 (checkpoint Batch A file set).

Applies deterministic MCQ rewrites to Active Recall + Checkpoint items for:
  - Campaign Kappa CS1-010 (3.1.1–3.1.6)
  - Campaign Lambda CS1-011 (3.2.1–3.2.8)
  - Campaign Mu CS1-012 (3.3.1–3.3.5)
  - Campaign Pi CS1-016 Section 3 Memory Front (3.1.1, 3.2.1, 3.3.1)

Does not touch revision packages, Rho, or other campaigns.
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
    # 3.1.1 Method of moments
    # ------------------------------------------------------------------
    "3.1.1-method-of-moments-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the method-of-moments "
                "construction of an estimator?"
            ),
            body="Select the statement that names the MoM move and what is equated.",
            choices=[
                c(
                    "a",
                    "Equate sample moments to the corresponding population moments "
                    "(written as functions of the unknown parameter) and solve for "
                    "the parameter.",
                ),
                c(
                    "b",
                    "Any closed-form formula for an estimator θ̂ is automatically a "
                    "method-of-moments estimator.",
                    "any_formula_is_mom",
                ),
                c(
                    "c",
                    "Maximise the likelihood (or log-likelihood) with respect to the "
                    "parameter; the maximising value is the method-of-moments estimator.",
                    "mle_as_mom",
                ),
                c(
                    "d",
                    "Construct an interval for the parameter from the sample; the "
                    "interval midpoint is the method-of-moments estimator.",
                    "interval_as_mom",
                ),
            ],
            correct="a",
            explanation=(
                "Method of moments equates sample moments to population moments and "
                "solves for the parameter(s). Maximising a likelihood is MLE, not MoM. "
                "Having some estimator formula, or building an interval, does not by "
                "itself make the construction method of moments."
            ),
            model_answer=(
                "Equate sample moments to the corresponding population moments "
                "(as functions of parameters) and solve for the parameter(s)."
            ),
            common_mistake=(
                "Treating any estimator formula, an MLE, or an interval midpoint as "
                "automatically method of moments."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Claim sizes are modelled as Exponential with mean θ. A "
                "sample has mean x̄ = 4. Which statement is correct?"
            ),
            body="Apply MoM to the Exponential mean and refuse MLE-as-MoM.",
            choices=[
                c(
                    "a",
                    "The population first-moment equation is E[X] = θ. Equating the "
                    "sample mean gives θ̂_MoM = x̄ = 4. Maximising the likelihood is "
                    "a different construction (MLE), not method of moments.",
                ),
                c(
                    "b",
                    "The population first-moment equation is E[X] = 1/θ. Equating the "
                    "sample mean gives θ̂_MoM = 1/4.",
                    "rate_mean_swap",
                ),
                c(
                    "c",
                    "Because maximising the Exponential likelihood yields θ̂ = x̄, that "
                    "procedure is already the method-of-moments construction.",
                    "mle_as_mom",
                ),
                c(
                    "d",
                    "Method of moments for this model sets Var(X) = x̄ and solves, so "
                    "θ̂_MoM = 4 because Var(X) = θ for the Exponential mean-θ "
                    "parametrisation.",
                    "wrong_moment",
                ),
            ],
            correct="a",
            explanation=(
                "For Exponential with mean θ, E[X] = θ, so MoM equates x̄ = θ and gives "
                "θ̂_MoM = 4. Coincidence that the MLE equals x̄ does not make likelihood "
                "maximisation into MoM. Using the wrong population moment (or treating "
                "variance as equal to the sample mean by fiat) is incorrect."
            ),
            model_answer=(
                "E[X] = θ; equate x̄ = θ, so θ̂_MoM = 4. Likelihood maximisation is MLE, "
                "not MoM."
            ),
            common_mistake=(
                "Swapping mean/rate parametrisation, treating MLE coincidence as MoM, "
                "or matching the wrong moment."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.1.2 Maximum likelihood
    # ------------------------------------------------------------------
    "3.1.2-maximum-likelihood-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes maximum-likelihood "
                "estimation and how it differs from method of moments?"
            ),
            body="Select the statement that names the MLE move and contrasts it with MoM.",
            choices=[
                c(
                    "a",
                    "Choose the parameter value that maximises the likelihood "
                    "(equivalently the log-likelihood under regularity). Method of "
                    "moments instead equates sample moments to population moments.",
                ),
                c(
                    "b",
                    "Maximum likelihood always equates the first sample moment to the "
                    "first population moment; that is what 'likelihood' means here.",
                    "mom_as_mle",
                ),
                c(
                    "c",
                    "Once a method-of-moments estimator exists, the maximum-likelihood "
                    "estimator is the same object by definition.",
                    "mom_finishes_mle",
                ),
                c(
                    "d",
                    "Maximum likelihood means choosing the parameter that minimises "
                    "mean square error among all unbiased estimators.",
                    "mse_as_mle",
                ),
            ],
            correct="a",
            explanation=(
                "MLE maximises the model likelihood (or log-likelihood). MoM matches "
                "moments. The two constructions are different even when numerical "
                "answers sometimes coincide. MSE comparison is a property criterion, "
                "not the MLE definition."
            ),
            model_answer=(
                "Maximise the likelihood (or log-likelihood); MoM matches moments "
                "instead."
            ),
            common_mistake=(
                "Collapsing MoM into MLE, or defining MLE as an MSE-optimality rule."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. IID claims X₁,…,Xₙ ~ Exponential with rate λ "
                "(pdf λ e^{−λx} for x>0). Which statement is correct?"
            ),
            body="Form the MLE for the Exponential rate and refuse MoM-as-MLE.",
            choices=[
                c(
                    "a",
                    "The log-likelihood is ℓ(λ) = n ln λ − λ Σ xᵢ, and the MLE is "
                    "λ̂ = n/Σ xᵢ = 1/x̄. Matching moments is a different construction "
                    "from maximising the likelihood, even if numbers sometimes agree.",
                ),
                c(
                    "b",
                    "The log-likelihood is ℓ(λ) = n ln λ − λ Σ xᵢ, and the MLE is "
                    "λ̂ = x̄ because the sample mean is always the MLE for a rate.",
                    "mle_equals_mean_rate",
                ),
                c(
                    "c",
                    "Because the method-of-moments estimator for this model equals 1/x̄, "
                    "that moment-matching procedure is already maximum likelihood.",
                    "mom_as_mle",
                ),
                c(
                    "d",
                    "The MLE maximises Σ xᵢ − n/λ, so λ̂ = n/Σ xᵢ comes from "
                    "minimising the sum of observations.",
                    "wrong_likelihood",
                ),
            ],
            correct="a",
            explanation=(
                "For Exponential rate λ, ℓ(λ) = n ln λ − λ Σ xᵢ and λ̂ = 1/x̄. MoM can "
                "give the same number here, but MoM is still moment matching, not "
                "likelihood maximisation. The MLE is 1/x̄, not x̄, for the rate "
                "parametrisation."
            ),
            model_answer=(
                "ℓ(λ) = n ln λ − λ Σ xᵢ; λ̂ = 1/x̄. MoM ≠ MLE as constructions."
            ),
            common_mistake=(
                "Taking λ̂ = x̄ for the rate, or treating MoM coincidence as MLE."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.1.3 Efficiency, bias, consistency, MSE
    # ------------------------------------------------------------------
    "3.1.3-efficiency-bias-consistency-mse-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly relates bias, MSE, efficiency, "
                "and consistency for an estimator?"
            ),
            body="Select the statement that gets the property definitions right.",
            choices=[
                c(
                    "a",
                    "Bias is E[θ̂] − θ. Under the usual decomposition, "
                    "MSE = Var(θ̂) + (bias)². Efficiency compares variance or MSE to a "
                    "benchmark; consistency concerns convergence in probability to the "
                    "true value as sample size grows.",
                ),
                c(
                    "b",
                    "Bias is Var(θ̂). MSE equals the absolute bias, and consistency means "
                    "the estimator is unbiased for every finite n.",
                    "bias_var_swap_consistency",
                ),
                c(
                    "c",
                    "MSE = Var(θ̂) − (bias)², so a larger bias always reduces MSE.",
                    "mse_minus_bias",
                ),
                c(
                    "d",
                    "Efficiency and consistency are synonyms for unbiasedness; an "
                    "unbiased estimator is automatically efficient and consistent.",
                    "unbiased_implies_all",
                ),
            ],
            correct="a",
            explanation=(
                "Bias is E[θ̂] − θ and MSE = variance + squared bias. Consistency is "
                "large-sample concentration on the truth, not the same as finite-sample "
                "unbiasedness. Efficiency is a comparative variance/MSE idea, not a "
                "synonym for unbiasedness."
            ),
            model_answer=(
                "Bias = E[θ̂] − θ; MSE = Var + bias²; efficiency compares "
                "variance/MSE; consistency is convergence in probability."
            ),
            common_mistake=(
                "Equating consistency with unbiasedness, or mangling the MSE "
                "decomposition."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Estimator A is unbiased with Var(A)=4/n. Estimator B has "
                "Bias(B)=1/n and Var(B)=1/n. Which statement is correct?"
            ),
            body="Compare MSE and refuse 'unbiased always wins' / consistency-as-unbiased.",
            choices=[
                c(
                    "a",
                    "MSE(A)=4/n and MSE(B)=1/n² + 1/n. For large n, MSE(B)≈1/n < 4/n, so "
                    "B has smaller MSE. Unbiasedness is not MSE optimality, and "
                    "consistency is not the same as unbiasedness.",
                ),
                c(
                    "b",
                    "MSE(A)=4/n and MSE(B)=1/n. Because A is unbiased it always has "
                    "smaller MSE than B.",
                    "unbiased_always_wins",
                ),
                c(
                    "c",
                    "MSE(A)=4/n and MSE(B)=(1/n)² = 1/n² only (variance is ignored when "
                    "bias is present), so B is preferred for all n.",
                    "drop_variance",
                ),
                c(
                    "d",
                    "Consistency means Bias(B)=0 for every n, so B cannot be consistent "
                    "and must have larger MSE than A for large n.",
                    "consistency_as_unbiased",
                ),
            ],
            correct="a",
            explanation=(
                "MSE(A)=4/n. MSE(B)=bias² + var = 1/n² + 1/n, which is about 1/n for "
                "large n and beats 4/n. A biased estimator can win on MSE. Consistency "
                "is large-sample concentration, not finite-sample unbiasedness."
            ),
            model_answer=(
                "MSE(A)=4/n; MSE(B)=1/n²+1/n; prefer B for large n on MSE; refuse "
                "unbiased-always-best and consistency=unbiasedness."
            ),
            common_mistake=(
                "Assuming unbiased estimators always dominate on MSE, or equating "
                "consistency with unbiasedness."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.1.4 Comparison via MSE
    # ------------------------------------------------------------------
    "3.1.4-comparison-mse-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes comparing two "
                "estimators using mean square error?"
            ),
            body="Select the statement that names how MSE comparison works.",
            choices=[
                c(
                    "a",
                    "Prefer the estimator with smaller MSE. A biased estimator can beat "
                    "an unbiased one on MSE if the variance reduction outweighs squared "
                    "bias.",
                ),
                c(
                    "b",
                    "Prefer the unbiased estimator whenever one exists; MSE comparison "
                    "is unnecessary once unbiasedness is known.",
                    "unbiased_skips_mse",
                ),
                c(
                    "c",
                    "Prefer the estimator with larger bias, because larger bias always "
                    "implies smaller variance and therefore smaller MSE.",
                    "larger_bias_better",
                ),
                c(
                    "d",
                    "Two estimators are compared by checking whether either is "
                    "asymptotically Normal; that check replaces computing MSE.",
                    "asymptotics_as_comparison",
                ),
            ],
            correct="a",
            explanation=(
                "MSE comparison prefers the smaller MSE. Bias can be acceptable when "
                "variance drops enough. Unbiasedness alone does not settle the "
                "comparison, and asymptotic Normality is a different criterion."
            ),
            model_answer=(
                "Prefer smaller MSE; a biased estimator can win if variance reduction "
                "outweighs squared bias."
            ),
            common_mistake=(
                "Stopping at unbiasedness or asymptotic Normality instead of comparing "
                "MSE."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Two estimators of θ: θ̂₁ is unbiased with Var=2/n; θ̂₂ has "
                "Bias=0.5/√n and Var=0.5/n. Which statement is correct?"
            ),
            body="Compute MSE for both and refuse definition-as-comparison.",
            choices=[
                c(
                    "a",
                    "MSE₁=2/n and MSE₂=(0.5/√n)² + 0.5/n = 0.75/n. Prefer θ̂₂ on MSE. "
                    "Naming the definitions of bias and MSE is not itself a comparison "
                    "of these two estimators.",
                ),
                c(
                    "b",
                    "MSE₁=2/n and MSE₂=0.5/n (ignore squared bias). Prefer θ̂₂, and "
                    "because θ̂₁ is unbiased the comparison is optional.",
                    "drop_bias_term",
                ),
                c(
                    "c",
                    "MSE₁=2/n and MSE₂=0.25/n + 0.5/n = 0.75/n, but prefer θ̂₁ because "
                    "any unbiased estimator beats any biased one on MSE.",
                    "unbiased_always_wins",
                ),
                c(
                    "d",
                    "MSE₂=(0.5/√n)² + 0.5/n = 0.25/√n + 0.5/n. Prefer θ̂₁ because "
                    "0.25/√n dominates 2/n for large n.",
                    "bias_square_error",
                ),
            ],
            correct="a",
            explanation=(
                "MSE₁=2/n. Bias² for θ̂₂ is (0.5/√n)²=0.25/n, so MSE₂=0.75/n < 2/n. "
                "Prefer θ̂₂. Squaring 0.5/√n incorrectly as 0.25/√n is algebraically "
                "wrong. Unbiasedness does not override a worse MSE."
            ),
            model_answer=(
                "MSE₁=2/n; MSE₂=0.75/n; prefer θ̂₂. Definitions alone are not a "
                "comparison."
            ),
            common_mistake=(
                "Dropping the bias² term, preferring unbiasedness over MSE, or "
                "mishandling (0.5/√n)²."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.1.5 Asymptotic MLE
    # ------------------------------------------------------------------
    "3.1.5-asymptotic-mle-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Under standard regularity conditions, which statement "
                "correctly describes the asymptotic behaviour of an MLE?"
            ),
            body="Select the asymptotic Normal / information claim for MLEs.",
            choices=[
                c(
                    "a",
                    "For large samples the MLE is approximately Normal about the true "
                    "parameter, with variance governed by Fisher information (or the "
                    "CMP large-sample information result).",
                ),
                c(
                    "b",
                    "For large samples the MLE is exactly equal to the method-of-moments "
                    "estimator, so no distributional result is needed.",
                    "mle_equals_mom_asymp",
                ),
                c(
                    "c",
                    "The asymptotic distribution of an MLE is always chi-square with "
                    "degrees of freedom equal to the sample size.",
                    "chi_square_as_mle_law",
                ),
                c(
                    "d",
                    "Asymptotic MLE theory is the same procedure as bootstrap "
                    "resampling: both estimate the sampling distribution by redrawing "
                    "the observed sample.",
                    "bootstrap_as_asymptotics",
                ),
            ],
            correct="a",
            explanation=(
                "Under regularity, MLEs are asymptotically Normal with information-based "
                "variance. That is not MoM identity, not a chi-square-with-n law, and "
                "not the same tool as bootstrap resampling."
            ),
            model_answer=(
                "Asymptotically Normal about the true parameter with variance tied to "
                "Fisher information / CMP large-sample results."
            ),
            common_mistake=(
                "Confusing asymptotic MLE laws with MoM coincidence, chi-square "
                "recipes, or bootstrap resampling."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Under regularity, an MLE θ̂ₙ satisfies "
                "√n (θ̂ₙ − θ) →ᵈ N(0, 1/I(θ)). Which statement is correct?"
            ),
            body="Interpret the asymptotic Normal claim; refuse bootstrap-as-substitute.",
            choices=[
                c(
                    "a",
                    "For large n, θ̂ₙ is approximately Normal about θ with variance "
                    "≈ 1/(n I(θ)), which supports large-sample standard errors and "
                    "Wald-type intervals or tests. Bootstrap resampling estimates "
                    "properties by redrawing the sample; it does not replace stating "
                    "this asymptotic distribution.",
                ),
                c(
                    "b",
                    "The result says Var(θ̂ₙ) = I(θ) exactly for every finite n, so no "
                    "large-sample approximation is involved.",
                    "finite_exact_info",
                ),
                c(
                    "c",
                    "Because bootstrap can estimate a sampling distribution, the "
                    "asymptotic Normal MLE result is unnecessary whenever bootstrap "
                    "is available.",
                    "bootstrap_replaces_asymptotics",
                ),
                c(
                    "d",
                    "The result implies θ̂ₙ →ᵈ N(0, 1/I(θ)) without the √n scaling, so "
                    "the variance of θ̂ₙ itself tends to 1/I(θ).",
                    "drop_sqrt_n",
                ),
            ],
            correct="a",
            explanation=(
                "The √n-scaled error is asymptotically N(0, 1/I(θ)), so θ̂ₙ is approx "
                "Normal with variance 1/(n I(θ)). Bootstrap is a different tool and "
                "does not erase the asymptotic claim. Dropping √n misstates the limit."
            ),
            model_answer=(
                "Large-sample Normal law with variance ≈ 1/(n I(θ)); bootstrap ≠ "
                "asymptotic MLE theory."
            ),
            common_mistake=(
                "Treating the information variance as exact for finite n, dropping √n, "
                "or replacing asymptotics with bootstrap."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.1.6 Bootstrap for estimator properties
    # ------------------------------------------------------------------
    "3.1.6-bootstrap-estimator-cs1010.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the bootstrap move "
                "for estimating properties of an estimator?"
            ),
            body="Select the resampling-for-properties statement.",
            choices=[
                c(
                    "a",
                    "Resample from the observed sample (with replacement, under the "
                    "usual nonparametric bootstrap), recompute the estimator on each "
                    "resample, and summarise the replicate distribution (for example "
                    "to estimate standard error or bias).",
                ),
                c(
                    "b",
                    "Replace the estimator by its asymptotic Normal approximation; that "
                    "replacement is what 'bootstrap' means for estimator properties.",
                    "asymptotics_as_bootstrap",
                ),
                c(
                    "c",
                    "Form a confidence interval from bootstrap percentiles; estimating "
                    "an estimator's standard error is the same learning objective as "
                    "building that interval.",
                    "bootstrap_ci_as_properties",
                ),
                c(
                    "d",
                    "Bootstrap means drawing a single new sample from the fitted "
                    "parametric model and reporting that one replicate as the property "
                    "estimate.",
                    "single_replicate",
                ),
            ],
            correct="a",
            explanation=(
                "Bootstrap for estimator properties resamples, recomputes the "
                "estimator many times, and summarises the replicates. Asymptotic Normal "
                "laws and bootstrap confidence intervals are related but distinct "
                "ideas; one replicate is not a property estimate."
            ),
            model_answer=(
                "Resample, recompute the estimator, summarise replicates (e.g. SE or "
                "bias)."
            ),
            common_mistake=(
                "Equating bootstrap property estimation with asymptotics or with "
                "bootstrap CI construction."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You have an estimator θ̂ from a sample of size n. Which "
                "statement correctly describes using the bootstrap to estimate the "
                "standard error of θ̂?"
            ),
            body="Bootstrap SE procedure; refuse asymptotics-as-bootstrap and CI-as-same.",
            choices=[
                c(
                    "a",
                    "Draw many resamples with replacement from the original sample, "
                    "recompute θ̂* on each resample, and use the empirical standard "
                    "deviation of the θ̂* values as the SE estimate. That is not the "
                    "same as quoting an asymptotic Normal law, and not the same as "
                    "constructing a bootstrap confidence interval.",
                ),
                c(
                    "b",
                    "Compute the asymptotic variance 1/(n I(θ̂)) once; that single "
                    "plug-in is the bootstrap standard error by definition.",
                    "asymptotics_as_bootstrap",
                ),
                c(
                    "c",
                    "Form the percentile bootstrap confidence interval and report half "
                    "its width as the only legitimate bootstrap standard error.",
                    "ci_halfwidth_as_se",
                ),
                c(
                    "d",
                    "Resample without replacement until the resample has size n/2, "
                    "compute one θ̂*, and take |θ̂* − θ̂| as the standard error.",
                    "wrong_resample_rule",
                ),
            ],
            correct="a",
            explanation=(
                "Bootstrap SE uses the spread of many with-replacement replicates of "
                "θ̂. Asymptotic variance plug-ins and bootstrap CI construction are "
                "different procedures."
            ),
            model_answer=(
                "With-replacement resamples → θ̂* replicates → empirical SD as SE; "
                "distinct from asymptotics and from bootstrap CIs."
            ),
            common_mistake=(
                "Calling an asymptotic plug-in or a CI half-width 'the bootstrap SE'."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.1 Parameter CI
    # ------------------------------------------------------------------
    "3.2.1-confidence-interval-parameter-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a confidence interval "
                "for an unknown parameter based on a random sample?"
            ),
            body="Select the parameter-CI reading (not a prediction claim).",
            choices=[
                c(
                    "a",
                    "A confidence interval uses random-sample evidence to give an "
                    "interval for an unknown parameter, with a stated frequentist "
                    "coverage interpretation under repeated sampling.",
                ),
                c(
                    "b",
                    "A confidence interval is an interval that contains the next "
                    "future observation with the stated probability.",
                    "prediction_as_ci",
                ),
                c(
                    "c",
                    "After the data are observed, a 95% confidence interval means there "
                    "is a 95% probability that the fixed unknown parameter lies in that "
                    "specific numerical interval, in the Bayesian posterior sense.",
                    "bayesian_reading",
                ),
                c(
                    "d",
                    "A confidence interval is simply any interval estimate of a future "
                    "loss, whether or not a parameter is targeted.",
                    "any_interval",
                ),
            ],
            correct="a",
            explanation=(
                "A parameter CI targets an unknown parameter with frequentist coverage. "
                "Covering a future observation is a prediction interval. A naive "
                "post-data probability-on-the-parameter reading is not the frequentist "
                "coverage claim."
            ),
            model_answer=(
                "Interval for an unknown parameter from sample evidence, with stated "
                "frequentist coverage."
            ),
            common_mistake=(
                "Reading a parameter CI as a prediction interval or as a post-data "
                "probability on the parameter."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. From a large sample you obtain a 95% CI for mean claim "
                "size μ as (120, 140). Which statement is correct?"
            ),
            body="Interpret the parameter CI; refuse prediction reading.",
            choices=[
                c(
                    "a",
                    "The interval comes from a procedure that covers the unknown "
                    "parameter μ in 95% of repeated samples. It is not a claim that "
                    "the next claim amount falls between 120 and 140 with probability "
                    "95%.",
                ),
                c(
                    "b",
                    "There is a 95% probability that the next claim amount falls "
                    "between 120 and 140.",
                    "prediction_as_ci",
                ),
                c(
                    "c",
                    "μ is a random variable that equals 130 with probability 95%, and "
                    "the interval endpoints are fixed constants only.",
                    "parameter_as_random",
                ),
                c(
                    "d",
                    "Because the interval is narrow, coverage must be exactly 100% for "
                    "this particular sample.",
                    "narrow_implies_certainty",
                ),
            ],
            correct="a",
            explanation=(
                "Frequentist coverage is about the procedure and the parameter μ, not "
                "about the next observation. Treating μ as a random draw inside the "
                "interval, or equating narrowness with certainty, misstates coverage."
            ),
            model_answer=(
                "95% coverage for μ under repeated sampling; not a prediction interval "
                "for the next claim."
            ),
            common_mistake=(
                "Reading the CI as a 95% probability for the next observation."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.2 Prediction interval
    # ------------------------------------------------------------------
    "3.2.2-prediction-interval-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly distinguishes a prediction "
                "interval from a parameter confidence interval?"
            ),
            body="Select the future-observation vs parameter contrast.",
            choices=[
                c(
                    "a",
                    "A prediction interval targets a future observation using a model "
                    "fitted to a random sample. A parameter confidence interval targets "
                    "an unknown parameter, not the future observation itself.",
                ),
                c(
                    "b",
                    "A prediction interval and a parameter confidence interval always "
                    "cover the same numerical object; only the name changes.",
                    "interchangeable",
                ),
                c(
                    "c",
                    "A prediction interval is always narrower than the corresponding "
                    "parameter CI because a single future observation has less "
                    "uncertainty than a mean.",
                    "narrower_wrong",
                ),
                c(
                    "d",
                    "A prediction interval estimates only the sampling variance of an "
                    "estimator and never involves residual or process variation.",
                    "se_only",
                ),
            ],
            correct="a",
            explanation=(
                "Prediction intervals cover future data; parameter CIs cover "
                "parameters. Prediction intervals are typically wider because they "
                "include process/residual variation as well as parameter uncertainty."
            ),
            model_answer=(
                "Prediction interval → future observation; parameter CI → unknown "
                "parameter."
            ),
            common_mistake=(
                "Treating the two interval types as interchangeable, or claiming "
                "prediction intervals are narrower."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You fit a model to historical annual losses and need an "
                "interval for next year's loss Y_new. Which statement is correct?"
            ),
            body="Prediction vs parameter CI; refuse mean-CI-as-prediction.",
            choices=[
                c(
                    "a",
                    "A prediction interval aims to cover the future observation Y_new "
                    "(parameter uncertainty plus process/residual variation). A "
                    "confidence interval for E[Y] covers only that mean parameter and "
                    "does not finish the prediction-interval task.",
                ),
                c(
                    "b",
                    "A confidence interval for mean loss already covers Y_new with the "
                    "same coverage probability, so no separate prediction interval is "
                    "needed.",
                    "mean_ci_as_prediction",
                ),
                c(
                    "c",
                    "A prediction interval covers E[Y] only; covering Y_new would "
                    "require a parameter confidence interval instead.",
                    "targets_swapped",
                ),
                c(
                    "d",
                    "Prediction intervals ignore parameter uncertainty and use only "
                    "the residual variance from a fitted model with parameters treated "
                    "as known exactly.",
                    "ignore_parameter_uncertainty",
                ),
            ],
            correct="a",
            explanation=(
                "Prediction targets Y_new; a CI for E[Y] targets the mean. Proper "
                "prediction intervals account for both parameter uncertainty and "
                "process variation."
            ),
            model_answer=(
                "Prediction interval covers Y_new; a CI for E[Y] does not substitute."
            ),
            common_mistake=(
                "Using a mean CI as if it covered the next observation."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.3 CI given sampling distribution
    # ------------------------------------------------------------------
    "3.2.3-ci-given-sampling-distribution-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes forming a confidence "
                "interval from a given sampling distribution?"
            ),
            body="Select the invert/pivot move.",
            choices=[
                c(
                    "a",
                    "Given a sampling distribution for an estimator or pivotal "
                    "quantity, invert that distributional relationship to isolate the "
                    "parameter and obtain a confidence interval.",
                ),
                c(
                    "b",
                    "Always use the Normal-mean cookbook formula x̄ ± z s/√n, regardless "
                    "of the sampling distribution you are given.",
                    "normal_cookbook_always",
                ),
                c(
                    "c",
                    "A given sampling distribution is used only to simulate data; the "
                    "interval endpoints are chosen by eye from a histogram.",
                    "eye_histogram",
                ),
                c(
                    "d",
                    "If a sampling distribution is given, the confidence interval is "
                    "the support of that distribution with no inversion step.",
                    "support_as_ci",
                ),
            ],
            correct="a",
            explanation=(
                "The move is to invert a known sampling/pivotal relationship. Memorised "
                "Normal-mean recipes do not replace using the distribution you were "
                "actually given."
            ),
            model_answer=(
                "Invert the given sampling distribution / pivot to isolate the "
                "parameter."
            ),
            common_mistake=(
                "Jumping to a Normal-mean template instead of inverting the given law."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. For an Exponential mean-θ model you are told that "
                "2n X̄ / θ ~ χ²_{2n}. Which statement is correct?"
            ),
            body="Invert the given chi-square pivot; refuse Normal-cookbook-as-done.",
            choices=[
                c(
                    "a",
                    "Choose χ² critical values so "
                    "P(χ²_L < 2n X̄ / θ < χ²_U) = 1−α, then rearrange to isolate θ "
                    "(bounds involve 2n X̄ / χ²). A memorised Normal-mean CI formula "
                    "does not replace that inversion for this model.",
                ),
                c(
                    "b",
                    "Because X̄ is approximately Normal for large n, ignore the given "
                    "χ² relationship and always use x̄ ± z s/√n for θ.",
                    "normal_cookbook",
                ),
                c(
                    "c",
                    "The interval for θ is (χ²_L, χ²_U) with no dependence on X̄, "
                    "because the pivot already contains all information.",
                    "drop_xbar",
                ),
                c(
                    "d",
                    "Rearrange to θ ∈ (2n X̄ · χ²_L, 2n X̄ · χ²_U), multiplying by the "
                    "critical values instead of dividing.",
                    "invert_algebra_error",
                ),
            ],
            correct="a",
            explanation=(
                "From χ²_L < 2n X̄ / θ < χ²_U, taking reciprocals (and reversing "
                "inequalities) yields bounds 2n X̄ / χ²_U and 2n X̄ / χ²_L. The given "
                "pivot must be used; Normal-mean cookbooks are not a substitute."
            ),
            model_answer=(
                "Invert P(χ²_L < 2n X̄ / θ < χ²_U)=1−α to bounds in 2n X̄ / χ²; refuse "
                "Normal-mean template."
            ),
            common_mistake=(
                "Ignoring the given χ² pivot or inverting the inequality incorrectly."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.4 Normal mean and variance CIs
    # ------------------------------------------------------------------
    "3.2.4-ci-normal-mean-variance-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. For an IID Normal sample, which statement correctly "
                "describes confidence intervals for the mean and for the variance?"
            ),
            body="Select the statement that covers both Normal mean and variance CIs.",
            choices=[
                c(
                    "a",
                    "A CI for the mean typically uses a Normal or t pivotal structure "
                    "(as appropriate when σ is known or unknown). A CI for the variance "
                    "typically uses a chi-square structure based on the sample "
                    "variance.",
                ),
                c(
                    "b",
                    "A CI for the mean finishes the requirement; the variance interval "
                    "uses the same t formula with s² in place of s.",
                    "mean_only_same_formula",
                ),
                c(
                    "c",
                    "Both the mean and the variance use the same binomial Normal "
                    "approximation interval because Normal data are approximately "
                    "binomial for large n.",
                    "binomial_swap",
                ),
                c(
                    "d",
                    "A CI for σ² is formed as x̄ ± z s/√n, the same centre as the mean "
                    "interval.",
                    "mean_formula_for_variance",
                ),
            ],
            correct="a",
            explanation=(
                "Normal mean and Normal variance intervals use different pivots (t/z "
                "versus chi-square). One does not stand in for the other, and binomial "
                "recipes are a different setting."
            ),
            model_answer=(
                "Mean CI via Normal/t pivot; variance CI via chi-square pivot on s²."
            ),
            common_mistake=(
                "Treating the mean CI as enough, or reusing the mean formula for σ²."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. IID Normal sample, n=16, x̄=10, s²=4 (σ unknown). Which "
                "statement is correct?"
            ),
            body="Both mean and variance CI forms; refuse mean-only / binomial conflation.",
            choices=[
                c(
                    "a",
                    "For μ use x̄ ± t_{15, 1−α/2} · s/√n. For σ² use "
                    "((n−1)s² / χ²_{15, 1−α/2}, (n−1)s² / χ²_{15, α/2}). Both forms are "
                    "required; a binomial interval is a different setting.",
                ),
                c(
                    "b",
                    "For μ use x̄ ± z_{1−α/2} · s/√n with z even though σ is unknown; "
                    "the variance CI can be skipped once the mean CI is written.",
                    "z_not_t_and_skip_var",
                ),
                c(
                    "c",
                    "For μ use x̄ ± t_{15, 1−α/2} · s/√n, and for σ² reuse that same "
                    "numerical interval because variance intervals share the mean "
                    "endpoints.",
                    "same_interval",
                ),
                c(
                    "d",
                    "For σ² use (s² − z s/√n, s² + z s/√n), centred at s² with Normal "
                    "mean SE.",
                    "normal_se_for_variance",
                ),
            ],
            correct="a",
            explanation=(
                "With σ unknown, the mean CI uses t_{n−1}. The variance CI inverts the "
                "chi-square pivot for (n−1)s²/σ². Mean-only or Normal-SE-for-variance "
                "shortcuts fail the dual requirement."
            ),
            model_answer=(
                "t interval for μ; chi-square interval for σ²; both required."
            ),
            common_mistake=(
                "Using z with unknown σ, skipping the variance CI, or forcing a "
                "Normal-mean SE onto σ²."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.5 Binomial / Poisson CIs
    # ------------------------------------------------------------------
    "3.2.5-ci-binomial-poisson-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes Normal-approximation "
                "confidence intervals for a binomial probability and a Poisson mean?"
            ),
            body="Select the dual binomial-p and Poisson-mean claim.",
            choices=[
                c(
                    "a",
                    "Form a CI for a binomial probability p and a CI for a Poisson mean "
                    "λ, using a Normal approximation (with the appropriate variance "
                    "function) when that approximation is justified.",
                ),
                c(
                    "b",
                    "A binomial CI for p is enough; the Poisson mean uses the identical "
                    "formula after renaming p as λ, including the p(1−p) variance.",
                    "binomial_stands_for_poisson",
                ),
                c(
                    "c",
                    "Normal approximation is never used for discrete data; only exact "
                    "binomial or Poisson intervals are allowed.",
                    "forbid_normal_approx",
                ),
                c(
                    "d",
                    "Two-sample difference intervals replace single-sample binomial and "
                    "Poisson intervals in this setting.",
                    "two_sample_swap",
                ),
            ],
            correct="a",
            explanation=(
                "Both single-sample binomial-p and Poisson-mean intervals appear, with "
                "Normal approximation where appropriate. They are not the same formula, "
                "and two-sample contrasts are a different setting."
            ),
            model_answer=(
                "Binomial-p and Poisson-mean CIs, with Normal approximation when "
                "appropriate."
            ),
            common_mistake=(
                "Covering only one discrete model, or swapping in two-sample formulas."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly gives Normal-approximation CI "
                "forms for a binomial probability and a Poisson mean (single sample)?"
            ),
            body="Both forms; refuse one-as-both.",
            choices=[
                c(
                    "a",
                    "Binomial: p̂ ± z_{1−α/2} √(p̂(1−p̂)/n). Poisson: "
                    "λ̂ ± z_{1−α/2} √(λ̂/n) (or an equivalent total-count form with "
                    "matching variance). Both are required; one does not replace the "
                    "other.",
                ),
                c(
                    "b",
                    "Binomial: p̂ ± z_{1−α/2} √(p̂(1−p̂)/n). The Poisson interval is the "
                    "same expression with λ̂ written in place of p̂ and with variance "
                    "p̂(1−p̂)/n kept unchanged.",
                    "reuse_bern_variance",
                ),
                c(
                    "c",
                    "Binomial: p̂ ± z_{1−α/2} √(p̂/n). Poisson: λ̂ ± z_{1−α/2} √(λ̂(1−λ̂)/n).",
                    "variances_swapped",
                ),
                c(
                    "d",
                    "Only the binomial form is required; Poisson means are handled by "
                    "transforming to a Normal mean interval for x̄ with variance s²/n "
                    "from continuous data.",
                    "binomial_only",
                ),
            ],
            correct="a",
            explanation=(
                "Bernoulli variance is p(1−p)/n; Poisson mean variance is λ/n (per "
                "observation in the usual sample-mean form). Swapping those variance "
                "functions, or dropping Poisson entirely, is wrong."
            ),
            model_answer=(
                "p̂ ± z√(p̂(1−p̂)/n) and λ̂ ± z√(λ̂/n); both required."
            ),
            common_mistake=(
                "Reusing Bernoulli variance for Poisson, or treating one discrete CI "
                "as enough."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.6 Two-sample CIs
    # ------------------------------------------------------------------
    "3.2.6-ci-two-sample-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes two-sample confidence "
                "intervals in the Normal / binomial / Poisson settings?"
            ),
            body="Select the independent two-sample contrast claim.",
            choices=[
                c(
                    "a",
                    "Form a CI for a contrast between two independent samples (for "
                    "example a difference of means or of probabilities/means), using "
                    "Normal models or Normal approximations as appropriate.",
                ),
                c(
                    "b",
                    "If two samples have equal size, they may be analysed as paired "
                    "data even when observations are not matched.",
                    "equal_n_as_paired",
                ),
                c(
                    "c",
                    "Two-sample intervals always pool the observations into one sample "
                    "and then use a one-sample CI for the grand mean.",
                    "pool_to_one_sample",
                ),
                c(
                    "d",
                    "Two-sample CIs require dependent observations within pairs; "
                    "independent groups are handled only by prediction intervals.",
                    "require_pairing",
                ),
            ],
            correct="a",
            explanation=(
                "Two-sample CIs target contrasts under independent sampling. Equal n "
                "does not create pairing, and pooling into one sample erases the "
                "contrast."
            ),
            model_answer=(
                "CI for a contrast between two independent samples (Normal or "
                "Normal-approx discrete)."
            ),
            common_mistake=(
                "Treating equal-n independent samples as paired, or pooling away the "
                "contrast."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Independent samples of claim amounts from portfolio A and "
                "portfolio B (Normal model). Which statement is correct?"
            ),
            body="Independent contrast; refuse paired-as-equal-n two-sample.",
            choices=[
                c(
                    "a",
                    "A two-sample CI typically targets μ_A − μ_B under independent "
                    "samples from the two groups. Paired before/after rows are not the "
                    "same design: equal sample sizes do not turn matched pairs into an "
                    "independent two-sample problem.",
                ),
                c(
                    "b",
                    "If n_A = n_B, analyse the data as paired differences even when "
                    "there is no natural matching between A and B units.",
                    "equal_n_as_paired",
                ),
                c(
                    "c",
                    "Independence between samples is optional; the two-sample mean "
                    "difference CI is valid for any dependence structure.",
                    "ignore_independence",
                ),
                c(
                    "d",
                    "The two-sample CI targets μ_A / μ_B only, never a difference, when "
                    "the model is Normal.",
                    "ratio_only",
                ),
            ],
            correct="a",
            explanation=(
                "Independent two-sample CIs need independent groups and usually target "
                "a difference of means. Pairing is a different design; equal n is not "
                "enough to justify paired analysis."
            ),
            model_answer=(
                "Target μ_A − μ_B under independent samples; refuse paired-as-equal-n."
            ),
            common_mistake=(
                "Applying independent two-sample formulas to paired rows (or the "
                "reverse) because n₁=n₂."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.7 Paired means
    # ------------------------------------------------------------------
    "3.2.7-ci-paired-means-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a confidence interval "
                "for a mean difference from paired data?"
            ),
            body="Select the paired-difference move.",
            choices=[
                c(
                    "a",
                    "Form within-pair differences and construct a one-sample CI for the "
                    "mean of those differences. Pairing exploits dependence between "
                    "matched observations and is not the same as an independent "
                    "two-sample analysis.",
                ),
                c(
                    "b",
                    "Apply the independent two-sample mean-difference CI to the before "
                    "column and the after column, because pairing only affects the "
                    "labels.",
                    "two_sample_on_paired",
                ),
                c(
                    "c",
                    "Ignore the pairing and average all before values against all after "
                    "values with a pooled variance that assumes independence.",
                    "ignore_pairing",
                ),
                c(
                    "d",
                    "Paired mean-difference CIs are identical to bootstrap confidence "
                    "intervals; resampling replaces forming differences.",
                    "bootstrap_as_paired",
                ),
            ],
            correct="a",
            explanation=(
                "Paired analysis works on differences within pairs. Independent "
                "two-sample formulas ignore the dependence that pairing creates. "
                "Bootstrap CI construction is a different method."
            ),
            model_answer=(
                "Analyse paired differences with a one-sample CI for the mean "
                "difference."
            ),
            common_mistake=(
                "Running an independent two-sample CI on paired columns."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Each policyholder has a before/after loss pair "
                "(Xᵢ, Yᵢ). Which statement is correct?"
            ),
            body="Paired differences; refuse independent two-sample on paired rows.",
            choices=[
                c(
                    "a",
                    "Form Dᵢ = Yᵢ − Xᵢ (or Xᵢ − Yᵢ) and build a one-sample CI for μ_D. "
                    "Applying the independent two-sample formula to the before and "
                    "after columns ignores pairing and uses the wrong variance "
                    "structure.",
                ),
                c(
                    "b",
                    "Compute x̄ and ȳ separately and use a two-sample CI for μ_Y − μ_X "
                    "that assumes independent samples, because each column has the "
                    "same length.",
                    "two_sample_on_paired",
                ),
                c(
                    "c",
                    "The paired CI is formed for μ_X and μ_Y separately; no difference "
                    "parameter is involved.",
                    "separate_means_only",
                ),
                c(
                    "d",
                    "Pairing means you must discard half the data at random so that "
                    "the remaining before and after values are independent.",
                    "discard_to_independence",
                ),
            ],
            correct="a",
            explanation=(
                "Matched pairs → differences → one-sample CI for the mean difference. "
                "Equal column lengths do not justify an independent two-sample "
                "analysis of paired rows."
            ),
            model_answer=(
                "Analyse Dᵢ = Yᵢ − Xᵢ with a one-sample CI for μ_D; refuse "
                "independent two-sample on paired columns."
            ),
            common_mistake=(
                "Using the independent two-sample interval on paired before/after "
                "columns."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.2.8 Bootstrap CI
    # ------------------------------------------------------------------
    "3.2.8-bootstrap-confidence-interval-cs1011.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the bootstrap method "
                "for obtaining a confidence interval?"
            ),
            body="Select the resample-to-interval move.",
            choices=[
                c(
                    "a",
                    "Resample from the sample, recompute the statistic on each "
                    "replicate, and form interval endpoints from that bootstrap "
                    "distribution (for example a percentile interval).",
                ),
                c(
                    "b",
                    "Estimate only the standard error of an estimator by bootstrap; "
                    "that SE estimate is already a confidence interval.",
                    "se_as_ci",
                ),
                c(
                    "c",
                    "Bootstrap confidence intervals are the same procedure as a "
                    "hypothesis test: both decide whether to reject a null.",
                    "ht_as_bootstrap_ci",
                ),
                c(
                    "d",
                    "A bootstrap CI is formed by taking the Normal-mean cookbook "
                    "interval and replacing s with a single bootstrap draw.",
                    "one_draw_plug_in",
                ),
            ],
            correct="a",
            explanation=(
                "Bootstrap CIs use the replicate distribution of the statistic to form "
                "endpoints. Estimating an SE alone is not yet an interval method of "
                "the same kind, and hypothesis testing is a different task."
            ),
            model_answer=(
                "Resample, recompute the statistic, form endpoints from the bootstrap "
                "distribution (e.g. percentiles)."
            ),
            common_mistake=(
                "Equating bootstrap SE estimation or hypothesis testing with bootstrap "
                "CI construction."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly outlines a percentile bootstrap "
                "confidence interval and keeps related ideas distinct?"
            ),
            body="Percentile bootstrap CI; refuse SE-only and HT conflation.",
            choices=[
                c(
                    "a",
                    "Resample with replacement, recompute the statistic on each "
                    "resample, then take the α/2 and 1−α/2 quantiles of those "
                    "replicates as interval endpoints. Estimating a bootstrap standard "
                    "error alone is not the same as constructing that CI, and forming "
                    "the CI is not a hypothesis test.",
                ),
                c(
                    "b",
                    "Compute a bootstrap SE and report (θ̂ − SE, θ̂ + SE) only; quantile "
                    "endpoints from replicates are never used.",
                    "se_only_as_ci",
                ),
                c(
                    "c",
                    "A bootstrap CI is completed by rejecting H₀ whenever θ̂ falls "
                    "outside a fixed null value, without forming interval endpoints.",
                    "ht_as_ci",
                ),
                c(
                    "d",
                    "Draw one bootstrap resample, compute θ̂*, and report the "
                    "singleton interval [θ̂*, θ̂*].",
                    "singleton_interval",
                ),
            ],
            correct="a",
            explanation=(
                "Percentile intervals use replicate quantiles. SE-only summaries and "
                "hypothesis-test decisions are different objects."
            ),
            model_answer=(
                "Percentile endpoints from bootstrap replicates; distinct from SE-only "
                "bootstrap and from HT."
            ),
            common_mistake=(
                "Treating bootstrap SE estimation or a reject/retain decision as the "
                "bootstrap CI."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.3.1 Hypothesis concepts
    # ------------------------------------------------------------------
    "3.3.1-hypothesis-concepts-cs1012.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly defines null vs alternative, "
                "Type I vs Type II error, p-value, and power?"
            ),
            body="Select the HT vocabulary statement.",
            choices=[
                c(
                    "a",
                    "The null is the statement under test; the alternative is the "
                    "competing claim. Type I error is rejecting a true null; Type II "
                    "error is failing to reject a false null. A p-value is the "
                    "probability, under the null, of a result at least as extreme as "
                    "observed; power is the probability of rejecting a false null.",
                ),
                c(
                    "b",
                    "Type I error is failing to reject a false null; Type II error is "
                    "rejecting a true null. A p-value is the probability that the "
                    "alternative is true.",
                    "errors_swapped_pvalue",
                ),
                c(
                    "c",
                    "A p-value is the probability that the null is true given the data, "
                    "and power is one minus the p-value.",
                    "pvalue_as_null_prob",
                ),
                c(
                    "d",
                    "Null and alternative are interchangeable labels; only the test "
                    "statistic formula matters, not which hypothesis is labelled null.",
                    "labels_interchangeable",
                ),
            ],
            correct="a",
            explanation=(
                "Keep Type I/II in the reject-true-null / fail-to-reject-false-null "
                "directions. A p-value is a tail probability under H₀, not P(H₀|data) "
                "and not P(H₁). Power is P(reject H₀ | H₁ true)."
            ),
            model_answer=(
                "Null vs alternative; Type I = false reject; Type II = false retain; "
                "p-value = extreme-tail probability under H₀; power = P(reject | H₁)."
            ),
            common_mistake=(
                "Swapping Type I/II, or reading the p-value as P(H₀|data) or P(H₁)."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Disease screening: H₀ = no disease, H₁ = disease present. "
                "Which statement is correct?"
            ),
            body="HT vocabulary on a vignette; refuse cookbook-test-as-concepts.",
            choices=[
                c(
                    "a",
                    "Type I error is a false positive (declare disease when healthy). "
                    "Type II error is a false negative (miss disease when present). A "
                    "p-value is the probability under H₀ of a result at least as "
                    "extreme as observed; power is P(reject H₀ | H₁ true). Running a "
                    "software z-test does not by itself replace this vocabulary.",
                ),
                c(
                    "b",
                    "Type I error is missing disease when it is present; Type II error "
                    "is declaring disease when healthy.",
                    "errors_swapped",
                ),
                c(
                    "c",
                    "A p-value is the probability of having the disease, and power is "
                    "the probability of not having the disease.",
                    "pvalue_as_disease_prob",
                ),
                c(
                    "d",
                    "Because a one-sample Normal mean test can be clicked in software, "
                    "Type I/II, p-value, and power definitions are unnecessary.",
                    "cookbook_as_concepts",
                ),
            ],
            correct="a",
            explanation=(
                "In this framing, false positive = Type I and false negative = Type II. "
                "p-value and power keep their usual frequentist meanings. Software "
                "theatre does not replace the concepts."
            ),
            model_answer=(
                "Type I = false positive; Type II = false negative; p-value under H₀; "
                "power = 1−β; concepts ≠ cookbook click."
            ),
            common_mistake=(
                "Swapping Type I/II, or treating a software z-test as the concepts."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.3.2 Basic tests
    # ------------------------------------------------------------------
    "3.3.2-basic-tests-cs1012.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly matches basic hypothesis-test "
                "settings to designs and models?"
            ),
            body="Select one-sample / two-sample / paired and Normal vs discrete.",
            choices=[
                c(
                    "a",
                    "One-sample tests a single population parameter; two-sample "
                    "compares independent groups; paired uses matched differences. "
                    "Basic procedures include Normal mean tests and binomial/Poisson "
                    "tests under CMP conditions.",
                ),
                c(
                    "b",
                    "Paired data should be analysed with the independent two-sample "
                    "test whenever n₁ = n₂.",
                    "paired_as_two_sample",
                ),
                c(
                    "c",
                    "Permutation reshuffling of labels is the basic parametric test "
                    "for Normal means in this learning objective.",
                    "permutation_as_basic",
                ),
                c(
                    "d",
                    "Binomial and Poisson data never use basic tests; only continuous "
                    "Normal means appear.",
                    "discrete_excluded",
                ),
            ],
            correct="a",
            explanation=(
                "Match design (one-sample, two-sample, paired) and model (Normal, "
                "binomial, Poisson). Permutation tests are a different approach; equal "
                "n does not erase pairing."
            ),
            model_answer=(
                "One-sample / two-sample / paired designs; Normal and binomial/Poisson "
                "basic tests."
            ),
            common_mistake=(
                "Using permutation as the basic parametric test, or mishandling "
                "paired vs independent designs."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Which statement correctly names the basic test family for "
                "each setting and keeps permutation distinct?"
            ),
            body="Match settings to basic tests; refuse permutation-as-basic.",
            choices=[
                c(
                    "a",
                    "(a) one Normal mean with σ known → one-sample Normal/z-test; "
                    "(b) two independent binomial proportions → two-sample proportion "
                    "test with Normal approximation; (c) paired Normal differences → "
                    "paired test on differences. Permutation tests are a different "
                    "approach, not a substitute for these basic parametric tests.",
                ),
                c(
                    "b",
                    "(a) chi-square GOF; (b) paired t on raw unpaired columns; "
                    "(c) independent two-sample z on matched pairs.",
                    "wrong_families",
                ),
                c(
                    "c",
                    "All three settings are handled by shuffling treatment labels under "
                    "a permutation null; parametric Normal/binomial tests are optional "
                    "flavour.",
                    "permutation_as_basic",
                ),
                c(
                    "d",
                    "(a) two-sample z for one mean; (b) one-sample Poisson test for two "
                    "proportions; (c) binomial test for paired Normal differences.",
                    "designs_scrambled",
                ),
            ],
            correct="a",
            explanation=(
                "Basic tests follow the sampling model and design. Permutation is "
                "separate. Scrambling designs (paired vs independent, one-sample vs "
                "two-sample) produces the wrong procedure."
            ),
            model_answer=(
                "z-test for one Normal mean (σ known); two-sample proportion test; "
                "paired test on differences; permutation ≠ basic parametric."
            ),
            common_mistake=(
                "Calling a permutation shuffle the basic-test requirement, or "
                "mismatching design to procedure."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.3.3 Permutation tests
    # ------------------------------------------------------------------
    "3.3.3-permutation-tests-cs1012.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a permutation "
                "hypothesis test?"
            ),
            body="Select the exchangeability → reference distribution move.",
            choices=[
                c(
                    "a",
                    "Under an exchangeability null, labels or assignments are permuted "
                    "to build a reference distribution for the test statistic; the "
                    "observed statistic is compared with that distribution.",
                ),
                c(
                    "b",
                    "A permutation test is identical to a Normal two-sample z-test; "
                    "only the name changes.",
                    "z_as_permutation",
                ),
                c(
                    "c",
                    "Permutation tests estimate a confidence interval by resampling "
                    "with replacement, the same way a bootstrap CI does.",
                    "bootstrap_as_permutation",
                ),
                c(
                    "d",
                    "Permutation tests are chi-square goodness-of-fit procedures that "
                    "compare observed frequencies to a named distribution.",
                    "gof_as_permutation",
                ),
            ],
            correct="a",
            explanation=(
                "Permutation HT uses reshuffling under an exchangeable null. It is not "
                "a Normal cookbook z-test, not bootstrap CI construction, and not "
                "chi-square GOF."
            ),
            model_answer=(
                "Permute labels under exchangeability; compare the observed statistic "
                "to the permutation reference distribution."
            ),
            common_mistake=(
                "Equating permutation with Normal z-tests, bootstrap CIs, or GOF."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Under H₀ of no treatment effect, treatment labels are "
                "exchangeable across units. Which statement is correct?"
            ),
            body="Permutation move; refuse Normal-cookbook and GOF conflation.",
            choices=[
                c(
                    "a",
                    "Shuffle or reassign labels under H₀, recompute the test statistic "
                    "many times, and compare the observed statistic to that permutation "
                    "reference distribution. That is not a Normal two-sample z-test by "
                    "another name, and not a chi-square GOF to a named distribution.",
                ),
                c(
                    "b",
                    "Compute a Normal two-sample z statistic once; permutation is only "
                    "an optional label for that same parametric test.",
                    "z_as_permutation",
                ),
                c(
                    "c",
                    "Compare observed frequencies to Poisson expected counts with a "
                    "chi-square GOF; that finishes the permutation requirement.",
                    "gof_as_permutation",
                ),
                c(
                    "d",
                    "Resample with replacement to form a percentile confidence "
                    "interval; reject H₀ if zero is outside that interval, and call "
                    "the procedure a permutation test.",
                    "bootstrap_ci_as_permutation",
                ),
            ],
            correct="a",
            explanation=(
                "Permutation builds a null reference from exchangeability. Parametric "
                "Normal tests, GOF, and bootstrap CIs are different tools."
            ),
            model_answer=(
                "Exchangeability → permute → reference distribution; refuse "
                "Normal-cookbook and GOF conflation."
            ),
            common_mistake=(
                "Treating permutation as optional flavour of a z-test, or swapping in "
                "GOF/bootstrap CI."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.3.4 Chi-square GOF
    # ------------------------------------------------------------------
    "3.3.4-chi-square-gof-cs1012.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a chi-square "
                "goodness-of-fit test, including unknown parameters?"
            ),
            body="Select the GOF hypothesis, expected counts, and DF adjustment.",
            choices=[
                c(
                    "a",
                    "GOF tests whether a sample is consistent with a stated "
                    "distribution. Expected counts come from the hypothesised "
                    "probabilities and the sample size. If parameters are estimated "
                    "from the same sample, degrees of freedom are reduced under CMP "
                    "rules.",
                ),
                c(
                    "b",
                    "GOF is identical to a two-way test of independence; expected "
                    "counts always use row and column totals only.",
                    "independence_as_gof",
                ),
                c(
                    "c",
                    "When parameters are estimated, degrees of freedom increase by the "
                    "number of estimated parameters.",
                    "df_increases",
                ),
                c(
                    "d",
                    "Expected frequencies are always set equal to the observed "
                    "frequencies, so the chi-square statistic is automatically zero.",
                    "e_equals_o",
                ),
            ],
            correct="a",
            explanation=(
                "GOF compares observed counts to expectations under a named "
                "distribution. Estimating parameters reduces DF. Independence in a "
                "contingency table is a different test."
            ),
            model_answer=(
                "Test fit to a stated distribution; expected counts from hypothesised "
                "probabilities; reduce DF when parameters are estimated."
            ),
            common_mistake=(
                "Equating GOF with independence, or adjusting DF in the wrong "
                "direction."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. You test whether claim counts follow a Poisson "
                "distribution; λ is estimated from the same sample. Which statement is "
                "correct?"
            ),
            body="Expected counts and DF adjust; refuse independence-as-GOF.",
            choices=[
                c(
                    "a",
                    "Expected frequencies are n times fitted Poisson probabilities "
                    "using λ̂. Degrees of freedom are (number of bins − 1 − number of "
                    "estimated parameters), so subtract 1 for λ̂. A chi-square test of "
                    "independence in a two-way table is a different procedure.",
                ),
                c(
                    "b",
                    "Expected frequencies use λ̂, but degrees of freedom stay at "
                    "(bins − 1) with no reduction for estimating λ.",
                    "forget_df_adjust",
                ),
                c(
                    "c",
                    "Because λ is estimated, replace GOF by a two-way independence test "
                    "on a contingency table of counts.",
                    "independence_as_gof",
                ),
                c(
                    "d",
                    "Expected frequencies are n/λ̂ in every bin, regardless of the "
                    "Poisson probabilities for those bins.",
                    "flat_expected",
                ),
            ],
            correct="a",
            explanation=(
                "Fit Poisson probabilities with λ̂, form expected counts, and reduce DF "
                "by one for λ̂. Independence testing is not GOF to a named "
                "distribution."
            ),
            model_answer=(
                "E = n × Poisson probabilities at λ̂; DF = bins − 1 − 1; independence ≠ "
                "GOF."
            ),
            common_mistake=(
                "Forgetting the DF reduction for λ̂, or treating independence as GOF."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # 3.3.5 Contingency independence
    # ------------------------------------------------------------------
    "3.3.5-contingency-independence-cs1012.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a chi-square test of "
                "independence in a contingency table?"
            ),
            body="Select the two-way independence claim.",
            choices=[
                c(
                    "a",
                    "A two-way table cross-classifies two criteria. The independence "
                    "null says the row and column factors do not associate; expected "
                    "cell counts use the product of marginal totals divided by n.",
                ),
                c(
                    "b",
                    "Independence testing is the same as one-sample goodness-of-fit to "
                    "a named distribution such as Poisson.",
                    "gof_as_independence",
                ),
                c(
                    "c",
                    "Expected cell counts are always n divided by the number of cells, "
                    "ignoring the observed margins.",
                    "flat_expected",
                ),
                c(
                    "d",
                    "A contingency table classifies only one factor; the second "
                    "dimension is reserved for expected counts under a continuous "
                    "Normal model.",
                    "one_factor_only",
                ),
            ],
            correct="a",
            explanation=(
                "Independence uses E_{ij} = (row total × column total)/n in a two-way "
                "table. That is not one-sample distributional GOF."
            ),
            model_answer=(
                "Two-way cross-classification; independence null; "
                "E_{ij}=(row total×column total)/n."
            ),
            common_mistake=(
                "Treating GOF and two-way independence as the same chi-square "
                "procedure."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Two-way table: rating class × claim/no-claim. Which "
                "statement is correct?"
            ),
            body="Independence null and expected counts; refuse GOF conflation.",
            choices=[
                c(
                    "a",
                    "H₀: row and column classifications are independent; "
                    "E_{ij} = (row i total × column j total) / n. This is not the same "
                    "as a chi-square GOF testing whether one sample follows a named "
                    "distribution.",
                ),
                c(
                    "b",
                    "H₀: the counts follow a Poisson distribution with mean estimated "
                    "from the table total; expected counts are that fitted Poisson pmf "
                    "times n.",
                    "gof_as_independence",
                ),
                c(
                    "c",
                    "H₀: independence; expected counts equal the observed counts in "
                    "every cell.",
                    "e_equals_o",
                ),
                c(
                    "d",
                    "H₀: independence; E_{ij} = row i total + column j total, without "
                    "dividing by n.",
                    "sum_not_product",
                ),
            ],
            correct="a",
            explanation=(
                "Independence expected counts are products of margins over n. GOF to a "
                "named distribution is a different hypothesis and different expected "
                "count construction."
            ),
            model_answer=(
                "Independence null; E_{ij}=(row total×column total)/n; refuse GOF "
                "conflation."
            ),
            common_mistake=(
                "Using GOF-style expected counts, or mangling the margin product "
                "formula."
            ),
        ),
    },
    # ------------------------------------------------------------------
    # Pi Memory Front Section 3
    # ------------------------------------------------------------------
    "cp-3.1.1-estimators-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes the method-of-moments "
                "move for constructing an estimator?"
            ),
            body="Select the MoM construction (estimator, not interval).",
            choices=[
                c(
                    "a",
                    "Match sample moments to population moments (as functions of "
                    "parameters) and solve to construct a point estimator of the "
                    "parameter.",
                ),
                c(
                    "b",
                    "Maximise the likelihood; the maximiser is called the "
                    "method-of-moments estimator by definition.",
                    "mle_as_mom",
                ),
                c(
                    "c",
                    "Construct a confidence interval for the parameter; the interval "
                    "itself is the method-of-moments estimator.",
                    "ci_as_estimator",
                ),
                c(
                    "d",
                    "Choose any convenient formula for θ̂; method of moments means "
                    "having a closed form, regardless of how it was derived.",
                    "any_formula",
                ),
            ],
            correct="a",
            explanation=(
                "MoM equates moments and solves for a point estimator. MLE is a "
                "different construction, and a confidence interval is not an estimator "
                "in the MoM sense."
            ),
            model_answer=(
                "Equate sample moments to population moments and solve for the "
                "parameter."
            ),
            common_mistake=(
                "Collapsing MoM with MLE, or treating a CI as the MoM estimator."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Exponential claim sizes with mean θ; sample mean x̄ = 5. "
                "Which statement is correct?"
            ),
            body="MoM for Exponential mean; refuse MLE-as-MoM and estimator-as-CI.",
            choices=[
                c(
                    "a",
                    "Equate E[X]=θ to x̄, so θ̂_MoM = 5. Maximising the likelihood is "
                    "MLE, a different construction. An estimator is a point estimate; "
                    "a confidence interval is an interval procedure for a parameter.",
                ),
                c(
                    "b",
                    "θ̂_MoM = 1/5 because the Exponential mean-θ model uses E[X]=1/θ.",
                    "rate_mean_swap",
                ),
                c(
                    "c",
                    "Because the MLE equals x̄ here, maximising the likelihood is "
                    "already the method-of-moments construction.",
                    "mle_as_mom",
                ),
                c(
                    "d",
                    "θ̂_MoM = 5 means the 95% confidence interval for θ is the singleton "
                    "{5}.",
                    "estimator_as_ci",
                ),
            ],
            correct="a",
            explanation=(
                "For mean-θ Exponential, MoM gives θ̂ = x̄ = 5. MLE coincidence does not "
                "rewrite the construction, and a point estimator is not a CI."
            ),
            model_answer=(
                "θ̂_MoM = x̄ = 5; refuse MLE-as-MoM and estimator-as-CI."
            ),
            common_mistake=(
                "Swapping mean/rate, collapsing MoM with MLE, or treating the point "
                "estimate as an interval."
            ),
        ),
    },
    "cp-3.2.1-ci-sample-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly describes a confidence interval "
                "for an unknown parameter from a random sample?"
            ),
            body="Select the parameter-CI claim.",
            choices=[
                c(
                    "a",
                    "A CI uses sample information to construct an interval for an "
                    "unknown parameter under stated assumptions, with a frequentist "
                    "coverage reading for that parameter.",
                ),
                c(
                    "b",
                    "A CI is a probability statement that the next observation falls "
                    "inside the numerical interval.",
                    "prediction_as_ci",
                ),
                c(
                    "c",
                    "A CI is the same decision procedure as a hypothesis test: both "
                    "only accept or reject a null.",
                    "ht_as_ci",
                ),
                c(
                    "d",
                    "After seeing the data, a 95% CI means the parameter equals the "
                    "interval midpoint with probability 95%.",
                    "midpoint_probability",
                ),
            ],
            correct="a",
            explanation=(
                "Parameter CIs target a parameter with coverage. They are not "
                "prediction intervals for the next observation, and not identical to "
                "hypothesis tests."
            ),
            model_answer=(
                "Sample-based interval for an unknown parameter with stated coverage."
            ),
            common_mistake=(
                "Reading a CI as a prediction claim or as a hypothesis test."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. A 95% CI for mean claim size μ is (80, 100). Which "
                "statement is correct?"
            ),
            body="Coverage reading; refuse prediction and HT conflation.",
            choices=[
                c(
                    "a",
                    "The interval comes from a procedure with 95% coverage for the "
                    "unknown parameter μ under repeated sampling. It is not a 95% "
                    "probability that the next claim falls in (80, 100), and it is not "
                    "the same object as a hypothesis test.",
                ),
                c(
                    "b",
                    "There is a 95% chance the next claim falls in (80, 100).",
                    "prediction_as_ci",
                ),
                c(
                    "c",
                    "The interval is a hypothesis test that automatically rejects every "
                    "null outside (80, 100) without further structure.",
                    "ht_as_ci",
                ),
                c(
                    "d",
                    "μ equals 90 with probability 95%, because 90 is the midpoint.",
                    "midpoint_probability",
                ),
            ],
            correct="a",
            explanation=(
                "Coverage is about μ and the procedure. Prediction readings and "
                "'midpoint probability' misstate frequentist CIs; HT is a related but "
                "distinct task."
            ),
            model_answer=(
                "95% coverage for μ; refuse prediction reading and CI=HT collapse."
            ),
            common_mistake=(
                "Reading the CI as a probability for the next claim, or equating CIs "
                "with hypothesis tests."
            ),
        ),
    },
    "cp-3.3.1-hypothesis-testing-cs1016.json": {
        "ar": _item(
            prompt=(
                "Closed-book. Which statement correctly distinguishes null vs "
                "alternative and Type I vs Type II error at foundation level?"
            ),
            body="Select the HT foundation statement.",
            choices=[
                c(
                    "a",
                    "The null and alternative frame the hypotheses under test. Type I "
                    "error is rejecting a true null; Type II error is failing to reject "
                    "a false null. Power is the probability of rejecting a false null.",
                ),
                c(
                    "b",
                    "Type I error is failing to reject a false null; Type II error is "
                    "rejecting a true null.",
                    "errors_swapped",
                ),
                c(
                    "c",
                    "Null and alternative matter only for linear regression fitting; "
                    "they are not used in hypothesis testing vocabulary.",
                    "regression_swap",
                ),
                c(
                    "d",
                    "Type I and Type II errors are the same event whenever the p-value "
                    "is below 5%.",
                    "errors_collapsed",
                ),
            ],
            correct="a",
            explanation=(
                "Keep null/alternative and Type I/II in their standard directions. "
                "Regression fitting is a different topic; Type I and Type II are not "
                "the same event."
            ),
            model_answer=(
                "Null vs alternative; Type I = false reject; Type II = false retain; "
                "power = P(reject | H₁)."
            ),
            common_mistake=(
                "Swapping Type I/II, or displacing HT vocabulary into regression."
            ),
        ),
        "cp": _item(
            prompt=(
                "Closed-book. Fraud flag: H₀ = genuine claim, H₁ = fraudulent. Which "
                "statement is correct?"
            ),
            body="Type I/II, p-value, power; refuse cookbook-as-concepts and regression.",
            choices=[
                c(
                    "a",
                    "Type I: flag fraud when the claim is genuine. Type II: miss fraud "
                    "when it is present. A p-value is the probability under H₀ of data "
                    "at least as extreme as observed; power is P(reject H₀ | H₁ true). "
                    "A software z-test click does not replace this vocabulary, and "
                    "linear regression is a different topic.",
                ),
                c(
                    "b",
                    "Type I: miss fraud when present; Type II: flag fraud when genuine.",
                    "errors_swapped",
                ),
                c(
                    "c",
                    "Because a software z-test can be run, Type I/II, p-value, and power "
                    "definitions are optional.",
                    "cookbook_as_concepts",
                ),
                c(
                    "d",
                    "HT foundations are the same skill as fitting a linear regression "
                    "of loss on covariates.",
                    "regression_as_ht",
                ),
            ],
            correct="a",
            explanation=(
                "False fraud flag = Type I; missed fraud = Type II. Keep p-value and "
                "power in frequentist form. Neither software theatre nor regression "
                "fitting substitutes for the concepts."
            ),
            model_answer=(
                "Type I = false fraud flag; Type II = missed fraud; p-value under H₀; "
                "power = 1−β; refuse cookbook-as-concepts and regression conflation."
            ),
            common_mistake=(
                "Swapping Type I/II, or treating a z-test click / regression fit as HT "
                "concepts."
            ),
        ),
    },
}

# Inventory filename -> campaign twin relative path under educational_campaigns/cs1/
CAMPAIGN_TWINS: dict[str, str] = {
    "3.1.1-method-of-moments-cs1010.json": "campaign-kappa-cs1010/packages/3.1.1-method-of-moments-cs1010.json",
    "3.1.2-maximum-likelihood-cs1010.json": "campaign-kappa-cs1010/packages/3.1.2-maximum-likelihood-cs1010.json",
    "3.1.3-efficiency-bias-consistency-mse-cs1010.json": "campaign-kappa-cs1010/packages/3.1.3-efficiency-bias-consistency-mse-cs1010.json",
    "3.1.4-comparison-mse-cs1010.json": "campaign-kappa-cs1010/packages/3.1.4-comparison-mse-cs1010.json",
    "3.1.5-asymptotic-mle-cs1010.json": "campaign-kappa-cs1010/packages/3.1.5-asymptotic-mle-cs1010.json",
    "3.1.6-bootstrap-estimator-cs1010.json": "campaign-kappa-cs1010/packages/3.1.6-bootstrap-estimator-cs1010.json",
    "3.2.1-confidence-interval-parameter-cs1011.json": "campaign-lambda-cs1011/packages/3.2.1-confidence-interval-parameter-cs1011.json",
    "3.2.2-prediction-interval-cs1011.json": "campaign-lambda-cs1011/packages/3.2.2-prediction-interval-cs1011.json",
    "3.2.3-ci-given-sampling-distribution-cs1011.json": "campaign-lambda-cs1011/packages/3.2.3-ci-given-sampling-distribution-cs1011.json",
    "3.2.4-ci-normal-mean-variance-cs1011.json": "campaign-lambda-cs1011/packages/3.2.4-ci-normal-mean-variance-cs1011.json",
    "3.2.5-ci-binomial-poisson-cs1011.json": "campaign-lambda-cs1011/packages/3.2.5-ci-binomial-poisson-cs1011.json",
    "3.2.6-ci-two-sample-cs1011.json": "campaign-lambda-cs1011/packages/3.2.6-ci-two-sample-cs1011.json",
    "3.2.7-ci-paired-means-cs1011.json": "campaign-lambda-cs1011/packages/3.2.7-ci-paired-means-cs1011.json",
    "3.2.8-bootstrap-confidence-interval-cs1011.json": "campaign-lambda-cs1011/packages/3.2.8-bootstrap-confidence-interval-cs1011.json",
    "3.3.1-hypothesis-concepts-cs1012.json": "campaign-mu-cs1012/packages/3.3.1-hypothesis-concepts-cs1012.json",
    "3.3.2-basic-tests-cs1012.json": "campaign-mu-cs1012/packages/3.3.2-basic-tests-cs1012.json",
    "3.3.3-permutation-tests-cs1012.json": "campaign-mu-cs1012/packages/3.3.3-permutation-tests-cs1012.json",
    "3.3.4-chi-square-gof-cs1012.json": "campaign-mu-cs1012/packages/3.3.4-chi-square-gof-cs1012.json",
    "3.3.5-contingency-independence-cs1012.json": "campaign-mu-cs1012/packages/3.3.5-contingency-independence-cs1012.json",
    "cp-3.1.1-estimators-cs1016.json": "campaign-pi-cs1016/packages/3.1.1-estimators-cs1016.json",
    "cp-3.2.1-ci-sample-cs1016.json": "campaign-pi-cs1016/packages/3.2.1-ci-sample-cs1016.json",
    "cp-3.3.1-hypothesis-testing-cs1016.json": "campaign-pi-cs1016/packages/3.3.1-hypothesis-testing-cs1016.json",
}


# Campaign package stem (filename without .json) -> inventory conversion key
STEM_TO_INVENTORY: dict[str, str] = {
    "3.1.1-method-of-moments-cs1010": "3.1.1-method-of-moments-cs1010.json",
    "3.1.2-maximum-likelihood-cs1010": "3.1.2-maximum-likelihood-cs1010.json",
    "3.1.3-efficiency-bias-consistency-mse-cs1010": "3.1.3-efficiency-bias-consistency-mse-cs1010.json",
    "3.1.4-comparison-mse-cs1010": "3.1.4-comparison-mse-cs1010.json",
    "3.1.5-asymptotic-mle-cs1010": "3.1.5-asymptotic-mle-cs1010.json",
    "3.1.6-bootstrap-estimator-cs1010": "3.1.6-bootstrap-estimator-cs1010.json",
    "3.2.1-confidence-interval-parameter-cs1011": "3.2.1-confidence-interval-parameter-cs1011.json",
    "3.2.2-prediction-interval-cs1011": "3.2.2-prediction-interval-cs1011.json",
    "3.2.3-ci-given-sampling-distribution-cs1011": "3.2.3-ci-given-sampling-distribution-cs1011.json",
    "3.2.4-ci-normal-mean-variance-cs1011": "3.2.4-ci-normal-mean-variance-cs1011.json",
    "3.2.5-ci-binomial-poisson-cs1011": "3.2.5-ci-binomial-poisson-cs1011.json",
    "3.2.6-ci-two-sample-cs1011": "3.2.6-ci-two-sample-cs1011.json",
    "3.2.7-ci-paired-means-cs1011": "3.2.7-ci-paired-means-cs1011.json",
    "3.2.8-bootstrap-confidence-interval-cs1011": "3.2.8-bootstrap-confidence-interval-cs1011.json",
    "3.3.1-hypothesis-concepts-cs1012": "3.3.1-hypothesis-concepts-cs1012.json",
    "3.3.2-basic-tests-cs1012": "3.3.2-basic-tests-cs1012.json",
    "3.3.3-permutation-tests-cs1012": "3.3.3-permutation-tests-cs1012.json",
    "3.3.4-chi-square-gof-cs1012": "3.3.4-chi-square-gof-cs1012.json",
    "3.3.5-contingency-independence-cs1012": "3.3.5-contingency-independence-cs1012.json",
    "3.1.1-estimators-cs1016": "cp-3.1.1-estimators-cs1016.json",
    "3.2.1-ci-sample-cs1016": "cp-3.2.1-ci-sample-cs1016.json",
    "3.3.1-hypothesis-testing-cs1016": "cp-3.3.1-hypothesis-testing-cs1016.json",
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace AR/CP knowledge_checks with Batch 1 MCQ content when stem is in scope."""
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

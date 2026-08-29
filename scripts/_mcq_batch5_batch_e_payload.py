#!/usr/bin/env python3
# ruff: noqa: E501
"""Batch 5 MCQ conversion payload for the checkpoint Batch E file set.

Applies deterministic four-option MCQ rewrites to Active Recall and Checkpoint
items for 17 CS1 educational packages. The Delta packages 4.2.10 and 5.1.9 are
the WEAK items in this scope. The STRONG Delta items 4.2.3, 4.2.5, 5.1.1, and
5.1.5 belong to Batch 6 and are intentionally excluded.
"""
from __future__ import annotations

import json
import re
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


CONVERSIONS: dict[str, dict[str, dict]] = {
    "2.1.6-software-generation-cs1004.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly describes generating and checking Poisson and Exponential simulated values?",
            body="Select the generation and sanity-check procedure.",
            choices=[
                c("a", "Generate Poisson values with the chosen mean parameter and check that values are non-negative integers with sample mean near that parameter. Generate Exponential values with the chosen mean and check positivity and a sample mean near that mean."),
                c("b", "Generate both distributions and accept the output without checking support or sample summaries because a library sampler cannot fail.", "software_without_check"),
                c("c", "Check Poisson values are positive real numbers and Exponential values are non-negative integers, since both use a mean parameter.", "supports_reversed"),
                c("d", "A matching sample mean proves the simulated distribution is correct even if Poisson outputs are fractional or Exponential outputs are negative.", "mean_check_only"),
            ],
            correct="a",
            explanation="Simulation requires both generation and basic validation against support and moments. Software output alone or a mean-only check is insufficient.",
            model_answer="Poisson: non-negative integers and mean check. Exponential: positive values and mean check.",
            common_mistake="Generating values without checking support and whether simple sample summaries are plausible.",
        ),
        "cp": _item(
            prompt="Closed-book. You simulate Poisson(λ=3) counts and Exponential waiting times with mean 2. Which statement is correct?",
            body="Choose the valid simulation and sanity-check conclusion.",
            choices=[
                c(
                    "a",
                    "Poisson draws should be non-negative integers with sample mean near 3. "
                    "Exponential draws should be positive with sample mean near 2. A built-in "
                    "sampler does not replace understanding inverse-transform sampling, and "
                    "generating alone is not a completed sanity check.",
                ),
                c(
                    "b",
                    "Using a built-in sampler removes the need to inspect support or sample "
                    "means because software generation is itself a sanity check.",
                    "sampler_replaces_check",
                ),
                c(
                    "c",
                    "Poisson draws should average near 2 and Exponential draws near 3 because "
                    "λ is a waiting-time mean.",
                    "parameters_swapped",
                ),
                c(
                    "d",
                    "The simulation is valid if both samples contain only integers, since "
                    "Exponential waiting times are discrete event counts.",
                    "exponential_as_discrete",
                ),
            ],
            correct="a",
            explanation=(
                "The checks must match each distribution's support and mean. A sampler "
                "performs generation, not validation or a substitute for inverse-transform "
                "understanding."
            ),
            model_answer=(
                "Poisson: integers near mean 3. Exponential: positive near mean 2. Sampler "
                "does not replace inverse-transform understanding or sanity checks."
            ),
            common_mistake=(
                "Treating software generation as complete without support or mean checks, or "
                "equating a sampler with inverse-transform understanding."
            ),
        ),
    },
    "2.2.1-marginal-conditional-cs1005.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly obtains marginal and conditional distributions from a joint distribution?",
            body="Select marginal and conditional construction.",
            choices=[
                c("a", "Obtain a marginal by summing or integrating the joint distribution over the other variable. Obtain a conditional by dividing the relevant joint probability or density by the marginal of the conditioning value."),
                c("b", "The joint distribution is already numerically equal to every marginal and conditional, so no extraction or normalisation is needed.", "joint_as_margins_done"),
                c("c", "Obtain a marginal by dividing each joint value by the other variable, and obtain a conditional by summing over the conditioning variable.", "operations_reversed"),
                c("d", "A conditional probability equals its joint numerator without division whenever the joint table totals one.", "conditional_without_normalise"),
            ],
            correct="a",
            explanation="Marginalisation removes the other variable by summation or integration. Conditioning renormalises by the conditioning event's marginal.",
            model_answer="Marginal: sum or integrate out the other variable. Conditional: joint divided by conditioning marginal.",
            common_mistake="Treating a joint entry as a finished marginal or conditional without the required operation.",
        ),
        "cp": _item(
            prompt="Closed-book. Joint PMF: P(0,0)=0.10, P(0,1)=0.20, P(1,0)=0.30, P(1,1)=0.40. Which statement is correct?",
            body="Compute one marginal and one conditional probability.",
            choices=[
                c("a", "P(X=1)=0.30+0.40=0.70, and P(Y=1|X=1)=0.40/0.70≈0.571."),
                c("b", "P(X=1)=0.40 because the largest cell in the X=1 row is the marginal.", "largest_cell_as_marginal"),
                c("c", "P(Y=1|X=1)=0.40 because the joint cell is already conditional.", "conditional_without_normalise"),
                c("d", "P(X=1)=0.70 and P(Y=1|X=1)=0.60 because P(Y=1) is the conditional numerator.", "wrong_conditional_numerator"),
            ],
            correct="a",
            explanation="Sum the X=1 row for the marginal, then divide the (1,1) cell by that row total.",
            model_answer="P(X=1)=0.70; P(Y=1|X=1)=0.40/0.70≈0.571.",
            common_mistake="Using a single joint cell as a marginal or failing to normalise a conditional.",
        ),
    },
    "2.2.3-cov-corr-expectation-cs1005.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly links expectation of a function, covariance, and correlation for a joint distribution?",
            body="Select the correct joint-distribution formulas.",
            choices=[
                c("a", "E[g(X,Y)] is the sum or integral of g(x,y) weighted by the joint distribution. Cov(X,Y)=E[XY]-E[X]E[Y], and Corr(X,Y)=Cov(X,Y)/(SD(X)SD(Y))."),
                c("b", "E[g(X,Y)] is found from marginal means alone for every g, so the joint distribution is unnecessary.", "marginals_determine_every_function"),
                c("c", "Correlation equals covariance multiplied by both standard deviations, so it retains measurement units.", "correlation_scaling_reversed"),
                c("d", "Covariance measures all forms of dependence, and zero covariance proves independence for any joint distribution.", "zero_cov_implies_independence"),
            ],
            correct="a",
            explanation="Joint expectation weights g by joint probabilities or density. Covariance captures linear co-movement, while correlation standardises it.",
            model_answer="E[g]=sum or integral of g times joint; Cov=E[XY]-EX EY; Corr=Cov/(SDX SDY).",
            common_mistake="Assuming zero covariance proves independence or reversing correlation standardisation.",
        ),
        "cp": _item(
            prompt="Closed-book. P(0,0)=0.2, P(0,1)=0.3, P(1,0)=0.1, P(1,1)=0.4. Which covariance statement is correct?",
            body="Compute E[X], E[Y], E[XY], and covariance.",
            choices=[
                c("a", "E[X]=0.5, E[Y]=0.7, E[XY]=0.4, so Cov(X,Y)=0.4-(0.5)(0.7)=0.05."),
                c("b", "E[XY]=E[X]E[Y]=0.35 by definition, so covariance must be zero before checking the joint table.", "assume_independence"),
                c("c", "Cov(X,Y)=E[XY]=0.4 because covariance is the expected product without centring.", "uncentred_product_as_covariance"),
                c("d", "E[X]=0.5 and E[Y]=0.7 imply independence, so no E[XY] calculation is needed.", "marginals_imply_independence"),
            ],
            correct="a",
            explanation="Only cell (1,1) contributes to E[XY]. Subtracting the product of the means gives 0.05.",
            model_answer="E[X]=0.5, E[Y]=0.7, E[XY]=0.4, Cov=0.05.",
            common_mistake="Assuming independence from marginals or using E[XY] as covariance without centring.",
        ),
    },
    "2.2.4-linear-combinations-cs1005.json": {
        "ar": _item(
            prompt="Closed-book. Which statement gives the expectation and variance of aX+bY?",
            body="Select the linear-combination formulas.",
            choices=[
                c("a", "E[aX+bY]=aE[X]+bE[Y], and Var(aX+bY)=a²Var(X)+b²Var(Y)+2abCov(X,Y)."),
                c("b", "Var(aX+bY)=aVar(X)+bVar(Y)+2abCov(X,Y), because variance is linear in constants.", "constants_not_squared"),
                c("c", "Var(aX+bY)=a²Var(X)+b²Var(Y) for all X and Y, because covariance never affects a linear combination.", "covariance_always_dropped"),
                c("d", "E[aX+bY]=a²E[X]+b²E[Y], matching the squared coefficients used in variance.", "expectation_coefficients_squared"),
            ],
            correct="a",
            explanation="Expectation is linear. Variance squares scale coefficients and includes the covariance cross-term.",
            model_answer="E=aEX+bEY; Var=a²VarX+b²VarY+2abCov.",
            common_mistake="Dropping covariance without independence or failing to square variance coefficients.",
        ),
        "cp": _item(
            prompt="Closed-book. Var(X)=4, Var(Y)=9, and Cov(X,Y)=2. What is Var(2X-Y)?",
            body="Compute the variance with its covariance term.",
            choices=[
                c("a", "Var(2X-Y)=2²(4)+(-1)²(9)+2(2)(-1)(2)=16+9-8=17."),
                c("b", "Var(2X-Y)=16+9=25 because covariance is omitted whenever the variables differ.", "covariance_dropped"),
                c("c", "Var(2X-Y)=2(4)-9+2(2)(-1)(2)=-9 because variance follows the signs in the linear combination.", "variance_not_squared"),
                c("d", "Var(2X-Y)=16+9+8=33 because covariance always enters with a positive sign.", "cross_term_sign_ignored"),
            ],
            correct="a",
            explanation="With a=2 and b=-1, the cross-term is negative: 2abCov=-8.",
            model_answer="16+9-8=17.",
            common_mistake="Dropping covariance for dependent variables or losing the negative coefficient in the cross-term.",
        ),
    },
    "2.3.1-conditional-expectation-cs1006.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly defines E[Y|X=x]?",
            body="Select the meaning and construction of conditional expectation.",
            choices=[
                c("a", "E[Y|X=x] is the expected value of Y under the conditional distribution of Y given X=x. As x varies it is a function of x, and it need not equal E[Y]."),
                c("b", "E[Y|X=x] is always the unconditional mean E[Y] because expectation removes all conditioning information.", "conditional_equals_unconditional"),
                c("c", "E[Y|X=x] is the joint probability P(X=x,Y=y) evaluated at the largest y.", "joint_cell_as_expectation"),
                c("d", "Conditional expectation is a fixed constant that cannot depend on the value x.", "not_a_function_of_x"),
            ],
            correct="a",
            explanation="Conditional expectation averages Y using its distribution after fixing X=x, so its value can vary with x.",
            model_answer="Expected Y under Y|X=x; a function of x and generally different from E[Y].",
            common_mistake="Replacing the conditional mean with the unconditional mean or a single joint cell.",
        ),
        "cp": _item(
            prompt="Closed-book. For P(0,0)=0.10, P(0,1)=0.20, P(1,0)=0.30, P(1,1)=0.40, what is E[Y|X=1]?",
            body="Compute the conditional mean from the joint PMF.",
            choices=[
                c("a", "Given X=1, P(Y=1|X=1)=0.40/0.70≈0.571, so E[Y|X=1]=0(0.30/0.70)+1(0.40/0.70)≈0.571."),
                c("b", "E[Y|X=1]=E[Y]=0.60 because conditioning does not change an expectation.", "conditional_equals_unconditional"),
                c("c", "E[Y|X=1]=0.40 because the joint cell P(1,1) needs no normalisation.", "joint_cell_as_conditional_mean"),
                c("d", "E[Y|X=1]=0.70 because the marginal P(X=1) is itself the conditional mean of Y.", "conditioning_marginal_as_mean"),
            ],
            correct="a",
            explanation="Normalise the X=1 row, then average Y under that conditional distribution.",
            model_answer="E[Y|X=1]=0.40/(0.30+0.40)≈0.571.",
            common_mistake="Using E[Y] or the unnormalised joint cell instead of the conditional distribution.",
        ),
    },
    "2.3.2-mean-variance-conditioning-cs1006.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly recovers unconditional mean and variance by conditioning on X?",
            body="Select the tower and total-variance identities.",
            choices=[
                c("a", "E[Y]=E[E[Y|X]], and Var(Y)=E[Var(Y|X)]+Var(E[Y|X])."),
                c("b", "E[Y]=E[Y|X] for every realised X, so no outer expectation is required.", "tower_outer_expectation_missing"),
                c("c", "Var(Y)=Var(E[Y|X]) only, because conditional variation disappears after conditioning.", "within_group_variance_dropped"),
                c("d", "Var(Y)=E[Var(Y|X)] only, because variation of conditional means is irrelevant.", "between_group_variance_dropped"),
            ],
            correct="a",
            explanation="The tower property averages conditional means. Total variance adds average within-condition variance and variance between conditional means.",
            model_answer="E[Y]=E(E[Y|X]); Var(Y)=E Var(Y|X)+Var E[Y|X].",
            common_mistake="Stopping at a conditional quantity without the outer expectation or omitting one variance component.",
        ),
        "cp": _item(
            prompt="Closed-book. P(X=1)=0.4, E[Y|X=0]=10, and E[Y|X=1]=20. What is E[Y]?",
            body="Apply the tower property.",
            choices=[
                c("a", "E[Y]=(0.6)(10)+(0.4)(20)=14."),
                c("b", "E[Y]=20 because E[Y|X=1] is the conditional mean for the event explicitly given.", "single_condition_as_unconditional"),
                c("c", "E[Y]=(10+20)/2=15 because conditional means always receive equal weight.", "conditions_equally_weighted"),
                c("d", "E[Y]=E[Y|X], so the answer remains the two-valued function 10 or 20 rather than one unconditional mean.", "outer_expectation_missing"),
            ],
            correct="a",
            explanation="The outer expectation weights each conditional mean by the probability of its condition.",
            model_answer="0.6×10+0.4×20=14.",
            common_mistake="Stopping at E[Y|X] or averaging conditional means without probability weights.",
        ),
    },
    "2.4.1-mgf-cgf-cs1007.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly defines the moment generating function and cumulant generating function?",
            body="Select the MGF and CGF definitions.",
            choices=[
                c("a", "Where it exists around t=0, M_X(t)=E[e^{tX}] and the cumulant generating function is K_X(t)=log M_X(t). Knowing only a mean and variance does not determine that the MGF has been obtained."),
                c("b", "M_X(t)=E[tX] and K_X(t)=e^{M_X(t)}, so both are linear in t.", "definitions_reversed"),
                c("c", "An MGF is simply the pair (E[X],Var(X)); no function of t is required.", "moments_as_mgf"),
                c("d", "Every random variable has a finite MGF for every real t, so existence conditions never matter.", "mgf_always_exists"),
            ],
            correct="a",
            explanation="The MGF is an exponential expectation and the CGF is its logarithm. A few moments are not the full function.",
            model_answer="M(t)=E[e^{tX}]; K(t)=log M(t), where the MGF exists.",
            common_mistake="Treating a stated mean and variance as though they were the MGF.",
        ),
        "cp": _item(
            prompt="Closed-book. If X is Poisson with parameter λ, which MGF and CGF pair is correct?",
            body="Identify the Poisson generating functions.",
            choices=[
                c("a", "M_X(t)=exp(λ(e^t-1)) and K_X(t)=λ(e^t-1)."),
                c("b", "M_X(t)=exp(λt) and K_X(t)=λt because the mean alone determines the full Poisson MGF.", "mean_only_mgf"),
                c("c", "M_X(t)=λ(e^t-1) and K_X(t)=exp(λ(e^t-1)), so the MGF and CGF are reversed.", "mgf_cgf_reversed"),
                c("d", "M_X(t)=λ and K_X(t)=log λ because Poisson mean and variance both equal λ.", "moments_as_generating_functions"),
            ],
            correct="a",
            explanation="Summing E[e^{tX}] under the Poisson PMF gives exp(λ(e^t-1)); taking its logarithm gives the CGF.",
            model_answer="M(t)=exp(λ(e^t-1)); K(t)=λ(e^t-1).",
            common_mistake="Replacing the generating function with the mean and variance or swapping MGF and CGF.",
        ),
    },
    "2.4.2-moment-via-gf-cs1007.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly extracts moments from an MGF?",
            body="Select the derivative and Taylor-coefficient rule.",
            choices=[
                c("a", "If M_X(t) exists around zero, its Taylor expansion has E[X^r] as the coefficient multiplied by r!, equivalently M_X^{(r)}(0)=E[X^r]."),
                c("b", "M_X(0)=E[X], so evaluating the MGF once at zero gives the first moment.", "mgf_value_as_mean"),
                c("c", "M_X'(1)=E[X] for every distribution because moments are evaluated at t=1.", "derivative_at_one"),
                c("d", "Writing M_X(t)=E[e^{tX}] completes moment extraction without differentiation or coefficient matching.", "definition_finishes_extraction"),
            ],
            correct="a",
            explanation="Raw moments are derivatives at zero, or equivalently factorial-scaled Taylor coefficients.",
            model_answer="M^{(r)}(0)=E[X^r]; in particular M'(0)=E[X].",
            common_mistake="Stopping at the MGF definition or evaluating the derivative at the wrong point.",
        ),
        "cp": _item(
            prompt="Closed-book. For Poisson X, M_X(t)=exp(λ(e^t-1)). Which statement correctly obtains E[X]?",
            body="Differentiate the MGF at zero.",
            choices=[
                c("a", "M_X'(t)=λe^t exp(λ(e^t-1)), so M_X'(0)=λ=E[X]."),
                c("b", "M_X(0)=1, so E[X]=1 for every Poisson distribution.", "mgf_value_as_mean"),
                c("c", "M_X'(0)=e^λ because differentiating removes the inner e^t-1 term.", "chain_rule_omitted"),
                c("d", "The formula M_X(t)=E[e^{tX}] already states the mean, so no derivative is needed.", "definition_finishes_extraction"),
            ],
            correct="a",
            explanation="Differentiate using the chain rule and set t=0. The value M(0)=1 is normalisation, not the mean.",
            model_answer="M'(0)=λ.",
            common_mistake="Using M(0) as the mean or writing the MGF without extracting a derivative.",
        ),
    },
    "2.5.1-clt-cs1008.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly states the central limit theorem for a sample mean?",
            body="Select the CLT conditions and target.",
            choices=[
                c("a", "For iid observations with finite mean μ and variance σ², the standardised sample mean approaches N(0,1), so X̄ is approximately N(μ,σ²/n) for large n."),
                c("b", "The CLT makes each individual observation approximately Normal as n grows.", "clt_on_single_observation"),
                c("c", "The CLT applies only when the parent population is already Normal.", "normal_parent_required"),
                c("d", "The sample mean has variance σ² rather than σ²/n because averaging changes only its mean.", "variance_not_reduced"),
            ],
            correct="a",
            explanation="The theorem concerns the distribution of the standardised sum or mean, not individual observations, under stated conditions.",
            model_answer="For iid finite-variance data, X̄≈N(μ,σ²/n) for large n.",
            common_mistake="Applying the CLT to one observation or forgetting the √n reduction in standard deviation.",
        ),
        "cp": _item(
            prompt="Closed-book. Claim sizes are iid with μ=500, σ=200, n=100. Using Φ(2)≈0.977, what is P(X̄>540)?",
            body="Apply and standardise the CLT approximation.",
            choices=[
                c("a", "SD(X̄)=200/√100=20, so z=(540-500)/20=2 and P(X̄>540)≈1-Φ(2)≈0.023."),
                c("b", "SD(X̄)=200, so z=0.2 because sample size does not change spread.", "forget_sqrt_n"),
                c("c", "P(X̄>540)≈0.977 because Φ(2) is the upper-tail probability.", "phi_as_upper_tail"),
                c("d", "P(X̄>540)=0.5 because 540 is above the mean and every above-mean event has probability one half.", "above_mean_half"),
            ],
            correct="a",
            explanation="The standard error is 20 and Φ is a lower-tail CDF, so the required upper tail is about 0.023.",
            model_answer="SE=20, z=2, upper tail≈0.023.",
            common_mistake="Using σ instead of σ/√n or reading Φ(2) as an upper-tail probability.",
        ),
    },
    "2.5.2-simulated-sample-normal-cs1008.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly uses simulation to investigate the Normal approximation for sample means?",
            body="Select the simulation comparison design.",
            choices=[
                c("a", "Repeatedly simulate samples of a fixed size from the parent distribution, record each sample mean, and compare the empirical distribution of means with the relevant Normal approximation across sample sizes."),
                c("b", "Simulate one observation from the parent and compare it with a Normal density; this directly tests the CLT for sample means.", "single_draw_as_clt_test"),
                c("c", "State the CLT without simulating repeated samples, because a theorem statement is the same as an empirical comparison.", "theorem_as_simulation"),
                c("d", "A skewed parent distribution prevents sample means from ever becoming approximately Normal.", "skewness_never_averages"),
            ],
            correct="a",
            explanation="The object to compare is the repeated-sampling distribution of X̄, and changing n reveals convergence behaviour.",
            model_answer="Simulate many samples, collect means, and compare their distribution with Normal across n.",
            common_mistake="Simulating single observations or asserting the theorem without performing the comparison.",
        ),
        "cp": _item(
            prompt="Closed-book. Samples come from an Exponential distribution with mean 1. What should repeated simulations show for X̄ at n=5 versus n=100?",
            body="Compare simulated sampling distributions by sample size.",
            choices=[
                c("a", "At n=5 the distribution of X̄ can remain noticeably right-skewed. At n=100 it should be much closer to Normal, centred near 1 with standard deviation about 1/√100=0.1."),
                c("b", "Both distributions of X̄ must be exactly Exponential with mean 1 because averaging preserves the parent family.", "mean_distribution_equals_parent"),
                c("c", "At n=100 the means remain as skewed as individual Exponential observations because a skewed parent can never yield approximately Normal means.", "skewness_never_averages"),
                c("d", "At n=5 the means are exactly Normal by the CLT, while at n=100 they return to an Exponential shape.", "clt_direction_reversed"),
            ],
            correct="a",
            explanation="The CLT approximation improves as n grows, while the mean stays near 1 and its standard deviation shrinks as 1/√n.",
            model_answer="n=5 may remain skewed; n=100 is closer to N(1,0.1²).",
            common_mistake="Assuming sample means retain the parent shape or that any sample size gives exact Normality.",
        ),
    },
    "2.6.1-random-samples-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly defines a random sample from a population?",
            body="Select the sampling warrant for inference.",
            choices=[
                c("a", "A random sample consists of observations generated from the stated population under a sampling model, commonly iid draws. A collection of n observations is not automatically representative or independent."),
                c("b", "Any n observations form a random sample once their sample mean and variance can be calculated.", "n_observations_as_sample"),
                c("c", "A sample is random exactly when its sample mean equals the population mean.", "mean_match_proves_randomness"),
                c("d", "Sampling design is irrelevant after an estimator formula has been selected.", "estimator_repairs_sampling"),
            ],
            correct="a",
            explanation="Random-sample status comes from the selection mechanism and population relationship, not from sample size or observed summaries.",
            model_answer="Observations must follow the stated sampling model, usually iid draws from the target population.",
            common_mistake="Treating an available data extract as random without examining how it was selected.",
        ),
        "cp": _item(
            prompt="Closed-book. An analyst takes the 40 most recent claims from one client as a sample of the whole motor book. Which statement is correct?",
            body="Assess the random-sample warrant.",
            choices=[
                c("a", "The extract is not a random sample of the whole book: one client's consecutive claims create selection and possible dependence. Having 40 observations does not repair that sampling mechanism."),
                c("b", "It is random because n=40 exceeds a common large-sample threshold.", "large_n_proves_randomness"),
                c("c", "It becomes random if its mean happens to be close to the whole-book mean.", "mean_match_proves_randomness"),
                c("d", "Choosing a t statistic later will correct any client-level selection bias.", "statistic_repairs_selection"),
            ],
            correct="a",
            explanation="Selection from one client does not represent an iid draw from the whole motor portfolio.",
            model_answer="Not random for the whole book; selection and dependence remain despite n=40.",
            common_mistake="Using sample size or a matching mean as evidence that the selection mechanism was random.",
        ),
    },
    "2.6.3-mean-var-sample-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. For an iid sample with population mean μ and variance σ², which statement about X̄ and S² is correct?",
            body="Select the sample-statistic moments.",
            choices=[
                c("a", "E[X̄]=μ, Var(X̄)=σ²/n, and for the usual denominator n-1 sample variance, E[S²]=σ²."),
                c("b", "E[X̄]=μ/n because averaging divides the expected value by n.", "mean_divided_by_n"),
                c("c", "Var(X̄)=σ² because averaging independent observations does not reduce variance.", "variance_not_divided_by_n"),
                c("d", "E[S²]=σ²/n because sample variance estimates the variance of X̄ rather than the population variance.", "sample_variance_targets_mean_variance"),
            ],
            correct="a",
            explanation="The sample mean is unbiased with variance σ²/n, and the usual S² is unbiased for population variance.",
            model_answer="E[X̄]=μ; Var(X̄)=σ²/n; E[S²]=σ².",
            common_mistake="Confusing population variance, variance of the sample mean, and the target of S².",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly summarises the distribution-free moment results for X̄ and unbiased S²?",
            body="Identify what the moment identities do and do not establish.",
            choices=[
                c("a", "E[X̄]=μ, Var(X̄)=σ²/n, and E[S²]=σ². These moment results alone do not establish exact Normal, chi-square, or t distribution laws."),
                c("b", "Var(X̄)=σ²/n proves X̄ is exactly Normal for every parent population and every n.", "moments_imply_normality"),
                c("c", "E[S²]=σ² proves (X̄-μ)/(S/√n) is t distributed without any population assumptions.", "unbiasedness_implies_t"),
                c("d", "E[X̄]=μ means X̄ equals μ in every sample, so sampling variability is zero.", "unbiased_means_exact"),
            ],
            correct="a",
            explanation="Means and variances do not by themselves determine exact sampling distributions.",
            model_answer="State the three moment identities; do not infer exact Normal or t laws from them alone.",
            common_mistake="Treating unbiasedness and variance formulas as sufficient for exact distributional results.",
        ),
    },
    "2.6.4-normal-sample-mean-var-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. For an iid sample from N(μ,σ²), which exact sampling laws are correct?",
            body="Select the Normal mean and sample-variance laws.",
            choices=[
                c("a", "X̄~N(μ,σ²/n), (n-1)S²/σ²~χ²_{n-1}, and X̄ is independent of S²."),
                c("b", "X̄~N(μ,σ²) because taking a mean does not change variance.", "mean_variance_not_scaled"),
                c("c", "S²/σ²~χ²_n because no scaling by n-1 is required.", "chi_square_scaling_missing"),
                c("d", "X̄ and S² are necessarily dependent for Normal samples because both use the same observations.", "normal_independence_denied"),
            ],
            correct="a",
            explanation="Normal sampling gives exact laws for the mean and scaled variance, plus their independence.",
            model_answer="X̄~N(μ,σ²/n); (n-1)S²/σ²~χ²_{n-1}; independence.",
            common_mistake="Missing the n-1 scale or forgetting the special Normal-sample independence result.",
        ),
        "cp": _item(
            prompt="Closed-book. An iid sample of size n comes from N(μ,σ²). Which statement correctly identifies the exact laws without prematurely using t?",
            body="Choose the exact component distributions.",
            choices=[
                c("a", "X̄~N(μ,σ²/n) and (n-1)S²/σ²~χ²_{n-1}, independently. A t law follows only after combining these when σ is unknown."),
                c("b", "X̄~t_{n-1} before standardisation because every Normal sample mean has a t distribution.", "t_too_early"),
                c("c", "(n-1)S²/σ²~N(0,1) because sample variance is an average.", "variance_as_normal"),
                c("d", "The two exact laws finish all t-statistic work even when S has not replaced σ in a standardised mean.", "normal_laws_finish_t"),
            ],
            correct="a",
            explanation="The Normal and chi-square components, with independence, are the ingredients from which the t result is derived.",
            model_answer="State the Normal mean and chi-square variance laws; t comes from their combination.",
            common_mistake="Calling the unstandardised mean t distributed or treating component laws as the finished t statistic.",
        ),
    },
    "2.6.5-t-statistic-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly defines the one-sample t statistic for a Normal population with unknown σ?",
            body="Select the statistic, use case, and degrees of freedom.",
            choices=[
                c("a", "T=(X̄-μ)/(S/√n) has a t distribution with n-1 degrees of freedom when sampling from a Normal population and σ is unknown."),
                c("b", "T=(X̄-μ)/S has t_n because dividing by √n is unnecessary.", "standard_error_missing"),
                c("c", "Replacing σ by S in a z statistic leaves an exact standard Normal distribution.", "z_with_estimated_sigma"),
                c("d", "The t statistic is used only for comparing two sample variances.", "t_as_variance_ratio"),
            ],
            correct="a",
            explanation="Estimating σ with S introduces t uncertainty, and the standard error remains S/√n.",
            model_answer="T=(X̄-μ)/(S/√n)~t_{n-1} for a Normal sample with unknown σ.",
            common_mistake="Using S as though it were known σ in a z law or omitting √n.",
        ),
        "cp": _item(
            prompt=(
                "Closed-book. A Normal sample has unknown population standard deviation. "
                "Which statement gives the correct pivot for μ and correctly refuses "
                "'The t-statistic finished the F variance-ratio LO and Chapter 3'?"
            ),
            body="Identify the t pivot and its boundary.",
            choices=[
                c(
                    "a",
                    "(X̄-μ)/(S/√n)~t_{n-1}. This supports inference for μ, but does not by "
                    "itself give the F law for comparing variances, so The t-statistic "
                    "finished the F variance-ratio LO is false.",
                ),
                c(
                    "b",
                    "(X̄-μ)/(S/√n)~N(0,1) exactly because S and σ are interchangeable.",
                    "z_with_sample_sd",
                ),
                c(
                    "c",
                    "(X̄-μ)/S~t_{n-1} because S is already a standard error.",
                    "sd_as_standard_error",
                ),
                c(
                    "d",
                    "S₁²/S₂²~t_{n-1} because t is the standard law for variance ratios.",
                    "t_for_variance_ratio",
                ),
            ],
            correct="a",
            explanation=(
                "The t pivot uses the estimated standard error and n-1 degrees of freedom. "
                "Variance ratios use F, not t."
            ),
            model_answer=(
                "Use (X̄-μ)/(S/√n)~t_{n-1}; refuse The t-statistic finished the F "
                "variance-ratio LO."
            ),
            common_mistake=(
                "Using a z law with S or treating t as the variance-ratio distribution."
            ),
        ),
    },
    "2.6.6-f-distribution-cs1009.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly describes an F distribution in variance comparison?",
            body="Select the variance-ratio construction.",
            choices=[
                c("a", "An F variable is a ratio of two independent chi-square variables, each divided by its degrees of freedom. It arises from a scaled ratio of independent sample variances from Normal populations and has two degrees of freedom."),
                c("b", "An F variable is the difference of two sample means divided by one pooled standard error.", "f_as_two_sample_t"),
                c("c", "An F distribution has one degrees-of-freedom parameter because numerator and denominator must have equal sample sizes.", "one_df_only"),
                c("d", "Any ratio of sample variances is exactly F distributed even when samples are dependent or populations are non-Normal.", "assumptions_ignored"),
            ],
            correct="a",
            explanation="F is a ratio construction with separate numerator and denominator degrees of freedom under independence and Normal-sample conditions.",
            model_answer="Scaled ratio of independent Normal-sample variances; two degrees of freedom.",
            common_mistake="Using t for a variance ratio or ignoring independence and population assumptions.",
        ),
        "cp": _item(
            prompt="Closed-book. Independent Normal samples of sizes n₁ and n₂ have equal population variances. Which statement is correct?",
            body="Identify the sample-variance ratio law.",
            choices=[
                c("a", "F=S₁²/S₂²~F_{n₁-1,n₂-1} under the equal-variance null, with the numerator and denominator degrees of freedom kept in that order."),
                c("b", "S₁²/S₂²~t_{n₁+n₂-2} because both t and F use sample variances.", "t_for_variance_ratio"),
                c("c", "S₁²/S₂²~F_{n₁,n₂} because estimating sample means does not consume degrees of freedom.", "degrees_of_freedom_not_reduced"),
                c("d", "S₁²/S₂² is standard Normal under equal variances because its expected value is near one.", "ratio_as_normal"),
            ],
            correct="a",
            explanation="Each sample variance contributes a chi-square component with n_i-1 degrees of freedom, producing the stated F ratio.",
            model_answer="S₁²/S₂²~F_{n₁-1,n₂-1} under equal variances.",
            common_mistake="Applying a t law to variance ratios or using n rather than n-1 degrees of freedom.",
        ),
    },
    "4.2.10-fit-interpret-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly describes what is required beyond fitting a GLM in software?",
            body="Select the complete fit-and-interpret procedure.",
            choices=[
                c("a", "Interpret coefficients on the link scale and, where useful, transform them to the response scale. Assess fit measures such as deviance or AIC as warranted, then inspect residuals and diagnostics. Fitting alone is incomplete."),
                c("b", "The software Fit command supplies all actuarial interpretation and validation automatically, so diagnostics are optional.", "fit_without_interpret"),
                c("c", "Only the intercept needs interpretation because factor coefficients have no response-scale meaning.", "intercept_only"),
                c("d", "Fitting a GLM completes Bayesian credibility because both methods can model claim counts.", "glm_finishes_bayesian"),
            ],
            correct="a",
            explanation="A fitted object still requires coefficient interpretation, fit assessment, and diagnostic checking.",
            model_answer="Interpret link-scale coefficients, assess fit, and check residuals and diagnostics; Fit alone is incomplete.",
            common_mistake="Stopping when software returns coefficients or conflating GLM fitting with Bayesian credibility.",
        ),
        "cp": _item(
            prompt="Closed-book. A Poisson log-link GLM reports β̂=0.20 for class High versus baseline. Which statement is correct?",
            body="Interpret the coefficient and assess the fit boundary.",
            choices=[
                c("a", "Holding other terms fixed, the fitted mean for class High is exp(0.20)≈1.22 times the baseline mean. This interpretation still needs fit and diagnostic assessment."),
                c("b", "The fitted mean rises by exactly 0.20 claims because log-link coefficients are additive on the response scale.", "link_scale_as_response_scale"),
                c("c", "The class High fitted mean equals 0.20 because every Poisson coefficient is itself a count mean.", "coefficient_as_mean"),
                c("d", "The coefficient provides a Bayesian credibility premium because a Poisson GLM and a prior-posterior model are the same method.", "glm_finishes_bayesian"),
            ],
            correct="a",
            explanation="Exponentiating a log-link coefficient gives a multiplicative mean ratio. The coefficient does not complete diagnostics or Bayesian work.",
            model_answer="exp(0.20)≈1.22 times baseline, other terms fixed; continue with fit and diagnostic checks.",
            common_mistake="Reading a log-link coefficient additively on the count scale or treating Fit as complete analysis.",
        ),
    },
    "5.1.9-bayes-vs-eb-cs1003.json": {
        "ar": _item(
            prompt="Closed-book. Which statement correctly distinguishes fully Bayesian credibility from Empirical Bayes?",
            body="Select the structural-assumption contrast.",
            choices=[
                c("a", "A fully Bayesian approach specifies a prior model for structural parameters. Empirical Bayes estimates structural parameters from collective data and plugs them into the analysis. These different inputs can produce different premiums."),
                c("b", "Fully Bayesian and Empirical Bayes are identical methods under different names, so their premiums must agree.", "same_method"),
                c("c", "Empirical Bayes specifies all structural parameters before observing data, while fully Bayesian analysis estimates them only from the collective.", "assumptions_reversed"),
                c("d", "Any premium difference is caused only by software rounding because the methods make identical structural assumptions.", "software_only_difference"),
            ],
            correct="a",
            explanation="The key distinction is specified prior structure versus structure estimated from collective experience.",
            model_answer="Bayes specifies prior structure; EB estimates structural parameters from collective data; premiums may differ.",
            common_mistake="Calling the approaches identical or reversing how structural information enters.",
        ),
        "cp": _item(
            prompt="Closed-book. Which statement correctly identifies the assumption difference between fully Bayesian credibility and Empirical Bayes?",
            body="Contrast the methods without overextending the result.",
            choices=[
                c("a", "Fully Bayesian credibility specifies structural or prior parameters within a prior model. Empirical Bayes estimates them from observed collective data. This contrast does not itself complete posterior, interval, or premium calculations."),
                c("b", "The methods are identical because both can return a credibility premium.", "same_method"),
                c("c", "Once the contrast is stated, all posterior distributions, estimators, intervals, and premiums have also been calculated.", "contrast_finishes_all"),
                c("d", "Empirical Bayes requires a fully specified prior before data, while fully Bayesian credibility uses only collective estimates.", "assumptions_reversed"),
            ],
            correct="a",
            explanation="The methods differ in how structural knowledge is supplied. Naming that difference is not a substitute for subsequent calculations.",
            model_answer="Specified prior structure versus estimated structural parameters from collective data.",
            common_mistake="Treating the methods as identical or assuming the conceptual contrast completes all Bayesian foundations.",
        ),
    },
}

STEM_TO_INVENTORY: dict[str, str] = {
    inv_key.removesuffix(".json"): inv_key for inv_key in CONVERSIONS
}
INVENTORY_TO_STEM: dict[str, str] = {v: k for k, v in STEM_TO_INVENTORY.items()}

CAMPAIGN_TWINS: dict[str, str] = {
    "2.1.6-software-generation-cs1004.json": "campaign-gamma-cs1004/packages/2.1.6-software-generation-cs1004.json",
    "2.2.1-marginal-conditional-cs1005.json": "campaign-epsilon-cs1005/packages/2.2.1-marginal-conditional-cs1005.json",
    "2.2.3-cov-corr-expectation-cs1005.json": "campaign-epsilon-cs1005/packages/2.2.3-cov-corr-expectation-cs1005.json",
    "2.2.4-linear-combinations-cs1005.json": "campaign-epsilon-cs1005/packages/2.2.4-linear-combinations-cs1005.json",
    "2.3.1-conditional-expectation-cs1006.json": "campaign-zeta-cs1006/packages/2.3.1-conditional-expectation-cs1006.json",
    "2.3.2-mean-variance-conditioning-cs1006.json": "campaign-zeta-cs1006/packages/2.3.2-mean-variance-conditioning-cs1006.json",
    "2.4.1-mgf-cgf-cs1007.json": "campaign-eta-cs1007/packages/2.4.1-mgf-cgf-cs1007.json",
    "2.4.2-moment-via-gf-cs1007.json": "campaign-eta-cs1007/packages/2.4.2-moment-via-gf-cs1007.json",
    "2.5.1-clt-cs1008.json": "campaign-theta-cs1008/packages/2.5.1-clt-cs1008.json",
    "2.5.2-simulated-sample-normal-cs1008.json": "campaign-theta-cs1008/packages/2.5.2-simulated-sample-normal-cs1008.json",
    "2.6.1-random-samples-cs1009.json": "campaign-iota-cs1009/packages/2.6.1-random-samples-cs1009.json",
    "2.6.3-mean-var-sample-cs1009.json": "campaign-iota-cs1009/packages/2.6.3-mean-var-sample-cs1009.json",
    "2.6.4-normal-sample-mean-var-cs1009.json": "campaign-iota-cs1009/packages/2.6.4-normal-sample-mean-var-cs1009.json",
    "2.6.5-t-statistic-cs1009.json": "campaign-iota-cs1009/packages/2.6.5-t-statistic-cs1009.json",
    "2.6.6-f-distribution-cs1009.json": "campaign-iota-cs1009/packages/2.6.6-f-distribution-cs1009.json",
    "4.2.10-fit-interpret-cs1003.json": "campaign-delta-cs1003/packages/4.2.10-fit-interpret-cs1003.json",
    "5.1.9-bayes-vs-eb-cs1003.json": "campaign-delta-cs1003/packages/5.1.9-bayes-vs-eb-cs1003.json",
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace in-scope Active Recall and Checkpoint checks with Batch 5 MCQs."""
    inv_key = STEM_TO_INVENTORY.get(stem)
    if not inv_key:
        return pkg
    parts = CONVERSIONS[inv_key]
    updated_checks: list[dict[str, Any]] = []
    for check in pkg.get("knowledge_checks") or []:
        updated = dict(check)
        if check.get("kind") == "active_recall":
            updated.update(parts["ar"])
        elif check.get("kind") == "checkpoint":
            updated.update(parts["cp"])
        updated_checks.append(updated)
    pkg["knowledge_checks"] = updated_checks
    return pkg


def sync_catalogue_twins(root: Path | None = None) -> int:
    """Patch catalogue twins with Batch 5 MCQ knowledge checks."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key in CONVERSIONS:
        path = catalogue_dir / inv_key
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def sync_campaign_twins(root: Path | None = None) -> int:
    """Patch campaign twins with Batch 5 MCQ knowledge checks."""
    repo = root or Path(__file__).resolve().parents[1]
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        path = campaign_dir / rel_path
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    """Scan synced checks for structural and student-facing writing defects."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    duplicate = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
    meta_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bcampaign\b",
            r"\bjourney\b",
            r"Batch \d",
            r"Wave \d",
            r"Isolated Golden Day",
            r"spine claims",
        )
    ]
    defects: list[str] = []
    paths = [
        path
        for inv_key in CONVERSIONS
        for path in (
            catalogue_dir / inv_key,
            campaign_dir / CAMPAIGN_TWINS[inv_key],
        )
    ]
    for path in paths:
        if not path.exists():
            defects.append(f"MISSING: {path}")
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        checks = {
            check.get("kind"): check for check in pkg.get("knowledge_checks") or []
        }
        for kind in ("active_recall", "checkpoint"):
            check = checks.get(kind)
            if check is None:
                defects.append(f"{path.name} {kind}: missing")
                continue
            if check.get("response_type") != "mcq":
                defects.append(f"{path.name} {kind}: not mcq")
            choices = check.get("choices") or []
            if [choice.get("id") for choice in choices] != ["a", "b", "c", "d"]:
                defects.append(f"{path.name} {kind}: bad choice ids")
            if len(choices) != 4:
                defects.append(f"{path.name} {kind}: not 4 choices")
            if check.get("correct_choice_id") not in {"a", "b", "c", "d"}:
                defects.append(f"{path.name} {kind}: bad correct_choice_id")
            for field in ("explanation", "model_answer", "common_mistake", "body"):
                if not check.get(field):
                    defects.append(f"{path.name} {kind}: missing {field}")
            if not str(check.get("prompt", "")).startswith("Closed-book."):
                defects.append(f"{path.name} {kind}: prompt is not closed-book")
            for choice in choices:
                tag = choice.get("misconception_tag")
                if choice.get("id") == check.get("correct_choice_id") and tag:
                    defects.append(f"{path.name} {kind}: correct choice has tag")
                if choice.get("id") != check.get("correct_choice_id") and not tag:
                    defects.append(f"{path.name} {kind}: distractor missing tag")
            blob = json.dumps(check, ensure_ascii=False)
            if "\u2014" in blob:
                defects.append(f"{path.name} {kind}: em dash found")
            for match in duplicate.finditer(blob):
                defects.append(
                    f"{path.name} {kind}: duplicate word '{match.group(1)}'"
                )
            for pattern in meta_patterns:
                if pattern.search(blob):
                    defects.append(
                        f"{path.name} {kind}: meta language '{pattern.pattern}'"
                    )
    return defects


if __name__ == "__main__":
    campaign_count = sync_campaign_twins()
    catalogue_count = sync_catalogue_twins()
    scan = mechanical_defect_scan()
    print(
        f"Synced {campaign_count} campaign + {catalogue_count} catalogue twins."
    )
    if scan:
        print("DEFECTS:")
        for defect in scan:
            print(" ", defect)
    else:
        print("Mechanical defect scan: PASS (0 issues)")

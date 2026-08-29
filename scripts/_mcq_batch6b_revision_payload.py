#!/usr/bin/env python3
# ruff: noqa: E501
"""MCQ conversion payload for 19 CS1 revision packages.

Applies deterministic four-option MCQ rewrites to active-recall and checkpoint
items, then synchronises catalogue and educational-campaign twins.
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


def _mcq(
    prompt: str,
    body: str,
    choices: list[Choice],
    explanation: str,
    model_answer: str,
    common_mistake: str,
) -> dict[str, Any]:
    return _item(
        prompt=prompt,
        body=body,
        choices=choices,
        correct="a",
        explanation=explanation,
        model_answer=model_answer,
        common_mistake=common_mistake,
    )


CONVERSIONS: dict[str, dict[str, Any]] = {
    "revision-purpose-eda-ep001.json": {
        "ar": _mcq(
            "Closed-book. Which statement correctly names the three primary aims of CS1 data analysis with distinct actuarial examples and one reproducibility element?",
            "Select the complete aims-and-examples statement.",
            [
                c("a", "Descriptive: summarise claim sizes in a portfolio year. Inferential: estimate mean claim severity for a population of similar risks. Predictive: forecast next year's claim count for pricing. Reproducibility needs something concrete such as versioned data and a scripted analysis path."),
                c("b", "The three aims are plotting, computing means, and using software. Reproducibility means saving the final chart.", "tools_as_aims"),
                c("c", "All three aims mean inspecting observed claims, so one sample summary covers description, population inference, and future prediction.", "aims_collapsed"),
                c("d", "Descriptive analysis forecasts future claims, inferential analysis reports only the observed sample, and predictive analysis estimates a fixed population parameter.", "aims_swapped"),
            ],
            "CS1 distinguishes descriptive, inferential, and predictive aims. Reproducibility requires a concrete repeatable analysis path.",
            "Describe the observed portfolio, infer a population quantity, and predict a future outcome, with versioned data and scripted analysis.",
            "Listing tools instead of aims, collapsing the aims, or swapping their roles.",
        ),
        "cps": [
            _mcq(
                "Closed-book. Claim amounts are strongly right-skewed and contain several large observations. Which descriptive analysis is most defensible?",
                "Select the best summary and visualisation.",
                [
                    c("a", "Report the median and interquartile range, use a histogram or boxplot to show skew and extremes, and investigate large claims rather than deleting them automatically."),
                    c("b", "Report only the mean because it is the standard summary for every numerical variable.", "mean_by_habit"),
                    c("c", "Use a pie chart because it displays the shape of continuous claim amounts more clearly than a histogram.", "pie_preferred"),
                    c("d", "Delete all claims above the upper quartile before calculating any summary.", "automatic_outlier_deletion"),
                ],
                "Robust summaries and a distributional plot reveal centre, spread, skewness, and possible outliers without assuming errors.",
                "Use the median, IQR, and a histogram or boxplot, then investigate the large claims.",
                "Using a mean-only summary or an unsuitable pie chart for skewed continuous data.",
            ),
            _mcq(
                "Closed-book. Two continuous variables have outliers and a strong monotone but nonlinear relationship. Which conclusion is justified?",
                "Select the best association statement.",
                [
                    c("a", "Spearman's rank correlation or Kendall's tau can measure the monotone association and reduce sensitivity to extreme magnitudes, but neither establishes causation."),
                    c("b", "Pearson correlation must equal 1 because every monotone relationship is perfectly linear.", "pearson_monotonicity_confusion"),
                    c("c", "Kendall's tau proves that changing one variable causes the other to change.", "association_as_causation"),
                    c("d", "No correlation measure can describe a nonlinear monotone relationship.", "linearity_required_for_rank_correlation"),
                ],
                "Rank correlations measure monotone association without requiring linearity. Association alone does not establish causation.",
                "Use Spearman's rho or Kendall's tau and avoid a causal claim.",
                "Using Pearson automatically or interpreting rank association as causation.",
            ),
        ],
    },
    "revision-pca-distributions-cs1002.json": {
        "ar": _mcq(
            "Closed-book. Which statement correctly describes principal component analysis?",
            "Select the most accurate statement.",
            [
                c("a", "PCA forms orthogonal linear combinations of variables, ordered by explained sample variance. It can reduce dimension but does not by itself establish causal relationships."),
                c("b", "PCA identifies which observed variables causally determine a response.", "pca_as_causal_model"),
                c("c", "PCA retains every original variable unchanged while reducing dimension.", "no_transformation_misconception"),
                c("d", "PCA maximises the variance of each original variable separately.", "component_definition_error"),
            ],
            "Principal components are orthogonal variance-ordered linear combinations, useful for dimension reduction rather than causal inference.",
            "PCA summarises correlated variation with fewer orthogonal components and does not establish causation.",
            "Treating PCA as a causal or supervised modelling method.",
        ),
        "cps": [
            _mcq(
                "Closed-book. A manufacturer independently inspects 40 items, each having the same probability p of being defective. What is the distribution of the number of defective items?",
                "Select the correct distribution.",
                [
                    c("a", "Binomial with parameters 40 and p."),
                    c("b", "Hypergeometric, because the number of inspections is fixed.", "without_replacement_confusion"),
                    c("c", "Poisson with parameter p, regardless of the number inspected.", "poisson_parameter_error"),
                    c("d", "Geometric with parameter p, because each item is defective or not defective.", "count_vs_waiting_time"),
                ],
                "A fixed number of independent Bernoulli trials with constant success probability produces a binomial count.",
                "The count is Binomial(40, p).",
                "Choosing hypergeometric without finite-population sampling without replacement.",
            ),
            _mcq(
                "Closed-book. Claims arrive according to a Poisson process with constant rate lambda. What is the distribution of the waiting time until the next claim?",
                "Select the correct distribution.",
                [
                    c("a", "Exponential with rate lambda."),
                    c("b", "Normal with mean 1/lambda because waiting times are continuous.", "normal_by_default"),
                    c("c", "Poisson with mean lambda because the arrivals form a Poisson process.", "count_time_confusion"),
                    c("d", "Uniform on the next unit interval because the hazard is constant.", "constant_hazard_uniform_confusion"),
                ],
                "Poisson-process interarrival times are exponentially distributed with constant hazard lambda.",
                "The waiting time is Exponential(lambda), with mean 1/lambda.",
                "Confusing the Poisson count with the exponential interarrival time.",
            ),
            _mcq(
                "Closed-book. Two continuous variables have outliers and a strong monotone but nonlinear relationship. Which conclusion is justified?",
                "Select the best association statement.",
                [
                    c("a", "Spearman's rank correlation or Kendall's tau can measure the monotone association, but neither establishes causation."),
                    c("b", "Pearson correlation measures every monotone relationship exactly.", "pearson_monotonicity_confusion"),
                    c("c", "A significant rank correlation proves that one variable causes the other.", "association_as_causation"),
                    c("d", "Correlation is necessarily zero whenever a relationship is nonlinear.", "nonlinear_zero_correlation"),
                ],
                "Rank measures capture monotone association, while causation requires additional design or evidence.",
                "Use Spearman's rho or Kendall's tau and avoid a causal interpretation.",
                "Assuming nonlinear association cannot be measured or that association proves causation.",
            ),
        ],
    },
    "revision-linear-models-cs1003.json": {
        "ar": _mcq(
            "Closed-book. In a multiple linear model Y = X beta + epsilon, which statement correctly describes ordinary least squares?",
            "Select the correct statement.",
            [
                c("a", "Y is the response, columns of X are explanatory variables, and OLS chooses beta to minimise the sum of squared residuals."),
                c("b", "OLS chooses Y to minimise the sum of squared fitted values.", "ols_objective_confusion"),
                c("c", "Every explanatory variable must be independent of every other explanatory variable.", "predictor_independence_requirement"),
                c("d", "Multiple regression fits a separate response for each predictor.", "multiple_regression_role_confusion"),
            ],
            "OLS estimates coefficients by minimising squared differences between observed and fitted responses.",
            "Y is the response, X contains predictors, and OLS minimises residual sum of squares.",
            "Confusing variable roles or minimising fitted values rather than residuals.",
        ),
        "cp": _mcq(
            "Closed-book. An OLS fit has residuals whose spread increases markedly with fitted values. What is the best interpretation?",
            "Select the warranted conclusion.",
            [
                c("a", "The constant-variance assumption is doubtful, so usual standard errors and inference may be unreliable without an appropriate remedy."),
                c("b", "The pattern proves the fitted mean relationship is exactly correct.", "diagnostic_as_confirmation"),
                c("c", "The pattern is harmless whenever R-squared is high.", "r_squared_overrides_diagnostics"),
                c("d", "Always remove observations with the largest residuals.", "automatic_residual_deletion"),
            ],
            "A funnel-shaped residual plot indicates heteroscedasticity, which affects usual OLS inference.",
            "Investigate non-constant variance and consider a justified transformation, variance model, or robust inference.",
            "Treating high R-squared as a substitute for residual diagnostics.",
        ),
    },
    "revision-regression-glm-cs1003.json": {
        "ar": _mcq(
            "Closed-book. What does the sequence Family to eta to link represent in a generalised linear model?",
            "Select the correct interpretation.",
            [
                c("a", "The response family specifies mean-variance behaviour, eta = X beta is the linear predictor, and the link satisfies g(mu) = eta."),
                c("b", "The family determines X, while the link transforms each predictor into response variance.", "glm_component_roles"),
                c("c", "Eta is the observed response and the link is its density.", "eta_response_confusion"),
                c("d", "The link requires the response itself to be Normal.", "normality_requirement"),
            ],
            "A GLM combines a response distribution, linear predictor, and link connecting the response mean to that predictor.",
            "Choose a family, form eta = X beta, and connect mu through g(mu) = eta.",
            "Confusing the link with a transformation of observations or predictors.",
        ),
        "cp": _mcq(
            "Closed-book. For a Poisson GLM, which statement about the canonical link and deviance is correct?",
            "Select the correct statement.",
            [
                c("a", "The canonical link is log(mu) = eta, and deviance compares fitted and saturated models through likelihoods."),
                c("b", "The canonical link is mu squared = eta, and deviance is residual sum of squares in every GLM.", "canonical_link_and_deviance_error"),
                c("c", "The identity link is the only valid Poisson link because counts are untransformed.", "identity_only_confusion"),
                c("d", "Small deviance proves every distributional and independence assumption.", "deviance_proves_assumptions"),
            ],
            "The Poisson canonical link is logarithmic, and GLM deviance is likelihood-based.",
            "Use log(mu) = eta and interpret deviance as a likelihood comparison with the saturated fit.",
            "Treating deviance as ordinary residual sum of squares or complete model validation.",
        ),
    },
    "revision-midspine-cs1003.json": {
        "ar": _mcq(
            "Closed-book. Which statement correctly distinguishes fully Bayesian inference from empirical Bayes inference?",
            "Select the best distinction.",
            [
                c("a", "A fully Bayesian analysis gives prior distributions to hyperparameters, while empirical Bayes estimates some prior hyperparameters from observed data."),
                c("b", "Empirical Bayes never uses a prior distribution.", "eb_no_prior"),
                c("c", "Fully Bayesian inference estimates every prior parameter by maximum likelihood from the same data.", "full_bayes_as_eb"),
                c("d", "The approaches always produce identical posterior uncertainty.", "uncertainty_equivalence"),
            ],
            "Empirical Bayes estimates prior-level quantities from data, while a full Bayesian model represents their uncertainty probabilistically.",
            "Empirical Bayes plugs in estimated hyperparameters; full Bayes models their uncertainty.",
            "Claiming empirical Bayes has no prior or fully propagates plug-in uncertainty.",
        ),
        "cp": _mcq(
            "Closed-book. If X given theta is Binomial(n, theta) and theta has a Beta(alpha, beta) prior, what is the posterior after observing X = x?",
            "Select the correct posterior.",
            [
                c("a", "Beta(alpha + x, beta + n - x)."),
                c("b", "Beta(alpha + n, beta + x).", "beta_binomial_parameter_update"),
                c("c", "Binomial(n + alpha + beta, theta).", "posterior_family_confusion"),
                c("d", "Beta(alpha + x, beta + x).", "failures_omitted"),
            ],
            "Beta-binomial conjugacy adds successes to alpha and failures to beta.",
            "The posterior is Beta(alpha + x, beta + n - x).",
            "Adding successes to both parameters and ignoring failures.",
        ),
    },
    "revision-distributions-generation-cs1004.json": {
        "ar": _mcq(
            "Closed-book. Let F be a continuous strictly increasing distribution function and U be Uniform(0, 1). Which variable has distribution function F?",
            "Select the inverse-transform construction.",
            [
                c("a", "X = F inverse(U)."),
                c("b", "X = F(U).", "cdf_vs_inverse"),
                c("c", "X = 1 minus U for every F.", "uniform_only_transform"),
                c("d", "X = log(U) regardless of the support of F.", "unsupported_fixed_transform"),
            ],
            "Inverse transform maps a uniform probability through the target quantile function.",
            "Generate U uniformly and set X = F inverse(U).",
            "Applying the distribution function rather than its inverse.",
        ),
        "cp": _mcq(
            "Closed-book. To generate an Exponential distribution with rate lambda from U distributed Uniform(0, 1), which formula is valid?",
            "Select the valid construction.",
            [
                c("a", "X = -log(1 - U) / lambda, equivalently -log(U) / lambda."),
                c("b", "X = log(U) / lambda.", "negative_support_error"),
                c("c", "X = lambda U.", "uniform_scaling_confusion"),
                c("d", "X = -lambda log(U).", "rate_scale_confusion"),
            ],
            "The exponential quantile is -log(1-u)/lambda, and 1-U is also uniform.",
            "Use X = -log(1-U)/lambda and verify non-negative support.",
            "Multiplying by the rate instead of dividing by it.",
        ),
    },
    "revision-joint-distributions-cs1005.json": {
        "ar": _mcq(
            "Closed-book. Which condition establishes independence of discrete random variables X and Y?",
            "Select the correct factorisation.",
            [
                c("a", "pX,Y(x, y) = pX(x)pY(y) for every pair in the joint support."),
                c("b", "Cov(X, Y) = 0 in every case.", "uncorrelated_as_independent"),
                c("c", "pX,Y(x, y) = pX(x) + pY(y).", "joint_addition_error"),
                c("d", "E[X] = E[Y].", "equal_means_as_independence"),
            ],
            "Independence requires joint factorisation everywhere; zero covariance is generally insufficient.",
            "Verify pX,Y(x,y) = pX(x)pY(y) for all possible pairs.",
            "Equating zero covariance with independence.",
        ),
        "cp": _mcq(
            "Closed-book. For random variables X and Y with finite variances, what is Var(aX + bY)?",
            "Select the correct expression.",
            [
                c("a", "a squared Var(X) + b squared Var(Y) + 2ab Cov(X, Y)."),
                c("b", "a Var(X) + b Var(Y).", "variance_scaling_error"),
                c("c", "a squared Var(X) + b squared Var(Y) in all cases.", "covariance_omitted"),
                c("d", "a squared Var(X) + b squared Var(Y) + ab Cov(X, Y).", "covariance_factor_error"),
            ],
            "Variance scales quadratically, and the cross-product contributes twice the covariance term.",
            "Var(aX+bY) = a²Var(X) + b²Var(Y) + 2abCov(X,Y).",
            "Omitting covariance without establishing zero covariance.",
        ),
    },
    "revision-conditional-expectations-cs1006.json": {
        "ar": _mcq(
            "Closed-book. Which identity is the law of total expectation?",
            "Select the correct identity.",
            [
                c("a", "E[Y] = E[E[Y given X]]."),
                c("b", "E[Y] = E[Y given X] for every realised X.", "conditional_as_constant"),
                c("c", "E[Y] = Var(E[Y given X]).", "mean_variance_confusion"),
                c("d", "E[Y given X] = E[X given Y] in general.", "conditional_symmetry"),
            ],
            "Averaging the conditional mean over X recovers the unconditional mean.",
            "Compute E[Y given X], then average over X.",
            "Treating conditional expectation as the unconditional constant.",
        ),
        "cp": _mcq(
            "Closed-book. Which formula correctly decomposes Var(Y) by conditioning on X?",
            "Select the correct formula.",
            [
                c("a", "Var(Y) = E[Var(Y given X)] + Var(E[Y given X])."),
                c("b", "Var(Y) = Var(Y given X) + Var(X).", "conditional_variance_addition"),
                c("c", "Var(Y) = E[Var(Y given X)] only.", "between_group_variance_omitted"),
                c("d", "Var(Y) = Var(E[Y given X]) only.", "within_group_variance_omitted"),
            ],
            "Total variance combines expected within-condition variance and variance between conditional means.",
            "Use Var(Y) = E[Var(Y|X)] + Var(E[Y|X]).",
            "Omitting either the within-condition or between-condition term.",
        ),
    },
    "revision-generating-functions-cs1007.json": {
        "ar": _mcq(
            "Closed-book. Which statement correctly defines the moment generating function and cumulant generating function of X?",
            "Select the correct statement.",
            [
                c("a", "M_X(t) = E[exp(tX)] where finite, and K_X(t) = log M_X(t)."),
                c("b", "M_X(t) = E[tX], and K_X(t) is its derivative.", "mgf_definition_error"),
                c("c", "M_X(t) = P(X less than or equal to t), and K_X(t) is the survival function.", "mgf_cdf_confusion"),
                c("d", "K_X(t) = exp(M_X(t)).", "cgf_transform_error"),
            ],
            "The MGF is E[exp(tX)], and its logarithm is the CGF.",
            "M_X(t)=E[e^(tX)] and K_X(t)=log M_X(t), where the MGF exists.",
            "Confusing the MGF with a distribution function or the CGF transformation.",
        ),
        "cp": _mcq(
            "Closed-book. If the MGF of X exists around zero, how are its first two raw moments obtained?",
            "Select the correct derivative statement.",
            [
                c("a", "E[X] = M_X'(0) and E[X squared] = M_X''(0)."),
                c("b", "E[X] = M_X(0) and E[X squared] = M_X'(0).", "derivative_order_error"),
                c("c", "Var(X) = M_X''(0) in every case.", "raw_second_moment_as_variance"),
                c("d", "E[X squared] = squared M_X'(0).", "second_moment_as_squared_mean"),
            ],
            "The nth MGF derivative at zero gives the nth raw moment; variance subtracts the squared mean.",
            "M_X'(0)=E[X] and M_X''(0)=E[X²].",
            "Calling the second raw moment the variance.",
        ),
    },
    "revision-central-limit-theorem-cs1008.json": {
        "ar": _mcq(
            "Closed-book. Let X1, ..., Xn be iid with finite mean mu and finite positive variance sigma squared. What does the central limit theorem state?",
            "Select the correct limiting statement.",
            [
                c("a", "sqrt(n)(sample mean minus mu)/sigma converges in distribution to a standard Normal variable as n grows."),
                c("b", "The sample mean equals mu with probability 1 for every finite n.", "clt_as_exact_equality"),
                c("c", "Each Xi becomes Normally distributed as n grows.", "observations_become_normal"),
                c("d", "The unstandardised sum converges to standard Normal without centring or scaling.", "missing_standardisation"),
            ],
            "The CLT concerns the centred and scaled sample mean or sum.",
            "The standardised sample mean converges in distribution to N(0,1).",
            "Applying the limit to observations or omitting standardisation.",
        ),
        "cp": _mcq(
            "Closed-book. The underlying observations are highly skewed but have finite variance. Which statement about their sample mean is justified?",
            "Select the correct statement.",
            [
                c("a", "For sufficiently large n, the standardised mean may be approximated by standard Normal, but the approximation is not generally exact at finite n."),
                c("b", "The sample mean is exactly Normal for every n because a mean was calculated.", "every_mean_exact_normal"),
                c("c", "The CLT cannot apply to any skewed distribution.", "skewness_blocks_clt"),
                c("d", "Increasing n makes the original observations less skewed.", "sample_vs_observation_confusion"),
            ],
            "Finite-variance skewed data can satisfy the CLT, although strong skewness may require a larger sample.",
            "Use the Normal approximation cautiously for sufficiently large n.",
            "Assuming every sample mean is exactly Normal.",
        ),
    },
    "revision-sampling-distributions-cs1009.json": {
        "ar": _mcq(
            "Closed-book. What is the sampling distribution of the sample mean?",
            "Select the correct definition.",
            [
                c("a", "It is the probability distribution of values the sample mean would take over repeated random samples of the same size."),
                c("b", "It is the single numerical sample mean observed in the available data.", "statistic_vs_distribution"),
                c("c", "It is the empirical distribution of observations within one sample.", "sample_distribution_confusion"),
                c("d", "It is always standard Normal, whatever the population and sample size.", "universal_normality"),
            ],
            "A sampling distribution describes repeated-sampling behaviour of a statistic.",
            "It is the distribution of the sample mean across repeated samples of fixed size.",
            "Confusing a realised statistic with its sampling distribution.",
        ),
        "cp": _mcq(
            "Closed-book. A random sample of size n comes from a Normal population with unknown variance. Which pivot is used for inference about the mean?",
            "Select the correct distributional result.",
            [
                c("a", "(sample mean minus mu)/(S divided by sqrt(n)) has a t distribution with n - 1 degrees of freedom."),
                c("b", "(sample mean minus mu)/S has a standard Normal distribution.", "missing_standard_error_and_t"),
                c("c", "(sample mean minus mu)/(S divided by sqrt(n)) has a chi-squared distribution.", "pivot_distribution_confusion"),
                c("d", "The sample mean itself has a t distribution with n degrees of freedom.", "unstandardised_mean_t"),
            ],
            "Estimating the unknown Normal population variance gives a t pivot with n - 1 degrees of freedom.",
            "Use T = (Xbar-mu)/(S/sqrt(n)), which follows t_(n-1).",
            "Using a standard Normal pivot when variance is estimated from the sample.",
        ),
    },
    "revision-estimators-cs1010.json": {
        "ar": _mcq(
            "Closed-book. Which statement correctly distinguishes method of moments from maximum likelihood estimation?",
            "Select the correct distinction.",
            [
                c("a", "Method of moments equates sample and model moments, while maximum likelihood maximises the likelihood of observed data."),
                c("b", "Both methods always produce the same estimator.", "mom_mle_equivalence"),
                c("c", "Method of moments maximises the probability of the observed sample.", "mom_as_mle"),
                c("d", "Maximum likelihood uses only the first population moment.", "mle_as_first_moment"),
            ],
            "The methods use different estimating principles and need not agree.",
            "MoM matches moments; MLE maximises the observed-data likelihood.",
            "Assuming the methods are identical because they coincide in some models.",
        ),
        "cp": _mcq(
            "Closed-book. Which identity correctly expresses the mean squared error of an estimator T for parameter theta?",
            "Select the correct identity.",
            [
                c("a", "MSE(T) = Var(T) + Bias(T) squared."),
                c("b", "MSE(T) = Var(T) + Bias(T).", "unsquared_bias"),
                c("c", "MSE(T) = Bias(T) squared only.", "variance_omitted"),
                c("d", "MSE(T) = Var(T) for every estimator.", "bias_omitted"),
            ],
            "MSE combines variance and squared bias; unbiasedness alone does not ensure minimum MSE.",
            "MSE equals variance plus squared bias.",
            "Treating unbiasedness as sufficient for efficiency.",
        ),
    },
    "revision-confidence-intervals-cs1011.json": {
        "ar": _mcq(
            "Closed-book. After a frequentist 95 percent confidence interval for fixed parameter theta has been calculated, which interpretation is correct?",
            "Select the correct interpretation.",
            [
                c("a", "The construction procedure covers theta in 95 percent of repeated samples under the model."),
                c("b", "Given these data, theta has probability 0.95 of lying in this interval.", "frequentist_parameter_probability"),
                c("c", "Ninety-five percent of sample values must lie inside the interval.", "parameter_vs_observations"),
                c("d", "There is a 95 percent probability that the statistical model is true.", "confidence_as_model_probability"),
            ],
            "The parameter is fixed; coverage refers to the long-run behaviour of the random interval procedure.",
            "A 95 percent confidence procedure has 95 percent repeated-sampling coverage under its assumptions.",
            "Assigning posterior probability to a fixed parameter.",
        ),
        "cp": _mcq(
            "Closed-book. In a Normal linear model, how does a prediction interval for one future response generally compare with a confidence interval for the mean response at the same predictor value?",
            "Select the correct comparison.",
            [
                c("a", "The prediction interval is wider because it includes mean-estimation uncertainty and the future observation's random variation."),
                c("b", "The prediction interval is narrower because only one future value is considered.", "single_value_narrower"),
                c("c", "The intervals are always identical.", "mean_prediction_equivalence"),
                c("d", "The confidence interval includes future observation noise, but the prediction interval does not.", "uncertainty_components_reversed"),
            ],
            "Prediction includes irreducible observation-level variance in addition to mean uncertainty.",
            "The prediction interval is wider because it covers a new response.",
            "Using a mean-response confidence interval to predict one future observation.",
        ),
    },
    "revision-hypothesis-testing-cs1012.json": {
        "ar": _mcq(
            "Closed-book. What is a p-value for an observed test statistic?",
            "Select the correct definition.",
            [
                c("a", "Assuming the null hypothesis, it is the probability of a test statistic at least as incompatible with the null as the observed value."),
                c("b", "It is the probability that the null hypothesis is true after observing data.", "p_value_as_null_probability"),
                c("c", "It is the probability that the alternative hypothesis is false.", "p_value_as_alternative_probability"),
                c("d", "It is the probability that the same sample result occurs again.", "replication_probability"),
            ],
            "The p-value is a null-conditional tail probability.",
            "It measures extremeness of the result under the null distribution.",
            "Interpreting the p-value as the probability that the null is true.",
        ),
        "cp": _mcq(
            "Closed-book. A test produces a very small p-value. Which conclusion is justified?",
            "Select the best conclusion.",
            [
                c("a", "The data are difficult to reconcile with the null under the test assumptions, but this does not prove the alternative or measure practical importance."),
                c("b", "The alternative has been proved with probability one.", "small_p_proves_alternative"),
                c("c", "The probability of a Type I error for this completed test equals the p-value.", "p_value_as_realised_type_i_rate"),
                c("d", "The effect must be large and practically important.", "significance_as_effect_size"),
            ],
            "A small p-value is evidence against the null, not proof or an effect-size measure.",
            "Question or reject the null at an appropriate level, then assess assumptions and practical importance.",
            "Treating significance as proof, certainty, or substantive importance.",
        ),
    },
    "revision-linear-regression-cs1013.json": {
        "ar": _mcq(
            "Closed-book. For observations (xi, yi), what criterion defines ordinary least squares estimates?",
            "Select the correct criterion.",
            [
                c("a", "Choose coefficients that minimise the sum over i of (yi minus fitted yi) squared."),
                c("b", "Choose coefficients that minimise the sum of fitted responses squared.", "fitted_values_objective"),
                c("c", "Choose coefficients that maximise sample correlation in every regression.", "correlation_as_ols"),
                c("d", "Choose coefficients that make every residual zero regardless of parameter count.", "perfect_interpolation_requirement"),
            ],
            "OLS minimises residual sum of squares for the specified model form.",
            "Minimise squared vertical differences between observed and fitted responses.",
            "Minimising fitted values or requiring exact interpolation.",
        ),
        "cp": _mcq(
            "Closed-book. Stepwise selection produces a linear model with high R-squared, but its residual plot shows clear curvature. What is the best conclusion?",
            "Select the warranted response.",
            [
                c("a", "The mean structure is likely misspecified, so investigate justified transformations or nonlinear terms and validate the revised model."),
                c("b", "High R-squared proves the linear functional form is adequate.", "r_squared_overrides_curvature"),
                c("c", "Variable selection guarantees unbiased coefficients and valid inference.", "selection_guarantees_inference"),
                c("d", "Delete observations on one side of the curve until residuals look flat.", "diagnostic_driven_deletion"),
            ],
            "Residual curvature indicates an inadequate mean structure; selection criteria do not replace diagnostics.",
            "Reconsider the functional form and validate a justified revised specification.",
            "Assuming automated selection or high R-squared establishes adequacy.",
        ),
    },
    "revision-glm-cs1014.json": {
        "ar": _mcq(
            "Closed-book. In a generalised linear model, what is the role of link function g?",
            "Select the correct statement.",
            [
                c("a", "It maps conditional mean mu to the linear predictor through g(mu) = eta = X beta."),
                c("b", "It maps each residual directly to a probability density.", "link_as_residual_density"),
                c("c", "It forces every response distribution to become Normal.", "link_normalises_response"),
                c("d", "It specifies covariance between all observations.", "link_as_dependence_model"),
            ],
            "The link connects the response mean scale to the systematic component.",
            "The link satisfies g(E[Y|X]) = X beta.",
            "Treating the link as a transformation that makes the raw response Normal.",
        ),
        "cp": _mcq(
            "Closed-book. Two nested GLMs use the same response family and scale treatment. What is a valid use of their deviance difference?",
            "Select the correct statement.",
            [
                c("a", "Under suitable regularity conditions, it can test whether added terms improve fit using an asymptotic chi-squared reference."),
                c("b", "The model with more parameters must be chosen because its deviance cannot increase.", "complexity_always_preferred"),
                c("c", "A deviance difference is always compared with standard Normal.", "wrong_reference_distribution"),
                c("d", "A non-significant difference proves every residual assumption.", "test_proves_adequacy"),
            ],
            "For appropriate nested GLMs, deviance difference is a likelihood-ratio statistic, often asymptotically chi-squared.",
            "Use the deviance difference for a nested-model test while retaining residual checks.",
            "Automatically choosing complexity or treating one test as complete validation.",
        ),
    },
    "revision-bayesian-cs1015.json": {
        "ar": _mcq(
            "Closed-book. Which expression gives the Bayesian posterior density for theta after observing data y?",
            "Select the correct proportionality.",
            [
                c("a", "posterior(theta given y) is proportional to likelihood(y given theta) times prior(theta)."),
                c("b", "posterior(theta given y) is proportional to likelihood(theta given y) plus prior(theta).", "bayes_addition_error"),
                c("c", "posterior equals likelihood without normalisation or a prior.", "prior_omitted"),
                c("d", "posterior(theta given y) is proportional to prior(y) times likelihood(theta).", "conditional_roles_reversed"),
            ],
            "Bayes' theorem multiplies prior by likelihood and normalises over theta.",
            "Posterior is proportional to likelihood times prior.",
            "Adding prior and likelihood or reversing conditional roles.",
        ),
        "cp": _mcq(
            "Closed-book. Which interpretation of a 95 percent Bayesian credible interval for theta is correct?",
            "Select the correct interpretation.",
            [
                c("a", "Given the model, prior, and data, posterior probability that theta lies in the interval is 0.95."),
                c("b", "Across repeated samples, exactly 95 percent of such intervals cover theta for every value.", "credible_as_confidence_coverage"),
                c("c", "Ninety-five percent of future observations lie in the interval.", "parameter_vs_prediction"),
                c("d", "The probability statement does not depend on prior or likelihood.", "posterior_inputs_ignored"),
            ],
            "A credible interval is a posterior probability statement conditional on the model and data.",
            "The posterior assigns probability 0.95 to theta lying in the interval.",
            "Giving a frequentist repeated-sampling interpretation to a credible interval.",
        ),
    },
    "revision-spine-memory-cs1016.json": {
        "ar": _mcq(
            "Closed-book. An unbiased estimator T has sampling variance 9/n. What does the central limit theorem add if sqrt(n)(T minus theta) converges to N(0, 9)?",
            "Select the correct implication.",
            [
                c("a", "For large n, T is approximately Normal with mean theta and variance 9/n; unbiasedness alone does not determine its sampling distribution."),
                c("b", "T is exactly Normal for every n because it is unbiased.", "unbiased_implies_normal"),
                c("c", "The variance of T is approximately 9n.", "asymptotic_variance_scaling"),
                c("d", "T converges to N(0, 9) without centring or scaling.", "standardisation_omitted"),
            ],
            "Unbiasedness specifies a mean, while asymptotic Normality supplies an approximate distribution after scaling.",
            "For large n, use T approximately N(theta, 9/n).",
            "Assuming unbiasedness determines the distribution or reversing n scaling.",
        ),
        "cp": _mcq(
            "Closed-book. A method-of-moments estimator sets the sample mean equal to model mean m(theta). Which statement is correct?",
            "Select the correct statement.",
            [
                c("a", "Solving sample mean = m(theta) defines an estimator; its sampling distribution describes estimator values over repeated samples."),
                c("b", "The estimating equation itself is the sampling distribution.", "estimating_equation_as_distribution"),
                c("c", "The estimator has zero variance because the sample moment is observed.", "observed_statistic_no_variance"),
                c("d", "Method of moments guarantees the same finite-sample distribution as maximum likelihood.", "mom_mle_distribution_equivalence"),
            ],
            "An estimating rule defines a statistic whose distribution must be derived from random sampling.",
            "Distinguish the MoM construction from the estimator's sampling distribution.",
            "Confusing an estimating equation with a sampling distribution.",
        ),
    },
    "revision-publication-front-cs1017.json": {
        "ar": _mcq(
            "Closed-book. A portfolio records the number of claims made by each policyholder during one year. Which model placement is most defensible?",
            "Select the correct classification and candidate family.",
            [
                c("a", "This is a non-negative integer count, so a discrete count model such as Poisson is a candidate, subject to assumption checks."),
                c("b", "It is continuous because a year is continuous, so Normal is mandatory.", "time_scale_determines_variable_type"),
                c("c", "It is categorical because some policyholders have zero claims.", "zero_implies_category"),
                c("d", "It must be exponential because claims occur over time.", "count_vs_waiting_time"),
            ],
            "The recorded variable is a count regardless of the continuous observation period.",
            "Treat annual claim number as discrete count data and assess an appropriate count distribution.",
            "Classifying a variable by its time window rather than its possible values.",
        ),
        "cp": _mcq(
            "Closed-book. A scatter plot shows a curved increasing association between advertising spend and policy sales. Which statement is most defensible?",
            "Select the most honest conclusion.",
            [
                c("a", "The variables appear positively associated, possibly nonlinearly, but the plot alone does not show that advertising caused the increase."),
                c("b", "The curve proves additional advertising causes additional sales.", "association_as_causation"),
                c("c", "Pearson correlation must equal zero because the pattern is curved.", "nonlinear_zero_pearson"),
                c("d", "A scatter plot cannot provide evidence about association between continuous variables.", "visualisation_has_no_association_evidence"),
            ],
            "The plot supports a descriptive association claim, not causal attribution.",
            "Report the positive nonlinear association and avoid a causal conclusion.",
            "Turning exploratory association into causation or assuming curvature means no association.",
        ),
    },
}

INVENTORY_TO_STEM = {k: k.removesuffix(".json") for k in CONVERSIONS}
STEM_TO_INVENTORY = {v: k for k, v in INVENTORY_TO_STEM.items()}

CAMPAIGN_TWINS = {
    "revision-purpose-eda-ep001.json": "campaign-alpha-ep001/packages/revision-purpose-eda-ep001.json",
    "revision-pca-distributions-cs1002.json": "campaign-beta-cs1002/packages/revision-pca-distributions-cs1002.json",
    "revision-linear-models-cs1003.json": "campaign-delta-cs1003/packages/revision-linear-models-cs1003.json",
    "revision-regression-glm-cs1003.json": "campaign-delta-cs1003/packages/revision-regression-glm-cs1003.json",
    "revision-midspine-cs1003.json": "campaign-delta-cs1003/packages/revision-midspine-cs1003.json",
    "revision-distributions-generation-cs1004.json": "campaign-gamma-cs1004/packages/revision-distributions-generation-cs1004.json",
    "revision-joint-distributions-cs1005.json": "campaign-epsilon-cs1005/packages/revision-joint-distributions-cs1005.json",
    "revision-conditional-expectations-cs1006.json": "campaign-zeta-cs1006/packages/revision-conditional-expectations-cs1006.json",
    "revision-generating-functions-cs1007.json": "campaign-eta-cs1007/packages/revision-generating-functions-cs1007.json",
    "revision-central-limit-theorem-cs1008.json": "campaign-theta-cs1008/packages/revision-central-limit-theorem-cs1008.json",
    "revision-sampling-distributions-cs1009.json": "campaign-iota-cs1009/packages/revision-sampling-distributions-cs1009.json",
    "revision-estimators-cs1010.json": "campaign-kappa-cs1010/packages/revision-estimators-cs1010.json",
    "revision-confidence-intervals-cs1011.json": "campaign-lambda-cs1011/packages/revision-confidence-intervals-cs1011.json",
    "revision-hypothesis-testing-cs1012.json": "campaign-mu-cs1012/packages/revision-hypothesis-testing-cs1012.json",
    "revision-linear-regression-cs1013.json": "campaign-nu-cs1013/packages/revision-linear-regression-cs1013.json",
    "revision-glm-cs1014.json": "campaign-xi-cs1014/packages/revision-glm-cs1014.json",
    "revision-bayesian-cs1015.json": "campaign-omicron-cs1015/packages/revision-bayesian-cs1015.json",
    "revision-spine-memory-cs1016.json": "campaign-pi-cs1016/packages/revision-spine-memory-cs1016.json",
    "revision-publication-front-cs1017.json": "campaign-rho-cs1017/packages/revision-publication-front-cs1017.json",
}

# Catalogue twin aliases for differently prefixed inventory files.
CATALOGUE_ALIASES = {
    "revision-spine-memory-cs1016.json": "cp-revision-spine-memory-cs1016.json",
    "revision-publication-front-cs1017.json": "cr-revision-publication-front-cs1017.json",
}


def apply_mcq_overlay(pkg: dict[str, Any], stem: str) -> dict[str, Any]:
    """Replace active-recall and ordered checkpoint checks with MCQs."""
    inv_key = stem if stem in CONVERSIONS else STEM_TO_INVENTORY.get(stem.removesuffix(".json"))
    if not inv_key:
        return pkg
    parts = CONVERSIONS[inv_key]
    checkpoint_items = parts.get("cps")
    if checkpoint_items is None:
        checkpoint_items = [parts["cp"]]
    checkpoint_index = 0
    updated_checks: list[dict[str, Any]] = []
    for check in pkg.get("knowledge_checks") or []:
        updated = dict(check)
        if check.get("kind") == "active_recall":
            updated.update(parts["ar"])
        elif check.get("kind") == "checkpoint" and checkpoint_index < len(
            checkpoint_items
        ):
            updated.update(checkpoint_items[checkpoint_index])
            checkpoint_index += 1
        updated_checks.append(updated)
    pkg["knowledge_checks"] = updated_checks
    return pkg


def sync_catalogue_twins(root: Path | None = None) -> int:
    """Patch catalogue twins with revision MCQ knowledge checks."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key in CONVERSIONS:
        path = catalogue_dir / CATALOGUE_ALIASES.get(inv_key, inv_key)
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        updated += 1
    return updated


def sync_campaign_twins(root: Path | None = None) -> int:
    """Patch educational-campaign twins with revision MCQ checks."""
    repo = root or Path(__file__).resolve().parents[1]
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        path = campaign_dir / rel_path
        if not path.exists():
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        apply_mcq_overlay(pkg, INVENTORY_TO_STEM[inv_key])
        path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
        updated += 1
    return updated


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    """Scan every synced revision check for structural and writing defects."""
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    duplicate = re.compile(r"\b(\w+)\s+\1\b", re.IGNORECASE)
    meta_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bspine\b",
            r"\bexam-ready\b",
            r"\bexam ready\b",
            r"\bweakest link\b",
            r"\bChapter \d+ complete\b",
            r"\bcampaign\b",
            r"\bjourney\b",
            r"\bBatch \d\b",
            r"\bWave \d\b",
            r"\bIsolated Golden Day\b",
        )
    ]
    defects: list[str] = []
    paths: list[tuple[Path, str]] = []
    for inv_key in CONVERSIONS:
        paths.append((catalogue_dir / CATALOGUE_ALIASES.get(inv_key, inv_key), inv_key))
        paths.append((campaign_dir / CAMPAIGN_TWINS[inv_key], inv_key))
    for path, inv_key in paths:
        if not path.exists():
            defects.append(f"MISSING: {path}")
            continue
        pkg = json.loads(path.read_text(encoding="utf-8"))
        active_recall = [
            check for check in pkg.get("knowledge_checks") or [] if check.get("kind") == "active_recall"
        ]
        checkpoints = [
            check for check in pkg.get("knowledge_checks") or [] if check.get("kind") == "checkpoint"
        ]
        expected_checkpoints = len(CONVERSIONS[inv_key].get("cps") or [CONVERSIONS[inv_key].get("cp")])
        if len(active_recall) != 1:
            defects.append(f"{path.name}: expected 1 active_recall, found {len(active_recall)}")
        if len(checkpoints) != expected_checkpoints:
            defects.append(f"{path.name}: expected {expected_checkpoints} checkpoints, found {len(checkpoints)}")
        for kind, index, check in [
            *[("active_recall", i, item) for i, item in enumerate(active_recall)],
            *[("checkpoint", i, item) for i, item in enumerate(checkpoints)],
        ]:
            location = f"{path.name} {kind}[{index}]"
            if check.get("response_type") != "mcq":
                defects.append(f"{location}: not mcq")
            choices = check.get("choices") or []
            if len(choices) != 4:
                defects.append(f"{location}: not 4 choices")
            if [choice.get("id") for choice in choices] != ["a", "b", "c", "d"]:
                defects.append(f"{location}: bad choice ids")
            correct = check.get("correct_choice_id")
            if correct not in {"a", "b", "c", "d"}:
                defects.append(f"{location}: bad correct_choice_id")
            for field in ("prompt", "body", "explanation", "model_answer", "common_mistake"):
                if not check.get(field):
                    defects.append(f"{location}: missing {field}")
            if not str(check.get("prompt", "")).startswith("Closed-book."):
                defects.append(f"{location}: prompt is not closed-book")
            for choice in choices:
                tag = choice.get("misconception_tag")
                if choice.get("id") == correct and tag:
                    defects.append(f"{location}: correct choice has tag")
                if choice.get("id") != correct and not tag:
                    defects.append(f"{location}: distractor missing tag")
            blob = json.dumps(check, ensure_ascii=False)
            if "\u2014" in blob:
                defects.append(f"{location}: em dash found")
            for match in duplicate.finditer(blob):
                defects.append(f"{location}: duplicate word '{match.group(1)}'")
            for pattern in meta_patterns:
                if pattern.search(blob):
                    defects.append(f"{location}: meta language '{pattern.pattern}'")
    return defects


if __name__ == "__main__":
    campaign_count = sync_campaign_twins()
    catalogue_count = sync_catalogue_twins()
    scan = mechanical_defect_scan()
    item_count = sum(
        1 + len(parts.get("cps") or [parts.get("cp")])
        for parts in CONVERSIONS.values()
    )
    print(f"Synced {campaign_count} campaign + {catalogue_count} catalogue twins.")
    print(f"Item count: {item_count}")
    if scan:
        print("DEFECTS:")
        for defect in scan:
            print(" ", defect)
    else:
        print("Mechanical defect scan: PASS (0 issues)")

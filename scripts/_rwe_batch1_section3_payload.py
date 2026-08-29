#!/usr/bin/env python3
"""Real Worked Examples Batch 1 — Section 3 (Kappa / Lambda / Mu + Pi Memory Front).

Injects genuine numeric ``worked_example`` objects into the same 22-package
scope as MCQ Batch 1, then synchronises catalogue and campaign twins.
"""
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Inventory key (catalogue filename) -> worked_example object
WORKED_EXAMPLES: dict[str, dict[str, Any]] = {
    # ------------------------------------------------------------------
    # Kappa 3.1.x
    # ------------------------------------------------------------------
    "3.1.1-method-of-moments-cs1010.json": {
        "title": "MoM mean claim severity (Exponential)",
        "problem_statement": (
            "A motor book records five independent claim sizes (£): "
            "2400, 1600, 3200, 1800, 2000. Model each claim as "
            "Exponential with unknown mean μ (so E[X] = μ). Construct the "
            "method-of-moments estimator of μ and evaluate it on this sample."
        ),
        "given": [
            {"symbol": "x₁…x₅", "value": "2400, 1600, 3200, 1800, 2000", "note": "claim sizes (£)"},
            {"symbol": "n", "value": "5", "note": "sample size"},
            {"symbol": "E[X]", "value": "μ", "note": "Exponential mean parameter"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Before uncovering, write the first population moment "
            "in terms of μ and the matching sample moment."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Write the first-moment equation",
                "attempt_cue": "Equate E[X] to the sample mean and solve for μ.",
                "explanation": (
                    "Method of moments equates the population moment E[X] = μ "
                    "to the sample moment x̄, then solves for the parameter."
                ),
                "calculation": "E[X] = μ  ⇒  μ̂_MoM = x̄",
                "result": "μ̂_MoM = x̄",
            },
            {
                "id": "S2",
                "label": "Compute the sample mean",
                "attempt_cue": "Add the five claim sizes and divide by 5.",
                "explanation": "The first sample moment is the ordinary arithmetic mean.",
                "calculation": "(2400 + 1600 + 3200 + 1800 + 2000) / 5 = 11000 / 5 = 2200",
                "result": "x̄ = 2200",
            },
            {
                "id": "S3",
                "label": "State the MoM estimate",
                "attempt_cue": "Substitute x̄ into μ̂_MoM.",
                "explanation": "For the Exponential mean parameter, MoM and the sample mean coincide.",
                "calculation": "μ̂_MoM = 2200",
                "result": "μ̂_MoM = 2200 (£)",
            },
        ],
        "final_answer": "μ̂_MoM = x̄ = £2200 for this sample.",
        "common_pitfall": (
            "Using the Exponential rate parameter λ = 1/μ and reporting "
            "λ̂ = 2200 (or 1/5) instead of solving the moment equation for the "
            "mean parameter actually requested."
        ),
        "syllabus_ref": "3.1.1",
    },
    "3.1.2-maximum-likelihood-cs1010.json": {
        "title": "MLE for Exponential claim waiting times",
        "problem_statement": (
            "Four independent claim settlement delays (months) are modelled as "
            "Exponential with rate λ (pdf f(x) = λ e^{−λx} for x > 0): "
            "2, 3, 1, 4. Find the maximum-likelihood estimate of λ."
        ),
        "given": [
            {"symbol": "x₁…x₄", "value": "2, 3, 1, 4", "note": "settlement delays (months)"},
            {"symbol": "n", "value": "4", "note": "sample size"},
            {"symbol": "f(x|λ)", "value": "λ e^{−λx}", "note": "Exponential rate pdf"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write the log-likelihood ℓ(λ) before differentiating."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Form the likelihood and log-likelihood",
                "attempt_cue": "Write L(λ) = λⁿ exp(−λ Σxᵢ) and ℓ(λ) = n ln λ − λ Σxᵢ.",
                "explanation": (
                    "Independence multiplies the densities. The log turns the "
                    "product into a sum that is easy to differentiate."
                ),
                "calculation": "Σxᵢ = 2+3+1+4 = 10;  ℓ(λ) = 4 ln λ − 10λ",
                "result": "ℓ(λ) = 4 ln λ − 10λ",
            },
            {
                "id": "S2",
                "label": "Differentiate and solve the score equation",
                "attempt_cue": "Set dℓ/dλ = 0 and solve for λ.",
                "explanation": (
                    "The MLE solves the score equation. For Exponential rate, "
                    "this yields λ̂ = n / Σxᵢ = 1/x̄."
                ),
                "calculation": "dℓ/dλ = 4/λ − 10 = 0  ⇒  λ̂ = 4/10 = 0.4",
                "result": "λ̂_MLE = 0.4",
            },
            {
                "id": "S3",
                "label": "Confirm it is a maximum",
                "attempt_cue": "Check the second derivative sign at λ̂.",
                "explanation": "d²ℓ/dλ² = −n/λ² < 0 for λ > 0, so the critical point is a maximum.",
                "calculation": "d²ℓ/dλ² = −4/λ² < 0 at λ̂ = 0.4",
                "result": "λ̂_MLE = 0.4 (maximum)",
            },
        ],
        "final_answer": "λ̂_MLE = 4/10 = 0.4 per month.",
        "common_pitfall": (
            "Reporting the MLE of the mean μ̂ = x̄ = 2.5 when the question asked "
            "for the rate λ, or writing λ̂ = Σxᵢ/n = 2.5 instead of n/Σxᵢ."
        ),
        "syllabus_ref": "3.1.2",
    },
    "3.1.3-efficiency-bias-consistency-mse-cs1010.json": {
        "title": "Bias and MSE for two reserve estimators",
        "problem_statement": (
            "Two estimators of mean ultimate claim cost μ (in £000) are under "
            "review. Estimator A is unbiased with Var(A) = 25. Estimator B has "
            "E[B] = μ + 2 and Var(B) = 16. Compute Bias(B) and MSE for both "
            "estimators, and state which has smaller MSE."
        ),
        "given": [
            {"symbol": "E[A]", "value": "μ", "note": "A is unbiased"},
            {"symbol": "Var(A)", "value": "25", "note": "variance of A"},
            {"symbol": "E[B]", "value": "μ + 2", "note": "expectation of B"},
            {"symbol": "Var(B)", "value": "16", "note": "variance of B"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write Bias(θ̂) = E[θ̂] − θ and MSE = Var + Bias² before computing."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Compute biases",
                "attempt_cue": "Bias(A) = E[A] − μ and Bias(B) = E[B] − μ.",
                "explanation": "Bias is the systematic error E[θ̂] − θ. Unbiased means Bias = 0.",
                "calculation": "Bias(A) = μ − μ = 0;  Bias(B) = (μ + 2) − μ = 2",
                "result": "Bias(A) = 0; Bias(B) = 2",
            },
            {
                "id": "S2",
                "label": "Compute MSE for each estimator",
                "attempt_cue": "Use MSE(θ̂) = Var(θ̂) + [Bias(θ̂)]².",
                "explanation": (
                    "Mean squared error decomposes into variance plus squared "
                    "bias, so a biased estimator can still win on MSE."
                ),
                "calculation": "MSE(A) = 25 + 0² = 25;  MSE(B) = 16 + 2² = 16 + 4 = 20",
                "result": "MSE(A) = 25; MSE(B) = 20",
            },
            {
                "id": "S3",
                "label": "Compare",
                "attempt_cue": "Name which estimator has smaller MSE.",
                "explanation": "Smaller MSE is the comparison criterion requested here.",
                "calculation": "20 < 25  ⇒  B has smaller MSE",
                "result": "B preferred on MSE (despite Bias = 2)",
            },
        ],
        "final_answer": (
            "Bias(A) = 0, MSE(A) = 25; Bias(B) = 2, MSE(B) = 20. "
            "B has smaller MSE."
        ),
        "common_pitfall": (
            "Choosing A solely because it is unbiased, and ignoring that "
            "MSE(B) = 20 is smaller than MSE(A) = 25."
        ),
        "syllabus_ref": "3.1.3",
    },
    "3.1.4-comparison-mse-cs1010.json": {
        "title": "Compare two premium estimators by MSE",
        "problem_statement": (
            "An insurer compares two estimators of mean annual premium μ (£). "
            "Estimator T₁ has Bias(T₁) = 0 and Var(T₁) = 9. Estimator T₂ has "
            "Bias(T₂) = 1 and Var(T₂) = 4. Compute both MSEs and select the "
            "estimator with smaller MSE."
        ),
        "given": [
            {"symbol": "Bias(T₁)", "value": "0", "note": "bias of T₁"},
            {"symbol": "Var(T₁)", "value": "9", "note": "variance of T₁"},
            {"symbol": "Bias(T₂)", "value": "1", "note": "bias of T₂"},
            {"symbol": "Var(T₂)", "value": "4", "note": "variance of T₂"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Before uncovering, write MSE = Var + Bias² for each estimator."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "MSE of T₁",
                "attempt_cue": "Substitute Bias(T₁) and Var(T₁) into the MSE identity.",
                "explanation": "MSE(T₁) = Var(T₁) + [Bias(T₁)]² collapses to variance when Bias = 0.",
                "calculation": "MSE(T₁) = 9 + 0² = 9",
                "result": "MSE(T₁) = 9",
            },
            {
                "id": "S2",
                "label": "MSE of T₂",
                "attempt_cue": "Substitute Bias(T₂) = 1 and Var(T₂) = 4.",
                "explanation": "Squared bias is added in full; do not omit the Bias² term.",
                "calculation": "MSE(T₂) = 4 + 1² = 4 + 1 = 5",
                "result": "MSE(T₂) = 5",
            },
            {
                "id": "S3",
                "label": "Select by MSE",
                "attempt_cue": "Compare 9 and 5.",
                "explanation": "Under an MSE comparison rule, prefer the smaller value.",
                "calculation": "5 < 9  ⇒  prefer T₂",
                "result": "T₂ has smaller MSE",
            },
        ],
        "final_answer": "MSE(T₁) = 9; MSE(T₂) = 5. Prefer T₂ on MSE.",
        "common_pitfall": (
            "Comparing variances alone (9 vs 4) and declaring T₂ better without "
            "adding Bias², or refusing T₂ because Bias ≠ 0 despite MSE(T₂) = 5 < 9."
        ),
        "syllabus_ref": "3.1.4",
    },
    "3.1.5-asymptotic-mle-cs1010.json": {
        "title": "Asymptotic SE and CI for Exponential rate MLE",
        "problem_statement": (
            "From n = 64 independent Exponential claim delays with rate λ, the "
            "MLE is λ̂ = 0.25. Using the asymptotic Normal approximation "
            "λ̂ ≈ N(λ, λ²/n) (equivalently SE ≈ λ̂/√n), give the estimated "
            "standard error and an approximate 95% confidence interval for λ."
        ),
        "given": [
            {"symbol": "n", "value": "64", "note": "sample size"},
            {"symbol": "λ̂", "value": "0.25", "note": "MLE of the rate"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal 97.5% quantile"},
            {"symbol": "asymptotic Var", "value": "λ²/n", "note": "Exp(rate) Fisher information inverse"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write SÊ = λ̂/√n before building the interval."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Estimated asymptotic standard error",
                "attempt_cue": "Compute λ̂/√n with √64 = 8.",
                "explanation": (
                    "For Exponential rate, I(λ) = 1/λ² per observation, so "
                    "asymptotic variance is λ²/n and SE = λ/√n, plugged in at λ̂."
                ),
                "calculation": "SÊ = 0.25 / √64 = 0.25 / 8 = 0.03125",
                "result": "SÊ = 0.03125",
            },
            {
                "id": "S2",
                "label": "Half-width of the approximate 95% CI",
                "attempt_cue": "Multiply SÊ by 1.96.",
                "explanation": "Wald interval uses the Normal quantile times the estimated SE.",
                "calculation": "1.96 × 0.03125 = 0.06125",
                "result": "half-width = 0.06125",
            },
            {
                "id": "S3",
                "label": "Form the interval",
                "attempt_cue": "Compute λ̂ ± 1.96 SÊ.",
                "explanation": "Centre at the MLE and add/subtract the half-width.",
                "calculation": "0.25 ± 0.06125  ⇒  (0.18875, 0.31125)",
                "result": "(0.18875, 0.31125)",
            },
        ],
        "final_answer": (
            "SÊ = 0.03125; approximate 95% CI for λ is (0.18875, 0.31125)."
        ),
        "common_pitfall": (
            "Using SE = 1/(λ̂√n) = 1/(0.25×8) = 0.5 (the Exponential-mean "
            "information form) instead of SE = λ̂/√n = 0.03125 for the rate."
        ),
        "syllabus_ref": "3.1.5",
    },
    "3.1.6-bootstrap-estimator-cs1010.json": {
        "title": "Bootstrap SE of mean claim severity",
        "problem_statement": (
            "A nonparametric bootstrap of the sample mean claim severity produced "
            "B = 5 bootstrap replicates (£00): 210, 195, 220, 205, 200. Estimate "
            "the bootstrap standard error of the mean using "
            "SÊ_boot = √[(1/B) Σ(θ̂*_b − θ̄*)²], where θ̄* is the mean of the "
            "bootstrap replicates."
        ),
        "given": [
            {"symbol": "θ̂*_1…θ̂*_5", "value": "210, 195, 220, 205, 200", "note": "bootstrap means (£00)"},
            {"symbol": "B", "value": "5", "note": "number of bootstrap replicates"},
        ],
        "attempt_before_reveal": (
            "CMP closed. First compute θ̄*, then the average squared deviation."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Mean of bootstrap replicates",
                "attempt_cue": "Average the five bootstrap means.",
                "explanation": "θ̄* centres the bootstrap deviations used in the SE formula.",
                "calculation": "(210 + 195 + 220 + 205 + 200) / 5 = 1030 / 5 = 206",
                "result": "θ̄* = 206",
            },
            {
                "id": "S2",
                "label": "Sum of squared deviations",
                "attempt_cue": "Compute Σ(θ̂*_b − 206)².",
                "explanation": "Each replicate's squared distance from θ̄* enters the bootstrap variance.",
                "calculation": (
                    "(210−206)² + (195−206)² + (220−206)² + (205−206)² + (200−206)² "
                    "= 16 + 121 + 196 + 1 + 36 = 370"
                ),
                "result": "Σ(θ̂*_b − θ̄*)² = 370",
            },
            {
                "id": "S3",
                "label": "Bootstrap SE",
                "attempt_cue": "Take √(370/B) with B = 5.",
                "explanation": "The stated bootstrap SE divides by B inside the square root.",
                "calculation": "SÊ_boot = √(370/5) = √74 ≈ 8.602",
                "result": "SÊ_boot ≈ 8.602 (£00)",
            },
        ],
        "final_answer": "θ̄* = 206; SÊ_boot = √74 ≈ 8.602 (£00).",
        "common_pitfall": (
            "Dividing by B−1 = 4 (ordinary sample SD) to get √(370/4) = √92.5 ≈ 9.62 "
            "instead of the bootstrap /B form √(370/5) = √74 required here."
        ),
        "syllabus_ref": "3.1.6",
    },
    # ------------------------------------------------------------------
    # Lambda 3.2.x
    # ------------------------------------------------------------------
    "3.2.1-confidence-interval-parameter-cs1011.json": {
        "title": "95% z-interval for mean claim cost",
        "problem_statement": (
            "A random sample of n = 36 commercial property claims has sample "
            "mean x̄ = £12,000. Claim sizes are modelled as Normal with known "
            "σ = £1,800. Construct a 95% confidence interval for the population "
            "mean μ."
        ),
        "given": [
            {"symbol": "n", "value": "36", "note": "sample size"},
            {"symbol": "x̄", "value": "12000", "note": "sample mean (£)"},
            {"symbol": "σ", "value": "1800", "note": "known population SD (£)"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write the z-interval formula x̄ ± z_{0.975} σ/√n before substituting."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Standard error of the mean",
                "attempt_cue": "Compute σ/√n with √36 = 6.",
                "explanation": "For a Normal mean with known σ, SE(x̄) = σ/√n.",
                "calculation": "1800 / 6 = 300",
                "result": "SE = 300",
            },
            {
                "id": "S2",
                "label": "Half-width",
                "attempt_cue": "Multiply the SE by 1.96.",
                "explanation": "The 95% z critical value scales the SE into the margin of error.",
                "calculation": "1.96 × 300 = 588",
                "result": "half-width = 588",
            },
            {
                "id": "S3",
                "label": "Interval endpoints",
                "attempt_cue": "Compute 12000 ± 588.",
                "explanation": "Centre at x̄ and add/subtract the half-width.",
                "calculation": "12000 − 588 = 11412;  12000 + 588 = 12588",
                "result": "(11412, 12588)",
            },
        ],
        "final_answer": "95% CI for μ: (£11,412, £12,588).",
        "common_pitfall": (
            "Using σ instead of σ/√n in the margin (1.96 × 1800) and producing "
            "a wildly wide interval, or using √n = √36 incorrectly as 36."
        ),
        "syllabus_ref": "3.2.1",
    },
    "3.2.2-prediction-interval-cs1011.json": {
        "title": "95% prediction interval for a future claim",
        "problem_statement": (
            "From n = 25 independent Normal claims with known σ = £40, the "
            "sample mean is x̄ = £500. Construct a 95% prediction interval for "
            "one future independent claim Y."
        ),
        "given": [
            {"symbol": "n", "value": "25", "note": "sample size"},
            {"symbol": "x̄", "value": "500", "note": "sample mean (£)"},
            {"symbol": "σ", "value": "40", "note": "known SD (£)"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write the prediction SE σ√(1 + 1/n) before the interval."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Prediction standard error",
                "attempt_cue": "Compute σ√(1 + 1/n).",
                "explanation": (
                    "A future observation has variance σ² plus the variance of "
                    "x̄, so the prediction SE is σ√(1 + 1/n), not σ/√n."
                ),
                "calculation": "√(1 + 1/25) = √1.04 ≈ 1.019804;  40 × 1.019804 ≈ 40.792",
                "result": "SE_pred ≈ 40.792",
            },
            {
                "id": "S2",
                "label": "Half-width",
                "attempt_cue": "Multiply SE_pred by 1.96.",
                "explanation": "Same Normal quantile as a mean CI, but applied to the prediction SE.",
                "calculation": "1.96 × 40.792 ≈ 79.953",
                "result": "half-width ≈ 79.953",
            },
            {
                "id": "S3",
                "label": "Prediction interval",
                "attempt_cue": "Compute 500 ± 79.953.",
                "explanation": "Centre at x̄; the wider SE distinguishes prediction from mean estimation.",
                "calculation": "500 − 79.953 ≈ 420.047;  500 + 79.953 ≈ 579.953",
                "result": "(420.047, 579.953)",
            },
        ],
        "final_answer": (
            "95% prediction interval for Y: approximately (£420.05, £579.95)."
        ),
        "common_pitfall": (
            "Using the mean CI half-width 1.96 × 40/√25 = 15.68 instead of the "
            "prediction form 1.96 × 40√(1+1/25) ≈ 79.95."
        ),
        "syllabus_ref": "3.2.2",
    },
    "3.2.3-ci-given-sampling-distribution-cs1011.json": {
        "title": "CI from a stated Normal sampling distribution",
        "problem_statement": (
            "An estimator θ̂ of a portfolio proportion satisfies "
            "θ̂ ~ N(θ, 0.01²) exactly (sampling distribution given). Observing "
            "θ̂ = 0.42, construct a 95% confidence interval for θ."
        ),
        "given": [
            {"symbol": "θ̂", "value": "0.42", "note": "observed estimate"},
            {"symbol": "SD(θ̂)", "value": "0.01", "note": "given sampling SD"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Invert θ̂ ~ N(θ, 0.01²) into θ̂ ± 1.96 × 0.01."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Identify the pivot half-width",
                "attempt_cue": "Compute 1.96 × 0.01.",
                "explanation": (
                    "When the sampling distribution is given as Normal with known "
                    "SD, the CI is the estimate plus/minus z times that SD."
                ),
                "calculation": "1.96 × 0.01 = 0.0196",
                "result": "half-width = 0.0196",
            },
            {
                "id": "S2",
                "label": "Form the interval",
                "attempt_cue": "Compute 0.42 ± 0.0196.",
                "explanation": "Centre at the observed θ̂.",
                "calculation": "0.42 − 0.0196 = 0.4004;  0.42 + 0.0196 = 0.4396",
                "result": "(0.4004, 0.4396)",
            },
        ],
        "final_answer": "95% CI for θ: (0.4004, 0.4396).",
        "common_pitfall": (
            "Dividing 0.01 by √n when no sample size is part of the given "
            "sampling distribution, or using 0.42 ± 1.96 × 0.01²."
        ),
        "syllabus_ref": "3.2.3",
    },
    "3.2.4-ci-normal-mean-variance-cs1011.json": {
        "title": "t-interval for Normal mean claim amount",
        "problem_statement": (
            "A sample of n = 16 Normal claim amounts has x̄ = £100 and sample "
            "SD s = £6. Using t_{15, 0.975} = 2.131, construct a 95% confidence "
            "interval for the mean μ (σ unknown)."
        ),
        "given": [
            {"symbol": "n", "value": "16", "note": "sample size"},
            {"symbol": "x̄", "value": "100", "note": "sample mean (£)"},
            {"symbol": "s", "value": "6", "note": "sample SD (£)"},
            {"symbol": "t_{15,0.975}", "value": "2.131", "note": "t critical value"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write x̄ ± t_{n−1} s/√n with n−1 = 15 before substituting."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Standard error",
                "attempt_cue": "Compute s/√n with √16 = 4.",
                "explanation": "With σ unknown, replace σ by s in the SE of the mean.",
                "calculation": "6 / 4 = 1.5",
                "result": "SE = 1.5",
            },
            {
                "id": "S2",
                "label": "Half-width",
                "attempt_cue": "Multiply SE by t_{15,0.975} = 2.131.",
                "explanation": "The t quantile (not 1.96) accounts for estimating σ.",
                "calculation": "2.131 × 1.5 = 3.1965",
                "result": "half-width = 3.1965",
            },
            {
                "id": "S3",
                "label": "Interval",
                "attempt_cue": "Compute 100 ± 3.1965.",
                "explanation": "Centre at x̄.",
                "calculation": "100 − 3.1965 = 96.8035;  100 + 3.1965 = 103.1965",
                "result": "(96.8035, 103.1965)",
            },
        ],
        "final_answer": "95% CI for μ: (£96.8035, £103.1965).",
        "common_pitfall": (
            "Using z = 1.96 instead of t_{15,0.975} = 2.131 when σ is estimated "
            "from the sample, which understates the half-width (2.94 vs 3.1965)."
        ),
        "syllabus_ref": "3.2.4",
    },
    "3.2.5-ci-binomial-poisson-cs1011.json": {
        "title": "Approximate 95% CI for a claim frequency proportion",
        "problem_statement": (
            "In a sample of n = 100 policies, x = 22 produce at least one claim "
            "in the year. Using the Normal approximation with p̂ = x/n, construct "
            "an approximate 95% confidence interval for the claim incidence "
            "probability p."
        ),
        "given": [
            {"symbol": "n", "value": "100", "note": "policies"},
            {"symbol": "x", "value": "22", "note": "policies with ≥1 claim"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write p̂ ± 1.96 √[p̂(1−p̂)/n] before substituting."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Sample proportion",
                "attempt_cue": "Compute p̂ = x/n.",
                "explanation": "The MLE / MoM estimator of a Bernoulli probability is the sample proportion.",
                "calculation": "p̂ = 22/100 = 0.22",
                "result": "p̂ = 0.22",
            },
            {
                "id": "S2",
                "label": "Estimated SE",
                "attempt_cue": "Compute √[0.22 × 0.78 / 100].",
                "explanation": "Binomial/Bernoulli variance p(1−p)/n is plugged in at p̂.",
                "calculation": "√(0.22 × 0.78 / 100) = √0.001716 ≈ 0.041425",
                "result": "SÊ ≈ 0.041425",
            },
            {
                "id": "S3",
                "label": "Interval",
                "attempt_cue": "Compute 0.22 ± 1.96 × 0.041425.",
                "explanation": "Wald interval for a proportion.",
                "calculation": (
                    "1.96 × 0.041425 ≈ 0.08119;  "
                    "0.22 − 0.08119 ≈ 0.13881;  0.22 + 0.08119 ≈ 0.30119"
                ),
                "result": "(0.13881, 0.30119)",
            },
        ],
        "final_answer": "Approximate 95% CI for p: (0.13881, 0.30119).",
        "common_pitfall": (
            "Using √[p̂/n] = √0.0022 (Poisson-style) instead of √[p̂(1−p̂)/n], "
            "or forgetting the (1−p̂) factor."
        ),
        "syllabus_ref": "3.2.5",
    },
    "3.2.6-ci-two-sample-cs1011.json": {
        "title": "95% CI for difference of two mean claim costs",
        "problem_statement": (
            "Independent samples from portfolios A and B (Normal, known "
            "variances): n_A = 40, x̄_A = £8,200, σ_A = £1,200; "
            "n_B = 45, x̄_B = £7,600, σ_B = £1,100. Construct a 95% CI for "
            "μ_A − μ_B."
        ),
        "given": [
            {"symbol": "n_A, x̄_A, σ_A", "value": "40, 8200, 1200", "note": "portfolio A"},
            {"symbol": "n_B, x̄_B, σ_B", "value": "45, 7600, 1100", "note": "portfolio B"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write SE = √(σ_A²/n_A + σ_B²/n_B) before the interval."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Point estimate of the difference",
                "attempt_cue": "Compute x̄_A − x̄_B.",
                "explanation": "The natural centre for μ_A − μ_B is the difference of sample means.",
                "calculation": "8200 − 7600 = 600",
                "result": "x̄_A − x̄_B = 600",
            },
            {
                "id": "S2",
                "label": "SE of the difference",
                "attempt_cue": "Compute √(1200²/40 + 1100²/45).",
                "explanation": "Independence adds the variances of the two sample means.",
                "calculation": (
                    "1200²/40 = 36000;  1100²/45 = 1210000/45 ≈ 26888.889;  "
                    "√(36000 + 26888.889) = √62888.889 ≈ 250.777"
                ),
                "result": "SE ≈ 250.777",
            },
            {
                "id": "S3",
                "label": "Interval",
                "attempt_cue": "Compute 600 ± 1.96 × 250.777.",
                "explanation": "Two-sample z-interval with known variances.",
                "calculation": (
                    "1.96 × 250.777 ≈ 491.522;  "
                    "600 − 491.522 ≈ 108.478;  600 + 491.522 ≈ 1091.522"
                ),
                "result": "(108.478, 1091.522)",
            },
        ],
        "final_answer": "95% CI for μ_A − μ_B: approximately (£108.48, £1,091.52).",
        "common_pitfall": (
            "Pooling into √(σ²(1/n_A+1/n_B)) with a single σ, or subtracting "
            "SEs instead of adding variances under the square root."
        ),
        "syllabus_ref": "3.2.6",
    },
    "3.2.7-ci-paired-means-cs1011.json": {
        "title": "Paired t-interval for before/after loss reduction",
        "problem_statement": (
            "Eight policyholders each have a before/after loss pair. Differences "
            "d = before − after (£00) are: 12, 8, −2, 15, 10, 5, 9, 7. Using "
            "t_{7, 0.975} = 2.365, construct a 95% CI for the mean difference μ_d."
        ),
        "given": [
            {"symbol": "d₁…d₈", "value": "12, 8, −2, 15, 10, 5, 9, 7", "note": "paired differences (£00)"},
            {"symbol": "n", "value": "8", "note": "pairs"},
            {"symbol": "t_{7,0.975}", "value": "2.365", "note": "t critical value"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Reduce to a one-sample t-interval on the differences."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Mean difference",
                "attempt_cue": "Average the eight differences.",
                "explanation": "Paired data are analysed through the differences d_i.",
                "calculation": "(12+8−2+15+10+5+9+7)/8 = 64/8 = 8",
                "result": "d̄ = 8",
            },
            {
                "id": "S2",
                "label": "Sample SD of differences",
                "attempt_cue": "Compute s_d = √[Σ(d_i − d̄)²/(n−1)].",
                "explanation": "The SE uses the sample SD of the paired differences, not the raw before/after series.",
                "calculation": (
                    "Σ(d_i−8)² = 16+0+100+49+4+9+1+1 = 180;  "
                    "s_d = √(180/7) = √25.714286 ≈ 5.0709"
                ),
                "result": "s_d ≈ 5.0709",
            },
            {
                "id": "S3",
                "label": "SE and interval",
                "attempt_cue": "SE = s_d/√n; then d̄ ± t × SE.",
                "explanation": "One-sample t formula applied to the differences.",
                "calculation": (
                    "SE = 5.0709/√8 ≈ 1.7928;  2.365 × 1.7928 ≈ 4.240;  "
                    "8 − 4.240 ≈ 3.760;  8 + 4.240 ≈ 12.240"
                ),
                "result": "(3.760, 12.240)",
            },
        ],
        "final_answer": "95% CI for μ_d: approximately (3.760, 12.240) in £00.",
        "common_pitfall": (
            "Treating the before and after samples as independent two-sample "
            "data instead of pairing, or using z = 1.96 with n = 8."
        ),
        "syllabus_ref": "3.2.7",
    },
    "3.2.8-bootstrap-confidence-interval-cs1011.json": {
        "title": "Percentile bootstrap CI for mean severity",
        "problem_statement": (
            "A nonparametric bootstrap of mean claim severity produced B = 10 "
            "bootstrap means (£), already sorted: "
            "1900, 1950, 1980, 2000, 2010, 2030, 2050, 2080, 2100, 2150. "
            "Using the percentile method with α = 0.05, form an approximate "
            "90% CI by taking the order statistics at indices "
            "⌊α(B+1)⌋ = ⌊0.55⌋ → 1 (use 1st) and ⌈(1−α)(B+1)⌉ = ⌈10.45⌉ → 11 "
            "(clamp to 10th)."
        ),
        "given": [
            {
                "symbol": "θ̂*_{(1)}…θ̂*_{(10)}",
                "value": "1900, 1950, 1980, 2000, 2010, 2030, 2050, 2080, 2100, 2150",
                "note": "sorted bootstrap means (£)",
            },
            {"symbol": "B", "value": "10", "note": "bootstrap replicates"},
            {"symbol": "α", "value": "0.05", "note": "for a 90% percentile interval"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Identify which order statistics become the lower and upper endpoints."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Lower index",
                "attempt_cue": "Evaluate ⌊α(B+1)⌋ and map to an order statistic.",
                "explanation": (
                    "The percentile method reads quantiles from the ordered "
                    "bootstrap replicates rather than using a Normal SE."
                ),
                "calculation": "⌊0.05 × 11⌋ = ⌊0.55⌋ = 0 → use the 1st order statistic",
                "result": "lower index = 1",
            },
            {
                "id": "S2",
                "label": "Upper index",
                "attempt_cue": "Evaluate ⌈(1−α)(B+1)⌉ and clamp to B if needed.",
                "explanation": "Symmetric upper quantile for the same α.",
                "calculation": "⌈0.95 × 11⌉ = ⌈10.45⌉ = 11 → clamp to 10",
                "result": "upper index = 10",
            },
            {
                "id": "S3",
                "label": "Read the interval",
                "attempt_cue": "Take θ̂*_{(1)} and θ̂*_{(10)}.",
                "explanation": "Endpoints are the selected order statistics themselves.",
                "calculation": "θ̂*_{(1)} = 1900;  θ̂*_{(10)} = 2150",
                "result": "(1900, 2150)",
            },
        ],
        "final_answer": "Approximate 90% percentile bootstrap CI: (£1,900, £2,150).",
        "common_pitfall": (
            "Building a Wald interval from the bootstrap SE instead of reading "
            "percentile order statistics, or taking the 2nd and 9th values "
            "without applying the α(B+1) index rule given in the problem."
        ),
        "syllabus_ref": "3.2.8",
    },
    # ------------------------------------------------------------------
    # Mu 3.3.x
    # ------------------------------------------------------------------
    "3.3.1-hypothesis-concepts-cs1012.json": {
        "title": "Two-sided p-value for a claim-mean z-test",
        "problem_statement": (
            "A pricing team tests H₀: μ = £10,000 vs H₁: μ ≠ £10,000 for mean "
            "claim cost at significance level α = 0.05. The test statistic is "
            "z = 2.1 under H₀ (standard Normal). Compute the two-sided p-value "
            "and state the decision. Use Φ(2.1) = 0.9821."
        ),
        "given": [
            {"symbol": "H₀", "value": "μ = 10000", "note": "null mean claim cost (£)"},
            {"symbol": "z", "value": "2.1", "note": "observed test statistic"},
            {"symbol": "Φ(2.1)", "value": "0.9821", "note": "standard Normal CDF"},
            {"symbol": "α", "value": "0.05", "note": "significance level"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write the two-sided p-value as 2[1 − Φ(|z|)] before substituting."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Upper-tail probability",
                "attempt_cue": "Compute 1 − Φ(2.1).",
                "explanation": "For a continuous symmetric null, the one-sided tail is 1 − Φ(|z|).",
                "calculation": "1 − 0.9821 = 0.0179",
                "result": "1 − Φ(2.1) = 0.0179",
            },
            {
                "id": "S2",
                "label": "Two-sided p-value",
                "attempt_cue": "Double the one-sided tail.",
                "explanation": (
                    "A two-sided alternative charges both tails; the p-value is "
                    "twice the one-sided tail probability."
                ),
                "calculation": "p = 2 × 0.0179 = 0.0358",
                "result": "p = 0.0358",
            },
            {
                "id": "S3",
                "label": "Decision at α = 0.05",
                "attempt_cue": "Compare p with α.",
                "explanation": "Reject H₀ when p ≤ α. Here p = 0.0358 < 0.05.",
                "calculation": "0.0358 < 0.05  ⇒  reject H₀",
                "result": "Reject H₀ at 5%",
            },
        ],
        "final_answer": (
            "Two-sided p-value = 0.0358; reject H₀: μ = £10,000 at α = 0.05."
        ),
        "common_pitfall": (
            "Reporting only the one-sided tail 0.0179 as the p-value for a "
            "two-sided alternative, or comparing z to α directly (2.1 vs 0.05)."
        ),
        "syllabus_ref": "3.3.1",
    },
    "3.3.2-basic-tests-cs1012.json": {
        "title": "One-sample z-test for mean repair cost",
        "problem_statement": (
            "Test H₀: μ = £500 vs H₁: μ ≠ £500 for mean repair cost. A sample "
            "of n = 36 repairs has x̄ = £520. Assume Normal data with known "
            "σ = £60. Compute the z statistic and the two-sided p-value using "
            "Φ(2.0) = 0.9772. Decide at α = 0.05."
        ),
        "given": [
            {"symbol": "μ₀", "value": "500", "note": "null mean (£)"},
            {"symbol": "n, x̄, σ", "value": "36, 520, 60", "note": "sample and known SD"},
            {"symbol": "Φ(2.0)", "value": "0.9772", "note": "standard Normal CDF"},
            {"symbol": "α", "value": "0.05", "note": "significance level"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write z = (x̄ − μ₀)/(σ/√n) before looking up the p-value."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Standard error and z",
                "attempt_cue": "Compute σ/√n and then z.",
                "explanation": "One-sample z-test standardises the sample mean under H₀.",
                "calculation": "σ/√n = 60/6 = 10;  z = (520 − 500)/10 = 20/10 = 2",
                "result": "z = 2",
            },
            {
                "id": "S2",
                "label": "Two-sided p-value",
                "attempt_cue": "Compute 2[1 − Φ(2)].",
                "explanation": "Two-sided alternative doubles the upper tail.",
                "calculation": "1 − 0.9772 = 0.0228;  p = 2 × 0.0228 = 0.0456",
                "result": "p = 0.0456",
            },
            {
                "id": "S3",
                "label": "Decision",
                "attempt_cue": "Compare p with 0.05.",
                "explanation": "Reject H₀ when p ≤ α.",
                "calculation": "0.0456 < 0.05  ⇒  reject H₀",
                "result": "Reject H₀ at 5%",
            },
        ],
        "final_answer": "z = 2; p = 0.0456; reject H₀: μ = £500 at α = 0.05.",
        "common_pitfall": (
            "Using (x̄ − μ₀)/σ = 20/60 ≈ 0.33 instead of dividing by σ/√n = 10, "
            "which collapses the test statistic toward zero."
        ),
        "syllabus_ref": "3.3.2",
    },
    "3.3.3-permutation-tests-cs1012.json": {
        "title": "Exact permutation test for two claim groups",
        "problem_statement": (
            "Small claim samples (£00): Group A = {10, 12, 14}, Group B = {8, 9, 11}. "
            "Test H₀: the two groups share the same distribution, using the "
            "two-sided permutation statistic |x̄_A − x̄_B|. Enumerate all "
            "C(6,3) = 20 assignments of three labels to A. The observed "
            "|x̄_A − x̄_B| equals 8/3. Exactly 4 of the 20 permutations have "
            "|diff| ≥ 8/3. Report the exact permutation p-value."
        ),
        "given": [
            {"symbol": "A", "value": "{10, 12, 14}", "note": "group A claims (£00)"},
            {"symbol": "B", "value": "{8, 9, 11}", "note": "group B claims (£00)"},
            {"symbol": "C(6,3)", "value": "20", "note": "number of label assignments"},
            {"symbol": "# extreme", "value": "4", "note": "permutations with |diff| ≥ observed"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Compute the observed |x̄_A − x̄_B|, then form p = (# extreme)/20."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Observed difference",
                "attempt_cue": "Compute |mean(A) − mean(B)|.",
                "explanation": "The permutation test needs the observed value of the chosen statistic.",
                "calculation": "x̄_A = 36/3 = 12;  x̄_B = 28/3 ≈ 9.333;  |12 − 28/3| = 8/3 ≈ 2.667",
                "result": "|x̄_A − x̄_B| = 8/3",
            },
            {
                "id": "S2",
                "label": "Exact p-value",
                "attempt_cue": "Divide the number of extreme permutations by 20.",
                "explanation": (
                    "Under H₀ every assignment of three labels to A is equally "
                    "likely; the p-value is the proportion at least as extreme "
                    "as observed."
                ),
                "calculation": "p = 4/20 = 0.2",
                "result": "p = 0.2",
            },
            {
                "id": "S3",
                "label": "Decision at α = 0.05",
                "attempt_cue": "Compare p with 0.05.",
                "explanation": "Do not reject H₀ when p > α.",
                "calculation": "0.2 > 0.05  ⇒  do not reject H₀",
                "result": "Do not reject H₀ at 5%",
            },
        ],
        "final_answer": (
            "Observed |x̄_A − x̄_B| = 8/3; exact permutation p-value = 0.2; "
            "do not reject H₀ at α = 0.05."
        ),
        "common_pitfall": (
            "Computing a two-sample t p-value on n = 3 per group and treating it "
            "as the permutation p-value, or reporting 4/C(6,3) incorrectly as "
            "4/15 by mixing combinations with permutations of a different size."
        ),
        "syllabus_ref": "3.3.3",
    },
    "3.3.4-chi-square-gof-cs1012.json": {
        "title": "Chi-square GOF for equal claim-type shares",
        "problem_statement": (
            "n = 100 claims are classified into five product types. Under H₀ "
            "each type has probability 1/5, so expected counts are 20. Observed "
            "counts: 18, 22, 20, 15, 25. Compute Pearson's χ² and decide at "
            "α = 0.05 using χ²_{4, 0.95} = 9.488."
        ),
        "given": [
            {"symbol": "Oᵢ", "value": "18, 22, 20, 15, 25", "note": "observed counts"},
            {"symbol": "Eᵢ", "value": "20", "note": "common expected count under H₀"},
            {"symbol": "df", "value": "4", "note": "5 − 1 categories"},
            {"symbol": "χ²_{4,0.95}", "value": "9.488", "note": "5% critical value"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write χ² = Σ(Oᵢ − Eᵢ)²/Eᵢ before summing."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Squared Pearson residuals",
                "attempt_cue": "Compute each (Oᵢ − 20)²/20.",
                "explanation": "Each category contributes (O − E)²/E to the Pearson statistic.",
                "calculation": (
                    "(−2)²/20 + 2²/20 + 0/20 + (−5)²/20 + 5²/20 "
                    "= 4/20 + 4/20 + 0 + 25/20 + 25/20"
                ),
                "result": "0.2 + 0.2 + 0 + 1.25 + 1.25",
            },
            {
                "id": "S2",
                "label": "Sum to χ²",
                "attempt_cue": "Add the five contributions.",
                "explanation": "The GOF statistic is the sum of the category contributions.",
                "calculation": "0.2 + 0.2 + 0 + 1.25 + 1.25 = 2.9",
                "result": "χ² = 2.9",
            },
            {
                "id": "S3",
                "label": "Decision",
                "attempt_cue": "Compare 2.9 with 9.488.",
                "explanation": "Reject H₀ for large χ²; here 2.9 < 9.488.",
                "calculation": "2.9 < 9.488  ⇒  do not reject H₀",
                "result": "Do not reject equal shares at 5%",
            },
        ],
        "final_answer": "χ² = 2.9 on 4 df; do not reject H₀ at α = 0.05.",
        "common_pitfall": (
            "Using df = 5 (forgetting −1 for the multinomial constraint) or "
            "comparing χ² to a Normal z critical value."
        ),
        "syllabus_ref": "3.3.4",
    },
    "3.3.5-contingency-independence-cs1012.json": {
        "title": "Chi-square test of independence in a 2×2 fraud table",
        "problem_statement": (
            "Claims are cross-classified by channel and fraud flag:\n"
            "Online & Fraud 20; Online & Clean 30; Broker & Fraud 10; "
            "Broker & Clean 40. Row totals 50 and 50; column totals 30 and 70; "
            "n = 100. Test independence at α = 0.05 using χ²_{1, 0.95} = 3.841."
        ),
        "given": [
            {"symbol": "table", "value": "20, 30 / 10, 40", "note": "Online then Broker rows"},
            {"symbol": "margins", "value": "rows 50,50; cols 30,70; n=100", "note": "totals"},
            {"symbol": "χ²_{1,0.95}", "value": "3.841", "note": "5% critical value"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Compute expected counts E_{ij} = (row × col)/n before χ²."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Expected counts",
                "attempt_cue": "Compute all four E_{ij} = (row total × column total)/n.",
                "explanation": "Under independence, expected cell counts factor through the margins.",
                "calculation": (
                    "E11 = 50×30/100 = 15;  E12 = 50×70/100 = 35;  "
                    "E21 = 50×30/100 = 15;  E22 = 50×70/100 = 35"
                ),
                "result": "E = 15, 35 / 15, 35",
            },
            {
                "id": "S2",
                "label": "Pearson χ²",
                "attempt_cue": "Sum (O − E)²/E over the four cells.",
                "explanation": "Same Pearson form as GOF, applied to the contingency table.",
                "calculation": (
                    "(20−15)²/15 + (30−35)²/35 + (10−15)²/15 + (40−35)²/35 "
                    "= 25/15 + 25/35 + 25/15 + 25/35 = 50/15 + 50/35 "
                    "= 10/3 + 10/7 = 100/21 ≈ 4.762"
                ),
                "result": "χ² = 100/21 ≈ 4.762",
            },
            {
                "id": "S3",
                "label": "Decision",
                "attempt_cue": "Compare 4.762 with 3.841.",
                "explanation": "Reject independence when χ² exceeds the df = 1 critical value.",
                "calculation": "4.762 > 3.841  ⇒  reject independence",
                "result": "Reject independence at 5%",
            },
        ],
        "final_answer": (
            "χ² = 100/21 ≈ 4.762 on 1 df; reject independence of channel and "
            "fraud flag at α = 0.05."
        ),
        "common_pitfall": (
            "Using E_{ij} = n/4 = 25 (ignoring unequal margins) or forgetting "
            "to square (O − E) before dividing by E."
        ),
        "syllabus_ref": "3.3.5",
    },
    # ------------------------------------------------------------------
    # Pi Memory Front (distinct scenarios from Kappa/Lambda/Mu learning days)
    # ------------------------------------------------------------------
    "cp-3.1.1-estimators-cs1016.json": {
        "title": "MoM for Poisson claim counts",
        "problem_statement": (
            "Six independent monthly claim counts on a small commercial book "
            "are modelled as Poisson(λ): 2, 1, 3, 0, 4, 2. Construct the "
            "method-of-moments estimator of λ and evaluate it on this sample."
        ),
        "given": [
            {"symbol": "x₁…x₆", "value": "2, 1, 3, 0, 4, 2", "note": "monthly claim counts"},
            {"symbol": "n", "value": "6", "note": "months"},
            {"symbol": "E[X]", "value": "λ", "note": "Poisson mean"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Equate the Poisson mean λ to the sample mean before computing."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Moment equation",
                "attempt_cue": "Write λ̂_MoM = x̄.",
                "explanation": "Poisson has E[X] = λ, so MoM matches λ to the sample mean.",
                "calculation": "E[X] = λ  ⇒  λ̂_MoM = x̄",
                "result": "λ̂_MoM = x̄",
            },
            {
                "id": "S2",
                "label": "Evaluate on the sample",
                "attempt_cue": "Average the six counts.",
                "explanation": "Substitute the observed counts into x̄.",
                "calculation": "(2+1+3+0+4+2)/6 = 12/6 = 2",
                "result": "λ̂_MoM = 2",
            },
        ],
        "final_answer": "λ̂_MoM = x̄ = 2 claims per month.",
        "common_pitfall": (
            "Equating λ to the sample variance (here also 2 by chance) as if that "
            "were a second-moment MoM step required for one-parameter Poisson, "
            "or reporting Σxᵢ = 12 as the estimate of λ."
        ),
        "syllabus_ref": "3.1.1",
    },
    "cp-3.2.1-ci-sample-cs1016.json": {
        "title": "95% z-interval for mean premium",
        "problem_statement": (
            "A random sample of n = 100 household premiums has x̄ = £450. "
            "Model premiums as Normal with known σ = £50. Construct a 95% "
            "confidence interval for the mean premium μ."
        ),
        "given": [
            {"symbol": "n", "value": "100", "note": "sample size"},
            {"symbol": "x̄", "value": "450", "note": "sample mean (£)"},
            {"symbol": "σ", "value": "50", "note": "known SD (£)"},
            {"symbol": "z_{0.975}", "value": "1.96", "note": "standard Normal quantile"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Write x̄ ± 1.96 σ/√n with √100 = 10."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Standard error",
                "attempt_cue": "Compute 50/10.",
                "explanation": "SE of the sample mean with known σ is σ/√n.",
                "calculation": "50 / 10 = 5",
                "result": "SE = 5",
            },
            {
                "id": "S2",
                "label": "Half-width and interval",
                "attempt_cue": "Compute 450 ± 1.96 × 5.",
                "explanation": "95% z-interval centres at x̄.",
                "calculation": "1.96 × 5 = 9.8;  450 − 9.8 = 440.2;  450 + 9.8 = 459.8",
                "result": "(440.2, 459.8)",
            },
        ],
        "final_answer": "95% CI for μ: (£440.2, £459.8).",
        "common_pitfall": (
            "Using 1.96 × 50 = 98 as the half-width (forgetting /√n), which "
            "yields the nonsensical interval (352, 548) for a mean of 450 with "
            "n = 100."
        ),
        "syllabus_ref": "3.2.1",
    },
    "cp-3.3.1-hypothesis-testing-cs1016.json": {
        "title": "Type I / Type II counts from a fraud screen",
        "problem_statement": (
            "A fraud screen is run on 1,000 claims. Truth vs decision: "
            "200 truly fraudulent claims, of which 40 are missed (flagged clean); "
            "800 truly clean claims, of which 24 are falsely flagged as fraud. "
            "Taking H₀: claim is clean, compute the empirical Type I error rate "
            "and Type II error rate from these counts."
        ),
        "given": [
            {"symbol": "n_clean", "value": "800", "note": "truly clean claims"},
            {"symbol": "false flags", "value": "24", "note": "clean flagged as fraud"},
            {"symbol": "n_fraud", "value": "200", "note": "truly fraudulent claims"},
            {"symbol": "misses", "value": "40", "note": "fraud flagged clean"},
        ],
        "attempt_before_reveal": (
            "CMP closed. Recall Type I = reject H₀ when H₀ true; Type II = fail to "
            "reject H₀ when H₀ false, with H₀: clean."
        ),
        "steps": [
            {
                "id": "S1",
                "label": "Type I error rate",
                "attempt_cue": "False fraud flags divided by truly clean claims.",
                "explanation": (
                    "Type I error is a false rejection of H₀. With H₀: clean, "
                    "that is flagging a clean claim as fraud."
                ),
                "calculation": "24 / 800 = 0.03",
                "result": "Type I rate = 0.03",
            },
            {
                "id": "S2",
                "label": "Type II error rate",
                "attempt_cue": "Missed frauds divided by truly fraudulent claims.",
                "explanation": (
                    "Type II error is failing to reject H₀ when the claim is "
                    "fraudulent (H₀ false)."
                ),
                "calculation": "40 / 200 = 0.20",
                "result": "Type II rate = 0.20",
            },
            {
                "id": "S3",
                "label": "Power (optional check)",
                "attempt_cue": "Power = 1 − Type II rate.",
                "explanation": "Power is the probability of correctly flagging fraud.",
                "calculation": "1 − 0.20 = 0.80",
                "result": "Power = 0.80",
            },
        ],
        "final_answer": (
            "Type I error rate = 0.03; Type II error rate = 0.20; power = 0.80."
        ),
        "common_pitfall": (
            "Swapping the denominators: dividing 24 by 200 or 40 by 800, which "
            "swaps Type I and Type II, or treating 24/1000 as the Type I rate."
        ),
        "syllabus_ref": "3.3.1",
    },
}


# Catalogue inventory key -> campaign twin relative path under educational_campaigns/cs1/
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


def _inject(pkg: dict[str, Any], example: dict[str, Any]) -> None:
    """Insert or replace top-level worked_example (after reading_guidance)."""
    pkg["worked_example"] = example


def sync_catalogue_twins(root: Path | None = None) -> int:
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    updated = 0
    for inv_key, example in WORKED_EXAMPLES.items():
        path = catalogue_dir / inv_key
        if not path.exists():
            raise FileNotFoundError(path)
        pkg = json.loads(path.read_text(encoding="utf-8"))
        _inject(pkg, example)
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def sync_campaign_twins(root: Path | None = None) -> int:
    repo = root or Path(__file__).resolve().parents[1]
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    updated = 0
    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        path = campaign_dir / rel_path
        if not path.exists():
            raise FileNotFoundError(path)
        pkg = json.loads(path.read_text(encoding="utf-8"))
        _inject(pkg, WORKED_EXAMPLES[inv_key])
        path.write_text(
            json.dumps(pkg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        updated += 1
    return updated


def mechanical_defect_scan(root: Path | None = None) -> list[str]:
    repo = root or Path(__file__).resolve().parents[1]
    catalogue_dir = repo / "app/curriculum/data/educational_packages/cs1"
    campaign_dir = repo / "app/curriculum/data/educational_campaigns/cs1"
    meta_patterns = [
        re.compile(pattern, re.IGNORECASE)
        for pattern in (
            r"\bcampaign\b",
            r"\bjourney\b",
            r"Batch \d",
            r"Wave \d",
            r"Isolated Golden Day",
            r"spine claims",
            r"Memory Front finished",
        )
    ]
    required_keys = {
        "title",
        "problem_statement",
        "given",
        "attempt_before_reveal",
        "steps",
        "final_answer",
        "common_pitfall",
        "syllabus_ref",
    }
    step_keys = {"id", "label", "attempt_cue", "explanation", "calculation", "result"}
    defects: list[str] = []

    for inv_key, rel_path in CAMPAIGN_TWINS.items():
        paths = [catalogue_dir / inv_key, campaign_dir / rel_path]
        # Twin equality
        blobs = []
        for path in paths:
            if not path.exists():
                defects.append(f"MISSING: {path}")
                continue
            pkg = json.loads(path.read_text(encoding="utf-8"))
            we = pkg.get("worked_example")
            if not isinstance(we, dict):
                defects.append(f"{path.name}: worked_example missing")
                continue
            blobs.append(json.dumps(we, sort_keys=True, ensure_ascii=False))
            missing = required_keys - set(we)
            if missing:
                defects.append(f"{path.name}: missing keys {sorted(missing)}")
            if "\u2014" in json.dumps(we, ensure_ascii=False):
                defects.append(f"{path.name}: em dash found")
            if "\u2013" in json.dumps(we, ensure_ascii=False):
                defects.append(f"{path.name}: en dash found")
            for pattern in meta_patterns:
                if pattern.search(json.dumps(we, ensure_ascii=False)):
                    defects.append(
                        f"{path.name}: meta language '{pattern.pattern}'"
                    )
            if not we.get("steps"):
                defects.append(f"{path.name}: empty steps")
            for step in we.get("steps") or []:
                sk_missing = step_keys - set(step)
                if sk_missing:
                    defects.append(
                        f"{path.name}: step {step.get('id')} missing {sorted(sk_missing)}"
                    )
            for g in we.get("given") or []:
                if not g.get("symbol") or not g.get("value"):
                    defects.append(f"{path.name}: given entry missing symbol/value")
        if len(blobs) == 2 and blobs[0] != blobs[1]:
            defects.append(f"{inv_key}: catalogue/campaign worked_example mismatch")

    if len(WORKED_EXAMPLES) != 22:
        defects.append(f"expected 22 examples, got {len(WORKED_EXAMPLES)}")
    return defects


if __name__ == "__main__":
    assert len(WORKED_EXAMPLES) == 22, len(WORKED_EXAMPLES)
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
        raise SystemExit(1)
    print("Mechanical defect scan: PASS (0 issues)")

#!/usr/bin/env python3
"""Wave 2 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 2 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Reuses Wave 1 conversion helpers; Wave 2-specific EXPLICIT overrides cover
notation families that Wave 1 did not author (bootstrap SE, Empirical Bayes
credibility weights, chi-square pivots, MoM estimators, etc.).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave2.py --dry-run
    python scripts/math_notation_wave2.py --apply
"""

# Mapping keys are verbatim package strings; line length is expected.
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402
import math_notation_wave1 as wave1  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Ledger wave_recommendation.wave_1 after Wave 1 backlog cleared (next tranche).
WAVE2_FILES = (
    "3.2.4-ci-normal-mean-variance-cs1011.json",
    "3.3.4-chi-square-gof-cs1012.json",
    "cp-3.1.1-estimators-cs1016.json",
    "3.1.6-bootstrap-estimator-cs1010.json",
    "5.1.8-empirical-bayes-cs1015.json",
    "5.1.8-empirical-bayes-cs1003.json",
    "cp-2.5.1-clt-cs1016.json",
    "3.1.3-efficiency-bias-consistency-mse-cs1010.json",
    "3.1.5-asymptotic-mle-cs1010.json",
    "4.1.2-simple-multiple-cs1003.json",
    "3.3.5-contingency-independence-cs1012.json",
    "cp-revision-spine-memory-cs1016.json",
)

EXPLICIT: dict[str, str] = {
    "Mean CI via Normal/t pivot; variance CI via chi-square pivot on s².": "Mean CI via Normal/t pivot; variance CI via chi-square pivot on $s^{2}$.",
    "A CI for the mean finishes the requirement; the variance interval uses the same t formula with s² in place of s.": "A CI for the mean finishes the requirement; the variance interval uses the same t formula with $s^{2}$ in place of s.",
    "A CI for σ² is formed as x̄ ± z s/√n, the same centre as the mean interval.": "A CI for $\\sigma^{2}$ is formed as $\\bar{x} \\pm z \\; s/\\sqrt{n}$, the same centre as the mean interval.",
    "Closed-book. IID Normal sample, n=16, x̄=10, s²=4 (σ unknown). Which statement is correct?": "Closed-book. IID Normal sample, n=16, $\\bar{x}$=10, $s^{2}$=4 ($\\sigma$ unknown). Which statement is correct?",
    "For μ use x̄ ± t_{15, 1−α/2} · s/√n. For σ² use ((n−1)s² / χ²_{15, 1−α/2}, (n−1)s² / χ²_{15, α/2}). Both forms are required; a binomial interval is a different setting.": "For $\\mu$ use $\\bar{x} \\pm t_{15, 1-\\alpha/2} \\cdot s/\\sqrt{n}$. For $\\sigma^{2}$ use $((n-1)s^{2} / \\chi^{2}_{15, 1-\\alpha/2}, (n-1)s^{2} / \\chi^{2}_{15, \\alpha/2})$. Both forms are required; a binomial interval is a different setting.",
    "For μ use x̄ ± z_{1−α/2} · s/√n with z even though σ is unknown; the variance CI can be skipped once the mean CI is written.": "For $\\mu$ use $\\bar{x} \\pm z_{1-\\alpha/2} \\cdot s/\\sqrt{n}$ with z even though $\\sigma$ is unknown; the variance CI can be skipped once the mean CI is written.",
    "For μ use x̄ ± t_{15, 1−α/2} · s/√n, and for σ² reuse that same numerical interval because variance intervals share the mean endpoints.": "For $\\mu$ use $\\bar{x} \\pm t_{15, 1-\\alpha/2} \\cdot s/\\sqrt{n}$, and for $\\sigma^{2}$ reuse that same numerical interval because variance intervals share the mean endpoints.",
    "For σ² use (s² − z s/√n, s² + z s/√n), centred at s² with Normal mean SE.": "For $\\sigma^{2}$ use ($s^{2} - z \\; s/\\sqrt{n}$, $s^{2} + z \\; s/\\sqrt{n}$), centred at $s^{2}$ with Normal mean SE.",
    "CMP closed. Write x̄ ± t_{n−1} s/√n with n−1 = 15 before substituting.": "CMP closed. Write $\\bar{x} \\pm t_{n-1}\\, s/\\sqrt{n}$ with $n-1 = 15$ before substituting.",
    "Compute s/√n with √16 = 4.": "Compute $s/\\sqrt{n}$ with $\\sqrt{16}$ = 4.",
    "95% CI for μ: (£96.8035, £103.1965).": "95% CI for $\\mu$: (£96.8035, £103.1965).",
    "E = n × Poisson probabilities at λ̂; DF = bins − 1 − 1; independence ≠ GOF.": "$E = n \\times$ Poisson probabilities at $\\hat{\\lambda}$; DF = bins - 1 - 1; independence $\\neq$ GOF.",
    "Expected frequencies are n times fitted Poisson probabilities using λ̂. Degrees of freedom are (number of bins − 1 − number of estimated parameters), so subtract 1 for λ̂. A chi-square test of independence in a two-way table is a different procedure.": "Expected frequencies are $n$ times fitted Poisson probabilities using $\\hat{\\lambda}$. Degrees of freedom are (number of bins - 1 - number of estimated parameters), so subtract 1 for $\\hat{\\lambda}$. A chi-square test of independence in a two-way table is a different procedure.",
    "Expected frequencies use λ̂, but degrees of freedom stay at (bins − 1) with no reduction for estimating λ.": "Expected frequencies use $\\hat{\\lambda}$, but degrees of freedom stay at (bins - 1) with no reduction for estimating $\\lambda$.",
    "n = 100 claims are classified into five product types. Under H₀ each type has probability 1/5, so expected counts are 20. Observed counts: 18, 22, 20, 15, 25. Compute Pearson's χ² and decide at α = 0.05 using χ²_{4, 0.95} = 9.488.": "n = 100 claims are classified into five product types. Under $H_{0}$ each type has probability $\\frac{1}{5}$, so expected counts are 20. Observed counts: 18, 22, 20, 15, 25. Compute Pearson's $\\chi^{2}$ and decide at $\\alpha$ = 0.05 using $\\chi^{2}_{4, 0.95}$ = 9.488.",
    "CMP closed. Write χ² = Σ(Oᵢ − Eᵢ)²/Eᵢ before summing.": "CMP closed. Write $\\chi^{2} = \\sum (O_{i}-E_{i})^{2}/E_{i}$ before summing.",
    "2.9 < 9.488  ⇒  do not reject H₀": "2.9 < 9.488 $\\Rightarrow$ do not reject $H_{0}$",
    "χ² = 2.9 on 4 df; do not reject H₀ at α = 0.05.": "$\\chi^{2}$ = 2.9 on 4 df; do not reject $H_{0}$ at $\\alpha$ = 0.05.",
    "E[X] = λ  ⇒  λ̂_MoM = x̄": "$E[X] = \\lambda \\Rightarrow \\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$",
    "λ̂_MoM = x̄ = 2 claims per month.": "$\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x} = 2$ claims per month.",
    "E[X] = λ implies λ̂_MoM = x̄. The sample mean is (2 + 1 + 3 + 0 + 4 + 2)/6 = 12/6 = 2, so λ̂_MoM = 2 claims per month.": "$E[X] = \\lambda$ implies $\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$. The sample mean is $(2 + 1 + 3 + 0 + 4 + 2)/6 = 12/6 = 2$, so $\\hat{\\lambda}_{\\mathrm{MoM}} = 2$ claims per month.",
    "Resample without replacement until the resample has size n/2, compute one θ̂*, and take |θ̂* − θ̂| as the standard error.": "Resample without replacement until the resample has size $n/2$, compute one $\\hat{\\theta}^{*}$, and take $|\\hat{\\theta}^{*} - \\hat{\\theta}|$ as the standard error.",
    "A nonparametric bootstrap of the sample mean claim severity produced B = 5 bootstrap replicates (£00): 210, 195, 220, 205, 200. Estimate the bootstrap standard error of the mean using SÊ_boot = √[(1/B) Σ(θ̂*_b − θ̄*)²], where θ̄* is the mean of the bootstrap replicates.": "A nonparametric bootstrap of the sample mean claim severity produced $B = 5$ bootstrap replicates (£00): 210, 195, 220, 205, 200. Estimate the bootstrap standard error of the mean using $\\widehat{\\mathrm{SE}}_{\\mathrm{boot}} = \\sqrt{(1/B)\\sum(\\hat{\\theta}^{*}_{b}-\\bar{\\theta}^{*})^{2}}$, where $\\bar{\\theta}^{*}$ is the mean of the bootstrap replicates.",
    "Compute Σ(θ̂*_b − 206)².": "Compute $\\sum (\\hat{\\theta}^{*}_{b} - 206)^{2}$.",
    "Take √(370/B) with B = 5.": "Take $\\sqrt{370/B}$ with B = 5.",
    "Dividing by B−1 = 4 (ordinary sample SD) to get √(370/4) = √92.5 ≈ 9.62 instead of the bootstrap /B form √(370/5) = √74 required here.": "Dividing by $B-1 = 4$ (ordinary sample SD) to get $\\sqrt{370/4} = \\sqrt{92.5} \\approx 9.62$ instead of the bootstrap /$B$ form $\\sqrt{370/5} = \\sqrt{74}$ required here.",
    "SÊ_boot = √(370/5) = √74 ≈ 8.602": "$\\widehat{\\mathrm{SE}}_{\\mathrm{boot}} = \\sqrt{370/5} = \\sqrt{74} \\approx 8.602$",
    "θ̄* = 206; SÊ_boot = √74 ≈ 8.602 (£00).": "$\\bar{\\theta}^{*} = 206$; $\\widehat{\\mathrm{SE}}_{\\mathrm{boot}} = \\sqrt{74} \\approx 8.602$ (£00).",
    "Under Empirical Bayes, structural parameters are estimated from collective data: μ̂ = £500 and k̂ = 10. A risk has n = 5 years with X̄ = £700. Compute Ẑ = n/(n+k̂) and the EB credibility premium P = Ẑ X̄ + (1 − Ẑ) μ̂.": "Under Empirical Bayes, structural parameters are estimated from collective data: $\\hat{\\mu}$ = £500 and $\\hat{k}$ = 10. A risk has n = 5 years with $\\bar{X}$ = £700. Compute $\\hat{Z}$ = $n/(n+\\hat{k})$ and the EB credibility premium P = $\\hat{Z} \\bar{X} + (1 - \\hat{Z}) \\hat{\\mu}$.",
    "Evaluate Ẑ X̄ + (1 − Ẑ) μ̂.": "Evaluate $\\hat{Z} \\bar{X} + (1 - \\hat{Z}) \\hat{\\mu}$.",
    "Structurals μ̂, k̂ from collective data (not a fixed prior)": "Structurals $\\hat{\\mu}$, $\\hat{k}$ from collective data (not a fixed prior)",
    "Ẑ = 1/3; Empirical Bayes premium P = 1700/3 ≈ £566.67.": "$\\hat{Z} = 1/3$; Empirical Bayes premium $P = 1700/3 \\approx$ £566.67.",
    "Under Empirical Bayes, structural parameters are estimated from collective data: μ̂ = £900 and k̂ = 6. A risk has n = 3 years with X̄ = £1200. Compute Ẑ = n/(n+k̂) and the EB credibility premium P = Ẑ X̄ + (1 − Ẑ)μ̂.": "Under Empirical Bayes, structural parameters are estimated from collective data: $\\hat{\\mu}$ = £900 and $\\hat{k}$ = 6. A risk has n = 3 years with $\\bar{X}$ = £1200. Compute $\\hat{Z}$ = $n/(n+\\hat{k})$ and the EB credibility premium P = $\\hat{Z} \\bar{X} + (1 - \\hat{Z})\\hat{\\mu}$.",
    "CMP closed. Form Ẑ from n and k̂ before mixing X̄ with μ̂.": "CMP closed. Form $\\hat{Z}$ from n and $\\hat{k}$ before mixing $\\bar{X}$ with $\\hat{\\mu}$.",
    "Compute Ẑ X̄ + (1 − Ẑ)μ̂.": "Compute $\\hat{Z} \\bar{X} + (1 - \\hat{Z})\\hat{\\mu}$.",
    "State the source of μ̂ and k̂.": "State the source of $\\hat{\\mu}$ and $\\hat{k}$.",
    "Treating μ̂ and k̂ as if they were known prior structurals (fully Bayesian), or using Z = k̂/(n+k̂).": "Treating $\\hat{\\mu}$ and $\\hat{k}$ as if they were known prior structurals (fully Bayesian), or using Z = $\\hat{k}/(n+\\hat{k})$.",
    "μ̂, k̂ from collective data (not a fully specified prior)": "$\\hat{\\mu}$, $\\hat{k}$ from collective data (not a fully specified prior)",
    "IID, finite mean/variance → sample mean ≈ Normal for large n.": "IID, finite mean/variance $\\Rightarrow$ sample mean $\\approx$ Normal for large n.",
    "The CLT approximates the distribution of a single observation X₁ as Normal whenever the population has a finite mean, regardless of sample size.": "The CLT approximates the distribution of a single observation $X_{1}$ as Normal whenever the population has a finite mean, regardless of sample size.",
    "Closed-book. Repair costs are iid with mean μ = 1200 and standard deviation σ = 300. A sample of n = 36 repairs is drawn. Using the CLT and Φ(1) ≈ 0.841, approximate P(X̄ < 1150). Enter the probability as a decimal.": "Closed-book. Repair costs are iid with mean $\\mu = 1200$ and standard deviation $\\sigma = 300$. A sample of $n = 36$ repairs is drawn. Using the CLT and $\\Phi(1) \\approx 0.841$, approximate $P(\\bar{X} < 1150)$. Enter the probability as a decimal.",
    "sd(X̄) = σ/√n = 300/√36 = 50, so z = (1150 - 1200)/50 = -1 and P(X̄ < 1150) ≈ Φ(-1) = 1 - Φ(1) ≈ 1 - 0.841 = 0.159.": "$\\operatorname{sd}(\\bar{X}) = \\sigma/\\sqrt{n} = 300/\\sqrt{36} = 50$, so $z = (1150 - 1200)/50 = -1$ and $P(\\bar{X} < 1150) \\approx \\Phi(-1) = 1 - \\Phi(1) \\approx 1 - 0.841 = 0.159$.",
    "Using σ = 300 instead of σ/√n = 50 so that z = -1/6, or reporting Φ(1) ≈ 0.841 as the lower-tail probability itself.": "Using $\\sigma = 300$ instead of $\\sigma/\\sqrt{n} = 50$ so that $z = -1/6$, or reporting $\\Phi(1) \\approx 0.841$ as the lower-tail probability itself.",
    "Repair costs are iid with mean μ = 1200 and standard deviation σ = 300. A sample of n = 36 repairs is drawn. Using the CLT, approximate P(X̄ < 1150). Use Φ(1) ≈ 0.841.": "Repair costs are iid with mean $\\mu = 1200$ and standard deviation $\\sigma = 300$. A sample of $n = 36$ repairs is drawn. Using the CLT, approximate $P(\\bar{X} < 1150)$. Use $\\Phi(1) \\approx 0.841$.",
    "Using X̄ ≈ Normal(1200, 300) and computing z = (1150 − 1200)/300 = −1/6, or reading Φ(1) ≈ 0.841 as the lower-tail probability itself.": "Using $\\bar{X} \\approx \\operatorname{Normal}(1200, 300)$ and computing $z = (1150 - 1200)/300 = -1/6$, or reading $\\Phi(1) \\approx 0.841$ as the lower-tail probability itself.",
    "σ/√n = 300 / √36 = 300 / 6 = 50": "$\\sigma/\\sqrt{n}$ = 300 / $\\sqrt{36}$ = 300 / 6 = 50",
    "z = (1150 − 1200)/50 = −1; P(X̄ < 1150) ≈ Φ(−1) = 1 − Φ(1) ≈ 1 − 0.841 = 0.159": "$z = (1150 - 1200)/50 = -1$; $P(\\bar{X} < 1150) \\approx \\Phi(-1) = 1 - \\Phi(1) \\approx 1 - 0.841 = 0.159$",
    "sd(X̄) = 50, not σ = 300": "$\\operatorname{sd}(\\bar{X})$ = 50, not $\\sigma$ = 300",
    "Must divide σ by √n": "Must divide $\\sigma$ by $\\sqrt{n}$",
    "X̄ ≈ Normal(1200, 50); z = −1; P(X̄ < 1150) ≈ 0.159. Casual Normal use without stating the IID CLT sampling sd is not the same skill.": "$\\bar{X} \\approx \\operatorname{Normal}(1200, 50)$; $z = -1$; $P(\\bar{X} < 1150) \\approx 0.159$. Casual Normal use without stating the IID CLT sampling sd is not the same skill.",
    "Bias is E[θ̂] − θ and MSE = variance + squared bias. Consistency is large-sample concentration on the truth, not the same as finite-sample unbiasedness. Efficiency is a comparative variance/MSE idea, not a synonym for unbiasedness.": "Bias is $E[\\hat{\\theta}] - \\theta$ and MSE = variance + squared bias. Consistency is large-sample concentration on the truth, not the same as finite-sample unbiasedness. Efficiency is a comparative variance/MSE idea, not a synonym for unbiasedness.",
    "Bias = E[θ̂] − θ; MSE = Var + bias²; efficiency compares variance/MSE; consistency is convergence in probability.": "Bias $= E[\\hat{\\theta}] - \\theta$; MSE $= \\operatorname{Var} + (\\mathrm{bias})^{2}$; efficiency compares variance or MSE; consistency is convergence in probability.",
    "Bias is E[θ̂] − θ. Under the usual decomposition, MSE = Var(θ̂) + (bias)². Efficiency compares variance or MSE to a benchmark; consistency concerns convergence in probability to the true value as sample size grows.": "Bias is $E[\\hat{\\theta}] - \\theta$. Under the usual decomposition, MSE $= \\operatorname{Var}(\\hat{\\theta}) + (\\mathrm{bias})^{2}$. Efficiency compares variance or MSE to a benchmark; consistency concerns convergence in probability to the true value as sample size grows.",
    "MSE = Var(θ̂) − (bias)², so a larger bias always reduces MSE.": "MSE $= \\operatorname{Var}(\\hat{\\theta}) - (\\mathrm{bias})^{2}$, so a larger bias always reduces MSE.",
    "MSE(A)=4/n. MSE(B)=bias² + var = 1/n² + 1/n, which is about 1/n for large n and beats 4/n. A biased estimator can win on MSE. Consistency is large-sample concentration, not finite-sample unbiasedness.": "$\\operatorname{MSE}(A)=\\frac{4}{n}$. $\\operatorname{MSE}(B)=(\\mathrm{bias})^{2} + \\mathrm{var} = \\frac{1}{n^{2}} + \\frac{1}{n}$, which is about $\\frac{1}{n}$ for large $n$ and beats $\\frac{4}{n}$. A biased estimator can win on MSE. Consistency is large-sample concentration, not finite-sample unbiasedness.",
    "MSE(A)=4/n; MSE(B)=1/n²+1/n; prefer B for large n on MSE; refuse unbiased-always-best and consistency=unbiasedness.": "$\\operatorname{MSE}(A)$=$\\frac{4}{n}$; $\\operatorname{MSE}(B)$=$\\frac{1}{n^{2}}$+$\\frac{1}{n}$; prefer B for large n on MSE; refuse unbiased-always-best and consistency=unbiasedness.",
    "MSE(A)=4/n and MSE(B)=1/n² + 1/n. For large n, MSE(B)≈1/n < 4/n, so B has smaller MSE. Unbiasedness is not MSE optimality, and consistency is not the same as unbiasedness.": "$\\operatorname{MSE}(A)$=$\\frac{4}{n}$ and $\\operatorname{MSE}(B)$=$\\frac{1}{n^{2}}$ + $\\frac{1}{n}$. For large n, $\\operatorname{MSE}(B) \\approx \\frac{1}{n}$ < $\\frac{4}{n}$, so B has smaller MSE. Unbiasedness is not MSE optimality, and consistency is not the same as unbiasedness.",
    "MSE(A)=4/n and MSE(B)=(1/n)² = 1/n² only (variance is ignored when bias is present), so B is preferred for all n.": "$\\operatorname{MSE}(A)=\\frac{4}{n}$ and $\\operatorname{MSE}(B)=(\\frac{1}{n})^{2} = \\frac{1}{n^{2}}$ only (variance is ignored when bias is present), so B is preferred for all $n$.",
    "CMP closed. Write Bias(θ̂) = E[θ̂] − θ and MSE = Var + Bias² before computing.": "CMP closed. Write $\\operatorname{Bias}(\\hat{\\theta}) = E[\\hat{\\theta}] - \\theta$ and $\\mathrm{MSE} = \\operatorname{Var} + \\mathrm{Bias}^{2}$ before computing.",
    "Bias(A) = E[A] − μ and Bias(B) = E[B] − μ.": "$\\operatorname{Bias}(A) = E[A] - \\mu$ and $\\operatorname{Bias}(B) = E[B] - \\mu$.",
    "Bias is the systematic error E[θ̂] − θ. Unbiased means Bias = 0.": "Bias is the systematic error $E[\\hat{\\theta}] - \\theta$. Unbiased means Bias = 0.",
    "Use MSE(θ̂) = Var(θ̂) + [Bias(θ̂)]².": "Use $\\operatorname{MSE}(\\hat{\\theta}) = \\operatorname{Var}(\\hat{\\theta}) + [\\operatorname{Bias}(\\hat{\\theta})]^{2}$.",
    "Closed-book. Under regularity, an MLE θ̂ₙ satisfies √n (θ̂ₙ − θ) →ᵈ N(0, 1/I(θ)). Which statement is correct?": "Closed-book. Under regularity, an MLE $\\hat{\\theta}_{n}$ satisfies $\\sqrt{n} (\\hat{\\theta}_{n} - \\theta) \\xrightarrow{d} N(0, 1/I(\\theta))$. Which statement is correct?",
    "The √n-scaled error is asymptotically N(0, 1/I(θ)), so θ̂ₙ is approx Normal with variance 1/(n I(θ)). Bootstrap is a different tool and does not erase the asymptotic claim. Dropping √n misstates the limit.": "The $\\sqrt{n}$-scaled error is asymptotically $N(0, 1/I(\\theta))$, so $\\hat{\\theta}_{n}$ is approx Normal with variance $1/(n I(\\theta))$. Bootstrap is a different tool and does not erase the asymptotic claim. Dropping $\\sqrt{n}$ misstates the limit.",
    "Large-sample Normal law with variance ≈ 1/(n I(θ)); bootstrap ≠ asymptotic MLE theory.": "Large-sample Normal law with variance $\\approx 1/(n I(\\theta))$; bootstrap $\\neq$ asymptotic MLE theory.",
    "For large n, θ̂ₙ is approximately Normal about θ with variance ≈ 1/(n I(θ)), which supports large-sample standard errors and Wald-type intervals or tests. Bootstrap resampling estimates properties by redrawing the sample; it does not replace stating this asymptotic distribution.": "For large n, $\\hat{\\theta}_{n}$ is approximately Normal about $\\theta$ with variance $\\approx 1/(n I(\\theta))$, which supports large-sample standard errors and Wald-type intervals or tests. Bootstrap resampling estimates properties by redrawing the sample; it does not replace stating this asymptotic distribution.",
    "The result says Var(θ̂ₙ) = I(θ) exactly for every finite n, so no large-sample approximation is involved.": "The result says $\\operatorname{Var}(\\hat{\\theta}_{n})$ = $I(\\theta)$ exactly for every finite n, so no large-sample approximation is involved.",
    "The result implies θ̂ₙ →ᵈ N(0, 1/I(θ)) without the √n scaling, so the variance of θ̂ₙ itself tends to 1/I(θ).": "The result implies $\\hat{\\theta}_{n} \\xrightarrow{d} N(0, 1/I(\\theta))$ without the $\\sqrt{n}$ scaling, so the variance of $\\hat{\\theta}_{n}$ itself tends to $1/I(\\theta)$.",
    "From n = 64 independent Exponential claim delays with rate λ, the MLE is λ̂ = 0.25. Using the asymptotic Normal approximation λ̂ ≈ N(λ, λ²/n) (equivalently SE ≈ λ̂/√n), give the estimated standard error and an approximate 95% confidence interval for λ.": "From $n = 64$ independent Exponential claim delays with rate $\\lambda$, the MLE is $\\hat{\\lambda} = 0.25$. Using the asymptotic Normal approximation $\\hat{\\lambda} \\approx N(\\lambda, \\lambda^{2}/n)$ (equivalently $\\mathrm{SE} \\approx \\hat{\\lambda}/\\sqrt{n}$), give the estimated standard error and an approximate 95% confidence interval for $\\lambda$.",
    "Compute λ̂/√n with √64 = 8.": "Compute $\\hat{\\lambda}/\\sqrt{n}$ with $\\sqrt{64} = 8$.",
    "For Exponential rate, I(λ) = 1/λ² per observation, so asymptotic variance is λ²/n and SE = λ/√n, plugged in at λ̂.": "For Exponential rate, $I(\\lambda)$ = $1/\\lambda^{2}$ per observation, so asymptotic variance is $\\lambda^{2}/n$ and SE = $\\lambda/\\sqrt{n}$, plugged in at $\\hat{\\lambda}$.",
    "Compute λ̂ ± 1.96 SÊ.": "Compute $\\hat{\\lambda} \\pm 1.96\\,\\widehat{\\mathrm{SE}}$.",
    "Using SE = 1/(λ̂√n) = 1/(0.25×8) = 0.5 (the Exponential-mean information form) instead of SE = λ̂/√n = 0.03125 for the rate.": "Using $\\mathrm{SE} = 1/(\\hat{\\lambda}\\sqrt{n}) = 1/(0.25\\times 8) = 0.5$ (the Exponential-mean information form) instead of $\\mathrm{SE} = \\hat{\\lambda}/\\sqrt{n} = 0.03125$ for the rate.",
    "SÊ = 0.03125; approximate 95% CI for λ is (0.18875, 0.31125).": "$\\widehat{\\mathrm{SE}} = 0.03125$; approximate 95% CI for $\\lambda$ is $(0.18875, 0.31125)$.",
    "SÊ = 0.25 / √64 = 0.25 / 8 = 0.03125": "$\\widehat{\\mathrm{SE}} = 0.25 / \\sqrt{64} = 0.25 / 8 = 0.03125$",
    "Closed-book. Which statement correctly writes a simple linear model for Y on X1 and a multiple linear model for Y on X1 and X2 using β notation?": "Closed-book. Which statement correctly writes a simple linear model for Y on X1 and a multiple linear model for Y on X1 and X2 using $\\beta$ notation?",
    "Simple: Y = β0 + β1 X1 + ε. Multiple: Y = β0 + β1 X1 + β2 X2 + ε.": "Simple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\varepsilon$. Multiple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\beta_{2} X_{2} + \\varepsilon$.",
    "Simple: Y = β0 + β1 X1 + ε. Multiple: Y = β0 + β1 X1 + β2 X2 + ε (or equivalent β notation).": "Simple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\varepsilon$. Multiple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\beta_{2} X_{2} + \\varepsilon$ (or equivalent $\\beta$ notation).",
    "Simple: Y = β0 + β1 X1 + β2 X2 + ε. Multiple: Y = β0 + β1 X1 + ε, because multiple means more parameters in the least-squares criterion.": "Simple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\beta_{2} X_{2} + \\varepsilon$. Multiple: $Y = \\beta_{0} + \\beta_{1} X_{1} + \\varepsilon$, because multiple means more parameters in the least-squares criterion.",
    "Simple and multiple models differ only in software menu choice; the equation Y = β0 + β1 X1 + ε covers both one and two predictors.": "Simple and multiple models differ only in software menu choice; the equation $Y = \\beta_{0} + \\beta_{1} X_{1} + \\varepsilon$ covers both one and two predictors.",
    "Simple: Y = β₀ + β₁ age + ε. Multiple adds β₂ sum_insured. Refuse OLS-as-form.": "Simple: $Y = \\beta_{0} + \\beta_{1}\\,\\mathrm{age} + \\varepsilon$. Multiple adds $\\beta_{2}\\,\\mathrm{sum\\_insured}$. Refuse OLS-as-form.",
    "Simple: Y = β₀ + β₁ age + ε. Multiple: Y = β₀ + β₁ age + β₂ sum_insured + ε. Writing least-squares formulae for β̂ is estimation, not stating the simple versus multiple linear model forms.": "Simple: $Y = \\beta_{0} + \\beta_{1}\\,\\mathrm{age} + \\varepsilon$. Multiple: $Y = \\beta_{0} + \\beta_{1}\\,\\mathrm{age} + \\beta_{2}\\,\\mathrm{sum\\_insured} + \\varepsilon$. Writing least-squares formulae for $\\hat{\\beta}$ is estimation, not stating the simple versus multiple linear model forms.",
    "Simple: Y = β₀ + β₁ age + β₂ sum_insured + ε. Multiple: Y = β₀ + β₁ age + ε, because multiple means more parameters in the criterion.": "Simple: $Y = \\beta_{0} + \\beta_{1}\\,\\mathrm{age} + \\beta_{2}\\,\\mathrm{sum\\_insured} + \\varepsilon$. Multiple: $Y = \\beta_{0} + \\beta_{1}\\,\\mathrm{age} + \\varepsilon$, because multiple means more parameters in the criterion.",
    "Two fitted linear models for travel medical claim cost Y (£00) are available.\nSimple: Ŷ_s = 3.5 + 0.8x₁, where x₁ is trip length in weeks.\nMultiple: Ŷ_m = 2.0 + 0.6x₁ + 0.4x₂, where x₂ is a destination risk score.\nFor a trip with x₁ = 5 and x₂ = 3, compute both fitted values and state which model form each equation represents.": "Two fitted linear models for travel medical claim cost Y (£00) are available.\nSimple: $\\hat{Y}_{s}$ = 3.5 + 0.8$x_{1}$, where $x_{1}$ is trip length in weeks.\nMultiple: $\\hat{Y}_{m}$ = 2.0 + 0.6$x_{1}$ + 0.4$x_{2}$, where $x_{2}$ is a destination risk score.\nFor a trip with $x_{1}$ = 5 and $x_{2}$ = 3, compute both fitted values and state which model form each equation represents.",
    "Ŷ_s uses only x₁ (simple); Ŷ_m uses x₁ and x₂ (multiple)": "$\\hat{Y}_{s}$ uses only $x_{1}$ (simple); $\\hat{Y}_{m}$ uses $x_{1}$ and $x_{2}$ (multiple)",
    "Independence uses E_{ij} = (row total × column total)/n in a two-way table. That is not one-sample distributional GOF.": "Independence uses $E_{ij} = (\\text{row total} \\times \\text{column total})/n$ in a two-way table. That is not one-sample distributional GOF.",
    "Two-way cross-classification; independence null; E_{ij}=(row total×column total)/n.": "Two-way cross-classification; independence null; $E_{ij}=(\\text{row total}\\times\\text{column total})/n$.",
    "Closed-book. Two-way table: rating class × claim/no-claim. Which statement is correct?": "Closed-book. Two-way table: rating class $\\times$ claim/no-claim. Which statement is correct?",
    "Independence null; E_{ij}=(row total×column total)/n; refuse GOF conflation.": "Independence null; $E_{ij}=(\\text{row total}\\times\\text{column total})/n$; refuse GOF conflation.",
    "H₀: row and column classifications are independent; E_{ij} = (row i total × column j total) / n. This is not the same as a chi-square GOF testing whether one sample follows a named distribution.": "$H_{0}$: row and column classifications are independent; $E_{ij} = (\\text{row i total} \\times \\text{column j total}) / n$. This is not the same as a chi-square GOF testing whether one sample follows a named distribution.",
    "H₀: the counts follow a Poisson distribution with mean estimated from the table total; expected counts are that fitted Poisson pmf times n.": "$H_{0}$: the counts follow a Poisson distribution with mean estimated from the table total; expected counts are that fitted Poisson pmf times n.",
    "H₀: independence; expected counts equal the observed counts in every cell.": "$H_{0}$: independence; expected counts equal the observed counts in every cell.",
    "H₀: independence; E_{ij} = row i total + column j total, without dividing by n.": "$H_{0}$: independence; $E_{ij}$ = row i total + column j total, without dividing by n.",
    "Claims are cross-classified by channel and fraud flag:\nOnline & Fraud 20; Online & Clean 30; Broker & Fraud 10; Broker & Clean 40. Row totals 50 and 50; column totals 30 and 70; n = 100. Test independence at α = 0.05 using χ²_{1, 0.95} = 3.841.": "Claims are cross-classified by channel and fraud flag:\nOnline & Fraud 20; Online & Clean 30; Broker & Fraud 10; Broker & Clean 40. Row totals 50 and 50; column totals 30 and 70; n = 100. Test independence at $\\alpha$ = 0.05 using $\\chi^{2}_{1, 0.95}$ = 3.841.",
    "CMP closed. Compute expected counts E_{ij} = (row × col)/n before χ².": "CMP closed. Compute expected counts $E_{ij} = (\\text{row} \\times \\text{col})/n$ before $\\chi^{2}$.",
    "Compute all four E_{ij} = (row total × column total)/n.": "Compute all four $E_{ij} = (\\text{row total} \\times \\text{column total})/n$.",
    "χ² = 100/21 ≈ 4.762 on 1 df; reject independence of channel and fraud flag at α = 0.05.": "$\\chi^{2} = 100/21 \\approx 4.762$ on 1 df; reject independence of channel and fraud flag at $\\alpha = 0.05$.",
    "Closed-book. An unbiased estimator T has sampling variance 9/n. What does the central limit theorem add if sqrt(n)(T minus theta) converges to N(0, 9)?": "Closed-book. An unbiased estimator T has sampling variance $\\frac{9}{n}$. What does the central limit theorem add if $\\sqrt{n}$(T minus theta) converges to $N(0, 9)$?",
    "Closed-book retrieval. A method-of-moments estimator sets the sample mean equal to a model mean m(θ). An unbiased estimator T has sampling variance 9/n, and √n(T - θ) converges in distribution to N(0, 9). Distinguish the MoM estimating equation from the estimator's sampling distribution, and state the large-n Normal approximation for T.": "Closed-book retrieval. A method-of-moments estimator sets the sample mean equal to a model mean $m(\\theta)$. An unbiased estimator T has sampling variance $\\frac{9}{n}$, and $\\sqrt{n}$(T - $\\theta$) converges in distribution to $N(0, 9)$. Distinguish the MoM estimating equation from the estimator's sampling distribution, and state the large-n Normal approximation for T.",
    "For large n, T is approximately Normal with mean θ and variance 9/n. Unbiasedness alone does not determine the sampling distribution.": "For large n, T is approximately Normal with mean $\\theta$ and variance $\\frac{9}{n}$. Unbiasedness alone does not determine the sampling distribution.",
    "sample mean = m(θ)": "sample mean = $m(\\theta)$",
    "√n(T - θ) →ᵈ N(0, 9)": "$\\sqrt{n}$(T - $\\theta$) $\\xrightarrow{d}$ $N(0, 9)$",
    "Estimating equation ≠ sampling distribution": "Estimating equation $\\neq$ sampling distribution",
    "T ≈ Normal(θ, 9/n) for large n": "T $\\approx \\operatorname{Normal}(\\theta, 9/n)$ for large n",
    "The MoM equation defines an estimator; the sampling distribution describes that estimator over repeated samples. For large n, T ≈ Normal(θ, 9/n). Unbiasedness alone does not make T exactly Normal for every n.": "The MoM equation defines an estimator; the sampling distribution describes that estimator over repeated samples. For large n, T $\\approx \\operatorname{Normal}(\\theta, 9/n)$. Unbiasedness alone does not make T exactly Normal for every n.",
    "A sample of n = 16 Normal claim amounts has x̄ = £100 and sample SD s = £6. Using t_{15, 0.975} = 2.131, construct a 95% confidence interval for the mean μ (σ unknown).": "A sample of $n = 16$ Normal claim amounts has $\\bar{x} =$ £100 and sample SD $s =$ £6. Using $t_{15, 0.975} = 2.131$, construct a 95% confidence interval for the mean $\\mu$ ($\\sigma$ unknown).",
    "Evaluate λ̂_MoM = x̄ on the stated sample.": "Evaluate $\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$ on the stated sample.",
    "For Poisson(λ), the first-moment equation gives λ̂_MoM = x̄.": "For Poisson($\\lambda$), the first-moment equation gives $\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$.",
    "Closed-book. Six independent monthly claim counts are modelled as Poisson(λ): 2, 1, 3, 0, 4, 2. Enter the method-of-moments estimate of λ.": "Closed-book. Six independent monthly claim counts are modelled as Poisson($\\lambda$): 2, 1, 3, 0, 4, 2. Enter the method-of-moments estimate of $\\lambda$.",
    "Six independent monthly claim counts on a small commercial book are modelled as Poisson(λ): 2, 1, 3, 0, 4, 2. Construct the method-of-moments estimator of λ and evaluate it on this sample.": "Six independent monthly claim counts on a small commercial book are modelled as Poisson($\\lambda$): 2, 1, 3, 0, 4, 2. Construct the method-of-moments estimator of $\\lambda$ and evaluate it on this sample.",
    "Write λ̂_MoM = x̄.": "Write $\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$.",
    "λ̂_MoM = x̄": "$\\hat{\\lambda}_{\\mathrm{MoM}} = \\bar{x}$",
    "λ̂_MoM = 2": "$\\hat{\\lambda}_{\\mathrm{MoM}} = 2$",
    "Equating λ to the sample variance (here also 2 by chance) as if that were a second-moment MoM step required for one-parameter Poisson, or reporting Σxᵢ = 12 as the estimate of λ.": "Equating $\\lambda$ to the sample variance (here also 2 by chance) as if that were a second-moment MoM step required for one-parameter Poisson, or reporting $\\sum x_{i} = 12$ as the estimate of $\\lambda$.",
    "x₁…x₆": "$x_{1},\\ldots,x_{6}$",
    "With-replacement resamples → θ̂* replicates → empirical SD as SE; distinct from asymptotics and from bootstrap CIs.": "With-replacement resamples $\\rightarrow$ $\\hat{\\theta}^{*}$ replicates $\\rightarrow$ empirical SD as SE; distinct from asymptotics and from bootstrap CIs.",
    "Draw many resamples with replacement from the original sample, recompute θ̂* on each resample, and use the empirical standard deviation of the θ̂* values as the SE estimate. That is not the same as quoting an asymptotic Normal law, and not the same as constructing a bootstrap confidence interval.": "Draw many resamples with replacement from the original sample, recompute $\\hat{\\theta}^{*}$ on each resample, and use the empirical standard deviation of the $\\hat{\\theta}^{*}$ values as the SE estimate. That is not the same as quoting an asymptotic Normal law, and not the same as constructing a bootstrap confidence interval.",
    "Compute the asymptotic variance 1/(n I(θ̂)) once; that single plug-in is the bootstrap standard error by definition.": "Compute the asymptotic variance $1/(n I(\\hat{\\theta}))$ once; that single plug-in is the bootstrap standard error by definition.",
    "θ̂*_1…θ̂*_5": "$\\hat{\\theta}^{*}_{1},\\ldots,\\hat{\\theta}^{*}_{5}$",
    "θ̄* = 206": "$\\bar{\\theta}^{*} = 206$",
    "Σ(θ̂*_b − θ̄*)² = 370": "$\\sum(\\hat{\\theta}^{*}_{b} - \\bar{\\theta}^{*})^{2} = 370$",
    "SÊ_boot ≈ 8.602 (£00)": "$\\widehat{\\mathrm{SE}}_{\\mathrm{boot}} \\approx 8.602$ (£00)",
    "Two estimators of mean ultimate claim cost μ (in £000) are under review. Estimator A is unbiased with Var(A) = 25. Estimator B has E[B] = μ + 2 and Var(B) = 16. Compute Bias(B) and MSE for both estimators, and state which has smaller MSE.": "Two estimators of mean ultimate claim cost $\\mu$ (in £000) are under review. Estimator A is unbiased with $\\operatorname{Var}(A) = 25$. Estimator B has $E[B] = \\mu + 2$ and $\\operatorname{Var}(B) = 16$. Compute $\\operatorname{Bias}(B)$ and MSE for both estimators, and state which has smaller MSE.",
    "CMP closed. Write SÊ = λ̂/√n before building the interval.": "CMP closed. Write $\\widehat{\\mathrm{SE}} = \\hat{\\lambda}/\\sqrt{n}$ before building the interval.",
    "SÊ = 0.03125": "$\\widehat{\\mathrm{SE}} = 0.03125$",
}

def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 2 EXPLICIT then Wave 1 helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave1.EXPLICIT:
        return wave1.EXPLICIT[text]
    return wave1.convert_string(text, field_path)


def wave2_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE2_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave2_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE2_FILES:
        packages[fname] = json.loads((CATALOGUE / fname).read_text(encoding="utf-8"))

    converted: list[dict[str, Any]] = []
    still_mathish: list[dict[str, Any]] = []
    for item in confident:
        original = item["text"]
        new = convert_string(original, item["field_path"])
        live = wave1.get_path(packages[item["package_file"]], item["field_path"])
        if live != original:
            raise RuntimeError(
                f"Live text mismatch {item['package_file']} "
                f"{item['field_path']}: ledger != package"
            )
        wave1.set_path(packages[item["package_file"]], item["field_path"], new)
        category, review, reason, signals = inventory.classify_string(
            "$." + item["field_path"], new
        )
        remaining = not (category == "already_compliant" and not review)
        rec = {
            "package_file": item["package_file"],
            "field_path": item["field_path"],
            "original": original,
            "converted": new,
            "category": category,
            "reason_code": reason,
            "signals": signals,
            "still_needs_work": remaining,
        }
        converted.append(rec)
        if remaining:
            still_mathish.append(rec)

    if apply and still_mathish:
        raise SystemExit(
            f"Refusing to apply: {len(still_mathish)} strings still "
            "classify as not already_compliant. Run --dry-run."
        )

    if apply:
        for fname, data in packages.items():
            (CATALOGUE / fname).write_text(
                json.dumps(data, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )

    return {
        "confident": len(confident),
        "skipped_manual_review": len(skipped),
        "converted": converted,
        "still_needs_work": still_mathish,
        "skipped": skipped,
        "applied": apply,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--show-failures", action="store_true")
    parser.add_argument("--show-sample", action="store_true")
    args = parser.parse_args(argv)
    if not args.apply and not args.dry_run:
        args.dry_run = True
    result = migrate_packages(apply=args.apply)
    print(
        f"confident={result['confident']} "
        f"skipped_manual_review={result['skipped_manual_review']} "
        f"still_needs_work={len(result['still_needs_work'])} "
        f"applied={result['applied']}",
        file=sys.stderr,
    )
    if args.show_failures or result["still_needs_work"]:
        for rec in result["still_needs_work"][:80]:
            print("--- FAIL", rec["package_file"], rec["field_path"])
            print("ORIG ", rec["original"])
            print("NEW  ", rec["converted"])
            print("CLSS ", rec["category"], rec["reason_code"], rec["signals"])
            print()
    if args.show_sample:
        for rec in result["converted"][:12]:
            print("---", rec["field_path"])
            print("ORIG ", rec["original"])
            print("NEW  ", rec["converted"])
            print()
    return 0 if not result["still_needs_work"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

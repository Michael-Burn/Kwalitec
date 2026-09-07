#!/usr/bin/env python3
"""Wave 7 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 7 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 7 is the next 12 highest-risk backlog packages after Waves 1–6
(ledger ranking by tier-1 then needs_migration). Confirmed scope:
173 needs_migration strings, of which 130 are confident and 43 need
manual review.

Reuses Wave 1–6 conversion helpers; Wave 7-specific EXPLICIT overrides
cover notation families for this set (GLM link/canonical, F-distribution,
CI for a parameter, exponential family, model choice / deviance,
variable selection / adjusted R², factors/interactions, credibility
premium, independence).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave7.py --dry-run
    python scripts/math_notation_wave7.py --apply
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
import math_notation_wave2 as wave2  # noqa: E402
import math_notation_wave3 as wave3  # noqa: E402
import math_notation_wave4 as wave4  # noqa: E402
import math_notation_wave5 as wave5  # noqa: E402
import math_notation_wave6 as wave6  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Next 12 by ledger ranking (tier-1 then needs_migration) after Waves 1–6.
WAVE7_FILES = (
    "4.2.3-link-canonical-cs1014.json",
    "2.6.6-f-distribution-cs1009.json",
    "3.2.1-confidence-interval-parameter-cs1011.json",
    "4.2.1-exponential-family-cs1003.json",
    "4.2.7-model-choice-cs1014.json",
    "4.1.5-variable-selection-cs1003.json",
    "4.1.5-variable-selection-cs1013.json",
    "4.2.3-link-canonical-cs1003.json",
    "4.2.4-factors-interactions-cs1003.json",
    "4.2.7-model-choice-cs1003.json",
    "5.1.6-credibility-premium-cs1003.json",
    "2.2.2-independence-cs1005.json",
)

EXPLICIT: dict[str, str] = {
    # --- 4.2.3-link-canonical-cs1014 ---
    "Link maps μ to η; canonical examples logit (binomial), log (Poisson).": "Link maps $\\mu$ to $\\eta$; canonical examples logit (binomial), log (Poisson).",
    "A link function connects the mean response mu to the linear predictor η. A canonical link is the natural family link equating eta with the natural parameter. Binomial: logit; Poisson: log.": "A link function connects the mean response mu to the linear predictor $\\eta$. A canonical link is the natural family link equating eta with the natural parameter. Binomial: logit; Poisson: log.",
    "Binomial: logit (μ in (0,1) and logit maps to the real line for eta). Gamma: reciprocal (negative-reciprocal canonical form as in CMP) because μ greater than 0 maps the positive mean onto the η scale for the gamma exponential-family form. A software default needs a warrant; canonical means the link equating eta with the natural parameter.": "Binomial: logit ($\\mu$ in $(0,1)$ and logit maps to the real line for eta). Gamma: reciprocal (negative-reciprocal canonical form as in CMP) because $\\mu$ greater than 0 maps the positive mean onto the $\\eta$ scale for the gamma exponential-family form. A software default needs a warrant; canonical means the link equating eta with the natural parameter.",
    "A GLM uses a link g so that η = g(μ) = xᵀβ.\n(a) For a binomial probability μ = 0.8, compute the canonical logit link η = ln(μ/(1 − μ)).\n(b) For a Poisson mean with linear predictor η = 0.5, compute μ = e^η under the canonical log link.\nState why logit and log are the canonical links for binomial and Poisson respectively.": "A GLM uses a link $g$ so that $\\eta = g(\\mu) = x^{\\mathrm{T}}\\beta$.\n(a) For a binomial probability $\\mu = 0.8$, compute the canonical logit link $\\eta = \\ln(\\mu/(1 - \\mu))$.\n(b) For a Poisson mean with linear predictor $\\eta = 0.5$, compute $\\mu = e^{\\eta}$ under the canonical log link.\nState why logit and log are the canonical links for binomial and Poisson respectively.",
    "μ_binom": "$\\mu_{\\mathrm{binom}}$",
    "η_pois": "$\\eta_{\\mathrm{pois}}$",
    "η = ln(0.8/0.2) = ln 4 ≈ 1.3863": "$\\eta = \\ln(0.8/0.2) = \\ln 4 \\approx 1.3863$",
    "η ≈ 1.3863": "$\\eta \\approx 1.3863$",
    "μ = e^{0.5} ≈ 1.6487": "$\\mu = e^{0.5} \\approx 1.6487$",
    "μ ≈ 1.6487": "$\\mu \\approx 1.6487$",
    "Link maps μ → η; canonical as above": "Link maps $\\mu \\rightarrow \\eta$; canonical as above",
    "logit(0.8) ≈ 1.3863; Poisson μ = e^{0.5} ≈ 1.6487. Canonical links: logit (binomial), log (Poisson).": "$\\operatorname{logit}(0.8) \\approx 1.3863$; Poisson $\\mu = e^{0.5} \\approx 1.6487$. Canonical links: logit (binomial), log (Poisson).",
    # --- 2.6.6-f-distribution-cs1009 ---
    "Closed-book. Independent Normal samples of sizes n₁ and n₂ have equal population variances. Which statement is correct?": "Closed-book. Independent Normal samples of sizes $n_{1}$ and $n_{2}$ have equal population variances. Which statement is correct?",
    "S₁²/S₂²~F_{n₁-1,n₂-1} under equal variances.": "$S_{1}^{2}/S_{2}^{2}\\sim F_{n_{1}-1,n_{2}-1}$ under equal variances.",
    "F=S₁²/S₂²~F_{n₁-1,n₂-1} under the equal-variance null, with the numerator and denominator degrees of freedom kept in that order.": "$F=S_{1}^{2}/S_{2}^{2}\\sim F_{n_{1}-1,n_{2}-1}$ under the equal-variance null, with the numerator and denominator degrees of freedom kept in that order.",
    "S₁²/S₂²~t_{n₁+n₂-2} because both t and F use sample variances.": "$S_{1}^{2}/S_{2}^{2}\\sim t_{n_{1}+n_{2}-2}$ because both $t$ and $F$ use sample variances.",
    "S₁²/S₂²~F_{n₁,n₂} because estimating sample means does not consume degrees of freedom.": "$S_{1}^{2}/S_{2}^{2}\\sim F_{n_{1},n_{2}}$ because estimating sample means does not consume degrees of freedom.",
    "S₁²/S₂² is standard Normal under equal variances because its expected value is near one.": "$S_{1}^{2}/S_{2}^{2}$ is standard Normal under equal variances because its expected value is near one.",
    "Two independent random samples are drawn from Normal populations with equal variances. Sample 1 has n₁ = 10 and S₁² = 20; sample 2 has n₂ = 8 and S₂² = 10. Form the variance-ratio statistic F = S₁² / S₂², state its null distribution (degrees of freedom), and explain why a one-sample t-statistic is the wrong tool for this comparison.": "Two independent random samples are drawn from Normal populations with equal variances. Sample 1 has $n_{1} = 10$ and $S_{1}^{2} = 20$; sample 2 has $n_{2} = 8$ and $S_{2}^{2} = 10$. Form the variance-ratio statistic $F = S_{1}^{2} / S_{2}^{2}$, state its null distribution (degrees of freedom), and explain why a one-sample $t$-statistic is the wrong tool for this comparison.",
    "n₁, S₁²": "$n_{1}$, $S_{1}^{2}$",
    "n₂, S₂²": "$n_{2}$, $S_{2}^{2}$",
    "σ₁² = σ₂²": "$\\sigma_{1}^{2} = \\sigma_{2}^{2}$",
    "df₁ = 10 − 1 = 9; df₂ = 8 − 1 = 7; F ~ F(9, 7)": "$\\mathrm{df}_{1} = 10 - 1 = 9$; $\\mathrm{df}_{2} = 8 - 1 = 7$; $F \\sim F(9, 7)$",
    # --- 3.2.1-confidence-interval-parameter-cs1011 ---
    "Closed-book. From a large sample you obtain a 95% CI for mean claim size μ as (120, 140). Which statement is correct?": "Closed-book. From a large sample you obtain a 95% CI for mean claim size $\\mu$ as $(120, 140)$. Which statement is correct?",
    "95% coverage for μ under repeated sampling; not a prediction interval for the next claim.": "95% coverage for $\\mu$ under repeated sampling; not a prediction interval for the next claim.",
    "The interval comes from a procedure that covers the unknown parameter μ in 95% of repeated samples. It is not a claim that the next claim amount falls between 120 and 140 with probability 95%.": "The interval comes from a procedure that covers the unknown parameter $\\mu$ in 95% of repeated samples. It is not a claim that the next claim amount falls between 120 and 140 with probability 95%.",
    "μ is a random variable that equals 130 with probability 95%, and the interval endpoints are fixed constants only.": "$\\mu$ is a random variable that equals 130 with probability 95%, and the interval endpoints are fixed constants only.",
    "A random sample of n = 36 commercial property claims has sample mean x̄ = £12,000. Claim sizes are modelled as Normal with known σ = £1,800. Construct a 95% confidence interval for the population mean μ.": "A random sample of $n = 36$ commercial property claims has sample mean $\\bar{x}$ = £12,000. Claim sizes are modelled as Normal with known $\\sigma$ = £1,800. Construct a 95% confidence interval for the population mean $\\mu$.",
    "x̄": "$\\bar{x}$",
    "σ": "$\\sigma$",
    "CMP closed. Write the z-interval formula x̄ ± z_{0.975} σ/√n before substituting.": "CMP closed. Write the z-interval formula $\\bar{x} \\pm z_{0.975}\\,\\sigma/\\sqrt{n}$ before substituting.",
    "Compute σ/√n with √36 = 6.": "Compute $\\sigma/\\sqrt{n}$ with $\\sqrt{36} = 6$.",
    "For a Normal mean with known σ, SE(x̄) = σ/√n.": "For a Normal mean with known $\\sigma$, $\\operatorname{SE}(\\bar{x}) = \\sigma/\\sqrt{n}$.",
    "1.96 × 300 = 588": "$1.96 \\times 300 = 588$",
    "12000 − 588 = 11412;  12000 + 588 = 12588": "$12000 - 588 = 11412$;  $12000 + 588 = 12588$",
    "95% CI for μ: (£11,412, £12,588).": "95% CI for $\\mu$: (£11,412, £12,588).",
    "Using σ instead of σ/√n in the margin (1.96 × 1800) and producing a wildly wide interval, or using √n = √36 incorrectly as 36.": "Using $\\sigma$ instead of $\\sigma/\\sqrt{n}$ in the margin ($1.96 \\times 1800$) and producing a wildly wide interval, or using $\\sqrt{n} = \\sqrt{36}$ incorrectly as 36.",
    # --- 4.2.1-exponential-family-cs1003 ---
    "Any continuous response is automatically in the exponential family because the density can be written with an exp() somewhere.": "Any continuous response is automatically in the exponential family because the density can be written with an $\\exp()$ somewhere.",
    "Example: Poisson (counts with E[Y]=Var[Y]=μ); binomial (bounded proportion or count responses); Normal (continuous responses with constant variance). Each has an exponential-family density usable as a GLM response. Package name is not GLM; a GLM response sits in an exponential family with later eta and link.": "Example: Poisson (counts with $E[Y]=\\operatorname{Var}[Y]=\\mu$); binomial (bounded proportion or count responses); Normal (continuous responses with constant variance). Each has an exponential-family density usable as a GLM response. Package name is not GLM; a GLM response sits in an exponential family with later eta and link.",
    "Poisson belongs because the pmf contains exp(); that single algebraic feature is the family definition without mean-variance structure.": "Poisson belongs because the pmf contains $\\exp()$; that single algebraic feature is the family definition without mean-variance structure.",
    "A policy lapse indicator is modelled as Bernoulli(p) with p = 0.25. Write the pmf in exponential-family form exp{yθ − b(θ)} / a(φ) × c(y, φ) (with φ = 1), identify the natural parameter θ = logit(p), and evaluate θ numerically. Also state why the Normal distribution is a special case within the same GLM exponential family, not a rival outside it.": "A policy lapse indicator is modelled as $\\mathrm{Bernoulli}(p)$ with $p = 0.25$. Write the pmf in exponential-family form $\\exp\\{y\\theta - b(\\theta)\\} / a(\\varphi) \\times c(y, \\varphi)$ (with $\\varphi = 1$), identify the natural parameter $\\theta = \\operatorname{logit}(p)$, and evaluate $\\theta$ numerically. Also state why the Normal distribution is a special case within the same GLM exponential family, not a rival outside it.",
    "p^y (1 − p)^{1−y}": "$p^{y} (1 - p)^{1-y}$",
    "exp{y ln(p/(1 − p)) + ln(1 − p)} matches exp{yθ − b(θ)} with θ = logit(p)": "$\\exp\\{y \\ln(p/(1 - p)) + \\ln(1 - p)\\}$ matches $\\exp\\{y\\theta - b(\\theta)\\}$ with $\\theta = \\operatorname{logit}(p)$",
    "θ = ln(0.25/0.75) = ln(1/3) ≈ −1.0986": "$\\theta = \\ln(0.25/0.75) = \\ln(1/3) \\approx -1.0986$",
    "θ ≈ −1.0986": "$\\theta \\approx -1.0986$",
    "Normal ∈ exponential family (canonical link = identity)": "Normal $\\in$ exponential family (canonical link = identity)",
    "θ = logit(0.25) = ln(1/3) ≈ −1.0986; Bernoulli/Binomial is exponential-family with b(θ) = ln(1 + e^θ). Normal is a member of the same family, not a rival outside it.": "$\\theta = \\operatorname{logit}(0.25) = \\ln(1/3) \\approx -1.0986$; Bernoulli/Binomial is exponential-family with $b(\\theta) = \\ln(1 + e^{\\theta})$. Normal is a member of the same family, not a rival outside it.",
    # --- 4.2.7-model-choice-cs1014 ---
    "Closed-book. Nested GLMs M_reduced subset M_full. Which statement is correct?": "Closed-book. Nested GLMs $M_{\\mathrm{reduced}} \\subset M_{\\mathrm{full}}$. Which statement is correct?",
    "Compare deviance (or −2Δℓ) between nested models against a chi-squared reference on the degrees-of-freedom difference; also inspect whether added parameters are statistically and scientifically warranted. Residual plots are diagnostics, not nested model comparison. Model choice here uses analysis of deviance and parameter significance.": "Compare deviance (or $-2\\Delta\\ell$) between nested models against a chi-squared reference on the degrees-of-freedom difference; also inspect whether added parameters are statistically and scientifically warranted. Residual plots are diagnostics, not nested model comparison. Model choice here uses analysis of deviance and parameter significance.",
    "Choose M_full whenever any single added p-value is below 0.05; deviance difference is redundant if significance exists.": "Choose $M_{\\mathrm{full}}$ whenever any single added p-value is below 0.05; deviance difference is redundant if significance exists.",
    "Two nested Poisson GLMs are fitted to the same claim-count data. The reduced model (no vehicle-type factor) has deviance D_R = 42.0 on more residual df. The fuller model (with vehicle-type) has D_F = 33.8. The difference uses ν = 2 degrees of freedom (two extra parameters). Test H₀: the reduced model suffices at α = 0.05 using χ²_{2, 0.95} = 5.991.": "Two nested Poisson GLMs are fitted to the same claim-count data. The reduced model (no vehicle-type factor) has deviance $D_{R} = 42.0$ on more residual df. The fuller model (with vehicle-type) has $D_{F} = 33.8$. The difference uses $\\nu = 2$ degrees of freedom (two extra parameters). Test $H_{0}$: the reduced model suffices at $\\alpha = 0.05$ using $\\chi^{2}_{2, 0.95} = 5.991$.",
    "D_R, D_F": "$D_{R}$, $D_{F}$",
    "ν": "$\\nu$",
    "χ²_{2,0.95}": "$\\chi^{2}_{2,0.95}$",
    "ΔD = 42.0 − 33.8 = 8.2": "$\\Delta D = 42.0 - 33.8 = 8.2$",
    "ΔD = 8.2 on 2 df": "$\\Delta D = 8.2$ on 2 df",
    "8.2 > 5.991 ⇒ reject H₀ (reduced model insufficient)": "$8.2 > 5.991 \\Rightarrow$ reject $H_{0}$ (reduced model insufficient)",
    # --- remaining dry-run failures ---
    "Two nested commercial-property severity regressions are fitted on the same n = 60 risks.\nModel A uses p = 3 explanatory variables and has R² = 0.55.\nModel B uses p = 6 explanatory variables and has R² = 0.58.\nCompute adjusted R² for each model using R²_adj = 1 − (1 − R²)(n − 1)/(n − p − 1), and select the model preferred by adjusted R².": "Two nested commercial-property severity regressions are fitted on the same $n = 60$ risks.\nModel A uses $p = 3$ explanatory variables and has $R^{2} = 0.55$.\nModel B uses $p = 6$ explanatory variables and has $R^{2} = 0.58$.\nCompute adjusted $R^{2}$ for each model using $R^{2}_{\\mathrm{adj}} = 1 - (1 - R^{2})(n - 1)/(n - p - 1)$, and select the model preferred by adjusted $R^{2}$.",
    "Two nested severity regressions are fitted on the same n = 50 policies.\nModel A uses p = 2 explanatory variables and has R² = 0.60.\nModel B uses p = 5 explanatory variables and has R² = 0.62.\nCompute adjusted R² for each model using R²_adj = 1 − (1 − R²)(n − 1)/(n − p − 1), and select the model preferred by adjusted R².": "Two nested severity regressions are fitted on the same $n = 50$ policies.\nModel A uses $p = 2$ explanatory variables and has $R^{2} = 0.60$.\nModel B uses $p = 5$ explanatory variables and has $R^{2} = 0.62$.\nCompute adjusted $R^{2}$ for each model using $R^{2}_{\\mathrm{adj}} = 1 - (1 - R^{2})(n - 1)/(n - p - 1)$, and select the model preferred by adjusted $R^{2}$.",
    "A GLM uses a link g so that η = g(μ) = xᵀβ.\n(a) For a binomial probability μ = 0.25, compute the canonical logit link η = ln(μ/(1 − μ)).\n(b) For a Poisson mean with linear predictor η = 1.2, compute μ = e^η.\nState the canonical links for binomial and Poisson.": "A GLM uses a link $g$ so that $\\eta = g(\\mu) = x^{\\mathrm{T}}\\beta$.\n(a) For a binomial probability $\\mu = 0.25$, compute the canonical logit link $\\eta = \\ln(\\mu/(1 - \\mu))$.\n(b) For a Poisson mean with linear predictor $\\eta = 1.2$, compute $\\mu = e^{\\eta}$.\nState the canonical links for binomial and Poisson.",
    "A Poisson log-link flood-frequency GLM uses two binary factors: Coastal (1 if coastal postcode, else 0) and HighRise (1 if high-rise property, else 0), plus their interaction. The fitted linear predictor is η = −1.5 + 0.4 Coastal + 0.25 HighRise + 0.15 Coastal×HighRise. Compute η and μ = e^η for (a) coastal high-rise and (b) inland low-rise. State when the interaction term contributes.": "A Poisson log-link flood-frequency GLM uses two binary factors: Coastal (1 if coastal postcode, else 0) and HighRise (1 if high-rise property, else 0), plus their interaction. The fitted linear predictor is $\\eta = -1.5 + 0.4\\,\\mathrm{Coastal} + 0.25\\,\\mathrm{HighRise} + 0.15\\,\\mathrm{Coastal}\\times\\mathrm{HighRise}$. Compute $\\eta$ and $\\mu = e^{\\eta}$ for (a) coastal high-rise and (b) inland low-rise. State when the interaction term contributes.",
    "Two nested Poisson GLMs are fitted to the same flood claim-count data. The reduced model (no region factor) has deviance D_R = 50.0 on more residual df. The fuller model (with region) has D_F = 40.0. The region factor uses ν = 2 degrees of freedom. Compute ΔD = D_R − D_F and compare with χ²_{2,0.95} = 5.991 at α = 0.05.": "Two nested Poisson GLMs are fitted to the same flood claim-count data. The reduced model (no region factor) has deviance $D_{R} = 50.0$ on more residual df. The fuller model (with region) has $D_{F} = 40.0$. The region factor uses $\\nu = 2$ degrees of freedom. Compute $\\Delta D = D_{R} - D_{F}$ and compare with $\\chi^{2}_{2,0.95} = 5.991$ at $\\alpha = 0.05$.",
    "A risk's sample mean claim cost is X̄ = £1200. The hypothetical mean for the risk class is μ = £1000. The credibility factor is Z = 0.55. Compute the credibility premium P = Z X̄ + (1 − Z)μ and state what Z weights.": "A risk's sample mean claim cost is $\\bar{X}$ = £1200. The hypothetical mean for the risk class is $\\mu$ = £1000. The credibility factor is $Z = 0.55$. Compute the credibility premium $P = Z\\bar{X} + (1 - Z)\\mu$ and state what $Z$ weights.",
    "Independence requires P(x,y) = P(X=x)P(Y=y) for every cell. Here P(X=0)P(Y=0) = 0.60×0.70 = 0.42, but P(0,0) = 0.50 ≠ 0.42, so X and Y are not independent.": "Independence requires $P(x,y) = P(X=x)P(Y=y)$ for every cell. Here $P(X=0)P(Y=0) = 0.60\\times 0.70 = 0.42$, but $P(0,0) = 0.50 \\neq 0.42$, so $X$ and $Y$ are not independent.",
    # --- quality fixes (auto-path mangled R²_adj / prose-in-math / bare η / Δ) ---
    "R²_adj,A = 1 − (1 − 0.55) × 59 / 56 = 1 − 0.45 × 59/56 = 1 − 26.55/56 ≈ 0.5259": "$R^{2}_{\\mathrm{adj},A} = 1 - (1 - 0.55) \\times 59 / 56 = 1 - 0.45 \\times 59/56 = 1 - 26.55/56 \\approx 0.5259$",
    "R²_adj,A ≈ 0.5259": "$R^{2}_{\\mathrm{adj},A} \\approx 0.5259$",
    "R²_adj,B = 1 − (1 − 0.58) × 59 / 53 = 1 − 0.42 × 59/53 = 1 − 24.78/53 ≈ 0.5325": "$R^{2}_{\\mathrm{adj},B} = 1 - (1 - 0.58) \\times 59 / 53 = 1 - 0.42 \\times 59/53 = 1 - 24.78/53 \\approx 0.5325$",
    "R²_adj,B ≈ 0.5325": "$R^{2}_{\\mathrm{adj},B} \\approx 0.5325$",
    "0.5325 > 0.5259 ⇒ prefer Model B on adjusted R²": "$0.5325 > 0.5259 \\Rightarrow$ prefer Model B on adjusted $R^{2}$",
    "R²_adj,A ≈ 0.5259; R²_adj,B ≈ 0.5325; select Model B. Raw R² alone is not the selection rule.": "$R^{2}_{\\mathrm{adj},A} \\approx 0.5259$; $R^{2}_{\\mathrm{adj},B} \\approx 0.5325$; select Model B. Raw $R^{2}$ alone is not the selection rule.",
    "p = 3, R² = 0.55": "$p = 3$, $R^{2} = 0.55$",
    "p = 6, R² = 0.58": "$p = 6$, $R^{2} = 0.58$",
    "R²_adj,A = 1 − (1 − 0.60) × 49 / 47 = 1 − 0.40 × 49/47 = 1 − 19.6/47 ≈ 0.5830": "$R^{2}_{\\mathrm{adj},A} = 1 - (1 - 0.60) \\times 49 / 47 = 1 - 0.40 \\times 49/47 = 1 - 19.6/47 \\approx 0.5830$",
    "R²_adj,A ≈ 0.5830": "$R^{2}_{\\mathrm{adj},A} \\approx 0.5830$",
    "R²_adj,B = 1 − (1 − 0.62) × 49 / 44 = 1 − 0.38 × 49/44 = 1 − 18.62/44 ≈ 0.5768": "$R^{2}_{\\mathrm{adj},B} = 1 - (1 - 0.62) \\times 49 / 44 = 1 - 0.38 \\times 49/44 = 1 - 18.62/44 \\approx 0.5768$",
    "R²_adj,B ≈ 0.5768": "$R^{2}_{\\mathrm{adj},B} \\approx 0.5768$",
    "0.5830 > 0.5768 ⇒ prefer Model A on adjusted R²": "$0.5830 > 0.5768 \\Rightarrow$ prefer Model A on adjusted $R^{2}$",
    "R²_adj,A ≈ 0.5830; R²_adj,B ≈ 0.5768; select Model A. More variables is not automatically better.": "$R^{2}_{\\mathrm{adj},A} \\approx 0.5830$; $R^{2}_{\\mathrm{adj},B} \\approx 0.5768$; select Model A. More variables is not automatically better.",
    "p = 2, R² = 0.60": "$p = 2$, $R^{2} = 0.60$",
    "p = 5, R² = 0.62": "$p = 5$, $R^{2} = 0.62$",
    "η = ln(0.25/0.75) = ln(1/3) ≈ −1.0986": "$\\eta = \\ln(0.25/0.75) = \\ln(1/3) \\approx -1.0986$",
    "logit(0.25) ≈ −1.0986": "$\\operatorname{logit}(0.25) \\approx -1.0986$",
    "μ = e^{1.2} ≈ 3.3201": "$\\mu = e^{1.2} \\approx 3.3201$",
    "μ ≈ 3.3201": "$\\mu \\approx 3.3201$",
    "logit(0.25) ≈ −1.0986; Poisson μ = e^{1.2} ≈ 3.3201. Canonical links: logit (binomial), log (Poisson).": "$\\operatorname{logit}(0.25) \\approx -1.0986$; Poisson $\\mu = e^{1.2} \\approx 3.3201$. Canonical links: logit (binomial), log (Poisson).",
    "η": "$\\eta$",
    "η = −1.5 + 0.4 + 0.25 + 0.15 = −0.7; μ = e^{−0.7} ≈ 0.4966": "$\\eta = -1.5 + 0.4 + 0.25 + 0.15 = -0.7$; $\\mu = e^{-0.7} \\approx 0.4966$",
    "Coastal & high-rise: η = −0.7, μ ≈ 0.4966": "Coastal & high-rise: $\\eta = -0.7$, $\\mu \\approx 0.4966$",
    "η = −1.5; μ = e^{−1.5} ≈ 0.2231": "$\\eta = -1.5$; $\\mu = e^{-1.5} \\approx 0.2231$",
    "Inland & low-rise: η = −1.5": "Inland & low-rise: $\\eta = -1.5$",
    "Coastal & high-rise: η = −0.7, μ ≈ 0.4966. Inland & low-rise: η = −1.5. The interaction term 0.15 applies only when both factors equal 1.": "Coastal & high-rise: $\\eta = -0.7$, $\\mu \\approx 0.4966$. Inland & low-rise: $\\eta = -1.5$. The interaction term 0.15 applies only when both factors equal 1.",
    "−1.5 + 0.4 C + 0.25 H + 0.15 C×H": "$-1.5 + 0.4\\,C + 0.25\\,H + 0.15\\,C\\times H$",
    "ΔD = 50.0 − 40.0 = 10.0": "$\\Delta D = 50.0 - 40.0 = 10.0$",
    "ΔD = 10.0": "$\\Delta D = 10.0$",
    "Reject reduced model at α = 0.05": "Reject reduced model at $\\alpha = 0.05$",
    "ΔD = 10.0 on 2 df > 5.991; reject the reduced model at α = 0.05 and retain region.": "$\\Delta D = 10.0$ on 2 df $> 5.991$; reject the reduced model at $\\alpha = 0.05$ and retain region.",
    "ΔD = 8.2 on 2 df > 5.991; reject the reduced model at α = 0.05 and retain vehicle-type.": "$\\Delta D = 8.2$ on 2 df $> 5.991$; reject the reduced model at $\\alpha = 0.05$ and retain vehicle-type.",
    "Marginals are P(X=0)=0.60, P(X=1)=0.40, P(Y=0)=0.70, P(Y=1)=0.30. Since 0.60×0.70 = 0.42 ≠ P(0,0) = 0.50, X and Y are not independent. Zero covariance would not by itself prove independence in general.": "Marginals are $P(X=0)=0.60$, $P(X=1)=0.40$, $P(Y=0)=0.70$, $P(Y=1)=0.30$. Since $0.60\\times 0.70 = 0.42 \\neq P(0,0) = 0.50$, $X$ and $Y$ are not independent. Zero covariance would not by itself prove independence in general.",
    "0.60×0.70 = 0.42 ≠ 0.50 = P(0,0) → not independent": "$0.60\\times 0.70 = 0.42 \\neq 0.50 = P(0,0)$ $\\rightarrow$ not independent",
    "Declaring independence from a quick look at the table, or treating Cov(X, Y) = 0 as a general proof of independence without checking joint factorisation.": "Declaring independence from a quick look at the table, or treating $\\operatorname{Cov}(X, Y) = 0$ as a general proof of independence without checking joint factorisation.",
    "P(X=0) = 0.50+0.10 = 0.60; P(X=1) = 0.20+0.20 = 0.40; P(Y=0) = 0.50+0.20 = 0.70; P(Y=1) = 0.10+0.20 = 0.30.": "$P(X=0) = 0.50+0.10 = 0.60$; $P(X=1) = 0.20+0.20 = 0.40$; $P(Y=0) = 0.50+0.20 = 0.70$; $P(Y=1) = 0.10+0.20 = 0.30$.",
    "Compare P(0,0) with P(X=0)P(Y=0), and at least one other cell.": "Compare $P(0,0)$ with $P(X=0)P(Y=0)$, and at least one other cell.",
    "P(X=0)=0.60, P(X=1)=0.40, P(Y=0)=0.70, P(Y=1)=0.30": "$P(X=0)=0.60$, $P(X=1)=0.40$, $P(Y=0)=0.70$, $P(Y=1)=0.30$",
    "Sum rows/columns for P(X) and P(Y).": "Sum rows/columns for $P(X)$ and $P(Y)$.",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 7 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave6.EXPLICIT:
        return wave6.EXPLICIT[text]
    if text in wave5.EXPLICIT:
        return wave5.EXPLICIT[text]
    if text in wave4.EXPLICIT:
        return wave4.EXPLICIT[text]
    if text in wave3.EXPLICIT:
        return wave3.EXPLICIT[text]
    if text in wave2.EXPLICIT:
        return wave2.EXPLICIT[text]
    if text in wave1.EXPLICIT:
        return wave1.EXPLICIT[text]
    return wave1.convert_string(text, field_path)


def wave7_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE7_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave7_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE7_FILES:
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
        for rec in result["still_needs_work"]:
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

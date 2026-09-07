#!/usr/bin/env python3
"""Wave 6 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 6 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 6 is the next 12 highest-risk backlog packages after Waves 1–5
(ledger ranking by tier-1 then needs_migration). Confirmed scope:
251 needs_migration strings, of which ~207 are confident.

Reuses Wave 1–5 conversion helpers; Wave 6-specific EXPLICIT overrides cover
notation families that prior waves did not fully author for this set
(GLM linear predictor η/Xβ/μ, exponential family, factors/interactions,
joint/marginal/conditional, moment-via-GF, hypothesis concepts, Bayes,
quantiles, credibility premium).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave6.py --dry-run
    python scripts/math_notation_wave6.py --apply
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

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Next 12 by ledger ranking (tier-1 then needs_migration) after Waves 1–5.
WAVE6_FILES = (
    "4.2.5-linear-predictor-cs1014.json",
    "2.2.1-marginal-conditional-cs1005.json",
    "revision-joint-distributions-cs1005.json",
    "2.4.2-moment-via-gf-cs1007.json",
    "3.3.1-hypothesis-concepts-cs1012.json",
    "4.2.4-factors-interactions-cs1014.json",
    "cp-2.1.3-prob-quantiles-cs1016.json",
    "5.1.1-bayes-theorem-cs1003.json",
    "4.2.5-linear-predictor-cs1003.json",
    "4.2.1-exponential-family-cs1014.json",
    "2.1.3-prob-quantiles-cs1004.json",
    "5.1.6-credibility-premium-cs1015.json",
)

EXPLICIT: dict[str, str] = {
    "η = X beta; examples with x and with factor or polynomial terms.": "$\\eta = X\\beta$; examples with $x$ and with factor or polynomial terms.",
    "The linear predictor η is typically X beta on the scale linked to the mean. Example simple: η = β₀ + β₁ x. Example with structure: eta includes factor indicators or polynomial powers such as x squared.": "The linear predictor $\\eta$ is typically $X\\beta$ on the scale linked to the mean. Example simple: $\\eta = \\beta_{0} + \\beta_{1} x$. Example with structure: eta includes factor indicators or polynomial powers such as x squared.",
    "η = β₀ + β₁ x + β₂ x^2 + β₃ I_Plus. Link maps μ to η.": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} x^{2} + \\beta_{3} I_{\\mathrm{Plus}}$. Link maps $\\mu$ to $\\eta$.",
    "η = β₀ + β₁ x + β₂ x squared + β₃ I_Plus with Standard baseline. η = Xβ is the linear predictor; the link g maps mean μ to η (for example log(μ)=η for Poisson log link).": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} x^{2} + \\beta_{3} I_{\\mathrm{Plus}}$ with Standard baseline. $\\eta = X\\beta$ is the linear predictor; the link $g$ maps mean $\\mu$ to $\\eta$ (for example $\\log(\\mu)=\\eta$ for Poisson log link).",
    "η = log(mu) = β₀ + β₁ x only; quadratic and factor terms belong in mu, not in eta.": "$\\eta = \\log(\\mu) = \\beta_{0} + \\beta_{1} x$ only; quadratic and factor terms belong in $\\mu$, not in $\\eta$.",
    "η = β₀ + β₁ x + β₂ I_Plus only because quadratic terms cannot appear in a Poisson GLM linear predictor.": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} I_{\\mathrm{Plus}}$ only because quadratic terms cannot appear in a Poisson GLM linear predictor.",
    "A severity GLM (gamma, log link) uses linear predictor η = β₀ + β₁x + β₂x² with fitted coefficients β₀ = 1.0, β₁ = 0.2, β₂ = −0.01. For a risk with x = 10 (age proxy), compute η and the mean severity μ = e^η.": "A severity GLM (gamma, log link) uses linear predictor $\\eta = \\beta_{0} + \\beta_{1}x + \\beta_{2}x^{2}$ with fitted coefficients $\\beta_{0} = 1.0$, $\\beta_{1} = 0.2$, $\\beta_{2} = -0.01$. For a risk with $x = 10$ (age proxy), compute $\\eta$ and the mean severity $\\mu = e^{\\eta}$.",
    "P(X=1)=0.70; P(Y=1|X=1)=0.40/0.70≈0.571.": "$P(X=1)=0.70$; $P(Y=1|X=1)=0.40/0.70\\approx 0.571$.",
    "P(X=1)=0.30+0.40=0.70, and P(Y=1|X=1)=0.40/0.70≈0.571.": "$P(X=1)=0.30+0.40=0.70$, and $P(Y=1|X=1)=0.40/0.70\\approx 0.571$.",
    "Var(aX+bY) = a²Var(X) + b²Var(Y) + 2abCov(X,Y).": "$\\operatorname{Var}(aX+bY) = a^{2}\\operatorname{Var}(X) + b^{2}\\operatorname{Var}(Y) + 2ab\\operatorname{Cov}(X,Y)$.",
    "Equating zero covariance with independence, or writing Var(aX+bY) = a²Var(X) + b²Var(Y) in all cases without checking Cov(X,Y).": "Equating zero covariance with independence, or writing $\\operatorname{Var}(aX+bY) = a^{2}\\operatorname{Var}(X) + b^{2}\\operatorname{Var}(Y)$ in all cases without checking $\\operatorname{Cov}(X,Y)$.",
    "If M_X(t) exists around zero, its Taylor expansion has E[X^r] as the coefficient multiplied by r!, equivalently M_X^{(r)}(0)=E[X^r].": "If $M_{X}(t)$ exists around zero, its Taylor expansion has $E[X^{r}]$ as the coefficient multiplied by $r!$, equivalently $M_{X}^{(r)}(0)=E[X^{r}]$.",
    "M_X(0)=E[X], so evaluating the MGF once at zero gives the first moment.": "$M_{X}(0)=E[X]$, so evaluating the MGF once at zero gives the first moment.",
    "M_X'(1)=E[X] for every distribution because moments are evaluated at t=1.": "$M_{X}'(1)=E[X]$ for every distribution because moments are evaluated at $t=1$.",
    "Writing M_X(t)=E[e^{tX}] completes moment extraction without differentiation or coefficient matching.": "Writing $M_{X}(t)=E[e^{tX}]$ completes moment extraction without differentiation or coefficient matching.",
    "Closed-book. For Poisson X, M_X(t)=exp(λ(e^t-1)). Which statement correctly obtains E[X]?": "Closed-book. For Poisson $X$, $M_{X}(t)=\\exp(\\lambda(e^{t}-1))$. Which statement correctly obtains $E[X]$?",
    "M_X'(t)=λe^t exp(λ(e^t-1)), so M_X'(0)=λ=E[X].": "$M_{X}'(t)=\\lambda e^{t}\\exp(\\lambda(e^{t}-1))$, so $M_{X}'(0)=\\lambda=E[X]$.",
    "M_X(0)=1, so E[X]=1 for every Poisson distribution.": "$M_{X}(0)=1$, so $E[X]=1$ for every Poisson distribution.",
    "M_X'(0)=e^λ because differentiating removes the inner e^t-1 term.": "$M_{X}'(0)=e^{\\lambda}$ because differentiating removes the inner $e^{t}-1$ term.",
    "The formula M_X(t)=E[e^{tX}] already states the mean, so no derivative is needed.": "The formula $M_{X}(t)=E[e^{tX}]$ already states the mean, so no derivative is needed.",
    "For X ~ Poisson(λ = 2), the cumulant generating function is C_X(t) = 2(e^t − 1). Obtain E[X] and Var(X) by differentiating the CGF at t = 0. Confirm that stopping at writing down C_X(t) without differentiation does not extract the moments.": "For $X \\sim \\mathrm{Poisson}(\\lambda = 2)$, the cumulant generating function is $C_{X}(t) = 2(e^{t} - 1)$. Obtain $E[X]$ and $\\operatorname{Var}(X)$ by differentiating the CGF at $t = 0$. Confirm that stopping at writing down $C_{X}(t)$ without differentiation does not extract the moments.",
    "Keep Type I/II in the reject-true-null / fail-to-reject-false-null directions. A p-value is a tail probability under H₀, not P(H₀|data) and not P(H₁). Power is P(reject H₀ | H₁ true).": "Keep Type I/II in the reject-true-null / fail-to-reject-false-null directions. A p-value is a tail probability under $H_{0}$, not $P(H_{0}|\\text{data})$ and not $P(H_{1})$. Power is $P(\\text{reject }H_{0} \\mid H_{1}\\text{ true})$.",
    "Null vs alternative; Type I = false reject; Type II = false retain; p-value = extreme-tail probability under H₀; power = P(reject | H₁).": "Null vs alternative; Type I = false reject; Type II = false retain; p-value = extreme-tail probability under $H_{0}$; power = $P(\\text{reject} \\mid H_{1})$.",
    "Closed-book. Disease screening: H₀ = no disease, H₁ = disease present. Which statement is correct?": "Closed-book. Disease screening: $H_{0}$ = no disease, $H_{1}$ = disease present. Which statement is correct?",
    "Type I = false positive; Type II = false negative; p-value under H₀; power = 1−β; concepts ≠ cookbook click.": "Type I = false positive; Type II = false negative; p-value under $H_{0}$; power = $1-\\beta$; concepts $\\neq$ cookbook click.",
    "Type I error is a false positive (declare disease when healthy). Type II error is a false negative (miss disease when present). A p-value is the probability under H₀ of a result at least as extreme as observed; power is P(reject H₀ | H₁ true). Running a software z-test does not by itself replace this vocabulary.": "Type I error is a false positive (declare disease when healthy). Type II error is a false negative (miss disease when present). A p-value is the probability under $H_{0}$ of a result at least as extreme as observed; power is $P(\\text{reject }H_{0} \\mid H_{1}\\text{ true})$. Running a software z-test does not by itself replace this vocabulary.",
    "A pricing team tests H₀: μ = £10,000 vs H₁: μ ≠ £10,000 for mean claim cost at significance level α = 0.05. The test statistic is z = 2.1 under H₀ (standard Normal). Compute the two-sided p-value and state the decision. Use Φ(2.1) = 0.9821.": "A pricing team tests $H_{0}\\colon \\mu$ = £10,000 vs $H_{1}\\colon \\mu \\neq$ £10,000 for mean claim cost at significance level $\\alpha = 0.05$. The test statistic is $z = 2.1$ under $H_{0}$ (standard Normal). Compute the two-sided p-value and state the decision. Use $\\Phi(2.1)$ = 0.9821.",
    "CMP closed. Write the two-sided p-value as 2[1 − Φ(|z|)] before substituting.": "CMP closed. Write the two-sided p-value as $2[1 - \\Phi(|z|)]$ before substituting.",
    "Compute 1 − Φ(2.1).": "Compute $1 - \\Phi(2.1)$.",
    "For a continuous symmetric null, the one-sided tail is 1 − Φ(|z|).": "For a continuous symmetric null, the one-sided tail is $1 - \\Phi(|z|)$.",
    "Writing η = β₀ + β₁ x with no factor indicators already explains categorical region levels completely.": "Writing $\\eta = \\beta_{0} + \\beta_{1} x$ with no factor indicators already explains categorical region levels completely.",
    "η = β₀ + β₁ x + β₂ I_South + β₃ x I_South. Refuse no-factor eta and interaction-as-main.": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} I_{\\mathrm{South}} + \\beta_{3} x I_{\\mathrm{South}}$. Refuse no-factor eta and interaction-as-main.",
    "η = β₀ + β₁ x + β₂ I_South + β₃ x times I_South with North baseline. Factors encode categorical levels; an interaction changes the age slope by region. It is not merely another additive main effect.": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} I_{\\mathrm{South}} + \\beta_{3} x\\times I_{\\mathrm{South}}$ with North baseline. Factors encode categorical levels; an interaction changes the age slope by region. It is not merely another additive main effect.",
    "η = β₀ + β₁ x finishes explaining factors and interactions because region is known to the modeller.": "$\\eta = \\beta_{0} + \\beta_{1} x$ finishes explaining factors and interactions because region is known to the modeller.",
    "η = β₀ + β₁ x + β₂ I_South only; the interaction is unnecessary because South adds a constant shift equal to an interaction.": "$\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} I_{\\mathrm{South}}$ only; the interaction is unnecessary because South adds a constant shift equal to an interaction.",
    "A Poisson log-link frequency GLM uses two binary factors: Male (1 if male, else 0) and Young (1 if age under 25, else 0), plus their interaction. The fitted linear predictor is η = −2.0 + 0.5 Male + 0.3 Young + 0.2 Male×Young.\nCompute η for (a) male and young, (b) female and not young. Also compute the implied mean frequency μ = e^η for (a).": "A Poisson log-link frequency GLM uses two binary factors: Male (1 if male, else 0) and Young (1 if age under 25, else 0), plus their interaction. The fitted linear predictor is $\\eta = -2.0 + 0.5\\,\\mathrm{Male} + 0.3\\,\\mathrm{Young} + 0.2\\,\\mathrm{Male}\\times\\mathrm{Young}$.\nCompute $\\eta$ for (a) male and young, (b) female and not young. Also compute the implied mean frequency $\\mu = e^{\\eta}$ for (a).",
    "Closed-book. Claim sizes are Exponential with mean θ = 1000. Which statement is correct?": "Closed-book. Claim sizes are Exponential with mean $\\theta = 1000$. Which statement is correct?",
    "P(X > 2000) ≈ 0.135; 90th percentile ≈ 2302.6; refuse recognition-only.": "$P(X > 2000) \\approx 0.135$; 90th percentile $\\approx 2302.6$; refuse recognition-only.",
    "P(X > 2000) = e^{-2} ≈ 0.135. The 90th percentile solves 1 − e^{-x/1000} = 0.9, giving x = 1000 ln(10) ≈ 2302.6. Naming Exponential does not replace these calculations.": "$P(X > 2000) = e^{-2} \\approx 0.135$. The 90th percentile solves $1 - e^{-x/1000} = 0.9$, giving $x = 1000 \\ln(10) \\approx 2302.6$. Naming Exponential does not replace these calculations.",
    "The 90th percentile is 900 because 0.9 × 1000 = 900 for any Exponential with mean θ.": "The 90th percentile is 900 because $0.9 \\times 1000 = 900$ for any Exponential with mean $\\theta$.",
    "Once the model is Exponential(θ = 1000), probability and quantile questions are answered by naming the family; numeric evaluation is optional decoration.": "Once the model is $\\mathrm{Exponential}(\\theta = 1000)$, probability and quantile questions are answered by naming the family; numeric evaluation is optional decoration.",
    "Household claim sizes X (£) are modelled as Exponential with mean θ = 800. Compute (a) P(X ≤ 400) and (b) the median claim size.": "Household claim sizes $X$ (£) are modelled as Exponential with mean $\\theta = 800$. Compute (a) $P(X \\leq 400)$ and (b) the median claim size.",
    "Treating P(X ≤ 400) as 0.5 because 400 is half the mean 800, or reporting the median as 0.5 × 800 = 400 instead of θ ln 2.": "Treating $P(X \\leq 400)$ as 0.5 because 400 is half the mean 800, or reporting the median as $0.5 \\times 800 = 400$ instead of $\\theta \\ln 2$.",
    "beta0+beta1x; beta0+beta_A I_A; beta0+beta1x+beta2x^2.": "$\\beta_{0}+\\beta_{1}x$; $\\beta_{0}+\\beta_{A} I_{A}$; $\\beta_{0}+\\beta_{1}x+\\beta_{2}x^{2}$.",
    "Simple slope: eta = beta0 + beta1 x. Two-level factor with baseline coding: eta = beta0 + beta_A I_A (versus baseline). Quadratic: eta = beta0 + beta1 x + beta2 x^2.": "Simple slope: $\\eta = \\beta_{0} + \\beta_{1} x$. Two-level factor with baseline coding: $\\eta = \\beta_{0} + \\beta_{A} I_{A}$ (versus baseline). Quadratic: $\\eta = \\beta_{0} + \\beta_{1} x + \\beta_{2} x^{2}$.",
    "A fleet mileage severity GLM (gamma, log link) uses linear predictor η = β₀ + β₁x + β₂x² with fitted coefficients β₀ = 0.5, β₁ = 0.15, β₂ = −0.005. For a risk with x = 8 (mileage band), compute η and the mean severity μ = e^η.": "A fleet mileage severity GLM (gamma, log link) uses linear predictor $\\eta = \\beta_{0} + \\beta_{1}x + \\beta_{2}x^{2}$ with fitted coefficients $\\beta_{0} = 0.5$, $\\beta_{1} = 0.15$, $\\beta_{2} = -0.005$. For a risk with $x = 8$ (mileage band), compute $\\eta$ and the mean severity $\\mu = e^{\\eta}$.",
    "Any continuous response is automatically in the exponential family because the density can be written with an exp() somewhere.": "Any continuous response is automatically in the exponential family because the density can be written with an $\\exp()$ somewhere.",
    "Poisson belongs because the pmf contains exp(); that single algebraic feature is the family definition without mean-variance structure.": "Poisson belongs because the pmf contains $\\exp()$; that single algebraic feature is the family definition without mean-variance structure.",
    "Weekly claim counts on a small commercial book are modelled as Poisson(λ). For λ = 4, write the pmf in exponential-family form exp{yθ − b(θ)} / a(φ) × c(y, φ) (with φ = 1), identify the natural parameter θ, and evaluate θ numerically. Also state why the Normal distribution is a special case within the same GLM exponential family, not a rival outside it.": "Weekly claim counts on a small commercial book are modelled as $\\mathrm{Poisson}(\\lambda)$. For $\\lambda = 4$, write the pmf in exponential-family form $\\exp\\{y\\theta - b(\\theta)\\} / a(\\varphi) \\times c(y, \\varphi)$ (with $\\varphi = 1$), identify the natural parameter $\\theta$, and evaluate $\\theta$ numerically. Also state why the Normal distribution is a special case within the same GLM exponential family, not a rival outside it.",
    "Closed-book. Travel medical claim sizes X (£) are modelled as Exponential with mean θ = 250. Compute P(X ≤ 100). Enter the probability as a decimal.": "Closed-book. Travel medical claim sizes $X$ (£) are modelled as Exponential with mean $\\theta = 250$. Compute $P(X \\leq 100)$. Enter the probability as a decimal.",
    "For Exponential mean θ, P(X ≤ x) = 1 - e^{-x/θ}. Here x/θ = 100/250 = 0.4, so P(X ≤ 100) = 1 - e^{-0.4} ≈ 0.3297. Naming the Exponential family alone does not produce this probability.": "For Exponential mean $\\theta$, $P(X \\leq x) = 1 - e^{-x/\\theta}$. Here $x/\\theta = 100/250 = 0.4$, so $P(X \\leq 100) = 1 - e^{-0.4} \\approx 0.3297$. Naming the Exponential family alone does not produce this probability.",
    "Travel medical claim sizes X (£) are modelled as Exponential with mean θ = 250. Compute (a) P(X ≤ 100) and (b) the median claim size.": "Travel medical claim sizes $X$ (£) are modelled as Exponential with mean $\\theta = 250$. Compute (a) $P(X \\leq 100)$ and (b) the median claim size.",
    "For Exponential mean θ, P(X ≤ x) = 1 - e^{-x/θ}. Here x/θ = 100/250 = 0.4.": "For Exponential mean $\\theta$, $P(X \\leq x) = 1 - e^{-x/\\theta}$. Here $x/\\theta = 100/250 = 0.4$.",
    "A risk's sample mean claim cost is X̄ = £800. The hypothetical mean for the risk class is μ = £600. The credibility factor is Z = 0.4. Compute the credibility premium P = Z X̄ + (1 − Z)μ and state what Z weights.": "A risk's sample mean claim cost is $\\bar{X}$ = £800. The hypothetical mean for the risk class is $\\mu$ = £600. The credibility factor is $Z = 0.4$. Compute the credibility premium $P = Z\\bar{X} + (1 - Z)\\mu$ and state what $Z$ weights.",
    "η(10) = 2.0; μ = e^{2} ≈ 7.3891 on the severity scale.": "$\\eta(10) = 2.0$; $\\mu = e^{2} \\approx 7.3891$ on the severity scale.",
    "P(Y = 1) = 0.25; P(X = 1 | Y = 1) = 0.40. The joint table is not interchangeable with its margins or conditionals without these moves.": "$P(Y = 1) = 0.25$; $P(X = 1 \\mid Y = 1) = 0.40$. The joint table is not interchangeable with its margins or conditionals without these moves.",
    "Independence requires p(x,y) = p_X(x)p_Y(y) for every pair. Var(aX+bY) = a²Var(X) + b²Var(Y) + 2ab Cov(X,Y). Refuse treating Cov = 0 as a general independence proof or dropping the covariance term without warrant.": "Independence requires $p(x,y) = p_{X}(x)p_{Y}(y)$ for every pair. $\\operatorname{Var}(aX+bY) = a^{2}\\operatorname{Var}(X) + b^{2}\\operatorname{Var}(Y) + 2ab\\operatorname{Cov}(X,Y)$. Refuse treating $\\operatorname{Cov} = 0$ as a general independence proof or dropping the covariance term without warrant.",
    "E[X] = C'(0) = 2; Var(X) = C''(0) = 2. Writing the CGF without differentiation does not extract the moments.": "$E[X] = C'(0) = 2$; $\\operatorname{Var}(X) = C''(0) = 2$. Writing the CGF without differentiation does not extract the moments.",
    "Male & young: η = −1.0, μ ≈ 0.3679. Female & not young: η = −2.0. The interaction term 0.2 applies only when both factors are active.": "Male & young: $\\eta = -1.0$, $\\mu \\approx 0.3679$. Female & not young: $\\eta = -2.0$. The interaction term 0.2 applies only when both factors are active.",
    "Do not report η as if it were mean severity": "Do not report $\\eta$ as if it were mean severity",
    "η(8) = 1.38; μ = e^{1.38} ≈ 3.9749 on the severity scale.": "$\\eta(8) = 1.38$; $\\mu = e^{1.38} \\approx 3.9749$ on the severity scale.",
    "θ = ln λ = ln 4 ≈ 1.3863; Poisson is exponential-family with b(θ) = e^θ. Normal is a member of the same family, not a rival outside it.": "$\\theta = \\ln\\lambda = \\ln 4 \\approx 1.3863$; Poisson is exponential-family with $b(\\theta) = e^{\\theta}$. Normal is a member of the same family, not a rival outside it.",
    "P(X ≤ 100) ≈ 0.3297; median ≈ 173.29. Naming the Exponential family alone does not finish the evaluation.": "$P(X \\leq 100) \\approx 0.3297$; median $\\approx 173.29$. Naming the Exponential family alone does not finish the evaluation.",
    "Z weights individual experience; here 40% on X̄, 60% on μ": "$Z$ weights individual experience; here $40\\%$ on $\\bar{X}$, $60\\%$ on $\\mu$",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 6 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
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


def wave6_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE6_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave6_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE6_FILES:
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
        for rec in result["still_needs_work"][:120]:
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

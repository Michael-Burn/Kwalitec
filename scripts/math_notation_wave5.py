#!/usr/bin/env python3
"""Wave 5 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 5 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 5 is the next 12 highest-risk backlog packages after Waves 1–4
(ledger ranking by tier-1 then needs_migration). This is the largest wave
so far (~370 needs_migration strings).

Reuses Wave 1–4 conversion helpers; Wave 5-specific EXPLICIT overrides cover
notation families that prior waves did not fully author for this set
(covariance/correlation chains, tower-law / law of total variance nests,
Bayes posterior evidence lines, MGF/CGF definitions, GLM mean-variance
boards, compact KC model answers).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave5.py --dry-run
    python scripts/math_notation_wave5.py --apply
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

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Next 12 by ledger ranking (tier-1 then needs_migration) after Waves 1–4.
WAVE5_FILES = (
    "revision-linear-models-cs1003.json",
    "2.2.3-cov-corr-expectation-cs1005.json",
    "2.3.1-conditional-expectation-cs1006.json",
    "2.3.2-mean-variance-conditioning-cs1006.json",
    "cp-5.1.1-bayes-theorem-cs1016.json",
    "2.2.4-linear-combinations-cs1005.json",
    "5.1.1-bayes-theorem-cs1015.json",
    "2.4.1-mgf-cgf-cs1007.json",
    "cp-2.2.1-marginal-conditional-cs1016.json",
    "4.2.2-mean-variance-cs1014.json",
    "revision-conditional-expectations-cs1006.json",
    "revision-generating-functions-cs1007.json",
)

EXPLICIT: dict[str, str] = {
    "Closed-book, state how E[Y] arises from E[E[Y|X]] (or equivalent).": "Closed-book, state how $E[Y]$ arises from $E[E[Y|X]]$ (or equivalent).",
    "Campaign chain retrieval: E[Y|X] → E[E[Y|X]] / Var via conditioning.": "Campaign chain retrieval: $E[Y|X] \\rightarrow E[E[Y|X]]$ / Var via conditioning.",
    "E[Y] = E[E[Y given X]].": "$E[Y] = E[E[Y\\text{ given }X]]$.",
    "Averaging the conditional mean over X recovers the unconditional mean: E[Y] = E[E[Y|X]].": "Averaging the conditional mean over X recovers the unconditional mean: $E[Y] = E[E[Y|X]]$.",
    "E[X + 2Y] = 1.50; Corr ≠ 0 here (and Corr = 0 ≠ independence in general)": "$E[X + 2Y] = 1.50$; $\\operatorname{Corr} \\neq 0$ here (and $\\operatorname{Corr} = 0 \\neq$ independence in general)",
    "E[Y] ≠ E[Y|X] as objects": "$E[Y] \\neq E[Y|X]$ as objects",
    "0.24 ≠ 0.90; base rate matters": "$0.24 \\neq 0.90$; base rate matters",
    "E[X] = 2 = M'(0); M_X(t) ≠ 2": "$E[X] = 2 = M'(0)$; $M_{X}(t) \\neq 2$",
    "Joint cell ≠ marginal or conditional": "Joint cell $\\neq$ marginal or conditional",
    "Raw second moment ≠ variance": "Raw second moment $\\neq$ variance",
    "Closed-book retrieval. In a multiple linear model Y = Xβ + ε fitted by ordinary least squares, state what Y and the columns of X are, and what OLS minimises. The residual plot then shows spread increasing markedly with fitted values. What is the warranted interpretation?": "Closed-book retrieval. In a multiple linear model $Y = X\\beta + \\varepsilon$ fitted by ordinary least squares, state what $Y$ and the columns of $X$ are, and what OLS minimises. The residual plot then shows spread increasing markedly with fitted values. What is the warranted interpretation?",
    "Joint moments → Cov(X,Y)=E[XY]−E[X]E[Y] → Corr=Cov/(σ_X σ_Y) → E[g(X,Y)] via the joint → refuse Corr=0⇒independence.": "Joint moments → $\\operatorname{Cov}(X,Y)=E[XY]-E[X]E[Y]$ → $\\operatorname{Corr}=\\operatorname{Cov}/(\\sigma_{X}\\sigma_{Y})$ → $E[g(X,Y)]$ via the joint → refuse $\\operatorname{Corr}=0\\Rightarrow$independence.",
    "E[Y|X=1]=0.40/(0.30+0.40)≈0.571.": "$E[Y|X=1]=0.40/(0.30+0.40)\\approx 0.571$.",
    "Given X=1, P(Y=1|X=1)=0.40/0.70≈0.571, so E[Y|X=1]=0(0.30/0.70)+1(0.40/0.70)≈0.571.": "Given $X=1$, $P(Y=1|X=1)=0.40/0.70\\approx 0.571$, so $E[Y|X=1]=0(0.30/0.70)+1(0.40/0.70)\\approx 0.571$.",
    "The unconditional mean E[Y] = 10×0.40 + 20×0.60 = 16 is a single number. E[Y|X] is a random function of X (15 when X = 1, 17 when X = 2). They are related by the tower law but are not the same object.": "The unconditional mean $E[Y] = 10\\times 0.40 + 20\\times 0.60 = 16$ is a single number. $E[Y|X]$ is a random function of $X$ (15 when $X = 1$, 17 when $X = 2$). They are related by the tower law but are not the same object.",
    "Reporting E[Y | X = 1] = 10×0.25 + 20×0.25 = 7.5 without dividing by P(X = 1), or treating the unconditional mean 16 as interchangeable with E[Y|X].": "Reporting $E[Y \\mid X = 1] = 10\\times 0.25 + 20\\times 0.25 = 7.5$ without dividing by $P(X = 1)$, or treating the unconditional mean 16 as interchangeable with $E[Y|X]$.",
    "Tower law E[Y]=E[E[Y|X]] → Var(Y)=E[Var(Y|X)]+Var(E[Y|X]) → refuse stopping at E[Y|X] alone.": "Tower law $E[Y]=E[E[Y|X]]$ → $\\operatorname{Var}(Y)=E[\\operatorname{Var}(Y|X)]+\\operatorname{Var}(E[Y|X])$ → refuse stopping at $E[Y|X]$ alone.",
    "E[Y]=E[E[Y|X]], and Var(Y)=E[Var(Y|X)]+Var(E[Y|X]).": "$E[Y]=E[E[Y|X]]$, and $\\operatorname{Var}(Y)=E[\\operatorname{Var}(Y|X)]+\\operatorname{Var}(E[Y|X])$.",
    "Var(Y)=E[Var(Y|X)] only, because variation of conditional means is irrelevant.": "$\\operatorname{Var}(Y)=E[\\operatorname{Var}(Y|X)]$ only, because variation of conditional means is irrelevant.",
    "CMP closed. Apply E[Y] = E[E[Y|X]], then Var(Y) = E[Var(Y|X)] + Var(E[Y|X]).": "CMP closed. Apply $E[Y] = E[E[Y|X]]$, then $\\operatorname{Var}(Y) = E[\\operatorname{Var}(Y|X)] + \\operatorname{Var}(E[Y|X])$.",
    "Form E[Var(Y|X)] and Var(E[Y|X])": "Form $E[\\operatorname{Var}(Y|X)]$ and $\\operatorname{Var}(E[Y|X])$",
    "Within-group variation is E[Var(Y|X)]. Between-group variation is Var(E[Y|X]) = E[m(X)²] − (E[m(X)])² with m(X) = E[Y|X].": "Within-group variation is $E[\\operatorname{Var}(Y|X)]$. Between-group variation is $\\operatorname{Var}(E[Y|X]) = E[m(X)^{2}] - (E[m(X)])^{2}$ with $m(X) = E[Y|X]$.",
    "Reporting only E[Y|X] = 5 or 12 as if that finished the mean, or computing Var(Y) as E[Var(Y|X)] = 7 and omitting the between-group term Var(E[Y|X]) = 11.76.": "Reporting only $E[Y|X] = 5$ or $12$ as if that finished the mean, or computing $\\operatorname{Var}(Y)$ as $E[\\operatorname{Var}(Y|X)] = 7$ and omitting the between-group term $\\operatorname{Var}(E[Y|X]) = 11.76$.",
    "1 − P(Breach)": "$1 - P(\\mathrm{Breach})$",
    "Evidence P(+) = 0.1085 and posterior ≈ 0.0876. Sensitivity 0.95 is not the posterior. Prior alone or the false-positive rate alone is wrong.": "Evidence $P(+) = 0.1085$ and posterior $\\approx 0.0876$. Sensitivity 0.95 is not the posterior. Prior alone or the false-positive rate alone is wrong.",
    "P(+)=0.1085; P(D|+)≈0.0876; refuse posterior equals likelihood.": "$P(+)=0.1085$; $P(D|+)\\approx 0.0876$; refuse posterior equals likelihood.",
    "P(+) = 0.95×0.01 + 0.10×0.99 = 0.1085. P(D|+) = 0.0095/0.1085 ≈ 0.0876. Equating P(D|+) with P(+|D) = 0.95 ignores the base rate; Bayes multiplies prior by likelihood and normalises.": "$P(+) = 0.95\\times 0.01 + 0.10\\times 0.99 = 0.1085$. $P(D|+) = 0.0095/0.1085 \\approx 0.0876$. Equating $P(D|+)$ with $P(+|D) = 0.95$ ignores the base rate; Bayes multiplies prior by likelihood and normalises.",
    "E[aX+bY]=aE[X]+bE[Y] → Var(aX+bY)=a²Var(X)+b²Var(Y)+2ab Cov(X,Y) → refuse dropping Cov when dependent.": "$E[aX+bY]=aE[X]+bE[Y]$ → $\\operatorname{Var}(aX+bY)=a^{2}\\operatorname{Var}(X)+b^{2}\\operatorname{Var}(Y)+2ab\\operatorname{Cov}(X,Y)$ → refuse dropping Cov when dependent.",
    "E=aEX+bEY; Var=a²VarX+b²VarY+2abCov.": "$E=aE[X]+bE[Y]$; $\\operatorname{Var}=a^{2}\\operatorname{Var}(X)+b^{2}\\operatorname{Var}(Y)+2ab\\operatorname{Cov}$.",
    "E[aX+bY]=aE[X]+bE[Y], and Var(aX+bY)=a²Var(X)+b²Var(Y)+2abCov(X,Y).": "$E[aX+bY]=aE[X]+bE[Y]$, and $\\operatorname{Var}(aX+bY)=a^{2}\\operatorname{Var}(X)+b^{2}\\operatorname{Var}(Y)+2ab\\operatorname{Cov}(X,Y)$.",
    "Var(aX+bY)=a²Var(X)+b²Var(Y) for all X and Y, because covariance never affects a linear combination.": "$\\operatorname{Var}(aX+bY)=a^{2}\\operatorname{Var}(X)+b^{2}\\operatorname{Var}(Y)$ for all $X$ and $Y$, because covariance never affects a linear combination.",
    "E[aX+bY]=a²E[X]+b²E[Y], matching the squared coefficients used in variance.": "$E[aX+bY]=a^{2}E[X]+b^{2}E[Y]$, matching the squared coefficients used in variance.",
    "Var(2X-Y)=2²(4)+(-1)²(9)+2(2)(-1)(2)=16+9-8=17.": "$\\operatorname{Var}(2X-Y)=2^{2}(4)+(-1)^{2}(9)+2(2)(-1)(2)=16+9-8=17$.",
    "Portfolio losses X and Y (£000) satisfy E[X] = 10, E[Y] = 4, Var(X) = 9, Var(Y) = 4, and Cov(X, Y) = 3. For the linear combination L = 2X − Y, compute E[L] and Var(L).": "Portfolio losses $X$ and $Y$ (£000) satisfy $E[X] = 10$, $E[Y] = 4$, $\\operatorname{Var}(X) = 9$, $\\operatorname{Var}(Y) = 4$, and $\\operatorname{Cov}(X, Y) = 3$. For the linear combination $L = 2X - Y$, compute $E[L]$ and $\\operatorname{Var}(L)$.",
    "Use E[aX + bY] = aE[X] + bE[Y] with a = 2, b = −1.": "Use $E[aX + bY] = aE[X] + bE[Y]$ with $a = 2$, $b = -1$.",
    "Write a²Var(X) + b²Var(Y) + 2ab Cov(X, Y).": "Write $a^{2}\\operatorname{Var}(X) + b^{2}\\operatorname{Var}(Y) + 2ab\\operatorname{Cov}(X, Y)$.",
    "Dropping the covariance term as if X and Y were uncorrelated gives 36 + 4 = 40, which overstates Var(L) when Cov = 3 > 0 and the combination is 2X − Y.": "Dropping the covariance term as if $X$ and $Y$ were uncorrelated gives $36 + 4 = 40$, which overstates $\\operatorname{Var}(L)$ when $\\operatorname{Cov} = 3 > 0$ and the combination is $2X - Y$.",
    "Evidence P(flag)=0.067 and posterior 0.018/0.067 ≈ 0.269. Likelihood 0.90 is not the posterior. Prior alone or genuine false-flag rate alone is wrong.": "Evidence $P(\\mathrm{flag})=0.067$ and posterior $0.018/0.067 \\approx 0.269$. Likelihood 0.90 is not the posterior. Prior alone or genuine false-flag rate alone is wrong.",
    "P(flag)=0.067; P(fraud|flag) ≈ 0.269. Refuse posterior equals likelihood.": "$P(\\mathrm{flag})=0.067$; $P(\\mathrm{fraud}|\\mathrm{flag}) \\approx 0.269$. Refuse posterior equals likelihood.",
    "P(flag)=0.90 times 0.02 + 0.05 times 0.98 = 0.018 + 0.049 = 0.067. P(fraud|flag)=0.018/0.067 ≈ 0.269. That equating posterior with P(flag|fraud)=0.90 ignores the base rate; Bayes multiplies prior times likelihood and normalises.": "$P(\\mathrm{flag})=0.90\\times 0.02 + 0.05\\times 0.98 = 0.018 + 0.049 = 0.067$. $P(\\mathrm{fraud}|\\mathrm{flag})=0.018/0.067 \\approx 0.269$. That equating posterior with $P(\\mathrm{flag}|\\mathrm{fraud})=0.90$ ignores the base rate; Bayes multiplies prior times likelihood and normalises.",
    "1 − P(F)": "$1 - P(F)$",
    "Named family → M_X(t)=E[e^{tX}] → CGF C_X(t)=log M_X(t) → refuse mean/var-as-MGF.": "Named family → $M_{X}(t)=E[e^{tX}]$ → CGF $C_{X}(t)=\\log M_{X}(t)$ → refuse mean/var-as-MGF.",
    "Where it exists around t=0, M_X(t)=E[e^{tX}] and the cumulant generating function is K_X(t)=log M_X(t). Knowing only a mean and variance does not determine that the MGF has been obtained.": "Where it exists around $t=0$, $M_{X}(t)=E[e^{tX}]$ and the cumulant generating function is $K_{X}(t)=\\log M_{X}(t)$. Knowing only a mean and variance does not determine that the MGF has been obtained.",
    "M_X(t)=E[tX] and K_X(t)=e^{M_X(t)}, so both are linear in t.": "$M_{X}(t)=E[tX]$ and $K_{X}(t)=e^{M_{X}(t)}$, so both are linear in $t$.",
    "Summing E[e^{tX}] under the Poisson PMF gives exp(λ(e^t-1)); taking its logarithm gives the CGF.": "Summing $E[e^{tX}]$ under the Poisson PMF gives $\\exp(\\lambda(e^{t}-1))$; taking its logarithm gives the CGF.",
    "M(t)=exp(λ(e^t-1)); K(t)=λ(e^t-1).": "$M(t)=\\exp(\\lambda(e^{t}-1))$; $K(t)=\\lambda(e^{t}-1)$.",
    "M_X(t)=exp(λ(e^t-1)) and K_X(t)=λ(e^t-1).": "$M_{X}(t)=\\exp(\\lambda(e^{t}-1))$ and $K_{X}(t)=\\lambda(e^{t}-1)$.",
    "M_X(t)=exp(λt) and K_X(t)=λt because the mean alone determines the full Poisson MGF.": "$M_{X}(t)=\\exp(\\lambda t)$ and $K_{X}(t)=\\lambda t$ because the mean alone determines the full Poisson MGF.",
    "M_X(t)=λ(e^t-1) and K_X(t)=exp(λ(e^t-1)), so the MGF and CGF are reversed.": "$M_{X}(t)=\\lambda(e^{t}-1)$ and $K_{X}(t)=\\exp(\\lambda(e^{t}-1))$, so the MGF and CGF are reversed.",
    "M_X(t)=λ and K_X(t)=log λ because Poisson mean and variance both equal λ.": "$M_{X}(t)=\\lambda$ and $K_{X}(t)=\\log\\lambda$ because Poisson mean and variance both equal $\\lambda$.",
    "Annual claim count X ~ Poisson(λ = 2). Obtain the moment generating function M_X(t) and the cumulant generating function C_X(t). State why writing M_X(t) = 2 does not define the MGF.": "Annual claim count $X \\sim \\mathrm{Poisson}(\\lambda = 2)$. Obtain the moment generating function $M_{X}(t)$ and the cumulant generating function $C_{X}(t)$. State why writing $M_{X}(t) = 2$ does not define the MGF.",
    "State why M_X(t) = 2 is wrong even though E[X] = 2.": "State why $M_{X}(t) = 2$ is wrong even though $E[X] = 2$.",
    "The mean E[X] = 2 is M'(0) (or C'(0)), not the MGF itself. The MGF is a function of t, here exp(2(e^t − 1)), not the constant mean.": "The mean $E[X] = 2$ is $M'(0)$ (or $C'(0)$), not the MGF itself. The MGF is a function of $t$, here $\\exp(2(e^{t} - 1))$, not the constant mean.",
    "P(X=1)=0.70; P(Y=1|X=1)≈0.571; refuse joint-as-margins-done.": "$P(X=1)=0.70$; $P(Y=1|X=1)\\approx 0.571$; refuse joint-as-margins-done.",
    "P(X=1) = 0.30 + 0.40 = 0.70. P(Y=1 | X=1) = 0.40 / 0.70 ≈ 0.571. The joint table is not interchangeable with its margins or conditionals without these moves.": "$P(X=1) = 0.30 + 0.40 = 0.70$. $P(Y=1 \\mid X=1) = 0.40 / 0.70 \\approx 0.571$. The joint table is not interchangeable with its margins or conditionals without these moves.",
    "For three candidate GLM responses, evaluate mean, variance, variance function V(μ), and scale φ where relevant:\n(1) Poisson with λ = 5;\n(2) Binomial(n = 10, p = 0.3);\n(3) Gamma with mean μ = 10 and shape α = 4 (so Var = μ²/α).": "For three candidate GLM responses, evaluate mean, variance, variance function $V(\\mu)$, and scale $\\varphi$ where relevant:\n(1) Poisson with $\\lambda = 5$;\n(2) $\\mathrm{Binomial}(n = 10, p = 0.3)$;\n(3) Gamma with mean $\\mu = 10$ and shape $\\alpha = 4$ (so $\\operatorname{Var} = \\mu^{2}/\\alpha$).",
    "CMP closed. For each family write E[Y], Var[Y], V(μ), and φ before substituting numbers.": "CMP closed. For each family write $E[Y]$, $\\operatorname{Var}[Y]$, $V(\\mu)$, and $\\varphi$ before substituting numbers.",
    "Use E[Y] = Var[Y] = λ and V(μ) = μ with φ = 1.": "Use $E[Y] = \\operatorname{Var}[Y] = \\lambda$ and $V(\\mu) = \\mu$ with $\\varphi = 1$.",
    "Compute np and np(1 − p); note V(μ) = μ(1 − μ/n) with φ = 1.": "Compute $np$ and $np(1 - p)$; note $V(\\mu) = \\mu(1 - \\mu/n)$ with $\\varphi = 1$.",
    "Use Var(Y) = E[Var(Y|X)] + Var(E[Y|X]).": "Use $\\operatorname{Var}(Y) = E[\\operatorname{Var}(Y|X)] + \\operatorname{Var}(E[Y|X])$.",
    "Var(Y) = E[Var(Y given X)] + Var(E[Y given X]).": "$\\operatorname{Var}(Y) = E[\\operatorname{Var}(Y\\text{ given }X)] + \\operatorname{Var}(E[Y\\text{ given }X])$.",
    "Var(Y) = E[Var(Y given X)] only.": "$\\operatorname{Var}(Y) = E[\\operatorname{Var}(Y\\text{ given }X)]$ only.",
    "CMP closed. Retrieve E[Y] = E[E[Y|X]] and Var(Y) = E[Var(Y|X)] + Var(E[Y|X]).": "CMP closed. Retrieve $E[Y] = E[E[Y|X]]$ and $\\operatorname{Var}(Y) = E[\\operatorname{Var}(Y|X)] + \\operatorname{Var}(E[Y|X])$.",
    "M_X(t)=E[e^(tX)] and K_X(t)=log M_X(t), where the MGF exists.": "$M_{X}(t)=E[e^{tX}]$ and $K_{X}(t)=\\log M_{X}(t)$, where the MGF exists.",
    "M_X(t) = E[exp(tX)] where finite, and K_X(t) = log M_X(t).": "$M_{X}(t) = E[\\exp(tX)]$ where finite, and $K_{X}(t) = \\log M_{X}(t)$.",
    "M_X(t) = E[tX], and K_X(t) is its derivative.": "$M_{X}(t) = E[tX]$, and $K_{X}(t)$ is its derivative.",
    "M_X(t) = P(X less than or equal to t), and K_X(t) is the survival function.": "$M_{X}(t) = P(X \\leq t)$, and $K_{X}(t)$ is the survival function.",
    "K_X(t) = exp(M_X(t)).": "$K_{X}(t) = \\exp(M_{X}(t))$.",
    "M_X'(0)=E[X] and M_X''(0)=E[X²].": "$M_{X}'(0)=E[X]$ and $M_{X}''(0)=E[X^{2}]$.",
    "E[X] = M_X'(0) and E[X squared] = M_X''(0).": "$E[X] = M_{X}'(0)$ and $E[X^{2}] = M_{X}''(0)$.",
    "E[X] = M_X(0) and E[X squared] = M_X'(0).": "$E[X] = M_{X}(0)$ and $E[X^{2}] = M_{X}'(0)$.",
    "Var(X) = M_X''(0) in every case.": "$\\operatorname{Var}(X) = M_{X}''(0)$ in every case.",
    "E[X squared] = squared M_X'(0).": "$E[X^{2}] = (M_{X}'(0))^{2}$.",
    "Closed-book retrieval. Define the moment generating function M_X(t) and the cumulant generating function K_X(t). If the MGF exists around zero, state how the first two raw moments are obtained from derivatives, and refuse calling M_X''(0) the variance in every case.": "Closed-book retrieval. Define the moment generating function $M_{X}(t)$ and the cumulant generating function $K_{X}(t)$. If the MGF exists around zero, state how the first two raw moments are obtained from derivatives, and refuse calling $M_{X}''(0)$ the variance in every case.",
    "CMP closed. Retrieve M_X = E[e^{tX}], K_X = log M_X, then the derivative-at-zero rules.": "CMP closed. Retrieve $M_{X} = E[e^{tX}]$, $K_{X} = \\log M_{X}$, then the derivative-at-zero rules.",
    "Where finite, M_X(t) = E[exp(tX)] and K_X(t) = log M_X(t).": "Where finite, $M_{X}(t) = E[\\exp(tX)]$ and $K_{X}(t) = \\log M_{X}(t)$.",
    "Variance is E[X²] - (E[X])², not M_X''(0) alone.": "Variance is $E[X^{2}] - (E[X])^{2}$, not $M_{X}''(0)$ alone.",
    "Calling the second MGF derivative at zero the variance without subtracting (E[X])², or confusing the MGF with a distribution function.": "Calling the second MGF derivative at zero the variance without subtracting $(E[X])^{2}$, or confusing the MGF with a distribution function.",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 5 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave4.EXPLICIT:
        return wave4.EXPLICIT[text]
    if text in wave3.EXPLICIT:
        return wave3.EXPLICIT[text]
    if text in wave2.EXPLICIT:
        return wave2.EXPLICIT[text]
    if text in wave1.EXPLICIT:
        return wave1.EXPLICIT[text]
    return wave1.convert_string(text, field_path)


def wave5_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE5_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave5_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE5_FILES:
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

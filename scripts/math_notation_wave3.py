#!/usr/bin/env python3
"""Wave 3 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 3 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Reuses Wave 1 conversion helpers; Wave 3-specific EXPLICIT overrides cover
notation families that prior waves did not author (deviance contributions,
paired/two-sample CIs, GLM mean-variance, Bayes vs EB, revision boards).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave3.py --dry-run
    python scripts/math_notation_wave3.py --apply
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

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Ledger wave_recommendation.wave_1 after Waves 1–2 backlog cleared (next tranche).
WAVE3_FILES = (
    "4.2.6-deviance-estimation-cs1014.json",
    "3.2.7-ci-paired-means-cs1011.json",
    "4.2.6-deviance-estimation-cs1003.json",
    "3.2.3-ci-given-sampling-distribution-cs1011.json",
    "4.1.2-simple-multiple-cs1013.json",
    "5.1.3-posterior-simple-cs1003.json",
    "5.1.9-bayes-vs-eb-cs1015.json",
    "revision-sampling-distributions-cs1009.json",
    "revision-linear-regression-cs1013.json",
    "revision-central-limit-theorem-cs1008.json",
    "4.2.2-mean-variance-cs1003.json",
    "3.2.6-ci-two-sample-cs1011.json",
)

EXPLICIT: dict[str, str] = {
    "A Poisson GLM fitted mean for one observation is μ̂ = 4, and the observed count is y = 5. Compute the observation's deviance contribution d = 2[y ln(y/μ̂) − (y − μ̂)]. Then, if the total deviance across the sample is D = 18.4 and the scale is φ = 1, state the scaled deviance D/φ. Finally, name how GLM parameters are estimated (MLE / IWLS).": "A Poisson GLM fitted mean for one observation is $\\hat{\\mu} = 4$, and the observed count is $y = 5$. Compute the observation's deviance contribution $d = 2\\bigl[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})\\bigr]$. Then, if the total deviance across the sample is $D = 18.4$ and the scale is $\\varphi = 1$, state the scaled deviance $D/\\varphi$. Finally, name how GLM parameters are estimated (MLE / IWLS).",
    "CMP closed. Write d = 2[y ln(y/μ̂) − (y − μ̂)] before substituting.": "CMP closed. Write $d = 2\\bigl[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})\\bigr]$ before substituting.",
    "Deviance compares the fitted model to the saturated model. For Poisson, each observation contributes 2[y ln(y/μ̂) − (y − μ̂)].": "Deviance compares the fitted model to the saturated model. For Poisson, each observation contributes $2\\bigl[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})\\bigr]$.",
    "Using (y − μ̂)²/μ̂ as if it were the deviance contribution (that is Pearson), or dividing by φ when φ is already 1 and then treating 18.4 as something other than D itself.": "Using $(y - \\hat{\\mu})^{2}/\\hat{\\mu}$ as if it were the deviance contribution (that is Pearson), or dividing by $\\varphi$ when $\\varphi$ is already 1 and then treating 18.4 as something other than $D$ itself.",
    "Analyse Dᵢ = Yᵢ − Xᵢ with a one-sample CI for μ_D; refuse independent two-sample on paired columns.": "Analyse $D_{i} = Y_{i} - X_{i}$ with a one-sample CI for $\\mu_{D}$; refuse independent two-sample on paired columns.",
    "Form Dᵢ = Yᵢ − Xᵢ (or Xᵢ − Yᵢ) and build a one-sample CI for μ_D. Applying the independent two-sample formula to the before and after columns ignores pairing and uses the wrong variance structure.": "Form $D_{i} = Y_{i} - X_{i}$ (or $X_{i} - Y_{i}$) and build a one-sample CI for $\\mu_{D}$. Applying the independent two-sample formula to the before and after columns ignores pairing and uses the wrong variance structure.",
    "Compute x̄ and ȳ separately and use a two-sample CI for μ_Y − μ_X that assumes independent samples, because each column has the same length.": "Compute $\\bar{x}$ and $\\bar{y}$ separately and use a two-sample CI for $\\mu_{Y} - \\mu_{X}$ that assumes independent samples, because each column has the same length.",
    "Eight policyholders each have a before/after loss pair. Differences d = before − after (£00) are: 12, 8, −2, 15, 10, 5, 9, 7. Using t_{7, 0.975} = 2.365, construct a 95% CI for the mean difference μ_d.": "Eight policyholders each have a before/after loss pair. Differences $d$ = before $-$ after (£00) are: 12, 8, $-2$, 15, 10, 5, 9, 7. Using $t_{7, 0.975} = 2.365$, construct a 95% CI for the mean difference $\\mu_{d}$.",
    "Compute s_d = √[Σ(d_i − d̄)²/(n−1)].": "Compute $s_{d} = \\sqrt{\\sum(d_{i} - \\bar{d})^{2}/(n-1)}$.",
    "SE = s_d/√n; then d̄ ± t × SE.": "$\\mathrm{SE} = s_{d}/\\sqrt{n}$; then $\\bar{d} \\pm t \\times \\mathrm{SE}$.",
    "A Poisson GLM fitted mean for one observation is μ̂ = 5, and the observed count is y = 8. Compute the observation's deviance contribution d = 2[y ln(y/μ̂) − (y − μ̂)]. Then, if the total deviance across the sample is D = 22.0 and φ = 1, state the scaled deviance D/φ and how parameters were estimated.": "A Poisson GLM fitted mean for one observation is $\\hat{\\mu} = 5$, and the observed count is $y = 8$. Compute the observation's deviance contribution $d = 2\\bigl[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})\\bigr]$. Then, if the total deviance across the sample is $D = 22.0$ and $\\varphi = 1$, state the scaled deviance $D/\\varphi$ and how parameters were estimated.",
    "CMP closed. Compute y ln(y/μ̂) before doubling; then form D/φ.": "CMP closed. Compute $y \\ln(y/\\hat{\\mu})$ before doubling; then form $D/\\varphi$.",
    "Always use the Normal-mean cookbook formula x̄ ± z s/√n, regardless of the sampling distribution you are given.": "Always use the Normal-mean cookbook formula $\\bar{x} \\pm z\\, s/\\sqrt{n}$, regardless of the sampling distribution you are given.",
    "Closed-book. For an Exponential mean-θ model you are told that 2n X̄ / θ ~ χ²_{2n}. Which statement is correct?": "Closed-book. For an Exponential mean-$\\theta$ model you are told that $2n \\bar{X} / \\theta \\sim \\chi^{2}_{2n}$. Which statement is correct?",
    "Invert P(χ²_L < 2n X̄ / θ < χ²_U)=1−α to bounds in 2n X̄ / χ²; refuse Normal-mean template.": "Invert $P(\\chi^{2}_{L} < 2n \\bar{X} / \\theta < \\chi^{2}_{U})=1-\\alpha$ to bounds in $2n \\bar{X} / \\chi^{2}$; refuse Normal-mean template.",
    "Choose χ² critical values so P(χ²_L < 2n X̄ / θ < χ²_U) = 1−α, then rearrange to isolate θ (bounds involve 2n X̄ / χ²). A memorised Normal-mean CI formula does not replace that inversion for this model.": "Choose $\\chi^{2}$ critical values so $P(\\chi^{2}_{L} < 2n \\bar{X} / \\theta < \\chi^{2}_{U}) = 1-\\alpha$, then rearrange to isolate $\\theta$ (bounds involve $2n \\bar{X} / \\chi^{2}$). A memorised Normal-mean CI formula does not replace that inversion for this model.",
    "Because X̄ is approximately Normal for large n, ignore the given χ² relationship and always use x̄ ± z s/√n for θ.": "Because $\\bar{X}$ is approximately Normal for large $n$, ignore the given $\\chi^{2}$ relationship and always use $\\bar{x} \\pm z\\, s/\\sqrt{n}$ for $\\theta$.",
    "The interval for θ is (χ²_L, χ²_U) with no dependence on X̄, because the pivot already contains all information.": "The interval for $\\theta$ is $(\\chi^{2}_{L}, \\chi^{2}_{U})$ with no dependence on $\\bar{X}$, because the pivot already contains all information.",
    "Rearrange to θ ∈ (2n X̄ · χ²_L, 2n X̄ · χ²_U), multiplying by the critical values instead of dividing.": "Rearrange to $\\theta \\in (2n \\bar{X} \\cdot \\chi^{2}_{L}, 2n \\bar{X} \\cdot \\chi^{2}_{U})$, multiplying by the critical values instead of dividing.",
    "An estimator θ̂ of a portfolio proportion satisfies θ̂ ~ N(θ, 0.01²) exactly (sampling distribution given). Observing θ̂ = 0.42, construct a 95% confidence interval for θ.": "An estimator $\\hat{\\theta}$ of a portfolio proportion satisfies $\\hat{\\theta} \\sim N(\\theta, 0.01^{2})$ exactly (sampling distribution given). Observing $\\hat{\\theta} = 0.42$, construct a 95% confidence interval for $\\theta$.",
    "Dividing 0.01 by √n when no sample size is part of the given sampling distribution, or using 0.42 ± 1.96 × 0.01².": "Dividing 0.01 by $\\sqrt{n}$ when no sample size is part of the given sampling distribution, or using $0.42 \\pm 1.96 \\times 0.01^{2}$.",
    "Two fitted linear models for claim severity Y (£000) are available.\nSimple: Ŷ_s = 2.0 + 0.5x₁, where x₁ is age/10.\nMultiple: Ŷ_m = 1.5 + 0.4x₁ + 0.3x₂, where x₂ is sum insured (£0000).\nFor a risk with x₁ = 4 and x₂ = 5, compute both fitted values and state which model form each equation represents.": "Two fitted linear models for claim severity $Y$ (£000) are available.\nSimple: $\\hat{Y}_{s} = 2.0 + 0.5x_{1}$, where $x_{1}$ is age/10.\nMultiple: $\\hat{Y}_{m} = 1.5 + 0.4x_{1} + 0.3x_{2}$, where $x_{2}$ is sum insured (£0000).\nFor a risk with $x_{1} = 4$ and $x_{2} = 5$, compute both fitted values and state which model form each equation represents.",
    "Annual flood claim counts are modelled as Poisson(λ). The prior is Gamma(α, β) with shape-rate parameterisation π(λ) ∝ λ^{α−1} e^{−βλ}, here α = 2, β = 3. A sample of n = 4 independent years has total counts Σyᵢ = 10. State the posterior distribution and its mean.": "Annual flood claim counts are modelled as $\\mathrm{Poisson}(\\lambda)$. The prior is $\\mathrm{Gamma}(\\alpha, \\beta)$ with shape-rate parameterisation $\\pi(\\lambda) \\propto \\lambda^{\\alpha-1} e^{-\\beta\\lambda}$, here $\\alpha = 2$, $\\beta = 3$. A sample of $n = 4$ independent years has total counts $\\sum y_{i} = 10$. State the posterior distribution and its mean.",
    "For Poisson observations with a Gamma(α, β) shape-rate prior, the posterior is Gamma(α+Σy, β+n).": "For Poisson observations with a $\\mathrm{Gamma}(\\alpha, \\beta)$ shape-rate prior, the posterior is $\\mathrm{Gamma}(\\alpha+\\sum y, \\beta+n)$.",
    "The same risk has n = 4 years and X̄ = £900.\nFully Bayesian structurals (from a specified prior): μ = £700, k = 6.\nEmpirical Bayes structurals (from collective data): μ̂ = £750, k̂ = 12.\nCompute both credibility premiums and explain why they differ.": "The same risk has $n = 4$ years and $\\bar{X}$ = £900.\nFully Bayesian structurals (from a specified prior): $\\mu$ = £700, $k = 6$.\nEmpirical Bayes structurals (from collective data): $\\hat{\\mu}$ = £750, $\\hat{k} = 12$.\nCompute both credibility premiums and explain why they differ.",
    "EB uses collectively estimated μ̂ and k̂.": "EB uses collectively estimated $\\hat{\\mu}$ and $\\hat{k}$.",
    "Use T = (Xbar-mu)/(S/sqrt(n)), which follows t_(n-1).": "Use $T = (\\bar{X}-\\mu)/(S/\\sqrt{n})$, which follows $t_{n-1}$.",
    "(sample mean minus mu)/(S divided by sqrt(n)) has a t distribution with n - 1 degrees of freedom.": "$(\\text{sample mean minus }\\mu)/(S\\text{ divided by }\\sqrt{n})$ has a $t$ distribution with $n - 1$ degrees of freedom.",
    "(sample mean minus mu)/(S divided by sqrt(n)) has a chi-squared distribution.": "$(\\text{sample mean minus }\\mu)/(S\\text{ divided by }\\sqrt{n})$ has a chi-squared distribution.",
    "Closed-book retrieval. For observations (x_i, y_i), state the ordinary least squares criterion. Stepwise selection then produces a linear model with high R², but the residual plot shows clear curvature. What is the warranted conclusion?": "Closed-book retrieval. For observations $(x_{i}, y_{i})$, state the ordinary least squares criterion. Stepwise selection then produces a linear model with high $R^{2}$, but the residual plot shows clear curvature. What is the warranted conclusion?",
    "sqrt(n)(sample mean minus mu)/sigma converges in distribution to a standard Normal variable as n grows.": "$\\sqrt{n}(\\text{sample mean minus }\\mu)/\\sigma$ converges in distribution to a standard Normal variable as $n$ grows.",
    "Closed-book retrieval. Let X₁, …, Xₙ be iid with finite mean μ and finite positive variance σ². State what the central limit theorem says about the standardised sample mean. The observations are highly skewed but have finite variance: what is justified about Normal approximation for their sample mean?": "Closed-book retrieval. Let $X_{1}, \\ldots, X_{n}$ be iid with finite mean $\\mu$ and finite positive variance $\\sigma^{2}$. State what the central limit theorem says about the standardised sample mean. The observations are highly skewed but have finite variance: what is justified about Normal approximation for their sample mean?",
    "The CLT states that √n (X̄ - μ)/σ converges in distribution to N(0,1) as n → ∞.": "The CLT states that $\\sqrt{n}\\,(\\bar{X} - \\mu)/\\sigma$ converges in distribution to $N(0,1)$ as $n \\to \\infty$.",
    "Mean and variance are defined only after writing the linear predictor η; family structure is secondary.": "Mean and variance are defined only after writing the linear predictor $\\eta$; family structure is secondary.",
    "Poisson: E[Y]=μ, Var[Y]=μ, V(μ)=μ (scale typically 1). Normal: E[Y]=μ, Var[Y]=σ², V(μ)=1 with scale σ². The link maps μ to η; this question requires the mean, variance, and scale structure of the response family.": "Poisson: $E[Y]=\\mu$, $\\operatorname{Var}[Y]=\\mu$, $V(\\mu)=\\mu$ (scale typically 1). Normal: $E[Y]=\\mu$, $\\operatorname{Var}[Y]=\\sigma^{2}$, $V(\\mu)=1$ with scale $\\sigma^{2}$. The link maps $\\mu$ to $\\eta$; this question requires the mean, variance, and scale structure of the response family.",
    "For three candidate GLM responses, evaluate mean, variance, variance function V(μ), and scale φ where relevant:\n(1) Poisson with λ = 3;\n(2) Binomial(n = 20, p = 0.4);\n(3) Gamma with mean μ = 8 and shape α = 2.": "For three candidate GLM responses, evaluate mean, variance, variance function $V(\\mu)$, and scale $\\varphi$ where relevant:\n(1) Poisson with $\\lambda = 3$;\n(2) Binomial($n = 20$, $p = 0.4$);\n(3) Gamma with mean $\\mu = 8$ and shape $\\alpha = 2$.",
    "CMP closed. For each family write E(Y), Var(Y), then identify V(μ) and φ.": "CMP closed. For each family write $E(Y)$, $\\operatorname{Var}(Y)$, then identify $V(\\mu)$ and $\\varphi$.",
    "Binomial mean is np; variance is np(1 − p); as a GLM for the count, V(μ) = μ(1 − μ/n).": "Binomial mean is $np$; variance is $np(1 - p)$; as a GLM for the count, $V(\\mu) = \\mu(1 - \\mu/n)$.",
    "Target μ_A − μ_B under independent samples; refuse paired-as-equal-n.": "Target $\\mu_{A} - \\mu_{B}$ under independent samples; refuse paired-as-equal-n.",
    "A two-sample CI typically targets μ_A − μ_B under independent samples from the two groups. Paired before/after rows are not the same design: equal sample sizes do not turn matched pairs into an independent two-sample problem.": "A two-sample CI typically targets $\\mu_{A} - \\mu_{B}$ under independent samples from the two groups. Paired before/after rows are not the same design: equal sample sizes do not turn matched pairs into an independent two-sample problem.",
    "If n_A = n_B, analyse the data as paired differences even when there is no natural matching between A and B units.": "If $n_{A} = n_{B}$, analyse the data as paired differences even when there is no natural matching between A and B units.",
    "Independent samples from portfolios A and B (Normal, known variances): n_A = 40, x̄_A = £8,200, σ_A = £1,200; n_B = 45, x̄_B = £7,600, σ_B = £1,100. Construct a 95% CI for μ_A − μ_B.": "Independent samples from portfolios A and B (Normal, known variances): $n_{A} = 40$, $\\bar{x}_{A}$ = £8,200, $\\sigma_{A}$ = £1,200; $n_{B} = 45$, $\\bar{x}_{B}$ = £7,600, $\\sigma_{B}$ = £1,100. Construct a 95% CI for $\\mu_{A} - \\mu_{B}$.",
    "CMP closed. Write SE = √(σ_A²/n_A + σ_B²/n_B) before the interval.": "CMP closed. Write $\\mathrm{SE} = \\sqrt{\\sigma_{A}^{2}/n_{A} + \\sigma_{B}^{2}/n_{B}}$ before the interval.",
    "Compute √(1200²/40 + 1100²/45).": "Compute $\\sqrt{1200^{2}/40 + 1100^{2}/45}$.",
    "Pooling into √(σ²(1/n_A+1/n_B)) with a single σ, or subtracting SEs instead of adding variances under the square root.": "Pooling into $\\sqrt{\\sigma^{2}(1/n_{A}+1/n_{B})}$ with a single $\\sigma$, or subtracting SEs instead of adding variances under the square root.",
    "95% CI for μ_d: approximately (3.760, 12.240) in £00.": "95% CI for $\\mu_{d}$: approximately (3.760, 12.240) in £00.",
    "95% CI for θ: (0.4004, 0.4396).": "95% CI for $\\theta$: (0.4004, 0.4396).",
    "95% CI for μ_A − μ_B: approximately (£108.48, £1,091.52).": "95% CI for $\\mu_{A} - \\mu_{B}$: approximately (£108.48, £1,091.52).",
    "√n (X̄ - μ)/σ →ᵈ N(0,1)": "$\\sqrt{n} (\\bar{X} - \\mu)/\\sigma \\xrightarrow{d} N(0,1)$",
}

def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 3 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave2.EXPLICIT:
        return wave2.EXPLICIT[text]
    if text in wave1.EXPLICIT:
        return wave1.EXPLICIT[text]
    return wave1.convert_string(text, field_path)


def wave3_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE3_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave3_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE3_FILES:
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

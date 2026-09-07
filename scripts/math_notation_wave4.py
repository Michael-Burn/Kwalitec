#!/usr/bin/env python3
"""Wave 4 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 4 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 4 is the ledger's ``wave_recommendation.wave_1`` tranche after Waves
1–3 cleared their packages (next 12 highest-risk compound boards).

Reuses Wave 1–3 conversion helpers; Wave 4-specific EXPLICIT overrides cover
notation families that prior waves did not author for this set (prediction
SE forms, Y_new, Wald software inference, log-link multiplicative effects,
Pearson X² GOF, Exponential-Gamma posterior, simulated CLT overlays).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave4.py --dry-run
    python scripts/math_notation_wave4.py --apply
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

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Ledger wave_recommendation.wave_1 after Waves 1–3 backlog cleared (next tranche).
WAVE4_FILES = (
    "3.2.2-prediction-interval-cs1011.json",
    "3.3.2-basic-tests-cs1012.json",
    "4.1.4-software-inference-cs1003.json",
    "4.2.10-fit-interpret-cs1003.json",
    "4.1.4-software-fit-cs1013.json",
    "4.2.9-goodness-tests-cs1003.json",
    "4.2.10-fit-interpret-cs1014.json",
    "5.1.3-posterior-simple-cs1015.json",
    "2.5.2-simulated-sample-normal-cs1008.json",
    "4.2.9-goodness-tests-cs1014.json",
    "revision-confidence-intervals-cs1011.json",
    "5.1.9-bayes-vs-eb-cs1003.json",
)

EXPLICIT: dict[str, str] = {
    "Closed-book. You fit a model to historical annual losses and need an interval for next year's loss Y_new. Which statement is correct?": "Closed-book. You fit a model to historical annual losses and need an interval for next year's loss $Y_{\\mathrm{new}}$. Which statement is correct?",
    "Prediction targets Y_new; a CI for E[Y] targets the mean. Proper prediction intervals account for both parameter uncertainty and process variation.": "Prediction targets $Y_{\\mathrm{new}}$; a CI for $E[Y]$ targets the mean. Proper prediction intervals account for both parameter uncertainty and process variation.",
    "Prediction interval covers Y_new; a CI for E[Y] does not substitute.": "Prediction interval covers $Y_{\\mathrm{new}}$; a CI for $E[Y]$ does not substitute.",
    "A prediction interval aims to cover the future observation Y_new (parameter uncertainty plus process/residual variation). A confidence interval for E[Y] covers only that mean parameter and does not finish the prediction-interval task.": "A prediction interval aims to cover the future observation $Y_{\\mathrm{new}}$ (parameter uncertainty plus process/residual variation). A confidence interval for $E[Y]$ covers only that mean parameter and does not finish the prediction-interval task.",
    "A confidence interval for mean loss already covers Y_new with the same coverage probability, so no separate prediction interval is needed.": "A confidence interval for mean loss already covers $Y_{\\mathrm{new}}$ with the same coverage probability, so no separate prediction interval is needed.",
    "A prediction interval covers E[Y] only; covering Y_new would require a parameter confidence interval instead.": "A prediction interval covers $E[Y]$ only; covering $Y_{\\mathrm{new}}$ would require a parameter confidence interval instead.",
    "CMP closed. Write the prediction SE σ√(1 + 1/n) before the interval.": "CMP closed. Write the prediction SE $\\sigma\\sqrt{1 + 1/n}$ before the interval.",
    "Compute σ√(1 + 1/n).": "Compute $\\sigma\\sqrt{1 + 1/n}$.",
    "A future observation has variance σ² plus the variance of x̄, so the prediction SE is σ√(1 + 1/n), not σ/√n.": "A future observation has variance $\\sigma^{2}$ plus the variance of $\\bar{x}$, so the prediction SE is $\\sigma\\sqrt{1 + 1/n}$, not $\\sigma/\\sqrt{n}$.",
    "Using the mean CI half-width 1.96 × 40/√25 = 15.68 instead of the prediction form 1.96 × 40√(1+1/25) ≈ 79.95.": "Using the mean CI half-width $1.96 \\times 40/\\sqrt{25} = 15.68$ instead of the prediction form $1.96 \\times 40\\sqrt{1+1/25} \\approx 79.95$.",
    "Paired data should be analysed with the independent two-sample test whenever n₁ = n₂.": "Paired data should be analysed with the independent two-sample test whenever $n_{1} = n_{2}$.",
    "z-test for one Normal mean (σ known); two-sample proportion test; paired test on differences; permutation ≠ basic parametric.": "z-test for one Normal mean ($\\sigma$ known); two-sample proportion test; paired test on differences; permutation $\\neq$ basic parametric.",
    "Test H₀: μ = £500 vs H₁: μ ≠ £500 for mean repair cost. A sample of n = 36 repairs has x̄ = £520. Assume Normal data with known σ = £60. Compute the z statistic and the two-sided p-value using Φ(2.0) = 0.9772. Decide at α = 0.05.": "Test $H_{0}\\colon \\mu$ = £500 vs $H_{1}\\colon \\mu \\neq$ £500 for mean repair cost. A sample of $n = 36$ repairs has $\\bar{x}$ = £520. Assume Normal data with known $\\sigma$ = £60. Compute the $z$ statistic and the two-sided $p$-value using $\\Phi(2.0) = 0.9772$. Decide at $\\alpha = 0.05$.",
    "CMP closed. Write z = (x̄ − μ₀)/(σ/√n) before looking up the p-value.": "CMP closed. Write $z = (\\bar{x} - \\mu_{0})/(\\sigma/\\sqrt{n})$ before looking up the $p$-value.",
    "Compute 2[1 − Φ(2)].": "Compute $2\\bigl[1 - \\Phi(2)\\bigr]$.",
    "Using (x̄ − μ₀)/σ = 20/60 ≈ 0.33 instead of dividing by σ/√n = 10, which collapses the test statistic toward zero.": "Using $(\\bar{x} - \\mu_{0})/\\sigma = 20/60 \\approx 0.33$ instead of dividing by $\\sigma/\\sqrt{n} = 10$, which collapses the test statistic toward zero.",
    "Software returns slope estimate β̂₁ = −8 (£ per year of pet age) with SE(β̂₁) = 2.5. Treat the Normal approximation as adequate and use z_{0.975} = 1.96.\n(a) Compute the Wald z statistic for H₀: β₁ = 0.\n(b) Form the approximate 95% CI for β₁.\n(c) At a fixed pet age, the fitted mean is ŷ = 320 with SE_mean = 15 and SE_pred = 40. Compare the half-widths of the 95% mean and individual prediction intervals.": "Software returns slope estimate $\\hat{\\beta}_{1} = -8$ (£ per year of pet age) with $\\mathrm{SE}(\\hat{\\beta}_{1}) = 2.5$. Treat the Normal approximation as adequate and use $z_{0.975} = 1.96$.\n(a) Compute the Wald $z$ statistic for $H_{0}\\colon \\beta_{1} = 0$.\n(b) Form the approximate 95% CI for $\\beta_{1}$.\n(c) At a fixed pet age, the fitted mean is $\\hat{y} = 320$ with $\\mathrm{SE}_{\\mathrm{mean}} = 15$ and $\\mathrm{SE}_{\\mathrm{pred}} = 40$. Compare the half-widths of the 95% mean and individual prediction intervals.",
    "Compute β̂₁ ± 1.96 × SE(β̂₁).": "Compute $\\hat{\\beta}_{1} \\pm 1.96 \\times \\mathrm{SE}(\\hat{\\beta}_{1})$.",
    "A fitted Poisson claim-frequency GLM with log link for employers' liability gives β̂_night = −0.15 for a night-shift indicator (baseline = day shift). Compute the multiplicative effect e^{β̂_night} on mean frequency, and the percentage change. Also, given D = 28 on df_res = 25 and max |r_P| = 2.4, state what else should accompany coefficient interpretation.": "A fitted Poisson claim-frequency GLM with log link for employers' liability gives $\\hat{\\beta}_{\\mathrm{night}} = -0.15$ for a night-shift indicator (baseline = day shift). Compute the multiplicative effect $e^{\\hat{\\beta}_{\\mathrm{night}}}$ on mean frequency, and the percentage change. Also, given $D = 28$ on $\\mathrm{df}_{\\mathrm{res}} = 25$ and $\\operatorname{max}|r_{P}| = 2.4$, state what else should accompany coefficient interpretation.",
    "Treating β̂_night = −0.15 as a −15% additive change on the frequency scale, without exponentiating.": "Treating $\\hat{\\beta}_{\\mathrm{night}} = -0.15$ as a $-15\\%$ additive change on the frequency scale, without exponentiating.",
    "Software returns slope estimate β̂₁ = 12 (£ per year of age) with SE(β̂₁) = 4. Treat the Normal approximation as adequate and use z_{0.975} = 1.96.\n(a) Compute the Wald z statistic for H₀: β₁ = 0.\n(b) Form the approximate 95% CI for β₁.\n(c) At a fixed age, the fitted mean is ŷ = 500 with SE_mean = 20 and SE_pred = 50. Compare the half-widths of the 95% mean and individual prediction intervals.": "Software returns slope estimate $\\hat{\\beta}_{1} = 12$ (£ per year of age) with $\\mathrm{SE}(\\hat{\\beta}_{1}) = 4$. Treat the Normal approximation as adequate and use $z_{0.975} = 1.96$.\n(a) Compute the Wald $z$ statistic for $H_{0}\\colon \\beta_{1} = 0$.\n(b) Form the approximate 95% CI for $\\beta_{1}$.\n(c) At a fixed age, the fitted mean is $\\hat{y} = 500$ with $\\mathrm{SE}_{\\mathrm{mean}} = 20$ and $\\mathrm{SE}_{\\mathrm{pred}} = 50$. Compare the half-widths of the 95% mean and individual prediction intervals.",
    "Pearson chi-square equals the deviance difference between M_full and M_reduced; LRT equals the sum of squared Pearson residuals only.": "Pearson chi-square equals the deviance difference between $M_{\\mathrm{full}}$ and $M_{\\mathrm{reduced}}$; LRT equals the sum of squared Pearson residuals only.",
    "Three exposure groups have observed claim counts O = 15, 9, 12 and fitted expected counts E = 12, 12, 12 from a Poisson GLM. Compute Pearson's X² = Σ(O − E)²/E. Decide at α = 0.05 using χ²_{2, 0.95} = 5.991. State what LRT/deviance tests are for by contrast.": "Three exposure groups have observed claim counts $O = 15, 9, 12$ and fitted expected counts $E = 12, 12, 12$ from a Poisson GLM. Compute Pearson's $X^{2} = \\sum(O - E)^{2}/E$. Decide at $\\alpha = 0.05$ using $\\chi^{2}_{2, 0.95} = 5.991$. State what LRT/deviance tests are for by contrast.",
    "CMP closed. Convert β̂ through e^β before discussing diagnostics.": "CMP closed. Convert $\\hat{\\beta}$ through $e^{\\beta}$ before discussing diagnostics.",
    "Claim waiting times (months) are Exponential with rate λ. The prior is Gamma(α, β) with shape-rate parameterisation π(λ) ∝ λ^{α−1} e^{−βλ}, here α = 4, β = 6. A sample of n = 5 independent waiting times has sum Σxᵢ = 8. Obtain the posterior distribution and its mean.": "Claim waiting times (months) are Exponential with rate $\\lambda$. The prior is $\\mathrm{Gamma}(\\alpha, \\beta)$ with shape-rate parameterisation $\\pi(\\lambda) \\propto \\lambda^{\\alpha-1} e^{-\\beta\\lambda}$, here $\\alpha = 4$, $\\beta = 6$. A sample of $n = 5$ independent waiting times has sum $\\sum x_{i} = 8$. Obtain the posterior distribution and its mean.",
    "Recall L(λ) ∝ λ^n exp(−λ Σxᵢ) for Exponential waiting times.": "Recall $L(\\lambda) \\propto \\lambda^{n} \\exp(-\\lambda \\sum x_{i})$ for Exponential waiting times.",
    "Conjugacy yields Gamma(α+n, β+Σxᵢ).": "Conjugacy yields $\\mathrm{Gamma}(\\alpha+n, \\beta+\\sum x_{i})$.",
    "For shape-rate Gamma, E[λ] = α'/β'.": "For shape-rate Gamma, $E[\\lambda] = \\alpha'/\\beta'$.",
    "At n=5 the distribution of X̄ can remain noticeably right-skewed. At n=100 it should be much closer to Normal, centred near 1 with standard deviation about 1/√100=0.1.": "At $n=5$ the distribution of $\\bar{X}$ can remain noticeably right-skewed. At $n=100$ it should be much closer to Normal, centred near 1 with standard deviation about $1/\\sqrt{100}=0.1$.",
    "Waiting times (days) follow Exponential with mean θ = 400 (so sd = 400 also). An analyst simulates samples of size n = 20 and overlays a Normal(400, 400²) density on the histogram of individual draws. Judge whether that Normal overlay is a good description of the individual-sample histogram, and state what changes if the object compared is instead the sampling distribution of X̄ at much larger n.": "Waiting times (days) follow Exponential with mean $\\theta = 400$ (so sd = 400 also). An analyst simulates samples of size $n = 20$ and overlays a $N(400, 400^{2})$ density on the histogram of individual draws. Judge whether that Normal overlay is a good description of the individual-sample histogram, and state what changes if the object compared is instead the sampling distribution of $\\bar{X}$ at much larger $n$.",
    "Three exposure groups have observed claim counts O = 8, 12, 10 and fitted expected counts E = 10, 10, 10 from a Poisson GLM. Compute Pearson's X² = Σ(O − E)²/E. Decide at α = 0.05 using χ²_{2, 0.95} = 5.991 (df = 3 − 1 for this illustrative grouped check). Also state what a nested likelihood-ratio / deviance test addresses that this aggregate Pearson check does not.": "Three exposure groups have observed claim counts $O = 8, 12, 10$ and fitted expected counts $E = 10, 10, 10$ from a Poisson GLM. Compute Pearson's $X^{2} = \\sum(O - E)^{2}/E$. Decide at $\\alpha = 0.05$ using $\\chi^{2}_{2, 0.95} = 5.991$ ($\\mathrm{df} = 3 - 1$ for this illustrative grouped check). Also state what a nested likelihood-ratio / deviance test addresses that this aggregate Pearson check does not.",
    "Closed-book retrieval. After a frequentist 95% confidence interval for a fixed parameter θ has been calculated, state the correct coverage interpretation. Then, given X̄ = 42 from n = 36 observations with known σ = 12, compute the 95% z-interval for μ (use z_{0.025} = 1.96).": "Closed-book retrieval. After a frequentist 95% confidence interval for a fixed parameter $\\theta$ has been calculated, state the correct coverage interpretation. Then, given $\\bar{X} = 42$ from $n = 36$ observations with known $\\sigma = 12$, compute the 95% $z$-interval for $\\mu$ (use $z_{0.025} = 1.96$).",
    "CMP closed. Retrieve the repeated-sampling coverage reading, then form X̄ ± 1.96 σ/√n.": "CMP closed. Retrieve the repeated-sampling coverage reading, then form $\\bar{X} \\pm 1.96\\,\\sigma/\\sqrt{n}$.",
    "The same risk has n = 5 years and X̄ = £1100.\nFully Bayesian structurals (from a specified prior): μ = £900, k = 5.\nEmpirical Bayes structurals (from collective data): μ̂ = £950, k̂ = 15.\nCompute both credibility premiums and state why they differ.": "The same risk has $n = 5$ years and $\\bar{X}$ = £1100.\nFully Bayesian structurals (from a specified prior): $\\mu$ = £900, $k = 5$.\nEmpirical Bayes structurals (from collective data): $\\hat{\\mu}$ = £950, $\\hat{k} = 15$.\nCompute both credibility premiums and state why they differ.",
    "Ẑ = n/(n+k̂), then mix with μ̂.": "$\\hat{Z} = n/(n+\\hat{k})$, then mix with $\\hat{\\mu}$.",
    "Reject H₀ at 5%": "Reject $H_{0}$ at 5%.",
    "95% CI ≈ (−12.9, −3.1)": "95% CI $\\approx (-12.9, -3.1)$",
    "z = −3.2; 95% CI for β₁ ≈ (−12.9, −3.1); mean interval (290.6, 349.4) is narrower than individual prediction interval (241.6, 398.4).": "$z = -3.2$; 95% CI for $\\beta_{1} \\approx (-12.9, -3.1)$; mean interval $(290.6, 349.4)$ is narrower than individual prediction interval $(241.6, 398.4)$.",
    "(0.8607 − 1) × 100% ≈ −13.93%": "$(0.8607 - 1) \\times 100\\% \\approx -13.93\\%$",
    "≈ −13.93% vs day shift": "$\\approx -13.93\\%$ vs day shift",
    "Night-shift mean frequency ≈ 0.8607× day-shift (≈ −13.93%). Also interpret deviance/df and residual diagnostics; Fit alone is incomplete.": "Night-shift mean frequency $\\approx 0.8607\\times$ day-shift ($\\approx -13.93\\%$). Also interpret deviance/df and residual diagnostics; Fit alone is incomplete.",
    "95% CI ≈ (4.16, 19.84)": "95% CI $\\approx (4.16, 19.84)$",
    "z = 3; 95% CI for β₁ ≈ (4.16, 19.84); mean interval (460.8, 539.2) is narrower than individual prediction interval (402, 598).": "$z = 3$; 95% CI for $\\beta_{1} \\approx (4.16, 19.84)$; mean interval $(460.8, 539.2)$ is narrower than individual prediction interval $(402, 598)$.",
    "(1.2214 − 1) × 100% ≈ 22.14%": "$(1.2214 - 1) \\times 100\\% \\approx 22.14\\%$",
    "≈ 22.14% higher mean frequency": "$\\approx 22.14\\%$ higher mean frequency",
    "Urban mean frequency ≈ 1.2214× rural (≈ +22.14%). Also interpret deviance/df and residual diagnostics; Fit alone is incomplete.": "Urban mean frequency $\\approx 1.2214\\times$ rural ($\\approx +22.14\\%$). Also interpret deviance/df and residual diagnostics; Fit alone is incomplete.",
    "X² = 0.8;  0.8 < 5.991 ⇒ do not reject aggregate adequacy at 5%": "$X^{2} = 0.8$; $0.8 < 5.991 \\Rightarrow$ do not reject aggregate adequacy at 5%",
    "frequentist 95% CI for fixed θ": "frequentist 95% CI for fixed $\\theta$",
    "A 95% frequentist CI procedure covers θ in 95% of repeated samples under the model (not a posterior probability for fixed θ given these data). Numerically, (38.08, 45.92).": "A 95% frequentist CI procedure covers $\\theta$ in 95% of repeated samples under the model (not a posterior probability for fixed $\\theta$ given these data). Numerically, $(38.08, 45.92)$.",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 4 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave3.EXPLICIT:
        return wave3.EXPLICIT[text]
    if text in wave2.EXPLICIT:
        return wave2.EXPLICIT[text]
    if text in wave1.EXPLICIT:
        return wave1.EXPLICIT[text]
    return wave1.convert_string(text, field_path)


def wave4_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE4_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave4_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE4_FILES:
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

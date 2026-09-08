#!/usr/bin/env python3
"""Wave 8 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 8 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 8 is the next 12 highest-risk backlog packages after Waves 1–7
(ledger ranking by tier-1 then needs_migration). Confirmed scope:
135 needs_migration strings, of which 114 are confident and 21 need
manual review.

Reuses Wave 1–7 conversion helpers; Wave 8-specific EXPLICIT overrides
cover notation families for this set (sampling distribution of X̄,
permutation tests, inverse transform, credible intervals, CI for a
sample mean, bootstrap percentile CI, Bayesian credibility, discrete
families, loss estimators, hypothesis testing errors, correlation).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave8.py --dry-run
    python scripts/math_notation_wave8.py --apply
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
import math_notation_wave7 as wave7  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Next 12 by ledger ranking (tier-1 then needs_migration) after Waves 1–7.
WAVE8_FILES = (
    "2.6.2-sampling-distribution-statistic-cs1009.json",
    "3.3.3-permutation-tests-cs1012.json",
    "2.1.5-inverse-transform-cs1004.json",
    "5.1.5-credible-intervals-cs1015.json",
    "cp-3.2.1-ci-sample-cs1016.json",
    "3.2.8-bootstrap-confidence-interval-cs1011.json",
    "5.1.7-bayesian-credibility-cs1015.json",
    "cr-2.1.1-discrete-cs1017.json",
    "5.1.7-bayesian-credibility-cs1003.json",
    "5.1.4-loss-estimators-cs1015.json",
    "cp-3.3.1-hypothesis-testing-cs1016.json",
    "cr-1.2.2-correlation-cs1017.json",
)

EXPLICIT: dict[str, str] = {
    'Closed-book. Under H₀ of no treatment effect, treatment labels are exchangeable across units. Which statement is correct?': 'Closed-book. Under $H_{0}$ of no treatment effect, treatment labels are exchangeable across units. Which statement is correct?',
    'Shuffle or reassign labels under H₀, recompute the test statistic many times, and compare the observed statistic to that permutation reference distribution. That is not a Normal two-sample z-test by another name, and not a chi-square GOF to a named distribution.': 'Shuffle or reassign labels under $H_{0}$, recompute the test statistic many times, and compare the observed statistic to that permutation reference distribution. That is not a Normal two-sample z-test by another name, and not a chi-square GOF to a named distribution.',
    'Resample with replacement to form a percentile confidence interval; reject H₀ if zero is outside that interval, and call the procedure a permutation test.': 'Resample with replacement to form a percentile confidence interval; reject $H_{0}$ if zero is outside that interval, and call the procedure a permutation test.',
    'Small claim samples (£00): Group A = {10, 12, 14}, Group B = {8, 9, 11}. Test H₀: the two groups share the same distribution, using the two-sided permutation statistic |x̄_A − x̄_B|. Enumerate all C(6,3) = 20 assignments of three labels to A. The observed |x̄_A − x̄_B| equals 8/3. Exactly 4 of the 20 permutations have |diff| ≥ 8/3. Report the exact permutation p-value.': 'Small claim samples (£00): Group A = {10, 12, 14}, Group B = {8, 9, 11}. Test $H_{0}$: the two groups share the same distribution, using the two-sided permutation statistic $|\\bar{x}_{A} - \\bar{x}_{B}|$. Enumerate all C(6,3) = 20 assignments of three labels to A. The observed $|\\bar{x}_{A} - \\bar{x}_{B}|$ equals 8/3. Exactly 4 of the 20 permutations have |diff| $\\geq 8/3$. Report the exact permutation p-value.',
    '0.2 > 0.05  ⇒  do not reject H₀': '$0.2 > 0.05 \\Rightarrow$ do not reject $H_{0}$',
    'Do not reject H₀ at 5%': 'Do not reject $H_{0}$ at 5%',
    'Observed |x̄_A − x̄_B| = 8/3; exact permutation p-value = 0.2; do not reject H₀ at α = 0.05.': 'Observed $|\\bar{x}_{A} - \\bar{x}_{B}| = 8/3$; exact permutation p-value = 0.2; do not reject $H_{0}$ at $\\alpha = 0.05$.',
    'realised x̄': 'realised $\\bar{x}$',
    'Sampling distribution = law of X̄ over repeated samples of size 16': 'Sampling distribution = law of $\\bar{X}$ over repeated samples of size 16',
    '78 = one realised X̄; refuse equating it with the sampling distribution': '$78$ = one realised $\\bar{X}$; refuse equating it with the sampling distribution',
    'The sampling distribution of X̄ is the distribution of the sample mean over repeated samples of size 16; E[X̄] = 80 and Var(X̄) = 25. The observed 78 is one realised value, not that distribution.': 'The sampling distribution of $\\bar{X}$ is the distribution of the sample mean over repeated samples of size 16; $E[\\bar{X}] = 80$ and $\\operatorname{Var}(\\bar{X}) = 25$. The observed 78 is one realised value, not that distribution.',
    'Exponential(rate λ = 0.5), U = 0.2': 'Exponential(rate $\\lambda = 0.5$), $U = 0.2$',
    '0.3 < 0.55 ≤ 0.8 → Y = 2': '$0.3 < 0.55 \\leq 0.8 \\Rightarrow Y = 2$',
    'Uniform + inverse CDF required; nameless RNG ≠ method shown': 'Uniform + inverse CDF required; nameless RNG $\\neq$ method shown',
    'X ≈ 0.4463 from Exponential(rate 0.5) with U = 0.2; Y = 2 from the discrete CDF with U = 0.55. A black-box RNG call without Uniform-to-inverse-CDF construction is not the inverse transform method.': '$X \\approx 0.4463$ from Exponential(rate 0.5) with $U = 0.2$; $Y = 2$ from the discrete CDF with $U = 0.55$. A black-box RNG call without Uniform-to-inverse-CDF construction is not the inverse transform method.',
    'Posterior probability statement for θ using posterior distribution.': 'Posterior probability statement for $\\theta$ using posterior distribution.',
    'A credible interval is a posterior probability statement about the parameter θ given the observed data, typically constructed from the posterior distribution (for example equal-tailed quantiles).': 'A credible interval is a posterior probability statement about the parameter $\\theta$ given the observed data, typically constructed from the posterior distribution (for example equal-tailed quantiles).',
    'Closed-book. Posterior for risk parameter θ is Normal(0.10, 0.02 squared). Which statement is correct?': 'Closed-book. Posterior for risk parameter $\\theta$ is Normal(0.10, 0.02 squared). Which statement is correct?',
    'Approximate 95% equal-tailed credible interval: 0.10 plus or minus 1.96 times 0.02 gives about (0.0608, 0.1392). That frequentist repeated-sampling coverage slogan is the confidence-interval reading; a credible interval is a posterior probability statement about θ given the data.': 'Approximate 95% equal-tailed credible interval: 0.10 plus or minus 1.96 times 0.02 gives about (0.0608, 0.1392). That frequentist repeated-sampling coverage slogan is the confidence-interval reading; a credible interval is a posterior probability statement about $\\theta$ given the data.',
    'After observing claim experience, the posterior for mean ultimate cost θ (£000) is Normal with mean 100 and standard deviation 5: θ | data ~ N(100, 5²). Using z_{0.975} = 1.96, construct a central 95% credible interval for θ. State what probability statement the interval makes.': 'After observing claim experience, the posterior for mean ultimate cost $\\theta$ (£000) is Normal with mean 100 and standard deviation 5: $\\theta \\mid \\mathrm{data} \\sim N(100, 5^{2})$. Using $z_{0.975} = 1.96$, construct a central 95% credible interval for $\\theta$. State what probability statement the interval makes.',
    '100 ± 1.96 × 5 = 100 ± 9.8 ⇒ (90.2, 109.8)': '$100 \\pm 1.96 \\times 5 = 100 \\pm 9.8 \\Rightarrow (90.2, 109.8)$',
    'Write P(90.2 < θ < 109.8 | data) = 0.95.': 'Write $P(90.2 < \\theta < 109.8 \\mid \\mathrm{data}) = 0.95$.',
    'Interval derived from π(θ|data) = N(100, 25)': 'Interval derived from $\\pi(\\theta \\mid \\mathrm{data}) = N(100, 25)$',
    'Central 95% credible interval (90.2, 109.8); P(90.2 < θ < 109.8 | data) = 0.95.': 'Central 95% credible interval (90.2, 109.8); $P(90.2 < \\theta < 109.8 \\mid \\mathrm{data}) = 0.95$.',
    'CMP closed. Write x̄ ± 1.96 σ/√n with √100 = 10.': 'CMP closed. Write $\\bar{x} \\pm 1.96\\,\\sigma/\\sqrt{n}$ with $\\sqrt{100} = 10$.',
    'Using 1.96 × 50 = 98 as the half-width (forgetting /√n), which yields the nonsensical interval (352, 548) for a mean of 450 with n = 100.': 'Using $1.96 \\times 50 = 98$ as the half-width (forgetting $/\\sqrt{n}$), which yields the nonsensical interval (352, 548) for a mean of 450 with $n = 100$.',
    '95% CI for μ: (£440.2, £459.8).': '95% CI for $\\mu$: (£440.2, £459.8).',
    'Resample with replacement, recompute the statistic on each resample, then take the α/2 and 1−α/2 quantiles of those replicates as interval endpoints. Estimating a bootstrap standard error alone is not the same as constructing that CI, and forming the CI is not a hypothesis test.': 'Resample with replacement, recompute the statistic on each resample, then take the $\\alpha/2$ and $1-\\alpha/2$ quantiles of those replicates as interval endpoints. Estimating a bootstrap standard error alone is not the same as constructing that CI, and forming the CI is not a hypothesis test.',
    'Compute a bootstrap SE and report (θ̂ − SE, θ̂ + SE) only; quantile endpoints from replicates are never used.': 'Compute a bootstrap SE and report ($\\hat{\\theta} - \\mathrm{SE}$, $\\hat{\\theta} + \\mathrm{SE}$) only; quantile endpoints from replicates are never used.',
    'A bootstrap CI is completed by rejecting H₀ whenever θ̂ falls outside a fixed null value, without forming interval endpoints.': 'A bootstrap CI is completed by rejecting $H_{0}$ whenever $\\hat{\\theta}$ falls outside a fixed null value, without forming interval endpoints.',
    'A nonparametric bootstrap of mean claim severity produced B = 10 bootstrap means (£), already sorted: 1900, 1950, 1980, 2000, 2010, 2030, 2050, 2080, 2100, 2150. Using the percentile method with α = 0.05, form an approximate 90% CI by taking the order statistics at indices ⌊α(B+1)⌋ = ⌊0.55⌋ → 1 (use 1st) and ⌈(1−α)(B+1)⌉ = ⌈10.45⌉ → 11 (clamp to 10th).': 'A nonparametric bootstrap of mean claim severity produced $B = 10$ bootstrap means (£), already sorted: 1900, 1950, 1980, 2000, 2010, 2030, 2050, 2080, 2100, 2150. Using the percentile method with $\\alpha = 0.05$, form an approximate 90% CI by taking the order statistics at indices $\\lfloor\\alpha(B+1)\\rfloor = \\lfloor 0.55\\rfloor \\rightarrow 1$ (use 1st) and $\\lceil(1-\\alpha)(B+1)\\rceil = \\lceil 10.45\\rceil \\rightarrow 11$ (clamp to 10th).',
    'Draw one bootstrap resample, compute θ̂*, and report the singleton interval [θ̂*, θ̂*].': 'Draw one bootstrap resample, compute $\\hat{\\theta}^{*}$, and report the singleton interval [$\\hat{\\theta}^{*}$, $\\hat{\\theta}^{*}$].',
    'θ̂*_{(1)}…θ̂*_{(10)}': '$\\hat{\\theta}^{*}_{(1)}\\ldots\\hat{\\theta}^{*}_{(10)}$',
    '⌊0.05 × 11⌋ = ⌊0.55⌋ = 0 → use the 1st order statistic': '$\\lfloor 0.05 \\times 11\\rfloor = \\lfloor 0.55\\rfloor = 0 \\rightarrow$ use the 1st order statistic',
    '⌈0.95 × 11⌉ = ⌈10.45⌉ = 11 → clamp to 10': '$\\lceil 0.95 \\times 11\\rceil = \\lceil 10.45\\rceil = 11 \\rightarrow$ clamp to 10',
    'θ̂*_{(1)} = 1900;  θ̂*_{(10)} = 2150': '$\\hat{\\theta}^{*}_{(1)} = 1900$; $\\hat{\\theta}^{*}_{(10)} = 2150$',
    'Match generative story to family; discrete ≠ interchangeable.': 'Match generative story to family; discrete $\\neq$ interchangeable.',
    'Choose Poisson for the rare-event fixed-year count story; with λ = 0.4, P(X = 0) ≈ 0.6703. Refuse Normal or hypergeometric for this generative story.': 'Choose Poisson for the rare-event fixed-year count story; with $\\lambda = 0.4$, $P(X = 0) \\approx 0.6703$. Refuse Normal or hypergeometric for this generative story.',
    'Closed-book. Posterior for θ is available. Which statement is correct?': 'Closed-book. Posterior for $\\theta$ is available. Which statement is correct?',
    'Under squared-error loss, use the posterior mean as the Bayesian point estimator; under absolute-error loss, use the posterior median. A point estimator summarises the posterior under a loss; a credible interval is a posterior probability set for θ. Different objects.': 'Under squared-error loss, use the posterior mean as the Bayesian point estimator; under absolute-error loss, use the posterior median. A point estimator summarises the posterior under a loss; a credible interval is a posterior probability set for $\\theta$. Different objects.',
    'A discrete posterior for a reserve parameter θ (£000) places probabilities 0.20, 0.50, 0.30 on the values 1, 2, 3 respectively. Find the Bayes estimate under squared-error loss and under absolute-error loss.': 'A discrete posterior for a reserve parameter $\\theta$ (£000) places probabilities 0.20, 0.50, 0.30 on the values 1, 2, 3 respectively. Find the Bayes estimate under squared-error loss and under absolute-error loss.',
    'Compute Σ θ π(θ|data).': 'Compute $\\sum \\theta\\,\\pi(\\theta \\mid \\mathrm{data})$.',
    'θ values': '$\\theta$ values',
    'δ_SE = 1×0.20 + 2×0.50 + 3×0.30 = 0.2 + 1.0 + 0.9 = 2.1': '$\\delta_{\\mathrm{SE}} = 1\\times 0.20 + 2\\times 0.50 + 3\\times 0.30 = 0.2 + 1.0 + 0.9 = 2.1$',
    'δ_SE = 2.1': '$\\delta_{\\mathrm{SE}} = 2.1$',
    'δ_AE = 2': '$\\delta_{\\mathrm{AE}} = 2$',
    'Closed-book. Fraud flag: H₀ = genuine claim, H₁ = fraudulent. Which statement is correct?': 'Closed-book. Fraud flag: $H_{0}$ = genuine claim, $H_{1}$ = fraudulent. Which statement is correct?',
    'Type I = false fraud flag; Type II = missed fraud; p-value under H₀; power = 1−β; refuse cookbook-as-concepts and regression conflation.': 'Type I = false fraud flag; Type II = missed fraud; p-value under $H_{0}$; power = $1-\\beta$; refuse cookbook-as-concepts and regression conflation.',
    'Type I: flag fraud when the claim is genuine. Type II: miss fraud when it is present. A p-value is the probability under H₀ of data at least as extreme as observed; power is P(reject H₀ | H₁ true). A software z-test click does not replace this vocabulary, and linear regression is a different topic.': 'Type I: flag fraud when the claim is genuine. Type II: miss fraud when it is present. A p-value is the probability under $H_{0}$ of data at least as extreme as observed; power is $P(\\text{reject }H_{0} \\mid H_{1}\\text{ true})$. A software z-test click does not replace this vocabulary, and linear regression is a different topic.',
    'A fraud screen is run on 1,000 claims. Truth vs decision: 200 truly fraudulent claims, of which 40 are missed (flagged clean); 800 truly clean claims, of which 24 are falsely flagged as fraud. Taking H₀: claim is clean, compute the empirical Type I error rate and Type II error rate from these counts.': 'A fraud screen is run on 1,000 claims. Truth vs decision: 200 truly fraudulent claims, of which 40 are missed (flagged clean); 800 truly clean claims, of which 24 are falsely flagged as fraud. Taking $H_{0}$: claim is clean, compute the empirical Type I error rate and Type II error rate from these counts.',
    'n_clean': '$n_{\\mathrm{clean}}$',
    'n_fraud': '$n_{\\mathrm{fraud}}$',
    'Pearson linear; Spearman/Kendall rank; correlation ≠ causation.': 'Pearson linear; Spearman/Kendall rank; correlation $\\neq$ causation.',
    'For years licensed versus claim frequency, frequency is skewed with outliers and the scatter looks roughly decreasing but nonlinear. Software reports Pearson r = −0.28 and Spearman ρ = −0.55. Which correlation measure should you prefer for describing the association, and what must you still refuse?': 'For years licensed versus claim frequency, frequency is skewed with outliers and the scatter looks roughly decreasing but nonlinear. Software reports Pearson $r = -0.28$ and Spearman $\\rho = -0.55$. Which correlation measure should you prefer for describing the association, and what must you still refuse?',
    'Spearman ρ': 'Spearman $\\rho$',
    '|ρ| = 0.55 > |r| = 0.28; rank measure captures monotone association better here': '$|\\rho| = 0.55 > |r| = 0.28$; rank measure captures monotone association better here',
    'Report Spearman ρ = −0.55 as the preferred description': 'Report Spearman $\\rho = -0.55$ as the preferred description',
    'Association ≠ causation (even if |ρ| is large)': 'Association $\\neq$ causation (even if $|\\rho|$ is large)',
    'Prefer Spearman ρ = −0.55 (monotone, skewed, outlier-prone) over Pearson r = −0.28. A large coefficient still does not prove causation.': 'Prefer Spearman $\\rho = -0.55$ (monotone, skewed, outlier-prone) over Pearson $r = -0.28$. A large coefficient still does not prove causation.',

    "Normal(μ, σ²) fits best because the sample mean and variance can always be matched for any count variable.": "$\\mathrm{Normal}(\\mu, \\sigma^{2})$ fits best because the sample mean and variance can always be matched for any count variable.",
    "F(1) = 0.20 < 0.5; F(2) = 0.20+0.50 = 0.70 ≥ 0.5 ⇒ median = 2": "$F(1) = 0.20 < 0.5$; $F(2) = 0.20+0.50 = 0.70 \\geq 0.5 \\Rightarrow$ median $= 2$",
    "Explicit prior structure supplies mu and Z; premium Z X̄ + (1-Z) mu.": "Explicit prior structure supplies $\\mu$ and $Z$; premium $Z\\bar{X} + (1 - Z)\\mu$.",
    "Null vs alternative; Type I = false reject; Type II = false retain; power = P(reject | H₁).": "Null vs alternative; Type I = false reject; Type II = false retain; power = $P(\\text{reject} \\mid H_{1})$.",
    "P(90.2 < θ < 109.8 | data) = 0.95": "$P(90.2 < \\theta < 109.8 \\mid \\mathrm{data}) = 0.95$",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 8 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave7.EXPLICIT:
        return wave7.EXPLICIT[text]
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


def wave8_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE8_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave8_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE8_FILES:
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

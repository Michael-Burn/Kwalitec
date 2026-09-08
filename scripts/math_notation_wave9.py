#!/usr/bin/env python3
"""Wave 9 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 9 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 9 is the next 12 highest-risk backlog packages after Waves 1–8
(ledger ranking by tier-1 then needs_migration). Confirmed scope:
97 needs_migration strings, of which 73 are confident and 24 need
manual review.

Reuses Wave 1–8 conversion helpers; Wave 9-specific EXPLICIT overrides
cover notation families for this set (Poisson process, prior/posterior
conjugacy, inverse transform generation, GLM link/η/deviance, discrete
and continuous families, software generation sanity checks, MSE of an
estimator, correlation preference).

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave9.py --dry-run
    python scripts/math_notation_wave9.py --apply
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
import math_notation_wave8 as wave8  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Next 12 by ledger ranking (tier-1 then needs_migration) after Waves 1–8.
WAVE9_FILES = (
    "2.1.4-poisson-process-cs1004.json",
    "5.1.2-prior-posterior-cs1015.json",
    "revision-distributions-generation-cs1004.json",
    "revision-glm-cs1014.json",
    "2.1.1-discrete-cs1002.json",
    "2.1.6-software-generation-cs1004.json",
    "5.1.2-prior-posterior-cs1003.json",
    "cr-2.1.2-continuous-cs1017.json",
    "revision-estimators-cs1010.json",
    "revision-regression-glm-cs1003.json",
    "1.2.2-eda-association-ep001.json",
    "2.1.2-continuous-cs1002.json",
)

EXPLICIT: dict[str, str] = {
    # --- 2.1.4 Poisson process ---
    "Claims arrive as a homogeneous Poisson process with rate λ = 1.5 claims per day. For a 4-day window, name the distribution of the claim count N(4), compute P(N(4) = 0), and state the distribution of the waiting time until the next claim.": "Claims arrive as a homogeneous Poisson process with rate $\\lambda = 1.5$ claims per day. For a 4-day window, name the distribution of the claim count $N(4)$, compute $P(N(4) = 0)$, and state the distribution of the waiting time until the next claim.",
    "λ": "$\\lambda$",
    "N(4) ~ Poisson(λt = 1.5 × 4 = 6)": "$N(4) \\sim \\mathrm{Poisson}(\\lambda t = 1.5 \\times 4 = 6)$",
    "Compute P(N(4) = 0)": "Compute $P(N(4) = 0)$",
    "For Poisson(6), P(N = 0) = e^{-6}.": "For Poisson(6), $P(N = 0) = e^{-6}$.",
    "P(N(4) = 0) = e^{-6} ≈ 0.0025": "$P(N(4) = 0) = e^{-6} \\approx 0.0025$",
    "P(N(4) = 0) ≈ 0.0025": "$P(N(4) = 0) \\approx 0.0025$",
    "N(4) ~ Poisson(6) with P(N(4) = 0) ≈ 0.0025; waiting time until the next claim is Exponential(rate 1.5). Refuse collapsing the count and the wait into one label.": "$N(4) \\sim \\mathrm{Poisson}(6)$ with $P(N(4) = 0) \\approx 0.0025$; waiting time until the next claim is Exponential(rate 1.5). Refuse collapsing the count and the wait into one label.",
    # --- 5.1.2 prior-posterior cs1015 ---
    "Prior encodes belief about θ before data; posterior is the updated belief after data. Conjugate prior: a prior family closed under updating so the posterior stays in the same family. Naming conjugate structures the update but still requires obtaining the posterior from prior plus data.": "Prior encodes belief about $\\theta$ before data; posterior is the updated belief after data. Conjugate prior: a prior family closed under updating so the posterior stays in the same family. Naming conjugate structures the update but still requires obtaining the posterior from prior plus data.",
    "Prior: belief about θ before data. Posterior: updated belief after data. Conjugate: prior family closed under updating so posterior stays in the same family. Example: Beta-Binomial or Gamma-Poisson. Conjugate language structures the update; you still must obtain the actual posterior parameters from prior plus data.": "Prior: belief about $\\theta$ before data. Posterior: updated belief after data. Conjugate: prior family closed under updating so posterior stays in the same family. Example: Beta-Binomial or Gamma-Poisson. Conjugate language structures the update; you still must obtain the actual posterior parameters from prior plus data.",
    "A portfolio claim probability θ has prior Beta(α, β) = Beta(2, 8). In a new sample of n = 10 independent risks, s = 3 claims are observed (Binomial likelihood). Using conjugacy, state the posterior distribution and compute the prior mean and posterior mean.": "A portfolio claim probability $\\theta$ has prior $\\mathrm{Beta}(\\alpha, \\beta) = \\mathrm{Beta}(2, 8)$. In a new sample of $n = 10$ independent risks, $s = 3$ claims are observed (Binomial likelihood). Using conjugacy, state the posterior distribution and compute the prior mean and posterior mean.",
    "Beta(α+s, β+n−s)": "$\\mathrm{Beta}(\\alpha+s, \\beta+n-s)$",
    "E[θ]_prior = 2/(2+8) = 2/10 = 0.2": "$E[\\theta]_{\\mathrm{prior}} = 2/(2+8) = 2/10 = 0.2$",
    "θ | data ~ Beta(5, 15)": "$\\theta \\mid \\mathrm{data} \\sim \\mathrm{Beta}(5, 15)$",
    "E[θ]_post = 5/20 = 0.25": "$E[\\theta]_{\\mathrm{post}} = 5/20 = 0.25$",
    # --- revision-distributions-generation ---
    "Closed-book retrieval. Let U ~ Uniform(0, 1). To generate an Exponential random variable with rate λ = 2, state a valid inverse-transform formula, evaluate it at U = 0.3, and refuse applying F instead of F inverse.": "Closed-book retrieval. Let $U \\sim \\mathrm{Uniform}(0, 1)$. To generate an Exponential random variable with rate $\\lambda = 2$, state a valid inverse-transform formula, evaluate it at $U = 0.3$, and refuse applying $F$ instead of $F$ inverse.",
    "Exponential(rate λ = 2)": "Exponential(rate $\\lambda = 2$)",
    "X = -ln(1-U)/λ": "$X = -\\ln(1-U)/\\lambda$",
    "X = -ln(0.7)/2 ≈ 0.3567/2 = 0.1783": "$X = -\\ln(0.7)/2 \\approx 0.3567/2 = 0.1783$",
    "X ≈ 0.1783": "$X \\approx 0.1783$",
    "Use X = -ln(1-U)/λ; at U = 0.3 and λ = 2, X ≈ 0.1783. Refuse setting X = F(U) in place of the inverse CDF.": "Use $X = -\\ln(1-U)/\\lambda$; at $U = 0.3$ and $\\lambda = 2$, $X \\approx 0.1783$. Refuse setting $X = F(U)$ in place of the inverse CDF.",
    # --- revision-glm ---
    "The link satisfies g(E[Y|X]) = X beta.": "The link satisfies $g(E[Y \\mid X]) = X\\beta$.",
    "g(μ) = η = Xβ": "$g(\\mu) = \\eta = X\\beta$",
    "Deviance difference ↔ nested likelihood-ratio style test (asymptotic χ² under conditions)": "Deviance difference $\\leftrightarrow$ nested likelihood-ratio style test (asymptotic $\\chi^{2}$ under conditions)",
    "The link satisfies g(μ) = η = Xβ. For nested GLMs with the same family/scale treatment, a deviance difference can support an asymptotic chi-squared nested test, but it does not automatically choose the larger model or replace residual checks.": "The link satisfies $g(\\mu) = \\eta = X\\beta$. For nested GLMs with the same family/scale treatment, a deviance difference can support an asymptotic chi-squared nested test, but it does not automatically choose the larger model or replace residual checks.",
    # --- 2.1.1 discrete ---
    "A manufacturer independently inspects n = 30 items, each with the same probability p of being defective. Choose the matching discrete family for the number of defectives. As a light numeric check, if p = 0.1 under that family, compute P(X = 0).": "A manufacturer independently inspects $n = 30$ items, each with the same probability $p$ of being defective. Choose the matching discrete family for the number of defectives. As a light numeric check, if $p = 0.1$ under that family, compute $P(X = 0)$.",
    "CMP closed. Match the generative story to a named discrete family before evaluating P(X = 0).": "CMP closed. Match the generative story to a named discrete family before evaluating $P(X = 0)$.",
    "Light numeric illustration P(X = 0)": "Light numeric illustration $P(X = 0)$",
    "Under Binomial(n, p), P(X = 0) = (1-p)^n. The numeric check confirms the chosen family is usable, not a substitute for the family-selection judgment.": "Under $\\mathrm{Binomial}(n, p)$, $P(X = 0) = (1-p)^{n}$. The numeric check confirms the chosen family is usable, not a substitute for the family-selection judgment.",
    "P(X = 0) = (0.9)^30 ≈ 0.0424": "$P(X = 0) = (0.9)^{30} \\approx 0.0424$",
    "P(X = 0) ≈ 0.0424": "$P(X = 0) \\approx 0.0424$",
    "Choose Binomial(30, p) for the fixed independent inspection story; with p = 0.1, P(X = 0) ≈ 0.0424. Refuse hypergeometric for this generative story.": "Choose $\\mathrm{Binomial}(30, p)$ for the fixed independent inspection story; with $p = 0.1$, $P(X = 0) \\approx 0.0424$. Refuse hypergeometric for this generative story.",
    # --- 2.1.6 software generation ---
    "Closed-book. You simulate Poisson(λ=3) counts and Exponential waiting times with mean 2. Which statement is correct?": "Closed-book. You simulate $\\mathrm{Poisson}(\\lambda=3)$ counts and Exponential waiting times with mean 2. Which statement is correct?",
    "Poisson draws should average near 2 and Exponential draws near 3 because λ is a waiting-time mean.": "Poisson draws should average near 2 and Exponential draws near 3 because $\\lambda$ is a waiting-time mean.",
    "An analyst needs software samples from two univariate families before any joint modelling: (i) annual claim counts as Poisson(λ = 3); (ii) inter-claim waiting times (days) as Exponential with mean θ = 5. Describe the generation plan for n = 50 draws of each family, state one sanity check for each sample, and decide whether a mean of 3.1 on the Poisson sample alone proves the software call was correct.": "An analyst needs software samples from two univariate families before any joint modelling: (i) annual claim counts as $\\mathrm{Poisson}(\\lambda = 3)$; (ii) inter-claim waiting times (days) as Exponential with mean $\\theta = 5$. Describe the generation plan for $n = 50$ draws of each family, state one sanity check for each sample, and decide whether a mean of 3.1 on the Poisson sample alone proves the software call was correct.",
    "Poisson(λ = 3)": "$\\mathrm{Poisson}(\\lambda = 3)$",
    "Exponential(mean θ = 5)": "Exponential(mean $\\theta = 5$)",
    "Poisson: all ≥ 0 integers, mean ≈ 3; Exponential: all > 0, mean ≈ 5": "Poisson: all $\\geq 0$ integers, mean $\\approx 3$; Exponential: all $> 0$, mean $\\approx 5$",
    "3.1 ≈ 3 is consistent, not a proof of correct generation": "$3.1 \\approx 3$ is consistent, not a proof of correct generation",
    # --- 5.1.2 prior-posterior cs1003 ---
    "Prior: belief about θ before data. Posterior: updated belief after data. Conjugate: prior family closed under updating so posterior stays in the same family. Example: Beta-Binomial or Gamma-Poisson. The prior is not the last sample; conjugate language structures the update but you still obtain the posterior from prior plus data.": "Prior: belief about $\\theta$ before data. Posterior: updated belief after data. Conjugate: prior family closed under updating so posterior stays in the same family. Example: Beta-Binomial or Gamma-Poisson. The prior is not the last sample; conjugate language structures the update but you still obtain the posterior from prior plus data.",
    "A portfolio claim probability θ has prior Beta(α, β) = Beta(3, 5). In a new sample of n = 12 independent risks, s = 4 claims are observed (Binomial likelihood). Using conjugacy, state the posterior distribution and compare prior and posterior means.": "A portfolio claim probability $\\theta$ has prior $\\mathrm{Beta}(\\alpha, \\beta) = \\mathrm{Beta}(3, 5)$. In a new sample of $n = 12$ independent risks, $s = 4$ claims are observed (Binomial likelihood). Using conjugacy, state the posterior distribution and compare prior and posterior means.",
    "Posterior = Beta(3+4, 5+12−4) = Beta(7, 13)": "Posterior $= \\mathrm{Beta}(3+4, 5+12-4) = \\mathrm{Beta}(7, 13)$",
    # --- cr-2.1.2 continuous ---
    "Normal(μ, σ²) is appropriate because the central limit theorem always makes waiting times Normal regardless of support.": "$\\mathrm{Normal}(\\mu, \\sigma^{2})$ is appropriate because the central limit theorem always makes waiting times Normal regardless of support.",
    "Inter-claim waiting times are strictly positive and, under a constant hazard story, memoryless. Choose the matching continuous family. As a light numeric check, if the mean waiting time is 6 months, compute P(T > 6).": "Inter-claim waiting times are strictly positive and, under a constant hazard story, memoryless. Choose the matching continuous family. As a light numeric check, if the mean waiting time is 6 months, compute $P(T > 6)$.",
    "Light numeric illustration P(T > 6)": "Light numeric illustration $P(T > 6)$",
    "With mean θ = 6, P(T > t) = e^{−t/θ}. At the mean, survival equals e^{−1}. The numeric check illustrates the chosen family; family selection remains the LO hinge.": "With mean $\\theta = 6$, $P(T > t) = e^{-t/\\theta}$. At the mean, survival equals $e^{-1}$. The numeric check illustrates the chosen family; family selection remains the LO hinge.",
    "P(T > 6) = e^{−6/6} = e^{−1} ≈ 0.3679": "$P(T > 6) = e^{-6/6} = e^{-1} \\approx 0.3679$",
    "P(T > 6) ≈ 0.3679": "$P(T > 6) \\approx 0.3679$",
    "Choose Exponential for positive memoryless waiting times; with mean 6 months, P(T > 6) ≈ 0.3679. Refuse Normal-by-default for this story.": "Choose Exponential for positive memoryless waiting times; with mean 6 months, $P(T > 6) \\approx 0.3679$. Refuse Normal-by-default for this story.",
    # --- revision-estimators ---
    "MSE(T) = Var(T) + Bias(T) squared.": "$\\mathrm{MSE}(T) = \\operatorname{Var}(T) + \\mathrm{Bias}(T)^{2}$.",
    "MSE(T) = Var(T) + Bias(T).": "$\\mathrm{MSE}(T) = \\operatorname{Var}(T) + \\mathrm{Bias}(T)$.",
    "MSE(T) = Var(T) for every estimator.": "$\\mathrm{MSE}(T) = \\operatorname{Var}(T)$ for every estimator.",
    "Closed-book retrieval. Distinguish method of moments from maximum likelihood in one sentence each. An estimator T of θ has Bias(T) = 3 and Var(T) = 7. Compute MSE(T), and refuse treating unbiasedness alone as minimum MSE.": "Closed-book retrieval. Distinguish method of moments from maximum likelihood in one sentence each. An estimator $T$ of $\\theta$ has $\\mathrm{Bias}(T) = 3$ and $\\operatorname{Var}(T) = 7$. Compute $\\mathrm{MSE}(T)$, and refuse treating unbiasedness alone as minimum MSE.",
    "Var(T)": "$\\operatorname{Var}(T)$",
    "MSE(T) = 7 + 3² = 7 + 9 = 16": "$\\mathrm{MSE}(T) = 7 + 3^{2} = 7 + 9 = 16$",
    # --- revision-regression-glm ---
    "Closed-book retrieval. State what the sequence Family → η → link means in a generalised linear model. For a Poisson GLM, name the canonical link and state what deviance compares.": "Closed-book retrieval. State what the sequence Family $\\rightarrow \\eta \\rightarrow$ link means in a generalised linear model. For a Poisson GLM, name the canonical link and state what deviance compares.",
    "Family → η → link": "Family $\\rightarrow \\eta \\rightarrow$ link",
    "Family = mean-variance; η = Xβ; g(μ) = η": "Family = mean-variance; $\\eta = X\\beta$; $g(\\mu) = \\eta$",
    "Canonical link: log(μ) = η": "Canonical link: $\\log(\\mu) = \\eta$",
    "Family specifies mean-variance behaviour, η = Xβ is the linear predictor, and g(μ) = η is the link. For Poisson, the canonical link is log(μ) = η, and deviance compares fitted and saturated models through likelihoods.": "Family specifies mean-variance behaviour, $\\eta = X\\beta$ is the linear predictor, and $g(\\mu) = \\eta$ is the link. For Poisson, the canonical link is $\\log(\\mu) = \\eta$, and deviance compares fitted and saturated models through likelihoods.",
    # --- 1.2.2 eda association ---
    "For annual mileage versus claim severity, severity is skewed with outliers and the scatter looks roughly increasing but nonlinear. Software reports Pearson r = 0.25 and Spearman ρ = 0.52. Which correlation measure should you prefer for describing the association, and what must you still refuse?": "For annual mileage versus claim severity, severity is skewed with outliers and the scatter looks roughly increasing but nonlinear. Software reports Pearson $r = 0.25$ and Spearman $\\rho = 0.52$. Which correlation measure should you prefer for describing the association, and what must you still refuse?",
    "Spearman ρ": "Spearman $\\rho$",
    "|ρ| = 0.52 > |r| = 0.25; rank measure captures monotone association better here": "$|\\rho| = 0.52 > |r| = 0.25$; rank measure captures monotone association better here",
    "Report Spearman ρ = 0.52 as the preferred description": "Report Spearman $\\rho = 0.52$ as the preferred description",
    "Association ≠ causation (even if |ρ| is large)": "Association $\\neq$ causation (even if $|\\rho|$ is large)",
    "Prefer Spearman ρ = 0.52 (monotone, skewed, outlier-prone) over Pearson r = 0.25. A large coefficient still does not prove causation.": "Prefer Spearman $\\rho = 0.52$ (monotone, skewed, outlier-prone) over Pearson $r = 0.25$. A large coefficient still does not prove causation.",
    # --- 2.1.2 continuous ---
    "Individual claim severities are strictly positive and strongly right-skewed on the raw scale, with a roughly symmetric shape after taking logs. Choose the matching continuous family. As a light numeric check, if ln(X) ~ Normal(μ = 6, σ = 1), compute the median of X.": "Individual claim severities are strictly positive and strongly right-skewed on the raw scale, with a roughly symmetric shape after taking logs. Choose the matching continuous family. As a light numeric check, if $\\ln(X) \\sim \\mathrm{Normal}(\\mu = 6, \\sigma = 1)$, compute the median of $X$.",
    "Normal(μ = 6, σ = 1)": "$\\mathrm{Normal}(\\mu = 6, \\sigma = 1)$",
    "median(X) = e^6 ≈ 403.43": "$\\mathrm{median}(X) = e^{6} \\approx 403.43$",
    "median(X) ≈ 403.43": "$\\mathrm{median}(X) \\approx 403.43$",
    "Choose Lognormal for positive right-skewed severities that are Normal on the log scale; with ln(X) ~ Normal(6, 1), median(X) = e^6 ≈ 403.43. Refuse Normal-by-default on the raw severity scale.": "Choose Lognormal for positive right-skewed severities that are Normal on the log scale; with $\\ln(X) \\sim \\mathrm{Normal}(6, 1)$, $\\mathrm{median}(X) = e^{6} \\approx 403.43$. Refuse Normal-by-default on the raw severity scale.",
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 9 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave8.EXPLICIT:
        return wave8.EXPLICIT[text]
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


def wave9_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE9_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave9_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE9_FILES:
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

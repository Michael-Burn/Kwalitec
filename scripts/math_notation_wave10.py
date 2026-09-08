#!/usr/bin/env python3
"""Wave 10 mathematical notation migration (final confident backlog).

Converts confident ``needs_migration`` strings in the 12 remaining packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Wave 10 is the final tranche after Waves 1–9 (ledger ranking by tier-1 then
needs_migration). Confirmed scope: 29 needs_migration strings, all confident
(0 with needs_manual_review on the needs_migration category). Sixteen
correctly_excluded strings in these packages still carry needs_manual_review
and are left untouched for the proposal document.

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave10.py --dry-run
    python scripts/math_notation_wave10.py --apply
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
import math_notation_wave9 as wave9  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

# Final 12 by ledger ranking after Waves 1–9 (zero overlap with prior 108).
WAVE10_FILES = (
    "5.1.4-loss-estimators-cs1003.json",
    "5.1.5-credible-intervals-cs1003.json",
    "revision-bayesian-cs1015.json",
    "revision-hypothesis-testing-cs1012.json",
    "revision-midspine-cs1003.json",
    "1.2.3-pca-cs1002.json",
    "4.1.1-response-explanatory-cs1003.json",
    "4.1.1-response-explanatory-cs1013.json",
    "cp-4.1.1-linear-regression-cs1016.json",
    "cr-1.1.3-data-sources-cs1017.json",
    "cr-1.1.2-stages-tools-cs1017.json",
    "cr-1.2.3-pca-cs1017.json",
)

EXPLICIT: dict[str, str] = {
    # --- 5.1.4 loss estimators ---
    "Closed-book. Posterior for θ is available. Which statement is correct?": (
        "Closed-book. Posterior for $\\theta$ is available. Which statement is correct?"
    ),
    (
        "Under squared-error loss, use the posterior mean as the Bayesian point estimator; "
        "under absolute-error loss, use the posterior median. Just taking the posterior mode "
        "always is not warranted without an explicit loss. A point estimator summarises the "
        "posterior under a loss; a credible interval is a posterior probability set for θ. "
        "Different objects."
    ): (
        "Under squared-error loss, use the posterior mean as the Bayesian point estimator; "
        "under absolute-error loss, use the posterior median. Just taking the posterior mode "
        "always is not warranted without an explicit loss. A point estimator summarises the "
        "posterior under a loss; a credible interval is a posterior probability set for "
        "$\\theta$. Different objects."
    ),
    (
        "A discrete posterior for an IBNR reserve parameter θ (£000) places probabilities "
        "0.15, 0.55, 0.30 on the values 4, 5, 7 respectively. Find the Bayes estimate under "
        "squared-error loss and under absolute-error loss."
    ): (
        "A discrete posterior for an IBNR reserve parameter $\\theta$ (£000) places "
        "probabilities 0.15, 0.55, 0.30 on the values 4, 5, 7 respectively. Find the Bayes "
        "estimate under squared-error loss and under absolute-error loss."
    ),
    "θ values": "$\\theta$ values",
    "E[θ|data] = 4×0.15 + 5×0.55 + 7×0.30 = 0.6 + 2.75 + 2.1 = 5.45": (
        "$E[\\theta \\mid \\mathrm{data}] = 4\\times 0.15 + 5\\times 0.55 + 7\\times 0.30 "
        "= 0.6 + 2.75 + 2.1 = 5.45$"
    ),
    "Mean 5.45 ≠ median 5 because of right-tail mass at 7": (
        "Mean $5.45 \\neq$ median $5$ because of right-tail mass at $7$"
    ),
    # --- 5.1.5 credible intervals ---
    (
        "After observing claim experience, the posterior for mean ultimate cost θ (£000) is "
        "Normal with mean 250 and standard deviation 8: θ | data ~ N(250, 8²). Using "
        "z_{0.975} = 1.96, construct a central 95% credible interval for θ."
    ): (
        "After observing claim experience, the posterior for mean ultimate cost $\\theta$ "
        "(£000) is Normal with mean 250 and standard deviation 8: "
        "$\\theta \\mid \\mathrm{data} \\sim N(250, 8^{2})$. Using $z_{0.975} = 1.96$, "
        "construct a central 95% credible interval for $\\theta$."
    ),
    "N(250, 8²)": "$N(250, 8^{2})$",
    "250 ± 1.96 × 8 = 250 ± 15.68 ⇒ (234.32, 265.68)": (
        "$250 \\pm 1.96 \\times 8 = 250 \\pm 15.68 \\Rightarrow (234.32, 265.68)$"
    ),
    "P(234.32 < θ < 265.68 | data) = 0.95": (
        "$P(234.32 < \\theta < 265.68 \\mid \\mathrm{data}) = 0.95$"
    ),
    (
        "Central 95% credible interval (234.32, 265.68); "
        "P(234.32 < θ < 265.68 | data) = 0.95."
    ): (
        "Central 95% credible interval $(234.32, 265.68)$; "
        "$P(234.32 < \\theta < 265.68 \\mid \\mathrm{data}) = 0.95$."
    ),
    # --- revision-bayesian ---
    (
        "Closed-book retrieval. Write the Bayesian posterior for θ after observing data y "
        "up to proportionality. Then, if the posterior for θ is Normal with mean 60 and "
        "standard deviation 4, compute a central 95% credible interval (use z_{0.025} = 1.96), "
        "and refuse a frequentist repeated-sampling reading of that interval."
    ): (
        "Closed-book retrieval. Write the Bayesian posterior for $\\theta$ after observing "
        "data $y$ up to proportionality. Then, if the posterior for $\\theta$ is Normal with "
        "mean 60 and standard deviation 4, compute a central 95% credible interval "
        "(use $z_{0.025} = 1.96$), and refuse a frequentist repeated-sampling reading of "
        "that interval."
    ),
    "posterior ∝ likelihood × prior": (
        "$\\mathrm{posterior} \\propto \\mathrm{likelihood} \\times \\mathrm{prior}$"
    ),
    "posterior(θ|y) ∝ likelihood(y|θ) × prior(θ)": (
        "$\\mathrm{posterior}(\\theta \\mid y) \\propto "
        "\\mathrm{likelihood}(y \\mid \\theta) \\times \\mathrm{prior}(\\theta)$"
    ),
    "60 ± 1.96×4 = 60 ± 7.84 → (52.16, 67.84)": (
        "$60 \\pm 1.96\\times 4 = 60 \\pm 7.84 \\rightarrow (52.16, 67.84)$"
    ),
    (
        "posterior(θ|y) ∝ likelihood(y|θ) × prior(θ). The Normal(60, 4²) central 95% "
        "credible interval is (52.16, 67.84), meaning posterior probability 0.95 under the "
        "model, prior, and data - not frequentist repeated-sampling coverage."
    ): (
        "$\\mathrm{posterior}(\\theta \\mid y) \\propto "
        "\\mathrm{likelihood}(y \\mid \\theta) \\times \\mathrm{prior}(\\theta)$. "
        "The $\\mathrm{Normal}(60, 4^{2})$ central 95% credible interval is "
        "$(52.16, 67.84)$, meaning posterior probability 0.95 under the model, prior, and "
        "data - not frequentist repeated-sampling coverage."
    ),
    # --- revision-hypothesis-testing ---
    "Small p ⇒ evidence against H₀ under assumptions (not automatic proof)": (
        "Small $p \\Rightarrow$ evidence against $H_{0}$ under assumptions "
        "(not automatic proof)"
    ),
    (
        "A small p-value does not prove the alternative with probability one, does not "
        "equal P(H₀ true), and does not by itself measure practical importance."
    ): (
        "A small p-value does not prove the alternative with probability one, does not "
        "equal $P(H_{0}\\ \\mathrm{true})$, and does not by itself measure practical "
        "importance."
    ),
    "Refuse P(H₀ true) reading and proof/importance collapse": (
        "Refuse $P(H_{0}\\ \\mathrm{true})$ reading and proof/importance collapse"
    ),
    (
        "A p-value is a null-conditional tail probability measuring extremeness of the "
        "observed statistic. A very small p-value is evidence against the null under the "
        "assumptions, not proof of the alternative, not P(H₀ true), and not a measure of "
        "practical importance by itself."
    ): (
        "A p-value is a null-conditional tail probability measuring extremeness of the "
        "observed statistic. A very small p-value is evidence against the null under the "
        "assumptions, not proof of the alternative, not $P(H_{0}\\ \\mathrm{true})$, and "
        "not a measure of practical importance by itself."
    ),
    # --- revision-midspine ---
    (
        "Closed-book retrieval of one Bayes hinge. If X | θ ~ Binomial(n = 8, θ) and θ has "
        "prior Beta(α, β) = Beta(4, 6), state the posterior after observing X = 2, and "
        "refuse one wrong update rule."
    ): (
        "Closed-book retrieval of one Bayes hinge. If "
        "$X \\mid \\theta \\sim \\mathrm{Binomial}(n = 8, \\theta)$ and $\\theta$ has "
        "prior $\\mathrm{Beta}(\\alpha, \\beta) = \\mathrm{Beta}(4, 6)$, state the "
        "posterior after observing $X = 2$, and refuse one wrong update rule."
    ),
    "X | θ ~ Binomial(8, θ)": (
        "$X \\mid \\theta \\sim \\mathrm{Binomial}(8, \\theta)$"
    ),
    # --- 1.2.3 pca ---
    "Variation summary ≠ proven latent pricing factors without further warrants": (
        "Variation summary $\\neq$ proven latent pricing factors without further warrants"
    ),
    # --- 4.1.1 response-explanatory (and siblings) ---
    "ŷ(8) = 2500 + 150 × 8 = 2500 + 1200 = 3700": (
        "$\\hat{y}(8) = 2500 + 150 \\times 8 = 2500 + 1200 = 3700$"
    ),
    "ŷ(45) = 1200 + 40 × 45 = 1200 + 1800 = 3000": (
        "$\\hat{y}(45) = 1200 + 40 \\times 45 = 1200 + 1800 = 3000$"
    ),
    "ŷ(25) = 180 + 12 × 25 = 180 + 300 = 480": (
        "$\\hat{y}(25) = 180 + 12 \\times 25 = 180 + 300 = 480$"
    ),
    # --- cr-1.1.3 data sources ---
    "Large n ≠ automatic fitness; scale may still require sampling/tooling": (
        "Large $n \\neq$ automatic fitness; scale may still require sampling/tooling"
    ),
    # --- cr-1.1.2 stages tools ---
    "Tool class for explore: summaries / exploratory plots; notebook-open ≠ path complete": (
        "Tool class for explore: summaries / exploratory plots; "
        "notebook-open $\\neq$ path complete"
    ),
    # --- cr-1.2.3 pca ---
    "Variation summary ≠ proven causal driver": (
        "Variation summary $\\neq$ proven causal driver"
    ),
}


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string using Wave 10 EXPLICIT then prior helpers."""
    if text in EXPLICIT:
        return EXPLICIT[text]
    if text in wave9.EXPLICIT:
        return wave9.EXPLICIT[text]
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


def wave10_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE10_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave10_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE10_FILES:
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

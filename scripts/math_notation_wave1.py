#!/usr/bin/env python3
"""Wave 1 mathematical notation migration (authored CS1 packages).

Converts confident ``needs_migration`` strings in the 12 Wave 1 packages
into $-delimited LaTeX per ``docs/content/MATHEMATICAL_NOTATION_STANDARD.md``.

Does not modify scoring keys (accepted_keywords, correct_choice_id,
numeric_tolerance, choice ids). Leaves ``needs_manual_review`` strings
untouched.

Usage:
    python scripts/math_notation_wave1.py --dry-run
    python scripts/math_notation_wave1.py --apply
"""

# Mapping keys are verbatim package strings; line length is expected.
# ruff: noqa: E501

from __future__ import annotations

import argparse
import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402

CATALOGUE = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"

WAVE1_FILES = (
    "4.1.3-least-squares-cs1003.json",
    "4.1.3-least-squares-cs1013.json",
    "4.2.8-residuals-cs1014.json",
    "4.2.8-residuals-cs1003.json",
    "2.6.3-mean-var-sample-cs1009.json",
    "2.6.5-t-statistic-cs1009.json",
    "3.1.2-maximum-likelihood-cs1010.json",
    "3.2.5-ci-binomial-poisson-cs1011.json",
    "2.5.1-clt-cs1008.json",
    "2.6.4-normal-sample-mean-var-cs1009.json",
    "3.1.4-comparison-mse-cs1010.json",
    "3.1.1-method-of-moments-cs1010.json",
)

BOARD_SUFFIXES = (
    ".calculation",
    ".result",
    ".final_answer",
    ".symbol",
    ".value",
)

# Whole-string math boards: convert then wrap (possibly splitting on ';').
_BOARD_PATH = re.compile(
    r"(?:calculation|result|final_answer|given\[\d+\]\.(?:symbol|value))$"
)


def parse_path(path: str) -> list[str | int]:
    parts: list[str | int] = []
    for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)|\[(\d+)\]", path):
        if match.group(1):
            parts.append(match.group(1))
        else:
            parts.append(int(match.group(2)))
    return parts


def get_path(obj: Any, path: str) -> Any:
    cur = obj
    for part in parse_path(path):
        cur = cur[part]
    return cur


def set_path(obj: Any, path: str, value: Any) -> None:
    parts = parse_path(path)
    cur = obj
    for part in parts[:-1]:
        cur = cur[part]
    cur[parts[-1]] = value


def _nfd(text: str) -> str:
    return unicodedata.normalize("NFD", text)


def _wrap(latex: str) -> str:
    latex = latex.strip()
    if not latex:
        return latex
    if latex.startswith("$") and latex.endswith("$"):
        return latex
    return f"${latex}$"


def _merge_adjacent_math(text: str) -> str:
    """Join immediately adjacent inline maths so `$a$$b$` cannot form `$$`."""
    previous = None
    while previous != text:
        previous = text
        text = re.sub(r"\$([^$]+)\$\$([^$]+)\$", r"$\1 \2$", text)
    # `$a$ = $b$` (only math punctuation between) → one island.
    text = re.sub(
        r"\$([^$]+)\$(\s*[=≈≠≤≥<>∼~\+\-−×/]\s*)\$([^$]+)\$",
        lambda m: _wrap(m.group(1) + m.group(2) + m.group(3)),
        text,
    )
    return text


def latexify(text: str) -> str:
    """Convert Unicode / actuarial notation into LaTeX *without* delimiters."""
    s = _nfd(text)

    # Combining decorations (after NFD).
    s = re.sub(r"([A-Za-zμσλβθΦχℓΕε])\u0302", r"\\hat{\1}", s)
    s = re.sub(r"([A-Za-zμσλβθΦχℓΕε])\u0304", r"\\bar{\1}", s)
    s = re.sub(r"([A-Za-zμσλβθΦχℓΕε])\u0305", r"\\bar{\1}", s)

    # Precomposed / remaining named letters.
    greek = {
        "μ": r"\mu",
        "σ": r"\sigma",
        "λ": r"\lambda",
        "β": r"\beta",
        "θ": r"\theta",
        "χ": r"\chi",
        "Φ": r"\Phi",
        "φ": r"\phi",
        "ε": r"\varepsilon",
        "ℓ": r"\ell",
        "α": r"\alpha",
        "Σ": r"\sum",
        "ȳ": r"\bar{y}",
        "ŷ": r"\hat{y}",
    }
    for src, dst in greek.items():
        s = s.replace(src, dst)
    # `\lambdax` is not a KaTeX command; insert a space after a control word
    # when a letter follows (e^{-\lambda x}).
    s = re.sub(
        r"(\\(?:mu|sigma|lambda|beta|theta|chi|Phi|phi|alpha|ell|varepsilon|sum|ln|log|times|approx|neq|leq|geq|sim|Rightarrow|ldots|mathrm|operatorname|widehat|hat|bar|frac|sqrt))(?=[A-Za-z])",
        r"\1 ",
        s,
    )

    # Unicode operators and scripts.
    s = s.replace("−", "-")
    s = s.replace("×", r"\times ")
    s = s.replace("≈", r"\approx ")
    # NFC ≠ and NFD (= + combining solidus U+0338); NFD runs first above.
    s = s.replace("≠", r"\neq ")
    s = s.replace("=\u0338", r"\neq ")
    s = s.replace("≤", r"\leq ")
    s = s.replace("≥", r"\geq ")
    s = s.replace("⇒", r"\Rightarrow ")
    s = s.replace("∼", r"\sim ")
    s = s.replace("…", r"\ldots ")
    s = s.replace("²", r"^{2}")
    s = s.replace("³", r"^{3}")
    s = s.replace("ᵢ", r"_{i}")
    s = s.replace("₀", r"_{0}")
    s = s.replace("₁", r"_{1}")
    s = s.replace("₂", r"_{2}")
    s = s.replace("₅", r"_{5}")

    # Functions with hats (estimator notation).
    s = s.replace(r"\hat{Cov}", r"\widehat{\operatorname{Cov}}")
    s = s.replace(r"\hat{Var}", r"\widehat{\operatorname{Var}}")
    s = s.replace(r"\hat{SE}", r"\widehat{\mathrm{SE}}")
    s = re.sub(r"\bCov\(", r"\\operatorname{Cov}(", s)
    s = re.sub(r"\bCorr\(", r"\\operatorname{Corr}(", s)
    s = re.sub(r"\bVar\(", r"\\operatorname{Var}(", s)
    s = re.sub(r"\bBias\(", r"\\operatorname{Bias}(", s)
    s = re.sub(r"\bMSE\(", r"\\operatorname{MSE}(", s)
    s = re.sub(r"\bsd\(", r"\\operatorname{sd}(", s)
    s = re.sub(r"\bsign\(", r"\\operatorname{sign}(", s)
    s = re.sub(r"\bln\b", r"\\ln", s)
    s = re.sub(r"\blog\b", r"\\log", s)

    # Bare e^{...} fragments already in packages.
    s = s.replace("e^{−", r"e^{-")
    s = s.replace("e^{-\\lambda x}", r"e^{-\\lambda x}")

    # Roots: parenthesised, then numeric, then identifier / latex command.
    s = re.sub(r"√\(([^)]+)\)", r"\\sqrt{\1}", s)
    s = re.sub(r"√(\d+(?:\.\d+)?)", r"\\sqrt{\1}", s)
    s = re.sub(
        r"√((?:\\[a-zA-Z]+(?:\{[^}]+\})?|\\hat\{[^}]+\}|[A-Za-z]+))",
        r"\\sqrt{\1}",
        s,
    )
    s = s.replace("sqrt(", r"\sqrt{")  # rare ASCII; closer patched below if needed

    # Subscripts written with underscore ASCII (S_xx, t_{n-1}, χ²_15).
    s = re.sub(r"\bS_xx\b", r"S_{xx}", s)
    s = re.sub(r"\bS_xy\b", r"S_{xy}", s)
    s = re.sub(r"\bS_yy\b", r"S_{yy}", s)
    s = re.sub(r"\br_P\b", r"r_{P}", s)
    s = re.sub(r"\br_D\b", r"r_{D}", s)
    s = re.sub(r"\\chi\^{2}_(\d+)", r"\\chi^{2}_{\1}", s)
    s = re.sub(r"\\chi\^{2}_\{([^}]+)\}", r"\\chi^{2}_{\1}", s)
    s = re.sub(r"\bt_\{([^}]+)\}", r"t_{\1}", s)
    s = re.sub(r"\bt_(\d+)\b", r"t_{\1}", s)
    s = re.sub(r"\bz_\{([^}]+)\}", r"z_{\1}", s)
    s = re.sub(r"\bT₁\b", r"T_{1}", s)
    s = re.sub(r"\bT₂\b", r"T_{2}", s)
    s = re.sub(r"T_1", r"T_{1}", s)
    s = re.sub(r"T_2", r"T_{2}", s)
    s = re.sub(r"\\hat\{\\theta\}_1", r"\\hat{\\theta}_{1}", s)
    s = re.sub(r"\\hat\{\\theta\}_2", r"\\hat{\\theta}_{2}", s)
    s = re.sub(r"\\hat\{\\beta\}_0", r"\\hat{\\beta}_{0}", s)
    s = re.sub(r"\\hat\{\\beta\}_1", r"\\hat{\\beta}_{1}", s)
    s = re.sub(r"\\beta_0", r"\\beta_{0}", s)
    s = re.sub(r"\\beta_1", r"\\beta_{1}", s)
    s = re.sub(r"\\hat\{\\lambda\}_MLE", r"\\hat{\\lambda}_{\\mathrm{MLE}}", s)
    s = re.sub(r"\\hat\{\\mu\}_MoM", r"\\hat{\\mu}_{\\mathrm{MoM}}", s)
    s = re.sub(r"\\hat\{\\mu\}_MLE", r"\\hat{\\mu}_{\\mathrm{MLE}}", s)
    s = re.sub(r"\bMoM\b", r"\\mathrm{MoM}", s)
    s = re.sub(r"\bMLE\b", r"\\mathrm{MLE}", s)

    # x_i / y_i written as xi, yi in formula context (not "maximum").
    s = re.sub(r"\bxi\b", r"x_{i}", s)
    s = re.sub(r"\byi\b", r"y_{i}", s)

    # Derivatives before generic fractions.
    s = s.replace(r"d^{2}\ell/d\lambda^{2}", r"\frac{d^{2}\ell}{d\lambda^{2}}")
    s = s.replace(r"d\ell/d\lambda", r"\frac{d\ell}{d\lambda}")
    s = s.replace(r"dℓ/dλ", r"\frac{d\ell}{d\lambda}")

    # Specific / corpus fractions (longest first).
    fraction_subs = [
        (r"\\sigma\^{2}/n", r"\\frac{\\sigma^{2}}{n}"),
        (r"\\sigma / \\sqrt\{n\}", r"\\frac{\\sigma}{\\sqrt{n}}"),
        (r"\\sigma/\\sqrt\{n\}", r"\\frac{\\sigma}{\\sqrt{n}}"),
        (r"S/\\sqrt\{n\}", r"\\frac{S}{\\sqrt{n}}"),
        (r"S / \\sqrt\{n\}", r"\\frac{S}{\\sqrt{n}}"),
        (r"S_\{\\mathrm\{xy\}\}/S_\{\\mathrm\{xx\}\}", r"\\frac{S_{xy}}{S_{xx}}"),
        (r"S_\{xy\}/S_\{xx\}", r"\\frac{S_{xy}}{S_{xx}}"),
        (r"S_\{xy\}/S_\{yy\}", r"\\frac{S_{xy}}{S_{yy}}"),
        (r"\(n-1\)S\^{2}/\\sigma\^{2}", r"\\frac{(n-1)S^{2}}{\\sigma^{2}}"),
        (r"\(n - 1\)S\^{2}/\\sigma\^{2}", r"\\frac{(n-1)S^{2}}{\\sigma^{2}}"),
        (r"15 S\^{2}/25", r"\\frac{15 S^{2}}{25}"),
        (r"\\hat\{p\}\(1-\\hat\{p\}\)/n", r"\\frac{\\hat{p}(1-\\hat{p})}{n}"),
        (r"\\hat\{\\lambda\}/n", r"\\frac{\\hat{\\lambda}}{n}"),
        (r"\\hat\{p\}/n", r"\\frac{\\hat{p}}{n}"),
        (r"s\^{2}/n", r"\\frac{s^{2}}{n}"),
        (r"\\mu/n", r"\\frac{\\mu}{n}"),
        (r"2/n", r"\\frac{2}{n}"),
        (r"0\.5/n", r"\\frac{0.5}{n}"),
        (r"0\.75/n", r"\\frac{0.75}{n}"),
        (r"0\.25/n", r"\\frac{0.25}{n}"),
        (r"0\.5/\\sqrt\{n\}", r"\\frac{0.5}{\\sqrt{n}}"),
        (r"0\.25/\\sqrt\{n\}", r"\\frac{0.25}{\\sqrt{n}}"),
        (r"4/\\lambda", r"\\frac{4}{\\lambda}"),
        (r"-4/\\lambda\^{2}", r"-\\frac{4}{\\lambda^{2}}"),
        (r"4/10", r"\\frac{4}{10}"),
        (r"8/5", r"\\frac{8}{5}"),
        (r"7/5", r"\\frac{7}{5}"),
        (r"22/100", r"\\frac{22}{100}"),
        (r"14/4", r"\\frac{14}{4}"),
        (r"26/4", r"\\frac{26}{4}"),
        (r"10/4", r"\\frac{10}{4}"),
        (r"16/4", r"\\frac{16}{4}"),
        (r"36 / 9", r"\\frac{36}{9}"),
        (r"36/9", r"\\frac{36}{9}"),
        (r"25/16", r"\\frac{25}{16}"),
        (r"11000/5", r"\\frac{11000}{5}"),
        (r"9/6", r"\\frac{9}{6}"),
        (r"3/6", r"\\frac{3}{6}"),
        (r"9/4", r"\\frac{9}{4}"),
        (r"\(2\+3\+4\+5\)/4", r"\\frac{2+3+4+5}{4}"),
        (r"\(4\+6\+7\+9\)/4", r"\\frac{4+6+7+9}{4}"),
        (r"\(1\+2\+3\+4\)/4", r"\\frac{1+2+3+4}{4}"),
        (r"\(2\+3\+5\+6\)/4", r"\\frac{2+3+5+6}{4}"),
        (r"\(2400 \+ 1600 \+ 3200 \+ 1800 \+ 2000\)/5",
         r"\\frac{2400 + 1600 + 3200 + 1800 + 2000}{5}"),
        (r"60 / \\sqrt\{36\}", r"\\frac{60}{\\sqrt{36}}"),
        (r"60 / 6", r"\\frac{60}{6}"),
        (r"8 / \\sqrt\{16\}", r"\\frac{8}{\\sqrt{16}}"),
        (r"8 / 4", r"\\frac{8}{4}"),
        (r"\(9 - 4\) / \\sqrt\{4\}", r"\\frac{9 - 4}{\\sqrt{4}}"),
        (r"5 / 2", r"\\frac{5}{2}"),
        (r"\(3 - 6\)/\\sqrt\{6\}", r"\\frac{3 - 6}{\\sqrt{6}}"),
        (r"-3/\\sqrt\{6\}", r"-\\frac{3}{\\sqrt{6}}"),
        (r"\(170 - 180\)/10", r"\\frac{170 - 180}{10}"),
        (r"\(170 - 180\)/60", r"\\frac{170 - 180}{60}"),
        (r"\(105 - 100\)/2", r"\\frac{105 - 100}{2}"),
        (r"\(105 - 100\)/\(8/4\)", r"\\frac{105 - 100}{8/4}"),
        (r"-1/6", r"-\\frac{1}{6}"),
        (r"1/\\mu", r"\\frac{1}{\\mu}"),
        (r"1/2200", r"\\frac{1}{2200}"),
        (r"1/5", r"\\frac{1}{5}"),
        (r"y/\\hat\{\\mu\}", r"\\frac{y}{\\hat{\\mu}}"),
        (r"\\hat\{\\operatorname\{Cov\}\}\(X, Y\) / \\widehat\{\\operatorname\{Var\}\}\(X\)",
         r"\\frac{\\widehat{\\operatorname{Cov}}(X, Y)}{\\widehat{\\operatorname{Var}}(X)}"),
        (r"\\widehat\{\\operatorname\{Cov\}\}\(X, Y\) / \\widehat\{\\operatorname\{Var\}\}\(X\)",
         r"\\frac{\\widehat{\\operatorname{Cov}}(X, Y)}{\\widehat{\\operatorname{Var}}(X)}"),
        (r"\\widehat\{\\operatorname\{Cov\}\}/\\widehat\{\\operatorname\{Var\}\}",
         r"\\frac{\\widehat{\\operatorname{Cov}}}{\\widehat{\\operatorname{Var}}}"),
        (r"\\operatorname\{Cov\}̂/\\operatorname\{Var\}̂",
         r"\\frac{\\widehat{\\operatorname{Cov}}}{\\widehat{\\operatorname{Var}}}"),
    ]
    for pat, repl in fraction_subs:
        s = re.sub(pat, repl, s)

    # Generic (y - μ̂) / √V(μ̂) family after other conversions.
    s = re.sub(
        r"\(([^()]+)\)\s*/\s*\\sqrt\{([^}]+)\}",
        r"\\frac{\1}{\\sqrt{\2}}",
        s,
    )
    s = re.sub(
        r"\\hat\{\\mu\}/\\sqrt\{V\(\\hat\{\\mu\}\)\}",
        r"\\frac{\\hat{\\mu}}{\\sqrt{V(\\hat{\\mu})}}",
        s,
    )

    # Remaining ASCII slash between tight math atoms: a/b numbers already done.
    s = re.sub(r"~+", r"\\sim ", s)

    # Collapse extra spaces introduced by operator tokens, keep single spaces.
    s = re.sub(r"[ \t]+", " ", s)
    s = s.replace(r"\times  ", r"\times ")
    s = s.replace(r"\approx  ", r"\approx ")
    return s.strip()


# Explicit whole-string overrides for formula spellings that mix English
# operators with live mathematics (MCQ OLS boards). Keys are exact originals.
EXPLICIT: dict[str, str] = {
    (
        "Choose β₀, β₁ to minimise sum (yi minus β₀ minus β₁ xi) squared. "
        "Slope β̂₁ = sum (xi minus x-bar)(yi minus ȳ) / sum (xi minus x̄) squared "
        "= Cov̂(X, Y) / Var̂(X); intercept β̂₀ = ȳ minus β̂₁ x̄. Fit implements OLS "
        "but is not the criterion; Corr(X, Y) is not the OLS slope."
    ): (
        "Choose $\\beta_{0}$, $\\beta_{1}$ to minimise "
        "$\\sum (y_{i} - \\beta_{0} - \\beta_{1} x_{i})^{2}$. "
        "Slope $\\hat{\\beta}_{1} = "
        "\\frac{\\sum (x_{i} - \\bar{x})(y_{i} - \\bar{y})}"
        "{\\sum (x_{i} - \\bar{x})^{2}} = "
        "\\frac{\\widehat{\\operatorname{Cov}}(X, Y)}"
        "{\\widehat{\\operatorname{Var}}(X)}$; "
        "intercept $\\hat{\\beta}_{0} = \\bar{y} - \\hat{\\beta}_{1} \\bar{x}$. "
        "Fit implements OLS but is not the criterion; "
        "$\\operatorname{Corr}(X, Y)$ is not the OLS slope."
    ),
    (
        "Minimise sum |yi minus β₀ minus β₁ xi|; the resulting slope is "
        "Cov̂(X, Y) / Var̂(X) for simple linear regression."
    ): (
        "Minimise $\\sum |y_{i} - \\beta_{0} - \\beta_{1} x_{i}|$; "
        "the resulting slope is "
        "$\\frac{\\widehat{\\operatorname{Cov}}(X, Y)}"
        "{\\widehat{\\operatorname{Var}}(X)}$ "
        "for simple linear regression."
    ),
    "y, μ̂": "$y$, $\\hat{\\mu}$",
    "x₁…x₅": "$x_{1},\\ldots,x_{5}$",
    "Φ(1)": "$\\Phi(1)$",
    "V(μ)": "$V(\\mu)$",
    "≈ 0.841": "$\\approx 0.841$",
    "y = β₀ + β₁x": "$y = \\beta_{0} + \\beta_{1} x$",
    "μ": "$\\mu$",
    "σ": "$\\sigma$",
    "n": "$n$",
    "Minimise sum squared residuals; β̂₁ = Cov̂/Var̂; refuse Fit-as-criterion and Corr-as-slope.": (
        "Minimise sum squared residuals; "
        "$\\hat{\\beta}_{1} = "
        "\\frac{\\widehat{\\operatorname{Cov}}}{\\widehat{\\operatorname{Var}}}$; "
        "refuse Fit-as-criterion and Corr-as-slope."
    ),
    "Compute S_xx = Σ(xᵢ − x̄)² and S_xy = Σ(xᵢ − x̄)(yᵢ − ȳ).": (
        "Compute $S_{xx} = \\sum (x_{i} - \\bar{x})^{2}$ and "
        "$S_{xy} = \\sum (x_{i} - \\bar{x})(y_{i} - \\bar{y})$."
    ),
    "β̂₁ = S_xy/S_xx, β̂₀ = ȳ − β̂₁ x̄, residual = y − (β̂₀ + β̂₁x).": (
        "$\\hat{\\beta}_{1} = \\frac{S_{xy}}{S_{xx}}$, "
        "$\\hat{\\beta}_{0} = \\bar{y} - \\hat{\\beta}_{1} \\bar{x}$, "
        "residual $= y - (\\hat{\\beta}_{0} + \\hat{\\beta}_{1} x)$."
    ),
    "Least squares minimises Σ residual²; the closed forms give the unique minimisers for simple linear regression.": (
        "Least squares minimises $\\sum \\mathrm{residual}^{2}$; "
        "the closed forms give the unique minimisers for simple linear regression."
    ),
    "Using S_xy/S_yy for the slope, or reporting the residual as ŷ − y instead of the convention e = y − ŷ.": (
        "Using $\\frac{S_{xy}}{S_{yy}}$ for the slope, or reporting the residual as "
        "$\\hat{y} - y$ instead of the convention $e = y - \\hat{y}$."
    ),
    "Pearson: standardised (y-μ̂)/sqrt(Var); deviance: signed deviance contribution.": (
        "Pearson: standardised $\\frac{y-\\hat{\\mu}}{\\sqrt{\\operatorname{Var}}}$; "
        "deviance: signed deviance contribution."
    ),
    (
        "Pearson residual uses observed minus fitted scaled by the variance structure: "
        "(y minus μ̂) over sqrt(Var̂(Y)). Deviance residual comes from the signed "
        "contribution of observation i to deviance. Both help check fit, outliers, and patterns."
    ): (
        "Pearson residual uses observed minus fitted scaled by the variance structure: "
        "$(y - \\hat{\\mu})$ over "
        "$\\sqrt{\\widehat{\\operatorname{Var}}(Y)}$. "
        "Deviance residual comes from the signed contribution of observation i to deviance. "
        "Both help check fit, outliers, and patterns."
    ),
    (
        "Pearson residual: (y minus μ̂) over sqrt(Var̂(Y)), a standardised discrepancy. "
        "Deviance residual: the signed contribution of observation i to the deviance. "
        "Both help check fit, outliers, and patterns. An LRT is a formal acceptability "
        "or model-comparison test, different from defining and using residual diagnostics."
    ): (
        "Pearson residual: $(y - \\hat{\\mu})$ over "
        "$\\sqrt{\\widehat{\\operatorname{Var}}(Y)}$, a standardised discrepancy. "
        "Deviance residual: the signed contribution of observation i to the deviance. "
        "Both help check fit, outliers, and patterns. An LRT is a formal acceptability "
        "or model-comparison test, different from defining and using residual diagnostics."
    ),
    (
        "One policy has observed claim count y = 9 and fitted Poisson mean μ̂ = 4. "
        "Compute the Pearson residual r_P = (y − μ̂) / √V(μ̂) with V(μ) = μ. "
        "Then compute the Poisson deviance contribution d = 2[y ln(y/μ̂) − (y − μ̂)] "
        "and the deviance residual r_D = sign(y − μ̂) √d."
    ): (
        "One policy has observed claim count $y = 9$ and fitted Poisson mean "
        "$\\hat{\\mu} = 4$. Compute the Pearson residual "
        "$r_{P} = \\frac{y - \\hat{\\mu}}{\\sqrt{V(\\hat{\\mu})}}$ with $V(\\mu) = \\mu$. "
        "Then compute the Poisson deviance contribution "
        "$d = 2[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})]$ "
        "and the deviance residual "
        "$r_{D} = \\operatorname{sign}(y - \\hat{\\mu})\\sqrt{d}$."
    ),
    "CMP closed. Compute r_P = (y − μ̂)/√μ̂ first, then d and r_D.": (
        "CMP closed. Compute $r_{P} = \\frac{y - \\hat{\\mu}}{\\sqrt{\\hat{\\mu}}}$ "
        "first, then $d$ and $r_{D}$."
    ),
    "Standardise the raw residual by √V(μ̂).": (
        "Standardise the raw residual by $\\sqrt{V(\\hat{\\mu})}$."
    ),
    "Pearson residuals are (y − μ̂)/√Var(μ̂). For Poisson, Var(μ̂) = μ̂.": (
        "Pearson residuals are $\\frac{y - \\hat{\\mu}}{\\sqrt{\\operatorname{Var}(\\hat{\\mu})}}$. "
        "For Poisson, $\\operatorname{Var}(\\hat{\\mu}) = \\hat{\\mu}$."
    ),
    "Compute d = 2[y ln(y/μ̂) − (y − μ̂)].": (
        "Compute $d = 2[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})]$."
    ),
    "r_D = sign(y − μ̂) √d.": (
        "$r_{D} = \\operatorname{sign}(y - \\hat{\\mu})\\sqrt{d}$."
    ),
    "The sign matches (y − μ̂). Large |r_P| or |r_D| flags observations for diagnostic review.": (
        "The sign matches $(y - \\hat{\\mu})$. Large $|r_{P}|$ or $|r_{D}|$ "
        "flags observations for diagnostic review."
    ),
    "Using √Var = √y instead of √μ̂ in the Pearson residual, or dropping the sign and reporting √d as unsigned when y < μ̂.": (
        "Using $\\sqrt{\\operatorname{Var}} = \\sqrt{y}$ instead of $\\sqrt{\\hat{\\mu}}$ "
        "in the Pearson residual, or dropping the sign and reporting $\\sqrt{d}$ as "
        "unsigned when $y < \\hat{\\mu}$."
    ),
    (
        "One commercial policy has observed claim count y = 3 and fitted Poisson mean μ̂ = 6. "
        "Compute the Pearson residual r_P = (y − μ̂) / √V(μ̂) with V(μ) = μ. "
        "Then compute the Poisson deviance contribution d = 2[y ln(y/μ̂) − (y − μ̂)] "
        "and the deviance residual r_D = sign(y − μ̂) √d."
    ): (
        "One commercial policy has observed claim count $y = 3$ and fitted Poisson mean "
        "$\\hat{\\mu} = 6$. Compute the Pearson residual "
        "$r_{P} = \\frac{y - \\hat{\\mu}}{\\sqrt{V(\\hat{\\mu})}}$ with $V(\\mu) = \\mu$. "
        "Then compute the Poisson deviance contribution "
        "$d = 2[y \\ln(y/\\hat{\\mu}) - (y - \\hat{\\mu})]$ "
        "and the deviance residual "
        "$r_{D} = \\operatorname{sign}(y - \\hat{\\mu})\\sqrt{d}$."
    ),
    "Compute (y − μ̂)/√μ̂.": (
        "Compute $\\frac{y - \\hat{\\mu}}{\\sqrt{\\hat{\\mu}}}$."
    ),
    "The deviance contribution is always non-negative; the residual takes the sign of y − μ̂.": (
        "The deviance contribution is always non-negative; the residual takes the sign of "
        "$y - \\hat{\\mu}$."
    ),
    "Apply sign(y − μ̂) √d.": (
        "Apply $\\operatorname{sign}(y - \\hat{\\mu})\\sqrt{d}$."
    ),
    "Dropping the sign when forming the deviance residual, or using √V(μ) = μ instead of √μ for Poisson.": (
        "Dropping the sign when forming the deviance residual, or using "
        "$\\sqrt{V(\\mu)} = \\mu$ instead of $\\sqrt{\\mu}$ for Poisson."
    ),
    "Normal sample · unknown σ → t=(X̄−μ)/(S/√n) → t_{n−1} → refuse z-with-S and F swallow.": (
        "Normal sample · unknown $\\sigma$ → "
        "$t=(\\bar{X}-\\mu)/(S/\\sqrt{n})$ → $t_{n-1}$ → refuse z-with-S and F swallow."
    ),
    "T=(X̄-μ)/S has t_n because dividing by √n is unnecessary.": (
        "$T=(\\bar{X}-\\mu)/S$ has $t_{n}$ because dividing by $\\sqrt{n}$ is unnecessary."
    ),
    "S₁²/S₂²~t_{n-1} because t is the standard law for variance ratios.": (
        "$S_{1}^{2}/S_{2}^{2} \\sim t_{n-1}$ because $t$ is the standard law for variance ratios."
    ),
    (
        "A random sample of size n = 16 from a Normal population yields X̄ = 105 and "
        "sample standard deviation S = 8. Under H₀: μ = 100, compute the t-statistic "
        "and state its null degrees of freedom. Explain why replacing S by the unknown "
        "σ in a z formula is not available here."
    ): (
        "A random sample of size $n = 16$ from a Normal population yields "
        "$\\bar{X} = 105$ and sample standard deviation $S = 8$. Under "
        "$H_{0}\\colon \\mu = 100$, compute the t-statistic and state its null "
        "degrees of freedom. Explain why replacing $S$ by the unknown $\\sigma$ "
        "in a $z$ formula is not available here."
    ),
    "CMP closed. Form t = (X̄ − μ₀)/(S/√n) and name df = n − 1.": (
        "CMP closed. Form $t = (\\bar{X} - \\mu_{0})/(S/\\sqrt{n})$ and name "
        "$\\mathrm{df} = n - 1$."
    ),
    "Write L(λ) = λⁿ exp(−λ Σxᵢ) and ℓ(λ) = n ln λ − λ Σxᵢ.": (
        "Write $L(\\lambda) = \\lambda^{n} \\exp(-\\lambda \\sum x_{i})$ and "
        "$\\ell(\\lambda) = n \\ln \\lambda - \\lambda \\sum x_{i}$."
    ),
    "d²ℓ/dλ² = −n/λ² < 0 for λ > 0, so the critical point is a maximum.": (
        "$\\frac{d^{2}\\ell}{d\\lambda^{2}} = -\\frac{n}{\\lambda^{2}} < 0$ for "
        "$\\lambda > 0$, so the critical point is a maximum."
    ),
    "A binomial CI for p is enough; the Poisson mean uses the identical formula after renaming p as λ, including the p(1−p) variance.": (
        "A binomial CI for $p$ is enough; the Poisson mean uses the identical formula "
        "after renaming $p$ as $\\lambda$, including the $p(1-p)$ variance."
    ),
    (
        "Bernoulli variance is p(1−p)/n; Poisson mean variance is λ/n "
        "(per observation in the usual sample-mean form). Swapping those variance "
        "functions, or dropping Poisson entirely, is wrong."
    ): (
        "Bernoulli variance is $\\frac{p(1-p)}{n}$; Poisson mean variance is "
        "$\\frac{\\lambda}{n}$ (per observation in the usual sample-mean form). "
        "Swapping those variance functions, or dropping Poisson entirely, is wrong."
    ),
    "p̂ ± z√(p̂(1−p̂)/n) and λ̂ ± z√(λ̂/n); both required.": (
        "$\\hat{p} \\pm z\\sqrt{\\hat{p}(1-\\hat{p})/n}$ and "
        "$\\hat{\\lambda} \\pm z\\sqrt{\\hat{\\lambda}/n}$; both required."
    ),
    (
        "Binomial: p̂ ± z_{1−α/2} √(p̂(1−p̂)/n). Poisson: λ̂ ± z_{1−α/2} √(λ̂/n) "
        "(or an equivalent total-count form with matching variance). Both are required; "
        "one does not replace the other."
    ): (
        "Binomial: $\\hat{p} \\pm z_{1-\\alpha/2} \\sqrt{\\hat{p}(1-\\hat{p})/n}$. "
        "Poisson: $\\hat{\\lambda} \\pm z_{1-\\alpha/2} \\sqrt{\\hat{\\lambda}/n}$ "
        "(or an equivalent total-count form with matching variance). Both are required; "
        "one does not replace the other."
    ),
    (
        "Binomial: p̂ ± z_{1−α/2} √(p̂(1−p̂)/n). The Poisson interval is the same "
        "expression with λ̂ written in place of p̂ and with variance p̂(1−p̂)/n kept unchanged."
    ): (
        "Binomial: $\\hat{p} \\pm z_{1-\\alpha/2} \\sqrt{\\hat{p}(1-\\hat{p})/n}$. "
        "The Poisson interval is the same expression with $\\hat{\\lambda}$ written in "
        "place of $\\hat{p}$ and with variance $\\hat{p}(1-\\hat{p})/n$ kept unchanged."
    ),
    "Binomial: p̂ ± z_{1−α/2} √(p̂/n). Poisson: λ̂ ± z_{1−α/2} √(λ̂(1−λ̂)/n).": (
        "Binomial: $\\hat{p} \\pm z_{1-\\alpha/2} \\sqrt{\\hat{p}/n}$. "
        "Poisson: $\\hat{\\lambda} \\pm z_{1-\\alpha/2} "
        "\\sqrt{\\hat{\\lambda}(1-\\hat{\\lambda})/n}$."
    ),
    (
        "Only the binomial form is required; Poisson means are handled by transforming "
        "to a Normal mean interval for x̄ with variance s²/n from continuous data."
    ): (
        "Only the binomial form is required; Poisson means are handled by transforming "
        "to a Normal mean interval for $\\bar{x}$ with variance $\\frac{s^{2}}{n}$ "
        "from continuous data."
    ),
    "CMP closed. Write p̂ ± 1.96 √[p̂(1−p̂)/n] before substituting.": (
        "CMP closed. Write $\\hat{p} \\pm 1.96 \\sqrt{\\hat{p}(1-\\hat{p})/n}$ "
        "before substituting."
    ),
    "Compute √[0.22 × 0.78 / 100].": (
        "Compute $\\sqrt{0.22 \\times 0.78 / 100}$."
    ),
    "Binomial/Bernoulli variance p(1−p)/n is plugged in at p̂.": (
        "Binomial/Bernoulli variance $\\frac{p(1-p)}{n}$ is plugged in at $\\hat{p}$."
    ),
    (
        "Using √[p̂/n] = √0.0022 (Poisson-style) instead of √[p̂(1−p̂)/n], "
        "or forgetting the (1−p̂) factor."
    ): (
        "Using $\\sqrt{\\hat{p}/n} = \\sqrt{0.0022}$ (Poisson-style) instead of "
        "$\\sqrt{\\hat{p}(1-\\hat{p})/n}$, or forgetting the $(1-\\hat{p})$ factor."
    ),
    (
        "Closed-book. Pet-insurance claim severities are iid with mean μ = 180 and "
        "standard deviation σ = 60. A sample of n = 36 claims is drawn. Using the CLT "
        "and Φ(1) ≈ 0.841, approximate P(X̄ < 170). Enter the probability as a decimal."
    ): (
        "Closed-book. Pet-insurance claim severities are iid with mean $\\mu = 180$ and "
        "standard deviation $\\sigma = 60$. A sample of $n = 36$ claims is drawn. Using "
        "the CLT and $\\Phi(1) \\approx 0.841$, approximate $P(\\bar{X} < 170)$. "
        "Enter the probability as a decimal."
    ),
    "Use Φ(-1) = 1 - Φ(1) with Φ(1) ≈ 0.841.": (
        "Use $\\Phi(-1) = 1 - \\Phi(1)$ with $\\Phi(1) \\approx 0.841$."
    ),
    (
        "sd(X̄) = σ/√n = 60/√36 = 10, so z = (170 - 180)/10 = -1 and "
        "P(X̄ < 170) ≈ Φ(-1) = 1 - Φ(1) ≈ 1 - 0.841 = 0.159."
    ): (
        "$\\operatorname{sd}(\\bar{X}) = \\frac{\\sigma}{\\sqrt{n}} = "
        "\\frac{60}{\\sqrt{36}} = 10$, so "
        "$z = \\frac{170 - 180}{10} = -1$ and "
        "$P(\\bar{X} < 170) \\approx \\Phi(-1) = 1 - \\Phi(1) \\approx 1 - 0.841 = 0.159$."
    ),
    (
        "Using σ = 60 instead of σ/√n = 10 so that z = -1/6, or reporting Φ(1) ≈ 0.841 "
        "as the lower-tail probability itself."
    ): (
        "Using $\\sigma = 60$ instead of $\\frac{\\sigma}{\\sqrt{n}} = 10$ so that "
        "$z = -\\frac{1}{6}$, or reporting $\\Phi(1) \\approx 0.841$ as the lower-tail "
        "probability itself."
    ),
    (
        "Pet-insurance claim severities are iid with mean μ = 180 and standard "
        "deviation σ = 60. A sample of n = 36 claims is drawn. Using the CLT, "
        "approximate P(X̄ < 170). Use Φ(1) ≈ 0.841."
    ): (
        "Pet-insurance claim severities are iid with mean $\\mu = 180$ and standard "
        "deviation $\\sigma = 60$. A sample of $n = 36$ claims is drawn. Using the CLT, "
        "approximate $P(\\bar{X} < 170)$. Use $\\Phi(1) \\approx 0.841$."
    ),
    "The probability is the lower Normal tail at z = −1, equal to 1 − Φ(1).": (
        "The probability is the lower Normal tail at $z = -1$, equal to $1 - \\Phi(1)$."
    ),
    (
        "Using X̄ ≈ Normal(180, 60) and computing z = (170 − 180)/60 = −1/6, "
        "or reading Φ(1) ≈ 0.841 as the lower-tail probability itself."
    ): (
        "Using $\\bar{X} \\approx \\operatorname{Normal}(180, 60)$ and computing "
        "$z = \\frac{170 - 180}{60} = -\\frac{1}{6}$, or reading "
        "$\\Phi(1) \\approx 0.841$ as the lower-tail probability itself."
    ),
    (
        "Closed-book. Two estimators of θ: θ̂₁ is unbiased with Var=2/n; θ̂₂ has "
        "Bias=0.5/√n and Var=0.5/n. Which statement is correct?"
    ): (
        "Closed-book. Two estimators of $\\theta$: $\\hat{\\theta}_{1}$ is unbiased with "
        "$\\operatorname{Var}=\\frac{2}{n}$; $\\hat{\\theta}_{2}$ has "
        "$\\operatorname{Bias}=\\frac{0.5}{\\sqrt{n}}$ and "
        "$\\operatorname{Var}=\\frac{0.5}{n}$. Which statement is correct?"
    ),
    (
        "MSE₁=2/n. Bias² for θ̂₂ is (0.5/√n)²=0.25/n, so MSE₂=0.75/n < 2/n. Prefer θ̂₂. "
        "Squaring 0.5/√n incorrectly as 0.25/√n is algebraically wrong. Unbiasedness "
        "does not override a worse MSE."
    ): (
        "$\\mathrm{MSE}_{1}=\\frac{2}{n}$. $\\mathrm{Bias}^{2}$ for $\\hat{\\theta}_{2}$ "
        "is $(\\frac{0.5}{\\sqrt{n}})^{2}=\\frac{0.25}{n}$, so "
        "$\\mathrm{MSE}_{2}=\\frac{0.75}{n} < \\frac{2}{n}$. Prefer $\\hat{\\theta}_{2}$. "
        "Squaring $\\frac{0.5}{\\sqrt{n}}$ incorrectly as $\\frac{0.25}{\\sqrt{n}}$ is "
        "algebraically wrong. Unbiasedness does not override a worse MSE."
    ),
    "Dropping the bias² term, preferring unbiasedness over MSE, or mishandling (0.5/√n)².": (
        "Dropping the $\\mathrm{bias}^{2}$ term, preferring unbiasedness over MSE, "
        "or mishandling $(\\frac{0.5}{\\sqrt{n}})^{2}$."
    ),
    "MSE(T₁) = Var(T₁) + [Bias(T₁)]² collapses to variance when Bias = 0.": (
        "$\\operatorname{MSE}(T_{1}) = \\operatorname{Var}(T_{1}) + "
        "[\\operatorname{Bias}(T_{1})]^{2}$ collapses to variance when Bias $= 0$."
    ),
}


def _is_board(field_path: str) -> bool:
    return bool(_BOARD_PATH.search(field_path))


def convert_string(text: str, field_path: str = "") -> str:
    """Convert one inventoried string. Preserve surrounding English prose."""
    if text in EXPLICIT:
        return EXPLICIT[text]

    if _is_board(field_path):
        # given.value that is a bare numeral stays a numeral but wrap if it
        # still contains math after latexify; plain integers wrap as math
        # only when the original was already mathish (caller guarantees that).
        if re.fullmatch(r"\d+(?:\.\d+)?", text.strip()):
            return _wrap(text.strip())
        converted = latexify(text)
        if ";" in text and "ln(" not in text[:20]:
            parts = [p.strip() for p in converted.split(";")]
            return "; ".join(_wrap(p) for p in parts if p)
        return _wrap(converted)

    # Mixed prose: convert math islands token-by-token via a covering pass.
    return _convert_mixed(text)


def _convert_mixed(text: str) -> str:
    """Wrap mathematical objects inside prose, leaving English words intact."""
    if text in EXPLICIT:
        return EXPLICIT[text]

    # Protect explicit overrides already wrapped.
    s = text

    # Build candidate spans from original text using conservative patterns.
    patterns = [
        r"Cov̂\s*\(\s*X\s*,\s*Y\s*\)",
        r"Var̂\s*\(\s*[XY]\s*\)",
        r"Corr\s*\(\s*X\s*,\s*Y\s*\)",
        r"E\[[^\]]{1,40}\]",
        r"Var\s*\([^)]{1,40}\)",
        r"Cov\s*\([^)]{1,40}\)",
        r"MSE\s*\([^)]{1,20}\)",
        r"Bias\s*\([^)]{1,20}\)",
        r"sd\s*\([^)]{1,20}\)",
        r"P\s*\([^)]{1,40}\)",
        r"Φ\s*\([^)]{1,20}\)",
        r"Normal\s*\([^)]{1,60}\)",
        r"N\s*\([^)]{1,40}\)",
        r"V\s*\([^)]{1,20}\)",
        r"ℓ\([^)]{1,20}\)",
        r"e\^\{[^}]+\}",
        r"σ/√n",
        r"σ²/n",
        r"S/√n",
        r"S_xy/S_xx",
        r"S_xy/S_yy",
        r"\(n\s*[−-]\s*1\)S²/σ²",
        r"\(n-1\)S²/σ²",
        r"t_\{n-1\}",
        r"t_\{15\}",
        r"χ²_\{n−1\}",
        r"χ²_\{n-1\}",
        r"χ²_\{n−1\}",
        r"χ²_15",
        r"χ²_n",
        r"z_\{1−α/2\}",
        r"z_\{1-α/2\}",
        r"β̂₀",
        r"β̂₁",
        r"β̂",
        r"β₀",
        r"β₁",
        r"λ̂_MLE",
        r"λ̂",
        r"μ̂_MoM",
        r"μ̂_MLE",
        r"μ̂",
        r"θ̂₁",
        r"θ̂₂",
        r"θ̂",
        r"p̂",
        r"λ̂",
        r"SÊ",
        r"X̄",
        r"x̄",
        r"ȳ",
        r"ŷ",
        r"S_xx",
        r"S_xy",
        r"S_yy",
        r"S²",
        r"r_P",
        r"r_D",
        r"T₁",
        r"T₂",
        r"MSE₁",
        r"MSE₂",
        r"√n",
        r"√d",
        r"√μ̂",
        r"√V\([^)]+\)",
        r"√Var[̂]?\([^)]+\)",
        r"σ²",
        r"μ",
        r"σ",
        r"λ",
        r"χ²",
        r"Φ",
        r"ε",
        r"ℓ",
        r"Σ",
        r"x₁",
        r"xᵢ",
        r"yᵢ",
        r"n-1",
        r"0\.5/√n",
        r"0\.25/√n",
        r"0\.5/n",
        r"0\.25/n",
        r"0\.75/n",
        r"2/n",
        r"4/10",
        r"\(0\.5/√n\)²",
        r"dℓ/dλ",
        r"d²ℓ/dλ²",
        r"Y = β₀ \+ β₁ x \+ ε",
        r"y = β₀ \+ β₁x",
        r"ŷ = 0\.9 \+ 1\.6x",
        r"ŷ = 0\.5 \+ 1\.4x",
    ]

    # Longer patterns first.
    patterns.sort(key=len, reverse=True)
    compiled = [(re.compile(p), p) for p in patterns]

    used = [False] * len(s)
    spans: list[tuple[int, int, str]] = []
    for cre, _raw in compiled:
        for match in cre.finditer(s):
            a, b = match.span()
            if any(used[a:b]):
                continue
            if a < b:
                for i in range(a, b):
                    used[i] = True
                spans.append((a, b, match.group(0)))
    spans.sort(key=lambda t: t[0])

    if not spans:
        # Fallback: latexify whole string if it is essentially a formula.
        if inventory.is_mathish(s) and len(s) < 80 and " " not in s.strip():
            return _wrap(latexify(s))
        return s

    out: list[str] = []
    cursor = 0
    for a, b, original in spans:
        out.append(s[cursor:a])
        out.append(_wrap(latexify(original)))
        cursor = b
    out.append(s[cursor:])
    merged = _merge_adjacent_math("".join(out))
    return merged


def wave1_items(ledger: dict[str, Any]) -> list[dict[str, Any]]:
    by_file = {row["package_file"]: row for row in ledger["packages"]}
    items: list[dict[str, Any]] = []
    for fname in WAVE1_FILES:
        row = by_file[fname]
        for item in row["items"]:
            if item["category"] != "needs_migration":
                continue
            items.append(item)
    return items


def migrate_packages(*, apply: bool) -> dict[str, Any]:
    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    items = wave1_items(ledger)
    confident = [i for i in items if not i["needs_manual_review"]]
    skipped = [i for i in items if i["needs_manual_review"]]

    packages: dict[str, dict[str, Any]] = {}
    for fname in WAVE1_FILES:
        packages[fname] = json.loads((CATALOGUE / fname).read_text(encoding="utf-8"))

    converted: list[dict[str, Any]] = []
    still_mathish: list[dict[str, Any]] = []
    for item in confident:
        original = item["text"]
        new = convert_string(original, item["field_path"])
        live = get_path(packages[item["package_file"]], item["field_path"])
        if live != original:
            raise RuntimeError(
                f"Live text mismatch {item['package_file']} "
                f"{item['field_path']}: ledger != package"
            )
        set_path(packages[item["package_file"]], item["field_path"], new)
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

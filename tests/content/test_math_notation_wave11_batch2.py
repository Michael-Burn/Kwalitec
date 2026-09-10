"""Wave 11 batch 2 mathematical notation: KaTeX, exclusions, scoring, ledger."""

# Representative samples use verbatim package text; line length is expected.
# ruff: noqa: E501

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import pytest

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.scoreable_practice import score_practice_response

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402
import math_notation_wave1 as wave1  # noqa: E402
import math_notation_wave11 as wave11  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave11_batch2_scoring_snapshot.json"
)

_KNOWN_COMMANDS = frozenset(
    {
        "frac",
        "sqrt",
        "bar",
        "hat",
        "widehat",
        "operatorname",
        "mathrm",
        "mu",
        "sigma",
        "lambda",
        "beta",
        "theta",
        "chi",
        "Phi",
        "phi",
        "varphi",
        "alpha",
        "varepsilon",
        "ell",
        "eta",
        "nu",
        "Delta",
        "pi",
        "sum",
        "ln",
        "log",
        "exp",
        "sim",
        "approx",
        "times",
        "leq",
        "geq",
        "ge",
        "neq",
        "Rightarrow",
        "rightarrow",
        "xrightarrow",
        "leftrightarrow",
        "ldots",
        "colon",
        "left",
        "right",
        "bigl",
        "bigr",
        "big",
        "Big",
        "quad",
        "qquad",
        "text",
        "in",
        "to",
        "cdot",
        "pm",
        "propto",
        "infty",
        "mid",
        "subset",
        "lfloor",
        "rfloor",
        "lceil",
        "rceil",
        "rho",
        "delta",
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Locked Wave 11 batch 2 migrations (7 full + 34 partial).
_WAVE11_B2_MIGRATIONS = (
    (
        "3.2.5-ci-binomial-poisson-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $0.22 \pm 1.96 \times 0.041425$.",
    ),
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $600 \pm 1.96 \times 250.777$.",
    ),
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.common_pitfall",
        r"Building a Wald interval from the bootstrap SE instead of reading percentile order statistics, or taking the 2nd and 9th values without applying the $\alpha(B+1)$ index rule given in the problem.",
    ),
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.steps[0].attempt_cue",
        r"Evaluate $\lfloor\alpha(B+1)\rfloor$ and map to an order statistic.",
    ),
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.steps[1].attempt_cue",
        r"Evaluate $\lceil(1-\alpha)(B+1)\rceil$ and clamp to B if needed.",
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.common_pitfall",
        r"Reporting only the one-sided tail 0.0179 as the p-value for a two-sided alternative, or comparing $z$ to $\alpha$ directly ($2.1$ vs $0.05$).",
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.steps[2].attempt_cue",
        r"Compare $p$ with $\alpha$.",
    ),
    (
        "3.3.2-basic-tests-cs1012.json",
        "worked_example.steps[0].explanation",
        r"One-sample z-test standardises the sample mean under $H_{0}$.",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $|\mathrm{mean}(A) - \mathrm{mean}(B)|$.",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.steps[1].explanation",
        r"Under $H_{0}$ every assignment of three labels to A is equally likely; the p-value is the proportion at least as extreme as observed.",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.given[2].note",
        r"$5 - 1$ categories",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[1].label",
        r"Sum to $\chi^{2}$",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.steps[1].label",
        r"Pearson $\chi^{2}$",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.title",
        r"Chi-square test of independence in a $2 \times 2$ fraud table",
    ),
    (
        "4.1.4-software-fit-cs1013.json",
        "worked_example.steps[1].label",
        r"Approximate 95% CI for $\beta_{1}$",
    ),
    (
        "4.1.4-software-fit-cs1013.json",
        "worked_example.steps[2].attempt_cue",
        r"Form $\hat{y} \pm 1.96 \times \mathrm{SE}$ for each SE, and compare widths.",
    ),
    (
        "4.1.4-software-inference-cs1003.json",
        "worked_example.steps[1].label",
        r"Approximate 95% CI for $\beta_{1}$",
    ),
    (
        "4.1.4-software-inference-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        r"Form $\hat{y} \pm 1.96 \times \mathrm{SE}$ for each SE, and compare widths.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model A",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model B",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].explanation",
        r"Prefer the larger $R^{2}_{\mathrm{adj}}$. Here Model B wins after the penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].label",
        r"Select by $R^{2}_{\mathrm{adj}}$",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model A",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model B",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].explanation",
        r"Prefer the larger $R^{2}_{\mathrm{adj}}$. Here Model A wins despite smaller raw $R^{2}$.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].label",
        r"Select by $R^{2}_{\mathrm{adj}}$",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Rewrite the pmf as $\exp\{y \operatorname{logit}(p) + \ln(1 - p)\}$ before naming θ.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.steps[0].explanation",
        r"Members of the exponential family admit a linear natural parameter multiplying y. For Poisson, that term is $y \ln \lambda$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "knowledge_checks[0].explanation",
        r"Family structure specifies mean, variance, $V(\mu)$, and scale. The link maps $\mu$ to $\eta$ and is a separate object from the response variance structure.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "knowledge_checks[1].explanation",
        r"Poisson has mean-variance equality; Normal has constant variance with scale $\sigma^{2}$. Link choice does not replace these family facts.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"State mean, variance, and $V(\mu)$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $np$ and $np(1 - p)$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.title",
        r"Mean, variance, $V(\mu)$, and scale for three families",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "knowledge_checks[0].explanation",
        r"Family structure specifies mean, variance, $V(\mu)$, and scale. The link maps $\mu$ to $\eta$ and is a separate object from the response variance structure.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "knowledge_checks[1].explanation",
        r"Poisson has mean-variance equality; Normal has constant variance with scale $\sigma^{2}$. Link choice does not replace these family facts.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.title",
        r"Mean, variance, $V(\mu)$, and scale for three families",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.title",
        r"Logit and log canonical links with numeric $\eta$",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "knowledge_checks[0].explanation",
        r"Link maps $\mu$ to $\eta$; canonical is family-specific natural parameter link. Software default needs a warrant, and link is not eta itself.",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.steps[0].explanation",
        r"The link maps the mean $\mu$ to the linear predictor $\eta$. For binomial, the canonical link is the logit.",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.title",
        r"Logit and log canonical links with numeric $\eta$",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Plug indicator patterns into $\eta$ before exponentiating; check when $C \times H$ is nonzero.",
    ),
)

_WAVE11_B2_EXCLUSIONS = (
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.steps[1].explanation",
        "Symmetric upper quantile for the same α.",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "mission.expected_benefit",
        "You will be able to outline a permutation test from exchangeability under H₀ to a reference distribution.",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.given[1].note",
        "common expected count under H₀",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "mission.tutor_intent",
        "Today I will force the candidate to write η forms for simple and multiple LM and refuse treating 'multiple' as automatic excellence.",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "worked_example.steps[1].explanation",
        "The simple model ignores x₂ even if that covariate is available.",
    ),
    (
        "4.1.2-simple-multiple-cs1013.json",
        "worked_example.steps[1].explanation",
        "The simple model ignores x₂ even if that covariate is available.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].explanation",
        "Adjusted R² penalises extra parameters so that raw R² inflation from adding variables is not automatic preference.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].explanation",
        "The larger model starts with higher raw R² but faces a heavier penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.title",
        "Choose explanatory set by adjusted R² (commercial property)",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "reading_guidance.misconception_watch[0]",
        "Watch for equating 'best R²' with automatically correct selection without CMP caveat.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].explanation",
        "Adjusted R² penalises extra parameters so that raw R² inflation from adding variables is not automatic preference.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].explanation",
        "The larger model starts with higher raw R² but faces a heavier penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.title",
        "Choose explanatory set by adjusted R²",
    ),
    (
        "4.2.10-fit-interpret-cs1014.json",
        "worked_example.steps[0].explanation",
        "Under a log link, a coefficient is a log mean ratio. Exponentiating yields the multiplicative effect on μ.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "mission.mission_purpose",
        "Today's Mission exists to explain the link and canonical link for exponential-family responses (completing EA-006 structure absorb into Campaign membership) so Family → η → link is Campaign-certified, not Isolated Golden Day.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "mission.tutor_intent",
        "Today I will force link vs η discrimination and one canonical pairing with mean-range warrant. Refuse software-default links.",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "mission.prior_bridge",
        "Yesterday closed Family → η → link (4.2.3). Today builds predictor structure.",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "mission.why_now",
        "4.2.4 is contiguous after structure before η form detail (4.2.5).",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "reading_guidance.out_of_scope_today[0]",
        "η form primary (4.2.5)",
    ),
)

# Partial migrations: surrounding prose that must remain untouched.
_WAVE11_B2_PARTIAL_PROSE = (
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.common_pitfall",
        (
            "Building a Wald interval from the bootstrap SE instead of reading percentile order statistics, or taking the 2nd and 9th values without applying the ",
            " index rule given in the problem.",
        ),
        (r"\alpha(B+1)",),
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.common_pitfall",
        (
            "Reporting only the one-sided tail 0.0179 as the p-value for a two-sided alternative, or comparing ",
            " to ",
            " directly (",
            " vs ",
            ").",
        ),
        (r"z", r"\alpha", r"2.1", r"0.05"),
    ),
    (
        "3.3.2-basic-tests-cs1012.json",
        "worked_example.steps[0].explanation",
        ("One-sample z-test standardises the sample mean under ",),
        (r"H_{0}",),
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.steps[1].explanation",
        (
            "Under ",
            " every assignment of three labels to A is equally likely; the p-value is the proportion at least as extreme as observed.",
        ),
        (r"H_{0}",),
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.given[2].note",
        (" categories",),
        (r"5 - 1",),
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[1].label",
        ("Sum to ",),
        (r"\chi^{2}",),
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.steps[1].label",
        ("Pearson ",),
        (r"\chi^{2}",),
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.title",
        ("Chi-square test of independence in a ", " fraud table"),
        (r"2 \times 2",),
    ),
    (
        "4.1.4-software-fit-cs1013.json",
        "worked_example.steps[1].label",
        ("Approximate 95% CI for ",),
        (r"\beta_{1}",),
    ),
    (
        "4.1.4-software-fit-cs1013.json",
        "worked_example.steps[2].attempt_cue",
        ("Form ", " for each SE, and compare widths."),
        (r"\hat{y} \pm 1.96 \times \mathrm{SE}",),
    ),
    (
        "4.1.4-software-inference-cs1003.json",
        "worked_example.steps[1].label",
        ("Approximate 95% CI for ",),
        (r"\beta_{1}",),
    ),
    (
        "4.1.4-software-inference-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        ("Form ", " for each SE, and compare widths."),
        (r"\hat{y} \pm 1.96 \times \mathrm{SE}",),
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].label",
        (" for Model A",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].label",
        (" for Model B",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].explanation",
        ("Prefer the larger ", ". Here Model B wins after the penalty."),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].label",
        ("Select by ",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].label",
        (" for Model A",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].label",
        (" for Model B",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].explanation",
        (
            "Prefer the larger ",
            ". Here Model A wins despite smaller raw ",
            ".",
        ),
        (r"R^{2}_{\mathrm{adj}}", r"R^{2}"),
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].label",
        ("Select by ",),
        (r"R^{2}_{\mathrm{adj}}",),
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Rewrite the pmf as ",
            " before naming θ.",
        ),
        (r"\exp\{y \operatorname{logit}(p) + \ln(1 - p)\}",),
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.steps[0].explanation",
        (
            "Members of the exponential family admit a linear natural parameter multiplying y. For Poisson, that term is ",
            ".",
        ),
        (r"y \ln \lambda",),
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "knowledge_checks[0].explanation",
        (
            "Family structure specifies mean, variance, ",
            ", and scale. The link maps ",
            " to ",
            " and is a separate object from the response variance structure.",
        ),
        (r"V(\mu)", r"\mu", r"\eta"),
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "knowledge_checks[1].explanation",
        (
            "Poisson has mean-variance equality; Normal has constant variance with scale ",
            ". Link choice does not replace these family facts.",
        ),
        (r"\sigma^{2}",),
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        ("State mean, variance, and ",),
        (r"V(\mu)",),
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.title",
        ("Mean, variance, ", ", and scale for three families"),
        (r"V(\mu)",),
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "knowledge_checks[0].explanation",
        (
            "Family structure specifies mean, variance, ",
            ", and scale. The link maps ",
            " to ",
            " and is a separate object from the response variance structure.",
        ),
        (r"V(\mu)", r"\mu", r"\eta"),
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "knowledge_checks[1].explanation",
        (
            "Poisson has mean-variance equality; Normal has constant variance with scale ",
            ". Link choice does not replace these family facts.",
        ),
        (r"\sigma^{2}",),
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.title",
        ("Mean, variance, ", ", and scale for three families"),
        (r"V(\mu)",),
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.title",
        ("Logit and log canonical links with numeric ",),
        (r"\eta",),
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "knowledge_checks[0].explanation",
        (
            "Link maps ",
            " to ",
            "; canonical is family-specific natural parameter link. Software default needs a warrant, and link is not eta itself.",
        ),
        (r"\mu", r"\eta"),
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.steps[0].explanation",
        (
            "The link maps the mean ",
            " to the linear predictor ",
            ". For binomial, the canonical link is the logit.",
        ),
        (r"\mu", r"\eta"),
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.title",
        ("Logit and log canonical links with numeric ",),
        (r"\eta",),
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Plug indicator patterns into ",
            " before exponentiating; check when ",
            " is nonzero.",
        ),
        (r"\eta", r"C \times H"),
    ),
)

# Adjusted R² distinction: compute/select migrated; title/mission/definitional excluded.
_ADJUSTED_R2_MIGRATED = (
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model A",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model B",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].explanation",
        r"Prefer the larger $R^{2}_{\mathrm{adj}}$. Here Model B wins after the penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[2].label",
        r"Select by $R^{2}_{\mathrm{adj}}$",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model A",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].label",
        r"$R^{2}_{\mathrm{adj}}$ for Model B",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].explanation",
        r"Prefer the larger $R^{2}_{\mathrm{adj}}$. Here Model A wins despite smaller raw $R^{2}$.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[2].label",
        r"Select by $R^{2}_{\mathrm{adj}}$",
    ),
)

_ADJUSTED_R2_EXCLUDED = (
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].explanation",
        "Adjusted R² penalises extra parameters so that raw R² inflation from adding variables is not automatic preference.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].explanation",
        "The larger model starts with higher raw R² but faces a heavier penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.title",
        "Choose explanatory set by adjusted R² (commercial property)",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "reading_guidance.misconception_watch[0]",
        "Watch for equating 'best R²' with automatically correct selection without CMP caveat.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].explanation",
        "Adjusted R² penalises extra parameters so that raw R² inflation from adding variables is not automatic preference.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].explanation",
        "The larger model starts with higher raw R² but faces a heavier penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.title",
        "Choose explanatory set by adjusted R²",
    ),
)


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _spans(text: str) -> list[str]:
    return _MATH_SPAN.findall(text)


def _assert_valid_latex(body: str, *, where: str) -> None:
    assert body.strip(), f"empty math span at {where}"
    assert body.count("{") == body.count("}"), f"unbalanced braces at {where}: {body}"
    depth = 0
    for ch in body:
        if ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
            assert depth >= 0, f"brace underflow at {where}: {body}"
    assert depth == 0, f"unclosed brace at {where}: {body}"
    assert body.count("[") == body.count("]"), f"unbalanced brackets at {where}: {body}"
    assert not re.search(r"(?<!\\)%", body), f"bare % in math at {where}: {body}"
    for cmd in _CONTROL.findall(body):
        assert cmd in _KNOWN_COMMANDS, (
            f"unknown KaTeX command \\{cmd} at {where}: {body}"
        )


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_B2_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B2_MIGRATIONS],
)
def test_wave11_batch2_migrations_are_valid_katex(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert text.count("$") % 2 == 0
    assert _spans(text), (
        f"expected dollar-delimited math in {package_file} {field_path}"
    )
    for body in _spans(text):
        _assert_valid_latex(body, where=f"{package_file}:{field_path}")


@pytest.mark.parametrize(
    ("package_file", "field_path", "prose_parts", "math_needles"),
    _WAVE11_B2_PARTIAL_PROSE,
    ids=[f"{p}:{f}" for p, f, *_ in _WAVE11_B2_PARTIAL_PROSE],
)
def test_wave11_batch2_partial_migrations_preserve_surrounding_prose(
    package_file: str,
    field_path: str,
    prose_parts: tuple[str, ...],
    math_needles: tuple[str, ...],
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    for part in prose_parts:
        assert part in text, (
            f"missing prose {part!r} in {package_file} {field_path}: {text}"
        )
    for needle in math_needles:
        assert needle in text, (
            f"missing math {needle!r} in {package_file} {field_path}: {text}"
        )
    assert _spans(text)


def test_wave11_batch2_adjusted_r2_distinction() -> None:
    """Step-label/comparison Adjusted R² migrates; title/definitional stays prose."""
    for package_file, field_path, expected in _ADJUSTED_R2_MIGRATED:
        text = wave1.get_path(_load(package_file), field_path)
        assert text == expected
        assert r"R^{2}_{\mathrm{adj}}" in text
        assert "$" in text

    for package_file, field_path, expected in _ADJUSTED_R2_EXCLUDED:
        text = wave1.get_path(_load(package_file), field_path)
        assert text == expected
        assert "$" not in text
        assert "R²" in text


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_B2_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B2_EXCLUSIONS],
)
def test_wave11_batch2_exclusions_are_byte_identical_and_confirmed(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text
    live = inventory.build_inventory(PACKAGES)
    matches = [
        item
        for row in live["packages"]
        if row["package_file"] == package_file
        for item in row["items"]
        if item["field_path"] == field_path and item["text"] == expected
    ]
    assert len(matches) == 1
    assert matches[0]["needs_manual_review"] is False
    assert matches[0]["migration_status"] == "correctly_excluded"
    assert matches[0]["reason_code"] == "manual_review_prose_exclusion"


def test_wave11_batch2_item40_preserves_prose_theta() -> None:
    text = wave1.get_path(
        _load("4.2.1-exponential-family-cs1003.json"),
        "worked_example.attempt_before_reveal",
    )
    assert "before naming θ." in text
    assert r"\theta" not in text
    assert r"\exp\{y \operatorname{logit}(p) + \ln(1 - p)\}" in text


def test_wave11_batch2_item54_preserves_english_eta() -> None:
    text = wave1.get_path(
        _load("4.2.3-link-canonical-cs1014.json"),
        "knowledge_checks[0].explanation",
    )
    assert "link is not eta itself." in text
    assert r"\mu" in text and r"\eta" in text
    assert "eta" in text


def test_wave11_batch2_scoring_unaffected_for_touched_knowledge_checks() -> None:
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    reset_educational_package_cache()
    loader = EducationalPackageLoader(
        root=REPO_ROOT / "app/curriculum/data/educational_packages"
    )
    by_id: dict[tuple[str, str], dict] = {}
    for rec in snapshot["items"]:
        by_id[(rec["package_file"], rec["item_id"])] = rec

    seen: set[tuple[str, str]] = set()
    for fname in snapshot["packages"]:
        pack = next(
            p for p in loader.all_approved() if Path(p.source_path).name == fname
        )
        substance = substance_from_package(
            pack, curriculum_identity="CS1:wave11b2", topic_id=pack.topic_code
        )
        practice = [
            a for a in substance.activities if a.stage is EducationalStage.PRACTICE
        ]
        for act in practice:
            item = act.scoreable
            assert item is not None
            key = (fname, item.item_id)
            seen.add(key)
            expected = by_id[key]
            assert item.answer_key.correct_choice_id == expected["correct_choice_id"]
            assert list(item.answer_key.accepted) == expected["accepted_keywords"]
            exp_tol = expected["numeric_tolerance"]
            if exp_tol is None:
                assert item.answer_key.numeric_tolerance is None
            else:
                assert item.answer_key.numeric_tolerance == pytest.approx(exp_tol)
            choice_ids = [
                c[0] if not isinstance(c, str) else c for c in item.choices
            ]
            assert choice_ids == expected["choice_ids"]
            for probe in expected["verdicts"]:
                result = score_practice_response(item, probe["response"])
                assert result.scored is probe["scored"]
                assert result.correct is probe["correct"]
                assert result.matched_key == probe["matched_key"]
    assert seen == set(by_id)
    assert len(seen) == 6


def test_wave11_batch2_ledger_totals_and_remainder() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["needs_migration"] == 0
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["needs_manual_review"] == 0
    assert checked["totals"]["migrated"] == 2075
    assert live["totals"] == checked["totals"]

    pending = [
        (row["package_file"], item["field_path"])
        for row in live["packages"]
        for item in row["items"]
        if item["needs_manual_review"]
    ]
    assert pending == []
    assert list(wave11.WAVE11_REMAINDER_PACKAGES) == []

    for row in live["packages"]:
        if row["package_file"] not in set(wave11.WAVE11_BATCH2_FILES):
            continue
        for item in row["items"]:
            if item["needs_manual_review"]:
                raise AssertionError(
                    f"batch2 still pending: {row['package_file']} {item['field_path']}"
                )

    for package_file, field_path, expected in _WAVE11_B2_EXCLUSIONS:
        matches = [
            item
            for row in live["packages"]
            if row["package_file"] == package_file
            for item in row["items"]
            if item["field_path"] == field_path and item["text"] == expected
        ]
        assert len(matches) == 1
        assert matches[0]["migration_status"] == "correctly_excluded"

    for package_file, field_path, expected in _WAVE11_B2_MIGRATIONS:
        text = wave1.get_path(_load(package_file), field_path)
        assert text == expected
        matches = [
            item
            for row in live["packages"]
            if row["package_file"] == package_file
            for item in row["items"]
            if item["field_path"] == field_path and item["text"] == expected
        ]
        assert len(matches) == 1
        assert matches[0]["migration_status"] == "migrated"


def test_wave11_batch2_migration_and_exclusion_counts() -> None:
    assert len(_WAVE11_B2_MIGRATIONS) == 41
    assert len(_WAVE11_B2_EXCLUSIONS) == 19
    assert len(_WAVE11_B2_MIGRATIONS) + len(_WAVE11_B2_EXCLUSIONS) == 60
    assert len(_WAVE11_B2_PARTIAL_PROSE) == 34
    assert len(_ADJUSTED_R2_MIGRATED) == 8
    assert len(_ADJUSTED_R2_EXCLUDED) == 7

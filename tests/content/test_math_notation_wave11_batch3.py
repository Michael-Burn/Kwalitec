"""Wave 11 batch 3 mathematical notation: KaTeX, exclusions, scoring, ledger."""

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
    REPO_ROOT / "tests/fixtures/math_notation_wave11_batch3_scoring_snapshot.json"
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

# Locked Wave 11 batch 3 migrations (5 full + 31 partial).
_WAVE11_B3_MIGRATIONS = (
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Plug the factor indicators into $\eta$, remembering the interaction is zero unless both factors equal 1.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.success_criteria[0]",
        r"Closed-book, write $\eta$ for a simple continuous model and a factor model.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Compute $x^{2}$ first, then form $\eta$ before exponentiating.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[0].explanation",
        r"The linear predictor is linear in the parameters even when it includes $x^{2}$ as a constructed covariate.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        r"State what $\eta$ is versus $\mu$.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[2].explanation",
        r"$\eta$ is the linear predictor on the link scale; $\mu$ is the mean on the response scale after the inverse link.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.common_pitfall",
        r"Reporting $\eta$ as the mean severity, or dropping the quadratic term when $x^{2}$ is part of the specified linear predictor.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.success_criteria[0]",
        r"Closed-book, define the linear predictor $\eta$.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "reading_guidance.misconception_watch[0]",
        r"Watch for equating $\eta$ with $\mu$ without the link.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "knowledge_checks[1].explanation",
        "$\\eta(10) = 1.0 + 0.2\\times 10 - 0.01\\times 100 = 2.0$, so $\\mu = e^{2} \\approx 7.3891$ on the severity scale.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.steps[0].label",
        r"Write $\eta$ as $x^{\mathrm{T}}\beta$",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form $\Delta D$ before comparing to the chi-square critical value.",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.steps[1].explanation",
        r"Reject the reduced model when $\Delta D$ exceeds the $\chi^{2}$ critical value.",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "worked_example.steps[0].label",
        r"Pearson $X^{2}$",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "reading_guidance.misconception_watch[0]",
        r"Watch for treating a non-significant $\chi^{2}$ as automatic model perfection.",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "worked_example.steps[1].attempt_cue",
        r"Sum to $X^{2}$ and compare with $5.991$.",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "worked_example.steps[1].explanation",
        r"Large $X^{2}$ rejects aggregate adequacy of the fitted means.",
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.given[0].note",
        r"conjugate prior for $\theta$",
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Update $\alpha$ and $\beta$ with the Binomial counts.",
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.steps[1].explanation",
        r"Conjugacy adds successes to $\alpha$ and failures to $\beta$.",
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.common_pitfall",
        r"Updating as $\mathrm{Beta}(\alpha+n, \beta+s)$ or forgetting to add failures $n - s$ to $\beta$.",
    ),
    (
        "5.1.2-prior-posterior-cs1015.json",
        "worked_example.given[0].note",
        r"prior for $\theta$",
    ),
    (
        "5.1.2-prior-posterior-cs1015.json",
        "worked_example.steps[1].attempt_cue",
        r"Update to $\mathrm{Beta}(2+3, 8+10-3)$.",
    ),
    (
        "5.1.3-posterior-simple-cs1015.json",
        "worked_example.given[0].note",
        r"shape-rate prior for $\lambda$",
    ),
    (
        "5.1.4-loss-estimators-cs1015.json",
        "worked_example.given[1].note",
        r"$\pi(\theta \mid \mathrm{data})$",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.given[0].note",
        r"posterior for $\theta$",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form $\mathrm{mean} \pm 1.96 \times \mathrm{posterior SD}$, and phrase it as a posterior probability statement.",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $100 \pm 1.96 \times 5$.",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.common_pitfall",
        r"Interpreting $(90.2, 109.8)$ as a frequentist confidence interval ('95% of samples cover θ') instead of a posterior probability statement for θ.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].hints[0]",
        r"Compute $1 - Z$ first, then blend $\bar{X}$ and $\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].hints[1]",
        r"$Z$ weights the individual experience $\bar{X}$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].success_criteria[1]",
        r"Uses $Z$ on $\bar{X}$ and $(1 - Z)$ on $\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form the convex combination with weights $Z$ and $1 - Z$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $1 - Z$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $Z\bar{X} + (1 - Z)\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.steps[2].explanation",
        r"$Z$ is the weight on the risk's own experience $\bar{X}$; $1 - Z$ weights the class hypothetical mean.",
    ),
)

_WAVE11_B3_EXCLUSIONS = (
    (
        "4.2.4-factors-interactions-cs1014.json",
        "mission.success_criteria[2]",
        "Refuse one 'I wrote η, so I finished today's LO' claim.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "mission.task_descriptions[2]",
        "Closed-book Knowledge Checks: factors + refuse η swallow.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "reading_guidance.misconception_watch[1]",
        "Watch for jumping to full η polynomial forms (4.2.5) as today's finish.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.mission_purpose",
        "Today's Mission exists to define the linear predictor and write its form for simple models including polynomials and factors. So η is concrete.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.educational_intent",
        "Produce concrete η literacy.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.expected_benefit",
        "Study Progress for η forms. Not deviance estimation as primary.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.success_criteria[2]",
        "Refuse conflating η with the link.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.task_descriptions[0]",
        "Write two η sketches before CMP.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.tutor_intent",
        "Today I will force η-form writing for simple GLM structures and refuse treating deviance as today's LO.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.why_now",
        "4.2.5 is contiguous after factors. Without η forms, deviance and software fit lack structure.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.task_descriptions[0]",
        "Sketch η forms before CMP.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.task_descriptions[2]",
        "Closed-book Knowledge Checks: η forms + refuse deviance swallow.",
    ),
    (
        "4.2.6-deviance-estimation-cs1014.json",
        "mission.educational_intent",
        "Produce a cognitive move from η forms to lawful deviance and parameter estimation under CMP.",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "mission.task_descriptions[2]",
        "Knowledge Checks: Δ deviance + refuse kitchen-sink.",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "mission.concept_focus",
        "Fitted GLM → Pearson χ² acceptability test → likelihood-ratio test.",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "mission.expected_benefit",
        "You will be able to apply Pearson's χ² and likelihood-ratio tests to judge acceptability of a fitted GLM.",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "mission.success_criteria[0]",
        "Closed-book, name Pearson χ² and likelihood-ratio tests in GLM context.",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "reading_guidance.open_point",
        "CMP · Syllabus 4.2.9 Pearson χ² and likelihood-ratio tests",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "mission.tutor_intent",
        "Today I will force χ² vs LRT acceptability discrimination and refuse treating full software interpretation as today's LO.",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "mission.concept_focus",
        "Fitted GLM → Pearson χ² acceptability test → likelihood-ratio test.",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "mission.expected_benefit",
        "You will be able to apply Pearson's χ² and likelihood-ratio tests to judge acceptability of a fitted GLM.",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "mission.task_descriptions[0]",
        "Sketch χ² vs LRT before CMP.",
    ),
    (
        "5.1.2-prior-posterior-cs1015.json",
        "worked_example.steps[0].explanation",
        "The prior is the distribution of θ before seeing the new sample.",
    ),
    (
        "5.1.2-prior-posterior-cs1015.json",
        "worked_example.steps[2].explanation",
        "The posterior is the distribution of θ after combining prior and likelihood.",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "knowledge_checks[0].explanation",
        "Credible interval is posterior probability for θ. Repeated-sampling coverage slogan is the frequentist confidence interval reading unless carefully distinguished.",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.steps[1].explanation",
        "Unlike a frequentist CI, the credible interval places probability on θ given the data and prior.",
    ),
)

# Partial migrations: surrounding prose that must remain untouched.
_WAVE11_B3_PARTIAL_PROSE = (
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Plug the factor indicators into ",
            ", remembering the interaction is zero unless both factors equal 1.",
        ),
        (r"\eta",),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.success_criteria[0]",
        ("Closed-book, write ", " for a simple continuous model and a factor model."),
        (r"\eta",),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.attempt_before_reveal",
        ("CMP closed. Compute ", " first, then form ", " before exponentiating."),
        (r"x^{2}", r"\eta"),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[0].explanation",
        (
            "The linear predictor is linear in the parameters even when it includes ",
            " as a constructed covariate.",
        ),
        (r"x^{2}",),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        ("State what ", " is versus ", "."),
        (r"\eta", r"\mu"),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[2].explanation",
        (
            " is the linear predictor on the link scale; ",
            " is the mean on the response scale after the inverse link.",
        ),
        (r"\eta", r"\mu"),
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.common_pitfall",
        (
            "Reporting ",
            " as the mean severity, or dropping the quadratic term when ",
            " is part of the specified linear predictor.",
        ),
        (r"\eta", r"x^{2}"),
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.success_criteria[0]",
        ("Closed-book, define the linear predictor ", "."),
        (r"\eta",),
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "reading_guidance.misconception_watch[0]",
        ("Watch for equating ", " with ", " without the link."),
        (r"\eta", r"\mu"),
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "knowledge_checks[1].explanation",
        (
            " on the severity scale.",
        ),
        (r"\eta(10)", r"\mu", r"e^{2}"),
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.steps[0].label",
        ("Write ", " as "),
        (r"\eta", r"x^{\mathrm{T}}\beta"),
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Form ",
            " before comparing to the chi-square critical value.",
        ),
        (r"\Delta D",),
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.steps[1].explanation",
        (
            "Reject the reduced model when ",
            " exceeds the ",
            " critical value.",
        ),
        (r"\Delta D", r"\chi^{2}"),
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "worked_example.steps[0].label",
        ("Pearson ",),
        (r"X^{2}",),
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "reading_guidance.misconception_watch[0]",
        (
            "Watch for treating a non-significant ",
            " as automatic model perfection.",
        ),
        (r"\chi^{2}",),
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "worked_example.steps[1].attempt_cue",
        ("Sum to ", " and compare with ", "."),
        (r"X^{2}", r"5.991"),
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "worked_example.steps[1].explanation",
        ("Large ", " rejects aggregate adequacy of the fitted means."),
        (r"X^{2}",),
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.given[0].note",
        ("conjugate prior for ",),
        (r"\theta",),
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        ("Update ", " and ", " with the Binomial counts."),
        (r"\alpha", r"\beta"),
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.steps[1].explanation",
        ("Conjugacy adds successes to ", " and failures to ", "."),
        (r"\alpha", r"\beta"),
    ),
    (
        "5.1.2-prior-posterior-cs1003.json",
        "worked_example.common_pitfall",
        (
            "Updating as ",
            " or forgetting to add failures ",
            " to ",
            ".",
        ),
        (r"\mathrm{Beta}(\alpha+n, \beta+s)", r"n - s", r"\beta"),
    ),
    (
        "5.1.2-prior-posterior-cs1015.json",
        "worked_example.given[0].note",
        ("prior for ",),
        (r"\theta",),
    ),
    (
        "5.1.3-posterior-simple-cs1015.json",
        "worked_example.given[0].note",
        ("shape-rate prior for ",),
        (r"\lambda",),
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.given[0].note",
        ("posterior for ",),
        (r"\theta",),
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Form ",
            ", and phrase it as a posterior probability statement.",
        ),
        (r"\mathrm{mean} \pm 1.96 \times \mathrm{posterior SD}",),
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.common_pitfall",
        (
            "Interpreting ",
            " as a frequentist confidence interval ('95% of samples cover θ') instead of a posterior probability statement for θ.",
        ),
        (r"(90.2, 109.8)",),
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].hints[0]",
        ("Compute ", " first, then blend ", " and ", "."),
        (r"1 - Z", r"\bar{X}", r"\mu"),
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].hints[1]",
        (" weights the individual experience ", "."),
        (r"Z", r"\bar{X}"),
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].success_criteria[1]",
        ("Uses ", " on ", " and ", " on ", "."),
        (r"Z", r"\bar{X}", r"(1 - Z)", r"\mu"),
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Form the convex combination with weights ",
            " and ",
            ".",
        ),
        (r"Z", r"1 - Z"),
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.steps[2].explanation",
        (
            " is the weight on the risk's own experience ",
            "; ",
            " weights the class hypothetical mean.",
        ),
        (r"Z", r"\bar{X}", r"1 - Z"),
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
    _WAVE11_B3_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B3_MIGRATIONS],
)
def test_wave11_batch3_migrations_are_valid_katex(
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
    _WAVE11_B3_PARTIAL_PROSE,
    ids=[f"{p}:{f}" for p, f, *_ in _WAVE11_B3_PARTIAL_PROSE],
)
def test_wave11_batch3_partial_migrations_preserve_surrounding_prose(
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


def test_wave11_batch3_item55_numeric_interval_vs_prose_theta() -> None:
    """Item 55: typeset (90.2, 109.8); both θ mentions stay plain prose."""
    text = wave1.get_path(
        _load("5.1.5-credible-intervals-cs1015.json"),
        "worked_example.common_pitfall",
    )
    assert r"$(90.2, 109.8)$" in text
    assert "cover θ" in text
    assert "statement for θ." in text
    assert r"\theta" not in text
    assert text.count("θ") == 2


def test_wave11_batch3_item22_preserves_english_eta() -> None:
    text = wave1.get_path(
        _load("4.2.5-linear-predictor-cs1014.json"),
        "knowledge_checks[1].explanation",
    )
    assert "on the severity scale" in text
    assert r"\mu" in text and r"\eta" in text
    assert r"e^{2}" in text


def test_wave11_batch3_item26_preserves_english_chi_square() -> None:
    text = wave1.get_path(
        _load("4.2.7-model-choice-cs1003.json"),
        "worked_example.attempt_before_reveal",
    )
    assert "chi-square critical value" in text
    assert r"\Delta D" in text
    assert r"\chi" not in text


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_B3_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B3_EXCLUSIONS],
)
def test_wave11_batch3_exclusions_are_byte_identical_and_confirmed(
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


def test_wave11_batch3_scoring_unaffected_for_touched_knowledge_checks() -> None:
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
            pack, curriculum_identity="CS1:wave11b3", topic_id=pack.topic_code
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


def test_wave11_batch3_ledger_totals_and_remainder() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["needs_migration"] == 0
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["needs_manual_review"] == 0
    assert checked["totals"]["migrated"] == 2087
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
        if row["package_file"] not in set(wave11.WAVE11_BATCH3_FILES):
            continue
        for item in row["items"]:
            if item["needs_manual_review"]:
                raise AssertionError(
                    f"batch3 still pending: {row['package_file']} {item['field_path']}"
                )

    for package_file, field_path, expected in _WAVE11_B3_EXCLUSIONS:
        matches = [
            item
            for row in live["packages"]
            if row["package_file"] == package_file
            for item in row["items"]
            if item["field_path"] == field_path and item["text"] == expected
        ]
        assert len(matches) == 1
        assert matches[0]["migration_status"] == "correctly_excluded"

    for package_file, field_path, expected in _WAVE11_B3_MIGRATIONS:
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


def test_wave11_batch3_migration_and_exclusion_counts() -> None:
    assert len(_WAVE11_B3_MIGRATIONS) == 36
    assert len(_WAVE11_B3_EXCLUSIONS) == 26
    assert len(_WAVE11_B3_MIGRATIONS) + len(_WAVE11_B3_EXCLUSIONS) == 62
    assert len(_WAVE11_B3_PARTIAL_PROSE) == 31

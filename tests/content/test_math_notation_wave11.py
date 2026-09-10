"""Wave 11 batch 1 mathematical notation: KaTeX, exclusions, scoring, ledger.

Batch 2 coverage lives in ``test_math_notation_wave11_batch2.py``.
"""

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
    REPO_ROOT / "tests/fixtures/math_notation_wave11_scoring_snapshot.json"
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

# Locked Wave 11 batch 1 migrations (9 full + 30 partial).
_WAVE11_MIGRATIONS = (
    (
        "1.2.2-eda-association-ep001.json",
        "worked_example.steps[1].attempt_cue",
        r"Compare $|r|$ and $|\rho|$ in light of the scatter.",
    ),
    (
        "2.1.2-continuous-cs1002.json",
        "worked_example.given[0].note",
        r"continuous support on $(0, \infty)$",
    ),
    (
        "2.1.4-poisson-process-cs1004.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Link process $\mathrm{rate} \times \mathrm{time}$ to the Poisson count mean, then name the interarrival family.",
    ),
    (
        "2.1.4-poisson-process-cs1004.json",
        "worked_example.steps[0].attempt_cue",
        r"State $N(t)$ for a Poisson process with rate $\lambda$.",
    ),
    (
        "2.1.4-poisson-process-cs1004.json",
        "worked_example.steps[0].explanation",
        r"In a homogeneous Poisson process with rate $\lambda$, the count in an interval of length t is Poisson with mean $\lambda t$.",
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "worked_example.given[1].note",
        r"waiting times in days; support $(0, \infty)$",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "worked_example.title",
        r"Mean and variance of $2X - Y$ with nonzero covariance",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.steps[0].explanation",
        r"An Exponential waiting-time law is right-skewed and supported on $(0, \infty)$. Matching mean and sd to a Normal does not remove that skew for individual observations.",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.steps[1].attempt_cue",
        r"Decide whether $Normal(400, 400^{2})$ describes the histogram of draws.",
    ),
    (
        "2.6.2-sampling-distribution-statistic-cs1009.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Define the sampling distribution over repeated samples, then compute mean and variance of $\bar{X}$, then classify 78.",
    ),
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "worked_example.title",
        r"Mean and variance of $\bar{X}$ and mean of $S^{2}$",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[0].attempt_cue",
        r"Name the Normal parameters for $\bar{X}$.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[0].label",
        r"Sampling distribution of $\bar{X}$",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[1].explanation",
        r"Under Normal sampling and $H_{0}$, t follows Student-t with $n - 1$ degrees of freedom.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "worked_example.common_pitfall",
        r"Using t with pooled sd to compare variances, or assigning F degrees of freedom as $n_{1}$ and $n_{2}$ instead of $n_{1} - 1$ and $n_{2} - 1$.",
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "mission.success_criteria[2]",
        r"Refuse one 'any formula for $\hat{\theta}$ is MoM' claim.",
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Before uncovering, write the first population moment in terms of $\mu$ and the matching sample moment.",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[0].note",
        r"bias of $T_{1}$",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[1].note",
        r"variance of $T_{1}$",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[2].note",
        r"bias of $T_{2}$",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[3].note",
        r"variance of $T_{2}$",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[0].label",
        r"MSE of $T_{1}$",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[1].explanation",
        r"Squared bias is added in full; do not omit the $\mathrm{Bias}^{2}$ term.",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[1].label",
        r"MSE of $T_{2}$",
    ),
    (
        "3.1.5-asymptotic-mle-cs1010.json",
        "worked_example.steps[1].attempt_cue",
        r"Multiply $\widehat{\mathrm{SE}}$ by $1.96$.",
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. First compute $\bar{\theta}^{*}$, then the average squared deviation.",
    ),
    (
        "3.2.1-confidence-interval-parameter-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $12000 \pm 588$.",
    ),
    (
        "3.2.2-prediction-interval-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $500 \pm 79.953$.",
    ),
    (
        "3.2.2-prediction-interval-cs1011.json",
        "worked_example.steps[2].explanation",
        r"Centre at $\bar{x}$; the wider SE distinguishes prediction from mean estimation.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "knowledge_checks[1].common_mistake",
        r"Ignoring the given $\chi^{2}$ pivot or inverting the inequality incorrectly.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Invert $\hat{\theta} \sim N(\theta, 0.01^{2})$ into $\hat{\theta} \pm 1.96 \times 0.01$.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $1.96 \times 0.01$.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $0.42 \pm 0.0196$.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.steps[1].explanation",
        r"Centre at the observed $\hat{\theta}$.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[0].common_mistake",
        r"Treating the mean CI as enough, or reusing the mean formula for $\sigma^{2}$.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[1].common_mistake",
        r"Using $z$ with unknown $\sigma$, skipping the variance CI, or forcing a Normal-mean SE onto $\sigma^{2}$.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[0].explanation",
        r"With $\sigma$ unknown, replace $\sigma$ by $s$ in the SE of the mean.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $100 \pm 3.1965$.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[2].explanation",
        r"Centre at $\bar{x}$.",
    ),
)

_WAVE11_EXCLUSIONS = (
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "knowledge_checks[1].success_criteria[1]",
        "Uses the Exponential CDF with mean θ, not the survival function alone.",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "knowledge_checks[0].explanation",
        "The object to compare is the repeated-sampling distribution of X̄, and changing n reveals convergence behaviour.",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.common_pitfall",
        "Treating a matched-mean-and-sd Normal overlay as automatically adequate for skewed individual draws, or confusing that histogram comparison with a CLT statement about X̄.",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.steps[2].attempt_cue",
        "State what improves when comparing sampling distributions of X̄ at large n.",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.steps[2].explanation",
        "The CLT concerns the sample mean, not individual draws. Histograms of X̄ from many large-n replications become closer to Normal even when the parent is Exponential; that is a different comparison from overlaying Normal on raw waiting times.",
    ),
    (
        "2.6.2-sampling-distribution-statistic-cs1009.json",
        "worked_example.steps[0].explanation",
        "The sampling distribution of the sample mean is the probability distribution of values X̄ would take over repeated random samples of the same size.",
    ),
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "knowledge_checks[0].common_mistake",
        "Confusing population variance, variance of the sample mean, and the target of S².",
    ),
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "worked_example.steps[0].explanation",
        "For a random sample with finite mean, the sample mean is unbiased for μ.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.expected_benefit",
        "You will be able to state the Normal and χ² sampling laws for X̄ and S² under Normal samples, without jumping to t.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.success_criteria[0]",
        "Closed-book, state the sampling distribution of X̄ for Normal samples (CMP form).",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.tutor_intent",
        "Today I will force Normal-sample laws for X̄ and S² (χ² form as CMP). Refuse treating moment results alone as the distributional laws.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.why_now",
        "2.6.4 is the distributional hinge before student-t when σ is unknown.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "mission.educational_intent",
        "Produce the cognitive move from Normal sample with unknown σ to the t-statistic and its sampling distribution (CMP).",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "mission.prior_bridge",
        "Yesterday you stated Normal sampling distributions for mean and variance (2.6.4). Today forms the t-statistic when σ is unknown.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "mission.task_descriptions[0]",
        "Sketch unknown-σ → t before CMP.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "mission.tutor_intent",
        "Today I will force the candidate through the t construction (unknown σ). Refuse treating Normal X̄ laws with known σ as having finished t.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "reading_guidance.misconception_watch[0]",
        "Watch for using z when S replaces σ without naming t.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[0].explanation",
        "With σ unknown, the studentised mean uses the sample sd in the denominator.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[2].explanation",
        "Using S inside a Normal z formula pretends σ is known. The t law accounts for estimating σ. An F comparison of two sample variances is a different sampling problem from this one-sample mean pivot.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "mission.concept_focus",
        "Two independent Normal samples → variance ratio → F(df₁, df₂) → refuse using t for that job.",
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "knowledge_checks[1].explanation",
        "Bootstrap SE uses the spread of many with-replacement replicates of θ̂. Asymptotic variance plug-ins and bootstrap CI construction are different procedures.",
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "worked_example.steps[0].explanation",
        "θ̄* centres the bootstrap deviations used in the SE formula.",
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "worked_example.steps[1].explanation",
        "Each replicate's squared distance from θ̄* enters the bootstrap variance.",
    ),
    (
        "3.2.1-confidence-interval-parameter-cs1011.json",
        "knowledge_checks[1].explanation",
        "Frequentist coverage is about the procedure and the parameter μ, not about the next observation. Treating μ as a random draw inside the interval, or equating narrowness with certainty, misstates coverage.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[1].explanation",
        "The t quantile (not 1.96) accounts for estimating σ.",
    ),
)

# Partial migrations: surrounding prose that must remain untouched.
_WAVE11_PARTIAL_PROSE = (
    (
        "1.2.2-eda-association-ep001.json",
        "worked_example.steps[1].attempt_cue",
        ("Compare ", " in light of the scatter."),
        (r"|r|", r"|\rho|"),
    ),
    (
        "2.1.2-continuous-cs1002.json",
        "worked_example.given[0].note",
        ("continuous support on ",),
        (r"(0, \infty)",),
    ),
    (
        "2.1.4-poisson-process-cs1004.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Link process ",
            " to the Poisson count mean, then name the interarrival family.",
        ),
        (r"\mathrm{rate} \times \mathrm{time}",),
    ),
    (
        "2.1.4-poisson-process-cs1004.json",
        "worked_example.steps[0].explanation",
        (
            "In a homogeneous Poisson process with rate ",
            ", the count in an interval of length t is Poisson with mean ",
            ".",
        ),
        (r"\lambda", r"\lambda t"),
    ),
    (
        "2.1.6-software-generation-cs1004.json",
        "worked_example.given[1].note",
        ("waiting times in days; support ",),
        (r"(0, \infty)",),
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "worked_example.title",
        ("Mean and variance of ", " with nonzero covariance"),
        (r"2X - Y",),
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.steps[0].explanation",
        (
            "An Exponential waiting-time law is right-skewed and supported on ",
            ". Matching mean and sd to a Normal does not remove that skew for individual observations.",
        ),
        (r"(0, \infty)",),
    ),
    (
        "2.6.2-sampling-distribution-statistic-cs1009.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Define the sampling distribution over repeated samples, then compute mean and variance of ",
            ", then classify 78.",
        ),
        (r"\bar{X}",),
    ),
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "worked_example.title",
        ("Mean and variance of ", " and mean of "),
        (r"\bar{X}", r"S^{2}"),
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[0].attempt_cue",
        ("Name the Normal parameters for ",),
        (r"\bar{X}",),
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[0].label",
        ("Sampling distribution of ",),
        (r"\bar{X}",),
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[1].explanation",
        (
            "Under Normal sampling and ",
            ", t follows Student-t with ",
            " degrees of freedom.",
        ),
        (r"H_{0}", r"n - 1"),
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "worked_example.common_pitfall",
        (
            "Using t with pooled sd to compare variances, or assigning F degrees of freedom as ",
            " and ",
            " instead of ",
            " and ",
            ".",
        ),
        (r"n_{1}", r"n_{2}", r"n_{1} - 1", r"n_{2} - 1"),
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "mission.success_criteria[2]",
        ("Refuse one 'any formula for ", " is MoM' claim."),
        (r"\hat{\theta}",),
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Before uncovering, write the first population moment in terms of ",
            " and the matching sample moment.",
        ),
        (r"\mu",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[0].note",
        ("bias of ",),
        (r"T_{1}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[1].note",
        ("variance of ",),
        (r"T_{1}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[2].note",
        ("bias of ",),
        (r"T_{2}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.given[3].note",
        ("variance of ",),
        (r"T_{2}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[0].label",
        ("MSE of ",),
        (r"T_{1}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[1].explanation",
        ("Squared bias is added in full; do not omit the ", " term."),
        (r"\mathrm{Bias}^{2}",),
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[1].label",
        ("MSE of ",),
        (r"T_{2}",),
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "worked_example.attempt_before_reveal",
        ("CMP closed. First compute ", ", then the average squared deviation."),
        (r"\bar{\theta}^{*}",),
    ),
    (
        "3.2.2-prediction-interval-cs1011.json",
        "worked_example.steps[2].explanation",
        (
            "Centre at ",
            "; the wider SE distinguishes prediction from mean estimation.",
        ),
        (r"\bar{x}",),
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "knowledge_checks[1].common_mistake",
        (
            "Ignoring the given ",
            " pivot or inverting the inequality incorrectly.",
        ),
        (r"\chi^{2}",),
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.steps[1].explanation",
        ("Centre at the observed ",),
        (r"\hat{\theta}",),
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[0].common_mistake",
        (
            "Treating the mean CI as enough, or reusing the mean formula for ",
            ".",
        ),
        (r"\sigma^{2}",),
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[1].common_mistake",
        (
            "Using ",
            " with unknown ",
            ", skipping the variance CI, or forcing a Normal-mean SE onto ",
            ".",
        ),
        (r"z", r"\sigma", r"\sigma^{2}"),
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[0].explanation",
        (
            "With ",
            " unknown, replace ",
            " by ",
            " in the SE of the mean.",
        ),
        (r"\sigma", r"\sigma", r"s"),
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.steps[2].explanation",
        ("Centre at ",),
        (r"\bar{x}",),
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
    for match in re.finditer(r"\\frac(?![A-Za-z])", body):
        rest = body[match.end() :]
        assert rest.startswith("{"), f"\\frac missing numerator at {where}: {body}"
    for match in re.finditer(r"\\sqrt(?![A-Za-z])", body):
        rest = body[match.end() :].lstrip()
        assert rest.startswith("{") or rest.startswith("["), (
            f"\\sqrt missing argument at {where}: {body}"
        )


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_MIGRATIONS],
)
def test_wave11_migrations_are_valid_katex(
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
    _WAVE11_PARTIAL_PROSE,
    ids=[f"{p}:{f}" for p, f, *_ in _WAVE11_PARTIAL_PROSE],
)
def test_wave11_partial_migrations_preserve_surrounding_prose(
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


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_EXCLUSIONS],
)
def test_wave11_exclusions_are_byte_identical_and_confirmed(
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


def test_wave11_scoring_unaffected_for_touched_knowledge_checks() -> None:
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
            pack, curriculum_identity="CS1:wave11", topic_id=pack.topic_code
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
    assert len(seen) == 14


def test_wave11_ledger_totals_and_remainder() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["needs_migration"] == 0
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["needs_manual_review"] == 0
    assert checked["totals"]["migrated"] == 2043
    assert live["totals"] == checked["totals"]

    pending = [
        (row["package_file"], item["field_path"])
        for row in live["packages"]
        for item in row["items"]
        if item["needs_manual_review"]
    ]
    assert pending == []
    assert list(wave11.WAVE11_REMAINDER_PACKAGES) == []

    batch1_manual = 0
    batch1_migrated_new = 0
    for row in live["packages"]:
        if row["package_file"] not in set(wave11.WAVE11_BATCH1_FILES):
            continue
        for item in row["items"]:
            if item["needs_manual_review"]:
                raise AssertionError(
                    f"batch1 still pending: {row['package_file']} {item['field_path']}"
                )
    for package_file, field_path, expected in _WAVE11_EXCLUSIONS:
        matches = [
            item
            for row in live["packages"]
            if row["package_file"] == package_file
            for item in row["items"]
            if item["field_path"] == field_path and item["text"] == expected
        ]
        assert len(matches) == 1
        assert matches[0]["migration_status"] == "correctly_excluded"
        batch1_manual += 1
    assert batch1_manual == 25

    for package_file, field_path, expected in _WAVE11_MIGRATIONS:
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
        batch1_migrated_new += 1
    assert batch1_migrated_new == 39


def test_wave11_migration_and_exclusion_counts() -> None:
    assert len(_WAVE11_MIGRATIONS) == 39
    assert len(_WAVE11_EXCLUSIONS) == 25
    assert len(_WAVE11_MIGRATIONS) + len(_WAVE11_EXCLUSIONS) == 64

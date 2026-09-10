"""Wave 11 batch 4 mathematical notation: KaTeX, exclusions, scoring, ledger."""

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
    REPO_ROOT / "tests/fixtures/math_notation_wave11_batch4_scoring_snapshot.json"
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

# Locked Wave 11 batch 4 migrations (6 full + 21 partial).
_WAVE11_B4_MIGRATIONS = (
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].hints[0]",
        r"Compute $1 - Z$ first, then blend $\bar{X}$ and $\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].hints[1]",
        r"$Z$ weights the individual experience $\bar{X}$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].success_criteria[1]",
        r"Uses $Z$ on $\bar{X}$ and $(1 - Z)$ on $\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $1 - Z$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[1].attempt_cue",
        r"Evaluate $Z\bar{X} + (1 - Z)\mu$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[1].explanation",
        r"$Z$ weights the individual mean; $(1 - Z)$ weights the class mean.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[2].explanation",
        r"Larger $Z$ places more weight on the risk's own experience $\bar{X}$.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $Z\bar{X} + (1 - Z)\mu$.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.steps[2].attempt_cue",
        r"Evaluate $Z\bar{X} + (1 - Z)\mu$.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1003.json",
        "worked_example.common_pitfall",
        r"Forcing the two premiums to match by reusing one $Z$ for both structural pairs, or claiming EB and Bayes must always agree for the same $\bar{X}$.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1003.json",
        "worked_example.steps[2].explanation",
        r"Same risk experience can produce different premiums when $(\mu, k)$ differ because Bayes uses specified prior structurals while EB uses estimated ones.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.common_pitfall",
        r"Assuming the two approaches must produce identical premiums whenever $\bar{X}$ and $n$ match, or mixing Bayes $\mu$ with EB $\hat{k}$ in one formula.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[2].explanation",
        r"Bayes assumes a specified prior structure; EB estimates structurals from collective data. Different $(\mu, k)$ pairs produce different $Z$ and different blends, so premiums need not match.",
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Equate the Poisson mean $\lambda$ to the sample mean before computing.",
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "worked_example.steps[1].explanation",
        r"Substitute the observed counts into $\bar{x}$.",
    ),
    (
        "cp-3.2.1-ci-sample-cs1016.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $450 \pm 1.96 \times 5$.",
    ),
    (
        "cp-3.2.1-ci-sample-cs1016.json",
        "worked_example.steps[1].explanation",
        r"95% z-interval centres at $\bar{x}$.",
    ),
    (
        "cr-1.2.2-correlation-cs1017.json",
        "worked_example.steps[1].attempt_cue",
        r"Compare $|r|$ and $|\rho|$ in light of the scatter.",
    ),
    (
        "cr-2.1.2-continuous-cs1017.json",
        "worked_example.given[0].note",
        r"continuous support on $(0, \infty)$",
    ),
    (
        "revision-confidence-intervals-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Compute $\bar{X} \pm 1.96\,\mathrm{SE}$.",
    ),
    (
        "revision-distributions-generation-cs1004.json",
        "worked_example.common_pitfall",
        r"Generating Exponential draws by applying the CDF to $U$ instead of the inverse CDF, or multiplying by $\lambda$ instead of dividing by $\lambda$ in the quantile formula.",
    ),
    (
        "revision-distributions-generation-cs1004.json",
        "worked_example.steps[0].attempt_cue",
        r"Write $X$ in terms of $U$ and $\lambda$.",
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.steps[0].explanation",
        r"$Y$ is the response; columns of $X$ are explanatory variables; OLS chooses $\beta$ to minimise the sum of squared residuals.",
    ),
    (
        "revision-regression-glm-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"State $g(\mu)$ for Poisson.",
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[0].attempt_cue",
        r"What distribution does $\bar{X}$ have across repeated samples?",
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[1].attempt_cue",
        r"Write $T$ when $\sigma$ is estimated by $S$.",
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[2].explanation",
        r"Replacing $\sigma$ by $S$ without switching to t ignores the extra uncertainty from estimating the variance.",
    ),
)

_WAVE11_B4_EXCLUSIONS = (
    (
        "5.1.7-bayesian-credibility-cs1003.json",
        "knowledge_checks[0].explanation",
        "Bayesian credibility requires prior-to-posterior structure that justifies μ and Z. Empty formula or EB conflation are wrong.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.steps[2].explanation",
        "The premium blends experience with the prior mean μ.",
    ),
    (
        "5.1.8-empirical-bayes-cs1003.json",
        "worked_example.steps[1].explanation",
        "The premium uses estimated μ and k in place of known prior structurals.",
    ),
    (
        "5.1.8-empirical-bayes-cs1015.json",
        "worked_example.steps[1].explanation",
        "The premium formula matches classical credibility, with estimated Z and μ.",
    ),
    (
        "5.1.8-empirical-bayes-cs1015.json",
        "worked_example.steps[2].explanation",
        "EB estimates μ and k from data; a fully Bayesian analysis would take them from an explicit prior structure.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[0].explanation",
        "Bayes uses prior-specified μ and k.",
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "knowledge_checks[1].success_criteria[1]",
        "Uses the sample mean as MoM for the Poisson mean λ.",
    ),
    (
        "cp-3.2.1-ci-sample-cs1016.json",
        "knowledge_checks[1].explanation",
        "Coverage is about μ and the procedure. Prediction readings and 'midpoint probability' misstate frequentist CIs; HT is a related but distinct task.",
    ),
    (
        "cp-3.3.1-hypothesis-testing-cs1016.json",
        "worked_example.steps[0].explanation",
        "Type I error is a false rejection of H₀. With H₀: clean, that is flagging a clean claim as fraud.",
    ),
    (
        "cp-3.3.1-hypothesis-testing-cs1016.json",
        "worked_example.steps[1].explanation",
        "Type II error is failing to reject H₀ when the claim is fraudulent (H₀ false).",
    ),
    (
        "revision-confidence-intervals-cs1011.json",
        "worked_example.common_pitfall",
        "Saying that given these data, θ has probability 0.95 of lying in the calculated interval, which swaps a frequentist coverage statement for a posterior probability reading.",
    ),
    (
        "revision-confidence-intervals-cs1011.json",
        "worked_example.steps[0].explanation",
        "The construction procedure covers the fixed parameter θ in 95% of repeated samples under the model. It does not assign posterior probability 0.95 to θ given these data.",
    ),
    (
        "revision-distributions-generation-cs1004.json",
        "worked_example.steps[2].explanation",
        "Applying the CDF rather than its inverse does not produce an Exponential(λ) draw. The method maps Uniform probability through the quantile function.",
    ),
    (
        "revision-glm-cs1014.json",
        "reading_guidance.focus_questions[1]",
        "Can you state family → link → η → deviance → residuals → tests → fit?",
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.common_pitfall",
        "Confusing OLS with minimising fitted values, or treating a large R² as proof that a funnel-shaped residual plot can be ignored.",
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        "Can high R² dismiss the residual pattern?",
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.steps[2].explanation",
        "A large R² does not repair a clear residual funnel. Diagnostics remain required.",
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.steps[2].label",
        "Refuse R²-as-diagnostics",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.attempt_before_reveal",
        "CMP closed. Retrieve the residual-sum-of-squares criterion, then interpret curvature despite high R².",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.common_pitfall",
        "Minimising the sum of fitted values instead of squared residuals, or treating high R² from automated selection as proof that a curved residual plot can be ignored.",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.steps[2].attempt_cue",
        "Does high R² clear the curvature?",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.steps[2].explanation",
        "High R² and automated selection do not establish adequacy when residuals show clear curvature. Reconsider justified transformations or nonlinear terms and validate.",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.steps[2].label",
        "Refuse R²-as-adequacy",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.title",
        "Retrieve OLS criterion and refuse R²-clears-curvature",
    ),
    (
        "revision-regression-glm-cs1003.json",
        "mission.success_criteria[1]",
        "Retrieve Family → η → link.",
    ),
    (
        "revision-regression-glm-cs1003.json",
        "worked_example.steps[0].label",
        "Retrieve Family → η → link",
    ),
)

# Partial migrations: surrounding prose that must remain untouched.
_WAVE11_B4_PARTIAL_PROSE = (
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].hints[0]",
        ("Compute ", " first, then blend ", " and ", "."),
        (r"1 - Z", r"\bar{X}", r"\mu"),
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].hints[1]",
        (" weights the individual experience ",),
        (r"Z", r"\bar{X}"),
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].success_criteria[1]",
        ("Uses ", " on ", " and ", " on ", "."),
        (r"Z", r"\bar{X}", r"(1 - Z)", r"\mu"),
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[1].explanation",
        (" weights the individual mean; ", " weights the class mean."),
        (r"Z", r"(1 - Z)"),
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.steps[2].explanation",
        ("Larger ", " places more weight on the risk's own experience ", "."),
        (r"Z", r"\bar{X}"),
    ),
    (
        "5.1.9-bayes-vs-eb-cs1003.json",
        "worked_example.common_pitfall",
        (
            "Forcing the two premiums to match by reusing one ",
            " for both structural pairs, or claiming EB and Bayes must always agree for the same ",
            ".",
        ),
        (r"Z", r"\bar{X}"),
    ),
    (
        "5.1.9-bayes-vs-eb-cs1003.json",
        "worked_example.steps[2].explanation",
        (
            "Same risk experience can produce different premiums when ",
            " differ because Bayes uses specified prior structurals while EB uses estimated ones.",
        ),
        (r"(\mu, k)",),
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.common_pitfall",
        (
            "Assuming the two approaches must produce identical premiums whenever ",
            " and ",
            " match, or mixing Bayes ",
            " with EB ",
            " in one formula.",
        ),
        (r"\bar{X}", r"n", r"\mu", r"\hat{k}"),
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[2].explanation",
        (
            "Bayes assumes a specified prior structure; EB estimates structurals from collective data. Different ",
            " pairs produce different ",
            " and different blends, so premiums need not match.",
        ),
        (r"(\mu, k)", r"Z"),
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "worked_example.attempt_before_reveal",
        (
            "CMP closed. Equate the Poisson mean ",
            " to the sample mean before computing.",
        ),
        (r"\lambda",),
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "worked_example.steps[1].explanation",
        ("Substitute the observed counts into ", "."),
        (r"\bar{x}",),
    ),
    (
        "cp-3.2.1-ci-sample-cs1016.json",
        "worked_example.steps[1].explanation",
        ("95% z-interval centres at ", "."),
        (r"\bar{x}",),
    ),
    (
        "cr-1.2.2-correlation-cs1017.json",
        "worked_example.steps[1].attempt_cue",
        ("Compare ", " and ", " in light of the scatter."),
        (r"|r|", r"|\rho|"),
    ),
    (
        "cr-2.1.2-continuous-cs1017.json",
        "worked_example.given[0].note",
        ("continuous support on ",),
        (r"(0, \infty)",),
    ),
    (
        "revision-distributions-generation-cs1004.json",
        "worked_example.common_pitfall",
        (
            "Generating Exponential draws by applying the CDF to ",
            " instead of the inverse CDF, or multiplying by ",
            " instead of dividing by ",
            " in the quantile formula.",
        ),
        (r"U", r"\lambda"),
    ),
    (
        "revision-distributions-generation-cs1004.json",
        "worked_example.steps[0].attempt_cue",
        ("Write ", " in terms of ", " and ", "."),
        (r"X", r"U", r"\lambda"),
    ),
    (
        "revision-linear-models-cs1003.json",
        "worked_example.steps[0].explanation",
        (
            " is the response; columns of ",
            " are explanatory variables; OLS chooses ",
            " to minimise the sum of squared residuals.",
        ),
        (r"Y", r"X", r"\beta"),
    ),
    (
        "revision-regression-glm-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        ("State ", " for Poisson."),
        (r"g(\mu)",),
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[0].attempt_cue",
        ("What distribution does ", " have across repeated samples?"),
        (r"\bar{X}",),
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[1].attempt_cue",
        ("Write ", " when ", " is estimated by ", "."),
        (r"T", r"\sigma", r"S"),
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[2].explanation",
        (
            "Replacing ",
            " by ",
            " without switching to t ignores the extra uncertainty from estimating the variance.",
        ),
        (r"\sigma", r"S"),
    ),
)


def _load(package_file: str) -> dict:
    return json.loads((PACKAGES / package_file).read_text(encoding="utf-8"))


def _spans(text: str) -> list[str]:
    return _MATH_SPAN.findall(text)


def _assert_valid_latex(body: str, *, where: str) -> None:
    assert body.strip(), f"empty math span at {where}"
    assert "$" not in body, f"nested dollar at {where}: {body!r}"
    for cmd in _CONTROL.findall(body):
        assert cmd in _KNOWN_COMMANDS, f"unknown command \\{cmd} at {where}: {body!r}"


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE11_B4_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B4_MIGRATIONS],
)
def test_wave11_batch4_migrations_are_valid_katex(
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
    _WAVE11_B4_PARTIAL_PROSE,
    ids=[f"{p}:{f}" for p, f, *_ in _WAVE11_B4_PARTIAL_PROSE],
)
def test_wave11_batch4_partial_migrations_preserve_surrounding_prose(
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
    _WAVE11_B4_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE11_B4_EXCLUSIONS],
)
def test_wave11_batch4_exclusions_are_byte_identical_and_confirmed(
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


def test_wave11_batch4_scoring_unaffected_for_touched_knowledge_checks() -> None:
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
            pack, curriculum_identity="CS1:wave11b4", topic_id=pack.topic_code
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
    assert len(seen) == 8


def test_wave11_batch4_ledger_catalogue_closed() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["needs_migration"] == 0
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["needs_manual_review"] == 0
    assert checked["totals"]["migrated"] == 2063
    assert live["totals"] == checked["totals"]

    pending_nmr = [
        (row["package_file"], item["field_path"])
        for row in live["packages"]
        for item in row["items"]
        if item["needs_manual_review"]
    ]
    assert pending_nmr == []
    # No provisional exclusion remains: every correctly_excluded row is either a
    # human-confirmed manual_review_prose_exclusion or an automated
    # prose_mention_cue (already needs_manual_review=false).
    provisional = [
        (row["package_file"], item["field_path"], item["reason_code"])
        for row in live["packages"]
        for item in row["items"]
        if item["category"] == "correctly_excluded" and item["needs_manual_review"]
    ]
    assert provisional == []
    assert list(wave11.WAVE11_REMAINDER_PACKAGES) == []
    assert wave11.WAVE11_BATCH4_FILES[0] == "5.1.6-credibility-premium-cs1015.json"
    assert len(wave11.WAVE11_BATCH4_FILES) == 19

    for row in live["packages"]:
        if row["package_file"] not in set(wave11.WAVE11_BATCH4_FILES):
            continue
        for item in row["items"]:
            if item["needs_manual_review"]:
                raise AssertionError(
                    f"batch4 still pending: {row['package_file']} {item['field_path']}"
                )

    for package_file, field_path, expected in _WAVE11_B4_EXCLUSIONS:
        matches = [
            item
            for row in live["packages"]
            if row["package_file"] == package_file
            for item in row["items"]
            if item["field_path"] == field_path and item["text"] == expected
        ]
        assert len(matches) == 1
        assert matches[0]["migration_status"] == "correctly_excluded"

    for package_file, field_path, expected in _WAVE11_B4_MIGRATIONS:
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


def test_wave11_batch4_migration_and_exclusion_counts() -> None:
    assert len(_WAVE11_B4_MIGRATIONS) == 27
    assert len(_WAVE11_B4_EXCLUSIONS) == 26
    assert len(_WAVE11_B4_MIGRATIONS) + len(_WAVE11_B4_EXCLUSIONS) == 53
    assert len(_WAVE11_B4_PARTIAL_PROSE) == 21

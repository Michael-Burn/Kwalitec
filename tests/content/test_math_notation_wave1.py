"""Wave 1 mathematical notation migration: KaTeX validity, scoring, ledger."""

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
from app.presentation.session.math_markup import prepare_math_markup

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402
import math_notation_wave1 as wave1  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave1_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Wave 1 authored math.
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
        "alpha",
        "varepsilon",
        "ell",
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
        "ldots",
        "colon",
        "left",
        "right",
        "quad",
        "qquad",
        "text",
        "in",
        "to",
        "cdot",
        "pm",
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Representative (package, path, must-contain) meaning checks across categories.
_MEANING_SAMPLES = (
    (
        "2.5.1-clt-cs1008.json",
        "worked_example.steps[0].calculation",
        (r"\frac{\sigma}{\sqrt{n}}", r"\frac{60}{\sqrt{36}}", "10"),
        "fraction + root of sampling sd",
    ),
    (
        "4.2.8-residuals-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"\sqrt{6}", r"\sqrt{1.5}", "-1.2247"),
        "nested root in Pearson residual",
    ),
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "knowledge_checks[0].model_answer",
        (r"\bar{X}", r"\mu", r"\frac{\sigma^{2}}{n}"),
        "Greek-as-variable sample-mean law",
    ),
    (
        "4.1.3-least-squares-cs1003.json",
        "worked_example.steps[2].result",
        (r"\hat{\beta}_{1}", r"\hat{\beta}_{0}", "-0.3"),
        "subscripted OLS estimates",
    ),
    (
        "3.1.2-maximum-likelihood-cs1010.json",
        "worked_example.steps[1].calculation",
        (r"\frac{d\ell}{d\lambda}", r"\hat{\lambda}", "0.4"),
        "multi-step MLE score equation",
    ),
    (
        "3.2.5-ci-binomial-poisson-cs1011.json",
        "worked_example.steps[1].calculation",
        (r"\sqrt", "0.22", "0.041425"),
        "binomial SE root",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[0].calculation",
        (r"\frac{S}{\sqrt{n}}", r"\sqrt{16}", "2"),
        "t-statistic standard error",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[0].calculation",
        (r"\bar{X}", r"\sim", "1.5625"),
        "Normal sampling law",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.steps[1].calculation",
        (r"\operatorname{MSE}", "T_{2}", "5"),
        "MSE arithmetic",
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "worked_example.final_answer",
        (r"\hat{\mu}", r"\mathrm{MoM}", "2200"),
        "MoM estimator value",
    ),
    (
        "4.1.3-least-squares-cs1013.json",
        "worked_example.steps[0].calculation",
        (r"\bar{x}", r"\frac{10}{4}", "2.5"),
        "least-squares means board",
    ),
    (
        "4.2.8-residuals-cs1014.json",
        "worked_example.steps[0].calculation",
        (r"r_{P}", "2.5"),
        "Pearson residual value",
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
    for cmd in _CONTROL.findall(body):
        assert cmd in _KNOWN_COMMANDS, (
            f"unknown KaTeX command \\{cmd} at {where}: {body}"
        )
    # \frac must be followed by two brace groups.
    for match in re.finditer(r"\\frac(?![A-Za-z])", body):
        rest = body[match.end() :]
        assert rest.startswith("{"), f"\\frac missing numerator at {where}: {body}"
    for match in re.finditer(r"\\sqrt(?![A-Za-z])", body):
        rest = body[match.end() :].lstrip()
        assert rest.startswith("{") or rest.startswith("["), (
            f"\\sqrt missing argument at {where}: {body}"
        )


def test_wave1_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave1.WAVE1_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave1_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 1 packages is valid KaTeX source."""
    span_count = 0
    for fname in wave1.WAVE1_FILES:
        pkg = _load(fname)

        def walk(obj: object, path: str = "$") -> None:
            nonlocal span_count
            if isinstance(obj, dict):
                for key, value in obj.items():
                    walk(value, f"{path}.{key}")
            elif isinstance(obj, list):
                for index, value in enumerate(obj):
                    walk(value, f"{path}[{index}]")
            elif isinstance(obj, str) and "$" in obj:
                assert obj.count("$") % 2 == 0, f"unbalanced $ in {fname} {path}"
                for body in _spans(obj):
                    span_count += 1
                    _assert_valid_latex(body, where=f"{fname}:{path}")

        walk(pkg)
    assert span_count >= 200


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave1_sample_latex_matches_intended_meaning(
    package_file: str,
    field_path: str,
    needles: tuple[str, ...],
    label: str,
) -> None:
    pkg = _load(package_file)
    text = wave1.get_path(pkg, field_path)
    joined = " ".join(_spans(text)) if _spans(text) else text
    for needle in needles:
        assert needle in text or needle in joined, (
            f"{label}: expected {needle!r} in {package_file} {field_path}: {text}"
        )
    for body in _spans(text):
        _assert_valid_latex(body, where=f"{label}:{field_path}")


def test_wave1_scoring_matches_pre_migration_snapshot() -> None:
    """Scoring keys and verdicts are unchanged for every KC in the 12 packages."""
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
            pack, curriculum_identity="CS1:wave1", topic_id=pack.topic_code
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


def test_wave1_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["migrated"] == 2055
    assert checked["totals"]["needs_migration"] == 0
    assert live["totals"] == checked["totals"]

    original_wave1 = set(wave1.WAVE1_FILES)
    migrated = 0
    still_pending_review = 0
    manual_excluded = 0
    for row in live["packages"]:
        if row["package_file"] not in original_wave1:
            continue
        for item in row["items"]:
            if item["migration_status"] == "migrated":
                migrated += 1
                assert item["category"] == "already_compliant"
                assert "dollar_delimited" in item["signals"]
            if item["category"] == "needs_migration" and item["needs_manual_review"]:
                still_pending_review += 1
            if item["migration_status"] == "correctly_excluded":
                manual_excluded += 1
                assert item["category"] == "correctly_excluded"
                assert item["needs_manual_review"] is False
                assert item["reason_code"] == "manual_review_prose_exclusion"
    assert migrated == 321
    assert still_pending_review == 0
    assert manual_excluded == 21


# Locked Wave 1 leftover migrations (manual-review close-out).
_WAVE1_LEFTOVER_MIGRATIONS = (
    (
        "2.6.3-mean-var-sample-cs1009.json",
        "worked_example.steps[2].label",
        "Mean of $S^{2}$ and refuse Normal/t jump",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "mission.expected_benefit",
        "You will be able to form the t-statistic with its degrees of freedom when "
        r"$\sigma$ is unknown, and refuse using a Normal/z form with $S$.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $\frac{\bar{X} - \mu_{0}}{\mathrm{SE}}$ and $\mathrm{df}$.",
    ),
    (
        "2.6.5-t-statistic-cs1009.json",
        "worked_example.common_pitfall",
        r"Computing $z = \frac{105 - 100}{8/4} = 2.5$ and treating it as standard "
        r"Normal because the arithmetic matches $t$, or reaching for an $F$ "
        "statistic when the question is about a single mean.",
    ),
    (
        "3.2.5-ci-binomial-poisson-cs1011.json",
        "worked_example.given[1].note",
        r"policies with $\ge 1$ claim",
    ),
    (
        "2.5.1-clt-cs1008.json",
        "worked_example.steps[1].attempt_cue",
        r"Form $z = \frac{170 - 180}{10}$, then convert with $\Phi$.",
    ),
    (
        "2.5.1-clt-cs1008.json",
        "worked_example.steps[2].attempt_cue",
        r"State why using $\operatorname{sd} = 60$ for $\bar{X}$ is wrong.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.task_descriptions[0]",
        r"Sketch Normal sample → $\bar{X}$ / $S^{2}$ laws before CMP.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "reading_guidance.misconception_watch[0]",
        r"Watch for using $t$ when $\sigma$ is known / when today only asks "
        "Normal laws.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.title",
        r"Normal laws for $\bar{X}$ and for $\frac{(n-1)S^{2}}{\sigma^{2}}$",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.steps[1].explanation",
        r"Independently of $\bar{X}$, $\frac{(n-1)S^{2}}{\sigma^{2}}$ follows "
        r"$\chi^{2}$ with $n-1$ degrees of freedom.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "worked_example.common_pitfall",
        r"Writing $\bar{X} \sim \operatorname{Normal}(100, 25)$ without dividing "
        r"by $n$, or labelling $\frac{(n-1)S^{2}}{\sigma^{2}} \sim \chi^{2}_{n-1}$ "
        "as the t-statistic.",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Before uncovering, write $\operatorname{MSE} = "
        r"\operatorname{Var} + \operatorname{Bias}^{2}$ for each estimator.",
    ),
    (
        "3.1.4-comparison-mse-cs1010.json",
        "worked_example.common_pitfall",
        r"Comparing variances alone (9 vs 4) and declaring $T_{2}$ better without "
        r"adding $\operatorname{Bias}^{2}$, or refusing $T_{2}$ because "
        r"$\operatorname{Bias} \neq 0$ despite $\operatorname{MSE}(T_{2}) = 5 < 9$.",
    ),
    (
        "3.1.1-method-of-moments-cs1010.json",
        "knowledge_checks[1].common_mistake",
        r"Reporting the rate $\frac{1}{2200}$ when the question asks for the mean "
        r"$\mu$, or reporting the sum 11000 instead of the sample mean.",
    ),
)

# Locked Wave 1 leftover prose exclusions (byte-identical; not converted).
_WAVE1_LEFTOVER_EXCLUSIONS = (
    (
        "4.2.8-residuals-cs1014.json",
        "mission.mission_purpose",
        "Today's Mission exists to explain Pearson and deviance residuals and "
        "their use. Without pretending χ² / LRT acceptability tests (4.2.9) are "
        "finished.",
    ),
    (
        "4.2.8-residuals-cs1014.json",
        "reading_guidance.misconception_watch[1]",
        "Watch for jumping into formal χ²/LRT (4.2.9) as today's finish.",
    ),
    (
        "4.2.8-residuals-cs1014.json",
        "reading_guidance.stop_condition",
        "Through the CMP treatment of Syllabus 4.2.8 (stop before χ² / LRT "
        "acceptability tests 4.2.9)",
    ),
    (
        "4.2.8-residuals-cs1014.json",
        "reading_guidance.out_of_scope_today[0]",
        "χ² / LRT acceptability tests as primary (4.2.9)",
    ),
    (
        "4.2.8-residuals-cs1014.json",
        "reading_guidance.exit_line",
        "Open your CMP (IFoA CS1 Core Reading / CMP · 2026 syllabus alignment) at "
        "CMP · Syllabus 4.2.8 Pearson and deviance residuals. Kwalitec is the "
        "guide; the CMP is the authoritative material (do not treat this activity "
        "body as a substitute textbook. Hunt with the focus questions; watch the "
        "misconception list. Ignore items in out_of_scope_today. Stop when: "
        "Through the CMP treatment of Syllabus 4.2.8 (stop before χ² / LRT "
        "acceptability tests 4.2.9). Then close the CMP and return here) next "
        "in-app activity: Worked-example re-entry (CMP closed), then Knowledge "
        "Checks.",
    ),
    (
        "4.2.8-residuals-cs1003.json",
        "reading_guidance.out_of_scope_today[0]",
        "χ²/LRT primary (4.2.9)",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "mission.success_criteria[1]",
        "State the sampling result for sample variance / χ² form as CMP directs.",
    ),
    (
        "2.6.4-normal-sample-mean-var-cs1009.json",
        "reading_guidance.misconception_watch[1]",
        "Watch for skipping χ² / variance result the CMP requires.",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE1_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE1_LEFTOVER_MIGRATIONS],
)
def test_wave1_leftover_migrations_are_valid_katex(
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
    ("package_file", "field_path", "expected"),
    _WAVE1_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE1_LEFTOVER_EXCLUSIONS],
)
def test_wave1_leftover_exclusions_are_byte_identical(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text


def test_wave1_leftover_knowledge_check_scoring_unaffected() -> None:
    """Only KC field touched in leftovers is common_mistake; scoring keys unchanged."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    target = "3.1.1-method-of-moments-cs1010.json"
    by_id = {
        r["item_id"]: r for r in snapshot["items"] if r["package_file"] == target
    }
    assert by_id
    reset_educational_package_cache()
    loader = EducationalPackageLoader(
        root=REPO_ROOT / "app/curriculum/data/educational_packages"
    )
    pack = next(p for p in loader.all_approved() if Path(p.source_path).name == target)
    substance = substance_from_package(
        pack, curriculum_identity="CS1:wave1", topic_id=pack.topic_code
    )
    practice = [
        a for a in substance.activities if a.stage is EducationalStage.PRACTICE
    ]
    seen: set[str] = set()
    for act in practice:
        item = act.scoreable
        assert item is not None
        expected = by_id[item.item_id]
        seen.add(item.item_id)
        assert item.response_type == expected["response_type"]
        assert item.answer_key.correct_choice_id == expected["correct_choice_id"]
        assert list(item.answer_key.accepted) == expected["accepted_keywords"]
        exp_tol = expected["numeric_tolerance"]
        if exp_tol is None:
            assert item.answer_key.numeric_tolerance is None
        else:
            assert item.answer_key.numeric_tolerance == pytest.approx(exp_tol)
        choice_ids = [c[0] if not isinstance(c, str) else c for c in item.choices]
        assert choice_ids == expected["choice_ids"]
        for probe in expected["verdicts"]:
            result = score_practice_response(item, probe["response"])
            assert result.scored is probe["scored"]
            assert result.correct is probe["correct"]
            assert result.matched_key == probe["matched_key"]
    assert seen == set(by_id)

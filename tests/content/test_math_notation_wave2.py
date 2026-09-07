"""Wave 2 mathematical notation migration: KaTeX validity, scoring, ledger."""

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
import math_notation_wave2 as wave2  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave2_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Wave 1 + Wave 2 authored math.
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
        "rightarrow",
        "xrightarrow",
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
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Representative (package, path, must-contain) meaning checks across categories.
_MEANING_SAMPLES = (
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[1].choices[0].label",
        (r"\bar{x}", r"t_{15, 1-\alpha/2}", r"s/\sqrt{n}", r"\chi^{2}"),
        "t / chi-square dual CI formula",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[0].calculation",
        (r"(-2)^{2}/20", "25/20"),
        "Pearson GOF sum of squares",
    ),
    (
        "cp-3.1.1-estimators-cs1016.json",
        "worked_example.steps[0].calculation",
        (r"\hat{\lambda}_{\mathrm{MoM}}", r"\bar{x}"),
        "MoM estimator equation",
    ),
    (
        "3.1.6-bootstrap-estimator-cs1010.json",
        "worked_example.steps[2].calculation",
        (r"\widehat{\mathrm{SE}}_{\mathrm{boot}}", r"\sqrt{370/5}", r"\sqrt{74}"),
        "bootstrap SE root",
    ),
    (
        "5.1.8-empirical-bayes-cs1015.json",
        "worked_example.steps[1].calculation",
        (r"(1/3)", "700", "1700/3"),
        "EB credibility premium arithmetic",
    ),
    (
        "5.1.8-empirical-bayes-cs1003.json",
        "worked_example.steps[1].calculation",
        ("1200", "900", "1000"),
        "EB premium blend",
    ),
    (
        "cp-2.5.1-clt-cs1016.json",
        "worked_example.steps[0].calculation",
        (r"\frac{\sigma}{\sqrt{n}}", r"\frac{300}{\sqrt{36}}", "50"),
        "CLT sampling sd",
    ),
    (
        "3.1.3-efficiency-bias-consistency-mse-cs1010.json",
        "worked_example.steps[1].calculation",
        (r"\operatorname{MSE}(A)", r"\operatorname{MSE}(B)", "20"),
        "MSE comparison board",
    ),
    (
        "3.1.5-asymptotic-mle-cs1010.json",
        "worked_example.steps[0].calculation",
        (r"\widehat{\mathrm{SE}}", r"\sqrt{64}", "0.03125"),
        "asymptotic SE for MLE",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "worked_example.steps[2].calculation",
        (r"\hat{Y}_{m}", "0.6", "6.2"),
        "multiple regression fitted value",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.steps[1].result",
        (r"\chi^{2}", "100/21", "4.762"),
        "contingency chi-square",
    ),
    (
        "cp-revision-spine-memory-cs1016.json",
        "worked_example.steps[1].calculation",
        (r"\operatorname{Normal}(\theta, 9/n)",),
        "CLT Normal law for T",
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
    for match in re.finditer(r"\\frac(?![A-Za-z])", body):
        rest = body[match.end() :]
        assert rest.startswith("{"), f"\\frac missing numerator at {where}: {body}"
    for match in re.finditer(r"\\sqrt(?![A-Za-z])", body):
        rest = body[match.end() :].lstrip()
        assert rest.startswith("{") or rest.startswith("["), (
            f"\\sqrt missing argument at {where}: {body}"
        )


def test_wave2_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave2.WAVE2_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave2_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 2 packages is valid KaTeX source."""
    span_count = 0
    for fname in wave2.WAVE2_FILES:
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
    assert span_count >= 150


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave2_sample_latex_matches_intended_meaning(
    package_file: str,
    field_path: str,
    needles: tuple[str, ...],
    label: str,
) -> None:
    from math_notation_wave1 import get_path

    pkg = _load(package_file)
    text = get_path(pkg, field_path)
    joined = " ".join(_spans(text)) if _spans(text) else text
    for needle in needles:
        assert needle in text or needle in joined, (
            f"{label}: expected {needle!r} in {package_file} {field_path}: {text}"
        )
    for body in _spans(text):
        _assert_valid_latex(body, where=f"{label}:{field_path}")


def test_wave2_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave2", topic_id=pack.topic_code
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


def test_wave2_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 434
    assert checked["totals"]["migrated"] == 1478
    assert checked["totals"]["needs_migration"] == 434
    assert live["totals"] == checked["totals"]

    wave2_files = set(wave2.WAVE2_FILES)
    migrated = 0
    still_pending_review = 0
    for row in live["packages"]:
        if row["package_file"] not in wave2_files:
            continue
        for item in row["items"]:
            if item["migration_status"] == "migrated":
                migrated += 1
                assert item["category"] == "already_compliant"
                assert "dollar_delimited" in item["signals"]
            if item["category"] == "needs_migration" and item["needs_manual_review"]:
                still_pending_review += 1
    assert migrated == 222
    assert still_pending_review == 0


def test_wave2_packages_disjoint_from_wave1() -> None:
    import math_notation_wave1 as wave1

    assert set(wave2.WAVE2_FILES).isdisjoint(set(wave1.WAVE1_FILES))


# Locked Wave 2 leftover migrations (manual-review close-out).
_WAVE2_LEFTOVER_MIGRATIONS = (
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "knowledge_checks[1].explanation",
        r"With $\sigma$ unknown, the mean CI uses $t_{n-1}$. The variance CI "
        r"inverts the chi-square pivot for $\frac{(n-1)s^{2}}{\sigma^{2}}$. "
        "Mean-only or Normal-SE-for-variance shortcuts fail the dual requirement.",
    ),
    (
        "3.2.4-ci-normal-mean-variance-cs1011.json",
        "worked_example.common_pitfall",
        r"Using $z = 1.96$ instead of $t_{15,0.975} = 2.131$ when $\sigma$ is "
        "estimated from the sample, which understates the half-width "
        "(2.94 vs 3.1965).",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute each $(O_{i} - 20)^{2}/20$.",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[0].explanation",
        r"Each category contributes $(O - E)^{2}/E$ to the Pearson statistic.",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.steps[2].explanation",
        r"Reject $H_{0}$ for large $\chi^{2}$; here $2.9 < 9.488$.",
    ),
    (
        "3.3.4-chi-square-gof-cs1012.json",
        "worked_example.common_pitfall",
        r"Using $\mathrm{df} = 5$ (forgetting $-1$ for the multinomial "
        r"constraint) or comparing $\chi^{2}$ to a Normal $z$ critical value.",
    ),
    (
        "5.1.8-empirical-bayes-cs1015.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $\hat{Z} = \frac{n}{n+\hat{k}}$.",
    ),
    (
        "5.1.8-empirical-bayes-cs1015.json",
        "worked_example.common_pitfall",
        r"Using the fully Bayesian $k = 3$ from a different exercise instead of "
        r"the collective estimate $\hat{k} = 10$, which would incorrectly give "
        r"$Z = \frac{5}{8}$ and a different premium.",
    ),
    (
        "5.1.8-empirical-bayes-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $\hat{Z} = \frac{n}{n+\hat{k}}$.",
    ),
    (
        "cp-2.5.1-clt-cs1016.json",
        "worked_example.steps[1].attempt_cue",
        r"Form $z = \frac{1150 - 1200}{50}$, then convert with $\Phi$.",
    ),
    (
        "cp-2.5.1-clt-cs1016.json",
        "worked_example.steps[2].attempt_cue",
        r"State why using $\operatorname{sd} = 300$ for $\bar{X}$ is wrong.",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Substitute $x_{1} = 5$ into $\hat{Y}_{s}$.",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        r"Substitute $x_{1} = 5$ and $x_{2} = 3$ into $\hat{Y}_{m}$.",
    ),
    (
        "4.1.2-simple-multiple-cs1003.json",
        "worked_example.common_pitfall",
        r"Calling $\hat{Y}_{m}$ 'simple' because it is still linear in the "
        r"parameters, or assuming the two fitted values must coincide at the "
        r"same $(x_{1}, x_{2})$.",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.steps[1].attempt_cue",
        r"Sum $(O - E)^{2}/E$ over the four cells.",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.steps[2].explanation",
        r"Reject independence when $\chi^{2}$ exceeds the $\mathrm{df} = 1$ "
        "critical value.",
    ),
    (
        "3.3.5-contingency-independence-cs1012.json",
        "worked_example.common_pitfall",
        r"Using $E_{ij} = \frac{n}{4} = 25$ (ignoring unequal margins) or "
        r"forgetting to square $(O - E)$ before dividing by $E$.",
    ),
    (
        "cp-revision-spine-memory-cs1016.json",
        "worked_example.steps[0].explanation",
        r"Solving $\text{sample mean} = m(\theta)$ defines an estimator. Its "
        "sampling distribution describes the values of that estimator over "
        "repeated samples.",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE2_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE2_LEFTOVER_MIGRATIONS],
)
def test_wave2_leftover_migrations_are_valid_katex(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    from math_notation_wave1 import get_path

    text = get_path(_load(package_file), field_path)
    assert text == expected
    assert text.count("$") % 2 == 0
    assert _spans(text), (
        f"expected dollar-delimited math in {package_file} {field_path}"
    )
    for body in _spans(text):
        _assert_valid_latex(body, where=f"{package_file}:{field_path}")


def test_wave2_leftover_knowledge_check_scoring_unaffected() -> None:
    """Only KC field touched in leftovers is explanation; scoring keys unchanged."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    target = "3.2.4-ci-normal-mean-variance-cs1011.json"
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
        pack, curriculum_identity="CS1:wave2", topic_id=pack.topic_code
    )
    practice = [
        a for a in substance.activities if a.stage is EducationalStage.PRACTICE
    ]
    assert practice
    for act in practice:
        item = act.scoreable
        assert item is not None
        expected = by_id[item.item_id]
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

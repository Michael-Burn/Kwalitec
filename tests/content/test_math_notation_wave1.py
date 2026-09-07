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
    assert checked["totals"]["remaining_backlog"] == 1636
    assert checked["totals"]["migrated"] == 292
    assert checked["totals"]["needs_migration"] == 1636
    assert live["totals"] == checked["totals"]

    original_wave1 = set(wave1.WAVE1_FILES)
    migrated = 0
    still_pending_review = 0
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
    assert migrated == 292
    assert still_pending_review == 23

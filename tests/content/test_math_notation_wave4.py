"""Wave 4 mathematical notation migration: KaTeX validity, scoring, ledger."""

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
import math_notation_wave2 as wave2  # noqa: E402
import math_notation_wave3 as wave3  # noqa: E402
import math_notation_wave4 as wave4  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave4_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–4 authored math.
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
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Representative (package, path, must-contain) meaning checks across categories.
_MEANING_SAMPLES = (
    (
        "3.2.2-prediction-interval-cs1011.json",
        "worked_example.steps[0].calculation",
        (r"\sqrt{1 + 1/25}", r"\approx", "40.792"),
        "prediction SE compound root",
    ),
    (
        "3.3.2-basic-tests-cs1012.json",
        "worked_example.steps[0].calculation",
        (r"\frac{\sigma}{\sqrt{n}}", "520", "2"),
        "one-sample z statistic",
    ),
    (
        "4.1.4-software-inference-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"z = -8 / 2.5", "-3.2"),
        "Wald z for slope",
    ),
    (
        "4.2.10-fit-interpret-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"e^{-0.15}", r"\approx", "0.8607"),
        "log-link multiplicative effect",
    ),
    (
        "4.1.4-software-fit-cs1013.json",
        "worked_example.attempt_before_reveal",
        (r"\hat{\beta}_{1}", "SE_mean", "SE_pred"),
        "software Wald attempt cue",
    ),
    (
        "4.2.9-goodness-tests-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"X^{2}", "(15-12)", "1.5"),
        "Pearson X-squared GOF",
    ),
    (
        "4.2.10-fit-interpret-cs1014.json",
        "worked_example.steps[0].calculation",
        (r"e^{0.2}", r"\approx", "1.2214"),
        "urban multiplicative effect",
    ),
    (
        "5.1.3-posterior-simple-cs1015.json",
        "worked_example.problem_statement",
        (r"\mathrm{Gamma}", r"\lambda", r"\sum x_{i}"),
        "Exponential-Gamma posterior setup",
    ),
    (
        "2.5.2-simulated-sample-normal-cs1008.json",
        "worked_example.problem_statement",
        (r"\theta = 400", r"N(400, 400^{2})", r"\bar{X}"),
        "simulated Normal overlay vs Exponential",
    ),
    (
        "4.2.9-goodness-tests-cs1014.json",
        "worked_example.steps[0].calculation",
        (r"\frac{4}{10}", "0.4"),
        "Pearson contributions sibling package",
    ),
    (
        "revision-confidence-intervals-cs1011.json",
        "worked_example.attempt_before_reveal",
        (r"\bar{X}", r"\sigma/\sqrt{n}"),
        "z-interval attempt before reveal",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1003.json",
        "worked_example.steps[0].calculation",
        ("Z = 5/(5+5)", "1000"),
        "Bayesian credibility premium",
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


def test_wave4_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave4.WAVE4_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave4_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 4 packages is valid KaTeX source."""
    span_count = 0
    for fname in wave4.WAVE4_FILES:
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
def test_wave4_sample_latex_matches_intended_meaning(
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


def test_wave4_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave4", topic_id=pack.topic_code
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


def test_wave4_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 1074
    assert checked["totals"]["migrated"] == 844
    assert checked["totals"]["needs_migration"] == 1074
    assert live["totals"] == checked["totals"]

    wave4_files = set(wave4.WAVE4_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    for row in live["packages"]:
        if row["package_file"] not in wave4_files:
            continue
        for item in row["items"]:
            if item["migration_status"] == "migrated":
                migrated += 1
                assert item["category"] == "already_compliant"
                assert "dollar_delimited" in item["signals"]
            if item["category"] == "needs_migration" and item["needs_manual_review"]:
                still_pending_review += 1
            if (
                item["category"] == "needs_migration"
                and not item["needs_manual_review"]
            ):
                confident_backlog += 1
    assert migrated == 147
    assert still_pending_review == 19
    assert confident_backlog == 0


def test_wave4_packages_disjoint_from_prior_waves() -> None:
    assert set(wave4.WAVE4_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave4.WAVE4_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave4.WAVE4_FILES).isdisjoint(set(wave3.WAVE3_FILES))


def test_wave4_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 4 packages match the pre-migration snapshot."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    for rec in snapshot["items"]:
        pkg = _load(rec["package_file"])
        kc = next(
            k
            for k in pkg["knowledge_checks"]
            if k.get("item_id") == rec["item_id"]
        )
        key = kc.get("answer_key") or {}
        live_cid = key.get("correct_choice_id", kc.get("correct_choice_id"))
        if live_cid is None:
            live_cid = ""
        assert live_cid == (rec["correct_choice_id"] or "")
        live_accepted = list(
            key.get("accepted_keywords")
            or kc.get("accepted_keywords")
            or []
        )
        assert live_accepted == rec["accepted_keywords"]
        live_tol = key.get("numeric_tolerance", kc.get("numeric_tolerance"))
        assert live_tol == rec["numeric_tolerance"]
        choice_ids = [c["id"] for c in kc.get("choices") or []]
        assert choice_ids == rec["choice_ids"]

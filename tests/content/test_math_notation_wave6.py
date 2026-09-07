"""Wave 6 mathematical notation migration: KaTeX validity, scoring, ledger."""

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
import math_notation_wave5 as wave5  # noqa: E402
import math_notation_wave6 as wave6  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave6_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–6 authored math.
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
        "mid",
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Representative (package, path, must-contain) meaning checks across all 12 packages.
_MEANING_SAMPLES = (
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.final_answer",
        (r"\eta(10)", r"\mu = e^{2}", r"\approx"),
        "linear predictor eta and mean",
    ),
    (
        "2.2.1-marginal-conditional-cs1005.json",
        "knowledge_checks[1].model_answer",
        (r"P(X=1)", r"P(Y=1|X=1)", r"\approx"),
        "marginal then conditional",
    ),
    (
        "revision-joint-distributions-cs1005.json",
        "worked_example.final_answer",
        (r"p_{X}(x)p_{Y}(y)", r"\operatorname{Var}(aX+bY)", r"\operatorname{Cov}"),
        "independence and linear combination variance",
    ),
    (
        "2.4.2-moment-via-gf-cs1007.json",
        "worked_example.final_answer",
        (r"E[X]", r"C'(0)", r"\operatorname{Var}(X)"),
        "CGF derivatives for moments",
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.problem_statement",
        (r"H_{0}", r"\alpha = 0.05", r"\Phi(2.1)"),
        "hypothesis test setup with Phi",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.final_answer",
        (r"\eta = -1.0", r"\mu \approx 0.3679"),
        "factor interaction fitted eta",
    ),
    (
        "cp-2.1.3-prob-quantiles-cs1016.json",
        "knowledge_checks[1].choices[0].label",
        (r"P(X > 2000)", r"e^{-2}", r"\ln(10)"),
        "exponential survival and quantile",
    ),
    (
        "5.1.1-bayes-theorem-cs1003.json",
        "worked_example.final_answer",
        (r"P(+)", r"P(Lapse|+)", r"\approx"),
        "Bayes evidence and posterior",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.final_answer",
        (r"\eta(8)", r"\mu = e^{1.38}"),
        "fleet mileage linear predictor",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.final_answer",
        (r"\theta = \ln\lambda", r"b(\theta)"),
        "exponential family natural parameter",
    ),
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "worked_example.final_answer",
        (r"P(X \leq 100)", r"\approx 0.3297"),
        "exponential CDF evaluation",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.problem_statement",
        (r"\bar{X}", r"Z\bar{X}", r"(1 - Z)\mu"),
        "credibility premium formula",
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


def test_wave6_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave6.WAVE6_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave6_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 6 packages is valid KaTeX source."""
    span_count = 0
    packages_with_spans = set()
    for fname in wave6.WAVE6_FILES:
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
                    packages_with_spans.add(fname)
                    _assert_valid_latex(body, where=f"{fname}:{path}")

        walk(pkg)
    assert span_count >= 300
    assert packages_with_spans == set(wave6.WAVE6_FILES)


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave6_sample_latex_matches_intended_meaning(
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


def test_wave6_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave6", topic_id=pack.topic_code
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
    assert len(seen) == 24


def test_wave6_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 478
    assert checked["totals"]["migrated"] == 1439
    assert checked["totals"]["needs_migration"] == 478
    assert live["totals"] == checked["totals"]

    wave6_files = set(wave6.WAVE6_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    for row in live["packages"]:
        if row["package_file"] not in wave6_files:
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
    assert migrated == 207
    assert still_pending_review == 44
    assert confident_backlog == 0


def test_wave6_packages_disjoint_from_prior_waves() -> None:
    assert set(wave6.WAVE6_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave6.WAVE6_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave6.WAVE6_FILES).isdisjoint(set(wave3.WAVE3_FILES))
    assert set(wave6.WAVE6_FILES).isdisjoint(set(wave4.WAVE4_FILES))
    assert set(wave6.WAVE6_FILES).isdisjoint(set(wave5.WAVE5_FILES))


def test_wave6_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 6 packages match the pre-migration snapshot."""
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

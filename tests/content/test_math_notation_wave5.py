"""Wave 5 mathematical notation migration: KaTeX validity, scoring, ledger."""

# Leftover exclusion strings are verbatim package text; line length is expected.
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
from app.presentation.session.math_markup import prepare_math_markup

REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))

import inventory_math_notation as inventory  # noqa: E402
import math_notation_wave1 as wave1  # noqa: E402
import math_notation_wave2 as wave2  # noqa: E402
import math_notation_wave3 as wave3  # noqa: E402
import math_notation_wave4 as wave4  # noqa: E402
import math_notation_wave5 as wave5  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave5_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–5 authored math.
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
        "revision-linear-models-cs1003.json",
        "worked_example.given[0].value",
        (r"X\beta", r"\varepsilon"),
        "OLS linear model board",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "worked_example.title",
        (r"E[X+2Y]",),
        "cov-corr joint expectation title",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "knowledge_checks[1].model_answer",
        (r"E[Y|X=1]", r"\approx", "0.571"),
        "conditional expectation model answer",
    ),
    (
        "2.3.2-mean-variance-conditioning-cs1006.json",
        "worked_example.attempt_before_reveal",
        (r"E[E[Y|X]]", r"\operatorname{Var}(Y)"),
        "tower law and total variance",
    ),
    (
        "cp-5.1.1-bayes-theorem-cs1016.json",
        "knowledge_checks[1].model_answer",
        (r"P(+)", r"P(D|+)", r"\approx"),
        "Bayes evidence and posterior",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "worked_example.problem_statement",
        (r"E[X]", r"\operatorname{Var}(X)", r"\operatorname{Cov}"),
        "linear combination moments setup",
    ),
    (
        "5.1.1-bayes-theorem-cs1015.json",
        "knowledge_checks[1].model_answer",
        (r"P(\mathrm{flag})", r"P(\mathrm{fraud}|"),
        "fraud flag Bayes model answer",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "worked_example.problem_statement",
        (r"\mathrm{Poisson}", r"M_{X}(t)", r"C_{X}(t)"),
        "Poisson MGF/CGF problem",
    ),
    (
        "cp-2.2.1-marginal-conditional-cs1016.json",
        "knowledge_checks[1].model_answer",
        (r"P(X=1)", r"P(Y=1|X=1)"),
        "marginal then conditional",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.problem_statement",
        (r"V(\mu)", r"\varphi", r"\mu^{2}/\alpha"),
        "GLM mean-variance families",
    ),
    (
        "revision-conditional-expectations-cs1006.json",
        "worked_example.attempt_before_reveal",
        (r"E[E[Y|X]]", r"\operatorname{Var}(E[Y|X])"),
        "revision tower and total variance",
    ),
    (
        "revision-generating-functions-cs1007.json",
        "worked_example.steps[0].explanation",
        (r"M_{X}(t)", r"E[\exp(tX)]", r"K_{X}(t)"),
        "MGF and CGF definitions",
    ),
)

# Locked Wave 5 leftover migrations (manual-review close-out).
_WAVE5_LEFTOVER_MIGRATIONS = (
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "worked_example.steps[2].attempt_cue",
        r"Apply linearity, then state why $\operatorname{Corr} \neq 0$ here does "
        "not finish an independence claim.",
    ),
    (
        "2.2.4-linear-combinations-cs1005.json",
        "worked_example.steps[1].explanation",
        r"Variance of a linear combination needs the covariance whenever "
        r"dependence is present. Here $a = 2$ and $b = -1$, so "
        r"$2ab\operatorname{Cov} = 2(2)(-1)(3) = -12$.",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "mission.mission_purpose",
        r"Today's Mission exists to obtain the moment and cumulant generating "
        r"functions of a random variable (so $M_{X}(t)$ and $K_{X}(t)$ (or CMP "
        "equivalents) are usable objects) without pretending moment-via-GF "
        "calculation is finished.",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "worked_example.steps[0].attempt_cue",
        r"Sum $e^{tx} e^{-\lambda} \lambda^{x} / x!$ and recognise the series.",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "worked_example.steps[0].explanation",
        r"For Poisson($\lambda$), $M_{X}(t) = \exp(\lambda(e^{t} - 1))$. With "
        r"$\lambda = 2$ this is $\exp(2(e^{t} - 1))$.",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "worked_example.steps[1].explanation",
        r"The CGF is $C_{X}(t) = \log M_{X}(t) = 2(e^{t} - 1)$.",
    ),
    (
        "2.4.1-mgf-cgf-cs1007.json",
        "worked_example.common_pitfall",
        r"Writing $M_{X}(t) = 2$ or $M_{X}(t) = e^{2t}$ because the mean is 2, "
        r"instead of $\exp(2(e^{t} - 1))$.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[0].label",
        r"$\mathrm{Poisson}(\lambda = 5)$",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[0].explanation",
        r"Poisson equates mean and variance; the variance function is "
        r"$V(\mu) = \mu$.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[1].explanation",
        r"Binomial mean is $np$ and variance is $np(1-p)$; here that yields "
        r"mean 3 and variance 2.1, with scale $\varphi = 1$.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[2].label",
        r"$\mathrm{Gamma}(\mu = 10, \alpha = 4)$",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[2].attempt_cue",
        r"Use $\operatorname{Var} = \mu^{2}/\alpha$ and identify "
        r"$V(\mu) = \mu^{2}$ with scale related to $1/\alpha$.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.steps[2].explanation",
        r"Gamma has variance function $V(\mu) = \mu^{2}$. With shape "
        r"$\alpha = 4$, $\operatorname{Var} = 100/4 = 25$.",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "worked_example.common_pitfall",
        r"Using $\operatorname{Var} = \mu$ for the Binomial or Gamma case, or "
        "forgetting that Poisson's mean-variance equality is a special "
        "property, not a universal GLM rule.",
    ),
    (
        "revision-generating-functions-cs1007.json",
        "worked_example.steps[1].attempt_cue",
        r"State $M_{X}'(0)$ and $M_{X}''(0)$.",
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


def test_wave5_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave5.WAVE5_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave5_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 5 packages is valid KaTeX source."""
    span_count = 0
    packages_with_spans = set()
    for fname in wave5.WAVE5_FILES:
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
    assert span_count >= 400
    assert packages_with_spans == set(wave5.WAVE5_FILES)


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave5_sample_latex_matches_intended_meaning(
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


def test_wave5_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave5", topic_id=pack.topic_code
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


def test_wave5_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 29
    assert checked["totals"]["migrated"] == 1871
    assert checked["totals"]["needs_migration"] == 29
    assert live["totals"] == checked["totals"]

    wave5_files = set(wave5.WAVE5_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    for row in live["packages"]:
        if row["package_file"] not in wave5_files:
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
    assert migrated == 370
    assert still_pending_review == 0
    assert confident_backlog == 0


def test_wave5_packages_disjoint_from_prior_waves() -> None:
    assert set(wave5.WAVE5_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave5.WAVE5_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave5.WAVE5_FILES).isdisjoint(set(wave3.WAVE3_FILES))
    assert set(wave5.WAVE5_FILES).isdisjoint(set(wave4.WAVE4_FILES))


def test_wave5_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 5 packages match the pre-migration snapshot."""
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


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE5_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE5_LEFTOVER_MIGRATIONS],
)
def test_wave5_leftover_migrations_are_valid_katex(
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


def test_wave5_leftover_partial_migrations_preserve_surrounding_prose() -> None:
    """Items 3, 9, and 14 typeset only the live formula; prose stays intact."""
    cases = (
        (
            "2.4.1-mgf-cgf-cs1007.json",
            "mission.mission_purpose",
            (
                "Today's Mission exists to obtain the moment and cumulant "
                "generating functions of a random variable (so ",
                " (or CMP equivalents) are usable objects) without pretending "
                "moment-via-GF calculation is finished.",
            ),
            (r"M_{X}(t)", r"K_{X}(t)"),
        ),
        (
            "4.2.2-mean-variance-cs1014.json",
            "worked_example.steps[0].explanation",
            (
                "Poisson equates mean and variance; the variance function is ",
                "",
            ),
            (r"V(\mu) = \mu",),
        ),
        (
            "4.2.2-mean-variance-cs1014.json",
            "worked_example.common_pitfall",
            (
                "Using ",
                " for the Binomial or Gamma case, or forgetting that Poisson's "
                "mean-variance equality is a special property, not a universal "
                "GLM rule.",
            ),
            (r"\operatorname{Var} = \mu",),
        ),
    )
    for package_file, field_path, prose_parts, needles in cases:
        text = wave1.get_path(_load(package_file), field_path)
        for part in prose_parts:
            if part:
                assert part in text, f"missing prose in {package_file} {field_path}"
        joined = " ".join(_spans(text))
        for needle in needles:
            assert needle in joined, (
                f"expected typeset {needle!r} in {package_file} {field_path}"
            )
        for body in _spans(text):
            _assert_valid_latex(body, where=f"partial:{package_file}:{field_path}")


def test_wave5_leftover_knowledge_check_scoring_unaffected() -> None:
    """No leftover fields were knowledge_checks; all Wave 5 KC scoring holds."""
    leftover_fields = {field for _, field, _ in _WAVE5_LEFTOVER_MIGRATIONS}
    assert not any(f.startswith("knowledge_checks") for f in leftover_fields)
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    reset_educational_package_cache()
    loader = EducationalPackageLoader(
        root=REPO_ROOT / "app/curriculum/data/educational_packages"
    )
    by_id = {(r["package_file"], r["item_id"]): r for r in snapshot["items"]}
    for fname in snapshot["packages"]:
        pack = next(
            p for p in loader.all_approved() if Path(p.source_path).name == fname
        )
        substance = substance_from_package(
            pack, curriculum_identity="CS1:wave5-left", topic_id=pack.topic_code
        )
        for act in substance.activities:
            if act.stage is not EducationalStage.PRACTICE or act.scoreable is None:
                continue
            item = act.scoreable
            expected = by_id[(fname, item.item_id)]
            assert item.answer_key.correct_choice_id == expected["correct_choice_id"]
            for probe in expected["verdicts"]:
                result = score_practice_response(item, probe["response"])
                assert result.scored is probe["scored"]
                assert result.correct is probe["correct"]
                assert result.matched_key == probe["matched_key"]

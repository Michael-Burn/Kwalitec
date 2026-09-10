"""Wave 8 mathematical notation migration: KaTeX validity, scoring, ledger."""

# Representative samples and leftovers use verbatim package text; line length is expected.
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
import math_notation_wave6 as wave6  # noqa: E402
import math_notation_wave7 as wave7  # noqa: E402
import math_notation_wave8 as wave8  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave8_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–8 authored math.
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

# Representative (package, path, must-contain) meaning checks across all 12 packages.
_MEANING_SAMPLES = (
    (
        "2.6.2-sampling-distribution-statistic-cs1009.json",
        "worked_example.final_answer",
        (r"\bar{X}", r"E[\bar{X}] = 80", r"\operatorname{Var}(\bar{X}) = 25"),
        "sampling distribution of sample mean",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.final_answer",
        (r"\bar{x}_{A}", r"H_{0}", r"\alpha = 0.05"),
        "permutation p-value decision",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.steps[0].calculation",
        (r"\ln(0.8)", r"\approx", r"0.4463"),
        "inverse transform exponential draw",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "worked_example.final_answer",
        (r"\theta", r"\mid \mathrm{data}", r"0.95"),
        "central credible interval probability",
    ),
    (
        "cp-3.2.1-ci-sample-cs1016.json",
        "worked_example.attempt_before_reveal",
        (r"\bar{x}", r"\sigma/\sqrt{n}", r"\sqrt{100} = 10"),
        "z CI formula before substitute",
    ),
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.steps[2].calculation",
        (r"\hat{\theta}^{*}_{(1)}", r"1900", r"2150"),
        "bootstrap percentile endpoints",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.steps[2].calculation",
        (r"P = (2/3)\times 850", r"800"),
        "Bayesian credibility premium",
    ),
    (
        "cr-2.1.1-discrete-cs1017.json",
        "worked_example.final_answer",
        (r"\lambda = 0.4", r"P(X = 0)", r"0.6703"),
        "Poisson rare-event family check",
    ),
    (
        "5.1.7-bayesian-credibility-cs1003.json",
        "worked_example.steps[1].calculation",
        (r"P = (2/3)\times 950", r"900"),
        "Bühlmann credibility premium",
    ),
    (
        "5.1.4-loss-estimators-cs1015.json",
        "worked_example.steps[0].calculation",
        (r"\delta_{\mathrm{SE}}", r"2.1"),
        "squared-error Bayes estimate",
    ),
    (
        "cp-3.3.1-hypothesis-testing-cs1016.json",
        "knowledge_checks[1].model_answer",
        (r"H_{0}", r"1-\beta"),
        "Type I/II and power vocabulary",
    ),
    (
        "cr-1.2.2-correlation-cs1017.json",
        "worked_example.final_answer",
        (r"\rho = -0.55", r"r = -0.28"),
        "Spearman preferred over Pearson",
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


def test_wave8_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave8.WAVE8_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave8_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 8 packages is valid KaTeX source."""
    span_count = 0
    packages_with_spans = set()
    for fname in wave8.WAVE8_FILES:
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
    assert span_count >= 150
    assert packages_with_spans == set(wave8.WAVE8_FILES)


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave8_sample_latex_matches_intended_meaning(
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


def test_wave8_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave8", topic_id=pack.topic_code
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


def test_wave8_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["migrated"] == 2043
    assert checked["totals"]["needs_migration"] == 0
    assert live["totals"] == checked["totals"]

    wave8_files = set(wave8.WAVE8_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    manual_excluded = 0
    for row in live["packages"]:
        if row["package_file"] not in wave8_files:
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
            if item["migration_status"] == "correctly_excluded":
                manual_excluded += 1
                assert item["category"] == "correctly_excluded"
                assert item["needs_manual_review"] is False
                assert item["reason_code"] == "manual_review_prose_exclusion"
    assert migrated == 148
    assert still_pending_review == 0
    assert confident_backlog == 0
    assert manual_excluded == 13


def test_wave8_packages_disjoint_from_prior_waves() -> None:
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave3.WAVE3_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave4.WAVE4_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave5.WAVE5_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave6.WAVE6_FILES))
    assert set(wave8.WAVE8_FILES).isdisjoint(set(wave7.WAVE7_FILES))


def test_wave8_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 8 packages match the pre-migration snapshot."""
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


# Locked Wave 8 leftover migrations (manual-review close-out).
_WAVE8_LEFTOVER_MIGRATIONS = (
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.given[3].note",
        r"permutations with $|\mathrm{diff}| \geq \text{observed}$",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Compute the observed $|\bar{x}_{A} - \bar{x}_{B}|$, then form $p = (\#\text{ extreme})/20$.",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.steps[2].label",
        r"Decision at $\alpha = 0.05$",
    ),
    (
        "3.3.3-permutation-tests-cs1012.json",
        "worked_example.steps[2].explanation",
        r"Do not reject $H_{0}$ when $p > \alpha$.",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.given[1].note",
        r"smallest y with $F(y) \geq U$",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Invert the Exponential CDF for (a); find the smallest support point with $F(y) \geq U$ for (b).",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.steps[0].explanation",
        r"For Exponential rate $\lambda$, $F(x) = 1 - e^{-\lambda x}$, so $x = -\ln(1-U)/\lambda$.",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.steps[1].attempt_cue",
        r"Find the smallest y with $F(y) \geq 0.55$.",
    ),
    (
        "2.1.5-inverse-transform-cs1004.json",
        "worked_example.steps[1].explanation",
        r"$F(1) = 0.3 < 0.55$, so $y = 1$ is too small. $F(2) = 0.8 \geq 0.55$, so the inverse-transform draw is $Y = 2$.",
    ),
    (
        "5.1.5-credible-intervals-cs1015.json",
        "knowledge_checks[1].explanation",
        r"$\mathrm{Normal}(0.10, 0.02^{2})$ gives equal-tailed interval $\approx (0.0608, 0.1392)$. Frequentist coverage language misstates credible intervals.",
    ),
    (
        "3.2.8-bootstrap-confidence-interval-cs1011.json",
        "worked_example.steps[2].attempt_cue",
        r"Take $\hat{\theta}^{*}_{(1)}$ and $\hat{\theta}^{*}_{(10)}$.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Confirm $k = 120/40$, then $Z = n/(n+k)$, then $P = Z\bar{X} + (1 - Z)\mu$.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.common_pitfall",
        r"Using $Z = k/(n+k) = 1/3$ (the weight on $\mu$) as if it were the credibility factor on $\bar{X}$, which swaps the blend to £750.",
    ),
    (
        "cr-2.1.1-discrete-cs1017.json",
        "worked_example.steps[1].attempt_cue",
        r"For Poisson($\lambda = 0.4$), evaluate $e^{-\lambda}$.",
    ),
    (
        "5.1.4-loss-estimators-cs1015.json",
        "worked_example.steps[1].attempt_cue",
        r"Find the smallest $\theta$ with cumulative posterior probability $\geq 0.5$.",
    ),
    (
        "cp-3.3.1-hypothesis-testing-cs1016.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Recall Type I = reject $H_{0}$ when $H_{0}$ true; Type II = fail to reject $H_{0}$ when $H_{0}$ false, with $H_{0}$: clean.",
    ),
    (
        "cp-3.3.1-hypothesis-testing-cs1016.json",
        "worked_example.steps[2].attempt_cue",
        r"$\operatorname{Power} = 1 - \text{Type II rate}$.",
    ),
    (
        "cr-1.2.2-correlation-cs1017.json",
        "worked_example.common_pitfall",
        r"Defaulting to Pearson because it is the familiar default, or treating Spearman $\rho = -0.55$ as proof that more years licensed causes lower claim frequency.",
    ),
)

# Locked Wave 8 leftover prose exclusions (byte-identical; not converted).
_WAVE8_LEFTOVER_EXCLUSIONS = (
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "mission.concept_focus",
        "Bayesian credibility with known structural/prior parameters → Z and μ → credibility premium.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1015.json",
        "worked_example.steps[0].explanation",
        "The Bayesian approach supplies structural parameters (including μ and k) from an explicit prior/process model.",
    ),
    (
        "5.1.7-bayesian-credibility-cs1003.json",
        "mission.concept_focus",
        "Bayesian credibility with known structural/prior parameters → Z and μ → credibility premium.",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE8_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE8_LEFTOVER_MIGRATIONS],
)
def test_wave8_leftover_migrations_are_valid_katex(
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
    _WAVE8_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE8_LEFTOVER_EXCLUSIONS],
)
def test_wave8_leftover_exclusions_are_byte_identical(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text


def test_wave8_leftover_partial_migrations_preserve_surrounding_prose() -> None:
    """Partial leftovers typeset only the live math object; framing prose stays."""
    cases = (
        (
            "3.3.3-permutation-tests-cs1012.json",
            "worked_example.given[3].note",
            ("permutations with ",),
            (r"\mathrm{diff}", r"\geq \text{observed}"),
        ),
        (
            "3.3.3-permutation-tests-cs1012.json",
            "worked_example.steps[2].label",
            ("Decision at ",),
            (r"\alpha = 0.05",),
        ),
        (
            "2.1.5-inverse-transform-cs1004.json",
            "worked_example.given[1].note",
            ("smallest y with ",),
            (r"F(y) \geq U",),
        ),
        (
            "2.1.5-inverse-transform-cs1004.json",
            "worked_example.attempt_before_reveal",
            (
                "CMP closed. Invert the Exponential CDF for (a); find the smallest support point with ",
                " for (b).",
            ),
            (r"F(y) \geq U",),
        ),
        (
            "2.1.5-inverse-transform-cs1004.json",
            "worked_example.steps[1].attempt_cue",
            ("Find the smallest y with ",),
            (r"F(y) \geq 0.55",),
        ),
        (
            "5.1.5-credible-intervals-cs1015.json",
            "knowledge_checks[1].explanation",
            (
                " gives equal-tailed interval ",
                ". Frequentist coverage language misstates credible intervals.",
            ),
            (r"\mathrm{Normal}(0.10, 0.02^{2})", r"\approx (0.0608, 0.1392)"),
        ),
        (
            "5.1.7-bayesian-credibility-cs1015.json",
            "worked_example.common_pitfall",
            (
                "Using ",
                " (the weight on ",
                ") as if it were the credibility factor on ",
                ", which swaps the blend to £750.",
            ),
            (r"Z = k/(n+k) = 1/3", r"\mu", r"\bar{X}"),
        ),
        (
            "5.1.4-loss-estimators-cs1015.json",
            "worked_example.steps[1].attempt_cue",
            ("Find the smallest ", " with cumulative posterior probability ",),
            (r"\theta", r"\geq 0.5"),
        ),
        (
            "cp-3.3.1-hypothesis-testing-cs1016.json",
            "worked_example.attempt_before_reveal",
            (
                "CMP closed. Recall Type I = reject ",
                " when ",
                " true; Type II = fail to reject ",
                " when ",
                " false, with ",
                ": clean.",
            ),
            (r"H_{0}",),
        ),
        (
            "cr-1.2.2-correlation-cs1017.json",
            "worked_example.common_pitfall",
            (
                "Defaulting to Pearson because it is the familiar default, or treating Spearman ",
                " as proof that more years licensed causes lower claim frequency.",
            ),
            (r"\rho = -0.55",),
        ),
    )
    for package_file, field_path, prose_parts, needles in cases:
        text = wave1.get_path(_load(package_file), field_path)
        for part in prose_parts:
            assert part in text, f"missing prose in {package_file} {field_path}"
        joined = " ".join(_spans(text))
        for needle in needles:
            assert needle in joined, (
                f"expected typeset {needle!r} in {package_file} {field_path}"
            )
        for body in _spans(text):
            _assert_valid_latex(body, where=f"partial:{package_file}:{field_path}")

    # Items 18–20: mixed English/symbol definitions must not force whole sentences
    # into a single raw LaTeX blob (Power/Type I follow MSE-style operatorname).
    power = wave1.get_path(
        _load("cp-3.3.1-hypothesis-testing-cs1016.json"),
        "worked_example.steps[2].attempt_cue",
    )
    assert power == r"$\operatorname{Power} = 1 - \text{Type II rate}$."
    assert "Recall Type I = reject" in wave1.get_path(
        _load("cp-3.3.1-hypothesis-testing-cs1016.json"),
        "worked_example.attempt_before_reveal",
    )
    assert "cumulative posterior probability" in wave1.get_path(
        _load("5.1.4-loss-estimators-cs1015.json"),
        "worked_example.steps[1].attempt_cue",
    )


def test_wave8_leftover_knowledge_check_scoring_unaffected() -> None:
    """Leftover KC edit is explanation only; scoring keys and verdicts hold."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    targets = ("5.1.5-credible-intervals-cs1015.json",)
    by_id = {
        (r["package_file"], r["item_id"]): r
        for r in snapshot["items"]
        if r["package_file"] in targets
    }
    assert by_id
    reset_educational_package_cache()
    loader = EducationalPackageLoader(
        root=REPO_ROOT / "app/curriculum/data/educational_packages"
    )
    seen: set[tuple[str, str]] = set()
    for fname in targets:
        pack = next(
            p for p in loader.all_approved() if Path(p.source_path).name == fname
        )
        substance = substance_from_package(
            pack, curriculum_identity="CS1:wave8-left", topic_id=pack.topic_code
        )
        practice = [
            a for a in substance.activities if a.stage is EducationalStage.PRACTICE
        ]
        for act in practice:
            item = act.scoreable
            assert item is not None
            key = (fname, item.item_id)
            expected = by_id[key]
            seen.add(key)
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


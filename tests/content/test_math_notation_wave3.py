"""Wave 3 mathematical notation migration: KaTeX validity, scoring, ledger."""

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

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave3_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–3 authored math.
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
        "4.2.6-deviance-estimation-cs1014.json",
        "worked_example.steps[0].calculation",
        (r"\ln(5/4)", r"\approx", "0.2314"),
        "Poisson deviance contribution",
    ),
    (
        "3.2.7-ci-paired-means-cs1011.json",
        "worked_example.steps[0].result",
        (r"\bar{d}", "8"),
        "paired mean difference",
    ),
    (
        "4.2.6-deviance-estimation-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"\ln(\frac{8}{5})", r"\approx", "1.5201"),
        "Poisson deviance sibling package",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "worked_example.final_answer",
        (r"\theta", "0.4004", "0.4396"),
        "sampling-distribution CI for theta",
    ),
    (
        "4.1.2-simple-multiple-cs1013.json",
        "worked_example.steps[2].calculation",
        (r"\hat{Y}_m", "0.4", "4.6"),
        "multiple fitted value",
    ),
    (
        "5.1.3-posterior-simple-cs1003.json",
        "worked_example.final_answer",
        ("Gamma", "12/7", "1.7143"),
        "Gamma-Poisson posterior mean",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[1].calculation",
        (r"\hat{Z}", "0.25", "787.5"),
        "EB credibility premium",
    ),
    (
        "revision-sampling-distributions-cs1009.json",
        "worked_example.steps[1].calculation",
        (r"\bar{X}", r"\sqrt{n}", r"t_{n-1}"),
        "t pivot for unknown variance",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.steps[0].calculation",
        (r"\sum", r"\hat{y}_i"),
        "OLS residual sum of squares",
    ),
    (
        "revision-central-limit-theorem-cs1008.json",
        "worked_example.steps[0].calculation",
        (r"\sqrt{n}", r"\xrightarrow{d}", r"N(0,1)"),
        "CLT convergence in distribution",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"V(\mu)", r"\mu", r"\phi"),
        "Poisson mean-variance structure",
    ),
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "worked_example.steps[0].result",
        (r"\bar{x}_A", r"\bar{x}_B", "600"),
        "two-sample mean difference",
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


def test_wave3_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave3.WAVE3_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave3_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 3 packages is valid KaTeX source."""
    span_count = 0
    for fname in wave3.WAVE3_FILES:
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
def test_wave3_sample_latex_matches_intended_meaning(
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


def test_wave3_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave3", topic_id=pack.topic_code
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


def test_wave3_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 1055
    assert checked["totals"]["migrated"] == 862
    assert checked["totals"]["needs_migration"] == 1055
    assert live["totals"] == checked["totals"]

    wave3_files = set(wave3.WAVE3_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    manual_excluded = 0
    for row in live["packages"]:
        if row["package_file"] not in wave3_files:
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
    assert migrated == 168
    assert still_pending_review == 0
    assert confident_backlog == 0
    assert manual_excluded == 2


def test_wave3_packages_disjoint_from_wave1_and_wave2() -> None:
    assert set(wave3.WAVE3_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave3.WAVE3_FILES).isdisjoint(set(wave2.WAVE2_FILES))


# Locked Wave 3 leftover migrations (manual-review close-out).
_WAVE3_LEFTOVER_MIGRATIONS = (
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[0].label",
        r"$\mathrm{Poisson}(\lambda = 3)$",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[0].explanation",
        r"For Poisson, mean equals variance and the variance function is "
        r"$V(\mu) = \mu$ with $\phi = 1$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[2].label",
        r"$\mathrm{Gamma}(\mu = 8, \alpha = 2)$",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[2].attempt_cue",
        r"Use $\operatorname{Var} = \mu^{2}/\alpha$ and $V(\mu) = \mu^{2}$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.steps[2].explanation",
        r"Gamma has variance function $V(\mu) = \mu^{2}$; with shape $\alpha$ "
        r"the scale relates as $\operatorname{Var} = \mu^{2}/\alpha$.",
    ),
    (
        "4.2.2-mean-variance-cs1003.json",
        "worked_example.common_pitfall",
        r"Using $V(\mu) = \mu$ for Gamma, or forgetting the $(1 - p)$ factor "
        "in the Binomial variance.",
    ),
    (
        "4.2.6-deviance-estimation-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $D/\phi$.",
    ),
    (
        "4.2.6-deviance-estimation-cs1003.json",
        "worked_example.steps[1].explanation",
        r"With $\phi = 1$ the scaled deviance equals the total deviance.",
    ),
    (
        "4.2.6-deviance-estimation-cs1003.json",
        "worked_example.common_pitfall",
        r"Omitting the factor of 2 in the deviance contribution, or treating "
        r"$D/\phi$ as something other than scaled deviance when $\phi = 1$.",
    ),
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "knowledge_checks[1].common_mistake",
        r"Applying independent two-sample formulas to paired rows (or the "
        r"reverse) because $n_{1} = n_{2}$.",
    ),
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $\bar{x}_{A} - \bar{x}_{B}$.",
    ),
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "worked_example.steps[0].explanation",
        r"The natural centre for $\mu_{A} - \mu_{B}$ is the difference of "
        "sample means.",
    ),
    (
        "4.1.2-simple-multiple-cs1013.json",
        "worked_example.steps[1].attempt_cue",
        r"Substitute $x_{1} = 4$ into $\hat{Y}_{s}$.",
    ),
    (
        "4.1.2-simple-multiple-cs1013.json",
        "worked_example.steps[2].attempt_cue",
        r"Substitute $x_{1} = 4$ and $x_{2} = 5$ into $\hat{Y}_{m}$.",
    ),
    (
        "4.1.2-simple-multiple-cs1013.json",
        "worked_example.common_pitfall",
        r"Calling $\hat{Y}_{m}$ 'simple' because it is still linear in the "
        r"parameters, or assuming the two fitted values must coincide at the "
        r"same $(x_{1}, x_{2})$.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[0].attempt_cue",
        r"$Z = \frac{4}{4+6}$; $P = Z\times 900 + (1-Z)\times 700$.",
    ),
    (
        "5.1.9-bayes-vs-eb-cs1015.json",
        "worked_example.steps[1].attempt_cue",
        r"$\hat{Z} = \frac{4}{4+12}$; "
        r"$P = \hat{Z}\times 900 + (1-\hat{Z})\times 750$.",
    ),
    (
        "4.2.6-deviance-estimation-cs1014.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $D/\phi$.",
    ),
    (
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
        "knowledge_checks[1].explanation",
        r"From $\chi^{2}_{L} < 2n \bar{X} / \theta < \chi^{2}_{U}$, taking "
        r"reciprocals (and reversing inequalities) yields bounds "
        r"$2n \bar{X} / \chi^{2}_{U}$ and $2n \bar{X} / \chi^{2}_{L}$. The "
        "given pivot must be used; Normal-mean cookbooks are not a substitute.",
    ),
    (
        "3.2.7-ci-paired-means-cs1011.json",
        "worked_example.steps[0].explanation",
        r"Paired data are analysed through the differences $d_{i}$.",
    ),
    (
        "5.1.3-posterior-simple-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $\alpha'/\beta'$.",
    ),
    (
        "revision-linear-regression-cs1013.json",
        "worked_example.steps[0].explanation",
        r"OLS chooses coefficients that minimise the sum over $i$ of "
        r"$(y_{i} - \hat{y}_{i})^{2}$.",
    ),
)

# Locked Wave 3 leftover prose exclusions (byte-identical; not converted).
_WAVE3_LEFTOVER_EXCLUSIONS = (
    (
        "4.2.6-deviance-estimation-cs1003.json",
        "mission.prior_bridge",
        "Yesterday η forms (4.2.5). Today estimation/deviance language.",
    ),
    (
        "4.2.6-deviance-estimation-cs1014.json",
        "mission.why_now",
        "4.2.6 is contiguous after η. Without deviance/estimation, model "
        "choice and diagnostics lack a criterion.",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE3_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE3_LEFTOVER_MIGRATIONS],
)
def test_wave3_leftover_migrations_are_valid_katex(
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
    _WAVE3_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE3_LEFTOVER_EXCLUSIONS],
)
def test_wave3_leftover_exclusions_are_byte_identical(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text


def test_wave3_leftover_knowledge_check_scoring_unaffected() -> None:
    """KC fields touched in leftovers are common_mistake/explanation only."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    targets = (
        "3.2.6-ci-two-sample-cs1011.json",
        "3.2.3-ci-given-sampling-distribution-cs1011.json",
    )
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
            pack, curriculum_identity="CS1:wave3", topic_id=pack.topic_code
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

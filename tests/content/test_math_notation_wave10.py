"""Wave 10 mathematical notation migration: KaTeX validity, scoring, ledger."""

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
import math_notation_wave9 as wave9  # noqa: E402
import math_notation_wave10 as wave10  # noqa: E402

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave10_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–10 authored math.
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

# Representative (package, path, must-contain) meaning checks across all 12 packages.
_MEANING_SAMPLES = (
    (
        "5.1.4-loss-estimators-cs1003.json",
        "worked_example.steps[0].calculation",
        (r"E[\theta \mid \mathrm{data}]", r"5.45"),
        "Bayes mean under squared-error loss",
    ),
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.final_answer",
        (r"234.32", r"265.68", r"\theta", r"0.95"),
        "central 95% credible interval",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[0].calculation",
        (r"\propto", r"\theta \mid y", r"\mathrm{prior}"),
        "posterior proportionality",
    ),
    (
        "revision-hypothesis-testing-cs1012.json",
        "worked_example.final_answer",
        (r"P(H_{0}\ \mathrm{true})",),
        "refuse P(H0 true) reading",
    ),
    (
        "revision-midspine-cs1003.json",
        "worked_example.given[0].value",
        (r"X \mid \theta", r"\mathrm{Binomial}(8, \theta)"),
        "Beta-Binomial midspine hinge",
    ),
    (
        "1.2.3-pca-cs1002.json",
        "worked_example.steps[1].calculation",
        (r"\neq",),
        "PCA variation not latent pricing",
    ),
    (
        "4.1.1-response-explanatory-cs1003.json",
        "worked_example.steps[1].calculation",
        (r"\hat{y}(8)", r"3700"),
        "linear predictor at x=8",
    ),
    (
        "4.1.1-response-explanatory-cs1013.json",
        "worked_example.steps[1].calculation",
        (r"\hat{y}(45)", r"3000"),
        "linear predictor at x=45",
    ),
    (
        "cp-4.1.1-linear-regression-cs1016.json",
        "worked_example.steps[1].calculation",
        (r"\hat{y}(25)", r"480"),
        "linear predictor at x=25",
    ),
    (
        "cr-1.1.3-data-sources-cs1017.json",
        "worked_example.steps[1].calculation",
        (r"n \neq",),
        "large n not automatic fitness",
    ),
    (
        "cr-1.1.2-stages-tools-cs1017.json",
        "worked_example.steps[2].calculation",
        (r"\neq", "path complete"),
        "notebook-open not path complete",
    ),
    (
        "cr-1.2.3-pca-cs1017.json",
        "worked_example.steps[1].calculation",
        (r"\neq", "causal"),
        "PCA variation not causal driver",
    ),
)

# Locked Wave 10 leftover migrations (manual-review close-out).
_WAVE10_LEFTOVER_MIGRATIONS = (
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.given[0].note",
        r"posterior for $\theta$",
    ),
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form $\mathrm{mean} \pm 1.96 \times \mathrm{sd}$; interpret as a posterior probability statement.",
    ),
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $250 \pm 1.96 \times 8$.",
    ),
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.common_pitfall",
        r"Narrating the credible interval as if it had frequentist confidence-interval coverage, or using $\pm \mathrm{sd}$ instead of $\pm 1.96\,\mathrm{sd}$ for 95%.",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Retrieve $\mathrm{posterior} \propto \mathrm{likelihood} \times \mathrm{prior}$, then form $\mathrm{mean} \pm 1.96\,\mathrm{sd}$, then refuse coverage-language swap.",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[0].attempt_cue",
        r"Write $\mathrm{posterior}(\theta \mid y)$ up to a constant.",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[1].attempt_cue",
        r"Use $\mathrm{mean} \pm 1.96\,\mathrm{sd}$ for a Normal posterior.",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[1].explanation",
        r"For a Normal posterior, a central 95% credible interval is $\mathrm{mean} \pm 1.96\,\mathrm{sd}$.",
    ),
    (
        "revision-midspine-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Apply Beta-Binomial conjugacy: add successes to $\alpha$ and failures to $\beta$.",
    ),
    (
        "revision-midspine-cs1003.json",
        "worked_example.steps[0].explanation",
        r"Beta-Binomial conjugacy adds observed successes to $\alpha$ and observed failures to $\beta$.",
    ),
    (
        "revision-midspine-cs1003.json",
        "worked_example.steps[1].explanation",
        r"Adding $n$ to $\alpha$ and $x$ to $\beta$ (or adding successes to both parameters) breaks conjugacy. Failures are $n - x$, not $x$.",
    ),
    (
        "revision-midspine-cs1003.json",
        "worked_example.common_pitfall",
        r"Updating $\mathrm{Beta}(\alpha, \beta)$ by adding the sample size to $\alpha$ and the success count to $\beta$, or claiming empirical Bayes uses no prior.",
    ),
)

# Locked Wave 10 leftover prose exclusions (byte-identical; not converted).
_WAVE10_LEFTOVER_EXCLUSIONS = (
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.steps[1].explanation",
        "A credible interval is a posterior probability statement about θ, not a frequentist coverage claim about repeated sampling of the interval.",
    ),
    (
        "5.1.5-credible-intervals-cs1003.json",
        "worked_example.steps[2].explanation",
        "Credible intervals condition on the data and treat θ as random under the posterior; confidence intervals are pre-data coverage procedures.",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[0].explanation",
        "Bayes' theorem multiplies prior by likelihood (and normalises over θ).",
    ),
    (
        "revision-bayesian-cs1015.json",
        "worked_example.steps[2].explanation",
        "Given the model, prior, and data, posterior probability that θ lies in the interval is 0.95. That is not the frequentist claim that 95% of repeated-sample intervals cover θ.",
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


def test_wave10_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave10.WAVE10_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        for step in we.get("steps") or []:
            calc = step.get("calculation") or ""
            if "$" in calc:
                assert prepare_math_markup(calc) == calc
                break


def test_wave10_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 10 packages is valid KaTeX source."""
    span_count = 0
    packages_with_spans = set()
    for fname in wave10.WAVE10_FILES:
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
    assert span_count >= 30
    assert packages_with_spans == set(wave10.WAVE10_FILES)


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave10_sample_latex_matches_intended_meaning(
    package_file: str,
    field_path: str,
    needles: tuple[str, ...],
    label: str,
) -> None:
    pkg = _load(package_file)
    text = wave1.get_path(pkg, field_path)
    for needle in needles:
        assert needle in text, (
            f"{label}: expected {needle!r} in {package_file} {field_path}: {text}"
        )
    for body in _spans(text):
        _assert_valid_latex(body, where=f"{label}:{field_path}")


def test_wave10_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave10", topic_id=pack.topic_code
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


def test_wave10_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["migrated"] == 1992
    assert checked["totals"]["needs_migration"] == 0
    assert checked["totals"]["packages_with_migration_backlog"] == 0
    assert live["totals"] == checked["totals"]

    wave10_files = set(wave10.WAVE10_FILES)
    migrated = 0
    still_pending_review_nm = 0
    confident_backlog = 0
    manual_excluded = 0
    pending_manual_excluded = 0
    for row in live["packages"]:
        if row["package_file"] not in wave10_files:
            continue
        for item in row["items"]:
            if item["migration_status"] == "migrated":
                migrated += 1
                assert item["category"] == "already_compliant"
                assert "dollar_delimited" in item["signals"]
            if item["category"] == "needs_migration" and item["needs_manual_review"]:
                still_pending_review_nm += 1
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
            if (
                item["category"] == "correctly_excluded"
                and item["needs_manual_review"]
            ):
                pending_manual_excluded += 1
    assert migrated == 41
    assert still_pending_review_nm == 0
    assert confident_backlog == 0
    assert manual_excluded == 4
    assert pending_manual_excluded == 0


def test_wave10_catalogue_needs_migration_is_zero() -> None:
    """Final-wave close-out: no confident needs_migration remains anywhere."""
    live = inventory.build_inventory(PACKAGES)
    assert live["totals"]["needs_migration"] == 0
    assert live["totals"]["remaining_backlog"] == 0
    assert live["totals"]["packages_with_migration_backlog"] == 0
    assert live["totals"]["needs_manual_review"] == 115
    assert live["totals"]["migrated"] == 1992


def test_wave10_packages_disjoint_from_prior_waves() -> None:
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave3.WAVE3_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave4.WAVE4_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave5.WAVE5_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave6.WAVE6_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave7.WAVE7_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave8.WAVE8_FILES))
    assert set(wave10.WAVE10_FILES).isdisjoint(set(wave9.WAVE9_FILES))


def test_wave10_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 10 packages match the pre-migration snapshot."""
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
    _WAVE10_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE10_LEFTOVER_MIGRATIONS],
)
def test_wave10_leftover_migrations_are_valid_katex(
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
    _WAVE10_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE10_LEFTOVER_EXCLUSIONS],
)
def test_wave10_leftover_exclusions_are_byte_identical(
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


def test_wave10_leftover_partial_migrations_preserve_surrounding_prose() -> None:
    """Partial leftovers typeset only the live math object; framing prose stays."""
    cases = (
        (
            "5.1.5-credible-intervals-cs1003.json",
            "worked_example.given[0].note",
            ("posterior for ",),
            (r"\theta",),
        ),
        (
            "5.1.5-credible-intervals-cs1003.json",
            "worked_example.attempt_before_reveal",
            (
                "CMP closed. Form ",
                "; interpret as a posterior probability statement.",
            ),
            (r"\mathrm{mean} \pm 1.96 \times \mathrm{sd}",),
        ),
        (
            "5.1.5-credible-intervals-cs1003.json",
            "worked_example.steps[0].attempt_cue",
            ("Compute ",),
            (r"250 \pm 1.96 \times 8",),
        ),
        (
            "5.1.5-credible-intervals-cs1003.json",
            "worked_example.common_pitfall",
            (
                "Narrating the credible interval as if it had frequentist confidence-interval coverage, or using ",
                " instead of ",
                " for 95%.",
            ),
            (r"\pm \mathrm{sd}", r"\pm 1.96\,\mathrm{sd}"),
        ),
        (
            "revision-bayesian-cs1015.json",
            "worked_example.attempt_before_reveal",
            (
                "CMP closed. Retrieve ",
                ", then form ",
                ", then refuse coverage-language swap.",
            ),
            (
                r"\mathrm{posterior} \propto \mathrm{likelihood} \times \mathrm{prior}",
                r"\mathrm{mean} \pm 1.96\,\mathrm{sd}",
            ),
        ),
        (
            "revision-bayesian-cs1015.json",
            "worked_example.steps[0].attempt_cue",
            ("Write ", " up to a constant."),
            (r"\mathrm{posterior}(\theta \mid y)",),
        ),
        (
            "revision-bayesian-cs1015.json",
            "worked_example.steps[1].attempt_cue",
            ("Use ", " for a Normal posterior."),
            (r"\mathrm{mean} \pm 1.96\,\mathrm{sd}",),
        ),
        (
            "revision-bayesian-cs1015.json",
            "worked_example.steps[1].explanation",
            ("For a Normal posterior, a central 95% credible interval is ",),
            (r"\mathrm{mean} \pm 1.96\,\mathrm{sd}",),
        ),
        (
            "revision-midspine-cs1003.json",
            "worked_example.attempt_before_reveal",
            (
                "CMP closed. Apply Beta-Binomial conjugacy: add successes to ",
                " and failures to ",
                ".",
            ),
            (r"\alpha", r"\beta"),
        ),
        (
            "revision-midspine-cs1003.json",
            "worked_example.steps[0].explanation",
            (
                "Beta-Binomial conjugacy adds observed successes to ",
                " and observed failures to ",
                ".",
            ),
            (r"\alpha", r"\beta"),
        ),
        (
            "revision-midspine-cs1003.json",
            "worked_example.steps[1].explanation",
            (
                "Adding ",
                " to ",
                " and ",
                " to ",
                " (or adding successes to both parameters) breaks conjugacy. Failures are ",
                ", not ",
                ".",
            ),
            (r"n", r"\alpha", r"x", r"\beta", r"n - x"),
        ),
        (
            "revision-midspine-cs1003.json",
            "worked_example.common_pitfall",
            (
                "Updating ",
                " by adding the sample size to ",
                " and the success count to ",
                ", or claiming empirical Bayes uses no prior.",
            ),
            (r"\mathrm{Beta}(\alpha, \beta)", r"\alpha", r"\beta"),
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


def test_wave10_leftover_knowledge_check_scoring_unaffected() -> None:
    """No leftover fields were knowledge_checks; all Wave 10 KC scoring holds."""
    leftover_fields = {field for _, field, _ in _WAVE10_LEFTOVER_MIGRATIONS}
    leftover_fields |= {field for _, field, _ in _WAVE10_LEFTOVER_EXCLUSIONS}
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
            pack, curriculum_identity="CS1:wave10-kc", topic_id=pack.topic_code
        )
        practice = [
            a for a in substance.activities if a.stage is EducationalStage.PRACTICE
        ]
        for act in practice:
            item = act.scoreable
            assert item is not None
            expected = by_id[(fname, item.item_id)]
            assert item.answer_key.correct_choice_id == expected["correct_choice_id"]
            assert list(item.answer_key.accepted) == expected["accepted_keywords"]
            for probe in expected["verdicts"]:
                result = score_practice_response(item, probe["response"])
                assert result.scored is probe["scored"]
                assert result.correct is probe["correct"]
                assert result.matched_key == probe["matched_key"]

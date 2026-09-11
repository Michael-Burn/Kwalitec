"""Wave 6 mathematical notation migration: KaTeX validity, scoring, ledger."""

# Leftover exclusion/migration strings are verbatim package text; line length is expected.
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
        "knowledge_checks[1].explanation",
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
        "knowledge_checks[1].explanation",
        (r"e^{-2000/1000}", r"e^{-2}", r"\approx 0.135"),
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
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["migrated"] == 2086
    assert checked["totals"]["needs_migration"] == 0
    assert live["totals"] == checked["totals"]

    wave6_files = set(wave6.WAVE6_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    manual_excluded = 0
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
            if item["migration_status"] == "correctly_excluded":
                manual_excluded += 1
                assert item["category"] == "correctly_excluded"
                assert item["needs_manual_review"] is False
                assert item["reason_code"] == "manual_review_prose_exclusion"
    assert migrated == 273
    assert still_pending_review == 0
    assert confident_backlog == 0
    assert manual_excluded == 18


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


# Locked Wave 6 leftover migrations (manual-review close-out).
_WAVE6_LEFTOVER_MIGRATIONS = (
    (
        "4.2.5-linear-predictor-cs1014.json",
        "mission.concept_focus",
        r"$\eta = X\beta$ definition → polynomial and factor forms → refuse conflating $\eta$ with the link function.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "knowledge_checks[0].explanation",
        r"$\eta = X\beta$ is the linear predictor; the link maps mu to eta. Polynomial and factor terms can enter eta in GLMs when specified.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Evaluate $\eta = 1.0 + 0.2x - 0.01x^{2}$ at $x = 10$, then $\mu = e^{\eta}$.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.steps[0].explanation",
        r"The linear predictor $\eta = x^{\mathrm{T}}\beta$ may include powers or factors; 'linear' refers to parameters $\beta$, not to the raw covariate.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.steps[1].label",
        r"Evaluate $\eta$ at $x = 10$",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.steps[2].attempt_cue",
        r"Apply the log link inverse $\mu = e^{\eta}$.",
    ),
    (
        "4.2.5-linear-predictor-cs1014.json",
        "worked_example.common_pitfall",
        r"Calling a quadratic model 'nonlinear regression' because of $x^{2}$, or reporting $\eta = 2.0$ as the mean severity without exponentiating.",
    ),
    (
        "revision-joint-distributions-cs1005.json",
        "worked_example.steps[0].explanation",
        r"Discrete X and Y are independent if and only if $p_{X,Y}(x,y) = p_{X}(x)p_{Y}(y)$ for every pair in the joint support.",
    ),
    (
        "2.4.2-moment-via-gf-cs1007.json",
        "worked_example.given[0].note",
        r"CGF for $\mathrm{Poisson}(\lambda = 2)$",
    ),
    (
        "2.4.2-moment-via-gf-cs1007.json",
        "worked_example.steps[2].attempt_cue",
        r"State why writing $C_{X}(t) = 2(e^{t} - 1)$ alone does not give the moments.",
    ),
    (
        "2.4.2-moment-via-gf-cs1007.json",
        "worked_example.common_pitfall",
        r"Treating the presence of $C_{X}(t) = 2(e^{t} - 1)$ as already giving the moments, or evaluating $C(0) = 0$ and calling that the mean.",
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.steps[2].label",
        r"Decision at $\alpha = 0.05$",
    ),
    (
        "3.3.1-hypothesis-concepts-cs1012.json",
        "worked_example.steps[2].explanation",
        r"Reject $H_{0}$ when $p \leq \alpha$. Here $p = 0.0358 < 0.05$.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "knowledge_checks[1].common_mistake",
        r"Accepting $\eta = \beta_{0} + \beta_{1} x$ only or treating interaction as another main effect.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.given[1].note",
        r"$\mu = e^{\eta}$",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.steps[2].attempt_cue",
        r"Convert $\eta = -1.0$ through the log link.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.steps[2].explanation",
        r"Under a log link, $\mu = e^{\eta}$ is the modelled mean count rate.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "worked_example.common_pitfall",
        r"Adding the interaction 0.2 for male-not-young or female-young (where $M\times Y = 0$), or treating factors as continuous covariates without indicator coding.",
    ),
    (
        "cp-2.1.3-prob-quantiles-cs1016.json",
        "worked_example.steps[0].attempt_cue",
        r"Use $F(x) = 1 - e^{-x/\theta}$ with $x = 400$ and $\theta = 800$.",
    ),
    (
        "cp-2.1.3-prob-quantiles-cs1016.json",
        "worked_example.steps[0].explanation",
        r"For an Exponential with mean $\theta$, the CDF is $1 - e^{-x/\theta}$. The threshold is half the mean, so the exponent is $-1/2$.",
    ),
    (
        "cp-2.1.3-prob-quantiles-cs1016.json",
        "worked_example.steps[1].attempt_cue",
        r"Solve $1 - e^{-m/800} = 0.5$ for $m$.",
    ),
    (
        "cp-2.1.3-prob-quantiles-cs1016.json",
        "worked_example.steps[1].explanation",
        r"The median is the 0.5-quantile. Survival equals one half when $e^{-m/\theta} = 1/2$, so $m = \theta \ln 2$.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.tutor_intent",
        r"Today I will force $\eta = X\beta$ writing for a factor model and a polynomial term. Refuse $\eta$/link conflation.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.concept_focus",
        r"$\eta = X\beta$ → polynomial / factor forms → refuse $\eta$=link conflation.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Substitute $x = 8$ into $\eta$.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $\mu = e^{\eta}$.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Rewrite the Poisson pmf as $\exp\{y \ln\lambda - \lambda - \ln y!\}$ and read off $\theta = \ln\lambda$.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.steps[1].label",
        r"Numeric natural parameter at $\lambda = 4$",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.steps[1].attempt_cue",
        r"Evaluate $\theta = \ln 4$.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "worked_example.common_pitfall",
        r"Reporting $\theta = \lambda = 4$ (the mean) instead of the natural parameter $\ln\lambda$, or claiming Normal is excluded from the GLM exponential family.",
    ),
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "knowledge_checks[1].hints[0]",
        r"Use $F(x) = 1 - e^{-x/\theta}$ with $\theta = 250$ and $x = 100$.",
    ),
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "knowledge_checks[1].common_mistake",
        r"Reporting $e^{-0.4} \approx 0.6703$ (the survival probability) instead of $1 - e^{-0.4}$, or treating $\theta = 250$ as a rate so that $F(100) = 1 - e^{-25000}$.",
    ),
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Use the Exponential CDF $F(x) = 1 - e^{-x/\theta}$ and the median formula $\theta \ln 2$.",
    ),
    (
        "2.1.3-prob-quantiles-cs1004.json",
        "worked_example.steps[1].explanation",
        r"The median $m$ satisfies $1 - e^{-m/\theta} = 0.5$, so $m = \theta \ln 2$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "mission.tutor_intent",
        r"Today I will force $\text{premium} = Z\cdot\text{mean} + (1-Z)\cdot\text{collateral}$ structure and refuse 'Z finished Bayesian credibility theory'.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].explanation",
        r"$P = 0.4 \times 800 + 0.6 \times 600 = 320 + 360 = 680$. $Z = 0.4$ weights individual experience; $(1 - Z)$ weights the hypothetical mean.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "knowledge_checks[1].common_mistake",
        r"Swapping the weights to get $0.4 \times 600 + 0.6 \times 800 = 720$, or taking full credibility $P = 800$.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Write $P = Z\bar{X} + (1 - Z)\mu$ before substituting.",
    ),
    (
        "5.1.6-credibility-premium-cs1015.json",
        "worked_example.common_pitfall",
        r"Computing $Z\mu + (1 - Z)\bar{X}$ (swapping the weights), which would give $0.4\times 600 + 0.6\times 800 = 720$ instead of 680.",
    ),
)

# Locked Wave 6 leftover prose exclusions (byte-identical; not converted).
_WAVE6_LEFTOVER_EXCLUSIONS = (
    (
        "4.2.4-factors-interactions-cs1014.json",
        "mission.tutor_intent",
        "Today I will force variable/factor/interaction discrimination and refuse treating η-form writing as today's LO.",
    ),
    (
        "4.2.4-factors-interactions-cs1014.json",
        "mission.why_now",
        "4.2.4 is contiguous after link. Without factors/interactions, η forms lack actuarial covariate honesty.",
    ),
    (
        "4.2.5-linear-predictor-cs1003.json",
        "mission.prior_bridge",
        "Yesterday factors/interactions (4.2.4). Today writes η forms.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "knowledge_checks[0].explanation",
        "GLM responses sit in named exponential families. Package name or presence of exp() does not make a GLM. Normal is one family member, not the universal definition.",
    ),
    (
        "4.2.1-exponential-family-cs1014.json",
        "knowledge_checks[1].explanation",
        "Family membership needs the exponential-family form tied to the response structure, not software branding or exp() alone.",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE6_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE6_LEFTOVER_MIGRATIONS],
)
def test_wave6_leftover_migrations_are_valid_katex(
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
    _WAVE6_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE6_LEFTOVER_EXCLUSIONS],
)
def test_wave6_leftover_exclusions_are_byte_identical(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text


def test_wave6_leftover_partial_migrations_preserve_surrounding_prose() -> None:
    """Partial leftovers typeset only the live math object; framing prose stays."""
    cases = (
        (
            "4.2.5-linear-predictor-cs1014.json",
            "mission.concept_focus",
            (
                " definition → polynomial and factor forms → refuse conflating ",
                " with the link function.",
            ),
            (r"\eta = X\beta", r"\eta"),
        ),
        (
            "2.4.2-moment-via-gf-cs1007.json",
            "worked_example.steps[2].attempt_cue",
            (
                "State why writing ",
                " alone does not give the moments.",
            ),
            (r"C_{X}(t) = 2(e^{t} - 1)",),
        ),
        (
            "4.2.4-factors-interactions-cs1014.json",
            "worked_example.steps[2].attempt_cue",
            (
                "Convert ",
                " through the log link.",
            ),
            (r"\eta = -1.0",),
        ),
        (
            "cp-2.1.3-prob-quantiles-cs1016.json",
            "worked_example.steps[1].explanation",
            (
                "The median is the 0.5-quantile. Survival equals one half when ",
                ", so ",
            ),
            (r"e^{-m/\theta} = 1/2", r"m = \theta \ln 2"),
        ),
        (
            "5.1.6-credibility-premium-cs1015.json",
            "mission.tutor_intent",
            (
                "Today I will force ",
                " structure and refuse 'Z finished Bayesian credibility theory'.",
            ),
            (r"\text{premium} = Z\cdot\text{mean} + (1-Z)\cdot\text{collateral}",),
        ),
        (
            "5.1.6-credibility-premium-cs1015.json",
            "worked_example.common_pitfall",
            (
                "Computing ",
                " (swapping the weights), which would give ",
                " instead of 680.",
            ),
            (r"Z\mu + (1 - Z)\bar{X}", r"0.4\times 600 + 0.6\times 800 = 720"),
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


def test_wave6_leftover_knowledge_check_scoring_unaffected() -> None:
    """Leftover KC edits are explanation/hint/common_mistake only; keys hold."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    targets = (
        "4.2.5-linear-predictor-cs1014.json",
        "4.2.4-factors-interactions-cs1014.json",
        "4.2.1-exponential-family-cs1014.json",
        "2.1.3-prob-quantiles-cs1004.json",
        "5.1.6-credibility-premium-cs1015.json",
    )
    by_id = {
        (r["package_file"], r["item_id"]): r
        for r in snapshot["items"]
        if r["package_file"] in targets
    }
    assert by_id
    # Excluded KC explanations remain byte-identical (no scoring surface change).
    for package_file, field_path, expected in _WAVE6_LEFTOVER_EXCLUSIONS:
        if field_path.startswith("knowledge_checks"):
            assert wave1.get_path(_load(package_file), field_path) == expected
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
            pack, curriculum_identity="CS1:wave6-left", topic_id=pack.topic_code
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

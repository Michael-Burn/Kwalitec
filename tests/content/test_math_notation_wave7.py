"""Wave 7 mathematical notation migration: KaTeX validity, scoring, ledger."""

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

PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"
LEDGER = REPO_ROOT / "docs/content/math_notation_inventory.json"
SCORING_SNAPSHOT = (
    REPO_ROOT / "tests/fixtures/math_notation_wave7_scoring_snapshot.json"
)

# KaTeX 0.16.x control words used in Waves 1–7 authored math.
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
    }
)

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")

# Representative (package, path, must-contain) meaning checks across all 12 packages.
_MEANING_SAMPLES = (
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.final_answer",
        (r"\operatorname{logit}(0.8)", r"\mu = e^{0.5}", r"\approx"),
        "logit and Poisson inverse link",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "knowledge_checks[1].model_answer",
        (r"S_{1}^{2}/S_{2}^{2}", r"F_{n_{1}-1,n_{2}-1}"),
        "F variance ratio null distribution",
    ),
    (
        "3.2.1-confidence-interval-parameter-cs1011.json",
        "worked_example.attempt_before_reveal",
        (r"\bar{x}", r"z_{0.975}", r"\sigma/\sqrt{n}"),
        "z-interval formula before substitute",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.final_answer",
        (r"\theta = \operatorname{logit}(0.25)", r"b(\theta)"),
        "Bernoulli natural parameter",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.final_answer",
        (r"\Delta D = 8.2", r"\alpha = 0.05"),
        "nested deviance comparison",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.final_answer",
        (r"R^{2}_{\mathrm{adj},A}", r"R^{2}_{\mathrm{adj},B}"),
        "adjusted R-squared model choice",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.final_answer",
        (r"R^{2}_{\mathrm{adj},A}", r"0.5830"),
        "adjusted R-squared prefers leaner model",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.final_answer",
        (r"\operatorname{logit}(0.25)", r"e^{1.2}"),
        "binomial logit and Poisson mean",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "worked_example.final_answer",
        (r"\eta = -0.7", r"\mu \approx 0.4966"),
        "factor interaction fitted eta",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.final_answer",
        (r"\Delta D = 10.0", r"\alpha = 0.05"),
        "flood nested deviance reject reduced",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.steps[1].calculation",
        (r"P = 0.55 \times 1200", r"1110"),
        "credibility premium arithmetic",
    ),
    (
        "2.2.2-independence-cs1005.json",
        "worked_example.final_answer",
        (r"P(X=0)=0.60", r"\neq P(0,0)"),
        "joint independence check",
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


def test_wave7_dollar_delimiters_pass_through_markup() -> None:
    for fname in wave7.WAVE7_FILES:
        pkg = _load(fname)
        we = pkg.get("worked_example") or {}
        calc = (we.get("steps") or [{}])[0].get("calculation") or ""
        if "$" in calc:
            assert prepare_math_markup(calc) == calc


def test_wave7_migrated_math_is_syntactically_valid_katex() -> None:
    """Every $...$ span in the 12 Wave 7 packages is valid KaTeX source."""
    span_count = 0
    packages_with_spans = set()
    for fname in wave7.WAVE7_FILES:
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
    assert span_count >= 200
    assert packages_with_spans == set(wave7.WAVE7_FILES)


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles", "label"),
    _MEANING_SAMPLES,
    ids=[row[3] for row in _MEANING_SAMPLES],
)
def test_wave7_sample_latex_matches_intended_meaning(
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


def test_wave7_scoring_matches_pre_migration_snapshot() -> None:
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
            pack, curriculum_identity="CS1:wave7", topic_id=pack.topic_code
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


def test_wave7_ledger_backlog_and_migration_status() -> None:
    checked = json.loads(LEDGER.read_text(encoding="utf-8"))
    live = inventory.build_inventory(PACKAGES)
    assert checked["content_fingerprint"] == live["content_fingerprint"]
    assert checked["totals"]["remaining_backlog"] == 0
    assert checked["totals"]["migrated"] == 1900
    assert checked["totals"]["needs_migration"] == 0
    assert live["totals"] == checked["totals"]

    wave7_files = set(wave7.WAVE7_FILES)
    migrated = 0
    still_pending_review = 0
    confident_backlog = 0
    manual_excluded = 0
    for row in live["packages"]:
        if row["package_file"] not in wave7_files:
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
    assert migrated == 167
    assert still_pending_review == 0
    assert confident_backlog == 0
    assert manual_excluded == 6


def test_wave7_packages_disjoint_from_prior_waves() -> None:
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave1.WAVE1_FILES))
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave2.WAVE2_FILES))
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave3.WAVE3_FILES))
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave4.WAVE4_FILES))
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave5.WAVE5_FILES))
    assert set(wave7.WAVE7_FILES).isdisjoint(set(wave6.WAVE6_FILES))


def test_wave7_scoring_keys_byte_identical_in_packages() -> None:
    """Scoring-key fields in Wave 7 packages match the pre-migration snapshot."""
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


# Locked Wave 7 leftover migrations (manual-review close-out).
_WAVE7_LEFTOVER_MIGRATIONS = (
    (
        "4.2.3-link-canonical-cs1014.json",
        "mission.concept_focus",
        r"$g(\mu)=\eta$ → link role → canonical link as natural-parameter pairing per family.",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Write $\eta = \operatorname{logit}(\mu)$ and $\mu = e^{\eta}$ before substituting.",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.steps[1].attempt_cue",
        r"Compute $\mu = \exp(0.5)$.",
    ),
    (
        "4.2.3-link-canonical-cs1014.json",
        "worked_example.common_pitfall",
        r"Using the identity link for Poisson ($\mu = \eta = 0.5$) or reporting $\operatorname{logit}(0.8) = 0.8/0.2 = 4$ without taking the logarithm.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "knowledge_checks[1].explanation",
        r"Each sample variance contributes a chi-square component with $n_{i}-1$ degrees of freedom, producing the stated F ratio.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form the ratio of sample variances and attach $F(\mathrm{df}_{1}, \mathrm{df}_{2})$ with $\mathrm{df} = n - 1$ for each sample.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $F = S_{1}^{2} / S_{2}^{2}$.",
    ),
    (
        "2.6.6-f-distribution-cs1009.json",
        "worked_example.steps[1].explanation",
        r"Under $\sigma_{1}^{2} = \sigma_{2}^{2}$, $F \sim F(n_{1} - 1, n_{2} - 1) = F(9, 7)$.",
    ),
    (
        "3.2.1-confidence-interval-parameter-cs1011.json",
        "worked_example.steps[2].explanation",
        r"Centre at $\bar{x}$ and add/subtract the half-width.",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.steps[0].explanation",
        r"$\ln \mathrm{pmf} = y \ln p + (1 - y) \ln(1 - p) = y \ln(p/(1 - p)) + \ln(1 - p)$.",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.steps[1].label",
        r"Evaluate $\theta$ at $p = 0.25$",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "worked_example.common_pitfall",
        r"Taking $\theta = p$ or $\theta = \ln p$ instead of $\operatorname{logit}(p)$, or claiming the Normal distribution is outside the exponential family used by GLMs.",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Form $\Delta D = D_{R} - D_{F}$ and compare with $\chi^{2}_{\nu, 0.95}$.",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.steps[0].explanation",
        r"For nested GLMs, the analysis of deviance uses $\Delta D = D_{\mathrm{reduced}} - D_{\mathrm{full}}$, which is approximately $\chi^{2}$ under $H_{0}$ with df equal to the number of extra parameters.",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "worked_example.common_pitfall",
        r"Comparing $D_{F} = 33.8$ alone with $\chi^{2}_{2, 0.95}$ instead of the nested difference $\Delta D = 8.2$, or using $|D_{F} - D_{R}|$ with the wrong sign convention while forgetting nesting.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Write $R^{2}_{\mathrm{adj}}$ for each model before comparing; do not select on raw $R^{2}$ alone.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Substitute $n = 60$, $p = 3$, $R^{2} = 0.55$ into the formula.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Substitute $n = 60$, $p = 6$, $R^{2} = 0.58$.",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "worked_example.common_pitfall",
        r"Choosing Model B solely because raw $R^{2} = 0.58$ exceeds $0.55$ without computing adjusted $R^{2}$, or assuming the larger model always loses after any penalty.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.attempt_before_reveal",
        r"CMP closed. Write $R^{2}_{\mathrm{adj}}$ for each model before comparing; do not select on raw $R^{2}$ alone.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[0].attempt_cue",
        r"Substitute $n = 50$, $p = 2$, $R^{2} = 0.60$ into the formula.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.steps[1].attempt_cue",
        r"Substitute $n = 50$, $p = 5$, $R^{2} = 0.62$.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "worked_example.common_pitfall",
        r"Choosing Model B solely because raw $R^{2} = 0.62$ exceeds $0.60$, and ignoring that adjusted $R^{2}$ falls after the extra three variables.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "mission.concept_focus",
        r"$g(\mu)=\eta$ → canonical pairing → refuse default-without-warrant.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.steps[0].label",
        r"Canonical logit at $\mu = 0.25$",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Evaluate $\ln(\mu/(1 - \mu))$.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.steps[1].label",
        r"Poisson mean from $\eta = 1.2$",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "worked_example.steps[1].attempt_cue",
        r"Invert the log link: $\mu = e^{\eta}$.",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "knowledge_checks[1].common_mistake",
        r"Accepting $\eta = \beta_{0} + \beta_{1} x$ only or treating interaction as another main effect.",
    ),
    (
        "4.2.4-factors-interactions-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Set $C = 1$, $H = 1$ and evaluate $\eta$, then $\mu$.",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.steps[0].attempt_cue",
        r"Compute $D_{R} - D_{F}$.",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.steps[1].explanation",
        r"Reject the reduced model at $\alpha = 0.05$ if $\Delta D$ exceeds the critical value.",
    ),
    (
        "4.2.7-model-choice-cs1003.json",
        "worked_example.common_pitfall",
        r"Comparing $D_{F}$ alone to the critical value, or reversing the subtraction as $D_{F} - D_{R}$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "mission.tutor_intent",
        r"Today I will force $Z\cdot\text{observation} + (1-Z)\cdot\text{prior-mean}$ structure and refuse $Z=1$ always.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].explanation",
        r"$P = 0.55 \times 1200 + 0.45 \times 1000 = 660 + 450 = 1110$. $Z = 0.55$ weights individual experience; $(1 - Z)$ weights the hypothetical mean.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "knowledge_checks[1].common_mistake",
        r"Swapping the weights to get $0.55 \times 1000 + 0.45 \times 1200 = 1090$, or taking full credibility $P = 1200$.",
    ),
    (
        "5.1.6-credibility-premium-cs1003.json",
        "worked_example.common_pitfall",
        r"Swapping the weights so that $Z$ multiplies $\mu$, or treating $Z$ as a probability that must equal $\bar{X}/\mu$.",
    ),
)

# Locked Wave 7 leftover prose exclusions (byte-identical; not converted).
_WAVE7_LEFTOVER_EXCLUSIONS = (
    (
        "4.2.1-exponential-family-cs1003.json",
        "knowledge_checks[0].explanation",
        "GLM responses sit in named exponential families. Package name or presence of exp() does not make a GLM. Normal is one family member, not the universal definition.",
    ),
    (
        "4.2.1-exponential-family-cs1003.json",
        "knowledge_checks[1].explanation",
        "Family membership needs the exponential-family form tied to the response structure, not software branding or exp() alone.",
    ),
    (
        "4.2.7-model-choice-cs1014.json",
        "reading_guidance.out_of_scope_today[1]",
        "χ² / LRT acceptability tests as primary (4.2.9)",
    ),
    (
        "4.1.5-variable-selection-cs1003.json",
        "mission.concept_focus",
        "Candidate explanatory sets → fit measures (e.g. adjusted R², AIC/BIC) → select an appropriate set.",
    ),
    (
        "4.1.5-variable-selection-cs1013.json",
        "mission.concept_focus",
        "Candidate explanatory sets → fit measures (e.g. adjusted R², AIC/BIC) → select an appropriate set.",
    ),
    (
        "4.2.3-link-canonical-cs1003.json",
        "mission.task_descriptions[0]",
        "Sketch Family / η / Link before CMP (EA-006 pedagogy retained).",
    ),
)


@pytest.mark.parametrize(
    ("package_file", "field_path", "expected"),
    _WAVE7_LEFTOVER_MIGRATIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE7_LEFTOVER_MIGRATIONS],
)
def test_wave7_leftover_migrations_are_valid_katex(
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
    _WAVE7_LEFTOVER_EXCLUSIONS,
    ids=[f"{p}:{f}" for p, f, _ in _WAVE7_LEFTOVER_EXCLUSIONS],
)
def test_wave7_leftover_exclusions_are_byte_identical(
    package_file: str,
    field_path: str,
    expected: str,
) -> None:
    text = wave1.get_path(_load(package_file), field_path)
    assert text == expected
    assert "$" not in text


def test_wave7_leftover_partial_migrations_preserve_surrounding_prose() -> None:
    """Partial leftovers typeset only the live math object; framing prose stays."""
    cases = (
        (
            "4.2.3-link-canonical-cs1014.json",
            "mission.concept_focus",
            (
                " → link role → canonical link as natural-parameter pairing per family.",
            ),
            (r"g(\mu)=\eta",),
        ),
        (
            "2.6.6-f-distribution-cs1009.json",
            "knowledge_checks[1].explanation",
            (
                "Each sample variance contributes a chi-square component with ",
                " degrees of freedom, producing the stated F ratio.",
            ),
            (r"n_{i}-1",),
        ),
        (
            "3.2.1-confidence-interval-parameter-cs1011.json",
            "worked_example.steps[2].explanation",
            (
                "Centre at ",
                " and add/subtract the half-width.",
            ),
            (r"\bar{x}",),
        ),
        (
            "4.2.1-exponential-family-cs1003.json",
            "worked_example.steps[1].label",
            (
                "Evaluate ",
                " at ",
            ),
            (r"\theta", r"p = 0.25"),
        ),
        (
            "4.2.7-model-choice-cs1014.json",
            "worked_example.steps[0].explanation",
            (
                "For nested GLMs, the analysis of deviance uses ",
                ", which is approximately ",
                " under ",
                " with df equal to the number of extra parameters.",
            ),
            (
                r"\Delta D = D_{\mathrm{reduced}} - D_{\mathrm{full}}",
                r"\chi^{2}",
                r"H_{0}",
            ),
        ),
        (
            "4.1.5-variable-selection-cs1003.json",
            "worked_example.steps[0].attempt_cue",
            (
                "Substitute ",
                " into the formula.",
            ),
            (r"n = 60", r"p = 3", r"R^{2} = 0.55"),
        ),
        (
            "4.2.3-link-canonical-cs1003.json",
            "mission.concept_focus",
            (
                " → canonical pairing → refuse default-without-warrant.",
            ),
            (r"g(\mu)=\eta",),
        ),
        (
            "4.2.4-factors-interactions-cs1003.json",
            "worked_example.steps[0].attempt_cue",
            (
                "Set ",
                " and evaluate ",
                ", then ",
            ),
            (r"C = 1", r"H = 1", r"\eta", r"\mu"),
        ),
        (
            "4.2.7-model-choice-cs1003.json",
            "worked_example.steps[1].explanation",
            (
                "Reject the reduced model at ",
                " if ",
                " exceeds the critical value.",
            ),
            (r"\alpha = 0.05", r"\Delta D"),
        ),
        (
            "5.1.6-credibility-premium-cs1003.json",
            "mission.tutor_intent",
            (
                "Today I will force ",
                " structure and refuse ",
                " always.",
            ),
            (
                r"Z\cdot\text{observation} + (1-Z)\cdot\text{prior-mean}",
                r"Z=1",
            ),
        ),
        (
            "5.1.6-credibility-premium-cs1003.json",
            "worked_example.common_pitfall",
            (
                "Swapping the weights so that ",
                " multiplies ",
                ", or treating ",
                " as a probability that must equal ",
            ),
            (r"Z", r"\mu", r"\bar{X}/\mu"),
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


def test_wave7_leftover_knowledge_check_scoring_unaffected() -> None:
    """Leftover KC edits are explanation/common_mistake only; keys hold."""
    snapshot = json.loads(SCORING_SNAPSHOT.read_text(encoding="utf-8"))
    targets = (
        "2.6.6-f-distribution-cs1009.json",
        "4.2.1-exponential-family-cs1003.json",
        "4.2.4-factors-interactions-cs1003.json",
        "5.1.6-credibility-premium-cs1003.json",
    )
    by_id = {
        (r["package_file"], r["item_id"]): r
        for r in snapshot["items"]
        if r["package_file"] in targets
    }
    assert by_id
    # Excluded KC explanations remain byte-identical (no scoring surface change).
    for package_file, field_path, expected in _WAVE7_LEFTOVER_EXCLUSIONS:
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
            pack, curriculum_identity="CS1:wave7-left", topic_id=pack.topic_code
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

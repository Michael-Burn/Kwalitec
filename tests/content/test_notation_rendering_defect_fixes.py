"""Regression tests for three notation-rendering defects found in audit item 11.

Fixes only; meaning and scoring keys are unchanged. Validates:
1. Broken $\\sigma$_X subscripts are closed inside a single math span.
2. Fragmented sum / prose-in-math fields are correctly delimited.
3. Correct MCQ choice uses consistent $\\mu$ / $\\lambda$ LaTeX.
4. concept_focus on 2.2.3 keeps its already-correct $\\sigma_{X}$ form.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from app.presentation.session.math_markup import prepare_math_markup

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

_MATH_SPAN = re.compile(r"(?<!\$)\$([^$]+)\$")
_CONTROL = re.compile(r"\\([A-Za-z]+)")
_BROKEN_SIGMA_SUB = re.compile(r"\$\\sigma\$_[XY]")
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
        "sum",
        "mid",
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

_FIXED_FIELDS: tuple[tuple[str, str, str], ...] = (
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "worked_example.steps[1].attempt_cue",
        r"\sigma_{X}",
    ),
    (
        "2.2.3-cov-corr-expectation-cs1005.json",
        "worked_example.steps[1].explanation",
        r"\sigma_{X}",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "worked_example.steps[1].explanation",
        r"\sum_{y}",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "worked_example.steps[2].calculation",
        r"E[Y|X]",
    ),
    (
        "2.3.1-conditional-expectation-cs1006.json",
        "worked_example.final_answer",
        r"E[Y]",
    ),
    (
        "4.2.2-mean-variance-cs1014.json",
        "knowledge_checks[0].choices[0].label",
        r"V(\mu)",
    ),
)


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _get_path(obj: object, path: str) -> str:
    cur: object = obj
    for part in path.split("."):
        if "[" in part:
            name, rest = part.split("[", 1)
            idx = int(rest.rstrip("]"))
            cur = getattr(cur, name) if not isinstance(cur, dict) else cur[name]
            cur = cur[idx]  # type: ignore[index]
        else:
            cur = cur[part] if isinstance(cur, dict) else getattr(cur, part)
    assert isinstance(cur, str), path
    return cur


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
    # Prose traps: spans must not contain multi-word English sentences.
    words = re.findall(r"[A-Za-z]{3,}", body)
    proseish = [
        w
        for w in words
        if w.lower()
        in {
            "takes",
            "values",
            "unconditional",
            "number",
            "function",
            "correlation",
            "independence",
            "automatic",
        }
    ]
    assert not proseish, f"prose trapped in math at {where}: {body!r} ({proseish})"


@pytest.mark.parametrize(
    ("package_file", "field_path", "needle"),
    _FIXED_FIELDS,
    ids=[f"{p}:{f}" for p, f, _ in _FIXED_FIELDS],
)
def test_fixed_fields_are_valid_correctly_delimited_latex(
    package_file: str,
    field_path: str,
    needle: str,
) -> None:
    pkg = _load(package_file)
    text = _get_path(pkg, field_path)
    assert text.count("$") % 2 == 0, f"unbalanced $ in {package_file} {field_path}"
    assert needle in text, f"expected {needle!r} in {field_path}: {text}"
    assert _BROKEN_SIGMA_SUB.search(text) is None, (
        f"broken $\\sigma$_X escape remains in {field_path}: {text}"
    )
    spans = _spans(text)
    assert spans, f"no math spans in {field_path}: {text}"
    for body in spans:
        _assert_valid_latex(body, where=f"{package_file}:{field_path}")
    # Authored $...$ must pass through prepare_math_markup unchanged.
    assert prepare_math_markup(text) == text


def test_cov_corr_has_no_remaining_broken_sigma_subscript_escapes() -> None:
    """Item 1: the $\\sigma$_X escape pattern is gone from the whole package."""
    raw = (PACKAGES / "2.2.3-cov-corr-expectation-cs1005.json").read_text(
        encoding="utf-8"
    )
    # Raw JSON stores a single backslash as \\ so match that encoding.
    assert r"\sigma$_" not in raw
    pkg = _load("2.2.3-cov-corr-expectation-cs1005.json")
    cue = pkg["worked_example"]["steps"][1]["attempt_cue"]
    expl = pkg["worked_example"]["steps"][1]["explanation"]
    assert r"\sigma_{X}" in cue and r"\sigma_{Y}" in cue
    assert r"\sigma_{X}" in expl and r"\sigma_{Y}" in expl
    assert "$\\sigma$_" not in cue and "$\\sigma$_" not in expl


def test_cov_corr_concept_focus_sigma_subscript_not_regressed() -> None:
    """Already-correct $\\sigma_{X}\\sigma_{Y}$ in concept_focus must stay intact."""
    pkg = _load("2.2.3-cov-corr-expectation-cs1005.json")
    focus = pkg["mission"]["concept_focus"]
    assert r"\sigma_{X}\sigma_{Y}" in focus
    assert _BROKEN_SIGMA_SUB.search(focus) is None
    for body in _spans(focus):
        _assert_valid_latex(body, where="concept_focus")


def test_conditional_expectation_english_stays_outside_math() -> None:
    pkg = _load("2.3.1-conditional-expectation-cs1006.json")
    calc = pkg["worked_example"]["steps"][2]["calculation"]
    final = pkg["worked_example"]["final_answer"]
    assert "takes values 15 and 17" in calc
    assert calc.index("$E[Y|X]$") < calc.index("takes values")
    assert "Unconditional" in final
    # The word Unconditional must not sit inside any $...$ span.
    for body in _spans(final):
        assert "Unconditional" not in body
        assert "number" not in body
        assert "function" not in body.lower() or "function" not in body


def test_mean_variance_correct_choice_uses_consistent_greek() -> None:
    pkg = _load("4.2.2-mean-variance-cs1014.json")
    kc = pkg["knowledge_checks"][0]
    assert kc["correct_choice_id"] == "a"
    label = next(c["label"] for c in kc["choices"] if c["id"] == "a")
    assert "$V(mu)$" not in label
    assert "mean lambda" not in label
    assert r"$V(\mu)$" in label
    assert r"$\lambda$" in label
    assert r"\operatorname{Var}" in label or r"\operatorname{Var}[Y]" in label
    for body in _spans(label):
        _assert_valid_latex(body, where="4.2.2 correct choice")

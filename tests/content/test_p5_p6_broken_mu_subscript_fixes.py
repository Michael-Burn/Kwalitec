"""Regression: broken $\\mu$_X style subscripts in P5-P6 CI packages.

Two distractor labels used `$\\mu$_A` / `$\\mu$_X` (math closed before the
subscript). Fixed to `$\\mu_{A}$` / `$\\mu_{X}` matching the catalogue
notation convention. Meaning and scoring keys are unchanged.
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
_BROKEN_MU_SUB = re.compile(r"\$\\mu\$_[A-Za-z]")
_KNOWN_COMMANDS = frozenset({"mu", "bar"})

_FIXED_FIELDS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "3.2.6-ci-two-sample-cs1011.json",
        "knowledge_checks[1].choices[3].label",
        (r"\mu_{A}", r"\mu_{B}"),
    ),
    (
        "3.2.7-ci-paired-means-cs1011.json",
        "knowledge_checks[1].choices[2].label",
        (r"\mu_{X}", r"\mu_{Y}"),
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
            cur = cur[name] if isinstance(cur, dict) else getattr(cur, name)  # type: ignore[index]
            cur = cur[idx]  # type: ignore[index]
        else:
            cur = cur[part] if isinstance(cur, dict) else getattr(cur, part)
    assert isinstance(cur, str), path
    return cur


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


@pytest.mark.parametrize(
    ("package_file", "field_path", "needles"),
    _FIXED_FIELDS,
    ids=[f"{p}:{f}" for p, f, _ in _FIXED_FIELDS],
)
def test_fixed_mu_subscript_fields_are_valid_latex(
    package_file: str,
    field_path: str,
    needles: tuple[str, ...],
) -> None:
    pkg = _load(package_file)
    text = _get_path(pkg, field_path)
    assert text.count("$") % 2 == 0, f"unbalanced $ in {package_file} {field_path}"
    assert _BROKEN_MU_SUB.search(text) is None, (
        f"broken $\\mu$_X escape remains in {field_path}: {text}"
    )
    for needle in needles:
        assert needle in text, f"expected {needle!r} in {field_path}: {text}"
    spans = _MATH_SPAN.findall(text)
    assert spans, f"no math spans in {field_path}: {text}"
    for body in spans:
        _assert_valid_latex(body, where=f"{package_file}:{field_path}")
    assert prepare_math_markup(text) == text


def test_p5_p6_scope_has_only_these_two_broken_mu_subscript_fixes() -> None:
    """The $\\mu$_Letter defect is gone from P5-P6 packages; only the two fixes exist as closed form."""
    scope_globs = (
        "2.2.*.json",
        "2.3.*.json",
        "3.2.*.json",
        "3.3.*.json",
        "cp-2.2*.json",
        "cp-2.3*.json",
        "cp-3.2*.json",
        "cp-3.3*.json",
        "revision-joint*.json",
        "revision-conditional*.json",
    )
    broken: list[str] = []
    closed_hits: list[str] = []
    for pattern in scope_globs:
        for path in sorted(PACKAGES.glob(pattern)):
            raw = path.read_text(encoding="utf-8")
            if r"\mu$_" in raw or "$\\mu$_" in raw:
                # JSON stores a single backslash as \\ in the file text when we
                # search for the authored escape; match the file encoding.
                if r"\mu$_" in raw:
                    broken.append(path.name)
            if path.name in {
                "3.2.6-ci-two-sample-cs1011.json",
                "3.2.7-ci-paired-means-cs1011.json",
            }:
                if r"\mu_{" in raw:
                    closed_hits.append(path.name)
    assert broken == [], f"broken $\\mu$_Letter remains in {broken}"
    assert set(closed_hits) == {
        "3.2.6-ci-two-sample-cs1011.json",
        "3.2.7-ci-paired-means-cs1011.json",
    }


def test_choice_ids_and_tags_unchanged_on_fixed_fields() -> None:
    """Fixes are markup-only: choice id, tag, and correct key stay put."""
    two_sample = _load("3.2.6-ci-two-sample-cs1011.json")
    cp = two_sample["knowledge_checks"][1]
    assert cp["item_id"] == "cs1011-3.2.6-cp-01"
    d = cp["choices"][3]
    assert d["id"] == "d"
    assert d["misconception_tag"] == "ratio_only"
    assert cp["correct_choice_id"] == "a"

    paired = _load("3.2.7-ci-paired-means-cs1011.json")
    cp = paired["knowledge_checks"][1]
    assert cp["item_id"] == "cs1011-3.2.7-cp-01"
    c = cp["choices"][2]
    assert c["id"] == "c"
    assert c["misconception_tag"] == "separate_means_only"
    assert cp["correct_choice_id"] == "a"

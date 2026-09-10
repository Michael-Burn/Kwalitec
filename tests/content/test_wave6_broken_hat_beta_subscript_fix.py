"""Regression: broken $\\hat{\\beta}$0 style subscripts in 4.1.2 AR.

Choice c on cs1003-4.1.2-ar-01 closed the math span before the digit
($\\hat{\\beta}$0). Fixed to $\\hat{\\beta}_{0}$ matching the catalogue
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
_BROKEN_HAT_BETA_DIGIT = re.compile(r"\$\\hat\{\\beta\}\$[0-9]")
_KNOWN_COMMANDS = frozenset({"hat", "beta", "varepsilon"})

_FIXED_FIELDS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (
        "4.1.2-simple-multiple-cs1003.json",
        "knowledge_checks[0].choices[2].label",
        (r"\hat{\beta}_{0}", r"\hat{\beta}_{1}"),
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
def test_fixed_hat_beta_subscript_fields_are_valid_latex(
    package_file: str,
    field_path: str,
    needles: tuple[str, ...],
) -> None:
    label = _get_path(_load(package_file), field_path)
    assert _BROKEN_HAT_BETA_DIGIT.search(label) is None
    assert "$_" not in label
    for needle in needles:
        assert needle in label
    for i, m in enumerate(_MATH_SPAN.finditer(label)):
        _assert_valid_latex(m.group(1), where=f"{field_path} span#{i}")
    assert prepare_math_markup(label) == label


def test_broken_hat_beta_digit_pattern_absent_from_fixed_package() -> None:
    """The specific $\\hat{\\beta}$0 defect must not remain in this package."""
    raw = (PACKAGES / "4.1.2-simple-multiple-cs1003.json").read_text(encoding="utf-8")
    assert _BROKEN_HAT_BETA_DIGIT.search(raw) is None


def test_fixed_label_still_belongs_to_cs1003_412_ar01_choice_c() -> None:
    data = _load("4.1.2-simple-multiple-cs1003.json")
    item = data["knowledge_checks"][0]
    assert item["item_id"] == "cs1003-4.1.2-ar-01"
    choice = item["choices"][2]
    assert choice["id"] == "c"
    assert r"\hat{\beta}_{0}" in choice["label"]
    assert r"\hat{\beta}_{1}" in choice["label"]

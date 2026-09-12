"""Regression: least-squares worked-example S3 cognitive-load segmentation.

Package S3 previously packed slope, intercept, fitted value, and residual into
one step (eight arithmetic sub-steps). Both catalogue twins are restructured
into S3/S4/S5 matching the one-result-per-step pattern used by e.g.
``3.1.5-asymptotic-mle-cs1010``. Mathematical content and final answers must
be preserved exactly.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
PACKAGES = REPO_ROOT / "app/curriculum/data/educational_packages/cs1"

_CS1003 = "4.1.3-least-squares-cs1003.json"
_CS1013 = "4.1.3-least-squares-cs1013.json"

# Banked pre-fix calculation body (semicolon-joined) and final answers.
_BANKED = {
    _CS1003: {
        "calculation_parts": (
            r"$\hat{\beta}_{1} = \frac{8}{5} = 1.6$",
            r"$\hat{\beta}_{0} = 6.5 - 1.6 \times 3.5 = 6.5 - 5.6 = 0.9$",
            r"$\hat{y}(4) = 0.9 + 1.6 \times 4 = 7.3$; residual $= 7 - 7.3 = -0.3$",
        ),
        "result_parts": (
            r"$\hat{\beta}_{1} = 1.6$",
            r"$\hat{\beta}_{0} = 0.9$",
            r"$e(4) = -0.3$",
        ),
        "final_answer": (
            r"$\hat{\beta}_{1} = 1.6$, $\hat{\beta}_{0} = 0.9$; "
            r"fitted line $\hat{y} = 0.9 + 1.6x$; "
            r"residual at $x = 4$ equals $-0.3$ (£000)."
        ),
        "residual_x": 4,
    },
    _CS1013: {
        "calculation_parts": (
            r"$\hat{\beta}_{1} = \frac{7}{5} = 1.4$",
            r"$\hat{\beta}_{0} = 4 - 1.4 \times 2.5 = 4 - 3.5 = 0.5$",
            r"$\hat{y}(3) = 0.5 + 1.4 \times 3 = 4.7$; residual $= 5 - 4.7 = 0.3$",
        ),
        "result_parts": (
            r"$\hat{\beta}_{1} = 1.4$",
            r"$\hat{\beta}_{0} = 0.5$",
            r"$e(3) = 0.3$",
        ),
        "final_answer": (
            r"$\hat{\beta}_{1} = 1.4$, $\hat{\beta}_{0} = 0.5$; "
            r"fitted line $\hat{y} = 0.5 + 1.4x$; "
            r"residual at $x = 3$ equals $0.3$ (£000)."
        ),
        "residual_x": 3,
    },
}


def _load(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


def _closing_steps(pkg: dict) -> list[dict]:
    steps = pkg["worked_example"]["steps"]
    # S1 means, S2 corrected sums stay; closing chain is S3 onward.
    return [s for s in steps if s["id"] in {"S3", "S4", "S5"}]


def test_both_twins_segment_overloaded_closing_step() -> None:
    for name in (_CS1003, _CS1013):
        steps = _load(name)["worked_example"]["steps"]
        ids = [s["id"] for s in steps]
        assert ids == ["S1", "S2", "S3", "S4", "S5"], name
        labels = [s["label"] for s in steps]
        assert labels[0] == "Sample means"
        assert labels[1] == "Corrected sums of squares and products"
        assert labels[2] == "OLS slope"
        assert labels[3] == "OLS intercept"
        assert labels[4].startswith("Fitted value and residual at x = ")


def test_segmented_calculations_preserve_banked_math() -> None:
    for name, banked in _BANKED.items():
        closing = _closing_steps(_load(name))
        assert len(closing) == 3
        calcs = [s["calculation"] for s in closing]
        results = [s["result"] for s in closing]
        assert calcs == list(banked["calculation_parts"]), name
        assert results == list(banked["result_parts"]), name
        # Rejoining S3–S5 calculations recovers the pre-fix single-step body.
        rejoined = "; ".join(calcs)
        expected_rejoin = "; ".join(banked["calculation_parts"])
        assert rejoined == expected_rejoin, name


def test_final_answers_unchanged() -> None:
    for name, banked in _BANKED.items():
        we = _load(name)["worked_example"]
        assert we["final_answer"] == banked["final_answer"]


def test_each_closing_step_is_single_concept() -> None:
    """No closing step may again pack slope + intercept + residual together."""
    packed = re.compile(
        r"Slope,\s*intercept,\s*and\s*residual",
        re.IGNORECASE,
    )
    for name, banked in _BANKED.items():
        closing = _closing_steps(_load(name))
        for step in closing:
            assert not packed.search(step["label"]), (name, step["id"])
            # At most one primary semicolon-separated calculation clause for
            # slope/intercept; residual step may keep fitted-value then residual.
            semis = step["calculation"].count(";")
            if step["id"] in {"S3", "S4"}:
                assert semis == 0, (name, step["id"], step["calculation"])
            else:
                assert semis == 1, (name, step["id"], step["calculation"])
                assert f"x = {banked['residual_x']}" in step["label"]

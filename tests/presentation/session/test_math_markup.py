"""KaTeX math markup preparation for Session presentation."""

from __future__ import annotations

import json
from pathlib import Path

from app.presentation.session.math_markup import prepare_math_markup

ROOT = Path(__file__).resolve().parents[3]
PACKAGES = ROOT / "app/curriculum/data/educational_packages/cs1"


def _load_package(name: str) -> dict:
    return json.loads((PACKAGES / name).read_text(encoding="utf-8"))


# --- Unit tests: delimiter normalization ---


def test_prepare_math_markup_passes_through_existing_delimiters() -> None:
    text = "Inline $E[X]=\\mu$ and display $$\\sum_{i=1}^n x_i$$"
    assert prepare_math_markup(text) == text


def test_prepare_math_markup_leaves_plain_probability_notation_unchanged() -> None:
    """Bayes notation is plain text — no false-positive wrapping."""
    text = "P(F|+) = 0.045 / 0.1875; P(Fraud|+) = 0.24"
    assert prepare_math_markup(text) == text


def test_prepare_math_markup_leaves_unicode_sample_mean_notation_unchanged() -> None:
    text = "E[X̄]=μ; Var(X̄)=σ²/n; E[S²]=σ²."
    assert prepare_math_markup(text) == text


def test_prepare_math_markup_wraps_exponential_pdf_fragment() -> None:
    """CS1010 MLE checkpoint — bare e^{−λx} in package JSON."""
    raw = "pdf f(x) = λ e^{−λx} for x > 0"
    assert prepare_math_markup(raw) == "pdf f(x) = λ $e^{−λx}$ for x > 0"


def test_prepare_math_markup_wraps_glm_log_link_effect() -> None:
    """CS1014 fit-interpret — e^{0.2} style fragment."""
    raw = "Enter the multiplicative effect e^{0.2} on mean frequency."
    expected = "Enter the multiplicative effect $e^{0.2}$ on mean frequency."
    assert prepare_math_markup(raw) == expected


def test_prepare_math_markup_wraps_bare_numeric_superscript() -> None:
    raw = "Likelihood contributes λ^5 e^{−8λ}"
    assert prepare_math_markup(raw) == "Likelihood contributes $λ^5$ $e^{−8λ}$"


# --- Representative live package strings ---


def test_bayes_worked_example_probability_strings_unchanged() -> None:
    pkg = _load_package("5.1.1-bayes-theorem-cs1015.json")
    we = pkg["worked_example"]
    assert prepare_math_markup(we["problem_statement"]) == we["problem_statement"]
    calc = we["steps"][0]["calculation"]
    assert prepare_math_markup(calc) == calc


def test_mle_numeric_checkpoint_prompt_gets_latex_wrapping() -> None:
    pkg = _load_package("3.1.2-maximum-likelihood-cs1010.json")
    cp = next(k for k in pkg["knowledge_checks"] if k["response_type"] == "numeric")
    marked = prepare_math_markup(cp["prompt"])
    assert "$e^{−λx}$" in marked
    assert "λ e^{−λx}" not in marked.replace("$e^{−λx}$", "")


def test_linear_combination_worked_example_multi_step_plain() -> None:
    pkg = _load_package("2.2.4-linear-combinations-cs1005.json")
    we = pkg["worked_example"]
    # Covariance expansion is plain Var/E notation — should stay readable as text.
    step2 = we["steps"][1]["calculation"]
    assert prepare_math_markup(step2) == step2


# --- Template / asset wiring ---


def test_session_base_includes_katex_cdn_assets() -> None:
    base = (ROOT / "app/templates/session/base.html").read_text(encoding="utf-8")
    assert "katex@0.16.11/dist/katex.min.css" in base
    assert "katex@0.16.11/dist/katex.min.js" in base
    assert "auto-render.min.js" in base
    assert "katex-auto-render.js" in base
    assert "katex-theme.css" in base


def test_session_body_exposes_katex_render_target() -> None:
    body = (ROOT / "app/templates/session/partials/session_body.html").read_text(
        encoding="utf-8"
    )
    assert 'data-katex-target="true"' in body

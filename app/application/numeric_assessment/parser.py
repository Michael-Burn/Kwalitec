"""Numeric response parser / normalizer.

Preserves the raw string. Produces a normalized value only when interpretation
is unambiguous. Genuine locale ambiguity is UNINTERPRETABLE, never a guess.
"""

from __future__ import annotations

import re

from app.application.numeric_assessment.results import ParseResult, ParseStatus
from app.application.numeric_assessment.specs import (
    AnswerSpecification,
    RepresentationForm,
)

# US-style number with optional thousands commas in groups of three.
_DECIMAL_OR_INT = re.compile(
    r"""
    ^
    [+-]?
    (?:
        (?: \d{1,3} (?:, \d{3} )+ | \d+ )
        (?: \. \d* )?
      | \. \d+
    )
    (?: [eE] [+-]? \d+ )?
    $
    """,
    re.VERBOSE,
)

# Integer display (no decimal point, optional thousands commas).
_INTEGER_SHAPE = re.compile(
    r"""
    ^
    [+-]?
    (?: \d{1,3} (?:, \d{3} )+ | \d+ )
    $
    """,
    re.VERBOSE,
)

# Percentage: number lexeme immediately followed by %.
_PERCENTAGE_SHAPE = re.compile(
    r"""
    ^
    (
      [+-]?
      (?:
          (?: \d{1,3} (?:, \d{3} )+ | \d+ )
          (?: \. \d* )?
        | \. \d+
      )
      (?: [eE] [+-]? \d+ )?
    )
    \s*%
    $
    """,
    re.VERBOSE,
)

# Shapes that are genuinely ambiguous under mixed locale conventions.
_AMBIGUOUS_COMMA_DECIMAL = re.compile(
    r"""
    ^
    [+-]?
    \d{1,3}
    (?:, \d{1,2} )+
    (?: \. \d+ )?
    $
    """,
    re.VERBOSE,
)

_EUROPEAN_MIXED = re.compile(
    r"""
    ^
    [+-]?
    \d{1,3}
    (?: \. \d{3} )+
    , \d+
    $
    """,
    re.VERBOSE,
)


def _strip_commas(lexeme: str) -> str:
    return lexeme.replace(",", "")


def _float_from_lexeme(lexeme: str) -> float | None:
    try:
        return float(_strip_commas(lexeme))
    except ValueError:
        return None


def _decimal_places_in_lexeme(lexeme: str) -> int | None:
    """Count digits after the decimal point in the numeric lexeme (no %)."""
    cleaned = lexeme.strip()
    if re.search(r"[eE]", cleaned):
        return None
    if "." not in cleaned:
        return 0
    frac = cleaned.split(".", 1)[1]
    # Drop trailing sign artifacts; lexeme should already be clean.
    return len(frac)


def count_decimal_places(numeric_lexeme: str | None) -> int | None:
    """Public helper for precision checks."""
    if numeric_lexeme is None:
        return None
    return _decimal_places_in_lexeme(numeric_lexeme)


def parse_numeric_response(
    raw_response: str,
    spec: AnswerSpecification,
) -> ParseResult:
    """Parse ``raw_response`` under the specification's representation policy.

    Returns PARSED with a normalized comparable value, INVALID for clearly
    non-numeric shapes, or UNINTERPRETABLE for genuine locale ambiguity.
    """
    raw = raw_response if raw_response is not None else ""
    text = raw.strip()
    if not text:
        return ParseResult(raw_response=raw, status=ParseStatus.INVALID)

    accepted = set(spec.accepted_forms)
    allow_thousands = spec.representation_policy.allow_thousands_separators

    # Locale ambiguity checks before any successful parse guess.
    if _EUROPEAN_MIXED.fullmatch(text) is not None:
        return ParseResult(raw_response=raw, status=ParseStatus.UNINTERPRETABLE)
    if _AMBIGUOUS_COMMA_DECIMAL.fullmatch(text) is not None:
        # e.g. "1,23" or "12,34": decimal comma vs bad thousands grouping.
        return ParseResult(raw_response=raw, status=ParseStatus.UNINTERPRETABLE)
    # "0,571" looks like a European decimal, but also matches a naive
    # thousands pattern as 571. Refuse to guess.
    if re.fullmatch(
        r"[+-]?0,\d+(?:\.\d+)?(?:[eE][+-]?\d+)?", text
    ) is not None:
        return ParseResult(raw_response=raw, status=ParseStatus.UNINTERPRETABLE)

    # Percentage form (only if authored as accepted).
    pct = _PERCENTAGE_SHAPE.fullmatch(text)
    if pct is not None:
        if RepresentationForm.PERCENTAGE not in accepted:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        lexeme = pct.group(1)
        if not allow_thousands and "," in lexeme:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        value = _float_from_lexeme(lexeme)
        if value is None:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        # Normalize percentage display to canonical decimal scale.
        return ParseResult(
            raw_response=raw,
            status=ParseStatus.PARSED,
            parsed_value=value / 100.0,
            detected_form=RepresentationForm.PERCENTAGE,
            numeric_lexeme=lexeme,
        )

    # Reject bare % attempts when percentage is not accepted (already handled).
    if text.endswith("%"):
        return ParseResult(raw_response=raw, status=ParseStatus.INVALID)

    # Integer form when authored (and not a decimal lexeme).
    if RepresentationForm.INTEGER in accepted and _INTEGER_SHAPE.fullmatch(text):
        if not allow_thousands and "," in text:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        value = _float_from_lexeme(text)
        if value is None:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        return ParseResult(
            raw_response=raw,
            status=ParseStatus.PARSED,
            parsed_value=value,
            detected_form=RepresentationForm.INTEGER,
            numeric_lexeme=text,
        )

    # Decimal / general numeric form.
    if RepresentationForm.DECIMAL in accepted or (
        RepresentationForm.INTEGER in accepted and "." in text
    ):
        if _DECIMAL_OR_INT.fullmatch(text) is None:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        if not allow_thousands and "," in text:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        # If only INTEGER is accepted, reject decimals.
        if (
            RepresentationForm.DECIMAL not in accepted
            and RepresentationForm.INTEGER in accepted
            and "." in text
        ):
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        value = _float_from_lexeme(text)
        if value is None:
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        form = (
            RepresentationForm.INTEGER
            if "." not in text and RepresentationForm.INTEGER in accepted
            else RepresentationForm.DECIMAL
        )
        if (
            form is RepresentationForm.DECIMAL
            and RepresentationForm.DECIMAL not in accepted
        ):
            return ParseResult(raw_response=raw, status=ParseStatus.INVALID)
        return ParseResult(
            raw_response=raw,
            status=ParseStatus.PARSED,
            parsed_value=value,
            detected_form=form,
            numeric_lexeme=text,
        )

    return ParseResult(raw_response=raw, status=ParseStatus.INVALID)

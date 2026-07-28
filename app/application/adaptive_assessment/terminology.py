"""Educational terminology guard for Adaptive Assessment product resources.

Prevents student-facing exam / judgement language. Validation fails when
forbidden terms appear in Adaptive Assessment product copy or session
metadata. Approved replacements come from ILE-001 design.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# Student-facing forbidden phrases / words (case-insensitive whole-word /
# phrase match). Keep specific multi-word phrases before single tokens.
FORBIDDEN_STUDENT_TERMS: tuple[str, ...] = (
    "strong student",
    "poor performance",
    "low intelligence",
    "exam",
    "test",
    "pass",
    "fail",
    "weak",
)

# Approved replacements (product vocabulary) — for documentation and
# guidance; enforcement uses the forbid list above.
APPROVED_REPLACEMENTS: dict[str, str] = {
    "exam": "learning check / readiness check (never exam chrome)",
    "test": "check / learning check",
    "pass": "complete / continue",
    "fail": "incomplete evidence / needs reinforcement",
    "weak": "needs reinforcement / thin evidence",
    "strong student": "solid evidence / well-supported understanding",
    "poor performance": "thin evidence / needs more practice",
    "low intelligence": "(never use — no identity language)",
}


@dataclass(frozen=True)
class TerminologyViolation:
    """One forbidden-term finding in a product resource string."""

    source: str
    term: str
    excerpt: str


class TerminologyError(ValueError):
    """Raised when Adaptive Assessment product copy violates terminology policy."""

    def __init__(self, violations: list[TerminologyViolation]) -> None:
        self.violations = list(violations)
        summary = "; ".join(
            f"{v.source}: '{v.term}' in {v.excerpt!r}" for v in self.violations
        )
        super().__init__(
            "Adaptive Assessment terminology policy violated: " + summary
        )


def _compile_patterns() -> list[tuple[str, re.Pattern[str]]]:
    """Compile case-insensitive word-boundary patterns for each forbid term."""
    compiled: list[tuple[str, re.Pattern[str]]] = []
    for term in FORBIDDEN_STUDENT_TERMS:
        # Multi-word: allow flexible whitespace; single word: word boundaries.
        escaped = re.escape(term).replace(r"\ ", r"\s+")
        pattern = re.compile(rf"(?<!\w){escaped}(?!\w)", re.IGNORECASE)
        compiled.append((term, pattern))
    return compiled


_PATTERNS = _compile_patterns()

# Contexts where "exam" may appear as a syllabus / calendar fact rather than
# assessment chrome — still blocked in Adaptive Assessment *product* copy
# (ILE-001A is strict for AA resources). Session type names must never use
# forbidden terms.


def find_forbidden_terms(
    text: str,
    *,
    source: str = "copy",
) -> list[TerminologyViolation]:
    """Return all forbidden-term violations in ``text``."""
    if not text:
        return []
    found: list[TerminologyViolation] = []
    for term, pattern in _PATTERNS:
        for match in pattern.finditer(text):
            start = max(0, match.start() - 20)
            end = min(len(text), match.end() + 20)
            found.append(
                TerminologyViolation(
                    source=source,
                    term=term,
                    excerpt=text[start:end].strip(),
                )
            )
    return found


def assert_adaptive_assessment_copy_safe(
    text: str,
    *,
    source: str = "copy",
) -> str:
    """Return ``text`` or raise ``TerminologyError`` if forbidden terms remain."""
    violations = find_forbidden_terms(text, source=source)
    if violations:
        raise TerminologyError(violations)
    return text


def validate_product_resources(
    texts: dict[str, str],
) -> list[TerminologyViolation]:
    """Validate a mapping of resource id → student-facing text.

    Returns all violations (empty list means pass). Does not raise.
    """
    all_violations: list[TerminologyViolation] = []
    for source, text in texts.items():
        all_violations.extend(find_forbidden_terms(text, source=source))
    return all_violations


def validate_registered_adaptive_assessment_resources() -> None:
    """Validate session registry + copy registry; raise on any violation."""
    from app.application.adaptive_assessment.copy_registry import (
        iter_copy_entries,
    )
    from app.application.adaptive_assessment.session_registry import (
        iter_session_types,
    )

    resources: dict[str, str] = {}
    for entry in iter_copy_entries():
        resources[f"copy:{entry.key}"] = entry.default
    for session in iter_session_types():
        resources[f"session:{session.identifier}.display_name"] = (
            session.display_name
        )
        resources[f"session:{session.identifier}.short_description"] = (
            session.short_description
        )
        resources[f"session:{session.identifier}.duration_label"] = (
            session.expected_duration_label
        )
    violations = validate_product_resources(resources)
    if violations:
        raise TerminologyError(violations)

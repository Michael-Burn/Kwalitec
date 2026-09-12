"""Parse outcomes for the Numeric Assessment Framework."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from app.application.numeric_assessment.specs import (
    EvaluationPolicy,
    RepresentationForm,
)


class ParseStatus(str, Enum):
    """Explicit parse layer outcome. Never a silent guess."""

    PARSED = "parsed"
    INVALID = "invalid"
    UNINTERPRETABLE = "uninterpretable"


class FeedbackTier(str, Enum):
    """Three-tier feedback classification."""

    TIER_1 = "1"
    TIER_2 = "2"
    TIER_3 = "3"


@dataclass(frozen=True)
class ParseResult:
    """Raw preservation plus normalized value when unambiguous."""

    raw_response: str
    status: ParseStatus
    parsed_value: float | None = None
    detected_form: RepresentationForm | None = None
    numeric_lexeme: str | None = None


@dataclass(frozen=True)
class NumericEvaluationResult:
    """Structured evaluation record (does not collapse to one boolean only)."""

    item_id: str
    raw_response: str
    parse_status: ParseStatus
    parsed_value: float | None
    detected_form: RepresentationForm | None
    value_correct: bool
    precision_compliant: bool | None
    representation_accepted: bool
    evaluation_policy: EvaluationPolicy
    matched_diagnostic_rule_id: str | None
    feedback_tier: FeedbackTier
    feedback_message: str

    @property
    def fully_correct(self) -> bool:
        """Parsed, value correct, representation ok, precision not failing."""
        if self.parse_status is not ParseStatus.PARSED:
            return False
        if not self.value_correct or not self.representation_accepted:
            return False
        if self.precision_compliant is False:
            return False
        return True

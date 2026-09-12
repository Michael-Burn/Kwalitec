"""Authored Answer Specification contract for numeric assessment.

An author should be able to read a specification and understand what the
question assesses, how strictly the value is checked, which representations
are allowed, and whether any Tier 2 diagnostic rules exist. There is no
universal tolerance default in this package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class EvaluationPolicy(str, Enum):
    """How numerical closeness is judged for this question."""

    EXACT = "exact"
    DECIMAL_PRECISION = "decimal_precision"
    ABSOLUTE_TOLERANCE = "absolute_tolerance"
    RELATIVE_TOLERANCE = "relative_tolerance"
    SIGNIFICANT_FIGURES = "significant_figures"
    INTERVAL_RANGE = "interval_range"
    CUSTOM_DOMAIN_RULE = "custom_domain_rule"


class AssessmentIntent(str, Enum):
    """What the question is actually assessing."""

    CALCULATE_VALUE = "calculate_value"
    APPLY_FORMULA = "apply_formula"
    ROUND_VALUE = "round_value"
    CONVERT_UNITS = "convert_units"
    INTERPRET_RESULT = "interpret_result"


class QuantityType(str, Enum):
    """Kind of quantity being assessed."""

    PROBABILITY = "probability"
    COUNT = "count"
    RATE = "rate"
    SCALAR = "scalar"
    RESIDUAL = "residual"
    FACTOR = "factor"
    CURRENCY_LIKE = "currency_like"
    OTHER = "other"


class RepresentationForm(str, Enum):
    """Author-declared response form (not inferred symbolic equivalence)."""

    DECIMAL = "decimal"
    PERCENTAGE = "percentage"
    INTEGER = "integer"


class PrecisionRequirement(str, Enum):
    """How the raw response's displayed precision is checked."""

    NONE = "none"
    EXACT_DECIMAL_PLACES = "exact_decimal_places"
    AT_LEAST_DECIMAL_PLACES = "at_least_decimal_places"
    AT_MOST_DECIMAL_PLACES = "at_most_decimal_places"


class RoundingPolicy(str, Enum):
    """How rounding interacts with comparison (authored, not inferred)."""

    NONE = "none"
    HALF_UP = "half_up"


@dataclass(frozen=True)
class ComparisonPolicy:
    """Evaluation policy plus the parameters that policy requires."""

    policy: EvaluationPolicy
    absolute_tolerance: float | None = None
    relative_tolerance: float | None = None
    decimal_places: int | None = None
    significant_figures: int | None = None
    interval_low: float | None = None
    interval_high: float | None = None
    custom_rule_id: str | None = None

    def validate(self) -> None:
        """Raise ValueError when required parameters for the policy are missing."""
        p = self.policy
        if p is EvaluationPolicy.ABSOLUTE_TOLERANCE:
            if self.absolute_tolerance is None or self.absolute_tolerance < 0:
                raise ValueError(
                    "absolute_tolerance policy requires non-negative absolute_tolerance"
                )
        elif p is EvaluationPolicy.RELATIVE_TOLERANCE:
            if self.relative_tolerance is None or self.relative_tolerance < 0:
                raise ValueError(
                    "relative_tolerance policy requires non-negative relative_tolerance"
                )
        elif p is EvaluationPolicy.DECIMAL_PRECISION:
            if self.decimal_places is None or self.decimal_places < 0:
                raise ValueError(
                    "decimal_precision policy requires non-negative decimal_places"
                )
        elif p is EvaluationPolicy.SIGNIFICANT_FIGURES:
            if self.significant_figures is None or self.significant_figures < 1:
                raise ValueError(
                    "significant_figures policy requires significant_figures >= 1"
                )
        elif p is EvaluationPolicy.INTERVAL_RANGE:
            if self.interval_low is None or self.interval_high is None:
                raise ValueError(
                    "interval_range policy requires interval_low and interval_high"
                )
            if self.interval_low > self.interval_high:
                raise ValueError("interval_low must be <= interval_high")
        elif p is EvaluationPolicy.CUSTOM_DOMAIN_RULE:
            if not (self.custom_rule_id or "").strip():
                raise ValueError(
                    "custom_domain_rule policy requires a non-empty custom_rule_id"
                )


@dataclass(frozen=True)
class PrecisionPolicy:
    """Precision / format compliance rules (independent of value comparison)."""

    requirement: PrecisionRequirement = PrecisionRequirement.NONE
    decimal_places: int | None = None

    def validate(self) -> None:
        if self.requirement is PrecisionRequirement.NONE:
            return
        if self.decimal_places is None or self.decimal_places < 0:
            raise ValueError(
                f"{self.requirement.value} requires non-negative decimal_places"
            )


@dataclass(frozen=True)
class RepresentationPolicy:
    """Which response forms are accepted for this question."""

    accepted_forms: tuple[RepresentationForm, ...] = (
        RepresentationForm.DECIMAL,
    )
    allow_thousands_separators: bool = True

    def validate(self) -> None:
        if not self.accepted_forms:
            raise ValueError("accepted_forms must contain at least one form")


@dataclass(frozen=True)
class DiagnosticRule:
    """Authored Tier 2 rule. Phrasing is always 'consistent with'."""

    rule_id: str
    match_value: float
    consistent_with: str
    match_absolute_tolerance: float = 0.0
    rationale: str = ""

    def validate(self) -> None:
        if not (self.rule_id or "").strip():
            raise ValueError("diagnostic rule_id must be non-empty")
        if not (self.consistent_with or "").strip():
            raise ValueError("diagnostic consistent_with must be non-empty")
        if self.match_absolute_tolerance < 0:
            raise ValueError("match_absolute_tolerance must be non-negative")


@dataclass(frozen=True)
class FeedbackPolicy:
    """How Tier 1 / 2 / 3 feedback is assembled for this item."""

    tier3_message: str = (
        "Kwalitec cannot determine the specific calculation error "
        "from the final answer alone."
    )
    prefer_first_matching_diagnostic: bool = True


@dataclass(frozen=True)
class AnswerSpecification:
    """Per-question authored numeric assessment contract.

    There is no universal tolerance. Comparison behaviour comes only from
    ``comparison_policy``. Precision compliance is tracked separately from
    numerical correctness.
    """

    item_id: str
    canonical_value: float
    quantity_type: QuantityType
    assessment_intent: AssessmentIntent
    comparison_policy: ComparisonPolicy
    unit: str = ""
    representation_policy: RepresentationPolicy = field(
        default_factory=RepresentationPolicy
    )
    precision_policy: PrecisionPolicy = field(default_factory=PrecisionPolicy)
    rounding_policy: RoundingPolicy = RoundingPolicy.NONE
    diagnostic_rules: tuple[DiagnosticRule, ...] = ()
    feedback_policy: FeedbackPolicy = field(default_factory=FeedbackPolicy)

    def __post_init__(self) -> None:
        if not (self.item_id or "").strip():
            raise ValueError("item_id must be non-empty")
        self.comparison_policy.validate()
        self.precision_policy.validate()
        self.representation_policy.validate()
        for rule in self.diagnostic_rules:
            rule.validate()

    @property
    def accepted_forms(self) -> tuple[RepresentationForm, ...]:
        return self.representation_policy.accepted_forms

    @property
    def evaluation_policy(self) -> EvaluationPolicy:
        return self.comparison_policy.policy

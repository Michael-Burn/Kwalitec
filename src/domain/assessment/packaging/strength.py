"""Deterministic evidence strength from observation quality factors.

Strength reflects observation *quality*, never mastery or educational certainty.

Architecture Source
    knowledge/product/AP-002/SCORING_MODEL.md §8
"""

from __future__ import annotations

from dataclasses import dataclass

from domain.assessment.aggregation.observation_collection import ObservationCollection
from domain.assessment.enums import AttemptOutcome, ObservationKind
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.evidence_dimensions import EvidenceDimensions
from domain.assessment.value_objects.levels import EvidenceStrength
from domain.education.foundation.base import EducationalValueObject

# Heuristic thresholds (SCORING_MODEL §8 illustrative contract).
_HEAVY_HINTS = 2
_HIGH_RETRIES = 2
_STRONG_MIN_POINTS = 6
_MODERATE_MIN_POINTS = 3
_MULTI_QUESTION_MIN = 2


@dataclass(frozen=True, slots=True)
class EvidenceStrengthFactors(EducationalValueObject):
    """Explicit quality factors contributing to evidence strength banding.

    Each flag describes observation packaging quality — not learner ability.
    """

    observation_completeness: bool
    response_validity: bool
    confidence_supplied: bool
    low_hint_usage: bool
    low_retry_count: bool
    timing_available: bool
    question_coverage: bool
    structural_consistency: bool
    heavy_scaffolding: bool
    single_item_only: bool

    def _validate(self) -> None:
        for name in (
            "observation_completeness",
            "response_validity",
            "confidence_supplied",
            "low_hint_usage",
            "low_retry_count",
            "timing_available",
            "question_coverage",
            "structural_consistency",
            "heavy_scaffolding",
            "single_item_only",
        ):
            value = getattr(self, name)
            if not isinstance(value, bool):
                raise AssessmentInvariantViolation(
                    f"{name} must be a bool",
                    invariant=f"EvidenceStrengthFactors.{name}.type",
                )

    def quality_points(self) -> int:
        """Count positive quality factors (excludes forced-thin markers)."""
        return sum(
            (
                self.observation_completeness,
                self.response_validity,
                self.confidence_supplied,
                self.low_hint_usage,
                self.low_retry_count,
                self.timing_available,
                self.question_coverage,
                self.structural_consistency,
            )
        )

    def to_strength(self) -> EvidenceStrength:
        """Map factors to thin / moderate / strong (SCORING_MODEL §8)."""
        if self.heavy_scaffolding or (
            self.single_item_only and not self.observation_completeness
        ):
            return EvidenceStrength.thin()
        points = self.quality_points()
        if (
            points >= _STRONG_MIN_POINTS
            and self.question_coverage
            and self.low_hint_usage
            and not self.heavy_scaffolding
        ):
            return EvidenceStrength.strong()
        if points >= _MODERATE_MIN_POINTS and not self.heavy_scaffolding:
            return EvidenceStrength.moderate()
        if self.single_item_only:
            return EvidenceStrength.thin()
        return EvidenceStrength.thin()


def _dimensions_of(observation) -> EvidenceDimensions | None:
    return observation.dimensions


def _is_structurally_complete(dimensions: EvidenceDimensions | None) -> bool:
    if dimensions is None:
        return False
    return (
        dimensions.confidence is not None
        or dimensions.response_time_ms is not None
        or dimensions.correctness is not None
        or bool(dimensions.misconception_tags)
        or dimensions.hints_used > 0
        or dimensions.retries > 0
    )


def _is_response_valid(observation, dimensions: EvidenceDimensions | None) -> bool:
    provenance = dict(observation.provenance or {})
    if provenance.get("abandoned") or provenance.get("skipped"):
        return False
    if dimensions is not None and dimensions.correctness in {
        AttemptOutcome.ABANDONED,
        AttemptOutcome.SKIPPED,
    }:
        return False
    payload = provenance.get("response_payload")
    if isinstance(payload, dict) and payload:
        return True
    if dimensions is not None and dimensions.correctness is not None:
        return dimensions.correctness not in {
            AttemptOutcome.UNCODED,
            AttemptOutcome.ABANDONED,
            AttemptOutcome.SKIPPED,
        }
    return False


def derive_strength_factors(
    collection: ObservationCollection,
    *,
    expected_question_count: int | None = None,
) -> EvidenceStrengthFactors:
    """Derive strength factors from packaged observation quality (deterministic)."""
    if not isinstance(collection, ObservationCollection):
        raise AssessmentInvariantViolation(
            "collection must be an ObservationCollection",
            invariant="derive_strength_factors.collection.type",
        )
    question_obs = collection.question_observations()
    if not question_obs:
        return EvidenceStrengthFactors(
            observation_completeness=False,
            response_validity=False,
            confidence_supplied=False,
            low_hint_usage=False,
            low_retry_count=False,
            timing_available=False,
            question_coverage=False,
            structural_consistency=False,
            heavy_scaffolding=False,
            single_item_only=True,
        )

    dims_list = [_dimensions_of(o) for o in question_obs]
    complete_flags = [_is_structurally_complete(d) for d in dims_list]
    validity_flags = [
        _is_response_valid(o, d) for o, d in zip(question_obs, dims_list, strict=True)
    ]

    hint_values = [
        (
            d.hints_used
            if d is not None
            else int((o.provenance or {}).get("hints_used", 0))
        )
        for o, d in zip(question_obs, dims_list, strict=True)
    ]
    retry_values = [
        (d.retries if d is not None else int((o.provenance or {}).get("retries", 0)))
        for o, d in zip(question_obs, dims_list, strict=True)
    ]
    confidence_flags = [
        (
            d.confidence is not None
            if d is not None
            else (o.provenance or {}).get("confidence") is not None
        )
        for o, d in zip(question_obs, dims_list, strict=True)
    ]
    timing_flags = [
        (
            d.response_time_ms is not None
            if d is not None
            else (o.provenance or {}).get("response_time_ms") is not None
        )
        for o, d in zip(question_obs, dims_list, strict=True)
    ]

    distinct_questions = len(collection.distinct_question_ids())
    single_item_only = distinct_questions < _MULTI_QUESTION_MIN

    avg_hints = sum(hint_values) / len(hint_values)
    avg_retries = sum(retry_values) / len(retry_values)
    heavy_scaffolding = avg_hints >= _HEAVY_HINTS or avg_retries >= _HIGH_RETRIES

    observation_completeness = all(complete_flags) or (
        sum(complete_flags) / len(complete_flags) >= 0.75
    )
    response_validity = all(validity_flags) or (
        sum(validity_flags) / len(validity_flags) >= 0.75
    )
    confidence_supplied = sum(confidence_flags) / len(confidence_flags) >= 0.5
    timing_available = sum(timing_flags) / len(timing_flags) >= 0.5
    low_hint_usage = avg_hints < _HEAVY_HINTS
    low_retry_count = avg_retries < _HIGH_RETRIES

    if expected_question_count is not None and expected_question_count > 0:
        question_coverage = (
            distinct_questions >= _MULTI_QUESTION_MIN
            and distinct_questions >= max(1, expected_question_count // 2)
        )
    else:
        question_coverage = distinct_questions >= _MULTI_QUESTION_MIN

    # Structural consistency: similar completeness / validity profile across items.
    structural_consistency = (
        len(question_obs) >= 2
        and (all(complete_flags) or not any(complete_flags))
        and (all(validity_flags) or sum(validity_flags) in {0, len(validity_flags)})
    )

    # Also count session-summary presence as mild completeness signal (not mastery).
    has_summary = any(
        o.kind is ObservationKind.QUIZ_COMPLETED for o in collection.observations
    )
    if has_summary and observation_completeness is False and any(complete_flags):
        observation_completeness = True

    return EvidenceStrengthFactors(
        observation_completeness=observation_completeness,
        response_validity=response_validity,
        confidence_supplied=confidence_supplied,
        low_hint_usage=low_hint_usage,
        low_retry_count=low_retry_count,
        timing_available=timing_available,
        question_coverage=question_coverage,
        structural_consistency=structural_consistency,
        heavy_scaffolding=heavy_scaffolding,
        single_item_only=single_item_only,
    )


def calculate_evidence_strength(
    collection: ObservationCollection,
    *,
    expected_question_count: int | None = None,
) -> EvidenceStrength:
    """Calculate deterministic evidence strength for an observation collection."""
    return derive_strength_factors(
        collection, expected_question_count=expected_question_count
    ).to_strength()

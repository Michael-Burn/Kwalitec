"""ObservationInterpreter — map present evidence dimensions to observations."""

from __future__ import annotations

from app.application.reasoning.builders.observation_builder import ObservationBuilder
from app.domain.reasoning.observations.category import ObservationCategory
from app.domain.reasoning.observations.observation import EducationalObservation
from application.assessment.evidence.dto import EvidenceBundleDTO, EvidenceItemDTO


class ObservationInterpreter:
    """Interpret one evidence item into zero-or-more educational observations.

    Only emits observations for dimensions that are explicitly present.
    Never invents missing educational data. Never estimates mastery.
    """

    def interpret_item(
        self,
        item: EvidenceItemDTO,
        *,
        bundle: EvidenceBundleDTO,
        builder: ObservationBuilder,
    ) -> tuple[EducationalObservation, ...]:
        evidence_reference = (
            f"evidence_bundle:{bundle.bundle_id}:{item.item_id}"
        )
        source_observation_id = (item.observation_id or "").strip()
        question_reference = item.question_id
        observations: list[EducationalObservation] = []

        if item.correctness is not None and str(item.correctness).strip():
            observations.append(
                builder.build(
                    category=ObservationCategory.OBSERVED_CORRECTNESS,
                    value={"correctness": str(item.correctness).strip()},
                    evidence_reference=evidence_reference,
                    source_observation_id=source_observation_id,
                    question_reference=question_reference,
                )
            )

        if item.confidence is not None:
            observations.append(
                builder.build(
                    category=ObservationCategory.OBSERVED_CONFIDENCE,
                    value={"confidence": int(item.confidence)},
                    evidence_reference=evidence_reference,
                    source_observation_id=source_observation_id,
                    question_reference=question_reference,
                )
            )

        if item.misconception_tags:
            tags = tuple(
                tag.strip()
                for tag in item.misconception_tags
                if tag is not None and str(tag).strip()
            )
            if tags:
                observations.append(
                    builder.build(
                        category=ObservationCategory.OBSERVED_MISCONCEPTION_INDICATORS,
                        value={"misconception_tags": tags},
                        evidence_reference=evidence_reference,
                        source_observation_id=source_observation_id,
                        question_reference=question_reference,
                    )
                )

        # Retries are always present as an int on the DTO (default 0) — emit only
        # when the item actually recorded persistence effort (retries > 0) OR when
        # correctness is present (structured response attempt). Prefer explicit
        # presence: emit retries when correctness is coded (response occurred).
        if item.correctness is not None and str(item.correctness).strip():
            observations.append(
                builder.build(
                    category=ObservationCategory.OBSERVED_RESPONSE_PERSISTENCE,
                    value={"retries": int(item.retries)},
                    evidence_reference=evidence_reference,
                    source_observation_id=source_observation_id,
                    question_reference=question_reference,
                )
            )
            observations.append(
                builder.build(
                    category=ObservationCategory.OBSERVED_HINT_DEPENDENCY,
                    value={"hints_used": int(item.hints_used)},
                    evidence_reference=evidence_reference,
                    source_observation_id=source_observation_id,
                    question_reference=question_reference,
                )
            )

        if item.response_time_ms is not None:
            observations.append(
                builder.build(
                    category=ObservationCategory.OBSERVED_TIMING_PROFILE,
                    value={"response_time_ms": int(item.response_time_ms)},
                    evidence_reference=evidence_reference,
                    source_observation_id=source_observation_id,
                    question_reference=question_reference,
                )
            )

        return tuple(observations)

    def interpret_bundle_summary(
        self,
        bundle: EvidenceBundleDTO,
        *,
        builder: ObservationBuilder,
    ) -> tuple[EducationalObservation, ...]:
        """Bundle-level coverage and consistency observations from summary facts."""
        evidence_reference = f"evidence_bundle:{bundle.bundle_id}"
        summary = bundle.summary
        observations: list[EducationalObservation] = []

        observations.append(
            builder.build(
                category=ObservationCategory.OBSERVED_COVERAGE,
                value={
                    "observation_count": summary.observation_count,
                    "question_observation_count": summary.question_observation_count,
                    "distinct_question_count": summary.distinct_question_count,
                    "evidence_strength": bundle.evidence_strength,
                },
                evidence_reference=evidence_reference,
                source_observation_id="",
                question_reference=None,
            )
        )

        observations.append(
            builder.build(
                category=ObservationCategory.OBSERVED_CONSISTENCY,
                value={
                    "correctness_counts": dict(summary.correctness_counts or {}),
                    "hint_total": summary.hint_total,
                    "retry_total": summary.retry_total,
                    "confidence_supplied_count": summary.confidence_supplied_count,
                    "timing_available_count": summary.timing_available_count,
                    "misconception_tag_count": summary.misconception_tag_count,
                },
                evidence_reference=evidence_reference,
                source_observation_id="",
                question_reference=None,
            )
        )
        return tuple(observations)

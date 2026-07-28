"""ObservationBuilder — deterministic EducationalObservation construction."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.reasoning.interpretation.versions import (
    INTERPRETATION_PROVENANCE_PREFIX,
    INTERPRETATION_VERSION,
)
from app.domain.reasoning.interpretation.context import InterpretationContext
from app.domain.reasoning.observations.category import (
    ObservationCategory,
    parse_observation_category,
)
from app.domain.reasoning.observations.observation import EducationalObservation


class ObservationBuilder:
    """Build immutable educational observations without inventing missing facts."""

    def __init__(
        self,
        *,
        context: InterpretationContext,
        learning_objective_reference: str,
        concept_reference: str,
        recorded_at: datetime | None = None,
    ) -> None:
        self._context = context
        self._learning_objective_reference = learning_objective_reference.strip()
        self._concept_reference = (concept_reference or "").strip()
        self._recorded_at = recorded_at or datetime.now(UTC).replace(tzinfo=None)
        self._seen_ids: set[str] = set()

    @property
    def seen_ids(self) -> frozenset[str]:
        return frozenset(self._seen_ids)

    def build(
        self,
        *,
        category: ObservationCategory | str,
        value: Any,
        evidence_reference: str,
        source_observation_id: str = "",
        question_reference: str | None = None,
        extra_traceability: dict[str, Any] | None = None,
    ) -> EducationalObservation:
        """Create one observation; reject duplicate ids within this builder."""
        resolved_category = parse_observation_category(category)
        observation_id = self._observation_id(
            category=resolved_category,
            evidence_reference=evidence_reference,
            source_observation_id=source_observation_id,
        )
        if observation_id in self._seen_ids:
            from app.domain.reasoning.interpretation.errors import (
                DuplicateInterpretedObservation,
            )

            raise DuplicateInterpretedObservation(
                f"duplicate interpreted observation: {observation_id!r}"
            )
        self._seen_ids.add(observation_id)

        context = self._context
        traceability: dict[str, Any] = {
            "reasoning_request_id": context.reasoning_request_id,
            "evidence_bundle_id": context.evidence_bundle_id,
            "session_id": context.session_id,
            "correlation_id": context.correlation_id,
            "packaging_version": context.packaging_version,
            "interpreter_version": context.interpreter_version,
            "source_observation_id": source_observation_id,
            "question_reference": question_reference,
            "category": resolved_category.value,
        }
        if extra_traceability:
            traceability.update(extra_traceability)

        return EducationalObservation(
            observation_id=observation_id,
            evidence_reference=evidence_reference.strip(),
            learning_objective_reference=self._learning_objective_reference,
            concept_reference=self._concept_reference,
            category=resolved_category,
            value=value,
            provenance=(
                f"{INTERPRETATION_PROVENANCE_PREFIX}:"
                f"{context.session_id}:{context.evidence_bundle_id}"
            ),
            interpretation_version=INTERPRETATION_VERSION,
            recorded_at=self._recorded_at,
            reasoning_request_id=context.reasoning_request_id,
            evidence_bundle_id=context.evidence_bundle_id,
            session_id=context.session_id,
            correlation_id=context.correlation_id,
            source_observation_id=source_observation_id,
            question_reference=question_reference,
            traceability=traceability,
        )

    @staticmethod
    def _observation_id(
        *,
        category: ObservationCategory,
        evidence_reference: str,
        source_observation_id: str,
    ) -> str:
        """Deterministic id from evidence reference + category (+ source obs)."""
        base = source_observation_id.strip() or evidence_reference.strip()
        return f"eo:{base}:{category.value}"

"""EvidenceInterpreter — orchestrate deterministic evidence interpretation."""

from __future__ import annotations

import uuid
from collections.abc import Collection
from datetime import UTC, datetime

from app.application.reasoning.builders.observation_builder import ObservationBuilder
from app.application.reasoning.dto.interpretation_dto import InterpretationRequestDTO
from app.application.reasoning.interpretation.observation_interpreter import (
    ObservationInterpreter,
)
from app.application.reasoning.interpretation.validator import (
    validate_evidence_for_interpretation,
)
from app.application.reasoning.interpretation.versions import (
    INTERPRETATION_VERSION,
    SUPPORTED_PACKAGING_VERSIONS,
)
from app.domain.reasoning.interpretation.context import InterpretationContext
from app.domain.reasoning.interpretation.result import InterpretationResult
from app.domain.reasoning.observations.observation import EducationalObservation
from app.domain.reasoning.observations.observation_set import EducationalObservationSet
from application.assessment.evidence.dto import EvidenceBundleDTO


class EvidenceInterpreter:
    """Interpret a validated EvidenceBundle into an EducationalObservationSet.

    Interpretation only. No Twin updates. No mastery. No recommendations.
    """

    def __init__(
        self,
        *,
        observation_interpreter: ObservationInterpreter | None = None,
        supported_versions: Collection[str] | None = None,
        interpreter_version: str = INTERPRETATION_VERSION,
    ) -> None:
        self._observation_interpreter = (
            observation_interpreter or ObservationInterpreter()
        )
        self._supported_versions = (
            frozenset(supported_versions)
            if supported_versions is not None
            else SUPPORTED_PACKAGING_VERSIONS
        )
        self._interpreter_version = interpreter_version

    def interpret(
        self,
        request: InterpretationRequestDTO,
        *,
        interpreted_at: datetime | None = None,
    ) -> InterpretationResult:
        """Validate and interpret evidence into an immutable observation set."""
        if request is None:
            from app.application.reasoning.interpretation.errors import (
                UnsupportedEvidenceSchema,
            )

            raise UnsupportedEvidenceSchema("interpretation request is null")
        if not (request.correlation_id or "").strip():
            from app.application.reasoning.interpretation.errors import (
                BrokenEvidenceReference,
            )

            raise BrokenEvidenceReference("missing correlation_id")

        bundle = validate_evidence_for_interpretation(
            request.bundle, supported_versions=self._supported_versions
        )
        when = interpreted_at or datetime.now(UTC).replace(tzinfo=None)
        reasoning_request_id = (
            (request.reasoning_request_id or "").strip()
            or f"rrq-{uuid.uuid4().hex[:16]}"
        )
        context = InterpretationContext.create(
            reasoning_request_id=reasoning_request_id,
            evidence_bundle_id=bundle.bundle_id,
            session_id=bundle.session_id,
            packaging_version=bundle.metadata.packaging_version,
            correlation_id=request.correlation_id.strip(),
            interpreter_version=self._interpreter_version,
        )
        lo_ref, concept_ref = _curriculum_refs(bundle)
        builder = ObservationBuilder(
            context=context,
            learning_objective_reference=lo_ref,
            concept_reference=concept_ref,
            recorded_at=when,
        )

        observations: list[EducationalObservation] = []
        for item in bundle.items:
            observations.extend(
                self._observation_interpreter.interpret_item(
                    item, bundle=bundle, builder=builder
                )
            )
        observations.extend(
            self._observation_interpreter.interpret_bundle_summary(
                bundle, builder=builder
            )
        )

        observation_set = EducationalObservationSet(
            set_id=f"eos:{bundle.bundle_id}:{reasoning_request_id}",
            observations=tuple(observations),
            interpretation_version=self._interpreter_version,
            evidence_bundle_id=bundle.bundle_id,
            reasoning_request_id=reasoning_request_id,
        )
        return InterpretationResult(
            context=context,
            observation_set=observation_set,
            interpreted_at=when,
        )

    def interpret_bundle(
        self,
        bundle: EvidenceBundleDTO,
        *,
        correlation_id: str,
        reasoning_request_id: str | None = None,
        interpreted_at: datetime | None = None,
    ) -> InterpretationResult:
        """Convenience wrapper around ``interpret``."""
        return self.interpret(
            InterpretationRequestDTO(
                bundle=bundle,
                correlation_id=correlation_id,
                reasoning_request_id=reasoning_request_id,
            ),
            interpreted_at=interpreted_at,
        )


def _curriculum_refs(bundle: EvidenceBundleDTO) -> tuple[str, str]:
    lo_ids = tuple(
        oid.strip()
        for oid in (bundle.metadata.learning_objective_ids or ())
        if (oid or "").strip()
    )
    concept_ids = tuple(
        cid.strip()
        for cid in (bundle.metadata.concept_ids or ())
        if (cid or "").strip()
    )
    return lo_ids[0], (concept_ids[0] if concept_ids else "")

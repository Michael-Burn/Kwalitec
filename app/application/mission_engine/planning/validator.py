"""Validate PlanningBatch before Mission persistence.

Rejects invalid plans explicitly. Never silently repairs or invents missing
learner state.
"""

from __future__ import annotations

from collections.abc import Collection

from app.application.mission_engine.planning.versions import (
    SUPPORTED_DECISION_VERSIONS_FOR_PLANNING,
    SUPPORTED_PLANNING_VERSIONS,
)
from app.domain.mission.planning.activity_type import (
    KNOWN_PLANNING_ACTIVITY_TYPES,
    PlanningActivityType,
)
from app.domain.mission.planning.batch import PlanningBatch
from app.domain.mission.planning.candidate import MissionCandidateProjection

REQUIRED_PROVENANCE_KEYS = frozenset(
    {
        "decision_id",
        "decision_version",
        "twin_version",
        "evidence_bundle_id",
        "educational_observation_ids",
        "reasoning_request_id",
        "assessment_session_id",
        "correlation_id",
        "planning_version",
    }
)


class PlanningValidator:
    """Fail-closed validation for Twin→Mission planning."""

    def __init__(
        self,
        *,
        supported_planning_versions: Collection[str] | None = None,
        supported_decision_versions: Collection[str] | None = None,
        existing_request_ids: Collection[str] | None = None,
        existing_candidate_ids: Collection[str] | None = None,
    ) -> None:
        self._supported_planning_versions = (
            frozenset(supported_planning_versions)
            if supported_planning_versions is not None
            else SUPPORTED_PLANNING_VERSIONS
        )
        self._supported_decision_versions = (
            frozenset(supported_decision_versions)
            if supported_decision_versions is not None
            else SUPPORTED_DECISION_VERSIONS_FOR_PLANNING
        )
        self._existing_request_ids = frozenset(existing_request_ids or ())
        self._existing_candidate_ids = frozenset(existing_candidate_ids or ())

    def validate(self, batch: PlanningBatch) -> PlanningBatch:
        """Validate and return the same batch, or raise explicitly."""
        if batch is None:
            from app.domain.mission.planning.errors import InvalidPlanningSchema

            raise InvalidPlanningSchema("planning batch is null")

        if batch.planning_version not in self._supported_planning_versions:
            from app.domain.mission.planning.errors import UnsupportedPlanningContract

            raise UnsupportedPlanningContract(
                f"unsupported planning version: {batch.planning_version!r}"
            )

        if batch.context.decision_version not in self._supported_decision_versions:
            from app.domain.mission.planning.errors import InvalidDecisionVersion

            raise InvalidDecisionVersion(
                f"invalid decision version for planning: "
                f"{batch.context.decision_version!r}"
            )

        if batch.context.twin_version < 1:
            from app.domain.mission.planning.errors import UnknownTwinVersion

            raise UnknownTwinVersion(
                f"unknown twin version: {batch.context.twin_version!r}"
            )

        request_id = batch.context.mission_request_id
        if request_id in self._existing_request_ids:
            from app.domain.mission.planning.errors import DuplicateMissionRequest

            raise DuplicateMissionRequest(
                f"duplicate mission request: {request_id!r}"
            )

        seen: set[str] = set()
        for cand in batch.candidates:
            self._validate_candidate(cand)
            if cand.candidate_id in seen:
                from app.domain.mission.planning.errors import DuplicateMissionRequest

                raise DuplicateMissionRequest(
                    f"duplicate candidate: {cand.candidate_id!r}"
                )
            if cand.candidate_id in self._existing_candidate_ids:
                from app.domain.mission.planning.errors import DuplicateMissionRequest

                raise DuplicateMissionRequest(
                    f"candidate already planned: {cand.candidate_id!r}"
                )
            seen.add(cand.candidate_id)

        return batch

    def _validate_candidate(self, cand: MissionCandidateProjection) -> None:
        if cand.activity_type.value not in KNOWN_PLANNING_ACTIVITY_TYPES:
            from app.domain.mission.planning.errors import PlanningRejected

            raise PlanningRejected(
                f"unknown activity type: {cand.activity_type!r}"
            )

        if cand.planning_version not in self._supported_planning_versions:
            from app.domain.mission.planning.errors import UnsupportedPlanningContract

            raise UnsupportedPlanningContract(
                f"unsupported planning version: {cand.planning_version!r}"
            )

        decision_version = cand.reference.decision_version
        if decision_version not in self._supported_decision_versions:
            from app.domain.mission.planning.errors import InvalidDecisionVersion

            raise InvalidDecisionVersion(
                f"invalid decision version: {decision_version!r}"
            )

        self._validate_provenance(cand)
        self._validate_references(cand)

    def _validate_provenance(self, cand: MissionCandidateProjection) -> None:
        from app.domain.mission.planning.errors import (
            IncompleteProvenance,
            MissingProvenance,
        )

        provenance = dict(cand.provenance or {})
        missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in provenance]
        if missing:
            raise IncompleteProvenance(
                f"missing provenance keys {missing} on {cand.candidate_id!r}"
            )

        ref = cand.reference
        if not (ref.decision_id or "").strip():
            raise MissingProvenance("missing decision_id")
        if not (ref.decision_version or "").strip():
            raise MissingProvenance("missing decision_version")
        if not (ref.evidence_bundle_id or "").strip():
            raise MissingProvenance("missing evidence_bundle_id")
        if not ref.educational_observation_ids:
            raise MissingProvenance("missing educational_observation_ids")
        if not (ref.reasoning_request_id or "").strip():
            raise MissingProvenance("missing reasoning_request_id")
        if not (ref.assessment_session_id or "").strip():
            raise MissingProvenance("missing assessment_session_id")
        if not (ref.correlation_id or "").strip():
            raise MissingProvenance("missing correlation_id")
        if not (ref.planning_version or "").strip():
            raise MissingProvenance("missing planning_version")
        if ref.twin_version < 1:
            raise MissingProvenance("invalid twin_version")

        obs_ids = provenance.get("educational_observation_ids")
        if not isinstance(obs_ids, list | tuple) or not obs_ids:
            raise IncompleteProvenance(
                "provenance educational_observation_ids must be non-empty"
            )

    def _validate_references(self, cand: MissionCandidateProjection) -> None:
        from app.domain.mission.planning.errors import (
            BrokenConceptReference,
            BrokenLearningObjectiveReference,
        )

        if not (cand.concept_id or "").strip():
            raise BrokenConceptReference(
                f"broken concept reference on {cand.candidate_id!r}"
            )

        if cand.activity_type is PlanningActivityType.CONFIDENCE_PRACTICE:
            lo = (cand.learning_objective_id or "").strip() or (
                cand.reference.learning_objective_reference or ""
            ).strip()
            if not lo:
                raise BrokenLearningObjectiveReference(
                    f"missing learning objective on {cand.candidate_id!r}"
                )

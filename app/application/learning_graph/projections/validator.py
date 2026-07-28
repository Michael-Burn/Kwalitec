"""Validate ProjectionBatch before Graph persistence.

Rejects invalid projections explicitly. Never silently repairs or invents
missing relationships.
"""

from __future__ import annotations

from collections.abc import Collection

from app.application.learning_graph.projections.versions import (
    SUPPORTED_DECISION_VERSIONS_FOR_PROJECTION,
    SUPPORTED_PROJECTION_VERSIONS,
)
from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.relationship_type import (
    KNOWN_PROJECTION_RELATIONSHIP_TYPES,
    ProjectionRelationshipType,
)

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
        "projection_version",
    }
)


class ProjectionValidator:
    """Fail-closed validation for Twin→Graph relationship projections."""

    def __init__(
        self,
        *,
        supported_projection_versions: Collection[str] | None = None,
        supported_decision_versions: Collection[str] | None = None,
        existing_projection_ids: Collection[str] | None = None,
    ) -> None:
        self._supported_projection_versions = (
            frozenset(supported_projection_versions)
            if supported_projection_versions is not None
            else SUPPORTED_PROJECTION_VERSIONS
        )
        self._supported_decision_versions = (
            frozenset(supported_decision_versions)
            if supported_decision_versions is not None
            else SUPPORTED_DECISION_VERSIONS_FOR_PROJECTION
        )
        self._existing_projection_ids = frozenset(existing_projection_ids or ())

    def validate(self, batch: ProjectionBatch) -> ProjectionBatch:
        """Validate and return the same batch, or raise explicitly."""
        if batch is None:
            from app.domain.learning_graph.projections.errors import (
                InvalidProjectionSchema,
            )

            raise InvalidProjectionSchema("projection batch is null")

        if batch.projection_version not in self._supported_projection_versions:
            from app.domain.learning_graph.projections.errors import (
                UnsupportedProjectionVersion,
            )

            raise UnsupportedProjectionVersion(
                f"unsupported projection version: {batch.projection_version!r}"
            )

        if batch.context.decision_version not in self._supported_decision_versions:
            from app.domain.learning_graph.projections.errors import (
                InvalidDecisionVersion,
            )

            raise InvalidDecisionVersion(
                f"invalid decision version for projection: "
                f"{batch.context.decision_version!r}"
            )

        seen: set[str] = set()
        for rel in batch.relationships:
            self._validate_relationship(rel)
            if rel.projection_id in seen:
                from app.domain.learning_graph.projections.errors import (
                    DuplicateProjection,
                )

                raise DuplicateProjection(
                    f"duplicate projection: {rel.projection_id!r}"
                )
            if rel.projection_id in self._existing_projection_ids:
                from app.domain.learning_graph.projections.errors import (
                    DuplicateProjection,
                )

                raise DuplicateProjection(
                    f"projection already applied: {rel.projection_id!r}"
                )
            seen.add(rel.projection_id)

        return batch

    def _validate_relationship(self, rel: RelationshipProjection) -> None:
        if rel.relationship_type.value not in KNOWN_PROJECTION_RELATIONSHIP_TYPES:
            from app.domain.learning_graph.projections.errors import (
                UnknownProjectionRelationshipType,
            )

            raise UnknownProjectionRelationshipType(
                f"unknown relationship type: {rel.relationship_type!r}"
            )

        if rel.projection_version not in self._supported_projection_versions:
            from app.domain.learning_graph.projections.errors import (
                UnsupportedProjectionVersion,
            )

            raise UnsupportedProjectionVersion(
                f"unsupported projection version: {rel.projection_version!r}"
            )

        decision_version = rel.reference.decision_version
        if decision_version not in self._supported_decision_versions:
            from app.domain.learning_graph.projections.errors import (
                InvalidDecisionVersion,
            )

            raise InvalidDecisionVersion(
                f"invalid decision version: {decision_version!r}"
            )

        self._validate_provenance(rel)
        self._validate_endpoints(rel)

    def _validate_provenance(self, rel: RelationshipProjection) -> None:
        from app.domain.learning_graph.projections.errors import (
            BrokenProjectionProvenance,
            IncompleteProjectionProvenance,
        )

        provenance = dict(rel.provenance or {})
        missing = [k for k in REQUIRED_PROVENANCE_KEYS if k not in provenance]
        if missing:
            raise IncompleteProjectionProvenance(
                f"missing provenance keys {missing} on {rel.projection_id!r}"
            )

        ref = rel.reference
        if not (ref.decision_id or "").strip():
            raise BrokenProjectionProvenance("missing decision_id")
        if not (ref.decision_version or "").strip():
            raise BrokenProjectionProvenance("missing decision_version")
        if not (ref.evidence_bundle_id or "").strip():
            raise BrokenProjectionProvenance("missing evidence_bundle_id")
        if not ref.educational_observation_ids:
            raise BrokenProjectionProvenance("missing educational_observation_ids")
        if not (ref.reasoning_request_id or "").strip():
            raise BrokenProjectionProvenance("missing reasoning_request_id")
        if not (ref.assessment_session_id or "").strip():
            raise BrokenProjectionProvenance("missing assessment_session_id")
        if not (ref.correlation_id or "").strip():
            raise BrokenProjectionProvenance("missing correlation_id")
        if not (ref.projection_version or "").strip():
            raise BrokenProjectionProvenance("missing projection_version")
        if ref.twin_version < 1:
            raise BrokenProjectionProvenance("invalid twin_version")

        obs_ids = provenance.get("educational_observation_ids")
        if not isinstance(obs_ids, list | tuple) or not obs_ids:
            raise IncompleteProjectionProvenance(
                "provenance educational_observation_ids must be non-empty"
            )

    def _validate_endpoints(self, rel: RelationshipProjection) -> None:
        from app.domain.learning_graph.projections.errors import (
            BrokenConceptReference,
            MissingLearningObjective,
        )

        rel_type = rel.relationship_type
        if rel_type in {
            ProjectionRelationshipType.STUDENT_CONCEPT,
            ProjectionRelationshipType.LEARNING_OBJECTIVE_CONCEPT,
            ProjectionRelationshipType.CONCEPT_CONCEPT,
            ProjectionRelationshipType.PREREQUISITE,
            ProjectionRelationshipType.DEPENDENCY,
        }:
            concept = (rel.to_ref or "").strip()
            if rel_type is ProjectionRelationshipType.STUDENT_CONCEPT:
                concept = (rel.to_ref or "").strip()
            elif rel_type is ProjectionRelationshipType.LEARNING_OBJECTIVE_CONCEPT:
                concept = (rel.to_ref or "").strip()
            elif rel_type in {
                ProjectionRelationshipType.CONCEPT_CONCEPT,
                ProjectionRelationshipType.PREREQUISITE,
                ProjectionRelationshipType.DEPENDENCY,
            }:
                if not (rel.from_ref or "").strip() or not (rel.to_ref or "").strip():
                    raise BrokenConceptReference(
                        f"broken concept endpoints on {rel.projection_id!r}"
                    )
                return
            if not concept:
                raise BrokenConceptReference(
                    f"broken concept reference on {rel.projection_id!r}"
                )

        if rel_type in {
            ProjectionRelationshipType.STUDENT_LEARNING_OBJECTIVE,
            ProjectionRelationshipType.LEARNING_OBJECTIVE_CONCEPT,
        }:
            lo = (
                (rel.to_ref or "").strip()
                if rel_type is ProjectionRelationshipType.STUDENT_LEARNING_OBJECTIVE
                else (rel.from_ref or "").strip()
            )
            if not lo:
                raise MissingLearningObjective(
                    f"missing learning objective on {rel.projection_id!r}"
                )

        if rel_type is ProjectionRelationshipType.STUDENT_MISCONCEPTION:
            if not (rel.to_ref or "").strip():
                raise BrokenConceptReference(
                    f"missing misconception reference on {rel.projection_id!r}"
                )

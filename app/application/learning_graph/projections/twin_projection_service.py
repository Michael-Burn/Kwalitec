"""TwinProjectionService — project validated Twin decisions into the Learning Graph.

Pipeline:
  EducationalDecisionSet (+ Twin)
    → RelationshipBuilder
    → ProjectionBatch
    → ProjectionValidator
    → GraphProjection + factual events
    → ProjectionPersistenceService
    → STOP

Does not modify Twin belief, Mission, Tutor, Assessment, or ReasoningService.
Does not store independent mastery. Never invents missing relationships.
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.learning_graph.projections.persistence import (
    ProjectionPersistenceService,
)
from app.application.learning_graph.projections.relationship_builder import (
    RelationshipBuilder,
)
from app.application.learning_graph.projections.validator import ProjectionValidator
from app.application.learning_graph.projections.versions import PROJECTION_VERSION
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.projections.batch import ProjectionBatch
from app.domain.learning_graph.projections.context import ProjectionContext
from app.domain.learning_graph.projections.events import (
    GraphProjectionCreated,
    GraphProjectionSkipped,
    GraphProjectionUpdated,
)
from app.domain.learning_graph.projections.projection import GraphProjection
from app.domain.learning_graph.projections.relationship import RelationshipProjection
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin


class TwinProjectionService:
    """Deterministic Twin → Learning Graph projection (AP-002D4)."""

    def __init__(
        self,
        *,
        persistence: ProjectionPersistenceService | None = None,
        validator: ProjectionValidator | None = None,
    ) -> None:
        self._persistence = persistence or ProjectionPersistenceService()
        self._validator = validator

    @property
    def persistence(self) -> ProjectionPersistenceService:
        return self._persistence

    def project(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        graph: LearningGraph | None = None,
        graph_id: str | None = None,
        projected_at: datetime | None = None,
        persist: bool = True,
        allow_idempotent_skip: bool = True,
    ) -> ProjectionResult:
        """Project Twin decisions into Graph relationships.

        Args:
            twin: Authoritative learner Twin after belief update.
            decision_set: Validated educational decisions to project.
            graph: Optional existing Learning Graph (structure owner).
            graph_id: Explicit graph id when graph is not supplied.
            projected_at: Deterministic timestamp for replay.
            persist: Persist into the projection ledger when True.
            allow_idempotent_skip: When True, duplicate projection ids emit
                GraphProjectionSkipped instead of raising DuplicateProjection.

        Returns:
            ProjectionResult with batch, graph projection, and factual events.
        """
        when = projected_at or datetime.now(UTC).replace(tzinfo=None)
        resolved_graph_id = self._resolve_graph_id(
            twin=twin, graph=graph, graph_id=graph_id
        )
        context = ProjectionContext(
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            graph_id=resolved_graph_id,
            reasoning_request_id=decision_set.context.reasoning_request_id,
            evidence_bundle_id=decision_set.context.evidence_bundle_id,
            session_id=decision_set.context.session_id,
            correlation_id=decision_set.context.correlation_id,
            projection_version=PROJECTION_VERSION,
            decision_version=decision_set.decision_version,
            twin_version=twin.version,
            decision_set_id=decision_set.set_id,
        )

        existing_ids = self._persistence.existing_projection_ids(
            twin_id=twin.twin_id, graph_id=resolved_graph_id
        )
        builder = RelationshipBuilder(context=context, created_at=when)

        relationships: list[RelationshipProjection] = []
        skipped_decision_ids: list[str] = []
        events: list[
            GraphProjectionCreated | GraphProjectionUpdated | GraphProjectionSkipped
        ] = []

        for decision in decision_set.decisions:
            built = builder.build_from_decision(decision)
            if not built:
                skipped_decision_ids.append(decision.decision_id)
                events.append(
                    GraphProjectionSkipped(
                        event_id=(
                            f"ev-skip:{decision.decision_id}:{PROJECTION_VERSION}"
                        ),
                        graph_id=resolved_graph_id,
                        twin_id=twin.twin_id,
                        decision_id=decision.decision_id,
                        reason_code="non_projectable_decision",
                        occurred_at=when,
                        projection_version=PROJECTION_VERSION,
                    )
                )
                continue

            for rel in built:
                if rel.projection_id in existing_ids:
                    if allow_idempotent_skip:
                        events.append(
                            GraphProjectionSkipped(
                                event_id=(
                                    f"ev-skip:{rel.projection_id}:{PROJECTION_VERSION}"
                                ),
                                graph_id=resolved_graph_id,
                                twin_id=twin.twin_id,
                                decision_id=decision.decision_id,
                                reason_code="duplicate_projection",
                                occurred_at=when,
                                projection_version=PROJECTION_VERSION,
                                projection_id=rel.projection_id,
                            )
                        )
                        if decision.decision_id not in skipped_decision_ids:
                            skipped_decision_ids.append(decision.decision_id)
                        continue
                    from app.domain.learning_graph.projections.errors import (
                        DuplicateProjection,
                    )

                    raise DuplicateProjection(
                        f"projection already applied: {rel.projection_id!r}"
                    )

                prior = self._persistence.get_relationship(
                    twin_id=twin.twin_id,
                    graph_id=resolved_graph_id,
                    projection_id=rel.projection_id,
                )
                relationships.append(rel)
                if prior is None:
                    events.append(
                        GraphProjectionCreated(
                            event_id=(
                                f"ev-create:{rel.projection_id}:{PROJECTION_VERSION}"
                            ),
                            projection_id=rel.projection_id,
                            graph_id=resolved_graph_id,
                            twin_id=twin.twin_id,
                            decision_id=decision.decision_id,
                            relationship_type=rel.relationship_type.value,
                            occurred_at=when,
                            projection_version=PROJECTION_VERSION,
                        )
                    )
                else:
                    events.append(
                        GraphProjectionUpdated(
                            event_id=(
                                f"ev-update:{rel.projection_id}:{PROJECTION_VERSION}"
                            ),
                            projection_id=rel.projection_id,
                            graph_id=resolved_graph_id,
                            twin_id=twin.twin_id,
                            decision_id=decision.decision_id,
                            relationship_type=rel.relationship_type.value,
                            occurred_at=when,
                            projection_version=PROJECTION_VERSION,
                        )
                    )

        batch = ProjectionBatch(
            batch_id=(
                f"gpb:{context.reasoning_request_id}:"
                f"{context.evidence_bundle_id}:{context.twin_version}"
            ),
            relationships=tuple(relationships),
            context=context,
            projection_version=PROJECTION_VERSION,
            skipped_decision_ids=tuple(skipped_decision_ids),
        )

        validator = self._validator or ProjectionValidator(
            existing_projection_ids=(
                () if allow_idempotent_skip else existing_ids
            )
        )
        validated = validator.validate(batch)

        graph_projection = GraphProjection(
            projection_id=(
                f"gpg:{context.reasoning_request_id}:"
                f"{context.evidence_bundle_id}:v{context.twin_version}"
            ),
            graph_id=resolved_graph_id,
            twin_id=twin.twin_id,
            context=context,
            relationships=validated.relationships,
            projection_version=PROJECTION_VERSION,
            twin_version=twin.version,
            created_at=when,
            prior_projection_ids=tuple(sorted(existing_ids)),
            provenance={
                "decision_set_id": decision_set.set_id,
                "decision_ids": list(decision_set.decision_ids),
                "evidence_bundle_id": context.evidence_bundle_id,
                "reasoning_request_id": context.reasoning_request_id,
                "assessment_session_id": context.session_id,
                "correlation_id": context.correlation_id,
                "twin_version": twin.version,
                "projection_version": PROJECTION_VERSION,
            },
        )

        result = ProjectionResult(
            context=context,
            batch=validated,
            graph_projection=graph_projection,
            projected_at=when,
            events=tuple(events),
        )
        if persist:
            return self._persistence.persist(result)
        return result

    def replay(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        graph: LearningGraph | None = None,
        graph_id: str | None = None,
        projected_at: datetime | None = None,
    ) -> ProjectionResult:
        """Replay projection into a fresh store (determinism / audit)."""
        replay_service = TwinProjectionService(
            persistence=self._persistence.clone_empty(),
            validator=self._validator,
        )
        return replay_service.project(
            twin,
            decision_set,
            graph=graph,
            graph_id=graph_id,
            projected_at=projected_at,
            persist=True,
            allow_idempotent_skip=True,
        )

    def graph_snapshot(
        self, *, twin_id: str, graph_id: str
    ) -> dict:
        """Deterministic ledger snapshot for identical-Twin identical-Graph checks."""
        return self._persistence.snapshot(twin_id=twin_id, graph_id=graph_id)

    @staticmethod
    def _resolve_graph_id(
        *,
        twin: StudentDigitalTwin,
        graph: LearningGraph | None,
        graph_id: str | None,
    ) -> str:
        if graph is not None:
            if graph.twin_id != twin.twin_id:
                from app.domain.learning_graph.projections.errors import (
                    ProjectionRejected,
                )

                raise ProjectionRejected(
                    f"graph twin_id {graph.twin_id!r} does not match Twin "
                    f"{twin.twin_id!r}"
                )
            return graph.graph_id
        if graph_id and graph_id.strip():
            return graph_id.strip()
        # Deterministic default graph id when structure not yet materialised.
        return f"lg-proj-{twin.twin_id}"

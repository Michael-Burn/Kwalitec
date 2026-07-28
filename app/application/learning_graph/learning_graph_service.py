"""LearningGraphService — lifecycle (create / load / sync) for SDT-003."""

from __future__ import annotations

import uuid
from datetime import UTC, datetime

from app.application.learning_graph.graph_builder_service import (
    LearningGraphBuilderService,
    project_mastery_onto_graph,
)
from app.application.learning_graph.persistence import LearningGraphPersistenceService
from app.application.learning_graph.projections.twin_projection_service import (
    TwinProjectionService,
)
from app.domain.educational_reasoning.reasoning_context import CurriculumEvidenceBundle
from app.domain.learning_graph.graph_update import GraphUpdate, GraphUpdateKind
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.learning_graph.projections.result import ProjectionResult
from app.domain.reasoning.decisions.decision_set import EducationalDecisionSet
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db
from app.models.learning_graph import LgLearningGraph


class LearningGraphService:
    """Create, load, and synchronise learner-specific Learning Graphs.

    One graph per Student Digital Twin. Twin remains canonical for mastery.
    """

    def __init__(
        self,
        *,
        persistence: LearningGraphPersistenceService | None = None,
        builder: LearningGraphBuilderService | None = None,
        twin_projection: TwinProjectionService | None = None,
    ) -> None:
        self._persistence = persistence or LearningGraphPersistenceService()
        self._builder = builder or LearningGraphBuilderService()
        self._twin_projection = twin_projection or TwinProjectionService()

    def create_for_twin(
        self,
        twin: StudentDigitalTwin,
        *,
        graph_id: str | None = None,
        created_at: datetime | None = None,
        persist: bool = True,
    ) -> LearningGraph:
        """Create an empty Learning Graph for a Twin (idempotent per twin_id)."""
        existing = self._persistence.load_graph_for_twin(twin.twin_id)
        if existing is not None:
            return existing

        now = created_at or datetime.now(UTC).replace(tzinfo=None)
        graph = LearningGraph.create(
            graph_id=graph_id or f"lg-{uuid.uuid4().hex[:16]}",
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            created_at=now,
        )
        update = GraphUpdate(
            update_id=f"lgu-{uuid.uuid4().hex[:16]}",
            graph_id=graph.graph_id,
            twin_id=graph.twin_id,
            kind=GraphUpdateKind.CREATE,
            summary="Learning Graph created for Twin",
            created_at=now,
            payload=(("twin_id", twin.twin_id),),
        )
        graph = graph.with_structure(update=update, updated_at=now)
        self._persistence.replace_structure(graph)
        if persist:
            db.session.commit()
        else:
            db.session.flush()
        return graph

    def get(self, graph_id: str) -> LearningGraph | None:
        return self._persistence.load_graph(graph_id)

    def get_for_twin(self, twin_id: str) -> LearningGraph | None:
        return self._persistence.load_graph_for_twin(twin_id)

    def get_or_create_for_twin(
        self,
        twin: StudentDigitalTwin,
        *,
        persist: bool = True,
    ) -> LearningGraph:
        graph = self.get_for_twin(twin.twin_id)
        if graph is not None:
            return graph
        return self.create_for_twin(twin, persist=persist)

    def sync(
        self,
        twin: StudentDigitalTwin,
        *,
        evidence: CurriculumEvidenceBundle | None = None,
        computed_at: datetime | None = None,
        persist: bool = True,
        record_snapshot: bool = True,
    ) -> LearningGraph:
        """Ensure graph exists and sync structure from Twin + curriculum evidence."""
        graph = self.get_or_create_for_twin(twin, persist=persist)
        synced = self._builder.sync_from_twin_and_evidence(
            graph,
            twin=twin,
            evidence=evidence,
            computed_at=computed_at,
            record_snapshot=record_snapshot,
        )
        synced = self._builder.ensure_stub_nodes(
            synced, computed_at=computed_at or synced.updated_at
        )
        synced = synced.recompute_prerequisite_statuses()
        if persist:
            self._persistence.replace_structure(synced)
            db.session.flush()
        return synced

    def refresh_projections(
        self,
        twin: StudentDigitalTwin,
        *,
        computed_at: datetime | None = None,
        persist: bool = True,
    ) -> LearningGraph | None:
        """Update mastery projections after Twin reasoning without rebuilding edges."""
        graph = self.get_for_twin(twin.twin_id)
        if graph is None:
            return None
        updated = project_mastery_onto_graph(
            graph,
            twin.mastery,
            observations=twin.observations,
            computed_at=computed_at,
        )
        if persist:
            self._persistence.replace_structure(updated)
            db.session.flush()
        return updated

    def project_twin_decisions(
        self,
        twin: StudentDigitalTwin,
        decision_set: EducationalDecisionSet,
        *,
        computed_at: datetime | None = None,
        persist: bool = True,
        refresh_mastery_cache: bool = True,
    ) -> ProjectionResult:
        """Project validated Twin decisions into Learning Graph relationships.

        AP-002D4 entry point. Stores educational relationships only — Twin remains
        the authority for mastery belief. Does not invoke Reasoning, Mission, or Tutor.
        """
        graph = self.get_or_create_for_twin(twin, persist=persist)
        result = self._twin_projection.project(
            twin,
            decision_set,
            graph=graph,
            projected_at=computed_at,
            persist=True,
            allow_idempotent_skip=True,
        )

        when = computed_at or result.projected_at
        update = GraphUpdate(
            update_id=(
                f"lgu-proj-{result.graph_projection.projection_id}"[:64]
            ),
            graph_id=graph.graph_id,
            twin_id=graph.twin_id,
            kind=GraphUpdateKind.PROJECT_FROM_TWIN_DECISIONS,
            summary=(
                f"Projected Twin decisions: relationships={result.relationship_count} "
                f"created={result.created_count} skipped={result.skipped_count}"
            ),
            created_at=when,
            payload=(
                ("projection_id", result.graph_projection.projection_id),
                ("relationship_count", str(result.relationship_count)),
                ("decision_set_id", decision_set.set_id),
                ("twin_version", str(twin.version)),
                ("projection_version", result.context.projection_version),
            ),
        )
        graph = graph.with_structure(update=update, updated_at=when)

        if refresh_mastery_cache:
            # Cache Twin belief for traversal only — Twin remains SoT.
            graph = project_mastery_onto_graph(
                graph,
                twin.mastery,
                observations=twin.observations,
                computed_at=when,
            )

        if persist:
            self._persistence.replace_structure(graph)
            db.session.flush()
        return result

    def list_for_student(self, student_id: str) -> list[LearningGraph]:
        rows = LgLearningGraph.query.filter_by(student_id=student_id).all()
        graphs: list[LearningGraph] = []
        for row in rows:
            graph = self._persistence.load_graph(row.graph_id)
            if graph is not None:
                graphs.append(graph)
        return graphs

    def as_dict(self, graph: LearningGraph) -> dict:
        return self._persistence.graph_as_dict(graph)

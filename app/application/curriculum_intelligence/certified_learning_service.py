"""EI-002B — Certified Learning Experience facade for Student Runtime.

Coordinates mission generation, knowledge graph, tutor context, progress,
adaptive signals, and Curriculum Observatory without introducing new
educational reasoning. Consumes published certified packages only.
"""

from __future__ import annotations

from typing import Any

from app.application.curriculum_intelligence.certified_adaptive_learning_service import (  # noqa: E501
    CertifiedAdaptiveLearningService,
)
from app.application.curriculum_intelligence.certified_mission_engine import (
    CertifiedMissionEngine,
)
from app.application.curriculum_intelligence.certified_progress_engine import (
    CertifiedProgressEngine,
)
from app.application.curriculum_intelligence.certified_tutor_context_service import (
    CertifiedTutorContextService,
)
from app.application.curriculum_intelligence.curriculum_observatory import (
    CurriculumObservatory,
)
from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
    extract_provenance,
)
from app.application.curriculum_intelligence.ports.generation_store_port import (
    GenerationStorePort,
)
from app.application.curriculum_studio_foundation.authority import (
    PublishedCurriculumAuthority,
)
from app.domain.curriculum_intelligence.certified_learning import (
    AdaptiveLearningPlan,
    CertifiedMissionSpec,
    CertifiedProgressSnapshot,
    CertifiedTutorContext,
    CurriculumObservatoryReport,
    CurriculumProvenanceRef,
    LearnerKnowledgeGraph,
)


class CertifiedLearningService:
    """Student-facing integration surface over certified published curriculum."""

    SERVICE_ID = "certified_learning"
    SERVICE_VERSION = "1.0.0"

    def __init__(
        self,
        *,
        authority: PublishedCurriculumAuthority | None = None,
        store: GenerationStorePort | None = None,
        graph_builder: LearnerKnowledgeGraphBuilder | None = None,
        mission_engine: CertifiedMissionEngine | None = None,
        tutor_context: CertifiedTutorContextService | None = None,
        progress_engine: CertifiedProgressEngine | None = None,
        adaptive: CertifiedAdaptiveLearningService | None = None,
        observatory: CurriculumObservatory | None = None,
    ) -> None:
        self._authority = authority or PublishedCurriculumAuthority()
        self._graph = graph_builder or LearnerKnowledgeGraphBuilder()
        self._missions = mission_engine or CertifiedMissionEngine(
            graph_builder=self._graph
        )
        self._tutor = tutor_context or CertifiedTutorContextService(
            graph_builder=self._graph
        )
        self._progress = progress_engine or CertifiedProgressEngine(
            graph_builder=self._graph
        )
        self._adaptive = adaptive or CertifiedAdaptiveLearningService(
            progress_engine=self._progress,
            graph_builder=self._graph,
        )
        self._store = store
        self._observatory = observatory
        if observatory is None and store is not None:
            self._observatory = CurriculumObservatory(store)

    def load_package(self, subject_code: str) -> dict[str, Any]:
        """Load the active published package and assert certified authority."""
        snap = self._authority.get_active(subject_code)
        if snap is None:
            raise ValueError(
                f"no active published curriculum for subject {subject_code!r}"
            )
        assert_certified_package(snap.package)
        return snap.package

    def provenance(self, package: dict[str, Any]) -> CurriculumProvenanceRef:
        return extract_provenance(package)

    def knowledge_graph(self, package: dict[str, Any]) -> LearnerKnowledgeGraph:
        return self._graph.build(package)

    def generate_daily_mission(
        self,
        package: dict[str, Any],
        **kwargs: Any,
    ) -> CertifiedMissionSpec:
        return self._missions.generate(package, **kwargs)

    def tutor_context(
        self,
        package: dict[str, Any],
        **kwargs: Any,
    ) -> CertifiedTutorContext:
        return self._tutor.build(package, **kwargs)

    def progress(
        self,
        package: dict[str, Any],
        **kwargs: Any,
    ) -> CertifiedProgressSnapshot:
        return self._progress.snapshot(package, **kwargs)

    def adaptive_plan(
        self,
        package: dict[str, Any],
        **kwargs: Any,
    ) -> AdaptiveLearningPlan:
        return self._adaptive.plan(package, **kwargs)

    def observatory_for_chain(self, chain_id: str) -> CurriculumObservatoryReport:
        if self._observatory is None:
            raise RuntimeError("Curriculum Observatory requires a GenerationStore")
        return self._observatory.report_for_chain(chain_id)

    def observatory_for_workspace(
        self, workspace_id: str
    ) -> CurriculumObservatoryReport:
        if self._observatory is None:
            raise RuntimeError("Curriculum Observatory requires a GenerationStore")
        return self._observatory.report_for_workspace(workspace_id)

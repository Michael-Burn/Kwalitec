"""EducationalReasoningService — application facade for SDT-002.

Pipeline:
  Observation
    → Retrieve Supporting Curriculum Evidence
    → Apply Educational Rules (EducationalReasoningEngine + RuleRegistry)
    → Generate Educational Inference
    → (caller updates Student Digital Twin)
    → Record Reasoning History
"""

from __future__ import annotations

from datetime import UTC, datetime

from app.application.curriculum_retrieval.curriculum_retrieval_service import (
    CurriculumRetrievalService,
)
from app.application.educational_reasoning.curriculum_evidence_service import (
    CurriculumEvidenceService,
)
from app.application.educational_reasoning.persistence import (
    ReasoningPersistenceService,
)
from app.application.learning_graph.learning_graph_service import LearningGraphService
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_engine import (
    ENGINE_VERSION,
    EducationalReasoningEngine,
)
from app.domain.educational_reasoning.reasoning_result import ReasoningResult
from app.domain.educational_reasoning.rule_registry import (
    RuleRegistry,
    build_default_registry,
)
from app.domain.learning_graph.learning_graph import LearningGraph
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation
from app.domain.student_digital_twin.student_digital_twin import StudentDigitalTwin
from app.extensions import db


class EducationalReasoningService:
    """Run the Educational Reasoning Engine and persist auditable history."""

    def __init__(
        self,
        *,
        engine: EducationalReasoningEngine | None = None,
        registry: RuleRegistry | None = None,
        evidence: CurriculumEvidenceService | None = None,
        persistence: ReasoningPersistenceService | None = None,
        retrieval: CurriculumRetrievalService | None = None,
        learning_graph: LearningGraphService | None = None,
    ) -> None:
        retrieval_svc = retrieval or CurriculumRetrievalService()
        reg = registry or build_default_registry()
        self._engine = engine or EducationalReasoningEngine(registry=reg)
        self._evidence = evidence or CurriculumEvidenceService(retrieval=retrieval_svc)
        self._persistence = persistence or ReasoningPersistenceService()
        self._learning_graph = learning_graph or LearningGraphService()

    @property
    def engine(self) -> EducationalReasoningEngine:
        return self._engine

    @property
    def registry(self) -> RuleRegistry:
        return self._engine.registry

    @property
    def learning_graph_service(self) -> LearningGraphService:
        return self._learning_graph

    def reason_for_twin(
        self,
        twin: StudentDigitalTwin,
        *,
        triggered_by: str = "manual",
        observation_ids: tuple[str, ...] | None = None,
        persist: bool = True,
        computed_at: datetime | None = None,
        learning_graph: LearningGraph | None = None,
    ) -> ReasoningResult:
        """Full pipeline for a Twin: evidence → graph sync → rules → history."""
        now = computed_at or datetime.now(UTC).replace(tzinfo=None)
        obs_ids = observation_ids or tuple(o.observation_id for o in twin.observations)

        # Stage 2 — retrieve supporting curriculum evidence (CIP-003 only).
        evidence = self._evidence.retrieve_for_reasoning(
            observations=twin.observations,
            mastery=twin.mastery,
            workspace_id=twin.student.workspace_id,
            subject_code=twin.student.subject_code,
        )

        # Stage 2b — sync Learning Graph so rules can traverse prerequisites.
        graph = learning_graph
        if graph is None:
            graph = self._learning_graph.sync(
                twin,
                evidence=evidence,
                computed_at=now,
                persist=persist,
                record_snapshot=persist,
            )

        context = ReasoningContext(
            twin_id=twin.twin_id,
            student_id=twin.student.student_id,
            workspace_id=twin.student.workspace_id,
            subject_code=twin.student.subject_code,
            observations=twin.observations,
            observation_ids=obs_ids,
            prior_mastery=twin.mastery or MasteryMap.empty(),
            curriculum_evidence=evidence,
            triggered_by=triggered_by,
            computed_at=now,
            learning_graph=graph,
        )

        # Stages 3–4 — apply rules, generate inferences.
        result = self._engine.reason(context)

        # Stage 6 — record reasoning history (immutable).
        if persist:
            self._persistence.persist_result(result)
            db.session.flush()

        return result

    def reason_from_observations(
        self,
        *,
        twin_id: str,
        student_id: str,
        workspace_id: str,
        subject_code: str,
        observations: tuple[Observation, ...],
        prior_mastery: MasteryMap | None = None,
        triggered_by: str = "manual",
        persist: bool = False,
        computed_at: datetime | None = None,
        learning_graph: LearningGraph | None = None,
    ) -> ReasoningResult:
        """Run engine without a Twin aggregate (pure / unit-test friendly)."""
        now = computed_at or datetime.now(UTC).replace(tzinfo=None)
        mastery = prior_mastery or MasteryMap.empty()
        evidence = self._evidence.retrieve_for_reasoning(
            observations=observations,
            mastery=mastery,
            workspace_id=workspace_id,
            subject_code=subject_code,
        )
        context = ReasoningContext(
            twin_id=twin_id,
            student_id=student_id,
            workspace_id=workspace_id,
            subject_code=subject_code,
            observations=observations,
            observation_ids=tuple(o.observation_id for o in observations),
            prior_mastery=mastery,
            curriculum_evidence=evidence,
            triggered_by=triggered_by,
            computed_at=now,
            learning_graph=learning_graph,
        )
        result = self._engine.reason(context)
        if persist:
            self._persistence.persist_result(result)
            db.session.flush()
        return result

    def list_rules(self) -> tuple[dict[str, str], ...]:
        return self.registry.list_rules()

    @staticmethod
    def engine_version() -> str:
        return ENGINE_VERSION

"""EducationalOrchestrator — application composition over Education OS engines.

Architecture Source
    EDU-003.6 Educational Orchestration Layer

Coordinates StudentEducationalState, EducationalEvidence, KnowledgeGraph,
MasteryEstimator, and RecommendationEngine without introducing coupling
between those bounded contexts. Owns workflow ordering and result
composition only — never educational reasoning.
"""

from __future__ import annotations

from datetime import datetime

from application.education.orchestration.dto.educational_evaluation import (
    EducationalEvaluation,
)
from application.education.orchestration.dto.interaction_requests import (
    CheckpointRequest,
    InteractionKind,
    QuestionAnswerRequest,
    ReflectionRequest,
    SessionCompletionRequest,
    StudentInteractionRequest,
)
from application.education.orchestration.ports.assessment_publisher import (
    AssessmentPublisher,
)
from application.education.orchestration.ports.evidence_provider import (
    EvidenceProvider,
)
from application.education.orchestration.ports.knowledge_graph_provider import (
    KnowledgeGraphProvider,
)
from application.education.orchestration.ports.recommendation_publisher import (
    RecommendationPublisher,
)
from application.education.orchestration.ports.student_state_provider import (
    StudentStateProvider,
)
from application.education.orchestration.result_composer import (
    compose_snapshot,
    compose_summary,
    project_decisions,
)
from application.education.orchestration.stages import (
    EVALUATION_PIPELINE,
    INTERACTION_PIPELINE,
    OrchestrationStage,
)
from application.errors import ApplicationError, NotFoundError
from application.ports.uuid_generator import UUIDGenerator
from domain.education.educational_evidence.aggregates.educational_evidence import (
    EducationalEvidence,
)
from domain.education.educational_evidence.enums import LearningEnvironmentKind
from domain.education.educational_evidence.ids import EvidenceId
from domain.education.educational_evidence.value_objects.evidence_source import (
    EvidenceSource,
)
from domain.education.educational_evidence.value_objects.learning_environment import (
    LearningEnvironment,
)
from domain.education.foundation.errors import EducationalDomainError
from domain.education.knowledge_graph.aggregates.knowledge_graph import (
    KnowledgeGraph,
)
from domain.education.mastery_estimation.aggregates.mastery_assessment import (
    MasteryAssessment,
)
from domain.education.mastery_estimation.engines.mastery_estimator import (
    MasteryEstimator,
)
from domain.education.mastery_estimation.ids import AssessmentId
from domain.education.recommendation_engine.aggregates.recommendation_set import (
    RecommendationSet,
)
from domain.education.recommendation_engine.engines.recommendation_engine import (
    RecommendationEngine,
)
from domain.education.recommendation_engine.ids import RecommendationSetId
from domain.education.student_state.aggregates.student_educational_state import (
    StudentEducationalState,
)

_FAILURE_CODES = {
    "invalid_request": "invalid_request",
    "student_state_unavailable": "student_state_unavailable",
    "knowledge_graph_unavailable": "knowledge_graph_unavailable",
    "evidence_unavailable": "evidence_unavailable",
    "evidence_record_failed": "evidence_record_failed",
    "mastery_estimation_failed": "mastery_estimation_failed",
    "recommendation_failed": "recommendation_failed",
    "assessment_publish_failed": "assessment_publish_failed",
    "recommendation_publish_failed": "recommendation_publish_failed",
    "domain_invariant": "domain_invariant",
    "coordination_failed": "coordination_failed",
}


class EducationalOrchestrator:
    """Coordinate Education OS engines for one student workflow turn.

    Injected ports supply inputs and publish outputs. Domain engines are
    invoked in lawful order. Failures become ``EducationalEvaluation``
    results — never HTTP exceptions, retries, or logging.
    """

    def __init__(
        self,
        *,
        student_state_provider: StudentStateProvider,
        evidence_provider: EvidenceProvider,
        knowledge_graph_provider: KnowledgeGraphProvider,
        uuid_generator: UUIDGenerator,
        assessment_publisher: AssessmentPublisher | None = None,
        recommendation_publisher: RecommendationPublisher | None = None,
        mastery_estimator: type[MasteryEstimator] = MasteryEstimator,
        recommendation_engine: type[RecommendationEngine] = RecommendationEngine,
    ) -> None:
        self._student_state_provider = student_state_provider
        self._evidence_provider = evidence_provider
        self._knowledge_graph_provider = knowledge_graph_provider
        self._uuid_generator = uuid_generator
        self._assessment_publisher = assessment_publisher
        self._recommendation_publisher = recommendation_publisher
        self._mastery_estimator = mastery_estimator
        self._recommendation_engine = recommendation_engine

    # --- public workflow operations -----------------------------------------

    def process_student_interaction(
        self, request: StudentInteractionRequest
    ) -> EducationalEvaluation:
        """Dispatch a generic interaction to the specialised workflow."""
        try:
            if request.kind is InteractionKind.QUESTION_ANSWER:
                assert request.question_answer is not None
                return self.process_question_answer(request.question_answer)
            if request.kind is InteractionKind.REFLECTION:
                assert request.reflection is not None
                return self.process_reflection(request.reflection)
            if request.kind is InteractionKind.CHECKPOINT:
                assert request.checkpoint is not None
                return self.process_checkpoint(request.checkpoint)
            if request.kind is InteractionKind.SESSION_COMPLETION:
                assert request.session_completion is not None
                return self.process_session_completion(request.session_completion)
            return EducationalEvaluation.failed(
                student_id="unknown",
                stages_completed=(),
                failure_code=_FAILURE_CODES["invalid_request"],
                failure_message=f"unsupported interaction kind: {request.kind!r}",
            )
        except ValueError as exc:
            student_id = ""
            try:
                student_id = request.student_id
            except Exception:
                pass
            return EducationalEvaluation.failed(
                student_id=student_id or "unknown",
                stages_completed=(),
                failure_code=_FAILURE_CODES["invalid_request"],
                failure_message=str(exc),
            )

    def process_question_answer(
        self, request: QuestionAnswerRequest
    ) -> EducationalEvaluation:
        """Record a question answer and run the full evaluation pipeline."""
        return self._run_interaction_pipeline(
            student_id=request.student_id,
            occurred_at=request.occurred_at,
            evidence_factory=lambda evidence_id: (
                EducationalEvidence.record_question_answer(
                    EvidenceId(evidence_id),
                    request.student_id,
                    request.occurred_at,
                    EvidenceSource.student_action(request.source_origin),
                    learning_environment=self._environment(
                        request.learning_environment
                    ),
                    competency_id=request.competency_id,
                    is_correct=request.is_correct,
                    subject_id=request.subject_id,
                    mission_id=request.mission_id,
                    learning_episode_id=request.learning_episode_id,
                )
            ),
            evidence_id_override=request.evidence_id,
        )

    def process_reflection(
        self, request: ReflectionRequest
    ) -> EducationalEvaluation:
        """Record a reflection and run the full evaluation pipeline."""
        return self._run_interaction_pipeline(
            student_id=request.student_id,
            occurred_at=request.occurred_at,
            evidence_factory=lambda evidence_id: EducationalEvidence.record_reflection(
                EvidenceId(evidence_id),
                request.student_id,
                request.occurred_at,
                EvidenceSource.student_action(request.source_origin),
                learning_environment=self._environment(request.learning_environment),
                reflection_text=request.reflection_text,
                subject_id=request.subject_id,
                competency_id=request.competency_id,
                mission_id=request.mission_id,
                learning_episode_id=request.learning_episode_id,
            ),
            evidence_id_override=request.evidence_id,
        )

    def process_checkpoint(
        self, request: CheckpointRequest
    ) -> EducationalEvaluation:
        """Record a checkpoint and run the full evaluation pipeline."""
        return self._run_interaction_pipeline(
            student_id=request.student_id,
            occurred_at=request.occurred_at,
            evidence_factory=lambda evidence_id: EducationalEvidence.record_checkpoint(
                EvidenceId(evidence_id),
                request.student_id,
                request.occurred_at,
                EvidenceSource.student_action(request.source_origin),
                learning_environment=self._environment(request.learning_environment),
                checkpoint_id=request.checkpoint_id,
                subject_id=request.subject_id,
            ),
            evidence_id_override=request.evidence_id,
        )

    def process_session_completion(
        self, request: SessionCompletionRequest
    ) -> EducationalEvaluation:
        """Record session completion and run the full evaluation pipeline."""
        return self._run_interaction_pipeline(
            student_id=request.student_id,
            occurred_at=request.occurred_at,
            evidence_factory=lambda evidence_id: (
                EducationalEvidence.record_session_completion(
                    EvidenceId(evidence_id),
                    request.student_id,
                    request.occurred_at,
                    EvidenceSource.student_action(request.source_origin),
                    learning_environment=self._environment(
                        request.learning_environment
                    ),
                    learning_episode_id=request.learning_episode_id,
                    subject_id=request.subject_id,
                )
            ),
            evidence_id_override=request.evidence_id,
        )

    def refresh_recommendations(
        self, student_id: str, *, as_of: datetime
    ) -> EducationalEvaluation:
        """Re-estimate mastery and refresh recommendations without new evidence."""
        return self._run_evaluation_pipeline(
            student_id=student_id,
            evaluated_at=as_of,
            new_evidence=None,
            publish=True,
        )

    def evaluate_student(
        self, student_id: str, *, as_of: datetime
    ) -> EducationalEvaluation:
        """Evaluate student state into an application result without publishing.

        Same educational pipeline as refresh, but skips outbound publishers so
        callers can inspect decisions without side effects.
        """
        return self._run_evaluation_pipeline(
            student_id=student_id,
            evaluated_at=as_of,
            new_evidence=None,
            publish=False,
        )

    # --- pipelines ----------------------------------------------------------

    def _run_interaction_pipeline(
        self,
        *,
        student_id: str,
        occurred_at: datetime,
        evidence_factory,
        evidence_id_override: str | None,
    ) -> EducationalEvaluation:
        stages: list[str] = []
        evidence_id: str | None = None
        try:
            evidence_id_value = (evidence_id_override or "").strip() or (
                self._uuid_generator.new_id()
            )
            new_evidence = evidence_factory(evidence_id_value)
            evidence_id = str(new_evidence.evidence_id)
            self._evidence_provider.record_evidence(new_evidence)
            stages.append(OrchestrationStage.RECORD_EVIDENCE.value)
        except EducationalDomainError as exc:
            return self._fail(
                student_id=student_id,
                stages=stages,
                code=_FAILURE_CODES["domain_invariant"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except ApplicationError as exc:
            return self._fail(
                student_id=student_id,
                stages=stages,
                code=_FAILURE_CODES["evidence_record_failed"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=student_id,
                stages=stages,
                code=_FAILURE_CODES["evidence_record_failed"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        return self._run_evaluation_pipeline(
            student_id=student_id,
            evaluated_at=occurred_at,
            new_evidence=new_evidence,
            publish=True,
            prior_stages=tuple(stages),
            evidence_id=evidence_id,
            expected_pipeline=INTERACTION_PIPELINE,
        )

    def _run_evaluation_pipeline(
        self,
        *,
        student_id: str,
        evaluated_at: datetime,
        new_evidence: EducationalEvidence | None,
        publish: bool,
        prior_stages: tuple[str, ...] = (),
        evidence_id: str | None = None,
        expected_pipeline: tuple[OrchestrationStage, ...] = EVALUATION_PIPELINE,
    ) -> EducationalEvaluation:
        _ = expected_pipeline  # documents lawful order; stages appended below
        stages: list[str] = list(prior_stages)
        cleaned_student_id = (student_id or "").strip()
        if not cleaned_student_id:
            return self._fail(
                student_id="unknown",
                stages=stages,
                code=_FAILURE_CODES["invalid_request"],
                message="student_id is required",
                evidence_id=evidence_id,
            )

        # 1. StudentEducationalState (read)
        try:
            state = self._student_state_provider.get_student_state(cleaned_student_id)
            stages.append(OrchestrationStage.LOAD_STUDENT_STATE.value)
        except NotFoundError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["student_state_unavailable"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except ApplicationError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["student_state_unavailable"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["student_state_unavailable"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        # 2. KnowledgeGraph (read)
        try:
            graph = self._knowledge_graph_provider.get_knowledge_graph(
                cleaned_student_id
            )
            stages.append(OrchestrationStage.LOAD_KNOWLEDGE_GRAPH.value)
        except NotFoundError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["knowledge_graph_unavailable"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except ApplicationError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["knowledge_graph_unavailable"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["knowledge_graph_unavailable"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        # 3. EducationalEvidence (read existing; merge new interaction evidence)
        try:
            existing = self._evidence_provider.list_evidence(cleaned_student_id)
            evidence = self._merge_evidence(existing, new_evidence)
            stages.append(OrchestrationStage.LOAD_EVIDENCE.value)
        except ApplicationError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["evidence_unavailable"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["evidence_unavailable"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        # 4. MasteryEstimator (domain)
        try:
            assessment = self._estimate_mastery(
                state=state,
                evidence=evidence,
                graph=graph,
                assessed_at=evaluated_at,
            )
            stages.append(OrchestrationStage.ESTIMATE_MASTERY.value)
        except EducationalDomainError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["mastery_estimation_failed"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["mastery_estimation_failed"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        # 5. RecommendationEngine (domain)
        try:
            recommendation_set = self._recommend(
                state=state,
                assessment=assessment,
                evidence=evidence,
                graph=graph,
                recommended_at=evaluated_at,
            )
            stages.append(OrchestrationStage.GENERATE_RECOMMENDATIONS.value)
        except EducationalDomainError as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["recommendation_failed"],
                message=exc.message,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["recommendation_failed"],
                message=str(exc),
                evidence_id=evidence_id,
            )

        # 6. Publish (optional)
        if publish and self._assessment_publisher is not None:
            try:
                self._assessment_publisher.publish_assessment(assessment)
                stages.append(OrchestrationStage.PUBLISH_ASSESSMENT.value)
            except ApplicationError as exc:
                return self._fail(
                    student_id=cleaned_student_id,
                    stages=stages,
                    code=_FAILURE_CODES["assessment_publish_failed"],
                    message=exc.message,
                    evidence_id=evidence_id,
                )
            except Exception as exc:
                return self._fail(
                    student_id=cleaned_student_id,
                    stages=stages,
                    code=_FAILURE_CODES["assessment_publish_failed"],
                    message=str(exc),
                    evidence_id=evidence_id,
                )
        elif publish:
            stages.append(OrchestrationStage.PUBLISH_ASSESSMENT.value)

        if publish and self._recommendation_publisher is not None:
            try:
                self._recommendation_publisher.publish_recommendations(
                    recommendation_set
                )
                stages.append(OrchestrationStage.PUBLISH_RECOMMENDATIONS.value)
            except ApplicationError as exc:
                return self._fail(
                    student_id=cleaned_student_id,
                    stages=stages,
                    code=_FAILURE_CODES["recommendation_publish_failed"],
                    message=exc.message,
                    evidence_id=evidence_id,
                )
            except Exception as exc:
                return self._fail(
                    student_id=cleaned_student_id,
                    stages=stages,
                    code=_FAILURE_CODES["recommendation_publish_failed"],
                    message=str(exc),
                    evidence_id=evidence_id,
                )
        elif publish:
            stages.append(OrchestrationStage.PUBLISH_RECOMMENDATIONS.value)

        # 7. Compose application result
        try:
            decisions = project_decisions(recommendation_set)
            summary = compose_summary(
                assessment=assessment,
                recommendation_set=recommendation_set,
                evidence_count=len(evidence),
                evaluated_at=evaluated_at,
                decisions=decisions,
            )
            stage_tuple = (*stages, OrchestrationStage.COMPOSE_RESULT.value)
            snapshot = compose_snapshot(
                student_id=cleaned_student_id,
                evaluated_at=evaluated_at,
                stages_completed=stage_tuple,
                summary=summary,
                decisions=decisions,
                evidence_id=evidence_id,
            )
            return EducationalEvaluation.succeeded(
                student_id=cleaned_student_id,
                stages_completed=stage_tuple,
                summary=summary,
                snapshot=snapshot,
                decisions=decisions,
                evidence_id=evidence_id,
            )
        except Exception as exc:
            return self._fail(
                student_id=cleaned_student_id,
                stages=stages,
                code=_FAILURE_CODES["coordination_failed"],
                message=str(exc),
                evidence_id=evidence_id,
            )

    # --- domain engine delegation -------------------------------------------

    def _estimate_mastery(
        self,
        *,
        state: StudentEducationalState,
        evidence: tuple[EducationalEvidence, ...],
        graph: KnowledgeGraph,
        assessed_at: datetime,
    ) -> MasteryAssessment:
        return self._mastery_estimator.estimate(
            state,
            evidence,
            graph,
            assessment_id=AssessmentId(self._uuid_generator.new_id()),
            assessed_at=assessed_at,
        )

    def _recommend(
        self,
        *,
        state: StudentEducationalState,
        assessment: MasteryAssessment,
        evidence: tuple[EducationalEvidence, ...],
        graph: KnowledgeGraph,
        recommended_at: datetime,
    ) -> RecommendationSet:
        return self._recommendation_engine.recommend(
            state,
            assessment,
            evidence,
            graph,
            set_id=RecommendationSetId(self._uuid_generator.new_id()),
            recommended_at=recommended_at,
        )

    # --- helpers ------------------------------------------------------------

    @staticmethod
    def _environment(kind_value: str) -> LearningEnvironment:
        kind = LearningEnvironmentKind(kind_value.strip())
        return LearningEnvironment.of(kind)

    @staticmethod
    def _merge_evidence(
        existing: tuple[EducationalEvidence, ...],
        new_evidence: EducationalEvidence | None,
    ) -> tuple[EducationalEvidence, ...]:
        if new_evidence is None:
            return tuple(existing)
        new_id = str(new_evidence.evidence_id)
        without_dup = tuple(
            item for item in existing if str(item.evidence_id) != new_id
        )
        return (*without_dup, new_evidence)

    @staticmethod
    def _fail(
        *,
        student_id: str,
        stages: list[str],
        code: str,
        message: str,
        evidence_id: str | None,
    ) -> EducationalEvaluation:
        return EducationalEvaluation.failed(
            student_id=student_id,
            stages_completed=tuple(stages),
            failure_code=code,
            failure_message=message,
            evidence_id=evidence_id,
        )

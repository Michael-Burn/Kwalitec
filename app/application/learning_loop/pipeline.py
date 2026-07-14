"""End-to-end Educational Intelligence learning loop (Capability 4.9.10).

Sequences the frozen Version 1.0 write/read pipeline without educational
algorithms, Twin redesign, or Strategy redesign. Collaborators own their
boundaries; this module only wires and observes operational milestones.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum

from app.application.orchestration.educational_orchestrator import (
    EducationalExperience,
    EducationalOrchestrator,
    ProductContext,
)
from app.application.twin.twin_provider import (
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
)
from app.application.twin_repository.types import TwinScope
from app.application.twin_update.composer import TwinComposer
from app.application.twin_update.coordinator import TwinUpdateCoordinator
from app.application.twin_update.evidence import (
    EVIDENCE_PACKAGE_VERSION_1_0,
    EducationalEvidencePackage,
)
from app.application.twin_update.knowledge_strategy import KnowledgeUpdateStrategy
from app.application.twin_update.protocols import (
    TwinComposerProtocol,
    TwinSuccessorRepositoryProtocol,
    TwinUpdateStrategyProtocol,
)
from app.application.twin_update.result import (
    TwinUpdateFailure,
    TwinUpdateFailureReason,
    TwinUpdateSuccess,
)
from app.domain.decision.constraints import Constraints
from app.domain.decision.history import DecisionHistory
from app.domain.mission.context import MissionExecutionContext
from app.domain.recommendation.context import RecommendationContext
from app.domain.recommendation.recommendation import Recommendation
from app.domain.twin.digital_twin import DigitalTwin

logger = logging.getLogger(__name__)


class LearningLoopFailureReason(str, Enum):
    """Honest learning-loop failure postures — never educational judgements."""

    INVALID_EVIDENCE = "invalid_evidence"
    MISSING_CURRENT_TWIN = "missing_current_twin"
    TWIN_UPDATE_FAILED = "twin_update_failed"
    PROVIDER_FAILURE = "provider_failure"
    EDUCATIONAL_INTELLIGENCE_UNAVAILABLE = "educational_intelligence_unavailable"


@dataclass(frozen=True)
class LearningLoopContext:
    """Caller-supplied product facts for one learning-loop execution.

    Sitting / feasibility / surface wiring only — never educational selection.
    """

    student_id: str
    curriculum_id: int
    constraints: Constraints
    twin_retrieval_context: TwinRetrievalContext | None = None
    product_context: ProductContext | None = None
    twin_scope: TwinScope | None = None
    mission_execution_context: MissionExecutionContext | None = None
    decision_history: DecisionHistory | None = None
    recommendation_context: RecommendationContext | None = None


@dataclass(frozen=True)
class LearningLoopSuccess:
    """Complete learning-loop cargo after write + Provider + Intelligence."""

    successor_twin: DigitalTwin
    twin_update: TwinUpdateSuccess
    experience: EducationalExperience
    recommendation: Recommendation


@dataclass(frozen=True)
class LearningLoopFailure:
    """Honest termination without incomplete educational theatre."""

    reason: LearningLoopFailureReason
    detail: str | None = None
    twin_update_failure: TwinUpdateFailure | None = None
    twin_update_success: TwinUpdateSuccess | None = None


LearningLoopResult = LearningLoopSuccess | LearningLoopFailure


def build_version_1_0_twin_update_coordinator(
    repository: TwinSuccessorRepositoryProtocol,
    *,
    strategies: list[TwinUpdateStrategyProtocol] | None = None,
    composer: TwinComposerProtocol | None = None,
) -> TwinUpdateCoordinator:
    """Wire Version 1.0 Twin Update write path (Knowledge Strategy only).

    Args:
        repository: Twin Repository successor persistence adapter.
        strategies: Optional Strategy catalogue; defaults to Knowledge only.
        composer: Optional Twin Composer; defaults to TwinComposer().

    Returns:
        TwinUpdateCoordinator ready for Evidence-driven succession.
    """
    return TwinUpdateCoordinator(
        strategies=(
            list(strategies)
            if strategies is not None
            else [KnowledgeUpdateStrategy()]
        ),
        composer=composer if composer is not None else TwinComposer(),
        repository=repository,
    )


def build_version_1_0_learning_loop(
    *,
    repository: TwinSuccessorRepositoryProtocol,
    twin_provider: TwinProvider | None = None,
    coordinator: TwinUpdateCoordinator | None = None,
    orchestrator: EducationalOrchestrator | None = None,
) -> EducationalLearningLoop:
    """Wire the Version 1.0 Evidence → Recommendation learning loop.

    Args:
        repository: Shared TwinRepository for write persistence and Provider load.
        twin_provider: Optional TwinProvider; defaults to repository-backed.
        coordinator: Optional write-path Coordinator; defaults to V1.0 Knowledge.
        orchestrator: Optional Educational Orchestrator; defaults to Provider-wired.

    Returns:
        EducationalLearningLoop Integration entry.
    """
    provider = (
        twin_provider
        if twin_provider is not None
        else TwinProvider(repository=repository)  # type: ignore[arg-type]
    )
    write = (
        coordinator
        if coordinator is not None
        else build_version_1_0_twin_update_coordinator(repository)
    )
    read = (
        orchestrator
        if orchestrator is not None
        else EducationalOrchestrator(twin_provider=provider)
    )
    return EducationalLearningLoop(
        twin_provider=provider,
        coordinator=write,
        orchestrator=read,
        repository=repository,
    )


class EducationalLearningLoop:
    """Application Integration: Evidence write path → Intelligence read path.

    Write: Provider (current) → Coordinator → Knowledge → Composer → Repository.
    Read: Provider (successor) → Educational Orchestrator → Recommendation.

    Never interprets Evidence, assembles Twins, persists directly, or selects
    next actions. Never bypasses TwinProvider for Educational Intelligence.
    """

    def __init__(
        self,
        *,
        twin_provider: TwinProvider,
        coordinator: TwinUpdateCoordinator,
        orchestrator: EducationalOrchestrator,
        repository: TwinSuccessorRepositoryProtocol | None = None,
    ) -> None:
        """Inject Collaborators for one Version 1.0 learning loop.

        Args:
            twin_provider: Sole Twin retrieval authority (current + successor).
            coordinator: Twin Update write-path orchestrator.
            orchestrator: Educational Intelligence read-side composition entry.
            repository: Optional Repository handle for tests / observability.
        """
        self._twin_provider = twin_provider
        self._coordinator = coordinator
        self._orchestrator = orchestrator
        self._repository = repository

    @property
    def twin_provider(self) -> TwinProvider:
        """Injected TwinProvider (never bypassed for Intelligence)."""
        return self._twin_provider

    @property
    def coordinator(self) -> TwinUpdateCoordinator:
        """Injected TwinUpdateCoordinator."""
        return self._coordinator

    @property
    def orchestrator(self) -> EducationalOrchestrator:
        """Injected EducationalOrchestrator."""
        return self._orchestrator

    @property
    def repository(self) -> TwinSuccessorRepositoryProtocol | None:
        """Optional injected TwinRepository handle."""
        return self._repository

    def execute(
        self,
        evidence: EducationalEvidencePackage | None,
        *,
        context: LearningLoopContext,
    ) -> LearningLoopResult:
        """Run one complete Version 1.0 learning loop.

        Args:
            evidence: Educational Evidence Package (observational cargo).
            context: Product / session facts for Provider + Intelligence.

        Returns:
            LearningLoopSuccess with Recommendation, or LearningLoopFailure.
            No partial pipeline completion: write failure skips Intelligence;
            Provider failure after persistence yields EI unavailable.
        """
        logger.info("Pipeline started")

        evidence_check = self._accept_evidence(evidence)
        if evidence_check is not None:
            return evidence_check
        assert evidence is not None
        logger.info("Evidence accepted")

        retrieval_context = self._resolve_retrieval_context(evidence, context)
        current = self._twin_provider.retrieve(
            context.student_id,
            context=retrieval_context,
        )
        if isinstance(current, TwinAbsent):
            logger.info("Pipeline failed: missing current twin")
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.MISSING_CURRENT_TWIN,
                detail=current.detail or current.reason.value,
            )

        update_result = self._coordinator.update(
            current,
            evidence,
            scope=context.twin_scope,
        )
        if isinstance(update_result, TwinUpdateFailure):
            return self._map_update_failure(update_result)

        logger.info("Coordinator completed")

        successor = self._twin_provider.retrieve(
            context.student_id,
            context=retrieval_context,
        )
        if isinstance(successor, TwinAbsent):
            logger.info("Pipeline failed: provider failure after persistence")
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.PROVIDER_FAILURE,
                detail=successor.detail or successor.reason.value,
                twin_update_success=update_result,
            )
        logger.info("Provider retrieved")

        logger.info("Educational Intelligence invoked")
        experience = self._orchestrator.build_experience(
            student_id=context.student_id,
            curriculum_id=context.curriculum_id,
            constraints=context.constraints,
            twin_retrieval_context=retrieval_context,
            mission_execution_context=context.mission_execution_context,
            decision_history=context.decision_history,
            recommendation_context=context.recommendation_context,
            product_context=context.product_context,
        )
        if isinstance(experience, TwinAbsent):
            logger.info(
                "Pipeline failed: educational intelligence unavailable"
            )
            return LearningLoopFailure(
                reason=(
                    LearningLoopFailureReason.EDUCATIONAL_INTELLIGENCE_UNAVAILABLE
                ),
                detail=experience.detail or experience.reason.value,
                twin_update_success=update_result,
            )

        recommendation = experience.todays_recommendation
        if not isinstance(recommendation, Recommendation):
            logger.info(
                "Pipeline failed: educational intelligence unavailable"
            )
            return LearningLoopFailure(
                reason=(
                    LearningLoopFailureReason.EDUCATIONAL_INTELLIGENCE_UNAVAILABLE
                ),
                detail="Educational Experience missing Recommendation",
                twin_update_success=update_result,
            )

        logger.info("Pipeline completed")
        return LearningLoopSuccess(
            successor_twin=successor,
            twin_update=update_result,
            experience=experience,
            recommendation=recommendation,
        )

    @staticmethod
    def _accept_evidence(
        evidence: EducationalEvidencePackage | None,
    ) -> LearningLoopFailure | None:
        """Structural Evidence handoff check — never educational correctness."""
        if evidence is None:
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail="Educational Evidence Package is required",
            )
        if not isinstance(evidence, EducationalEvidencePackage):
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail="Evidence payload is not an EducationalEvidencePackage",
            )
        if not evidence.evidence_id.strip():
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail="evidence_id must be present",
            )
        if not evidence.student_id.strip():
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail="student_id must be present",
            )
        if evidence.contract_version.strip() != EVIDENCE_PACKAGE_VERSION_1_0:
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail=(
                    f"unsupported Evidence contract_version: "
                    f"{evidence.contract_version!r}"
                ),
            )
        if not evidence.observed_events:
            return LearningLoopFailure(
                reason=LearningLoopFailureReason.INVALID_EVIDENCE,
                detail="observed_events must be non-empty",
            )
        return None

    @staticmethod
    def _resolve_retrieval_context(
        evidence: EducationalEvidencePackage,
        context: LearningLoopContext,
    ) -> TwinRetrievalContext:
        """Wire TwinRetrievalContext from product + Evidence sitting facts."""
        if context.twin_retrieval_context is not None:
            return context.twin_retrieval_context

        sitting_id = None
        curriculum_key: str | None = str(context.curriculum_id)
        if context.twin_scope is not None:
            sitting_id = context.twin_scope.sitting_id
            curriculum_key = context.twin_scope.curriculum_id or curriculum_key
        elif evidence.sitting_id:
            sitting_id = evidence.sitting_id

        if curriculum_key is None and evidence.curriculum_id:
            curriculum_key = evidence.curriculum_id

        surface = (
            context.product_context.surface_intent
            if context.product_context is not None
            else None
        )
        return TwinRetrievalContext(
            curriculum_id=curriculum_key,
            sitting_id=sitting_id,
            surface_intent=surface,
        )

    @staticmethod
    def _map_update_failure(
        failure: TwinUpdateFailure,
    ) -> LearningLoopFailure:
        """Map Coordinator failure without inventing educational state."""
        if failure.reason is TwinUpdateFailureReason.INVALID_EVIDENCE:
            mapped = LearningLoopFailureReason.INVALID_EVIDENCE
        elif failure.reason is TwinUpdateFailureReason.MISSING_CURRENT_TWIN:
            mapped = LearningLoopFailureReason.MISSING_CURRENT_TWIN
        else:
            mapped = LearningLoopFailureReason.TWIN_UPDATE_FAILED
        logger.info("Pipeline failed: twin update failed")
        return LearningLoopFailure(
            reason=mapped,
            detail=failure.detail or failure.reason.value,
            twin_update_failure=failure,
        )

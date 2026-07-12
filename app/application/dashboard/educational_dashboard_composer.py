"""Educational Dashboard Composer — Stage A product Integration entry.

Coordinates the Twin-first dashboard read path for Presentation:

    TwinProvider → ConstraintBuilder → EducationalOrchestrator
        (CurriculumContextBuilder inside) → DashboardAssembler → DashboardViewModel

Owns Application coordination and honest fallback signalling only. Never scores
readiness, selects next actions, fabricates Twin / Readiness, averages legacy
with Twin factors, or imports Flask / routes / templates / ORM.

When Educational Intelligence cannot produce a truthful Experience, returns
``None`` so Presentation falls back to the legacy recommendation peer.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from app.application.config.feature_flags import (
    FEATURE_FLAGS,
    EducationalIntelligenceFeatureFlags,
)
from app.application.constraints.constraint_builder import (
    ConstraintBuilder,
    ConstraintBuildError,
    ConstraintProductContext,
)
from app.application.dashboard.dashboard_assembler import DashboardAssembler
from app.application.dashboard.dashboard_view_model import DashboardViewModel
from app.application.orchestration.educational_orchestrator import (
    EducationalOrchestrator,
    ProductContext,
)
from app.application.twin.twin_provider import (
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
)

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class DashboardCompositionContext:
    """Authorised product facts for one dashboard EI composition pass.

    Sitting / capacity facts only. Never educational scoring inputs.
    """

    student_id: str
    curriculum_id: int | None = None
    available_minutes: int | None = None
    session_type: str | None = None


class EducationalDashboardComposer:
    """Compose DashboardViewModel for Stage A Educational Intelligence cutover.

    Presentation calls this entry when ``ENABLE_EDUCATIONAL_ORCHESTRATOR`` is
    on. Educational judgement remains in domain owners (ADR-002).
    """

    def __init__(
        self,
        *,
        twin_provider: TwinProvider | None = None,
        constraint_builder: ConstraintBuilder | None = None,
        orchestrator: EducationalOrchestrator | None = None,
        flags: EducationalIntelligenceFeatureFlags | None = None,
    ) -> None:
        """Wire Application adapters for one composition path.

        Args:
            twin_provider: Twin retrieval adapter (default: no persistence source).
            constraint_builder: Constraints constructor from product facts.
            orchestrator: Educational Experience composition entry.
            flags: Optional flag snapshot for tests / staged rollout.
        """
        self._twin_provider = (
            twin_provider if twin_provider is not None else TwinProvider()
        )
        self._constraint_builder = (
            constraint_builder
            if constraint_builder is not None
            else ConstraintBuilder()
        )
        self._orchestrator = (
            orchestrator
            if orchestrator is not None
            else EducationalOrchestrator()
        )
        self._flags = flags if flags is not None else FEATURE_FLAGS

    def compose(
        self,
        context: DashboardCompositionContext,
    ) -> DashboardViewModel | None:
        """Compose Twin-first DashboardViewModel, or ``None`` for legacy fallback.

        Returns ``None`` when:
        - Educational Orchestrator flag is off (Stage A default)
        - Twin is absent / corrupt / unavailable (never fabricate)
        - Curriculum identity is missing
        - Constraint construction, CurriculumContextBuilder, or domain composition fails

        Args:
            context: Authorised student / sitting product facts.

        Returns:
            Immutable DashboardViewModel, or ``None`` to keep the legacy
            recommendation peer as today's recommendation authority.
        """
        if not self._flags.ENABLE_EDUCATIONAL_ORCHESTRATOR:
            return None

        if context.curriculum_id is None:
            logger.info(
                "Educational dashboard fallback: missing curriculum_id for student=%s",
                context.student_id,
            )
            return None

        twin_result = self._twin_provider.retrieve(
            context.student_id,
            context=TwinRetrievalContext(
                curriculum_id=str(context.curriculum_id),
                surface_intent="dashboard",
            ),
        )
        if isinstance(twin_result, TwinAbsent):
            logger.info(
                "Educational dashboard fallback: TwinAbsent reason=%s student=%s",
                twin_result.reason.value,
                context.student_id,
            )
            return None

        try:
            constraints = self._constraint_builder.build(
                ConstraintProductContext(
                    student_id=context.student_id,
                    available_minutes=context.available_minutes,
                    session_type=context.session_type,
                )
            )
            experience = self._orchestrator.build_experience(
                curriculum_id=context.curriculum_id,
                twin=twin_result,
                constraints=constraints,
                product_context=ProductContext(
                    surface_intent="dashboard",
                    cutover_mode="stage_a",
                ),
            )
            return DashboardAssembler.assemble(experience, flags=self._flags)
        except ConstraintBuildError as exc:
            logger.info(
                "Educational dashboard fallback: constraints failed for student=%s: %s",
                context.student_id,
                exc,
            )
            return None
        except Exception as exc:
            # Missing curriculum, domain failure, or builder error — never fabricate.
            logger.info(
                "Educational dashboard fallback: composition failed for student=%s: %s",
                context.student_id,
                exc,
            )
            return None

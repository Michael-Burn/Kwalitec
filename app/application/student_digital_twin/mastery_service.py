"""Mastery inference helpers — delegates to MasteryUpdateRule (SDT-002)."""

from __future__ import annotations

from datetime import UTC, datetime

from app.domain.educational_reasoning.mastery_update import MasteryUpdateRule
from app.domain.educational_reasoning.reasoning_context import (
    CurriculumEvidenceBundle,
    ReasoningContext,
)
from app.domain.student_digital_twin.mastery import MasteryMap
from app.domain.student_digital_twin.observation import Observation


class MasteryService:
    """Derive mastery records from observation outcomes via MasteryUpdateRule."""

    LEARNING_RATE = MasteryUpdateRule.learning_rate
    PRIOR = MasteryUpdateRule.prior

    def recompute(
        self,
        *,
        twin_id: str,
        observations: tuple[Observation, ...],
        prior: MasteryMap | None = None,
    ) -> MasteryMap:
        """Recompute mastery for every concept referenced by observations."""
        now = datetime.now(UTC).replace(tzinfo=None)
        context = ReasoningContext(
            twin_id=twin_id,
            student_id=twin_id,
            workspace_id="",
            subject_code="",
            observations=observations,
            observation_ids=tuple(o.observation_id for o in observations),
            prior_mastery=prior or MasteryMap.empty(),
            curriculum_evidence=CurriculumEvidenceBundle.empty(),
            triggered_by="mastery_service",
            computed_at=now,
        )
        execution = MasteryUpdateRule().apply(context)
        return execution.mastery or MasteryMap.empty()

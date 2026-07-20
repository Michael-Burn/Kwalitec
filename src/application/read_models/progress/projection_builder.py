"""ProgressSummaryProjectionBuilder — project learner state into progress cues.

Forwards Twin / evidence summary scalars. Does not compute mastery, readiness,
or next-action recommendations.
"""

from __future__ import annotations

from application.dto.learner import LearnerStateDTO
from application.read_models.progress.progress_summary_read_model import (
    ProgressSummaryReadModel,
)


class ProgressSummaryProjectionBuilder:
    """Build ``ProgressSummaryReadModel`` from learner-state DTOs."""

    @staticmethod
    def build(state: LearnerStateDTO) -> ProgressSummaryReadModel:
        """Project a learner-state DTO into an immutable progress summary."""
        cues = (
            f"activity:{state.activity_status}",
            f"twin:{state.twin_status}",
            f"concepts:{state.concept_count}",
            f"evidence:{state.evidence_count}",
        )
        return ProgressSummaryReadModel(
            student_id=state.student_id,
            activity_status=state.activity_status,
            twin_status=state.twin_status,
            concept_count=state.concept_count,
            evidence_count=state.evidence_count,
            intervention_count=state.intervention_count,
            progress_cues=cues,
            twin_id=state.twin_id,
        )

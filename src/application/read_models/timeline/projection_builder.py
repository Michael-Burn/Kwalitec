"""TimelineProjectionBuilder — project trajectory / evidence into timeline rows.

Structural ordering for presentation. Does not interpret educational meaning
or modify aggregates.
"""

from __future__ import annotations

from application.dto.evidence import EvidenceHistoryDTO
from application.dto.trajectory import LearningTrajectoryDTO
from application.read_models.timeline.timeline_read_model import (
    TimelineEventReadModel,
    TimelineReadModel,
)


class TimelineProjectionBuilder:
    """Build ``TimelineReadModel`` from trajectory and evidence history DTOs."""

    @staticmethod
    def from_trajectory(trajectory: LearningTrajectoryDTO) -> TimelineReadModel:
        """Project a learning-trajectory DTO into a timeline read model."""
        events = tuple(
            TimelineEventReadModel(
                sequence=point.sequence,
                kind=point.kind,
                label=point.label,
            )
            for point in trajectory.points
        )
        return TimelineReadModel(
            student_id=trajectory.student_id,
            events=events,
            twin_id=trajectory.twin_id,
        )

    @staticmethod
    def from_evidence_history(history: EvidenceHistoryDTO) -> TimelineReadModel:
        """Project evidence history into a chronological timeline read model."""
        events = tuple(
            TimelineEventReadModel(
                sequence=index,
                kind="evidence",
                label=(
                    f"Evidence · {record.strength_level} strength · "
                    f"{record.confidence_level} confidence"
                ),
                occurred_at=record.occurred_at,
            )
            for index, record in enumerate(history.records)
        )
        return TimelineReadModel(
            student_id=history.student_id,
            events=events,
        )

    @staticmethod
    def build(
        *,
        student_id: str,
        events: tuple[TimelineEventReadModel, ...] = (),
        twin_id: str | None = None,
    ) -> TimelineReadModel:
        """Assemble a timeline read model from already-shaped event rows."""
        return TimelineReadModel(
            student_id=student_id.strip(),
            events=events,
            twin_id=twin_id.strip() if twin_id else None,
        )

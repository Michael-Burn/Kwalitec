"""Comparison service — deterministic Twin snapshot deltas."""

from __future__ import annotations

from app.application.student_twin.dto.comparison_snapshot import ComparisonSnapshot
from app.application.student_twin.exceptions import ComparisonError
from app.domain.student_twin.twin_snapshot import TwinSnapshot


class ComparisonService:
    """Compare two Twin snapshots deterministically."""

    @staticmethod
    def compare(
        baseline: TwinSnapshot,
        current: TwinSnapshot,
    ) -> ComparisonSnapshot:
        """Compare mastery / readiness / confidence deltas."""
        if baseline.identity.twin_id != current.identity.twin_id:
            raise ComparisonError("cannot compare snapshots from different twins")
        if current.version.precedes(baseline.version):
            raise ComparisonError("baseline version must not be newer than current")
        return ComparisonSnapshot.create(
            twin_id=baseline.twin_id,
            baseline_version=baseline.version_label,
            current_version=current.version_label,
            mastery_delta=(
                current.mastery.overall_score - baseline.mastery.overall_score
            ),
            readiness_delta=(
                current.readiness.readiness_score - baseline.readiness.readiness_score
            ),
            confidence_delta=(
                current.confidence.overall_score - baseline.confidence.overall_score
            ),
            retention_delta=(
                current.retention.overall_score - baseline.retention.overall_score
            ),
            evidence_added=max(
                0, len(current.history_event_ids) - len(baseline.history_event_ids)
            ),
        )

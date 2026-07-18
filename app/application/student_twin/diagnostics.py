"""Twin diagnostics — integrity inspection without mutation."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.student_twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class TwinDiagnosticsReport:
    """Immutable diagnostics over a Twin instance."""

    twin_id: str
    event_count: int
    topic_count: int
    version_label: str
    has_recommendations: bool
    readiness_score: float
    overall_mastery: float
    issues: tuple[str, ...] = field(default_factory=tuple)


class TwinDiagnostics:
    """Framework-independent Twin health / integrity diagnostics."""

    @staticmethod
    def inspect(twin: DigitalTwin) -> TwinDiagnosticsReport:
        """Inspect Twin integrity without mutating state."""
        issues: list[str] = []
        if twin.history.event_count != twin.evidence_profile.total_events:
            issues.append("evidence_profile_out_of_sync")
        if twin.history.event_count > 0 and twin.mastery.topic_count == 0:
            topic_scoped = any(e.topic_id for e in twin.history.events)
            if topic_scoped:
                issues.append("mastery_not_recalculated")
        for rec in twin.recommendations.recommendations:
            if not rec.rationale:
                issues.append(
                    f"recommendation_missing_rationale:{rec.recommendation_id}"
                )
            if not rec.expected_benefit:
                issues.append(
                    f"recommendation_missing_benefit:{rec.recommendation_id}"
                )
        return TwinDiagnosticsReport(
            twin_id=twin.twin_id,
            event_count=twin.event_count,
            topic_count=twin.mastery.topic_count,
            version_label=twin.version.label,
            has_recommendations=not twin.recommendations.is_empty,
            readiness_score=twin.readiness.readiness_score,
            overall_mastery=twin.mastery.overall_score,
            issues=tuple(issues),
        )

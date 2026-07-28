"""Daily Mission Intelligence application service (ILE-004).

Orchestrates composition and Decision Journal presentation writes.
No HTTP; no Twin; no recommendation ranking.
"""

from __future__ import annotations

from datetime import date
from typing import Any

from app.application.daily_mission_intelligence.dto import (
    DailyMissionIntelligenceSnapshot,
)
from app.domain.daily_mission_intelligence import (
    DailyMissionBrief,
    MissionLifecyclePhase,
)
from app.services.daily_mission_intelligence_service import (
    DailyMissionIntelligenceService,
)


class DailyMissionIntelligenceApplicationService:
    """Application façade for today's primary Mission Intelligence."""

    @staticmethod
    def compose_snapshot(
        *,
        title: str = "",
        summary: str = "",
        why_recommended: str = "",
        timeliness_line: str = "",
        supporting_evidence: tuple[str, ...] | list[str] = (),
        estimated_effort: str = "",
        expected_benefit: str = "",
        suggested_next_action: str = "",
        review_point: str = "",
        completion_loop_line: str = "",
        confidence_label: str = "",
        confidence_basis: str = "",
        uncertainty: str = "",
        honest_refusal: bool = False,
        alternative_titles: tuple[str, ...] | list[str] = (),
        recommendation_key: str = "",
        mission_id: str = "",
        session_id: str = "",
        educational_context: str = "",
        lifecycle_phase: str = MissionLifecyclePhase.PRESENTED.value,
        prior_deferral_note: str = "",
        optimisation_axis: str = "",
    ) -> DailyMissionIntelligenceSnapshot:
        """Compose the Home-facing mission intelligence snapshot."""
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title=title,
            summary=summary,
            why_recommended=why_recommended,
            timeliness_line=timeliness_line,
            supporting_evidence=supporting_evidence,
            estimated_effort=estimated_effort,
            expected_benefit=expected_benefit,
            suggested_next_action=suggested_next_action,
            review_point=review_point,
            completion_loop_line=completion_loop_line,
            confidence_label=confidence_label,
            confidence_basis=confidence_basis,
            uncertainty=uncertainty,
            honest_refusal=honest_refusal,
            alternative_titles=alternative_titles,
            recommendation_key=recommendation_key,
            mission_id=mission_id,
            session_id=session_id,
            educational_context=educational_context,
            lifecycle_phase=lifecycle_phase,
            prior_deferral_note=prior_deferral_note,
            optimisation_axis=optimisation_axis,
        )
        return DailyMissionIntelligenceApplicationService.from_brief(brief)

    @staticmethod
    def from_brief(
        brief: DailyMissionBrief,
        *,
        journal_entry_id: str = "",
    ) -> DailyMissionIntelligenceSnapshot:
        """Map domain brief → presentation snapshot."""
        return DailyMissionIntelligenceSnapshot(
            title=brief.title,
            educational_purpose=brief.educational_purpose,
            why_today=brief.why_today,
            why_not_something_else=brief.why_not_something_else,
            supporting_evidence=brief.supporting_evidence,
            estimated_effort=brief.estimated_effort,
            expected_learning_outcome=brief.expected_learning_outcome,
            what_happens_after_completion=brief.what_happens_after_completion,
            reflection_prompt=brief.reflection_prompt,
            mission_confidence=brief.mission_confidence,
            uncertainty=brief.uncertainty,
            mission_explanation=brief.mission_explanation,
            skip_consequence=brief.skip_consequence,
            optimisation_axis_label=brief.optimisation_axis_label,
            lifecycle_phase=brief.lifecycle_phase.value,
            qualitative_confidence=brief.qualitative_confidence.value,
            recommendation_key=brief.recommendation_key,
            mission_id=brief.mission_id,
            session_id=brief.session_id,
            has_mission=brief.has_mission,
            empty=brief.empty,
            journal_entry_id=journal_entry_id,
            metadata=brief.metadata,
        )

    @staticmethod
    def present(
        user_id: int,
        snapshot_or_fields: DailyMissionIntelligenceSnapshot | dict[str, Any],
        *,
        for_day: date | None = None,
    ) -> DailyMissionIntelligenceSnapshot:
        """Compose (if needed) and record presentation in the Decision Journal."""
        if isinstance(snapshot_or_fields, DailyMissionIntelligenceSnapshot):
            snap = snapshot_or_fields
            brief = DailyMissionIntelligenceService.compose_from_home_fields(
                title=snap.title,
                summary=snap.educational_purpose,
                why_recommended=snap.educational_purpose,
                timeliness_line=snap.why_today,
                supporting_evidence=snap.supporting_evidence,
                estimated_effort=snap.estimated_effort,
                expected_benefit=snap.expected_learning_outcome,
                review_point=snap.what_happens_after_completion,
                completion_loop_line=snap.what_happens_after_completion,
                confidence_label=snap.mission_confidence,
                uncertainty=snap.uncertainty,
                recommendation_key=snap.recommendation_key,
                mission_id=snap.mission_id,
                session_id=snap.session_id,
                lifecycle_phase=snap.lifecycle_phase
                or MissionLifecyclePhase.PRESENTED.value,
            )
        else:
            brief = DailyMissionIntelligenceService.compose_from_home_fields(
                **snapshot_or_fields
            )
            snap = DailyMissionIntelligenceApplicationService.from_brief(
                brief
            )

        entry = DailyMissionIntelligenceService.present_to_journal(
            user_id,
            brief,
            for_day=for_day,
        )
        entry_id = getattr(entry, "entry_id", "") if entry is not None else ""
        return DailyMissionIntelligenceApplicationService.from_brief(
            brief,
            journal_entry_id=entry_id or "",
        )

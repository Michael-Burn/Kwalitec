"""Daily Mission Intelligence service (ILE-004).

Composes today's primary mission brief from authorised Home / Recommendation
evidence and records significant lifecycle moments into the Decision Journal.
Never re-ranks, never mutates Twin or mastery, never invents educational need.
"""

from __future__ import annotations

import logging
from datetime import date, datetime
from typing import Any

from app.domain.daily_mission_intelligence import (
    DailyMissionBrief,
    DailyMissionEvidenceInput,
    MissionLifecyclePhase,
    compose_daily_mission,
)
from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    StudentAction,
)
from app.domain.decision_journal.enums import ReflectionStatus
from app.services.decision_journal_service import DecisionJournalService

logger = logging.getLogger(__name__)

# Catalogue Decision ID for ILE-011 primary daily mission guidance.
CATALOGUE_DECISION_ID = "D-L01"


class DailyMissionIntelligenceService:
    """Compose and journal today's primary educational mission."""

    @staticmethod
    def compose_from_home_fields(
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
    ) -> DailyMissionBrief:
        """Compose a mission brief from already-resolved Home/MES fields."""
        evidence = DailyMissionEvidenceInput(
            title=title or "",
            summary=summary or "",
            why_recommended=why_recommended or "",
            timeliness_line=timeliness_line or "",
            supporting_evidence=tuple(supporting_evidence or ()),
            estimated_effort=estimated_effort or "",
            expected_benefit=expected_benefit or "",
            suggested_next_action=suggested_next_action or "",
            review_point=review_point or "",
            completion_loop_line=completion_loop_line or "",
            confidence_label=confidence_label or "",
            confidence_basis=confidence_basis or "",
            uncertainty=uncertainty or "",
            honest_refusal=bool(honest_refusal),
            alternative_titles=tuple(alternative_titles or ()),
            recommendation_key=recommendation_key or "",
            mission_id=mission_id or "",
            session_id=session_id or "",
            educational_context=educational_context or "Today's Mission",
            optimisation_axis=optimisation_axis
            or "learning_value",
            lifecycle_phase=lifecycle_phase
            or MissionLifecyclePhase.PRESENTED.value,
            prior_deferral_note=prior_deferral_note or "",
        )
        brief = compose_daily_mission(evidence)
        logger.info(
            "daily_mission_composed empty=%s title=%s phase=%s",
            brief.empty,
            (brief.title or "")[:48],
            brief.lifecycle_phase.value,
        )
        return brief

    @staticmethod
    def present_to_journal(
        user_id: int,
        brief: DailyMissionBrief,
        *,
        for_day: date | None = None,
    ) -> Any | None:
        """Idempotently record that today's Mission was presented.

        Creates a ``recommended`` journal entry once per learner / day /
        recommendation key. Fail-open: journal errors never block Home.

        Returns:
            Journal entry when created or found; ``None`` when empty brief
            or on soft failure.
        """
        if brief.empty or not brief.has_mission:
            return None
        day = for_day or date.today()
        key = (brief.recommendation_key or brief.title or "").strip()
        try:
            existing = DailyMissionIntelligenceService._find_presented(
                user_id,
                day=day,
                recommendation_key=key,
            )
            if existing is not None:
                return existing
            context = brief.educational_context or "Today's Mission"
            if key and f"[{key}]" not in context:
                context = f"{context} [{key}]"[:255]
            entry = DecisionJournalService.record_entry(
                user_id,
                kind=EntryKind.MISSION_RECOMMENDATION,
                educational_context=context,
                observation=brief.why_today or brief.educational_purpose,
                meaning=brief.educational_purpose,
                recommendation=brief.title,
                supporting_evidence_summary=_evidence_summary(brief),
                qualitative_confidence=brief.qualitative_confidence,
                expected_benefit=brief.expected_learning_outcome,
                uncertainty=brief.uncertainty,
                catalogue_decision_id=CATALOGUE_DECISION_ID,
                student_action=StudentAction.NONE_YET,
                lifecycle_status=JournalLifecycleStatus.RECOMMENDED,
                reflection_status=ReflectionStatus.PENDING,
                recorded_at=datetime.combine(
                    day, datetime.min.time().replace(hour=12)
                ),
            )
            logger.info(
                "daily_mission_presented user_id=%s entry_id=%s day=%s",
                user_id,
                entry.entry_id,
                day.isoformat(),
            )
            return entry
        except Exception:
            logger.exception(
                "daily_mission_present_journal_failed user_id=%s",
                user_id,
            )
            return None

    @staticmethod
    def record_acceptance(
        user_id: int,
        brief: DailyMissionBrief,
        *,
        tip: dict[str, Any] | None = None,
    ) -> Any | None:
        """Record learner acceptance of today's Mission into the journal."""
        if brief.empty:
            return None
        tip_payload = tip or DailyMissionIntelligenceService.to_tip_dict(brief)
        try:
            return DecisionJournalService.record_from_recommendation(
                user_id,
                tip_payload,
                accepted=True,
                completed=False,
                kind=EntryKind.MISSION_RECOMMENDATION,
                catalogue_decision_id=CATALOGUE_DECISION_ID,
            )
        except Exception:
            logger.exception(
                "daily_mission_accept_journal_failed user_id=%s",
                user_id,
            )
            return None

    @staticmethod
    def record_deferral(
        user_id: int,
        brief: DailyMissionBrief,
        *,
        tip: dict[str, Any] | None = None,
        reason_note: str = "",
    ) -> Any | None:
        """Record learner deferral of today's Mission into the journal."""
        if brief.empty:
            return None
        tip_payload = tip or DailyMissionIntelligenceService.to_tip_dict(brief)
        if reason_note and not tip_payload.get("uncertainty"):
            tip_payload = {
                **tip_payload,
                "uncertainty": reason_note.strip()[:500],
            }
        try:
            return DecisionJournalService.record_from_recommendation(
                user_id,
                tip_payload,
                accepted=False,
                completed=False,
                kind=EntryKind.MISSION_RECOMMENDATION,
                catalogue_decision_id=CATALOGUE_DECISION_ID,
            )
        except Exception:
            logger.exception(
                "daily_mission_defer_journal_failed user_id=%s",
                user_id,
            )
            return None

    @staticmethod
    def record_completion(
        user_id: int,
        brief: DailyMissionBrief,
        *,
        tip: dict[str, Any] | None = None,
        outcome_summary: str = "Mission completed",
    ) -> Any | None:
        """Record Mission completion outcome into the Decision Journal."""
        if brief.empty:
            return None
        tip_payload = tip or DailyMissionIntelligenceService.to_tip_dict(brief)
        try:
            return DecisionJournalService.record_from_recommendation(
                user_id,
                tip_payload,
                accepted=True,
                completed=True,
                outcome_summary=outcome_summary
                or brief.what_happens_after_completion
                or "Mission completed",
                kind=EntryKind.MISSION_RECOMMENDATION,
                catalogue_decision_id=CATALOGUE_DECISION_ID,
            )
        except Exception:
            logger.exception(
                "daily_mission_complete_journal_failed user_id=%s",
                user_id,
            )
            return None

    @staticmethod
    def record_reflection(
        user_id: int,
        entry_id: str,
        *,
        note: str,
    ) -> Any | None:
        """Persist post-mission reflection onto a journal entry."""
        try:
            return DecisionJournalService.record_reflection(
                user_id,
                entry_id,
                note=note,
            )
        except Exception:
            logger.exception(
                "daily_mission_reflection_journal_failed user_id=%s",
                user_id,
            )
            return None

    @staticmethod
    def to_tip_dict(brief: DailyMissionBrief) -> dict[str, Any]:
        """Map a mission brief onto the commitment / journal tip shape."""
        return {
            "title": brief.title,
            "summary": brief.educational_purpose,
            "why_recommended": brief.educational_purpose,
            "reason": brief.why_today,
            "expected_benefit": brief.expected_learning_outcome,
            "supporting_evidence": _evidence_summary(brief),
            "suggested_next_action": brief.title,
            "uncertainty": brief.uncertainty,
            "observation": brief.why_today or brief.educational_purpose,
            "meaning": brief.educational_purpose,
            "recommendation": brief.title,
            "educational_context": brief.educational_context
            or "Today's Mission",
            "review_point": brief.what_happens_after_completion,
            "recommendation_key": brief.recommendation_key,
        }

    @staticmethod
    def _find_presented(
        user_id: int,
        *,
        day: date,
        recommendation_key: str,
    ) -> Any | None:
        """Find an existing presented mission journal row for this day/key."""
        rows = DecisionJournalService.get_timeline(
            user_id,
            limit=40,
            include_archived=False,
        )
        start = datetime.combine(day, datetime.min.time())
        end = datetime.combine(day, datetime.max.time())
        key = (recommendation_key or "").strip()
        for row in rows:
            if row.kind != EntryKind.MISSION_RECOMMENDATION.value:
                continue
            if row.lifecycle_status == JournalLifecycleStatus.ARCHIVED.value:
                continue
            recorded = row.recorded_at
            if recorded is None or recorded < start or recorded > end:
                continue
            ctx = row.educational_context or ""
            rec = row.recommendation or ""
            if key and (key in ctx or key == rec or key in rec):
                return row
            if not key and rec:
                return row
        return None


def _evidence_summary(brief: DailyMissionBrief) -> str:
    if brief.supporting_evidence:
        return "; ".join(brief.supporting_evidence[:4])
    return brief.why_today or brief.educational_purpose or ""

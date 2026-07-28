"""Service tests for Daily Mission Intelligence (ILE-004)."""

from __future__ import annotations

from datetime import date

from app.domain.decision_journal import EntryKind, JournalLifecycleStatus
from app.services.daily_mission_intelligence_service import (
    DailyMissionIntelligenceService,
)
from app.services.decision_journal_service import DecisionJournalService


class TestDailyMissionIntelligenceService:
    def test_compose_from_home_fields(self):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="Revise CT1 chapter 4",
            why_recommended="Evidence suggests this focus is highest value today.",
            timeliness_line="Your plan places this focus today.",
            supporting_evidence=("Recent practice was uneven.",),
            estimated_effort="About 20 minutes",
            expected_benefit="Stronger recall before later topics.",
            confidence_label="Reliable guidance",
        )
        assert brief.has_mission
        assert brief.title.startswith("Revise")
        assert brief.estimated_effort

    def test_present_to_journal_idempotent(self, user, db):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="Today's equity Mission",
            why_recommended="Supports later syllabus steps.",
            expected_benefit="A steadier base.",
            recommendation_key="equity-key",
        )
        day = date(2026, 7, 28)
        first = DailyMissionIntelligenceService.present_to_journal(
            user.id, brief, for_day=day
        )
        second = DailyMissionIntelligenceService.present_to_journal(
            user.id, brief, for_day=day
        )
        assert first is not None
        assert second is not None
        assert first.entry_id == second.entry_id
        rows = DecisionJournalService.get_timeline(user.id, limit=20)
        mission_rows = [
            r
            for r in rows
            if r.kind == EntryKind.MISSION_RECOMMENDATION.value
            and r.lifecycle_status == JournalLifecycleStatus.RECOMMENDED.value
        ]
        assert len(mission_rows) == 1

    def test_record_completion(self, user, db):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="Complete duration matching practice",
            why_recommended="Highest-value focus today.",
            expected_benefit="Clearer method grasp.",
        )
        entry = DailyMissionIntelligenceService.record_completion(
            user.id,
            brief,
            outcome_summary="Mission completed",
        )
        assert entry is not None
        assert entry.lifecycle_status == (
            JournalLifecycleStatus.OUTCOME_RECORDED.value
        )
        student = DecisionJournalService.to_student_dict(entry)
        assert "Mission" in student["recommendation"] or student["recommendation"]

    def test_record_deferral(self, user, db):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="Deferral test mission",
            why_recommended="Still valuable, but not today.",
        )
        entry = DailyMissionIntelligenceService.record_deferral(user.id, brief)
        assert entry is not None
        assert entry.lifecycle_status == JournalLifecycleStatus.DEFERRED.value

    def test_empty_brief_skips_journal(self, user, db):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="",
        )
        assert brief.empty
        assert (
            DailyMissionIntelligenceService.present_to_journal(user.id, brief)
            is None
        )

    def test_to_tip_dict(self):
        brief = DailyMissionIntelligenceService.compose_from_home_fields(
            title="Tip map mission",
            why_recommended="Because evidence supports it.",
            expected_benefit="Learning benefit.",
            uncertainty="Still provisional.",
        )
        tip = DailyMissionIntelligenceService.to_tip_dict(brief)
        assert tip["title"] == "Tip map mission"
        assert tip["expected_benefit"]
        assert tip["uncertainty"]

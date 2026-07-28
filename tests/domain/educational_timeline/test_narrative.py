"""Domain tests for Educational Timeline narrative (ILE-003)."""

from __future__ import annotations

from datetime import datetime, timedelta

import pytest

from app.domain.decision_journal import (
    EntryKind,
    JournalLifecycleStatus,
    QualitativeConfidence,
    ReflectionStatus,
    StudentAction,
)
from app.domain.educational_timeline import (
    NarrativeCertainty,
    TimelineSectionKind,
    assert_narrative_humble,
    build_educational_narrative,
)


def _entry(
    *,
    decision_id: str,
    recorded_at: datetime,
    kind: str = EntryKind.MISSION_RECOMMENDATION.value,
    lifecycle: str = JournalLifecycleStatus.ACCEPTED.value,
    confidence: str = QualitativeConfidence.EMERGING.value,
    action: str = StudentAction.ACCEPTED.value,
    observation: str = "Practice looked fragile on this topic.",
    meaning: str = "That topic supports later syllabus steps.",
    recommendation: str = "Spend today's Mission reinforcing the topic.",
    uncertainty: str = "",
    outcome: str = "",
    reflection_status: str = ReflectionStatus.PENDING.value,
    reflection_note: str = "",
) -> dict:
    return {
        "decision_id": decision_id,
        "recorded_at": recorded_at,
        "kind": kind,
        "lifecycle_status": lifecycle,
        "educational_context": "Study guidance",
        "observation": observation,
        "meaning": meaning,
        "recommendation": recommendation,
        "qualitative_confidence": confidence,
        "uncertainty": uncertainty,
        "student_action": action,
        "outcome_summary": outcome,
        "reflection_status": reflection_status,
        "reflection_note": reflection_note,
        "expected_benefit": "A steadier base.",
    }


class TestBuildEducationalNarrative:
    def test_empty_entries_yield_empty_narrative(self):
        narrative = build_educational_narrative([])
        assert narrative.empty is True
        assert narrative.entry_count == 0
        assert narrative.sections == ()

    def test_single_entry_produces_learning_journey(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        narrative = build_educational_narrative(
            [_entry(decision_id="dj_1", recorded_at=base)]
        )
        assert narrative.empty is False
        assert narrative.entry_count == 1
        assert narrative.certainty == NarrativeCertainty.INSUFFICIENT
        kinds = {s.kind for s in narrative.sections}
        assert TimelineSectionKind.LEARNING_JOURNEY in kinds
        journey = next(
            s
            for s in narrative.sections
            if s.kind == TimelineSectionKind.LEARNING_JOURNEY
        )
        moment = journey.moments[0]
        assert moment.observation
        assert moment.pattern
        assert moment.educational_meaning
        assert moment.reflection_question
        assert moment.evidence_decision_ids == ("dj_1",)

    def test_turning_points_from_reliable_acceptance(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        entries = [
            _entry(decision_id="dj_a", recorded_at=base),
            _entry(
                decision_id="dj_b",
                recorded_at=base + timedelta(days=2),
                confidence=QualitativeConfidence.RELIABLE.value,
            ),
            _entry(
                decision_id="dj_c",
                recorded_at=base + timedelta(days=4),
            ),
        ]
        narrative = build_educational_narrative(entries)
        turning = next(
            (
                s
                for s in narrative.sections
                if s.kind == TimelineSectionKind.TURNING_POINTS
            ),
            None,
        )
        assert turning is not None
        titles = [m.title for m in turning.moments]
        assert any("steadier" in t.lower() for t in titles)

    def test_recoveries_section_from_recovery_kind(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        entries = [
            _entry(decision_id="dj_1", recorded_at=base),
            _entry(
                decision_id="dj_2",
                recorded_at=base + timedelta(days=1),
                kind=EntryKind.RECOVERY_RECOMMENDATION.value,
                recommendation="Rebuild foundations on Discounting.",
                observation="Recent checks showed fragile recall.",
            ),
        ]
        narrative = build_educational_narrative(entries)
        recoveries = next(
            s
            for s in narrative.sections
            if s.kind == TimelineSectionKind.RECOVERIES
        )
        assert recoveries.moments
        assert "Discounting" in recoveries.moments[0].title

    def test_consistency_streak(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        entries = [
            _entry(
                decision_id=f"dj_{i}",
                recorded_at=base + timedelta(days=i),
            )
            for i in range(4)
        ]
        narrative = build_educational_narrative(entries)
        consistency = next(
            (
                s
                for s in narrative.sections
                if s.kind == TimelineSectionKind.PERIODS_OF_CONSISTENCY
            ),
            None,
        )
        assert consistency is not None
        assert consistency.moments

    def test_uncertainty_period(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        entries = [
            _entry(
                decision_id="dj_1",
                recorded_at=base,
                confidence=QualitativeConfidence.INSUFFICIENT.value,
                uncertainty="Only one short session so far.",
            ),
            _entry(
                decision_id="dj_2",
                recorded_at=base + timedelta(days=1),
                confidence=QualitativeConfidence.OBSERVATION_ONLY.value,
                uncertainty="Still gathering evidence.",
            ),
        ]
        narrative = build_educational_narrative(entries)
        uncertain = next(
            s
            for s in narrative.sections
            if s.kind == TimelineSectionKind.PERIODS_OF_UNCERTAINTY
        )
        assert uncertain.moments

    def test_reflection_and_decision_milestones(self):
        base = datetime(2026, 7, 1, 10, 0, 0)
        entries = [
            _entry(
                decision_id="dj_1",
                recorded_at=base,
                lifecycle=JournalLifecycleStatus.REFLECTED.value,
                reflection_status=ReflectionStatus.REFLECTED.value,
                reflection_note="Short focused sessions helped.",
                outcome="Recall felt steadier afterwards.",
            ),
            _entry(
                decision_id="dj_2",
                recorded_at=base + timedelta(days=2),
                lifecycle=JournalLifecycleStatus.OUTCOME_RECORDED.value,
                outcome="Completed the Mission focus.",
            ),
        ]
        narrative = build_educational_narrative(entries)
        kinds = {s.kind for s in narrative.sections}
        assert TimelineSectionKind.REFLECTION_HIGHLIGHTS in kinds
        assert TimelineSectionKind.DECISION_MILESTONES in kinds
        assert TimelineSectionKind.MISSION_MILESTONES in kinds

    def test_learning_momentum_present_with_dated_span(self):
        base = datetime(2026, 6, 1, 10, 0, 0)
        entries = [
            _entry(
                decision_id="dj_old",
                recorded_at=base,
            ),
            _entry(
                decision_id="dj_new1",
                recorded_at=base + timedelta(days=20),
            ),
            _entry(
                decision_id="dj_new2",
                recorded_at=base + timedelta(days=21),
            ),
            _entry(
                decision_id="dj_new3",
                recorded_at=base + timedelta(days=22),
            ),
        ]
        narrative = build_educational_narrative(entries)
        momentum = next(
            (
                s
                for s in narrative.sections
                if s.kind == TimelineSectionKind.LEARNING_MOMENTUM
            ),
            None,
        )
        assert momentum is not None
        assert momentum.moments[0].reflection_question

    def test_sections_only_from_journal_evidence(self):
        """No section invents content without journal-backed moments."""
        narrative = build_educational_narrative(
            [
                _entry(
                    decision_id="dj_only",
                    recorded_at=datetime(2026, 7, 1),
                    action=StudentAction.NONE_YET.value,
                    lifecycle=JournalLifecycleStatus.RECOMMENDED.value,
                )
            ]
        )
        for section in narrative.sections:
            assert section.moments
            for moment in section.moments:
                assert moment.evidence_decision_ids


class TestNarrativeHumility:
    def test_rejects_overclaim(self):
        with pytest.raises(ValueError, match="overclaim"):
            assert_narrative_humble(
                "This proves that you have mastered the topic.",
                certainty=NarrativeCertainty.SUPPORTED,
            )

    def test_rejects_absolute_when_insufficient(self):
        with pytest.raises(ValueError, match="tentative"):
            assert_narrative_humble(
                "You never improve without this.",
                certainty=NarrativeCertainty.INSUFFICIENT,
            )

    def test_allows_whenever_under_insufficient(self):
        assert_narrative_humble(
            "Whenever evidence is thin, guidance stays cautious.",
            certainty=NarrativeCertainty.INSUFFICIENT,
        )

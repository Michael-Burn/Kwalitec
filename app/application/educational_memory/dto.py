"""Educational Memory DTOs (KWP-011).

Immutable structures for intelligence snapshots, timeline entries,
longitudinal patterns, milestones, and student journey narratives.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Any

INTELLIGENCE_SNAPSHOT_SCHEMA = "kwp011.1"


class TimelineEventKind(StrEnum):
    """Chronological educational events derived from sitting evidence."""

    STARTED_TOPIC = "started_topic"
    REPEATED_REINFORCEMENT = "repeated_reinforcement"
    UNDERSTANDING_IMPROVED = "understanding_improved"
    ADVANCED = "advanced"
    KNOWLEDGE_DECAYED = "knowledge_decayed"
    RECOVERED = "recovered"
    MASTERED = "mastered"
    CONSOLIDATED = "consolidated"
    REFLECTED = "reflected"
    SITTING_RECORDED = "sitting_recorded"
    # KWP-014 — optional curriculum movement references.
    FOUNDATION_COMPLETE = "foundation_complete"
    INTERMEDIATE_MODELLING = "intermediate_modelling"
    EXAM_INTEGRATION = "exam_integration"


class PatternKind(StrEnum):
    """Recurring educational patterns across sittings."""

    REPEATED_PREREQUISITE_WEAKNESS = "repeated_prerequisite_weakness"
    REPEATED_CONFIDENCE_MISMATCH = "repeated_confidence_mismatch"
    REPEATED_SUCCESSFUL_RECOVERIES = "repeated_successful_recoveries"
    REPEATED_CONSOLIDATION = "repeated_consolidation"
    INCREASING_INDEPENDENCE = "increasing_independence"
    IMPROVING_CONSISTENCY = "improving_consistency"
    LONG_TERM_RETENTION_IMPROVEMENTS = "long_term_retention_improvements"


class MilestoneKind(StrEnum):
    """Educational growth milestones — not gamification."""

    FIRST_SUCCESSFUL_RECOVERY = "first_successful_recovery"
    FIRST_SUSTAINED_MASTERY = "first_sustained_mastery"
    LONGEST_CONSISTENCY_STREAK = "longest_consistency_streak"
    RECOVERED_FORGOTTEN_KNOWLEDGE = "recovered_forgotten_knowledge"
    COMPLETED_DIFFICULT_TOPIC = "completed_difficult_topic"
    IMPROVED_CONFIDENCE_ALIGNMENT = "improved_confidence_alignment"


# Student-safe titles (no points / badges / leaderboards).
TIMELINE_TITLES: dict[TimelineEventKind, str] = {
    TimelineEventKind.STARTED_TOPIC: "Started topic",
    TimelineEventKind.REPEATED_REINFORCEMENT: "Repeated reinforcement",
    TimelineEventKind.UNDERSTANDING_IMPROVED: "Understanding improved",
    TimelineEventKind.ADVANCED: "Advanced",
    TimelineEventKind.KNOWLEDGE_DECAYED: "Knowledge decayed",
    TimelineEventKind.RECOVERED: "Recovered",
    TimelineEventKind.MASTERED: "Mastered",
    TimelineEventKind.CONSOLIDATED: "Consolidated",
    TimelineEventKind.REFLECTED: "Reflected",
    TimelineEventKind.SITTING_RECORDED: "Study sitting",
    TimelineEventKind.FOUNDATION_COMPLETE: "Foundation complete",
    TimelineEventKind.INTERMEDIATE_MODELLING: "Intermediate modelling",
    TimelineEventKind.EXAM_INTEGRATION: "Exam integration",
}

PATTERN_TITLES: dict[PatternKind, str] = {
    PatternKind.REPEATED_PREREQUISITE_WEAKNESS: (
        "Repeated prerequisite weaknesses"
    ),
    PatternKind.REPEATED_CONFIDENCE_MISMATCH: "Repeated confidence mismatch",
    PatternKind.REPEATED_SUCCESSFUL_RECOVERIES: (
        "Repeated successful recoveries"
    ),
    PatternKind.REPEATED_CONSOLIDATION: "Repeated consolidation",
    PatternKind.INCREASING_INDEPENDENCE: "Increasing independence",
    PatternKind.IMPROVING_CONSISTENCY: "Improving consistency",
    PatternKind.LONG_TERM_RETENTION_IMPROVEMENTS: (
        "Long-term retention improvements"
    ),
}

MILESTONE_TITLES: dict[MilestoneKind, str] = {
    MilestoneKind.FIRST_SUCCESSFUL_RECOVERY: "First successful recovery",
    MilestoneKind.FIRST_SUSTAINED_MASTERY: "First sustained mastery",
    MilestoneKind.LONGEST_CONSISTENCY_STREAK: "Longest consistency streak",
    MilestoneKind.RECOVERED_FORGOTTEN_KNOWLEDGE: (
        "Recovered forgotten knowledge"
    ),
    MilestoneKind.COMPLETED_DIFFICULT_TOPIC: "Completed difficult topic",
    MilestoneKind.IMPROVED_CONFIDENCE_ALIGNMENT: (
        "Improved confidence alignment"
    ),
}


@dataclass(frozen=True)
class IntelligenceSnapshot:
    """Point-in-time educational intelligence for one sitting.

    Frozen at capture — History must never rebuild advice with current rules.
    """

    schema_version: str = INTELLIGENCE_SNAPSHOT_SCHEMA
    captured_at: str = ""
    student_id: str = ""
    session_id: str = ""
    package_id: str = ""
    topic_title: str = ""
    topic_id: str = ""
    # Full engine opaques (founder / continuity).
    strategy: dict[str, Any] = field(default_factory=dict)
    diagnostics: dict[str, Any] = field(default_factory=dict)
    difficulty: dict[str, Any] = field(default_factory=dict)
    effectiveness: dict[str, Any] = field(default_factory=dict)
    # Continuity chain.
    prior_intervention: dict[str, Any] = field(default_factory=dict)
    outgoing_intervention: dict[str, Any] = field(default_factory=dict)
    # Student-facing Sitting Report fields as they existed at capture.
    student_sitting_report: dict[str, str] = field(default_factory=dict)

    @property
    def has_student_report(self) -> bool:
        report = self.student_sitting_report
        return bool(
            report.get("strategy_title")
            or report.get("diagnostic_guidance")
            or report.get("difficulty_guidance")
            or report.get("effectiveness_feedback")
        )

    def to_opaque(self) -> dict[str, Any]:
        return {
            "schema_version": self.schema_version,
            "captured_at": self.captured_at,
            "student_id": self.student_id,
            "session_id": self.session_id,
            "package_id": self.package_id,
            "topic_title": self.topic_title,
            "topic_id": self.topic_id,
            "strategy": dict(self.strategy),
            "diagnostics": dict(self.diagnostics),
            "difficulty": dict(self.difficulty),
            "effectiveness": dict(self.effectiveness),
            "prior_intervention": dict(self.prior_intervention),
            "outgoing_intervention": dict(self.outgoing_intervention),
            "student_sitting_report": dict(self.student_sitting_report),
        }

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> IntelligenceSnapshot | None:
        if not isinstance(raw, dict) or not raw:
            return None
        report_raw = raw.get("student_sitting_report") or {}
        report = {
            str(k): str(v)
            for k, v in report_raw.items()
            if isinstance(k, str) and v is not None
        }
        return cls(
            schema_version=str(
                raw.get("schema_version") or INTELLIGENCE_SNAPSHOT_SCHEMA
            ),
            captured_at=str(raw.get("captured_at") or ""),
            student_id=str(raw.get("student_id") or ""),
            session_id=str(raw.get("session_id") or ""),
            package_id=str(raw.get("package_id") or ""),
            topic_title=str(raw.get("topic_title") or ""),
            topic_id=str(raw.get("topic_id") or ""),
            strategy=dict(raw.get("strategy") or {}),
            diagnostics=dict(raw.get("diagnostics") or {}),
            difficulty=dict(raw.get("difficulty") or {}),
            effectiveness=dict(raw.get("effectiveness") or {}),
            prior_intervention=dict(raw.get("prior_intervention") or {}),
            outgoing_intervention=dict(raw.get("outgoing_intervention") or {}),
            student_sitting_report=report,
        )


@dataclass(frozen=True)
class TimelineEntry:
    """One chronological educational event from existing evidence."""

    kind: TimelineEventKind
    title: str
    body: str
    topic_title: str = ""
    session_id: str = ""
    package_id: str = ""
    recorded_at: str = ""
    evidence_codes: tuple[str, ...] = ()
    # KWP-014 — optional curriculum movement reference.
    curriculum_movement: str = ""

    def to_opaque(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "title": self.title,
            "body": self.body,
            "topic_title": self.topic_title,
            "session_id": self.session_id,
            "package_id": self.package_id,
            "recorded_at": self.recorded_at,
            "evidence_codes": list(self.evidence_codes),
            "curriculum_movement": self.curriculum_movement,
        }


@dataclass(frozen=True)
class LongitudinalPattern:
    """A recurring educational pattern supported by multiple sittings."""

    kind: PatternKind
    title: str
    narrative: str
    occurrence_count: int = 0
    topics: tuple[str, ...] = ()
    evidence_codes: tuple[str, ...] = ()

    def to_opaque(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "title": self.title,
            "narrative": self.narrative,
            "occurrence_count": self.occurrence_count,
            "topics": list(self.topics),
            "evidence_codes": list(self.evidence_codes),
        }


@dataclass(frozen=True)
class LearningMilestone:
    """An educational growth milestone (no points / badges)."""

    kind: MilestoneKind
    title: str
    narrative: str
    topic_title: str = ""
    session_id: str = ""
    recorded_at: str = ""
    evidence_codes: tuple[str, ...] = ()

    def to_opaque(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "title": self.title,
            "narrative": self.narrative,
            "topic_title": self.topic_title,
            "session_id": self.session_id,
            "recorded_at": self.recorded_at,
            "evidence_codes": list(self.evidence_codes),
        }


@dataclass(frozen=True)
class LearningJourneyNarrative:
    """Student-facing educational story — not raw analytics."""

    headline: str
    story_paragraphs: tuple[str, ...] = ()
    timeline: tuple[TimelineEntry, ...] = ()
    patterns: tuple[LongitudinalPattern, ...] = ()
    milestones: tuple[LearningMilestone, ...] = ()
    sitting_archives: tuple[dict[str, str], ...] = ()
    sitting_count: int = 0
    topic_count: int = 0
    has_memory: bool = False

    def to_opaque(self) -> dict[str, Any]:
        return {
            "headline": self.headline,
            "story_paragraphs": list(self.story_paragraphs),
            "timeline": [e.to_opaque() for e in self.timeline],
            "patterns": [p.to_opaque() for p in self.patterns],
            "milestones": [m.to_opaque() for m in self.milestones],
            "sitting_archives": [dict(a) for a in self.sitting_archives],
            "sitting_count": self.sitting_count,
            "topic_count": self.topic_count,
            "has_memory": self.has_memory,
        }

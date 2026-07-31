"""Candidate educational observations emitted during a Study Session (EV-001B).

Candidates are Generated-state observations. They are not Accepted evidence
until EducationalEvidenceAuthority validates the sitting package.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
from enum import StrEnum
from typing import Any


class RuntimeEvidenceType(StrEnum):
    """EV-001A Student Runtime evidence type catalogue (stable ids)."""

    LEARNING_OBJECTIVES_PRESENTED = "EV-RT-01"
    READING_STARTED = "EV-RT-02"
    READING_COMPLETED = "EV-RT-03"
    WORKED_EXAMPLE_STARTED = "EV-RT-04"
    WORKED_EXAMPLE_COMPLETED = "EV-RT-05"
    PRACTICE_ATTEMPTED = "EV-RT-06"
    PRACTICE_CORRECT = "EV-RT-07"
    PRACTICE_INCORRECT = "EV-RT-08"
    PRACTICE_PARTIAL_UNSCORED = "EV-RT-09"
    REFLECTION_SUBMITTED = "EV-RT-10"
    REFLECTION_SKIPPED = "EV-RT-11"
    CONFIDENCE_REPORTED = "EV-RT-12"
    SESSION_STARTED = "EV-RT-20"
    SESSION_PAUSED = "EV-RT-21"
    SESSION_RESUMED = "EV-RT-22"
    FINISH_REVIEW_YES = "EV-RT-23"
    FINISH_REVIEW_PARTIALLY = "EV-RT-24"
    FINISH_REVIEW_NO = "EV-RT-25"
    SESSION_COMPLETED = "EV-RT-26"
    SKIPPED_ACTIVITY = "EV-RT-27"
    PARTIAL_COMPLETION = "EV-RT-28"
    ABANDONED_SESSION = "EV-RT-29"
    MISSION_ACCEPTED = "EV-RT-30"
    MISSION_DEFERRED = "EV-RT-31"
    MISSION_COMPLETED = "EV-RT-32"
    TOPIC_COVERAGE_ADVANCED = "EV-RT-33"
    MARK_COMPLETE_PILOT = "EV-RT-34"
    STRUCTURED_QUESTION_RESULTS = "EV-RT-40"
    QUIZ_RESULTS = "EV-RT-41"
    MISSION_ASSESSMENT_RESULTS = "EV-RT-42"
    MOCK_EXAMINATION_RESULTS = "EV-RT-43"
    OFFICIAL_EXAMINATION_RESULTS = "EV-RT-44"
    SESSION_DURATION = "EV-RT-90"
    BUTTON_CLICKS = "EV-RT-91"
    CHECKLIST_TICKS = "EV-RT-92"
    RECOMMENDATION_PREFERENCE = "EV-RT-93"


# Ceiling grades per EV-001A taxonomy (Validation may only lower).
TYPE_CEILING_GRADE: dict[RuntimeEvidenceType, str] = {
    RuntimeEvidenceType.LEARNING_OBJECTIVES_PRESENTED: "informational",
    RuntimeEvidenceType.READING_STARTED: "informational",
    RuntimeEvidenceType.READING_COMPLETED: "behavioural",
    RuntimeEvidenceType.WORKED_EXAMPLE_STARTED: "informational",
    RuntimeEvidenceType.WORKED_EXAMPLE_COMPLETED: "behavioural",
    RuntimeEvidenceType.PRACTICE_ATTEMPTED: "behavioural",
    RuntimeEvidenceType.PRACTICE_CORRECT: "educational",
    RuntimeEvidenceType.PRACTICE_INCORRECT: "educational",
    RuntimeEvidenceType.PRACTICE_PARTIAL_UNSCORED: "behavioural",
    RuntimeEvidenceType.REFLECTION_SUBMITTED: "behavioural",
    RuntimeEvidenceType.REFLECTION_SKIPPED: "informational",
    RuntimeEvidenceType.CONFIDENCE_REPORTED: "informational",
    RuntimeEvidenceType.SESSION_STARTED: "informational",
    RuntimeEvidenceType.SESSION_PAUSED: "informational",
    RuntimeEvidenceType.SESSION_RESUMED: "informational",
    RuntimeEvidenceType.FINISH_REVIEW_YES: "behavioural",
    RuntimeEvidenceType.FINISH_REVIEW_PARTIALLY: "behavioural",
    RuntimeEvidenceType.FINISH_REVIEW_NO: "behavioural",
    RuntimeEvidenceType.SESSION_COMPLETED: "behavioural",
    RuntimeEvidenceType.SKIPPED_ACTIVITY: "behavioural",
    RuntimeEvidenceType.PARTIAL_COMPLETION: "behavioural",
    RuntimeEvidenceType.ABANDONED_SESSION: "informational",
    RuntimeEvidenceType.MISSION_ACCEPTED: "informational",
    RuntimeEvidenceType.MISSION_DEFERRED: "informational",
    RuntimeEvidenceType.MISSION_COMPLETED: "behavioural",
    RuntimeEvidenceType.TOPIC_COVERAGE_ADVANCED: "behavioural",
    RuntimeEvidenceType.MARK_COMPLETE_PILOT: "informational",
    RuntimeEvidenceType.STRUCTURED_QUESTION_RESULTS: "educational",
    RuntimeEvidenceType.QUIZ_RESULTS: "educational",
    RuntimeEvidenceType.MISSION_ASSESSMENT_RESULTS: "educational",
    RuntimeEvidenceType.MOCK_EXAMINATION_RESULTS: "mastery",
    RuntimeEvidenceType.OFFICIAL_EXAMINATION_RESULTS: "constitutional",
    RuntimeEvidenceType.SESSION_DURATION: "informational",
    RuntimeEvidenceType.BUTTON_CLICKS: "informational",
    RuntimeEvidenceType.CHECKLIST_TICKS: "informational",
    RuntimeEvidenceType.RECOMMENDATION_PREFERENCE: "informational",
}


@dataclass(frozen=True)
class CandidateObservation:
    """Generated-state observation — not yet Accepted evidence."""

    observation_id: str
    type_id: RuntimeEvidenceType
    recorded_at: datetime
    student_id: str
    session_id: str
    topic_id: str = ""
    mission_instance_id: str = ""
    stage: str = ""
    activity_id: str = ""
    payload: dict[str, Any] | None = None
    lifecycle_state: str = "generated"

    def to_opaque(self) -> dict[str, Any]:
        return {
            "observation_id": self.observation_id,
            "type_id": self.type_id.value,
            "recorded_at": self.recorded_at.isoformat(),
            "student_id": self.student_id,
            "session_id": self.session_id,
            "topic_id": self.topic_id,
            "mission_instance_id": self.mission_instance_id,
            "stage": self.stage,
            "activity_id": self.activity_id,
            "payload": dict(self.payload or {}),
            "lifecycle_state": self.lifecycle_state,
            "ceiling_grade": TYPE_CEILING_GRADE.get(self.type_id, "informational"),
        }

    @classmethod
    def create(
        cls,
        *,
        observation_id: str,
        type_id: RuntimeEvidenceType | str,
        student_id: str,
        session_id: str,
        recorded_at: datetime | None = None,
        topic_id: str = "",
        mission_instance_id: str = "",
        stage: str = "",
        activity_id: str = "",
        payload: dict[str, Any] | None = None,
    ) -> CandidateObservation:
        tid = (
            type_id
            if isinstance(type_id, RuntimeEvidenceType)
            else RuntimeEvidenceType(str(type_id).strip())
        )
        return cls(
            observation_id=observation_id.strip(),
            type_id=tid,
            recorded_at=recorded_at or datetime.now(tz=UTC),
            student_id=student_id.strip(),
            session_id=session_id.strip(),
            topic_id=(topic_id or "").strip(),
            mission_instance_id=(mission_instance_id or "").strip(),
            stage=(stage or "").strip(),
            activity_id=(activity_id or "").strip(),
            payload=dict(payload or {}),
            lifecycle_state="generated",
        )

    @classmethod
    def from_opaque(cls, raw: dict[str, Any] | None) -> CandidateObservation | None:
        if not isinstance(raw, dict) or not raw.get("type_id"):
            return None
        recorded = raw.get("recorded_at")
        if isinstance(recorded, str):
            try:
                recorded_at = datetime.fromisoformat(recorded)
            except ValueError:
                recorded_at = datetime.now(tz=UTC)
        elif isinstance(recorded, datetime):
            recorded_at = recorded
        else:
            recorded_at = datetime.now(tz=UTC)
        try:
            return cls.create(
                observation_id=str(raw.get("observation_id") or ""),
                type_id=str(raw["type_id"]),
                student_id=str(raw.get("student_id") or ""),
                session_id=str(raw.get("session_id") or ""),
                recorded_at=recorded_at,
                topic_id=str(raw.get("topic_id") or ""),
                mission_instance_id=str(raw.get("mission_instance_id") or ""),
                stage=str(raw.get("stage") or ""),
                activity_id=str(raw.get("activity_id") or ""),
                payload=dict(raw.get("payload") or {}),
            )
        except (ValueError, KeyError):
            return None

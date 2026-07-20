"""Policy governing Educational Digital Twin memory updates.

Architecture Source
    STUDENT_DIGITAL_TWIN.md
Concept
    Twin Update Policy
"""

from __future__ import annotations

from domain.education.digital_twin.entities.evidence_history import (
    EvidenceHistoryEntry,
)
from domain.education.digital_twin.entities.intervention_history import (
    InterventionHistoryEntry,
)
from domain.education.digital_twin.enums import (
    LearnerActivityStatus,
    MisconceptionPresence,
    TwinStatus,
)
from domain.education.digital_twin.value_objects.learning_trajectory import (
    LearningTrajectory,
    TrajectoryPoint,
)
from domain.education.foundation.base import require_non_empty_text
from domain.education.foundation.errors import EducationalInvariantViolation


class TwinUpdatePolicy:
    """Enforces Twin memory-update law without educational reasoning.

    Rules:
    - archived twins are immutable
    - evidence history is append-only and never lost
    - intervention history is append-only and never rewritten
    - trajectory grows only by append
    """

    @staticmethod
    def assert_mutable(status: TwinStatus, *, action: str) -> None:
        if status is TwinStatus.ARCHIVED:
            raise EducationalInvariantViolation(
                f"archived twin cannot {action}",
                invariant="EducationalDigitalTwin.immutable_when_archived",
            )

    @staticmethod
    def assert_can_archive(status: TwinStatus) -> None:
        if status is TwinStatus.ARCHIVED:
            raise EducationalInvariantViolation(
                "twin is already archived",
                invariant="EducationalDigitalTwin.archive.already",
            )
        if status is not TwinStatus.ACTIVE:
            raise EducationalInvariantViolation(
                "only ACTIVE twins may be archived",
                invariant="EducationalDigitalTwin.archive.from_active",
            )

    @staticmethod
    def next_evidence_sequence(
        history: list[EvidenceHistoryEntry] | tuple[EvidenceHistoryEntry, ...],
    ) -> int:
        if not history:
            return 1
        return history[-1].sequence + 1

    @staticmethod
    def next_intervention_sequence(
        history: list[InterventionHistoryEntry]
        | tuple[InterventionHistoryEntry, ...],
    ) -> int:
        if not history:
            return 1
        return history[-1].sequence + 1

    @staticmethod
    def assert_evidence_appendable(
        history: list[EvidenceHistoryEntry] | tuple[EvidenceHistoryEntry, ...],
        entry: EvidenceHistoryEntry,
    ) -> None:
        if not isinstance(entry, EvidenceHistoryEntry):
            raise EducationalInvariantViolation(
                "evidence append requires EvidenceHistoryEntry",
                invariant="TwinUpdatePolicy.evidence.type",
            )
        expected = TwinUpdatePolicy.next_evidence_sequence(history)
        if entry.sequence != expected:
            raise EducationalInvariantViolation(
                "evidence sequence must continue append-only history",
                invariant="TwinUpdatePolicy.evidence.sequence",
            )
        existing_ids = {item.evidence_id.value for item in history}
        if entry.evidence_id.value in existing_ids:
            raise EducationalInvariantViolation(
                "cannot lose uniqueness of evidence history — duplicate evidence_id",
                invariant="TwinUpdatePolicy.evidence.unique",
            )
        existing_entries = {item.entry_id.value for item in history}
        if entry.entry_id.value in existing_entries:
            raise EducationalInvariantViolation(
                "duplicate evidence history entry_id",
                invariant="TwinUpdatePolicy.evidence.entry_unique",
            )

    @staticmethod
    def assert_intervention_appendable(
        history: list[InterventionHistoryEntry]
        | tuple[InterventionHistoryEntry, ...],
        entry: InterventionHistoryEntry,
    ) -> None:
        if not isinstance(entry, InterventionHistoryEntry):
            raise EducationalInvariantViolation(
                "intervention append requires InterventionHistoryEntry",
                invariant="TwinUpdatePolicy.intervention.type",
            )
        expected = TwinUpdatePolicy.next_intervention_sequence(history)
        if entry.sequence != expected:
            raise EducationalInvariantViolation(
                "intervention sequence must continue append-only history",
                invariant="TwinUpdatePolicy.intervention.sequence",
            )
        existing_entries = {item.entry_id.value for item in history}
        if entry.entry_id.value in existing_entries:
            raise EducationalInvariantViolation(
                "cannot rewrite historical interventions — duplicate entry_id",
                invariant="TwinUpdatePolicy.intervention.entry_unique",
            )

    @staticmethod
    def assert_history_preserved(
        before_count: int,
        after_count: int,
        *,
        kind: str,
    ) -> None:
        if after_count < before_count:
            raise EducationalInvariantViolation(
                f"cannot lose {kind} history",
                invariant=f"TwinUpdatePolicy.{kind}.preserved",
            )

    @staticmethod
    def assert_trajectory_append(
        trajectory: LearningTrajectory, point: TrajectoryPoint
    ) -> LearningTrajectory:
        return trajectory.with_appended(point)

    @staticmethod
    def assert_learner_activity_transition(
        current: LearnerActivityStatus,
        nxt: LearnerActivityStatus,
    ) -> LearnerActivityStatus:
        if not isinstance(nxt, LearnerActivityStatus):
            raise EducationalInvariantViolation(
                "activity_status must be a LearnerActivityStatus",
                invariant="TwinUpdatePolicy.learner_activity.type",
            )
        if current is LearnerActivityStatus.JOURNEY_COMPLETE and nxt is not current:
            raise EducationalInvariantViolation(
                "journey_complete learner activity is terminal",
                invariant="TwinUpdatePolicy.learner_activity.terminal",
            )
        return nxt

    @staticmethod
    def assert_misconception_presence_transition(
        current: MisconceptionPresence,
        nxt: MisconceptionPresence,
    ) -> MisconceptionPresence:
        if not isinstance(nxt, MisconceptionPresence):
            raise EducationalInvariantViolation(
                "presence must be a MisconceptionPresence",
                invariant="TwinUpdatePolicy.misconception_presence.type",
            )
        # CLEARED may return to ACTIVE/SUSPECTED if re-recorded; no other bans.
        # Twin remembers; it does not diagnose legality of educational meaning.
        _ = current
        return nxt

    @staticmethod
    def assert_archive_note(note: str | None) -> str | None:
        if note is None:
            return None
        return require_non_empty_text(note, "archive_note")

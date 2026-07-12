"""Structural Mission Completion / Failure evidence linkage hooks.

Behaviour / planning evidence candidates only — never mastery, exam readiness,
or Knowledge / Memory / Performance belief writes. Recording happens outside
this domain package via product paths → Learning Evidence → Behaviour Strategy.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class MissionOutcomeIdentity(StrEnum):
    """Structural completion / failure outcome identities (not mastery)."""

    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"
    EXPIRED = "expired"


class BehaviourEvidenceCategoryHint(StrEnum):
    """Evidence category hint for later recording — never Knowledge/Memory."""

    BEHAVIOUR = "behaviour"
    PLANNING = "planning"


COMPLETION_OUTCOME_CATALOGUE: tuple[MissionOutcomeIdentity, ...] = tuple(
    MissionOutcomeIdentity
)


@dataclass(frozen=True)
class MissionEvidenceHooks:
    """Structural linkage slots for Mission Completion / Failure recording.

    Attributes:
        completion_outcome_identities: Allowed outcome identities for recording.
        behaviour_evidence_category_hint: Behaviour / planning — never mastery.
        journal_or_recording_refs: Optional linkage identities when available.
        notes: Structural notes — never mastery writes or Twin belief claims.
        mastery_implied: Always False — Completion ≠ mastery / exam readiness.
    """

    completion_outcome_identities: tuple[MissionOutcomeIdentity, ...]
    behaviour_evidence_category_hint: BehaviourEvidenceCategoryHint
    journal_or_recording_refs: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()
    mastery_implied: bool = False

    @classmethod
    def create(
        cls,
        *,
        completion_outcome_identities: list[MissionOutcomeIdentity]
        | tuple[MissionOutcomeIdentity, ...]
        | None = None,
        behaviour_evidence_category_hint: BehaviourEvidenceCategoryHint
        | str = BehaviourEvidenceCategoryHint.BEHAVIOUR,
        journal_or_recording_refs: list[str] | tuple[str, ...] | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
    ) -> MissionEvidenceHooks:
        """Construct structural evidence hooks (Completion ≠ mastery)."""
        outcomes = tuple(
            completion_outcome_identities
            if completion_outcome_identities is not None
            else COMPLETION_OUTCOME_CATALOGUE
        )
        if not outcomes:
            raise ValueError("completion_outcome_identities must be non-empty")
        hint = (
            behaviour_evidence_category_hint
            if isinstance(
                behaviour_evidence_category_hint, BehaviourEvidenceCategoryHint
            )
            else BehaviourEvidenceCategoryHint(behaviour_evidence_category_hint)
        )
        if hint not in (
            BehaviourEvidenceCategoryHint.BEHAVIOUR,
            BehaviourEvidenceCategoryHint.PLANNING,
        ):
            raise ValueError(
                "behaviour_evidence_category_hint must be behaviour or planning"
            )
        note_tags = list(notes or ())
        for required in (
            "completion_not_mastery",
            "completion_not_exam_readiness",
            "behaviour_or_planning_evidence_only",
        ):
            if required not in note_tags:
                note_tags.append(required)
        return cls(
            completion_outcome_identities=outcomes,
            behaviour_evidence_category_hint=hint,
            journal_or_recording_refs=tuple(journal_or_recording_refs or ()),
            notes=tuple(note_tags),
            mastery_implied=False,
        )

    @classmethod
    def default_behaviour_hooks(
        cls,
        *,
        journal_or_recording_refs: list[str] | tuple[str, ...] | None = None,
    ) -> MissionEvidenceHooks:
        """Default Behaviour-category hooks for Mission / MissionTask."""
        return cls.create(
            behaviour_evidence_category_hint=BehaviourEvidenceCategoryHint.BEHAVIOUR,
            journal_or_recording_refs=journal_or_recording_refs,
        )

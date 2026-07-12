"""Candidate contrast projected from Decision candidate set only.

“Why not Y?” uses Decision statuses — never invents rejected alternatives.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.decision.action_types import ActionFamily, ActionIntent
from app.domain.decision.candidate import CandidateAction, CandidateStatus
from app.domain.decision.decision import Decision


@dataclass(frozen=True)
class CandidateContrast:
    """One contrast entry drawn from a Decision candidate.

    Attributes:
        candidate_id: Identity within the Decision candidate set.
        family: Action family considered.
        curriculum_entity_id: Syllabus scope when present.
        intent: Named tension from the candidate.
        status: Decision candidate status (considered / demoted / blocked).
        note_tags: Structural tags from Decision — not invented.
    """

    candidate_id: str
    family: ActionFamily
    curriculum_entity_id: str | None
    intent: ActionIntent
    status: CandidateStatus
    note_tags: tuple[str, ...] = ()

    @classmethod
    def from_candidate(cls, candidate: CandidateAction) -> CandidateContrast:
        """Project one Decision candidate into a contrast entry."""
        return cls(
            candidate_id=candidate.candidate_id,
            family=candidate.family,
            curriculum_entity_id=candidate.curriculum_entity_id,
            intent=candidate.intent,
            status=candidate.status,
            note_tags=candidate.note_tags,
        )


def project_candidate_contrast(
    decision: Decision,
) -> tuple[CandidateContrast, ...]:
    """Build contrast entries for non-selected Decision candidates.

    Selected candidate is the suggestion authority; contrast covers considered,
    demoted, and blocked alternatives only. Never invents candidates.
    """
    contrasts: list[CandidateContrast] = []
    for candidate in decision.candidates:
        if candidate.status == CandidateStatus.SELECTED:
            continue
        contrasts.append(CandidateContrast.from_candidate(candidate))
    return tuple(contrasts)

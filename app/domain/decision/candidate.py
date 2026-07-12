"""Candidate action representation for Decision Engine.

The candidate set is mandatory on every core Decision — opaque single-action
output without alternatives is forbidden.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.decision.action_types import ActionFamily, ActionIntent


class CandidateStatus(StrEnum):
    """Status of a candidate within the Decision candidate set."""

    SELECTED = "selected"
    CONSIDERED = "considered"
    DEMOTED_BY_CONSTRAINT = "demoted_by_constraint"
    BLOCKED = "blocked"


class FeasibilityEnvelope(StrEnum):
    """Structural session-fit tags relative to Constraints (not scores)."""

    AMPLE = "ample"
    TIGHT = "tight"
    EXCEEDS = "exceeds"
    PROTECT = "protect"
    UNKNOWN = "unknown"


@dataclass(frozen=True)
class CandidateAction:
    """One structured alternative considered before selection.

    Attributes:
        candidate_id: Stable id within this evaluation's candidate set.
        family: Action family.
        curriculum_entity_id: Official syllabus identity when applicable.
        intent: Named educational tension addressed.
        status: Role in the candidate set.
        feasibility: Structural fit relative to Constraints.
        twin_domains: Twin domains that nominated this candidate.
        readiness_factor_ids: Readiness factors that nominated this candidate.
        note_tags: Short structural nomination tags.
    """

    candidate_id: str
    family: ActionFamily
    curriculum_entity_id: str | None
    intent: ActionIntent
    status: CandidateStatus
    feasibility: FeasibilityEnvelope = FeasibilityEnvelope.UNKNOWN
    twin_domains: tuple[str, ...] = ()
    readiness_factor_ids: tuple[str, ...] = ()
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        candidate_id: str,
        family: ActionFamily | str,
        *,
        curriculum_entity_id: str | None = None,
        intent: ActionIntent | str = ActionIntent.EVIDENCE_CREATING,
        status: CandidateStatus | str = CandidateStatus.CONSIDERED,
        feasibility: FeasibilityEnvelope | str = FeasibilityEnvelope.UNKNOWN,
        twin_domains: list[str] | tuple[str, ...] | None = None,
        readiness_factor_ids: list[str] | tuple[str, ...] | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> CandidateAction:
        """Construct a CandidateAction."""
        normalized_id = candidate_id.strip() if isinstance(candidate_id, str) else ""
        if not normalized_id:
            raise ValueError("candidate_id must be a non-empty string")
        fam = family if isinstance(family, ActionFamily) else ActionFamily(family)
        inten = intent if isinstance(intent, ActionIntent) else ActionIntent(intent)
        stat = (
            status if isinstance(status, CandidateStatus) else CandidateStatus(status)
        )
        feas = (
            feasibility
            if isinstance(feasibility, FeasibilityEnvelope)
            else FeasibilityEnvelope(feasibility)
        )
        entity = None
        if curriculum_entity_id is not None:
            stripped = curriculum_entity_id.strip()
            entity = stripped or None
        return cls(
            candidate_id=normalized_id,
            family=fam,
            curriculum_entity_id=entity,
            intent=inten,
            status=stat,
            feasibility=feas,
            twin_domains=tuple(twin_domains or ()),
            readiness_factor_ids=tuple(readiness_factor_ids or ()),
            note_tags=tuple(note_tags or ()),
        )

    def with_status(self, status: CandidateStatus | str) -> CandidateAction:
        """Return a copy with updated status (immutable)."""
        stat = (
            status if isinstance(status, CandidateStatus) else CandidateStatus(status)
        )
        return CandidateAction(
            candidate_id=self.candidate_id,
            family=self.family,
            curriculum_entity_id=self.curriculum_entity_id,
            intent=self.intent,
            status=stat,
            feasibility=self.feasibility,
            twin_domains=self.twin_domains,
            readiness_factor_ids=self.readiness_factor_ids,
            note_tags=self.note_tags,
        )

    def with_feasibility(
        self, feasibility: FeasibilityEnvelope | str
    ) -> CandidateAction:
        """Return a copy with updated feasibility envelope."""
        feas = (
            feasibility
            if isinstance(feasibility, FeasibilityEnvelope)
            else FeasibilityEnvelope(feasibility)
        )
        return CandidateAction(
            candidate_id=self.candidate_id,
            family=self.family,
            curriculum_entity_id=self.curriculum_entity_id,
            intent=self.intent,
            status=self.status,
            feasibility=feas,
            twin_domains=self.twin_domains,
            readiness_factor_ids=self.readiness_factor_ids,
            note_tags=self.note_tags,
        )

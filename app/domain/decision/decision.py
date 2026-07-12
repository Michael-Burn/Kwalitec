"""Decision model — live read-side selection result.

Immutable, explainable, curriculum-bound. Not a Twin write-domain peer.
Not Recommendation packaging. Not Mission generation.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum

from app.domain.decision.action_types import SelectedAction
from app.domain.decision.candidate import CandidateAction, CandidateStatus
from app.domain.decision.constraints import ConstraintClass
from app.domain.decision.reason_codes import ReasonCodeRef
from app.domain.readiness.curriculum_context import CurriculumFormat
from app.domain.readiness.factors import OverallPosture, WarrantPosture


class DecisionWarrantPosture(StrEnum):
    """Warrant honesty inherited onto the Decision when readiness is thin."""

    INHERITED_LOW = "inherited_low"
    INHERITED_MEDIUM = "inherited_medium"
    INHERITED_HIGH = "inherited_high"
    COLD_START = "cold_start"
    NOT_YET_KNOWABLE = "not_yet_knowable"


@dataclass(frozen=True)
class DecisionScope:
    """Scope identity for one Decision evaluation.

    Attributes:
        student_id: Learner identity from Twin.
        curriculum_id: Syllabus identity when known.
        sitting_date: Target sitting when known.
        exam_label: Current exam label when known.
    """

    student_id: str
    curriculum_id: str | None = None
    sitting_date: date | None = None
    exam_label: str | None = None

    @classmethod
    def create(
        cls,
        student_id: str,
        *,
        curriculum_id: str | None = None,
        sitting_date: date | None = None,
        exam_label: str | None = None,
    ) -> DecisionScope:
        """Construct a DecisionScope."""
        normalized = student_id.strip() if isinstance(student_id, str) else ""
        if not normalized:
            raise ValueError("student_id must be a non-empty string")
        return cls(
            student_id=normalized,
            curriculum_id=curriculum_id,
            sitting_date=sitting_date,
            exam_label=exam_label,
        )


@dataclass(frozen=True)
class DecisionLineage:
    """Lineage hooks supporting explainability (Curriculum → Evidence → Twin → …).

    Attributes:
        twin_domains: Twin domain tags consulted.
        readiness_factor_ids: Readiness factor ids consulted.
        curriculum_entity_ids: Curriculum identities used.
        evidence_ids: Evidence lineage hooks when Twin exposes them.
        value_rationale_tags: Short structural tension tags — not marketing.
    """

    twin_domains: tuple[str, ...] = ()
    readiness_factor_ids: tuple[str, ...] = ()
    curriculum_entity_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    value_rationale_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        twin_domains: list[str] | tuple[str, ...] | None = None,
        readiness_factor_ids: list[str] | tuple[str, ...] | None = None,
        curriculum_entity_ids: list[str] | tuple[str, ...] | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        value_rationale_tags: list[str] | tuple[str, ...] | None = None,
    ) -> DecisionLineage:
        """Construct DecisionLineage with defensive tuple copies."""
        return cls(
            twin_domains=tuple(twin_domains or ()),
            readiness_factor_ids=tuple(readiness_factor_ids or ()),
            curriculum_entity_ids=tuple(curriculum_entity_ids or ()),
            evidence_ids=tuple(evidence_ids or ()),
            value_rationale_tags=tuple(value_rationale_tags or ()),
        )


@dataclass(frozen=True)
class ConstraintAcknowledgement:
    """Visible record that constraints demoted or reshaped candidates.

    Attributes:
        constraint_class: Which constraint class applied.
        demoted_candidate_ids: Candidates demoted or reshaped.
        note_tags: Structural notes — educational need remains visible.
    """

    constraint_class: ConstraintClass
    demoted_candidate_ids: tuple[str, ...] = ()
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        constraint_class: ConstraintClass | str,
        *,
        demoted_candidate_ids: list[str] | tuple[str, ...] | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> ConstraintAcknowledgement:
        """Construct a ConstraintAcknowledgement."""
        cclass = (
            constraint_class
            if isinstance(constraint_class, ConstraintClass)
            else ConstraintClass(constraint_class)
        )
        return cls(
            constraint_class=cclass,
            demoted_candidate_ids=tuple(demoted_candidate_ids or ()),
            note_tags=tuple(note_tags or ()),
        )


@dataclass(frozen=True)
class Decision:
    """Authoritative next-action selection for one input snapshot.

    Produced only by Decision Engine. Never writes Twin beliefs. Never
    recomputes readiness. Never packages recommendations or missions.

    Attributes:
        scope: Student / curriculum / sitting scope.
        selected: Canonical selected action.
        candidates: Mandatory ordered candidate set (includes selected).
        reason_codes: Stable authored educational justifications (≥1).
        lineage: Twin / readiness / curriculum / evidence hooks.
        constraint_acknowledgements: Visible feasibility demotions.
        warrant_posture: Inherited honesty under low warrant / cold start.
        curriculum_format: V1 / V2 format tag.
        readiness_overall_posture: Context-only readiness overall (cited).
        readiness_overall_warrant: Context-only readiness warrant (cited).
        engine_version: Additive audit tag.
        evaluation_id: Optional audit identity.
        evaluated_at: Optional timestamp (omit for determinism tests).
    """

    scope: DecisionScope
    selected: SelectedAction
    candidates: tuple[CandidateAction, ...]
    reason_codes: tuple[ReasonCodeRef, ...]
    lineage: DecisionLineage
    constraint_acknowledgements: tuple[ConstraintAcknowledgement, ...]
    warrant_posture: DecisionWarrantPosture
    curriculum_format: CurriculumFormat
    readiness_overall_posture: OverallPosture
    readiness_overall_warrant: WarrantPosture
    engine_version: str
    evaluation_id: str | None = None
    evaluated_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        scope: DecisionScope,
        selected: SelectedAction,
        candidates: list[CandidateAction] | tuple[CandidateAction, ...],
        reason_codes: list[ReasonCodeRef] | tuple[ReasonCodeRef, ...],
        lineage: DecisionLineage,
        constraint_acknowledgements: list[ConstraintAcknowledgement]
        | tuple[ConstraintAcknowledgement, ...]
        | None = None,
        warrant_posture: DecisionWarrantPosture | str,
        curriculum_format: CurriculumFormat | str,
        readiness_overall_posture: OverallPosture | str,
        readiness_overall_warrant: WarrantPosture | str,
        engine_version: str,
        evaluation_id: str | None = None,
        evaluated_at: datetime | None = None,
    ) -> Decision:
        """Construct a Decision after validating explainability contracts.

        Raises:
            ValueError: If candidates empty, no reason codes, or selected missing.
        """
        candidate_tuple = tuple(candidates)
        reason_tuple = tuple(reason_codes)
        if not candidate_tuple:
            raise ValueError("Decision.candidates must be non-empty")
        if not reason_tuple:
            raise ValueError("Decision.reason_codes must contain at least one code")
        _validate_selected_in_candidates(selected, candidate_tuple)

        warrant = (
            warrant_posture
            if isinstance(warrant_posture, DecisionWarrantPosture)
            else DecisionWarrantPosture(warrant_posture)
        )
        fmt = (
            curriculum_format
            if isinstance(curriculum_format, CurriculumFormat)
            else CurriculumFormat(str(curriculum_format).strip().lower())
        )
        overall = (
            readiness_overall_posture
            if isinstance(readiness_overall_posture, OverallPosture)
            else OverallPosture(readiness_overall_posture)
        )
        r_warrant = (
            readiness_overall_warrant
            if isinstance(readiness_overall_warrant, WarrantPosture)
            else WarrantPosture(readiness_overall_warrant)
        )
        return cls(
            scope=scope,
            selected=selected,
            candidates=candidate_tuple,
            reason_codes=reason_tuple,
            lineage=lineage,
            constraint_acknowledgements=tuple(constraint_acknowledgements or ()),
            warrant_posture=warrant,
            curriculum_format=fmt,
            readiness_overall_posture=overall,
            readiness_overall_warrant=r_warrant,
            engine_version=engine_version,
            evaluation_id=evaluation_id,
            evaluated_at=evaluated_at,
        )

    @property
    def selected_candidate(self) -> CandidateAction:
        """Return the candidate marked selected."""
        for candidate in self.candidates:
            if candidate.status == CandidateStatus.SELECTED:
                return candidate
        raise KeyError("no selected candidate in Decision.candidates")

    @property
    def considered_candidates(self) -> tuple[CandidateAction, ...]:
        """Candidates with considered status."""
        return tuple(
            c for c in self.candidates if c.status == CandidateStatus.CONSIDERED
        )

    @property
    def demoted_candidates(self) -> tuple[CandidateAction, ...]:
        """Candidates demoted by constraints."""
        return tuple(
            c
            for c in self.candidates
            if c.status == CandidateStatus.DEMOTED_BY_CONSTRAINT
        )


def _validate_selected_in_candidates(
    selected: SelectedAction,
    candidates: tuple[CandidateAction, ...],
) -> None:
    selected_marks = [c for c in candidates if c.status == CandidateStatus.SELECTED]
    if len(selected_marks) != 1:
        raise ValueError(
            "Decision.candidates must contain exactly one CandidateStatus.SELECTED"
        )
    marked = selected_marks[0]
    if marked.family != selected.family:
        raise ValueError("selected action family must match selected candidate")
    if marked.curriculum_entity_id != selected.curriculum_entity_id:
        raise ValueError(
            "selected action curriculum_entity_id must match selected candidate"
        )

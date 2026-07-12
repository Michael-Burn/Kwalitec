"""Derived ReadinessState and factor judgement types.

Read-side educational judgement objects — not Twin write-domain peers.
Immutable, factorable, warrant-aware. No scoring percentages.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime

from app.domain.readiness.curriculum_context import CurriculumFormat
from app.domain.readiness.factors import (
    FACTOR_CATALOGUE,
    FactorId,
    FactorPosture,
    OverallPosture,
    WarrantPosture,
)


@dataclass(frozen=True)
class FactorAttribution:
    """Citations supporting one factor judgement.

    Attributes:
        twin_domains: Twin domain tags consulted (e.g. knowledge, performance).
        curriculum_entity_ids: Curriculum topic/section ids used.
        evidence_ids: Evidence lineage hooks when Twin exposes them.
        notes: Short structural attribution tags — not LLM prose.
    """

    twin_domains: tuple[str, ...] = ()
    curriculum_entity_ids: tuple[str, ...] = ()
    evidence_ids: tuple[str, ...] = ()
    notes: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        twin_domains: list[str] | tuple[str, ...] | None = None,
        curriculum_entity_ids: list[str] | tuple[str, ...] | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        notes: list[str] | tuple[str, ...] | None = None,
    ) -> FactorAttribution:
        """Construct a FactorAttribution with defensive tuple copies."""
        return cls(
            twin_domains=tuple(twin_domains or ()),
            curriculum_entity_ids=tuple(curriculum_entity_ids or ()),
            evidence_ids=tuple(evidence_ids or ()),
            notes=tuple(notes or ()),
        )


@dataclass(frozen=True)
class FactorJudgement:
    """Judgement for one catalogue factor.

    Attributes:
        factor_id: Stable catalogue identity.
        posture: Educational posture for this dimension.
        warrant: Per-factor Evidence Warrant.
        attribution: Twin / curriculum / evidence citations.
        sparse: True when inputs are thin or absent.
    """

    factor_id: FactorId
    posture: FactorPosture
    warrant: WarrantPosture
    attribution: FactorAttribution
    sparse: bool = False

    @classmethod
    def create(
        cls,
        factor_id: FactorId | str,
        *,
        posture: FactorPosture | str,
        warrant: WarrantPosture | str,
        attribution: FactorAttribution | None = None,
        sparse: bool = False,
    ) -> FactorJudgement:
        """Construct a FactorJudgement."""
        fid = factor_id if isinstance(factor_id, FactorId) else FactorId(factor_id)
        post = posture if isinstance(posture, FactorPosture) else FactorPosture(posture)
        war = (
            warrant
            if isinstance(warrant, WarrantPosture)
            else WarrantPosture(warrant)
        )
        return cls(
            factor_id=fid,
            posture=post,
            warrant=war,
            attribution=(
                attribution
                if attribution is not None
                else FactorAttribution.create()
            ),
            sparse=sparse,
        )


@dataclass(frozen=True)
class ReadinessScope:
    """Scope identity for a readiness derivation.

    Attributes:
        student_id: Learner identity from Twin.
        curriculum_id: Syllabus identity (Twin and/or CurriculumContext).
        sitting_date: Target sitting / completion date when known.
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
    ) -> ReadinessScope:
        """Construct a ReadinessScope."""
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
class ReadinessState:
    """Derived, factorable preparedness judgement for one Twin snapshot.

    Produced only by Readiness Aggregation. Never written by Update Strategies.
    Never selects next actions. Never invents Twin beliefs.

    Attributes:
        scope: Student / curriculum / sitting scope.
        overall_posture: Synthesised preparedness posture (honest under uncertainty).
        overall_warrant: Evidence Warrant constraining assertiveness.
        factors: Full catalogue of factor judgements (ordered).
        curriculum_format: V1 / V2 format tag from CurriculumContext.
        cold_start: True when educational Twin domains are empty/sparse.
        derivation_id: Optional audit identity.
        derived_at: Optional derivation timestamp (does not affect structural equality
            when callers omit it for determinism tests).
        goal_constraint_notes: Structural tags describing Goals context used.
    """

    scope: ReadinessScope
    overall_posture: OverallPosture
    overall_warrant: WarrantPosture
    factors: tuple[FactorJudgement, ...]
    curriculum_format: CurriculumFormat
    cold_start: bool = False
    derivation_id: str | None = None
    derived_at: datetime | None = None
    goal_constraint_notes: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        *,
        scope: ReadinessScope,
        overall_posture: OverallPosture | str,
        overall_warrant: WarrantPosture | str,
        factors: list[FactorJudgement] | tuple[FactorJudgement, ...],
        curriculum_format: CurriculumFormat | str,
        cold_start: bool = False,
        derivation_id: str | None = None,
        derived_at: datetime | None = None,
        goal_constraint_notes: list[str] | tuple[str, ...] | None = None,
    ) -> ReadinessState:
        """Construct a ReadinessState after validating the factor catalogue.

        Raises:
            ValueError: If factors do not cover the full catalogue exactly once.
        """
        posture = (
            overall_posture
            if isinstance(overall_posture, OverallPosture)
            else OverallPosture(overall_posture)
        )
        warrant = (
            overall_warrant
            if isinstance(overall_warrant, WarrantPosture)
            else WarrantPosture(overall_warrant)
        )
        fmt = (
            curriculum_format
            if isinstance(curriculum_format, CurriculumFormat)
            else CurriculumFormat(str(curriculum_format).strip().lower())
        )
        factor_tuple = tuple(factors)
        _validate_catalogue(factor_tuple)
        return cls(
            scope=scope,
            overall_posture=posture,
            overall_warrant=warrant,
            factors=factor_tuple,
            curriculum_format=fmt,
            cold_start=cold_start,
            derivation_id=derivation_id,
            derived_at=derived_at,
            goal_constraint_notes=tuple(goal_constraint_notes or ()),
        )

    def factor(self, factor_id: FactorId | str) -> FactorJudgement:
        """Return the judgement for ``factor_id``.

        Raises:
            KeyError: If the factor is missing (should not happen for valid states).
        """
        fid = factor_id if isinstance(factor_id, FactorId) else FactorId(factor_id)
        for judgement in self.factors:
            if judgement.factor_id == fid:
                return judgement
        raise KeyError(f"factor not found: {fid}")

    @property
    def sparse_factor_ids(self) -> tuple[FactorId, ...]:
        """Factor ids marked sparse."""
        return tuple(j.factor_id for j in self.factors if j.sparse)


def _validate_catalogue(factors: tuple[FactorJudgement, ...]) -> None:
    ids = tuple(j.factor_id for j in factors)
    expected = FACTOR_CATALOGUE
    if len(ids) != len(expected) or set(ids) != set(expected):
        raise ValueError(
            "ReadinessState.factors must cover the full factor catalogue exactly once; "
            f"got {ids!r}, expected {expected!r}"
        )

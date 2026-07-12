"""Student Calibration Contract — Version 1.0 (immutable Application input).

Closed Presentation → Application declaration artefact for Twin birth.
Carries what the student declared. Never educational judgement.

See ``CAPABILITY_3_6_4_STUDENT_CALIBRATION_CONTRACT.md``.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from enum import StrEnum
from typing import Any

CONTRACT_VERSION_1_0 = "1.0"

SOURCE_SELF_DECLARED = "self_declared"
WARRANT_THIN = "thin"


class PreviouslyStudied(StrEnum):
    """Coarse prior-engagement declaration."""

    FIRST_TIME = "first_time"
    PREVIOUSLY_STUDIED = "previously_studied"


class CoreReadingCompleted(StrEnum):
    """Declared Core Reading completion posture (paper-level tokens).

    Section-scoped completion uses ``CoreReadingDeclaration`` with section ids.
    """

    NONE = "none"
    WHOLE_PAPER = "whole_paper"


class StudyObjective(StrEnum):
    """Recognised Version 1.0 study objective tokens."""

    FIRST_SIT = "first_sit"
    REVISION = "revision"
    FINISH_REMAINING = "finish_remaining"
    RESIT = "resit"


class BeginnerOrHistoryPosture(StrEnum):
    """Explicit empty-history vs history-present posture."""

    EMPTY_HISTORY = "empty_history"
    HISTORY_PRESENT = "history_present"


class DeclaredPosture(StrEnum):
    """Derived coarse posture — structural honesty, never a readiness band."""

    FIRST_TIME = "first_time"
    RETURNING = "returning"
    REVISION_FRAMED = "revision_framed"
    REPEAT_ATTEMPT_FRAMED = "repeat_attempt_framed"


@dataclass(frozen=True)
class CurriculumExamScope:
    """Canonical curriculum / exam scope for Twin birth."""

    curriculum_id: str
    current_exam: str | None = None

    @classmethod
    def create(
        cls,
        curriculum_id: str,
        *,
        current_exam: str | None = None,
    ) -> CurriculumExamScope:
        """Construct a curriculum / exam scope.

        Raises:
            ValueError: If ``curriculum_id`` is blank.
        """
        normalized = _require_nonblank(curriculum_id, "curriculum_id")
        exam = _optional_nonblank(current_exam)
        return cls(curriculum_id=normalized, current_exam=exam)


@dataclass(frozen=True)
class CoreReadingDeclaration:
    """Declared Core Reading completion (none / whole paper / section-scoped)."""

    posture: CoreReadingCompleted
    section_ids: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        posture: CoreReadingCompleted | str,
        *,
        section_ids: list[str] | tuple[str, ...] | None = None,
    ) -> CoreReadingDeclaration:
        """Construct a Core Reading declaration.

        Raises:
            ValueError: If posture is unrecognised or section ids are blank.
        """
        resolved = _as_enum(posture, CoreReadingCompleted, "core_reading_completed")
        ids = _normalize_id_tuple(section_ids, field_name="core_reading section_ids")
        if resolved is CoreReadingCompleted.NONE and ids:
            raise ValueError(
                "core_reading_completed=none must not carry section_ids"
            )
        return cls(posture=resolved, section_ids=ids)

    @classmethod
    def none(cls) -> CoreReadingDeclaration:
        """Explicit none / unread Core Reading declaration."""
        return cls(posture=CoreReadingCompleted.NONE, section_ids=())

    @classmethod
    def whole_paper(cls) -> CoreReadingDeclaration:
        """Declared whole-paper Core Reading completion."""
        return cls(posture=CoreReadingCompleted.WHOLE_PAPER, section_ids=())


@dataclass(frozen=True)
class PreviousAttemptsDeclaration:
    """Declared prior sitting attempts — history facts only, never marks."""

    none: bool
    count: int | None = None
    sitting_labels: tuple[str, ...] = ()
    declared_outcome: str | None = None

    @classmethod
    def create_none(cls) -> PreviousAttemptsDeclaration:
        """Explicit no prior attempts."""
        return cls(none=True, count=None, sitting_labels=(), declared_outcome=None)

    @classmethod
    def create(
        cls,
        *,
        count: int | None = None,
        sitting_labels: list[str] | tuple[str, ...] | None = None,
        declared_outcome: str | None = None,
    ) -> PreviousAttemptsDeclaration:
        """Construct a non-empty attempt-history declaration.

        Raises:
            ValueError: If neither count nor sitting labels are provided, or
                count is negative.
        """
        labels = _normalize_id_tuple(
            sitting_labels, field_name="previous_attempts sitting_labels"
        )
        if count is None and not labels:
            raise ValueError(
                "previous_attempts requires count and/or sitting_labels "
                "(or use create_none)"
            )
        if count is not None:
            if isinstance(count, bool) or not isinstance(count, int):
                raise ValueError(
                    f"previous_attempts count must be int or None, got {type(count)!r}"
                )
            if count < 0:
                raise ValueError(
                    f"previous_attempts count must be non-negative, got {count}"
                )
            if count == 0 and not labels:
                return cls.create_none()
        outcome = _optional_nonblank(declared_outcome)
        return cls(
            none=False,
            count=count,
            sitting_labels=labels,
            declared_outcome=outcome,
        )


@dataclass(frozen=True)
class IntendedSitting:
    """Target exam sitting / date anchor."""

    sitting_date: date | None = None
    sitting_label: str | None = None

    @classmethod
    def create(
        cls,
        *,
        sitting_date: date | None = None,
        sitting_label: str | None = None,
    ) -> IntendedSitting:
        """Construct an intended sitting anchor.

        Raises:
            ValueError: If both date and label are absent.
        """
        label = _optional_nonblank(sitting_label)
        if sitting_date is None and label is None:
            raise ValueError(
                "intended_sitting requires sitting_date and/or sitting_label"
            )
        if sitting_date is not None and not isinstance(sitting_date, date):
            raise ValueError(
                f"sitting_date must be date or None, got {type(sitting_date)!r}"
            )
        return cls(sitting_date=sitting_date, sitting_label=label)


@dataclass(frozen=True)
class StudentCalibrationContract:
    """Immutable Version 1.0 Student Calibration Contract.

    Sole self-declared educational-history input to Calibration Twin birth.
    """

    authorised_student_identity: str
    curriculum_exam_scope: CurriculumExamScope
    contract_version: str
    declaration_confirmation: bool
    previously_studied: PreviouslyStudied
    core_reading_completed: CoreReadingDeclaration
    previous_attempts: PreviousAttemptsDeclaration
    study_objective: StudyObjective
    intended_sitting: IntendedSitting
    beginner_or_history_posture: BeginnerOrHistoryPosture
    declared_completed_sections: tuple[str, ...] = ()
    declared_study_capacity: float | None = None
    optional_notes: str | None = None
    emitted_at: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        authorised_student_identity: str,
        curriculum_exam_scope: CurriculumExamScope,
        declaration_confirmation: bool,
        previously_studied: PreviouslyStudied | str,
        core_reading_completed: CoreReadingDeclaration,
        previous_attempts: PreviousAttemptsDeclaration,
        study_objective: StudyObjective | str,
        intended_sitting: IntendedSitting,
        beginner_or_history_posture: BeginnerOrHistoryPosture | str,
        contract_version: str = CONTRACT_VERSION_1_0,
        declared_completed_sections: list[str] | tuple[str, ...] | None = None,
        declared_study_capacity: float | None = None,
        optional_notes: str | None = None,
        emitted_at: datetime | None = None,
    ) -> StudentCalibrationContract:
        """Construct an immutable Student Calibration Contract snapshot.

        Does not structurally validate educational coherence — that is the
        Builder's job. Factory only normalises closed shapes.

        Raises:
            ValueError: If required identity / enums / shapes are unlawful.
        """
        student_id = _require_nonblank(
            authorised_student_identity, "authorised_student_identity"
        )
        if not isinstance(curriculum_exam_scope, CurriculumExamScope):
            raise ValueError(
                "curriculum_exam_scope must be CurriculumExamScope, "
                f"got {type(curriculum_exam_scope)!r}"
            )
        if not isinstance(core_reading_completed, CoreReadingDeclaration):
            raise ValueError(
                "core_reading_completed must be CoreReadingDeclaration, "
                f"got {type(core_reading_completed)!r}"
            )
        if not isinstance(previous_attempts, PreviousAttemptsDeclaration):
            raise ValueError(
                "previous_attempts must be PreviousAttemptsDeclaration, "
                f"got {type(previous_attempts)!r}"
            )
        if not isinstance(intended_sitting, IntendedSitting):
            raise ValueError(
                "intended_sitting must be IntendedSitting, "
                f"got {type(intended_sitting)!r}"
            )
        if not isinstance(declaration_confirmation, bool):
            raise ValueError(
                "declaration_confirmation must be bool, "
                f"got {type(declaration_confirmation)!r}"
            )
        version = _require_nonblank(contract_version, "contract_version")
        studied = _as_enum(
            previously_studied, PreviouslyStudied, "previously_studied"
        )
        objective = _as_enum(study_objective, StudyObjective, "study_objective")
        posture = _as_enum(
            beginner_or_history_posture,
            BeginnerOrHistoryPosture,
            "beginner_or_history_posture",
        )
        sections = _normalize_id_tuple(
            declared_completed_sections,
            field_name="declared_completed_sections",
        )
        capacity = _validate_optional_capacity(declared_study_capacity)
        notes = optional_notes if isinstance(optional_notes, str) else None
        if notes is not None:
            notes = notes.strip() or None

        return cls(
            authorised_student_identity=student_id,
            curriculum_exam_scope=curriculum_exam_scope,
            contract_version=version,
            declaration_confirmation=declaration_confirmation,
            previously_studied=studied,
            core_reading_completed=core_reading_completed,
            previous_attempts=previous_attempts,
            study_objective=objective,
            intended_sitting=intended_sitting,
            beginner_or_history_posture=posture,
            declared_completed_sections=sections,
            declared_study_capacity=capacity,
            optional_notes=notes,
            emitted_at=emitted_at,
        )


def derive_declared_posture(
    contract: StudentCalibrationContract,
) -> DeclaredPosture:
    """Derive coarse declared posture from closed Required fields only.

    Structural honesty label — never a readiness band or Mid/High theatre.
    """
    if (
        contract.previously_studied is PreviouslyStudied.FIRST_TIME
        or contract.beginner_or_history_posture
        is BeginnerOrHistoryPosture.EMPTY_HISTORY
    ):
        return DeclaredPosture.FIRST_TIME

    if (
        not contract.previous_attempts.none
        or contract.study_objective is StudyObjective.RESIT
    ):
        return DeclaredPosture.REPEAT_ATTEMPT_FRAMED

    if contract.study_objective is StudyObjective.REVISION:
        return DeclaredPosture.REVISION_FRAMED

    return DeclaredPosture.RETURNING


def _require_nonblank(value: Any, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_nonblank(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"optional string must be str or None, got {type(value)!r}")
    normalized = value.strip()
    return normalized or None


def _normalize_id_tuple(
    values: list[str] | tuple[str, ...] | None,
    *,
    field_name: str,
) -> tuple[str, ...]:
    if values is None:
        return ()
    if not isinstance(values, list | tuple):
        raise ValueError(f"{field_name} must be a list/tuple of strings or None")
    normalized: list[str] = []
    seen: set[str] = set()
    for raw in values:
        if not isinstance(raw, str):
            raise ValueError(f"{field_name} entries must be strings, got {type(raw)!r}")
        item = raw.strip()
        if not item:
            raise ValueError(f"{field_name} must not contain blank ids")
        if item not in seen:
            seen.add(item)
            normalized.append(item)
    return tuple(normalized)


def _as_enum(value: Any, enum_cls: type[StrEnum], field_name: str) -> Any:
    if isinstance(value, enum_cls):
        return value
    if isinstance(value, str):
        try:
            return enum_cls(value.strip())
        except ValueError as exc:
            raise ValueError(
                f"{field_name} is not a recognised {enum_cls.__name__}: {value!r}"
            ) from exc
    raise ValueError(
        f"{field_name} must be {enum_cls.__name__} or str, got {type(value)!r}"
    )


def _validate_optional_capacity(value: float | None) -> float | None:
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int | float):
        raise ValueError(
            f"declared_study_capacity must be a number or None, got {type(value)!r}"
        )
    capacity = float(value)
    if capacity < 0.0:
        raise ValueError(
            f"declared_study_capacity must be non-negative, got {capacity}"
        )
    return capacity

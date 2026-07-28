"""Exceptions for Student Curriculum Binding application services."""

from __future__ import annotations

from app.domain.student_curriculum_binding.invariants import BindingInvariantError


class StudentCurriculumBindingError(Exception):
    """Base error for student curriculum binding services."""


class EditionNotFoundError(StudentCurriculumBindingError):
    """Requested curriculum edition does not exist."""


class InstanceNotFoundError(StudentCurriculumBindingError):
    """Requested Student Curriculum Instance does not exist."""


class BindingGateError(StudentCurriculumBindingError):
    """Binding invariant or gate failed."""

    def __init__(self, message: str, *, cause: Exception | None = None) -> None:
        super().__init__(message)
        self.cause = cause


def gate_from_invariant(exc: BindingInvariantError) -> BindingGateError:
    return BindingGateError(str(exc), cause=exc)

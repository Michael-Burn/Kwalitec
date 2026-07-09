"""Curriculum Engine exceptions.

Every exception carries a clear, human-readable message so that callers
can surface meaningful errors to developers or administrators.
"""

from __future__ import annotations


class CurriculumError(Exception):
    """Base exception for all Curriculum Engine errors."""


class CurriculumNotFoundError(CurriculumError):
    """Raised when a requested curriculum / paper / version does not exist."""

    def __init__(self, exam_key: str, version: str | None = None) -> None:
        if version:
            msg = f"Curriculum not found: {exam_key} version {version}"
        else:
            msg = f"Curriculum not found: {exam_key}"
        super().__init__(msg)
        self.exam_key = exam_key
        self.version = version


class CurriculumLoadError(CurriculumError):
    """Raised when a curriculum file cannot be parsed or loaded."""

    def __init__(self, path: str, reason: str) -> None:
        super().__init__(f"Failed to load curriculum from {path}: {reason}")
        self.path = path
        self.reason = reason


class CurriculumValidationError(CurriculumError):
    """Raised when curriculum data fails integrity validation."""

    def __init__(self, messages: list[str]) -> None:
        joined = "; ".join(messages)
        super().__init__(f"Curriculum validation failed: {joined}")
        self.messages = messages


class DuplicateTopicCodeError(CurriculumValidationError):
    """Raised when two topics share the same code within a curriculum."""

    def __init__(self, code: str) -> None:
        super().__init__([f"Duplicate topic code: {code}"])
        self.code = code


class DuplicateLearningOutcomeCodeError(CurriculumValidationError):
    """Raised when two learning outcomes share the same code."""

    def __init__(self, code: str) -> None:
        super().__init__([f"Duplicate learning outcome code: {code}"])
        self.code = code


class InvalidWeightingError(CurriculumValidationError):
    """Raised when topic weightings do not sum to approximately 100 %."""

    def __init__(self, total: float) -> None:
        super().__init__(
            [f"Total weighting {total:.1f}% is not within acceptable range (95–105 %)"]
        )
        self.total = total


class InvalidPrerequisiteError(CurriculumValidationError):
    """Raised when a topic references a prerequisite that does not exist."""

    def __init__(self, topic_id: str, prerequisite: str) -> None:
        super().__init__(
            [f"Topic '{topic_id}' has unknown prerequisite '{prerequisite}'"]
        )
        self.topic_id = topic_id
        self.prerequisite = prerequisite
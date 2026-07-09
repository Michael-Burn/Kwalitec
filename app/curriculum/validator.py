"""Curriculum integrity validator.

Validates that a loaded Curriculum instance satisfies all business rules:
unique codes, valid weightings, positive hours, valid prerequisites, etc.
"""

from __future__ import annotations

from app.curriculum.exceptions import (
    CurriculumValidationError,
    DuplicateLearningOutcomeCodeError,
    DuplicateTopicCodeError,
    InvalidPrerequisiteError,
    InvalidWeightingError,
)
from app.curriculum.models import Curriculum

WEIGHTING_TOLERANCE = 5.0  # ±5 % from 100


def validate_curriculum(curriculum: Curriculum) -> None:
    """Run all validation rules against a curriculum.

    Raises:
        CurriculumValidationError: If any rule is violated.
    """
    messages: list[str] = []

    # --- unique topic IDs ---
    ids: set[str] = set()
    for t in curriculum.topics:
        if t.id in ids:
            messages.append(f"Duplicate topic id: {t.id}")
        ids.add(t.id)

    # --- unique topic codes ---
    codes: set[str] = set()
    for t in curriculum.topics:
        if t.code in codes:
            messages.append(f"Duplicate topic code: {t.code}")
        codes.add(t.code)

    # --- unique learning outcome codes ---
    lo_codes: set[str] = set()
    for t in curriculum.topics:
        for lo in t.learning_outcomes:
            if lo.code in lo_codes:
                messages.append(f"Duplicate learning outcome code: {lo.code}")
            lo_codes.add(lo.code)

    # --- weighting sum ≈ 100 ---
    total_weight = sum(t.weighting for t in curriculum.topics)
    if abs(total_weight - 100.0) > WEIGHTING_TOLERANCE:
        messages.append(
            f"Total weighting {total_weight:.1f}% is outside acceptable range "
            f"(100 ± {WEIGHTING_TOLERANCE}%)"
        )

    # --- positive estimated hours ---
    for t in curriculum.topics:
        if t.estimated_hours <= 0:
            messages.append(
                f"Topic '{t.id}' has non-positive estimated_hours: {t.estimated_hours}"
            )

    # --- valid prerequisites ---
    valid_ids = {t.id for t in curriculum.topics}
    for t in curriculum.topics:
        for prereq in t.prerequisites:
            if prereq not in valid_ids:
                messages.append(
                    f"Topic '{t.id}' references unknown prerequisite '{prereq}'"
                )

    # --- difficulty enum ---
    valid_difficulties = {"foundational", "intermediate", "advanced"}
    for t in curriculum.topics:
        if t.difficulty not in valid_difficulties:
            messages.append(
                f"Topic '{t.id}' has invalid difficulty '{t.difficulty}'"
            )

    # --- positive revision days ---
    for t in curriculum.topics:
        for lo in t.learning_outcomes:
            if lo.suggested_revision_days <= 0:
                messages.append(
                    f"Learning outcome '{lo.code}' has non-positive "
                    f"suggested_revision_days: {lo.suggested_revision_days}"
                )

    if messages:
        raise CurriculumValidationError(messages)


def validate_duplicate_topic_codes(curriculum: Curriculum) -> None:
    """Validate that no two topics share the same code."""
    seen: set[str] = set()
    for t in curriculum.topics:
        if t.code in seen:
            raise DuplicateTopicCodeError(t.code)
        seen.add(t.code)


def validate_duplicate_lo_codes(curriculum: Curriculum) -> None:
    """Validate that no two learning outcomes share the same code."""
    seen: set[str] = set()
    for t in curriculum.topics:
        for lo in t.learning_outcomes:
            if lo.code in seen:
                raise DuplicateLearningOutcomeCodeError(lo.code)
            seen.add(lo.code)


def validate_weightings(curriculum: Curriculum) -> None:
    """Validate that topic weightings sum to approximately 100%."""
    total = sum(t.weighting for t in curriculum.topics)
    if abs(total - 100.0) > WEIGHTING_TOLERANCE:
        raise InvalidWeightingError(total)


def validate_prerequisites(curriculum: Curriculum) -> None:
    """Validate that all prerequisite references are valid topic IDs."""
    valid_ids = {t.id for t in curriculum.topics}
    for t in curriculum.topics:
        for prereq in t.prerequisites:
            if prereq not in valid_ids:
                raise InvalidPrerequisiteError(t.id, prereq)

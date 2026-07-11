"""Curriculum integrity validator.

Validates that a loaded Curriculum instance satisfies all business rules:
unique codes, valid weightings, positive hours, valid prerequisites, etc.

Supports both V1 (flat) and V2 (hierarchical) formats.
"""

from __future__ import annotations

from app.curriculum.exceptions import (
    CurriculumValidationError,
    DuplicateLearningOutcomeCodeError,
    DuplicateTopicCodeError,
    InvalidPrerequisiteError,
    InvalidWeightingError,
)
from app.curriculum.models import (
    Curriculum,
    CurriculumDefinition,
)

WEIGHTING_TOLERANCE = 5.0  # ±5 % from 100


# ═══════════════════════════════════════════════════════════════════════════════
# V1 Validation (Legacy)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_curriculum(curriculum: Curriculum) -> None:
    """Run all V1 validation rules against a curriculum.

    Args:
        curriculum: The V1 Curriculum instance to validate.

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


# ═══════════════════════════════════════════════════════════════════════════════
# V2 Validation (Canonical Format)
# ═══════════════════════════════════════════════════════════════════════════════

def validate_curriculum_v2(curriculum: CurriculumDefinition) -> None:
    """Run all V2 validation rules against a curriculum.

    Args:
        curriculum: The V2 CurriculumDefinition instance to validate.

    Raises:
        CurriculumValidationError: If any rule is violated.
    """
    messages: list[str] = []

    # --- unique section IDs ---
    section_ids: set[str] = set()
    for s in curriculum.sections:
        if s.id in section_ids:
            messages.append(f"Duplicate section id: {s.id}")
        section_ids.add(s.id)

    # --- unique topic IDs ---
    topic_ids: set[str] = set()
    for s in curriculum.sections:
        for t in s.topics:
            if t.id in topic_ids:
                messages.append(f"Duplicate topic id: {t.id}")
            topic_ids.add(t.id)

    # --- unique learning objective IDs ---
    lo_ids: set[str] = set()
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.id in lo_ids:
                    messages.append(f"Duplicate learning objective id: {lo.id}")
                lo_ids.add(lo.id)

    # --- unique learning objective codes ---
    lo_codes: set[str] = set()
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.code in lo_codes:
                    messages.append(f"Duplicate learning objective code: {lo.code}")
                lo_codes.add(lo.code)

    # --- section weight sum ≈ 100 ---
    total_weight = sum(s.exam_weight for s in curriculum.sections)
    if abs(total_weight - 100.0) > WEIGHTING_TOLERANCE:
        messages.append(
            f"Total section weight {total_weight:.1f}% is outside acceptable range "
            f"(100 ± {WEIGHTING_TOLERANCE}%)"
        )

    # --- positive estimated hours ---
    for s in curriculum.sections:
        if s.estimated_hours <= 0:
            messages.append(
                f"Section '{s.id}' has non-positive estimated_hours: {s.estimated_hours}"
            )

    # --- positive estimated minutes ---
    for s in curriculum.sections:
        for t in s.topics:
            if t.estimated_minutes <= 0:
                messages.append(
                    f"Topic '{t.id}' has non-positive estimated_minutes: {t.estimated_minutes}"
                )

    # --- positive LO estimated minutes ---
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.estimated_minutes <= 0:
                    messages.append(
                        f"Learning objective '{lo.id}' has non-positive "
                        f"estimated_minutes: {lo.estimated_minutes}"
                    )

    # --- valid section_id references ---
    for s in curriculum.sections:
        for t in s.topics:
            if t.section_id != s.id:
                messages.append(
                    f"Topic '{t.id}' has section_id '{t.section_id}' "
                    f"that does not match parent section '{s.id}'"
                )

    # --- valid topic_id references ---
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.topic_id != t.id:
                    messages.append(
                        f"Learning objective '{lo.id}' has topic_id '{lo.topic_id}' "
                        f"that does not match parent topic '{t.id}'"
                    )

    # --- difficulty enum ---
    valid_difficulties = {"foundational", "intermediate", "advanced"}
    for s in curriculum.sections:
        if s.difficulty not in valid_difficulties:
            messages.append(
                f"Section '{s.id}' has invalid difficulty '{s.difficulty}'"
            )
        for t in s.topics:
            if t.difficulty not in valid_difficulties:
                messages.append(
                    f"Topic '{t.id}' has invalid difficulty '{t.difficulty}'"
                )

    # --- cognitive_level enum ---
    valid_cognitive_levels = {"remember", "understand", "apply", "analyze", "evaluate", "create"}
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.cognitive_level not in valid_cognitive_levels:
                    messages.append(
                        f"Learning objective '{lo.id}' has invalid "
                        f"cognitive_level '{lo.cognitive_level}'"
                    )

    # --- learning_type enum ---
    valid_learning_types = {"concept", "procedure", "problem_solving", "application", "analysis"}
    for s in curriculum.sections:
        for t in s.topics:
            for lo in t.learning_objectives:
                if lo.learning_type not in valid_learning_types:
                    messages.append(
                        f"Learning objective '{lo.id}' has invalid "
                        f"learning_type '{lo.learning_type}'"
                    )

    # --- positive display_order ---
    for s in curriculum.sections:
        if s.display_order <= 0:
            messages.append(
                f"Section '{s.id}' has non-positive display_order: {s.display_order}"
            )
        for t in s.topics:
            if t.display_order <= 0:
                messages.append(
                    f"Topic '{t.id}' has non-positive display_order: {t.display_order}"
                )
            for lo in t.learning_objectives:
                if lo.display_order <= 0:
                    messages.append(
                        f"Learning objective '{lo.id}' has non-positive "
                        f"display_order: {lo.display_order}"
                    )

    if messages:
        raise CurriculumValidationError(messages)


# ═══════════════════════════════════════════════════════════════════════════════
# Unified Validation API
# ═══════════════════════════════════════════════════════════════════════════════

def validate_curriculum_unified(curriculum: Curriculum | CurriculumDefinition) -> None:
    """Validate a curriculum (V1 or V2) by dispatching to the appropriate validator.

    Args:
        curriculum: The curriculum instance to validate.

    Raises:
        CurriculumValidationError: If any rule is violated.
        TypeError: If curriculum is neither V1 nor V2 format.
    """
    if isinstance(curriculum, Curriculum):
        validate_curriculum(curriculum)
    elif isinstance(curriculum, CurriculumDefinition):
        validate_curriculum_v2(curriculum)
    else:
        raise TypeError(
            f"Expected Curriculum or CurriculumDefinition, got {type(curriculum).__name__}"
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Legacy V1 Validators (preserved for backwards compatibility)
# ═══════════════════════════════════════════════════════════════════════════════

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
"""Semantic roles for extracted curriculum text (EQ-001).

Only ``EDUCATIONAL`` (and educational subtypes) should become curriculum
hierarchy entities. Other roles are retained for diagnostics / review packs.
"""

from __future__ import annotations

from enum import StrEnum


class ContentRole(StrEnum):
    """Classification of a text block or structural node."""

    EDUCATIONAL = "educational_content"
    HEADING = "heading"
    LEARNING_OBJECTIVE = "learning_objective"
    EXAMPLE = "example"
    EXERCISE = "exercise"
    DEFINITION = "definition"
    FORMULA = "formula"
    WORKED_EXAMPLE = "worked_example"
    EXAM_TIP = "exam_tip"
    NAVIGATION = "navigation"
    PUBLISHER_METADATA = "publisher_metadata"
    FRONT_MATTER = "front_matter"
    TABLE_OF_CONTENTS = "table_of_contents"
    COPYRIGHT = "copyright"
    QUALIFICATION_INFORMATION = "qualification_information"
    ASSESSMENT_LOGISTICS = "assessment_logistics"
    APPENDIX = "appendix"
    INDEX = "index"
    REFERENCES = "references"
    BLANK_ARTEFACT = "blank_artefact"


# Roles that must never become Subject / Module / Topic / Objective nodes.
NON_CURRICULUM_ROLES: frozenset[ContentRole] = frozenset(
    {
        ContentRole.NAVIGATION,
        ContentRole.PUBLISHER_METADATA,
        ContentRole.FRONT_MATTER,
        ContentRole.TABLE_OF_CONTENTS,
        ContentRole.COPYRIGHT,
        ContentRole.QUALIFICATION_INFORMATION,
        ContentRole.ASSESSMENT_LOGISTICS,
        ContentRole.APPENDIX,
        ContentRole.INDEX,
        ContentRole.REFERENCES,
        ContentRole.BLANK_ARTEFACT,
    }
)


def is_curriculum_role(role: ContentRole | str | None) -> bool:
    """Return True when the role may become a curriculum hierarchy entity."""
    if role is None:
        return True
    try:
        value = role if isinstance(role, ContentRole) else ContentRole(str(role))
    except ValueError:
        return True
    return value not in NON_CURRICULUM_ROLES

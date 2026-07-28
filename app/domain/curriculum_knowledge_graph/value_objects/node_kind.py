"""Classification of Curriculum Knowledge Graph node kinds."""

from __future__ import annotations

from enum import StrEnum


class CkgNodeKind(StrEnum):
    """Educational classification of a CKG node."""

    SUBJECT = "subject"
    TOPIC = "topic"
    SECTION = "section"
    SUBSECTION = "subsection"
    LEARNING_OBJECTIVE = "learning_objective"
    DEFINITION = "definition"
    FORMULA = "formula"
    WORKED_EXAMPLE = "worked_example"
    PRACTICE_EXERCISE = "practice_exercise"
    READING_REFERENCE = "reading_reference"
    SYLLABUS_OUTCOME = "syllabus_outcome"

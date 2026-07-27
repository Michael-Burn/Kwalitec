"""Student identity within the Student Digital Twin bounded context."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Student:
    """Canonical learner identity owned by the Twin aggregate.

    Curriculum content is never stored here — only the learner reference.
    """

    student_id: str
    display_name: str = ""
    subject_code: str = ""
    workspace_id: str = ""
    external_user_id: str | None = None

    def __post_init__(self) -> None:
        if not (self.student_id or "").strip():
            raise ValueError("student_id is required")

"""Syllabus Outcome — official outcome reference linked to the graph."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import (
    optional_non_empty,
    require_non_empty,
)
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass(frozen=True)
class SyllabusOutcome:
    """Official syllabus outcome reference (code/text ref — not a dump)."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    outcome_code: str
    statement_ref: str = ""

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        outcome_code: str,
        *,
        statement_ref: str = "",
    ) -> SyllabusOutcome:
        """Construct a SyllabusOutcome owned by subject or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.SYLLABUS_OUTCOME:
            raise ValueError(
                "SyllabusOutcome.stable_id must be a syllabus_outcome id"
            )
        if owner.depth not in {
            StableIdDepth.SUBJECT,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError("SyllabusOutcome.owner_id must be subject or LO")
        if sid.parent_id() != owner:
            raise ValueError(
                "SyllabusOutcome.stable_id must be a child of owner_id"
            )
        return cls(
            stable_id=sid,
            owner_id=owner,
            outcome_code=require_non_empty(outcome_code, "outcome_code"),
            statement_ref=optional_non_empty(statement_ref) or "",
        )

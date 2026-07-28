"""Worked Example — educational object owned by a Subsection or LO."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import require_non_empty
from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass(frozen=True)
class WorkedExample:
    """Worked-example educational object (title/summary only)."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    title: str
    summary: str = ""

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        title: str,
        *,
        summary: str = "",
    ) -> WorkedExample:
        """Construct a WorkedExample owned by a subsection or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.WORKED_EXAMPLE:
            raise ValueError("WorkedExample.stable_id must be a worked_example id")
        if owner.depth not in {
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError("WorkedExample.owner_id must be subsection or LO")
        if sid.parent_id() != owner:
            raise ValueError("WorkedExample.stable_id must be a child of owner_id")
        return cls(
            stable_id=sid,
            owner_id=owner,
            title=require_non_empty(title, "title"),
            summary=summary.strip() if isinstance(summary, str) else "",
        )

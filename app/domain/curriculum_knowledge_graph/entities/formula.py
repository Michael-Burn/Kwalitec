"""Formula — educational object owned by a Subsection or LO."""

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
class Formula:
    """Formula educational object (label / notation refs only)."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    title: str
    notation: str = ""
    latex: str | None = None

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        title: str,
        *,
        notation: str = "",
        latex: str | None = None,
    ) -> Formula:
        """Construct a Formula owned by a subsection or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.FORMULA:
            raise ValueError("Formula.stable_id must be a formula id")
        if owner.depth not in {
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError("Formula.owner_id must be subsection or LO")
        if sid.parent_id() != owner:
            raise ValueError("Formula.stable_id must be a child of owner_id")
        return cls(
            stable_id=sid,
            owner_id=owner,
            title=require_non_empty(title, "title"),
            notation=notation.strip() if isinstance(notation, str) else "",
            latex=optional_non_empty(latex),
        )

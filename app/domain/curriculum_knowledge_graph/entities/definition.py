"""Definition — educational object owned by a Subsection."""

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
class Definition:
    """Definitional educational object (structure/metadata only)."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    title: str
    body: str = ""
    cmp_locator: str | None = None

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        title: str,
        *,
        body: str = "",
        cmp_locator: str | None = None,
    ) -> Definition:
        """Construct a Definition owned by a subsection or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.DEFINITION:
            raise ValueError("Definition.stable_id must be a definition id")
        if owner.depth not in {
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError("Definition.owner_id must be subsection or LO")
        if sid.parent_id() != owner:
            raise ValueError("Definition.stable_id must be a child of owner_id")
        return cls(
            stable_id=sid,
            owner_id=owner,
            title=require_non_empty(title, "title"),
            body=body.strip() if isinstance(body, str) else "",
            cmp_locator=optional_non_empty(cmp_locator),
        )

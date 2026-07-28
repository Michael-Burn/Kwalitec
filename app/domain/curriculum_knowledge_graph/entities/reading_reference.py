"""Reading Reference — CMP citation (no PDF bytes)."""

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
class ReadingReference:
    """CMP / Core Reading citation locator — never stores document bytes."""

    stable_id: StableCurriculumId
    owner_id: StableCurriculumId
    title: str
    document_kind: str = "cmp"
    locator: str = ""

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        owner_id: str | StableCurriculumId,
        title: str,
        *,
        document_kind: str = "cmp",
        locator: str = "",
    ) -> ReadingReference:
        """Construct a ReadingReference owned by subject, subsection, or LO."""
        sid = StableCurriculumId.of(stable_id)
        owner = StableCurriculumId.of(owner_id)
        if sid.kind != CkgNodeKind.READING_REFERENCE:
            raise ValueError(
                "ReadingReference.stable_id must be a reading_reference id"
            )
        if owner.depth not in {
            StableIdDepth.SUBJECT,
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError(
                "ReadingReference.owner_id must be subject, subsection, or LO"
            )
        if sid.parent_id() != owner:
            raise ValueError(
                "ReadingReference.stable_id must be a child of owner_id"
            )
        return cls(
            stable_id=sid,
            owner_id=owner,
            title=require_non_empty(title, "title"),
            document_kind=require_non_empty(document_kind, "document_kind"),
            locator=optional_non_empty(locator) or "",
        )

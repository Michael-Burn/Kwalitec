"""Subject — examinable programme root of a Curriculum Knowledge Graph."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph._text import require_non_empty
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)


@dataclass(frozen=True)
class Subject:
    """Graph root for one IFoA (or similar) subject edition.

    Attributes:
        stable_id: Edition-stable subject identity (e.g. ``CS1``).
        code: Short subject code (normally matches stable_id).
        title: Operational title (not copyrighted syllabus prose dump).
        provider: Awarding body (e.g. ``IFoA``).
        edition_label: Curriculum edition (e.g. ``2026``) — not in stable_id.
        sequence_index: Order when multiple subjects are loaded (0-based).
    """

    stable_id: StableCurriculumId
    code: str
    title: str
    provider: str
    edition_label: str
    sequence_index: int = 0

    @classmethod
    def create(
        cls,
        stable_id: str | StableCurriculumId,
        title: str,
        *,
        code: str | None = None,
        provider: str = "IFoA",
        edition_label: str,
        sequence_index: int = 0,
    ) -> Subject:
        """Construct a Subject after validating invariants."""
        sid = StableCurriculumId.of(stable_id)
        if sid.depth != StableIdDepth.SUBJECT:
            raise ValueError("Subject.stable_id must be subject-depth")
        label = require_non_empty(title, "title")
        subject_code = require_non_empty(code or sid.value, "code").upper()
        provider_v = require_non_empty(provider, "provider")
        edition = require_non_empty(edition_label, "edition_label")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        return cls(
            stable_id=sid,
            code=subject_code,
            title=label,
            provider=provider_v,
            edition_label=edition,
            sequence_index=sequence_index,
        )

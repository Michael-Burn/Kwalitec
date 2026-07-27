"""Document type registry — extensible curriculum source kinds.

Upload UI and APIs resolve kinds through this registry so CMP / Syllabus
are not hardcoded. Future kinds (core reading, past papers, …) register here.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentTypeDefinition:
    """One curriculum document kind available to Founders."""

    kind: str
    label: str
    description: str
    required_for_publish: bool = False
    accept: str = "application/pdf"
    phase: int = 1


class DocumentTypeRegistry:
    """Lookup table for curriculum document kinds."""

    def __init__(self, definitions: tuple[DocumentTypeDefinition, ...]) -> None:
        self._by_kind = {d.kind: d for d in definitions}
        if len(self._by_kind) != len(definitions):
            raise ValueError("Duplicate document kinds in registry")

    def get(self, kind: str) -> DocumentTypeDefinition | None:
        token = _normalize_kind_token(kind)
        return self._by_kind.get(token)

    def require(self, kind: str) -> DocumentTypeDefinition:
        found = self.get(kind)
        if found is None:
            raise ValueError(f"Unsupported document kind: {kind!r}")
        return found

    def list_kinds(
        self, *, phase: int | None = None
    ) -> tuple[DocumentTypeDefinition, ...]:
        items = tuple(self._by_kind.values())
        if phase is None:
            return items
        return tuple(d for d in items if d.phase <= phase)

    def publish_required(self) -> tuple[DocumentTypeDefinition, ...]:
        return tuple(d for d in self._by_kind.values() if d.required_for_publish)

    def known_kind_tokens(self) -> frozenset[str]:
        return frozenset(self._by_kind)


def _normalize_kind_token(kind: str) -> str:
    return (kind or "").strip().lower().replace("-", "_").replace(" ", "_")


def default_document_type_registry() -> DocumentTypeRegistry:
    """Built-in registry aligned with AssetKind + future curriculum sources."""
    return DocumentTypeRegistry(
        (
            DocumentTypeDefinition(
                kind="cmp",
                label="Official CMP",
                description=(
                    "Curriculum Master Pack — the authoritative source for "
                    "sections, topics, and learning objectives."
                ),
                required_for_publish=True,
                phase=1,
            ),
            DocumentTypeDefinition(
                kind="syllabus",
                label="Official Syllabus",
                description=(
                    "Official syllabus PDF grounding authorised curriculum order."
                ),
                required_for_publish=True,
                phase=1,
            ),
            DocumentTypeDefinition(
                kind="learning_objectives",
                label="Learning Objectives",
                description="Supplementary learning objective document.",
                phase=2,
            ),
            DocumentTypeDefinition(
                kind="formula_sheet",
                label="Formula Sheets",
                description="Official formula sheet for the subject.",
                phase=2,
            ),
            DocumentTypeDefinition(
                kind="core_reading",
                label="Core Reading",
                description="Core reading / study guide material.",
                phase=2,
            ),
            DocumentTypeDefinition(
                kind="assignment_bank",
                label="Assignments",
                description="Assignment bank for practice and assessment.",
                phase=3,
            ),
            DocumentTypeDefinition(
                kind="past_papers",
                label="Past Papers",
                description="Past examination papers.",
                phase=3,
            ),
            DocumentTypeDefinition(
                kind="solutions",
                label="Solutions",
                description="Official or authorised solutions.",
                phase=3,
            ),
            DocumentTypeDefinition(
                kind="exam_reports",
                label="Exam Reports",
                description="Examiner reports and commentary.",
                phase=3,
            ),
            DocumentTypeDefinition(
                kind="lecture_notes",
                label="Lecture Notes",
                description="Lecture notes supporting the syllabus.",
                phase=3,
            ),
            DocumentTypeDefinition(
                kind="supporting_document",
                label="Supporting Document",
                description="Additional supporting curriculum material.",
                phase=1,
            ),
        )
    )

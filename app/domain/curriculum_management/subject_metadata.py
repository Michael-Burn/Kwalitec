"""Subject metadata — labels and tags only, never binary assets."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class SubjectMetadata:
    """Operational metadata for a curriculum subject product.

    Attributes:
        title: Display title (not copyrighted syllabus prose).
        description: Short operational description.
        exam_board: Optional board / awarding body token.
        academic_year: Optional academic year label (e.g. 2026-27).
        locale: BCP-47-ish locale token (default en-GB).
        tags: Immutable operational tags.
    """

    title: str
    description: str = ""
    exam_board: str | None = None
    academic_year: str | None = None
    locale: str = "en-GB"
    tags: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        title: str,
        *,
        description: str = "",
        exam_board: str | None = None,
        academic_year: str | None = None,
        locale: str = "en-GB",
        tags: list[str] | tuple[str, ...] | None = None,
    ) -> SubjectMetadata:
        """Construct SubjectMetadata after validating invariants."""
        label = _require_non_empty(title, "title")
        desc = (description or "").strip()
        board = _optional_token(exam_board, "exam_board")
        year = _optional_token(academic_year, "academic_year")
        loc = _require_non_empty(locale, "locale")
        tag_values = tuple(
            _require_non_empty(tag, "tag") for tag in (tags or ())
        )
        return cls(
            title=label,
            description=desc,
            exam_board=board,
            academic_year=year,
            locale=loc,
            tags=tag_values,
        )

    def with_tags(
        self,
        tags: list[str] | tuple[str, ...],
    ) -> SubjectMetadata:
        """Return a copy with replacement tags."""
        return SubjectMetadata.create(
            self.title,
            description=self.description,
            exam_board=self.exam_board,
            academic_year=self.academic_year,
            locale=self.locale,
            tags=tags,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _optional_token(value: str | None, field_name: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a string or None")
    normalized = value.strip()
    if not normalized:
        return None
    return normalized

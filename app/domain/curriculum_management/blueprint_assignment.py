"""Blueprint assignment — explicit section → blueprint profile linkage."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlueprintAssignment:
    """Associates a curriculum section with an Instructional Blueprint Profile.

    Assignments are explicit. No automatic recommendation.
    """

    assignment_id: str
    version_id: str
    section_ref: str
    blueprint_profile_id: str
    notes: str = ""
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        assignment_id: str,
        version_id: str,
        section_ref: str,
        blueprint_profile_id: str,
        *,
        notes: str = "",
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintAssignment:
        """Construct a BlueprintAssignment after validating invariants."""
        return cls(
            assignment_id=_require_non_empty(assignment_id, "assignment_id"),
            version_id=_require_non_empty(version_id, "version_id"),
            section_ref=_require_non_empty(section_ref, "section_ref"),
            blueprint_profile_id=_require_non_empty(
                blueprint_profile_id, "blueprint_profile_id"
            ),
            notes=(notes or "").strip(),
            metadata=tuple(metadata or ()),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized

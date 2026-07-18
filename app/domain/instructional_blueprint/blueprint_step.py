"""One structural step inside an Instructional Blueprint.

Steps name activity kinds and roles only — never questions, explanations,
or syllabus prose.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class BlueprintStep:
    """Ordered instructional step (structure without educational content).

    Attributes:
        step_id: Stable identity within the blueprint.
        activity_kind: Structural activity kind token (e.g. concept_learning).
        sequence_index: 0-based ordering within the blueprint.
        role: Optional pedagogical role tag (e.g. warm_up, core, consolidate).
        effort_weight: Relative weight contributing to effort estimation (≥ 0).
        required: Whether compilation must retain this step.
        metadata: Immutable structural tags (never educational payloads).
    """

    step_id: str
    activity_kind: str
    sequence_index: int
    role: str | None = None
    effort_weight: int = 1
    required: bool = True
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        step_id: str,
        activity_kind: str,
        *,
        sequence_index: int = 0,
        role: str | None = None,
        effort_weight: int = 1,
        required: bool = True,
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintStep:
        """Construct a BlueprintStep after validating invariants.

        Raises:
            ValueError: On empty identities, negative index, or negative weight.
        """
        sid = _require_non_empty(step_id, "step_id")
        kind = _require_non_empty(activity_kind, "activity_kind")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        if effort_weight < 0:
            raise ValueError("effort_weight must be non-negative")
        return cls(
            step_id=sid,
            activity_kind=_normalise_token(kind),
            sequence_index=sequence_index,
            role=_optional_token(role),
            effort_weight=effort_weight,
            required=bool(required),
            metadata=tuple(metadata or ()),
        )

    def with_index(self, sequence_index: int) -> BlueprintStep:
        """Return a copy with a new sequence_index."""
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        return BlueprintStep(
            step_id=self.step_id,
            activity_kind=self.activity_kind,
            sequence_index=sequence_index,
            role=self.role,
            effort_weight=self.effort_weight,
            required=self.required,
            metadata=self.metadata,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _normalise_token(value: str) -> str:
    return value.strip().lower().replace("-", "_").replace(" ", "_")


def _optional_token(value: str | None) -> str | None:
    if value is None:
        return None
    stripped = value.strip()
    if not stripped:
        return None
    return _normalise_token(stripped)

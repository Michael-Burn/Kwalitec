"""Pedagogical profile describing instructional balance.

Profiles express relative theory / practice / revision / assessment weights.
They never encode curriculum content or student-specific state.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.instructional_blueprint.effort_band import (
    EffortBand,
    resolve_effort_band,
)


@dataclass(frozen=True)
class BlueprintProfile:
    """Structural pedagogical balance for an Instructional Blueprint.

    Attributes:
        profile_id: Stable profile identity.
        theory_weight: Relative theory emphasis (0–100).
        practice_weight: Relative practice emphasis (0–100).
        revision_weight: Relative revision emphasis (0–100).
        assessment_weight: Relative assessment emphasis (0–100).
        default_effort_band: Baseline effort band for compilation.
        intensity: Relative instructional intensity (1–5).
        metadata: Immutable structural tags.
    """

    profile_id: str
    theory_weight: int = 25
    practice_weight: int = 25
    revision_weight: int = 25
    assessment_weight: int = 25
    default_effort_band: EffortBand = EffortBand.MEDIUM
    intensity: int = 3
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        profile_id: str,
        *,
        theory_weight: int = 25,
        practice_weight: int = 25,
        revision_weight: int = 25,
        assessment_weight: int = 25,
        default_effort_band: EffortBand | str = EffortBand.MEDIUM,
        intensity: int = 3,
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintProfile:
        """Construct a BlueprintProfile after validating invariants.

        Raises:
            ValueError: On empty identity, out-of-range weights, or intensity.
        """
        pid = _require_non_empty(profile_id, "profile_id")
        for name, value in (
            ("theory_weight", theory_weight),
            ("practice_weight", practice_weight),
            ("revision_weight", revision_weight),
            ("assessment_weight", assessment_weight),
        ):
            if not isinstance(value, int) or value < 0 or value > 100:
                raise ValueError(f"{name} must be an int in 0..100")
        if not isinstance(intensity, int) or intensity < 1 or intensity > 5:
            raise ValueError("intensity must be an int in 1..5")
        return cls(
            profile_id=pid,
            theory_weight=theory_weight,
            practice_weight=practice_weight,
            revision_weight=revision_weight,
            assessment_weight=assessment_weight,
            default_effort_band=resolve_effort_band(default_effort_band),
            intensity=intensity,
            metadata=tuple(metadata or ()),
        )

    @property
    def total_weight(self) -> int:
        """Sum of the four pedagogical weights."""
        return (
            self.theory_weight
            + self.practice_weight
            + self.revision_weight
            + self.assessment_weight
        )

    @property
    def dominant_dimension(self) -> str:
        """Return the dimension with the highest weight (deterministic ties)."""
        dimensions = (
            ("theory", self.theory_weight),
            ("practice", self.practice_weight),
            ("revision", self.revision_weight),
            ("assessment", self.assessment_weight),
        )
        return max(dimensions, key=lambda item: (item[1], -_DIM_ORDER[item[0]]))[0]

    def normalised_weights(self) -> dict[str, float]:
        """Return weights as fractions of total (0.0 when total is 0)."""
        total = self.total_weight
        if total == 0:
            return {
                "theory": 0.0,
                "practice": 0.0,
                "revision": 0.0,
                "assessment": 0.0,
            }
        return {
            "theory": self.theory_weight / total,
            "practice": self.practice_weight / total,
            "revision": self.revision_weight / total,
            "assessment": self.assessment_weight / total,
        }


_DIM_ORDER = {"theory": 0, "practice": 1, "revision": 2, "assessment": 3}


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized

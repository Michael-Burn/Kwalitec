"""Immutable EducationalObservationSet ready for Twin consumption."""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.reasoning.observations.observation import EducationalObservation


@dataclass(frozen=True)
class EducationalObservationSet:
    """Ordered, immutable set of educational observations for one interpretation."""

    set_id: str
    observations: tuple[EducationalObservation, ...]
    interpretation_version: str
    evidence_bundle_id: str
    reasoning_request_id: str

    def __post_init__(self) -> None:
        if not (self.set_id or "").strip():
            raise ValueError("set_id is required")
        if not (self.interpretation_version or "").strip():
            raise ValueError("interpretation_version is required")
        if not (self.evidence_bundle_id or "").strip():
            raise ValueError("evidence_bundle_id is required")
        if not (self.reasoning_request_id or "").strip():
            raise ValueError("reasoning_request_id is required")
        if not isinstance(self.observations, tuple):
            object.__setattr__(self, "observations", tuple(self.observations))

        seen: set[str] = set()
        for observation in self.observations:
            if not isinstance(observation, EducationalObservation):
                raise TypeError(
                    "EducationalObservationSet accepts EducationalObservation only"
                )
            if observation.observation_id in seen:
                from app.domain.reasoning.interpretation.errors import (
                    DuplicateInterpretedObservation,
                )

                raise DuplicateInterpretedObservation(
                    "duplicate interpreted observation: "
                    f"{observation.observation_id!r}"
                )
            seen.add(observation.observation_id)

    @property
    def observation_ids(self) -> tuple[str, ...]:
        return tuple(o.observation_id for o in self.observations)

    def __len__(self) -> int:
        return len(self.observations)

    def by_category(self, category: str) -> tuple[EducationalObservation, ...]:
        return tuple(o for o in self.observations if o.category.value == category)

"""Observation aggregation for assessment evidence packaging.

Maintains traceability: every evidence item references originating observations.
No information loss; no educational inference.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator, Sequence
from dataclasses import dataclass

from domain.assessment.entities.assessment_observation import AssessmentObservation
from domain.assessment.enums import ObservationKind
from domain.assessment.exceptions import AssessmentInvariantViolation
from domain.assessment.value_objects.ids import ObservationId, QuestionId, SessionId
from domain.education.foundation.base import EducationalValueObject


@dataclass(frozen=True, slots=True)
class ObservationCollection(EducationalValueObject):
    """Ordered, de-duplicated collection of assessment observations.

    Preserves insertion order. Rejects duplicate observation identities and
    mixed session identities.
    """

    observations: tuple[AssessmentObservation, ...] = ()

    def _validate(self) -> None:
        items: list[AssessmentObservation] = []
        seen: set[str] = set()
        session_id: SessionId | None = None
        for observation in self.observations or ():
            if not isinstance(observation, AssessmentObservation):
                raise AssessmentInvariantViolation(
                    "observations must contain AssessmentObservation values",
                    invariant="ObservationCollection.observations.type",
                )
            oid = observation.observation_id.value
            if oid in seen:
                raise AssessmentInvariantViolation(
                    f"duplicate observation_id in collection: {oid}",
                    invariant="ObservationCollection.observations.unique",
                )
            if session_id is None:
                session_id = observation.session_id
            elif observation.session_id != session_id:
                raise AssessmentInvariantViolation(
                    "all observations in a collection must share one session_id",
                    invariant="ObservationCollection.session.uniform",
                )
            seen.add(oid)
            items.append(observation)
        object.__setattr__(self, "observations", tuple(items))

    def __iter__(self) -> Iterator[AssessmentObservation]:
        return iter(self.observations)

    def __len__(self) -> int:
        return len(self.observations)

    def __bool__(self) -> bool:
        return bool(self.observations)

    @property
    def session_id(self) -> SessionId | None:
        if not self.observations:
            return None
        return self.observations[0].session_id

    def observation_ids(self) -> tuple[ObservationId, ...]:
        return tuple(o.observation_id for o in self.observations)

    def question_observations(self) -> tuple[AssessmentObservation, ...]:
        return tuple(
            o
            for o in self.observations
            if o.kind is ObservationKind.QUESTION_ANSWERED
        )

    def distinct_question_ids(self) -> tuple[QuestionId, ...]:
        seen: set[str] = set()
        result: list[QuestionId] = []
        for observation in self.question_observations():
            if observation.question_id is None:
                continue
            if observation.question_id.value in seen:
                continue
            seen.add(observation.question_id.value)
            result.append(observation.question_id)
        return tuple(result)

    def get(self, observation_id: ObservationId) -> AssessmentObservation | None:
        for observation in self.observations:
            if observation.observation_id == observation_id:
                return observation
        return None


class ObservationAggregator:
    """Aggregate raw observations into a validated ObservationCollection."""

    @staticmethod
    def aggregate(
        observations: Sequence[AssessmentObservation] | Iterable[AssessmentObservation],
    ) -> ObservationCollection:
        """Build a collection preserving order and rejecting duplicates."""
        return ObservationCollection(observations=tuple(observations))

    @staticmethod
    def merge(
        *collections: ObservationCollection,
    ) -> ObservationCollection:
        """Concatenate collections while enforcing uniqueness."""
        merged: list[AssessmentObservation] = []
        for collection in collections:
            merged.extend(collection.observations)
        return ObservationCollection(observations=tuple(merged))

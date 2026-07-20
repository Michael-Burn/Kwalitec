"""LearningApplicationService — start and complete learning episodes."""

from __future__ import annotations

from application.commands.complete_learning_episode import CompleteLearningEpisode
from application.commands.start_learning_session import StartLearningSession
from application.dto.learning import LearningEpisodeDTO, LearningSessionDTO
from application.errors import ConflictError, NotFoundError
from application.events.learning import (
    LearningEpisodeCompletedApplicationEvent,
    LearningSessionStartedApplicationEvent,
)
from application.ports.clock import Clock
from application.ports.event_publisher import ApplicationEventPublisher
from application.ports.unit_of_work import UnitOfWork
from application.services.mappers import (
    to_learning_episode_dto,
    to_learning_session_dto,
)
from domain.education.foundation.enums import ConfidenceLevel, ReflectionType
from domain.education.foundation.errors import (
    EducationalDomainError,
    EducationalInvariantViolation,
)
from domain.education.foundation.ids import EvidenceId, LearningEpisodeId, ReflectionId
from domain.education.learning_episode import (
    EpisodeOutcome,
    EpisodeOutcomeId,
    EpisodeOutcomeKind,
    EpisodeReflection,
    LearningEpisode,
)
from domain.education.learning_episode.enums import EpisodeStatus


class LearningApplicationService:
    """Coordinates learning-session workflows against LearningEpisode aggregates.

    Does not choose strategies, diagnose, or calculate mastery.
    """

    def __init__(
        self,
        uow: UnitOfWork,
        events: ApplicationEventPublisher,
        clock: Clock,
    ) -> None:
        self._uow = uow
        self._events = events
        self._clock = clock

    def start_learning_session(
        self, command: StartLearningSession
    ) -> LearningSessionDTO:
        """Load a planned episode, invoke domain ``start``, commit, publish."""
        episode_id = LearningEpisodeId(command.episode_id)
        with self._uow:
            episode = self._uow.episodes.get(episode_id)
            if episode is None:
                raise NotFoundError("LearningEpisode", command.episode_id)
            if episode.status is not EpisodeStatus.PLANNED:
                raise ConflictError(
                    f"episode {command.episode_id} is not planned "
                    f"(status={episode.status.value})"
                )
            try:
                episode.start()
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.episodes.save(episode)
            self._uow.commit()
        self._events.publish(
            LearningSessionStartedApplicationEvent.create(
                episode_id=episode.episode_id.value,
                student_id=episode.student_id,
                occurred_at=self._clock.now(),
            )
        )
        return to_learning_session_dto(episode)

    def complete_learning_episode(
        self, command: CompleteLearningEpisode
    ) -> LearningEpisodeDTO:
        """Record reflection, complete episode under domain rules, commit, publish."""
        episode_id = LearningEpisodeId(command.episode_id)
        with self._uow:
            episode = self._uow.episodes.get(episode_id)
            if episode is None:
                raise NotFoundError("LearningEpisode", command.episode_id)
            if episode.status is not EpisodeStatus.IN_PROGRESS:
                raise ConflictError(
                    f"episode {command.episode_id} is not in progress "
                    f"(status={episode.status.value})"
                )
            try:
                self._finish_remaining_steps(episode)
                if episode.reflection is None:
                    reflection = EpisodeReflection(
                        reflection_id=ReflectionId(command.reflection_id),
                        reflection_type=ReflectionType(command.reflection_type),
                        content=command.reflection_content,
                        perceived_difficulty=(
                            ConfidenceLevel(command.perceived_difficulty)
                            if command.perceived_difficulty
                            else None
                        ),
                        perceived_understanding=(
                            ConfidenceLevel(command.perceived_understanding)
                            if command.perceived_understanding
                            else None
                        ),
                    )
                    episode.record_reflection(reflection)
                outcome = EpisodeOutcome(
                    outcome_id=EpisodeOutcomeId(command.outcome_id),
                    kind=EpisodeOutcomeKind(command.outcome_kind),
                    summary=command.outcome_summary,
                )
                episode.complete(outcome)
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.episodes.save(episode)
            self._uow.commit()
        outcome_kind = (
            episode.outcome.kind.value if episode.outcome is not None else "unknown"
        )
        self._events.publish(
            LearningEpisodeCompletedApplicationEvent.create(
                episode_id=episode.episode_id.value,
                student_id=episode.student_id,
                outcome_kind=outcome_kind,
                occurred_at=self._clock.now(),
            )
        )
        return to_learning_episode_dto(episode)

    def attach_evidence(self, episode_id: str, evidence_id: str) -> LearningEpisodeDTO:
        """Attach an evidence identity to an in-progress episode (coordination)."""
        with self._uow:
            episode = self._uow.episodes.get(LearningEpisodeId(episode_id))
            if episode is None:
                raise NotFoundError("LearningEpisode", episode_id)
            try:
                episode.attach_evidence(EvidenceId(evidence_id))
            except EducationalDomainError as exc:
                raise ConflictError(str(exc)) from exc
            self._uow.episodes.save(episode)
            self._uow.commit()
        return to_learning_episode_dto(episode)

    @staticmethod
    def _finish_remaining_steps(episode: LearningEpisode) -> None:
        """Advance domain sequence until required steps are exhausted."""
        while True:
            try:
                episode.advance_step()
            except EducationalInvariantViolation as exc:
                if exc.invariant in {
                    "SequencingPolicy.exhausted",
                    "SequencingPolicy.not_advanceable",
                }:
                    break
                raise

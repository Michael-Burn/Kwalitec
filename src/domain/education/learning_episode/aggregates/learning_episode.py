"""Learning Episode aggregate root — fundamental educational unit.

Architecture Source
    LEARNING_EPISODE_ARCHITECTURE.md / LEARNING_EPISODE_INVARIANTS.md /
    EDUCATIONAL_ATOMICITY.md / LEARNING_EPISODE_LIFECYCLE.md
Concept
    Learning Episode
"""

from __future__ import annotations

from domain.education.foundation.enums import LearningDimension
from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.foundation.ids import (
    EvidenceId,
    LearningEpisodeId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.learning_episode.entities.episode_goal import EpisodeGoal
from domain.education.learning_episode.entities.episode_outcome import EpisodeOutcome
from domain.education.learning_episode.entities.episode_reflection import (
    EpisodeReflection,
)
from domain.education.learning_episode.entities.episode_step import EpisodeStep
from domain.education.learning_episode.enums import EpisodeStatus
from domain.education.learning_episode.events.episode_completed import EpisodeCompleted
from domain.education.learning_episode.events.episode_started import EpisodeStarted
from domain.education.learning_episode.events.reflection_recorded import (
    ReflectionRecorded,
)
from domain.education.learning_episode.policies.atomicity_policy import AtomicityPolicy
from domain.education.learning_episode.policies.episode_validation_policy import (
    EpisodeValidationPolicy,
)
from domain.education.learning_episode.policies.sequencing_policy import (
    SequencingPolicy,
)
from domain.education.learning_episode.value_objects.episode_duration import (
    EpisodeDuration,
)
from domain.education.learning_episode.value_objects.episode_progress import (
    EpisodeProgress,
)
from domain.education.learning_episode.value_objects.episode_sequence import (
    EpisodeSequence,
    EpisodeStepId,
)

DomainEvent = EpisodeStarted | EpisodeCompleted | ReflectionRecorded


class LearningEpisode:
    """Aggregate root for a bounded educational engagement with one purpose.

    Owns the teaching goal, strategy reference, learning objective and concept
    references, episode steps, reflection, outcome, and evidence references.
    Behaviour is exposed only through methods — no public setters.

    Invariants are enforced from LEARNING_EPISODE_INVARIANTS.md and
    EDUCATIONAL_ATOMICITY.md (exactly one purpose, sequence integrity,
    reflection before completion, no mastery theatre).
    """

    def __init__(
        self,
        episode_id: LearningEpisodeId,
        student_id: str,
        teaching_goal: EpisodeGoal,
        teaching_strategy_id: TeachingStrategyId,
        learning_objectives: list[LearningObjectiveReference]
        | tuple[LearningObjectiveReference, ...],
        steps: list[EpisodeStep] | tuple[EpisodeStep, ...],
        *,
        concept_references: list[ConceptReference]
        | tuple[ConceptReference, ...]
        | None = None,
        primary_dimension: LearningDimension | None = None,
        duration: EpisodeDuration | None = None,
        selection_rationale: str | None = None,
        status: EpisodeStatus = EpisodeStatus.PLANNED,
        reflection: EpisodeReflection | None = None,
        outcome: EpisodeOutcome | None = None,
        evidence_ids: list[EvidenceId] | tuple[EvidenceId, ...] | None = None,
        _record_created: bool = False,
    ) -> None:
        self._episode_id = EpisodeValidationPolicy.assert_identity(episode_id)
        self._student_id = EpisodeValidationPolicy.assert_student_id(student_id)
        self._teaching_goal = AtomicityPolicy.assert_atomic_goal(
            EpisodeValidationPolicy.assert_teaching_goal(teaching_goal)
        )
        self._teaching_strategy_id = EpisodeValidationPolicy.assert_teaching_strategy(
            teaching_strategy_id
        )
        self._learning_objectives = list(
            EpisodeValidationPolicy.assert_learning_objectives(learning_objectives)
        )
        self._concept_references = list(
            EpisodeValidationPolicy.assert_concept_references(
                concept_references or ()
            )
        )
        dimension = primary_dimension or teaching_goal.primary_dimension
        self._primary_dimension = EpisodeValidationPolicy.assert_primary_dimension(
            dimension
        )
        if self._primary_dimension is not teaching_goal.primary_dimension:
            raise EducationalInvariantViolation(
                "episode primary_dimension must match teaching goal dimension",
                invariant="LearningEpisode.primary_dimension.aligned",
            )
        self._steps = list(EpisodeValidationPolicy.assert_steps(steps))
        if duration is not None and not isinstance(duration, EpisodeDuration):
            raise EducationalInvariantViolation(
                "duration must be an EpisodeDuration when provided",
                invariant="LearningEpisode.duration.type",
            )
        self._duration = duration
        self._selection_rationale = EpisodeValidationPolicy.assert_selection_rationale(
            selection_rationale
        )
        if not isinstance(status, EpisodeStatus):
            raise EducationalInvariantViolation(
                "status must be an EpisodeStatus",
                invariant="LearningEpisode.status.type",
            )
        self._status = status
        self._reflection = reflection
        self._outcome = outcome
        self._evidence_ids: list[EvidenceId] = []
        for evidence_id in evidence_ids or ():
            EpisodeValidationPolicy.assert_evidence_not_duplicate(
                self._evidence_ids, evidence_id
            )
            self._evidence_ids.append(evidence_id)
        self._pending_events: list[DomainEvent] = []
        # _record_created reserved for future create-time events; start() emits.
        _ = _record_created

    @classmethod
    def create(
        cls,
        episode_id: LearningEpisodeId,
        student_id: str,
        teaching_goal: EpisodeGoal,
        teaching_strategy_id: TeachingStrategyId,
        learning_objectives: list[LearningObjectiveReference]
        | tuple[LearningObjectiveReference, ...],
        steps: list[EpisodeStep] | tuple[EpisodeStep, ...],
        *,
        concept_references: list[ConceptReference]
        | tuple[ConceptReference, ...]
        | None = None,
        duration: EpisodeDuration | None = None,
        selection_rationale: str | None = None,
    ) -> LearningEpisode:
        """Factory: create a PLANNED Learning Episode with one teaching goal."""
        return cls(
            episode_id=episode_id,
            student_id=student_id,
            teaching_goal=teaching_goal,
            teaching_strategy_id=teaching_strategy_id,
            learning_objectives=learning_objectives,
            steps=steps,
            concept_references=concept_references,
            primary_dimension=teaching_goal.primary_dimension,
            duration=duration,
            selection_rationale=selection_rationale,
            status=EpisodeStatus.PLANNED,
            _record_created=True,
        )

    # --- identity / read models (no setters) ---

    @property
    def episode_id(self) -> LearningEpisodeId:
        return self._episode_id

    @property
    def student_id(self) -> str:
        return self._student_id

    @property
    def teaching_goal(self) -> EpisodeGoal:
        return self._teaching_goal

    @property
    def teaching_strategy_id(self) -> TeachingStrategyId:
        return self._teaching_strategy_id

    @property
    def learning_objectives(self) -> tuple[LearningObjectiveReference, ...]:
        return tuple(self._learning_objectives)

    @property
    def concept_references(self) -> tuple[ConceptReference, ...]:
        return tuple(self._concept_references)

    @property
    def primary_dimension(self) -> LearningDimension:
        return self._primary_dimension

    @property
    def steps(self) -> tuple[EpisodeStep, ...]:
        return tuple(self._steps)

    @property
    def duration(self) -> EpisodeDuration | None:
        return self._duration

    @property
    def selection_rationale(self) -> str | None:
        return self._selection_rationale

    @property
    def status(self) -> EpisodeStatus:
        return self._status

    @property
    def reflection(self) -> EpisodeReflection | None:
        return self._reflection

    @property
    def outcome(self) -> EpisodeOutcome | None:
        return self._outcome

    @property
    def evidence_ids(self) -> tuple[EvidenceId, ...]:
        return tuple(self._evidence_ids)

    @property
    def sequence(self) -> EpisodeSequence:
        return SequencingPolicy.build_sequence(self._steps)

    @property
    def progress(self) -> EpisodeProgress:
        return SequencingPolicy.progress_of(self._steps)

    def pull_events(self) -> list[DomainEvent]:
        """Return and clear pending domain events."""
        events = list(self._pending_events)
        self._pending_events.clear()
        return events

    # --- behaviour ---

    def start(self) -> None:
        """Begin the episode: PLANNED → IN_PROGRESS; activate first step."""
        EpisodeValidationPolicy.assert_can_start(self._status)
        self._steps = SequencingPolicy.activate_first_pending(self._steps)
        self._status = EpisodeStatus.IN_PROGRESS
        first_active = next(step for step in self._steps if step.is_active())
        self._pending_events.append(
            EpisodeStarted(
                episode_id=self._episode_id,
                teaching_goal_id=self._teaching_goal.goal_id,
                first_step_id=first_active.step_id,
            )
        )

    def advance_step(self) -> EpisodeStep:
        """Complete the active step and activate the next pending step.

        Returns the step that was completed. Raises when required sequence
        would be skipped or no step remains.
        """
        EpisodeValidationPolicy.assert_in_progress(
            self._status, action="advance_step"
        )
        current = SequencingPolicy.assert_can_advance(self._steps)
        if current.is_pending():
            activated = current.activate()
            self._steps = SequencingPolicy.replace_step(self._steps, activated)
            current = activated
        completed = current.complete()
        self._steps = SequencingPolicy.replace_step(self._steps, completed)

        # Activate next pending step if any remain.
        try:
            nxt = SequencingPolicy.assert_can_advance(self._steps)
        except EducationalInvariantViolation as exc:
            if exc.invariant == "SequencingPolicy.exhausted":
                return completed
            raise
        if nxt.is_pending():
            self._steps = SequencingPolicy.replace_step(self._steps, nxt.activate())
        return completed

    def record_reflection(self, reflection: EpisodeReflection) -> None:
        """Attach structured reflection (Invariant E6). One reflection only."""
        EpisodeValidationPolicy.assert_in_progress(
            self._status, action="record_reflection"
        )
        if self._reflection is not None:
            raise EducationalInvariantViolation(
                "episode reflection is already recorded",
                invariant="LearningEpisode.reflection.already_recorded",
            )
        self._reflection = EpisodeValidationPolicy.assert_reflection(reflection)
        self._pending_events.append(
            ReflectionRecorded(
                episode_id=self._episode_id,
                reflection_id=reflection.reflection_id,
                reflection_type=reflection.reflection_type,
            )
        )

    def attach_evidence(self, evidence_id: EvidenceId) -> None:
        """Attach evidence attributable to this episode's purpose (E3, E14)."""
        EpisodeValidationPolicy.assert_in_progress(
            self._status, action="attach_evidence"
        )
        EpisodeValidationPolicy.assert_evidence_not_duplicate(
            self._evidence_ids, evidence_id
        )
        self._evidence_ids.append(evidence_id)

    def complete(self, outcome: EpisodeOutcome) -> None:
        """Close the episode successfully under completion criteria."""
        EpisodeValidationPolicy.assert_can_complete(
            self._status,
            required_steps_complete=SequencingPolicy.required_steps_complete(
                self._steps
            ),
            has_reflection=self._reflection is not None,
            has_evidence=bool(self._evidence_ids),
        )
        validated = EpisodeValidationPolicy.assert_completion_outcome(outcome)
        self._outcome = validated
        self._status = EpisodeStatus.COMPLETED
        self._pending_events.append(
            EpisodeCompleted(
                episode_id=self._episode_id,
                outcome_id=validated.outcome_id,
                outcome_kind=validated.kind,
            )
        )

    def interrupt(self, outcome: EpisodeOutcome) -> None:
        """Abort the episode while preserving educational truth (E16)."""
        EpisodeValidationPolicy.assert_not_terminal(
            self._status, action="interrupt"
        )
        if self._status is EpisodeStatus.COMPLETED:
            raise EducationalInvariantViolation(
                "cannot interrupt a completed episode",
                invariant="LearningEpisode.interrupt.completed",
            )
        validated = EpisodeValidationPolicy.assert_interrupt_outcome(outcome)
        self._outcome = validated
        self._status = EpisodeStatus.INTERRUPTED

    def replace_teaching_goal(self, goal: EpisodeGoal) -> None:
        """Replace teaching goal only while PLANNED (immutable after start)."""
        EpisodeValidationPolicy.assert_not_started_for_goal_change(self._status)
        self._teaching_goal = AtomicityPolicy.assert_atomic_goal(
            EpisodeValidationPolicy.assert_teaching_goal(goal)
        )
        self._primary_dimension = self._teaching_goal.primary_dimension

    # --- queries ---

    def has_learning_objective(self, objective_id_value: str) -> bool:
        return any(
            obj.objective_id.value == objective_id_value
            for obj in self._learning_objectives
        )

    def has_concept(self, concept_id_value: str) -> bool:
        return any(
            ref.concept_id.value == concept_id_value
            for ref in self._concept_references
        )

    def has_evidence(self, evidence_id: EvidenceId) -> bool:
        return evidence_id in self._evidence_ids

    def step_by_id(self, step_id: EpisodeStepId) -> EpisodeStep:
        return SequencingPolicy.assert_step_belongs(self._steps, step_id)

    def is_planned(self) -> bool:
        return self._status is EpisodeStatus.PLANNED

    def is_in_progress(self) -> bool:
        return self._status is EpisodeStatus.IN_PROGRESS

    def is_completed(self) -> bool:
        return self._status is EpisodeStatus.COMPLETED

    def is_interrupted(self) -> bool:
        return self._status is EpisodeStatus.INTERRUPTED

    def is_terminal(self) -> bool:
        return self._status in {
            EpisodeStatus.COMPLETED,
            EpisodeStatus.INTERRUPTED,
        }

    def educational_purpose(self) -> str:
        """The single deliberate educational purpose of this episode."""
        return self._teaching_goal.educational_purpose

    def __eq__(self, other: object) -> bool:
        if other is self:
            return True
        if not isinstance(other, LearningEpisode):
            return NotImplemented
        return self._episode_id == other._episode_id

    def __hash__(self) -> int:
        return hash((type(self), self._episode_id))

    def __repr__(self) -> str:
        return (
            f"LearningEpisode(episode_id={self._episode_id!r}, "
            f"status={self._status!r})"
        )

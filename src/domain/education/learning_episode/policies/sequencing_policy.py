"""Policy enforcing required step sequencing within a Learning Episode.

Architecture Source
    LEARNING_EPISODE_LIFECYCLE.md / LEARNING_EPISODE_SEQUENCE.md
Concept
    Sequencing Policy
"""

from __future__ import annotations

from domain.education.foundation.errors import EducationalInvariantViolation
from domain.education.learning_episode.entities.episode_step import EpisodeStep
from domain.education.learning_episode.enums import EpisodeStepStatus
from domain.education.learning_episode.value_objects.episode_progress import (
    EpisodeProgress,
)
from domain.education.learning_episode.value_objects.episode_sequence import (
    EpisodeSequence,
    EpisodeStepId,
)


class SequencingPolicy:
    """Enforces ordered advancement through episode steps."""

    @staticmethod
    def build_sequence(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
    ) -> EpisodeSequence:
        ordered = tuple(sorted(steps, key=lambda s: s.sequence_index))
        return EpisodeSequence(
            step_ids=tuple(step.step_id for step in ordered),
            required_step_ids=tuple(
                step.step_id for step in ordered if step.required
            ),
        )

    @staticmethod
    def progress_of(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
    ) -> EpisodeProgress:
        ordered = tuple(sorted(steps, key=lambda s: s.sequence_index))
        completed = sum(1 for step in ordered if step.is_completed())
        required = [step for step in ordered if step.required]
        completed_required = sum(1 for step in required if step.is_completed())
        active = next((step for step in ordered if step.is_active()), None)
        if active is not None:
            current_index = active.sequence_index
        elif completed == len(ordered):
            current_index = len(ordered)
        else:
            pending = next((step for step in ordered if step.is_pending()), None)
            current_index = pending.sequence_index if pending else 0
        return EpisodeProgress(
            current_index=current_index,
            completed_steps=completed,
            total_steps=len(ordered),
            completed_required_steps=completed_required,
            total_required_steps=len(required),
        )

    @staticmethod
    def required_steps_complete(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
    ) -> bool:
        return SequencingPolicy.progress_of(steps).required_sequence_complete

    @staticmethod
    def assert_can_advance(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
    ) -> EpisodeStep:
        """Return the step that must be advanced next; forbid skipping."""
        ordered = tuple(sorted(steps, key=lambda s: s.sequence_index))
        active = [step for step in ordered if step.is_active()]
        if len(active) > 1:
            raise EducationalInvariantViolation(
                "at most one episode step may be active",
                invariant="SequencingPolicy.single_active",
            )
        if active:
            return active[0]

        for index, step in enumerate(ordered):
            if step.is_completed():
                continue
            # Prior required steps must already be complete.
            for prior in ordered[:index]:
                if prior.required and not prior.is_completed():
                    raise EducationalInvariantViolation(
                        "cannot skip a required episode step in sequence",
                        invariant="SequencingPolicy.no_skip_required",
                    )
            if step.is_pending():
                return step
            raise EducationalInvariantViolation(
                "episode step is not advanceable",
                invariant="SequencingPolicy.not_advanceable",
            )

        raise EducationalInvariantViolation(
            "no remaining episode step to advance",
            invariant="SequencingPolicy.exhausted",
        )

    @staticmethod
    def assert_step_belongs(
        steps: tuple[EpisodeStep, ...] | list[EpisodeStep],
        step_id: EpisodeStepId,
    ) -> EpisodeStep:
        for step in steps:
            if step.step_id == step_id:
                return step
        raise EducationalInvariantViolation(
            "episode step is not owned by this episode",
            invariant="SequencingPolicy.step.not_found",
        )

    @staticmethod
    def replace_step(
        steps: list[EpisodeStep],
        updated: EpisodeStep,
    ) -> list[EpisodeStep]:
        """Return a new step list with ``updated`` substituted by identity."""
        found = False
        result: list[EpisodeStep] = []
        for step in steps:
            if step.step_id == updated.step_id:
                result.append(updated)
                found = True
            else:
                result.append(step)
        if not found:
            raise EducationalInvariantViolation(
                "cannot replace unknown episode step",
                invariant="SequencingPolicy.replace.not_found",
            )
        return result

    @staticmethod
    def activate_first_pending(
        steps: list[EpisodeStep],
    ) -> list[EpisodeStep]:
        """Activate the first pending step when starting an episode."""
        ordered = sorted(steps, key=lambda s: s.sequence_index)
        for step in ordered:
            if step.status is EpisodeStepStatus.PENDING:
                return SequencingPolicy.replace_step(steps, step.activate())
        raise EducationalInvariantViolation(
            "no pending step available to activate on start",
            invariant="SequencingPolicy.start.no_pending",
        )

"""Shared factories for Learning Episode domain tests."""

from __future__ import annotations

import pytest

from domain.education.foundation.enums import (
    ConfidenceLevel,
    LearningDimension,
    ReflectionType,
)
from domain.education.foundation.ids import (
    ConceptId,
    EvidenceId,
    LearningEpisodeId,
    LearningObjectiveId,
    ReflectionId,
    TeachingStrategyId,
)
from domain.education.foundation.references import (
    ConceptReference,
    LearningObjectiveReference,
)
from domain.education.learning_episode import (
    DurationBand,
    EpisodeDuration,
    EpisodeGoal,
    EpisodeGoalId,
    EpisodeOutcome,
    EpisodeOutcomeId,
    EpisodeOutcomeKind,
    EpisodeReflection,
    EpisodeStep,
    EpisodeStepId,
    EpisodeStepKind,
    LearningEpisode,
)


@pytest.fixture
def episode_id() -> LearningEpisodeId:
    return LearningEpisodeId("episode-001")


@pytest.fixture
def student_id() -> str:
    return "student-ada"


@pytest.fixture
def strategy_id() -> TeachingStrategyId:
    return TeachingStrategyId("strategy-worked-example-fading")


def make_goal(
    *,
    goal_id: str = "goal-001",
    statement: str = "Repair select-vs-ultimate mortality confusion",
    purpose: str = "Replace select-vs-ultimate confusion with correct discrimination",
    dimension: LearningDimension = LearningDimension.UNDERSTANDING,
) -> EpisodeGoal:
    return EpisodeGoal(
        goal_id=EpisodeGoalId(goal_id),
        statement=statement,
        educational_purpose=purpose,
        primary_dimension=dimension,
    )


def make_step(
    *,
    step_id: str = "step-001",
    kind: EpisodeStepKind | None = None,
    index: int = 0,
    label: str = "Explanation",
    required: bool = True,
) -> EpisodeStep:
    return EpisodeStep(
        step_id=EpisodeStepId(step_id),
        kind=kind or EpisodeStepKind.explanation(),
        sequence_index=index,
        label=label,
        required=required,
    )


def make_steps(
    kinds: list[EpisodeStepKind] | None = None,
    *,
    all_required: bool = True,
) -> list[EpisodeStep]:
    kinds = kinds or [
        EpisodeStepKind.explanation(),
        EpisodeStepKind.worked_example(),
        EpisodeStepKind.guided_practice(),
    ]
    steps: list[EpisodeStep] = []
    for index, kind in enumerate(kinds):
        required = all_required
        if not all_required and index == len(kinds) - 1:
            required = False
        steps.append(
            make_step(
                step_id=f"step-{index + 1:03d}",
                kind=kind,
                index=index,
                label=kind.value.replace("_", " ").title(),
                required=required if index < len(kinds) - 1 or all_required else False,
            )
        )
    # Ensure at least one required when trailing step was marked optional.
    if not all_required and not any(s.required for s in steps):
        steps[0] = make_step(
            step_id="step-001",
            kind=kinds[0],
            index=0,
            label=kinds[0].value,
            required=True,
        )
    return steps


def make_objective_ref(
    *,
    objective_id: str = "lo-select-ultimate",
    label: str = "Interpret select mortality tables",
) -> LearningObjectiveReference:
    return LearningObjectiveReference(
        objective_id=LearningObjectiveId(objective_id),
        label=label,
    )


def make_concept_ref(
    *,
    concept_id: str = "concept-select-mortality",
    label: str = "Select mortality",
) -> ConceptReference:
    return ConceptReference(
        concept_id=ConceptId(concept_id),
        label=label,
    )


def make_reflection(
    *,
    reflection_id: str = "refl-001",
    content: str = "I still confuse select and ultimate ages under pressure",
) -> EpisodeReflection:
    return EpisodeReflection(
        reflection_id=ReflectionId(reflection_id),
        reflection_type=ReflectionType.POST_EPISODE,
        content=content,
        perceived_difficulty=ConfidenceLevel.HIGH,
        perceived_understanding=ConfidenceLevel.MEDIUM,
    )


def make_outcome(
    *,
    outcome_id: str = "out-001",
    kind: EpisodeOutcomeKind = EpisodeOutcomeKind.GOAL_ACHIEVED,
    summary: str = "Student correctly discriminated select vs ultimate on probes",
) -> EpisodeOutcome:
    return EpisodeOutcome(
        outcome_id=EpisodeOutcomeId(outcome_id),
        kind=kind,
        summary=summary,
    )


def make_episode(
    *,
    episode_id: str = "episode-001",
    student_id: str = "student-ada",
    goal: EpisodeGoal | None = None,
    steps: list[EpisodeStep] | None = None,
    objectives: list[LearningObjectiveReference] | None = None,
    concepts: list[ConceptReference] | None = None,
    duration: EpisodeDuration | None = None,
    rationale: str | None = "Diagnosed select-vs-ultimate misconception",
) -> LearningEpisode:
    return LearningEpisode.create(
        episode_id=LearningEpisodeId(episode_id),
        student_id=student_id,
        teaching_goal=goal or make_goal(),
        teaching_strategy_id=TeachingStrategyId("strategy-contrast"),
        learning_objectives=objectives or [make_objective_ref()],
        steps=steps or make_steps(),
        concept_references=concepts or [make_concept_ref()],
        duration=duration
        or EpisodeDuration(planned_minutes=25, band=DurationBand.MEDIUM),
        selection_rationale=rationale,
    )


def start_and_finish_required_steps(episode: LearningEpisode) -> None:
    """Drive an episode through all required steps (leaves optional pending)."""
    episode.start()
    # Advance until required steps are complete.
    safety = 0
    while not episode.progress.required_sequence_complete:
        episode.advance_step()
        safety += 1
        if safety > 50:
            raise RuntimeError("step advancement loop exceeded safety bound")


def complete_happy_path(episode: LearningEpisode | None = None) -> LearningEpisode:
    """Create (if needed), run through steps, evidence, reflection, complete."""
    ep = episode or make_episode()
    start_and_finish_required_steps(ep)
    # Finish any remaining optional steps still active/pending if required done
    # but active optional remains — advance until exhausted or required done.
    safety = 0
    while True:
        try:
            ep.advance_step()
        except Exception:
            break
        safety += 1
        if safety > 50:
            break
    if not ep.has_evidence(EvidenceId("ev-001")):
        ep.attach_evidence(EvidenceId("ev-001"))
    if ep.reflection is None:
        ep.record_reflection(make_reflection())
    if not ep.is_completed():
        ep.complete(make_outcome())
    return ep

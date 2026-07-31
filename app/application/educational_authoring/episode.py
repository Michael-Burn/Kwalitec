"""Learning Episode builder (KWP-015).

Transforms curriculum-grounded AuthoringContext into one Learning Episode.
Activities remain deterministic. No CMP paste. No fabricated content.
"""

from __future__ import annotations

from app.application.educational_authoring.dto import (
    ACTIVITY_TITLES,
    AuthoringContext,
    EpisodeActivity,
    EpisodeActivityKind,
    LearningEpisode,
)
from app.application.educational_authoring.duration import (
    estimate_duration_minutes,
    split_activity_minutes,
)
from app.application.educational_authoring.guidance import scrub
from app.application.educational_authoring.writing import (
    compose_connection,
    compose_educational_context,
    compose_learning_objective,
    compose_success_criteria,
    select_concept_focus,
)


def build_learning_episode(
    context: AuthoringContext,
    *,
    sequence: int = 1,
    episode_id: str = "",
) -> LearningEpisode:
    """Compose one Learning Episode from curriculum-aligned inputs."""
    topic = scrub(context.topic_title)
    concepts = select_concept_focus(
        topic_title=topic,
        concept_titles=context.concept_titles,
        prerequisite_titles=context.prerequisite_titles,
        foundation_titles=context.foundation_titles,
    )
    educational_context = compose_educational_context(
        topic_title=topic,
        prerequisite_titles=context.prerequisite_titles,
        foundation_titles=context.foundation_titles,
        successor_titles=context.successor_titles,
        recently_strengthened_titles=context.recently_strengthened_titles,
    )
    objective = compose_learning_objective(
        topic_title=topic,
        objective_text=context.objective_text,
        concept_titles=concepts,
    )
    success = compose_success_criteria(
        topic_title=topic,
        concept_titles=concepts,
        objective_text=context.objective_text,
    )
    connection = compose_connection(
        topic_title=topic,
        tomorrow_title=context.tomorrow_topic_title,
        successor_titles=context.successor_titles,
    )
    activities = _build_activities(
        topic=topic, concepts=concepts, weak=context.weak_topic
    )
    duration = estimate_duration_minutes(
        base_effort_minutes=context.estimated_effort_minutes,
        difficulty_band=context.difficulty_band,
        student_pace_factor=context.student_pace_factor,
        previous_evidence_minutes=context.previous_evidence_minutes,
        weak_topic=context.weak_topic,
        activity_count=len(activities),
    )
    minute_parts = split_activity_minutes(duration, activity_count=len(activities))
    timed = tuple(
        EpisodeActivity(
            kind=act.kind,
            title=act.title,
            prompt=act.prompt,
            sequence=act.sequence,
            estimated_minutes=minute_parts[i] if i < len(minute_parts) else 0,
        )
        for i, act in enumerate(activities)
    )

    eid = (episode_id or "").strip() or _episode_id(context, sequence)
    alignment = _alignment_codes(context)

    return LearningEpisode(
        episode_id=eid,
        educational_context=educational_context,
        learning_objective=objective,
        concept_focus=concepts,
        activities=timed,
        success_criteria=success,
        estimated_duration_minutes=duration,
        connection=connection,
        topic_id=(context.topic_id or "").strip(),
        topic_title=topic,
        sequence=sequence,
        alignment_codes=alignment,
    )


def _build_activities(
    *,
    topic: str,
    concepts: tuple[str, ...],
    weak: bool,
) -> tuple[EpisodeActivity, ...]:
    focus = concepts[0] if concepts else topic
    kinds: list[EpisodeActivityKind] = [
        EpisodeActivityKind.READ,
        EpisodeActivityKind.WORKED_EXAMPLE,
        EpisodeActivityKind.PRACTICE,
    ]
    if weak:
        kinds.insert(1, EpisodeActivityKind.REVISION)
    kinds.append(EpisodeActivityKind.CHECKPOINT)

    prompts = {
        EpisodeActivityKind.READ: (
            f"Read the core ideas for {topic}, paying particular "
            f"attention to {focus}."
        ),
        EpisodeActivityKind.WORKED_EXAMPLE: (
            f"Study a worked example that applies {focus} within {topic}."
        ),
        EpisodeActivityKind.PRACTICE: (
            f"Practice solving problems that use {focus} in the "
            f"context of {topic}."
        ),
        EpisodeActivityKind.REVISION: (
            f"Briefly revise prerequisite ideas that support {topic} "
            f"before continuing."
        ),
        EpisodeActivityKind.CHECKPOINT: (
            f"Check that you can explain {topic} and solve a standard "
            f"problem without notes."
        ),
        EpisodeActivityKind.REFLECTION: (
            f"Note what in {topic} is clearer and what still needs care."
        ),
    }

    activities: list[EpisodeActivity] = []
    for idx, kind in enumerate(kinds, start=1):
        activities.append(
            EpisodeActivity(
                kind=kind,
                title=ACTIVITY_TITLES[kind],
                prompt=scrub(prompts[kind]),
                sequence=idx,
            )
        )
    return tuple(activities)


def _episode_id(context: AuthoringContext, sequence: int) -> str:
    mid = (context.mission_instance_id or context.topic_id or "mission").strip()
    tid = (context.topic_id or context.topic_title or "topic").strip()
    safe_mid = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in mid)[:48]
    safe_tid = "".join(ch if ch.isalnum() or ch in "-_" else "-" for ch in tid)[:32]
    return f"ep-{safe_mid}-{safe_tid}-{sequence}"


def _alignment_codes(context: AuthoringContext) -> tuple[str, ...]:
    codes: list[str] = []
    if context.topic_id:
        codes.append(f"topic:{context.topic_id}")
    if context.topic_code:
        codes.append(f"code:{context.topic_code}")
    for oid in context.objective_ids[:4]:
        if oid:
            codes.append(f"objective:{oid}")
    for title in context.prerequisite_titles[:3]:
        if title:
            codes.append(f"prereq:{title}")
    for title in context.successor_titles[:2]:
        if title:
            codes.append(f"successor:{title}")
    if context.subject_code:
        codes.append(f"subject:{context.subject_code}")
    return tuple(codes)

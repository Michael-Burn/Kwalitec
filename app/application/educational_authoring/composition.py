"""Mission composition from Learning Episodes (KWP-015).

Morning Brief (workspace) → Learning Episode(s) → Checkpoint →
Reflection → Tomorrow Preview. Educational Authoring owns composition
language only.
"""

from __future__ import annotations

from app.application.educational_authoring.dto import (
    AuthoringContext,
    MissionComposition,
)
from app.application.educational_authoring.episode import build_learning_episode
from app.application.educational_authoring.extra_study import (
    build_extra_study_offers,
)
from app.application.educational_authoring.tomorrow import build_tomorrow_preview
from app.application.educational_authoring.writing import (
    compose_checkpoint_prompt,
    compose_mission_narrative,
    compose_reflection_prompt,
)


def compose_mission(context: AuthoringContext) -> MissionComposition:
    """Compose an authored mission arc from curriculum-aligned inputs."""
    topic = (context.topic_title or "").strip()
    if not topic and not (context.topic_id or "").strip():
        return MissionComposition(has_composition=False)

    primary = build_learning_episode(context, sequence=1)
    episodes = (primary,)

    # Optional second episode when weak foundations warrant revision first.
    if context.weak_topic and context.prerequisite_titles:
        revision_context = AuthoringContext(
            topic_id=context.topic_id,
            topic_title=context.prerequisite_titles[0],
            topic_code="",
            concept_titles=(context.prerequisite_titles[0],),
            prerequisite_titles=(),
            successor_titles=(topic,),
            foundation_titles=(),
            estimated_effort_minutes=max(
                15, int(context.estimated_effort_minutes or 45) // 3
            ),
            difficulty_band=context.difficulty_band,
            student_pace_factor=context.student_pace_factor,
            weak_topic=True,
            mission_instance_id=context.mission_instance_id,
            subject_code=context.subject_code,
            tomorrow_topic_title=topic,
        )
        foundation_episode = build_learning_episode(
            revision_context,
            sequence=1,
            episode_id=f"{primary.episode_id}-foundation",
        )
        primary_renumbered = build_learning_episode(context, sequence=2)
        episodes = (foundation_episode, primary_renumbered)

    total = sum(ep.estimated_duration_minutes for ep in episodes)
    tomorrow = build_tomorrow_preview(context)
    extra = build_extra_study_offers(context, mission_minutes=total)
    narrative = compose_mission_narrative(
        topic_title=topic,
        educational_context=episodes[-1].educational_context,
    )
    alignment: list[str] = []
    for ep in episodes:
        alignment.extend(ep.alignment_codes)

    return MissionComposition(
        episodes=episodes,
        checkpoint_prompt=compose_checkpoint_prompt(topic_title=topic),
        reflection_prompt=compose_reflection_prompt(topic_title=topic),
        tomorrow_preview=tomorrow if tomorrow.has_preview else None,
        extra_study=extra,
        mission_narrative=narrative,
        total_duration_minutes=total,
        alignment_codes=tuple(dict.fromkeys(alignment)),
        has_composition=True,
    )

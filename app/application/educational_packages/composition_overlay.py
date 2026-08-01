"""Overlay certified educational package language onto Mission composition (EA-006)."""

from __future__ import annotations

from app.application.educational_authoring.dto import (
    AuthoringContext,
    EpisodeActivity,
    EpisodeActivityKind,
    LearningEpisode,
    MissionComposition,
    TomorrowPreview,
)
from app.application.educational_authoring.duration import split_activity_minutes
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_educational_package,
)
from app.application.educational_packages.models import CertifiedEducationalPackage
from app.application.educational_packages.selection import packages_for_subject
from app.application.educational_packages.tomorrow_chrome import (
    resolve_package_for_tomorrow_chrome,
)


def resolve_package_for_context(
    context: AuthoringContext,
) -> CertifiedEducationalPackage | None:
    """Find a publication-approved package for an authoring context.

    RO1-R1: prefer educational_package_id and campaign chain selection over
    shared topic_code first-match so Tomorrow Preview chrome matches the
    approved package for the sitting. Never overlay via title keywords alone.
    """
    pack = resolve_package_for_tomorrow_chrome(
        educational_package_id=context.educational_package_id,
        subject_id=context.subject_code,
        syllabus_topic_code=context.topic_code,
        topic_title=context.topic_title,
        completed_package_ids=context.completed_package_ids,
        last_completed_package_id=context.last_completed_package_id,
        prefer_completed_package=context.prefer_completed_package,
    )
    if pack is not None:
        return pack
    # Exact identity / unique code only — no title-keyword overlay for
    # synthetic authoring topics (KWP-015) or ambiguous shared codes.
    code = (context.topic_code or "").strip()
    tid = (context.topic_id or "").strip()
    if not code and not tid:
        return None
    if code:
        subject = (context.subject_code or "").strip()
        if subject:
            matches = [p for p in packages_for_subject(subject) if p.topic_code == code]
        else:
            matches = [
                p
                for p in EducationalPackageLoader().all_approved()
                if p.topic_code == code
            ]
        if len(matches) == 1:
            return matches[0]
        return None
    return find_educational_package(
        topic_id=tid,
        topic_code="",
        topic_title="",
        subject_id=context.subject_code,
    )


def compose_from_package(
    pack: CertifiedEducationalPackage,
    context: AuthoringContext,
) -> MissionComposition:
    """Compose Home / briefing language from a certified package (joint bundle)."""
    duration = pack.estimated_duration_minutes
    if context.estimated_effort_minutes > 0:
        duration = context.estimated_effort_minutes
    activities = _episode_activities(pack)
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
    concepts = tuple(
        part.strip()
        for part in pack.concept_focus.replace("→", "|").split("|")
        if part.strip()
    ) or (pack.concept_focus,)
    episode = LearningEpisode(
        episode_id=f"lep-pkg-{pack.topic_code or 'topic'}",
        educational_context=pack.mission_narrative,
        learning_objective=pack.learning_objective,
        concept_focus=concepts,
        activities=timed,
        success_criteria=pack.success_criteria,
        estimated_duration_minutes=duration,
        connection=pack.tomorrow.continuity_line,
        topic_id=context.topic_id or pack.topic_code,
        topic_title=pack.display_title or pack.topic_title,
        sequence=1,
        alignment_codes=(
            f"pkg:{pack.package_id}",
            f"topic:{pack.topic_code}",
            "ea006",
        ),
    )
    tomorrow = TomorrowPreview(
        topic_title=pack.tomorrow.next_topic_title,
        topic_id="",
        topic_code=pack.tomorrow.next_topic_code,
        continuity_line=pack.tomorrow.continuity_line,
        estimated_duration_minutes=duration,
        start_early_available=True,
        start_early_label="Start Early",
        start_early_detail=pack.tomorrow.light_prep_cue
        or "Optional light prep only — titles, not deep study tonight.",
        has_preview=bool(pack.tomorrow.next_topic_title),
    )
    checkpoint = ""
    if pack.knowledge_checks:
        checkpoint = pack.knowledge_checks[-1].prompt
    reflection = pack.reflection_prompt or pack.reflection_framing
    return MissionComposition(
        episodes=(episode,),
        checkpoint_prompt=checkpoint,
        reflection_prompt=reflection,
        tomorrow_preview=tomorrow if tomorrow.has_preview else None,
        extra_study=(),
        mission_narrative=pack.student_brief or pack.mission_narrative,
        total_duration_minutes=duration,
        alignment_codes=episode.alignment_codes,
        has_composition=True,
    )


def _episode_activities(
    pack: CertifiedEducationalPackage,
) -> tuple[EpisodeActivity, ...]:
    return (
        EpisodeActivity(
            kind=EpisodeActivityKind.READ,
            title="Guided Reading",
            prompt=pack.reading.lead_line or pack.reading.exit_line,
            sequence=1,
        ),
        EpisodeActivity(
            kind=EpisodeActivityKind.PRACTICE,
            title="Knowledge Checks",
            prompt=(
                pack.knowledge_checks[0].prompt
                if pack.knowledge_checks
                else "Retrieve today's Mission success criteria closed-book."
            ),
            sequence=2,
        ),
        EpisodeActivity(
            kind=EpisodeActivityKind.REFLECTION,
            title="Reflection",
            prompt=pack.reflection_prompt or pack.reflection_framing,
            sequence=3,
        ),
    )


def display_title_for_topic(
    *,
    topic_id: str = "",
    topic_code: str = "",
    topic_title: str = "",
    subject_id: str = "",
) -> str | None:
    """Return certified display_title when a published package matches."""
    pack = find_educational_package(
        topic_id=topic_id,
        topic_code=topic_code,
        topic_title=topic_title,
        subject_id=subject_id,
    )
    if pack is None:
        return None
    return pack.display_title or None


def why_now_for_topic(
    *,
    topic_id: str = "",
    topic_code: str = "",
    topic_title: str = "",
    subject_id: str = "",
) -> str | None:
    """Return certified why_now when a published package matches."""
    pack = find_educational_package(
        topic_id=topic_id,
        topic_code=topic_code,
        topic_title=topic_title,
        subject_id=subject_id,
    )
    if pack is None:
        return None
    return pack.why_now or pack.explainability or None

"""Presentation view models for Runtime C educational experience (PX-001)."""

from __future__ import annotations

from datetime import date

from app.application.educational_experience.dto import (
    EducationalExperienceSnapshot,
)
from app.presentation.student.navigation import build_navigation
from app.presentation.student.view_models import (
    CountdownCardViewModel,
    EducationalExperienceViewModel,
    ExplanationViewModel,
    HomePageViewModel,
    JourneyPageViewModel,
    JourneyTopicViewModel,
    RecommendationCardViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
)


def educational_vm(
    snap: EducationalExperienceSnapshot | None,
) -> EducationalExperienceViewModel | None:
    if snap is None or not snap.is_runtime_c:
        return None
    pos = snap.curriculum_position
    mission = snap.mission
    journey = snap.journey
    pacing = snap.pacing
    return EducationalExperienceViewModel(
        active=True,
        subject_code=snap.subject_code,
        examination_label=snap.examination_label,
        today_topic_title=pos.topic_title,
        today_topic_code=pos.topic_code,
        section_title=pos.section_title,
        position_label=pos.position_label,
        coverage_percent=pos.coverage_percent,
        coverage_label=f"{pos.coverage_percent}% of syllabus topics complete",
        mission_title=(mission.title if mission else pos.topic_title),
        mission_rationale=(
            (mission.educational_rationale if mission else "")
            or journey.why_today
        ),
        learning_objectives=(
            mission.learning_objectives if mission else ()
        ),
        estimated_duration_label=(
            mission.estimated_duration_label if mission else ""
        ),
        completion_definition=(
            mission.completion_definition if mission else ""
        ),
        prerequisite_status_label=(
            mission.prerequisite_status_label if mission else ""
        ),
        prerequisite_satisfied=(
            mission.prerequisite_satisfied if mission else True
        ),
        task_descriptions=(mission.task_descriptions if mission else ()),
        why_this_mission=(mission.why_this_mission if mission else ""),
        supporting_evidence=(
            mission.supporting_evidence if mission else ()
        ),
        confidence_label=(mission.confidence_label if mission else ""),
        expected_benefit=(mission.expected_benefit if mission else ""),
        suggested_next_action=(
            mission.suggested_next_action if mission else ""
        ),
        review_point=(mission.review_point if mission else ""),
        why_today=journey.why_today,
        why_previous_complete=journey.why_previous_complete,
        unlocks_next=journey.unlocks_next,
        journey_evidence=journey.supporting_evidence,
        progress_percent=pos.coverage_percent,
        progress_label=f"{pos.coverage_percent}% complete",
        pacing_summary=pacing.pacing_summary,
        feasibility_label=pacing.feasibility_label,
        exam_date_label=pacing.exam_date_label,
        syllabus_complete=snap.syllabus_complete,
    )


def page_from_educational_experience(
    snap: EducationalExperienceSnapshot,
    *,
    surface: str,
) -> StudentPageViewModel:
    """Assemble Home / Journey pages from Runtime C educational projection."""
    edu = educational_vm(snap)
    assert edu is not None

    nav = build_navigation(active_surface=surface)
    titles = {
        "home": "Home",
        "journey": "Journey",
        "revision": "Revision",
        "history": "History",
        "profile": "Settings",
    }
    descriptions = {
        "home": "What you should study today, and why.",
        "journey": "Where you are on the published syllabus path.",
        "revision": (
            "Revision that supports today's Mission — not a second Mission."
        ),
        "history": (
            "Practice archives and progress context — not Study Sensei’s "
            "learning story. Educational meaning lives in the Decision "
            "Journal and Educational Timeline."
        ),
        "profile": "Examination, preferences, goals, and account.",
    }
    shell = StudentShellViewModel(
        active_surface=surface,
        active_label=titles.get(surface, surface.title()),
        navigation=nav,
        page_title=titles.get(surface, surface.title()),
        page_eyebrow="Your learning",
        page_description=descriptions.get(surface, ""),
        learning_activity_status=(
            "mission_ready" if snap.mission else "planning"
        ),
        journey_stage=snap.curriculum_position.journey_stage.lower(),
        unified_journey_enabled=False,
    )

    home = None
    journey_page = None
    if surface == "home":
        home = _home_from_educational(snap, edu)
        journey_page = _journey_from_educational(snap, edu)
    elif surface == "journey":
        journey_page = _journey_from_educational(snap, edu)
    else:
        # Revision / history / profile still expose educational context strip.
        home = None
        journey_page = None

    return StudentPageViewModel(
        shell=shell,
        home=home,
        journey=journey_page,
        educational=edu,
    )


def _home_from_educational(
    snap: EducationalExperienceSnapshot,
    edu: EducationalExperienceViewModel,
) -> HomePageViewModel:
    mission = snap.mission
    title = edu.mission_title or edu.today_topic_title or "Today's Mission"
    why = edu.why_this_mission or edu.mission_rationale or edu.why_today
    duration = edu.estimated_duration_label
    mission_open = bool(
        mission
        and mission.mission_instance_id
        and (mission.status or "").lower() == "generated"
    )
    mission_done_today = bool(
        mission and (mission.status or "").lower() == "completed"
    )
    day_complete = bool(snap.syllabus_complete or mission_done_today)
    if snap.syllabus_complete:
        cta_label = "Syllabus complete"
        cta_enabled = False
        session_control = ""
    elif mission_open:
        cta_label = "Mark mission complete"
        cta_enabled = True
        session_control = "complete_runtime_c"
    elif mission_done_today:
        cta_label = "Today's mission complete"
        cta_enabled = False
        session_control = ""
    else:
        cta_label = "Review today's mission"
        cta_enabled = False
        session_control = ""

    explanation = ExplanationViewModel(
        summary=mission.judgement if mission else "",
        why_recommended=why,
        evidence_points=edu.supporting_evidence[:4],
        expected_benefit=edu.expected_benefit,
        confidence_label=edu.confidence_label,
        suggested_next_action=edu.suggested_next_action or edu.unlocks_next,
        review_point=edu.review_point,
        is_complete=bool(why and edu.supporting_evidence),
        has_content=bool(
            why or edu.expected_benefit or edu.suggested_next_action
        ),
        has_disclosure=bool(
            edu.supporting_evidence
            or edu.review_point
            or edu.confidence_label
        ),
        timeliness_line=edu.why_today,
        completion_loop_line=edu.review_point,
    )
    countdown_days = None
    if snap.pacing.exam_date is not None:
        countdown_days = (snap.pacing.exam_date - date.today()).days

    status_label = ""
    if snap.syllabus_complete:
        status_label = "Syllabus complete"
    elif mission_done_today:
        status_label = "Mission complete for today"
    elif mission_open:
        status_label = "Ready to study"

    return HomePageViewModel(
        greeting=snap.greeting,
        examination_label=edu.examination_label,
        countdown=CountdownCardViewModel(
            days=countdown_days,
            label=_countdown_label(countdown_days),
            examination_label=edu.examination_label,
            has_countdown=countdown_days is not None,
        ),
        recommendation=RecommendationCardViewModel(
            title=title,
            summary=why,
            benefit_label=edu.expected_benefit,
            time_label=duration,
            reason=why,
            cta_label=cta_label,
            cta_enabled=cta_enabled,
            has_recommendation=True,
        ),
        explanation=explanation,
        estimated_study_label=duration,
        expected_benefit_label=edu.expected_benefit,
        can_start_session=False,
        primary_cta_label=cta_label,
        primary_cta_enabled=cta_enabled,
        mission_id=(mission.mission_instance_id if mission else ""),
        journey_story=_journey_story(edu),
        coach_insight=why or edu.why_today,
        primary_mission_title=title,
        why_it_matters=why,
        estimated_duration_label=duration,
        expected_outcome=edu.expected_benefit,
        mission_summary=edu.completion_definition,
        completion_status="complete" if day_complete else "ready",
        completion_status_label=status_label,
        session_control=session_control,
        session_control_label=cta_label,
        day_complete=day_complete,
        l1_expected_benefit=edu.expected_benefit,
        educational=edu,
    )


def _journey_from_educational(
    snap: EducationalExperienceSnapshot,
    edu: EducationalExperienceViewModel,
) -> JourneyPageViewModel:
    journey = snap.journey
    current = None
    if snap.curriculum_position.topic_id:
        current = JourneyTopicViewModel(
            topic_id=snap.curriculum_position.topic_id,
            title=edu.today_topic_title,
            status_label="Current",
            prerequisite_note=edu.why_today,
        )
    completed = tuple(
        JourneyTopicViewModel(
            topic_id=tid,
            title=title,
            status_label="Completed",
        )
        for tid, title in journey.completed_topics
    )
    upcoming = tuple(
        JourneyTopicViewModel(
            topic_id=tid,
            title=title,
            status_label="Upcoming",
            prerequisite_note=edu.unlocks_next if i == 0 else "",
        )
        for i, (tid, title) in enumerate(journey.upcoming_topics)
    )
    return JourneyPageViewModel(
        examination_label=edu.examination_label,
        current=current,
        completed=completed,
        upcoming=upcoming,
        progress_percent=edu.progress_percent,
        progress_label=edu.progress_label,
        estimated_completion_label=edu.feasibility_label,
        prerequisite_notes=tuple(
            note
            for note in (
                edu.why_today,
                edu.why_previous_complete,
                edu.unlocks_next,
            )
            if note
        ),
        completed_count=len(completed),
        upcoming_count=len(upcoming),
        primary_cta_label="Return to today's mission",
        primary_cta_enabled=True,
        educational=edu,
    )


def _journey_story(edu: EducationalExperienceViewModel) -> str:
    parts: list[str] = []
    if edu.position_label:
        parts.append(edu.position_label + ".")
    if edu.today_topic_title:
        parts.append(f"Today's topic is {edu.today_topic_title}.")
    if edu.why_today:
        parts.append(edu.why_today)
    if parts:
        return " ".join(parts[:3])
    return "Your published syllabus journey will appear here."


def _countdown_label(days: int | None) -> str:
    if days is None:
        return ""
    if days < 0:
        return "Exam date passed"
    if days == 0:
        return "Exam is today"
    if days == 1:
        return "1 day until exam"
    return f"{days} days until exam"

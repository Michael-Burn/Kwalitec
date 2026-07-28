"""Presentation view models for Student Experience surfaces.

Formatting and labels only. Never compute readiness, recommendations,
missions, or journeys — those arrive from application snapshots.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from app.application.student_experience.dashboard_service import (
    DashboardSnapshot,
    NavigationItemSnapshot,
)
from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.history_snapshot import (
    AchievementSnapshot,
    CompletedSessionSnapshot,
    HistorySnapshot,
    ReadinessPointSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.application.student_experience.dto.journey_snapshot import (
    JourneySnapshot,
    JourneyTopicSnapshot,
)
from app.application.student_experience.dto.profile_snapshot import (
    AccountSettingsSnapshot,
    LearningGoalSnapshot,
    LearningStatisticsSnapshot,
    ProfileSnapshot,
    StudyPreferencesSnapshot,
)
from app.application.student_experience.dto.revision_snapshot import (
    RevisionOptionSnapshot,
    RevisionSnapshot,
)
from app.presentation.formatting import format_minutes as _format_minutes
from app.presentation.student.navigation import StudentNavItem, build_navigation

# Terms that must never appear in learner-facing copy.
FORBIDDEN_LEARNER_TERMS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "graph node",
    "graph edge",
)


@dataclass(frozen=True)
class ExplanationViewModel:
    summary: str = ""
    why_recommended: str = ""
    evidence_points: tuple[str, ...] = ()
    expected_benefit: str = ""
    confidence_label: str = ""
    suggested_next_action: str = ""
    review_point: str = ""
    confidence_basis: str = ""
    is_complete: bool = False
    has_content: bool = False
    has_disclosure: bool = False
    # EP-008.1 — Recommendation Trust.
    plan_coherence: str = ""
    plan_coherence_label: str = ""
    honest_refusal: bool = False
    timeliness_line: str = ""
    completion_loop_line: str = ""


@dataclass(frozen=True)
class RecommendationAlternativeViewModel:
    title: str = ""
    why_recommended: str = ""
    expected_benefit: str = ""
    suggested_next_action: str = ""


@dataclass(frozen=True)
class CoachTrustViewModel:
    """Structured Coach insight from the same authored Home fields."""

    why: str = ""
    why_now: str = ""
    next: str = ""
    benefit: str = ""
    is_refusal: bool = False
    has_content: bool = False


@dataclass(frozen=True)
class RecommendationCardViewModel:
    title: str = ""
    summary: str = ""
    benefit_label: str = ""
    time_label: str = ""
    reason: str = ""
    cta_label: str = "Start Today's Session"
    cta_enabled: bool = False
    has_recommendation: bool = False


@dataclass(frozen=True)
class ReadinessCardViewModel:
    readiness_label: str = ""
    readiness_percent_label: str = ""
    trend_label: str = ""
    confidence_label: str = ""
    confidence_basis: str = ""
    why_this_estimate: str = ""
    suggested_next_action: str = ""
    review_point: str = ""
    readiness_drivers: tuple[str, ...] = ()
    supporting_evidence: tuple[str, ...] = ()
    expected_benefit: str = ""
    has_readiness: bool = False
    has_disclosure: bool = False


@dataclass(frozen=True)
class CountdownCardViewModel:
    days: int | None = None
    label: str = ""
    examination_label: str = ""
    has_countdown: bool = False


@dataclass(frozen=True)
class JourneyTopicViewModel:
    topic_id: str = ""
    title: str = ""
    status_label: str = ""
    prerequisite_note: str = ""


@dataclass(frozen=True)
class JourneyCardViewModel:
    current_topic_title: str = ""
    progress_percent: int = 0
    progress_label: str = ""
    next_topic_title: str = ""
    estimated_completion_label: str = ""
    has_journey: bool = False


@dataclass(frozen=True)
class EducationalExperienceViewModel:
    """Student-visible Runtime C educational information (PX-001)."""

    active: bool = False
    subject_code: str = ""
    examination_label: str = ""
    today_topic_title: str = ""
    today_topic_code: str = ""
    section_title: str = ""
    position_label: str = ""
    coverage_percent: int = 0
    coverage_label: str = ""
    mission_title: str = ""
    mission_rationale: str = ""
    learning_objectives: tuple[str, ...] = ()
    estimated_duration_label: str = ""
    completion_definition: str = ""
    prerequisite_status_label: str = ""
    prerequisite_satisfied: bool = True
    task_descriptions: tuple[str, ...] = ()
    why_this_mission: str = ""
    supporting_evidence: tuple[str, ...] = ()
    confidence_label: str = ""
    expected_benefit: str = ""
    suggested_next_action: str = ""
    review_point: str = ""
    why_today: str = ""
    why_previous_complete: str = ""
    unlocks_next: str = ""
    journey_evidence: tuple[str, ...] = ()
    progress_percent: int = 0
    progress_label: str = ""
    pacing_summary: str = ""
    feasibility_label: str = ""
    exam_date_label: str = ""
    syllabus_complete: bool = False


@dataclass(frozen=True)
class JourneyPageViewModel:
    examination_label: str = ""
    current: JourneyTopicViewModel | None = None
    completed: tuple[JourneyTopicViewModel, ...] = ()
    upcoming: tuple[JourneyTopicViewModel, ...] = ()
    progress_percent: int = 0
    progress_label: str = ""
    estimated_completion_label: str = ""
    prerequisite_notes: tuple[str, ...] = ()
    completed_count: int = 0
    upcoming_count: int = 0
    primary_cta_label: str = "Continue Journey"
    primary_cta_enabled: bool = False
    # PX-001 — Runtime C educational enrichment (optional).
    educational: EducationalExperienceViewModel | None = None


@dataclass(frozen=True)
class RevisionOptionViewModel:
    option_id: str = ""
    topic_title: str = ""
    priority_label: str = ""
    time_label: str = ""
    expected_benefit: str = ""
    explanation: ExplanationViewModel | None = None
    is_primary: bool = False


@dataclass(frozen=True)
class RevisionPageViewModel:
    primary: RevisionOptionViewModel | None = None
    alternatives: tuple[RevisionOptionViewModel, ...] = ()
    empty_message: str = ""
    has_revision: bool = False
    option_count: int = 0
    primary_cta_label: str = "Begin Revision"
    primary_cta_enabled: bool = False


@dataclass(frozen=True)
class HistorySessionViewModel:
    session_id: str = ""
    topic_title: str = ""
    completed_at: str = ""
    duration_label: str = ""
    outcome_label: str = "Completed"


@dataclass(frozen=True)
class HistoryPageViewModel:
    sessions: tuple[HistorySessionViewModel, ...] = ()
    total_study_label: str = ""
    readiness_points: tuple[tuple[str, str], ...] = ()
    mastered_topics: tuple[str, ...] = ()
    revision_history: tuple[str, ...] = ()
    achievements: tuple[AchievementSnapshot, ...] = ()
    session_count: int = 0
    mastered_count: int = 0
    readiness_trend_label: str = ""
    primary_cta_label: str = "Return Home"
    primary_cta_enabled: bool = True
    # EP-008.3 educational narrative.
    recommendation_narrative: tuple[
        RecommendationNarrativeEntryViewModel, ...
    ] = ()
    recommendation_narrative_header: str = ""


@dataclass(frozen=True)
class ProfilePageViewModel:
    display_name: str = ""
    examination_label: str = ""
    preferences: StudyPreferencesSnapshot = field(
        default_factory=StudyPreferencesSnapshot
    )
    statistics: LearningStatisticsSnapshot = field(
        default_factory=LearningStatisticsSnapshot
    )
    goals: tuple[LearningGoalSnapshot, ...] = ()
    account: AccountSettingsSnapshot = field(
        default_factory=AccountSettingsSnapshot
    )
    preferences_days_label: str = ""
    readiness_percent_label: str = ""
    total_study_label: str = ""
    primary_cta_label: str = "Update Study Preferences"
    primary_cta_enabled: bool = True
    primary_cta_endpoint: str = "settings.preferences"


@dataclass(frozen=True)
class HomeMilestoneViewModel:
    title: str = ""
    detail: str = ""


@dataclass(frozen=True)
class HomeQuickActionViewModel:
    label: str = ""
    href: str = ""
    detail: str = ""


@dataclass(frozen=True)
class ExperienceTimelineStepViewModel:
    """One step on today's Experience timeline (presentation only)."""

    key: str = ""
    label: str = ""
    status: str = "pending"  # pending | current | complete


@dataclass(frozen=True)
class ReflectionPromptViewModel:
    """One Guided Reflection prompt (presentation only — never persisted)."""

    prompt: str = ""
    response_type: str = ""
    available_options: tuple[str, ...] = ()
    optional_note_placeholder: str = ""


@dataclass(frozen=True)
class ExperienceFeedbackFactViewModel:
    """Presentation projection of one factual Experience Feedback line."""

    key: str = ""
    label: str = ""
    value_label: str = ""
    source_description: str = ""


@dataclass(frozen=True)
class CommitmentReflectionViewModel:
    what_you_did: str = ""
    what_changed: str = ""
    why_it_mattered: str = ""
    what_was_learned: str = ""
    what_happens_next: str = ""


@dataclass(frozen=True)
class CommitmentViewModel:
    """EP-008.3 preference/intent commitment chrome."""

    state: str = "offered"
    recommendation_key: str = ""
    title: str = ""
    continuity_line: str = ""
    deferred_reason_label: str = ""
    show_commit_affordance: bool = False
    show_defer_affordance: bool = False
    is_committed: bool = False
    is_deferred: bool = False
    show_reflection: bool = False
    reflection: CommitmentReflectionViewModel | None = None
    coach_status_line: str = ""


@dataclass(frozen=True)
class RecommendationNarrativeEntryViewModel:
    kind: str = ""
    title: str = ""
    occurred_at: str = ""
    summary_line: str = ""
    reason_label: str = ""


@dataclass(frozen=True)
class HomePageViewModel:
    greeting: str = ""
    examination_label: str = ""
    countdown: CountdownCardViewModel = field(
        default_factory=CountdownCardViewModel
    )
    readiness: ReadinessCardViewModel = field(
        default_factory=ReadinessCardViewModel
    )
    recommendation: RecommendationCardViewModel = field(
        default_factory=RecommendationCardViewModel
    )
    explanation: ExplanationViewModel | None = None
    start_session: StartSessionActionSnapshot | None = None
    estimated_study_label: str = ""
    expected_benefit_label: str = ""
    can_start_session: bool = False
    primary_cta_label: str = "Start Today's Session"
    primary_cta_enabled: bool = False
    mission_id: str = ""
    session_id: str = ""
    # PX-003 decision-screen projections (presentation only).
    journey_story: str = (
        "Your learning story will appear here as you complete sessions."
    )
    coach_insight: str = (
        "Guidance will appear after your next study Session."
    )
    milestones: tuple[HomeMilestoneViewModel, ...] = ()
    quick_actions: tuple[HomeQuickActionViewModel, ...] = ()
    # P2-MS002–P2-MS005 Unified Student Journey — Home consumes
    # JourneyContext via DailyMission / DayExperience. Ignored when
    # ENABLE_UNIFIED_JOURNEY is off.
    unified_journey_enabled: bool = False
    journey_stage: str = ""
    primary_mission_title: str = ""
    why_it_matters: str = ""
    estimated_duration_label: str = ""
    expected_outcome: str = ""
    # P2-MS003 Daily Mission Experience
    mission_summary: str = ""
    mission_priority: str = ""
    completion_status: str = ""
    completion_status_label: str = ""
    timeline_steps: tuple[ExperienceTimelineStepViewModel, ...] = ()
    # P2-MS004 Guided Study Session (presentation only)
    guided_session_active: bool = False
    session_phase: str = ""
    session_status: str = ""
    session_learning_objective: str = ""
    session_next_step: str = ""
    session_elapsed_state: str = ""
    session_start_time_label: str = ""
    session_progress_summary: str = ""
    session_control_label: str = ""
    session_control: str = ""  # start | resume | finish | ""
    reflection_available: bool = False
    # P2-MS005 Guided Reflection (presentation only — never persisted)
    reflection_active: bool = False
    reflection_state: str = ""
    reflection_headline: str = ""
    reflection_supporting_message: str = ""
    reflection_next_transition: str = ""
    reflection_skip_available: bool = False
    reflection_prompts: tuple[ReflectionPromptViewModel, ...] = ()
    session_outcome_summary: str = ""
    day_complete: bool = False
    # P2-MS008 Experience Feedback Loop (factual Evidence display only)
    experience_feedback_enabled: bool = False
    experience_feedback_period_label: str = ""
    experience_feedback_source: str = ""
    experience_feedback_facts: tuple[ExperienceFeedbackFactViewModel, ...] = ()
    # EP-008.1 — Recommendation Trust presentation.
    trust_state: str = ""
    recommendation_alternatives: tuple[
        RecommendationAlternativeViewModel, ...
    ] = ()
    readiness_bridge_line: str = ""
    coach_trust: CoachTrustViewModel | None = None
    completion_loop_echo: str = ""
    l1_expected_benefit: str = ""
    # EP-008.3 — Recommendation Commitment.
    commitment: CommitmentViewModel | None = None
    # PX-001 — Runtime C educational enrichment (optional).
    educational: EducationalExperienceViewModel | None = None
    # TUTOR-001 — evidence-backed Tutor preview (mission extension).
    tutor_guidance: str = ""
    tutor_next_action: str = ""
    tutor_available: bool = False
    # ILE-004 — Daily Mission Intelligence (composition over authorised tip).
    mission_intelligence: object | None = None

@dataclass(frozen=True)
class StudentShellViewModel:
    """Shared shell chrome for every student surface."""

    active_surface: str
    active_label: str
    navigation: tuple[StudentNavItem, ...]
    page_title: str
    page_eyebrow: str = "Your learning"
    page_description: str = ""
    learning_activity_status: str = ""
    journey_stage: str = ""
    unified_journey_enabled: bool = False


@dataclass(frozen=True)
class StudentPageViewModel:
    """Composite page payload passed to templates."""

    shell: StudentShellViewModel
    home: HomePageViewModel | None = None
    journey: JourneyPageViewModel | None = None
    revision: RevisionPageViewModel | None = None
    history: HistoryPageViewModel | None = None
    profile: ProfilePageViewModel | None = None
    # PX-001 — Runtime C educational experience (when enrolled).
    educational: EducationalExperienceViewModel | None = None


# PX-002A T1-2: re-exported from the shared helper so Home, Mission and
# Session Overview share one duration-formatting implementation. Keep the
# name here for backward compatibility with existing importers.
format_minutes = _format_minutes


def format_readiness_percent(value: float | None) -> str:
    """Format a readiness ratio (0–1 or 0–100) as a percent label."""
    if value is None:
        return ""
    ratio = float(value)
    if ratio <= 1.0:
        pct = int(round(ratio * 100))
    else:
        pct = int(round(ratio))
    return f"{pct}%"


def format_benefit(delta: float | None, fallback: str = "") -> str:
    """Format expected readiness improvement for display."""
    if fallback:
        return fallback
    if delta is None:
        return ""
    pct = abs(delta)
    if pct <= 1.0:
        pct = pct * 100
    return f"About {pct:.0f}% readiness gain"


def contains_forbidden_term(text: str) -> bool:
    """True when learner-facing copy leaks internal architecture terms."""
    lowered = (text or "").lower()
    return any(term in lowered for term in FORBIDDEN_LEARNER_TERMS)


def explanation_vm(
    snap: ExplanationSnapshot | None,
) -> ExplanationViewModel | None:
    if snap is None:
        return None
    # EP-006.2: keep up to 4 evidence points for L2 disclosure (service cap).
    evidence = tuple(snap.evidence_points or ())[:4]
    next_action = (snap.suggested_next_action or "").strip()
    review_point = (snap.review_point or "").strip()
    confidence_basis = (snap.confidence_basis or "").strip()
    alternatives_hint = False  # disclosure also opened by home alternatives
    has_disclosure = bool(
        evidence
        or review_point
        or confidence_basis
        or next_action
        or alternatives_hint
        or (snap.plan_coherence_label and not snap.honest_refusal)
    )
    return ExplanationViewModel(
        summary=snap.summary,
        why_recommended=snap.why_recommended,
        evidence_points=evidence,
        expected_benefit=snap.expected_benefit,
        confidence_label=snap.confidence_label,
        suggested_next_action=next_action,
        review_point=review_point,
        confidence_basis=confidence_basis,
        is_complete=snap.is_complete,
        has_content=bool(
            snap.summary
            or snap.why_recommended
            or evidence
            or snap.expected_benefit
            or next_action
            or snap.timeliness_line
            or snap.plan_coherence_label
        ),
        has_disclosure=has_disclosure,
        plan_coherence=snap.plan_coherence or "",
        plan_coherence_label=snap.plan_coherence_label or "",
        honest_refusal=bool(snap.honest_refusal),
        timeliness_line=snap.timeliness_line or "",
        completion_loop_line=(
            snap.completion_loop_line or review_point or ""
        ),
    )


def home_vm(
    snap: HomeSnapshot,
    *,
    journey: JourneySnapshot | None = None,
    history: HistorySnapshot | None = None,
    revision: RevisionSnapshot | None = None,
    unified_journey: bool | None = None,
    experience_feedback: object | None = None,
) -> HomePageViewModel:
    start = snap.start_session
    cta_enabled = bool(snap.can_start_session and start and start.enabled)
    cta_label = (
        (start.label if start and start.label else "Continue")
        if cta_enabled
        else "Continue"
    )
    benefit = format_benefit(
        snap.expected_readiness_improvement,
        fallback=(
            snap.explanation.expected_benefit if snap.explanation else ""
        ),
    )
    trend = ""
    if history is not None:
        trend = _readiness_trend_label(history.readiness_progression)
    use_unified = (
        unified_journey
        if unified_journey is not None
        else _unified_journey_enabled()
    )
    daily_mission = _home_daily_mission(
        snap,
        cta_label=cta_label,
        cta_enabled=cta_enabled,
        benefit=benefit,
        enabled=use_unified,
    )
    day_experience = _home_day_experience(
        daily_mission,
        enabled=use_unified,
        cta_label=cta_label,
    )
    study_session = _home_study_session(day_experience, enabled=use_unified)
    reflection = _home_reflection(day_experience, enabled=use_unified)
    guided = bool(use_unified and day_experience.mission_active)
    reflection_active = bool(use_unified and day_experience.reflection_active)
    day_complete = bool(
        use_unified
        and (
            (daily_mission.is_completed or study_session.is_complete)
            and not reflection_active
        )
    )
    timeline_steps = (
        tuple(
            ExperienceTimelineStepViewModel(
                key=step.key,
                label=step.label,
                status=step.status,
            )
            for step in day_experience.timeline.steps
        )
        if use_unified
        else ()
    )
    control_label, control_action = _home_session_control(
        day_experience,
        study_session,
        guided=guided,
        cta_enabled=cta_enabled,
    )
    # CQ-003 / CR2: Resume labelling without Unified Journey — Continue + deep link.
    resume_without_unified = bool(
        not use_unified
        and cta_enabled
        and start
        and start.session_id
        and _is_resume_cta_label(start.label)
    )
    if resume_without_unified:
        control_label = "Continue"
        control_action = "resume"
    mission_cta_label = (
        control_label
        if use_unified and control_label
        else (
            daily_mission.start_action.label
            if use_unified and daily_mission.start_action.label
            else cta_label
        )
    )
    if resume_without_unified:
        mission_cta_label = control_label
    # Session gate remains the live Home authority for enabling start.
    mission_cta_enabled = (
        cta_enabled and daily_mission.start_action.enabled
        if use_unified
        else cta_enabled
    )
    if use_unified and daily_mission.is_completed:
        mission_cta_enabled = False
    if use_unified and guided and study_session.is_studying:
        # Finish is presentation-only; keep CTA available while studying.
        mission_cta_enabled = True
    if use_unified and guided and study_session.is_wrapping_up:
        mission_cta_enabled = True
    if use_unified and reflection_active:
        mission_cta_enabled = False
    explanation = explanation_vm(snap.explanation)
    # Open disclosure when Home carries alternatives (EP-008.1 T10).
    if (
        explanation is not None
        and snap.recommendation_alternatives
        and not (snap.explanation and snap.explanation.honest_refusal)
    ):
        from dataclasses import replace as _replace_vm

        explanation = _replace_vm(explanation, has_disclosure=True)
    alternatives_vm = tuple(
        RecommendationAlternativeViewModel(
            title=alt.title,
            why_recommended=alt.why_recommended,
            expected_benefit=alt.expected_benefit,
            suggested_next_action=alt.suggested_next_action,
        )
        for alt in (snap.recommendation_alternatives or ())
    )
    coach_trust = _compose_coach_trust(snap)
    coach_insight = _compose_coach_insight(snap, coach_trust=coach_trust)
    l1_benefit = ""
    if snap.explanation and snap.explanation.expected_benefit:
        l1_benefit = snap.explanation.expected_benefit.strip()
    readiness_bridge = ""
    if (
        snap.explanation
        and not snap.explanation.honest_refusal
        and snap.readiness_explanation
        and (snap.readiness_explanation.expected_benefit or "").strip()
    ):
        from app.application.student_experience.recommendation_trust import (
            readiness_bridge_sentence,
        )

        readiness_bridge = readiness_bridge_sentence(
            readiness_expected_benefit=snap.readiness_explanation.expected_benefit
        )
    completion_echo = ""
    if snap.explanation:
        completion_echo = (
            snap.explanation.completion_loop_line
            or snap.explanation.review_point
            or ""
        ).strip()
    if not completion_echo and day_complete:
        from app.application.student_experience.recommendation_trust import (
            completion_loop_fallback,
        )

        completion_echo = completion_loop_fallback()

    return HomePageViewModel(
        greeting=snap.greeting or "Welcome back",
        examination_label=snap.examination_label,
        countdown=CountdownCardViewModel(
            days=snap.exam_countdown_days,
            label=_countdown_label(snap.exam_countdown_days),
            examination_label=snap.examination_label,
            has_countdown=snap.exam_countdown_days is not None,
        ),
        readiness=ReadinessCardViewModel(
            readiness_label=snap.exam_readiness_label or "Exam Readiness",
            readiness_percent_label=format_readiness_percent(
                snap.exam_readiness
            ),
            trend_label=trend,
            confidence_label=_home_readiness_confidence(snap),
            confidence_basis=_home_readiness_confidence_basis(snap),
            why_this_estimate=_home_readiness_why(snap),
            suggested_next_action=_home_readiness_next_action(snap),
            review_point=_home_readiness_review_point(snap),
            readiness_drivers=_home_readiness_drivers(snap),
            supporting_evidence=_home_readiness_evidence(snap),
            expected_benefit=_home_readiness_expected_benefit(snap),
            has_readiness=snap.exam_readiness is not None
            or bool(
                snap.readiness_explanation
                and snap.readiness_explanation.why_this_estimate
            ),
            has_disclosure=_home_readiness_has_disclosure(snap),
        ),
        recommendation=RecommendationCardViewModel(
            title=snap.recommendation_title,
            summary=snap.recommendation_summary,
            benefit_label=benefit,
            time_label=format_minutes(snap.estimated_study_minutes),
            reason=(
                snap.explanation.why_recommended if snap.explanation else ""
            ),
            cta_label=cta_label,
            cta_enabled=cta_enabled,
            has_recommendation=snap.has_recommendation,
        ),
        explanation=explanation,
        start_session=start,
        estimated_study_label=format_minutes(snap.estimated_study_minutes),
        expected_benefit_label=benefit,
        can_start_session=snap.can_start_session,
        primary_cta_label=mission_cta_label if use_unified else cta_label,
        primary_cta_enabled=mission_cta_enabled if use_unified else cta_enabled,
        mission_id=(start.mission_id or "") if start else "",
        session_id=(start.session_id or "") if start else "",
        journey_story=_compose_journey_story(
            snap, journey=journey, history=history
        ),
        coach_insight=coach_insight,
        milestones=_compose_milestones(journey=journey, revision=revision),
        quick_actions=_compose_quick_actions(
            snap, revision=revision, cta_enabled=cta_enabled
        ),
        unified_journey_enabled=use_unified,
        journey_stage=daily_mission.stage.value if use_unified else "",
        primary_mission_title=daily_mission.title if use_unified else "",
        why_it_matters=daily_mission.reason if use_unified else "",
        estimated_duration_label=(
            daily_mission.estimated_duration if use_unified else ""
        ),
        expected_outcome=daily_mission.expected_outcome if use_unified else "",
        mission_summary=daily_mission.mission_summary if use_unified else "",
        mission_priority=daily_mission.priority if use_unified else "",
        completion_status=(
            daily_mission.completion_status if use_unified else ""
        ),
        completion_status_label=(
            daily_mission.completion_status_label if use_unified else ""
        ),
        timeline_steps=timeline_steps,
        guided_session_active=guided,
        session_phase=study_session.current_phase.value if use_unified else "",
        session_status=day_experience.session_status if use_unified else "",
        session_learning_objective=(
            study_session.learning_objective if use_unified else ""
        ),
        session_next_step=study_session.next_step if use_unified else "",
        session_elapsed_state=(
            study_session.elapsed_state if use_unified else ""
        ),
        session_start_time_label=(
            study_session.start_time if use_unified else ""
        ),
        session_progress_summary=(
            day_experience.progress_summary if use_unified else ""
        ),
        session_control_label=(
            control_label if use_unified or resume_without_unified else ""
        ),
        session_control=(
            control_action if use_unified or resume_without_unified else ""
        ),
        reflection_available=(
            day_experience.reflection_available if use_unified else False
        ),
        reflection_active=reflection_active,
        reflection_state=(
            day_experience.reflection_state.value
            if use_unified and day_experience.reflection_state is not None
            else ""
        ),
        reflection_headline=reflection.headline if use_unified else "",
        reflection_supporting_message=(
            reflection.supporting_message if use_unified else ""
        ),
        reflection_next_transition=(
            reflection.next_transition if use_unified else ""
        ),
        reflection_skip_available=(
            bool(reflection.skip_available and reflection_active)
            if use_unified
            else False
        ),
        reflection_prompts=(
            tuple(
                ReflectionPromptViewModel(
                    prompt=prompt.prompt,
                    response_type=prompt.response_type,
                    available_options=prompt.available_options,
                    optional_note_placeholder=prompt.optional_note_placeholder,
                )
                for prompt in reflection.prompts
            )
            if use_unified and reflection_active
            else ()
        ),
        session_outcome_summary=(
            (
                day_experience.session_outcome.summary_message
                if day_experience.session_outcome is not None
                else ""
            )
            if use_unified
            else ""
        ),
        day_complete=day_complete,
        experience_feedback_enabled=bool(
            use_unified and _experience_feedback_displayable(experience_feedback)
        ),
        experience_feedback_period_label=(
            str(getattr(experience_feedback, "reporting_period_label", "") or "")
            if use_unified and experience_feedback is not None
            else ""
        ),
        experience_feedback_source=(
            str(getattr(experience_feedback, "source_description", "") or "")
            if use_unified and experience_feedback is not None
            else ""
        ),
        experience_feedback_facts=(
            _experience_feedback_facts(experience_feedback)
            if use_unified and experience_feedback is not None
            else ()
        ),
        trust_state=snap.trust_state or "",
        recommendation_alternatives=alternatives_vm,
        readiness_bridge_line=readiness_bridge,
        coach_trust=coach_trust,
        completion_loop_echo=completion_echo,
        l1_expected_benefit=l1_benefit,
        commitment=_commitment_vm(snap),
        mission_intelligence=_home_mission_intelligence(
            snap,
            benefit=benefit,
            alternatives=alternatives_vm,
            completion_echo=completion_echo,
        ),
        **_tutor_home_fields(snap),
    )


def _home_mission_intelligence(
    snap: HomeSnapshot,
    *,
    benefit: str,
    alternatives: tuple,
    completion_echo: str,
):
    """ILE-004 — compose today's primary mission brief (no re-decision)."""
    from app.application.daily_mission_intelligence import (
        DailyMissionIntelligenceApplicationService,
    )

    expl = snap.explanation
    title = (snap.recommendation_title or "").strip()
    if not title and snap.start_session:
        title = (snap.start_session.topic_title or "").strip()
    if not title and not (expl and expl.honest_refusal):
        return DailyMissionIntelligenceApplicationService.compose_snapshot()

    effort = ""
    if snap.estimated_study_minutes is not None:
        effort = format_minutes(snap.estimated_study_minutes) or ""
    elif snap.start_session and snap.start_session.estimated_minutes is not None:
        effort = format_minutes(snap.start_session.estimated_minutes) or ""

    alt_titles = tuple(
        (a.title or "").strip()
        for a in (alternatives or ())
        if (getattr(a, "title", None) or "").strip()
    )
    evidence = ()
    if expl and expl.evidence_points:
        evidence = tuple(expl.evidence_points)
    commitment = getattr(snap, "commitment", None)
    rec_key = ""
    if commitment is not None:
        rec_key = (commitment.recommendation_key or "").strip()
    prior = ""
    if commitment is not None and (commitment.state or "") == "deferred":
        prior = (
            "You deferred related guidance earlier. "
            "Still the right call for today?"
        )

    return DailyMissionIntelligenceApplicationService.compose_snapshot(
        title=title,
        summary=snap.recommendation_summary or "",
        why_recommended=(expl.why_recommended if expl else "") or "",
        timeliness_line=(expl.timeliness_line if expl else "") or "",
        supporting_evidence=evidence,
        estimated_effort=effort,
        expected_benefit=(
            (expl.expected_benefit if expl else "") or benefit or ""
        ),
        suggested_next_action=(
            (expl.suggested_next_action if expl else "") or ""
        ),
        review_point=(expl.review_point if expl else "") or "",
        completion_loop_line=(
            (expl.completion_loop_line if expl else "")
            or completion_echo
            or ""
        ),
        confidence_label=(expl.confidence_label if expl else "") or "",
        confidence_basis=(expl.confidence_basis if expl else "") or "",
        uncertainty="",
        honest_refusal=bool(expl.honest_refusal) if expl else False,
        alternative_titles=alt_titles,
        recommendation_key=rec_key,
        mission_id=(
            (snap.start_session.mission_id or "") if snap.start_session else ""
        ),
        session_id=(
            (snap.start_session.session_id or "") if snap.start_session else ""
        ),
        educational_context="Today's Mission",
        prior_deferral_note=prior,
    )


def _tutor_home_fields(_snap: HomeSnapshot) -> dict:
    """Best-effort TUTOR-001 preview from Twin / Adaptive Mission (no redesign)."""
    empty = {
        "tutor_guidance": "",
        "tutor_next_action": "",
        "tutor_available": False,
    }
    try:
        from flask_login import current_user

        from app.application.intelligent_tutor.intelligent_tutor_service import (
            IntelligentTutorService,
        )
        from app.application.student_digital_twin.student_digital_twin_service import (
            StudentDigitalTwinService,
        )

        user_id = str(getattr(current_user, "id", "") or "")
        if not user_id:
            return empty
        twins = StudentDigitalTwinService().list_twins_for_student(user_id)
        if not twins:
            # Also try external_user_id match via student_id conventions.
            return empty
        preview = IntelligentTutorService().preview_mission_guidance(
            twins[0].twin_id
        )
        return {
            "tutor_guidance": preview.get("guidance") or "",
            "tutor_next_action": preview.get("next_action") or "",
            "tutor_available": bool(preview.get("available")),
        }
    except Exception:  # noqa: BLE001 — Home must never fail on Tutor preview
        return empty


def _commitment_vm(snap: HomeSnapshot) -> CommitmentViewModel | None:
    """Map commitment snapshot to presentation VM."""
    c = getattr(snap, "commitment", None)
    if c is None:
        return None
    state = (c.state or "offered").strip().lower()
    reflection_vm = None
    if c.reflection is not None:
        reflection_vm = CommitmentReflectionViewModel(
            what_you_did=c.reflection.what_you_did or "",
            what_changed=c.reflection.what_changed or "",
            why_it_mattered=c.reflection.why_it_mattered or "",
            what_was_learned=c.reflection.what_was_learned or "",
            what_happens_next=c.reflection.what_happens_next or "",
        )
    is_committed = state in {"committed", "in_session"}
    coach_status = "Committed for today" if is_committed else ""
    return CommitmentViewModel(
        state=state,
        recommendation_key=c.recommendation_key or "",
        title=c.title or "",
        continuity_line=c.continuity_line or "",
        deferred_reason_label=c.deferred_reason_label or "",
        show_commit_affordance=bool(c.show_commit_affordance),
        show_defer_affordance=bool(c.show_defer_affordance),
        is_committed=is_committed,
        is_deferred=state == "deferred",
        show_reflection=state == "completed" and reflection_vm is not None,
        reflection=reflection_vm,
        coach_status_line=coach_status,
    )


def _home_daily_mission(
    snap: HomeSnapshot,
    *,
    cta_label: str,
    cta_enabled: bool,
    benefit: str,
    enabled: bool,
):
    """Assemble presentation DailyMission from JourneyContext (Programme I)."""
    from app.application.unified_journey import (
        DailyMissionAssembler,
        JourneyCoordinator,
        JourneyStage,
        JourneySubsystemInputs,
        MissionStartAction,
        empty_daily_mission,
    )
    from app.application.unified_journey.daily_mission import DailyMission

    if not enabled:
        return empty_daily_mission()

    coordinator = JourneyCoordinator()
    inputs: JourneySubsystemInputs | None = None
    if snap.has_recommendation and snap.recommendation_title:
        why = (
            snap.explanation.why_recommended
            if snap.explanation and snap.explanation.why_recommended
            else snap.recommendation_summary
        )
        explanation: dict[str, Any] = {}
        if snap.explanation is not None:
            explanation = {
                "why_recommended": snap.explanation.why_recommended or "",
                "expected_benefit": snap.explanation.expected_benefit or "",
                "summary": snap.explanation.summary or "",
                "confidence_label": snap.explanation.confidence_label or "",
                "suggested_next_action": (
                    snap.explanation.suggested_next_action or ""
                ),
                "review_point": snap.explanation.review_point or "",
                "supporting_evidence": list(
                    snap.explanation.evidence_points or ()
                ),
                "evidence_points": list(snap.explanation.evidence_points or ()),
                "confidence_basis": snap.explanation.confidence_basis or "",
                "plan_coherence": snap.explanation.plan_coherence or "",
                "plan_coherence_label": (
                    snap.explanation.plan_coherence_label or ""
                ),
                "honest_refusal": bool(snap.explanation.honest_refusal),
                "timeliness_line": snap.explanation.timeliness_line or "",
                "completion_loop_line": (
                    snap.explanation.completion_loop_line or ""
                ),
            }
        # HomeSnapshot already carries Runtime A recommendation projection —
        # pass through as opaque runtime_a map. Assembler does not invent.
        runtime_a = {
            "title": snap.recommendation_title,
            "summary": snap.recommendation_summary,
            "why_it_matters": why or "",
            "expected_outcome": benefit or "",
            "expected_benefit": benefit or "",
            "estimated_minutes": snap.estimated_study_minutes,
            "cta_label": cta_label,
            "endpoint": (
                "student.start_session" if cta_enabled else "student.home"
            ),
            "journey_stage": JourneyStage.DAILY_MISSION.value,
            "explanation": explanation,
            "has_recommendation": True,
            "can_start_session": snap.can_start_session,
            "suggested_next_action": (
                snap.explanation.suggested_next_action
                if snap.explanation
                else ""
            ),
            "review_point": (
                snap.explanation.review_point if snap.explanation else ""
            ),
            "why_recommended": (
                snap.explanation.why_recommended if snap.explanation else ""
            ),
            "supporting_evidence": list(
                snap.explanation.evidence_points if snap.explanation else ()
            ),
            "confidence_level": (
                snap.explanation.confidence_label if snap.explanation else ""
            ),
        }
        inputs = JourneySubsystemInputs(
            runtime_a=runtime_a,
            stage_hint=JourneyStage.DAILY_MISSION,
        )
    context = coordinator.journey_context(
        snap.student_id or "anonymous",
        inputs=inputs,
    )
    mission = DailyMissionAssembler().assemble(context)
    # Preserve CTA enabled from the live Home session gate (presentation).
    if mission.start_action.enabled != cta_enabled or (
        cta_label and cta_label != mission.start_action.label
        and not mission.is_completed
    ):
        label = mission.start_action.label
        if cta_label and not mission.is_completed:
            label = cta_label
        enabled_cta = False if mission.is_completed else cta_enabled
        return DailyMission(
            title=mission.title,
            reason=mission.reason,
            estimated_duration=mission.estimated_duration,
            expected_outcome=mission.expected_outcome,
            priority=mission.priority,
            completion_status=mission.completion_status,
            start_action=MissionStartAction(
                label=label,
                enabled=enabled_cta,
                endpoint=mission.start_action.endpoint,
            ),
            mission_summary=mission.mission_summary,
            stage=mission.stage,
            metadata=mission.metadata,
        )
    return mission


def _home_timeline(mission):
    from app.application.unified_journey import timeline_from_daily_mission

    return timeline_from_daily_mission(mission)


def _home_day_experience(mission, *, enabled: bool, cta_label: str = ""):
    """Assemble DayExperience from DailyMission (P2-MS004)."""
    from app.application.unified_journey import (
        DayExperienceAssembler,
        empty_day_experience,
    )

    if not enabled:
        return empty_day_experience()
    phase = _infer_guided_phase(mission, cta_label=cta_label)
    return DayExperienceAssembler().assemble(mission, phase=phase)


def _infer_guided_phase(mission, *, cta_label: str = ""):
    """Presentation phase hint from existing UI completion / CTA wording."""
    from app.application.unified_journey import SessionPhase

    if mission.is_completed:
        return SessionPhase.COMPLETE
    if mission.is_in_progress:
        return SessionPhase.STUDYING
    label = (cta_label or "").casefold()
    if "continue" in label or "resume" in label:
        return SessionPhase.STUDYING
    return None


def _home_study_session(day, *, enabled: bool):
    """Assemble StudySession from DayExperience (P2-MS004)."""
    from app.application.unified_journey import (
        StudySessionAssembler,
        empty_study_session,
    )

    if not enabled:
        return empty_study_session()
    return StudySessionAssembler().assemble(day)


def _home_reflection(day, *, enabled: bool):
    """Assemble ReflectionExperience from SessionOutcome (P2-MS005)."""
    from app.application.unified_journey import (
        ReflectionAssembler,
        empty_reflection_experience,
    )

    if not enabled:
        return empty_reflection_experience()
    return ReflectionAssembler().assemble(
        day.session_outcome,
        state=day.reflection_state,
    )


def _home_session_control(day, session, *, guided: bool, cta_enabled: bool):
    """Resolve presentation Start / Resume / Finish label + action key."""
    if not guided:
        return "", ""
    if session.is_ready:
        label = "Resume" if day.daily_mission.is_in_progress else "Start"
        action = "resume" if day.daily_mission.is_in_progress else "start"
        if not cta_enabled and action == "start":
            return label, action
        return label, action
    if session.is_studying:
        return "Finish", "finish"
    if session.is_wrapping_up:
        return "Complete session", "finish"
    return "", ""


def _home_primary_mission(
    snap: HomeSnapshot,
    *,
    cta_label: str,
    cta_enabled: bool,
    benefit: str,
    enabled: bool,
):
    """Legacy HomePrimaryMission projection — prefer ``_home_daily_mission``."""
    from app.application.unified_journey import (
        HomePrimaryMission,
        empty_home_primary_mission,
    )

    mission = _home_daily_mission(
        snap,
        cta_label=cta_label,
        cta_enabled=cta_enabled,
        benefit=benefit,
        enabled=enabled,
    )
    if not enabled:
        return empty_home_primary_mission()
    return HomePrimaryMission(
        title=mission.title,
        why_it_matters=mission.reason,
        estimated_duration_label=mission.estimated_duration,
        expected_outcome=mission.expected_outcome,
        cta_label=mission.start_action.label,
        cta_enabled=mission.start_action.enabled,
        endpoint=mission.start_action.endpoint,
        stage=mission.stage,
        availability=(
            "available"
            if mission.title and mission.title != "Today's Mission"
            else "placeholder"
        ),
        unavailable_reason="",
        metadata=mission.metadata,
    )



def _unified_journey_enabled() -> bool:
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags

        return bool(resolve_v2_feature_flags().ENABLE_UNIFIED_JOURNEY)
    except Exception:
        return False


def _experience_feedback_enabled() -> bool:
    try:
        from app.application.config.v2_flags import resolve_v2_feature_flags

        return bool(resolve_v2_feature_flags().ENABLE_EXPERIENCE_FEEDBACK)
    except Exception:
        return False


def _experience_feedback_displayable(feedback: object | None) -> bool:
    if feedback is None:
        return False
    facts = getattr(feedback, "facts", ()) or ()
    return bool(facts)


def _experience_feedback_facts(
    feedback: object,
) -> tuple[ExperienceFeedbackFactViewModel, ...]:
    facts = getattr(feedback, "facts", ()) or ()
    return tuple(
        ExperienceFeedbackFactViewModel(
            key=str(getattr(fact, "key", "") or ""),
            label=str(getattr(fact, "label", "") or ""),
            value_label=str(getattr(fact, "value_label", "") or ""),
            source_description=str(
                getattr(fact, "source_description", "") or ""
            ),
        )
        for fact in facts
    )


def _load_experience_feedback(student_id: str) -> object | None:
    """Load factual ExperienceFeedback via composition DI (flag-gated)."""
    if not _experience_feedback_enabled():
        return None
    sid = (student_id or "").strip()
    if not sid:
        return None
    try:
        from app.presentation.student.factory import get_experience_composition

        composition = get_experience_composition()
    except Exception:
        return None
    if composition is None:
        return None
    reader = getattr(composition, "experience_feedback", None)
    if reader is None or not hasattr(reader, "load"):
        return None
    try:
        return reader.load(sid)
    except Exception:
        return None


def journey_vm(snap: JourneySnapshot) -> JourneyPageViewModel:
    has_current = snap.current_topic is not None
    return JourneyPageViewModel(
        examination_label=snap.examination_label,
        current=_topic_vm(snap.current_topic) if snap.current_topic else None,
        completed=tuple(_topic_vm(t) for t in snap.completed_topics),
        upcoming=tuple(_topic_vm(t) for t in snap.upcoming_topics),
        progress_percent=snap.progress_percent,
        progress_label=f"{snap.progress_percent}% complete",
        estimated_completion_label=snap.estimated_completion_label,
        prerequisite_notes=snap.prerequisite_visibility,
        completed_count=snap.completed_count,
        upcoming_count=snap.upcoming_count,
        primary_cta_label="Continue with current topic"
        if has_current
        else "Explore your journey",
        primary_cta_enabled=has_current or bool(snap.upcoming_topics),
    )


def journey_card_vm(snap: JourneySnapshot) -> JourneyCardViewModel:
    next_topic = snap.upcoming_topics[0] if snap.upcoming_topics else None
    return JourneyCardViewModel(
        current_topic_title=(
            snap.current_topic.title if snap.current_topic else ""
        ),
        progress_percent=snap.progress_percent,
        progress_label=f"{snap.progress_percent}% complete",
        next_topic_title=next_topic.title if next_topic else "",
        estimated_completion_label=snap.estimated_completion_label,
        has_journey=bool(
            snap.current_topic or snap.completed_topics or snap.upcoming_topics
        ),
    )


def revision_vm(snap: RevisionSnapshot) -> RevisionPageViewModel:
    primary = _revision_option_vm(snap.primary) if snap.primary else None
    return RevisionPageViewModel(
        primary=primary,
        alternatives=tuple(_revision_option_vm(o) for o in snap.alternatives),
        empty_message=snap.empty_message
        or (
            "No revision support is ready yet. Follow today's Mission on "
            "Home — Revision will appear when there is something worth "
            "strengthening."
        ),
        has_revision=snap.has_revision,
        option_count=snap.option_count,
        primary_cta_label="Begin Revision",
        primary_cta_enabled=snap.has_revision and primary is not None,
    )


def history_vm(snap: HistorySnapshot) -> HistoryPageViewModel:
    points = tuple(
        (p.recorded_at, format_readiness_percent(p.exam_readiness) or p.label)
        for p in snap.readiness_progression
    )
    trend = _readiness_trend_label(snap.readiness_progression)
    narrative = tuple(
        RecommendationNarrativeEntryViewModel(
            kind=entry.kind,
            title=entry.title,
            occurred_at=entry.occurred_at,
            summary_line=entry.summary_line,
            reason_label=entry.reason_label,
        )
        for entry in (snap.recommendation_narrative or ())
    )
    return HistoryPageViewModel(
        sessions=tuple(_session_vm(s) for s in snap.completed_sessions),
        total_study_label=format_minutes(snap.total_study_minutes)
        or "No study time recorded yet",
        readiness_points=points,
        mastered_topics=snap.mastered_topics,
        revision_history=snap.revision_history,
        achievements=snap.recent_achievements,
        session_count=snap.session_count,
        mastered_count=snap.mastered_count,
        readiness_trend_label=trend,
        primary_cta_label="Return Home",
        primary_cta_enabled=True,
        recommendation_narrative=narrative,
        recommendation_narrative_header=(
            snap.recommendation_narrative_header or ""
        ),
    )


def decision_journal_page_vm(timeline) -> StudentPageViewModel:
    """Build shell + empty siblings for the ILE-002 Decision Journal page."""
    from app.domain.student_experience.experience_workspace import (
        ExperienceSurface,
    )

    shell = shell_vm(
        active_surface=ExperienceSurface.HISTORY.value,
        page_title=timeline.page_title,
        page_description=timeline.page_description,
    )
    shell = StudentShellViewModel(
        active_surface=shell.active_surface,
        active_label=shell.active_label,
        navigation=shell.navigation,
        page_title=timeline.page_title,
        page_eyebrow=timeline.page_eyebrow,
        page_description=timeline.page_description,
        learning_activity_status=shell.learning_activity_status,
        journey_stage=shell.journey_stage,
        unified_journey_enabled=shell.unified_journey_enabled,
    )
    return StudentPageViewModel(shell=shell)


def educational_timeline_page_vm(timeline) -> StudentPageViewModel:
    """Build shell for the ILE-003 Educational Timeline page."""
    from app.domain.student_experience.experience_workspace import (
        ExperienceSurface,
    )

    shell = shell_vm(
        active_surface=ExperienceSurface.HISTORY.value,
        page_title=timeline.page_title,
        page_description=timeline.page_description,
    )
    shell = StudentShellViewModel(
        active_surface=shell.active_surface,
        active_label=shell.active_label,
        navigation=shell.navigation,
        page_title=timeline.page_title,
        page_eyebrow=timeline.page_eyebrow,
        page_description=timeline.page_description,
        learning_activity_status=shell.learning_activity_status,
        journey_stage=shell.journey_stage,
        unified_journey_enabled=shell.unified_journey_enabled,
    )
    return StudentPageViewModel(shell=shell)


def _authoritative_examination_label(student_id: str) -> str:
    """Resolve "Current Examination" from the same source of truth used by
    Dashboard, Study Plan, and Settings -> Internal Alpha
    (``StudyPlanService.get_user_active_plan``), so Profile can never show
    "Not set" while those screens show an active plan (B2, PX-003 release
    blockers). Returns "" — letting the Twin-derived value or "Not set"
    apply — for non-persisted identities (e.g. test doubles) or students
    with no active plan.
    """
    if not student_id.isdigit():
        return ""
    from app.services.study_plan_service import StudyPlanService

    plan = StudyPlanService.get_user_active_plan(int(student_id))
    if plan is None:
        return ""
    return str(plan.exam_name or "")


def profile_vm(snap: ProfileSnapshot) -> ProfilePageViewModel:
    prefs = snap.preferences
    days = ", ".join(prefs.preferred_study_days) if prefs.preferred_study_days else ""
    return ProfilePageViewModel(
        display_name=snap.display_name,
        examination_label=(
            _authoritative_examination_label(snap.student_id)
            or snap.examination_label
        ),
        preferences=prefs,
        statistics=snap.statistics,
        goals=snap.goals,
        account=snap.account,
        preferences_days_label=days,
        readiness_percent_label=format_readiness_percent(
            snap.statistics.current_exam_readiness
        ),
        total_study_label=format_minutes(snap.statistics.total_study_minutes),
        primary_cta_label="Open account settings",
        primary_cta_enabled=True,
        # B9 (PX-003): "settings.index" (bare `/settings/`) now redirects to
        # this very page under sole runtime — pointing here instead avoids a
        # CTA that appears to do nothing, and lands on preferences, which
        # (per `alpha/help.html`'s own guidance) is the first genuinely
        # distinct, not-yet-migrated settings capability.
        primary_cta_endpoint="settings.preferences",
    )


def shell_vm(
    *,
    active_surface: str,
    page_title: str,
    page_description: str = "",
    learning_activity_status: str = "",
    navigation: tuple[NavigationItemSnapshot, ...] | None = None,
    unified_journey: bool | None = None,
) -> StudentShellViewModel:
    use_unified = (
        unified_journey
        if unified_journey is not None
        else _unified_journey_enabled()
    )
    # Prefer the consolidated OS nav tree (primary + Study Plan + Help),
    # or journey-stage chrome when ENABLE_UNIFIED_JOURNEY is on.
    nav = build_navigation(active_surface, unified_journey=use_unified)
    if navigation and not use_unified:
        # Preserve active highlighting from the dashboard aggregate when present.
        active_keys = {item.surface for item in navigation if item.active}
        if active_keys:
            nav = tuple(
                StudentNavItem(
                    surface=item.surface,
                    label=item.label,
                    endpoint=item.endpoint,
                    active=item.surface in active_keys,
                )
                for item in nav
            )
    active_label = next(
        (item.label for item in nav if item.active),
        active_surface.title(),
    )
    journey_stage = ""
    if use_unified:
        from app.application.unified_journey.navigation_map import (
            stage_for_surface,
        )

        try:
            journey_stage = stage_for_surface(active_surface).value
        except ValueError:
            journey_stage = ""
    return StudentShellViewModel(
        active_surface=active_surface,
        active_label=active_label,
        navigation=nav,
        page_title=page_title,
        page_eyebrow="Your learning",
        page_description=page_description,
        learning_activity_status=learning_activity_status,
        journey_stage=journey_stage,
        unified_journey_enabled=use_unified,
    )


def page_from_dashboard(
    dash: DashboardSnapshot,
    *,
    surface: str,
) -> StudentPageViewModel:
    """Build a page view model from a dashboard snapshot for ``surface``."""
    use_unified = _unified_journey_enabled()
    descriptions = {
        "home": "What you should do next, and why.",
        "journey": "Where you are on the path to exam readiness.",
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
    titles = {
        # PX-002A T1-1: "Home" retired the "Dashboard" collision with the
        # legacy Learning Workspace home (still "Student Dashboard").
        "home": "Home" if not use_unified else "Today",
        "journey": "Journey" if not use_unified else "Exam Readiness",
        "revision": "Revision",
        # PX-002A: renamed from "Analytics" — see SURFACE_LABELS note.
        "history": "History" if not use_unified else "Archive",
        "profile": "Settings" if not use_unified else "Onboarding",
    }
    shell = shell_vm(
        active_surface=surface,
        page_title=titles.get(surface, surface.title()),
        page_description=descriptions.get(surface, ""),
        learning_activity_status=dash.learning_activity_status,
        navigation=dash.navigation,
        unified_journey=use_unified,
    )
    home = None
    if dash.home is not None:
        # Reuse sibling XP snapshots already loaded on the dashboard aggregate.
        feedback = None
        if use_unified and surface == "home":
            feedback = _load_experience_feedback(dash.home.student_id)
        home = home_vm(
            dash.home,
            journey=dash.journey,
            history=dash.history,
            revision=dash.revision,
            unified_journey=use_unified,
            experience_feedback=feedback,
        )
        if surface == "home" and home is not None:
            home = _present_mission_intelligence(dash.home.student_id, home)
    return StudentPageViewModel(
        shell=shell,
        home=home,
        journey=journey_vm(dash.journey) if dash.journey else None,
        revision=revision_vm(dash.revision) if dash.revision else None,
        history=history_vm(dash.history) if dash.history else None,
        profile=profile_vm(dash.profile) if dash.profile else None,
    )


def _present_mission_intelligence(
    student_id: str,
    home: HomePageViewModel,
) -> HomePageViewModel:
    """ILE-004 — idempotently journal Mission presentation (fail-open)."""
    from dataclasses import replace

    mi = getattr(home, "mission_intelligence", None)
    if mi is None or not getattr(mi, "has_mission", False):
        return home
    try:
        user_id = int(str(student_id).strip())
    except (TypeError, ValueError):
        return home
    try:
        from app.application.daily_mission_intelligence import (
            DailyMissionIntelligenceApplicationService,
        )

        presented = DailyMissionIntelligenceApplicationService.present(
            user_id,
            mi,
        )
        return replace(home, mission_intelligence=presented)
    except Exception:  # noqa: BLE001 — Home must never fail on journal mirror
        return home


def _topic_vm(topic: JourneyTopicSnapshot) -> JourneyTopicViewModel:
    return JourneyTopicViewModel(
        topic_id=topic.topic_id,
        title=topic.title,
        status_label=topic.status_label,
        prerequisite_note=topic.prerequisite_note,
    )


def _revision_option_vm(
    option: RevisionOptionSnapshot,
) -> RevisionOptionViewModel:
    return RevisionOptionViewModel(
        option_id=option.option_id,
        topic_title=option.topic_title,
        priority_label=option.priority_label,
        time_label=format_minutes(option.estimated_study_minutes),
        expected_benefit=option.expected_benefit,
        explanation=explanation_vm(option.explanation),
        is_primary=option.is_primary,
    )


def _session_vm(session: CompletedSessionSnapshot) -> HistorySessionViewModel:
    return HistorySessionViewModel(
        session_id=session.session_id,
        topic_title=session.topic_title,
        completed_at=session.completed_at,
        duration_label=format_minutes(session.study_minutes),
        outcome_label="Completed",
    )


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


def _readiness_trend_label(
    points: tuple[ReadinessPointSnapshot, ...],
) -> str:
    if len(points) < 2:
        return "Not enough history for a trend yet"
    first = points[0].exam_readiness
    last = points[-1].exam_readiness
    if last > first:
        return "Readiness is improving"
    if last < first:
        return "Readiness needs attention"
    return "Readiness is steady"


def _compose_journey_story(
    snap: HomeSnapshot,
    *,
    journey: JourneySnapshot | None,
    history: HistorySnapshot | None,
) -> str:
    """Project one journey story from existing XP snapshots — no new reasoning."""
    parts: list[str] = []
    if history and history.completed_sessions:
        latest = history.completed_sessions[0]
        topic = (latest.topic_title or "a study session").strip()
        parts.append(f"You recently completed {topic}.")
    if history and len(history.readiness_progression) >= 2:
        trend = _readiness_trend_label(history.readiness_progression)
        if trend:
            parts.append(trend + ".")
    if journey and journey.current_topic:
        parts.append(f"You are now focused on {journey.current_topic.title}.")
    elif snap.recommendation_title:
        parts.append(f"Today's focus is {snap.recommendation_title}.")
    if not parts:
        return "Your learning story will appear here as you complete sessions."
    return " ".join(parts[:3])


def _compose_coach_trust(snap: HomeSnapshot) -> CoachTrustViewModel:
    """Structured Coach trust summary from authored Home fields (EP-008.1)."""
    explanation = snap.explanation
    if explanation is None:
        return CoachTrustViewModel()
    why = (explanation.why_recommended or "").strip()
    why_now = (explanation.timeliness_line or "").strip()
    next_action = (explanation.suggested_next_action or "").strip()
    benefit = (explanation.expected_benefit or "").strip()
    is_refusal = bool(explanation.honest_refusal)
    has_content = bool(why or why_now or next_action or benefit)
    return CoachTrustViewModel(
        why=why,
        why_now=why_now,
        next=next_action,
        benefit=benefit,
        is_refusal=is_refusal,
        has_content=has_content,
    )


def _compose_coach_insight(
    snap: HomeSnapshot,
    *,
    coach_trust: CoachTrustViewModel | None = None,
) -> str:
    """Level-1 coach insight from authored MES — structured trust when complete.

    EP-006.2 MES-04: when evidence / review_point / next action exist for
    progressive disclosure, keep authored sentences intact.
    EP-008.1: prefer Why / Why now / Next / Benefit composition glue only.
    """
    trust = coach_trust or _compose_coach_trust(snap)
    if trust.has_content:
        lines: list[str] = []
        if trust.why:
            lines.append(f"Why: {trust.why}")
        if trust.why_now:
            lines.append(f"Why now: {trust.why_now}")
        if trust.next:
            lines.append(f"Next: {trust.next}")
        if trust.benefit and not trust.is_refusal:
            lines.append(f"Benefit: {trust.benefit}")
        elif trust.benefit and trust.is_refusal:
            lines.append(f"Benefit: {trust.benefit}")
        text = " ".join(lines)
        if text:
            return " ".join(text.split()).strip()

    explanation = snap.explanation
    if explanation is None:
        if snap.recommendation_summary:
            return _clip_sentences(snap.recommendation_summary, 3)
        return "Guidance will appear after your next study Session."

    has_disclosure = bool(
        explanation.evidence_points
        or explanation.review_point
        or explanation.confidence_basis
        or explanation.suggested_next_action
    )
    chunks = [
        explanation.summary,
        explanation.why_recommended,
    ]
    if explanation.suggested_next_action:
        chunks.append(explanation.suggested_next_action)
    elif not has_disclosure and explanation.expected_benefit:
        chunks.append(explanation.expected_benefit)
    text = " ".join(chunk.strip() for chunk in chunks if chunk and chunk.strip())
    if not text:
        return "Guidance will appear after your next study Session."
    if has_disclosure:
        return " ".join(text.split()).strip()
    return _clip_sentences(text, 3)


def _home_readiness_why(snap: HomeSnapshot) -> str:
    """L1 readiness why — prefer authored readiness MES over recommendation cues."""
    readiness = snap.readiness_explanation
    if readiness and readiness.why_this_estimate.strip():
        return readiness.why_this_estimate.strip()
    if snap.explanation and snap.explanation.confidence_basis:
        return snap.explanation.confidence_basis.strip()
    return ""


def _home_readiness_confidence(snap: HomeSnapshot) -> str:
    readiness = snap.readiness_explanation
    if readiness and readiness.confidence_label.strip():
        return readiness.confidence_label.strip()
    if snap.explanation and snap.explanation.confidence_label:
        return snap.explanation.confidence_label.strip()
    return ""


def _home_readiness_confidence_basis(snap: HomeSnapshot) -> str:
    readiness = snap.readiness_explanation
    if readiness and readiness.confidence_basis.strip():
        return readiness.confidence_basis.strip()
    if snap.explanation and snap.explanation.confidence_basis:
        return snap.explanation.confidence_basis.strip()
    return ""


def _home_readiness_next_action(snap: HomeSnapshot) -> str:
    """Readiness-panel next only when it does not compete with the hero.

    CQ-002 / CR1: Home must present one primary “Next”. When the Mission hero
    already carries ``explanation.suggested_next_action``, suppress the
    Readiness panel next (including the old fallback that duplicated it).
    """
    hero_next = ""
    if snap.explanation and snap.explanation.suggested_next_action:
        hero_next = snap.explanation.suggested_next_action.strip()
    if hero_next:
        return ""
    readiness = snap.readiness_explanation
    if readiness and readiness.suggested_next_action.strip():
        return readiness.suggested_next_action.strip()
    return ""


def _home_readiness_review_point(snap: HomeSnapshot) -> str:
    readiness = snap.readiness_explanation
    if readiness and readiness.review_point.strip():
        return readiness.review_point.strip()
    if snap.explanation and snap.explanation.review_point:
        return snap.explanation.review_point.strip()
    return ""


def _home_readiness_drivers(snap: HomeSnapshot) -> tuple[str, ...]:
    readiness = snap.readiness_explanation
    if readiness and readiness.readiness_drivers:
        return tuple(readiness.readiness_drivers[:4])
    return ()


def _home_readiness_evidence(snap: HomeSnapshot) -> tuple[str, ...]:
    readiness = snap.readiness_explanation
    if readiness and readiness.supporting_evidence:
        return tuple(readiness.supporting_evidence[:5])
    if snap.explanation and snap.explanation.evidence_points:
        return tuple(snap.explanation.evidence_points[:5])
    return ()


def _home_readiness_expected_benefit(snap: HomeSnapshot) -> str:
    readiness = snap.readiness_explanation
    if readiness and readiness.expected_benefit.strip():
        return readiness.expected_benefit.strip()
    if snap.explanation and snap.explanation.expected_benefit:
        return snap.explanation.expected_benefit.strip()
    return ""


def _home_readiness_has_disclosure(snap: HomeSnapshot) -> bool:
    readiness = snap.readiness_explanation
    if readiness and (
        readiness.readiness_drivers
        or readiness.supporting_evidence
        or readiness.review_point
        or readiness.confidence_basis
        or readiness.confidence_label
    ):
        return True
    return bool(
        snap.explanation
        and (
            snap.explanation.evidence_points
            or snap.explanation.review_point
            or snap.explanation.confidence_basis
        )
    )


def _compose_milestones(
    *,
    journey: JourneySnapshot | None,
    revision: RevisionSnapshot | None,
) -> tuple[HomeMilestoneViewModel, ...]:
    milestones: list[HomeMilestoneViewModel] = []
    if journey and journey.upcoming_topics:
        topic = journey.upcoming_topics[0]
        milestones.append(
            HomeMilestoneViewModel(
                title=topic.title,
                detail=topic.status_label or "Upcoming topic",
            )
        )
    if revision and revision.primary is not None:
        milestones.append(
            HomeMilestoneViewModel(
                title=revision.primary.topic_title or "Revision",
                detail=revision.primary.expected_benefit
                or revision.primary.priority_label
                or "Revision focus",
            )
        )
    if journey and journey.estimated_completion_label:
        milestones.append(
            HomeMilestoneViewModel(
                title="Estimated completion",
                detail=journey.estimated_completion_label,
            )
        )
    return tuple(milestones[:3])


def _is_resume_cta_label(label: str | None) -> bool:
    """True when the Start Session action is a return-to-study Continue/Resume."""
    text = (label or "").casefold()
    return "continue" in text or "resume" in text


def _compose_quick_actions(
    snap: HomeSnapshot,
    *,
    revision: RevisionSnapshot | None,
    cta_enabled: bool,
) -> tuple[HomeQuickActionViewModel, ...]:
    actions: list[HomeQuickActionViewModel] = []
    if cta_enabled:
        start = snap.start_session
        resume = bool(
            start and start.session_id and _is_resume_cta_label(start.label)
        )
        # CQ-003 / CR2: deep-link to open session when returning mid-study.
        href = (
            f"/session/{start.session_id}/overview"
            if resume and start and start.session_id
            else "/student/"
        )
        actions.append(
            HomeQuickActionViewModel(
                label=(
                    start.label
                    if start and start.label
                    else ("Continue" if resume else "Resume Mission")
                ),
                href=href,
                detail=(
                    "Pick up where you left off"
                    if resume
                    else "Continue today's mission"
                ),
            )
        )
    actions.append(
        HomeQuickActionViewModel(
            label="Open History",
            href="/student/history",
            detail="Practice archives and progress context",
        )
    )
    if revision and revision.has_revision:
        actions.append(
            HomeQuickActionViewModel(
                label="Open Revision",
                href="/student/revision",
                detail="Supports today's Mission",
            )
        )
    actions.append(
        HomeQuickActionViewModel(
            label="Open Journey",
            href="/student/journey",
            detail="See what comes next",
        )
    )
    return tuple(actions[:4])


def _clip_sentences(text: str, maximum: int) -> str:
    cleaned = " ".join(text.split()).strip()
    if not cleaned or maximum < 1:
        return cleaned
    sentences: list[str] = []
    remainder = cleaned
    while remainder and len(sentences) < maximum:
        cut = -1
        for separator in (". ", "! ", "? "):
            index = remainder.find(separator)
            if index != -1 and (cut == -1 or index < cut):
                cut = index + 1
        if cut == -1:
            sentences.append(remainder.strip())
            break
        sentences.append(remainder[:cut].strip())
        remainder = remainder[cut:].lstrip()
    return " ".join(sentences)

"""Exam Week Briefing — presentation projector for Student Home (KWP-006).

Aggregates existing History, Journey, Revision, readiness, and streak signals
into a calm weekly briefing. No Progress / Twin / Evidence / Mission redesign.
Never reproduces CMP question text — topic titles and syllabus refs only.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HomePageViewModel,
    JourneyPageViewModel,
    ProfilePageViewModel,
    RevisionPageViewModel,
)

# Stage language preferred over percentages (KWP-006 readiness policy).
_READINESS_STAGES: tuple[tuple[float, str], ...] = (
    (0.20, "Building"),
    (0.40, "Developing"),
    (0.60, "Strengthening"),
    (0.80, "Ready for Revision"),
    (1.01, "Ready for Assessment"),
)


@dataclass(frozen=True)
class ExamWeekBriefingViewModel:
    """Student-facing weekly briefing — empty when insufficient signal."""

    has_briefing: bool = False
    title: str = "This Week"
    strengthened: tuple[str, ...] = ()
    needs_reinforcement: tuple[str, ...] = ()
    consistency_label: str = ""
    recommended_focus: str = ""
    recommended_detail: str = ""
    readiness_stage: str = ""
    summary_line: str = ""


@dataclass(frozen=True)
class HomeInsightCard:
    """One calm Home insight — answers a daily command-centre question."""

    kind: str  # position | changed | weak | achievement | next | milestone
    label: str
    body: str


def readiness_stage_label(
    value: float | None,
    *,
    existing_label: str = "",
) -> str:
    """Map a readiness ratio to calm stage language.

    Prefer an existing non-percent authored label when it already uses stage
    vocabulary; otherwise derive from the numeric value.
    """
    existing = (existing_label or "").strip()
    if existing and "%" not in existing:
        lowered = existing.lower()
        # Ignore generic product nouns — they are not stage claims.
        if lowered not in {"exam readiness", "readiness", "on track"}:
            stage_phrases = (
                "building",
                "developing",
                "strengthening",
                "ready for revision",
                "ready for assessment",
            )
            if any(phrase in lowered for phrase in stage_phrases):
                return existing

    if value is None:
        return "Building"

    ratio = float(value)
    if ratio > 1.0:
        ratio = ratio / 100.0
    ratio = max(0.0, min(ratio, 1.0))
    for threshold, label in _READINESS_STAGES:
        if ratio < threshold:
            return label
    return "Ready for Assessment"


def format_readiness_stage_display(
    value: float | None,
    *,
    existing_label: str = "",
    percent_fallback: str = "",
) -> tuple[str, str]:
    """Return (stage_label, secondary_detail).

    Stage is primary. Percent is optional secondary detail only — never the
    hero claim when a stage can be shown.
    """
    stage = readiness_stage_label(value, existing_label=existing_label)
    detail = ""
    # Keep percent as quiet secondary only when stage is derived from number.
    if value is not None and (percent_fallback or "").strip():
        if "%" in (existing_label or "") or not (existing_label or "").strip():
            detail = percent_fallback.strip()
    return stage, detail


def build_exam_week_briefing(
    *,
    home: HomePageViewModel | None,
    history: HistoryPageViewModel | None = None,
    journey: JourneyPageViewModel | None = None,
    revision: RevisionPageViewModel | None = None,
    profile: ProfilePageViewModel | None = None,
) -> ExamWeekBriefingViewModel:
    """Project a weekly briefing from existing experience VMs."""
    strengthened = _strengthened_topics(history=history)
    needs = _needs_reinforcement(revision=revision, history=history, journey=journey)
    consistency = _consistency_label(profile=profile, history=history)
    focus, focus_detail = _recommended_focus(
        home=home,
        revision=revision,
        journey=journey,
    )
    stage = ""
    if home and home.readiness and home.readiness.has_readiness:
        stage = (
            home.readiness.readiness_label
            or readiness_stage_label(None, existing_label="")
        ).strip()
        # Prefer stage vocabulary even if VM still carries a percent primary.
        if "%" in stage or stage.lower() in {"exam readiness", ""}:
            raw_pct = home.readiness.readiness_percent_label or ""
            numeric = _parse_percent(raw_pct)
            stage = readiness_stage_label(numeric, existing_label="")

    has_signal = bool(
        strengthened or needs or consistency or focus or stage
    )
    if not has_signal:
        return ExamWeekBriefingViewModel()

    summary_parts: list[str] = []
    if strengthened:
        summary_parts.append(
            f"Strengthened {', '.join(strengthened[:2])}."
        )
    if needs:
        summary_parts.append(f"Reinforce {needs[0]}.")
    if focus:
        summary_parts.append(f"Focus: {focus}.")

    return ExamWeekBriefingViewModel(
        has_briefing=True,
        title="This Week",
        strengthened=strengthened[:4],
        needs_reinforcement=needs[:4],
        consistency_label=consistency,
        recommended_focus=focus,
        recommended_detail=focus_detail,
        readiness_stage=stage,
        summary_line=" ".join(summary_parts)[:220],
    )


def build_home_insights(
    *,
    home: HomePageViewModel | None,
    history: HistoryPageViewModel | None = None,
    journey: JourneyPageViewModel | None = None,
    revision: RevisionPageViewModel | None = None,
    briefing: ExamWeekBriefingViewModel | None = None,
    forecast_guidance: str = "",
    forecast_title: str = "",
) -> tuple[HomeInsightCard, ...]:
    """Compact insight cards answering the daily command-centre questions."""
    cards: list[HomeInsightCard] = []

    position = _position_line(home=home, journey=journey)
    if position:
        cards.append(
            HomeInsightCard(
                kind="position",
                label="Where you are",
                body=position,
            )
        )

    # KWP-012 — trajectory insight (where you are heading).
    guidance = (forecast_guidance or "").strip()
    if guidance:
        label = (forecast_title or "Study Trajectory").strip() or "Study Trajectory"
        cards.append(
            HomeInsightCard(
                kind="trajectory",
                label=label,
                body=guidance[:180],
            )
        )

    changed = _changed_line(home=home, history=history)
    if changed:
        cards.append(
            HomeInsightCard(
                kind="changed",
                label="Since last Session",
                body=changed,
            )
        )

    if briefing and briefing.needs_reinforcement:
        cards.append(
            HomeInsightCard(
                kind="weak",
                label="Needs attention",
                body=", ".join(briefing.needs_reinforcement[:3]),
            )
        )
    elif revision and revision.has_revision and revision.primary:
        title = (revision.primary.topic_title or "").strip()
        if title:
            cards.append(
                HomeInsightCard(
                    kind="weak",
                    label="Needs attention",
                    body=title,
                )
            )

    achievement = _achievement_line(history=history)
    if achievement:
        cards.append(
            HomeInsightCard(
                kind="achievement",
                label="Recent achievement",
                body=achievement,
            )
        )

    next_action = _next_action_line(home=home, revision=revision, journey=journey)
    if next_action:
        cards.append(
            HomeInsightCard(
                kind="next",
                label="Recommended next",
                body=next_action,
            )
        )

    milestone = _milestone_line(home=home, journey=journey)
    if milestone:
        cards.append(
            HomeInsightCard(
                kind="milestone",
                label="Upcoming",
                body=milestone,
            )
        )

    return tuple(cards[:5])


def _strengthened_topics(
    *,
    history: HistoryPageViewModel | None,
) -> tuple[str, ...]:
    if history is None:
        return ()
    topics: list[str] = []
    seen: set[str] = set()
    for title in history.mastered_topics or ():
        clean = str(title).strip()
        key = clean.lower()
        if not clean or key in seen:
            continue
        seen.add(key)
        topics.append(clean)
    if not topics and history.sessions:
        for session in history.sessions[:3]:
            clean = (session.topic_title or "").strip()
            key = clean.lower()
            if not clean or key in seen:
                continue
            seen.add(key)
            topics.append(clean)
    return tuple(topics[:4])


def _needs_reinforcement(
    *,
    revision: RevisionPageViewModel | None,
    history: HistoryPageViewModel | None,
    journey: JourneyPageViewModel | None,
) -> tuple[str, ...]:
    items: list[str] = []
    seen: set[str] = set()

    def _add(title: str) -> None:
        clean = (title or "").strip()
        key = clean.lower()
        if not clean or key in seen:
            return
        seen.add(key)
        items.append(clean)

    if journey and journey.needs_attention:
        for topic in journey.needs_attention[:4]:
            _add(topic.title)
    if revision and revision.has_revision:
        if revision.primary:
            _add(revision.primary.topic_title)
        for alt in revision.alternatives[:3]:
            _add(alt.topic_title)
    if history:
        for title in history.revision_history[:4]:
            _add(str(title))
    return tuple(items[:4])


def _consistency_label(
    *,
    profile: ProfilePageViewModel | None,
    history: HistoryPageViewModel | None,
) -> str:
    streak_raw = ""
    if profile and (profile.streak_label or "").strip():
        streak_raw = profile.streak_label.strip().lower()
    days = _parse_streak_days(streak_raw)
    session_count = history.session_count if history else 0

    if days >= 5 or session_count >= 5:
        return "Excellent"
    if days >= 3 or session_count >= 3:
        return "Steady"
    if days >= 1 or session_count >= 1:
        return "Building"
    if history and history.sessions:
        return "Building"
    return ""


def _recommended_focus(
    *,
    home: HomePageViewModel | None,
    revision: RevisionPageViewModel | None,
    journey: JourneyPageViewModel | None,
) -> tuple[str, str]:
    """Topic + optional syllabus position detail — never CMP content.

    KWP-007: when Revision signals a weak topic, enrich detail with a
    Learning Strategy WHY (deterministic, student-safe).
    """
    if revision and revision.has_revision and revision.primary:
        title = (revision.primary.topic_title or "").strip()
        detail = (revision.primary.expected_benefit or "").strip()[:120]
        if title:
            strategy_detail = _strategy_focus_detail(title)
            if strategy_detail:
                detail = strategy_detail
            return title, detail

    if journey and journey.current:
        title = (journey.current.title or "").strip()
        detail = ""
        if journey.up_next and journey.up_next.title:
            detail = f"Then: {journey.up_next.title}"
        if title:
            return title, detail

    if home:
        edu = home.educational
        if edu and getattr(edu, "active", False):
            title = (edu.today_topic_title or edu.mission_title or "").strip()
            detail_parts = [
                p
                for p in (
                    (edu.section_title or "").strip(),
                    (edu.position_label or "").strip(),
                )
                if p
            ]
            if title:
                return title, " · ".join(detail_parts)
        if home.recommendation and home.recommendation.title:
            return home.recommendation.title.strip(), ""
        if home.primary_mission_title:
            return home.primary_mission_title.strip(), ""
    return "", ""


def _strategy_focus_detail(topic_title: str) -> str:
    """Project a calm cause WHY for weekly focus from Revision weakness.

    Uses Learning Diagnostics (KWP-008) for cause-level WHY, with Learning
    Strategy explanation as fallback.
    """
    from app.application.learning_diagnostics import (
        DiagnosticEvidenceInput,
        get_learning_diagnostics_engine,
    )
    from app.application.learning_strategy import (
        StrategyEvidenceInput,
        get_learning_strategy_engine,
    )

    diagnostic = get_learning_diagnostics_engine().evaluate(
        DiagnosticEvidenceInput(
            topic_title=topic_title,
            practice_incorrect=2,
            practice_attempted=2,
            weak_topic=True,
            retention_risk=True,
        )
    )
    why = (diagnostic.explanation or "").strip()
    if not why:
        advice = get_learning_strategy_engine().evaluate(
            StrategyEvidenceInput(
                topic_title=topic_title,
                practice_incorrect=2,
                practice_attempted=2,
                weak_topic=True,
                retention_risk=True,
            )
        )
        why = (advice.explanation or "").strip()
    if not why:
        return ""
    return why[:160]


def _position_line(
    *,
    home: HomePageViewModel | None,
    journey: JourneyPageViewModel | None,
) -> str:
    if journey and journey.current and journey.current.title:
        parts = [f"Current topic: {journey.current.title}"]
        if journey.progress_label:
            # Prefer narrative over raw % when possible.
            label = journey.progress_label
            if "%" in label and journey.estimated_completion_label:
                parts.append(journey.estimated_completion_label)
            else:
                parts.append(label)
        return " · ".join(parts)
    if home and home.educational and getattr(home.educational, "active", False):
        edu = home.educational
        topic = (edu.today_topic_title or "").strip()
        section = (edu.section_title or "").strip()
        position = (edu.position_label or "").strip()
        bits = [b for b in (topic, section, position) if b]
        if bits:
            return " · ".join(bits)
    if home and home.journey_story:
        story = home.journey_story.strip()
        if story and "will appear here" not in story.lower():
            return story
    return ""


def _changed_line(
    *,
    home: HomePageViewModel | None,
    history: HistoryPageViewModel | None,
) -> str:
    if home and (home.completion_loop_echo or "").strip():
        return home.completion_loop_echo.strip()[:160]
    if history and history.sessions:
        latest = history.sessions[0]
        topic = (latest.topic_title or "a Session").strip()
        when = (latest.completed_at or "").strip()
        if when:
            return f"You completed {topic} ({when})."
        return f"You completed {topic}."
    if home and home.journey_story:
        story = home.journey_story.strip()
        if story and "will appear here" not in story.lower():
            return story[:160]
    return ""


def _achievement_line(*, history: HistoryPageViewModel | None) -> str:
    if history is None:
        return ""
    if history.achievements:
        a = history.achievements[0]
        title = (getattr(a, "title", "") or "").strip()
        if title:
            desc = (getattr(a, "description", "") or "").strip()
            return f"{title}." if not desc else f"{title}–{desc}"[:140]
    if history.mastered_topics:
        sample = ", ".join(history.mastered_topics[:2])
        return f"Strengthened {sample}."
    return ""


def _next_action_line(
    *,
    home: HomePageViewModel | None,
    revision: RevisionPageViewModel | None,
    journey: JourneyPageViewModel | None,
) -> str:
    if home and home.explanation and home.explanation.suggested_next_action:
        return home.explanation.suggested_next_action.strip()[:140]
    if home and home.readiness and home.readiness.suggested_next_action:
        return home.readiness.suggested_next_action.strip()[:140]
    if home and (home.expected_outcome or "").strip():
        return home.expected_outcome.strip()[:140]
    focus, detail = _recommended_focus(
        home=home, revision=revision, journey=journey
    )
    if focus:
        return f"Study {focus}." if not detail else f"Study {focus}–{detail}"
    return ""


def _milestone_line(
    *,
    home: HomePageViewModel | None,
    journey: JourneyPageViewModel | None,
) -> str:
    if home and home.milestones:
        m = home.milestones[0]
        title = (m.title or "").strip()
        detail = (m.detail or "").strip()
        if title and detail:
            return f"{title} · {detail}"
        return title
    if home and home.countdown and home.countdown.has_countdown:
        label = home.countdown.label or ""
        exam = home.countdown.examination_label or home.examination_label or "Exam"
        if label:
            return f"{exam} · {label}"
    if journey and journey.up_next and journey.up_next.title:
        return f"Next on Journey: {journey.up_next.title}"
    if journey and journey.estimated_completion_label:
        return journey.estimated_completion_label
    return ""


def _parse_percent(label: str) -> float | None:
    text = (label or "").strip().rstrip("%")
    if not text:
        return None
    try:
        value = float(text)
    except ValueError:
        return None
    if value > 1.0:
        return value / 100.0
    return value


def _parse_streak_days(label: str) -> int:
    text = (label or "").strip().lower()
    if not text or text in {"0 days", "no streak yet", "0 day streak"}:
        return 0
    digits = "".join(ch for ch in text if ch.isdigit())
    if not digits:
        return 0
    try:
        return int(digits)
    except ValueError:
        return 0

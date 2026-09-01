"""Adaptive Study Workspace composer (KWP-013).

Presentation-only composition of Mission, Readiness, Forecast, Learning
Journey, Recent Progress, Current Focus, and Today's Session into one
coherent student workspace.

Does not redesign Learning Runtime, Evidence, Progress, Strategy,
Diagnostics, Difficulty, Intervention Effectiveness, Educational Memory,
Forecast engines, or Mission Runtime. Consumes existing outputs only.
"""

from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from flask import has_request_context, url_for

from app.presentation.student.dto.adaptive_workspace import (
    AdaptiveStudyWorkspace,
    WorkspaceCurrentFocus,
    WorkspaceExtraStudyOffer,
    WorkspaceForecastSummary,
    WorkspaceJourneyHighlights,
    WorkspaceLearningEpisode,
    WorkspaceMissionComposition,
    WorkspaceMorningBrief,
    WorkspaceProgressNarrative,
    WorkspaceQuickAction,
    WorkspaceSessionPlan,
    WorkspaceTomorrowPreview,
)
from app.presentation.student.dto.student_home import (
    HomeMission,
    HomeStudyHealth,
    HomeStudySignals,
    StudentHomePage,
)
from app.presentation.student.view_models import (
    HistoryPageViewModel,
    HomePageViewModel,
    RevisionPageViewModel,
    StudentPageViewModel,
)

logger = logging.getLogger(__name__)

_FORBIDDEN: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "evidence authority",
    "evidence package",
    "practice evidence",
    "educational evidence",
    "building evidence",
    "cognitive load",
    "mental load",
    "burnout",
    "overloaded",
    "pass probability",
    "guaranteed",
    "will definitely",
    "badge",
    "leaderboard",
)


def compose_adaptive_workspace(
    page: StudentPageViewModel | None,
    home: StudentHomePage,
    *,
    now: datetime | None = None,
) -> AdaptiveStudyWorkspace:
    """Project Adaptive Study Workspace sections from existing Home + EI."""
    if home.state == "empty" or page is None or page.home is None:
        return AdaptiveStudyWorkspace(
            enabled=False,
            page_question=home.page_question,
        )

    home_vm = page.home
    history = page.history
    revision = page.revision
    clock = now or datetime.now(UTC)

    store, student_id = _store_and_student()
    narrative = _journey_narrative(store=store, student_id=student_id)
    forecast_dto = _readiness_forecast(
        store=store,
        student_id=student_id,
        home_vm=home_vm,
    )

    morning = _morning_brief(
        home=home,
        home_vm=home_vm,
        history=history,
        narrative=narrative,
        clock=clock,
    )
    mission_composition = _mission_composition(
        home=home,
        home_vm=home_vm,
        revision=revision,
        store=store,
        student_id=student_id,
    )
    session_plan = _session_plan(
        home.mission,
        composition=mission_composition,
    )
    focus = _current_focus(
        home=home,
        home_vm=home_vm,
        revision=revision,
        store=store,
        student_id=student_id,
    )
    progress = _progress_narrative(
        home=home,
        history=history,
        narrative=narrative,
    )
    forecast = _forecast_summary(forecast_dto)
    journey = _journey_highlights(narrative)
    actions = _quick_actions(
        home=home,
        home_vm=home_vm,
        history=history,
        revision=revision,
        has_journey=bool(journey and journey.has_highlights),
        has_forecast=bool(forecast and forecast.has_forecast),
        composition=mission_composition,
    )

    return AdaptiveStudyWorkspace(
        morning_brief=morning,
        session_plan=session_plan,
        current_focus=focus,
        progress_narrative=progress,
        forecast=forecast,
        journey_highlights=journey,
        mission_composition=mission_composition,
        quick_actions=actions,
        page_question=(
            "What should I do now?"
        ),
        enabled=True,
    )


def _store_and_student() -> tuple[Any, str]:
    try:
        from flask_login import current_user

        from app.presentation.session.factory import (
            get_session_experience_composition,
        )

        composition = get_session_experience_composition()
        store = getattr(composition, "store", None) if composition else None
        student_id = str(getattr(current_user, "id", "") or "")
        return store, student_id
    except Exception:  # noqa: BLE001
        return None, ""


def _journey_narrative(*, store: Any, student_id: str):
    if store is None or not student_id:
        return None
    try:
        from app.application.educational_memory import (
            get_educational_memory_service,
        )

        return get_educational_memory_service().journey_for_student(
            store=store,
            student_id=student_id,
        )
    except Exception:  # noqa: BLE001
        return None


def _readiness_forecast(
    *,
    store: Any,
    student_id: str,
    home_vm: HomePageViewModel,
):
    if store is None or not student_id:
        return None
    try:
        from app.application.readiness_forecast import (
            get_readiness_forecast_engine,
        )

        days = None
        if home_vm.countdown and home_vm.countdown.has_countdown:
            days = home_vm.countdown.days
        readiness_ratio = None
        if home_vm.readiness and home_vm.readiness.has_readiness:
            raw = home_vm.readiness.readiness_percent_label or ""
            digits = "".join(ch for ch in raw if ch.isdigit() or ch == ".")
            if digits:
                readiness_ratio = float(digits)
                if readiness_ratio > 1.0:
                    readiness_ratio /= 100.0
        return get_readiness_forecast_engine().forecast_from_store(
            store,
            student_id=student_id,
            days_to_exam=days,
            current_readiness_ratio=readiness_ratio,
        )
    except Exception:  # noqa: BLE001
        return None


def _morning_brief(
    *,
    home: StudentHomePage,
    home_vm: HomePageViewModel,
    history: HistoryPageViewModel | None,
    narrative,
    clock: datetime,
) -> WorkspaceMorningBrief | None:
    greeting = _greeting(clock)
    momentum = _momentum_line(home.study_health, narrative)
    yesterday = _yesterday_line(history=history, narrative=narrative)
    today = _today_line(home.mission, home_vm=home_vm)
    duration = ""
    if home.mission and home.mission.duration_label:
        duration = home.mission.duration_label.strip()
    elif home.signals and home.signals.estimated_study_label:
        duration = home.signals.estimated_study_label.strip()
    elif home_vm.estimated_duration_label or home_vm.estimated_study_label:
        duration = (
            home_vm.estimated_duration_label or home_vm.estimated_study_label or ""
        ).strip()

    # Fold Exam Week Briefing reinforcement into the morning narrative when
    # present — avoids a second independent briefing card (KWP-013).
    if (
        not yesterday
        and home.briefing
        and home.briefing.needs_reinforcement
    ):
        topic = home.briefing.needs_reinforcement[0]
        yesterday = f"Needs reinforcement: {topic}."
    elif (
        home.briefing
        and home.briefing.strengthened
        and not yesterday
    ):
        topic = home.briefing.strengthened[0]
        yesterday = f"This week you strengthened {topic}."

    has_brief = bool(greeting or momentum or yesterday or today or duration)
    if not has_brief:
        return None
    return WorkspaceMorningBrief(
        greeting=greeting,
        momentum_line=_scrub(momentum),
        yesterday_line=_scrub(yesterday),
        today_line=_scrub(today),
        estimated_study_label=duration,
        has_brief=True,
    )


def _greeting(clock: datetime) -> str:
    hour = clock.hour
    if hour < 12:
        return "Good morning."
    if hour < 17:
        return "Good afternoon."
    return "Good evening."


def _momentum_line(
    health: HomeStudyHealth | None,
    narrative,
) -> str:
    if narrative is not None and getattr(narrative, "has_memory", False):
        patterns = getattr(narrative, "patterns", ()) or ()
        for pattern in patterns:
            title = (getattr(pattern, "title", "") or "").strip().lower()
            body = (getattr(pattern, "narrative", "") or "").strip()
            if "consistenc" in title and body:
                return "You are maintaining steady progress."
            if "recover" in title:
                return "You are recovering well from earlier difficulties."
            if "independen" in title:
                return "Your independence in study is growing."
        paragraphs = getattr(narrative, "story_paragraphs", ()) or ()
        if paragraphs:
            first = str(paragraphs[0]).strip()
            if first:
                # Prefer a short momentum claim, not the full story.
                if "recover" in first.lower():
                    return "You are recovering and rebuilding understanding."
                if "consist" in first.lower() or "steady" in first.lower():
                    return "You are maintaining steady progress."
                return "Your recent sittings show meaningful educational growth."

    if health is None:
        return "Your study path is ready when you are."
    tone = (health.tone or "neutral").strip().lower()
    status = (health.status_label or "").strip()
    if tone == "positive":
        return "You are maintaining steady progress."
    if tone == "caution":
        return "A steadier rhythm will strengthen today's session."
    if status:
        if "%" in status:
            return "You are building exam readiness step by step."
        return f"You are currently {status.lower()}."
    return "You are building exam readiness step by step."


def _yesterday_line(
    *,
    history: HistoryPageViewModel | None,
    narrative,
) -> str:
    topic = ""
    if history and history.sessions:
        latest = history.sessions[0]
        topic = (latest.topic_title or "").strip()
    if not topic and narrative is not None:
        archives = getattr(narrative, "sitting_archives", ()) or ()
        if archives:
            topic = str(archives[0].get("topic_title") or "").strip()
    if not topic:
        return ""
    # Prefer Educational Memory recovery / improvement language when present.
    if narrative is not None:
        for entry in getattr(narrative, "timeline", ()) or ():
            kind = getattr(getattr(entry, "kind", None), "value", "") or ""
            entry_topic = (getattr(entry, "topic_title", "") or "").strip()
            if entry_topic and entry_topic.lower() != topic.lower():
                continue
            if kind in {
                "understanding_improved",
                "recovered",
                "repeated_reinforcement",
                "consolidated",
            }:
                verb = {
                    "understanding_improved": "improved your understanding of",
                    "recovered": "helped you recover",
                    "repeated_reinforcement": "reinforced",
                    "consolidated": "consolidated",
                }.get(kind, "strengthened")
                return f"Yesterday's reinforcement {verb} {topic}."
    return f"Yesterday's session strengthened {topic}."


def _today_line(
    mission: HomeMission | None,
    *,
    home_vm: HomePageViewModel,
) -> str:
    if home_vm.day_complete:
        return "Today's session is complete. Return tomorrow to continue."
    if mission is None:
        return "Today's session will appear when your focus is ready."
    if mission.primary_kind == "link":
        return "Continue your open session to keep today's momentum."
    title = (mission.title or mission.objective or "").strip()
    if title:
        return f"Today's session continues that momentum with {title}."
    return "Today's session continues that momentum."


def _mission_composition(
    *,
    home: StudentHomePage,
    home_vm: HomePageViewModel,
    revision: RevisionPageViewModel | None,
    store: Any,
    student_id: str,
) -> WorkspaceMissionComposition | None:
    """Compose Learning Episodes via Educational Authoring (KWP-015).

    Presentation consumption only — does not modify Mission Runtime or EI.
    """
    topic = ""
    if home.mission and (home.mission.title or home.mission.objective):
        topic = (home.mission.title or home.mission.objective or "").strip()
    if not topic and home.briefing and home.briefing.recommended_focus:
        topic = home.briefing.recommended_focus.strip()
    if not topic:
        return None

    try:
        from app.application.educational_authoring import (
            EducationalAuthoringEngine,
            get_educational_authoring_engine,
        )
        from app.application.knowledge_architecture.graph_adapter import (
            graph_from_learner_package,
        )

        subject_code = ""
        topic_id = ""
        topic_code = ""
        objective_text = ""
        tomorrow_title = ""
        tomorrow_id = ""
        edu = getattr(home_vm, "educational", None)
        if edu and getattr(edu, "active", False):
            subject_code = (getattr(edu, "subject_code", "") or "").strip()
            topic_code = (getattr(edu, "today_topic_code", "") or "").strip()
            objs = getattr(edu, "learning_objectives", ()) or ()
            if objs:
                objective_text = str(objs[0] or "").strip()
            # Prefer explicit unlocks_next title fragment when it is a short label.
            unlocks = (getattr(edu, "unlocks_next", "") or "").strip()
            if unlocks and len(unlocks) <= 80 and "\n" not in unlocks:
                tomorrow_title = unlocks

        # Journey page may carry the next syllabus topic for Tomorrow Preview.
        journey_vm = getattr(home_vm, "journey", None)
        if journey_vm is None:
            # Some Home VMs nest journey under page; soft-read common attrs.
            journey_vm = getattr(home_vm, "journey_page", None)
        up_next = getattr(journey_vm, "up_next", None) if journey_vm else None
        if up_next is None and journey_vm is not None:
            upcoming = getattr(journey_vm, "upcoming", ()) or ()
            up_next = upcoming[0] if upcoming else None
        if up_next is not None:
            tomorrow_title = tomorrow_title or (
                getattr(up_next, "topic_title", "") or ""
            ).strip()
            tomorrow_id = (getattr(up_next, "topic_id", "") or "").strip()

        if home.mission and home.mission.learning_objective:
            objective_text = objective_text or home.mission.learning_objective

        package = None
        if subject_code:
            try:
                from app.application.curriculum_intelligence import (
                    certified_learning_service as cls,
                )

                package = cls.CertifiedLearningService().load_package(subject_code)
            except Exception:  # noqa: BLE001
                package = None

        graph = graph_from_learner_package(package) if package else None
        engine: EducationalAuthoringEngine
        if graph is not None and graph.topic_count() > 0:
            engine = EducationalAuthoringEngine(graph)
        else:
            engine = get_educational_authoring_engine()

        weak = bool(
            revision
            and revision.has_revision
            and revision.primary
            and (revision.primary.topic_title or "").strip().lower()
            == topic.lower()
        )
        available = _available_minutes(home)
        recent = _recently_strengthened_titles(
            store=store, student_id=student_id
        )

        pack_ctx = _package_journey_context(
            student_id=student_id,
            subject_code=subject_code,
            home_vm=home_vm,
        )

        composition = engine.author_from_topic(
            topic_id=topic_id,
            topic_title=topic,
            topic_code=topic_code,
            objective_text=objective_text,
            estimated_effort_minutes=_parse_minutes(
                (home.mission.duration_label if home.mission else "") or ""
            ),
            weak_topic=weak,
            available_minutes=available,
            tomorrow_topic_id=tomorrow_id,
            tomorrow_topic_title=tomorrow_title,
            recently_strengthened_titles=recent,
            revision_available=bool(
                revision and revision.has_revision and revision.primary
            ),
            mission_instance_id=(
                (home.mission.mission_id if home.mission else "")
                or (home_vm.mission_id if hasattr(home_vm, "mission_id") else "")
                or ""
            ),
            subject_code=subject_code,
            educational_package_id=pack_ctx["educational_package_id"],
            completed_package_ids=pack_ctx["completed_package_ids"],
            last_completed_package_id=pack_ctx["last_completed_package_id"],
            prefer_completed_package=pack_ctx["prefer_completed_package"],
        )
        if not composition.has_composition:
            return _quiet_mission_composition(
                "Today's learning episode is not ready yet. "
                "Your mission focus is still available above. "
                "begin the Session when ready."
            )
        return _project_mission_composition(composition)
    except Exception:  # noqa: BLE001 — never hide failure silently (V1S-005 DF-003)
        logger.warning("mission_composition_failed", exc_info=True)
        return _quiet_mission_composition(
            "Today's learning episode could not be prepared. "
            "Your mission focus is still available above. "
            "begin the Session when ready, or return after a short break."
        )


def _package_journey_context(
    *,
    student_id: str,
    subject_code: str,
    home_vm: HomePageViewModel,
) -> dict[str, Any]:
    """Resolve approved-package journey state for Home Tomorrow Preview (RO1-R1)."""
    empty: dict[str, Any] = {
        "educational_package_id": "",
        "completed_package_ids": None,
        "last_completed_package_id": "",
        "prefer_completed_package": bool(getattr(home_vm, "day_complete", False)),
    }
    if not subject_code:
        return empty
    try:
        from app.application.educational_runtime_engine.service import (
            EducationalRuntimeEngineService,
        )
        from app.models.educational_runtime_engine import RuntimeEnrolment

        user_id = int(str(student_id).strip())
        runtime = EducationalRuntimeEngineService()
        enrolment = (
            RuntimeEnrolment.query.filter_by(
                user_id=user_id, subject_code=subject_code.upper()
            ).first()
            or RuntimeEnrolment.query.filter_by(
                user_id=user_id, subject_code=subject_code
            ).first()
        )
        if enrolment is None:
            enrolment = RuntimeEnrolment.query.filter_by(user_id=user_id).first()
        curriculum_identity = (
            str(getattr(enrolment, "curriculum_identity", "") or "")
            if enrolment is not None
            else ""
        )
        completed = runtime._completed_educational_package_ids(
            user_id=user_id,
            curriculum_identity=curriculum_identity,
        )
        last_completed = runtime._last_completed_educational_package_id(
            user_id=user_id,
            curriculum_identity=curriculum_identity,
        )
        pack_id = ""
        mid = (getattr(home_vm, "mission_id", "") or "").strip()
        if mid and not getattr(home_vm, "day_complete", False):
            pack_id = runtime._educational_package_id_for_mission(mid)
        prefer_completed = bool(getattr(home_vm, "day_complete", False))
        if prefer_completed and last_completed:
            pack_id = last_completed
        return {
            "educational_package_id": pack_id,
            "completed_package_ids": completed,
            "last_completed_package_id": last_completed,
            "prefer_completed_package": prefer_completed,
        }
    except Exception:  # noqa: BLE001 — Home chrome must stay resilient
        logger.debug("package_journey_context_unavailable", exc_info=True)
        return empty


def _quiet_mission_composition(reason: str) -> WorkspaceMissionComposition:
    """Calm educational quiet state when authoring cannot compose (DF-003)."""
    return WorkspaceMissionComposition(
        has_composition=False,
        composition_quiet_reason=_scrub(reason) or reason,
    )


def _project_mission_composition(composition) -> WorkspaceMissionComposition:
    episodes = tuple(
        WorkspaceLearningEpisode(
            educational_context=_scrub(ep.educational_context),
            learning_objective=_scrub(ep.learning_objective),
            concept_focus=tuple(_scrub(c) for c in ep.concept_focus if c),
            activity_labels=tuple(
                a.title for a in ep.activities if a and a.title
            ),
            success_criteria=tuple(
                _scrub(c) for c in ep.success_criteria if c
            ),
            estimated_duration_label=ep.estimated_duration_label,
            connection=_scrub(ep.connection),
            sequence=ep.sequence,
            has_episode=ep.has_episode,
        )
        for ep in composition.episodes
    )
    tomorrow = None
    if composition.tomorrow_preview and composition.tomorrow_preview.has_preview:
        tp = composition.tomorrow_preview
        tomorrow = WorkspaceTomorrowPreview(
            topic_title=_scrub(tp.topic_title),
            continuity_line=_scrub(tp.continuity_line),
            estimated_duration_label=tp.estimated_duration_label,
            start_early_available=tp.start_early_available,
            start_early_label=tp.start_early_label,
            start_early_detail=_scrub(tp.start_early_detail),
            has_preview=True,
        )
    extra = tuple(
        WorkspaceExtraStudyOffer(
            label=o.label,
            detail=_scrub(o.detail),
            kind=o.kind.value if hasattr(o.kind, "value") else str(o.kind),
            href=_extra_study_href(o.href_hint),
        )
        for o in composition.extra_study
    )
    return WorkspaceMissionComposition(
        mission_narrative=_scrub(composition.mission_narrative),
        episodes=episodes,
        checkpoint_prompt=_scrub(composition.checkpoint_prompt),
        reflection_prompt=_scrub(composition.reflection_prompt),
        tomorrow_preview=tomorrow,
        extra_study=extra,
        total_duration_label=composition.total_duration_label,
        has_composition=True,
    )


def _extra_study_href(hint: str) -> str:
    """Resolve Extra Study destinations honestly (V1S-005 DF-006).

    ``start_tomorrow`` / ``start_early`` are continuity hints only — they do
    not advance the syllabus, so they must not look like actionable links.
    """
    if not has_request_context():
        return ""
    try:
        if hint == "revision":
            return url_for("student.revision")
        if hint in {"start_tomorrow", "start_early"}:
            return ""
    except Exception:  # noqa: BLE001
        return ""
    return ""


def _available_minutes(home: StudentHomePage) -> int | None:
    if home.signals and home.signals.estimated_study_label:
        parsed = _parse_minutes(home.signals.estimated_study_label)
        if parsed > 0:
            return parsed
    return None


def _parse_minutes(label: str) -> int:
    text = (label or "").strip().lower()
    if not text:
        return 0
    digits = "".join(ch if ch.isdigit() else " " for ch in text).split()
    if not digits:
        return 0
    value = int(digits[0])
    if "h" in text and value < 24:
        rem = int(digits[1]) if len(digits) > 1 else 0
        return value * 60 + rem
    return value


def _recently_strengthened_titles(
    *,
    store: Any,
    student_id: str,
) -> tuple[str, ...]:
    if store is None or not student_id:
        return ()
    try:
        from app.services.educational_yield_metrics import list_evidence_packages

        packages = list_evidence_packages(store)
        sid = student_id.strip()
        titles: list[str] = []
        for package in sorted(
            (
                p
                for p in packages
                if isinstance(p, dict)
                and (not sid or str(p.get("student_id") or "").strip() == sid)
            ),
            key=lambda p: str(p.get("created_at") or ""),
            reverse=True,
        )[:5]:
            title = str(package.get("topic_title") or "").strip()
            if title and title not in titles:
                titles.append(title)
        return tuple(titles[:3])
    except Exception:  # noqa: BLE001
        return ()


def _session_plan(
    mission: HomeMission | None,
    *,
    composition: WorkspaceMissionComposition | None = None,
) -> WorkspaceSessionPlan | None:
    # Prefer authored Learning Episode objective over raw mission dump (KWP-015).
    authored_objective = ""
    authored_duration = ""
    if composition and composition.has_composition:
        primary = composition.episodes[0] if composition.episodes else None
        if primary and primary.learning_objective:
            authored_objective = primary.learning_objective
        authored_duration = (composition.total_duration_label or "").strip()

    if mission is None and not authored_objective:
        return None
    objective = authored_objective or (
        (
            (mission.learning_objective or mission.objective or mission.title or "")
            if mission
            else ""
        ).strip()
    )
    # V1S-008 / DF-016: Mission card duration is the continuity authority.
    # Prefer it over authored episode sums so Home ↔ Session Plan agree.
    mission_duration = (
        (mission.duration_label or "").strip() if mission else ""
    )
    duration = mission_duration or authored_duration
    status = (mission.status_label or "").strip() if mission else ""
    after_completion = (
        (mission.after_completion or "").strip() if mission else ""
    )
    if not objective and not duration:
        return None
    return WorkspaceSessionPlan(
        objective=objective,
        duration_label=duration,
        status_label=status,
        after_completion=after_completion,
        has_plan=True,
    )


def _current_focus(
    *,
    home: StudentHomePage,
    home_vm: HomePageViewModel,
    revision: RevisionPageViewModel | None,
    store: Any,
    student_id: str,
) -> WorkspaceCurrentFocus | None:
    topic = ""
    if home.mission and (home.mission.title or home.mission.objective):
        topic = (home.mission.title or home.mission.objective or "").strip()
    if not topic and home.briefing and home.briefing.recommended_focus:
        topic = home.briefing.recommended_focus.strip()
    if not topic and revision and revision.has_revision and revision.primary:
        topic = (revision.primary.topic_title or "").strip()
    if not topic and home_vm.recommendation and home_vm.recommendation.title:
        topic = home_vm.recommendation.title.strip()
    if not topic:
        return None

    guidance, detail = _focus_guidance(
        topic_title=topic,
        home=home,
        revision=revision,
        store=store,
        student_id=student_id,
    )
    if home.briefing and home.briefing.needs_reinforcement:
        reinforce = ", ".join(home.briefing.needs_reinforcement[:2])
        reinforce_line = f"Needs reinforcement: {reinforce}."
        if reinforce_line.lower() not in (detail or "").lower():
            detail = f"{detail} {reinforce_line}".strip() if detail else reinforce_line

    curriculum_why = _curriculum_why_for_focus(
        topic_title=topic,
        home=home,
        home_vm=home_vm,
        store=store,
        student_id=student_id,
    )
    return WorkspaceCurrentFocus(
        topic_title=topic,
        guidance=_scrub(guidance),
        detail=_scrub(detail),
        curriculum_why=_scrub(curriculum_why),
        has_focus=True,
    )


def _focus_guidance(
    *,
    topic_title: str,
    home: StudentHomePage,
    revision: RevisionPageViewModel | None,
    store: Any,
    student_id: str,
) -> tuple[str, str]:
    """Combine Strategy / Diagnostics / Difficulty into one explanation.

    Prefers the latest frozen Educational Memory snapshot for this topic;
    otherwise projects live engines for the current focus topic only.
    """
    snapshot_fields = _latest_topic_snapshot_fields(
        store=store,
        student_id=student_id,
        topic_title=topic_title,
    )
    if snapshot_fields:
        strategy = snapshot_fields.get("strategy_body") or snapshot_fields.get(
            "strategy_title"
        )
        diagnostic = snapshot_fields.get("diagnostic_guidance")
        difficulty = snapshot_fields.get("difficulty_guidance")
        parts = [p for p in (strategy, diagnostic, difficulty) if p]
        if parts:
            primary = parts[0]
            detail = " ".join(parts[1:2])
            return primary, detail

    # Live projection for today's focus — presentation consumption only.
    try:
        from app.application.learning_diagnostics import (
            DiagnosticEvidenceInput,
            get_learning_diagnostics_engine,
        )
        from app.application.learning_difficulty import (
            DifficultyEvidenceInput,
            get_learning_difficulty_engine,
        )
        from app.application.learning_strategy import (
            StrategyEvidenceInput,
            get_learning_strategy_engine,
        )

        weak = bool(
            revision
            and revision.has_revision
            and revision.primary
            and (revision.primary.topic_title or "").strip().lower()
            == topic_title.lower()
        )
        strategy = get_learning_strategy_engine().evaluate(
            StrategyEvidenceInput(
                topic_title=topic_title,
                weak_topic=weak,
                practice_attempted=2 if weak else 0,
                practice_incorrect=2 if weak else 0,
            )
        )
        diagnostic = get_learning_diagnostics_engine().evaluate(
            DiagnosticEvidenceInput(
                topic_title=topic_title,
                weak_topic=weak,
                practice_attempted=2 if weak else 0,
                practice_incorrect=2 if weak else 0,
                retention_risk=weak,
            )
        )
        difficulty = get_learning_difficulty_engine().evaluate(
            DifficultyEvidenceInput(
                topic_title=topic_title,
                weak_topic=weak,
            )
        )
        strategy_line = (
            (strategy.recommendation_body or strategy.recommendation_title or "")
            if strategy
            else ""
        ).strip()
        diagnostic_line = (diagnostic.guidance or "").strip() if diagnostic else ""
        difficulty_line = (
            (difficulty.guidance or "").strip() if difficulty else ""
        )
        # Compose one student-facing explanation.
        if weak and diagnostic_line:
            guidance = (
                f"Strengthen prerequisite foundations first, then continue "
                f"with {topic_title}."
            )
            detail = diagnostic_line[:160]
            if strategy_line and strategy_line not in detail:
                detail = f"{detail} {strategy_line}".strip()[:220]
            return guidance, detail
        if strategy_line:
            detail_parts = [p for p in (diagnostic_line, difficulty_line) if p]
            return strategy_line[:180], " ".join(detail_parts)[:180]
        if home.briefing and home.briefing.recommended_detail:
            return (
                f"Today's focus is {topic_title}.",
                home.briefing.recommended_detail[:180],
            )
    except Exception:  # noqa: BLE001
        pass

    why = ""
    if home.mission and home.mission.why_now:
        why = home.mission.why_now.strip()
    elif home.briefing and home.briefing.recommended_detail:
        why = home.briefing.recommended_detail.strip()
    return f"Today's focus is {topic_title}.", why[:180]


def _latest_topic_snapshot_fields(
    *,
    store: Any,
    student_id: str,
    topic_title: str,
) -> dict[str, str]:
    if store is None or not student_id or not topic_title:
        return {}
    try:
        from app.application.educational_memory.snapshot import (
            snapshot_from_package,
        )
        from app.services.educational_yield_metrics import list_evidence_packages

        packages = list_evidence_packages(store)
        topic_lower = topic_title.lower()
        sid = student_id.strip()
        ordered = sorted(
            (
                p
                for p in packages
                if isinstance(p, dict)
                and (not sid or str(p.get("student_id") or "").strip() == sid)
            ),
            key=lambda p: str(p.get("created_at") or ""),
            reverse=True,
        )
        for package in ordered:
            if str(package.get("topic_title") or "").strip().lower() != topic_lower:
                continue
            snap = snapshot_from_package(package)
            if snap is None or not snap.has_student_report:
                continue
            report = snap.student_sitting_report or {}
            return {str(k): str(v) for k, v in report.items() if v}
    except Exception:  # noqa: BLE001
        return {}
    return {}


def _curriculum_why_for_focus(
    *,
    topic_title: str,
    home: StudentHomePage,
    home_vm: HomePageViewModel,
    store: Any,
    student_id: str,
) -> str:
    """Explain why today's topic matters using curriculum relationships (KWP-014)."""
    topic = (topic_title or "").strip()
    if not topic:
        return ""
    try:
        from app.application.knowledge_architecture import (
            KnowledgeArchitectureEngine,
            LearnerGraphContext,
        )
        from app.application.knowledge_architecture.graph_adapter import (
            graph_from_learner_package,
        )

        subject_code = ""
        topic_id = ""
        edu = getattr(home_vm, "educational", None)
        if edu and getattr(edu, "active", False):
            subject_code = (getattr(edu, "subject_code", "") or "").strip()
            topic_id = (getattr(edu, "today_topic_code", "") or "").strip()

        package = None
        if subject_code:
            try:
                from app.application.curriculum_intelligence import (
                    certified_learning_service as cls,
                )

                package = cls.CertifiedLearningService().load_package(subject_code)
            except Exception:  # noqa: BLE001
                package = None

        graph = graph_from_learner_package(package) if package else None
        if graph is None or graph.topic_count() == 0:
            return ""

        resolved = topic_id
        if not resolved or not graph.has_topic(resolved):
            for node in graph.nodes():
                if node.name.strip().lower() == topic.lower():
                    resolved = node.topic_id.value
                    break
        if not resolved or not graph.has_topic(resolved):
            return ""

        completed: set[str] = set()
        weak: set[str] = set()
        recent: set[str] = set()
        if store is not None and student_id:
            try:
                from app.services.educational_yield_metrics import (
                    list_evidence_packages,
                )

                packages = list_evidence_packages(store)
                sid = student_id.strip()
                ordered = sorted(
                    (
                        p
                        for p in packages
                        if isinstance(p, dict)
                        and (
                            not sid
                            or str(p.get("student_id") or "").strip() == sid
                        )
                    ),
                    key=lambda p: str(p.get("created_at") or ""),
                )
                for package_row in ordered:
                    tid = str(package_row.get("topic_id") or "").strip()
                    title = str(package_row.get("topic_title") or "").strip()
                    key = tid or title
                    if not key:
                        continue
                    if package_row.get("progress_advanced"):
                        completed.add(key)
                    incorrect = 0
                    for obs in package_row.get("observations") or ():
                        if (
                            isinstance(obs, dict)
                            and obs.get("type_id") == "EV-RT-08"
                        ):
                            incorrect += 1
                    if incorrect >= 2:
                        weak.add(key)
                for package_row in reversed(ordered[-5:]):
                    if package_row.get("progress_advanced"):
                        tid = str(package_row.get("topic_id") or "").strip()
                        title = str(package_row.get("topic_title") or "").strip()
                        if tid:
                            recent.add(tid)
                        if title:
                            recent.add(title.lower())
            except Exception:  # noqa: BLE001
                pass

        engine = KnowledgeArchitectureEngine(graph)
        ctx = LearnerGraphContext(
            completed_topic_ids=frozenset(completed),
            weak_topic_ids=frozenset(weak),
            current_topic_id=resolved,
            recently_strengthened_ids=frozenset(recent),
        )
        return engine.why_matters(resolved, context=ctx)
    except Exception:  # noqa: BLE001
        return ""


def _progress_narrative(
    *,
    home: StudentHomePage,
    history: HistoryPageViewModel | None,
    narrative,
) -> WorkspaceProgressNarrative | None:
    if narrative is not None and getattr(narrative, "has_memory", False):
        for pattern in getattr(narrative, "patterns", ()) or ():
            title = (getattr(pattern, "title", "") or "").strip()
            body = (getattr(pattern, "narrative", "") or "").strip()
            lowered = title.lower()
            if "recover" in lowered and body:
                return WorkspaceProgressNarrative(
                    headline="Recovery in progress",
                    body=_scrub(body[:220]),
                    has_narrative=True,
                )
            if "consistenc" in lowered and body:
                return WorkspaceProgressNarrative(
                    headline="Stronger consistency",
                    body=_scrub(
                        body[:220]
                        or "Recent sessions suggest stronger consistency."
                    ),
                    has_narrative=True,
                )
        for milestone in getattr(narrative, "milestones", ()) or ():
            body = (getattr(milestone, "narrative", "") or "").strip()
            title = (getattr(milestone, "title", "") or "").strip()
            if body or title:
                return WorkspaceProgressNarrative(
                    headline=title or "Recent progress",
                    body=_scrub(
                        body[:220]
                        or "You have made meaningful progress in recent sittings."
                    ),
                    has_narrative=True,
                )
        paragraphs = getattr(narrative, "story_paragraphs", ()) or ()
        if paragraphs:
            return WorkspaceProgressNarrative(
                headline="Recent progress",
                body=_scrub(str(paragraphs[0])[:220]),
                has_narrative=True,
            )

    if home.study_health and home.study_health.detail:
        # Kept for Session/Journey consumers; Home omits via home_worthy=False.
        return WorkspaceProgressNarrative(
            headline=home.study_health.status_label or "Study Health",
            body=_scrub(home.study_health.detail[:220]),
            has_narrative=True,
            home_worthy=False,
        )

    achievement = ""
    if home.insights:
        for insight in home.insights:
            if insight.kind in {"achievement", "changed"} and insight.body:
                achievement = insight.body.strip()
                break
    if not achievement and history and history.sessions:
        latest = history.sessions[0]
        topic = (latest.topic_title or "").strip()
        if topic:
            achievement = f"You recently completed {topic}."
    if achievement:
        return WorkspaceProgressNarrative(
            headline="Recent progress",
            body=_scrub(achievement[:220]),
            has_narrative=True,
            home_worthy=True,
        )
    return None


# Health-path momentum fillers — calm but not history/memory continuity.
_GENERIC_MOMENTUM_LINES = frozenset(
    {
        "your study path is ready when you are.",
        "a steadier rhythm will strengthen today's session.",
        "you are building exam readiness step by step.",
        "you are maintaining steady progress.",
    }
)


def _is_generic_momentum_line(text: str) -> bool:
    lowered = (text or "").strip().lower()
    if not lowered:
        return True
    if lowered in _GENERIC_MOMENTUM_LINES:
        return True
    return lowered.startswith("you are currently ")


def home_continuity_line(
    brief: WorkspaceMorningBrief | None,
    *,
    fallback: str = "",
) -> str:
    """One Home continuity line from morning brief (never yesterday + momentum + today).

    Prefers ``yesterday_line`` when present; otherwise a non-generic
    ``momentum_line`` (memory/tutor voice). Omits filler when no history/memory
    exists. Falls back to density/gap continuity when brief has nothing specific.
    """
    if brief is not None:
        yesterday = (brief.yesterday_line or "").strip()
        if yesterday:
            return yesterday
        momentum = (brief.momentum_line or "").strip()
        if momentum and not _is_generic_momentum_line(momentum):
            return momentum
    return (fallback or "").strip()


def _forecast_summary(forecast) -> WorkspaceForecastSummary | None:
    if forecast is None:
        return None
    guidance = (getattr(forecast, "guidance", "") or "").strip()
    title = (getattr(forecast, "title", "") or "").strip()
    if not guidance and not title:
        return None
    href = ""
    if has_request_context():
        try:
            href = url_for("student.learning_journey")
        except Exception:  # noqa: BLE001
            href = ""
    return WorkspaceForecastSummary(
        title=title or "Readiness Forecast",
        guidance=_scrub(guidance),
        href=href,
        has_forecast=bool(guidance),
    )


def _journey_highlights(narrative) -> WorkspaceJourneyHighlights | None:
    if narrative is None or not getattr(narrative, "has_memory", False):
        return None
    milestone = ""
    milestones = getattr(narrative, "milestones", ()) or ()
    if milestones:
        m = milestones[0]
        milestone = (
            getattr(m, "narrative", "") or getattr(m, "title", "") or ""
        ).strip()
    pattern = ""
    patterns = getattr(narrative, "patterns", ()) or ()
    if patterns:
        p = patterns[0]
        pattern = (
            getattr(p, "narrative", "") or getattr(p, "title", "") or ""
        ).strip()
    improvement = ""
    for entry in reversed(getattr(narrative, "timeline", ()) or ()):
        kind = getattr(getattr(entry, "kind", None), "value", "") or ""
        if kind in {
            "understanding_improved",
            "recovered",
            "advanced",
            "mastered",
            "consolidated",
        }:
            improvement = (getattr(entry, "body", "") or "").strip()
            if not improvement:
                topic = (getattr(entry, "topic_title", "") or "").strip()
                title = (getattr(entry, "title", "") or "").strip()
                improvement = f"{title}: {topic}".strip(": ")
            break
    if not any((milestone, pattern, improvement)):
        paragraphs = getattr(narrative, "story_paragraphs", ()) or ()
        if paragraphs:
            improvement = str(paragraphs[0]).strip()
    if not any((milestone, pattern, improvement)):
        return None
    href = ""
    if has_request_context():
        try:
            href = url_for("student.learning_journey")
        except Exception:  # noqa: BLE001
            href = ""
    return WorkspaceJourneyHighlights(
        milestone=_scrub(milestone[:200]),
        pattern=_scrub(pattern[:200]),
        improvement=_scrub(improvement[:200]),
        href=href,
        has_highlights=True,
    )


def _quick_actions(
    *,
    home: StudentHomePage,
    home_vm: HomePageViewModel,
    history: HistoryPageViewModel | None,
    revision: RevisionPageViewModel | None,
    has_journey: bool,
    has_forecast: bool,
    composition: WorkspaceMissionComposition | None = None,
) -> tuple[WorkspaceQuickAction, ...]:
    actions: list[WorkspaceQuickAction] = []

    # UX-001: mission hero owns Start / Continue — do not duplicate in Quick Actions.

    # Extra study with a real destination only (V1S-005 DF-006 honesty).
    if composition and composition.extra_study:
        for offer in composition.extra_study[:2]:
            if offer.href and not any(a.label == offer.label for a in actions):
                actions.append(
                    WorkspaceQuickAction(
                        label=offer.label,
                        href=offer.href,
                        detail=(offer.detail or "")[:120],
                        kind="link",
                    )
                )
    # Start Early is continuity copy on Tomorrow Preview — not a Quick Action.

    # Review Yesterday
    review_href = ""
    review_detail = "Revisit your last Sitting Report"
    if history and history.sessions:
        latest = history.sessions[0]
        review_href = (latest.sitting_report_href or "").strip()
        topic = (latest.topic_title or "").strip()
        if topic:
            review_detail = topic
    if not review_href and has_request_context():
        try:
            review_href = url_for("student.history")
        except Exception:  # noqa: BLE001
            review_href = ""
    if review_href:
        actions.append(
            WorkspaceQuickAction(
                label="Review Yesterday",
                href=review_href,
                detail=review_detail,
                kind="link",
            )
        )

    # Resume Revision
    if revision and revision.has_revision and revision.primary:
        rev_href = ""
        if has_request_context():
            try:
                rev_href = url_for("student.revision")
            except Exception:  # noqa: BLE001
                rev_href = ""
        if rev_href and not any(a.label == "Continue Revision" for a in actions):
            actions.append(
                WorkspaceQuickAction(
                    label="Resume Revision",
                    href=rev_href,
                    detail=(revision.primary.topic_title or "Supporting revision"),
                    kind="link",
                )
            )

    # View Journey
    journey_href = ""
    if has_request_context():
        try:
            journey_href = url_for("student.learning_journey")
        except Exception:  # noqa: BLE001
            journey_href = ""
    if journey_href:
        actions.append(
            WorkspaceQuickAction(
                label="View My Learning Journey",
                href=journey_href,
                detail="My Learning Journey" if has_journey else "See your story",
                kind="link",
            )
        )

    # Curriculum Map (KWP-014)
    map_href = ""
    if has_request_context():
        try:
            map_href = url_for("student.knowledge_graph")
        except Exception:  # noqa: BLE001
            map_href = ""
    if map_href:
        actions.append(
            WorkspaceQuickAction(
                label="Curriculum Map",
                href=map_href,
                detail="Where today's topic sits",
                kind="link",
            )
        )

    # View Forecast — Learning Journey forecast section when present
    # (Home no longer hosts #ws-forecast-title; see learning_journey.html).
    forecast_href = ""
    if has_request_context():
        try:
            forecast_href = url_for(
                "student.learning_journey",
                _anchor="journey-forecast-title",
            )
        except Exception:  # noqa: BLE001
            forecast_href = ""
    if forecast_href and has_forecast:
        actions.append(
            WorkspaceQuickAction(
                label="View Readiness Forecast",
                href=forecast_href,
                detail="Readiness Forecast",
                kind="link",
            )
        )

    # Cap workspace actions; preserve order.
    return tuple(actions[:6])


def _scrub(text: str) -> str:
    value = (text or "").strip()
    if not value:
        return ""
    lowered = value.lower()
    for fragment in _FORBIDDEN:
        if fragment in lowered:
            # Drop sentences containing forbidden internal vocabulary.
            parts = [p.strip() for p in value.replace("!", ".").split(".") if p.strip()]
            kept = [
                p
                for p in parts
                if not any(f in p.lower() for f in _FORBIDDEN)
            ]
            return ". ".join(kept).strip()
    return value


# Re-export signals type for template convenience typing.
__all__ = [
    "AdaptiveStudyWorkspace",
    "HomeStudySignals",
    "compose_adaptive_workspace",
]

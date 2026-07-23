"""WorkspacePresenter — format PipelineResult into MissionWorkspaceViewModel.

Presentation orchestration only. Reads Educational Pipeline outputs and
assembles display fields. Never diagnoses, recommends, persists, or calls AI.
"""

from __future__ import annotations

from dataclasses import replace
from typing import Any

from presentation.mission_workspace.mission_progress_mapper import (
    MissionProgressMapper,
)
from presentation.mission_workspace.workspace_view_model import (
    CompletionActionView,
    MissionWorkspaceViewModel,
    RecommendationSummaryView,
    ReflectionStatusView,
    StudyResourceView,
)
from presentation.provenance import ProvenanceMapper

_DEFAULT_GREETING = "Welcome back — ready for today's session."
_DEFAULT_TITLE = "Today's Session"
_DEFAULT_OBJECTIVE = "Your session objective will appear here when available."
_DEFAULT_EXPLANATION = "Session guidance will appear here when available."
_DEFAULT_DURATION = "Duration not available"
_DEFAULT_RECOMMENDATION_HEADLINE = "Next step"
_DEFAULT_RECOMMENDATION_DETAIL = "No recommendation summary is available yet."
_DEFAULT_REFLECTION_LABEL = "Reflection"
_DEFAULT_REFLECTION_DETAIL = (
    "Take a moment to note what felt clear and what still needs practice."
)

_CATEGORY_LABELS: dict[str, str] = {
    "continue_mission": "Continue session",
    "review_previous_topic": "Review previous topic",
    "increase_difficulty": "Increase challenge carefully",
    "reduce_cognitive_load": "Reduce cognitive load",
    "repeat_assessment": "Repeat assessment",
    "schedule_revision": "Schedule revision",
    "revisit_prerequisites": "Revisit prerequisites",
    "pause_for_consolidation": "Pause to consolidate",
}

_COMPLETION_ACTION_BY_CATEGORY: dict[str, tuple[str, str]] = {
    "continue_mission": (
        "Continue Session",
        "Resume the current session work.",
    ),
    "review_previous_topic": (
        "Start Revision",
        "Review the previous topic first.",
    ),
    "increase_difficulty": (
        "Continue Session",
        "Continue with a careful challenge increase.",
    ),
    "reduce_cognitive_load": (
        "Continue Session",
        "Continue with a lighter focus.",
    ),
    "repeat_assessment": (
        "Continue Session",
        "Continue to recalibrate confidence.",
    ),
    "schedule_revision": (
        "Plan Revision",
        "Schedule spaced revision next.",
    ),
    "revisit_prerequisites": (
        "Review Prerequisites",
        "Revisit supporting concepts first.",
    ),
    "pause_for_consolidation": (
        "Return Home",
        "Pause advancement and consolidate.",
    ),
}


class WorkspacePresenter:
    """Present one study session workspace from a ``PipelineResult``."""

    @classmethod
    def present(
        cls,
        result: Any = None,
        *,
        experience: Any = None,
    ) -> MissionWorkspaceViewModel:
        """Map a ``PipelineResult`` into an immutable workspace view model.

        Args:
            result: Complete Educational Pipeline cargo. Structural duck-typing
                is accepted for tests; production callers pass ``PipelineResult``.
            experience: Optional XP journey / workspace snapshot. When present,
                greeting and reflection chrome prefer live experience projections.

        Returns:
            Immutable ``MissionWorkspaceViewModel`` with null-safe display fields.
        """
        if result is None and experience is None:
            return cls._empty_workspace()

        mission = getattr(result, "mission", None) if result is not None else None
        enhanced = (
            getattr(result, "enhanced_mission", None) if result is not None else None
        )
        explanation = (
            getattr(result, "explanation", None) if result is not None else None
        )
        recommendations = (
            getattr(result, "recommendations", None) if result is not None else None
        )
        enhanced_recs = (
            getattr(result, "enhanced_recommendations", None)
            if result is not None
            else None
        )
        pipeline_experience = (
            getattr(result, "student_experience", None) if result is not None else None
        )

        greeting = cls._greeting_from_xp(experience) or cls._greeting(
            pipeline_experience
        )
        if mission is not None or enhanced is not None:
            mission_title = cls._mission_title(mission, enhanced)
        else:
            mission_title = cls._xp_mission_title(experience)
        if mission is not None:
            mission_objective = cls._mission_objective(mission)
        else:
            mission_objective = cls._xp_objective(experience)
        mission_explanation = cls._mission_explanation(
            explanation=explanation,
            mission=mission,
            enhanced=enhanced,
        )
        estimated_duration = cls._estimated_duration(mission)
        study_resources = cls._study_resources(mission=mission, enhanced=enhanced)
        progress_summary = MissionProgressMapper.map_progress_summary(result)
        recommendation_summary = cls._recommendation_summary(
            recommendations=recommendations,
            enhanced_recs=enhanced_recs,
        )
        reflection_status = cls._reflection_status_from_xp(
            experience
        ) or cls._reflection_status(pipeline_experience)
        session_progress = MissionProgressMapper.map_session_progress(result)
        completion_actions = cls._completion_actions(
            mission=mission,
            recommendations=recommendations,
        )
        workspace = MissionWorkspaceViewModel(
            greeting=greeting,
            mission_title=mission_title,
            mission_objective=mission_objective,
            mission_explanation=mission_explanation,
            estimated_duration=estimated_duration,
            study_resources=study_resources,
            progress_summary=progress_summary,
            recommendation_summary=recommendation_summary,
            reflection_status=reflection_status,
            session_progress=session_progress,
            completion_actions=completion_actions,
        )
        return replace(
            workspace,
            provenance=ProvenanceMapper.for_mission(
                workspace, result=result, experience=experience
            ),
        )

    @classmethod
    def _empty_workspace(cls) -> MissionWorkspaceViewModel:
        return MissionWorkspaceViewModel(
            greeting=_DEFAULT_GREETING,
            mission_title=_DEFAULT_TITLE,
            mission_objective=_DEFAULT_OBJECTIVE,
            mission_explanation=_DEFAULT_EXPLANATION,
            estimated_duration=_DEFAULT_DURATION,
            study_resources=(),
            progress_summary=MissionProgressMapper.map_progress_summary(None),
            recommendation_summary=RecommendationSummaryView(
                headline=_DEFAULT_RECOMMENDATION_HEADLINE,
                detail=_DEFAULT_RECOMMENDATION_DETAIL,
                category_label="",
                expected_outcome="",
            ),
            reflection_status=ReflectionStatusView(
                label=_DEFAULT_REFLECTION_LABEL,
                detail=_DEFAULT_REFLECTION_DETAIL,
                is_available=False,
            ),
            session_progress=MissionProgressMapper.map_session_progress(None),
            completion_actions=(
                CompletionActionView(
                    label="Return Home",
                    detail="Return when you are ready to continue.",
                    action_key="return_home",
                ),
            ),
            provenance=ProvenanceMapper.for_mission(None),
        )

    @classmethod
    def _greeting_from_xp(cls, experience: Any) -> str:
        if experience is None:
            return ""
        workspace = getattr(experience, "workspace", None)
        snap = getattr(experience, "workspace_snapshot", None)
        for candidate in (
            getattr(snap, "primary_focus_prompt", None),
            getattr(
                getattr(getattr(workspace, "focus", None), "primary", None),
                "prompt",
                None,
            ),
            getattr(getattr(experience, "home_snapshot", None), "focus_headline", None),
        ):
            text = _text(candidate)
            if text:
                return text
        return ""

    @classmethod
    def _xp_mission_title(cls, experience: Any) -> str:
        if experience is None:
            return _DEFAULT_TITLE
        snap = getattr(experience, "workspace_snapshot", None)
        home = getattr(experience, "home_snapshot", None)
        workspace = getattr(experience, "workspace", None)
        session = getattr(workspace, "current_session", None) if workspace else None
        return (
            _text(getattr(snap, "mission_title", None))
            or _text(getattr(session, "mission_title", None))
            or _text(getattr(home, "focus_mission_title", None))
            or _DEFAULT_TITLE
        )

    @classmethod
    def _xp_objective(cls, experience: Any) -> str:
        if experience is None:
            return _DEFAULT_OBJECTIVE
        snap = getattr(experience, "workspace_snapshot", None)
        workspace = getattr(experience, "workspace", None)
        focus = getattr(workspace, "focus", None) if workspace else None
        primary = getattr(focus, "primary", None) if focus else None
        return (
            _text(getattr(snap, "current_objective_label", None))
            or _text(getattr(primary, "prompt", None))
            or _DEFAULT_OBJECTIVE
        )

    @classmethod
    def _reflection_status_from_xp(cls, experience: Any) -> ReflectionStatusView | None:
        if experience is None:
            return None
        workspace = getattr(experience, "workspace", None)
        reflection = getattr(workspace, "reflection", None) if workspace else None
        if reflection is None:
            return None
        label = _DEFAULT_REFLECTION_LABEL
        detail = (
            _text(getattr(reflection, "reflection_prompt", None))
            or _text(getattr(reflection, "summary", None))
            or _DEFAULT_REFLECTION_DETAIL
        )
        return ReflectionStatusView(
            label=label,
            detail=detail,
            is_available=bool(getattr(reflection, "available", True)),
        )

    @classmethod
    def _greeting(cls, experience: Any) -> str:
        motivation = getattr(experience, "motivation", None) if experience else None
        message = _text(getattr(motivation, "message", None))
        if message:
            return message
        narrative = _text(getattr(experience, "presentation_narrative", None))
        if narrative:
            return _first_sentence(narrative) or _DEFAULT_GREETING
        return _DEFAULT_GREETING

    @classmethod
    def _mission_title(cls, mission: Any, enhanced: Any) -> str:
        improved = _text(getattr(enhanced, "improved_wording", None))
        if improved:
            return _first_sentence(improved) or _DEFAULT_TITLE
        objective = getattr(mission, "objective", None) if mission else None
        statement = _text(getattr(objective, "statement", None))
        if statement:
            return _first_sentence(statement) or _DEFAULT_TITLE
        return _DEFAULT_TITLE

    @classmethod
    def _mission_objective(cls, mission: Any) -> str:
        objective = getattr(mission, "objective", None) if mission else None
        return _text(
            getattr(objective, "statement", None),
            fallback=_DEFAULT_OBJECTIVE,
        )

    @classmethod
    def _mission_explanation(
        cls,
        *,
        explanation: Any,
        mission: Any,
        enhanced: Any,
    ) -> str:
        summary = _text(getattr(explanation, "summary", None))
        if summary:
            return summary
        rationale = _text(getattr(mission, "educational_rationale", None))
        if rationale:
            return rationale
        improved = _text(getattr(enhanced, "improved_wording", None))
        if improved:
            return improved
        return _DEFAULT_EXPLANATION

    @classmethod
    def _estimated_duration(cls, mission: Any) -> str:
        duration = getattr(mission, "duration", None) if mission else None
        minutes = getattr(duration, "planned_minutes", None)
        if minutes is None or isinstance(minutes, bool):
            return _DEFAULT_DURATION
        try:
            value = int(minutes)
        except (TypeError, ValueError):
            return _DEFAULT_DURATION
        if value <= 0:
            return _DEFAULT_DURATION
        if value == 1:
            return "1 minute"
        return f"{value} minutes"

    @classmethod
    def _study_resources(
        cls,
        *,
        mission: Any,
        enhanced: Any,
    ) -> tuple[StudyResourceView, ...]:
        resources: list[StudyResourceView] = []
        tasks = ()
        if mission is not None:
            sequence = getattr(mission, "sequence", None)
            tasks = _as_tuple(getattr(sequence, "tasks", ()))
            if not tasks:
                tasks = _as_tuple(getattr(mission, "ordered_tasks", ()))
        for task in tasks:
            if task is None:
                continue
            label = _text(getattr(task, "label", None), fallback="Study task")
            detail = _text(getattr(task, "success_hint", None))
            minutes = getattr(task, "estimated_minutes", None)
            estimated: int | None
            try:
                estimated = int(minutes) if minutes is not None else None
            except (TypeError, ValueError):
                estimated = None
            if estimated is not None and estimated <= 0:
                estimated = None
            resources.append(
                StudyResourceView(
                    label=label,
                    detail=detail,
                    kind="task",
                    estimated_minutes=estimated,
                )
            )

        for tip in _as_tuple(getattr(enhanced, "revision_tips", ())):
            text = _text(tip)
            if text:
                resources.append(
                    StudyResourceView(label=text, detail="", kind="tip")
                )
        for example in _as_tuple(getattr(enhanced, "worked_examples", ())):
            text = _text(example)
            if text:
                resources.append(
                    StudyResourceView(label=text, detail="", kind="example")
                )
        for example in _as_tuple(getattr(enhanced, "examples", ())):
            text = _text(example)
            if text:
                resources.append(
                    StudyResourceView(label=text, detail="", kind="example")
                )
        return tuple(resources)

    @classmethod
    def _recommendation_summary(
        cls,
        *,
        recommendations: Any,
        enhanced_recs: Any,
    ) -> RecommendationSummaryView:
        if recommendations is None:
            return RecommendationSummaryView(
                headline=_DEFAULT_RECOMMENDATION_HEADLINE,
                detail=_DEFAULT_RECOMMENDATION_DETAIL,
                category_label="",
                expected_outcome="",
            )

        primary = _primary_recommendation(recommendations)
        category_raw = _enum_value(getattr(primary, "category", None))
        category_label = _CATEGORY_LABELS.get(
            category_raw,
            _humanise(category_raw) if category_raw else "",
        )
        reason = getattr(primary, "reason", None)
        reason_text = _text(getattr(reason, "statement", None))
        expected = _text(getattr(primary, "expected_outcome", None))
        improved = _text(getattr(enhanced_recs, "improved_wording", None))
        rationale = _text(getattr(recommendations, "educational_rationale", None))

        detail = improved or rationale or reason_text or _DEFAULT_RECOMMENDATION_DETAIL
        headline = category_label or _DEFAULT_RECOMMENDATION_HEADLINE
        return RecommendationSummaryView(
            headline=headline,
            detail=detail,
            category_label=category_label,
            expected_outcome=expected,
        )

    @classmethod
    def _reflection_status(cls, experience: Any) -> ReflectionStatusView:
        if experience is None:
            return ReflectionStatusView(
                label=_DEFAULT_REFLECTION_LABEL,
                detail=_DEFAULT_REFLECTION_DETAIL,
                is_available=False,
            )
        summary = getattr(experience, "session_summary", None)
        honesty = _text(getattr(summary, "honesty_note", None))
        celebrations = _as_tuple(getattr(experience, "celebrations", ()))
        if celebrations:
            first = celebrations[0]
            headline = _text(getattr(first, "headline", None))
            detail = (
                _text(getattr(first, "detail", None))
                or honesty
                or _DEFAULT_REFLECTION_DETAIL
            )
            return ReflectionStatusView(
                label=headline or "Reflection ready",
                detail=detail,
                is_available=True,
            )
        if honesty:
            return ReflectionStatusView(
                label="Reflection available",
                detail=honesty,
                is_available=True,
            )
        return ReflectionStatusView(
            label=_DEFAULT_REFLECTION_LABEL,
            detail=_DEFAULT_REFLECTION_DETAIL,
            is_available=True,
        )

    @classmethod
    def _completion_actions(
        cls,
        *,
        mission: Any,
        recommendations: Any,
    ) -> tuple[CompletionActionView, ...]:
        actions: list[CompletionActionView] = []

        primary = _primary_recommendation(recommendations)
        category_raw = _enum_value(getattr(primary, "category", None))
        if category_raw in _COMPLETION_ACTION_BY_CATEGORY:
            label, detail = _COMPLETION_ACTION_BY_CATEGORY[category_raw]
            actions.append(
                CompletionActionView(
                    label=label,
                    detail=detail,
                    action_key=category_raw,
                )
            )

        conditions = _as_tuple(getattr(mission, "completion_conditions", ()))
        for condition in conditions:
            statement = _text(getattr(condition, "statement", None))
            code = _enum_value(getattr(condition, "code", None))
            if not statement:
                continue
            actions.append(
                CompletionActionView(
                    label="Completion check",
                    detail=statement,
                    action_key=code or "completion_condition",
                )
            )

        if not actions:
            actions.append(
                CompletionActionView(
                    label="Begin Session",
                    detail="Open today's session when you are ready.",
                    action_key="begin_session",
                )
            )
        actions.append(
            CompletionActionView(
                label="Return Home",
                detail="Return to Home when you are finished.",
                action_key="return_home",
            )
        )
        return tuple(actions)


def _primary_recommendation(recommendations: Any) -> Any:
    if recommendations is None:
        return None
    primary = getattr(recommendations, "primary", None)
    if callable(primary):
        try:
            primary = primary()
        except TypeError:
            primary = None
    if primary is not None:
        return primary
    items = _as_tuple(getattr(recommendations, "recommendations", ()))
    return items[0] if items else None


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    try:
        return tuple(value)
    except TypeError:
        return ()


def _enum_value(value: Any) -> str:
    if value is None:
        return ""
    raw = getattr(value, "value", value)
    return _text(str(raw) if raw is not None else None)


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback


def _first_sentence(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        return ""
    for separator in (". ", "! ", "? "):
        index = cleaned.find(separator)
        if index != -1:
            return cleaned[: index + 1].strip()
    return cleaned


def _humanise(value: str) -> str:
    cleaned = value.strip()
    if not cleaned:
        return cleaned
    return cleaned.replace("_", " ").replace("-", " ").strip().capitalize()

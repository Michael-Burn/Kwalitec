"""SessionPresenter — PipelineResult / workspace → StudySessionViewModel.

Presentation orchestration only. Assembles Design System chrome around
already-decided Educational OS outputs. Never diagnoses, recommends, persists,
orchestrates learning, or calls AI.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import (
    ContainerWidth,
    MissionCard,
    PageHeader,
    ProgressBar,
    ProgressCard,
    Section,
    StatisticTile,
)
from presentation.mission_workspace.workspace_presenter import WorkspacePresenter
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)
from presentation.study_session.completion_mapper import CompletionMapper
from presentation.study_session.resource_mapper import ResourceMapper
from presentation.study_session.session_timeline import SessionTimeline
from presentation.study_session.session_view_model import (
    SessionSectionView,
    StudySessionViewModel,
)

_DEFAULT_HEADER_TITLE = "Today's Session"
_DEFAULT_HEADER_DESCRIPTION = "A guided session for today's focused work."
_DEFAULT_OBJECTIVE_BODY = "Your session objective will appear here when available."
_DEFAULT_EXPLANATION_BODY = "Session guidance will appear here when available."
_DEFAULT_DURATION_VALUE = "Not available"
_DEFAULT_REFLECTION_BODY = (
    "Take a moment to note what felt clear and what still needs practice."
)
_ACTIVE_KEY = "mission_header"


class SessionPresenter:
    """Present one guided study session from pipeline / workspace inputs."""

    @classmethod
    def present(
        cls,
        result: Any = None,
        workspace: MissionWorkspaceViewModel | None = None,
    ) -> StudySessionViewModel:
        """Map pipeline and/or workspace inputs into a study session view model.

        Args:
            result: Optional ``PipelineResult`` (structural duck-typing accepted).
            workspace: Optional ``MissionWorkspaceViewModel``. When omitted and
                ``result`` is provided, a workspace is derived via
                ``WorkspacePresenter``.

        Returns:
            Immutable ``StudySessionViewModel`` with null-safe Design System chrome.
        """
        resolved = cls._resolve_workspace(result=result, workspace=workspace)

        resources = ResourceMapper.map_resources(resolved, result=result)
        worked_examples = ResourceMapper.map_worked_examples(resolved, result=result)
        completion = CompletionMapper.map_completion(resolved)
        next_step = CompletionMapper.map_next_step(resolved)

        greeting = _text(getattr(resolved, "greeting", None))
        mission_title = _text(
            getattr(resolved, "mission_title", None),
            fallback=_DEFAULT_HEADER_TITLE,
        )
        mission_objective = _text(
            getattr(resolved, "mission_objective", None),
            fallback=_DEFAULT_OBJECTIVE_BODY,
        )
        mission_explanation = _text(
            getattr(resolved, "mission_explanation", None),
            fallback=_DEFAULT_EXPLANATION_BODY,
        )
        estimated_duration = _text(
            getattr(resolved, "estimated_duration", None),
            fallback=_DEFAULT_DURATION_VALUE,
        )

        reflection = getattr(resolved, "reflection_status", None)
        reflection_body = _text(
            getattr(reflection, "detail", None),
            fallback=_DEFAULT_REFLECTION_BODY,
        )
        reflection_title = _text(
            getattr(reflection, "label", None),
            fallback="Reflection",
        )

        session_progress = getattr(resolved, "session_progress", None)
        progress_summary = getattr(resolved, "progress_summary", None)
        progress_label = _text(
            getattr(session_progress, "progress_label", None),
            fallback=_text(
                getattr(progress_summary, "headline", None),
                fallback="Session progress",
            ),
        )
        progress_detail = _text(
            getattr(progress_summary, "detail", None),
            fallback=progress_label,
        )
        trend_label = _text(
            getattr(session_progress, "mastery_trend_label", None)
            or getattr(progress_summary, "trend_label", None),
            fallback="Not available",
        )

        study_notes_body = ResourceMapper.study_notes_body(resolved, result=result)
        resources_body = ResourceMapper.resources_summary_body(resources)
        examples_body = ResourceMapper.examples_summary_body(worked_examples)
        completion_body = CompletionMapper.completion_section_body(completion)

        sections = SessionTimeline.order_sections(
            (
                SessionSectionView(
                    key="mission_header",
                    title=SessionTimeline.title_for("mission_header"),
                    body=mission_title,
                    eyebrow=greeting,
                ),
                SessionSectionView(
                    key="mission_objective",
                    title=SessionTimeline.title_for("mission_objective"),
                    body=mission_objective,
                ),
                SessionSectionView(
                    key="educational_explanation",
                    title=SessionTimeline.title_for("educational_explanation"),
                    body=mission_explanation,
                ),
                SessionSectionView(
                    key="estimated_duration",
                    title=SessionTimeline.title_for("estimated_duration"),
                    body=estimated_duration,
                ),
                SessionSectionView(
                    key="learning_resources",
                    title=SessionTimeline.title_for("learning_resources"),
                    body=resources_body,
                ),
                SessionSectionView(
                    key="worked_example",
                    title=SessionTimeline.title_for("worked_example"),
                    body=examples_body,
                ),
                SessionSectionView(
                    key="progress_indicator",
                    title=SessionTimeline.title_for("progress_indicator"),
                    body=progress_detail,
                ),
                SessionSectionView(
                    key="study_notes",
                    title=SessionTimeline.title_for("study_notes"),
                    body=study_notes_body,
                ),
                SessionSectionView(
                    key="reflection_prompt",
                    title=SessionTimeline.title_for("reflection_prompt"),
                    body=reflection_body,
                    eyebrow=reflection_title,
                ),
                SessionSectionView(
                    key="completion_summary",
                    title=SessionTimeline.title_for("completion_summary"),
                    body=completion_body,
                ),
                SessionSectionView(
                    key="next_step",
                    title=SessionTimeline.title_for("next_step"),
                    body=next_step.detail,
                    eyebrow=next_step.headline,
                ),
            )
        )

        timeline = SessionTimeline.build_timeline(sections, active_key=_ACTIVE_KEY)
        stepper = SessionTimeline.build_stepper(sections, current_key=_ACTIVE_KEY)
        percent = SessionTimeline.progress_percent(
            sections, current_key=_ACTIVE_KEY
        )

        header = PageHeader(
            title=mission_title,
            description=mission_objective
            if mission_objective != _DEFAULT_OBJECTIVE_BODY
            else _DEFAULT_HEADER_DESCRIPTION,
            eyebrow=greeting or "Session",
        )
        mission_card = MissionCard(
            title=mission_title,
            body=mission_objective,
            eyebrow="Today's Session",
            duration_label=estimated_duration,
            status_label=progress_label,
        )
        objective = Section(
            title="Objective",
            description=mission_objective,
            eyebrow="Session",
        )
        explanation = Section(
            title="Why this session",
            description=mission_explanation,
            eyebrow="Guidance",
        )
        duration = StatisticTile(
            label="Estimated duration",
            value=estimated_duration,
            detail="Planned focus time for this session",
        )
        progress_bar = ProgressBar(
            label=progress_label,
            percent=percent,
            value_text=progress_label,
        )
        progress_card = ProgressCard(
            title="Progress",
            body=progress_detail,
            eyebrow="Session",
            metric_label=progress_label,
            trend_label=trend_label,
        )
        study_notes = Section(
            title="Study notes",
            description=study_notes_body,
            eyebrow="Notes",
        )
        reflection_section = Section(
            title=reflection_title,
            description=reflection_body,
            eyebrow="Reflection",
        )

        return StudySessionViewModel(
            header=header,
            mission_card=mission_card,
            objective=objective,
            explanation=explanation,
            duration=duration,
            resources=resources,
            worked_examples=worked_examples,
            progress_bar=progress_bar,
            progress_card=progress_card,
            study_notes=study_notes,
            reflection=reflection_section,
            completion=completion,
            next_step=next_step,
            timeline=timeline,
            stepper=stepper,
            sections=sections,
            container_width=ContainerWidth.CONTENT,
            greeting=greeting,
        )

    @classmethod
    def _resolve_workspace(
        cls,
        *,
        result: Any,
        workspace: MissionWorkspaceViewModel | None,
    ) -> MissionWorkspaceViewModel:
        if workspace is not None:
            return workspace
        return WorkspacePresenter.present(result)


def _text(value: str | None, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback

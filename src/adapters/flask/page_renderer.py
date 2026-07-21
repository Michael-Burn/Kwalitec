"""PageRenderer — view models + Design System renderer → template context.

Composes ``TemplateMapper`` serialisation with ``ComponentRenderer`` HTML
fragments and student-flow navigation links. Flask-free.
"""

from __future__ import annotations

from typing import Any

from adapters.flask.navigation import student_flow_nav
from adapters.flask.rendering import ComponentRenderer
from adapters.flask.template_mapper import TemplateMapper
from presentation.dashboard.dashboard_view_model import DashboardViewModel
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)
from presentation.onboarding.onboarding_view_model import OnboardingViewModel
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel


class PageRenderer:
    """Build Jinja contexts with mapped view data and rendered HTML fragments."""

    def __init__(self, renderer: ComponentRenderer | None = None) -> None:
        self._renderer = renderer or ComponentRenderer()

    @property
    def renderer(self) -> ComponentRenderer:
        return self._renderer

    def for_dashboard(
        self,
        view_model: DashboardViewModel,
        *,
        student_id: str = "",
    ) -> dict[str, Any]:
        context = TemplateMapper.for_dashboard(view_model)
        context.update(self._chrome(student_id=student_id))
        context["fragments"] = {
            "header": self._renderer.render_page_header(view_model.header),
            "greeting": self._renderer.render_section(view_model.greeting),
            "mission_card": self._renderer.render_mission_card(view_model.mission_card),
            "primary_action": self._renderer.render_button(view_model.primary_action),
            "progress_bar": self._renderer.render_progress_bar(view_model.progress_bar),
            "statistics": tuple(
                self._renderer.render_statistic_card(tile)
                for tile in view_model.learning_statistics
            ),
            "achievements": tuple(
                self._renderer.render_achievement_card(item)
                for item in view_model.achievements
            ),
        }
        context["primary_action_key"] = "begin_session"
        return context

    def for_mission(
        self,
        view_model: MissionWorkspaceViewModel,
        *,
        student_id: str = "",
    ) -> dict[str, Any]:
        context = TemplateMapper.for_mission(view_model)
        context.update(self._chrome(student_id=student_id))
        return context

    def for_session(
        self,
        view_model: StudySessionViewModel,
        *,
        student_id: str = "",
        session_id: str = "",
        stage: str = "",
        paused: bool = False,
    ) -> dict[str, Any]:
        context = TemplateMapper.for_session(view_model)
        context.update(
            self._chrome(student_id=student_id, session_id=session_id)
        )
        context["stage"] = stage
        context["paused"] = paused
        context["session_id"] = session_id or context.get("session_id", "")
        context["fragments"] = {
            "header": self._renderer.render_page_header(view_model.header),
            "mission_card": self._renderer.render_mission_card(view_model.mission_card),
            "objective": self._renderer.render_section(view_model.objective),
            "progress_bar": self._renderer.render_progress_bar(view_model.progress_bar),
            "timeline": self._renderer.render_timeline(view_model.timeline),
        }
        return context

    def for_reflection(
        self,
        view_model: ReflectionViewModel,
        *,
        student_id: str = "",
        session_id: str = "",
        evidence_updated: bool = False,
    ) -> dict[str, Any]:
        context = TemplateMapper.for_reflection(view_model)
        context.update(
            self._chrome(
                student_id=student_id,
                session_id=session_id or context.get("session_id", ""),
            )
        )
        context["evidence_updated"] = evidence_updated
        context["student_id"] = student_id
        context["fragments"] = {
            "header": self._renderer.render_page_header(view_model.header),
            "confidence": self._renderer.render_section(view_model.confidence.section),
            "difficulty": self._renderer.render_section(view_model.difficulty.section),
            "weak_concept": self._renderer.render_section(
                view_model.weak_concept.section
            ),
            "student_notes": self._renderer.render_section(
                view_model.student_notes.section
            ),
            "summary": self._renderer.render_section(
                view_model.reflection_summary.section
            ),
        }
        if view_model.primary_button is not None:
            context["fragments"]["primary_button"] = self._renderer.render_button(
                view_model.primary_button
            )
        return context

    def for_onboarding(
        self,
        view_model: OnboardingViewModel,
        *,
        student_id: str = "",
    ) -> dict[str, Any]:
        resolved = student_id or view_model.student_id
        context = self._chrome(student_id=resolved)
        context.update(
            {
                "onboarding_id": view_model.onboarding_id,
                "student_id": resolved,
                "status_label": view_model.status_label,
                "progress_percent": view_model.progress_percent,
                "is_complete": view_model.is_complete,
                "redirect_path": view_model.redirect_path,
                "current_step": view_model.current_step.key,
                "review_lines": view_model.review_lines,
            }
        )
        context["fragments"] = {
            "header": self._renderer.render_page_header(view_model.header),
            "progress_bar": self._renderer.render_progress_bar(view_model.progress_bar),
            "section": self._renderer.render_section(view_model.current_step.section),
        }
        if view_model.primary_button is not None:
            context["fragments"]["primary_button"] = self._renderer.render_button(
                view_model.primary_button
            )
        return context

    def _chrome(
        self,
        *,
        student_id: str = "",
        session_id: str = "",
    ) -> dict[str, Any]:
        return {
            "token_css": self._renderer.token_style_tag(),
            "nav": student_flow_nav(student_id=student_id, session_id=session_id),
            "student_id": student_id,
        }

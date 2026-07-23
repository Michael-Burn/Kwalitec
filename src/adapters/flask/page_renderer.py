"""PageRenderer — view models + Design System renderer → template context.

Composes ``TemplateMapper`` serialisation with ``ComponentRenderer`` HTML
fragments and student-flow navigation links. Flask-free.
"""

from __future__ import annotations

from typing import Any

from adapters.flask.navigation import primary_cta_href, student_flow_nav
from adapters.flask.rendering import ComponentRenderer
from adapters.flask.template_mapper import TemplateMapper
from presentation.dashboard.dashboard_view_model import DashboardViewModel
from presentation.design_system import (
    EmptyState,
    Skeleton,
    SkeletonVariant,
    Toast,
    ToastTone,
)
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
)
from presentation.onboarding.onboarding_view_model import OnboardingViewModel
from presentation.polish import ContinuityBanner, continuity_from_query
from presentation.reflection.reflection_view_model import ReflectionViewModel
from presentation.study_session.session_view_model import StudySessionViewModel


class PageRenderer:
    """Build Jinja contexts with mapped view data and rendered HTML fragments."""

    def __init__(self, renderer: ComponentRenderer | None = None) -> None:
        self._renderer = renderer or ComponentRenderer()
        self._chrome_cache: dict[tuple[str, str], dict[str, Any]] = {}

    @property
    def renderer(self) -> ComponentRenderer:
        return self._renderer

    def for_dashboard(
        self,
        view_model: DashboardViewModel,
        *,
        student_id: str = "",
        session_id: str = "",
        primary_action_key: str | None = None,
        readiness_change_message: str | None = None,
        experience_success_message: str | None = None,
        continuity: ContinuityBanner | None = None,
        from_surface: str | None = None,
        updated: str | None = None,
    ) -> dict[str, Any]:
        context = TemplateMapper.for_dashboard(view_model)
        context.update(self._chrome(student_id=student_id, session_id=session_id))
        # PX-004: render only fragments the decision-screen template consumes.
        mission_card = getattr(view_model, "mission_card", None) or getattr(
            getattr(view_model, "hero", None), "mission_card", None
        )
        context["fragments"] = {
            "mission_card": (
                self._renderer.render_mission_card(mission_card)
                if mission_card is not None
                else ""
            ),
            "statistics": (),
            "achievements": (),
            "hero_provenance": self._renderer.render_provenance(
                getattr(getattr(view_model, "hero", None), "provenance", None)
            ),
            "readiness_provenance": self._renderer.render_provenance(
                getattr(getattr(view_model, "readiness", None), "provenance", None)
            ),
            "journey_provenance": self._renderer.render_provenance(
                getattr(getattr(view_model, "journey", None), "provenance", None)
            ),
            "coach_provenance": self._renderer.render_provenance(
                getattr(getattr(view_model, "coach", None), "provenance", None)
            ),
            "revision_provenance": self._renderer.render_provenance(
                getattr(view_model, "revision_provenance", None)
            ),
        }
        # Prefer hero action key, then continuous-journey / quick-action keys.
        resolved_key = (primary_action_key or "").strip()
        if not resolved_key:
            hero = getattr(view_model, "hero", None)
            resolved_key = (getattr(hero, "action_key", None) or "").strip()
        if not resolved_key:
            quick = tuple(getattr(view_model, "quick_actions", ()) or ())
            for action in quick:
                key = (getattr(action, "action_key", None) or "").strip()
                if key and key != "return_home":
                    resolved_key = key
                    break
            else:
                resolved_key = "begin_session"
        context["primary_action_key"] = resolved_key
        context["primary_cta_href"] = primary_cta_href(
            resolved_key,
            student_id=student_id,
            session_id=session_id,
        )
        banner = continuity or continuity_from_query(
            from_surface=from_surface,
            updated=updated,
        )
        success = (experience_success_message or "").strip() or None
        readiness = (readiness_change_message or "").strip() or None
        if banner is not None:
            success = success or banner.success_message
            readiness = readiness or (banner.readiness_hint or None)
            context["continuity"] = banner
            context["fragments"]["success_toast"] = self._renderer.render_toast(
                Toast(message=banner.success_message, tone=ToastTone.SUCCESS)
            )
        else:
            context["continuity"] = None
        context["readiness_change_message"] = readiness
        context["experience_success_message"] = success
        milestones = tuple(getattr(view_model, "upcoming_milestones", ()) or ())
        if not milestones or (
            len(milestones) == 1
            and "appear" in (getattr(milestones[0], "detail", "") or "").lower()
        ):
            context["fragments"]["milestones_empty"] = (
                self._renderer.render_empty_state(
                    EmptyState(
                        title="No upcoming milestones yet",
                        description=(
                            "Milestones appear once a study plan is active and "
                            "session outcomes start updating your journey."
                        ),
                        action_label="Continue today's mission to build this view.",
                    )
                )
            )
        else:
            context["fragments"]["milestones_empty"] = ""
        context["fragments"]["dashboard_skeleton"] = self._renderer.render_skeleton(
            Skeleton(
                variant=SkeletonVariant.CARD,
                label="Preparing your learning overview",
            )
        )
        return context

    def for_mission(
        self,
        view_model: MissionWorkspaceViewModel,
        *,
        student_id: str = "",
    ) -> dict[str, Any]:
        context = TemplateMapper.for_mission(view_model)
        context.update(self._chrome(student_id=student_id))
        context["fragments"] = {
            "provenance": self._renderer.render_provenance(
                getattr(view_model, "provenance", None)
            )
        }
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
            "provenance": self._renderer.render_provenance(
                getattr(view_model, "provenance", None)
                or getattr(
                    getattr(view_model, "reflection_summary", None),
                    "provenance",
                    None,
                )
            ),
        }
        if view_model.primary_button is not None:
            context["fragments"]["primary_button"] = self._renderer.render_button(
                view_model.primary_button
            )
        return context

    def for_experience_surface(
        self,
        view_model: Any,
        *,
        student_id: str = "",
        readiness_change_message: str | None = None,
        experience_success_message: str | None = None,
    ) -> dict[str, Any]:
        """Build template context for Journey / Readiness / Coach pages."""
        context = TemplateMapper.for_experience_surface(view_model)
        context.update(self._chrome(student_id=student_id))
        readiness = (readiness_change_message or "").strip() or None
        success = (experience_success_message or "").strip() or None
        if not readiness:
            readiness = (
                getattr(view_model, "readiness_change_message", None) or ""
            ).strip() or None
        if not success:
            success = (
                getattr(view_model, "success_message", None) or ""
            ).strip() or None
        context["readiness_change_message"] = readiness
        context["experience_success_message"] = success
        action_key = (getattr(view_model, "action_key", None) or "").strip()
        context["primary_action_key"] = action_key or "return_home"
        context["primary_cta_href"] = primary_cta_href(
            context["primary_action_key"],
            student_id=student_id,
        )
        if getattr(view_model, "empty", False):
            context["fragments"] = {
                "empty_state": self._renderer.render_empty_state(
                    EmptyState(
                        title=getattr(view_model, "title", None) or "Not ready yet",
                        description=(
                            getattr(view_model, "empty_reason", None)
                            or "This view updates as you study."
                        ),
                        action_label=(
                            getattr(view_model, "action_label", None) or ""
                        ).strip()
                        or "Return home",
                    )
                ),
                "provenance": self._renderer.render_provenance(
                    getattr(view_model, "provenance", None)
                ),
            }
        else:
            context["fragments"] = {
                "empty_state": "",
                "provenance": self._renderer.render_provenance(
                    getattr(view_model, "provenance", None)
                ),
            }
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
        key = (student_id or "", session_id or "")
        cached = self._chrome_cache.get(key)
        if cached is not None:
            return dict(cached)
        chrome = {
            "token_css": self._renderer.token_style_tag(),
            "nav": student_flow_nav(student_id=student_id, session_id=session_id),
            "student_id": student_id,
        }
        self._chrome_cache[key] = chrome
        return dict(chrome)

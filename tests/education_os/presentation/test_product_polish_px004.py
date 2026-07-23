"""PX-004 product polish — continuity, motion, feedback rendering, performance."""

from __future__ import annotations

from adapters.flask.page_renderer import PageRenderer
from adapters.flask.rendering import ComponentRenderer
from application.pipeline import EducationalPipeline, PipelineResult
from presentation.dashboard import DashboardPresenter
from presentation.design_system import (
    MOTION,
    EmptyState,
    LoadingState,
    MotionToken,
    Skeleton,
    SkeletonVariant,
    Toast,
    ToastTone,
)
from presentation.polish import (
    COMPLETION_FLOW_STEPS,
    continuity_from_query,
    success_reward_message,
)
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


def test_page_motion_tokens_match_ux001_durations() -> None:
    assert MotionToken.PAGE in MOTION
    assert MOTION[MotionToken.PAGE].duration_ms == 250
    assert MOTION[MotionToken.SIDEBAR].duration_ms == 220
    assert MOTION[MotionToken.TOOLTIP].duration_ms == 120
    assert set(MotionToken) == set(MOTION)


def test_completion_flow_steps_are_continuous() -> None:
    assert COMPLETION_FLOW_STEPS == (
        "Reflection",
        "Journey",
        "Readiness",
        "Coach",
        "Home",
    )


def test_continuity_from_reflection_query() -> None:
    banner = continuity_from_query(from_surface="reflection", updated="1")
    assert banner is not None
    assert banner.origin == "reflection"
    assert banner.active_step == "Home"
    assert "Reflection saved" in banner.success_message
    assert "Readiness" in banner.readiness_hint


def test_success_reward_messages_are_professional() -> None:
    message = success_reward_message("reflection")
    assert message is not None
    assert "streak" not in message.lower()
    assert "badge" not in message.lower()
    assert "xp" not in message.lower()


def test_empty_state_and_skeleton_render_accessible_html() -> None:
    renderer = ComponentRenderer()
    empty = renderer.render_empty_state(
        EmptyState(
            title="No upcoming milestones yet",
            description="Milestones appear once a study plan is active.",
            action_label="Continue today's mission.",
        )
    )
    assert 'data-empty-state="true"' in empty
    assert 'role="status"' in empty
    assert "No upcoming milestones yet" in empty
    assert "study plan is active" in empty

    skeleton = renderer.render_skeleton(
        Skeleton(variant=SkeletonVariant.CARD, label="Preparing overview")
    )
    assert 'data-skeleton="card"' in skeleton
    assert 'aria-busy="true"' in skeleton
    assert "Preparing overview" in skeleton

    toast = renderer.render_toast(
        Toast(message="Reflection saved.", tone=ToastTone.SUCCESS)
    )
    assert 'data-toast-tone="success"' in toast
    assert "Reflection saved." in toast

    loading = renderer.render_loading_state(LoadingState(label="Loading dashboard"))
    assert 'data-loading-state="true"' in loading
    assert "Loading dashboard" in loading


def test_dashboard_page_renderer_skips_unused_fragments() -> None:
    result: PipelineResult = EducationalPipeline().run(make_pipeline_request())
    view = DashboardPresenter.present(result)
    renderer = PageRenderer()
    context = renderer.for_dashboard(
        view,
        student_id="student-1",
        from_surface="reflection",
        updated="1",
    )
    fragments = context["fragments"]
    assert "header" not in fragments
    assert "greeting" not in fragments
    assert "progress_bar" not in fragments
    assert "mission_card" in fragments
    assert context["experience_success_message"]
    assert context["continuity"] is not None
    assert context["continuity"].origin == "reflection"
    assert "milestones_empty" in fragments

    # Token stylesheet cached across chrome reuse.
    first = renderer.renderer.token_style_tag()
    second = renderer.renderer.token_style_tag()
    assert first is second


def test_empty_state_explains_why() -> None:
    empty = EmptyState(
        title="Coach insight pending",
        description=(
            "Coach guidance stays quiet until there is enough session evidence "
            "to speak accurately."
        ),
    )
    assert "until" in empty.description.lower() or "enough" in empty.description.lower()
    a11y = empty.accessibility()
    assert a11y.role == "status"
    assert a11y.reduced_motion_safe is False or a11y.label_required

"""RR-001.1 — Critical Home honesty remediations (JR-06 / JR-07)."""

from __future__ import annotations

from dataclasses import replace
from types import SimpleNamespace

from flask import render_template

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import HomeSnapshot
from app.application.unified_journey import (
    COMPLETION_COMPLETE,
    DailyMission,
    DayExperienceAssembler,
    MissionStartAction,
    SessionPhase,
)
from app.presentation.student.view_models import (
    ReflectionPromptViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)
from app.services.learning_lifecycle_service import LearningLifecycleService
from tests.test_v1sp001a_learning_lifecycle import (
    _complete_all_topics,
    _make_active_plan,
    _make_curriculum,
)


def _base_snap(**overrides) -> HomeSnapshot:
    data = dict(
        student_id="stu-1",
        greeting="Welcome back",
        examination_label="ACCA AA",
        exam_countdown_days=30,
        exam_readiness=0.62,
        exam_readiness_label="Exam Readiness",
        recommendation_title="Cash flow statements",
        recommendation_summary="Focus on cash flow statements next.",
        estimated_study_minutes=25,
        explanation=ExplanationSnapshot(
            summary="Focus on cash flow statements next.",
            why_recommended="Soft recall on cash flow statements.",
            evidence_points=("Recent practice below average.",),
            expected_benefit="Strengthen exam readiness on cash flow analysis.",
            confidence_label="Suggested",
            suggested_next_action="Start a 25-minute cash flow practice session.",
            review_point="Reassess after tonight's practice set.",
            confidence_basis="Based on recent practice outcomes.",
            is_complete=True,
        ),
        has_recommendation=True,
        can_start_session=False,
    )
    data.update(overrides)
    return HomeSnapshot(**data)


def _render_home(app, page_home, **template_kwargs):
    page = SimpleNamespace(
        home=page_home,
        shell=SimpleNamespace(active_surface="home", navigation=()),
        educational=None,
    )
    with app.test_request_context("/student/"):
        return render_template(
            "student/home.html",
            page=page,
            form=None,
            **template_kwargs,
        )


def test_guided_reflection_preview_has_no_false_controls(app, ctx):
    """JR-06 / IR-03: remove Done reflecting / Skip for today fake actions."""
    mission = DailyMission(
        title="Revise equity",
        reason="High educational return",
        estimated_duration="25 minutes",
        expected_outcome="Strengthen readiness",
        completion_status=COMPLETION_COMPLETE,
        start_action=MissionStartAction(enabled=False, label="Start"),
        mission_summary="High educational return",
        metadata=(("availability", "available"),),
    )
    day = DayExperienceAssembler().assemble(
        mission,
        phase=SessionPhase.COMPLETE,
    )
    assert day.reflection_active is True

    from app.presentation.student import view_models as vm_mod

    reflection = vm_mod._home_reflection(day, enabled=True)
    page_home = replace(
        home_vm(_base_snap(), unified_journey=True),
        reflection_active=True,
        reflection_state=(
            day.reflection_state.value if day.reflection_state else ""
        ),
        reflection_headline=reflection.headline,
        reflection_supporting_message=reflection.supporting_message,
        reflection_next_transition=reflection.next_transition,
        reflection_skip_available=True,
        reflection_prompts=tuple(
            ReflectionPromptViewModel(
                prompt=item.prompt,
                response_type=item.response_type,
                available_options=tuple(item.available_options or ()),
                optional_note_placeholder=item.optional_note_placeholder or "",
            )
            for item in reflection.prompts
        ),
        unified_journey_enabled=True,
    )

    html = _render_home(app, page_home)
    assert "Done reflecting" not in html
    assert "Skip for today" not in html
    assert 'data-reflection-control="complete"' not in html
    assert 'data-reflection-control="skip"' not in html
    assert 'data-reflection-honesty="preview-only"' in html
    assert "nothing here is recorded" in html


def test_student_home_shows_revision_acknowledgement(
    app, client, db, user, monkeypatch
):
    """JR-07: syllabus-complete ack reachable on sole-runtime Student Home."""
    monkeypatch.setenv("KWALITEC_V2_SOLE_RUNTIME", "1")
    monkeypatch.setenv("KWALITEC_V2_STUDENT_EXPERIENCE", "1")

    curriculum, topics = _make_curriculum("CM1-RR", ["A", "B"])
    plan = _make_active_plan(user.id, curriculum=curriculum)
    _complete_all_topics(user.id, topics)
    lifecycle = LearningLifecycleService.resolve(user.id, study_plan=plan)
    assert lifecycle.show_completion_acknowledgement is True

    with client.session_transaction() as sess:
        sess["_user_id"] = str(user.id)
        sess["_fresh"] = True

    from app.presentation.student import views as student_views

    empty_home = home_vm(_base_snap(can_start_session=False), unified_journey=False)
    stub_page = StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=empty_home,
    )
    monkeypatch.setattr(student_views, "load_page", lambda *_a, **_k: stub_page)
    monkeypatch.setattr(
        "app.services.alpha_onboarding_service.AlphaOnboardingService.should_show",
        lambda *_a, **_k: False,
    )

    response = client.get("/student/")
    assert response.status_code == 200
    body = response.get_data(as_text=True)
    assert 'data-lifecycle="revision-ack"' in body
    assert lifecycle.acknowledgement_title in body
    assert "revision/acknowledge" in body

    ack = client.post("/dashboard/revision/acknowledge", follow_redirects=True)
    assert ack.status_code == 200
    db.session.refresh(plan)
    assert plan.revision_acknowledged is True

"""UX-001 — Premium Closed Beta presentation contracts."""

from __future__ import annotations

from pathlib import Path

from app.application.student_experience.dto.explanation_snapshot import (
    ExplanationSnapshot,
)
from app.application.student_experience.dto.home_snapshot import (
    HomeSnapshot,
    StartSessionActionSnapshot,
)
from app.presentation.student.services.student_home_service import (
    StudentHomeService,
)
from app.presentation.student.view_models import (
    StudentPageViewModel,
    StudentShellViewModel,
    home_vm,
)

ROOT = Path(__file__).resolve().parents[3]


def _page(home_vm_obj) -> StudentPageViewModel:
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home_vm_obj,
    )


def test_home_mission_includes_duration_and_title(app, ctx):
    home = home_vm(
        HomeSnapshot(
            student_id="1",
            greeting="Welcome",
            examination_label="CS1",
            has_recommendation=True,
            recommendation_title="Conditional probability",
            can_start_session=True,
            estimated_study_minutes=25,
            explanation=ExplanationSnapshot(
                summary="Practice conditional probability.",
                why_recommended="Builds on recent weak recall.",
                evidence_points=("Recent practice below average.",),
                expected_benefit="Strengthen readiness.",
                confidence_label="Suggested",
                suggested_next_action="Start a focused practice session.",
                review_point="Reassess after practice.",
                confidence_basis="Based on recent practice.",
                is_complete=True,
            ),
            start_session=StartSessionActionSnapshot(
                label="Start Session",
                enabled=True,
                can_start=True,
                mission_id="m1",
                topic_title="Conditional probability",
                estimated_minutes=25,
            ),
        ),
        unified_journey=False,
    )
    with app.test_request_context("/student/"):
        page = StudentHomeService().build_home(_page(home))
    assert page.state == "mission"
    assert page.mission is not None
    assert page.mission.duration_label
    assert page.mission.title
    assert page.page_question == "What should I do now?"
    assert page.signals is not None
    assert page.signals.subject_label == "CS1"
    # UX-001: duration lives on the mission hero, not the progress strip.
    assert not page.signals.estimated_study_label
    assert page.mission is not None
    assert page.mission.duration_label
    assert page.greeting


def test_design_system_includes_ux001_surfaces():
    css = (ROOT / "app/static/css/design_system.css").read_text(encoding="utf-8")
    assert ".ds-os-signals" in css
    assert ".ds-mission-chip" in css
    assert ".ds-session-reading-progress" in css
    assert ".ds-kg-list" in css
    assert "body.ds-focus-mode" in css


def test_eos_footer_has_beta_affordance():
    html = (
        ROOT / "app/templates/layouts/eos_student.html"
    ).read_text(encoding="utf-8")
    assert "Private Beta" in html
    assert "Report issue" in html
    assert "Release notes" in html


def test_tutor_and_knowledge_graph_routes_registered(app):
    rules = {rule.endpoint for rule in app.url_map.iter_rules()}
    assert "student.tutor" in rules
    assert "student.knowledge_graph" in rules
    assert "founder_dashboard.curriculum_health" in rules
    assert "founder_dashboard.beta" in rules
    assert "alpha.feedback_beta" in rules

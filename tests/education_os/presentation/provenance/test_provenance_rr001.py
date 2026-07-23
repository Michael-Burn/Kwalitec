"""RR-001 Explainability & Trust — provenance model and surface integration."""

from __future__ import annotations

from types import SimpleNamespace

from adapters.flask.page_renderer import PageRenderer
from adapters.flask.rendering import ComponentRenderer
from application.pipeline import EducationalPipeline
from presentation.dashboard import DashboardPresenter
from presentation.mission_workspace import WorkspacePresenter
from presentation.provenance import (
    MAX_PROVENANCE_REASONS,
    ProvenanceKind,
    ProvenanceMapper,
    ProvenanceReasonView,
    ProvenanceViewModel,
    narrate_reason_code,
)
from presentation.reflection import ReflectionPresenter
from tests.education_os.application.pipeline.test_educational_pipeline import (
    make_pipeline_request,
)


def _pipeline_result():
    return EducationalPipeline().run(make_pipeline_request())


def test_provenance_view_model_caps_at_three_reasons() -> None:
    reasons = tuple(
        ProvenanceReasonView(
            kind=ProvenanceKind.WEAK_TOPIC.value,
            sentence=f"Reason number {index}.",
        )
        for index in range(1, 6)
    )
    view = ProvenanceViewModel.from_reasons(reasons)
    assert view.reason_count == MAX_PROVENANCE_REASONS
    assert view.available
    assert len(view.sentences) == 3


def test_provenance_view_model_null_safe_empty() -> None:
    empty = ProvenanceViewModel.empty(surface="mission")
    assert not empty.available
    assert empty.reasons == ()
    assert empty.as_accordion().panels[0].body == ""


def test_narrate_reason_code_uses_existing_codes_only() -> None:
    assert narrate_reason_code("weak_prerequisite") is not None
    assert "prerequisite" in narrate_reason_code("weak_prerequisite").lower()
    assert narrate_reason_code("invented_new_concept") is None


def test_mission_provenance_from_pipeline() -> None:
    result = _pipeline_result()
    workspace = WorkspacePresenter.present(result)
    assert workspace.provenance is not None
    assert workspace.provenance.surface == "mission"
    assert workspace.provenance.reason_count <= MAX_PROVENANCE_REASONS
    for reason in workspace.provenance.reasons:
        assert reason.sentence.endswith((".", "!", "?"))
        assert "\n" not in reason.sentence


def test_dashboard_provenance_on_hero_and_panels() -> None:
    result = _pipeline_result()
    view = DashboardPresenter.present(result)
    assert view.hero.provenance is not None
    assert view.hero.provenance.surface == "dashboard"
    assert view.readiness.provenance is not None
    assert view.journey.provenance is not None
    assert view.coach.provenance is not None
    assert view.revision_provenance is not None
    assert view.coach.provenance.surface == "coach"


def test_journey_and_readiness_provenance_mappers() -> None:
    experience = SimpleNamespace(
        journey_snapshot=SimpleNamespace(
            trajectory_message="Mastery trend is improving across recent sessions.",
            consistency_message="Study consistency has been steady this week.",
            habits_message="Morning study remains your preferred habit.",
            home_focus_headline=None,
        ),
        readiness_snapshot=SimpleNamespace(
            direction_message="Readiness is holding steady.",
            assessment_confidence_label="Evidence confidence is building.",
            journey_trajectory_message=(
                "Mastery trend supports the current readiness band."
            ),
            days_remaining=21,
            readiness_available=True,
        ),
        coach_snapshot=None,
        coach=None,
        home=None,
        home_snapshot=None,
        todays_focus=None,
        primary_focus=None,
    )
    journey = ProvenanceMapper.for_journey(experience)
    readiness = ProvenanceMapper.for_readiness(experience)
    assert journey.available
    assert journey.surface == "journey"
    assert readiness.available
    assert readiness.reason_count <= MAX_PROVENANCE_REASONS
    assert readiness.reason_count >= 1
    kinds = {reason.kind for reason in readiness.reasons}
    assert (
        ProvenanceKind.READINESS.value in kinds
        or ProvenanceKind.MASTERY_TREND.value in kinds
    )


def test_coach_provenance_consumes_shared_evidence() -> None:
    result = _pipeline_result()
    experience = SimpleNamespace(
        coach=SimpleNamespace(
            explanation_cards=SimpleNamespace(
                cards=(
                    SimpleNamespace(
                        body="Mission purpose: revise a weak topic identified recently."
                    ),
                    SimpleNamespace(
                        body="Readiness reasoning: evidence freshness remains limited."
                    ),
                )
            )
        ),
        coach_snapshot=SimpleNamespace(
            focus_headline="Focus on foundation practice.",
            journey_message="Journey momentum is improving.",
            readiness_label="Developing",
        ),
        home=None,
        home_snapshot=None,
        todays_focus=None,
        primary_focus=None,
        journey_snapshot=None,
        readiness_snapshot=None,
    )
    coach = ProvenanceMapper.for_coach(experience, result=result)
    assert coach.available
    assert coach.surface == "coach"
    assert coach.reason_count <= MAX_PROVENANCE_REASONS


def test_revision_provenance_from_existing_explanation() -> None:
    revision = SimpleNamespace(
        primary=SimpleNamespace(
            explanation=SimpleNamespace(
                why_recommended=(
                    "It has been a while since you last revisited this topic."
                ),
                evidence_points=(
                    "Recall has softened on this topic.",
                    "Revision spacing suggests a short review now.",
                    "Exam proximity raises the value of this revision.",
                    "Extra fourth reason must be dropped.",
                ),
                expected_benefit="Protect recent learning.",
            ),
            expected_benefit="Protect recent learning.",
            priority_label="High priority",
        )
    )
    view = ProvenanceMapper.for_revision(revision)
    assert view.available
    assert view.surface == "revision"
    assert view.reason_count <= MAX_PROVENANCE_REASONS


def test_reflection_provenance_null_safe() -> None:
    view = ReflectionPresenter.present(None, None)
    assert view.provenance is not None
    # Without captured evidence, provenance may be empty — never raises.
    assert view.provenance.reason_count <= MAX_PROVENANCE_REASONS
    assert view.reflection_summary.provenance is view.provenance or (
        view.reflection_summary.provenance is not None
    )


def test_provenance_html_is_accessible_and_collapsible() -> None:
    provenance = ProvenanceViewModel.from_reasons(
        (
            ProvenanceReasonView(
                kind=ProvenanceKind.WEAK_TOPIC.value,
                sentence=(
                    "A weak topic was identified in your recent learning evidence."
                ),
            ),
            ProvenanceReasonView(
                kind=ProvenanceKind.MASTERY_TREND.value,
                sentence=(
                    "Mastery is developing, so continued practice is warranted."
                ),
            ),
        ),
        title="Why this mission",
        surface="mission",
    )
    html = ComponentRenderer().render_provenance(provenance)
    assert 'data-provenance="true"' in html
    assert "<details" in html
    assert "<summary" in html
    assert "Why this mission" in html
    assert "weak topic" in html.lower()
    assert ComponentRenderer().render_provenance(None) == ""
    assert ComponentRenderer().render_provenance(ProvenanceViewModel.empty()) == ""


def test_page_renderer_includes_dashboard_provenance_fragments() -> None:
    result = _pipeline_result()
    view = DashboardPresenter.present(result)
    context = PageRenderer().for_dashboard(view, student_id="student-1")
    fragments = context["fragments"]
    assert "hero_provenance" in fragments
    assert "readiness_provenance" in fragments
    assert "journey_provenance" in fragments
    assert "coach_provenance" in fragments
    assert "revision_provenance" in fragments


def test_mission_page_renderer_includes_provenance_fragment() -> None:
    result = _pipeline_result()
    workspace = WorkspacePresenter.present(result)
    context = PageRenderer().for_mission(workspace, student_id="student-1")
    html = context["fragments"]["provenance"]
    if workspace.provenance and workspace.provenance.available:
        assert 'data-provenance="true"' in html
        assert "<details" in html

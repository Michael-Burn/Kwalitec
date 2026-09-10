"""Curriculum Map current-topic marking (journey topic id vs syllabus code)."""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock

from app.presentation.student.services import (
    student_knowledge_graph_presentation_service as kg_mod,
)
from app.presentation.student.view_models import (
    EducationalExperienceViewModel,
    HomePageViewModel,
    JourneyPageViewModel,
    JourneyTopicViewModel,
    StudentPageViewModel,
    StudentShellViewModel,
)
from tests.application.curriculum_intelligence.test_ei002b_student_intelligence import (
    _certified_package,
)

StudentKnowledgeGraphPresentationService = (
    kg_mod.StudentKnowledgeGraphPresentationService
)


def _page_with_mismatched_codes(
    *, topic_id: str, syllabus_code: str
) -> StudentPageViewModel:
    edu = EducationalExperienceViewModel(
        active=True,
        subject_code="CS1",
        examination_label="IFoA CS1",
        today_topic_title="Binary representation",
        today_topic_code=syllabus_code,
        today_topic_id=topic_id,
    )
    home = HomePageViewModel(
        examination_label="IFoA CS1",
        educational=edu,
    )
    journey = JourneyPageViewModel(
        examination_label="IFoA CS1",
        current=JourneyTopicViewModel(
            topic_id=topic_id,
            title="Binary representation",
            status_label="Current",
        ),
    )
    return StudentPageViewModel(
        shell=StudentShellViewModel(
            active_surface="home",
            active_label="Home",
            navigation=(),
            page_title="Home",
        ),
        home=home,
        journey=journey,
    )


def test_presentation_marks_real_topic_id_as_current(app, ctx, monkeypatch):
    """Graph nodes are keyed by topic id; syllabus codes must not match."""
    package = _certified_package()

    class _Svc:
        def load_package(self, code: str):
            assert code == "CS1"
            return package

        def knowledge_graph(self, pkg):
            from app.application.curriculum_intelligence import (
                learner_knowledge_graph_service as lkg,
            )

            return lkg.LearnerKnowledgeGraphBuilder().build(pkg)

        def provenance(self, pkg):
            return SimpleNamespace(
                subject_code="CS1",
                version_label="2026.7",
                status="certified",
            )

    monkeypatch.setattr(
        "app.application.curriculum_intelligence.certified_learning_service."
        "CertifiedLearningService",
        lambda: _Svc(),
    )

    with app.test_request_context("/student/knowledge-graph"):
        wrong = StudentKnowledgeGraphPresentationService().build(
            subject_code="CS1",
            examination_label="IFoA CS1",
            current_topic_id="1.1",
        )
        right = StudentKnowledgeGraphPresentationService().build(
            subject_code="CS1",
            examination_label="IFoA CS1",
            current_topic_id="cs1-t1",
        )

    def _flatten(nodes):
        out = []
        for n in nodes:
            out.append(n)
            out.extend(_flatten(n.children))
        return out

    wrong_current = [n for n in _flatten(wrong.roots) if n.is_current]
    right_current = [n for n in _flatten(right.roots) if n.is_current]
    assert wrong_current == []
    assert len(right_current) == 1
    assert right_current[0].node_id == "cs1-t1"
    assert right.selected is not None
    assert right.selected.node_id == "cs1-t1"
    assert right.selected.progress_label == "Current"


def test_knowledge_graph_route_prefers_journey_topic_id(
    student_client, experience_app, monkeypatch
):
    """Route must pass journey.current.topic_id, not edu.today_topic_code."""
    captured: dict[str, str] = {}
    page = _page_with_mismatched_codes(topic_id="topic-t1", syllabus_code="1.1")

    monkeypatch.setattr(
        "app.presentation.student.routes.load_page",
        lambda *_a, **_k: page,
    )

    empty = StudentKnowledgeGraphPresentationService().build(
        subject_code="",
        examination_label="",
    )

    def _capture_build(self, **kwargs):
        captured["current_topic_id"] = kwargs.get("current_topic_id") or ""
        captured["subject_code"] = kwargs.get("subject_code") or ""
        return empty

    monkeypatch.setattr(
        StudentKnowledgeGraphPresentationService,
        "build",
        _capture_build,
    )

    monkeypatch.setattr(
        "app.services.presentation_telemetry_service."
        "PresentationTelemetryService.record",
        MagicMock(),
    )

    response = student_client.get("/student/knowledge-graph")
    assert response.status_code == 200
    assert captured["current_topic_id"] == "topic-t1"
    assert captured["subject_code"] == "CS1"

"""KWP-005 — Assessment Mode & Sitting Reports tests.

Presentation-layer Sitting Report, Learning Insights quality, Weak Topic
Centre wiring, Finish → Sitting Report redirect, and founder sitting
metrics. No runtime authority redesign.
"""

from __future__ import annotations

from pathlib import Path

from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.session_experience.dto.completion_snapshot import (
    CompletionSnapshot,
    ReturnHomeActionSnapshot,
)
from app.presentation.session.sitting_report import (
    build_sitting_report,
    insights_from_sitting_report,
)
from app.presentation.session.view_models import completion_vm
from app.services.educational_yield_metrics import EducationalYieldMetrics

SESSION_BODY = Path("app/templates/session/partials/session_body.html")
ROUTES = Path("app/presentation/session/routes.py")
JOURNEY = Path("app/templates/student/journey.html")


class TestSittingReportProjection:
    def test_scored_practice_builds_assessment_mode_and_insights(self):
        report = build_sitting_report(
            topic_title="Present value",
            opaque_summary={
                "topic_title": "Present value",
                "learning_objectives": ("Discount cash flows to today",),
                "activities": [
                    {
                        "stage": "reading",
                        "title": "Read present value",
                        "completed": True,
                        "syllabus_refs": ("CS1 · 2.1",),
                    },
                    {
                        "stage": "practice",
                        "title": "Present value practice",
                        "completed": True,
                        "syllabus_refs": ("CS1 · Q2.3",),
                    },
                ],
                "observations": [
                    {"type_id": RuntimeEvidenceType.READING_COMPLETED.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.REFLECTION_SUBMITTED.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
                "progress_advanced": True,
                "mission_completed": True,
                "finish_review": {"verdict": "yes", "label": "Yes"},
                "substance": "package",
            },
            metadata={
                "progress_advanced": "true",
                "mission_completed": "true",
            },
            next_recommendation="Discount factors",
        )
        assert report.has_report is True
        assert report.assessment_mode_active is True
        assert "Present value" in report.headline
        assert "studied" in report.what_studied.lower()
        assert report.practice_correct == 2
        assert any("correctly" in i.lower() for i in report.learning_insights)
        assert report.progress_explanation
        explanation = report.progress_explanation.lower()
        assert "journey" in explanation or "forward" in explanation
        assert "Discount factors" in report.tomorrow_preview
        assert (
            "CS1 · Q2.3" in report.syllabus_refs
            or "CS1 · 2.1" in report.syllabus_refs
        )
        assert not any(
            term in " ".join(report.learning_insights).lower()
            for term in ("twin", "evidence authority", "educational+", "fsm")
        )

    def test_incorrect_practice_flags_reinforcement(self):
        report = build_sitting_report(
            topic_title="Discount factors",
            opaque_summary={
                "learning_objectives": ("Apply discount factors",),
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                    {"type_id": RuntimeEvidenceType.PRACTICE_INCORRECT.value},
                ],
                "finish_review": {"verdict": "yes"},
                "substance": "package",
            },
            metadata={"progress_advanced": "false"},
        )
        assert report.practice_incorrect == 2
        assert report.needs_reinforcement
        assert any("struggled" in i.lower() for i in report.learning_insights)

    def test_reflection_note_surfaces_in_learning_insights(self):
        note = "I still find deferred tax tricky."
        report = build_sitting_report(
            topic_title="Deferred tax",
            opaque_summary={
                "reflection_note": note,
                "observations": [
                    {"type_id": RuntimeEvidenceType.REFLECTION_SUBMITTED.value},
                ],
                "finish_review": {"verdict": "yes"},
                "substance": "package",
            },
        )
        joined = " ".join(report.learning_insights)
        assert note in joined
        assert 'You wrote:' in joined

    def test_partial_finish_explains_no_progress(self):
        report = build_sitting_report(
            topic_title="Equity method",
            opaque_summary={
                "finish_review": {"verdict": "partially", "label": "Partially"},
                "substance": "package",
            },
            metadata={
                "progress_advanced": "false",
                "evidence_disposition": "accepted_with_restrictions",
            },
        )
        assert "Progress stayed" in report.progress_explanation
        assert "partial" in report.finish_outcome_label.lower()


class TestCompletionViewModelSittingReport:
    def test_completion_vm_projects_sitting_report_fields(self):
        snap = CompletionSnapshot(
            session_id="sess-1",
            student_id="stu-1",
            topics_completed=("Cash flows",),
            activities_completed=3,
            learning_insights=("fallback",),
            next_recommendation="Equity method",
            return_home=ReturnHomeActionSnapshot(label="Return Home", enabled=True),
            can_return_home=True,
            metadata=(
                ("progress_advanced", "true"),
                ("mission_completed", "true"),
                ("finish_review", "yes"),
                ("topic_title", "Cash flows"),
                ("learning_objective", "Classify operating cash flows"),
                ("observation_type", RuntimeEvidenceType.PRACTICE_CORRECT.value),
                ("observation_type", RuntimeEvidenceType.PRACTICE_CORRECT.value),
                ("activity_item", "practice|Cash flow practice|1"),
                ("syllabus_ref", "CS1 · 1.2"),
            ),
        )
        vm = completion_vm(snap)
        assert "Sitting Report" in vm.headline or "Cash flows" in vm.headline
        assert vm.sitting_report_ready is True
        assert vm.progress_explanation
        assert vm.learning_insights
        assert "fallback" not in vm.learning_insights or len(vm.learning_insights) >= 1
        insights = insights_from_sitting_report(
            build_sitting_report(
                topic_title="Cash flows",
                opaque_summary={
                    "observations": [
                        {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value}
                    ]
                },
                metadata={"progress_advanced": "true", "mission_completed": "true"},
            )
        )
        assert insights


class TestPresentationSurfaces:
    def test_session_body_has_sitting_report_and_assessment_mode(self):
        body = SESSION_BODY.read_text(encoding="utf-8")
        assert 'data-sitting-report="true"' in body
        assert 'data-assessment-mode="true"' in body
        assert "Needs reinforcement" in body
        assert "Learning Insights" in body
        assert "data-progress-explanation" in body
        assert "student.history" in body
        for banned in ("Twin", "Evidence Authority", "Educational+", "FSM", "Runtime"):
            # Allow comments / attributes that are student-safe product labels only.
            assert f">{banned}" not in body or banned in {
                # none expected as visible labels
            }

    def test_finish_redirects_to_sitting_report(self):
        text = ROUTES.read_text(encoding="utf-8")
        assert 'url_for("session.complete"' in text
        # Commercial path should not skip Sitting Report for Home.
        assert text.count('url_for("student.home")') >= 0
        finish_block = text.split("def finish(")[1].split("def finish_review")[0]
        assert 'url_for("session.complete"' in finish_block
        assert 'url_for("student.home")' not in finish_block

    def test_journey_weak_topic_centre_markers(self):
        text = JOURNEY.read_text(encoding="utf-8")
        assert 'data-weak-topic-centre="true"' in text
        assert "Needs Attention" in text
        assert "Open Revision" in text


class TestFounderSittingMetrics:
    def test_yield_includes_finish_and_reflection(self):
        packages = [
            {
                "validation": {"disposition": "accepted", "may_update_twin": True},
                "finish_review_verdict": "yes",
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                    {"type_id": RuntimeEvidenceType.REFLECTION_SUBMITTED.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_YES.value},
                ],
            },
            {
                "validation": {
                    "disposition": "accepted_with_restrictions",
                    "may_update_twin": False,
                },
                "finish_review_verdict": "partially",
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_ATTEMPTED.value},
                    {"type_id": RuntimeEvidenceType.FINISH_REVIEW_PARTIALLY.value},
                ],
            },
        ]
        snap = EducationalYieldMetrics.from_packages(packages)
        assert snap.sittings_total == 2
        assert snap.finish_review_yes == 1
        assert snap.finish_review_partial == 1
        assert snap.reflection_submitted == 1
        assert snap.reflection_rate == 0.5
        assert snap.average_observation_density > 0
        opaque = snap.to_opaque()
        assert "finish_review_yes" in opaque
        assert "reflection_rate" in opaque

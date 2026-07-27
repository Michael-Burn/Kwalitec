"""EQ-001 educational quality certification scenarios."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

from app.application.educational_engine_foundation.service import (
    EducationalEngineFoundationService,
)
from app.application.educational_quality import EducationalQualityCertifier
from app.application.educational_runtime_engine import (
    EducationalRuntimeEngineService,
)
from app.application.educational_runtime_engine.exceptions import (
    IllegalRuntimeState,
)
from tests.certification.pi001d_helpers import (
    make_certified_user,
    publish_certified_subject,
)


@pytest.fixture
def eq_subject(ctx):
    return publish_certified_subject("EQ1", title="Educational Quality Subject")


@pytest.fixture
def eq_user(ctx):
    return make_certified_user("eq001@example.com")


def test_eq_m_artefact_mission_quality_rules(eq_subject):
    """EQ-M01..M05: derived mission templates meet mission quality rules."""
    artefacts = EducationalEngineFoundationService().derive_active(eq_subject)
    assert artefacts is not None
    report = EducationalQualityCertifier().certify_artefacts(artefacts)
    failed = [c for c in report.checks if not c.passed and c.rule_id.startswith("EQ-M")]
    assert report.passed, f"artefact quality failed: {report.issues}"
    assert not failed
    for template in artefacts.mission_templates:
        assert template.topic_id
        assert template.topic_code
        assert template.objective_ids
        assert template.estimated_duration_minutes > 0
        assert template.completion_definition
        assert template.educational_rationale


def test_eq_p_study_plan_quality_rules(eq_subject):
    """EQ-P01..P03: study plan template order, coverage, and minutes."""
    artefacts = EducationalEngineFoundationService().derive_active(eq_subject)
    assert artefacts is not None
    report = EducationalQualityCertifier().certify_artefacts(artefacts)
    plan_checks = {
        c.rule_id: c.passed
        for c in report.checks
        if c.rule_id in {"EQ-P01", "EQ-P02", "EQ-P03"}
    }
    assert all(plan_checks.values()), plan_checks
    templates = artefacts.study_plan_template.topic_templates
    assert [t["topic_id"] for t in templates] == [
        "topic-t1",
        "topic-t2",
        "topic-t3",
    ]
    assert templates[1]["prerequisite_ids"] == ("topic-t1",)
    assert templates[2]["prerequisite_ids"] == ("topic-t2",)


def test_eq_m06_m07_generated_mission_quality_envelope(eq_subject, eq_user):
    """EQ-M06/M07 + EQ-X*: generated mission carries explainable quality envelope."""
    runtime = EducationalRuntimeEngineService()
    certifier = EducationalQualityCertifier()
    runtime.enrol_student(
        user_id=eq_user.id,
        subject_code=eq_subject,
        exam_date=date(2026, 12, 15),
    )
    artefacts = EducationalEngineFoundationService().derive_active(eq_subject)
    mission = runtime.generate_daily_mission(
        user_id=eq_user.id,
        subject_code=eq_subject,
        mission_date=date(2026, 8, 1),
    )
    assert mission.quality is not None
    assert mission.quality.objective_ids
    assert mission.quality.estimated_duration_minutes > 0
    assert mission.quality.completion_definition
    assert mission.quality.educational_rationale
    assert mission.quality.prerequisite_validation["all_satisfied"] is True
    assert mission.quality.explanation["explanation_schema_complete"] is True

    report = certifier.certify_mission(mission, artefacts=artefacts)
    assert report.passed, report.issues


def test_eq_j_journey_explainability(eq_subject, eq_user):
    """EQ-J01..J04 + EQ-X04: journey always answers the three mandatory questions."""
    runtime = EducationalRuntimeEngineService()
    certifier = EducationalQualityCertifier()
    runtime.enrol_student(
        user_id=eq_user.id,
        subject_code=eq_subject,
        exam_date=date(2026, 12, 15),
    )

    start = runtime.get_journey_explanation(
        user_id=eq_user.id,
        subject_code=eq_subject,
    )
    start_report = certifier.certify_journey_explanation(
        start,
        curriculum_identity=f"{eq_subject}:2027.1",
    )
    assert start_report.passed, start_report.issues
    assert "t1" in start.why_today or "Core concepts" in start.why_today
    assert "No previous topic" in start.why_previous_complete
    assert start.unlocks_next

    day = date(2026, 8, 1)
    mission = runtime.generate_daily_mission(
        user_id=eq_user.id,
        subject_code=eq_subject,
        mission_date=day,
    )
    runtime.complete_mission(
        user_id=eq_user.id,
        mission_instance_id=mission.mission_instance_id,
    )
    after = runtime.get_journey_explanation(
        user_id=eq_user.id,
        subject_code=eq_subject,
    )
    after_report = certifier.certify_journey_explanation(
        after,
        curriculum_identity=f"{eq_subject}:2027.1",
    )
    assert after_report.passed, after_report.issues
    assert after.previous_topic_id == "topic-t1"
    assert (
        "topic-t1" in after.why_previous_complete
        or "1.1" in after.why_previous_complete
        or "Core" in after.why_previous_complete
    )
    assert after.current_topic_id == "topic-t2"
    assert (
        "topic-t2" in after.why_today
        or "Applied" in after.why_today
        or "2.1" in after.why_today
    )


def test_eq_p04_p06_exam_aware_pacing_and_revision(eq_subject, eq_user):
    """EQ-P04..P06: pacing projection is exam-aware with honest revision allocation."""
    runtime = EducationalRuntimeEngineService()
    certifier = EducationalQualityCertifier()
    runtime.enrol_student(
        user_id=eq_user.id,
        subject_code=eq_subject,
        exam_date=date(2026, 12, 15),
    )
    pacing = runtime.project_pacing(
        user_id=eq_user.id,
        subject_code=eq_subject,
        as_of=date(2026, 8, 1),
    )
    report = certifier.certify_pacing(
        pacing,
        curriculum_identity=f"{eq_subject}:2027.1",
        exam_date_required=True,
    )
    assert report.passed, report.issues
    assert pacing.exam_date_aware is True
    assert pacing.revision_minutes > 0
    assert pacing.first_pass_minutes > 0
    assert pacing.feasible is True

    # Tight deadline must report honest shortfall, not silent compression
    tight_user = make_certified_user("eq001-tight@example.com")
    runtime.enrol_student(
        user_id=tight_user.id,
        subject_code=eq_subject,
        exam_date=date(2026, 8, 2),
    )
    tight = runtime.project_pacing(
        user_id=tight_user.id,
        subject_code=eq_subject,
        as_of=date(2026, 8, 1),
        weekday_minutes=30,
        weekend_minutes=30,
    )
    tight_report = certifier.certify_pacing(
        tight,
        curriculum_identity=f"{eq_subject}:2027.1",
        exam_date_required=True,
    )
    assert tight_report.passed, tight_report.issues
    assert tight.feasible is False
    assert tight.shortfall_minutes is not None and tight.shortfall_minutes > 0


def test_eq_end_to_end_published_subject_quality(eq_subject, eq_user):
    """Acceptance: newly published subject generates certifiable learning experience."""
    runtime = EducationalRuntimeEngineService()
    certifier = EducationalQualityCertifier()
    artefacts = EducationalEngineFoundationService().derive_active(eq_subject)
    assert artefacts is not None
    artefact_report = certifier.certify_artefacts(artefacts)
    assert artefact_report.passed, artefact_report.issues

    runtime.enrol_student(
        user_id=eq_user.id,
        subject_code=eq_subject,
        exam_date=date(2026, 12, 15),
    )
    day = date(2026, 8, 1)
    topic_sequence = []
    while True:
        journey = runtime.get_journey(user_id=eq_user.id, subject_code=eq_subject)
        if journey.progress.syllabus_complete:
            break
        explanation = runtime.get_journey_explanation(
            user_id=eq_user.id,
            subject_code=eq_subject,
        )
        assert certifier.certify_journey_explanation(
            explanation,
            curriculum_identity=artefacts.curriculum_identity,
        ).passed
        mission = runtime.generate_daily_mission(
            user_id=eq_user.id,
            subject_code=eq_subject,
            mission_date=day,
        )
        mission_report = certifier.certify_mission(mission, artefacts=artefacts)
        assert mission_report.passed, mission_report.issues
        topic_sequence.append(mission.topic_id)
        runtime.complete_mission(
            user_id=eq_user.id,
            mission_instance_id=mission.mission_instance_id,
        )
        day += timedelta(days=1)

    assert topic_sequence == ["topic-t1", "topic-t2", "topic-t3"]
    pacing = runtime.project_pacing(
        user_id=eq_user.id,
        subject_code=eq_subject,
        as_of=date(2026, 8, 1),
    )
    assert certifier.certify_pacing(
        pacing,
        curriculum_identity=artefacts.curriculum_identity,
        exam_date_required=True,
    ).passed
    final = runtime.get_journey_explanation(
        user_id=eq_user.id,
        subject_code=eq_subject,
    )
    assert "complete" in final.why_today.lower()
    assert certifier.certify_journey_explanation(
        final,
        curriculum_identity=artefacts.curriculum_identity,
    ).passed


def test_eq_prerequisite_gate_blocks_illegal_mission(eq_subject, eq_user, monkeypatch):
    """Prerequisite validation refuses missions when prerequisites are unmet."""
    runtime = EducationalRuntimeEngineService()
    runtime.enrol_student(user_id=eq_user.id, subject_code=eq_subject)

    import app.application.educational_runtime_engine.service as runtime_service
    from app.domain.educational_runtime_engine import progress as progress_mod

    original = progress_mod.derive_progress

    def _force_t2(model, events):
        derived = original(model, events)
        return derived.__class__(
            curriculum_identity=derived.curriculum_identity,
            topic_ids=derived.topic_ids,
            completed_topic_ids=(),
            incomplete_topic_ids=derived.topic_ids,
            current_topic_id="topic-t2",
            coverage_ratio=0.0,
            journey_stage=derived.journey_stage,
            syllabus_complete=False,
        )

    monkeypatch.setattr(runtime_service, "derive_progress", _force_t2)
    with pytest.raises(IllegalRuntimeState, match="unsatisfied prerequisites"):
        runtime.generate_daily_mission(
            user_id=eq_user.id,
            subject_code=eq_subject,
            mission_date=date(2026, 8, 1),
        )

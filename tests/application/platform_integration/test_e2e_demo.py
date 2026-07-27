"""End-to-end demonstration of PI-002A Founder → Student bridge."""

from __future__ import annotations

from datetime import date, timedelta

from app.application.educational_runtime_engine import RuntimeAuthority
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.models.platform_integration import RuntimeEnrolmentRoutingAudit
from app.services.study_plan_service import StudyPlanService
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def test_e2e_founder_publish_to_student_enrolment_demo(ctx):
    """Demonstrate the safe founder → student bridge with coexistence.

    Steps:
      1. Founder publishes a subject (PI-001A path).
      2. Discovery surfaces it when flags are on.
      3. Student enrols via bridge → Runtime C + audit.
      4. Same student creates a Runtime A study plan (JSON CS1).
      5. Both runtimes remain independently functional.
    """
    flags = bridge_flags()

    # 1–2. Publish + discover
    subject = publish_subject("E2E1", title="E2E Bridge Subject")
    discovery = PublishedSubjectDiscoveryService(flags=flags)
    offers = discovery.list_active_offers()
    assert any(o.subject_code == "E2E1" for o in offers)
    assert any(
        c.code == PUBLISHED_CATEGORY_CODE for c in discovery.augmented_categories()
    )

    student = make_user("e2e-student@example.com")

    # 3. Runtime C enrolment via bridge
    bridge = FounderStudentEnrolmentBridge(flags=flags)
    result = bridge.enrol(
        user_id=student.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=100),
    )
    assert result.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert result.audit_id.startswith("rta_")

    runtime = EducationalRuntimeEngineService()
    mission = runtime.generate_daily_mission(
        user_id=student.id,
        subject_code=subject,
        mission_date=date(2026, 8, 1),
    )
    assert mission.status == "generated"

    # 4. Runtime A enrolment unchanged
    plan = StudyPlanService.create_study_plan(
        user_id=student.id,
        exam_name="IFoA CS1",
        exam_sitting="April 2027",
        exam_date=date.today() + timedelta(days=120),
        weekday_study_minutes=90,
        weekend_study_minutes=120,
        current_stage="Learning",
        study_preference="Mixed",
        target_grade="Pass",
        preferred_session_minutes=60,
        curriculum_version="2026",
    )
    router = RuntimeRoutingService(flags=flags)
    decision = router.resolve(subject_code="CS1", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    router.record_decision(
        user_id=student.id,
        decision=decision,
        study_plan_id=plan.id,
        commit=True,
    )

    # 5. Audit trail covers both runtimes
    audits = RuntimeEnrolmentRoutingAudit.query.filter_by(
        user_id=student.id
    ).order_by(RuntimeEnrolmentRoutingAudit.id.asc()).all()
    authorities = [a.runtime_authority for a in audits]
    assert "published_curriculum" in authorities
    assert "json_bundled" in authorities
    assert StudyPlanService.get_user_active_plan(student.id).id == plan.id
    assert runtime.get_journey(
        user_id=student.id, subject_code=subject
    ).enrolment.status == "active"

"""Unit and integration tests for PI-002A Founder → Student bridge."""

from __future__ import annotations

from datetime import date, timedelta

import pytest

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
from app.application.platform_integration.exceptions import (
    BridgeEnrolmentBlocked,
    PublishedSubjectNotDiscoverable,
)
from app.application.platform_integration.flags import (
    resolve_founder_student_bridge_flags,
)
from app.application.platform_integration.routing import RuntimeRoutingService
from app.models.educational_runtime_engine import RuntimeEnrolment
from app.models.platform_integration import RuntimeEnrolmentRoutingAudit
from app.services.study_plan_service import StudyPlanService
from app.services.subject_support_service import (
    SubjectSupportService,
    SupportStatus,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)


def test_flags_default_off():
    flags = resolve_founder_student_bridge_flags(environ={})
    assert flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY is False
    assert flags.ENABLE_RUNTIME_C_ENROLMENT is False
    assert flags.RUNTIME_C_SUBJECT_ALLOWLIST == frozenset()
    assert flags.bridge_active is False


def test_flags_umbrella_enables_both():
    flags = resolve_founder_student_bridge_flags(
        environ={"KWALITEC_FOUNDER_STUDENT_BRIDGE": "1"}
    )
    assert flags.ENABLE_PUBLISHED_SUBJECT_DISCOVERY is True
    assert flags.ENABLE_RUNTIME_C_ENROLMENT is True


def test_flags_allowlist_parsed():
    flags = resolve_founder_student_bridge_flags(
        environ={"KWALITEC_RUNTIME_C_SUBJECT_ALLOWLIST": " alpha ,Beta "}
    )
    assert flags.RUNTIME_C_SUBJECT_ALLOWLIST == frozenset({"ALPHA", "BETA"})


def test_discovery_hidden_when_flag_off(ctx):
    publish_subject("HIDE1")
    discovery = PublishedSubjectDiscoveryService(flags=bridge_flags(discovery=False))
    assert discovery.list_active_offers() == ()
    codes = {c.code for c in discovery.augmented_categories()}
    assert PUBLISHED_CATEGORY_CODE not in codes


def test_discovery_lists_published_when_flag_on(ctx):
    publish_subject("SHOW1", title="Shown Subject")
    discovery = PublishedSubjectDiscoveryService(flags=bridge_flags())
    offers = discovery.list_active_offers()
    assert len(offers) == 1
    assert offers[0].subject_code == "SHOW1"
    assert offers[0].title == "Shown Subject"
    categories = discovery.augmented_categories()
    published = next(c for c in categories if c.code == PUBLISHED_CATEGORY_CODE)
    assert any(p.code == "SHOW1" for p in published.papers)


def test_routing_defaults_to_runtime_a_when_enrolment_disabled(ctx):
    publish_subject("ROUTE1")
    router = RuntimeRoutingService(flags=bridge_flags(enrolment=False))
    decision = router.resolve(
        subject_code="ROUTE1", category_code=PUBLISHED_CATEGORY_CODE
    )
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    assert decision.reason == "runtime_c_enrolment_disabled"


def test_routing_published_category_to_runtime_c(ctx):
    publish_subject("ROUTE2")
    router = RuntimeRoutingService(flags=bridge_flags())
    decision = router.resolve(
        subject_code="ROUTE2", category_code=PUBLISHED_CATEGORY_CODE
    )
    assert decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert decision.reason == "published_category_selection"
    assert decision.curriculum_identity == "ROUTE2:2027.1"


def test_routing_legacy_catalogue_stays_runtime_a_even_if_published(ctx):
    publish_subject("CS1X")
    router = RuntimeRoutingService(flags=bridge_flags())
    decision = router.resolve(subject_code="CS1X", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    assert decision.reason == "legacy_catalogue_defaults_to_runtime_a"


def test_routing_allowlist_selects_runtime_c(ctx):
    publish_subject("ALLOW1")
    router = RuntimeRoutingService(
        flags=bridge_flags(allowlist=frozenset({"ALLOW1"}))
    )
    decision = router.resolve(subject_code="ALLOW1", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert decision.reason == "subject_allowlist"


def test_subject_support_published_enrolable(ctx):
    publish_subject("SUP1", title="Support Subject")
    # Inject flags via env for SubjectSupportService (reads process env).
    import os

    os.environ["KWALITEC_FOUNDER_STUDENT_BRIDGE"] = "1"
    try:
        info = SubjectSupportService.resolve(PUBLISHED_CATEGORY_CODE, "SUP1")
        assert info.status is SupportStatus.SUPPORTED
        assert info.allows_plan_creation is True
    finally:
        os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)


def test_subject_support_published_discovery_only(ctx):
    publish_subject("SUP2")
    import os

    os.environ["KWALITEC_PUBLISHED_SUBJECT_DISCOVERY"] = "1"
    os.environ.pop("KWALITEC_RUNTIME_C_ENROLMENT", None)
    os.environ.pop("KWALITEC_FOUNDER_STUDENT_BRIDGE", None)
    try:
        info = SubjectSupportService.resolve(PUBLISHED_CATEGORY_CODE, "SUP2")
        assert info.status is SupportStatus.COMING_SOON
        assert info.allows_plan_creation is False
    finally:
        os.environ.pop("KWALITEC_PUBLISHED_SUBJECT_DISCOVERY", None)


def test_bridge_enrols_runtime_c_with_audit(ctx):
    user = make_user("enrol-c@example.com")
    subject = publish_subject("ENRC1")
    flags = bridge_flags()
    bridge = FounderStudentEnrolmentBridge(flags=flags)

    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=90),
    )

    assert result.runtime_authority == RuntimeAuthority.PUBLISHED_CURRICULUM
    assert result.enrolment_id is not None
    assert result.curriculum_identity == "ENRC1:2027.1"
    assert result.study_plan_id is None

    enrolment = RuntimeEnrolment.query.filter_by(user_id=user.id).one()
    assert enrolment.subject_code == "ENRC1"

    audit = RuntimeEnrolmentRoutingAudit.query.filter_by(
        audit_id=result.audit_id
    ).one()
    assert audit.runtime_authority == "published_curriculum"
    assert audit.enrolment_id == result.enrolment_id
    assert audit.decision_reason == "published_category_selection"


def test_bridge_blocks_when_discovery_disabled(ctx):
    user = make_user("block@example.com")
    subject = publish_subject("BLK1")
    bridge = FounderStudentEnrolmentBridge(
        flags=bridge_flags(discovery=False, enrolment=True)
    )
    with pytest.raises(PublishedSubjectNotDiscoverable):
        bridge.enrol(
            user_id=user.id,
            category_code=PUBLISHED_CATEGORY_CODE,
            subject_code=subject,
        )


def test_bridge_blocks_when_enrolment_disabled(ctx):
    user = make_user("block2@example.com")
    subject = publish_subject("BLK2")
    bridge = FounderStudentEnrolmentBridge(
        flags=bridge_flags(discovery=True, enrolment=False)
    )
    with pytest.raises(BridgeEnrolmentBlocked):
        bridge.enrol(
            user_id=user.id,
            category_code=PUBLISHED_CATEGORY_CODE,
            subject_code=subject,
        )


def test_runtime_a_enrolment_unchanged_and_audited(ctx):
    user = make_user("runtime-a@example.com")
    plan = StudyPlanService.create_study_plan(
        user_id=user.id,
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
    assert plan is not None
    assert StudyPlanService.get_user_active_plan(user.id) is not None

    router = RuntimeRoutingService(flags=bridge_flags(enrolment=False))
    decision = router.resolve(subject_code="CS1", category_code="IFoA")
    assert decision.runtime_authority == RuntimeAuthority.JSON_BUNDLED
    audit = router.record_decision(
        user_id=user.id,
        decision=decision,
        study_plan_id=plan.id,
        commit=True,
    )
    row = RuntimeEnrolmentRoutingAudit.query.filter_by(
        audit_id=audit.audit_id
    ).one()
    assert row.runtime_authority == "json_bundled"
    assert row.study_plan_id == plan.id
    assert RuntimeEnrolment.query.filter_by(user_id=user.id).count() == 0


def test_coexistence_runtime_c_and_runtime_a_parallel(ctx):
    """Published enrolment and JSON study plan coexist for the same user."""
    user = make_user("coex@example.com")
    subject = publish_subject("COEXA")
    flags = bridge_flags()
    bridge = FounderStudentEnrolmentBridge(flags=flags)
    bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
    )

    plan = StudyPlanService.create_study_plan(
        user_id=user.id,
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
    assert plan.active is True
    assert RuntimeEnrolment.query.filter_by(user_id=user.id).count() == 1
    journey = EducationalRuntimeEngineService().get_journey(
        user_id=user.id, subject_code=subject
    )
    assert journey.runtime_authority == "published_curriculum"

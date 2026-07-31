"""V1S-007 — Educational Runtime Singularity.

Proves SCI auto-create, no Runtime A fallback for Runtime C students,
one educational pipeline, and readiness messaging for missing prerequisites.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_runtime_engine import (
    EducationalPrerequisiteMissing,
    ensure_active_sci,
)
from app.application.educational_runtime_engine.sci_lifecycle import (
    provision_ckg_edition_from_published_package,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.progress_engine import ProgressEngine
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.models.curriculum_knowledge_graph import CkgGraphEdition
from app.models.student_curriculum_binding import SciStudentCurriculumInstance
from app.models.user import User
from app.services.runtime_ownership import (
    A9_EDUCATIONAL_RUNTIME_SINGULARITY,
    MISSION_SPINE,
    RUNTIME_OWNERSHIP_MATRIX,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)

REPO_ROOT = Path(__file__).resolve().parents[1]


def _enrol_runtime_c(user: User, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


def test_a9_principle_registered():
    assert "Educational Runtime" in A9_EDUCATIONAL_RUNTIME_SINGULARITY
    assert "never" in A9_EDUCATIONAL_RUNTIME_SINGULARITY.lower()
    caps = {e.capability for e in RUNTIME_OWNERSHIP_MATRIX}
    assert any("SCI" in c or "Curriculum Instance" in c for c in caps)
    assert "ensure_active_sci" in " ".join(MISSION_SPINE)


def test_sci_auto_created_on_runtime_c_enrolment(app, db, ctx):
    subject = publish_subject("SNG1", title="Singularity Subject")
    user = make_user("sci-enrol@example.com")
    assert (
        SciStudentCurriculumInstance.query.filter_by(student_id=user.id).count()
        == 0
    )

    _enrol_runtime_c(user, subject)

    instances = SciStudentCurriculumInstance.query.filter_by(
        student_id=user.id, subject_code=subject, is_active=True
    ).all()
    assert len(instances) == 1
    edition = CkgGraphEdition.query.filter_by(
        edition_id=instances[0].edition_id
    ).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value


def test_ensure_sci_idempotent(app, db, ctx):
    subject = publish_subject("SNG2", title="Idempotent SCI")
    user = make_user("sci-idem@example.com")
    _enrol_runtime_c(user, subject)

    first = ensure_active_sci(student_id=user.id, subject_code=subject)
    second = ensure_active_sci(student_id=user.id, subject_code=subject)
    assert first is not None and second is not None
    assert first.instance_id == second.instance_id
    assert second.created is False
    assert second.source == "existing"
    assert (
        SciStudentCurriculumInstance.query.filter_by(
            student_id=user.id, is_active=True
        ).count()
        == 1
    )


def test_ckg_bridge_from_published_package(app, db, ctx):
    subject = publish_subject("SNG3", title="Bridge Subject")
    assert (
        CkgGraphEdition.query.filter_by(
            subject_code=subject,
            publication_state=PublicationState.PUBLISHED.value,
        ).count()
        == 0
    )
    edition_id = provision_ckg_edition_from_published_package(subject)
    assert edition_id is not None
    assert edition_id.startswith("ckg-runtime-bridge-")
    again = provision_ckg_edition_from_published_package(subject)
    assert again == edition_id


def test_ensure_sci_reports_missing_prerequisites(app, db, ctx):
    user = make_user("sci-missing@example.com")
    with pytest.raises(EducationalPrerequisiteMissing) as excinfo:
        ensure_active_sci(
            student_id=user.id,
            subject_code="ZZ99",
            require=True,
        )
    assert excinfo.value.missing_prerequisite == "published_curriculum_or_ckg_edition"
    soft = ensure_active_sci(
        student_id=user.id,
        subject_code="ZZ99",
        require=False,
    )
    assert soft is None


def test_session_never_routes_runtime_c_to_runtime_a(app, db, ctx, monkeypatch):
    """Runtime C enrolment must not fall through to Experience.start_session."""
    subject = publish_subject("SNG4", title="No Fallback")
    user = make_user("nofallback@example.com")
    _enrol_runtime_c(user, subject)
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")

    legacy = MagicMock(name="legacy_start_session")
    with (
        patch(
            "app.presentation.student.views.get_experience_service"
        ) as get_svc,
        patch(
            "flask_login.utils._get_user",
            return_value=user,
        ),
        patch(
            "app.presentation.student.views._try_runtime_c_session_start",
            return_value=None,
        ),
    ):
        get_svc.return_value.start_session = legacy
        from app.presentation.student import views as student_views

        with pytest.raises(EducationalPrerequisiteMissing) as excinfo:
            student_views.start_todays_session()
        assert "legacy" in str(excinfo.value).lower() or (
            excinfo.value.missing_prerequisite == "educational_runtime_session"
        )
        legacy.assert_not_called()


def test_progress_engine_is_sole_progress_owner():
    owners = {
        e.capability: e.owner for e in RUNTIME_OWNERSHIP_MATRIX
    }
    assert owners["Progress"] == "ProgressEngine"
    assert ProgressEngine is not None


def test_mission_spine_is_single_pipeline():
    joined = " → ".join(MISSION_SPINE)
    assert "PublishedCurriculumPackage" in joined
    assert "ensure_active_sci" in joined
    assert "LearningSessionRuntime" in joined
    assert "ProgressEngine" in joined or "Progress" in joined
    assert "PlanningService" not in joined
    assert "MissionEngineV2" not in joined
    assert "Runtime A" not in joined


def test_no_student_route_imports_planning_service_for_session():
    """Student presentation session start must not import PlanningService."""
    views_src = (
        REPO_ROOT / "app/presentation/student/views.py"
    ).read_text(encoding="utf-8")
    assert "from app.services.planning_service" not in views_src
    assert "MissionStartAdapter" not in views_src
    assert "ensure_active_sci" in views_src
    assert "EducationalPrerequisiteMissing" in views_src


def test_learning_journey_shell_vm_call_is_keyword_only():
    routes_src = (
        REPO_ROOT / "app/presentation/student/routes.py"
    ).read_text(encoding="utf-8")
    assert "shell_vm(ExperienceSurface.HISTORY)" not in routes_src
    assert "active_surface=ExperienceSurface.HISTORY.value" in routes_src


def test_v1s007_report_exists():
    assert (
        REPO_ROOT / "V1S007_EDUCATIONAL_RUNTIME_SINGULARITY_REPORT.md"
    ).is_file()


def test_release_criteria_includes_a9():
    text = (REPO_ROOT / "V1_RELEASE_CRITERIA.md").read_text(encoding="utf-8")
    assert "A9" in text
    assert "Educational Runtime Singularity" in text


def test_runtime_ownership_sci_and_journey(app, db, ctx):
    subject = publish_subject("SNG5", title="Ownership")
    user = make_user("own@example.com")
    _enrol_runtime_c(user, subject)
    ensure_active_sci(student_id=user.id, subject_code=subject)
    assert (
        SciStudentCurriculumInstance.query.filter_by(
            student_id=user.id, is_active=True
        ).count()
        == 1
    )
    flags = resolve_v2_feature_flags(environ={"SR_SESSION_PRIMARY": "1"})
    assert flags.SR_SESSION_PRIMARY is True

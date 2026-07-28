"""VP-001 — Version 1 product journey: LP onboard + RIS + evidence refresh."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch

from app.application.curriculum_extraction.dto import ExtractionRequest
from app.application.curriculum_extraction.extraction_engine import (
    CurriculumExtractionEngine,
)
from app.application.curriculum_publishing.editorial_operations_service import (
    EditorialOperationsService,
)
from app.application.curriculum_publishing.publication_engine import (
    PublicationEngine,
)
from app.application.runtime_integration.dto import IntegrationSurface
from app.application.runtime_integration.service import RuntimeIntegrationService
from app.application.student_experience.revision_service import RevisionService
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.learning_evidence.evidence_type import EvidenceType
from app.infrastructure.adapters.learner_lifecycle import (
    onboard_after_enrolment,
    record_session_evidence,
    resolve_published_edition_id,
)
from app.models.curriculum_knowledge_graph import CkgGraphEdition
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import SciStudentCurriculumInstance
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"
AS_OF = datetime(2026, 7, 28, 21, 0, 0)


def _publish_edition(*, job_id: str = "job-vp001-1") -> str:
    engine = CurriculumExtractionEngine()
    result = engine.extract(
        ExtractionRequest(
            job_id=job_id,
            subject_code="CS1",
            edition_label="2026",
            subject_title="Actuarial Statistics",
            cmp_document=cmp_document(),
            syllabus_document=syllabus_document(),
            persist=True,
        )
    )
    assert result.persisted is True
    assert result.edition_id is not None
    edition_id = result.edition_id
    EditorialOperationsService().approve_edition(edition_id, actor=FOUNDER)
    PublicationEngine().publish(
        edition_id,
        publisher=FOUNDER,
        rationale="VP-001 test published edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value
    return edition_id


def test_resolve_published_edition_id(app, db, ctx) -> None:
    edition_id = _publish_edition()
    assert resolve_published_edition_id("CS1") == edition_id
    assert resolve_published_edition_id("UNKNOWN") is None


def test_onboard_after_enrolment_creates_sci_and_decisions(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-vp001-onboard")

    result = onboard_after_enrolment(
        student_id=user.id,
        subject_code="CS1",
        edition_id=edition_id,
        correlation_id="corr-vp001-onboard",
    )

    assert result is not None
    assert result.succeeded
    instance = SciStudentCurriculumInstance.query.filter_by(
        student_id=user.id, is_active=True
    ).first()
    assert instance is not None
    assert (
        EreEducationalDecision.query.filter_by(
            instance_id=instance.instance_id
        ).count()
        > 0
    )


def test_onboard_skips_without_published_edition(app, db, ctx) -> None:
    user = _make_user()
    result = onboard_after_enrolment(
        student_id=user.id,
        subject_code="NOPE",
    )
    assert result is None
    assert (
        SciStudentCurriculumInstance.query.filter_by(student_id=user.id).count()
        == 0
    )


def test_end_to_end_ei_journey_without_manual_intervention(app, db, ctx) -> None:
    """register-equivalent → onboard → SCI → study evidence → refreshed EI → RIS."""
    user = _make_user()
    edition_id = _publish_edition(job_id="job-vp001-e2e")

    # Onboarding (enrolment hook)
    onboarded = onboard_after_enrolment(
        student_id=user.id,
        subject_code="CS1",
        edition_id=edition_id,
        correlation_id="corr-vp001-e2e",
    )
    assert onboarded is not None and onboarded.succeeded
    instance_id = onboarded.instance_id
    assert instance_id is not None

    # Student surfaces resolve Preferred Authority
    ris = RuntimeIntegrationService(integration_enabled=True)
    for surface in (
        IntegrationSurface.DASHBOARD,
        IntegrationSurface.REVISION_PLANNER,
        IntegrationSurface.STUDY_SESSION,
        IntegrationSurface.DAILY_MISSION,
        IntegrationSurface.COACH,
    ):
        resolved = ris.resolve_for_surface(user.id, surface)
        assert resolved.uses_educational_intelligence, surface

    # Session evidence refreshes derived state
    before = LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
    evidence = record_session_evidence(
        student_id=user.id,
        session_id="sess-vp001-e2e",
        activity_id="act-1",
        event="practice_attempt",
        metadata={"correct": True},
    )
    assert evidence is not None and evidence.succeeded
    assert (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
        == before + 1
    )

    complete = record_session_evidence(
        student_id=user.id,
        session_id="sess-vp001-e2e",
        event="study_session",
    )
    assert complete is not None and complete.succeeded
    assert (
        LeeEvidenceEvent.query.filter_by(
            instance_id=instance_id,
            evidence_type=EvidenceType.STUDY_SESSION.value,
        ).count()
        >= 1
    )

    # Experiences still resolvable after refresh
    after = ris.resolve_for_surface(user.id, IntegrationSurface.DASHBOARD)
    assert after.uses_educational_intelligence
    assert after.experience is not None


def test_revision_service_prefers_educational_intelligence(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-vp001-rev")
    onboard_after_enrolment(
        student_id=user.id,
        subject_code="CS1",
        edition_id=edition_id,
    )

    adaptive = MagicMock()
    adaptive.is_available.return_value = True
    adaptive.get_revision_options.return_value = [
        {"option_id": "runtime-a", "title": "Should not win"}
    ]
    snap = RevisionService(adaptive_decision=adaptive).revision(str(user.id))
    assert snap.has_revision
    assert snap.primary is not None
    assert snap.primary.option_id != "runtime-a"
    adaptive.get_revision_options.assert_not_called()


def test_session_views_call_evidence_hook(app, db, ctx) -> None:
    from app.presentation.session import views as session_views

    user = _make_user()
    with (
        patch.object(session_views, "assert_session_owned"),
        patch.object(session_views, "service") as svc_factory,
        patch.object(session_views, "current_user") as cu,
        patch(
            "app.infrastructure.adapters.learner_lifecycle.record_session_evidence"
        ) as record,
    ):
        cu.id = user.id
        svc = MagicMock()
        svc.submit_response.return_value = MagicMock()
        svc.complete_session.return_value = MagicMock(
            topics_completed=("T1",),
            next_recommendation="",
        )
        svc_factory.return_value = svc

        with patch.object(session_views, "_link_commitment_completion"):
            session_views.submit_answer(
                session_id="s1", activity_id="a1", response="42"
            )
            session_views.complete_and_return(session_id="s1")

    assert record.call_count == 2


def test_vp001_surface_modules_reference_runtime_integration() -> None:
    """Revision + Session production paths must reference RIS (inventory gate)."""
    modules = (
        Path("app/application/student_experience/revision_service.py"),
        Path("app/presentation/session/views.py"),
        Path("app/infrastructure/adapters/learner_lifecycle/enrolment_hook.py"),
        Path("app/infrastructure/adapters/learner_lifecycle/evidence_hook.py"),
    )
    for path in modules:
        source = path.read_text(encoding="utf-8")
        assert "runtime_integration" in source or "LearnerLifecycle" in source, path

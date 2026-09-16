"""End-to-end: Runtime C sitting moves Progression Readiness via real OEA writes.

Exercises PackageActivityEngine → Objective Assessment Evidence → evaluator →
Study observation presenter. Does not seed OEA rows directly.
"""

from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.educational_experience import EducationalExperienceService
from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_package_by_id,
)
from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)
from app.application.learning_session.runtime import LearningSessionRuntime
from app.application.objective_evidence.recorder import (
    ObjectiveAssessmentEvidenceRecorder,
)
from app.application.objective_evidence.store import (
    ObjectiveAssessmentEvidenceStore,
)
from app.application.platform_integration.discovery import PUBLISHED_CATEGORY_CODE
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.progression_readiness import (
    CS1_A_T01_LO01,
    ProgressionReadiness,
    evaluate_from_store,
)
from app.application.student_runtime import StudentRuntimeCoordinator
from app.infrastructure.adapters.learning_session.package_activity_engine import (
    PackageActivityEngine,
)
from app.infrastructure.adapters.learning_session.persistence import (
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
)
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.student.services.progression_observation_presenter import (
    panels_by_topic_for_student,
)
from tests.application.objective_evidence.test_objective_evidence_architecture import (
    LIVE_ROOT,
    _advance_to_item,
    _correct_response_for_item,
)
from tests.application.platform_integration.helpers import (
    bridge_flags,
    make_user,
    publish_subject,
)

PACKAGE_ID = "CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS"
PACKAGE_FILE = "cr-1.1.1-aims-analysis-cs1017.json"
CONTRACT_ITEMS = (
    "cs1017-1.1.1-ar-01",
    "cs1017-1.1.1-cp-01",
)
TOPIC_ID = "CS1-A-T01"


def _flags():
    return resolve_v2_feature_flags(
        environ={
            "SR_SESSION_PRIMARY": "1",
            "SR_SESSION_SUBSTANCE": "1",
            "SR_SESSION_SQL_EVIDENCE_COMPANION": "0",
            "KWALITEC_COMMERCIAL_LOOP": "0",
            "KWALITEC_V2_SOLE_RUNTIME": "0",
            "SR_EVIDENCE_GATE": "0",
            "SR_TWIN_DAILY_LOOP": "0",
            "SR_SESSION_COMPLETION_PRODUCT": "0",
            "SR_NUMERIC_ASSESSMENT_FRAMEWORK": "0",
        }
    )


def _enrol_runtime_c(user, subject: str) -> None:
    bridge = FounderStudentEnrolmentBridge(flags=bridge_flags())
    result = bridge.enrol(
        user_id=user.id,
        category_code=PUBLISHED_CATEGORY_CODE,
        subject_code=subject,
        exam_date=date.today() + timedelta(days=120),
    )
    assert result.runtime_authority == "published_curriculum"


@pytest.mark.usefixtures("ctx")
def test_runtime_c_sitting_moves_progression_readiness_panel(monkeypatch):
    """Full path: start → practice responses → complete → panel READY."""
    monkeypatch.setenv("SR_SESSION_PRIMARY", "1")
    monkeypatch.setenv("SR_SESSION_SUBSTANCE", "1")
    monkeypatch.setenv("KWALITEC_COMMERCIAL_LOOP", "0")
    monkeypatch.setenv("SR_EVIDENCE_GATE", "0")
    monkeypatch.setenv("SR_NUMERIC_ASSESSMENT_FRAMEWORK", "0")

    pack = find_package_by_id(PACKAGE_ID)
    assert pack is not None
    assert Path(pack.source_path).name == PACKAGE_FILE
    for item_id in CONTRACT_ITEMS:
        assert any(c.item_id == item_id for c in pack.knowledge_checks)

    subject = publish_subject(
        "PRCE2E", title="Progression E2E", version_label="2026.1"
    )
    user = make_user("progression-e2e-runtime-c@example.com")
    _enrol_runtime_c(user, subject)
    EducationalExperienceService().load_for_user(user.id)
    progress = EducationalRuntimeEngineService().get_study_progress(
        user_id=user.id, subject_code=subject
    )
    current = progress.current_topic_id
    assert current

    oea_store = ObjectiveAssessmentEvidenceStore()
    recorder = ObjectiveAssessmentEvidenceRecorder(store=oea_store)
    session_store = SessionDocumentStore()
    persistence = LearningSessionPersistenceAdapter(store=session_store)
    coordinator = StudentRuntimeCoordinator(
        persistence=persistence,
        flags=_flags(),
    )

    before = evaluate_from_store(
        CS1_A_T01_LO01.objective_id,
        str(user.id),
        CS1_A_T01_LO01,
        store=oea_store,
    )
    assert before.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
    assert panels_by_topic_for_student(
        student_id=str(user.id),
        store=oea_store,
        topic_ids=(TOPIC_ID,),
    ) == {}

    binding = coordinator.start_student_selected_session(
        user_id=user.id,
        topic_id=current,
        subject_code=subject,
        educational_package_id=PACKAGE_ID,
    )
    assert binding.session_id.startswith("lsr-")

    engine = PackageActivityEngine(
        store=session_store,
        persistence=persistence,
        objective_evidence_recorder=recorder,
    )
    # Coordinator already provisioned the sequence; engine shares the store.
    for item_id in CONTRACT_ITEMS:
        activity = _advance_to_item(
            engine,
            student_id=str(user.id),
            session_id=binding.session_id,
            item_id=item_id,
        )
        response = _correct_response_for_item(pack, item_id)
        result = engine.submit_response_opaque(
            str(user.id),
            session_id=binding.session_id,
            activity_id=activity["activity_id"],
            response=response,
        )
        assert result.get("scored_correct") is True
        # Advance past the answered item so the next seek does not re-submit
        # an incorrect "noted" response that would overwrite latest OEA.
        engine.advance_activity_opaque(
            str(user.id), session_id=binding.session_id
        )

    after = evaluate_from_store(
        CS1_A_T01_LO01.objective_id,
        str(user.id),
        CS1_A_T01_LO01,
        store=oea_store,
    )
    assert after.readiness is ProgressionReadiness.READY

    panels = panels_by_topic_for_student(
        student_id=str(user.id),
        store=oea_store,
        topic_ids=(TOPIC_ID,),
    )
    assert TOPIC_ID in panels
    lo01_panels = [
        p for p in panels[TOPIC_ID] if p.objective_id == CS1_A_T01_LO01.objective_id
    ]
    assert len(lo01_panels) == 1
    assert lo01_panels[0].scenario_heading == (
        "Sufficient evidence to move forward"
    )

    runtime = LearningSessionRuntimeEngine(
        runtime=LearningSessionRuntime(),
        persistence=persistence,
    )
    completed = runtime.complete_session_opaque(
        str(user.id),
        session_id=binding.session_id,
        finish_verdict="yes",
    )
    assert completed is not None
    assert completed.get("status") == "completed"
    # Student-selected sittings never complete today's recommended mission.
    assert completed.get("mission_completed") is False

    # Completing must not erase the OEA-backed READY judgment.
    final = evaluate_from_store(
        CS1_A_T01_LO01.objective_id,
        str(user.id),
        CS1_A_T01_LO01,
        store=oea_store,
    )
    assert final.readiness is ProgressionReadiness.READY


def test_contract_package_still_exists_on_disk():
    """Guard: the authored contract package used above remains loadable."""
    loader = EducationalPackageLoader(root=LIVE_ROOT)
    packs = {Path(p.source_path).name: p for p in loader.all_approved()}
    assert PACKAGE_FILE in packs
    assert packs[PACKAGE_FILE].package_id == PACKAGE_ID

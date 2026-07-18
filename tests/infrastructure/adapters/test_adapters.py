"""Adapter conformance and behavioural tests."""

from __future__ import annotations

from datetime import UTC, datetime

import pytest

from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.application.curriculum_studio.ports.education_platform_port import (
    EducationPlatformPort,
)
from app.application.learning_orchestrator.ports.adaptive_learning_port import (
    AdaptiveLearningPort,
)
from app.application.learning_orchestrator.ports.analytics_port import AnalyticsPort
from app.application.learning_orchestrator.ports.evidence_port import EvidencePort
from app.application.learning_orchestrator.ports.mission_port import MissionPort
from app.application.learning_orchestrator.ports.twin_port import TwinPort
from app.infrastructure.adapters.adaptive_learning import AdaptiveLearningAdapter
from app.infrastructure.adapters.curriculum_ingestion import (
    CurriculumIngestionAdapter,
)
from app.infrastructure.adapters.curriculum_management import (
    CurriculumManagementAdapter,
)
from app.infrastructure.adapters.education_platform import EducationPlatformAdapter
from app.infrastructure.adapters.learning_orchestrator import (
    AnalyticsPortAdapter,
    EvidencePortAdapter,
    LearningOrchestratorAdapter,
)
from app.infrastructure.adapters.mission import MissionPortAdapter
from app.infrastructure.adapters.student_twin import StudentTwinAdapter
from tests.infrastructure.helpers import LEARNERS, SUBJECTS, make_request

NOW = datetime(2026, 7, 18, 20, 0, tzinfo=UTC)


@pytest.mark.parametrize(
    "adapter_factory,port",
    [
        (CurriculumManagementAdapter, CurriculumManagementPort),
        (CurriculumIngestionAdapter, CurriculumIngestionPort),
        (EducationPlatformAdapter, EducationPlatformPort),
        (StudentTwinAdapter, TwinPort),
        (AdaptiveLearningAdapter, AdaptiveLearningPort),
        (MissionPortAdapter, MissionPort),
        (EvidencePortAdapter, EvidencePort),
        (AnalyticsPortAdapter, AnalyticsPort),
    ],
)
def test_adapter_satisfies_protocol(adapter_factory, port):
    adapter = adapter_factory()
    assert isinstance(adapter, port)
    assert adapter.is_available() is True
    assert adapter.component_id
    assert adapter.component_version


@pytest.mark.parametrize("code", SUBJECTS)
def test_curriculum_management_create_subject_and_version(code):
    adapter = CurriculumManagementAdapter()
    subject = adapter.create_subject(code, title=f"Title {code}")
    assert subject["subject_code"] == code.upper()
    version = adapter.create_version(code, "2026.1")
    assert version["version_id"]
    assert adapter.get_version_summary(version["version_id"]) is not None
    assert adapter.list_versions(code)
    assert adapter.list_subjects()


@pytest.mark.parametrize("available", [True, False])
def test_adapters_availability_toggle(available):
    for factory in (
        CurriculumManagementAdapter,
        CurriculumIngestionAdapter,
        EducationPlatformAdapter,
        StudentTwinAdapter,
        AdaptiveLearningAdapter,
        MissionPortAdapter,
        EvidencePortAdapter,
        AnalyticsPortAdapter,
    ):
        adapter = factory()
        adapter.set_available(available)
        assert adapter.is_available() is available


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_orchestrator_ports_pipeline_payloads(learner_id, subject_id):
    evidence = EvidencePortAdapter()
    twin = StudentTwinAdapter()
    adaptive = AdaptiveLearningAdapter()
    mission = MissionPortAdapter()
    request = make_request(learner_id=learner_id, subject_id=subject_id)
    ev = evidence.process_evidence(request)
    assert ev["ok"] is True
    tw = twin.update_from_evidence(request, evidence_payload=ev)
    assert tw["authority"] == "student_twin"
    dec = adaptive.decide(request, twin_payload=tw, evidence_payload=ev)
    assert dec["next_action_authority"] is True
    ms = mission.apply_decision(
        request, decision_payload=dec, twin_payload=tw
    )
    assert ms["next_action_authority"] is False


@pytest.mark.parametrize("learner_id", LEARNERS[:3])
@pytest.mark.parametrize("subject_id", SUBJECTS[:2])
def test_learning_orchestrator_adapter_orchestrate(learner_id, subject_id):
    orch = LearningOrchestratorAdapter()
    response = orch.orchestrate(
        make_request(learner_id=learner_id, subject_id=subject_id)
    )
    assert response.learner_id == learner_id
    assert response.success is True


@pytest.mark.parametrize("code", SUBJECTS[:2])
def test_education_platform_health_and_surface(code):
    adapter = EducationPlatformAdapter()
    health = adapter.health()
    assert isinstance(health, dict)
    assert adapter.student_surface(subject_code=code) is None
    adapter.register_student_surface(code, {"label": "preview"})
    surface = adapter.student_surface(subject_code=code, version_id="v1")
    assert surface is not None
    assert surface["display_only"] is True


@pytest.mark.parametrize("code", SUBJECTS[:2])
def test_ingestion_adapter_start(code):
    adapter = CurriculumIngestionAdapter()
    summary = adapter.start_ingestion(
        subject_code=code,
        sources=[
            {
                "document_id": f"doc-{code}",
                "source_ref": "ref://x",
                "title": "Syllabus",
                "entries": [
                    {"entry_id": "1", "entry_type": "topic", "text": "T1"}
                ],
            }
        ],
    )
    job_id = summary["job_id"]
    assert adapter.get_ingestion_summary(job_id) is not None

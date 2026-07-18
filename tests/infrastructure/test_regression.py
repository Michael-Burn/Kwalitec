"""Regression guards for V2-017 production integration."""

from __future__ import annotations

from pathlib import Path

import pytest

from app.infrastructure import INFRASTRUCTURE_VERSION
from app.infrastructure.adapters.adaptive_learning import AdaptiveLearningAdapter
from app.infrastructure.adapters.curriculum_management import (
    CurriculumManagementAdapter,
)
from app.infrastructure.adapters.learning_orchestrator import (
    LearningOrchestratorAdapter,
)
from app.infrastructure.events.types import EVENT_TYPES
from app.infrastructure.persistence.contracts import AGGREGATE_CONTRACTS
from tests.infrastructure.helpers import make_request

ROOT = Path(__file__).resolve().parents[2]
KNOWLEDGE = ROOT / "knowledge" / "version2"
ADR = KNOWLEDGE / "ARCHITECTURE_DECISIONS"


def test_infrastructure_version_present():
    assert INFRASTRUCTURE_VERSION.startswith("v2-017")


def test_required_docs_exist():
    for name in (
        "PRODUCTION_INTEGRATION.md",
        "AUTHORITY_MATRIX.md",
        "VERSION2_ROADMAP.md",
        "README.md",
    ):
        assert (KNOWLEDGE / name).is_file()


@pytest.mark.parametrize(
    "adr",
    [
        "ADR-005-Single-Next-Action-Authority.md",
        "ADR-006-Authority-Boundaries.md",
        "ADR-007-Legacy-Retirement-Strategy.md",
    ],
)
def test_adrs_exist(adr):
    path = ADR / adr
    assert path.is_file()
    text = path.read_text(encoding="utf-8")
    assert "Status:" in text
    assert "Decision" in text


def test_event_catalogue_complete():
    required = {
        "EvidenceRecorded",
        "TwinUpdated",
        "AdaptiveDecisionGenerated",
        "MissionUpdated",
        "CurriculumPublished",
        "CurriculumValidated",
        "LearningSessionCompleted",
    }
    assert set(EVENT_TYPES) == required


def test_aggregate_contracts_nonempty():
    assert len(AGGREGATE_CONTRACTS) >= 8


def test_management_adapter_does_not_bypass_facade():
    adapter = CurriculumManagementAdapter()
    assert adapter.facade is not None
    subject = adapter.create_subject("REG1", title="Regression")
    assert subject["subject_code"] == "REG1"


def test_orchestrator_preserves_success_path():
    orch = LearningOrchestratorAdapter()
    response = orch.orchestrate(make_request(event_id="reg-orch-1"))
    assert response.success is True


def test_adaptive_authority_flag_stable():
    adaptive = AdaptiveLearningAdapter()
    decision = adaptive.decide(
        make_request(),
        twin_payload={"evidence_count": 0},
        evidence_payload={"evidence_id": "e1"},
    )
    assert decision["next_action_authority"] is True
    assert decision["authority"] == "adaptive_decision_engine"


def test_roadmap_mentions_v2017_integration():
    text = (KNOWLEDGE / "VERSION2_ROADMAP.md").read_text(encoding="utf-8")
    assert "Production Integration Foundation" in text
    assert "V2-017" in text


def test_readme_mentions_authority_matrix():
    text = (KNOWLEDGE / "README.md").read_text(encoding="utf-8")
    assert "AUTHORITY_MATRIX.md" in text
    assert "ADR-005" in text

"""Authority enforcement tests (ADR-005 / ADR-006)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.infrastructure.adapters.adaptive_learning import AdaptiveLearningAdapter
from app.infrastructure.adapters.mission import MissionPortAdapter
from app.infrastructure.adapters.student_twin import StudentTwinAdapter
from app.infrastructure.persistence.contracts import (
    AGGREGATE_CONTRACTS,
    AggregateOwner,
)
from tests.infrastructure.helpers import LEARNERS, SUBJECTS, make_request

INFRA_ROOT = Path(__file__).resolve().parents[3] / "app" / "infrastructure"

FORBIDDEN_IN_REPOS = (
    "readiness_score",
    "educational_roi",
    "recommend_next",
    "interventionselector",
    "revisionplanner",
)


@pytest.mark.parametrize("learner_id", LEARNERS)
@pytest.mark.parametrize("subject_id", SUBJECTS)
def test_adaptive_is_sole_next_action_authority(learner_id, subject_id):
    adaptive = AdaptiveLearningAdapter()
    mission = MissionPortAdapter()
    twin = StudentTwinAdapter()
    request = make_request(learner_id=learner_id, subject_id=subject_id)
    twin_payload = twin.update_from_evidence(
        request, evidence_payload={"evidence_id": request.event_id}
    )
    decision = adaptive.decide(
        request,
        twin_payload=twin_payload,
        evidence_payload={"evidence_id": request.event_id},
    )
    mission_payload = mission.apply_decision(
        request,
        decision_payload=decision,
        twin_payload=twin_payload,
    )
    assert decision["next_action_authority"] is True
    assert decision["authority"] == "adaptive_decision_engine"
    assert mission_payload["next_action_authority"] is False
    assert twin_payload["authority"] == "student_twin"


@pytest.mark.parametrize(
    "name,owner",
    [(c.name, c.owner) for c in AGGREGATE_CONTRACTS],
)
def test_aggregate_owner_declared(name, owner):
    assert isinstance(owner, AggregateOwner)
    assert name


def test_evidence_append_only_contract():
    evidence = next(c for c in AGGREGATE_CONTRACTS if c.name == "EvidenceEvent")
    assert evidence.append_only is True
    assert evidence.optimistic_locking is False


def test_twin_snapshot_eligible():
    twin = next(c for c in AGGREGATE_CONTRACTS if c.name == "DigitalTwin")
    assert twin.snapshot_eligible is True
    assert twin.owner is AggregateOwner.STUDENT_TWIN


@pytest.mark.parametrize(
    "path",
    list((INFRA_ROOT / "repositories").rglob("*.py"))
    + list((INFRA_ROOT / "persistence").rglob("*.py")),
)
def test_repositories_have_no_educational_rule_tokens(path):
    if path.name == "__init__.py":
        return
    text = path.read_text(encoding="utf-8").lower()
    for token in FORBIDDEN_IN_REPOS:
        assert token not in text, f"{path} contains educational token {token}"


def test_adapters_do_not_import_flask_into_application_ports():
    """Infrastructure may import flask, but application packages must not
    import infrastructure (checked in test_independence)."""
    app_root = Path(__file__).resolve().parents[3] / "app" / "application"
    offenders = []
    for path in app_root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith("app.infrastructure"):
                        offenders.append(str(path))
            elif isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith("app.infrastructure"):
                    offenders.append(str(path))
    assert offenders == []

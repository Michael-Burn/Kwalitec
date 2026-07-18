"""Port Protocol and substitution tests."""

from __future__ import annotations

from typing import Protocol

import pytest

from app.application.learning_orchestrator.ports.adaptive_learning_port import (
    AdaptiveLearningPort,
)
from app.application.learning_orchestrator.ports.analytics_port import (
    AnalyticsPort,
)
from app.application.learning_orchestrator.ports.evidence_port import (
    EvidencePort,
)
from app.application.learning_orchestrator.ports.mission_port import MissionPort
from app.application.learning_orchestrator.ports.twin_port import TwinPort
from tests.application.learning_orchestrator.helpers import (
    EVENT_TYPES,
    FakeAdaptive,
    FakeAnalytics,
    FakeEvidence,
    FakeMission,
    FakeTwin,
    make_orchestrator,
    make_request,
)

PORTS = [
    ("evidence", EvidencePort, FakeEvidence),
    ("twin", TwinPort, FakeTwin),
    ("adaptive_learning", AdaptiveLearningPort, FakeAdaptive),
    ("mission", MissionPort, FakeMission),
    ("analytics", AnalyticsPort, FakeAnalytics),
]


@pytest.mark.parametrize("name,protocol,fake_cls", PORTS)
def test_ports_are_protocols(name, protocol, fake_cls):
    del name, fake_cls
    assert issubclass(protocol, Protocol)


@pytest.mark.parametrize("name,protocol,fake_cls", PORTS)
def test_fakes_satisfy_runtime_checkable(name, protocol, fake_cls):
    del name
    instance = fake_cls()
    assert isinstance(instance, protocol)


@pytest.mark.parametrize("name,protocol,fake_cls", PORTS)
@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_replace_each_port(name, protocol, fake_cls, event_type):
    del protocol
    if name == "mission" and event_type == "manual_confidence_update":
        pytest.skip("mission not in manual confidence pipeline")
    orch = make_orchestrator()
    replacement = fake_cls(payload={"component": name, "replaced": True})
    orch.replace_port(name, replacement)
    response = orch.orchestrate(make_request(event_type=event_type))
    assert response.pipeline_snapshots
    assert replacement.calls


@pytest.mark.parametrize("event_type", EVENT_TYPES)
def test_bind_ports_after_create(event_type):
    orch = make_orchestrator(include_all=False)
    orch.bind_ports(
        evidence=FakeEvidence(),
        twin=FakeTwin(),
        adaptive_learning=FakeAdaptive(),
        mission=FakeMission(),
        analytics=FakeAnalytics(),
    )
    response = orch.orchestrate(make_request(event_type=event_type))
    assert response.success is True

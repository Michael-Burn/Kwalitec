"""Shared helpers for Learning Orchestrator tests."""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

from app.application.learning_orchestrator.dto.orchestration_request import (
    OrchestrationRequest,
)
from app.application.learning_orchestrator.learning_orchestrator import (
    LearningOrchestrator,
)
from app.application.learning_orchestrator.policies.pipeline_policy import (
    PipelinePolicy,
)
from app.application.learning_orchestrator.policies.retry_policy import (
    RetryPolicy,
)
from app.domain.learning_orchestrator.orchestration_event import (
    OrchestrationEvent,
    OrchestrationEventType,
)

NOW = datetime(2026, 7, 18, 18, 0, tzinfo=UTC)

EVENT_TYPES: tuple[str, ...] = tuple(
    e.value for e in OrchestrationEventType
)

PORT_NAMES: tuple[str, ...] = (
    "evidence",
    "twin",
    "adaptive_learning",
    "mission",
    "analytics",
)

STAGES: tuple[str, ...] = (
    "evidence",
    "twin",
    "decision",
    "mission",
    "analytics",
)


class _FakePortBase:
    """Shared availability / identity helpers for fake ports."""

    def __init__(
        self,
        *,
        component_id: str,
        available: bool = True,
        call_log: list[str] | None = None,
        component_version: str = "1.0.0",
        fail_times: int = 0,
        raise_error: Exception | None = None,
        payload: dict[str, Any] | None = None,
    ) -> None:
        self._component_id = component_id
        self._available = available
        self.calls: list[str] = call_log if call_log is not None else []
        self._component_version = component_version
        self._fail_times = fail_times
        self._failures_seen = 0
        self._raise_error = raise_error
        self._payload = payload or {"component": component_id, "ok": True}

    @property
    def component_id(self) -> str:
        return self._component_id

    @property
    def component_version(self) -> str:
        return self._component_version

    def set_available(self, available: bool) -> None:
        self._available = available

    def is_available(self) -> bool:
        return self._available

    def _maybe_fail(self, method: str) -> dict[str, Any]:
        self.calls.append(method)
        if self._raise_error is not None:
            raise self._raise_error
        if self._failures_seen < self._fail_times:
            self._failures_seen += 1
            raise RuntimeError(f"{self._component_id} transient failure")
        return dict(self._payload)


class FakeEvidence(_FakePortBase):
    """Deterministic EvidencePort double."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(component_id="evidence", **kwargs)

    def process_evidence(self, request: OrchestrationRequest) -> dict[str, Any]:
        payload = self._maybe_fail("process_evidence")
        payload["event_id"] = request.event_id
        payload["learner_id"] = request.learner_id
        return payload


class FakeTwin(_FakePortBase):
    """Deterministic TwinPort double."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(component_id="twin", **kwargs)

    def update_from_evidence(
        self,
        request: OrchestrationRequest,
        *,
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        payload = self._maybe_fail("update_from_evidence")
        payload["twin_version"] = "twin-v1"
        payload["evidence_keys"] = sorted(evidence_payload.keys())
        payload["learner_id"] = request.learner_id
        return payload


class FakeAdaptive(_FakePortBase):
    """Deterministic AdaptiveLearningPort double."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(component_id="adaptive_learning", **kwargs)

    def decide(
        self,
        request: OrchestrationRequest,
        *,
        twin_payload: dict[str, Any],
        evidence_payload: dict[str, Any],
    ) -> dict[str, Any]:
        payload = self._maybe_fail("decide")
        payload["intervention"] = "revision"
        payload["twin_keys"] = sorted(twin_payload.keys())
        payload["evidence_keys"] = sorted(evidence_payload.keys())
        payload["learner_id"] = request.learner_id
        return payload


class FakeMission(_FakePortBase):
    """Deterministic MissionPort double."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(component_id="mission", **kwargs)

    def apply_decision(
        self,
        request: OrchestrationRequest,
        *,
        decision_payload: dict[str, Any],
        twin_payload: dict[str, Any],
    ) -> dict[str, Any]:
        payload = self._maybe_fail("apply_decision")
        payload["mission_action"] = "schedule_revision"
        payload["decision_keys"] = sorted(decision_payload.keys())
        payload["twin_keys"] = sorted(twin_payload.keys())
        payload["learner_id"] = request.learner_id
        return payload


class FakeAnalytics(_FakePortBase):
    """Deterministic AnalyticsPort double."""

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(component_id="analytics", **kwargs)

    def record_execution(
        self,
        request: OrchestrationRequest,
        *,
        stage_payloads: dict[str, Any],
        execution_summary: dict[str, Any],
    ) -> dict[str, Any]:
        payload = self._maybe_fail("record_execution")
        payload["recorded"] = True
        payload["stage_count"] = len(stage_payloads)
        payload["summary_keys"] = sorted(execution_summary.keys())
        payload["learner_id"] = request.learner_id
        return payload


def make_request(
    *,
    event_type: str = OrchestrationEventType.LEARNING_ACTIVITY_COMPLETED.value,
    learner_id: str = "learner-1",
    event_id: str = "evt-1",
    occurred_at: datetime | None = None,
    orchestration_id: str | None = "orch-1",
    **kwargs: Any,
) -> OrchestrationRequest:
    """Build a deterministic OrchestrationRequest."""
    return OrchestrationRequest(
        event_type=event_type,
        learner_id=learner_id,
        event_id=event_id,
        occurred_at=occurred_at or NOW,
        orchestration_id=orchestration_id,
        subject_id=kwargs.get("subject_id", "subject-1"),
        topic_id=kwargs.get("topic_id", "topic-1"),
        journey_id=kwargs.get("journey_id", "journey-1"),
        session_id=kwargs.get("session_id"),
        activity_id=kwargs.get("activity_id"),
        mission_id=kwargs.get("mission_id"),
        evidence_id=kwargs.get("evidence_id"),
        correlation_id=kwargs.get("correlation_id", "corr-1"),
        payload=kwargs.get("payload"),
        metadata=kwargs.get("metadata"),
    )


def make_event(
    *,
    event_type: OrchestrationEventType | str = (
        OrchestrationEventType.LEARNING_ACTIVITY_COMPLETED
    ),
    learner_id: str = "learner-1",
    event_id: str = "evt-1",
    occurred_at: datetime | None = None,
    **kwargs: Any,
) -> OrchestrationEvent:
    """Build a deterministic domain OrchestrationEvent."""
    return OrchestrationEvent.create(
        event_type=event_type,
        learner_id=learner_id,
        event_id=event_id,
        occurred_at=occurred_at or NOW,
        subject_id=kwargs.get("subject_id", "subject-1"),
        topic_id=kwargs.get("topic_id", "topic-1"),
        journey_id=kwargs.get("journey_id", "journey-1"),
        session_id=kwargs.get("session_id"),
        activity_id=kwargs.get("activity_id"),
        mission_id=kwargs.get("mission_id"),
        evidence_id=kwargs.get("evidence_id"),
        payload=kwargs.get("payload"),
        correlation_id=kwargs.get("correlation_id", "corr-1"),
    )


def make_orchestrator(
    *,
    evidence: FakeEvidence | None = None,
    twin: FakeTwin | None = None,
    adaptive_learning: FakeAdaptive | None = None,
    mission: FakeMission | None = None,
    analytics: FakeAnalytics | None = None,
    include_all: bool = True,
    pipeline_policy: PipelinePolicy | None = None,
    retry_policy: RetryPolicy | None = None,
    call_log: list[str] | None = None,
    clock=None,
    id_factory=None,
) -> LearningOrchestrator:
    """Assemble a LearningOrchestrator with deterministic fake ports."""
    log = call_log if call_log is not None else []
    if include_all:
        evidence = evidence if evidence is not None else FakeEvidence(call_log=log)
        twin = twin if twin is not None else FakeTwin(call_log=log)
        adaptive_learning = (
            adaptive_learning
            if adaptive_learning is not None
            else FakeAdaptive(call_log=log)
        )
        mission = mission if mission is not None else FakeMission(call_log=log)
        analytics = (
            analytics if analytics is not None else FakeAnalytics(call_log=log)
        )
    counter = {"n": 0}

    def _ids() -> str:
        counter["n"] += 1
        return f"orch-fixed-{counter['n']}"

    return LearningOrchestrator.create(
        evidence=evidence,
        twin=twin,
        adaptive_learning=adaptive_learning,
        mission=mission,
        analytics=analytics,
        pipeline_policy=pipeline_policy,
        retry_policy=retry_policy,
        clock=clock or (lambda: NOW),
        id_factory=id_factory or _ids,
    )


def outcomes(response) -> dict[str, str]:
    """Map stage → outcome from an OrchestrationResponse."""
    return {s.stage: s.outcome for s in response.pipeline_snapshots}

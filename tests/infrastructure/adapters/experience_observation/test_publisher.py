"""Publisher + Evidence integration tests — Experience Observation Bridge."""

from __future__ import annotations

from dataclasses import dataclass

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.application.unified_journey import (
    SessionOutcome,
    mission_started,
    reflection_skipped,
    session_completed,
    session_started,
)
from app.infrastructure.adapters.evidence_platform import (
    EvidencePlatformAdapter,
    ObservedEvent,
    build_evidence_platform_adapter,
)
from app.infrastructure.adapters.experience_observation import (
    PUBLISH_STATUS_FAILED,
    PUBLISH_STATUS_PUBLISHED,
    PUBLISH_STATUS_SKIPPED,
    REASON_EVIDENCE_REJECTED,
    REASON_EVIDENCE_UNAVAILABLE,
    REASON_FLAG_OFF,
    REASON_NOT_OBSERVABLE,
    ExperienceObservation,
    ExperienceObservationPublisher,
    ObservationAssembler,
    build_experience_observation_publisher,
    observation_to_observed_event,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from app.infrastructure.diagnostics.dual_run import build_dual_run_status


@dataclass
class _FakeEvidence:
    """Minimal EvidenceObservationPort stand-in for DI tests."""

    calls: list
    fail: bool = False

    def collect_event(self, event: ObservedEvent):
        if self.fail:
            raise RuntimeError("intake rejected")
        self.calls.append(event)

        @dataclass(frozen=True)
        class _Record:
            evidence_id: str

        return _Record(evidence_id=f"ev-{event.event_type}")


def test_experience_observation_flag_defaults_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_EXPERIENCE_OBSERVATION is False
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_observation is False


def test_experience_observation_flag_enables_dual_run_field():
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_OBSERVATION": "1"}
    )
    assert flags.ENABLE_EXPERIENCE_OBSERVATION is True
    dual = build_dual_run_status(flags=flags)
    assert dual.experience_observation is True


def test_flags_are_independently_controllable():
    obs_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_OBSERVATION": "1"}
    )
    assert obs_only.ENABLE_EXPERIENCE_OBSERVATION is True
    assert obs_only.ENABLE_EVIDENCE_PLATFORM is False

    evidence_only = resolve_v2_feature_flags(
        environ={"KWALITEC_EVIDENCE_PLATFORM": "1"}
    )
    assert evidence_only.ENABLE_EVIDENCE_PLATFORM is True
    assert evidence_only.ENABLE_EXPERIENCE_OBSERVATION is False

    both = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    assert both.ENABLE_EXPERIENCE_OBSERVATION is True
    assert both.ENABLE_EVIDENCE_PLATFORM is True


def test_build_publisher_off_by_default():
    assert build_experience_observation_publisher(enabled=False) is None
    publisher = build_experience_observation_publisher(enabled=True)
    assert isinstance(publisher, ExperienceObservationPublisher)
    assert publisher.evidence is None


def test_composition_wires_publisher_only_when_flag_on():
    flags_off = resolve_v2_feature_flags(environ={})
    composition_off, _ = build_production_experience(flags=flags_off)
    assert composition_off.experience_observation is None

    flags_on = resolve_v2_feature_flags(
        environ={"KWALITEC_EXPERIENCE_OBSERVATION": "1"}
    )
    composition_on, _ = build_production_experience(flags=flags_on)
    assert isinstance(
        composition_on.experience_observation, ExperienceObservationPublisher
    )
    # Evidence remains independently off → sink is None.
    assert composition_on.evidence_platform is None
    assert composition_on.experience_observation.evidence is None


def test_composition_wires_publisher_with_evidence_when_both_on():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_EXPERIENCE_OBSERVATION": "1",
            "KWALITEC_EVIDENCE_PLATFORM": "1",
        }
    )
    composition, _ = build_production_experience(flags=flags)
    assert isinstance(
        composition.experience_observation, ExperienceObservationPublisher
    )
    assert isinstance(composition.evidence_platform, EvidencePlatformAdapter)
    assert composition.experience_observation.evidence is composition.evidence_platform


def test_publisher_skips_when_flag_disabled_instance():
    publisher = ExperienceObservationPublisher(
        enabled=False, evidence=_FakeEvidence([])
    )
    obs = ExperienceObservation(
        observation_id="expobs-x",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="daily_mission",
        experience_event="mission_started",
        student_id="1",
    )
    result = publisher.publish(obs)
    assert result.ok is False
    assert result.status == PUBLISH_STATUS_SKIPPED
    assert result.reason == REASON_FLAG_OFF


def test_publisher_skips_when_evidence_unavailable():
    publisher = ExperienceObservationPublisher(enabled=True, evidence=None)
    result = publisher.publish_journey_event(
        mission_started(),
        student_id="1",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="c1",
    )
    assert result.ok is False
    assert result.status == PUBLISH_STATUS_SKIPPED
    assert result.reason == REASON_EVIDENCE_UNAVAILABLE
    assert result.observation is not None


def test_publisher_skips_non_observable_events():
    publisher = ExperienceObservationPublisher(
        enabled=True, evidence=_FakeEvidence([])
    )
    obs = ExperienceObservation(
        observation_id="expobs-y",
        timestamp="2026-07-25T10:00:00+00:00",
        journey_stage="weekly_review",
        experience_event="weekly_review_available",
        student_id="1",
    )
    result = publisher.publish(obs)
    assert result.ok is False
    assert result.status == PUBLISH_STATUS_SKIPPED
    assert result.reason == REASON_NOT_OBSERVABLE


def test_publisher_publishes_via_injected_evidence_port():
    sink = _FakeEvidence([])
    publisher = ExperienceObservationPublisher(enabled=True, evidence=sink)
    result = publisher.publish_journey_event(
        session_started(),
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="corr-session",
    )
    assert result.ok is True
    assert result.status == PUBLISH_STATUS_PUBLISHED
    assert result.evidence_id == "ev-session_started"
    assert len(sink.calls) == 1
    assert isinstance(sink.calls[0], ObservedEvent)
    assert sink.calls[0].event_type == "session_started"
    assert (
        sink.calls[0].experience["observation_id"]
        == result.observation.observation_id
    )


def test_publisher_dependency_injection_accepts_custom_assembler():
    class TrackingAssembler(ObservationAssembler):
        def __init__(self) -> None:
            self.calls = 0

        def assemble_from_journey_event(self, *args, **kwargs):
            self.calls += 1
            return super().assemble_from_journey_event(*args, **kwargs)

    assembler = TrackingAssembler()
    sink = _FakeEvidence([])
    publisher = ExperienceObservationPublisher(
        enabled=True, evidence=sink, assembler=assembler
    )
    publisher.publish_journey_event(
        session_completed(),
        student_id="9",
        timestamp="2026-07-25T11:00:00+00:00",
    )
    assert assembler.calls == 1
    assert len(sink.calls) == 1


def test_publisher_failure_does_not_raise():
    sink = _FakeEvidence([], fail=True)
    publisher = ExperienceObservationPublisher(enabled=True, evidence=sink)
    result = publisher.publish_journey_event(
        reflection_skipped(),
        student_id="5",
        timestamp="2026-07-25T12:00:00+00:00",
    )
    assert result.ok is False
    assert result.status == PUBLISH_STATUS_FAILED
    assert result.reason == REASON_EVIDENCE_REJECTED
    assert "intake rejected" in result.message


def test_observation_to_observed_event_uses_public_evidence_contract():
    obs = ObservationAssembler().assemble_from_journey_event(
        mission_started(),
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="corr",
    )
    event = observation_to_observed_event(obs)
    assert isinstance(event, ObservedEvent)
    assert event.student_id == "42"
    assert event.event_type == "mission_started"
    assert event.claim_boundary == "organisation"
    assert event.evidence_class == "DELIVERY_EVENT"
    assert event.experience["observation_id"] == obs.observation_id
    assert event.source_refs[0].ref_kind == "experience"


def test_end_to_end_evidence_adapter_collect_event_integration():
    evidence = build_evidence_platform_adapter(enabled=True)
    assert evidence is not None
    publisher = ExperienceObservationPublisher(enabled=True, evidence=evidence)
    result = publisher.publish_journey_event(
        session_completed(),
        student_id="42",
        timestamp="2026-07-25T10:00:00+00:00",
        correlation_id="corr-e2e",
    )
    assert result.ok is True
    assert result.status == PUBLISH_STATUS_PUBLISHED
    assert result.evidence_id
    assert result.observation is not None
    assert result.observation.experience_event == "session_completed"


def test_publish_session_outcome_and_reflection_helpers():
    sink = _FakeEvidence([])
    publisher = ExperienceObservationPublisher(enabled=True, evidence=sink)
    outcome = SessionOutcome(
        mission_title="Geometry",
        completion_status="complete",
        reflection_available=True,
    )
    session_result = publisher.publish_session_outcome(
        outcome,
        student_id="8",
        timestamp="2026-07-25T14:00:00+00:00",
        experience_event="session_completed",
        correlation_id="c-out",
    )
    assert session_result.ok is True
    assert session_result.evidence_id == "ev-session_completed"

    from app.application.unified_journey import ReflectionExperience
    from app.application.unified_journey.reflection_states import ReflectionState

    reflection = ReflectionExperience(
        session_outcome=outcome,
        reflection_state=ReflectionState.SKIPPED,
    )
    reflection_result = publisher.publish_reflection(
        reflection,
        student_id="8",
        timestamp="2026-07-25T14:05:00+00:00",
        experience_event="reflection_skipped",
        correlation_id="c-ref",
    )
    assert reflection_result.ok is True
    assert reflection_result.evidence_id == "ev-reflection_skipped"
    assert len(sink.calls) == 2


def test_publisher_does_not_accept_non_observation():
    publisher = ExperienceObservationPublisher(enabled=True, evidence=_FakeEvidence([]))
    with pytest.raises(TypeError, match="ExperienceObservation"):
        publisher.publish({"not": "an observation"})  # type: ignore[arg-type]

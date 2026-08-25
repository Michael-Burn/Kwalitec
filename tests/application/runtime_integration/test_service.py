"""RuntimeIntegrationService Preferred Authority tests (RI-001)."""

from __future__ import annotations

from datetime import datetime
from types import SimpleNamespace
from unittest.mock import MagicMock

from app.application.educational_experience_engine.experience_service import (
    ExperienceTransformationService,
)
from app.application.educational_reasoning_engine.dto import DecisionView
from app.application.runtime_integration.dto import (
    AuthoritySource,
    FallbackReason,
    IntegrationSurface,
)
from app.application.runtime_integration.service import RuntimeIntegrationService
from app.application.runtime_integration.telemetry import RuntimeIntegrationTelemetry
from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.explanation import (
    DecisionExplanation,
    PriorityCalculation,
)
from app.domain.educational_reasoning_engine.version import REASONING_VERSION

AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _decision() -> EducationalDecision:
    return EducationalDecision(
        decision_id="ere-dec-svc",
        instance_id="sci-svc",
        decision_type=DecisionType.STUDY_NEW.value,
        curriculum_target="CS1.LO2",
        priority=0.8,
        rank_position=1,
        rationale_summary="Continue the incomplete curriculum path.",
        prerequisite_chain=(),
        estimated_effort_minutes=30,
        expected_educational_outcome=ExpectedOutcome.INTRODUCE_NODE.value,
        supporting_belief_ids=("tie-2",),
        supporting_curriculum_refs=("CS1.LO2",),
        supporting_evidence_ids=("lee-2",),
        applied_rule_ids=("incomplete_curriculum_paths",),
        reasoned_at=AS_OF,
        reasoning_version=REASONING_VERSION,
    )


def _view() -> DecisionView:
    decision = _decision()
    return DecisionView(
        decision=decision,
        explanation=DecisionExplanation(
            decision_id=decision.decision_id,
            contributing_beliefs=decision.supporting_belief_ids,
            curriculum_dependencies=decision.supporting_curriculum_refs,
            educational_rules_applied=decision.applied_rule_ids,
            evidence_references=decision.supporting_evidence_ids,
            priority_calculation=PriorityCalculation(
                raw_sum=decision.priority,
                clamped=decision.priority,
                formula="sum(deltas)",
                components=("incomplete_curriculum_paths:+0.8",),
            ),
            rule_proposals=(),
            rationale_summary=decision.rationale_summary,
            reasoning_version=decision.reasoning_version,
        ),
    )


def test_educational_intelligence_path_skips_runtime_a(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value={"legacy": True})
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = (_view(),)

    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: SimpleNamespace(
            instance_id="sci-svc", subject_code="CS1"
        ),
    )

    service = RuntimeIntegrationService(
        experience=ExperienceTransformationService(),
        decision_query=decision_query,
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=True,
    )
    result = service.resolve_for_surface(42, IntegrationSurface.DASHBOARD)

    assert result.authority is AuthoritySource.EDUCATIONAL_INTELLIGENCE
    assert result.decision_id == "ere-dec-svc"
    assert result.experience is not None
    runtime_a.assert_not_called()
    assert telemetry.educational_intelligence_adoption_pct() == 100.0
    assert telemetry.fallback_rate() == 0.0


def test_runtime_a_selected_when_no_sci(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value={"legacy": True})
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = ()

    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: None,
    )

    service = RuntimeIntegrationService(
        decision_query=decision_query,
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=True,
    )
    result = service.resolve_for_surface(7, IntegrationSurface.RECOMMENDATION)

    assert result.authority is AuthoritySource.RUNTIME_A_COMPATIBILITY
    assert result.fallback_reason is FallbackReason.NO_ACTIVE_SCI
    assert result.compatibility_payload == {"legacy": True}
    runtime_a.assert_called_once()
    assert telemetry.fallback_rate() == 1.0


def test_runtime_a_selected_when_no_decisions(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value="ok")
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = ()

    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: SimpleNamespace(
            instance_id="sci-empty", subject_code="CS1"
        ),
    )

    service = RuntimeIntegrationService(
        decision_query=decision_query,
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=True,
    )
    result = service.resolve_for_surface(9, IntegrationSurface.COACH)

    assert result.authority is AuthoritySource.RUNTIME_A_COMPATIBILITY
    assert result.fallback_reason is FallbackReason.NO_EDUCATIONAL_DECISIONS
    assert result.instance_id == "sci-empty"
    runtime_a.assert_called_once()


def test_flag_off_forces_runtime_a(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value="compat")
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = (_view(),)

    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: SimpleNamespace(
            instance_id="sci-svc", subject_code="CS1"
        ),
    )

    service = RuntimeIntegrationService(
        decision_query=decision_query,
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=False,
    )
    result = service.resolve_recommendation(3)
    assert result.authority is AuthoritySource.RUNTIME_A_COMPATIBILITY
    assert result.fallback_reason is FallbackReason.RUNTIME_INTEGRATION_DISABLED
    runtime_a.assert_called_once()


def test_surface_consistency_across_dashboard_mission_coach(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = (_view(),)
    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: SimpleNamespace(
            instance_id="sci-svc", subject_code="CS1"
        ),
    )
    service = RuntimeIntegrationService(
        experience=ExperienceTransformationService(),
        decision_query=decision_query,
        telemetry=telemetry,
        integration_enabled=True,
    )
    surfaces = [
        IntegrationSurface.DASHBOARD,
        IntegrationSurface.DAILY_MISSION,
        IntegrationSurface.COACH,
        IntegrationSurface.REVISION_PLANNER,
    ]
    results = [service.resolve_for_surface(1, surface) for surface in surfaces]
    decision_ids = {r.decision_id for r in results}
    assert decision_ids == {"ere-dec-svc"}
    titles = {
        r.experience.surfaces.experience.title
        for r in results
        if r.experience is not None
    }
    assert len(titles) == 1
    whys = {
        r.experience.surfaces.experience.educational_rationale
        for r in results
        if r.experience is not None
    }
    assert len(whys) == 1
    why = next(iter(whys))
    assert why != "Continue the incomplete curriculum path."
    assert "LO2" in why
    assert "rank" not in why.lower()
    assert "priority" not in why.lower()


def test_has_educational_intelligence_does_not_record_telemetry(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = (_view(),)
    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda student_id, subject_code=None: SimpleNamespace(
            instance_id="sci-svc", subject_code="CS1"
        ),
    )
    service = RuntimeIntegrationService(
        decision_query=decision_query,
        telemetry=telemetry,
        integration_enabled=True,
    )
    assert service.has_educational_intelligence(11) is True
    assert telemetry.snapshot().total_requests == 0

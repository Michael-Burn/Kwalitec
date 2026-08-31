"""RI-002 verification: preferred authority, telemetry, no RIS bypass."""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path
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

# Legacy Runtime A / RI-002 surfaces that must still route through RIS.
_RI002_RUNTIME_INTEGRATION_SURFACES = (
    Path("app/dashboard/routes.py"),
    Path("app/mission/routes.py"),
    Path("app/presentation/session/views.py"),
    Path("app/application/student_experience/revision_service.py"),
    Path("app/infrastructure/adapters/educational_runtime_bridge/recommendation_adapter.py"),
)

# V1S-007 Runtime C canonical surfaces (Educational Runtime, not RIS).
_RUNTIME_C_CANONICAL_SURFACES = (
    Path("app/presentation/student/views.py"),
)

_STUDENT_SURFACE_MODULES = _RI002_RUNTIME_INTEGRATION_SURFACES + _RUNTIME_C_CANONICAL_SURFACES


def _decision_view() -> DecisionView:
    decision = EducationalDecision(
        decision_id="ere-ri002",
        instance_id="sci-ri002",
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


def test_preferred_authority_selected_when_prerequisites_exist(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value={"legacy": True})
    decision_query = MagicMock()
    decision_query.highest_value_actions.return_value = [_decision_view()]
    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda *_a, **_k: type(
            "Inst",
            (),
            {"instance_id": "sci-ri002", "subject_code": "CS1"},
        )(),
    )
    svc = RuntimeIntegrationService(
        experience=ExperienceTransformationService(),
        decision_query=decision_query,
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=True,
    )
    result = svc.resolve_for_surface(
        1, IntegrationSurface.DASHBOARD, subject_code="CS1"
    )
    assert result.authority is AuthoritySource.EDUCATIONAL_INTELLIGENCE
    runtime_a.assert_not_called()
    snap = telemetry.snapshot()
    assert snap.educational_intelligence_count == 1
    assert snap.fallback_count == 0
    assert "dashboard" in snap.by_surface


def test_fallback_telemetry_emitted_correctly(monkeypatch) -> None:
    telemetry = RuntimeIntegrationTelemetry()
    runtime_a = MagicMock(return_value={"legacy": True})
    monkeypatch.setattr(
        "app.application.runtime_integration.service.resolve_active_instance",
        lambda *_a, **_k: None,
    )
    svc = RuntimeIntegrationService(
        decision_query=MagicMock(),
        telemetry=telemetry,
        runtime_a_fallback=runtime_a,
        integration_enabled=True,
    )
    result = svc.resolve_for_surface(7, IntegrationSurface.RECOMMENDATION)
    assert result.authority is AuthoritySource.RUNTIME_A_COMPATIBILITY
    assert result.fallback_reason is FallbackReason.NO_ACTIVE_SCI
    runtime_a.assert_called_once()
    snap = telemetry.snapshot()
    assert snap.fallback_count == 1
    assert snap.fallback_by_reason[FallbackReason.NO_ACTIVE_SCI.value] == 1
    assert snap.by_surface["recommendation"].fallback_count == 1


def test_student_surfaces_route_through_runtime_integration_service() -> None:
    """Legacy surfaces use RIS; Runtime C Home/Journey use Educational Runtime."""
    for path in _RI002_RUNTIME_INTEGRATION_SURFACES:
        text = path.read_text(encoding="utf-8")
        assert "runtime_integration" in text or "RuntimeIntegrationService" in text, (
            f"{path} must reference Runtime Integration"
        )
    for path in _RUNTIME_C_CANONICAL_SURFACES:
        text = path.read_text(encoding="utf-8")
        assert (
            "educational_runtime_engine" in text
            or "EducationalExperienceService" in text
        ), f"{path} must reference Educational Runtime (V1S-007 singularity)"


def test_student_surfaces_do_not_import_educational_reasoning_engine() -> None:
    forbidden = {
        "app.domain.educational_reasoning_engine.engine",
        "app.domain.educational_reasoning_engine.rules",
        "app.application.educational_reasoning_engine.reasoning_service",
    }
    for path in _STUDENT_SURFACE_MODULES:
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        assert not forbidden.intersection(imports), path


def test_adoption_modules_do_not_import_reasoning_engine() -> None:
    root = Path("app/application/runtime_integration")
    forbidden = {
        "app.domain.educational_reasoning_engine.engine",
        "app.domain.educational_reasoning_engine.rules",
        "app.application.educational_reasoning_engine.reasoning_service",
    }
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        imports: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                imports.extend(alias.name for alias in node.names)
            elif isinstance(node, ast.ImportFrom) and node.module:
                imports.append(node.module)
        assert not forbidden.intersection(imports), path

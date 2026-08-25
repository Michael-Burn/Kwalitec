"""Application tests for Educational Experience Engine (EX-001)."""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path

import pytest

from app.application.educational_experience_engine.contracts import (
    ExperienceEnginePort,
)
from app.application.educational_experience_engine.exceptions import (
    DecisionRequiredError,
)
from app.application.educational_experience_engine.experience_service import (
    ExperienceTransformationService,
)
from app.application.educational_reasoning_engine.dto import DecisionView
from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION
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


def _decision(
    *,
    decision_id: str = "ere-dec-1",
    decision_type: str = DecisionType.STUDY_NEW.value,
    priority: float = 0.6,
    rank: int = 1,
    target: str = "CS1.LO1",
) -> EducationalDecision:
    return EducationalDecision(
        decision_id=decision_id,
        instance_id="sci-1",
        decision_type=decision_type,
        curriculum_target=target,
        priority=priority,
        rank_position=rank,
        rationale_summary="Study new incomplete learning objective.",
        prerequisite_chain=(),
        estimated_effort_minutes=25,
        expected_educational_outcome=ExpectedOutcome.INTRODUCE_NODE.value,
        supporting_belief_ids=("tie-1",),
        supporting_curriculum_refs=(target,),
        supporting_evidence_ids=("lee-1",),
        applied_rule_ids=("incomplete_curriculum_paths",),
        reasoned_at=AS_OF,
        reasoning_version=REASONING_VERSION,
    )


def _view(decision: EducationalDecision) -> DecisionView:
    explanation = DecisionExplanation(
        decision_id=decision.decision_id,
        contributing_beliefs=decision.supporting_belief_ids,
        curriculum_dependencies=decision.supporting_curriculum_refs,
        educational_rules_applied=decision.applied_rule_ids,
        evidence_references=decision.supporting_evidence_ids,
        priority_calculation=PriorityCalculation(
            raw_sum=decision.priority,
            clamped=decision.priority,
            formula="sum(deltas)",
            components=("incomplete_curriculum_paths:+0.6",),
        ),
        rule_proposals=(),
        rationale_summary=decision.rationale_summary,
        reasoning_version=decision.reasoning_version,
    )
    return DecisionView(decision=decision, explanation=explanation)


def test_service_implements_experience_engine_port() -> None:
    service = ExperienceTransformationService()
    assert isinstance(service, ExperienceEnginePort)


def test_present_all_surfaces_are_consistent() -> None:
    service = ExperienceTransformationService()
    decision = _decision()
    bundle = service.present_all_surfaces(decision, presented_at=AS_OF)

    assert bundle.experience.experience_version == EXPERIENCE_VERSION
    assert bundle.daily_mission.decision_id == decision.decision_id
    assert bundle.coach.decision_id == decision.decision_id
    assert bundle.dashboard_card.decision_id == decision.decision_id
    assert bundle.revision_entry.decision_id == decision.decision_id
    assert bundle.session_briefing.decision_id == decision.decision_id

    assert (
        bundle.daily_mission.why_this_mission
        == bundle.coach.educational_why
        == bundle.dashboard_card.why_label
        == bundle.experience.educational_rationale
    )
    # Catalogue why — not the internal EI-007 rationale_summary.
    assert bundle.experience.educational_rationale != decision.rationale_summary
    assert "LO1" in bundle.experience.educational_rationale
    assert "rank" not in bundle.experience.educational_rationale.lower()
    assert (
        bundle.daily_mission.curriculum_target
        == bundle.session_briefing.curriculum_target
        == decision.curriculum_target
    )


def test_explainable_presentation_preserves_traceability() -> None:
    service = ExperienceTransformationService()
    payload = service.explainable_presentation(_decision())
    assert payload["what_is_recommended"]
    assert payload["why_it_is_recommended"]
    assert payload["curriculum_area"]
    assert payload["curriculum_target"] == "CS1.LO1"
    assert payload["expected_learning_outcome"]
    assert payload["estimated_effort"]["minutes"] == 25
    assert payload["trace"]["decision_id"] == "ere-dec-1"
    assert payload["trace"]["supporting_belief_ids"] == ["tie-1"]
    assert payload["experience_version"] == EXPERIENCE_VERSION


def test_decision_view_projection_ignores_explanation_for_ranking() -> None:
    """Experience engine must not re-rank; it only presents the decision."""
    service = ExperienceTransformationService()
    decision = _decision(priority=0.42, rank=3)
    view = _view(decision)
    bundle = service.present_decision_view(view, presented_at=AS_OF)
    assert bundle.dashboard_card.rank_position == 3
    assert bundle.dashboard_card.priority == pytest.approx(0.42)


def test_missing_decision_raises() -> None:
    service = ExperienceTransformationService()
    with pytest.raises(DecisionRequiredError):
        service.present(None)  # type: ignore[arg-type]


def test_experience_service_does_not_import_flask_request() -> None:
    path = Path("app/application/educational_experience_engine/experience_service.py")
    tree = ast.parse(path.read_text(encoding="utf-8"))
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    forbidden = {
        "flask",
        "flask.request",
        "flask.session",
    }
    assert not forbidden.intersection(imports)


def test_architecture_purity_no_decision_mutation_helpers() -> None:
    """Experience application package must not write ere_* tables."""
    root = Path("app/application/educational_experience_engine")
    for path in root.rglob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "EreEducationalDecision" not in text
        assert "db.session.add" not in text
        assert "db.session.commit" not in text

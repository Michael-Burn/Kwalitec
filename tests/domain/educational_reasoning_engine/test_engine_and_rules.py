"""Domain tests for Educational Reasoning Engine (EI-007)."""

from __future__ import annotations

from datetime import datetime

import pytest

from app.domain.educational_reasoning_engine.context import (
    NodeReasoningState,
    ReasoningContext,
)
from app.domain.educational_reasoning_engine.decision import EducationalDecision
from app.domain.educational_reasoning_engine.decision_type import (
    DecisionType,
    ExpectedOutcome,
)
from app.domain.educational_reasoning_engine.engine import EducationalReasoningEngine
from app.domain.educational_reasoning_engine.rules.effort_estimation import (
    EffortEstimationRule,
)
from app.domain.educational_reasoning_engine.rules.incomplete_paths import (
    IncompletePathsRule,
)
from app.domain.educational_reasoning_engine.rules.low_confidence import (
    LowConfidenceRule,
)
from app.domain.educational_reasoning_engine.rules.prerequisite_satisfaction import (
    PrerequisiteSatisfactionRule,
)
from app.domain.educational_reasoning_engine.rules.revision_due import RevisionDueRule
from app.domain.educational_reasoning_engine.rules.study_continuity import (
    StudyContinuityRule,
)
from app.domain.educational_reasoning_engine.rules.syllabus_priority import (
    SyllabusPriorityRule,
)
from app.domain.educational_reasoning_engine.rules.topic_dependency import (
    TopicDependencyRule,
)
from app.domain.educational_reasoning_engine.version import REASONING_VERSION
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    RevisionStatus,
)
from app.domain.twin_inference.learning_state import LearningState

AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _node(
    nid: str,
    *,
    kind: str = "learning_objective",
    completion: str = CompletionStatus.NOT_STARTED.value,
    revision: str = RevisionStatus.NOT_DUE.value,
    mastery: float = 0.0,
    confidence: float = 0.0,
    learning_state: str = LearningState.UNKNOWN.value,
    belief_id: str | None = None,
    evidence: tuple[str, ...] = (),
    prereqs: tuple[str, ...] = (),
    syllabus_index: int = 0,
    difficulty: str = "foundational",
    last_interaction_at: datetime | None = None,
) -> NodeReasoningState:
    return NodeReasoningState(
        node_stable_id=nid,
        node_kind=kind,
        completion_status=completion,
        revision_status=revision,
        mastery=mastery,
        confidence=confidence,
        learning_state=learning_state,
        belief_id=belief_id,
        supporting_evidence_ids=evidence,
        prerequisite_ids=prereqs,
        syllabus_index=syllabus_index,
        difficulty=difficulty,
        last_interaction_at=last_interaction_at,
        attempts=0,
        total_study_time_minutes=0,
    )


def test_decision_requires_rationale() -> None:
    with pytest.raises(ValueError, match="rationale_summary"):
        EducationalDecision(
            decision_id="ere-1",
            instance_id="sci-1",
            decision_type=DecisionType.STUDY_NEW.value,
            curriculum_target="CS1.LO1",
            priority=0.5,
            rank_position=1,
            rationale_summary="  ",
            prerequisite_chain=(),
            estimated_effort_minutes=30,
            expected_educational_outcome=ExpectedOutcome.INTRODUCE_NODE.value,
            supporting_belief_ids=(),
            supporting_curriculum_refs=("CS1.LO1",),
            supporting_evidence_ids=(),
            applied_rule_ids=("incomplete_curriculum_paths",),
            reasoned_at=AS_OF,
        )


def test_rules_are_independently_testable() -> None:
    context = ReasoningContext(
        instance_id="sci-1",
        as_of=AS_OF,
        nodes=(
            _node(
                "LO-A",
                completion=CompletionStatus.COMPLETED.value,
                mastery=0.9,
                confidence=0.8,
                belief_id="tie-a",
                syllabus_index=0,
            ),
            _node(
                "LO-B",
                completion=CompletionStatus.NOT_STARTED.value,
                mastery=0.0,
                confidence=0.0,
                prereqs=("LO-A",),
                belief_id="tie-b",
                syllabus_index=1,
            ),
            _node(
                "LO-C",
                completion=CompletionStatus.IN_PROGRESS.value,
                mastery=0.4,
                confidence=0.2,
                belief_id="tie-c",
                evidence=("lee-1",),
                syllabus_index=2,
                revision=RevisionStatus.DUE.value,
                last_interaction_at=datetime(2026, 7, 27, 10, 0, 0),
            ),
        ),
    )

    assert PrerequisiteSatisfactionRule().apply(context) == ()
    incomplete = IncompletePathsRule().apply(context)
    assert {p.curriculum_target for p in incomplete} == {"LO-B", "LO-C"}
    low = LowConfidenceRule().apply(context)
    assert [p.curriculum_target for p in low] == ["LO-C"]
    revise = RevisionDueRule().apply(context)
    assert [p.curriculum_target for p in revise] == ["LO-C"]
    assert SyllabusPriorityRule().apply(context)
    assert TopicDependencyRule().apply(context)
    assert EffortEstimationRule().apply(context)
    continuity = StudyContinuityRule().apply(context)
    assert continuity
    assert continuity[0].decision_type == DecisionType.CONTINUE_PATH.value


def test_prerequisite_rule_targets_weak_prereq() -> None:
    context = ReasoningContext(
        instance_id="sci-1",
        as_of=AS_OF,
        nodes=(
            _node("LO-A", mastery=0.1, belief_id="tie-a"),
            _node(
                "LO-B",
                completion=CompletionStatus.NOT_STARTED.value,
                prereqs=("LO-A",),
                belief_id="tie-b",
                syllabus_index=1,
            ),
        ),
    )
    proposals = PrerequisiteSatisfactionRule().apply(context)
    assert len(proposals) == 1
    assert proposals[0].curriculum_target == "LO-A"
    assert proposals[0].decision_type == DecisionType.SATISFY_PREREQUISITE.value


def test_engine_deterministic_and_explainable() -> None:
    context = ReasoningContext(
        instance_id="sci-1",
        as_of=AS_OF,
        nodes=(
            _node(
                "LO-1",
                completion=CompletionStatus.NOT_STARTED.value,
                belief_id="tie-1",
                syllabus_index=0,
            ),
            _node(
                "LO-2",
                completion=CompletionStatus.IN_PROGRESS.value,
                mastery=0.35,
                confidence=0.25,
                belief_id="tie-2",
                evidence=("lee-2",),
                syllabus_index=1,
                revision=RevisionStatus.OVERDUE.value,
                last_interaction_at=datetime(2026, 7, 26, 9, 0, 0),
            ),
        ),
    )
    engine = EducationalReasoningEngine()
    first = engine.evaluate(context)
    second = engine.evaluate(context)

    assert first.reasoning_version == REASONING_VERSION
    assert len(first.items) >= 1
    assert first.to_dict() == second.to_dict()

    top = first.items[0]
    assert top.decision.rationale_summary
    assert top.decision.applied_rule_ids
    assert top.explanation.educational_rules_applied
    assert top.explanation.priority_calculation.components
    assert top.decision.rank_position == 1


def test_revision_outranks_plain_study_when_overdue() -> None:
    context = ReasoningContext(
        instance_id="sci-1",
        as_of=AS_OF,
        nodes=(
            _node("LO-NEW", syllabus_index=0, belief_id="tie-n"),
            _node(
                "LO-REV",
                completion=CompletionStatus.COMPLETED.value,
                mastery=0.8,
                confidence=0.7,
                syllabus_index=1,
                revision=RevisionStatus.OVERDUE.value,
                belief_id="tie-r",
            ),
        ),
    )
    result = EducationalReasoningEngine().evaluate(context)
    types = [i.decision.decision_type for i in result.items]
    assert DecisionType.REVISE.value in types
    revise = next(
        i for i in result.items if i.decision.decision_type == DecisionType.REVISE.value
    )
    study = next(
        (
            i
            for i in result.items
            if i.decision.decision_type == DecisionType.STUDY_NEW.value
        ),
        None,
    )
    assert study is not None
    assert revise.decision.priority >= study.decision.priority

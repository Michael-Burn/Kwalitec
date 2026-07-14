"""Tests for KnowledgeUpdateStrategy (Capability 4.9.9).

Version 1 educational conservatism: preserve unless assessment observation
satisfies educational sufficiency. Framework-free; Knowledge domain only.
"""

from __future__ import annotations

import ast
import logging
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.application.twin_update import (
    DomainStrategyOutput,
    EducationalEvidencePackage,
    KnowledgeStrategyOutput,
    KnowledgeUpdateStrategy,
    ObservedEvent,
    ReasoningTrace,
    TwinComposer,
)
from app.domain.twin import (
    BehaviourState,
    DigitalTwin,
    GoalState,
    IdentityState,
    KnowledgeState,
    MemoryState,
    PerformanceState,
    TopicMasteryRecord,
)

STRATEGY_MODULE = (
    Path(__file__).resolve().parents[2]
    / "app"
    / "application"
    / "twin_update"
    / "knowledge_strategy.py"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
        "sqlalchemy",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
    "app.domain.readiness",
    "app.domain.decision",
    "app.domain.recommendation",
    "app.domain.mission",
    "app.application.twin_repository",
    "app.application.twin_update.composer",
    "app.application.twin_update.coordinator",
)

FORBIDDEN_LOGIC_TOKENS = (
    "pass_probability",
    "OverallPosture",
    "WarrantPosture",
    "nominate_candidates",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "ReadinessAggregation",
    "re_rank",
    "rerank",
)


def _ts() -> datetime:
    return datetime(2026, 7, 14, 11, 0, tzinfo=UTC)


def _identity() -> IdentityState:
    return IdentityState.create(
        student_id="student-42",
        curriculum_id="CS1-2026",
        current_exam="CS1",
        target_sitting=date(2026, 9, 15),
    )


def _twin(**overrides: object) -> DigitalTwin:
    defaults: dict[str, object] = {
        "identity": _identity(),
        "goals": GoalState.create(),
        "knowledge": KnowledgeState.create(),
        "memory": MemoryState.create(),
        "behaviour": BehaviourState.create(),
        "performance": PerformanceState.create(),
    }
    defaults.update(overrides)
    identity = defaults.pop("identity")
    return DigitalTwin.create(identity, **defaults)  # type: ignore[arg-type]


def _package(**overrides: object) -> EducationalEvidencePackage:
    defaults: dict[str, object] = {
        "evidence_id": "ev-kn-001",
        "student_id": "student-42",
        "evidence_timestamp": _ts(),
        "provenance": "observed:end_of_session",
        "study_plan_id": "plan-1",
        "curriculum_id": "CS1-2026",
        "observed_events": (ObservedEvent.SYSTEM_TIMESTAMP,),
    }
    defaults.update(overrides)
    return EducationalEvidencePackage.create(**defaults)  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Preservation (Version 1 sufficiency)
# ═══════════════════════════════════════════════════════════════════════════════


class TestPreservation:
    def test_no_evidence_preserves(self) -> None:
        twin = _twin()
        knowledge = twin.knowledge
        out = KnowledgeUpdateStrategy().interpret(twin, _package())
        assert out.preserved is True
        assert out.domain_contribution is knowledge
        assert "no educational warrant" in out.reasoning_trace.statement

    def test_mission_completed_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                observed_events=(ObservedEvent.MISSION_COMPLETED,),
                topic_id="topic-4.2",
                mission_id="mission-1",
            ),
        )
        assert out.preserved is True
        assert out.domain_contribution is twin.knowledge
        assert (
            out.reasoning_trace.statement
            == "Knowledge preserved — mission completion alone is insufficient."
        )

    def test_practice_completed_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
                topic_id="topic-4.2",
                practice_count=5,
            ),
        )
        assert out.preserved is True
        assert (
            out.reasoning_trace.statement
            == "Knowledge preserved — practice observation without assessment."
        )

    def test_practice_attempted_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(observed_events=(ObservedEvent.PRACTICE_ATTEMPTED,)),
        )
        assert out.preserved is True
        assert "practice observation without assessment" in (
            out.reasoning_trace.statement
        )

    def test_reflection_only_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                observed_events=(ObservedEvent.SESSION_ENDED_MANUAL,),
                reflection="I understood generalised linear models today.",
            ),
        )
        assert out.preserved is True
        assert (
            out.reasoning_trace.statement
            == "Knowledge preserved — reflection alone is insufficient."
        )

    def test_study_duration_only_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                observed_events=(ObservedEvent.STUDY_DURATION,),
                declared_duration=45.0,
            ),
        )
        assert out.preserved is True
        assert (
            out.reasoning_trace.statement
            == "Knowledge preserved — study duration alone is insufficient."
        )

    def test_assessment_without_topic_preserves(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
                assessment_result={"score": 8, "max_score": 10},
            ),
        )
        assert out.preserved is True
        assert "without topic scope" in out.reasoning_trace.statement
        assert out.domain_contribution is twin.knowledge


# ═══════════════════════════════════════════════════════════════════════════════
# Assessment → eligible update
# ═══════════════════════════════════════════════════════════════════════════════


class TestAssessmentUpdate:
    def test_assessment_observation_updates_knowledge(self) -> None:
        twin = _twin()
        evidence = _package(
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
            topic_id="topic-4.2",
            assessment_result={"score": 7, "max_score": 10},
        )
        out = KnowledgeUpdateStrategy().interpret(twin, evidence)

        assert out.preserved is False
        assert isinstance(out, KnowledgeStrategyOutput)
        assert isinstance(out, DomainStrategyOutput)
        assert out.owned_domain == "knowledge"
        assert out.strategy_identity == "Knowledge"
        knowledge = out.domain_contribution
        assert isinstance(knowledge, KnowledgeState)
        assert knowledge is not twin.knowledge
        assert "topic-4.2" in {r.topic_id for r in knowledge.topic_mastery}
        assert evidence.evidence_id in knowledge.evidence_ids
        topic = next(r for r in knowledge.topic_mastery if r.topic_id == "topic-4.2")
        assert topic.mastery_belief is None
        assert knowledge.last_updated == evidence.evidence_timestamp
        assert (
            out.reasoning_trace.statement
            == "Knowledge updated — assessment observation satisfied "
            "Version 1 educational sufficiency."
        )

    def test_assessment_preserves_existing_mastery_belief(self) -> None:
        prior = TopicMasteryRecord.create(
            "topic-4.2",
            mastery_belief=0.4,
            evidence_ids=("ev-prior",),
        )
        twin = _twin(knowledge=KnowledgeState.create(topic_mastery=[prior]))
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                evidence_id="ev-kn-002",
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
                topic_id="topic-4.2",
                assessment_result={"items_correct": 3, "items_total": 5},
            ),
        )
        assert out.preserved is False
        topic = next(
            r
            for r in out.domain_contribution.topic_mastery
            if r.topic_id == "topic-4.2"
        )
        assert topic.mastery_belief == 0.4
        assert "ev-prior" in topic.evidence_ids
        assert "ev-kn-002" in topic.evidence_ids


# ═══════════════════════════════════════════════════════════════════════════════
# Failure behaviour
# ═══════════════════════════════════════════════════════════════════════════════


class TestFailureBehaviour:
    def test_invalid_knowledge_state_fails(self) -> None:
        twin = _twin()
        object.__setattr__(twin, "knowledge", "not-knowledge")  # type: ignore[misc]
        with pytest.raises(ValueError, match="Invalid KnowledgeState"):
            KnowledgeUpdateStrategy().interpret(twin, _package())

    def test_unknown_observed_event_rejected(self) -> None:
        # Bypass package.create validation by constructing a raw package shape
        # that carries an illegal token after structural creation would have
        # rejected it — Strategy still fails closed.
        package = _package()
        object.__setattr__(
            package,
            "observed_events",
            ("invented_mastery_event",),  # type: ignore[misc]
        )
        with pytest.raises(ValueError, match="unknown observed_event"):
            KnowledgeUpdateStrategy().interpret(_twin(), package)

    def test_malformed_empty_assessment_result_fails(self) -> None:
        package = _package(
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
            topic_id="topic-4.2",
        )
        object.__setattr__(package, "assessment_result", {})  # type: ignore[misc]
        with pytest.raises(ValueError, match="malformed assessment_result"):
            KnowledgeUpdateStrategy().interpret(_twin(), package)

    def test_non_mapping_assessment_result_fails_at_package(self) -> None:
        with pytest.raises(ValueError, match="assessment_result"):
            _package(assessment_result=["not", "a", "mapping"])  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Isolation / immutability / explainability / determinism
# ═══════════════════════════════════════════════════════════════════════════════


class TestDomainIsolation:
    def test_never_returns_whole_twin(self) -> None:
        out = KnowledgeUpdateStrategy().interpret(
            _twin(),
            _package(
                topic_id="topic-4.2",
                assessment_result={"score": 1, "max_score": 1},
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
            ),
        )
        assert not isinstance(out.domain_contribution, DigitalTwin)
        assert isinstance(out.domain_contribution, KnowledgeState)

    def test_current_twin_immutable(self) -> None:
        behaviour = BehaviourState.create()
        memory = MemoryState.create()
        goals = GoalState.create()
        performance = PerformanceState.create()
        knowledge = KnowledgeState.create()
        twin = _twin(
            behaviour=behaviour,
            memory=memory,
            goals=goals,
            performance=performance,
            knowledge=knowledge,
        )
        KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                topic_id="topic-4.2",
                assessment_result={"score": 9, "max_score": 10},
                observed_events=(ObservedEvent.MISSION_COMPLETED,),
            ),
        )
        assert twin.knowledge is knowledge
        assert twin.behaviour is behaviour
        assert twin.memory is memory
        assert twin.goals is goals
        assert twin.performance is performance
        assert twin.knowledge.topic_mastery == ()

    def test_explainability_always_produced(self) -> None:
        for package in (
            _package(),
            _package(observed_events=(ObservedEvent.MISSION_COMPLETED,)),
            _package(
                topic_id="t1",
                assessment_result={"score": 1, "max_score": 1},
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
            ),
        ):
            out = KnowledgeUpdateStrategy().interpret(_twin(), package)
            assert isinstance(out.reasoning_trace, ReasoningTrace)
            assert out.reasoning_trace.statement.startswith("Knowledge ")

    def test_deterministic_behaviour(self) -> None:
        twin = _twin(
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create("topic-a", evidence_ids=("e0",))
                ],
                evidence_ids=("e0",),
            )
        )
        evidence = _package(
            topic_id="topic-a",
            assessment_result={"score": 2, "max_score": 4},
            observed_events=(ObservedEvent.PRACTICE_COMPLETED,),
        )
        first = KnowledgeUpdateStrategy().interpret(twin, evidence)
        second = KnowledgeUpdateStrategy().interpret(twin, evidence)
        assert first == second
        assert first.domain_contribution == second.domain_contribution
        assert first.reasoning_trace == second.reasoning_trace


class TestComposerCompatibility:
    def test_output_assembles_via_composer(self) -> None:
        twin = _twin()
        out = KnowledgeUpdateStrategy().interpret(
            twin,
            _package(
                topic_id="topic-4.2",
                assessment_result={"score": 5, "max_score": 10},
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
            ),
        )
        successor = TwinComposer().compose(twin, (out,))
        assert successor.knowledge is out.domain_contribution
        assert successor.behaviour is twin.behaviour
        assert successor.memory is twin.memory
        assert successor.identity is twin.identity


class TestLogging:
    def test_operational_logging_on_preserve(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.INFO)
        KnowledgeUpdateStrategy().interpret(
            _twin(),
            _package(observed_events=(ObservedEvent.MISSION_COMPLETED,)),
        )
        messages = [r.getMessage() for r in caplog.records]
        assert "Knowledge Strategy started" in messages
        assert "Evidence validated" in messages
        assert "Knowledge preserved" in messages
        assert "Strategy completed" in messages
        joined = " ".join(messages)
        assert "mastery" not in joined.lower() or "Knowledge preserved" in joined
        assert "ready" not in joined.lower()
        assert "recommend" not in joined.lower()

    def test_operational_logging_on_update(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        caplog.set_level(logging.INFO)
        KnowledgeUpdateStrategy().interpret(
            _twin(),
            _package(
                topic_id="topic-4.2",
                assessment_result={"score": 1, "max_score": 1},
                observed_events=(ObservedEvent.TOPIC_STUDIED,),
            ),
        )
        messages = [r.getMessage() for r in caplog.records]
        assert "Knowledge updated" in messages
        assert "Strategy completed" in messages


class TestArchitectureIndependence:
    def test_no_forbidden_imports(self) -> None:
        tree = ast.parse(STRATEGY_MODULE.read_text(encoding="utf-8"))
        imported: set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imported.add(alias.name.split(".")[0])
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    imported.add(node.module)
        for root in FORBIDDEN_ROOT_MODULES:
            assert root not in imported
        for module in imported:
            for prefix in FORBIDDEN_PREFIXES:
                assert not module.startswith(prefix), module

    def test_no_forbidden_logic_tokens(self) -> None:
        src = STRATEGY_MODULE.read_text(encoding="utf-8")
        for token in FORBIDDEN_LOGIC_TOKENS:
            assert token not in src, token

    def test_protocol_surface(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        assert strategy.strategy_identity == "Knowledge"
        assert callable(strategy.interpret)

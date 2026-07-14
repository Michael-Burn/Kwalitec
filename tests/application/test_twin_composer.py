"""Tests for TwinComposer (Capability 4.9.8).

Covers happy path, per-domain replacement, multi-domain replacement,
unchanged domain preservation, duplicate / unknown domain rejection,
Current Twin immutability, complete Successor Twin creation, invalid
outputs, logging, and framework / educational-reasoning independence.
"""

from __future__ import annotations

import ast
import logging
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.application.twin_update import (
    DomainOutputCollection,
    DomainStrategyOutput,
    TwinComposer,
    TwinCompositionError,
)
from app.domain.twin import (
    BehaviourState,
    DigitalTwin,
    GoalState,
    IdentityState,
    KnowledgeState,
    MemoryState,
    PerformanceState,
    PerformanceSummary,
    PredictionState,
    RetentionRecord,
    TopicMasteryRecord,
)

TWIN_UPDATE_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "twin_update"
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
)

FORBIDDEN_LOGIC_TOKENS = (
    "mastery_belief",
    "average(",
    "pass_probability",
    "OverallPosture",
    "WarrantPosture",
    "nominate_candidates",
    "DecisionEngine",
    "RecommendationEngine",
    "MissionIntelligence",
    "ReadinessAggregation",
    "hybrid",
    "re_rank",
    "rerank",
    "EducationalEvidence",
    "interpret(",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures
# ═══════════════════════════════════════════════════════════════════════════════


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "CS1-2026",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _knowledge(
    *, topic_id: str = "t-old", belief: float | None = 0.2
) -> KnowledgeState:
    return KnowledgeState.create(
        topic_mastery=[
            TopicMasteryRecord.create(topic_id, mastery_belief=belief),
        ],
        evidence_ids=["ev-old-k"],
        last_updated=datetime(2026, 6, 1, tzinfo=UTC),
    )


def _memory(*, topic_id: str = "t-old", belief: float | None = 0.3) -> MemoryState:
    return MemoryState.create(
        retention=[
            RetentionRecord.create(topic_id, retention_belief=belief),
        ],
        revision_ids=["rev-old"],
        last_updated=datetime(2026, 6, 2, tzinfo=UTC),
    )


def _behaviour(*, session_id: str = "sess-old") -> BehaviourState:
    return BehaviourState.create(
        consistency_metrics={"adherence": 0.4},
        session_history_ids=[session_id],
        evidence_ids=["ev-old-b"],
        last_updated=datetime(2026, 6, 3, tzinfo=UTC),
    )


def _performance(*, scope_id: str = "scope-old") -> PerformanceState:
    return PerformanceState.create(
        assessment_ids=["assess-old"],
        performance_summaries=[
            PerformanceSummary.create(scope_id, summary={"score": 0.5}),
        ],
        evidence_ids=["ev-old-p"],
        last_updated=datetime(2026, 6, 4, tzinfo=UTC),
    )


def _goals(*, probability: float | None = 0.6) -> GoalState:
    return GoalState.create(
        target_pass_probability=probability,
        planned_study_hours_per_week=10.0,
    )


def _predictions() -> PredictionState:
    return PredictionState.create(
        readiness_snapshot=0.55,
        pass_probability_snapshot=0.45,
        as_of=datetime(2026, 6, 5, tzinfo=UTC),
        metadata={"source": "prior"},
    )


def _twin(**overrides: object) -> DigitalTwin:
    identity = overrides.pop("identity", None)
    if identity is None:
        identity = _identity()
    defaults: dict[str, object] = {
        "goals": _goals(),
        "knowledge": _knowledge(),
        "memory": _memory(),
        "behaviour": _behaviour(),
        "performance": _performance(),
        "predictions": _predictions(),
    }
    defaults.update(overrides)
    return DigitalTwin.create(identity, **defaults)  # type: ignore[arg-type]


def _output(
    domain: str,
    contribution: object,
    *,
    strategy: str | None = None,
    preserved: bool = False,
) -> DomainStrategyOutput:
    identity = strategy if strategy is not None else domain.capitalize()
    if domain == "goals":
        identity = strategy if strategy is not None else "Goal"
    return DomainStrategyOutput.create(
        identity,
        domain,
        contribution,
        preserved=preserved,
    )


def _new_knowledge() -> KnowledgeState:
    return KnowledgeState.create(
        topic_mastery=[
            TopicMasteryRecord.create("t-new", mastery_belief=0.8),
        ],
        evidence_ids=["ev-new-k"],
        last_updated=datetime(2026, 7, 14, tzinfo=UTC),
    )


def _new_memory() -> MemoryState:
    return MemoryState.create(
        retention=[
            RetentionRecord.create("t-new", retention_belief=0.7),
        ],
        revision_ids=["rev-new"],
        last_updated=datetime(2026, 7, 14, tzinfo=UTC),
    )


def _new_behaviour() -> BehaviourState:
    return BehaviourState.create(
        consistency_metrics={"adherence": 0.9},
        session_history_ids=["sess-new"],
        evidence_ids=["ev-new-b"],
        last_updated=datetime(2026, 7, 14, tzinfo=UTC),
    )


def _new_performance() -> PerformanceState:
    return PerformanceState.create(
        assessment_ids=["assess-new"],
        performance_summaries=[
            PerformanceSummary.create("scope-new", summary={"score": 0.9}),
        ],
        evidence_ids=["ev-new-p"],
        last_updated=datetime(2026, 7, 14, tzinfo=UTC),
    )


def _new_goals() -> GoalState:
    return GoalState.create(
        target_pass_probability=0.85,
        planned_study_hours_per_week=12.0,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Happy path
# ═══════════════════════════════════════════════════════════════════════════════


class TestHappyPath:
    def test_empty_outputs_carries_forward_complete_successor(self) -> None:
        twin = _twin()
        successor = TwinComposer().compose(twin, ())

        assert isinstance(successor, DigitalTwin)
        assert successor is not twin
        assert successor.identity is twin.identity
        assert successor.knowledge is twin.knowledge
        assert successor.memory is twin.memory
        assert successor.behaviour is twin.behaviour
        assert successor.performance is twin.performance
        assert successor.goals is twin.goals
        assert successor.predictions is twin.predictions

    def test_compose_via_domain_output_collection(self) -> None:
        twin = _twin()
        new_k = _new_knowledge()
        collection = DomainOutputCollection.from_outputs(
            (_output("knowledge", new_k),)
        )
        successor = TwinComposer().compose(twin, collection)

        assert successor.knowledge is new_k
        assert successor.memory is twin.memory


# ═══════════════════════════════════════════════════════════════════════════════
# Domain replacement
# ═══════════════════════════════════════════════════════════════════════════════


class TestKnowledgeReplacement:
    def test_replaces_knowledge_only(self) -> None:
        twin = _twin()
        new_k = _new_knowledge()
        successor = TwinComposer().compose(twin, (_output("knowledge", new_k),))

        assert successor.knowledge is new_k
        assert successor.knowledge is not twin.knowledge
        assert successor.memory is twin.memory
        assert successor.behaviour is twin.behaviour
        assert successor.performance is twin.performance
        assert successor.goals is twin.goals
        assert successor.predictions is twin.predictions
        assert successor.identity is twin.identity


class TestMemoryReplacement:
    def test_replaces_memory_only(self) -> None:
        twin = _twin()
        new_m = _new_memory()
        successor = TwinComposer().compose(twin, (_output("memory", new_m),))

        assert successor.memory is new_m
        assert successor.knowledge is twin.knowledge
        assert successor.behaviour is twin.behaviour


class TestBehaviourReplacement:
    def test_replaces_behaviour_only(self) -> None:
        twin = _twin()
        new_b = _new_behaviour()
        successor = TwinComposer().compose(twin, (_output("behaviour", new_b),))

        assert successor.behaviour is new_b
        assert successor.knowledge is twin.knowledge
        assert successor.memory is twin.memory


class TestPerformanceReplacement:
    def test_replaces_performance_only(self) -> None:
        twin = _twin()
        new_p = _new_performance()
        successor = TwinComposer().compose(twin, (_output("performance", new_p),))

        assert successor.performance is new_p
        assert successor.knowledge is twin.knowledge


class TestGoalsReplacement:
    def test_replaces_goals_only(self) -> None:
        twin = _twin()
        new_g = _new_goals()
        successor = TwinComposer().compose(twin, (_output("goals", new_g),))

        assert successor.goals is new_g
        assert successor.knowledge is twin.knowledge


class TestMultipleDomainReplacement:
    def test_replaces_knowledge_memory_and_behaviour(self) -> None:
        twin = _twin()
        new_k = _new_knowledge()
        new_m = _new_memory()
        new_b = _new_behaviour()
        outputs = (
            _output("knowledge", new_k),
            _output("memory", new_m),
            _output("behaviour", new_b),
        )

        successor = TwinComposer().compose(twin, outputs)

        assert successor.knowledge is new_k
        assert successor.memory is new_m
        assert successor.behaviour is new_b
        assert successor.performance is twin.performance
        assert successor.goals is twin.goals
        assert successor.predictions is twin.predictions

    def test_preserved_output_still_replaces_domain(self) -> None:
        twin = _twin()
        preserved = twin.behaviour
        successor = TwinComposer().compose(
            twin,
            (_output("behaviour", preserved, preserved=True),),
        )
        assert successor.behaviour is preserved
        assert successor.knowledge is twin.knowledge


class TestUnchangedDomainPreservation:
    def test_unsupplied_domains_are_same_objects(self) -> None:
        twin = _twin()
        new_k = _new_knowledge()
        successor = TwinComposer().compose(twin, (_output("knowledge", new_k),))

        assert successor.memory is twin.memory
        assert successor.behaviour is twin.behaviour
        assert successor.performance is twin.performance
        assert successor.goals is twin.goals
        assert successor.predictions is twin.predictions
        assert successor.identity is twin.identity


# ═══════════════════════════════════════════════════════════════════════════════
# Rejection / failure
# ═══════════════════════════════════════════════════════════════════════════════


class TestDuplicateDomainRejection:
    def test_rejects_duplicate_domain_outputs(self) -> None:
        twin = _twin()
        outputs = (
            _output("knowledge", _new_knowledge(), strategy="KnowledgeA"),
            _output("knowledge", _new_knowledge(), strategy="KnowledgeB"),
        )
        with pytest.raises(TwinCompositionError, match="duplicate domain"):
            TwinComposer().compose(twin, outputs)

    def test_domain_output_collection_rejects_duplicates(self) -> None:
        with pytest.raises(TwinCompositionError, match="duplicate domain"):
            DomainOutputCollection.from_outputs(
                (
                    _output("memory", _new_memory(), strategy="MemoryA"),
                    _output("memory", _new_memory(), strategy="MemoryB"),
                )
            )


class TestUnknownDomainRejection:
    def test_rejects_unknown_domain(self) -> None:
        twin = _twin()
        bad = DomainStrategyOutput.create(
            "Mystery",
            "confidence",
            domain_contribution=_new_knowledge(),
        )
        with pytest.raises(TwinCompositionError, match="unknown domain"):
            TwinComposer().compose(twin, (bad,))

    def test_rejects_identity_domain(self) -> None:
        twin = _twin()
        bad = DomainStrategyOutput.create(
            "IdentityHack",
            "identity",
            domain_contribution=twin.identity,
        )
        with pytest.raises(TwinCompositionError, match="unknown domain"):
            TwinComposer().compose(twin, (bad,))

    def test_rejects_predictions_domain(self) -> None:
        twin = _twin()
        bad = DomainStrategyOutput.create(
            "PredictionHack",
            "predictions",
            domain_contribution=twin.predictions,
        )
        with pytest.raises(TwinCompositionError, match="unknown domain"):
            TwinComposer().compose(twin, (bad,))


class TestInvalidStrategyOutput:
    def test_rejects_wrong_contribution_type(self) -> None:
        twin = _twin()
        bad = DomainStrategyOutput.create(
            "Knowledge",
            "knowledge",
            domain_contribution=_new_memory(),
        )
        with pytest.raises(TwinCompositionError, match="invalid Strategy Output"):
            TwinComposer().compose(twin, (bad,))

    def test_rejects_none_contribution(self) -> None:
        twin = _twin()
        bad = DomainStrategyOutput.create(
            "Knowledge",
            "knowledge",
            domain_contribution=None,
        )
        with pytest.raises(TwinCompositionError, match="invalid Strategy Output"):
            TwinComposer().compose(twin, (bad,))

    def test_rejects_non_output_items(self) -> None:
        twin = _twin()
        with pytest.raises(TwinCompositionError, match="DomainStrategyOutput"):
            TwinComposer().compose(twin, ("not-an-output",))  # type: ignore[arg-type]

    def test_rejects_none_outputs_sequence(self) -> None:
        twin = _twin()
        with pytest.raises(TwinCompositionError, match="required"):
            TwinComposer().compose(twin, None)


class TestMissingCurrentTwin:
    def test_rejects_none_current_twin(self) -> None:
        with pytest.raises(TwinCompositionError, match="Current Twin is required"):
            TwinComposer().compose(None, ())

    def test_rejects_non_digital_twin(self) -> None:
        with pytest.raises(TwinCompositionError, match="not a DigitalTwin"):
            TwinComposer().compose("twin", ())  # type: ignore[arg-type]


# ═══════════════════════════════════════════════════════════════════════════════
# Immutability / completeness
# ═══════════════════════════════════════════════════════════════════════════════


class TestCurrentTwinImmutability:
    def test_current_twin_unchanged_after_compose(self) -> None:
        twin = _twin()
        original_knowledge = twin.knowledge
        original_memory = twin.memory
        original_behaviour = twin.behaviour
        new_k = _new_knowledge()

        TwinComposer().compose(twin, (_output("knowledge", new_k),))

        assert twin.knowledge is original_knowledge
        assert twin.memory is original_memory
        assert twin.behaviour is original_behaviour
        assert twin.knowledge is not new_k

    def test_current_twin_frozen(self) -> None:
        twin = _twin()
        with pytest.raises(AttributeError):
            twin.knowledge = _new_knowledge()  # type: ignore[misc]


class TestCompleteSuccessorTwin:
    def test_successor_has_all_domains(self) -> None:
        twin = _twin()
        successor = TwinComposer().compose(
            twin,
            (
                _output("knowledge", _new_knowledge()),
                _output("performance", _new_performance()),
            ),
        )
        for attr in (
            "identity",
            "goals",
            "knowledge",
            "memory",
            "behaviour",
            "performance",
            "predictions",
        ):
            assert getattr(successor, attr) is not None

    def test_successor_is_new_frozen_instance(self) -> None:
        twin = _twin()
        successor = TwinComposer().compose(
            twin,
            (_output("goals", _new_goals()),),
        )
        assert successor is not twin
        assert isinstance(successor, DigitalTwin)
        with pytest.raises(AttributeError):
            successor.goals = twin.goals  # type: ignore[misc]


# ═══════════════════════════════════════════════════════════════════════════════
# Logging
# ═══════════════════════════════════════════════════════════════════════════════


class TestOperationalLogging:
    def test_logs_replacement_and_preservation(
        self, caplog: pytest.LogCaptureFixture
    ) -> None:
        twin = _twin()
        composer_logger = "app.application.twin_update.composer"
        with caplog.at_level(logging.INFO, logger=composer_logger):
            TwinComposer().compose(twin, (_output("knowledge", _new_knowledge()),))

        messages = [record.getMessage() for record in caplog.records]
        assert "Composer started" in messages
        assert "Knowledge domain replaced" in messages
        assert "Memory preserved" in messages
        assert "Behaviour preserved" in messages
        assert "Successor Twin assembled" in messages
        assert "Composer completed" in messages
        assert not any(
            "mastery" in msg.lower() and "warrant" in msg.lower()
            for msg in messages
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Architecture compliance
# ═══════════════════════════════════════════════════════════════════════════════


class TestArchitectureCompliance:
    def test_composer_module_has_no_flask_or_orm(self) -> None:
        path = TWIN_UPDATE_ROOT / "composer.py"
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    assert root not in FORBIDDEN_ROOT_MODULES
                    assert not any(
                        alias.name == p or alias.name.startswith(f"{p}.")
                        for p in FORBIDDEN_PREFIXES
                    )
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                assert root not in FORBIDDEN_ROOT_MODULES
                assert not any(
                    node.module == p or node.module.startswith(f"{p}.")
                    for p in FORBIDDEN_PREFIXES
                )

    def test_composer_source_avoids_educational_logic_tokens(self) -> None:
        source = (TWIN_UPDATE_ROOT / "composer.py").read_text(encoding="utf-8")
        for token in FORBIDDEN_LOGIC_TOKENS:
            assert token not in source, f"forbidden token present: {token}"

    def test_satisfies_twin_composer_protocol(self) -> None:
        from app.application.twin_update.protocols import TwinComposerProtocol

        composer: TwinComposerProtocol = TwinComposer()
        twin = _twin()
        successor = composer.compose(twin, (_output("knowledge", _new_knowledge()),))
        assert isinstance(successor, DigitalTwin)

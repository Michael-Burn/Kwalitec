"""Unit tests for the Knowledge Update Strategy."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, date, datetime, timedelta
from pathlib import Path
from typing import Any

import pytest

from app.domain.evidence import (
    EvidenceConfidenceLevel,
    EvidenceType,
    LearningEvidence,
)
from app.domain.twin import (
    KNOWLEDGE_EVIDENCE_TYPES,
    BaseUpdateStrategy,
    DigitalTwin,
    IdentityState,
    KnowledgeState,
    KnowledgeUpdateStrategy,
    TopicMasteryRecord,
    TwinUpdatePipeline,
    UpdateContext,
)

TWIN_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "twin"
STRATEGY_PATH = TWIN_ROOT / "strategies" / "knowledge_update_strategy.py"
FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "sqlalchemy",
        "wtforms",
    }
)


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "CS1-2026",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _twin(**overrides: Any) -> DigitalTwin:
    identity = overrides.pop("identity", None) or _identity()
    return DigitalTwin.create(identity, **overrides)


def _evidence(**overrides: Any) -> LearningEvidence:
    defaults: dict[str, Any] = {
        "evidence_id": "ev-1",
        "evidence_type": EvidenceType.QUESTION_ATTEMPT,
        "originating_event_id": "evt-1",
        "timestamp": datetime(2026, 7, 11, 8, 0, tzinfo=UTC),
        "topic_id": "CS1-A-T01",
        "curriculum_id": "CS1-2026",
        "payload": {"correct": True},
        "provenance": "quiz_engine",
        "confidence_level": EvidenceConfidenceLevel.MEDIUM,
        "metadata": {"stage": "test"},
    }
    defaults.update(overrides)
    return LearningEvidence.create(**defaults)


def _context(
    twin: DigitalTwin | None = None,
    evidence: LearningEvidence | list[LearningEvidence] | None = None,
) -> UpdateContext:
    return UpdateContext.create(
        twin if twin is not None else _twin(),
        evidence if evidence is not None else _evidence(),
    )


class TestStrategyContract:
    """Strategy registration and BaseUpdateStrategy contract."""

    def test_is_base_update_strategy(self) -> None:
        assert issubclass(KnowledgeUpdateStrategy, BaseUpdateStrategy)

    def test_name_is_stable(self) -> None:
        assert KnowledgeUpdateStrategy().name == "knowledge_update"

    def test_registers_with_pipeline(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        pipeline = TwinUpdatePipeline()
        pipeline.register(strategy)
        assert pipeline.strategies == (strategy,)

    def test_constructor_registration(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        pipeline = TwinUpdatePipeline([strategy])
        assert pipeline.strategies == (strategy,)


class TestApplicability:
    """supports() filters Knowledge-related, topic-scoped evidence."""

    def test_supports_knowledge_evidence_with_topic(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        assert strategy.supports(_context(evidence=_evidence())) is True

    def test_supports_each_knowledge_evidence_type(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        for evidence_type in sorted(KNOWLEDGE_EVIDENCE_TYPES, key=lambda t: t.value):
            context = _context(
                evidence=_evidence(
                    evidence_id=f"ev-{evidence_type.value}",
                    evidence_type=evidence_type,
                )
            )
            assert strategy.supports(context) is True, evidence_type

    def test_rejects_non_knowledge_evidence(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.REVISION_SESSION,
                evidence_id="ev-revision",
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_knowledge_evidence_without_topic(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        context = _context(evidence=_evidence(topic_id=None))
        assert strategy.supports(context) is False

    def test_rejects_blank_topic_id(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        context = _context(evidence=_evidence(topic_id="   "))
        assert strategy.supports(context) is False

    def test_supports_when_mixed_batch_has_applicable_item(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        context = _context(
            evidence=[
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                ),
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_CORRECT,
                ),
            ]
        )
        assert strategy.supports(context) is True

    def test_rejects_empty_evidence(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        context = UpdateContext.create(_twin(), ())
        assert strategy.supports(context) is False


class TestNewTopicCreation:
    """First evidence for a topic creates a TopicMasteryRecord."""

    def test_creates_topic_record_on_first_evidence(self) -> None:
        twin = _twin()
        strategy = KnowledgeUpdateStrategy()
        updated = strategy.apply(_context(twin=twin, evidence=_evidence()))
        assert len(updated.knowledge.topic_mastery) == 1
        record = updated.knowledge.topic_mastery[0]
        assert record.topic_id == "CS1-A-T01"
        assert record.evidence_ids == ("ev-1",)
        assert record.mastery_belief is None

    def test_creates_distinct_topics_from_batch(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        updated = strategy.apply(
            _context(
                evidence=[
                    _evidence(evidence_id="ev-a", topic_id="T-A"),
                    _evidence(evidence_id="ev-b", topic_id="T-B"),
                ]
            )
        )
        topic_ids = [record.topic_id for record in updated.knowledge.topic_mastery]
        assert topic_ids == ["T-A", "T-B"]


class TestExistingTopicUpdate:
    """Subsequent evidence updates an existing topic slot."""

    def test_updates_existing_topic_without_duplicating_slot(self) -> None:
        prior = TopicMasteryRecord.create("CS1-A-T01", evidence_ids=("ev-0",))
        twin = _twin(knowledge=KnowledgeState.create(topic_mastery=[prior]))
        strategy = KnowledgeUpdateStrategy()
        updated = strategy.apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert len(updated.knowledge.topic_mastery) == 1
        record = updated.knowledge.topic_mastery[0]
        assert record.topic_id == "CS1-A-T01"
        assert record.evidence_ids == ("ev-0", "ev-1")

    def test_preserves_existing_mastery_belief(self) -> None:
        prior = TopicMasteryRecord.create(
            "CS1-A-T01",
            mastery_belief=0.42,
            evidence_ids=("ev-0",),
        )
        twin = _twin(knowledge=KnowledgeState.create(topic_mastery=[prior]))
        updated = KnowledgeUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert updated.knowledge.topic_mastery[0].mastery_belief == 0.42

    def test_preserves_unrelated_topics(self) -> None:
        other = TopicMasteryRecord.create("OTHER", evidence_ids=("ev-x",))
        twin = _twin(knowledge=KnowledgeState.create(topic_mastery=[other]))
        updated = KnowledgeUpdateStrategy().apply(
            _context(
                twin=twin,
                evidence=_evidence(evidence_id="ev-1", topic_id="CS1-A-T01"),
            )
        )
        topic_ids = [record.topic_id for record in updated.knowledge.topic_mastery]
        assert topic_ids == ["OTHER", "CS1-A-T01"]
        assert updated.knowledge.topic_mastery[0].evidence_ids == ("ev-x",)


class TestEvidenceCountAndReferences:
    """Evidence count is len(evidence_ids); references are recorded."""

    def test_increments_evidence_count_via_evidence_ids(self) -> None:
        twin = _twin()
        strategy = KnowledgeUpdateStrategy()
        first = strategy.apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        second = strategy.apply(
            _context(
                twin=first,
                evidence=_evidence(evidence_id="ev-2", topic_id="CS1-A-T01"),
            )
        )
        record = second.knowledge.topic_mastery[0]
        assert len(record.evidence_ids) == 2
        assert record.evidence_ids == ("ev-1", "ev-2")

    def test_records_evidence_on_knowledge_state(self) -> None:
        updated = KnowledgeUpdateStrategy().apply(
            _context(evidence=_evidence(evidence_id="ev-99"))
        )
        assert updated.knowledge.evidence_ids == ("ev-99",)

    def test_dedupes_repeated_evidence_id(self) -> None:
        prior = TopicMasteryRecord.create("CS1-A-T01", evidence_ids=("ev-1",))
        twin = _twin(
            knowledge=KnowledgeState.create(
                topic_mastery=[prior],
                evidence_ids=("ev-1",),
            )
        )
        updated = KnowledgeUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert updated.knowledge.topic_mastery[0].evidence_ids == ("ev-1",)
        assert updated.knowledge.evidence_ids == ("ev-1",)

    def test_updates_last_updated_to_latest_timestamp(self) -> None:
        earlier = datetime(2026, 7, 10, 8, 0, tzinfo=UTC)
        later = earlier + timedelta(hours=5)
        updated = KnowledgeUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(evidence_id="ev-a", topic_id="T1", timestamp=later),
                    _evidence(evidence_id="ev-b", topic_id="T2", timestamp=earlier),
                ]
            )
        )
        assert updated.knowledge.last_updated == later

    def test_does_not_compute_mastery(self) -> None:
        updated = KnowledgeUpdateStrategy().apply(_context())
        assert updated.knowledge.topic_mastery[0].mastery_belief is None


class TestImmutability:
    """Original Twin and evidence remain unchanged."""

    def test_original_twin_unchanged(self) -> None:
        twin = _twin()
        original_knowledge = twin.knowledge
        KnowledgeUpdateStrategy().apply(_context(twin=twin))
        assert twin.knowledge is original_knowledge
        assert twin.knowledge.topic_mastery == ()
        assert twin.knowledge.evidence_ids == ()
        assert twin.knowledge.last_updated is None

    def test_returns_new_twin_instance(self) -> None:
        twin = _twin()
        updated = KnowledgeUpdateStrategy().apply(_context(twin=twin))
        assert updated is not twin
        assert updated.knowledge is not twin.knowledge

    def test_preserves_other_domain_states(self) -> None:
        twin = _twin()
        updated = KnowledgeUpdateStrategy().apply(_context(twin=twin))
        assert updated.identity is twin.identity
        assert updated.goals is twin.goals
        assert updated.memory is twin.memory
        assert updated.behaviour is twin.behaviour
        assert updated.performance is twin.performance
        assert updated.predictions is twin.predictions

    def test_twin_remains_frozen(self) -> None:
        twin = _twin()
        updated = KnowledgeUpdateStrategy().apply(_context(twin=twin))
        with pytest.raises(AttributeError):
            updated.knowledge = twin.knowledge  # type: ignore[misc]


class TestPipelineIntegration:
    """KnowledgeUpdateStrategy through TwinUpdatePipeline."""

    def test_pipeline_applies_knowledge_strategy(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([KnowledgeUpdateStrategy()])
        result = pipeline.update(twin, _evidence())
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is not twin
        assert result.applied_strategies == ("knowledge_update",)
        assert len(result.updated_twin.knowledge.topic_mastery) == 1
        assert twin.knowledge.topic_mastery == ()

    def test_pipeline_skips_when_not_applicable(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([KnowledgeUpdateStrategy()])
        result = pipeline.update(
            twin,
            _evidence(evidence_type=EvidenceType.SKIPPED_SESSION, topic_id=None),
        )
        assert result.updated_twin is twin
        assert result.applied_strategies == ()
        assert any("not applicable" in msg for msg in result.processing_messages)

    def test_pipeline_processes_batch_of_knowledge_evidence(self) -> None:
        pipeline = TwinUpdatePipeline([KnowledgeUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(evidence_id="ev-1", topic_id="T1"),
                _evidence(evidence_id="ev-2", topic_id="T1"),
                _evidence(evidence_id="ev-3", topic_id="T2"),
            ],
        )
        assert result.applied_strategies == ("knowledge_update",)
        topics = {
            record.topic_id: record
            for record in result.updated_twin.knowledge.topic_mastery
        }
        assert len(topics["T1"].evidence_ids) == 2
        assert len(topics["T2"].evidence_ids) == 1
        assert result.updated_twin.knowledge.evidence_ids == ("ev-1", "ev-2", "ev-3")

    def test_pipeline_ignores_non_knowledge_items_in_mixed_batch(self) -> None:
        pipeline = TwinUpdatePipeline([KnowledgeUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                    topic_id="T1",
                ),
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                ),
            ],
        )
        record = result.updated_twin.knowledge.topic_mastery[0]
        assert record.evidence_ids == ("ev-q",)
        assert result.updated_twin.knowledge.evidence_ids == ("ev-q",)


class TestFrameworkIndependence:
    """Knowledge strategy must remain framework-independent."""

    def test_strategy_source_has_no_framework_imports(self) -> None:
        violations: list[str] = []
        tree = ast.parse(
            STRATEGY_PATH.read_text(encoding="utf-8"),
            filename=str(STRATEGY_PATH),
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root = alias.name.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES:
                        loc = f"{STRATEGY_PATH}:{node.lineno}"
                        violations.append(f"{loc} import {alias.name}")
            elif isinstance(node, ast.ImportFrom) and node.module:
                root = node.module.split(".", 1)[0]
                if root in FORBIDDEN_ROOT_MODULES:
                    loc = f"{STRATEGY_PATH}:{node.lineno}"
                    violations.append(f"{loc} from {node.module}")
        assert violations == []

    def test_strategy_does_not_import_services_or_models(self) -> None:
        violations: list[str] = []
        forbidden_prefixes = (
            "app.services",
            "app.models",
            "app.auth",
            "app.dashboard",
        )
        tree = ast.parse(
            STRATEGY_PATH.read_text(encoding="utf-8"),
            filename=str(STRATEGY_PATH),
        )
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                if node.module.startswith(forbidden_prefixes):
                    loc = f"{STRATEGY_PATH}:{node.lineno}"
                    violations.append(f"{loc} from {node.module}")
            elif isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.startswith(forbidden_prefixes):
                        loc = f"{STRATEGY_PATH}:{node.lineno}"
                        violations.append(f"{loc} import {alias.name}")
        assert violations == []

    def test_importing_strategy_does_not_require_flask(self) -> None:
        module_name = "app.domain.twin.strategies.knowledge_update_strategy"
        assert module_name in sys.modules
        module = sys.modules[module_name]
        assert not any(
            dep in getattr(module, "__dict__", {})
            for dep in ("Flask", "request", "db", "SQLAlchemy")
        )

    def test_strategy_has_no_educational_scoring_api(self) -> None:
        strategy = KnowledgeUpdateStrategy()
        public_callables = {
            name
            for name in dir(strategy)
            if callable(getattr(strategy, name)) and not name.startswith("_")
        }
        forbidden = {
            "compute_mastery",
            "bayesian_update",
            "irt",
            "decay_memory",
            "predict",
            "recommend",
            "plan",
            "persist",
            "save",
        }
        assert forbidden.isdisjoint(public_callables)
        assert KNOWLEDGE_EVIDENCE_TYPES  # catalogue is exported for extension

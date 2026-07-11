"""Unit tests for the Memory Update Strategy."""

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
    MEMORY_EVIDENCE_TYPES,
    BaseUpdateStrategy,
    DigitalTwin,
    IdentityState,
    KnowledgeState,
    KnowledgeUpdateStrategy,
    MemoryState,
    MemoryUpdateStrategy,
    RetentionRecord,
    TopicMasteryRecord,
    TwinUpdatePipeline,
    UpdateContext,
)

TWIN_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "twin"
STRATEGY_PATH = TWIN_ROOT / "strategies" / "memory_update_strategy.py"
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
        "evidence_type": EvidenceType.REVISION_SESSION,
        "originating_event_id": "evt-1",
        "timestamp": datetime(2026, 7, 11, 8, 0, tzinfo=UTC),
        "topic_id": "CS1-A-T01",
        "curriculum_id": "CS1-2026",
        "payload": {"duration_minutes": 20},
        "provenance": "revision_engine",
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
        assert issubclass(MemoryUpdateStrategy, BaseUpdateStrategy)

    def test_name_is_stable(self) -> None:
        assert MemoryUpdateStrategy().name == "memory_update"

    def test_registers_with_pipeline(self) -> None:
        strategy = MemoryUpdateStrategy()
        pipeline = TwinUpdatePipeline()
        pipeline.register(strategy)
        assert pipeline.strategies == (strategy,)

    def test_constructor_registration(self) -> None:
        strategy = MemoryUpdateStrategy()
        pipeline = TwinUpdatePipeline([strategy])
        assert pipeline.strategies == (strategy,)


class TestApplicability:
    """supports() filters Memory-related, topic-scoped evidence."""

    def test_supports_memory_evidence_with_topic(self) -> None:
        strategy = MemoryUpdateStrategy()
        assert strategy.supports(_context(evidence=_evidence())) is True

    def test_supports_each_memory_evidence_type(self) -> None:
        strategy = MemoryUpdateStrategy()
        for evidence_type in sorted(MEMORY_EVIDENCE_TYPES, key=lambda t: t.value):
            context = _context(
                evidence=_evidence(
                    evidence_id=f"ev-{evidence_type.value}",
                    evidence_type=evidence_type,
                )
            )
            assert strategy.supports(context) is True, evidence_type

    def test_rejects_non_memory_evidence(self) -> None:
        strategy = MemoryUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.QUESTION_ATTEMPT,
                evidence_id="ev-question",
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_memory_evidence_without_topic(self) -> None:
        strategy = MemoryUpdateStrategy()
        context = _context(evidence=_evidence(topic_id=None))
        assert strategy.supports(context) is False

    def test_rejects_blank_topic_id(self) -> None:
        strategy = MemoryUpdateStrategy()
        context = _context(evidence=_evidence(topic_id="   "))
        assert strategy.supports(context) is False

    def test_supports_when_mixed_batch_has_applicable_item(self) -> None:
        strategy = MemoryUpdateStrategy()
        context = _context(
            evidence=[
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_CORRECT,
                ),
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                ),
            ]
        )
        assert strategy.supports(context) is True

    def test_rejects_empty_evidence(self) -> None:
        strategy = MemoryUpdateStrategy()
        context = UpdateContext.create(_twin(), ())
        assert strategy.supports(context) is False


class TestNewMemoryEntryCreation:
    """First evidence for a topic creates a RetentionRecord."""

    def test_creates_retention_record_on_first_evidence(self) -> None:
        twin = _twin()
        strategy = MemoryUpdateStrategy()
        ts = datetime(2026, 7, 11, 8, 0, tzinfo=UTC)
        updated = strategy.apply(
            _context(twin=twin, evidence=_evidence(timestamp=ts))
        )
        assert len(updated.memory.retention) == 1
        record = updated.memory.retention[0]
        assert record.topic_id == "CS1-A-T01"
        assert record.retention_belief is None
        assert record.last_reinforced == ts

    def test_creates_distinct_topics_from_batch(self) -> None:
        strategy = MemoryUpdateStrategy()
        updated = strategy.apply(
            _context(
                evidence=[
                    _evidence(evidence_id="ev-a", topic_id="T-A"),
                    _evidence(evidence_id="ev-b", topic_id="T-B"),
                ]
            )
        )
        topic_ids = [record.topic_id for record in updated.memory.retention]
        assert topic_ids == ["T-A", "T-B"]


class TestExistingMemoryUpdate:
    """Subsequent evidence updates an existing retention slot."""

    def test_updates_existing_topic_without_duplicating_slot(self) -> None:
        prior_ts = datetime(2026, 7, 1, 8, 0, tzinfo=UTC)
        prior = RetentionRecord.create(
            "CS1-A-T01",
            last_reinforced=prior_ts,
        )
        twin = _twin(memory=MemoryState.create(retention=[prior]))
        strategy = MemoryUpdateStrategy()
        later = prior_ts + timedelta(days=3)
        updated = strategy.apply(
            _context(
                twin=twin,
                evidence=_evidence(evidence_id="ev-1", timestamp=later),
            )
        )
        assert len(updated.memory.retention) == 1
        record = updated.memory.retention[0]
        assert record.topic_id == "CS1-A-T01"
        assert record.last_reinforced == later

    def test_preserves_existing_retention_belief(self) -> None:
        prior = RetentionRecord.create(
            "CS1-A-T01",
            retention_belief=0.55,
            last_reinforced=datetime(2026, 7, 1, 8, 0, tzinfo=UTC),
        )
        twin = _twin(memory=MemoryState.create(retention=[prior]))
        updated = MemoryUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert updated.memory.retention[0].retention_belief == 0.55

    def test_does_not_regress_last_reinforced_on_older_evidence(self) -> None:
        newer = datetime(2026, 7, 10, 8, 0, tzinfo=UTC)
        older = datetime(2026, 7, 5, 8, 0, tzinfo=UTC)
        prior = RetentionRecord.create(
            "CS1-A-T01",
            last_reinforced=newer,
        )
        twin = _twin(memory=MemoryState.create(retention=[prior]))
        updated = MemoryUpdateStrategy().apply(
            _context(
                twin=twin,
                evidence=_evidence(evidence_id="ev-old", timestamp=older),
            )
        )
        assert updated.memory.retention[0].last_reinforced == newer

    def test_preserves_unrelated_topics(self) -> None:
        other = RetentionRecord.create(
            "OTHER",
            last_reinforced=datetime(2026, 6, 1, tzinfo=UTC),
        )
        twin = _twin(memory=MemoryState.create(retention=[other]))
        updated = MemoryUpdateStrategy().apply(
            _context(
                twin=twin,
                evidence=_evidence(evidence_id="ev-1", topic_id="CS1-A-T01"),
            )
        )
        topic_ids = [record.topic_id for record in updated.memory.retention]
        assert topic_ids == ["OTHER", "CS1-A-T01"]
        assert updated.memory.retention[0].topic_id == "OTHER"


class TestEvidenceReferenceTracking:
    """Revision evidence references are recorded on MemoryState."""

    def test_records_evidence_on_memory_state(self) -> None:
        updated = MemoryUpdateStrategy().apply(
            _context(evidence=_evidence(evidence_id="ev-99"))
        )
        assert updated.memory.revision_ids == ("ev-99",)

    def test_appends_multiple_evidence_references(self) -> None:
        twin = _twin()
        strategy = MemoryUpdateStrategy()
        first = strategy.apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        second = strategy.apply(
            _context(
                twin=first,
                evidence=_evidence(evidence_id="ev-2", topic_id="CS1-A-T01"),
            )
        )
        assert second.memory.revision_ids == ("ev-1", "ev-2")

    def test_dedupes_repeated_evidence_id(self) -> None:
        prior = RetentionRecord.create("CS1-A-T01")
        twin = _twin(
            memory=MemoryState.create(
                retention=[prior],
                revision_ids=("ev-1",),
            )
        )
        updated = MemoryUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert updated.memory.revision_ids == ("ev-1",)

    def test_updates_last_updated_to_latest_timestamp(self) -> None:
        earlier = datetime(2026, 7, 10, 8, 0, tzinfo=UTC)
        later = earlier + timedelta(hours=5)
        updated = MemoryUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(evidence_id="ev-a", topic_id="T1", timestamp=later),
                    _evidence(evidence_id="ev-b", topic_id="T2", timestamp=earlier),
                ]
            )
        )
        assert updated.memory.last_updated == later

    def test_does_not_compute_retention(self) -> None:
        updated = MemoryUpdateStrategy().apply(_context())
        assert updated.memory.retention[0].retention_belief is None


class TestImmutability:
    """Original Twin and evidence remain unchanged."""

    def test_original_twin_unchanged(self) -> None:
        twin = _twin()
        original_memory = twin.memory
        MemoryUpdateStrategy().apply(_context(twin=twin))
        assert twin.memory is original_memory
        assert twin.memory.retention == ()
        assert twin.memory.revision_ids == ()
        assert twin.memory.last_updated is None

    def test_returns_new_twin_instance(self) -> None:
        twin = _twin()
        updated = MemoryUpdateStrategy().apply(_context(twin=twin))
        assert updated is not twin
        assert updated.memory is not twin.memory

    def test_preserves_other_domain_states(self) -> None:
        twin = _twin()
        updated = MemoryUpdateStrategy().apply(_context(twin=twin))
        assert updated.identity is twin.identity
        assert updated.goals is twin.goals
        assert updated.knowledge is twin.knowledge
        assert updated.behaviour is twin.behaviour
        assert updated.performance is twin.performance
        assert updated.predictions is twin.predictions

    def test_twin_remains_frozen(self) -> None:
        twin = _twin()
        updated = MemoryUpdateStrategy().apply(_context(twin=twin))
        with pytest.raises(AttributeError):
            updated.memory = twin.memory  # type: ignore[misc]


class TestPipelineIntegration:
    """MemoryUpdateStrategy through TwinUpdatePipeline."""

    def test_pipeline_applies_memory_strategy(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([MemoryUpdateStrategy()])
        result = pipeline.update(twin, _evidence())
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is not twin
        assert result.applied_strategies == ("memory_update",)
        assert len(result.updated_twin.memory.retention) == 1
        assert twin.memory.retention == ()

    def test_pipeline_skips_when_not_applicable(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([MemoryUpdateStrategy()])
        result = pipeline.update(
            twin,
            _evidence(evidence_type=EvidenceType.SKIPPED_SESSION, topic_id=None),
        )
        assert result.updated_twin is twin
        assert result.applied_strategies == ()
        assert any("not applicable" in msg for msg in result.processing_messages)

    def test_pipeline_processes_batch_of_memory_evidence(self) -> None:
        pipeline = TwinUpdatePipeline([MemoryUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(evidence_id="ev-1", topic_id="T1"),
                _evidence(
                    evidence_id="ev-2",
                    topic_id="T1",
                    evidence_type=EvidenceType.FLASHCARD_REVIEW,
                ),
                _evidence(evidence_id="ev-3", topic_id="T2"),
            ],
        )
        assert result.applied_strategies == ("memory_update",)
        topics = {
            record.topic_id: record for record in result.updated_twin.memory.retention
        }
        assert set(topics) == {"T1", "T2"}
        assert result.updated_twin.memory.revision_ids == ("ev-1", "ev-2", "ev-3")

    def test_pipeline_ignores_non_memory_items_in_mixed_batch(self) -> None:
        pipeline = TwinUpdatePipeline([MemoryUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                ),
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                    topic_id="T1",
                ),
            ],
        )
        assert len(result.updated_twin.memory.retention) == 1
        assert result.updated_twin.memory.revision_ids == ("ev-rev",)

    def test_pipeline_coordinates_knowledge_and_memory_independently(self) -> None:
        pipeline = TwinUpdatePipeline(
            [KnowledgeUpdateStrategy(), MemoryUpdateStrategy()]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                ),
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                    topic_id="T1",
                ),
            ],
        )
        assert result.applied_strategies == ("knowledge_update", "memory_update")
        assert result.updated_twin.knowledge.evidence_ids == ("ev-q",)
        assert result.updated_twin.memory.revision_ids == ("ev-rev",)
        assert result.updated_twin.knowledge.topic_mastery[0].topic_id == "T1"
        assert result.updated_twin.memory.retention[0].topic_id == "T1"
        # Domains evolved independently — Knowledge does not own revision ids.
        assert isinstance(result.updated_twin.knowledge, KnowledgeState)
        assert isinstance(result.updated_twin.memory, MemoryState)
        assert result.updated_twin.knowledge.topic_mastery[0].evidence_ids == (
            "ev-q",
        )

    def test_memory_strategy_does_not_mutate_knowledge(self) -> None:
        prior = TopicMasteryRecord.create("T1", evidence_ids=("ev-prior",))
        twin = _twin(knowledge=KnowledgeState.create(topic_mastery=[prior]))
        updated = MemoryUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(topic_id="T1"))
        )
        assert updated.knowledge is twin.knowledge
        assert updated.knowledge.topic_mastery[0].evidence_ids == ("ev-prior",)


class TestFrameworkIndependence:
    """Memory strategy must remain framework-independent."""

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
        module_name = "app.domain.twin.strategies.memory_update_strategy"
        assert module_name in sys.modules
        module = sys.modules[module_name]
        assert not any(
            dep in getattr(module, "__dict__", {})
            for dep in ("Flask", "request", "db", "SQLAlchemy")
        )

    def test_strategy_has_no_educational_scoring_api(self) -> None:
        strategy = MemoryUpdateStrategy()
        public_callables = {
            name
            for name in dir(strategy)
            if callable(getattr(strategy, name)) and not name.startswith("_")
        }
        forbidden = {
            "compute_retention",
            "forgetting_curve",
            "spaced_repetition",
            "fsrs",
            "sm2",
            "leitner",
            "decay_memory",
            "schedule_revision",
            "predict",
            "recommend",
            "plan",
            "persist",
            "save",
        }
        assert forbidden.isdisjoint(public_callables)
        assert MEMORY_EVIDENCE_TYPES  # catalogue is exported for extension

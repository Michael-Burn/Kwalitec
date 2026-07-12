"""Unit tests for the Behaviour Update Strategy."""

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
    BEHAVIOUR_EVIDENCE_TYPES,
    BaseUpdateStrategy,
    BehaviourState,
    BehaviourUpdateStrategy,
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
STRATEGY_PATH = TWIN_ROOT / "strategies" / "behaviour_update_strategy.py"
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
        "evidence_type": EvidenceType.MISSION_COMPLETED,
        "originating_event_id": "evt-1",
        "timestamp": datetime(2026, 7, 11, 8, 0, tzinfo=UTC),
        "topic_id": None,
        "curriculum_id": "CS1-2026",
        "payload": {"mission_id": "mission-1"},
        "provenance": "mission_engine",
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
        assert issubclass(BehaviourUpdateStrategy, BaseUpdateStrategy)

    def test_name_is_stable(self) -> None:
        assert BehaviourUpdateStrategy().name == "behaviour_update"

    def test_registers_with_pipeline(self) -> None:
        strategy = BehaviourUpdateStrategy()
        pipeline = TwinUpdatePipeline()
        pipeline.register(strategy)
        assert pipeline.strategies == (strategy,)

    def test_constructor_registration(self) -> None:
        strategy = BehaviourUpdateStrategy()
        pipeline = TwinUpdatePipeline([strategy])
        assert pipeline.strategies == (strategy,)


class TestApplicability:
    """supports() filters Behaviour-primary evidence without requiring topic_id."""

    def test_supports_behaviour_evidence(self) -> None:
        strategy = BehaviourUpdateStrategy()
        assert strategy.supports(_context(evidence=_evidence())) is True

    def test_supports_each_behaviour_evidence_type(self) -> None:
        strategy = BehaviourUpdateStrategy()
        for evidence_type in sorted(BEHAVIOUR_EVIDENCE_TYPES, key=lambda t: t.value):
            context = _context(
                evidence=_evidence(
                    evidence_id=f"ev-{evidence_type.value}",
                    evidence_type=evidence_type,
                    payload={},
                )
            )
            assert strategy.supports(context) is True, evidence_type

    def test_supports_without_topic_id(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(evidence=_evidence(topic_id=None))
        assert strategy.supports(context) is True

    def test_supports_with_blank_topic_id(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(evidence=_evidence(topic_id="   "))
        assert strategy.supports(context) is True

    def test_rejects_non_behaviour_evidence(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.QUESTION_ATTEMPT,
                evidence_id="ev-question",
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_revision_only_evidence(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.REVISION_SESSION,
                evidence_id="ev-rev",
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_post_exam_outcome(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.POST_EXAM_OUTCOME,
                evidence_id="ev-post",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_secondary_recommendation_decision(self) -> None:
        """Choice A: secondary types are not primary Behaviour ownership."""
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.RECOMMENDATION_DECISION,
                evidence_id="ev-rec",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_supports_when_mixed_batch_has_applicable_item(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=[
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_CORRECT,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                ),
            ]
        )
        assert strategy.supports(context) is True

    def test_rejects_empty_evidence(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = UpdateContext.create(_twin(), ())
        assert strategy.supports(context) is False


class TestStructuralApply:
    """Structural lineage, timestamps, and metric preservation."""

    def test_appends_session_lineage_from_payload_mission_id(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(evidence=_evidence(payload={"mission_id": "mission-9"}))
        )
        assert updated.behaviour.session_history_ids == ("mission-9",)

    def test_prefers_session_id_over_mission_id(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "session_id": "sess-1",
                        "mission_id": "mission-9",
                    }
                )
            )
        )
        assert updated.behaviour.session_history_ids == ("sess-1",)

    def test_falls_back_to_originating_event_id(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    originating_event_id="evt-77",
                    payload={},
                )
            )
        )
        assert updated.behaviour.session_history_ids == ("evt-77",)

    def test_falls_back_to_evidence_id(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    evidence_id="ev-fallback",
                    originating_event_id=None,
                    payload={},
                )
            )
        )
        assert updated.behaviour.session_history_ids == ("ev-fallback",)

    def test_appends_supplied_pattern_ids_only(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "mission_id": "mission-1",
                        "study_pattern_id": "pat-friday",
                    },
                    metadata={"study_pattern_ids": ["pat-evening"]},
                )
            )
        )
        assert updated.behaviour.study_pattern_ids == (
            "pat-friday",
            "pat-evening",
        )

    def test_does_not_invent_pattern_ids(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(evidence=_evidence(payload={"mission_id": "mission-1"}))
        )
        assert updated.behaviour.study_pattern_ids == ()

    def test_records_evidence_ids(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(evidence=_evidence(evidence_id="ev-99"))
        )
        assert updated.behaviour.evidence_ids == ("ev-99",)

    def test_preserves_consistency_metrics(self) -> None:
        metrics = {"adherence_ratio": 0.42, "custom_slot": "kept"}
        twin = _twin(
            behaviour=BehaviourState.create(consistency_metrics=metrics)
        )
        updated = BehaviourUpdateStrategy().apply(_context(twin=twin))
        assert updated.behaviour.consistency_metrics == metrics
        assert updated.behaviour.consistency_metrics is not metrics

    def test_does_not_invent_consistency_metrics(self) -> None:
        updated = BehaviourUpdateStrategy().apply(_context())
        assert updated.behaviour.consistency_metrics == {}

    def test_updates_last_updated_to_latest_timestamp(self) -> None:
        earlier = datetime(2026, 7, 10, 8, 0, tzinfo=UTC)
        later = earlier + timedelta(hours=5)
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(
                        evidence_id="ev-a",
                        timestamp=later,
                        payload={"session_id": "s-a"},
                    ),
                    _evidence(
                        evidence_id="ev-b",
                        timestamp=earlier,
                        payload={"session_id": "s-b"},
                    ),
                ]
            )
        )
        assert updated.behaviour.last_updated == later

    def test_applies_without_topic_id(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(evidence=_evidence(topic_id=None))
        )
        assert updated.behaviour.evidence_ids == ("ev-1",)
        assert updated.behaviour.session_history_ids == ("mission-1",)


class TestIdempotenceAndDeterminism:
    """Replay and identical inputs must not invent duplicate lineage."""

    def test_dedupes_repeated_evidence_id(self) -> None:
        twin = _twin(
            behaviour=BehaviourState.create(
                session_history_ids=("mission-1",),
                evidence_ids=("ev-1",),
            )
        )
        updated = BehaviourUpdateStrategy().apply(
            _context(twin=twin, evidence=_evidence(evidence_id="ev-1"))
        )
        assert updated.behaviour.evidence_ids == ("ev-1",)
        assert updated.behaviour.session_history_ids == ("mission-1",)

    def test_dedupes_session_id_across_distinct_evidence(self) -> None:
        updated = BehaviourUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(
                        evidence_id="ev-1",
                        payload={"session_id": "sess-shared"},
                    ),
                    _evidence(
                        evidence_id="ev-2",
                        payload={"session_id": "sess-shared"},
                    ),
                ]
            )
        )
        assert updated.behaviour.session_history_ids == ("sess-shared",)
        assert updated.behaviour.evidence_ids == ("ev-1", "ev-2")

    def test_same_inputs_yield_same_structural_outcome(self) -> None:
        twin = _twin()
        evidence = [
            _evidence(evidence_id="ev-a", payload={"session_id": "s-a"}),
            _evidence(evidence_id="ev-b", payload={"session_id": "s-b"}),
        ]
        first = BehaviourUpdateStrategy().apply(
            _context(twin=twin, evidence=evidence)
        )
        second = BehaviourUpdateStrategy().apply(
            _context(twin=twin, evidence=evidence)
        )
        assert first.behaviour.session_history_ids == (
            second.behaviour.session_history_ids
        )
        assert first.behaviour.evidence_ids == second.behaviour.evidence_ids
        assert first.behaviour.last_updated == second.behaviour.last_updated
        assert (
            first.behaviour.consistency_metrics
            == second.behaviour.consistency_metrics
        )


class TestImmutability:
    """Original Twin and evidence remain unchanged."""

    def test_original_twin_unchanged(self) -> None:
        twin = _twin()
        original_behaviour = twin.behaviour
        BehaviourUpdateStrategy().apply(_context(twin=twin))
        assert twin.behaviour is original_behaviour
        assert twin.behaviour.session_history_ids == ()
        assert twin.behaviour.evidence_ids == ()
        assert twin.behaviour.last_updated is None

    def test_returns_new_twin_instance(self) -> None:
        twin = _twin()
        updated = BehaviourUpdateStrategy().apply(_context(twin=twin))
        assert updated is not twin
        assert updated.behaviour is not twin.behaviour

    def test_preserves_other_domain_states(self) -> None:
        twin = _twin()
        updated = BehaviourUpdateStrategy().apply(_context(twin=twin))
        assert updated.identity is twin.identity
        assert updated.goals is twin.goals
        assert updated.knowledge is twin.knowledge
        assert updated.memory is twin.memory
        assert updated.performance is twin.performance
        assert updated.predictions is twin.predictions

    def test_twin_remains_frozen(self) -> None:
        twin = _twin()
        updated = BehaviourUpdateStrategy().apply(_context(twin=twin))
        with pytest.raises(AttributeError):
            updated.behaviour = twin.behaviour  # type: ignore[misc]


class TestCrossDomainIsolation:
    """Behaviour must not steal Knowledge/Memory ownership or mutate them."""

    def test_mission_only_leaves_knowledge_and_memory_unchanged(self) -> None:
        prior_knowledge = TopicMasteryRecord.create(
            "T1", evidence_ids=("ev-prior-k",)
        )
        prior_memory = RetentionRecord.create(
            "T1",
            last_reinforced=datetime(2026, 6, 1, tzinfo=UTC),
        )
        twin = _twin(
            knowledge=KnowledgeState.create(topic_mastery=[prior_knowledge]),
            memory=MemoryState.create(retention=[prior_memory]),
        )
        updated = BehaviourUpdateStrategy().apply(_context(twin=twin))
        assert updated.knowledge is twin.knowledge
        assert updated.memory is twin.memory
        assert updated.knowledge.topic_mastery[0].evidence_ids == ("ev-prior-k",)
        assert updated.memory.retention[0].last_reinforced == datetime(
            2026, 6, 1, tzinfo=UTC
        )

    def test_quiz_only_does_not_run_behaviour(self) -> None:
        strategy = BehaviourUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.QUESTION_ATTEMPT,
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False


class TestPipelineIntegration:
    """BehaviourUpdateStrategy through TwinUpdatePipeline."""

    def test_pipeline_applies_behaviour_strategy(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([BehaviourUpdateStrategy()])
        result = pipeline.update(twin, _evidence())
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is not twin
        assert result.applied_strategies == ("behaviour_update",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-1",)
        assert twin.behaviour.evidence_ids == ()

    def test_pipeline_skips_when_not_applicable(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([BehaviourUpdateStrategy()])
        result = pipeline.update(
            twin,
            _evidence(
                evidence_type=EvidenceType.REVISION_SESSION,
                topic_id="T1",
                payload={},
            ),
        )
        assert result.updated_twin is twin
        assert result.applied_strategies == ()
        assert any("not applicable" in msg for msg in result.processing_messages)

    def test_pipeline_processes_batch_of_behaviour_evidence(self) -> None:
        pipeline = TwinUpdatePipeline([BehaviourUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-1",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    payload={"mission_id": "m-1"},
                ),
                _evidence(
                    evidence_id="ev-2",
                    evidence_type=EvidenceType.SKIPPED_SESSION,
                    payload={"session_id": "s-2"},
                ),
                _evidence(
                    evidence_id="ev-3",
                    evidence_type=EvidenceType.TIME_ON_TASK,
                    payload={"session_id": "s-3"},
                ),
            ],
        )
        assert result.applied_strategies == ("behaviour_update",)
        assert result.updated_twin.behaviour.session_history_ids == (
            "m-1",
            "s-2",
            "s-3",
        )
        assert result.updated_twin.behaviour.evidence_ids == (
            "ev-1",
            "ev-2",
            "ev-3",
        )

    def test_pipeline_ignores_non_behaviour_items_in_mixed_batch(self) -> None:
        pipeline = TwinUpdatePipeline([BehaviourUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    payload={"mission_id": "m-1"},
                ),
            ],
        )
        assert result.updated_twin.behaviour.evidence_ids == ("ev-mission",)
        assert result.updated_twin.behaviour.session_history_ids == ("m-1",)

    def test_pipeline_registration_order_knowledge_memory_behaviour(self) -> None:
        pipeline = TwinUpdatePipeline(
            [
                KnowledgeUpdateStrategy(),
                MemoryUpdateStrategy(),
                BehaviourUpdateStrategy(),
            ]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-rev",
                    evidence_type=EvidenceType.REVISION_SESSION,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    payload={"mission_id": "m-1"},
                ),
            ],
        )
        assert result.applied_strategies == (
            "knowledge_update",
            "memory_update",
            "behaviour_update",
        )
        assert result.updated_twin.knowledge.evidence_ids == ("ev-q",)
        assert result.updated_twin.memory.revision_ids == ("ev-rev",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-mission",)

    def test_pipeline_mission_plus_quiz_applies_knowledge_then_behaviour(
        self,
    ) -> None:
        pipeline = TwinUpdatePipeline(
            [KnowledgeUpdateStrategy(), BehaviourUpdateStrategy()]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-q",
                    evidence_type=EvidenceType.QUESTION_ATTEMPT,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    payload={"mission_id": "m-1"},
                ),
            ],
        )
        assert result.applied_strategies == (
            "knowledge_update",
            "behaviour_update",
        )
        assert result.updated_twin.knowledge.evidence_ids == ("ev-q",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-mission",)
        # Mission must not overwrite quiz-driven Knowledge.
        assert result.updated_twin.knowledge.topic_mastery[0].evidence_ids == (
            "ev-q",
        )

    def test_pipeline_flashcard_plus_skip_applies_memory_and_behaviour(
        self,
    ) -> None:
        pipeline = TwinUpdatePipeline(
            [MemoryUpdateStrategy(), BehaviourUpdateStrategy()]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-flash",
                    evidence_type=EvidenceType.FLASHCARD_REVIEW,
                    topic_id="T1",
                    payload={},
                ),
                _evidence(
                    evidence_id="ev-skip",
                    evidence_type=EvidenceType.SKIPPED_SESSION,
                    payload={"session_id": "s-skip"},
                ),
            ],
        )
        assert result.applied_strategies == ("memory_update", "behaviour_update")
        assert result.updated_twin.memory.revision_ids == ("ev-flash",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-skip",)


class TestFrameworkIndependence:
    """Behaviour strategy must remain framework-independent."""

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
        module_name = "app.domain.twin.strategies.behaviour_update_strategy"
        assert module_name in sys.modules
        module = sys.modules[module_name]
        assert not any(
            dep in getattr(module, "__dict__", {})
            for dep in ("Flask", "request", "db", "SQLAlchemy")
        )

    def test_strategy_has_no_educational_scoring_api(self) -> None:
        strategy = BehaviourUpdateStrategy()
        public_callables = {
            name
            for name in dir(strategy)
            if callable(getattr(strategy, name)) and not name.startswith("_")
        }
        forbidden = {
            "compute_consistency",
            "adherence_ratio",
            "burnout_risk",
            "learning_velocity",
            "streak",
            "predict",
            "recommend",
            "plan",
            "persist",
            "save",
            "compute_mastery",
            "compute_retention",
        }
        assert forbidden.isdisjoint(public_callables)
        assert BEHAVIOUR_EVIDENCE_TYPES  # catalogue is exported for extension

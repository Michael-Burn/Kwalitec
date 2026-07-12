"""Unit tests for the Performance Update Strategy."""

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
    PERFORMANCE_EVIDENCE_TYPES,
    BaseUpdateStrategy,
    BehaviourState,
    BehaviourUpdateStrategy,
    DigitalTwin,
    IdentityState,
    KnowledgeState,
    KnowledgeUpdateStrategy,
    MemoryState,
    MemoryUpdateStrategy,
    PerformanceState,
    PerformanceSummary,
    PerformanceUpdateStrategy,
    RetentionRecord,
    TopicMasteryRecord,
    TwinUpdatePipeline,
    UpdateContext,
)

TWIN_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "twin"
STRATEGY_PATH = TWIN_ROOT / "strategies" / "performance_update_strategy.py"
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
        "evidence_type": EvidenceType.QUIZ_COMPLETED,
        "originating_event_id": "evt-1",
        "timestamp": datetime(2026, 7, 11, 8, 0, tzinfo=UTC),
        "topic_id": "CS1-A-T01",
        "curriculum_id": "CS1-2026",
        "payload": {"assessment_id": "quiz-1"},
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
        assert issubclass(PerformanceUpdateStrategy, BaseUpdateStrategy)

    def test_name_is_stable(self) -> None:
        assert PerformanceUpdateStrategy().name == "performance_update"

    def test_registers_with_pipeline(self) -> None:
        strategy = PerformanceUpdateStrategy()
        pipeline = TwinUpdatePipeline()
        pipeline.register(strategy)
        assert pipeline.strategies == (strategy,)

    def test_constructor_registration(self) -> None:
        strategy = PerformanceUpdateStrategy()
        pipeline = TwinUpdatePipeline([strategy])
        assert pipeline.strategies == (strategy,)


class TestApplicability:
    """supports() filters Performance-primary evidence without requiring topic_id."""

    def test_supports_performance_evidence(self) -> None:
        strategy = PerformanceUpdateStrategy()
        assert strategy.supports(_context(evidence=_evidence())) is True

    def test_supports_each_performance_evidence_type(self) -> None:
        strategy = PerformanceUpdateStrategy()
        for evidence_type in sorted(PERFORMANCE_EVIDENCE_TYPES, key=lambda t: t.value):
            context = _context(
                evidence=_evidence(
                    evidence_id=f"ev-{evidence_type.value}",
                    evidence_type=evidence_type,
                    payload={"assessment_id": f"a-{evidence_type.value}"},
                )
            )
            assert strategy.supports(context) is True, evidence_type

    def test_supports_without_topic_id(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(evidence=_evidence(topic_id=None))
        assert strategy.supports(context) is True

    def test_supports_post_exam_without_topic_id(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.POST_EXAM_OUTCOME,
                topic_id=None,
                payload={"assessment_id": "sitting-2026-09"},
            )
        )
        assert strategy.supports(context) is True

    def test_supports_with_blank_topic_id(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(evidence=_evidence(topic_id="   "))
        assert strategy.supports(context) is True

    def test_rejects_question_attempt_choice_a(self) -> None:
        """Choice A: question attempts remain Knowledge-primary only."""
        strategy = PerformanceUpdateStrategy()
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
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.REVISION_SESSION,
                evidence_id="ev-rev",
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_mission_only_evidence(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.MISSION_COMPLETED,
                evidence_id="ev-mission",
                topic_id=None,
                payload={"mission_id": "m-1"},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_confidence_rating(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.CONFIDENCE_RATING,
                evidence_id="ev-conf",
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_rejects_recommendation_decision(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.RECOMMENDATION_DECISION,
                evidence_id="ev-rec",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_supports_when_mixed_batch_has_applicable_item(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=[
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    topic_id=None,
                    payload={"mission_id": "m-1"},
                ),
                _evidence(
                    evidence_id="ev-quiz",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    payload={"assessment_id": "quiz-9"},
                ),
            ]
        )
        assert strategy.supports(context) is True

    def test_rejects_empty_evidence(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = UpdateContext.create(_twin(), ())
        assert strategy.supports(context) is False


class TestStructuralApply:
    """Structural lineage, scoped summaries, timestamps, and fact preservation."""

    def test_appends_assessment_lineage_from_payload(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(evidence=_evidence(payload={"assessment_id": "quiz-9"}))
        )
        assert updated.performance.assessment_ids == ("quiz-9",)

    def test_prefers_assessment_id_over_quiz_id(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "assessment_id": "assess-1",
                        "quiz_id": "quiz-9",
                    }
                )
            )
        )
        assert updated.performance.assessment_ids == ("assess-1",)

    def test_falls_back_to_evidence_id_for_assessment_lineage(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    evidence_id="ev-fallback",
                    payload={},
                    metadata={},
                )
            )
        )
        assert updated.performance.assessment_ids == ("ev-fallback",)

    def test_creates_topic_scoped_summary_from_topic_id(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id="CS1-A-T01",
                    payload={},
                    metadata={},
                    originating_event_id=None,
                )
            )
        )
        assert len(updated.performance.performance_summaries) == 1
        assert updated.performance.performance_summaries[0].scope_id == "CS1-A-T01"

    def test_prefers_explicit_scope_id_over_topic_id(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id="CS1-A-T01",
                    payload={"scope_id": "mock-instance-7"},
                )
            )
        )
        assert updated.performance.performance_summaries[0].scope_id == (
            "mock-instance-7"
        )

    def test_assessment_instance_scope_without_topic(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id=None,
                    payload={"assessment_id": "mock-42"},
                    originating_event_id=None,
                )
            )
        )
        assert updated.performance.performance_summaries[0].scope_id == "mock-42"
        assert updated.performance.assessment_ids == ("mock-42",)

    def test_falls_back_to_originating_event_id_for_scope(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id=None,
                    originating_event_id="evt-77",
                    payload={},
                    metadata={},
                )
            )
        )
        assert updated.performance.performance_summaries[0].scope_id == "evt-77"

    def test_weak_lineage_without_usable_scope(self) -> None:
        """No fabricated scope when topic/instance/originating ids are absent."""
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    evidence_id="ev-weak",
                    topic_id=None,
                    originating_event_id=None,
                    payload={},
                    metadata={},
                )
            )
        )
        assert updated.performance.assessment_ids == ("ev-weak",)
        assert updated.performance.evidence_ids == ("ev-weak",)
        assert updated.performance.performance_summaries == ()

    def test_does_not_fabricate_scope_from_free_text(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id=None,
                    originating_event_id=None,
                    payload={"notes": "practice on compound interest"},
                    metadata={},
                )
            )
        )
        assert updated.performance.performance_summaries == ()

    def test_records_evidence_ids(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(evidence=_evidence(evidence_id="ev-99"))
        )
        assert updated.performance.evidence_ids == ("ev-99",)

    def test_merges_supplied_summary_facts(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "assessment_id": "quiz-1",
                        "summary": {"items_attempted": 20, "source": "engine"},
                    }
                )
            )
        )
        assert updated.performance.performance_summaries[0].summary == {
            "items_attempted": 20,
            "source": "engine",
        }

    def test_preserves_unknown_summary_keys_on_merge(self) -> None:
        prior = PerformanceSummary.create(
            "quiz-1",
            summary={"custom_slot": "kept", "items_attempted": 10},
        )
        twin = _twin(
            performance=PerformanceState.create(
                assessment_ids=["quiz-1"],
                performance_summaries=[prior],
            )
        )
        updated = PerformanceUpdateStrategy().apply(
            _context(
                twin=twin,
                evidence=_evidence(
                    evidence_id="ev-2",
                    payload={
                        "assessment_id": "quiz-1",
                        "summary": {"items_attempted": 20},
                    },
                ),
            )
        )
        assert len(updated.performance.performance_summaries) == 1
        assert updated.performance.performance_summaries[0].summary == {
            "custom_slot": "kept",
            "items_attempted": 20,
        }

    def test_stores_condition_tag_when_supplied(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "assessment_id": "quiz-1",
                        "condition": "formative",
                    }
                )
            )
        )
        assert updated.performance.performance_summaries[0].summary["condition"] == (
            "formative"
        )

    def test_does_not_invent_summary_facts(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(evidence=_evidence(payload={"assessment_id": "quiz-1"}))
        )
        assert updated.performance.performance_summaries[0].summary == {}

    def test_updates_last_updated_to_latest_timestamp(self) -> None:
        earlier = datetime(2026, 7, 10, 8, 0, tzinfo=UTC)
        later = earlier + timedelta(hours=5)
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(
                        evidence_id="ev-a",
                        timestamp=later,
                        payload={"assessment_id": "a-a"},
                    ),
                    _evidence(
                        evidence_id="ev-b",
                        timestamp=earlier,
                        payload={"assessment_id": "a-b"},
                    ),
                ]
            )
        )
        assert updated.performance.last_updated == later

    def test_applies_without_topic_id(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    topic_id=None,
                    payload={"assessment_id": "mock-1"},
                )
            )
        )
        assert updated.performance.evidence_ids == ("ev-1",)
        assert updated.performance.assessment_ids == ("mock-1",)


class TestIdempotenceAndDeterminism:
    """Replay and identical inputs must not invent duplicate lineage."""

    def test_dedupes_repeated_evidence_id(self) -> None:
        twin = _twin(
            performance=PerformanceState.create(
                assessment_ids=("quiz-1",),
                evidence_ids=("ev-1",),
            )
        )
        updated = PerformanceUpdateStrategy().apply(
            _context(
                twin=twin,
                evidence=_evidence(
                    evidence_id="ev-1",
                    payload={"assessment_id": "quiz-1"},
                ),
            )
        )
        assert updated.performance.evidence_ids == ("ev-1",)
        assert updated.performance.assessment_ids == ("quiz-1",)

    def test_dedupes_assessment_id_across_distinct_evidence(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(
                        evidence_id="ev-1",
                        payload={"assessment_id": "quiz-shared"},
                    ),
                    _evidence(
                        evidence_id="ev-2",
                        payload={"assessment_id": "quiz-shared"},
                    ),
                ]
            )
        )
        assert updated.performance.assessment_ids == ("quiz-shared",)
        assert updated.performance.evidence_ids == ("ev-1", "ev-2")
        assert len(updated.performance.performance_summaries) == 1

    def test_same_inputs_yield_same_structural_outcome(self) -> None:
        twin = _twin()
        evidence = [
            _evidence(evidence_id="ev-a", payload={"assessment_id": "a-a"}),
            _evidence(evidence_id="ev-b", payload={"assessment_id": "a-b"}),
        ]
        first = PerformanceUpdateStrategy().apply(
            _context(twin=twin, evidence=evidence)
        )
        second = PerformanceUpdateStrategy().apply(
            _context(twin=twin, evidence=evidence)
        )
        assert first.performance.assessment_ids == (
            second.performance.assessment_ids
        )
        assert first.performance.evidence_ids == second.performance.evidence_ids
        assert first.performance.last_updated == second.performance.last_updated
        assert [
            (s.scope_id, s.summary)
            for s in first.performance.performance_summaries
        ] == [
            (s.scope_id, s.summary)
            for s in second.performance.performance_summaries
        ]


class TestImmutability:
    """Original Twin and evidence remain unchanged."""

    def test_original_twin_unchanged(self) -> None:
        twin = _twin()
        original_performance = twin.performance
        PerformanceUpdateStrategy().apply(_context(twin=twin))
        assert twin.performance is original_performance
        assert twin.performance.assessment_ids == ()
        assert twin.performance.evidence_ids == ()
        assert twin.performance.last_updated is None

    def test_returns_new_twin_instance(self) -> None:
        twin = _twin()
        updated = PerformanceUpdateStrategy().apply(_context(twin=twin))
        assert updated is not twin
        assert updated.performance is not twin.performance

    def test_preserves_other_domain_states(self) -> None:
        twin = _twin()
        updated = PerformanceUpdateStrategy().apply(_context(twin=twin))
        assert updated.identity is twin.identity
        assert updated.goals is twin.goals
        assert updated.knowledge is twin.knowledge
        assert updated.memory is twin.memory
        assert updated.behaviour is twin.behaviour
        assert updated.predictions is twin.predictions

    def test_twin_remains_frozen(self) -> None:
        twin = _twin()
        updated = PerformanceUpdateStrategy().apply(_context(twin=twin))
        with pytest.raises(AttributeError):
            updated.performance = twin.performance  # type: ignore[misc]


class TestOwnershipAndCrossDomainIsolation:
    """Performance must not steal sibling ownership or mutate other domains."""

    def test_quiz_only_leaves_behaviour_knowledge_memory_unchanged(self) -> None:
        prior_knowledge = TopicMasteryRecord.create(
            "T1",
            mastery_belief=0.55,
            evidence_ids=("ev-prior-k",),
        )
        prior_memory = RetentionRecord.create(
            "T1",
            last_reinforced=datetime(2026, 6, 1, tzinfo=UTC),
        )
        prior_behaviour = BehaviourState.create(
            consistency_metrics={"adherence_ratio": 0.8},
            evidence_ids=("ev-prior-b",),
        )
        twin = _twin(
            knowledge=KnowledgeState.create(topic_mastery=[prior_knowledge]),
            memory=MemoryState.create(retention=[prior_memory]),
            behaviour=prior_behaviour,
        )
        updated = PerformanceUpdateStrategy().apply(_context(twin=twin))
        assert updated.knowledge is twin.knowledge
        assert updated.memory is twin.memory
        assert updated.behaviour is twin.behaviour
        assert updated.knowledge.topic_mastery[0].mastery_belief == 0.55
        assert updated.memory.retention[0].last_reinforced == datetime(
            2026, 6, 1, tzinfo=UTC
        )
        assert updated.behaviour.consistency_metrics == {"adherence_ratio": 0.8}

    def test_mission_only_does_not_run_performance(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.MISSION_COMPLETED,
                topic_id=None,
                payload={"mission_id": "m-1"},
            )
        )
        assert strategy.supports(context) is False

    def test_revision_only_does_not_run_performance(self) -> None:
        strategy = PerformanceUpdateStrategy()
        context = _context(
            evidence=_evidence(
                evidence_type=EvidenceType.FLASHCARD_REVIEW,
                topic_id="T1",
                payload={},
            )
        )
        assert strategy.supports(context) is False

    def test_post_exam_is_not_behaviour_primary(self) -> None:
        assert EvidenceType.POST_EXAM_OUTCOME not in BEHAVIOUR_EVIDENCE_TYPES
        behaviour = BehaviourUpdateStrategy()
        performance = PerformanceUpdateStrategy()
        evidence = _evidence(
            evidence_type=EvidenceType.POST_EXAM_OUTCOME,
            payload={"assessment_id": "sitting-1"},
        )
        assert behaviour.supports(_context(evidence=evidence)) is False
        assert performance.supports(_context(evidence=evidence)) is True

    def test_performance_does_not_write_mastery_or_retention(self) -> None:
        updated = PerformanceUpdateStrategy().apply(_context())
        assert updated.knowledge.topic_mastery == ()
        assert updated.memory.retention == ()
        assert updated.behaviour.consistency_metrics == {}


class TestPipelineIntegration:
    """PerformanceUpdateStrategy through TwinUpdatePipeline."""

    def test_pipeline_applies_performance_strategy(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([PerformanceUpdateStrategy()])
        result = pipeline.update(twin, _evidence())
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is not twin
        assert result.applied_strategies == ("performance_update",)
        assert result.updated_twin.performance.evidence_ids == ("ev-1",)
        assert twin.performance.evidence_ids == ()

    def test_pipeline_skips_when_not_applicable(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([PerformanceUpdateStrategy()])
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

    def test_pipeline_processes_batch_of_performance_evidence(self) -> None:
        pipeline = TwinUpdatePipeline([PerformanceUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-1",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    payload={"assessment_id": "quiz-1"},
                ),
                _evidence(
                    evidence_id="ev-2",
                    evidence_type=EvidenceType.MOCK_EXAM,
                    payload={"mock_id": "mock-2"},
                ),
                _evidence(
                    evidence_id="ev-3",
                    evidence_type=EvidenceType.DIAGNOSTIC_ASSESSMENT,
                    payload={"diagnostic_id": "diag-3"},
                ),
            ],
        )
        assert result.applied_strategies == ("performance_update",)
        assert result.updated_twin.performance.assessment_ids == (
            "quiz-1",
            "mock-2",
            "diag-3",
        )
        assert result.updated_twin.performance.evidence_ids == (
            "ev-1",
            "ev-2",
            "ev-3",
        )

    def test_pipeline_ignores_non_performance_items_in_mixed_batch(self) -> None:
        pipeline = TwinUpdatePipeline([PerformanceUpdateStrategy()])
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    topic_id=None,
                    payload={"mission_id": "m-1"},
                ),
                _evidence(
                    evidence_id="ev-quiz",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    payload={"assessment_id": "quiz-1"},
                ),
            ],
        )
        assert result.updated_twin.performance.evidence_ids == ("ev-quiz",)
        assert result.updated_twin.performance.assessment_ids == ("quiz-1",)

    def test_pipeline_registration_order_knowledge_memory_behaviour_performance(
        self,
    ) -> None:
        pipeline = TwinUpdatePipeline(
            [
                KnowledgeUpdateStrategy(),
                MemoryUpdateStrategy(),
                BehaviourUpdateStrategy(),
                PerformanceUpdateStrategy(),
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
                    topic_id=None,
                    payload={"mission_id": "m-1"},
                ),
                _evidence(
                    evidence_id="ev-quiz",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    topic_id="T1",
                    payload={"assessment_id": "quiz-1"},
                ),
            ],
        )
        assert result.applied_strategies == (
            "knowledge_update",
            "memory_update",
            "behaviour_update",
            "performance_update",
        )
        assert result.updated_twin.knowledge.evidence_ids == ("ev-q", "ev-quiz")
        assert result.updated_twin.memory.revision_ids == ("ev-rev",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-mission",)
        assert result.updated_twin.performance.evidence_ids == ("ev-quiz",)

    def test_pipeline_mission_plus_quiz_keeps_domains_distinct(self) -> None:
        pipeline = TwinUpdatePipeline(
            [
                KnowledgeUpdateStrategy(),
                BehaviourUpdateStrategy(),
                PerformanceUpdateStrategy(),
            ]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(
                    evidence_id="ev-quiz",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    topic_id="T1",
                    payload={"assessment_id": "quiz-1"},
                ),
                _evidence(
                    evidence_id="ev-mission",
                    evidence_type=EvidenceType.MISSION_COMPLETED,
                    topic_id=None,
                    payload={"mission_id": "m-1"},
                ),
            ],
        )
        assert result.applied_strategies == (
            "knowledge_update",
            "behaviour_update",
            "performance_update",
        )
        assert result.updated_twin.knowledge.evidence_ids == ("ev-quiz",)
        assert result.updated_twin.behaviour.evidence_ids == ("ev-mission",)
        assert result.updated_twin.performance.assessment_ids == ("quiz-1",)
        # Mission must not overwrite quiz-driven Knowledge/Performance.
        assert result.updated_twin.knowledge.topic_mastery[0].evidence_ids == (
            "ev-quiz",
        )
        assert result.updated_twin.performance.evidence_ids == ("ev-quiz",)

    def test_pipeline_flashcard_plus_quiz_applies_memory_knowledge_performance(
        self,
    ) -> None:
        pipeline = TwinUpdatePipeline(
            [
                KnowledgeUpdateStrategy(),
                MemoryUpdateStrategy(),
                PerformanceUpdateStrategy(),
            ]
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
                    evidence_id="ev-quiz",
                    evidence_type=EvidenceType.QUIZ_COMPLETED,
                    topic_id="T1",
                    payload={"assessment_id": "quiz-1"},
                ),
            ],
        )
        assert result.applied_strategies == (
            "knowledge_update",
            "memory_update",
            "performance_update",
        )
        assert result.updated_twin.memory.revision_ids == ("ev-flash",)
        assert result.updated_twin.performance.assessment_ids == ("quiz-1",)


class TestEducationalFidelity:
    """Hard educational rules for structural Performance."""

    def test_mission_completion_alone_does_not_invent_performance(self) -> None:
        pipeline = TwinUpdatePipeline(
            [BehaviourUpdateStrategy(), PerformanceUpdateStrategy()]
        )
        result = pipeline.update(
            _twin(),
            _evidence(
                evidence_type=EvidenceType.MISSION_COMPLETED,
                topic_id=None,
                payload={"mission_id": "m-1"},
            ),
        )
        assert result.applied_strategies == ("behaviour_update",)
        assert result.updated_twin.performance.assessment_ids == ()
        assert result.updated_twin.performance.performance_summaries == ()
        assert result.updated_twin.performance.evidence_ids == ()

    def test_cold_start_stays_empty_without_assessment_evidence(self) -> None:
        twin = _twin()
        assert twin.performance.assessment_ids == ()
        assert twin.performance.performance_summaries == ()
        strategy = PerformanceUpdateStrategy()
        non_assessment = _evidence(
            evidence_type=EvidenceType.TIME_ON_TASK,
            topic_id=None,
            payload={"session_id": "s-1"},
        )
        assert strategy.supports(_context(evidence=non_assessment)) is False
        updated = strategy.apply(_context(twin=twin, evidence=non_assessment))
        assert updated is twin
        assert updated.performance.assessment_ids == ()
        assert updated.performance.performance_summaries == ()
        assert updated.performance.evidence_ids == ()

    def test_formative_condition_is_not_upgraded_to_exam_condition(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=_evidence(
                    payload={
                        "assessment_id": "quiz-1",
                        "condition": "formative",
                    }
                )
            )
        )
        summary = updated.performance.performance_summaries[0].summary
        assert summary["condition"] == "formative"
        assert summary.get("condition") != "exam-condition"
        assert "exam-condition" not in summary.values()

    def test_does_not_invent_high_performance_or_pass_probability(self) -> None:
        updated = PerformanceUpdateStrategy().apply(_context())
        summary = updated.performance.performance_summaries[0].summary
        forbidden_keys = {
            "accuracy",
            "strength",
            "pass_probability",
            "readiness",
            "irt_theta",
            "high_performance",
        }
        assert forbidden_keys.isdisjoint(summary)
        assert updated.predictions.readiness_snapshot is None
        assert updated.predictions.pass_probability_snapshot is None

    def test_contradictory_scopes_remain_visible(self) -> None:
        updated = PerformanceUpdateStrategy().apply(
            _context(
                evidence=[
                    _evidence(
                        evidence_id="ev-formative",
                        payload={
                            "assessment_id": "quiz-untimed",
                            "condition": "formative",
                            "summary": {"note": "strong"},
                        },
                    ),
                    _evidence(
                        evidence_id="ev-exam",
                        evidence_type=EvidenceType.MOCK_EXAM,
                        payload={
                            "assessment_id": "mock-timed",
                            "condition": "exam-condition",
                            "summary": {"note": "weak"},
                        },
                    ),
                ]
            )
        )
        scopes = {
            s.scope_id: s.summary
            for s in updated.performance.performance_summaries
        }
        assert scopes["quiz-untimed"]["condition"] == "formative"
        assert scopes["quiz-untimed"]["note"] == "strong"
        assert scopes["mock-timed"]["condition"] == "exam-condition"
        assert scopes["mock-timed"]["note"] == "weak"

    def test_does_not_compute_scoring_api(self) -> None:
        strategy = PerformanceUpdateStrategy()
        public_callables = {
            name
            for name in dir(strategy)
            if callable(getattr(strategy, name)) and not name.startswith("_")
        }
        forbidden = {
            "compute_accuracy",
            "compute_strength",
            "pass_probability",
            "readiness",
            "irt",
            "predict",
            "recommend",
            "plan",
            "persist",
            "save",
            "compute_mastery",
            "compute_retention",
        }
        assert forbidden.isdisjoint(public_callables)
        assert PERFORMANCE_EVIDENCE_TYPES  # catalogue is exported for extension


class TestFrameworkIndependence:
    """Performance strategy must remain framework-independent."""

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
        module_name = "app.domain.twin.strategies.performance_update_strategy"
        assert module_name in sys.modules
        module = sys.modules[module_name]
        assert not any(
            dep in getattr(module, "__dict__", {})
            for dep in ("Flask", "request", "db", "SQLAlchemy")
        )

"""Unit tests for structural Readiness Aggregation (Capability 2.7)."""

from __future__ import annotations

import ast
import copy
import sys
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.domain.readiness import (
    FACTOR_CATALOGUE,
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    FactorId,
    FactorPosture,
    OverallPosture,
    ReadinessAggregation,
    ReadinessState,
    WarrantPosture,
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
    RetentionRecord,
    TopicMasteryRecord,
)

READINESS_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "readiness"
AGGREGATION_PATH = READINESS_ROOT / "aggregation.py"
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
FORBIDDEN_PREFIXES = (
    "app.services",
    "app.models",
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


def _identity(**overrides: object) -> IdentityState:
    defaults: dict[str, object] = {
        "student_id": "student-42",
        "curriculum_id": "CS1-2026",
        "current_exam": "CS1",
        "target_sitting": date(2026, 9, 15),
    }
    defaults.update(overrides)
    return IdentityState.create(**defaults)  # type: ignore[arg-type]


def _curriculum_v1() -> CurriculumContext:
    return CurriculumContext.create(
        "CS1-2026",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.4),
            CurriculumTopicRef.create("topic-b", weight=0.4),
            CurriculumTopicRef.create("topic-c", weight=0.2),
        ],
    )


def _curriculum_v2() -> CurriculumContext:
    return CurriculumContext.create(
        "CS1-2026",
        format=CurriculumFormat.V2,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.5, section_id="sec-1"),
            CurriculumTopicRef.create("topic-b", weight=0.3, section_id="sec-1"),
            CurriculumTopicRef.create("topic-c", weight=0.2, section_id="sec-2"),
        ],
        section_ids=("sec-1", "sec-2"),
    )


def _goals_only_twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2026, 9, 15),
            planned_study_hours_per_week=10.0,
        ),
    )


def _empty_twin() -> DigitalTwin:
    return DigitalTwin.create(_identity(curriculum_id="CS1-2026"))


def _behaviour_only_twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
        behaviour=BehaviourState.create(
            evidence_ids=["ev-mission-1"],
            session_history_ids=["session-1"],
        ),
    )


def _disagreement_twin() -> DigitalTwin:
    """Supportive Knowledge proxy beside risk-elevating Memory/Performance."""
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
        knowledge=KnowledgeState.create(
            topic_mastery=[
                TopicMasteryRecord.create(
                    "topic-a",
                    mastery_belief=0.75,
                    evidence_ids=["ev-k-1"],
                ),
            ],
            evidence_ids=["ev-k-1"],
        ),
        memory=MemoryState.create(
            retention=[
                RetentionRecord.create("topic-a", last_reinforced=None),
            ],
            revision_ids=["ev-m-1"],
        ),
        performance=PerformanceState.create(
            assessment_ids=["assess-1"],
            evidence_ids=["ev-p-1"],
            performance_summaries=[
                PerformanceSummary.create(
                    "topic-a",
                    summary={"strength": "weak", "condition": "mock"},
                ),
            ],
        ),
    )


def _snapshot_domains(twin: DigitalTwin) -> dict[str, object]:
    return {
        "knowledge": twin.knowledge,
        "memory": twin.memory,
        "behaviour": twin.behaviour,
        "performance": twin.performance,
        "goals": twin.goals,
        "identity": twin.identity,
        "predictions": twin.predictions,
    }


# ---------------------------------------------------------------------------
# Contract / catalogue / immutability
# ---------------------------------------------------------------------------


class TestContract:
    """derive returns a full-catalogue frozen ReadinessState."""

    def test_derive_returns_readiness_state_with_full_catalogue(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        assert isinstance(state, ReadinessState)
        assert tuple(j.factor_id for j in state.factors) == FACTOR_CATALOGUE
        assert len(state.factors) == 7

    def test_readiness_state_is_frozen(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        with pytest.raises(AttributeError):
            state.overall_posture = OverallPosture.FRAGILE  # type: ignore[misc]
        with pytest.raises(AttributeError):
            state.factors[0].posture = FactorPosture.SUPPORTIVE  # type: ignore[misc]

    def test_factor_lookup(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        judgement = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert judgement.factor_id == FactorId.ASSESSMENT_PERFORMANCE

    def test_no_numeric_score_or_pass_probability_fields(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        assert not hasattr(state, "score")
        assert not hasattr(state, "readiness_percent")
        assert not hasattr(state, "pass_probability")
        assert not hasattr(state, "composite")


class TestDeterminism:
    """Same Twin + CurriculumContext → equal structural fields."""

    def test_same_inputs_equal_structural_fields(self) -> None:
        twin = _disagreement_twin()
        curriculum = _curriculum_v1()
        a = ReadinessAggregation.derive(twin, curriculum)
        b = ReadinessAggregation.derive(twin, curriculum)
        assert a.overall_posture == b.overall_posture
        assert a.overall_warrant == b.overall_warrant
        assert a.cold_start == b.cold_start
        assert a.factors == b.factors
        assert a.scope == b.scope
        assert a.goal_constraint_notes == b.goal_constraint_notes


# ---------------------------------------------------------------------------
# Cold start / unknown
# ---------------------------------------------------------------------------


class TestColdStart:
    """Goals-only / empty domains never fabricate Mid/High readiness."""

    def test_goals_only_not_yet_knowable(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        assert state.cold_start is True
        assert state.overall_posture == OverallPosture.NOT_YET_KNOWABLE
        assert state.overall_warrant == WarrantPosture.LOW
        assert state.overall_posture.value not in {"mid", "high", "ready", "supportive"}

    def test_empty_twin_not_yet_knowable(self) -> None:
        state = ReadinessAggregation.derive(_empty_twin(), _curriculum_v1())
        assert state.cold_start is True
        assert state.overall_posture == OverallPosture.NOT_YET_KNOWABLE
        assert state.overall_warrant == WarrantPosture.LOW

    def test_cold_start_factors_unknown_or_low_warrant(self) -> None:
        state = ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        forbidden = {FactorPosture.SUPPORTIVE}  # content factors must not claim ready
        content_factors = {
            FactorId.CURRICULUM_COVERAGE,
            FactorId.KNOWLEDGE_STRENGTH,
            FactorId.MEMORY_STABILITY,
            FactorId.ASSESSMENT_PERFORMANCE,
        }
        for judgement in state.factors:
            if judgement.factor_id in content_factors:
                assert judgement.posture in {
                    FactorPosture.UNKNOWN,
                    FactorPosture.LOW_WARRANT,
                    FactorPosture.NOT_APPLICABLE,
                    FactorPosture.RISK_ELEVATING,
                }
                assert judgement.posture not in forbidden or judgement.factor_id == (
                    FactorId.TIME_GOAL_PRESSURE
                )
                assert judgement.sparse or judgement.posture != FactorPosture.SUPPORTIVE

    def test_behaviour_only_does_not_yield_exam_ready(self) -> None:
        state = ReadinessAggregation.derive(_behaviour_only_twin(), _curriculum_v1())
        assert state.overall_posture == OverallPosture.NOT_YET_KNOWABLE
        assert state.overall_warrant == WarrantPosture.LOW
        behaviour = state.factor(FactorId.BEHAVIOUR_RELIABILITY)
        assessment = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert behaviour.posture == FactorPosture.SUPPORTIVE
        assert assessment.posture == FactorPosture.UNKNOWN
        assert "not_exam_readiness" in behaviour.attribution.notes


class TestEmptyDomains:
    """Domain-empty mapping contracts."""

    def test_empty_performance_assessment_unknown(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create("topic-a", mastery_belief=0.6),
                ],
            ),
            behaviour=BehaviourState.create(evidence_ids=["ev-b-1"]),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        assessment = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert assessment.posture == FactorPosture.UNKNOWN
        assert assessment.warrant == WarrantPosture.LOW
        assert state.overall_warrant == WarrantPosture.LOW

    def test_empty_mastery_beliefs_knowledge_strength_unknown(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[TopicMasteryRecord.create("topic-a")],
            ),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        strength = state.factor(FactorId.KNOWLEDGE_STRENGTH)
        coverage = state.factor(FactorId.CURRICULUM_COVERAGE)
        assert strength.posture == FactorPosture.UNKNOWN
        assert "empty_mastery_beliefs" in strength.attribution.notes
        assert coverage.posture == FactorPosture.LOW_WARRANT
        assert strength.posture != FactorPosture.SUPPORTIVE

    def test_empty_memory_stability_unknown(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create("topic-a", mastery_belief=0.5),
                ],
            ),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        memory = state.factor(FactorId.MEMORY_STABILITY)
        assert memory.posture == FactorPosture.UNKNOWN
        assert memory.sparse is True


# ---------------------------------------------------------------------------
# Factor disagreement / warrant / confidence
# ---------------------------------------------------------------------------


class TestFactorDisagreement:
    """Factors may conflict; disagreement remains visible."""

    def test_supportive_knowledge_beside_risk_elevating_peers(self) -> None:
        state = ReadinessAggregation.derive(_disagreement_twin(), _curriculum_v1())
        knowledge = state.factor(FactorId.KNOWLEDGE_STRENGTH)
        memory = state.factor(FactorId.MEMORY_STABILITY)
        assessment = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert knowledge.posture == FactorPosture.SUPPORTIVE
        assert memory.posture == FactorPosture.RISK_ELEVATING
        assert assessment.posture == FactorPosture.RISK_ELEVATING
        assert state.overall_posture in {
            OverallPosture.MIXED,
            OverallPosture.FRAGILE,
            OverallPosture.NOT_YET_KNOWABLE,
        }
        # Disagreement not averaged into a fabricated Mid/High.
        assert state.overall_posture.value not in {"mid", "high", "ready"}


class TestWarrantPropagation:
    """Overall warrant constrained by sparse critical factors."""

    def test_sparse_performance_constrains_overall_warrant(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create(
                        "topic-a",
                        mastery_belief=0.8,
                        evidence_ids=["ev-k"],
                    ),
                ],
            ),
            behaviour=BehaviourState.create(
                evidence_ids=["ev-b"],
                session_history_ids=["s1"],
            ),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        assert state.factor(FactorId.ASSESSMENT_PERFORMANCE).sparse is True
        assert state.overall_warrant == WarrantPosture.LOW
        warrant_factor = state.factor(FactorId.EVIDENCE_WARRANT)
        assert warrant_factor.warrant == WarrantPosture.LOW

    def test_low_weight_dense_evidence_does_not_inflate_sitting_warrant(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create(
                        "topic-c",  # low weight 0.2
                        mastery_belief=0.9,
                        evidence_ids=["ev-low"],
                    ),
                ],
            ),
            performance=PerformanceState.create(
                assessment_ids=["a1"],
                evidence_ids=["ev-p"],
                performance_summaries=[
                    PerformanceSummary.create("topic-c", summary={"note": "ok"}),
                ],
            ),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        assert state.overall_warrant == WarrantPosture.LOW


class TestConfidenceOmission:
    """Confidence-shaped bags must not upgrade Assessment Performance."""

    def test_confidence_in_knowledge_lineage_does_not_upgrade_assessment(self) -> None:
        # Structural proxy: confidence-like payload must not invent Performance.
        twin = DigitalTwin.create(
            _identity(),
            knowledge=KnowledgeState.create(
                topic_mastery=[
                    TopicMasteryRecord.create(
                        "topic-a",
                        mastery_belief=0.5,
                        evidence_ids=["ev-confidence"],
                    ),
                ],
                evidence_ids=["ev-confidence"],
            ),
            behaviour=BehaviourState.create(
                consistency_metrics={"confidence_self_report": 0.95},
                evidence_ids=["ev-b"],
            ),
        )
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        assessment = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert assessment.posture == FactorPosture.UNKNOWN
        assert state.overall_warrant == WarrantPosture.LOW
        # No confidence factor in catalogue.
        assert all(j.factor_id != "confidence" for j in state.factors)


# ---------------------------------------------------------------------------
# Curriculum V1/V2 / attributions / explainability
# ---------------------------------------------------------------------------


class TestCurriculumContext:
    """V1 and V2 contexts both derive with the same catalogue."""

    def test_v1_flat_context_derives(self) -> None:
        state = ReadinessAggregation.derive(_disagreement_twin(), _curriculum_v1())
        assert state.curriculum_format == CurriculumFormat.V1
        assert len(state.factors) == len(FACTOR_CATALOGUE)

    def test_v2_section_context_derives(self) -> None:
        state = ReadinessAggregation.derive(_disagreement_twin(), _curriculum_v2())
        assert state.curriculum_format == CurriculumFormat.V2
        assert len(state.factors) == len(FACTOR_CATALOGUE)
        coverage = state.factor(FactorId.CURRICULUM_COVERAGE)
        assert "format_v2" in coverage.attribution.notes

    def test_v1_does_not_require_sections(self) -> None:
        curriculum = CurriculumContext.create(
            "flat-only",
            format="v1",
            topics=[CurriculumTopicRef.create("t1", weight=1.0)],
            section_ids=(),
        )
        state = ReadinessAggregation.derive(_empty_twin(), curriculum)
        assert state.curriculum_format == CurriculumFormat.V1
        assert state.overall_posture == OverallPosture.NOT_YET_KNOWABLE


class TestAttributionsAndExplainability:
    """Explainability chain: Curriculum → Twin → Factor → Overall."""

    def test_factors_cite_twin_domains_and_curriculum(self) -> None:
        state = ReadinessAggregation.derive(_disagreement_twin(), _curriculum_v1())
        knowledge = state.factor(FactorId.KNOWLEDGE_STRENGTH)
        assessment = state.factor(FactorId.ASSESSMENT_PERFORMANCE)
        assert "knowledge" in knowledge.attribution.twin_domains
        assert knowledge.attribution.curriculum_entity_ids
        assert knowledge.attribution.evidence_ids
        assert "performance" in assessment.attribution.twin_domains
        assert "topic-a" in assessment.attribution.curriculum_entity_ids

    def test_overall_accompanied_by_factors_and_warrant(self) -> None:
        state = ReadinessAggregation.derive(_disagreement_twin(), _curriculum_v1())
        assert state.factors
        assert state.overall_warrant is not None
        warrant = state.factor(FactorId.EVIDENCE_WARRANT)
        assert warrant.factor_id == FactorId.EVIDENCE_WARRANT
        assert any(
            note.startswith("overall_warrant_") for note in warrant.attribution.notes
        )

    def test_scope_binds_identity_and_goals(self) -> None:
        twin = _goals_only_twin()
        state = ReadinessAggregation.derive(twin, _curriculum_v1())
        assert state.scope.student_id == "student-42"
        assert state.scope.curriculum_id == "CS1-2026"
        assert state.scope.sitting_date == date(2026, 9, 15)
        assert "goal_completion_date" in state.goal_constraint_notes


# ---------------------------------------------------------------------------
# Purity / immutability / firewall
# ---------------------------------------------------------------------------


class TestNoTwinMutation:
    """Aggregation must not mutate Twin domains."""

    def test_twin_domains_unchanged_after_derive(self) -> None:
        twin = _disagreement_twin()
        before = _snapshot_domains(twin)
        before_copy = copy.deepcopy(before)
        ReadinessAggregation.derive(twin, _curriculum_v1())
        after = _snapshot_domains(twin)
        assert after == before
        assert after == before_copy

    def test_goals_only_twin_unchanged(self) -> None:
        twin = _goals_only_twin()
        before = twin.knowledge, twin.memory, twin.behaviour, twin.performance
        ReadinessAggregation.derive(twin, _curriculum_v1())
        assert (
            twin.knowledge,
            twin.memory,
            twin.behaviour,
            twin.performance,
        ) == before


class TestFrameworkPurity:
    """Domain package must remain framework-free."""

    def test_aggregation_source_has_no_framework_imports(self) -> None:
        violations: list[str] = []
        for path in READINESS_ROOT.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES:
                            violations.append(
                                f"{path}:{node.lineno} import {alias.name}"
                            )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES:
                        violations.append(f"{path}:{node.lineno} from {node.module}")
        assert violations == []

    def test_aggregation_does_not_import_services_or_decision(self) -> None:
        violations: list[str] = []
        for path in READINESS_ROOT.glob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.startswith(FORBIDDEN_PREFIXES):
                        violations.append(f"{path}:{node.lineno} from {node.module}")
                    if "decision" in node.module or "mission" in node.module:
                        if node.module.startswith("app."):
                            violations.append(
                                f"{path}:{node.lineno} from {node.module}"
                            )
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith(FORBIDDEN_PREFIXES):
                            violations.append(
                                f"{path}:{node.lineno} import {alias.name}"
                            )
        assert violations == []

    def test_importing_readiness_does_not_require_flask(self) -> None:
        module_name = "app.domain.readiness.aggregation"
        assert module_name in sys.modules
        module = sys.modules[module_name]
        assert not any(
            dep in getattr(module, "__dict__", {})
            for dep in ("Flask", "request", "db", "SQLAlchemy")
        )

    def test_no_update_strategy_registration_side_effects(self) -> None:
        # Readiness must not be an Update Strategy; derive must not require
        # pipeline registration. Import pipeline lazily to keep domain tests light.
        from app.domain.twin.update_pipeline import TwinUpdatePipeline

        pipeline = TwinUpdatePipeline()
        before = tuple(s.name for s in pipeline.strategies)
        ReadinessAggregation.derive(_goals_only_twin(), _curriculum_v1())
        after = tuple(s.name for s in pipeline.strategies)
        assert before == after == ()


class TestPublicApi:
    """Package exports are stable and additive."""

    def test_package_exports(self) -> None:
        import app.domain.readiness as readiness

        for name in (
            "ReadinessState",
            "ReadinessAggregation",
            "CurriculumContext",
            "FactorId",
            "FactorPosture",
            "WarrantPosture",
            "OverallPosture",
            "FACTOR_CATALOGUE",
        ):
            assert hasattr(readiness, name)

    def test_derive_accepts_optional_as_of(self) -> None:
        as_of = datetime(2026, 7, 11, tzinfo=UTC)
        state = ReadinessAggregation.derive(
            _goals_only_twin(),
            _curriculum_v1(),
            as_of=as_of,
            derivation_id="deriv-1",
        )
        assert state.derived_at == as_of
        assert state.derivation_id == "deriv-1"

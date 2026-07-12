"""Unit tests for structural Mission Intelligence (Capability 2.10.4)."""

from __future__ import annotations

import ast
import copy
from datetime import date
from pathlib import Path

import pytest

from app.domain.decision import (
    ACTION_FAMILY_CATALOGUE,
    ENGINE_VERSION,
    ActionFamily,
    ActionIntent,
    CandidateStatus,
    Constraints,
    Decision,
    DecisionEngine,
    DecisionHistory,
    DecisionWarrantPosture,
    HistoryEntry,
    HistoryOutcome,
    IntensityPosture,
    ReasonCodeId,
)
from app.domain.mission import (
    COMPLETION_OUTCOME_CATALOGUE,
    MISSION_INTELLIGENCE_VERSION,
    THIN_MISSION_WARRANT_POSTURES,
    BehaviourEvidenceCategoryHint,
    FeasibilityEffect,
    Mission,
    MissionEngine,
    MissionEvidenceHooks,
    MissionExecutionContext,
    MissionExplanationChainLayer,
    MissionIntelligence,
    MissionOutcomeIdentity,
    MissionTask,
    MissionWarrantPosture,
)
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    OverallPosture,
    ReadinessAggregation,
    WarrantPosture,
)
from app.domain.recommendation import (
    Recommendation,
    RecommendationEngine,
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

MISSION_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "mission"
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
    "app.domain.twin.strategies",
    "app.domain.twin.update_pipeline",
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


def _disagreement_twin() -> DigitalTwin:
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


def _behaviour_strong_perf_thin_twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
        knowledge=KnowledgeState.create(
            topic_mastery=[
                TopicMasteryRecord.create(
                    "topic-a",
                    mastery_belief=0.6,
                    evidence_ids=["ev-k"],
                ),
            ],
            evidence_ids=["ev-k"],
        ),
        behaviour=BehaviourState.create(
            evidence_ids=["ev-b-1"],
            session_history_ids=["session-1"],
            consistency_metrics={"adherence": 0.9},
        ),
    )


def _ample_constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


def _protect_constraints() -> Constraints:
    return Constraints.create(
        available_minutes=40,
        intensity=IntensityPosture.PROTECT,
        burnout_risk=True,
        note_tags=("burnout_flag",),
    )


def _decide(
    twin: DigitalTwin,
    curriculum: CurriculumContext | None = None,
    constraints: Constraints | None = None,
    *,
    decision_history: DecisionHistory | None = None,
) -> Decision:
    curriculum = curriculum or _curriculum_v1()
    constraints = constraints or _ample_constraints()
    readiness = ReadinessAggregation.derive(twin, curriculum)
    return DecisionEngine.evaluate(
        twin,
        readiness,
        curriculum,
        constraints,
        decision_history=decision_history,
    )


def _ample_context(**overrides: object) -> MissionExecutionContext:
    defaults: dict[str, object] = {
        "session_window_id": "session-1",
        "session_date": date(2026, 7, 12),
        "constraints": _ample_constraints(),
        "twin_snapshot_ref": "twin-snap-1",
    }
    defaults.update(overrides)
    return MissionExecutionContext.create(**defaults)  # type: ignore[arg-type]


def _compose(
    twin: DigitalTwin,
    curriculum: CurriculumContext | None = None,
    constraints: Constraints | None = None,
    *,
    execution_context: MissionExecutionContext | None = None,
    recommendation_language: Recommendation | None = None,
    decision_history: DecisionHistory | None = None,
) -> tuple[Decision, Mission]:
    decision = _decide(
        twin,
        curriculum,
        constraints,
        decision_history=decision_history,
    )
    ctx = execution_context or _ample_context(
        constraints=constraints or _ample_constraints()
    )
    mission = MissionIntelligence.compose(
        decision,
        ctx,
        recommendation_language=recommendation_language,
    )
    return decision, mission


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
# Contract / composition
# ---------------------------------------------------------------------------


class TestCompositionContract:
    def test_compose_returns_mission_with_required_fields(self) -> None:
        decision, mission = _compose(_goals_only_twin())
        assert isinstance(mission, Mission)
        assert mission.mission_intelligence_version == MISSION_INTELLIGENCE_VERSION
        assert len(mission.decision_citations) >= 1
        assert mission.decision_citations[0].engine_version == decision.engine_version
        assert mission.scope.student_id == decision.scope.student_id
        assert mission.evidence_hooks.mastery_implied is False
        assert mission.regeneration_identity.compose_version == (
            MISSION_INTELLIGENCE_VERSION
        )

    def test_mission_engine_alias(self) -> None:
        assert MissionEngine is MissionIntelligence

    def test_tasks_attributable_and_frozen(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        assert len(mission.tasks) >= 1
        for task in mission.tasks:
            assert isinstance(task, MissionTask)
            assert len(task.attribution.reason_code_citations) >= 1
            assert task.family == decision.selected.family
        with pytest.raises(AttributeError):
            mission.mission_intelligence_version = "mutated"  # type: ignore[misc]
        with pytest.raises(AttributeError):
            mission.tasks[0].family = ActionFamily.STUDY  # type: ignore[misc]

    def test_no_scoring_or_optimisation_fields(self) -> None:
        _, mission = _compose(_goals_only_twin())
        assert not hasattr(mission, "score")
        assert not hasattr(mission, "priority_score")
        assert not hasattr(mission, "ranking_score")
        assert not hasattr(mission, "optimization_objective")
        assert not hasattr(mission, "packing_score")
        assert not hasattr(mission.tasks[0], "priority_percent")


# ---------------------------------------------------------------------------
# Decision attribution / explainability
# ---------------------------------------------------------------------------


class TestDecisionAttribution:
    def test_every_task_maps_to_decision_reason_codes(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        decision_codes = {r.code_id for r in decision.reason_codes}
        for task in mission.tasks:
            assert task.attribution.reason_code_ids
            for code in task.attribution.reason_code_ids:
                assert code in decision_codes

    def test_lineage_subset_of_decision(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        for task in mission.tasks:
            assert task.attribution.lineage == decision.lineage
            asserted = set(task.attribution.explanation_chain.evidence_ids)
            allowed = set(decision.lineage.evidence_ids)
            assert asserted <= allowed
            asserted_curriculum = set(
                task.attribution.explanation_chain.curriculum_entity_ids
            )
            allowed_curriculum = set(decision.lineage.curriculum_entity_ids)
            assert asserted_curriculum <= allowed_curriculum

    def test_no_invented_evidence_ids(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        for task in mission.tasks:
            for eid in task.attribution.lineage.evidence_ids:
                assert eid in decision.lineage.evidence_ids

    def test_candidate_contrast_never_promotes_rejected(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        decision_ids = {c.candidate_id for c in decision.candidates}
        for task in mission.tasks:
            for contrast in task.attribution.candidate_contrast:
                assert contrast.candidate_id in decision_ids
                assert contrast.status != CandidateStatus.SELECTED

    def test_explainability_chain_layers(self) -> None:
        _, mission = _compose(_disagreement_twin())
        layers = mission.tasks[0].attribution.explanation_chain.layers_present
        assert MissionExplanationChainLayer.CURRICULUM in layers
        assert MissionExplanationChainLayer.EVIDENCE in layers
        assert MissionExplanationChainLayer.TWIN in layers
        assert MissionExplanationChainLayer.DECISION in layers
        assert MissionExplanationChainLayer.MISSION_TASK in layers


# ---------------------------------------------------------------------------
# No re-selection / action-family fidelity / tension
# ---------------------------------------------------------------------------


class TestNoReselection:
    def test_task_matches_decision_selected(self) -> None:
        for twin_factory in (
            _goals_only_twin,
            _disagreement_twin,
            _behaviour_strong_perf_thin_twin,
        ):
            decision, mission = _compose(twin_factory())
            assert mission.tasks
            task = mission.tasks[0]
            assert task.family == decision.selected.family
            assert task.curriculum_entity_id == decision.selected.curriculum_entity_id
            assert task.intent == decision.selected.intent

    def test_rejected_candidates_not_promoted_under_tight_capacity(self) -> None:
        decision = _decide(_disagreement_twin())
        considered = [
            c for c in decision.candidates if c.status != CandidateStatus.SELECTED
        ]
        ctx = _ample_context(
            constraints=Constraints.create(available_minutes=0),
            already_committed_minutes=0,
        )
        mission = MissionIntelligence.compose(decision, ctx)
        assert mission.is_empty
        for c in considered:
            assert all(
                t.family != c.family or t.curriculum_entity_id != c.curriculum_entity_id
                for t in mission.tasks
            )

    def test_does_not_call_decision_engine(self) -> None:
        engine_src = (MISSION_ROOT / "engine.py").read_text(encoding="utf-8")
        assert "from app.domain.decision.engine" not in engine_src
        assert "DecisionEngine.evaluate" not in engine_src
        assert "DecisionEngine(" not in engine_src
        assert "from app.domain.decision.decision import Decision" in engine_src


class TestActionFamilyFidelity:
    def test_revise_not_collapsed_to_study(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        assert decision.selected.family == ActionFamily.REVISE
        assert mission.tasks[0].family == ActionFamily.REVISE
        assert mission.tasks[0].family != ActionFamily.STUDY

    def test_families_remain_decision_catalogue(self) -> None:
        _, mission = _compose(_disagreement_twin())
        assert mission.tasks[0].family in ACTION_FAMILY_CATALOGUE


class TestTensionPreservation:
    def test_knowledge_vs_memory_tension_visible(self) -> None:
        decision, mission = _compose(_disagreement_twin())
        code_ids = {c.value for c in mission.tasks[0].attribution.reason_code_ids}
        assert ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN.value in code_ids
        tags = mission.tasks[0].attribution.explanation_chain.value_rationale_tags
        assert tags == decision.lineage.value_rationale_tags


# ---------------------------------------------------------------------------
# Load shaping / empty capacity / constraints
# ---------------------------------------------------------------------------


class TestLoadShaping:
    def test_empty_capacity_valid_no_filler(self) -> None:
        decision = _decide(_disagreement_twin())
        ctx = _ample_context(
            constraints=Constraints.create(available_minutes=0),
        )
        mission = MissionIntelligence.compose(decision, ctx)
        assert mission.is_empty
        assert any(
            a.effect == FeasibilityEffect.EMPTY_CAPACITY_REMAINDER
            for a in mission.feasibility_acknowledgements
        )
        note_blob = " ".join(
            " ".join(a.note_tags) for a in mission.feasibility_acknowledgements
        )
        assert "no_filler" in note_blob or "empty_capacity" in note_blob

    def test_already_committed_reduces_capacity(self) -> None:
        decision = _decide(_goals_only_twin())
        ctx = _ample_context(
            constraints=Constraints.create(available_minutes=30),
            already_committed_minutes=30,
        )
        mission = MissionIntelligence.compose(decision, ctx)
        assert mission.is_empty
        assert any(
            a.effect
            in {
                FeasibilityEffect.EMPTY_CAPACITY_REMAINDER,
                FeasibilityEffect.ALREADY_COMMITTED_CAPACITY,
            }
            for a in mission.feasibility_acknowledgements
        )

    def test_batch_trailing_omission_preserves_order(self) -> None:
        d1 = _decide(_goals_only_twin())
        d2 = _decide(_disagreement_twin())
        # Force distinct evaluation ids for lineage clarity.
        ctx = _ample_context(
            constraints=Constraints.create(available_minutes=25),
            max_tasks=1,
        )
        mission = MissionIntelligence.compose((d1, d2), ctx)
        assert mission.task_count == 1
        assert mission.tasks[0].family == d1.selected.family
        assert any(
            a.effect == FeasibilityEffect.OMITTED_TRAILING_CAPACITY
            for a in mission.feasibility_acknowledgements
        )
        assert len(mission.decision_citations) == 2

    def test_leftover_capacity_does_not_invent_tasks(self) -> None:
        decision = _decide(_goals_only_twin())
        ctx = _ample_context(
            constraints=Constraints.create(available_minutes=180),
        )
        mission = MissionIntelligence.compose(decision, ctx)
        assert mission.task_count == 1
        assert mission.tasks[0].family == decision.selected.family


class TestConstraintAcknowledgements:
    def test_sustainability_demotes_intensity_not_family(self) -> None:
        decision, mission = _compose(
            _disagreement_twin(),
            constraints=_protect_constraints(),
            execution_context=_ample_context(constraints=_protect_constraints()),
        )
        assert decision.selected.family == ActionFamily.REST_PROTECT_INTENSITY
        assert mission.tasks[0].family == ActionFamily.REST_PROTECT_INTENSITY
        assert mission.tasks[0].intensity_demoted is True
        assert any(
            a.effect == FeasibilityEffect.SUSTAINABILITY_PROTECT
            for a in mission.feasibility_acknowledgements
        )
        note_blob = " ".join(
            " ".join(a.note_tags) for a in mission.feasibility_acknowledgements
        )
        assert "rest_protect_not_failure" in note_blob


# ---------------------------------------------------------------------------
# Warrant / cold-start
# ---------------------------------------------------------------------------


class TestWarrantInheritance:
    def test_cold_start_honest_warrant(self) -> None:
        decision, mission = _compose(_goals_only_twin())
        assert decision.warrant_posture in {
            DecisionWarrantPosture.COLD_START,
            DecisionWarrantPosture.NOT_YET_KNOWABLE,
            DecisionWarrantPosture.INHERITED_LOW,
        }
        assert mission.warrant_posture in THIN_MISSION_WARRANT_POSTURES
        assert mission.warrant_posture != MissionWarrantPosture.HONEST_HIGH
        assert "mid" not in mission.warrant_posture.value

    def test_not_yet_knowable_first_class(self) -> None:
        decision, mission = _compose(_goals_only_twin())
        assert decision.readiness_overall_posture == OverallPosture.NOT_YET_KNOWABLE
        assert decision.readiness_overall_warrant == WarrantPosture.LOW
        if decision.warrant_posture == DecisionWarrantPosture.NOT_YET_KNOWABLE:
            assert mission.warrant_posture == MissionWarrantPosture.NOT_YET_KNOWABLE


class TestColdStartMissions:
    def test_diagnostic_shaped_mission(self) -> None:
        decision, mission = _compose(_goals_only_twin())
        assert decision.selected.family == ActionFamily.DIAGNOSTIC
        assert mission.tasks[0].family == ActionFamily.DIAGNOSTIC
        assert mission.tasks[0].intent == ActionIntent.EVIDENCE_CREATING
        code_ids = {c.value for c in mission.tasks[0].attribution.reason_code_ids}
        assert ReasonCodeId.INSUFFICIENT_WARRANT.value in code_ids
        assert ReasonCodeId.PREFER_EVIDENCE_CREATING.value in code_ids


# ---------------------------------------------------------------------------
# Behaviour evidence hooks / completion ≠ mastery
# ---------------------------------------------------------------------------


class TestBehaviourEvidenceHooks:
    def test_completion_not_mastery(self) -> None:
        _, mission = _compose(_goals_only_twin())
        hooks = mission.evidence_hooks
        assert isinstance(hooks, MissionEvidenceHooks)
        assert hooks.mastery_implied is False
        assert hooks.behaviour_evidence_category_hint in {
            BehaviourEvidenceCategoryHint.BEHAVIOUR,
            BehaviourEvidenceCategoryHint.PLANNING,
        }
        assert MissionOutcomeIdentity.COMPLETED in COMPLETION_OUTCOME_CATALOGUE
        assert "completion_not_mastery" in hooks.notes
        assert "completion_not_exam_readiness" in hooks.notes
        for task in mission.tasks:
            assert task.evidence_hooks.mastery_implied is False


# ---------------------------------------------------------------------------
# Recommendation optional / Priority never sequences
# ---------------------------------------------------------------------------


class TestRecommendationOptional:
    def test_mission_valid_without_recommendation(self) -> None:
        _, mission = _compose(_disagreement_twin())
        assert mission.tasks[0].recommendation_language is None

    def test_language_attached_selection_unchanged(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        rec = RecommendationEngine.package(decision)
        mission_plain = MissionIntelligence.compose(decision, _ample_context())
        mission_lang = MissionIntelligence.compose(
            decision,
            _ample_context(),
            recommendation_language=rec,
        )
        assert mission_lang.tasks[0].family == mission_plain.tasks[0].family
        assert (
            mission_lang.tasks[0].curriculum_entity_id
            == mission_plain.tasks[0].curriculum_entity_id
        )
        assert mission_lang.tasks[0].recommendation_language is not None
        assert (
            mission_lang.tasks[0].recommendation_language.suggestion_family
            == decision.selected.family.value
        )

    def test_mismatched_recommendation_rejected(self) -> None:
        d1 = _decide(_goals_only_twin())
        d2 = _decide(_disagreement_twin())
        rec = RecommendationEngine.package(d2)
        with pytest.raises(ValueError, match="recommendation_language"):
            MissionIntelligence.compose(
                d1,
                _ample_context(),
                recommendation_language=rec,
            )


# ---------------------------------------------------------------------------
# Determinism / purity / no Twin mutation
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_same_inputs_equal_structural_fields(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        ctx = _ample_context()
        a = MissionIntelligence.compose(decision, ctx)
        b = MissionIntelligence.compose(decision, ctx)
        assert a.scope == b.scope
        assert a.tasks == b.tasks
        assert a.warrant_posture == b.warrant_posture
        assert a.feasibility_acknowledgements == b.feasibility_acknowledgements
        assert a.regeneration_identity == b.regeneration_identity


class TestNoTwinMutation:
    def test_twin_domains_unchanged_after_compose(self) -> None:
        twin = _disagreement_twin()
        before = _snapshot_domains(twin)
        before_copy = copy.deepcopy(before)
        decision = _decide(twin)
        MissionIntelligence.compose(decision, _ample_context())
        after = _snapshot_domains(twin)
        assert after == before
        assert after == before_copy

    def test_decision_unchanged_after_compose(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        before = (
            decision.selected,
            decision.candidates,
            decision.reason_codes,
            decision.lineage,
            decision.warrant_posture,
        )
        MissionIntelligence.compose(decision, _ample_context())
        assert (
            decision.selected,
            decision.candidates,
            decision.reason_codes,
            decision.lineage,
            decision.warrant_posture,
        ) == before


# ---------------------------------------------------------------------------
# Curriculum V1/V2 / lineage
# ---------------------------------------------------------------------------


class TestCurriculumFormat:
    def test_v1_flat_context_composes(self) -> None:
        decision, mission = _compose(_disagreement_twin(), _curriculum_v1())
        assert decision.curriculum_format == CurriculumFormat.V1
        assert mission.curriculum_format == CurriculumFormat.V1
        assert mission.tasks[0].family in ACTION_FAMILY_CATALOGUE

    def test_v2_section_context_composes_same_families(self) -> None:
        decision, mission = _compose(_disagreement_twin(), _curriculum_v2())
        assert decision.curriculum_format == CurriculumFormat.V2
        assert mission.curriculum_format == CurriculumFormat.V2
        assert mission.tasks[0].family == decision.selected.family
        assert mission.tasks[0].family == ActionFamily.REVISE


class TestMissionLineage:
    def test_regeneration_identity_cites_decision(self) -> None:
        decision, mission = _compose(_goals_only_twin())
        regen = mission.regeneration_identity
        assert regen.compose_version == MISSION_INTELLIGENCE_VERSION
        assert ENGINE_VERSION in regen.decision_engine_versions
        assert regen.twin_snapshot_ref == "twin-snap-1"
        assert regen.session_window_id == "session-1"
        if decision.evaluation_id:
            assert decision.evaluation_id in regen.decision_evaluation_ids


# ---------------------------------------------------------------------------
# History / behaviour tension
# ---------------------------------------------------------------------------


class TestHistoryAndBehaviour:
    def test_prior_dismiss_reason_preserved(self) -> None:
        twin = _disagreement_twin()
        history = DecisionHistory.create(
            [
                HistoryEntry.create(
                    ActionFamily.REVISE,
                    curriculum_entity_id="topic-a",
                    outcome=HistoryOutcome.DISMISSED,
                ),
            ]
        )
        decision, mission = _compose(twin, decision_history=history)
        code_ids = {c.value for c in mission.tasks[0].attribution.reason_code_ids}
        assert ReasonCodeId.PRIOR_DISMISS_RESPECTED.value in code_ids

    def test_behaviour_performance_tension_preserved(self) -> None:
        decision, mission = _compose(_behaviour_strong_perf_thin_twin())
        code_ids = {c.value for c in mission.tasks[0].attribution.reason_code_ids}
        assert (
            ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN.value in code_ids
            or ReasonCodeId.THIN_PERFORMANCE_WARRANT.value in code_ids
        )
        assert mission.tasks[0].family == decision.selected.family


# ---------------------------------------------------------------------------
# Framework purity / firewall / ORM boundary
# ---------------------------------------------------------------------------


class TestFrameworkPurity:
    def test_mission_package_has_no_forbidden_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(MISSION_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".")[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".")[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
        assert not violations, violations

    def test_does_not_import_update_strategies_or_planning(self) -> None:
        for path in sorted(MISSION_ROOT.rglob("*.py")):
            src = path.read_text(encoding="utf-8")
            assert "update_pipeline" not in src
            assert "UpdateStrategy" not in src
            assert "KnowledgeUpdateStrategy" not in src
            assert "PlanningService" not in src
            assert "planning_service" not in src
            assert "ReadinessAggregation" not in src

    def test_does_not_import_orm_mission(self) -> None:
        violations: list[str] = []
        for path in sorted(MISSION_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith("app.models"):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.startswith("app.models"):
                        violations.append(f"{path.name}: from {node.module}")
        assert not violations, violations

class TestOrmBoundary:
    def test_domain_mission_is_not_orm_model(self) -> None:
        _, mission = _compose(_goals_only_twin())
        assert mission.__class__.__module__.startswith("app.domain.mission")
        assert "app.models" not in mission.__class__.__module__

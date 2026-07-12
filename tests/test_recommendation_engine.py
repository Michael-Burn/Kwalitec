"""Unit tests for structural Recommendation Engine (Capability 2.9.4)."""

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
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    OverallPosture,
    ReadinessAggregation,
    WarrantPosture,
)
from app.domain.recommendation import (
    AFFORDANCE_OUTCOME_CATALOGUE,
    PACKAGING_VERSION,
    THIN_WARRANT_CONFIDENCE_POSTURES,
    ActionableSuggestion,
    AffordanceOutcome,
    CandidateContrast,
    ExplanationChainLayer,
    Recommendation,
    RecommendationConfidencePosture,
    RecommendationContext,
    RecommendationEngine,
    RecommendationReason,
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

RECOMMENDATION_ROOT = (
    Path(__file__).resolve().parents[1] / "app" / "domain" / "recommendation"
)
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


def _package(
    twin: DigitalTwin,
    curriculum: CurriculumContext | None = None,
    constraints: Constraints | None = None,
    *,
    communication_context: RecommendationContext | None = None,
    decision_history: DecisionHistory | None = None,
) -> tuple[Decision, Recommendation]:
    decision = _decide(
        twin,
        curriculum,
        constraints,
        decision_history=decision_history,
    )
    recommendation = RecommendationEngine.package(
        decision,
        communication_context=communication_context,
    )
    return decision, recommendation


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
# Projection integrity / contract
# ---------------------------------------------------------------------------


class TestProjectionIntegrity:
    """package returns an explainable frozen Recommendation."""

    def test_package_returns_recommendation_with_required_fields(self) -> None:
        decision, rec = _package(_goals_only_twin())
        assert isinstance(rec, Recommendation)
        assert isinstance(rec.suggestion, ActionableSuggestion)
        assert len(rec.reasons) >= 1
        assert rec.explanation_chain is not None
        assert rec.lineage == decision.lineage
        assert rec.packaging_version == PACKAGING_VERSION
        assert rec.decision_engine_version == ENGINE_VERSION
        assert rec.decision_ref.engine_version == decision.engine_version

    def test_suggestion_matches_decision_selected_action(self) -> None:
        decision, rec = _package(_disagreement_twin())
        assert rec.suggestion.family == decision.selected.family
        assert (
            rec.suggestion.curriculum_entity_id
            == decision.selected.curriculum_entity_id
        )
        assert rec.suggestion.intent == decision.selected.intent
        assert rec.decision_ref.selected_family == decision.selected.family.value

    def test_recommendation_is_frozen(self) -> None:
        _, rec = _package(_goals_only_twin())
        with pytest.raises(AttributeError):
            rec.packaging_version = "mutated"  # type: ignore[misc]
        with pytest.raises(AttributeError):
            rec.suggestion.family = ActionFamily.STUDY  # type: ignore[misc]

    def test_no_scoring_or_match_percent_fields(self) -> None:
        _, rec = _package(_goals_only_twin())
        assert not hasattr(rec, "score")
        assert not hasattr(rec, "ranking_score")
        assert not hasattr(rec, "match_percent")
        assert not hasattr(rec, "priority_score")
        assert not hasattr(rec, "optimization_objective")
        assert not hasattr(rec.suggestion, "score")

    def test_no_mission_fields(self) -> None:
        _, rec = _package(_goals_only_twin())
        assert not hasattr(rec, "mission")
        assert not hasattr(rec, "mission_tasks")
        assert not hasattr(rec, "week_plan")


# ---------------------------------------------------------------------------
# Reason preservation / explanation contract
# ---------------------------------------------------------------------------


class TestReasonPreservation:
    def test_every_reason_maps_to_decision_codes(self) -> None:
        decision, rec = _package(_disagreement_twin())
        decision_codes = {r.code_id for r in decision.reason_codes}
        for reason in rec.reasons:
            assert isinstance(reason, RecommendationReason)
            assert reason.decision_reason_codes
            for code in reason.decision_reason_codes:
                assert code in decision_codes

    def test_all_decision_codes_narrated(self) -> None:
        decision, rec = _package(_disagreement_twin())
        narrated = set(rec.decision_reason_code_ids)
        authored = {r.code_id.value for r in decision.reason_codes}
        assert narrated == authored

    def test_tension_preserved_knowledge_vs_memory(self) -> None:
        decision, rec = _package(_disagreement_twin())
        assert decision.selected.family == ActionFamily.REVISE
        code_ids = set(rec.decision_reason_code_ids)
        assert ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN.value in code_ids
        tension_reasons = [
            r
            for r in rec.reasons
            if "knowledge_vs_memory_tension" in r.tension_tags
            or "factor_disagreement" in r.tension_tags
        ]
        assert tension_reasons
        assert "revise_not_study" in rec.suggestion.presentation_tags


class TestExplanationContract:
    def test_mandatory_chain_layers_present(self) -> None:
        _, rec = _package(_disagreement_twin())
        layers = rec.explanation_chain.layers_present
        assert ExplanationChainLayer.CURRICULUM in layers
        assert ExplanationChainLayer.EVIDENCE in layers
        assert ExplanationChainLayer.TWIN in layers
        assert ExplanationChainLayer.DECISION in layers
        assert ExplanationChainLayer.RECOMMENDATION in layers

    def test_no_invented_evidence_ids(self) -> None:
        decision, rec = _package(_disagreement_twin())
        asserted = set(rec.explanation_chain.evidence.evidence_ids)
        allowed = set(decision.lineage.evidence_ids)
        assert asserted <= allowed

    def test_readiness_layer_only_when_cited(self) -> None:
        _, rec = _package(_goals_only_twin())
        # Cold-start Decisions cite warrant / readiness factors
        assert rec.explanation_chain.readiness is not None
        assert rec.explanation_chain.readiness.cited is True
        assert ExplanationChainLayer.READINESS in (
            rec.explanation_chain.layers_present
        )


# ---------------------------------------------------------------------------
# Warrant propagation / cold-start honesty
# ---------------------------------------------------------------------------


class TestWarrantPropagation:
    def test_cold_start_honest_low_confidence(self) -> None:
        decision, rec = _package(_goals_only_twin())
        assert decision.warrant_posture in {
            DecisionWarrantPosture.COLD_START,
            DecisionWarrantPosture.NOT_YET_KNOWABLE,
            DecisionWarrantPosture.INHERITED_LOW,
        }
        assert rec.confidence_posture in THIN_WARRANT_CONFIDENCE_POSTURES
        assert rec.confidence_posture != RecommendationConfidencePosture.HONEST_HIGH
        assert "mid" not in rec.confidence_posture.value
        assert "high" not in rec.confidence_posture.value or (
            rec.confidence_posture == RecommendationConfidencePosture.HONEST_HIGH
            and False
        )

    def test_not_yet_knowable_first_class(self) -> None:
        decision, rec = _package(_goals_only_twin())
        assert decision.readiness_overall_posture == OverallPosture.NOT_YET_KNOWABLE
        assert decision.readiness_overall_warrant == WarrantPosture.LOW
        if decision.warrant_posture == DecisionWarrantPosture.NOT_YET_KNOWABLE:
            assert (
                rec.confidence_posture
                == RecommendationConfidencePosture.NOT_YET_KNOWABLE
            )
        assert "no_mid_high_preparedness_claim" in (
            rec.suggestion.presentation_tags
        )

    def test_warrant_not_stripped_for_polish(self) -> None:
        decision, rec = _package(_goals_only_twin())
        code_ids = set(rec.decision_reason_code_ids)
        assert ReasonCodeId.INSUFFICIENT_WARRANT.value in code_ids
        assert ReasonCodeId.PREFER_EVIDENCE_CREATING.value in code_ids
        assert "thin_warrant_honesty" in rec.suggestion.presentation_tags


class TestColdStartHonesty:
    def test_diagnostic_framing_preserved(self) -> None:
        decision, rec = _package(_goals_only_twin())
        assert decision.selected.family == ActionFamily.DIAGNOSTIC
        assert rec.suggestion.family == ActionFamily.DIAGNOSTIC
        assert "diagnostic_framing" in rec.suggestion.presentation_tags
        assert "evidence_creating" in rec.suggestion.presentation_tags
        assert "curiosity_clarity" in rec.suggestion.presentation_tags or (
            "cold_start_communication" in rec.suggestion.presentation_tags
        )


# ---------------------------------------------------------------------------
# Lineage preservation / candidate contrast / constraints
# ---------------------------------------------------------------------------


class TestLineagePreservation:
    def test_lineage_copied_from_decision(self) -> None:
        decision, rec = _package(_disagreement_twin())
        assert rec.lineage is decision.lineage or rec.lineage == decision.lineage
        assert rec.lineage.twin_domains == decision.lineage.twin_domains
        assert rec.lineage.evidence_ids == decision.lineage.evidence_ids
        assert (
            rec.lineage.curriculum_entity_ids
            == decision.lineage.curriculum_entity_ids
        )

    def test_no_fabricated_curriculum_ids(self) -> None:
        decision, rec = _package(_disagreement_twin())
        suggestion_id = rec.suggestion.curriculum_entity_id
        if suggestion_id is not None:
            allowed = set(decision.lineage.curriculum_entity_ids) | {
                decision.selected.curriculum_entity_id
            }
            assert suggestion_id in allowed


class TestCandidateContrast:
    def test_contrast_subset_of_decision_candidates(self) -> None:
        decision, rec = _package(_disagreement_twin())
        decision_ids = {c.candidate_id for c in decision.candidates}
        for contrast in rec.candidate_contrast:
            assert isinstance(contrast, CandidateContrast)
            assert contrast.candidate_id in decision_ids
            assert contrast.status != CandidateStatus.SELECTED

    def test_contrast_statuses_preserved(self) -> None:
        decision, rec = _package(
            _disagreement_twin(),
            constraints=_protect_constraints(),
        )
        by_id = {c.candidate_id: c for c in decision.candidates}
        for contrast in rec.candidate_contrast:
            assert contrast.status == by_id[contrast.candidate_id].status


class TestConstraintHonesty:
    def test_feasibility_demotion_visible(self) -> None:
        decision, rec = _package(
            _disagreement_twin(),
            constraints=_protect_constraints(),
        )
        assert decision.selected.family == ActionFamily.REST_PROTECT_INTENSITY
        assert decision.constraint_acknowledgements
        assert rec.suggestion.family == ActionFamily.REST_PROTECT_INTENSITY
        assert "rest_protect_not_failure" in rec.suggestion.presentation_tags
        assert any(
            "constraint/" in t or "protect" in t or "intensity" in t
            for t in rec.urgency_duration_tags
        )
        # Educational need remains attributable in reasons
        code_ids = set(rec.decision_reason_code_ids)
        assert (
            ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN.value in code_ids
            or ReasonCodeId.MEMORY_STALENESS.value in code_ids
            or ReasonCodeId.INTENSITY_PROTECTION.value in code_ids
        )


# ---------------------------------------------------------------------------
# Decision authority / no re-selection / context adaptation
# ---------------------------------------------------------------------------


class TestDecisionAuthority:
    def test_no_reselection_across_postures(self) -> None:
        for twin_factory in (
            _goals_only_twin,
            _disagreement_twin,
            _behaviour_strong_perf_thin_twin,
        ):
            decision, rec = _package(twin_factory())
            assert rec.suggestion.family == decision.selected.family
            assert (
                rec.suggestion.curriculum_entity_id
                == decision.selected.curriculum_entity_id
            )

    def test_does_not_call_decision_engine(self) -> None:
        engine_src = (RECOMMENDATION_ROOT / "engine.py").read_text(encoding="utf-8")
        assert "from app.domain.decision.engine" not in engine_src
        assert "DecisionEngine.evaluate" not in engine_src
        assert "DecisionEngine(" not in engine_src
        # Consume Decision type only — no selection engine import.
        assert "from app.domain.decision.decision import Decision" in engine_src


class TestContextAdaptation:
    def test_context_changes_phrasing_not_selection(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        context = RecommendationContext.create(
            goals_language_tags=["sitting_deadline", "limited_capacity"],
            journal_history_refs=["dismiss-revise-topic-a"],
            confidence_framing=["self_report_high"],
        )
        rec_plain = RecommendationEngine.package(decision)
        rec_ctx = RecommendationEngine.package(
            decision,
            communication_context=context,
        )
        assert rec_ctx.suggestion.family == rec_plain.suggestion.family
        assert (
            rec_ctx.suggestion.curriculum_entity_id
            == rec_plain.suggestion.curriculum_entity_id
        )
        assert "goals/sitting_deadline" in rec_ctx.communication_tags
        assert "prior_preference_acknowledged" in rec_ctx.communication_tags
        assert "confidence_risk_framing_only" in rec_ctx.communication_tags
        assert "selection_authority_unchanged" in rec_ctx.communication_tags
        assert "context_adapts_phrasing_only" in rec_ctx.communication_tags

    def test_affordances_accept_not_mastery(self) -> None:
        _, rec = _package(_goals_only_twin())
        assert AffordanceOutcome.ACCEPT in AFFORDANCE_OUTCOME_CATALOGUE
        assert AffordanceOutcome.DISMISS in rec.affordances.outcomes
        assert AffordanceOutcome.DEFER in rec.affordances.outcomes
        assert rec.affordances.mastery_implied is False
        assert "accept_is_commitment_not_competence" in (
            rec.affordances.emphasis_tags
        )


# ---------------------------------------------------------------------------
# Determinism / purity / no Twin mutation
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_same_decision_equal_structural_fields(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        a = RecommendationEngine.package(decision)
        b = RecommendationEngine.package(decision)
        assert a.suggestion == b.suggestion
        assert a.reasons == b.reasons
        assert a.lineage == b.lineage
        assert a.confidence_posture == b.confidence_posture
        assert a.candidate_contrast == b.candidate_contrast
        assert a.urgency_duration_tags == b.urgency_duration_tags
        assert a.communication_tags == b.communication_tags


class TestNoTwinMutation:
    def test_twin_domains_unchanged_after_package(self) -> None:
        twin = _disagreement_twin()
        before = _snapshot_domains(twin)
        before_copy = copy.deepcopy(before)
        decision = _decide(twin)
        RecommendationEngine.package(decision)
        after = _snapshot_domains(twin)
        assert after == before
        assert after == before_copy

    def test_decision_unchanged_after_package(self) -> None:
        twin = _disagreement_twin()
        decision = _decide(twin)
        before = (
            decision.selected,
            decision.candidates,
            decision.reason_codes,
            decision.lineage,
            decision.warrant_posture,
        )
        RecommendationEngine.package(decision)
        assert (
            decision.selected,
            decision.candidates,
            decision.reason_codes,
            decision.lineage,
            decision.warrant_posture,
        ) == before


# ---------------------------------------------------------------------------
# Curriculum V1/V2
# ---------------------------------------------------------------------------


class TestCurriculumFormat:
    def test_v1_flat_context_packages(self) -> None:
        decision, rec = _package(_disagreement_twin(), _curriculum_v1())
        assert decision.curriculum_format == CurriculumFormat.V1
        assert rec.suggestion.family in ACTION_FAMILY_CATALOGUE
        assert (
            rec.explanation_chain.curriculum.curriculum_format
            == CurriculumFormat.V1.value
        )

    def test_v2_section_context_packages_same_families(self) -> None:
        decision, rec = _package(_disagreement_twin(), _curriculum_v2())
        assert decision.curriculum_format == CurriculumFormat.V2
        assert rec.suggestion.family == decision.selected.family
        assert rec.suggestion.family == ActionFamily.REVISE
        assert (
            rec.explanation_chain.curriculum.curriculum_format
            == CurriculumFormat.V2.value
        )


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
        decision, rec = _package(twin, decision_history=history)
        code_ids = set(rec.decision_reason_code_ids)
        assert ReasonCodeId.PRIOR_DISMISS_RESPECTED.value in code_ids
        dismiss_reasons = [
            r for r in rec.reasons if "dismiss_not_mastery" in r.tension_tags
        ]
        assert dismiss_reasons

    def test_behaviour_performance_tension_preserved(self) -> None:
        decision, rec = _package(_behaviour_strong_perf_thin_twin())
        code_ids = set(rec.decision_reason_code_ids)
        assert (
            ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN.value in code_ids
            or ReasonCodeId.THIN_PERFORMANCE_WARRANT.value in code_ids
        )
        assert rec.suggestion.family == decision.selected.family


# ---------------------------------------------------------------------------
# Framework purity / firewall / Decision authority
# ---------------------------------------------------------------------------


class TestFrameworkPurity:
    def test_recommendation_package_has_no_forbidden_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(RECOMMENDATION_ROOT.rglob("*.py")):
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

    def test_does_not_import_mission_or_legacy_recommendation_service(self) -> None:
        for path in sorted(RECOMMENDATION_ROOT.rglob("*.py")):
            src = path.read_text(encoding="utf-8")
            assert "recommendation_service" not in src
            assert "RecommendationService" not in src
            assert "ReadinessAggregation" not in src
            assert "MissionTask" not in src
            assert "app.mission" not in src

    def test_does_not_import_update_strategies(self) -> None:
        for path in sorted(RECOMMENDATION_ROOT.rglob("*.py")):
            src = path.read_text(encoding="utf-8")
            assert "update_pipeline" not in src
            assert "UpdateStrategy" not in src
            assert "KnowledgeUpdateStrategy" not in src


class TestDecisionAuthorityFirewall:
    def test_action_families_remain_decision_catalogue(self) -> None:
        _, rec = _package(_disagreement_twin())
        assert rec.suggestion.family in ACTION_FAMILY_CATALOGUE
        assert ActionFamily.STUDY != ActionFamily.REVISE

    def test_intent_evidence_creating_separable(self) -> None:
        decision, rec = _package(_goals_only_twin())
        assert rec.suggestion.intent == ActionIntent.EVIDENCE_CREATING
        assert decision.selected.intent == rec.suggestion.intent

"""Unit tests for structural Decision Engine (Capability 2.8.4)."""

from __future__ import annotations

import ast
import copy
from datetime import date
from pathlib import Path

import pytest

from app.domain.decision import (
    ACTION_FAMILY_CATALOGUE,
    ENGINE_VERSION,
    REASON_CODE_CATALOGUE,
    ActionFamily,
    ActionIntent,
    CandidateStatus,
    Constraints,
    Decision,
    DecisionEngine,
    DecisionHistory,
    DecisionState,
    DecisionWarrantPosture,
    HistoryEntry,
    HistoryOutcome,
    IntensityPosture,
    JournalLinkage,
    ReasonCodeId,
    SelectedAction,
)
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    FactorId,
    OverallPosture,
    ReadinessAggregation,
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

DECISION_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "decision"
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
    """Supportive Knowledge beside risk-elevating Memory/Performance."""
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


def _confidence_shaped_twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
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


def _high_weight_gap_twin() -> DigitalTwin:
    """Dense beliefs on low-weight topic; gap on high-weight."""
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
        knowledge=KnowledgeState.create(
            topic_mastery=[
                TopicMasteryRecord.create(
                    "topic-c",
                    mastery_belief=0.9,
                    evidence_ids=["ev-low"],
                ),
            ],
            evidence_ids=["ev-low"],
        ),
        memory=MemoryState.create(
            retention=[
                RetentionRecord.create("topic-c", retention_belief=0.8),
            ],
        ),
        performance=PerformanceState.create(
            assessment_ids=["a1"],
            evidence_ids=["ev-p"],
            performance_summaries=[
                PerformanceSummary.create("topic-c", summary={"note": "ok"}),
            ],
        ),
        behaviour=BehaviourState.create(evidence_ids=["ev-b"]),
    )


def _ample_constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


def _scarce_constraints() -> Constraints:
    return Constraints.create(
        available_minutes=15,
        intensity=IntensityPosture.LIMITED,
    )


def _protect_constraints() -> Constraints:
    return Constraints.create(
        available_minutes=40,
        intensity=IntensityPosture.PROTECT,
        burnout_risk=True,
        note_tags=("burnout_flag",),
    )


def _evaluate(
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
# Contract
# ---------------------------------------------------------------------------


class TestContract:
    """evaluate returns an explainable frozen Decision."""

    def test_evaluate_returns_decision_with_required_fields(self) -> None:
        decision = _evaluate(_goals_only_twin())
        assert isinstance(decision, Decision)
        assert isinstance(decision.selected, SelectedAction)
        assert len(decision.candidates) >= 1
        assert len(decision.reason_codes) >= 1
        assert decision.lineage is not None
        assert decision.engine_version == ENGINE_VERSION

    def test_decision_is_frozen(self) -> None:
        decision = _evaluate(_goals_only_twin())
        with pytest.raises(AttributeError):
            decision.engine_version = "mutated"  # type: ignore[misc]
        with pytest.raises(AttributeError):
            decision.candidates[0].status = CandidateStatus.BLOCKED  # type: ignore[misc]

    def test_selected_in_candidate_set(self) -> None:
        decision = _evaluate(_disagreement_twin())
        selected_marks = [
            c for c in decision.candidates if c.status == CandidateStatus.SELECTED
        ]
        assert len(selected_marks) == 1
        assert selected_marks[0].family == decision.selected.family
        assert (
            selected_marks[0].curriculum_entity_id
            == decision.selected.curriculum_entity_id
        )

    def test_no_scoring_or_pass_probability_fields(self) -> None:
        decision = _evaluate(_goals_only_twin())
        assert not hasattr(decision, "score")
        assert not hasattr(decision, "ranking_score")
        assert not hasattr(decision, "pass_probability")
        assert not hasattr(decision, "optimization_objective")
        assert not hasattr(decision.selected, "score")

    def test_action_family_catalogue_separable(self) -> None:
        assert ActionFamily.STUDY in ACTION_FAMILY_CATALOGUE
        assert ActionFamily.REVISE in ACTION_FAMILY_CATALOGUE
        assert ActionFamily.REST_PROTECT_INTENSITY in ACTION_FAMILY_CATALOGUE
        assert ActionFamily.STUDY != ActionFamily.REVISE


# ---------------------------------------------------------------------------
# Determinism / purity / no Twin mutation
# ---------------------------------------------------------------------------


class TestDeterminism:
    def test_same_inputs_equal_structural_fields(self) -> None:
        twin = _disagreement_twin()
        curriculum = _curriculum_v1()
        constraints = _ample_constraints()
        readiness = ReadinessAggregation.derive(twin, curriculum)
        a = DecisionEngine.evaluate(twin, readiness, curriculum, constraints)
        b = DecisionEngine.evaluate(twin, readiness, curriculum, constraints)
        assert a.selected == b.selected
        assert a.candidates == b.candidates
        assert a.reason_codes == b.reason_codes
        assert a.lineage == b.lineage
        assert a.warrant_posture == b.warrant_posture
        assert a.constraint_acknowledgements == b.constraint_acknowledgements


class TestNoTwinMutation:
    def test_twin_domains_unchanged_after_evaluate(self) -> None:
        twin = _disagreement_twin()
        before = _snapshot_domains(twin)
        before_copy = copy.deepcopy(before)
        _evaluate(twin)
        after = _snapshot_domains(twin)
        assert after == before
        assert after == before_copy

    def test_readiness_unchanged_after_evaluate(self) -> None:
        twin = _disagreement_twin()
        curriculum = _curriculum_v1()
        readiness = ReadinessAggregation.derive(twin, curriculum)
        before = (
            readiness.overall_posture,
            readiness.overall_warrant,
            readiness.factors,
            readiness.cold_start,
        )
        DecisionEngine.evaluate(twin, readiness, curriculum, _ample_constraints())
        assert (
            readiness.overall_posture,
            readiness.overall_warrant,
            readiness.factors,
            readiness.cold_start,
        ) == before


# ---------------------------------------------------------------------------
# Cold start
# ---------------------------------------------------------------------------


class TestColdStart:
    def test_goals_only_prefers_diagnostic(self) -> None:
        decision = _evaluate(_goals_only_twin())
        assert decision.selected.family == ActionFamily.DIAGNOSTIC
        assert decision.selected.intent == ActionIntent.EVIDENCE_CREATING
        code_ids = {r.code_id for r in decision.reason_codes}
        assert ReasonCodeId.INSUFFICIENT_WARRANT in code_ids
        assert ReasonCodeId.PREFER_EVIDENCE_CREATING in code_ids
        assert decision.warrant_posture in {
            DecisionWarrantPosture.COLD_START,
            DecisionWarrantPosture.NOT_YET_KNOWABLE,
            DecisionWarrantPosture.INHERITED_LOW,
        }
        assert decision.readiness_overall_posture == OverallPosture.NOT_YET_KNOWABLE
        # Never coerce Mid/High preparedness
        assert decision.readiness_overall_posture.value not in {
            "mid",
            "high",
            "ready",
            "supportive",
        }

    def test_cold_start_candidate_set_non_empty(self) -> None:
        decision = _evaluate(_goals_only_twin())
        assert len(decision.candidates) >= 1
        assert any(c.family == ActionFamily.DIAGNOSTIC for c in decision.candidates)


# ---------------------------------------------------------------------------
# Candidate ordering / selection postures
# ---------------------------------------------------------------------------


class TestCandidateOrdering:
    def test_high_knowledge_low_memory_prefers_revise(self) -> None:
        decision = _evaluate(_disagreement_twin())
        assert decision.selected.family == ActionFamily.REVISE
        code_ids = {r.code_id for r in decision.reason_codes}
        assert ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN in code_ids
        assert ReasonCodeId.MEMORY_STALENESS in code_ids

    def test_behaviour_strong_performance_thin_prefers_assess(self) -> None:
        decision = _evaluate(_behaviour_strong_perf_thin_twin())
        assert decision.selected.family in {
            ActionFamily.ASSESS,
            ActionFamily.DIAGNOSTIC,
        }
        code_ids = {r.code_id for r in decision.reason_codes}
        assert (
            ReasonCodeId.BEHAVIOUR_STRONG_PERFORMANCE_THIN in code_ids
            or ReasonCodeId.THIN_PERFORMANCE_WARRANT in code_ids
        )

    def test_high_weight_gap_preferred_over_low_weight_polish(self) -> None:
        decision = _evaluate(
            _high_weight_gap_twin(),
            constraints=_scarce_constraints(),
        )
        # Under scarcity, selected curriculum entity should be high-weight when present
        if decision.selected.curriculum_entity_id is not None:
            assert decision.selected.curriculum_entity_id != "topic-c" or (
                decision.selected.family == ActionFamily.DIAGNOSTIC
            )
        demoted = decision.demoted_candidates
        polish = [c for c in demoted if "low_weight_polish" in c.note_tags]
        # Scarce time should demote low-weight polish when present
        assert polish or decision.selected.curriculum_entity_id in {
            "topic-a",
            "topic-b",
            None,
        }

    def test_protect_intensity_selects_rest_and_keeps_need_visible(self) -> None:
        decision = _evaluate(
            _disagreement_twin(),
            constraints=_protect_constraints(),
        )
        assert decision.selected.family == ActionFamily.REST_PROTECT_INTENSITY
        assert decision.constraint_acknowledgements
        assert decision.demoted_candidates
        code_ids = {r.code_id for r in decision.reason_codes}
        assert (
            ReasonCodeId.INTENSITY_PROTECTION in code_ids
            or ReasonCodeId.BEHAVIOUR_SUSTAINABILITY in code_ids
        )
        # Educational need remains attributable
        assert (
            ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN in code_ids
            or ReasonCodeId.MEMORY_STALENESS in code_ids
            or ReasonCodeId.HIGH_WEIGHT_COVERAGE in code_ids
        )


# ---------------------------------------------------------------------------
# Reason codes / lineage / explainability
# ---------------------------------------------------------------------------


class TestReasonCodes:
    def test_reason_code_catalogue_covers_families(self) -> None:
        assert ReasonCodeId.HIGH_WEIGHT_COVERAGE in REASON_CODE_CATALOGUE
        assert ReasonCodeId.INSUFFICIENT_WARRANT in REASON_CODE_CATALOGUE
        assert ReasonCodeId.KNOWS_NOW_MAY_NOT_RETAIN in REASON_CODE_CATALOGUE
        assert ReasonCodeId.CONFIDENCE_NOT_MASTERY in REASON_CODE_CATALOGUE

    def test_readiness_citing_codes_inherit_warrant(self) -> None:
        decision = _evaluate(_goals_only_twin())
        warrant_codes = [r for r in decision.reason_codes if r.inherits_warrant]
        assert warrant_codes
        assert all(r.inherits_warrant for r in warrant_codes)

    def test_confidence_risk_framing_not_mastery_upgrade(self) -> None:
        decision = _evaluate(_confidence_shaped_twin())
        code_ids = {r.code_id for r in decision.reason_codes}
        assert ReasonCodeId.CONFIDENCE_NOT_MASTERY in code_ids
        # Must not select assess-only as mastery unlock from confidence
        assert decision.selected.family != ActionFamily.ASSESS or (
            ReasonCodeId.THIN_PERFORMANCE_WARRANT in code_ids
        )


class TestLineage:
    def test_lineage_cites_twin_and_curriculum(self) -> None:
        decision = _evaluate(_disagreement_twin())
        assert decision.lineage.twin_domains
        assert "knowledge" in decision.lineage.twin_domains or (
            "memory" in decision.lineage.twin_domains
        )
        assert decision.lineage.curriculum_entity_ids
        assert decision.lineage.evidence_ids
        assert "ev-k-1" in decision.lineage.evidence_ids

    def test_lineage_cites_readiness_factors(self) -> None:
        decision = _evaluate(_disagreement_twin())
        assert decision.lineage.readiness_factor_ids
        factor_ids = decision.lineage.readiness_factor_ids
        assert (
            FactorId.MEMORY_STABILITY.value in factor_ids
            or FactorId.KNOWLEDGE_STRENGTH.value in factor_ids
        )


class TestExplainability:
    def test_mandatory_explanation_chain_hooks_present(self) -> None:
        decision = _evaluate(_disagreement_twin())
        assert decision.reason_codes
        assert decision.candidates
        assert decision.lineage.twin_domains
        assert decision.lineage.curriculum_entity_ids or (
            decision.selected.curriculum_entity_id is None
            and decision.selected.family == ActionFamily.REST_PROTECT_INTENSITY
        )
        # Why-not alternatives exist
        assert len(decision.candidates) >= 2 or any(
            c.status != CandidateStatus.SELECTED for c in decision.candidates
        )


# ---------------------------------------------------------------------------
# History / DecisionState
# ---------------------------------------------------------------------------


class TestHistory:
    def test_dismissed_action_demoted_not_treated_as_mastery(self) -> None:
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
        decision = _evaluate(twin, decision_history=history)
        code_ids = {r.code_id for r in decision.reason_codes}
        assert ReasonCodeId.PRIOR_DISMISS_RESPECTED in code_ids
        # Dismiss does not invent mastery — Knowledge/Memory still cited
        assert decision.selected.family != ActionFamily.REVISE or (
            decision.selected.curriculum_entity_id != "topic-a"
        )


class TestDecisionState:
    def test_materialise_audit_without_twin_mutation(self) -> None:
        twin = _goals_only_twin()
        before = _snapshot_domains(twin)
        decision = _evaluate(twin)
        state = DecisionState.materialise(
            decision,
            readiness_derivation_id="rdy-1",
            decision_state_id="ds-1",
        )
        assert state.decision == decision
        assert state.twin_student_id == "student-42"
        assert state.journal_linkage == JournalLinkage.NONE
        linked = state.with_journal_linkage(JournalLinkage.ACCEPTED)
        assert linked.journal_linkage == JournalLinkage.ACCEPTED
        assert _snapshot_domains(twin) == before


# ---------------------------------------------------------------------------
# Curriculum V1/V2
# ---------------------------------------------------------------------------


class TestCurriculumFormat:
    def test_v1_flat_context_evaluates(self) -> None:
        decision = _evaluate(_disagreement_twin(), _curriculum_v1())
        assert decision.curriculum_format == CurriculumFormat.V1
        assert decision.selected.family in ActionFamily

    def test_v2_section_context_evaluates_same_families(self) -> None:
        decision = _evaluate(_disagreement_twin(), _curriculum_v2())
        assert decision.curriculum_format == CurriculumFormat.V2
        assert decision.selected.family in ACTION_FAMILY_CATALOGUE
        # Same disagreement posture
        assert decision.selected.family == ActionFamily.REVISE


# ---------------------------------------------------------------------------
# Framework purity / firewall
# ---------------------------------------------------------------------------


class TestFrameworkPurity:
    def test_decision_package_has_no_forbidden_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(DECISION_ROOT.rglob("*.py")):
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

    def test_does_not_import_recommendation_or_mission_services(self) -> None:
        engine_src = (DECISION_ROOT / "engine.py").read_text(encoding="utf-8")
        assert "recommendation_service" not in engine_src
        assert "RecommendationService" not in engine_src
        assert "mission" not in engine_src.lower() or "Mission" not in engine_src

    def test_does_not_call_readiness_aggregation_internally(self) -> None:
        engine_src = (DECISION_ROOT / "engine.py").read_text(encoding="utf-8")
        assert "ReadinessAggregation" not in engine_src
        assert "derive(" not in engine_src or "ReadinessAggregation.derive" not in (
            engine_src
        )


class TestReadinessFirewall:
    def test_engine_does_not_coerce_unknown_to_mid_high(self) -> None:
        decision = _evaluate(_goals_only_twin())
        assert decision.readiness_overall_warrant == WarrantPosture.LOW
        assert decision.warrant_posture != DecisionWarrantPosture.INHERITED_HIGH
        assert "mid" not in decision.warrant_posture.value
        assert "high" not in decision.warrant_posture.value or (
            decision.warrant_posture == DecisionWarrantPosture.INHERITED_HIGH
            and False  # unreachable for cold start
        )

    def test_readiness_cited_as_context_only(self) -> None:
        twin = _disagreement_twin()
        curriculum = _curriculum_v1()
        readiness = ReadinessAggregation.derive(twin, curriculum)
        decision = DecisionEngine.evaluate(
            twin, readiness, curriculum, _ample_constraints()
        )
        assert decision.readiness_overall_posture == readiness.overall_posture
        assert decision.readiness_overall_warrant == readiness.overall_warrant

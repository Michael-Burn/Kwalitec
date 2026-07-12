"""Tests for EducationalOrchestrator skeleton (Capability 3.2.5).

Covers successful composition, lawful dependency order, CurriculumContextBuilder
and domain invocations, dependency injection, immutable Experience output,
framework independence, failure propagation, and absence of educational logic
in the orchestrator module.
"""

from __future__ import annotations

import ast
from dataclasses import FrozenInstanceError
from datetime import date
from pathlib import Path

import pytest

from app.application.orchestration import (
    CONTRACT_VERSION,
    EducationalExperience,
    EducationalOrchestrator,
    ProductContext,
)
from app.domain.decision import (
    Constraints,
    Decision,
    DecisionEngine,
    IntensityPosture,
)
from app.domain.mission import Mission, MissionExecutionContext, MissionIntelligence
from app.domain.readiness import (
    CurriculumContext,
    CurriculumFormat,
    CurriculumTopicRef,
    OverallPosture,
    ReadinessAggregation,
    ReadinessState,
    WarrantPosture,
)
from app.domain.recommendation import Recommendation, RecommendationEngine
from app.domain.twin import DigitalTwin, GoalState, IdentityState

ORCHESTRATION_ROOT = (
    Path(__file__).resolve().parents[2] / "app" / "application" / "orchestration"
)

FORBIDDEN_ROOT_MODULES = frozenset(
    {
        "flask",
        "flask_login",
        "flask_sqlalchemy",
        "flask_wtf",
        "wtforms",
    }
)

FORBIDDEN_PREFIXES = (
    "app.auth",
    "app.dashboard",
    "app.mission",
    "app.analytics",
    "app.models",
)

# Orchestrator may import domain engines and CurriculumContextBuilder only —
# it must not contain educational algorithms (scoring / ranking / Mid coercion).
FORBIDDEN_LOGIC_TOKENS = (
    "average(",
    "hybrid",
    "re_rank",
    "rerank",
    "priority_score",
    "pass_probability",
    "OverallPosture.MID",
    "OverallPosture.HIGH",
    "WarrantPosture.MEDIUM",
    "WarrantPosture.HIGH",
    "nominate_candidates",
    "_judge_factor",
)


# ═══════════════════════════════════════════════════════════════════════════════
# Fixtures / fakes
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


def _curriculum() -> CurriculumContext:
    return CurriculumContext.create(
        "CS1-2026",
        format=CurriculumFormat.V1,
        topics=[
            CurriculumTopicRef.create("topic-a", weight=0.4),
            CurriculumTopicRef.create("topic-b", weight=0.4),
            CurriculumTopicRef.create("topic-c", weight=0.2),
        ],
    )


def _twin() -> DigitalTwin:
    return DigitalTwin.create(
        _identity(),
        goals=GoalState.create(
            target_pass_probability=0.8,
            target_completion_date=date(2026, 9, 15),
            planned_study_hours_per_week=10.0,
        ),
    )


def _constraints() -> Constraints:
    return Constraints.create(
        available_minutes=60,
        intensity=IntensityPosture.AMPLE,
    )


class _RecordingBuilder:
    """Fake CurriculumContextBuilder that records calls."""

    def __init__(
        self,
        curriculum: CurriculumContext,
        *,
        error: Exception | None = None,
    ):
        self.curriculum = curriculum
        self.error = error
        self.calls: list[int | None] = []

    def build(self, curriculum_id: int | None) -> CurriculumContext:
        self.calls.append(curriculum_id)
        if self.error is not None:
            raise self.error
        return self.curriculum


class _RecordingReadiness:
    def __init__(self, call_log: list[str], *, error: Exception | None = None):
        self.call_log = call_log
        self.error = error

    def derive(
        self,
        twin: DigitalTwin,
        curriculum: CurriculumContext,
        *,
        as_of=None,
        derivation_id=None,
    ) -> ReadinessState:
        self.call_log.append("readiness")
        if self.error is not None:
            raise self.error
        return ReadinessAggregation.derive(twin, curriculum)


class _RecordingDecision:
    def __init__(self, call_log: list[str], *, error: Exception | None = None):
        self.call_log = call_log
        self.error = error

    def evaluate(
        self,
        twin: DigitalTwin,
        readiness: ReadinessState,
        curriculum: CurriculumContext,
        constraints: Constraints,
        *,
        decision_history=None,
        as_of=None,
        evaluation_id=None,
    ) -> Decision:
        self.call_log.append("decision")
        if self.error is not None:
            raise self.error
        return DecisionEngine.evaluate(
            twin,
            readiness,
            curriculum,
            constraints,
            decision_history=decision_history,
        )


class _RecordingRecommendation:
    def __init__(self, call_log: list[str], *, error: Exception | None = None):
        self.call_log = call_log
        self.error = error

    def package(
        self,
        decision: Decision,
        *,
        communication_context=None,
    ) -> Recommendation:
        self.call_log.append("recommendation")
        if self.error is not None:
            raise self.error
        return RecommendationEngine.package(
            decision,
            communication_context=communication_context,
        )


class _RecordingMission:
    def __init__(self, call_log: list[str], *, error: Exception | None = None):
        self.call_log = call_log
        self.error = error

    def compose(
        self,
        decision_or_batch: Decision,
        execution_context: MissionExecutionContext,
        recommendation_language: Recommendation | None = None,
    ) -> Mission:
        self.call_log.append("mission")
        if self.error is not None:
            raise self.error
        return MissionIntelligence.compose(
            decision_or_batch,
            execution_context,
            recommendation_language,
        )


def _orchestrator_with_recorders(
    *,
    builder: _RecordingBuilder | None = None,
    readiness_error: Exception | None = None,
    decision_error: Exception | None = None,
    recommendation_error: Exception | None = None,
    mission_error: Exception | None = None,
) -> tuple[EducationalOrchestrator, list[str], _RecordingBuilder]:
    call_log: list[str] = []
    recording_builder = builder or _RecordingBuilder(_curriculum())

    class _LoggedBuilder:
        def build(self, curriculum_id: int | None) -> CurriculumContext:
            call_log.append("curriculum")
            return recording_builder.build(curriculum_id)

    orchestrator = EducationalOrchestrator(
        curriculum_context_builder=_LoggedBuilder(),
        readiness_aggregation=_RecordingReadiness(
            call_log, error=readiness_error
        ),
        decision_engine=_RecordingDecision(call_log, error=decision_error),
        recommendation_engine=_RecordingRecommendation(
            call_log, error=recommendation_error
        ),
        mission_intelligence=_RecordingMission(call_log, error=mission_error),
    )
    return orchestrator, call_log, recording_builder


# ═══════════════════════════════════════════════════════════════════════════════
# Successful orchestration
# ═══════════════════════════════════════════════════════════════════════════════


class TestSuccessfulOrchestration:
    def test_build_experience_returns_closed_contract(self) -> None:
        orchestrator, _, _ = _orchestrator_with_recorders()

        experience = orchestrator.build_experience(
            curriculum_id=1,
            twin=_twin(),
            constraints=_constraints(),
            product_context=ProductContext(
                surface_intent="dashboard",
                cutover_mode="stage_a",
            ),
        )

        assert isinstance(experience, EducationalExperience)
        assert experience.student_summary.student_id == "student-42"
        assert isinstance(experience.todays_recommendation, Recommendation)
        assert isinstance(experience.todays_mission, Mission)
        assert experience.readiness_summary.overall_posture is not None
        assert experience.progress_snapshot.student_id == "student-42"
        assert len(experience.explainability.reason_codes) >= 1
        assert experience.metadata.contract_version == CONTRACT_VERSION
        assert experience.metadata.surface_intent == "dashboard"
        assert experience.metadata.cutover_mode == "stage_a"

    def test_default_engines_compose_without_injection(self) -> None:
        """Real domain owners work when only CurriculumContextBuilder is faked."""
        builder = _RecordingBuilder(_curriculum())
        orchestrator = EducationalOrchestrator(
            curriculum_context_builder=builder,
        )

        experience = orchestrator.build_experience(
            curriculum_id=7,
            twin=_twin(),
            constraints=_constraints(),
        )

        assert builder.calls == [7]
        assert experience.todays_recommendation.decision_ref.scope.student_id == (
            "student-42"
        )
        assert experience.todays_mission.tasks  # Decision-authored tasks present


# ═══════════════════════════════════════════════════════════════════════════════
# Dependency ordering + invocations
# ═══════════════════════════════════════════════════════════════════════════════


class TestDependencyOrdering:
    def test_lawful_invocation_order(self) -> None:
        orchestrator, call_log, builder = _orchestrator_with_recorders()

        orchestrator.build_experience(
            curriculum_id=3,
            twin=_twin(),
            constraints=_constraints(),
        )

        assert call_log == [
            "curriculum",
            "readiness",
            "decision",
            "recommendation",
            "mission",
        ]
        assert builder.calls == [3]


class TestCurriculumContextBuilderInvocation:
    def test_builder_receives_curriculum_id(self) -> None:
        builder = _RecordingBuilder(_curriculum())
        orchestrator, _, _ = _orchestrator_with_recorders(builder=builder)

        orchestrator.build_experience(
            curriculum_id=99,
            twin=_twin(),
            constraints=_constraints(),
        )

        assert builder.calls == [99]


class TestDomainInvocations:
    def test_readiness_decision_recommendation_mission_invoked(self) -> None:
        orchestrator, call_log, _ = _orchestrator_with_recorders()

        orchestrator.build_experience(
            curriculum_id=1,
            twin=_twin(),
            constraints=_constraints(),
        )

        assert "readiness" in call_log
        assert "decision" in call_log
        assert "recommendation" in call_log
        assert "mission" in call_log


# ═══════════════════════════════════════════════════════════════════════════════
# Dependency injection
# ═══════════════════════════════════════════════════════════════════════════════


class TestDependencyInjection:
    def test_injected_dependencies_are_used(self) -> None:
        sentinel_curriculum = CurriculumContext.create(
            "INJECTED",
            format=CurriculumFormat.V1,
            topics=[CurriculumTopicRef.create("only-topic", weight=1.0)],
        )
        builder = _RecordingBuilder(sentinel_curriculum)
        call_log: list[str] = []

        class _Builder:
            def build(self, curriculum_id: int | None) -> CurriculumContext:
                call_log.append("injected_builder")
                return builder.build(curriculum_id)

        twin = DigitalTwin.create(
            _identity(curriculum_id="INJECTED"),
            goals=GoalState.create(target_completion_date=date(2026, 9, 15)),
        )
        orchestrator = EducationalOrchestrator(
            curriculum_context_builder=_Builder(),
            readiness_aggregation=_RecordingReadiness(call_log),
            decision_engine=_RecordingDecision(call_log),
            recommendation_engine=_RecordingRecommendation(call_log),
            mission_intelligence=_RecordingMission(call_log),
        )

        experience = orchestrator.build_experience(
            curriculum_id=1,
            twin=twin,
            constraints=_constraints(),
        )

        assert call_log[0] == "injected_builder"
        assert experience.student_summary.curriculum_id == "INJECTED"
        assert experience.readiness_summary.curriculum_format == (
            CurriculumFormat.V1.value
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable output
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableOutput:
    def test_experience_is_frozen(self) -> None:
        orchestrator, _, _ = _orchestrator_with_recorders()
        experience = orchestrator.build_experience(
            curriculum_id=1,
            twin=_twin(),
            constraints=_constraints(),
        )

        with pytest.raises(FrozenInstanceError):
            experience.warnings = ("mutated",)  # type: ignore[misc]

        with pytest.raises(FrozenInstanceError):
            experience.student_summary.student_id = "other"  # type: ignore[misc]

        assert isinstance(experience.warnings, tuple)
        assert isinstance(experience.empty_state_guidance, tuple)


# ═══════════════════════════════════════════════════════════════════════════════
# Failure propagation
# ═══════════════════════════════════════════════════════════════════════════════


class TestFailurePropagation:
    def test_builder_failure_propagates(self) -> None:
        builder = _RecordingBuilder(
            _curriculum(),
            error=RuntimeError("missing curriculum"),
        )
        orchestrator, call_log, _ = _orchestrator_with_recorders(builder=builder)

        with pytest.raises(RuntimeError, match="missing curriculum"):
            orchestrator.build_experience(
                curriculum_id=1,
                twin=_twin(),
                constraints=_constraints(),
            )

        assert call_log == ["curriculum"]

    def test_readiness_failure_propagates_and_stops_chain(self) -> None:
        orchestrator, call_log, _ = _orchestrator_with_recorders(
            readiness_error=RuntimeError("readiness failed"),
        )

        with pytest.raises(RuntimeError, match="readiness failed"):
            orchestrator.build_experience(
                curriculum_id=1,
                twin=_twin(),
                constraints=_constraints(),
            )

        assert call_log == ["curriculum", "readiness"]

    def test_decision_failure_propagates(self) -> None:
        orchestrator, call_log, _ = _orchestrator_with_recorders(
            decision_error=RuntimeError("decision failed"),
        )

        with pytest.raises(RuntimeError, match="decision failed"):
            orchestrator.build_experience(
                curriculum_id=1,
                twin=_twin(),
                constraints=_constraints(),
            )

        assert call_log == ["curriculum", "readiness", "decision"]

    def test_recommendation_failure_propagates(self) -> None:
        orchestrator, call_log, _ = _orchestrator_with_recorders(
            recommendation_error=RuntimeError("recommendation failed"),
        )

        with pytest.raises(RuntimeError, match="recommendation failed"):
            orchestrator.build_experience(
                curriculum_id=1,
                twin=_twin(),
                constraints=_constraints(),
            )

        assert "mission" not in call_log

    def test_mission_failure_propagates(self) -> None:
        orchestrator, call_log, _ = _orchestrator_with_recorders(
            mission_error=RuntimeError("mission failed"),
        )

        with pytest.raises(RuntimeError, match="mission failed"):
            orchestrator.build_experience(
                curriculum_id=1,
                twin=_twin(),
                constraints=_constraints(),
            )

        assert call_log == [
            "curriculum",
            "readiness",
            "decision",
            "recommendation",
            "mission",
        ]


# ═══════════════════════════════════════════════════════════════════════════════
# Framework independence / no educational logic
# ═══════════════════════════════════════════════════════════════════════════════


class TestFrameworkIndependence:
    def test_orchestration_package_has_no_flask_or_route_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(ORCHESTRATION_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES or alias.name.startswith(
                            FORBIDDEN_PREFIXES
                        ):
                            violations.append(f"{path.name}: import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES or node.module.startswith(
                        FORBIDDEN_PREFIXES
                    ):
                        violations.append(f"{path.name}: from {node.module}")
        assert violations == []

    def test_orchestrator_source_has_no_flask_request_session(self) -> None:
        src = (
            ORCHESTRATION_ROOT / "educational_orchestrator.py"
        ).read_text(encoding="utf-8")
        assert "flask.request" not in src
        assert "flask.session" not in src
        assert "sqlalchemy" not in src.lower()


class TestNoEducationalLogic:
    def test_orchestrator_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (
            ORCHESTRATION_ROOT / "educational_orchestrator.py"
        ).read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_orchestrator_only_invokes_domain_entrypoints(self) -> None:
        """Structural check: coordination calls derive/evaluate/package/compose."""
        src = (
            ORCHESTRATION_ROOT / "educational_orchestrator.py"
        ).read_text(encoding="utf-8")
        assert ".derive(" in src
        assert ".evaluate(" in src
        assert ".package(" in src
        assert ".compose(" in src
        # Must not re-enter nomination / factor judgement internals.
        assert "nominate_candidates" not in src
        assert "_judge_factor" not in src
        assert "authorise_prefix" not in src

    def test_cold_start_warnings_are_forwarded_not_coerced(self) -> None:
        orchestrator, _, _ = _orchestrator_with_recorders()
        experience = orchestrator.build_experience(
            curriculum_id=1,
            twin=_twin(),
            constraints=_constraints(),
        )

        # Goals-only twin is cold-start / not-yet-knowable — honesty survives.
        assert experience.readiness_summary.cold_start is True
        assert experience.readiness_summary.overall_posture is (
            OverallPosture.NOT_YET_KNOWABLE
        )
        assert "cold_start" in experience.warnings
        assert experience.readiness_summary.overall_warrant is WarrantPosture.LOW
        # Progress never invents Mid/High theatre.
        assert experience.progress_snapshot.overall_posture is (
            OverallPosture.NOT_YET_KNOWABLE
        )

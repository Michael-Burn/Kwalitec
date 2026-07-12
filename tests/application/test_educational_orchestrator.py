"""Tests for EducationalOrchestrator (Capability 3.2.5 + 3.7.7 TwinProvider).

Covers successful composition, TwinProvider retrieval, TwinAbsent honesty,
lawful dependency order, CurriculumContextBuilder and domain invocations,
dependency injection, immutable Experience output, framework independence,
failure propagation, and absence of educational logic in the orchestrator.
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
from app.application.twin import (
    TwinAbsenceReason,
    TwinAbsent,
    TwinProvider,
    TwinRetrievalContext,
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


class _TwinSource:
    """Interim TwinSource double for TwinProvider."""

    def __init__(
        self,
        twin: DigitalTwin | None = None,
        *,
        error: Exception | None = None,
    ):
        self.twin = twin if twin is not None else _twin()
        self.error = error
        self.calls: list[tuple[str, TwinRetrievalContext | None]] = []

    def load(
        self,
        student_id: str,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | None:
        self.calls.append((student_id, context))
        if self.error is not None:
            raise self.error
        return self.twin


class _RecordingTwinProvider:
    """TwinProvider double that records retrieve calls."""

    def __init__(
        self,
        result: DigitalTwin | TwinAbsent | None = None,
        *,
        call_log: list[str] | None = None,
    ):
        self.result: DigitalTwin | TwinAbsent = (
            result if result is not None else _twin()
        )
        self.call_log = call_log
        self.calls: list[tuple[str | None, TwinRetrievalContext | None]] = []

    def retrieve(
        self,
        student_id: str | None,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | TwinAbsent:
        self.calls.append((student_id, context))
        if self.call_log is not None:
            self.call_log.append("twin")
        return self.result


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
    twin: DigitalTwin | TwinAbsent | None = None,
    builder: _RecordingBuilder | None = None,
    readiness_error: Exception | None = None,
    decision_error: Exception | None = None,
    recommendation_error: Exception | None = None,
    mission_error: Exception | None = None,
) -> tuple[
    EducationalOrchestrator,
    list[str],
    _RecordingBuilder,
    _RecordingTwinProvider,
]:
    call_log: list[str] = []
    recording_builder = builder or _RecordingBuilder(_curriculum())
    twin_provider = _RecordingTwinProvider(
        twin if twin is not None else _twin(),
        call_log=call_log,
    )

    class _LoggedBuilder:
        def build(self, curriculum_id: int | None) -> CurriculumContext:
            call_log.append("curriculum")
            return recording_builder.build(curriculum_id)

    orchestrator = EducationalOrchestrator(
        twin_provider=twin_provider,
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
    return orchestrator, call_log, recording_builder, twin_provider


def _build(
    orchestrator: EducationalOrchestrator,
    *,
    student_id: str = "student-42",
    curriculum_id: int = 1,
    product_context: ProductContext | None = None,
) -> EducationalExperience | TwinAbsent:
    return orchestrator.build_experience(
        student_id=student_id,
        curriculum_id=curriculum_id,
        constraints=_constraints(),
        product_context=product_context,
    )


# ═══════════════════════════════════════════════════════════════════════════════
# Successful orchestration
# ═══════════════════════════════════════════════════════════════════════════════


class TestSuccessfulOrchestration:
    def test_build_experience_returns_closed_contract(self) -> None:
        orchestrator, _, _, _ = _orchestrator_with_recorders()

        experience = _build(
            orchestrator,
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
        """Real domain owners work when CurriculumContextBuilder + Twin are faked."""
        builder = _RecordingBuilder(_curriculum())
        source = _TwinSource(_twin())
        orchestrator = EducationalOrchestrator(
            twin_provider=TwinProvider(source=source),
            curriculum_context_builder=builder,
        )

        experience = _build(orchestrator, curriculum_id=7)

        assert isinstance(experience, EducationalExperience)
        assert builder.calls == [7]
        assert experience.todays_recommendation.decision_ref.scope.student_id == (
            "student-42"
        )
        assert experience.todays_mission.tasks  # Decision-authored tasks present
        assert source.calls[0][0] == "student-42"


# ═══════════════════════════════════════════════════════════════════════════════
# TwinProvider integration (Capability 3.7.7)
# ═══════════════════════════════════════════════════════════════════════════════


class TestTwinProviderIntegration:
    def test_caller_does_not_supply_twin(self) -> None:
        """build_experience accepts identity + request context — not a Twin."""
        orchestrator, _, _, twin_provider = _orchestrator_with_recorders()
        experience = _build(orchestrator)

        assert isinstance(experience, EducationalExperience)
        assert twin_provider.calls[0][0] == "student-42"
        # Signature must not require a Twin keyword — already enforced by helper.

    def test_twin_absent_path_preserved(self) -> None:
        absent = TwinAbsent(
            reason=TwinAbsenceReason.MISSING,
            student_id="student-42",
            detail="no Twin snapshot",
        )
        orchestrator, call_log, builder, _ = _orchestrator_with_recorders(
            twin=absent,
        )

        result = _build(orchestrator)

        assert result is absent
        assert isinstance(result, TwinAbsent)
        assert result.reason is TwinAbsenceReason.MISSING
        # Educational chain must not run when Twin is absent.
        assert call_log == ["twin"]
        assert builder.calls == []

    def test_no_twin_parameter_on_build_experience(self) -> None:
        import inspect

        params = inspect.signature(
            EducationalOrchestrator.build_experience
        ).parameters
        assert "twin" not in params
        assert "student_id" in params


# ═══════════════════════════════════════════════════════════════════════════════
# Dependency ordering + invocations
# ═══════════════════════════════════════════════════════════════════════════════


class TestDependencyOrdering:
    def test_lawful_invocation_order(self) -> None:
        orchestrator, call_log, builder, _ = _orchestrator_with_recorders()

        _build(orchestrator, curriculum_id=3)

        assert call_log == [
            "twin",
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
        orchestrator, _, _, _ = _orchestrator_with_recorders(builder=builder)

        _build(orchestrator, curriculum_id=99)

        assert builder.calls == [99]


class TestDomainInvocations:
    def test_readiness_decision_recommendation_mission_invoked(self) -> None:
        orchestrator, call_log, _, _ = _orchestrator_with_recorders()

        _build(orchestrator)

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
        twin_provider = _RecordingTwinProvider(twin, call_log=call_log)
        orchestrator = EducationalOrchestrator(
            twin_provider=twin_provider,
            curriculum_context_builder=_Builder(),
            readiness_aggregation=_RecordingReadiness(call_log),
            decision_engine=_RecordingDecision(call_log),
            recommendation_engine=_RecordingRecommendation(call_log),
            mission_intelligence=_RecordingMission(call_log),
        )

        experience = _build(orchestrator)

        assert isinstance(experience, EducationalExperience)
        assert call_log[0] == "twin"
        assert call_log[1] == "injected_builder"
        assert experience.student_summary.curriculum_id == "INJECTED"
        assert experience.readiness_summary.curriculum_format == (
            CurriculumFormat.V1.value
        )


# ═══════════════════════════════════════════════════════════════════════════════
# Immutable output
# ═══════════════════════════════════════════════════════════════════════════════


class TestImmutableOutput:
    def test_experience_is_frozen(self) -> None:
        orchestrator, _, _, _ = _orchestrator_with_recorders()
        experience = _build(orchestrator)
        assert isinstance(experience, EducationalExperience)

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
        orchestrator, call_log, _, _ = _orchestrator_with_recorders(builder=builder)

        with pytest.raises(RuntimeError, match="missing curriculum"):
            _build(orchestrator)

        assert call_log == ["twin", "curriculum"]

    def test_readiness_failure_propagates_and_stops_chain(self) -> None:
        orchestrator, call_log, _, _ = _orchestrator_with_recorders(
            readiness_error=RuntimeError("readiness failed"),
        )

        with pytest.raises(RuntimeError, match="readiness failed"):
            _build(orchestrator)

        assert call_log == ["twin", "curriculum", "readiness"]

    def test_decision_failure_propagates(self) -> None:
        orchestrator, call_log, _, _ = _orchestrator_with_recorders(
            decision_error=RuntimeError("decision failed"),
        )

        with pytest.raises(RuntimeError, match="decision failed"):
            _build(orchestrator)

        assert call_log == ["twin", "curriculum", "readiness", "decision"]

    def test_recommendation_failure_propagates(self) -> None:
        orchestrator, call_log, _, _ = _orchestrator_with_recorders(
            recommendation_error=RuntimeError("recommendation failed"),
        )

        with pytest.raises(RuntimeError, match="recommendation failed"):
            _build(orchestrator)

        assert "mission" not in call_log

    def test_mission_failure_propagates(self) -> None:
        orchestrator, call_log, _, _ = _orchestrator_with_recorders(
            mission_error=RuntimeError("mission failed"),
        )

        with pytest.raises(RuntimeError, match="mission failed"):
            _build(orchestrator)

        assert call_log == [
            "twin",
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
        assert "TwinRepository" not in src  # Provider is sole retrieval authority


class TestNoEducationalLogic:
    def test_orchestrator_does_not_contain_scoring_or_selection_tokens(self) -> None:
        src = (
            ORCHESTRATION_ROOT / "educational_orchestrator.py"
        ).read_text(encoding="utf-8")
        hits = [token for token in FORBIDDEN_LOGIC_TOKENS if token in src]
        assert hits == []

    def test_orchestrator_only_invokes_domain_entrypoints(self) -> None:
        """Structural check: retrieve / derive / evaluate / package / compose."""
        src = (
            ORCHESTRATION_ROOT / "educational_orchestrator.py"
        ).read_text(encoding="utf-8")
        assert ".retrieve(" in src
        assert ".derive(" in src
        assert ".evaluate(" in src
        assert ".package(" in src
        assert ".compose(" in src
        # Must not re-enter nomination / factor judgement internals.
        assert "nominate_candidates" not in src
        assert "_judge_factor" not in src
        assert "authorise_prefix" not in src

    def test_cold_start_warnings_are_forwarded_not_coerced(self) -> None:
        orchestrator, _, _, _ = _orchestrator_with_recorders()
        experience = _build(orchestrator)
        assert isinstance(experience, EducationalExperience)

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

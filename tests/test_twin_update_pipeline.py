"""Unit tests for the Twin Update Pipeline domain framework."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, date, datetime
from pathlib import Path
from typing import Any

import pytest

from app.domain.evidence import (
    EvidenceConfidenceLevel,
    EvidenceType,
    LearningEvidence,
)
from app.domain.twin import (
    BaseUpdateStrategy,
    DigitalTwin,
    GoalState,
    IdentityState,
    TwinUpdatePipeline,
    UpdateContext,
    UpdateResult,
    UpdateStrategy,
)

TWIN_ROOT = Path(__file__).resolve().parents[1] / "app" / "domain" / "twin"
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


class _AlwaysApplyStrategy(BaseUpdateStrategy):
    """Test double that always supports and rebuilds goals hours."""

    def __init__(self, name: str = "always_apply", hours: float = 10.0) -> None:
        self._name = name
        self._hours = hours

    @property
    def name(self) -> str:
        return self._name

    def supports(self, context: UpdateContext) -> bool:
        return True

    def apply(self, context: UpdateContext) -> DigitalTwin:
        twin = context.twin
        return DigitalTwin.create(
            twin.identity,
            goals=GoalState.create(planned_study_hours_per_week=self._hours),
            knowledge=twin.knowledge,
            memory=twin.memory,
            behaviour=twin.behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )


class _NeverSupportsStrategy(BaseUpdateStrategy):
    """Test double that never claims applicability."""

    @property
    def name(self) -> str:
        return "never_supports"

    def supports(self, context: UpdateContext) -> bool:
        return False

    def apply(self, context: UpdateContext) -> DigitalTwin:
        raise AssertionError("apply must not be called when supports is False")


class _EvidenceScopedStrategy(BaseUpdateStrategy):
    """Applies only when evidence ids contain a marker."""

    @property
    def name(self) -> str:
        return "evidence_scoped"

    def supports(self, context: UpdateContext) -> bool:
        return any(
            item.evidence_id.startswith("knowledge-") for item in context.evidence
        )

    def apply(self, context: UpdateContext) -> DigitalTwin:
        twin = context.twin
        return DigitalTwin.create(
            twin.identity,
            goals=GoalState.create(planned_study_hours_per_week=7.0),
            knowledge=twin.knowledge,
            memory=twin.memory,
            behaviour=twin.behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )


class _RecordingStrategy(BaseUpdateStrategy):
    """Records the Twin hours seen at apply time for order assertions."""

    def __init__(self, name: str, hours: float, seen: list[float | None]) -> None:
        self._name = name
        self._hours = hours
        self._seen = seen

    @property
    def name(self) -> str:
        return self._name

    def supports(self, context: UpdateContext) -> bool:
        return True

    def apply(self, context: UpdateContext) -> DigitalTwin:
        self._seen.append(context.twin.goals.planned_study_hours_per_week)
        twin = context.twin
        return DigitalTwin.create(
            twin.identity,
            goals=GoalState.create(planned_study_hours_per_week=self._hours),
            knowledge=twin.knowledge,
            memory=twin.memory,
            behaviour=twin.behaviour,
            performance=twin.performance,
            predictions=twin.predictions,
        )


class TestUpdateContext:
    """UpdateContext creation and immutability."""

    def test_create_with_single_evidence(self) -> None:
        twin = _twin()
        evidence = _evidence()
        context = UpdateContext.create(twin, evidence, metadata={"run": "r1"})
        assert context.twin is twin
        assert context.evidence == (evidence,)
        assert context.metadata == {"run": "r1"}

    def test_create_with_multiple_evidence(self) -> None:
        twin = _twin()
        first = _evidence(evidence_id="ev-a")
        second = _evidence(evidence_id="ev-b")
        context = UpdateContext.create(twin, [first, second])
        assert context.evidence == (first, second)

    def test_create_copies_metadata(self) -> None:
        metadata = {"k": "v"}
        context = UpdateContext.create(_twin(), _evidence(), metadata=metadata)
        metadata["mutated"] = True
        assert context.metadata == {"k": "v"}

    def test_context_is_frozen(self) -> None:
        context = UpdateContext.create(_twin(), _evidence())
        with pytest.raises(AttributeError):
            context.twin = _twin()  # type: ignore[misc]

    def test_with_twin_returns_new_context(self) -> None:
        original = _twin()
        context = UpdateContext.create(
            original, _evidence(), metadata={"stage": "pipeline"}
        )
        updated = DigitalTwin.create(
            original.identity,
            goals=GoalState.create(planned_study_hours_per_week=3.0),
        )
        next_context = context.with_twin(updated)
        assert next_context is not context
        assert next_context.twin is updated
        assert next_context.evidence == context.evidence
        assert next_context.metadata == {"stage": "pipeline"}
        assert context.twin is original


class TestUpdateResult:
    """UpdateResult creation and immutability."""

    def test_create_update_result(self) -> None:
        original = _twin()
        updated = DigitalTwin.create(
            original.identity,
            goals=GoalState.create(planned_study_hours_per_week=5.0),
        )
        result = UpdateResult.create(
            original,
            updated,
            applied_strategies=["stub"],
            processing_messages=["Applied strategy 'stub'."],
            success=True,
        )
        assert result.original_twin is original
        assert result.updated_twin is updated
        assert result.applied_strategies == ("stub",)
        assert result.processing_messages == ("Applied strategy 'stub'.",)
        assert result.success is True

    def test_create_defaults(self) -> None:
        twin = _twin()
        result = UpdateResult.create(twin, twin)
        assert result.applied_strategies == ()
        assert result.processing_messages == ()
        assert result.success is True

    def test_result_is_frozen(self) -> None:
        twin = _twin()
        result = UpdateResult.create(twin, twin)
        with pytest.raises(AttributeError):
            result.success = False  # type: ignore[misc]


class TestPipelineConstruction:
    """Pipeline construction and strategy registration."""

    def test_empty_pipeline_construction(self) -> None:
        pipeline = TwinUpdatePipeline()
        assert pipeline.strategies == ()

    def test_constructor_accepts_initial_strategies(self) -> None:
        first = _AlwaysApplyStrategy("first")
        second = _NeverSupportsStrategy()
        pipeline = TwinUpdatePipeline([first, second])
        assert pipeline.strategies == (first, second)

    def test_register_strategy(self) -> None:
        pipeline = TwinUpdatePipeline()
        stub = _AlwaysApplyStrategy()
        pipeline.register(stub)
        assert pipeline.strategies == (stub,)

    def test_update_strategy_alias_is_base(self) -> None:
        assert UpdateStrategy is BaseUpdateStrategy
        assert issubclass(_AlwaysApplyStrategy, UpdateStrategy)


class TestPipelineExecution:
    """Strategy discovery, applicability, and execution order."""

    def test_no_strategies_returns_original_twin(self) -> None:
        twin = _twin()
        evidence = _evidence()
        result = TwinUpdatePipeline().update(twin, evidence)
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is twin
        assert result.applied_strategies == ()
        assert any(
            "No update strategies registered" in msg
            for msg in result.processing_messages
        )

    def test_applies_supporting_strategy(self) -> None:
        twin = _twin()
        result = TwinUpdatePipeline([_AlwaysApplyStrategy(hours=12.0)]).update(
            twin, _evidence()
        )
        assert result.success is True
        assert result.original_twin is twin
        assert result.updated_twin is not twin
        assert result.updated_twin.goals.planned_study_hours_per_week == 12.0
        assert result.applied_strategies == ("always_apply",)
        assert any(
            "Applied strategy 'always_apply'" in msg
            for msg in result.processing_messages
        )

    def test_skips_non_supporting_strategy(self) -> None:
        twin = _twin()
        pipeline = TwinUpdatePipeline([_NeverSupportsStrategy()])
        result = pipeline.update(twin, _evidence())
        assert result.updated_twin is twin
        assert result.applied_strategies == ()
        assert any("not applicable" in msg for msg in result.processing_messages)
        assert any(
            "No applicable update strategies" in msg
            for msg in result.processing_messages
        )

    def test_execution_order_chains_twin_snapshots(self) -> None:
        seen: list[float | None] = []
        pipeline = TwinUpdatePipeline(
            [
                _RecordingStrategy("first", hours=4.0, seen=seen),
                _RecordingStrategy("second", hours=8.0, seen=seen),
            ]
        )
        twin = _twin()
        result = pipeline.update(twin, _evidence())
        assert seen == [None, 4.0]
        assert result.applied_strategies == ("first", "second")
        assert result.updated_twin.goals.planned_study_hours_per_week == 8.0

    def test_mixed_support_preserves_registration_order(self) -> None:
        pipeline = TwinUpdatePipeline(
            [
                _NeverSupportsStrategy(),
                _AlwaysApplyStrategy("second", hours=6.0),
                _EvidenceScopedStrategy(),
            ]
        )
        result = pipeline.update(
            _twin(),
            [
                _evidence(evidence_id="knowledge-1"),
                _evidence(evidence_id="ev-other"),
            ],
        )
        assert result.applied_strategies == ("second", "evidence_scoped")
        assert result.updated_twin.goals.planned_study_hours_per_week == 7.0

    def test_accepts_sequence_of_evidence(self) -> None:
        pipeline = TwinUpdatePipeline([_EvidenceScopedStrategy()])
        result = pipeline.update(
            _twin(),
            (_evidence(evidence_id="knowledge-a"), _evidence(evidence_id="b")),
        )
        assert result.applied_strategies == ("evidence_scoped",)

    def test_pipeline_does_not_mutate_original_twin(self) -> None:
        twin = _twin()
        original_hours = twin.goals.planned_study_hours_per_week
        TwinUpdatePipeline([_AlwaysApplyStrategy(hours=15.0)]).update(twin, _evidence())
        assert twin.goals.planned_study_hours_per_week == original_hours
        with pytest.raises(AttributeError):
            twin.identity = _identity(student_id="mutated")  # type: ignore[misc]

    def test_pipeline_does_not_mutate_evidence(self) -> None:
        evidence = _evidence(payload={"correct": True}, metadata={"k": "v"})
        payload = dict(evidence.payload)
        metadata = dict(evidence.metadata)
        TwinUpdatePipeline([_AlwaysApplyStrategy()]).update(_twin(), evidence)
        assert evidence.payload == payload
        assert evidence.metadata == metadata
        with pytest.raises(AttributeError):
            evidence.evidence_id = "mutated"  # type: ignore[misc]

    def test_metadata_passed_into_context(self) -> None:
        captured: list[dict[str, Any]] = []

        class _CaptureMetadata(BaseUpdateStrategy):
            @property
            def name(self) -> str:
                return "capture_metadata"

            def supports(self, context: UpdateContext) -> bool:
                captured.append(dict(context.metadata))
                return False

            def apply(self, context: UpdateContext) -> DigitalTwin:
                return context.twin

        TwinUpdatePipeline([_CaptureMetadata()]).update(
            _twin(), _evidence(), metadata={"correlation_id": "c-9"}
        )
        assert captured == [{"correlation_id": "c-9"}]


class TestFrameworkIndependence:
    """Twin update framework must remain framework-independent."""

    def test_source_files_have_no_framework_imports(self) -> None:
        violations: list[str] = []
        for path in sorted(TWIN_ROOT.rglob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        root = alias.name.split(".", 1)[0]
                        if root in FORBIDDEN_ROOT_MODULES:
                            loc = f"{path}:{node.lineno}"
                            violations.append(f"{loc} import {alias.name}")
                elif isinstance(node, ast.ImportFrom) and node.module:
                    root = node.module.split(".", 1)[0]
                    if root in FORBIDDEN_ROOT_MODULES:
                        loc = f"{path}:{node.lineno}"
                        violations.append(f"{loc} from {node.module}")
        assert violations == []

    def test_importing_package_does_not_require_flask(self) -> None:
        domain_modules = [
            name
            for name in sys.modules
            if name == "app.domain.twin" or name.startswith("app.domain.twin.")
        ]
        assert domain_modules
        for name in domain_modules:
            module = sys.modules[name]
            module_file = getattr(module, "__file__", "") or ""
            if "site-packages" in module_file or "flask" in module_file.lower():
                pytest.fail(
                    f"Unexpected framework module path for {name}: {module_file}"
                )
            assert not any(
                dep in getattr(module, "__dict__", {})
                for dep in ("Flask", "request", "db", "SQLAlchemy")
            )

    def test_pipeline_modules_do_not_import_services_or_models(self) -> None:
        violations: list[str] = []
        forbidden_prefixes = ("app.services", "app.models", "app.auth", "app.dashboard")
        pipeline_paths = [
            TWIN_ROOT / "update_pipeline.py",
            TWIN_ROOT / "update_context.py",
            TWIN_ROOT / "update_result.py",
            TWIN_ROOT / "update_strategy.py",
            TWIN_ROOT / "strategies" / "base_strategy.py",
            TWIN_ROOT / "strategies" / "__init__.py",
        ]
        for path in pipeline_paths:
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom) and node.module:
                    if node.module.startswith(forbidden_prefixes):
                        loc = f"{path}:{node.lineno}"
                        violations.append(f"{loc} from {node.module}")
                elif isinstance(node, ast.Import):
                    for alias in node.names:
                        if alias.name.startswith(forbidden_prefixes):
                            loc = f"{path}:{node.lineno}"
                            violations.append(f"{loc} import {alias.name}")
        assert violations == []

    def test_pipeline_has_no_educational_algorithm_api(self) -> None:
        pipeline = TwinUpdatePipeline()
        public_callables = {
            name
            for name in dir(pipeline)
            if callable(getattr(pipeline, name)) and not name.startswith("_")
        }
        forbidden = {
            "compute_mastery",
            "decay_memory",
            "predict",
            "recommend",
            "plan",
            "persist",
            "save",
        }
        assert forbidden.isdisjoint(public_callables)

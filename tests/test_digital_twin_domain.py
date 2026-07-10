"""Unit tests for the Student Digital Twin domain package."""

from __future__ import annotations

import ast
import sys
from datetime import UTC, date, datetime
from pathlib import Path

import pytest

from app.domain.twin import (
    BehaviourState,
    DigitalTwin,
    GoalState,
    IdentityState,
    KnowledgeState,
    MemoryState,
    PerformanceState,
    PerformanceSummary,
    PredictionState,
    RetentionRecord,
    TopicMasteryRecord,
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


class TestIdentityState:
    """Identity state construction and validation."""

    def test_create_full_identity(self) -> None:
        state = _identity()
        assert state.student_id == "student-42"
        assert state.curriculum_id == "CS1-2026"
        assert state.current_exam == "CS1"
        assert state.target_sitting == date(2026, 9, 15)

    def test_create_minimal_identity(self) -> None:
        state = IdentityState.create("user-1")
        assert state.student_id == "user-1"
        assert state.curriculum_id is None
        assert state.current_exam is None
        assert state.target_sitting is None

    def test_strips_student_id(self) -> None:
        assert IdentityState.create("  abc  ").student_id == "abc"

    def test_rejects_empty_student_id(self) -> None:
        with pytest.raises(ValueError, match="student_id"):
            IdentityState.create("")
        with pytest.raises(ValueError, match="student_id"):
            IdentityState.create("   ")

    def test_identity_is_frozen(self) -> None:
        state = _identity()
        with pytest.raises(AttributeError):
            state.student_id = "other"  # type: ignore[misc]


class TestGoalState:
    """Goal state construction and validation."""

    def test_create_empty_goals(self) -> None:
        state = GoalState.create()
        assert state.target_pass_probability is None
        assert state.target_completion_date is None
        assert state.planned_study_hours_per_week is None

    def test_create_full_goals(self) -> None:
        state = GoalState.create(
            target_pass_probability=0.85,
            target_completion_date=date(2026, 8, 1),
            planned_study_hours_per_week=12.5,
        )
        assert state.target_pass_probability == 0.85
        assert state.target_completion_date == date(2026, 8, 1)
        assert state.planned_study_hours_per_week == 12.5

    def test_rejects_probability_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="target_pass_probability"):
            GoalState.create(target_pass_probability=1.5)
        with pytest.raises(ValueError, match="target_pass_probability"):
            GoalState.create(target_pass_probability=-0.1)

    def test_rejects_negative_hours(self) -> None:
        with pytest.raises(ValueError, match="planned_study_hours_per_week"):
            GoalState.create(planned_study_hours_per_week=-1.0)

    def test_goals_are_frozen(self) -> None:
        state = GoalState.create(target_pass_probability=0.7)
        with pytest.raises(AttributeError):
            state.target_pass_probability = 0.9  # type: ignore[misc]


class TestKnowledgeState:
    """Knowledge state construction."""

    def test_create_empty_knowledge(self) -> None:
        state = KnowledgeState.create()
        assert state.topic_mastery == ()
        assert state.evidence_ids == ()
        assert state.last_updated is None

    def test_create_with_topic_mastery_and_evidence(self) -> None:
        ts = datetime(2026, 7, 10, 12, 0, tzinfo=UTC)
        record = TopicMasteryRecord.create(
            "CS1-A-T01",
            mastery_belief=0.6,
            evidence_ids=["ev-1", "ev-2"],
        )
        state = KnowledgeState.create(
            topic_mastery=[record],
            evidence_ids=["ev-1", "ev-2"],
            last_updated=ts,
        )
        assert len(state.topic_mastery) == 1
        assert state.topic_mastery[0].topic_id == "CS1-A-T01"
        assert state.topic_mastery[0].mastery_belief == 0.6
        assert state.evidence_ids == ("ev-1", "ev-2")
        assert state.last_updated == ts

    def test_topic_mastery_rejects_empty_topic_id(self) -> None:
        with pytest.raises(ValueError, match="topic_id"):
            TopicMasteryRecord.create("")

    def test_topic_mastery_copies_evidence_ids(self) -> None:
        ids = ["ev-a"]
        record = TopicMasteryRecord.create("T1", evidence_ids=ids)
        ids.append("ev-b")
        assert record.evidence_ids == ("ev-a",)

    def test_knowledge_is_frozen(self) -> None:
        state = KnowledgeState.create(evidence_ids=["ev-1"])
        with pytest.raises(AttributeError):
            state.evidence_ids = ()  # type: ignore[misc]


class TestMemoryState:
    """Memory state construction."""

    def test_create_empty_memory(self) -> None:
        state = MemoryState.create()
        assert state.retention == ()
        assert state.revision_ids == ()
        assert state.last_updated is None

    def test_create_with_retention_and_revisions(self) -> None:
        ts = datetime(2026, 7, 9, 8, 0, tzinfo=UTC)
        retention = RetentionRecord.create(
            "CS1-B-T02",
            retention_belief=0.4,
            last_reinforced=ts,
        )
        state = MemoryState.create(
            retention=[retention],
            revision_ids=["rev-9"],
            last_updated=ts,
        )
        assert state.retention[0].topic_id == "CS1-B-T02"
        assert state.retention[0].retention_belief == 0.4
        assert state.revision_ids == ("rev-9",)

    def test_retention_rejects_empty_topic_id(self) -> None:
        with pytest.raises(ValueError, match="topic_id"):
            RetentionRecord.create("  ")

    def test_memory_is_frozen(self) -> None:
        state = MemoryState.create(revision_ids=["r1"])
        with pytest.raises(AttributeError):
            state.revision_ids = ()  # type: ignore[misc]


class TestBehaviourState:
    """Behaviour state construction."""

    def test_create_empty_behaviour(self) -> None:
        state = BehaviourState.create()
        assert state.consistency_metrics == {}
        assert state.session_history_ids == ()
        assert state.study_pattern_ids == ()

    def test_create_with_metrics_and_references(self) -> None:
        metrics = {"adherence_ratio": 0.8, "sessions_completed": 12}
        state = BehaviourState.create(
            consistency_metrics=metrics,
            session_history_ids=["sess-1", "sess-2"],
            study_pattern_ids=["pat-weekday"],
        )
        assert state.consistency_metrics["adherence_ratio"] == 0.8
        assert state.session_history_ids == ("sess-1", "sess-2")
        assert state.study_pattern_ids == ("pat-weekday",)
        # Defensive copy of metrics bag
        metrics["adherence_ratio"] = 0.1
        assert state.consistency_metrics["adherence_ratio"] == 0.8

    def test_behaviour_is_frozen(self) -> None:
        state = BehaviourState.create()
        with pytest.raises(AttributeError):
            state.session_history_ids = ("x",)  # type: ignore[misc]


class TestPerformanceState:
    """Performance state construction."""

    def test_create_empty_performance(self) -> None:
        state = PerformanceState.create()
        assert state.assessment_ids == ()
        assert state.performance_summaries == ()

    def test_create_with_assessments_and_summaries(self) -> None:
        summary = PerformanceSummary.create(
            "quiz-3",
            summary={"accuracy": 0.75, "items": 20},
        )
        state = PerformanceState.create(
            assessment_ids=["assess-1"],
            performance_summaries=[summary],
        )
        assert state.assessment_ids == ("assess-1",)
        assert state.performance_summaries[0].scope_id == "quiz-3"
        assert state.performance_summaries[0].summary["accuracy"] == 0.75

    def test_summary_rejects_empty_scope_id(self) -> None:
        with pytest.raises(ValueError, match="scope_id"):
            PerformanceSummary.create("")

    def test_summary_copies_payload(self) -> None:
        payload = {"score": 0.5}
        summary = PerformanceSummary.create("mock-1", summary=payload)
        payload["score"] = 0.9
        assert summary.summary["score"] == 0.5

    def test_performance_is_frozen(self) -> None:
        state = PerformanceState.create(assessment_ids=["a1"])
        with pytest.raises(AttributeError):
            state.assessment_ids = ()  # type: ignore[misc]


class TestPredictionState:
    """Prediction state construction and validation."""

    def test_create_empty_predictions(self) -> None:
        state = PredictionState.create()
        assert state.readiness_snapshot is None
        assert state.pass_probability_snapshot is None
        assert state.as_of is None
        assert state.metadata == {}

    def test_create_with_snapshots(self) -> None:
        ts = datetime(2026, 7, 10, 18, 0, tzinfo=UTC)
        state = PredictionState.create(
            readiness_snapshot=0.72,
            pass_probability_snapshot=0.61,
            as_of=ts,
            metadata={"model": "stub-v0"},
        )
        assert state.readiness_snapshot == 0.72
        assert state.pass_probability_snapshot == 0.61
        assert state.as_of == ts
        assert state.metadata["model"] == "stub-v0"

    def test_rejects_pass_probability_out_of_range(self) -> None:
        with pytest.raises(ValueError, match="pass_probability_snapshot"):
            PredictionState.create(pass_probability_snapshot=1.2)

    def test_predictions_are_frozen(self) -> None:
        state = PredictionState.create(readiness_snapshot=0.5)
        with pytest.raises(AttributeError):
            state.readiness_snapshot = 0.9  # type: ignore[misc]


class TestDigitalTwinAggregate:
    """Digital Twin aggregate construction and immutability."""

    def test_create_with_identity_only_defaults_empty_domains(self) -> None:
        twin = DigitalTwin.create(_identity())
        assert twin.identity.student_id == "student-42"
        assert twin.goals.target_pass_probability is None
        assert twin.knowledge.topic_mastery == ()
        assert twin.memory.retention == ()
        assert twin.behaviour.session_history_ids == ()
        assert twin.performance.assessment_ids == ()
        assert twin.predictions.pass_probability_snapshot is None

    def test_create_with_all_domains(self) -> None:
        twin = DigitalTwin.create(
            _identity(),
            goals=GoalState.create(target_pass_probability=0.9),
            knowledge=KnowledgeState.create(
                topic_mastery=[TopicMasteryRecord.create("T1")],
                evidence_ids=["ev-1"],
            ),
            memory=MemoryState.create(
                retention=[RetentionRecord.create("T1")],
                revision_ids=["rev-1"],
            ),
            behaviour=BehaviourState.create(
                consistency_metrics={"streak_days": 5},
                session_history_ids=["s1"],
            ),
            performance=PerformanceState.create(assessment_ids=["a1"]),
            predictions=PredictionState.create(pass_probability_snapshot=0.55),
        )
        assert twin.goals.target_pass_probability == 0.9
        assert twin.knowledge.evidence_ids == ("ev-1",)
        assert twin.memory.revision_ids == ("rev-1",)
        assert twin.behaviour.consistency_metrics["streak_days"] == 5
        assert twin.performance.assessment_ids == ("a1",)
        assert twin.predictions.pass_probability_snapshot == 0.55

    def test_aggregate_exposes_all_required_states(self) -> None:
        twin = DigitalTwin.create(_identity())
        assert isinstance(twin.identity, IdentityState)
        assert isinstance(twin.goals, GoalState)
        assert isinstance(twin.knowledge, KnowledgeState)
        assert isinstance(twin.memory, MemoryState)
        assert isinstance(twin.behaviour, BehaviourState)
        assert isinstance(twin.performance, PerformanceState)
        assert isinstance(twin.predictions, PredictionState)

    def test_aggregate_is_frozen(self) -> None:
        twin = DigitalTwin.create(_identity())
        with pytest.raises(AttributeError):
            twin.identity = IdentityState.create("other")  # type: ignore[misc]

    def test_nested_state_replacement_requires_new_aggregate(self) -> None:
        twin = DigitalTwin.create(_identity())
        updated_goals = GoalState.create(planned_study_hours_per_week=10.0)
        rebuilt = DigitalTwin.create(twin.identity, goals=updated_goals)
        assert twin.goals.planned_study_hours_per_week is None
        assert rebuilt.goals.planned_study_hours_per_week == 10.0
        assert rebuilt is not twin


class TestFrameworkIndependence:
    """Twin package must remain framework-independent."""

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

    def test_twin_modules_do_not_import_services_or_models(self) -> None:
        violations: list[str] = []
        forbidden_prefixes = ("app.services", "app.models", "app.auth", "app.dashboard")
        for path in sorted(TWIN_ROOT.rglob("*.py")):
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

    def test_no_update_or_prediction_methods_on_aggregate(self) -> None:
        twin = DigitalTwin.create(_identity())
        public_callables = [
            name
            for name in dir(twin)
            if callable(getattr(twin, name)) and not name.startswith("_")
        ]
        # Frozen dataclass exposes no domain behaviour beyond construction helpers
        # on the class; instance should not expose update/predict APIs.
        forbidden = {
            "update",
            "apply_evidence",
            "predict",
            "recommend",
            "recalculate",
            "persist",
            "save",
        }
        assert forbidden.isdisjoint(public_callables)

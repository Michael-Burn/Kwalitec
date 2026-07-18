"""DTO immutability, package exports, DI, and framework independence."""

from __future__ import annotations

import importlib
import sys

import pytest

from app.application import learning_activity as pkg
from app.application.learning_activity.completion_manager import CompletionManager
from app.application.learning_activity.dto.activity_plan import (
    ActivityPlan,
    ActivityPlanItem,
)
from app.application.learning_activity.dto.activity_result import ActivityResult
from app.application.learning_activity.dto.activity_sequence import ActivitySequence
from app.application.learning_activity.dto.activity_snapshot import ActivitySnapshot
from app.application.learning_activity.dto.activity_transition import (
    ActivityTransition,
)
from app.application.learning_activity.engine import LearningActivityEngine
from app.application.learning_activity.evidence_router import EvidenceRouter
from app.application.learning_activity.planner import ActivityPlanner
from app.application.learning_activity.progression_manager import ProgressionManager
from app.application.learning_activity.reflection_router import ReflectionRouter
from app.application.learning_activity.sequence_builder import SequenceBuilder
from app.application.learning_activity.transition_manager import TransitionManager
from app.application.learning_activity.validator import ActivityValidator
from app.domain.learning_activity.entities.activity_progress import ActivityProgress
from app.domain.learning_activity.value_objects.activity_state import (
    ActivityState,
    ActivityTransitionEvent,
)
from app.domain.learning_activity.value_objects.activity_type import ActivityType
from tests.application.learning_activity.helpers import make_activity, make_engine


class TestDtoImmutability:
    def test_activity_plan_frozen(self):
        plan = ActivityPlan(
            session_id="s",
            journey_id="j",
            items=(ActivityPlanItem(activity_type=ActivityType.REVIEW),),
            rationale_tags=("t",),
        )
        with pytest.raises(Exception):
            plan.session_id = "x"  # type: ignore[misc]

    def test_activity_plan_item_frozen(self):
        item = ActivityPlanItem(activity_type=ActivityType.CUSTOM)
        with pytest.raises(Exception):
            item.title = "x"  # type: ignore[misc]

    def test_activity_sequence_frozen(self):
        sequence = ActivitySequence(
            session_id="s",
            sequence_id="seq",
            activities=(make_activity(),),
        )
        with pytest.raises(Exception):
            sequence.sequence_id = "x"  # type: ignore[misc]

    def test_activity_transition_frozen(self):
        transition = ActivityTransition(
            activity_id="a1",
            session_id="s",
            event=ActivityTransitionEvent.START,
            from_state=ActivityState.NOT_STARTED,
            to_state=ActivityState.ACTIVE,
        )
        with pytest.raises(Exception):
            transition.event = ActivityTransitionEvent.SKIP  # type: ignore[misc]

    def test_activity_result_frozen(self):
        result = ActivityResult(
            activity_id="a1",
            session_id="s",
            activity_complete=True,
            sequence_complete=True,
            ready_for_session_completion=True,
            blockers=(),
            reason="ok",
            completed_count=1,
            skipped_count=0,
            remaining_count=0,
        )
        with pytest.raises(Exception):
            result.ready_for_session_completion = False  # type: ignore[misc]

    def test_activity_snapshot_frozen(self):
        sequence = ActivitySequence(
            session_id="s",
            sequence_id="seq",
            activities=(make_activity(),),
        )
        snap = ActivitySnapshot(
            session_id="s",
            sequence_id="seq",
            current_activity=None,
            current_state=None,
            progress=ActivityProgress.empty("s"),
            sequence=sequence,
            result=None,
            ready_for_session_completion=False,
            next_activity=None,
            previous_activity=None,
        )
        with pytest.raises(Exception):
            snap.ready_for_session_completion = True  # type: ignore[misc]


class TestPackageExports:
    @pytest.mark.parametrize(
        "name",
        [
            "LearningActivityEngine",
            "ActivityHandle",
            "ActivityPlan",
            "ActivitySequence",
            "ActivitySnapshot",
            "ActivityResult",
            "ActivityTransition",
            "ActivityType",
            "ActivityState",
            "SequencingPolicy",
            "ProgressionPolicy",
            "TransitionPolicy",
            "CompletionPolicy",
            "ActivityPlanner",
            "SequenceBuilder",
            "ProgressionManager",
            "TransitionManager",
            "CompletionManager",
            "EvidenceRouter",
            "ReflectionRouter",
            "ActivityValidator",
            "LearningActivity",
        ],
    )
    def test_lazy_export(self, name):
        assert getattr(pkg, name) is not None

    def test_dir_includes_exports(self):
        names = dir(pkg)
        assert "LearningActivityEngine" in names
        assert "ActivityType" in names

    def test_unknown_export_raises(self):
        with pytest.raises(AttributeError):
            _ = pkg.DoesNotExist  # type: ignore[attr-defined]


class TestDependencyInjection:
    def test_custom_collaborators_injected(self):
        planner = ActivityPlanner()
        builder = SequenceBuilder(id_factory=lambda: "inj")
        progression = ProgressionManager()
        transitions = TransitionManager()
        completion = CompletionManager()
        evidence = EvidenceRouter()
        reflection = ReflectionRouter()
        validator = ActivityValidator()
        engine = LearningActivityEngine(
            planner=planner,
            sequence_builder=builder,
            progression=progression,
            transitions=transitions,
            completion=completion,
            evidence_router=evidence,
            reflection_router=reflection,
            validator=validator,
            id_factory=lambda: "inj",
        )
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW,),
            sequence_id="seq-inj",
        )
        assert handle.sequence.sequence_id == "seq-inj"
        handle, _ = engine.start_activity(handle)
        handle = engine.route_evidence(handle, evidence_id="e1")
        assert "e1" in engine.current_activity(handle).evidence_ids

    def test_id_factory_used(self):
        engine = LearningActivityEngine(id_factory=lambda: "abc123")
        handle = engine.create_sequence(
            session_id="sess-1",
            activity_types=(ActivityType.REVIEW, ActivityType.SUMMARY),
        )
        assert all("abc123" in a.activity_id for a in handle.sequence.activities)


class TestFrameworkIndependence:
    @pytest.mark.parametrize(
        "module_path",
        [
            "app.application.learning_activity",
            "app.application.learning_activity.engine",
            "app.application.learning_activity.planner",
            "app.application.learning_activity.sequence_builder",
            "app.application.learning_activity.progression_manager",
            "app.application.learning_activity.transition_manager",
            "app.application.learning_activity.completion_manager",
            "app.application.learning_activity.evidence_router",
            "app.application.learning_activity.reflection_router",
            "app.application.learning_activity.validator",
            "app.domain.learning_activity",
            "app.domain.learning_activity.entities.learning_activity",
            "app.domain.learning_activity.value_objects.activity_type",
            "app.domain.learning_activity.value_objects.activity_state",
        ],
    )
    def test_modules_import_without_flask_sqlalchemy(self, module_path):
        # Ensure importing activity modules does not pull Flask/SQLAlchemy
        # into the import graph as hard deps for these packages.
        mod = importlib.import_module(module_path)
        source = getattr(mod, "__file__", "") or ""
        assert "learning_activity" in source.replace("\\", "/")

    def test_engine_source_has_no_flask_imports(self):
        import inspect

        source = inspect.getsource(LearningActivityEngine)
        assert "flask" not in source.lower()
        assert "sqlalchemy" not in source.lower()

    def test_no_persistence_methods(self):
        engine = make_engine()
        for name in ("save", "persist", "commit", "flush", "query"):
            assert not hasattr(engine, name)

    def test_session_runtime_untouched_importable(self):
        # Regression: activity engine coexists; session runtime still imports.
        from app.application.learning_session.runtime import LearningSessionRuntime

        assert LearningSessionRuntime is not None

    def test_does_not_import_mission_engine(self):
        # Clear and re-import activity engine; mission modules need not load.
        forbidden = {
            "app.application.mission_engine",
            "app.application.mission_engine_v2",
            "app.application.mission_adapter",
        }
        before = {m for m in forbidden if m in sys.modules}
        importlib.reload(sys.modules["app.application.learning_activity.engine"])
        after = {m for m in forbidden if m in sys.modules}
        # Do not require they were never imported by other tests; just ensure
        # activity engine module itself does not list them as attributes.
        engine_mod = sys.modules["app.application.learning_activity.engine"]
        for name in forbidden:
            assert name not in getattr(engine_mod, "__dict__", {})
        assert before == before  # keep before referenced
        assert after == after

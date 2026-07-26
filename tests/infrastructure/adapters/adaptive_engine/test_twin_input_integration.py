"""Integration / boundary / read-only tests — Twin Input Adapter (MS-004 T4)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

import pytest

import app.infrastructure.adapters.adaptive_engine as adaptive_engine_pkg
import app.infrastructure.adapters.digital_twin as digital_twin_pkg
from app.infrastructure.adapters.adaptive_engine import (
    AVAILABILITY_AVAILABLE,
    AVAILABILITY_UNAVAILABLE,
    FIELD_TWIN,
    AdaptiveEngineExecutor,
    AdaptiveInputAssembler,
    AdaptiveInputBundle,
    CollectorResult,
    TwinInputAdapter,
    build_adaptive_input_assembler,
    build_twin_input_adapter,
)
from app.infrastructure.adapters.digital_twin import (
    TwinExplainabilityService,
    TwinFacetAssembler,
    TwinSnapshotBuilder,
)
from app.infrastructure.adapters.student_experience.composition import (
    build_production_experience,
)
from tests.conftest import (
    _make_curriculum,
    _make_mission,
    _make_study_attempt,
    _make_study_plan,
    _make_subject,
    _make_topic_progress,
    _make_user,
)

ADAPTER_ROOT = Path(adaptive_engine_pkg.__file__).resolve().parent
TWIN_ROOT = Path(digital_twin_pkg.__file__).resolve().parent

FORBIDDEN_WRITE_TOKENS = (
    "db.session.commit",
    "db.session.add",
    "generate_today_mission",
    "start_session",
    "complete_session",
    "accept_evidence",
    "alembic",
)

FORBIDDEN_TWIN_SYNTHESIS_CALLS = (
    "TwinSnapshotBuilder",
    "TwinFacetAssembler",
    "build_twin_snapshot_builder",
    "build_twin_facet_assembler",
)

FORBIDDEN_EXPERIENCE_IMPORTS = (
    "app.infrastructure.adapters.student_experience",
    "app.application.student_experience",
    "ExperienceTwinAdapter",
)


@pytest.fixture
def learner(app, ctx):
    user = _make_user()
    subject = _make_subject(user.id)
    curriculum, topics = _make_curriculum()
    plan = _make_study_plan(user.id)
    plan.curriculum_id = curriculum.id
    from app.extensions import db

    db.session.commit()
    mission = _make_mission(user.id, subject.id, study_plan_id=plan.id)
    attempt = _make_study_attempt(user.id, topics[0].id, mission.id)
    progress = _make_topic_progress(user.id, topics[0].id)
    return {
        "user": user,
        "subject": subject,
        "curriculum": curriculum,
        "topics": topics,
        "plan": plan,
        "mission": mission,
        "attempt": attempt,
        "progress": progress,
    }


class _StubCollector:
    def __init__(
        self,
        field_name: str,
        *,
        available: bool = True,
        payload: Any = None,
        reason: str = "",
        source_service: str = "stub_service",
        source_entity: str = "StubEntity",
    ) -> None:
        self.field_name = field_name
        self._available = available
        self._payload = payload if payload is not None else (
            [] if field_name in {"topic_progress", "study_attempts"} else {}
        )
        self._reason = reason
        self._source_service = source_service
        self._source_entity = source_entity

    def collect(
        self,
        user_id: int,
        *,
        as_of: str | None = None,
        context: dict[str, Any] | None = None,
    ) -> CollectorResult:
        _ = (user_id, as_of, context)
        return CollectorResult(
            available=self._available,
            payload=self._payload,
            source_service=self._source_service,
            source_entity=self._source_entity,
            unavailable_reason=self._reason,
        )


def _stub_collectors(**overrides: _StubCollector) -> dict[str, _StubCollector]:
    from app.infrastructure.adapters.adaptive_engine import INPUT_FIELD_NAMES

    collectors: dict[str, _StubCollector] = {}
    for name in INPUT_FIELD_NAMES:
        collectors[name] = overrides.get(name) or _StubCollector(name)
    return collectors


class _FakePlan:
    id = 1


class _FakePlanService:
    def read_active_plan(self, user_id: int) -> Any:
        _ = user_id
        return _FakePlan()


def test_assembler_attaches_prebuilt_twin_snapshot_read_only(learner):
    sid = str(learner["user"].id)
    twin_assembler = TwinFacetAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
    )
    builder = TwinSnapshotBuilder(facet_assembler=twin_assembler)
    explain = TwinExplainabilityService()
    snapshot = builder.build(sid, as_of="2026-07-25")
    explanation = explain.explain_snapshot(snapshot)
    before = snapshot.serialize()

    twin_input = TwinInputAdapter()
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
        twin_input=twin_input,
    )
    bundle = assembler.assemble(
        sid,
        as_of="2026-07-25",
        twin_snapshot=snapshot,
        twin_explanation=explanation,
    )

    assert bundle.twin["availability"] == AVAILABILITY_AVAILABLE
    assert bundle.twin["twin_snapshot_ref"]
    assert bundle.twin["explanation"]["explainability_version"]
    assert FIELD_TWIN in bundle.field_provenance
    assert snapshot.serialize() == before  # Twin immutable / unread-write


def test_assembler_fail_open_without_twin_snapshot(learner):
    sid = str(learner["user"].id)
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
        twin_input=TwinInputAdapter(),
    )
    with_flag = assembler.assemble(sid, as_of="2026-07-25")
    without = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
        twin_input=None,
    ).assemble(sid, as_of="2026-07-25")

    # Runtime A primary fields identical whether Twin attach skipped or unavailable.
    assert with_flag.evidence == without.evidence
    assert with_flag.topic_progress == without.topic_progress
    assert with_flag.mission == without.mission
    assert with_flag.curriculum == without.curriculum
    assert with_flag.twin["availability"] == AVAILABILITY_UNAVAILABLE
    assert without.twin == {}


def test_identical_runtime_a_and_twin_yield_identical_bundle(learner):
    sid = str(learner["user"].id)
    twin_assembler = TwinFacetAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
    )
    snapshot = TwinSnapshotBuilder(facet_assembler=twin_assembler).build(
        sid, as_of="2026-07-25"
    )
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
        twin_input=TwinInputAdapter(),
    )
    left = assembler.assemble(sid, as_of="2026-07-25", twin_snapshot=snapshot)
    right = assembler.assemble(sid, as_of="2026-07-25", twin_snapshot=snapshot)
    assert left.serialize() == right.serialize()


def test_executor_deterministic_with_twin_attachment(learner):
    sid = str(learner["user"].id)
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler(
            collectors=_stub_collectors(),
            study_plan_service=_FakePlanService(),
        )
    ).build(sid, as_of="2026-07-25")
    bundle = AdaptiveInputAssembler(
        collectors=_stub_collectors(
            curriculum=_StubCollector(
                "curriculum",
                payload={
                    "leaves": [{"topic_id": "T1", "topic_name": "Intro"}],
                    "leaf_count": 1,
                },
            )
        ),
        study_plan_service=_FakePlanService(),
        twin_input=TwinInputAdapter(),
    ).assemble(sid, as_of="2026-07-25", twin_snapshot=snapshot)
    executor = AdaptiveEngineExecutor()
    left = executor.evaluate(bundle).serialize()
    right = executor.evaluate(bundle).serialize()
    assert left == right


def test_runtime_a_remains_authoritative_primary_input(learner):
    sid = str(learner["user"].id)
    snapshot = TwinSnapshotBuilder(
        facet_assembler=TwinFacetAssembler(
            collectors=_stub_collectors(),
            study_plan_service=_FakePlanService(),
        )
    ).build(sid, as_of="2026-07-25")
    assembler = AdaptiveInputAssembler(
        collectors=_stub_collectors(),
        study_plan_service=_FakePlanService(),
        twin_input=TwinInputAdapter(),
    )
    with_twin = assembler.assemble(sid, as_of="2026-07-25", twin_snapshot=snapshot)
    assert "runtime_a" in with_twin.authority_tags
    assert isinstance(with_twin, AdaptiveInputBundle)
    assert with_twin.twin["availability"] == AVAILABILITY_AVAILABLE


def test_twin_input_module_is_read_only():
    path = ADAPTER_ROOT / "twin_input.py"
    source = path.read_text(encoding="utf-8")
    tree = ast.parse(source)
    for token in FORBIDDEN_WRITE_TOKENS:
        assert token not in source, f"twin_input contains {token}"
    for name in FORBIDDEN_TWIN_SYNTHESIS_CALLS:
        assert name not in source, (
            f"twin_input must not trigger Twin synthesis ({name})"
        )
    for forbidden in FORBIDDEN_EXPERIENCE_IMPORTS:
        assert forbidden not in source
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            assert node.func.attr not in {
                "generate_today_mission",
                "start_session",
                "complete_session",
                "accept_evidence",
                "commit",
                "flush",
            }, f"forbidden write API {node.func.attr}"


def test_no_circular_dependency_twin_input_to_experience():
    twin_input_source = (ADAPTER_ROOT / "twin_input.py").read_text(encoding="utf-8")
    assert "student_experience" not in twin_input_source
    # Twin package must not import TwinInputAdapter (Adaptive consumes Twin).
    for path in TWIN_ROOT.glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom):
                module = node.module or ""
                assert "twin_input" not in module
                for alias in node.names:
                    assert alias.name != "TwinInputAdapter"
            if isinstance(node, ast.Import):
                for alias in node.names:
                    assert "twin_input" not in alias.name
                    assert alias.name != "TwinInputAdapter"

def test_digital_twin_does_not_import_experience_for_t4():
    for path in TWIN_ROOT.glob("*.py"):
        text = path.read_text(encoding="utf-8")
        assert "app.infrastructure.adapters.student_experience" not in text
        assert "ExperienceTwinAdapter" not in text


def test_di_helpers_and_composition_boundary(monkeypatch):
    assert build_twin_input_adapter(enabled=False) is None
    assert build_adaptive_input_assembler(enabled=False) is None
    monkeypatch.setenv("KWALITEC_DIGITAL_TWIN", "1")
    monkeypatch.setenv("KWALITEC_ADAPTIVE_ENGINE", "1")
    composition, _ = build_production_experience()
    assert composition.twin_input_adapter.adapter_id == "twin_input_adapter"
    assert composition.adaptive_input_assembler.twin_input is (
        composition.twin_input_adapter
    )
    # Experience TwinPort remains the prior adapter — T5 adds projection port
    # alongside without UX authority cutover.
    assert composition.twin.__class__.__name__ == "ExperienceTwinAdapter"
    assert composition.student_twin_projection_port is not None
    assert composition.student_twin_projection_port is not composition.twin

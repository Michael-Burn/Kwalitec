"""EP-002.3 — Twin & Authority soak unit tests."""

from __future__ import annotations

from types import MappingProxyType, SimpleNamespace
from unittest.mock import MagicMock

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.adapters.consumer_chain import (
    API_BUILD_DAILY_STUDY_PLAN,
    API_BUILD_READINESS_INTELLIGENCE,
    API_BUILD_STUDY_INSIGHTS,
    CELL_TWIN_OFF_AUTHORITY_ENV,
    CELL_TWIN_OFF_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    assemble_shared_canonical_state,
    build_consumer_chain_telemetry,
    build_twin_authority_soak_orchestrator,
    classify_twin_port,
    evaluate_matrix_cell,
    set_consumer_chain_telemetry,
    verify_authority_fail_open,
    verify_twin_authority_soak_rollback,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    TWINPORT_EXPERIENCE as EXP,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    TWINPORT_FOUNDATION_AUTHORITY as AUTH,
)
from app.infrastructure.adapters.digital_twin.authority import AUTHORITY_ADAPTER_ID
from app.infrastructure.adapters.digital_twin.contracts import (
    AVAILABILITY_AVAILABLE,
)
from app.infrastructure.adapters.digital_twin.foundation import (
    FOUNDATION_VERSION,
    CanonicalLearnerState,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry


def _block(payload: dict) -> dict:
    return {
        "availability": AVAILABILITY_AVAILABLE,
        "unavailable_reason": "",
        "authority": "runtime_a",
        "source_field": "test",
        "evidence_refs": [],
        "payload": payload,
    }


def _canonical_state(student_id: str = "7") -> CanonicalLearnerState:
    return CanonicalLearnerState(
        student_id=student_id,
        as_of="2026-07-26T10:00:00",
        foundation_version=FOUNDATION_VERSION,
        twin_id=f"twin-{student_id}",
        study_state=_block({"exam_readiness": 50.0}),
        topic_mastery=_block({"topics": []}),
        topic_progress=_block({"topics": []}),
        learning_evidence=_block({}),
        practice_performance=_block({}),
        mock_performance=_block({}),
        study_behaviour=_block({}),
        study_consistency=_block({}),
        streaks=_block({"current_streak_days": 1}),
        mission_completion=_block({}),
        facet_labels=MappingProxyType({}),
        limitations_codes=(),
        provenance_refs=(),
        availability=AVAILABILITY_AVAILABLE,
        unavailable_reason="",
    )


@pytest.fixture
def chain_telemetry():
    sink = build_consumer_chain_telemetry(
        structured=StructuredLogger("test.soak.chain"),
        events=EventRegistry(),
    )
    previous = set_consumer_chain_telemetry(sink)
    yield sink
    set_consumer_chain_telemetry(previous)


def _fake_composition(
    *,
    twin_on: bool,
    authority_on: bool,
):
    experience = SimpleNamespace(
        ADAPTER_ID="experience_twin_adapter",
        __class__=type("ExperienceTwinAdapter", (), {}),
    )
    # Rebuild with correct class name for classify_twin_port.
    class ExperienceTwinAdapter:
        ADAPTER_ID = "experience_twin_adapter"

    class StudentTwinFoundationAuthorityPortStub:
        ADAPTER_ID = AUTHORITY_ADAPTER_ID

    experience = ExperienceTwinAdapter()
    foundation = object() if twin_on else None
    if authority_on and twin_on and foundation is not None:
        twin = StudentTwinFoundationAuthorityPortStub()
    else:
        twin = experience
    comp = SimpleNamespace(
        twin=twin,
        twin_foundation=foundation,
        twin_authority_enabled=authority_on and twin_on,
        digital_twin=object() if twin_on else None,
        twin_shadow=object() if twin_on else None,
        twin_facet_assembler=object() if twin_on else None,
        twin_snapshot_builder=object() if twin_on else None,
        twin_explainability=object() if twin_on else None,
        twin_input_adapter=object() if twin_on else None,
        student_twin_projector=object() if twin_on else None,
        student_twin_projection_port=object() if twin_on else None,
        _seed_demo=not (authority_on and twin_on),
    )
    service = SimpleNamespace(name="experience")
    return comp, service


def _factory_from_flags(flags):
    return _fake_composition(
        twin_on=bool(flags.ENABLE_DIGITAL_TWIN),
        authority_on=bool(flags.ENABLE_DIGITAL_TWIN_AUTHORITY),
    )


def test_classify_twin_port():
    class ExperienceTwinAdapter:
        pass

    class StudentTwinFoundationAuthorityPort:
        ADAPTER_ID = AUTHORITY_ADAPTER_ID

    assert classify_twin_port(ExperienceTwinAdapter()) == EXP
    assert classify_twin_port(StudentTwinFoundationAuthorityPort()) == AUTH


def test_flag_matrix_authority_requires_twin():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_DIGITAL_TWIN": "0",
            "KWALITEC_DIGITAL_TWIN_AUTHORITY": "1",
        }
    )
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False


def test_evaluate_matrix_cells_with_fake_composition():
    for cell_id, twin_env, authority_env in (
        (CELL_TWIN_OFF_AUTHORITY_OFF, False, False),
        (CELL_TWIN_OFF_AUTHORITY_ENV, False, True),
        (CELL_TWIN_ON_AUTHORITY_OFF, True, False),
        (CELL_TWIN_ON_AUTHORITY_ON, True, True),
    ):
        cell = evaluate_matrix_cell(
            cell_id=cell_id,
            twin_env=twin_env,
            authority_env=authority_env,
            composition_factory=lambda flags, **_kw: _factory_from_flags(flags),
        )
        assert cell.ok, cell.details
        assert cell.twin_resolved is twin_env
        assert cell.authority_resolved is (twin_env and authority_env)


def test_authority_fail_open():
    class _Fallback:
        def get_learner_summary(self, student_id):  # noqa: ANN001
            return {"student_id": student_id, "authority": "fallback"}

        def get_readiness_summary(self, student_id):  # noqa: ANN001
            return {"authority": "fallback"}

        def get_learning_insights(self, student_id):  # noqa: ANN001
            return {"authority": "fallback"}

    ok, details = verify_authority_fail_open(fallback=_Fallback())
    assert ok
    assert "authority_fail_open_ok" in details


def test_soak_workload_exercises_all_build_apis(chain_telemetry):
    state = _canonical_state()
    foundation = MagicMock()
    foundation.is_enabled.return_value = True
    foundation.assemble.return_value = state

    plan_payload = {
        "mission_slots": [],
        "limitations_codes": (),
    }
    ready_payload = {
        "score": 0.5,
        "limitations_codes": ("sparse_evidence",),
    }
    insight_payload = {
        "todays_focus": "revise",
        "limitations_codes": (),
    }

    orch = build_twin_authority_soak_orchestrator(
        chain_telemetry=chain_telemetry,
        events=EventRegistry(),
        build_plan=lambda user_id, **kw: plan_payload,
        build_readiness=lambda user_id, **kw: ready_payload,
        build_insights=lambda user_id, **kw: insight_payload,
        composition_factory=lambda flags, **_kw: _factory_from_flags(flags),
    )

    # Drive share-hits via assemble helper so foundation telemetry exists.
    assemble_shared_canonical_state(
        foundation,
        "7",
        service_name="PlanningService",
        api_name=API_BUILD_DAILY_STUDY_PLAN,
        telemetry=chain_telemetry,
    )
    assemble_shared_canonical_state(
        foundation,
        "7",
        canonical_state=state,
        service_name="ReadinessService",
        api_name=API_BUILD_READINESS_INTELLIGENCE,
        telemetry=chain_telemetry,
    )
    assemble_shared_canonical_state(
        foundation,
        "7",
        canonical_state=state,
        service_name="RecommendationService",
        api_name=API_BUILD_STUDY_INSIGHTS,
        telemetry=chain_telemetry,
    )

    report = orch.execute_full_soak(
        student_ids=[7, 8],
        iterations=5,
        foundation=foundation,
        canonical_state=state,
        fail_open_fallback=SimpleNamespace(
            get_learner_summary=lambda sid: {"authority": "fallback"},
            get_readiness_summary=lambda sid: {"authority": "fallback"},
            get_learning_insights=lambda sid: {"authority": "fallback"},
        ),
    )

    assert report.requests_exercised == (2 * 5 * 3) + (2 * 2 * 3)  # off + on/2
    assert report.exception_count == 0
    assert report.rollback_success is True
    assert report.behavioural_regressions == 0
    assert report.ok is True
    assert report.foundation_assemble_count >= 1
    assert report.share_hit_count >= 1
    assert report.share_hit_rate > 0
    assert report.average_latency_ms >= 0
    assert report.p95_latency_ms >= 0
    apis = {o.api_name for o in report.observations}
    assert apis == {
        API_BUILD_DAILY_STUDY_PLAN,
        API_BUILD_READINESS_INTELLIGENCE,
        API_BUILD_STUDY_INSIGHTS,
    }
    assert len(report.matrix_cells) == 4
    assert all(c.ok for c in report.matrix_cells)
    assert "sparse_evidence" in report.limitation_code_counts


def test_rollback_restores_pre_soak():
    result = verify_twin_authority_soak_rollback(
        events=EventRegistry(),
        composition_factory=lambda flags, **_kw: _factory_from_flags(flags),
    )
    assert result.ok
    assert result.flags_match_pre_soak
    assert result.authority_off_restores_experience_port
    assert result.twin_off_removes_participation
    assert result.behavioural_regressions == 0


def test_production_defaults_remain_off():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_DIGITAL_TWIN is False
    assert flags.ENABLE_DIGITAL_TWIN_AUTHORITY is False

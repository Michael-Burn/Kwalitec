"""EP-002.3 integration — real Experience composition TwinPort matrix."""

from __future__ import annotations

from app.infrastructure.adapters.consumer_chain import (
    CELL_TWIN_OFF_AUTHORITY_ENV,
    CELL_TWIN_OFF_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_OFF,
    CELL_TWIN_ON_AUTHORITY_ON,
    build_twin_authority_soak_orchestrator,
    evaluate_matrix_cell,
    verify_twin_authority_soak_rollback,
)
from app.infrastructure.adapters.consumer_chain.soak_contracts import (
    TWINPORT_EXPERIENCE,
    TWINPORT_FOUNDATION_AUTHORITY,
)
from app.infrastructure.diagnostics.logging import StructuredLogger
from app.infrastructure.events.registry import EventRegistry


def test_real_composition_matrix_cells():
    expectations = {
        CELL_TWIN_OFF_AUTHORITY_OFF: (False, False, TWINPORT_EXPERIENCE),
        CELL_TWIN_OFF_AUTHORITY_ENV: (False, False, TWINPORT_EXPERIENCE),
        CELL_TWIN_ON_AUTHORITY_OFF: (True, False, TWINPORT_EXPERIENCE),
        CELL_TWIN_ON_AUTHORITY_ON: (True, True, TWINPORT_FOUNDATION_AUTHORITY),
    }
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
        )
        twin_r, auth_r, port = expectations[cell_id]
        assert cell.ok, (cell_id, cell.details)
        assert cell.twin_resolved is twin_r
        assert cell.authority_resolved is auth_r
        assert cell.twin_port_kind == port


def test_real_composition_rollback():
    result = verify_twin_authority_soak_rollback(events=EventRegistry())
    assert result.ok, result.details
    assert result.flags_match_pre_soak
    assert result.behavioural_regressions == 0
    assert result.authority_off_restores_experience_port
    assert result.twin_off_removes_participation


def test_orchestrator_report_shape_with_real_matrix():
    orch = build_twin_authority_soak_orchestrator(
        events=EventRegistry(),
        structured=StructuredLogger("test.soak.integration"),
        build_plan=lambda user_id, **kw: None,
        build_readiness=lambda user_id, **kw: None,
        build_insights=lambda user_id, **kw: None,
    )
    report = orch.execute_full_soak(
        student_ids=[1],
        iterations=2,
        run_matrix=True,
        run_rollback=True,
        fail_open_fallback=type(
            "FB",
            (),
            {
                "get_learner_summary": lambda self, sid: {"authority": "fallback"},
                "get_readiness_summary": lambda self, sid: {"authority": "fallback"},
                "get_learning_insights": lambda self, sid: {"authority": "fallback"},
            },
        )(),
    )
    # Without foundation injection, unavailable is expected — still operational.
    assert report.requests_exercised == (1 * 2 * 3) + (1 * 1 * 3)
    assert report.rollback_success is True
    assert len(report.matrix_cells) == 4
    assert all(c.ok for c in report.matrix_cells)
    assert report.ownership_violations == 0

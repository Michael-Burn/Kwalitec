"""Tests for Version 2 dual-run flags and cutover helpers."""

from __future__ import annotations

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.founder.intelligence import FounderIntelligenceService
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.diagnostics.evidence_gates import build_evidence_gates_report


def test_v2_flags_default_keep_v1_primary():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.ENABLE_STUDENT_EXPERIENCE is False
    assert flags.ENABLE_DURABLE_STORE is False
    assert flags.SOLE_RUNTIME is False
    assert flags.SEED_DEMO_LEARNERS is True


def test_v2_flags_dual_run_disables_demo_when_durable():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_V2_STUDENT_EXPERIENCE": "1",
            "KWALITEC_V2_DURABLE_STORE": "1",
        }
    )
    assert flags.ENABLE_STUDENT_EXPERIENCE is True
    assert flags.ENABLE_DURABLE_STORE is True
    assert flags.INJECT_PHASE_I_ENGINES is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_v2_sole_runtime_implies_student_experience():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_V2_SOLE_RUNTIME": "1"})
    assert flags.SOLE_RUNTIME is True
    assert flags.ENABLE_STUDENT_EXPERIENCE is True


def test_dual_run_status_labels():
    dual = build_dual_run_status(
        flags=resolve_v2_feature_flags(
            environ={"KWALITEC_V2_STUDENT_EXPERIENCE": "1"}
        )
    )
    assert dual.label == "dual-run-active"
    assert len(dual.ready_for_cutover_checklist) == 6


def test_evidence_gates_report_blocks_product_evidence():
    report = build_evidence_gates_report()
    assert any(i.code == "product_evidence" and not i.technical_ready for i in report.items)
    assert report.cutover_blocked is True


def test_founder_intelligence_advisory_empty_without_store():
    snap = FounderIntelligenceService().build(experience_store=None)
    assert snap.signals == ()
    assert "advisory" in snap.notes[0].lower()

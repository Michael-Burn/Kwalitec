"""Sole-runtime protection: Internal Alpha must not silently cut over."""

from __future__ import annotations

from unittest.mock import patch

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.diagnostics.evidence_gates import build_evidence_gates_report
from tests.operational.helpers import ALPHA_DUAL_RUN_ENV, REPO_ROOT, alpha_flags


def test_alpha_env_keeps_sole_runtime_off():
    flags = resolve_v2_feature_flags(environ=dict(ALPHA_DUAL_RUN_ENV))
    assert flags.SOLE_RUNTIME is False


def test_render_enables_sole_runtime_for_rc():
    """V2-023 RC-1: production Render activates sole runtime."""
    from tests.operational.helpers import render_env_map

    assert render_env_map().get("KWALITEC_V2_SOLE_RUNTIME") == "1"


def test_local_alpha_checklist_documents_rollback():
    checklist = (
        REPO_ROOT / "knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md"
    ).read_text(encoding="utf-8")
    assert "KWALITEC_V2_SOLE_RUNTIME" in checklist
    assert "Rollback" in checklist or "unset" in checklist.lower()


def test_dual_run_label_for_alpha_posture():
    status = build_dual_run_status(flags=alpha_flags(SOLE_RUNTIME=False))
    assert status.label == "dual-run-active"
    assert status.sole_runtime is False


def test_sole_runtime_label_only_when_flag_on():
    status = build_dual_run_status(flags=alpha_flags(SOLE_RUNTIME=True))
    assert status.label == "sole-runtime-v2"


def test_product_evidence_never_auto_ready():
    report = build_evidence_gates_report()
    product = next(i for i in report.items if i.code == "product_evidence")
    assert product.technical_ready is False


def test_rollback_unsets_sole_runtime_home(client):
    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=True),
    ):
        sole = client.get("/")
    assert "/student" in sole.headers.get("Location", "")

    with patch(
        "app.application.config.v2_flags.resolve_v2_feature_flags",
        return_value=alpha_flags(SOLE_RUNTIME=False),
    ):
        rolled = client.get("/")
    assert "/dashboard" in rolled.headers.get("Location", "")

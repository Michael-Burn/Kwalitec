"""Configuration alignment: env docs, Render, and flag resolver behaviour."""

from __future__ import annotations

import pytest

from app.application.config.v2_flags import resolve_v2_feature_flags
from app.infrastructure.diagnostics.dual_run import build_dual_run_status
from app.infrastructure.diagnostics.evidence_gates import build_evidence_gates_report
from tests.operational.helpers import (
    ALEMBIC_HEAD,
    ALPHA_DUAL_RUN_ENV,
    ALPHA_ENV_VARS,
    REPO_ROOT,
    render_env_map,
)


def _env_example() -> str:
    return (REPO_ROOT / ".env.example").read_text(encoding="utf-8")


def test_env_example_documents_all_v2_flags():
    text = _env_example()
    for var in ALPHA_ENV_VARS:
        assert var in text


def test_env_example_warns_sole_runtime_is_gated():
    text = _env_example()
    assert "ONLY after evidence gates" in text
    assert "KWALITEC_V2_SOLE_RUNTIME" in text


def test_env_example_does_not_enable_sole_runtime_by_default():
    for line in _env_example().splitlines():
        stripped = line.strip()
        if stripped.startswith("KWALITEC_V2_SOLE_RUNTIME=") and not stripped.startswith(
            "#"
        ):
            pytest.fail("SOLE_RUNTIME must not be actively set in .env.example")


def test_render_sets_dual_run_flags():
    env = render_env_map()
    for key, value in ALPHA_DUAL_RUN_ENV.items():
        actual = env.get(key)
        assert actual == value, f"{key} mismatch: {actual!r}"


def test_render_does_not_set_sole_runtime():
    # Comment may mention the flag; it must not be an active env key.
    assert "KWALITEC_V2_SOLE_RUNTIME" not in render_env_map()


def test_render_generates_secret_key():
    env = render_env_map()
    assert env.get("SECRET_KEY") == "<generateValue>"


def test_render_database_from_managed_db():
    env = render_env_map()
    assert env.get("DATABASE_URL") == "<fromDatabase>"


def test_render_admin_credentials_synced_not_hardcoded():
    env = render_env_map()
    assert env.get("ADMIN_EMAIL") == "<sync:false>"
    assert env.get("ADMIN_PASSWORD") == "<sync:false>"


def test_alpha_dual_run_env_resolves_expected_flags():
    flags = resolve_v2_feature_flags(environ=dict(ALPHA_DUAL_RUN_ENV))
    assert flags.ENABLE_STUDENT_EXPERIENCE is True
    assert flags.ENABLE_DURABLE_STORE is True
    assert flags.INJECT_PHASE_I_ENGINES is True
    assert flags.SEED_DEMO_LEARNERS is False
    assert flags.ENABLE_FOUNDER_INTELLIGENCE is True
    assert flags.SOLE_RUNTIME is False


def test_default_flags_keep_v1_primary():
    flags = resolve_v2_feature_flags(environ={})
    assert flags.SOLE_RUNTIME is False
    assert flags.ENABLE_STUDENT_EXPERIENCE is False
    assert flags.ENABLE_DURABLE_STORE is False


@pytest.mark.parametrize(
    ("raw", "expected"),
    [("1", True), ("true", True), ("0", False), ("", False)],
)
def test_truthy_parsing_for_student_flag(raw, expected):
    flags = resolve_v2_feature_flags(
        environ={"KWALITEC_V2_STUDENT_EXPERIENCE": raw}
    )
    assert flags.ENABLE_STUDENT_EXPERIENCE is expected


def test_durable_implies_engine_injection_and_seed_off():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_V2_DURABLE_STORE": "1"})
    assert flags.INJECT_PHASE_I_ENGINES is True
    assert flags.SEED_DEMO_LEARNERS is False


def test_explicit_seed_override_when_durable():
    flags = resolve_v2_feature_flags(
        environ={
            "KWALITEC_V2_DURABLE_STORE": "1",
            "KWALITEC_V2_SEED_DEMO": "1",
        }
    )
    assert flags.SEED_DEMO_LEARNERS is True


def test_sole_runtime_implies_student_experience():
    flags = resolve_v2_feature_flags(environ={"KWALITEC_V2_SOLE_RUNTIME": "1"})
    assert flags.SOLE_RUNTIME is True
    assert flags.ENABLE_STUDENT_EXPERIENCE is True


def test_dual_run_status_for_alpha_env():
    status = build_dual_run_status(
        flags=resolve_v2_feature_flags(environ=dict(ALPHA_DUAL_RUN_ENV))
    )
    assert status.label == "dual-run-active"
    assert status.sole_runtime is False
    assert status.durable_store is True
    assert len(status.ready_for_cutover_checklist) == 6


def test_evidence_gates_block_product_evidence():
    report = build_evidence_gates_report(
        dual_run=build_dual_run_status(
            flags=resolve_v2_feature_flags(environ=dict(ALPHA_DUAL_RUN_ENV))
        )
    )
    assert report.cutover_blocked is True
    assert any(
        i.code == "product_evidence" and not i.technical_ready for i in report.items
    )


def test_checklist_doc_complete():
    path = REPO_ROOT / "knowledge/version2/INTERNAL_ALPHA_CHECKLIST.md"
    text = path.read_text(encoding="utf-8")
    for needle in (
        "Deployment checklist",
        "Smoke test checklist",
        "Rollback checklist",
        "Known limitations",
        "Success criteria",
        ALEMBIC_HEAD,
        "KWALITEC_V2_SOLE_RUNTIME",
    ):
        assert needle in text


def test_alembic_head_and_migration_files():
    from alembic.script import ScriptDirectory

    sd = ScriptDirectory(str(REPO_ROOT / "migrations"))
    assert sd.get_current_head() == ALEMBIC_HEAD
    versions = REPO_ROOT / "migrations" / "versions"
    assert (versions / "202607190001_create_v2_aggregate_tables.py").is_file()
    assert (versions / "202607190002_merge_v2_aggregate_heads.py").is_file()


def test_secret_key_placeholder_documented():
    text = _env_example()
    assert "change-this-secret-key" in text
    assert "Generate a strong random key" in text

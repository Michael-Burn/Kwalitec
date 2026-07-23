"""GA-001 WS6 — recovery verification (backup export, restore docs, env recreation)."""

from __future__ import annotations

import json

from app.services.database_readiness_service import DatabaseReadinessService
from tests.ga.helpers import (
    REPO_ROOT,
    REQUIRED_PRODUCTION_DOCS,
    login_as,
    make_student,
)
from tests.operational.helpers import render_env_map


class TestDatabaseRestoreVerification:
    def test_migration_status_readable(self, app, ctx) -> None:
        status = DatabaseReadinessService.migration_status(app)
        payload = status.to_dict()
        assert "current" in payload
        assert "head" in payload
        assert "up_to_date" in payload

    def test_schema_audit_runs(self, app, ctx) -> None:
        report = DatabaseReadinessService.schema_audit()
        payload = report.to_dict()
        assert payload["table_count"] >= 1
        assert isinstance(payload["tables"], list)


class TestBackupValidation:
    def test_user_backup_export_roundtrip_shape(self, client, ctx) -> None:
        make_student("ga-backup@kwalitec.example")
        login_as(client, "ga-backup@kwalitec.example")
        response = client.get("/settings/export/backup")
        assert response.status_code == 200
        raw = response.get_data(as_text=True)
        data = json.loads(raw)
        assert isinstance(data, dict)
        # Backup must identify the exporting user without secrets.
        blob = json.dumps(data).lower()
        assert "password" not in blob
        assert "secret" not in blob

    def test_backup_and_recovery_doc_has_restore_steps(self) -> None:
        text = (REPO_ROOT / "docs/production/BACKUP_AND_RECOVERY.md").read_text(
            encoding="utf-8"
        )
        assert "pg_dump" in text
        assert "pg_restore" in text
        assert "/health/ready" in text
        assert "Disaster recovery" in text or "disaster recovery" in text.lower()


class TestConfigurationRecovery:
    def test_environment_doc_lists_required_secrets(self) -> None:
        text = (REPO_ROOT / "docs/production/ENVIRONMENT.md").read_text(
            encoding="utf-8"
        )
        for key in ("SECRET_KEY", "DATABASE_URL", "APP_ENV"):
            assert key in text

    def test_render_yaml_recreates_core_env(self) -> None:
        env = render_env_map()
        assert "SECRET_KEY" in env or any("SECRET" in k for k in env)
        assert "DATABASE_URL" in env or any("DATABASE" in k for k in env)

    def test_deployment_doc_includes_rollback(self) -> None:
        text = (REPO_ROOT / "docs/production/DEPLOYMENT.md").read_text(
            encoding="utf-8"
        )
        assert "Rollback" in text or "rollback" in text
        assert "/health/ready" in text


class TestRecoveryDocumentationPresence:
    def test_all_production_ops_docs_exist(self) -> None:
        missing = [
            path
            for path in REQUIRED_PRODUCTION_DOCS
            if not (REPO_ROOT / path).is_file()
        ]
        assert not missing, f"Missing production docs: {missing}"

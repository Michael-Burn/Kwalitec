"""Production health aggregation (PR-001).

Builds structured health payloads for liveness, readiness, and operator
dashboards without touching educational domain logic.
"""

from __future__ import annotations

import logging
import time
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask, current_app

from app.extensions import db

logger = logging.getLogger("kwalitec.health")


@dataclass(frozen=True)
class ComponentHealth:
    """Health of a single dependency or subsystem."""

    name: str
    status: str  # ok | degraded | error | unavailable
    detail: str = ""
    latency_ms: float | None = None
    meta: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        payload = asdict(self)
        if not payload["meta"]:
            payload.pop("meta")
        if payload["latency_ms"] is None:
            payload.pop("latency_ms")
        if not payload["detail"]:
            payload.pop("detail")
        return payload


class HealthService:
    """Collect application, database, migration, and queue health."""

    @staticmethod
    def check_database(app: Flask | None = None) -> ComponentHealth:
        """Probe the primary database with ``SELECT 1``."""
        flask_app = app or current_app
        threshold = float(flask_app.config.get("HEALTH_ALERT_DB_LATENCY_MS", 500))
        started = time.perf_counter()
        try:
            db.session.execute(db.text("SELECT 1"))
            latency_ms = round((time.perf_counter() - started) * 1000, 1)
            status = "ok" if latency_ms <= threshold else "degraded"
            detail = (
                ""
                if status == "ok"
                else f"latency {latency_ms}ms exceeds alert threshold {threshold}ms"
            )
            return ComponentHealth(
                name="database",
                status=status,
                detail=detail,
                latency_ms=latency_ms,
            )
        except Exception as exc:  # noqa: BLE001
            latency_ms = round((time.perf_counter() - started) * 1000, 1)
            logger.error("Health database probe failed: %s", exc)
            return ComponentHealth(
                name="database",
                status="error",
                detail=exc.__class__.__name__,
                latency_ms=latency_ms,
            )

    @staticmethod
    def check_migrations(app: Flask | None = None) -> ComponentHealth:
        """Compare Alembic DB revision against script head."""
        flask_app = app or current_app
        try:
            migrate_cfg = flask_app.extensions["migrate"]
            migrations_dir = Path(flask_app.root_path).parent / migrate_cfg.directory
            script_dir = ScriptDirectory(str(migrations_dir))
            head_revision = script_dir.get_current_head()
            with db.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current_revision = context.get_current_revision()
            if current_revision is None:
                return ComponentHealth(
                    name="migrations",
                    status="degraded",
                    detail="no alembic_version stamp",
                    meta={"head": head_revision},
                )
            if head_revision and current_revision != head_revision:
                return ComponentHealth(
                    name="migrations",
                    status="degraded",
                    detail="database behind head",
                    meta={"current": current_revision, "head": head_revision},
                )
            return ComponentHealth(
                name="migrations",
                status="ok",
                meta={"current": current_revision, "head": head_revision},
            )
        except Exception as exc:  # noqa: BLE001
            return ComponentHealth(
                name="migrations",
                status="unavailable",
                detail=exc.__class__.__name__,
            )

    @staticmethod
    def check_queue() -> ComponentHealth:
        """Report background job queue health.

        Kwalitec has no Celery/APScheduler broker. Automation runs are
        manually invoked; this probe reports that operational fact.
        """
        return ComponentHealth(
            name="queue",
            status="ok",
            detail="manual automation runner (no external broker)",
            meta={"runner": "app.automation", "broker": "none"},
        )

    @staticmethod
    def check_dependencies() -> list[ComponentHealth]:
        """Lightweight dependency checks (filesystem instance path, etc.)."""
        components: list[ComponentHealth] = []
        try:
            instance_path = Path(current_app.instance_path)
            writable = instance_path.exists() and os_access_writable(instance_path)
            components.append(
                ComponentHealth(
                    name="instance_storage",
                    status="ok" if writable else "degraded",
                    detail="" if writable else "instance path not writable",
                    meta={"path": str(instance_path)},
                )
            )
        except Exception as exc:  # noqa: BLE001
            components.append(
                ComponentHealth(
                    name="instance_storage",
                    status="unavailable",
                    detail=exc.__class__.__name__,
                )
            )
        return components

    @staticmethod
    def aggregate(*, ready: bool = False) -> dict[str, Any]:
        """Build a full health document.

        Args:
            ready: When True, treat migrations-behind as a readiness failure.
        """
        from app.services.release_info_service import ReleaseInfoService
        from app.version import APP_VERSION

        database = HealthService.check_database()
        migrations = HealthService.check_migrations()
        queue = HealthService.check_queue()
        dependencies = HealthService.check_dependencies()
        components = [database, migrations, queue, *dependencies]

        statuses = {c.status for c in components}
        if "error" in statuses:
            overall = "error"
        elif "degraded" in statuses or "unavailable" in statuses:
            overall = "degraded"
        else:
            overall = "ok"

        release = ReleaseInfoService.current()
        payload: dict[str, Any] = {
            "status": overall,
            "timestamp": datetime.now(UTC).isoformat(),
            "version": APP_VERSION,
            "environment": release.environment,
            "build_date": release.build_date,
            "build_number": release.build_number,
            "commit": release.commit,
            "components": {c.name: c.to_dict() for c in components},
            # Backward-compatible top-level database field for existing probes.
            "database": database.status if database.status != "ok" else "connected",
        }
        if ready:
            ready_ok = database.status == "ok" and migrations.status == "ok"
            payload["ready"] = ready_ok
            if not ready_ok and overall == "ok":
                payload["status"] = "degraded"
        return payload


def os_access_writable(path: Path) -> bool:
    """Return whether ``path`` is writable without importing os at module top."""
    import os

    return os.access(path, os.W_OK)

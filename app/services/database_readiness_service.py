"""Database readiness helpers — migration verification and schema audits (PR-001)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from alembic.migration import MigrationContext
from alembic.script import ScriptDirectory
from flask import Flask, current_app
from sqlalchemy import inspect

from app.extensions import db

logger = logging.getLogger("kwalitec.database")


@dataclass
class MigrationStatus:
    """Alembic current vs head comparison."""

    current: str | None
    head: str | None
    up_to_date: bool
    detail: str = ""

    def to_dict(self) -> dict[str, Any]:
        return {
            "current": self.current,
            "head": self.head,
            "up_to_date": self.up_to_date,
            "detail": self.detail,
        }


@dataclass
class SchemaAuditReport:
    """Lightweight index / FK / constraint inventory for operators."""

    tables: list[str] = field(default_factory=list)
    foreign_keys: list[dict[str, Any]] = field(default_factory=list)
    indexes: list[dict[str, Any]] = field(default_factory=list)
    unique_constraints: list[dict[str, Any]] = field(default_factory=list)
    check_constraints: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "table_count": len(self.tables),
            "tables": self.tables,
            "foreign_key_count": len(self.foreign_keys),
            "index_count": len(self.indexes),
            "unique_constraint_count": len(self.unique_constraints),
            "check_constraint_count": len(self.check_constraints),
            "foreign_keys": self.foreign_keys,
            "indexes": self.indexes,
            "unique_constraints": self.unique_constraints,
            "check_constraints": self.check_constraints,
        }


class DatabaseReadinessService:
    """Verify migrations and audit schema metadata."""

    @staticmethod
    def migration_status(app: Flask | None = None) -> MigrationStatus:
        """Return whether the database Alembic stamp matches script head."""
        flask_app = app or current_app
        try:
            migrate_cfg = flask_app.extensions["migrate"]
            migrations_dir = Path(flask_app.root_path).parent / migrate_cfg.directory
            script_dir = ScriptDirectory(str(migrations_dir))
            head = script_dir.get_current_head()
            with db.engine.connect() as connection:
                context = MigrationContext.configure(connection)
                current = context.get_current_revision()
            if current is None:
                return MigrationStatus(
                    current=None,
                    head=head,
                    up_to_date=False,
                    detail="no alembic_version stamp",
                )
            if head is None:
                return MigrationStatus(
                    current=current,
                    head=None,
                    up_to_date=False,
                    detail="no migration scripts on disk",
                )
            up_to_date = current == head
            return MigrationStatus(
                current=current,
                head=head,
                up_to_date=up_to_date,
                detail="ok" if up_to_date else "database behind head",
            )
        except Exception as exc:  # noqa: BLE001
            logger.warning("Migration status check failed: %s", exc)
            return MigrationStatus(
                current=None,
                head=None,
                up_to_date=False,
                detail=exc.__class__.__name__,
            )

    @staticmethod
    def assert_migrations_current(app: Flask | None = None) -> None:
        """Raise ``RuntimeError`` when migrations are behind head."""
        status = DatabaseReadinessService.migration_status(app)
        if not status.up_to_date:
            raise RuntimeError(
                f"Migrations not current: {status.detail} "
                f"(db={status.current}, head={status.head})"
            )

    @staticmethod
    def schema_audit() -> SchemaAuditReport:
        """Inventory tables, indexes, foreign keys, and constraints."""
        inspector = inspect(db.engine)
        report = SchemaAuditReport(tables=sorted(inspector.get_table_names()))
        for table in report.tables:
            for fk in inspector.get_foreign_keys(table):
                report.foreign_keys.append(
                    {
                        "table": table,
                        "constrained_columns": fk.get("constrained_columns"),
                        "referred_table": fk.get("referred_table"),
                        "referred_columns": fk.get("referred_columns"),
                        "name": fk.get("name"),
                    }
                )
            for index in inspector.get_indexes(table):
                report.indexes.append(
                    {
                        "table": table,
                        "name": index.get("name"),
                        "columns": index.get("column_names"),
                        "unique": index.get("unique"),
                    }
                )
            for uc in inspector.get_unique_constraints(table):
                report.unique_constraints.append(
                    {
                        "table": table,
                        "name": uc.get("name"),
                        "columns": uc.get("column_names"),
                    }
                )
            try:
                for cc in inspector.get_check_constraints(table):
                    report.check_constraints.append(
                        {
                            "table": table,
                            "name": cc.get("name"),
                            "sqltext": cc.get("sqltext"),
                        }
                    )
            except NotImplementedError:
                # SQLite / some dialects may not expose check constraints.
                pass
        return report

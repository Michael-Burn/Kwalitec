"""Internal Alpha educational-state reset.

Removes generated learning history while preserving users, curricula,
configuration, and Alembic metadata. This is not a database wipe.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import inspect, text

from app.extensions import db
from app.models.curriculum import Curriculum, Section, Topic
from app.models.decision import Decision
from app.models.learning import LearningObjective, Mistake, StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.twin_snapshot import TwinSnapshot
from app.models.user import User

logger = logging.getLogger(__name__)

# Child tables first so FK constraints remain satisfied during delete.
RESET_MODELS: tuple[type, ...] = (
    Mistake,
    StudyAttempt,
    MissionTask,
    Mission,
    WeekPlan,
    TopicProgress,
    Decision,
    TwinSnapshot,
    StudyPlan,
    Subject,
)

PRESERVED_MODELS: tuple[type, ...] = (
    User,
    Curriculum,
    Section,
    Topic,
    LearningObjective,
)


@dataclass(frozen=True)
class TableCount:
    """Row count for a named table."""

    table: str
    count: int


@dataclass(frozen=True)
class InternalAlphaResetPreview:
    """Inventory shown before confirmation."""

    to_delete: tuple[TableCount, ...]
    preserved: tuple[TableCount, ...]
    total_to_delete: int


@dataclass(frozen=True)
class InternalAlphaResetResult:
    """Per-table deletion report after a successful reset."""

    deleted: tuple[TableCount, ...]
    preserved: tuple[TableCount, ...]
    total_deleted: int


class InternalAlphaResetService:
    """Reset generated educational state for a fair Internal Alpha baseline."""

    @staticmethod
    def preview() -> InternalAlphaResetPreview:
        """Return current row counts for reset and preserved tables."""
        to_delete = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in RESET_MODELS
        )
        preserved = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in PRESERVED_MODELS
        )
        return InternalAlphaResetPreview(
            to_delete=to_delete,
            preserved=preserved,
            total_to_delete=sum(item.count for item in to_delete),
        )

    @staticmethod
    def execute() -> InternalAlphaResetResult:
        """Delete all generated educational rows inside one transaction.

        Preserves users, curricula (including sections/topics/learning
        objectives), and never touches Alembic metadata.

        Returns:
            InternalAlphaResetResult with exact per-table delete counts.

        Raises:
            Exception: Any database error rolls back the whole reset.
        """
        preview = InternalAlphaResetService.preview()
        deleted_counts: list[TableCount] = []

        try:
            for model in RESET_MODELS:
                before = db.session.query(model).count()
                db.session.query(model).delete(synchronize_session=False)
                deleted_counts.append(
                    TableCount(table=model.__tablename__, count=before)
                )

            db.session.commit()
        except Exception:
            db.session.rollback()
            logger.exception("internal-alpha-reset: transaction rolled back")
            raise

        # Clear any process-local TwinRepository handle so retrieval sees
        # the empty durable store immediately within this process.
        try:
            from app.application.twin_repository.shared import (
                reset_shared_twin_repository,
            )

            reset_shared_twin_repository()
        except Exception:
            logger.warning(
                "internal-alpha-reset: shared TwinRepository reset skipped",
                exc_info=True,
            )

        preserved = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in PRESERVED_MODELS
        )
        deleted = tuple(deleted_counts)
        total = sum(item.count for item in deleted)

        logger.info(
            "internal-alpha-reset: deleted %d row(s) across %d table(s); "
            "preserved users=%d curricula=%d",
            total,
            len(deleted),
            next(p.count for p in preserved if p.table == "users"),
            next(p.count for p in preserved if p.table == "curricula"),
        )

        # Sanity: nothing scheduled for delete should remain.
        for model in RESET_MODELS:
            remaining = db.session.query(model).count()
            if remaining != 0:
                raise RuntimeError(
                    f"internal-alpha-reset incomplete: {model.__tablename__} "
                    f"still has {remaining} row(s)"
                )

        # Preserve alembic_version when present (never delete).
        InternalAlphaResetService._assert_alembic_untouched()

        if preview.total_to_delete != total:
            raise RuntimeError(
                "internal-alpha-reset count mismatch: "
                f"preview={preview.total_to_delete} deleted={total}"
            )

        return InternalAlphaResetResult(
            deleted=deleted,
            preserved=preserved,
            total_deleted=total,
        )

    @staticmethod
    def _assert_alembic_untouched() -> None:
        """No-op probe: confirm alembic_version still readable if it exists."""
        inspector = inspect(db.engine)
        if "alembic_version" not in inspector.get_table_names():
            return
        db.session.execute(text("SELECT version_num FROM alembic_version LIMIT 1"))

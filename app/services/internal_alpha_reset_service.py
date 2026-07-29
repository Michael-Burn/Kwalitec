"""Founder / Internal Alpha educational-state reset.

Removes learner-generated operational artefacts while preserving users,
canonical curricula, Curriculum Studio configuration, published curriculum
metadata, and Alembic history. This is not a database wipe.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sqlalchemy import inspect, text

from app.extensions import db
from app.models.analytics_events import (
    AnalyticsAuditLogRecord,
    AnalyticsEventRecord,
    AnalyticsOutboxRecord,
)
from app.models.curriculum import Curriculum, Section, Topic
from app.models.curriculum_studio_foundation import (
    PublishedCurriculumPackage,
    StudioFoundationAuditEvent,
    StudioFoundationDocument,
    StudioFoundationSubject,
    StudioFoundationVersion,
)
from app.models.decision import Decision
from app.models.educational_runtime_engine import (
    RuntimeEducationalEvent,
    RuntimeEnrolment,
    RuntimeMissionInstance,
    RuntimeStudyPlanInstance,
)
from app.models.learning import LearningObjective, Mistake, StudyAttempt
from app.models.mission import Mission, MissionTask
from app.models.platform_integration import RuntimeEnrolmentRoutingAudit
from app.models.recommendation_commitment import RecommendationCommitment
from app.models.research_feedback import (
    ResearchContribution,
    ResearchContributorBadge,
    ResearchFeedbackReview,
    ResearchFeedbackStatusTransition,
    ResearchFeedbackSubmission,
    ResearchFounderNote,
    ResearchProductFinding,
    ResearchProductFindingLink,
    ResearchProductFindingStatusTransition,
)
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from app.models.student_digital_twin import (
    SdtKnowledgeGap,
    SdtLearningStateSnapshot,
    SdtMasteryRecord,
    SdtObservation,
    SdtPrediction,
    SdtReasoningHistory,
    SdtRecommendation,
    SdtStudentDigitalTwin,
)
from app.models.study_plan import StudyPlan, WeekPlan
from app.models.subject import Subject
from app.models.topic_progress import TopicProgress
from app.models.twin_snapshot import TwinSnapshot
from app.models.user import User
from app.models.v2_aggregate import (
    V2AggregateDocument,
    V2AggregateSnapshot,
    V2EvidenceEvent,
)

logger = logging.getLogger(__name__)

# Child tables first so FK constraints remain satisfied during delete.
RESET_MODELS: tuple[type, ...] = (
    # Research feedback graph (children → submissions)
    ResearchProductFindingLink,
    ResearchProductFindingStatusTransition,
    ResearchProductFinding,
    ResearchFounderNote,
    ResearchFeedbackStatusTransition,
    ResearchFeedbackReview,
    ResearchContributorBadge,
    ResearchContribution,
    ResearchFeedbackSubmission,
    # Analytics / durable aggregates
    AnalyticsAuditLogRecord,
    AnalyticsOutboxRecord,
    AnalyticsEventRecord,
    V2EvidenceEvent,
    V2AggregateSnapshot,
    V2AggregateDocument,
    # Runtime C / SCI learner bindings
    RuntimeEducationalEvent,
    RuntimeMissionInstance,
    RuntimeStudyPlanInstance,
    RuntimeEnrolment,
    RuntimeEnrolmentRoutingAudit,
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
    # Student digital twin projections
    SdtReasoningHistory,
    SdtPrediction,
    SdtRecommendation,
    SdtKnowledgeGap,
    SdtMasteryRecord,
    SdtObservation,
    SdtLearningStateSnapshot,
    SdtStudentDigitalTwin,
    # Recommendation commitments
    RecommendationCommitment,
    # Runtime A educational history
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
    PublishedCurriculumPackage,
    StudioFoundationSubject,
    StudioFoundationVersion,
    StudioFoundationDocument,
    StudioFoundationAuditEvent,
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
    """Canonical Founder / Internal Alpha educational-state reset."""

    @staticmethod
    def _models_with_tables(models: tuple[type, ...]) -> tuple[type, ...]:
        """Return only models whose tables exist in the current database."""
        inspector = inspect(db.engine)
        present = set(inspector.get_table_names())
        return tuple(model for model in models if model.__tablename__ in present)

    @staticmethod
    def preview() -> InternalAlphaResetPreview:
        """Return current row counts for reset and preserved tables."""
        reset_models = InternalAlphaResetService._models_with_tables(RESET_MODELS)
        preserved_models = InternalAlphaResetService._models_with_tables(
            PRESERVED_MODELS
        )
        to_delete = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in reset_models
        )
        preserved = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in preserved_models
        )
        return InternalAlphaResetPreview(
            to_delete=to_delete,
            preserved=preserved,
            total_to_delete=sum(item.count for item in to_delete),
        )

    @staticmethod
    def execute() -> InternalAlphaResetResult:
        """Delete all learner-generated operational rows inside one transaction.

        Preserves users (Founder / Administrator and any other accounts),
        canonical curricula (including sections / topics / learning objectives),
        Curriculum Studio configuration, published curriculum metadata, and
        never touches Alembic metadata.

        Returns:
            InternalAlphaResetResult with exact per-table delete counts.

        Raises:
            Exception: Any database error rolls back the whole reset.
        """
        preview = InternalAlphaResetService.preview()
        reset_models = InternalAlphaResetService._models_with_tables(RESET_MODELS)
        deleted_counts: list[TableCount] = []

        try:
            for model in reset_models:
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

        preserved_models = InternalAlphaResetService._models_with_tables(
            PRESERVED_MODELS
        )
        preserved = tuple(
            TableCount(table=model.__tablename__, count=db.session.query(model).count())
            for model in preserved_models
        )
        deleted = tuple(deleted_counts)
        total = sum(item.count for item in deleted)

        users_preserved = next((p.count for p in preserved if p.table == "users"), 0)
        curricula_preserved = next(
            (p.count for p in preserved if p.table == "curricula"), 0
        )

        logger.info(
            "internal-alpha-reset: deleted %d row(s) across %d table(s); "
            "preserved users=%d curricula=%d",
            total,
            len(deleted),
            users_preserved,
            curricula_preserved,
        )

        # Sanity: nothing scheduled for delete should remain.
        for model in reset_models:
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

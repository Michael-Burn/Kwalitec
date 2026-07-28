"""Educational Intelligence adoption metrics (RI-002).

Observational coverage + RIS telemetry aggregation only.
Does not reason, present, or mutate educational state.
"""

from __future__ import annotations

from datetime import UTC, datetime

from sqlalchemy import distinct, func

from app.application.runtime_integration.dto import (
    AdoptionMetricsReport,
    CoverageMetric,
    TelemetrySnapshot,
)
from app.application.runtime_integration.telemetry import (
    DEFAULT_TELEMETRY,
    RuntimeIntegrationTelemetry,
)
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgGraphEdition
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import SciStudentCurriculumInstance
from app.models.study_plan import StudyPlan


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class AdoptionMetricsService:
    """Compute objective EI adoption metrics for operators."""

    def __init__(
        self,
        *,
        telemetry: RuntimeIntegrationTelemetry | None = None,
    ) -> None:
        self._telemetry = telemetry or DEFAULT_TELEMETRY

    def build_report(self) -> AdoptionMetricsReport:
        """Assemble coverage metrics and process-scoped RIS telemetry."""
        snap = self._telemetry.snapshot()
        route_usage = tuple(
            snap.by_surface[key] for key in sorted(snap.by_surface.keys())
        )
        return AdoptionMetricsReport(
            sci_coverage=self.sci_coverage(),
            published_curriculum_coverage=self.published_curriculum_coverage(),
            educational_decision_coverage=self.educational_decision_coverage(),
            experience_model_generation_rate=snap.experience_model_generation_rate,
            runtime_a_fallback_rate=snap.fallback_rate,
            educational_intelligence_request_pct=(
                snap.educational_intelligence_adoption_pct
            ),
            route_level_usage=route_usage,
            fallback_by_reason=dict(snap.fallback_by_reason),
            telemetry=snap,
            computed_at=_utc_now_iso(),
        )

    @staticmethod
    def sci_coverage() -> CoverageMetric:
        """Share of active-plan students with ≥1 active SCI."""
        plan_students = (
            db.session.query(func.count(distinct(StudyPlan.user_id)))
            .filter(StudyPlan.active.is_(True), StudyPlan.archived.is_(False))
            .scalar()
        )
        denominator = int(plan_students or 0)

        sci_students = (
            db.session.query(func.count(distinct(SciStudentCurriculumInstance.student_id)))
            .filter(SciStudentCurriculumInstance.is_active.is_(True))
            .scalar()
        )
        # Bound numerator to students who also have an active plan when plans exist.
        if denominator > 0:
            covered = (
                db.session.query(
                    func.count(distinct(SciStudentCurriculumInstance.student_id))
                )
                .join(
                    StudyPlan,
                    StudyPlan.user_id == SciStudentCurriculumInstance.student_id,
                )
                .filter(
                    SciStudentCurriculumInstance.is_active.is_(True),
                    StudyPlan.active.is_(True),
                    StudyPlan.archived.is_(False),
                )
                .scalar()
            )
            numerator = int(covered or 0)
        else:
            numerator = int(sci_students or 0)
            denominator = max(numerator, 0)

        return CoverageMetric(
            metric_id="sci_coverage",
            label="SCI coverage",
            numerator=numerator,
            denominator=denominator,
            definition=(
                "Distinct students with an active study plan who also have ≥1 "
                "active Student Curriculum Instance."
            ),
        )

    @staticmethod
    def published_curriculum_coverage() -> CoverageMetric:
        """Share of CKG subject codes that have ≥1 published edition."""
        subjects_total = (
            db.session.query(func.count(distinct(CkgGraphEdition.subject_code))).scalar()
        )
        denominator = int(subjects_total or 0)
        published = (
            db.session.query(func.count(distinct(CkgGraphEdition.subject_code)))
            .filter(CkgGraphEdition.publication_state == "published")
            .scalar()
        )
        numerator = int(published or 0)
        return CoverageMetric(
            metric_id="published_curriculum_coverage",
            label="Published curriculum coverage",
            numerator=numerator,
            denominator=denominator,
            definition=(
                "Distinct subject codes with ≥1 published CKG edition, "
                "over all subject codes that have any CKG edition."
            ),
        )

    @staticmethod
    def educational_decision_coverage() -> CoverageMetric:
        """Share of active SCIs that have ≥1 persisted Educational Decision."""
        active_instances = (
            db.session.query(func.count(SciStudentCurriculumInstance.id))
            .filter(SciStudentCurriculumInstance.is_active.is_(True))
            .scalar()
        )
        denominator = int(active_instances or 0)
        with_decisions = (
            db.session.query(
                func.count(distinct(EreEducationalDecision.instance_id))
            )
            .join(
                SciStudentCurriculumInstance,
                SciStudentCurriculumInstance.instance_id
                == EreEducationalDecision.instance_id,
            )
            .filter(SciStudentCurriculumInstance.is_active.is_(True))
            .scalar()
        )
        numerator = int(with_decisions or 0)
        return CoverageMetric(
            metric_id="educational_decision_coverage",
            label="Educational Decision coverage",
            numerator=numerator,
            denominator=denominator,
            definition=(
                "Active Student Curriculum Instances that have ≥1 persisted "
                "EI-007 Educational Decision."
            ),
        )

    def telemetry_snapshot(self) -> TelemetrySnapshot:
        return self._telemetry.snapshot()

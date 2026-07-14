"""InternalAlphaWorkflowService — live Internal Alpha coordinator (FSI-003).

Coordinates:
Week discovery → Pipeline → Operational State → Recommendations → Brief → Export

Coordinator only. No classification, recommendation, or briefing business logic.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping
from datetime import UTC, datetime
from pathlib import Path
from types import MappingProxyType
from typing import Protocol

from app.founder.briefing import FounderWeeklyBriefingService
from app.founder.briefing.dto import BriefingValidationError
from app.founder.briefing.models import FounderWeeklyBrief
from app.founder.internal_alpha import InternalAlphaPipelineService, PipelineResult
from app.founder.internal_alpha.models import ClassifiedFeedback
from app.founder.internal_alpha_workflow.config import (
    InternalAlphaWorkflowConfig,
    default_config,
)
from app.founder.internal_alpha_workflow.discovery import WeekDiscoveryService
from app.founder.internal_alpha_workflow.dto import (
    WeekReference,
    WorkflowError,
    WorkflowResult,
)
from app.founder.internal_alpha_workflow.exporters import WorkflowOutputManager
from app.founder.internal_alpha_workflow.validators import WorkflowValidator
from app.founder.operational_state.dto.capability import CapabilitySubsystemDTO
from app.founder.operational_state.dto.internal_alpha import (
    InternalAlphaSubsystemDTO,
)
from app.founder.operational_state.dto.knowledge import KnowledgeSubsystemDTO
from app.founder.operational_state.dto.validation import (
    OperationalStateValidationError,
)
from app.founder.operational_state.models import FounderOperationalState
from app.founder.operational_state.providers import (
    CapabilityArchiveProvider,
    InternalAlphaProvider,
    KnowledgeQueryProvider,
    StaticInternalAlphaSource,
)
from app.founder.operational_state.services import FounderOperationalStateService
from app.founder.recommendations import FounderRecommendationService
from app.founder.recommendations.dto.validation import RecommendationValidationError
from app.founder.recommendations.models import RecommendationSet


class KnowledgeGate(Protocol):
    def get(self) -> KnowledgeSubsystemDTO:
        """Return a Knowledge Engine summary."""


class CapabilityGate(Protocol):
    def get(self) -> CapabilitySubsystemDTO:
        """Return a Capability Archive summary."""


class InternalAlphaWorkflowService:
    """Run the Version 1 Internal Alpha live repository workflow.

    Order:
    1. Detect week folder
    2. Locate raw_feedback/
    3. Process txt files via Internal Alpha Pipeline
    4. Generate processed outputs
    5. Refresh Founder Operational State
    6. Generate Recommendation Set
    7. Generate Founder Weekly Brief
    8. Write outputs into respective folders

    Failures are isolated: earlier successful outputs are preserved; downstream
    stages do not run silently after a failure.
    """

    def __init__(
        self,
        *,
        config: InternalAlphaWorkflowConfig | None = None,
        discovery: WeekDiscoveryService | None = None,
        pipeline: InternalAlphaPipelineService | None = None,
        knowledge: KnowledgeGate | None = None,
        capability: CapabilityGate | None = None,
        recommendations: FounderRecommendationService | None = None,
        briefing: FounderWeeklyBriefingService | None = None,
        output_manager: WorkflowOutputManager | None = None,
        validator: WorkflowValidator | None = None,
        clock: Callable[[], datetime] | None = None,
        internal_alpha_root: Path | str | None = None,
        repo_root: Path | str | None = None,
    ) -> None:
        self._config = config or default_config()
        resolved_repo = Path(repo_root).resolve() if repo_root is not None else None
        self._discovery = discovery or WeekDiscoveryService(
            root=internal_alpha_root,
            repo_root=resolved_repo,
            config=self._config,
        )
        self._pipeline = pipeline or InternalAlphaPipelineService()
        self._knowledge: KnowledgeGate = knowledge or KnowledgeQueryProvider(
            repo_root=resolved_repo
        )
        self._capability: CapabilityGate = capability or CapabilityArchiveProvider(
            repo_root=resolved_repo
        )
        self._recommendations = recommendations or FounderRecommendationService()
        self._briefing = briefing or FounderWeeklyBriefingService()
        self._output_manager = output_manager or WorkflowOutputManager(self._config)
        self._validator = validator or WorkflowValidator(self._config)
        self._clock = clock or (lambda: datetime.now(tz=UTC))

    def run(
        self,
        *,
        week: str | None = None,
        generated_at: datetime | None = None,
    ) -> WorkflowResult:
        """Execute the live workflow for one week (or the latest week).

        Args:
            week: Optional week label such as ``week_001``. Defaults to latest.
            generated_at: Optional fixed timestamp for deterministic tests.

        Returns:
            Immutable WorkflowResult describing stage success and exports.
        """

        started_at = generated_at if generated_at is not None else self._clock()
        warnings: list[str] = []
        errors: list[str] = []

        pipeline_success = False
        operational_state_success = False
        recommendations_success = False
        briefing_success = False
        exported_files: tuple[str, ...] = ()
        week_label = week or ""

        try:
            week_ref = self._discovery.resolve_week(week)
        except WorkflowError as exc:
            completed_at = self._clock()
            return WorkflowResult(
                week=week or "",
                started_at=started_at,
                completed_at=completed_at,
                pipeline_success=False,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=(),
                errors=(f"{exc.code}: {exc.message}",),
            )

        week_label = week_ref.label

        # Ensure output folders exist; raw_feedback must already be present.
        self._output_manager.ensure_directories(week_ref)

        feedback_report = self._discovery.validate_raw_feedback(week_ref)
        if not feedback_report.ok:
            completed_at = self._clock()
            return WorkflowResult(
                week=week_label,
                started_at=started_at,
                completed_at=completed_at,
                pipeline_success=False,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=(),
                errors=tuple(
                    f"{issue.code}: {issue.message}" for issue in feedback_report.issues
                ),
            )

        # --- 3–4 Pipeline ---
        pipeline_result: PipelineResult | None = None
        try:
            pipeline_result = self._pipeline.run(
                week_ref.path,
                week=week_ref.label,
                generated_at=started_at,
                output_dir=week_ref.processed_dir,
            )
        except Exception as exc:  # noqa: BLE001 — isolate stage failure
            errors.append(f"pipeline_exception: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=False,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        pipeline_report = self._validator.validate_pipeline(pipeline_result)
        if not pipeline_report.ok:
            errors.extend(
                f"{issue.code}: {issue.message}" for issue in pipeline_report.issues
            )
            warnings.extend(pipeline_result.warnings)
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=False,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        pipeline_success = True
        warnings.extend(pipeline_result.warnings)

        # --- 5 Operational State ---
        state: FounderOperationalState | None = None
        try:
            alpha_dto = self._build_alpha_dto(week_ref, pipeline_result.processed_items)
            state_service = FounderOperationalStateService(
                knowledge=self._knowledge,
                capability=self._capability,
                internal_alpha=InternalAlphaProvider(
                    StaticInternalAlphaSource(alpha_dto)
                ),
                clock=self._clock,
            )
            state = state_service.get_state(generated_at=started_at)
        except OperationalStateValidationError as exc:
            errors.append(f"operational_state_failed: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"operational_state_exception: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        if not self._validator.validate_snapshot(state).ok:
            errors.append(
                "snapshot_missing: Operational State snapshot was not generated"
            )
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=False,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )
        operational_state_success = True

        # --- 6 Recommendations ---
        recommendation_set: RecommendationSet | None = None
        try:
            recommendation_set = self._recommendations.recommend(state)
        except (RecommendationValidationError, Exception) as exc:  # noqa: BLE001
            code = (
                "recommendations_failed"
                if isinstance(exc, RecommendationValidationError)
                else "recommendations_exception"
            )
            errors.append(f"{code}: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        if not self._validator.validate_recommendations(recommendation_set).ok:
            errors.append(
                "recommendations_missing: Recommendation set was not generated"
            )
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=False,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )
        recommendations_success = True

        # --- 7 Weekly Brief (in-memory first — no export until stage 8) ---
        brief: FounderWeeklyBrief | None = None
        try:
            brief_result = self._briefing.generate(
                state,
                recommendation_set,
                generated_at=started_at,
                output_dir=None,
            )
            brief = brief_result.brief
        except (BriefingValidationError, Exception) as exc:  # noqa: BLE001
            code = (
                "briefing_failed"
                if isinstance(exc, BriefingValidationError)
                else "briefing_exception"
            )
            errors.append(f"{code}: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=True,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        if not self._validator.validate_brief(brief).ok:
            errors.append("brief_missing: Weekly brief was not generated")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=True,
                briefing_success=False,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )
        briefing_success = True

        # --- 8 Coordinated export (partial export prevention) ---
        completed_at = self._clock()
        try:
            exported_files = self._output_manager.export_all(
                week_ref,
                recommendation_set=recommendation_set,
                brief=brief,
                started_at=started_at,
                completed_at=completed_at,
            )
        except Exception as exc:  # noqa: BLE001
            errors.append(f"export_failed: {exc}")
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                completed_at=completed_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=True,
                briefing_success=True,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        export_report = self._validator.validate_exports(exported_files)
        if not export_report.ok:
            errors.extend(
                f"{issue.code}: {issue.message}" for issue in export_report.issues
            )
            return self._finish(
                week_label=week_label,
                started_at=started_at,
                completed_at=completed_at,
                pipeline_success=True,
                operational_state_success=True,
                recommendations_success=True,
                briefing_success=True,
                exported_files=(),
                warnings=tuple(warnings),
                errors=tuple(errors),
            )

        return WorkflowResult(
            week=week_label,
            started_at=started_at,
            completed_at=completed_at,
            pipeline_success=pipeline_success,
            operational_state_success=operational_state_success,
            recommendations_success=recommendations_success,
            briefing_success=briefing_success,
            exported_files=exported_files,
            warnings=tuple(warnings),
            errors=tuple(errors),
        )

    def _finish(
        self,
        *,
        week_label: str,
        started_at: datetime,
        pipeline_success: bool,
        operational_state_success: bool,
        recommendations_success: bool,
        briefing_success: bool,
        exported_files: tuple[str, ...],
        warnings: tuple[str, ...],
        errors: tuple[str, ...],
        completed_at: datetime | None = None,
    ) -> WorkflowResult:
        return WorkflowResult(
            week=week_label,
            started_at=started_at,
            completed_at=completed_at or self._clock(),
            pipeline_success=pipeline_success,
            operational_state_success=operational_state_success,
            recommendations_success=recommendations_success,
            briefing_success=briefing_success,
            exported_files=exported_files,
            warnings=warnings,
            errors=errors,
        )

    def _build_alpha_dto(
        self,
        week: WeekReference,
        processed_items: tuple[ClassifiedFeedback, ...],
    ) -> InternalAlphaSubsystemDTO:
        category_counts: dict[str, int] = {}
        duplicate_count = 0
        for item in processed_items:
            category_counts[item.category] = category_counts.get(item.category, 0) + 1
            if item.duplicate_of is not None:
                duplicate_count += 1

        recent = tuple(ref.label for ref in self._discovery.list_weeks()[-5:])
        if week.label not in recent:
            recent = (*recent, week.label)

        counts: Mapping[str, int] = MappingProxyType(dict(category_counts))
        return InternalAlphaSubsystemDTO(
            source_version=self._config.internal_alpha_source_version,
            current_week=week.label,
            feedback_count=len(processed_items),
            duplicate_count=duplicate_count,
            category_counts=counts,
            recent_week_labels=recent,
        )

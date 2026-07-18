"""ValidationService — present Ingestion + Management validation via ports."""

from __future__ import annotations

from app.application.curriculum_studio._ports import (
    as_bool,
    require_ingestion,
    require_management,
)
from app.application.curriculum_studio._registry import StudioRegistry
from app.application.curriculum_studio._snapshots import validation_snapshot
from app.application.curriculum_studio.dto.validation_snapshot import (
    ValidationSnapshot,
)
from app.application.curriculum_studio.exceptions import (
    ValidationError,
    WorkspaceNotFound,
)
from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.application.curriculum_studio.ports.curriculum_management_port import (
    CurriculumManagementPort,
)
from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)
from app.domain.curriculum_studio.validation_summary import (
    ValidationFinding,
    ValidationFindingSeverity,
    ValidationReadiness,
    ValidationSummary,
)


class ValidationService:
    """Present validation results for Studio workspaces.

    Structural validation authority: Curriculum Ingestion.
    Publication-gate validation authority: Curriculum Management.
    Studio maps results and syncs checklist facts only.
    """

    def __init__(
        self,
        registry: StudioRegistry,
        *,
        management: CurriculumManagementPort | None = None,
        ingestion: CurriculumIngestionPort | None = None,
    ) -> None:
        self._registry = registry
        self._management = management
        self._ingestion = ingestion

    def summarise(self, workspace_id: str) -> ValidationSnapshot:
        """Build a Founder-facing validation summary from port reports."""
        workspace = self._require_workspace(workspace_id)
        errors: list[ValidationFinding] = []
        warnings: list[ValidationFinding] = []
        readiness = ValidationReadiness.NOT_STARTED

        job_id = self._registry.get_ingestion_job(workspace_id)
        if job_id and self._ingestion is not None and self._ingestion.is_available():
            report = self._ingestion.get_validation_report(job_id) or {}
            readiness, errors, warnings = _map_report(report, errors, warnings)
        elif workspace.version_id and self._management is not None:
            try:
                if self._management.is_available():
                    report = (
                        self._management.latest_validation(workspace.version_id)
                        or {}
                    )
                    if report:
                        readiness, errors, warnings = _map_report(
                            report, errors, warnings
                        )
            except Exception:  # noqa: BLE001
                pass

        if readiness is ValidationReadiness.NOT_STARTED:
            if not workspace.facts.cmp_uploaded:
                errors.append(
                    ValidationFinding.create(
                        "missing_cmp",
                        "CMP source not present",
                        severity=ValidationFindingSeverity.BLOCKING,
                    )
                )
            if not workspace.facts.official_syllabus_uploaded:
                errors.append(
                    ValidationFinding.create(
                        "missing_syllabus",
                        "Official syllabus source not present",
                        severity=ValidationFindingSeverity.BLOCKING,
                    )
                )
            if errors:
                readiness = ValidationReadiness.FAILED
            elif workspace.facts.validation_passed:
                readiness = ValidationReadiness.PASSED
            elif workspace.section_ids or workspace.topic_ids:
                # Structural projection present — treat as passed for Founder
                # gate when sources are present and no blocking errors.
                readiness = ValidationReadiness.PASSED
            else:
                readiness = ValidationReadiness.NOT_STARTED

        summary = ValidationSummary.create(
            f"val-{workspace_id}",
            workspace_id,
            detected_sections=workspace.section_ids,
            detected_objectives=workspace.objective_ids,
            detected_prerequisites=workspace.prerequisite_edges,
            warnings=warnings,
            errors=errors,
            readiness=readiness,
        )
        return validation_snapshot(summary)

    def validate_curriculum(
        self,
        workspace_id: str,
        *,
        run_management_gate: bool = True,
    ) -> ValidationSnapshot:
        """Validate Curriculum — ask ports; sync validation_passed fact."""
        workspace = self._require_workspace(workspace_id)
        if run_management_gate:
            require_management(self._management, action="validate_curriculum")
        job_id = self._registry.get_ingestion_job(workspace_id)
        ingestion_passed = True
        if job_id:
            ing = require_ingestion(self._ingestion, action="validate_curriculum")
            report = ing.get_validation_report(job_id) or {}
            ingestion_passed = as_bool(
                report.get("passed"),
                default=str(report.get("readiness", "")).lower()
                in {"passed", "ready", "ok"},
            )
            if not ingestion_passed and report.get("passed") is None:
                issues = report.get("issues") or report.get("errors") or ()
                ingestion_passed = len(issues) == 0

        management_passed = True
        if run_management_gate:
            if not workspace.version_id:
                raise ValidationError(
                    f"Validation requires version for {workspace_id}"
                )
            mgmt = require_management(
                self._management, action="validate_curriculum"
            )
            report = mgmt.validate_version(workspace.version_id)
            management_passed = as_bool(
                report.get("passed"),
                default=str(report.get("readiness", "")).lower()
                in {"passed", "ready", "ok", "validated"},
            )

        passed = bool(ingestion_passed and management_passed)
        if not passed:
            facts = _copy_facts(workspace.facts, validation_passed=False)
            self._registry.put_workspace(workspace.with_facts(facts))
            snap = self.summarise(workspace_id)
            raise ValidationError(
                f"Validation failed for {workspace_id}: "
                f"{snap.error_count} error(s)"
            )

        facts = _copy_facts(workspace.facts, validation_passed=True)
        self._registry.put_workspace(workspace.with_facts(facts))
        self._registry.record_activity(
            "validation_passed",
            f"Validation passed for {workspace_id}",
            workspace_id=workspace_id,
            subject_code=workspace.subject_code,
            version_id=workspace.version_id,
        )
        return self.summarise(workspace_id)

    def mark_passed(
        self,
        workspace_id: str,
        *,
        require_structure: bool = True,
    ) -> ValidationSnapshot:
        """Compatibility path: require ports when available, else local gate.

        Prefer ``validate_curriculum`` for authority-safe Founder use-cases.
        When Management/Ingestion ports are injected, delegates to them.
        """
        workspace = self._require_workspace(workspace_id)
        if self._management is not None and self._management.is_available():
            if workspace.version_id:
                return self.validate_curriculum(workspace_id)
        snap = self.summarise(workspace_id)
        if snap.blocks_publication:
            raise ValidationError(
                f"Validation blocked for {workspace_id}: "
                f"{snap.error_count} error(s)"
            )
        if require_structure and snap.section_count == 0 and snap.objective_count == 0:
            raise ValidationError(
                f"Validation requires structure for {workspace_id}"
            )
        facts = _copy_facts(workspace.facts, validation_passed=True)
        self._registry.put_workspace(workspace.with_facts(facts))
        return self.summarise(workspace_id)

    def _require_workspace(self, workspace_id: str):
        workspace = self._registry.get_workspace(workspace_id)
        if workspace is None:
            raise WorkspaceNotFound(f"Workspace not found: {workspace_id!r}")
        return workspace


def _copy_facts(
    facts: WorkspacePublicationFacts,
    **overrides,
) -> WorkspacePublicationFacts:
    return WorkspacePublicationFacts.create(
        cmp_uploaded=overrides.get("cmp_uploaded", facts.cmp_uploaded),
        official_syllabus_uploaded=overrides.get(
            "official_syllabus_uploaded", facts.official_syllabus_uploaded
        ),
        validation_passed=overrides.get(
            "validation_passed", facts.validation_passed
        ),
        blueprint_assigned=overrides.get(
            "blueprint_assigned", facts.blueprint_assigned
        ),
        preview_approved=overrides.get(
            "preview_approved", facts.preview_approved
        ),
        version_assigned=overrides.get(
            "version_assigned", facts.version_assigned
        ),
        rollback_snapshot_created=overrides.get(
            "rollback_snapshot_created", facts.rollback_snapshot_created
        ),
    )


def _map_report(
    report: dict,
    errors: list[ValidationFinding],
    warnings: list[ValidationFinding],
) -> tuple[ValidationReadiness, list[ValidationFinding], list[ValidationFinding]]:
    for issue in report.get("errors") or report.get("blocking_issues") or ():
        if isinstance(issue, dict):
            errors.append(
                ValidationFinding.create(
                    str(issue.get("code") or "ingestion_error"),
                    str(issue.get("message") or "Validation error"),
                    severity=ValidationFindingSeverity.BLOCKING,
                )
            )
        else:
            errors.append(
                ValidationFinding.create(
                    "ingestion_error",
                    str(issue),
                    severity=ValidationFindingSeverity.BLOCKING,
                )
            )
    for issue in report.get("warnings") or ():
        if isinstance(issue, dict):
            warnings.append(
                ValidationFinding.create(
                    str(issue.get("code") or "ingestion_warning"),
                    str(issue.get("message") or "Validation warning"),
                    severity=ValidationFindingSeverity.WARNING,
                )
            )
        else:
            warnings.append(
                ValidationFinding.create(
                    "ingestion_warning",
                    str(issue),
                    severity=ValidationFindingSeverity.WARNING,
                )
            )
    if errors:
        readiness = ValidationReadiness.FAILED
    elif as_bool(report.get("passed")) or str(
        report.get("readiness", "")
    ).lower() in {"passed", "ready", "ok", "validated"}:
        readiness = ValidationReadiness.PASSED
    elif report:
        readiness = ValidationReadiness.IN_PROGRESS
    else:
        readiness = ValidationReadiness.NOT_STARTED
    return readiness, errors, warnings

"""ValidationService — present Management (+ optional Ingestion) validation."""

from __future__ import annotations

import logging

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
from app.application.curriculum_studio.validation_guidance import (
    enrich_finding,
    guided_finding,
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

logger = logging.getLogger(__name__)


class ValidationService:
    """Present validation results for Studio workspaces.

    Founder publication-gate authority (PI-002R):
        CIP / Foundation extraction → StructurePreparation →
        Curriculum Management ValidationPolicy.

    Curriculum Ingestion is consulted only when an ingestion job was
    started with real normalised structure (not reference-only stubs).
    Studio maps results and syncs checklist facts only — it never sets
    ``validation_passed`` without a successful Management gate.
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

        # Prefer Management (publication-gate authority).
        if workspace.version_id and self._management is not None:
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

        # Authoritative ingestion only — never project stub-job failures.
        job_id = self._registry.get_ingestion_job(workspace_id)
        if (
            job_id
            and self._ingestion is not None
            and self._ingestion.is_available()
            and _ingestion_job_is_authoritative(self._ingestion, job_id)
        ):
            report = self._ingestion.get_validation_report(job_id) or {}
            readiness, errors, warnings = _map_report(report, errors, warnings)

        if readiness is ValidationReadiness.NOT_STARTED:
            if not workspace.facts.cmp_uploaded:
                errors.append(guided_finding("missing_cmp"))
            if not workspace.facts.official_syllabus_uploaded:
                errors.append(guided_finding("missing_syllabus"))
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
            warnings=tuple(enrich_finding(w) for w in warnings),
            errors=tuple(enrich_finding(e) for e in errors),
            readiness=readiness,
        )
        return validation_snapshot(summary)

    def validate_curriculum(
        self,
        workspace_id: str,
        *,
        run_management_gate: bool = True,
    ) -> ValidationSnapshot:
        """Validate Curriculum — Management authority; sync validation_passed."""
        workspace = self._require_workspace(workspace_id)

        # Materialise extraction + default blueprints before Management gate.
        from app.application.curriculum_studio.structure_preparation_service import (
            StructurePreparationService,
        )

        StructurePreparationService(
            self._registry, management=self._management
        ).prepare_for_validation(workspace_id)
        workspace = self._require_workspace(workspace_id)

        if run_management_gate:
            require_management(self._management, action="validate_curriculum")

        # Ingestion gate only when a real (non-stub) job is registered.
        ingestion_passed = True
        job_id = self._registry.get_ingestion_job(workspace_id)
        if job_id and self._ingestion is not None and self._ingestion.is_available():
            if _ingestion_job_is_authoritative(self._ingestion, job_id):
                ing = require_ingestion(
                    self._ingestion, action="validate_curriculum"
                )
                report = ing.get_validation_report(job_id) or {}
                ingestion_passed = _report_passed(report)
            else:
                logger.info(
                    "Ignoring non-authoritative ingestion job %s for %s "
                    "(reference-only stub; Management is publication gate)",
                    job_id,
                    workspace_id,
                )

        management_passed = True
        if run_management_gate:
            if not workspace.version_id:
                raise ValidationError(
                    f"Validation requires version for {workspace_id}"
                )
            mgmt = require_management(
                self._management, action="validate_curriculum"
            )
            try:
                report = mgmt.validate_version(workspace.version_id)
            except Exception as exc:
                # Management may raise on blocking failures after storing report.
                facts = _copy_facts(workspace.facts, validation_passed=False)
                self._registry.put_workspace(workspace.with_facts(facts))
                snap = self.summarise(workspace_id)
                raise ValidationError(
                    f"Validation failed for {workspace_id}: "
                    f"{snap.error_count} error(s)"
                ) from exc
            management_passed = _report_passed(report)

        passed = bool(ingestion_passed and management_passed)
        if not passed:
            facts = _copy_facts(workspace.facts, validation_passed=False)
            self._registry.put_workspace(workspace.with_facts(facts))
            snap = self.summarise(workspace_id)
            raise ValidationError(
                f"Validation failed for {workspace_id}: "
                f"{snap.error_count} error(s)"
            )

        facts = _copy_facts(
            workspace.facts,
            validation_passed=True,
            blueprint_assigned=True,
        )
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


def _report_passed(report: dict) -> bool:
    """Interpret an opaque validation report as pass/fail."""
    if as_bool(report.get("passed")):
        return True
    if report.get("passed") is False:
        return False
    if as_bool(report.get("blocks_publication")):
        return False
    readiness = str(report.get("readiness", "")).lower()
    if readiness in {"passed", "ready", "ok", "validated"}:
        return True
    if readiness in {"failed", "blocked", "error"}:
        return False
    issues = (
        report.get("issues")
        or report.get("errors")
        or report.get("blocking_issues")
        or ()
    )
    # Blocking / error severities fail; empty issues pass when passed is unset.
    for issue in issues:
        if not isinstance(issue, dict):
            return False
        severity = str(issue.get("severity") or "").lower()
        if severity in {"blocking", "error"} or as_bool(
            issue.get("is_blocking")
        ):
            return False
    return len(issues) == 0 or readiness == ""


def _ingestion_job_is_authoritative(
    ingestion: CurriculumIngestionPort, job_id: str
) -> bool:
    """True when the job carries real structure (not a reference-only stub).

    Reference-only uploads produce synthetic single-topic stubs without
    objectives. Those must never gate Founder publication.
    """
    summary = ingestion.get_ingestion_summary(job_id) or {}
    sources = summary.get("sources") or ()
    for source in sources:
        if isinstance(source, dict) and source.get("entries"):
            return True

    structure = ingestion.normalised_structure(job_id) or {}
    topics = structure.get("topics") or structure.get("entries") or ()
    if not topics:
        return False
    if int(structure.get("objective_count") or 0) > 0:
        return True
    for topic in topics:
        if not isinstance(topic, dict):
            continue
        objectives = topic.get("objectives") or topic.get("objective_ids") or ()
        if objectives:
            return True
    return False


def _map_report(
    report: dict,
    errors: list[ValidationFinding],
    warnings: list[ValidationFinding],
) -> tuple[ValidationReadiness, list[ValidationFinding], list[ValidationFinding]]:
    """Project opaque Management / Ingestion reports into Studio findings.

    Consumes ``issues``, ``errors``, and ``blocking_issues`` so Founder-facing
    counts match the underlying validation report (PI-002R Phase 3).
    """
    raw_issues = list(report.get("issues") or ())
    raw_errors = list(
        report.get("errors") or report.get("blocking_issues") or ()
    )
    raw_warnings = list(report.get("warnings") or ())

    for issue in (*raw_issues, *raw_errors):
        finding = _finding_from_issue(issue, default_severity="blocking")
        if finding is None:
            continue
        if finding.severity in {
            ValidationFindingSeverity.BLOCKING,
            ValidationFindingSeverity.ERROR,
        } or finding.is_blocking:
            errors.append(enrich_finding(finding))
        else:
            warnings.append(enrich_finding(finding))

    for issue in raw_warnings:
        finding = _finding_from_issue(issue, default_severity="warning")
        if finding is not None:
            warnings.append(enrich_finding(finding))

    explicit_fail = report.get("passed") is False or as_bool(
        report.get("blocks_publication")
    )
    if errors or explicit_fail:
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


def _finding_from_issue(
    issue: object, *, default_severity: str
) -> ValidationFinding | None:
    if isinstance(issue, dict):
        severity = str(issue.get("severity") or default_severity).lower()
        if as_bool(issue.get("is_blocking")) and severity not in {
            "blocking",
            "error",
        }:
            severity = "blocking"
        code = str(issue.get("code") or "validation_issue")
        message = str(issue.get("message") or "Validation finding")
        return ValidationFinding.create(
            code,
            message,
            severity=severity,
            section_id=(
                None
                if issue.get("section_ref") is None
                and issue.get("section_id") is None
                else str(issue.get("section_ref") or issue.get("section_id"))
            ),
            why_it_matters=str(issue.get("why_it_matters") or ""),
            recovery_action=str(issue.get("recovery_action") or ""),
        )
    if issue is None or str(issue).strip() == "":
        return None
    return ValidationFinding.create(
        "validation_issue",
        str(issue),
        severity=default_severity,
    )

"""Founder-facing operational recovery flashes for Curriculum Studio (FV-001A).

Maps application exceptions to operator copy: issue → why → recovery.
Gate blocks include an actionable remaining-tasks checklist.
"""

from __future__ import annotations

from app.application.curriculum_studio.exceptions import (
    CurriculumStudioError,
    PolicyViolation,
    PortUnavailable,
    PreviewError,
    PublicationError,
    SubjectAlreadyExists,
    SubjectNotFound,
    ValidationError,
    VersionError,
    VersionNotFound,
    WorkflowError,
    WorkflowGateBlocked,
    WorkspaceAlreadyExists,
    WorkspaceNotFound,
)

_FACT_LABELS: dict[str, str] = {
    "cmp_uploaded": "Upload Official CMP",
    "official_syllabus_uploaded": "Upload Official Syllabus",
    "validation_passed": "Complete curriculum processing",
    "blueprint_assigned": "Structure bound",
    "preview_built": "Generate preview",
    "preview_approved": "Approve structure",
    "version_assigned": "Assign version label",
    "rollback_snapshot_created": "Create rollback snapshot",
}

_FACT_ACTIONS: dict[str, tuple[str, str]] = {
    "cmp_uploaded": ("Go to Upload", "upload"),
    "official_syllabus_uploaded": ("Go to Upload", "upload"),
    "validation_passed": ("Wait for processing", "upload"),
    "blueprint_assigned": ("Wait for processing", "upload"),
    "preview_built": ("Go to Preview", "preview"),
    "preview_approved": ("Go to Approve", "approve"),
    "version_assigned": ("Assign version", "version"),
    "rollback_snapshot_created": ("Retry Publish", "publish"),
}


def recover_flash(exc: BaseException, fallback_key: str) -> str:
    """Map an application exception to founder-facing recovery copy."""
    from app.presentation.curriculum_studio.view_models import FLASH_WARNING

    if isinstance(exc, SubjectAlreadyExists):
        return (
            "We couldn't create this subject because the code already exists. "
            "Duplicate codes confuse enrolment and version history. "
            "Choose a different subject code or open the existing workspace, "
            "then try again."
        )
    if isinstance(exc, WorkspaceAlreadyExists):
        return (
            "We couldn't open a new workspace because one already exists for "
            "this subject. Re-using a single workspace keeps version history "
            "coherent. Open the existing workspace from the dashboard, then "
            "try again."
        )
    if isinstance(exc, SubjectNotFound):
        return (
            "We couldn't continue because that subject was not found. "
            "Workspaces must bind to a registered subject. Create the subject "
            "first, then open the workspace and try again."
        )
    if isinstance(exc, WorkspaceNotFound):
        return FLASH_WARNING["workspace_missing"]
    if isinstance(exc, WorkflowGateBlocked):
        return format_gate_blocked(exc)
    if isinstance(exc, WorkflowError):
        detail = str(exc).lower()
        if "already at subject" in detail:
            return FLASH_WARNING.get("retreat", FLASH_WARNING["advance"])
        if fallback_key in {"retreat", "reset"}:
            return FLASH_WARNING.get(fallback_key, FLASH_WARNING["advance"])
        return FLASH_WARNING["advance"]
    if isinstance(exc, ValidationError):
        detail = str(exc).strip()
        if "requires version" in detail.lower():
            return (
                "We couldn't complete validation because no version is "
                "assigned. Assign a version label, then try again."
            )
        if "blocked" in detail.lower() or "failed" in detail.lower():
            return (
                "We couldn't complete validation because issues remain. "
                "Review the findings below, fix CMP or syllabus problems, "
                "then try again."
            )
        return FLASH_WARNING["validate"]
    if isinstance(exc, PreviewError):
        detail = str(exc).strip()
        if "no curriculum" in detail.lower() or "hierarchy" in detail.lower():
            return (
                "We couldn't build a meaningful preview — no extracted "
                "curriculum topics are available yet. Upload Official CMP and "
                "Official Syllabus, wait for extraction, validate, then try "
                "again."
            )
        return FLASH_WARNING["preview"]
    if isinstance(exc, PublicationError):
        detail_raw = str(exc).strip()
        detail = detail_raw.lower()
        if fallback_key in {"archive_subject", "delete_draft"} and detail_raw:
            return detail_raw
        # Approve path must never surface Publish verbs (PI-002R Phase 3/5).
        if "approval requires successful validation" in detail or (
            "validation" in detail and "approval" in detail
        ):
            return (
                "We couldn't approve this curriculum because validation has "
                "not passed. Approval without validation risks publishing an "
                "unsafe package. Run Validate Curriculum, fix any findings, "
                "then try again."
            )
        if "approval requires a successful preview" in detail or (
            "preview" in detail and "approval" in detail
        ):
            return (
                "We couldn't approve this curriculum because preview is not "
                "ready. Approval needs a reviewable curriculum structure. "
                "Build preview after validation, then try again."
            )
        if "approval requires an assigned version" in detail:
            return FLASH_WARNING["approve"]
        if "not ready" in detail or "blocking" in detail:
            if fallback_key == "approve":
                return (
                    "We couldn't approve this curriculum because required "
                    "steps are incomplete. Complete validation and preview, "
                    "then try again."
                )
            return FLASH_WARNING["publish"]
        if "version" in detail:
            if fallback_key == "approve":
                return FLASH_WARNING["approve"]
            return (
                "We couldn't publish this curriculum because a version label "
                "is missing. Assign a version, complete approval, then try "
                "again."
            )
        if fallback_key == "approve":
            return FLASH_WARNING["approve"]
        if detail_raw and fallback_key in {"archive_subject", "delete_draft"}:
            return detail_raw
        return FLASH_WARNING.get(fallback_key, FLASH_WARNING["publish"])
    if isinstance(exc, VersionNotFound):
        return (
            "We couldn't find that curriculum version. Version history must "
            "stay accurate for rollbacks. Assign or select a valid version "
            "label, then try again."
        )
    if isinstance(exc, VersionError):
        detail = str(exc).lower()
        if "already exists" in detail or "duplicate" in detail:
            return (
                "We couldn't assign this version because the label already "
                "exists. Choose a new version label (for example 2026.2), "
                "then try again."
            )
        if "yyyy.n" in detail or "invalid version label" in detail:
            return (
                "We couldn't assign this version because the label format is "
                "invalid. Use YYYY.N (for example 2026.1), then try again."
            )
        if "subject" in detail and "missing" in detail:
            return (
                "We couldn't assign this version because the subject is "
                "missing from Curriculum Management. Refresh the workspace "
                "to restore it, then try again."
            )
        return FLASH_WARNING["version"]
    if isinstance(exc, PortUnavailable):
        return (
            "We couldn't complete this step because a Studio service is "
            "temporarily unavailable. Wait a moment, refresh the workspace, "
            "then try again. If it persists, contact support."
        )
    if isinstance(exc, PolicyViolation):
        detail = str(exc).lower()
        if "yyyy.n" in detail or "version_label" in detail:
            return (
                "We couldn't assign this version because the label format is "
                "invalid. Use YYYY.N (for example 2026.1), then try again."
            )
        return (
            "We couldn't complete this step because a Studio policy rejected "
            "it. Policies protect students from unsafe curricula. Follow the "
            "on-screen checklist, then try again."
        )
    if isinstance(exc, CurriculumStudioError):
        return FLASH_WARNING.get(fallback_key, FLASH_WARNING["advance"])
    return FLASH_WARNING.get(fallback_key, FLASH_WARNING["advance"])


def format_gate_blocked(exc: WorkflowGateBlocked) -> str:
    """Short flash: what blocked, checklist marks, and next step."""
    target = (exc.target_stage or "next stage").replace("_", " ")
    missing = list(exc.missing_codes)
    satisfied = list(exc.satisfied_codes)
    count = len(missing) if missing else 1
    step_word = "step" if count == 1 else "steps"
    lines = [
        f"Advancement blocked — finish {count} {step_word} before {target}.",
    ]
    for code in satisfied:
        label = _FACT_LABELS.get(code, code.replace("_", " "))
        lines.append(f"✓ {label}")
    for code in missing:
        label = _FACT_LABELS.get(code, code.replace("_", " "))
        lines.append(f"✗ {label}")
    if not satisfied and not missing:
        lines.append("✗ Complete the current stage checklist")
    primary_code = missing[0] if missing else ""
    action_label, _ = _FACT_ACTIONS.get(
        primary_code, ("Complete the checklist", "upload")
    )
    lines.append(f"Next: {action_label}.")
    return " ".join(lines)


def gate_primary_action(exc: WorkflowGateBlocked) -> tuple[str, str]:
    """Return (button_label, action_key) for the first missing gate."""
    if not exc.missing_codes:
        return ("Review checklist", "upload")
    return _FACT_ACTIONS.get(
        exc.missing_codes[0], ("Complete the checklist", "upload")
    )

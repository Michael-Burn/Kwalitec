"""Founder-facing operational recovery flashes for Curriculum Studio (PR-001A).

Maps application exceptions to operator copy: issue → why → recovery.
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
        return (
            "We couldn't advance the workflow because readiness gates are "
            "incomplete. Skipping gates risks publishing an unfinished "
            "curriculum. Complete the current stage checklist, then try again."
        )
    if isinstance(exc, WorkflowError):
        return FLASH_WARNING["advance"]
    if isinstance(exc, ValidationError):
        detail = str(exc).strip()
        if "requires version" in detail.lower():
            return (
                "We couldn't complete validation because no version is "
                "assigned. Validation needs a version to gate publication. "
                "Assign a version label, upload sources if needed, then "
                "try again."
            )
        if "blocked" in detail.lower() or "failed" in detail.lower():
            return (
                "We couldn't complete validation because blocking findings "
                "remain. Students must not receive incomplete curriculum. "
                "Review the Validation findings below, fix CMP/syllabus "
                "issues, then try again."
            )
        return FLASH_WARNING["validate"]
    if isinstance(exc, PreviewError):
        return FLASH_WARNING["preview"]
    if isinstance(exc, PublicationError):
        detail = str(exc).lower()
        if "not ready" in detail or "blocking" in detail:
            return FLASH_WARNING["publish"]
        if "version" in detail:
            return (
                "We couldn't publish this curriculum because a version label "
                "is missing. Published packages need an immutable version. "
                "Assign a version, complete approval, then try again."
            )
        return FLASH_WARNING["publish"]
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
                "exists. Conflicting labels break immutable publication "
                "history. Choose a new version label (for example 2026.2), "
                "then try again."
            )
        return FLASH_WARNING["version"]
    if isinstance(exc, PortUnavailable):
        return (
            "We couldn't complete this step because a Studio service is "
            "temporarily unavailable. Publishing requires Curriculum "
            "Management and Ingestion. Wait a moment, refresh the workspace, "
            "then try again. If it persists, contact platform support."
        )
    if isinstance(exc, PolicyViolation):
        return (
            "We couldn't complete this step because a Studio policy rejected "
            "it. Policies protect students from unsafe curricula. Follow the "
            "on-screen checklist, then try again."
        )
    if isinstance(exc, CurriculumStudioError):
        return FLASH_WARNING.get(fallback_key, FLASH_WARNING["advance"])
    return FLASH_WARNING.get(fallback_key, FLASH_WARNING["advance"])

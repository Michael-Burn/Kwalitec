"""Deterministic publication checklist for Curriculum Studio.

Checklist items are **computed** from workspace facts.
They are never manually toggled.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class ChecklistItemCode(StrEnum):
    """Canonical publication checklist item codes."""

    CMP_UPLOADED = "cmp_uploaded"
    OFFICIAL_SYLLABUS_UPLOADED = "official_syllabus_uploaded"
    VALIDATION_PASSED = "validation_passed"
    BLUEPRINT_ASSIGNED = "blueprint_assigned"
    PREVIEW_APPROVED = "preview_approved"
    VERSION_ASSIGNED = "version_assigned"
    ROLLBACK_SNAPSHOT_CREATED = "rollback_snapshot_created"
    READY_TO_PUBLISH = "ready_to_publish"


class ChecklistItemStatus(StrEnum):
    """Computed status of a checklist item."""

    SATISFIED = "satisfied"
    PENDING = "pending"
    BLOCKED = "blocked"


# Authoritative ordered checklist (READY_TO_PUBLISH is derived last).
CHECKLIST_ORDER: tuple[ChecklistItemCode, ...] = (
    ChecklistItemCode.CMP_UPLOADED,
    ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED,
    ChecklistItemCode.VALIDATION_PASSED,
    ChecklistItemCode.BLUEPRINT_ASSIGNED,
    ChecklistItemCode.PREVIEW_APPROVED,
    ChecklistItemCode.VERSION_ASSIGNED,
    ChecklistItemCode.ROLLBACK_SNAPSHOT_CREATED,
    ChecklistItemCode.READY_TO_PUBLISH,
)

CHECKLIST_LABELS: dict[ChecklistItemCode, str] = {
    ChecklistItemCode.CMP_UPLOADED: "CMP Uploaded",
    ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED: "Official Syllabus Uploaded",
    ChecklistItemCode.VALIDATION_PASSED: "Validation Passed",
    ChecklistItemCode.BLUEPRINT_ASSIGNED: "Blueprint Assigned",
    ChecklistItemCode.PREVIEW_APPROVED: "Preview Approved",
    ChecklistItemCode.VERSION_ASSIGNED: "Version Assigned",
    ChecklistItemCode.ROLLBACK_SNAPSHOT_CREATED: "Rollback Snapshot Created",
    ChecklistItemCode.READY_TO_PUBLISH: "Ready To Publish",
}

# Prerequisite codes that must be satisfied for READY_TO_PUBLISH.
_READINESS_PREREQUISITES: tuple[ChecklistItemCode, ...] = (
    ChecklistItemCode.CMP_UPLOADED,
    ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED,
    ChecklistItemCode.VALIDATION_PASSED,
    ChecklistItemCode.BLUEPRINT_ASSIGNED,
    ChecklistItemCode.PREVIEW_APPROVED,
    ChecklistItemCode.VERSION_ASSIGNED,
    ChecklistItemCode.ROLLBACK_SNAPSHOT_CREATED,
)


@dataclass(frozen=True)
class WorkspacePublicationFacts:
    """Observable facts used to compute the publication checklist.

    Facts are inputs — never checklist toggles.
    """

    cmp_uploaded: bool = False
    official_syllabus_uploaded: bool = False
    validation_passed: bool = False
    blueprint_assigned: bool = False
    preview_approved: bool = False
    version_assigned: bool = False
    rollback_snapshot_created: bool = False

    @classmethod
    def create(
        cls,
        *,
        cmp_uploaded: bool = False,
        official_syllabus_uploaded: bool = False,
        validation_passed: bool = False,
        blueprint_assigned: bool = False,
        preview_approved: bool = False,
        version_assigned: bool = False,
        rollback_snapshot_created: bool = False,
    ) -> WorkspacePublicationFacts:
        """Construct facts from boolean inputs."""
        return cls(
            cmp_uploaded=bool(cmp_uploaded),
            official_syllabus_uploaded=bool(official_syllabus_uploaded),
            validation_passed=bool(validation_passed),
            blueprint_assigned=bool(blueprint_assigned),
            preview_approved=bool(preview_approved),
            version_assigned=bool(version_assigned),
            rollback_snapshot_created=bool(rollback_snapshot_created),
        )

    def fact_for(self, code: ChecklistItemCode) -> bool:
        """Return the raw fact for a non-derived checklist code."""
        mapping = {
            ChecklistItemCode.CMP_UPLOADED: self.cmp_uploaded,
            ChecklistItemCode.OFFICIAL_SYLLABUS_UPLOADED: (
                self.official_syllabus_uploaded
            ),
            ChecklistItemCode.VALIDATION_PASSED: self.validation_passed,
            ChecklistItemCode.BLUEPRINT_ASSIGNED: self.blueprint_assigned,
            ChecklistItemCode.PREVIEW_APPROVED: self.preview_approved,
            ChecklistItemCode.VERSION_ASSIGNED: self.version_assigned,
            ChecklistItemCode.ROLLBACK_SNAPSHOT_CREATED: (
                self.rollback_snapshot_created
            ),
        }
        if code is ChecklistItemCode.READY_TO_PUBLISH:
            return all(mapping[c] for c in _READINESS_PREREQUISITES)
        return mapping[code]


@dataclass(frozen=True)
class ChecklistItem:
    """Single computed checklist item — never manually toggled."""

    code: ChecklistItemCode
    label: str
    status: ChecklistItemStatus
    satisfied: bool

    @classmethod
    def from_facts(
        cls,
        code: ChecklistItemCode,
        facts: WorkspacePublicationFacts,
    ) -> ChecklistItem:
        """Compute a checklist item from workspace facts."""
        ok = facts.fact_for(code)
        if code is ChecklistItemCode.READY_TO_PUBLISH:
            status = (
                ChecklistItemStatus.SATISFIED
                if ok
                else ChecklistItemStatus.BLOCKED
            )
        else:
            status = (
                ChecklistItemStatus.SATISFIED
                if ok
                else ChecklistItemStatus.PENDING
            )
        return cls(
            code=code,
            label=CHECKLIST_LABELS[code],
            status=status,
            satisfied=ok,
        )


@dataclass(frozen=True)
class PublicationChecklist:
    """Immutable, fully computed publication checklist.

    ``READY_TO_PUBLISH`` is true only when every prerequisite fact is true.
    """

    items: tuple[ChecklistItem, ...] = field(default_factory=tuple)
    ready_to_publish: bool = False
    satisfied_count: int = 0
    pending_count: int = 0

    @classmethod
    def compute(cls, facts: WorkspacePublicationFacts) -> PublicationChecklist:
        """Compute the full checklist from workspace facts."""
        items = tuple(
            ChecklistItem.from_facts(code, facts) for code in CHECKLIST_ORDER
        )
        ready = facts.fact_for(ChecklistItemCode.READY_TO_PUBLISH)
        satisfied = sum(1 for item in items if item.satisfied)
        pending = len(items) - satisfied
        return cls(
            items=items,
            ready_to_publish=ready,
            satisfied_count=satisfied,
            pending_count=pending,
        )

    def item(self, code: ChecklistItemCode | str) -> ChecklistItem:
        """Return the checklist item for ``code``."""
        resolved = (
            code
            if isinstance(code, ChecklistItemCode)
            else ChecklistItemCode(str(code).strip().lower())
        )
        for entry in self.items:
            if entry.code is resolved:
                return entry
        raise KeyError(f"Unknown checklist item: {code!r}")

    @property
    def blocking_codes(self) -> tuple[ChecklistItemCode, ...]:
        """Codes that are not yet satisfied (excluding READY when blocked)."""
        return tuple(
            item.code
            for item in self.items
            if (
                not item.satisfied
                and item.code is not ChecklistItemCode.READY_TO_PUBLISH
            )
        )

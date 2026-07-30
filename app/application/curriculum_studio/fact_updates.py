"""Helpers for copying WorkspacePublicationFacts (FV-001A / EI-002A)."""

from __future__ import annotations

from app.domain.curriculum_studio.publication_checklist import (
    WorkspacePublicationFacts,
)


def copy_publication_facts(
    facts: WorkspacePublicationFacts,
    **overrides: bool | None,
) -> WorkspacePublicationFacts:
    """Return facts with selected boolean fields overridden.

    Pass ``None`` (or omit) to keep the existing value.
    """

    def _pick(name: str, current: bool) -> bool:
        if name not in overrides or overrides[name] is None:
            return current
        return bool(overrides[name])

    return WorkspacePublicationFacts.create(
        cmp_uploaded=_pick("cmp_uploaded", facts.cmp_uploaded),
        official_syllabus_uploaded=_pick(
            "official_syllabus_uploaded", facts.official_syllabus_uploaded
        ),
        validation_passed=_pick("validation_passed", facts.validation_passed),
        blueprint_assigned=_pick("blueprint_assigned", facts.blueprint_assigned),
        preview_built=_pick("preview_built", facts.preview_built),
        preview_approved=_pick("preview_approved", facts.preview_approved),
        version_assigned=_pick("version_assigned", facts.version_assigned),
        rollback_snapshot_created=_pick(
            "rollback_snapshot_created", facts.rollback_snapshot_created
        ),
        intelligence_certified=_pick(
            "intelligence_certified", facts.intelligence_certified
        ),
        calibration_applied=_pick("calibration_applied", facts.calibration_applied),
        legacy_publish_fallback=_pick(
            "legacy_publish_fallback", facts.legacy_publish_fallback
        ),
    )

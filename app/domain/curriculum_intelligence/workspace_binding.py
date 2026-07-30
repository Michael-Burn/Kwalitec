"""Workspace ↔ Generation Chain binding (EI-002A).

Every Curriculum Studio workspace owns exactly one active Generation Chain.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_intelligence.generation import CertificationOutcome

# Metadata keys persisted on CurriculumWorkspace.metadata
META_CHAIN_ID = "ei_chain_id"
META_CERTIFIED_SNAPSHOT_ID = "ei_certified_snapshot_id"
META_CALIBRATION_PROFILE_ID = "ei_calibration_profile_id"
META_CERTIFICATION_STATUS = "ei_certification_status"
META_REVIEW_PACK_REF = "ei_review_pack_ref"
META_LEGACY_FALLBACK = "ei_legacy_fallback"

LEGACY_FALLBACK_VALUE = "true"


@dataclass(frozen=True)
class WorkspaceGenerationBinding:
    """Authoritative EI binding for one Studio workspace."""

    workspace_id: str
    chain_id: str
    active_snapshot_id: str | None = None
    certified_snapshot_id: str | None = None
    calibration_profile_id: str | None = None
    certification_status: CertificationOutcome | None = None
    review_pack_ref: str | None = None
    legacy_fallback: bool = False

    @property
    def is_certified(self) -> bool:
        """True when Gen 7 outcome allows Preview / Publish."""
        return self.certification_status in {
            CertificationOutcome.CERTIFIED,
            CertificationOutcome.CERTIFIED_WITH_WARNINGS,
        }

    def as_metadata(self) -> tuple[tuple[str, str], ...]:
        """Flatten binding into workspace metadata pairs."""
        pairs: list[tuple[str, str]] = [
            (META_CHAIN_ID, self.chain_id),
        ]
        if self.certified_snapshot_id:
            pairs.append((META_CERTIFIED_SNAPSHOT_ID, self.certified_snapshot_id))
        if self.active_snapshot_id:
            pairs.append(("ei_active_snapshot_id", self.active_snapshot_id))
        if self.calibration_profile_id:
            pairs.append((META_CALIBRATION_PROFILE_ID, self.calibration_profile_id))
        if self.certification_status is not None:
            pairs.append((META_CERTIFICATION_STATUS, self.certification_status.value))
        if self.review_pack_ref:
            pairs.append((META_REVIEW_PACK_REF, self.review_pack_ref))
        if self.legacy_fallback:
            pairs.append((META_LEGACY_FALLBACK, LEGACY_FALLBACK_VALUE))
        return tuple(pairs)

    @classmethod
    def from_metadata(
        cls,
        workspace_id: str,
        metadata: tuple[tuple[str, str], ...] | dict[str, str],
    ) -> WorkspaceGenerationBinding | None:
        """Rehydrate binding from workspace metadata, or None if unbound."""
        meta = dict(metadata) if not isinstance(metadata, dict) else dict(metadata)
        chain_id = (meta.get(META_CHAIN_ID) or "").strip()
        if not chain_id:
            return None
        status_raw = (meta.get(META_CERTIFICATION_STATUS) or "").strip()
        status: CertificationOutcome | None = None
        if status_raw:
            try:
                status = CertificationOutcome(status_raw)
            except ValueError:
                status = None
        return cls(
            workspace_id=workspace_id,
            chain_id=chain_id,
            active_snapshot_id=(meta.get("ei_active_snapshot_id") or None),
            certified_snapshot_id=(meta.get(META_CERTIFIED_SNAPSHOT_ID) or None),
            calibration_profile_id=(meta.get(META_CALIBRATION_PROFILE_ID) or None),
            certification_status=status,
            review_pack_ref=(meta.get(META_REVIEW_PACK_REF) or None),
            legacy_fallback=meta.get(META_LEGACY_FALLBACK) == LEGACY_FALLBACK_VALUE,
        )


def chain_id_for_workspace(workspace_id: str) -> str:
    """Deterministic active chain id for a Studio workspace."""
    wid = (workspace_id or "").strip()
    if not wid:
        raise ValueError("workspace_id must be non-empty")
    return f"ei-chain-{wid}"

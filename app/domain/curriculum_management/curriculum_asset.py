"""Curriculum asset — reference and metadata only (never PDF bytes)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class AssetKind(StrEnum):
    """Recognised curriculum asset kinds (references only)."""

    CMP = "cmp"
    SYLLABUS = "syllabus"
    LEARNING_OBJECTIVES = "learning_objectives"
    FORMULA_SHEET = "formula_sheet"
    SUPPORTING_DOCUMENT = "supporting_document"


def resolve_asset_kind(value: AssetKind | str) -> AssetKind:
    """Resolve an AssetKind from enum or string token."""
    if isinstance(value, AssetKind):
        return value
    token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
    aliases = {
        "learning_objective": AssetKind.LEARNING_OBJECTIVES,
        "objectives": AssetKind.LEARNING_OBJECTIVES,
        "formula": AssetKind.FORMULA_SHEET,
        "supporting": AssetKind.SUPPORTING_DOCUMENT,
        "support": AssetKind.SUPPORTING_DOCUMENT,
        "document": AssetKind.SUPPORTING_DOCUMENT,
    }
    if token in aliases:
        return aliases[token]
    try:
        return AssetKind(token)
    except ValueError as exc:
        raise ValueError(f"Unknown asset kind: {value!r}") from exc


@dataclass(frozen=True)
class CurriculumAsset:
    """Reference to an uploaded educational asset.

    Stores references and metadata only — never PDF content, never bytes.
    """

    asset_id: str
    kind: AssetKind
    reference: str
    label: str
    media_type: str | None = None
    checksum: str | None = None
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        asset_id: str,
        kind: AssetKind | str,
        reference: str,
        label: str,
        *,
        media_type: str | None = None,
        checksum: str | None = None,
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> CurriculumAsset:
        """Construct a CurriculumAsset after validating invariants.

        Raises:
            ValueError: On empty identity/reference/label, or content-like refs.
        """
        aid = _require_non_empty(asset_id, "asset_id")
        ref = _require_non_empty(reference, "reference")
        name = _require_non_empty(label, "label")
        _reject_embedded_content(ref)
        media = (
            None
            if media_type is None
            else _require_non_empty(media_type, "media_type")
        )
        check = None if checksum is None else _require_non_empty(checksum, "checksum")
        return cls(
            asset_id=aid,
            kind=resolve_asset_kind(kind),
            reference=ref,
            label=name,
            media_type=media,
            checksum=check,
            metadata=tuple(metadata or ()),
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _reject_embedded_content(reference: str) -> None:
    """Reject obvious embedded payloads (data URIs / raw PDF markers)."""
    lowered = reference.lower()
    if lowered.startswith("data:"):
        raise ValueError("reference must not embed content (data URI)")
    if "%pdf-" in lowered or lowered.startswith("%pdf"):
        raise ValueError("reference must not embed PDF content")

"""Curriculum package — collection of asset references for a subject version."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum_management.curriculum_asset import (
    AssetKind,
    CurriculumAsset,
)


@dataclass(frozen=True)
class CurriculumPackage:
    """Uploaded educational asset package (references only).

    No parsing. No extraction. No ingestion.
    """

    package_id: str
    version_id: str
    assets: tuple[CurriculumAsset, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        package_id: str,
        version_id: str,
        *,
        assets: list[CurriculumAsset] | tuple[CurriculumAsset, ...] | None = None,
    ) -> CurriculumPackage:
        """Construct a CurriculumPackage after validating invariants."""
        pid = _require_non_empty(package_id, "package_id")
        vid = _require_non_empty(version_id, "version_id")
        assets_t = tuple(assets or ())
        seen: set[str] = set()
        for asset in assets_t:
            if asset.asset_id in seen:
                raise ValueError(f"duplicate asset_id: {asset.asset_id!r}")
            seen.add(asset.asset_id)
        return cls(package_id=pid, version_id=vid, assets=assets_t)

    @property
    def asset_count(self) -> int:
        """Number of referenced assets."""
        return len(self.assets)

    def asset_by_id(self, asset_id: str) -> CurriculumAsset | None:
        """Return an asset by identity, or None."""
        token = (asset_id or "").strip()
        if not token:
            return None
        for asset in self.assets:
            if asset.asset_id == token:
                return asset
        return None

    def assets_of_kind(self, kind: AssetKind | str) -> tuple[CurriculumAsset, ...]:
        """Return assets matching ``kind``."""
        from app.domain.curriculum_management.curriculum_asset import resolve_asset_kind

        resolved = resolve_asset_kind(kind)
        return tuple(a for a in self.assets if a.kind is resolved)

    def has_kind(self, kind: AssetKind | str) -> bool:
        """True when at least one asset of ``kind`` is present."""
        return bool(self.assets_of_kind(kind))

    def with_asset(self, asset: CurriculumAsset) -> CurriculumPackage:
        """Return a package with an appended asset."""
        if any(a.asset_id == asset.asset_id for a in self.assets):
            raise ValueError(f"duplicate asset_id: {asset.asset_id!r}")
        return CurriculumPackage(
            package_id=self.package_id,
            version_id=self.version_id,
            assets=(*self.assets, asset),
        )

    def without_asset(self, asset_id: str) -> CurriculumPackage:
        """Return a package with ``asset_id`` removed."""
        token = _require_non_empty(asset_id, "asset_id")
        remaining = tuple(a for a in self.assets if a.asset_id != token)
        if len(remaining) == len(self.assets):
            raise ValueError(f"asset not found: {token!r}")
        return CurriculumPackage(
            package_id=self.package_id,
            version_id=self.version_id,
            assets=remaining,
        )


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized

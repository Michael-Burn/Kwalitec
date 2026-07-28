"""Machine-readable Runtime A / legacy dependency inventory (RI-002).

Static catalogue derived from the RI-001 runtime audit, with optional
path-existence checks. Classification only — no educational reasoning.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from app.application.runtime_integration.dto import (
    InventoryEntry,
    InventoryStatus,
    RuntimeInventoryReport,
)

_REPO_ROOT = Path(__file__).resolve().parents[3]


def _utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


# Canonical inventory — keep aligned with RUNTIME_AUDIT.md.
_INVENTORY_SPEC: tuple[dict[str, object], ...] = (
    {
        "entry_id": "rec-service",
        "component": "RecommendationService",
        "path": "app/services/recommendation_service.py",
        "category": "runtime_a_recommendation",
        "status": InventoryStatus.ACTIVE,
        "notes": (
            "Temporary compatibility educational selection when RIS falls back."
        ),
        "blocks_retirement": True,
    },
    {
        "entry_id": "rec-bridge",
        "component": "RecommendationAdapter (Runtime Bridge)",
        "path": (
            "app/infrastructure/adapters/educational_runtime_bridge/"
            "recommendation_adapter.py"
        ),
        "category": "compatibility_adapter",
        "status": InventoryStatus.DEPRECATED,
        "notes": (
            "RIS-first adapter; Runtime A path remains for unmigrated students."
        ),
        "blocks_retirement": False,
    },
    {
        "entry_id": "planning-selection",
        "component": "PlanningService educational slot selection",
        "path": "app/services/planning_service.py",
        "category": "runtime_a_planning",
        "status": InventoryStatus.ACTIVE,
        "notes": (
            "Educational slot selection Temporary compatibility; "
            "mission ORM persistence may remain after recommendation retirement."
        ),
        "blocks_retirement": True,
    },
    {
        "entry_id": "stage-a-decision",
        "component": "Stage A DecisionEngine / EducationalOrchestrator",
        "path": "app/application/orchestration",
        "category": "legacy_recommendation",
        "status": InventoryStatus.DEPRECATED,
        "notes": "Flag-gated; prefer RIS. Selection Replace over time.",
        "blocks_retirement": False,
    },
    {
        "entry_id": "mission-optimizer",
        "component": "MissionOptimizer",
        "path": "app/services/mission_optimizer.py",
        "category": "legacy_recommendation",
        "status": InventoryStatus.REMOVABLE,
        "notes": "Quarantined; no production callers expected.",
        "blocks_retirement": False,
    },
    {
        "entry_id": "runtime-c",
        "component": "Runtime C / PX-001 educational fork",
        "path": "app/application/educational_experience",
        "category": "compatibility_consumer",
        "status": InventoryStatus.DEPRECATED,
        "notes": (
            "Temporary compatibility consumer; defers when Preferred Authority "
            "available. No new educational logic."
        ),
        "blocks_retirement": False,
    },
    {
        "entry_id": "sdt-educational-reasoning",
        "component": "SDT-002 educational_reasoning vocabulary",
        "path": "app/domain/educational_reasoning",
        "category": "legacy_recommendation",
        "status": InventoryStatus.DEPRECATED,
        "notes": "Distinct from EI-007; replace over time.",
        "blocks_retirement": False,
    },
    {
        "entry_id": "ap002-decision-generator",
        "component": "AP-002 DecisionGenerator",
        "path": "app/application/reasoning/decisions",
        "category": "legacy_recommendation",
        "status": InventoryStatus.ACTIVE,
        "notes": (
            "Evidence→twin explanation path; not Preferred Authority for "
            "recommendations. Consolidation deferred."
        ),
        "blocks_retirement": True,
    },
    {
        "entry_id": "eos-src-engines",
        "component": "EOS src/ recommendation engines",
        "path": "src/domain/education/recommendation_engine",
        "category": "out_of_scope",
        "status": InventoryStatus.REMOVABLE,
        "notes": "Out of student Runtime A path; do not wire into RIS.",
        "blocks_retirement": False,
    },
    {
        "entry_id": "ris-adapters",
        "component": "RI-001 surface adapters",
        "path": "app/application/runtime_integration/adapters",
        "category": "compatibility_adapter",
        "status": InventoryStatus.ACTIVE,
        "notes": (
            "Presentation mapping only for Preferred Authority. Not Runtime A. "
            "Remain after Runtime A retirement."
        ),
        "blocks_retirement": False,
    },
    {
        "entry_id": "enable-flag",
        "component": "ENABLE_RUNTIME_INTEGRATION flag",
        "path": "app/application/config/v2_flags.py",
        "category": "compatibility_control",
        "status": InventoryStatus.ACTIVE,
        "notes": (
            "Forces Runtime A when off. Removable only after hard Preferred "
            "Authority cutover (RI-005)."
        ),
        "blocks_retirement": True,
    },
    {
        "entry_id": "dashboard-legacy-rec",
        "component": "Dashboard RecommendationService direct calls",
        "path": "app/dashboard/routes.py",
        "category": "legacy_recommendation",
        "status": InventoryStatus.DEPRECATED,
        "notes": "RIS preferred; Runtime A Temporary compatibility retained.",
        "blocks_retirement": False,
    },
)


class RuntimeInventoryService:
    """Generate the machine-readable remaining-dependency inventory."""

    def __init__(self, *, repo_root: Path | None = None) -> None:
        self._repo_root = repo_root or _REPO_ROOT

    def build_report(self) -> RuntimeInventoryReport:
        entries: list[InventoryEntry] = []
        for spec in _INVENTORY_SPEC:
            path = str(spec["path"])
            status = spec["status"]
            assert isinstance(status, InventoryStatus)
            # Soft existence check — missing removable paths stay removable.
            resolved = self._repo_root / path
            notes = str(spec["notes"])
            if not resolved.exists() and status is InventoryStatus.ACTIVE:
                status = InventoryStatus.BLOCKED
                notes = f"{notes} Path missing on disk — investigate before retirement."
            elif not resolved.exists() and status is InventoryStatus.DEPRECATED:
                status = InventoryStatus.REMOVABLE
                notes = f"{notes} Path already absent."
            entries.append(
                InventoryEntry(
                    entry_id=str(spec["entry_id"]),
                    component=str(spec["component"]),
                    path=path,
                    category=str(spec["category"]),
                    status=status,
                    notes=notes,
                    blocks_retirement=bool(spec["blocks_retirement"]),
                )
            )
        return RuntimeInventoryReport(
            generated_at=_utc_now_iso(),
            entries=tuple(entries),
        )

    def to_json_dict(self) -> dict:
        """Serialisable inventory payload for operators / tooling."""
        return self.build_report().to_dict()

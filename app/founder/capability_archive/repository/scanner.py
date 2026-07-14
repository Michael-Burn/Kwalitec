"""Filesystem scanner for the Capability Archive (FOS-002).

Internal to the subsystem — never export Paths outside this package.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from app.founder.capability_archive.config import CapabilityArchiveConfig
from app.founder.capability_archive.dto.record import CapabilityRecordDTO
from app.founder.capability_archive.dto.validation import ArchiveValidationIssue


@dataclass(frozen=True)
class ArchiveScanResult:
    """Internal archive scan payload."""

    records: tuple[CapabilityRecordDTO, ...]
    issues: tuple[ArchiveValidationIssue, ...]


class CapabilityArchiveScanner:
    """Discover Capability Archive JSON entries under the configured root."""

    def __init__(
        self,
        *,
        repo_root: Path,
        config: CapabilityArchiveConfig,
    ) -> None:
        self._root = repo_root.resolve()
        self._config = config

    def scan(self) -> ArchiveScanResult:
        """Load and validate archive entries."""
        issues: list[ArchiveValidationIssue] = []
        archive_root = self._root / self._config.archive_root
        if not archive_root.is_dir():
            issues.append(
                ArchiveValidationIssue(
                    code="missing_archive_root",
                    message=(
                        f"Capability archive root is missing: "
                        f"{self._config.archive_root}"
                    ),
                )
            )
            return ArchiveScanResult(records=(), issues=tuple(issues))

        entries_dir = archive_root / self._config.entries_dir
        if not entries_dir.is_dir():
            issues.append(
                ArchiveValidationIssue(
                    code="missing_entries_dir",
                    message=(
                        f"Capability archive entries directory is missing: "
                        f"{self._config.entries_dir}"
                    ),
                )
            )
            return ArchiveScanResult(records=(), issues=tuple(issues))

        records: list[CapabilityRecordDTO] = []
        seen_ids: dict[str, int] = {}

        for path in sorted(entries_dir.iterdir()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in self._config.entry_suffixes:
                continue
            if path.name.startswith("."):
                continue

            record, entry_issues = self._load_entry(path)
            issues.extend(entry_issues)
            if record is None:
                continue

            count = seen_ids.get(record.capability_id, 0) + 1
            seen_ids[record.capability_id] = count
            if count > 1:
                issues.append(
                    ArchiveValidationIssue(
                        code="duplicate_capability_id",
                        message=(
                            f"Duplicate capability id '{record.capability_id}'."
                        ),
                        capability_id=record.capability_id,
                    )
                )
            records.append(record)

        records.sort(key=lambda r: (r.completion_date, r.capability_id), reverse=True)
        return ArchiveScanResult(records=tuple(records), issues=tuple(issues))

    def _load_entry(
        self, path: Path
    ) -> tuple[CapabilityRecordDTO | None, list[ArchiveValidationIssue]]:
        issues: list[ArchiveValidationIssue] = []
        try:
            raw = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            issues.append(
                ArchiveValidationIssue(
                    code="unreadable_entry",
                    message=f"Unable to parse archive entry: {exc.__class__.__name__}",
                    capability_id=path.stem,
                )
            )
            return None, issues

        if not isinstance(raw, dict):
            issues.append(
                ArchiveValidationIssue(
                    code="invalid_entry_shape",
                    message="Archive entry must be a JSON object.",
                    capability_id=path.stem,
                )
            )
            return None, issues

        payload: dict[str, Any] = raw
        capability_id = str(payload.get("capability_id") or path.stem).strip()

        for field_name in self._config.required_fields:
            if field_name not in payload or payload[field_name] in (None, ""):
                issues.append(
                    ArchiveValidationIssue(
                        code="missing_field",
                        message=(
                            f"Missing required field '{field_name}' "
                            f"for capability '{capability_id}'."
                        ),
                        capability_id=capability_id,
                    )
                )

        related = payload.get("related_documents", ())
        if related in (None, ""):
            related_docs: tuple[str, ...] = ()
        elif isinstance(related, list):
            related_docs = tuple(str(item) for item in related)
        else:
            issues.append(
                ArchiveValidationIssue(
                    code="invalid_related_documents",
                    message=(
                        f"related_documents must be a list for '{capability_id}'."
                    ),
                    capability_id=capability_id,
                )
            )
            related_docs = ()

        # Still emit a record when capability_id is present so duplicates /
        # status counts remain visible; incomplete fields stay in issues.
        if not capability_id:
            return None, issues

        record = CapabilityRecordDTO(
            capability_id=capability_id,
            status=str(payload.get("status") or "").strip(),
            version=str(payload.get("version") or "").strip(),
            completion_date=str(payload.get("completion_date") or "").strip(),
            programme=str(payload.get("programme") or "").strip(),
            subsystem=str(payload.get("subsystem") or "").strip(),
            related_documents=related_docs,
            title=str(payload.get("title") or "").strip(),
        )
        return record, issues

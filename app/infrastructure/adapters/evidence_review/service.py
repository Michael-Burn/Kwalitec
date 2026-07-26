"""Educational Evidence Query Service (P4-MS003).

Read-only inspection layer over the Longitudinal Learning Evidence Repository.

Supports:
- query by time window / event type / policy version / trial / advisory field
- combined filtering (including feature-flag provenance)
- immutable timeline views
- reproducible JSON / CSV exports

Never appends, updates, or deletes evidence. Never influences Runtime A,
recommendations, Adaptive, Recovery, or educational policy.
"""

from __future__ import annotations

import csv
import hashlib
import io
import logging
from collections.abc import Mapping, Sequence
from typing import Any

from app.infrastructure.adapters.longitudinal_evidence.contracts import (
    LearningEvidenceRecord,
    LongitudinalEvidenceProvenance,
    LongitudinalEvidenceRepository,
)
from app.infrastructure.adapters.longitudinal_evidence.contracts import (
    serialize_canonical as longitudinal_serialize_canonical,
)

from .contracts import (
    AUTHORITY_EVIDENCE_REVIEW,
    CSV_COLUMNS,
    EVIDENCE_REVIEW_SCHEMA_VERSION,
    EXPORT_FORMAT_CSV,
    EXPORT_FORMAT_JSON,
    EXPORT_FORMATS,
    INVALID_STATE,
    UNAVAILABLE,
    EvidenceEventGroup,
    EvidenceProvenanceSummary,
    EvidenceReviewExport,
    EvidenceReviewFilter,
    EvidenceReviewResult,
    EvidenceTimeline,
    EvidenceTimeWindow,
    serialize_canonical,
)

logger = logging.getLogger(__name__)

SERVICE_ID = "evidence_query_service"
SOURCE_SERVICE = "evidence_review"
SERVICE_VERSION = EVIDENCE_REVIEW_SCHEMA_VERSION


def deterministic_timeline_id(
    *,
    record_ids: Sequence[str],
    filter_snapshot: Mapping[str, Any] | None = None,
) -> str:
    """Deterministic timeline id from observations + filter."""
    material = {
        "filter": dict(filter_snapshot or {}),
        "record_ids": list(record_ids),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"evtl-{digest}"


def deterministic_export_id(
    *,
    format: str,
    content_digest: str,
    filter_snapshot: Mapping[str, Any] | None = None,
) -> str:
    """Deterministic export id from format, content digest, and filter."""
    material = {
        "content_digest": (content_digest or "").strip(),
        "filter": dict(filter_snapshot or {}),
        "format": (format or "").strip().lower(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"evexp-{digest}"


def content_digest(content: str) -> str:
    """SHA-256 digest of export body (reproducibility check)."""
    return hashlib.sha256((content or "").encode("utf-8")).hexdigest()


def _coerce_filter(
    value: EvidenceReviewFilter | Mapping[str, Any] | None,
) -> EvidenceReviewFilter:
    if value is None:
        return EvidenceReviewFilter()
    if isinstance(value, EvidenceReviewFilter):
        return value
    if isinstance(value, Mapping):
        return EvidenceReviewFilter(
            start_timestamp=str(value.get("start_timestamp", "") or ""),
            end_timestamp=str(value.get("end_timestamp", "") or ""),
            event_type=str(value.get("event_type", "") or ""),
            policy_version=str(value.get("policy_version", "") or ""),
            trial_id=str(value.get("trial_id", "") or ""),
            advisory_field=str(value.get("advisory_field", "") or ""),
            feature_flag=str(value.get("feature_flag", "") or ""),
            feature_flag_value=value.get("feature_flag_value", True),
        )
    raise TypeError(
        "filter must be EvidenceReviewFilter, Mapping, or None"
    )


def _feature_flag_matches(
    record: LearningEvidenceRecord,
    *,
    flag_name: str,
    expected: Any,
) -> bool:
    provenance = record.provenance
    flags: Mapping[str, Any]
    if isinstance(provenance, LongitudinalEvidenceProvenance):
        flags = provenance.feature_flags
    elif isinstance(provenance, Mapping):
        flags = provenance.get("feature_flags") or {}
    else:
        flags = {}
    if flag_name not in flags:
        return False
    observed = flags[flag_name]
    if expected is True:
        return bool(observed)
    if expected is False:
        return not bool(observed)
    return observed == expected


def _matches_filter(
    record: LearningEvidenceRecord,
    filt: EvidenceReviewFilter,
) -> bool:
    if filt.start_timestamp and record.event_timestamp < filt.start_timestamp:
        return False
    if filt.end_timestamp and record.event_timestamp > filt.end_timestamp:
        return False
    if filt.event_type and record.event_type != filt.event_type:
        return False
    if filt.policy_version and record.policy_version != filt.policy_version:
        return False
    if filt.trial_id and record.trial_id != filt.trial_id:
        return False
    if filt.advisory_field and record.advisory_field != filt.advisory_field:
        return False
    if filt.feature_flag and not _feature_flag_matches(
        record,
        flag_name=filt.feature_flag,
        expected=filt.feature_flag_value,
    ):
        return False
    return True


def _unique_sorted(values: Sequence[str]) -> tuple[str, ...]:
    seen: set[str] = set()
    ordered: list[str] = []
    for raw in values:
        item = (raw or "").strip()
        if not item or item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(sorted(ordered))


def _csv_escape_cell(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, Mapping | list | tuple):
        return longitudinal_serialize_canonical(value)
    return str(value)


def _records_to_csv(records: Sequence[LearningEvidenceRecord]) -> str:
    buffer = io.StringIO()
    writer = csv.writer(buffer, lineterminator="\n")
    writer.writerow(CSV_COLUMNS)
    for record in records:
        provenance = record.provenance
        if isinstance(provenance, LongitudinalEvidenceProvenance):
            origin = provenance.originating_component
            prov_policy = provenance.policy_version
            collected = provenance.collected_at
            feature_flags = dict(provenance.feature_flags)
            trial_context = dict(provenance.trial_context)
            advisory_prov = dict(provenance.advisory_provenance)
            notes = list(provenance.notes)
        elif isinstance(provenance, Mapping):
            origin = str(provenance.get("originating_component", "") or "")
            prov_policy = str(provenance.get("policy_version", "") or "")
            collected = str(provenance.get("collected_at", "") or "")
            feature_flags = dict(provenance.get("feature_flags") or {})
            trial_context = dict(provenance.get("trial_context") or {})
            advisory_prov = dict(provenance.get("advisory_provenance") or {})
            notes = list(provenance.get("notes") or ())
        else:
            origin = ""
            prov_policy = ""
            collected = ""
            feature_flags = {}
            trial_context = {}
            advisory_prov = {}
            notes = []
        writer.writerow(
            [
                record.record_id,
                record.student_id_hash,
                record.event_type,
                record.event_timestamp,
                record.source_component,
                record.policy_version,
                record.advisory_field,
                record.trial_id,
                record.schema_version,
                record.authority,
                record.operational_only,
                origin,
                prov_policy,
                collected,
                _csv_escape_cell(feature_flags),
                _csv_escape_cell(trial_context),
                _csv_escape_cell(advisory_prov),
                _csv_escape_cell(notes),
            ]
        )
    return buffer.getvalue()


def _records_to_json(records: Sequence[LearningEvidenceRecord]) -> str:
    payload = {
        "authority": AUTHORITY_EVIDENCE_REVIEW,
        "record_count": len(records),
        "records": [item.to_canonical_dict() for item in records],
        "schema_version": EVIDENCE_REVIEW_SCHEMA_VERSION,
    }
    return serialize_canonical(payload)


class EvidenceQueryService:
    """Read-only Educational Evidence Review Workspace (P4-MS003).

    Queries the Longitudinal Learning Evidence Repository without mutation.
    """

    def __init__(
        self,
        *,
        enabled: bool = True,
        repository: LongitudinalEvidenceRepository | None = None,
    ) -> None:
        self._enabled = bool(enabled)
        self._repository = repository

    @property
    def service_id(self) -> str:
        return SERVICE_ID

    @property
    def service_version(self) -> str:
        return SERVICE_VERSION

    @property
    def authority(self) -> str:
        return AUTHORITY_EVIDENCE_REVIEW

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def repository(self) -> LongitudinalEvidenceRepository | None:
        return self._repository

    def _unavailable(
        self,
        *,
        message: str,
        filter_snapshot: Mapping[str, Any] | None = None,
    ) -> EvidenceReviewResult:
        return EvidenceReviewResult(
            ok=False,
            filter_snapshot=filter_snapshot or {},
            error_code=UNAVAILABLE,
            message=message,
        )

    def _gate(
        self,
        *,
        filter_snapshot: Mapping[str, Any] | None = None,
    ) -> EvidenceReviewResult | None:
        if not self._enabled:
            return self._unavailable(
                message="ENABLE_EVIDENCE_REVIEW is OFF",
                filter_snapshot=filter_snapshot,
            )
        if self._repository is None:
            return self._unavailable(
                message="longitudinal_evidence_repository_unavailable",
                filter_snapshot=filter_snapshot,
            )
        if not self._repository.is_enabled():
            return self._unavailable(
                message="ENABLE_LONGITUDINAL_EVIDENCE is OFF",
                filter_snapshot=filter_snapshot,
            )
        return None

    def query_by_time_window(
        self,
        *,
        start_timestamp: str,
        end_timestamp: str,
    ) -> EvidenceReviewResult:
        """Query evidence whose event_timestamp falls in ``[start, end]``."""
        filt = EvidenceReviewFilter(
            start_timestamp=start_timestamp,
            end_timestamp=end_timestamp,
        )
        gated = self._gate(filter_snapshot=filt.to_canonical_dict())
        if gated is not None:
            return gated
        assert self._repository is not None
        result = self._repository.get_by_time_window(
            start_timestamp=filt.start_timestamp,
            end_timestamp=filt.end_timestamp,
        )
        if not result.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=filt.to_canonical_dict(),
                error_code=result.error_code or INVALID_STATE,
                message=result.message,
            )
        return EvidenceReviewResult(
            ok=True,
            records=tuple(result.records),
            filter_snapshot=filt.to_canonical_dict(),
        )

    def query_by_event_type(self, event_type: str) -> EvidenceReviewResult:
        """Query evidence matching ``event_type``."""
        filt = EvidenceReviewFilter(event_type=event_type)
        gated = self._gate(filter_snapshot=filt.to_canonical_dict())
        if gated is not None:
            return gated
        assert self._repository is not None
        result = self._repository.get_by_event_type(filt.event_type)
        if not result.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=filt.to_canonical_dict(),
                error_code=result.error_code or INVALID_STATE,
                message=result.message,
            )
        return EvidenceReviewResult(
            ok=True,
            records=tuple(result.records),
            filter_snapshot=filt.to_canonical_dict(),
        )

    def query_by_policy_version(
        self, policy_version: str
    ) -> EvidenceReviewResult:
        """Query evidence matching ``policy_version``."""
        filt = EvidenceReviewFilter(policy_version=policy_version)
        gated = self._gate(filter_snapshot=filt.to_canonical_dict())
        if gated is not None:
            return gated
        assert self._repository is not None
        result = self._repository.get_by_policy_version(filt.policy_version)
        if not result.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=filt.to_canonical_dict(),
                error_code=result.error_code or INVALID_STATE,
                message=result.message,
            )
        return EvidenceReviewResult(
            ok=True,
            records=tuple(result.records),
            filter_snapshot=filt.to_canonical_dict(),
        )

    def query_by_trial(self, trial_id: str) -> EvidenceReviewResult:
        """Query evidence matching ``trial_id``."""
        filt = EvidenceReviewFilter(trial_id=trial_id)
        gated = self._gate(filter_snapshot=filt.to_canonical_dict())
        if gated is not None:
            return gated
        assert self._repository is not None
        result = self._repository.get_by_trial_id(filt.trial_id)
        if not result.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=filt.to_canonical_dict(),
                error_code=result.error_code or INVALID_STATE,
                message=result.message,
            )
        return EvidenceReviewResult(
            ok=True,
            records=tuple(result.records),
            filter_snapshot=filt.to_canonical_dict(),
        )

    def query_by_advisory_field(
        self, advisory_field: str
    ) -> EvidenceReviewResult:
        """Query evidence matching ``advisory_field``."""
        filt = EvidenceReviewFilter(advisory_field=advisory_field)
        gated = self._gate(filter_snapshot=filt.to_canonical_dict())
        if gated is not None:
            return gated
        assert self._repository is not None
        result = self._repository.get_by_advisory_field(filt.advisory_field)
        if not result.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=filt.to_canonical_dict(),
                error_code=result.error_code or INVALID_STATE,
                message=result.message,
            )
        return EvidenceReviewResult(
            ok=True,
            records=tuple(result.records),
            filter_snapshot=filt.to_canonical_dict(),
        )

    def filter(
        self,
        filters: EvidenceReviewFilter | Mapping[str, Any] | None = None,
    ) -> EvidenceReviewResult:
        """Apply combined read-only filters (AND semantics)."""
        filt = _coerce_filter(filters)
        snapshot = filt.to_canonical_dict()
        gated = self._gate(filter_snapshot=snapshot)
        if gated is not None:
            return gated
        assert self._repository is not None

        if filt.start_timestamp and filt.end_timestamp:
            if filt.start_timestamp > filt.end_timestamp:
                return EvidenceReviewResult(
                    ok=False,
                    filter_snapshot=snapshot,
                    error_code=INVALID_STATE,
                    message="time_window_start_after_end",
                )

        listed = self._repository.list_all()
        if not listed.ok:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=snapshot,
                error_code=listed.error_code or INVALID_STATE,
                message=listed.message,
            )
        matched = tuple(
            item for item in listed.records if _matches_filter(item, filt)
        )
        return EvidenceReviewResult(
            ok=True,
            records=matched,
            filter_snapshot=snapshot,
        )

    def build_timeline(
        self,
        filters: EvidenceReviewFilter | Mapping[str, Any] | None = None,
    ) -> EvidenceReviewResult:
        """Construct an immutable timeline view from filtered observations."""
        queried = self.filter(filters)
        if not queried.ok:
            return queried

        records = queried.records
        record_ids = tuple(item.record_id for item in records)
        timestamps = [item.event_timestamp for item in records if item.event_timestamp]
        window = EvidenceTimeWindow(
            start_timestamp=min(timestamps) if timestamps else "",
            end_timestamp=max(timestamps) if timestamps else "",
        )

        by_type: dict[str, list[str]] = {}
        for item in records:
            by_type.setdefault(item.event_type, []).append(item.record_id)
        event_groups = tuple(
            EvidenceEventGroup(
                event_type=event_type,
                observation_count=len(ids),
                record_ids=tuple(ids),
            )
            for event_type, ids in sorted(by_type.items(), key=lambda i: i[0])
        )

        origins: list[str] = []
        policies: list[str] = []
        trials: list[str] = []
        advisories: list[str] = []
        schemas: list[str] = []
        observed_flags: dict[str, Any] = {}
        for item in records:
            if item.policy_version:
                policies.append(item.policy_version)
            if item.trial_id:
                trials.append(item.trial_id)
            if item.advisory_field:
                advisories.append(item.advisory_field)
            if item.schema_version:
                schemas.append(item.schema_version)
            provenance = item.provenance
            if isinstance(provenance, LongitudinalEvidenceProvenance):
                if provenance.originating_component:
                    origins.append(provenance.originating_component)
                for key, value in provenance.feature_flags.items():
                    observed_flags[str(key)] = value
            elif isinstance(provenance, Mapping):
                origin = str(provenance.get("originating_component", "") or "")
                if origin:
                    origins.append(origin)
                flags = provenance.get("feature_flags") or {}
                if isinstance(flags, Mapping):
                    for key, value in flags.items():
                        observed_flags[str(key)] = value

        timeline = EvidenceTimeline(
            timeline_id=deterministic_timeline_id(
                record_ids=record_ids,
                filter_snapshot=queried.filter_snapshot,
            ),
            observation_count=len(records),
            time_window=window,
            event_groups=event_groups,
            provenance_summary=EvidenceProvenanceSummary(
                originating_components=_unique_sorted(origins),
                policy_versions=_unique_sorted(policies),
                trial_ids=_unique_sorted(trials),
                advisory_fields=_unique_sorted(advisories),
                feature_flags_observed=observed_flags,
                schema_versions=_unique_sorted(schemas),
            ),
            record_ids=record_ids,
            filter_snapshot=queried.filter_snapshot,
        )
        return EvidenceReviewResult(
            ok=True,
            records=records,
            timeline=timeline,
            filter_snapshot=queried.filter_snapshot,
        )

    def export(
        self,
        filters: EvidenceReviewFilter | Mapping[str, Any] | None = None,
        *,
        format: str = EXPORT_FORMAT_JSON,
    ) -> EvidenceReviewResult:
        """Build a reproducible immutable export (JSON or CSV)."""
        fmt = (format or EXPORT_FORMAT_JSON).strip().lower()
        if fmt not in EXPORT_FORMATS:
            return EvidenceReviewResult(
                ok=False,
                filter_snapshot=_coerce_filter(filters).to_canonical_dict(),
                error_code=INVALID_STATE,
                message="export_format_unsupported",
            )

        queried = self.filter(filters)
        if not queried.ok:
            return queried

        records = queried.records
        if fmt == EXPORT_FORMAT_CSV:
            body = _records_to_csv(records)
        else:
            body = _records_to_json(records)

        digest = content_digest(body)
        export = EvidenceReviewExport(
            export_id=deterministic_export_id(
                format=fmt,
                content_digest=digest,
                filter_snapshot=queried.filter_snapshot,
            ),
            format=fmt,
            content=body,
            record_count=len(records),
            filter_snapshot=queried.filter_snapshot,
            content_digest=digest,
        )
        logger.debug(
            "evidence_review_export format=%s records=%s export_id=%s",
            fmt,
            len(records),
            export.export_id,
        )
        return EvidenceReviewResult(
            ok=True,
            records=records,
            export=export,
            filter_snapshot=queried.filter_snapshot,
        )


def build_evidence_query_service(
    *,
    enabled: bool = False,
    repository: LongitudinalEvidenceRepository | None = None,
) -> EvidenceQueryService | None:
    """Construct the Evidence Query Service when the review flag is ON.

    Returns ``None`` when disabled so composition does not expose a review
    surface that could later be mistaken for Runtime A influence.
    """
    if not enabled:
        return None
    return EvidenceQueryService(enabled=True, repository=repository)


__all__ = [
    "SERVICE_ID",
    "SERVICE_VERSION",
    "SOURCE_SERVICE",
    "EvidenceQueryService",
    "build_evidence_query_service",
    "content_digest",
    "deterministic_export_id",
    "deterministic_timeline_id",
]

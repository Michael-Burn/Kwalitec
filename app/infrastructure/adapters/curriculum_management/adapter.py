"""CurriculumManagementAdapter — implements CurriculumManagementPort."""

from __future__ import annotations

from typing import Any

from app.application.curriculum_management import CurriculumManagementFacade
from app.infrastructure._opaque import opaque_dict
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import (
    curriculum_published,
    curriculum_validated,
)


class CurriculumManagementAdapter:
    """Production adapter for CurriculumManagementPort.

    Delegates to Curriculum Management application services.
    Emits integration events. Owns no publication policies.
    """

    ADAPTER_ID = "curriculum_management"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        facade: CurriculumManagementFacade | None = None,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._facade = facade or CurriculumManagementFacade()
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    @property
    def component_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def component_version(self) -> str:
        return self.ADAPTER_VERSION

    @property
    def facade(self) -> CurriculumManagementFacade:
        """Underlying Curriculum Management facade."""
        return self._facade

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    def create_subject(
        self,
        subject_code: str,
        *,
        title: str = "",
        metadata: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        meta = dict(metadata or {})
        snap = self._facade.subjects.create_subject(
            subject_code,
            title or subject_code,
            description=str(meta.get("description") or ""),
            exam_board=meta.get("exam_board"),
            academic_year=meta.get("academic_year"),
            locale=str(meta.get("locale") or "en-GB"),
            tags=meta.get("tags"),
        )
        return self._subject_summary_dict(snap.code)

    def get_subject_summary(self, subject_code: str) -> dict[str, Any] | None:
        try:
            return self._subject_summary_dict(subject_code)
        except Exception:
            return None

    def list_subjects(self) -> tuple[dict[str, Any], ...]:
        return tuple(
            opaque_dict(
                {
                    "subject_code": s.code,
                    "title": s.title,
                    "subject_id": s.subject_id,
                    "active_version_id": s.active_version_id,
                    "version_count": s.version_count,
                    "publication_state": s.publication_state,
                }
            )
            for s in self._facade.subjects.list_subjects()
        )

    def create_version(
        self,
        subject_code: str,
        version_label: str,
        *,
        version_id: str | None = None,
        parent_version_id: str | None = None,
        notes: str = "",
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        subject = self._facade.subjects.get_subject_by_code(subject_code)
        snap = self._facade.versions.create_version(
            subject.subject_id,
            version_label,
            version_id=version_id,
        )
        payload = opaque_dict(snap)
        payload["subject_code"] = subject.code
        payload["status"] = snap.publication_state
        payload["notes"] = notes
        payload["parent_version_id"] = parent_version_id
        return payload

    def get_version_summary(self, version_id: str) -> dict[str, Any] | None:
        try:
            snap = self._facade.versions.get_version(version_id)
            payload = opaque_dict(snap)
            payload["status"] = snap.publication_state
            return payload
        except Exception:
            return None

    def list_versions(self, subject_code: str) -> tuple[dict[str, Any], ...]:
        subject = self._facade.subjects.get_subject_by_code(subject_code)
        rows = []
        for snap in self._facade.versions.list_versions(
            subject_id=subject.subject_id
        ):
            payload = opaque_dict(snap)
            payload["subject_code"] = subject.code
            payload["status"] = snap.publication_state
            rows.append(payload)
        return tuple(rows)

    def archive_version(
        self, version_id: str, *, occurred_at: str = ""
    ) -> dict[str, Any]:
        return self.archive(version_id, occurred_at=occurred_at)

    def rollback_version(
        self, version_id: str, *, occurred_at: str = ""
    ) -> dict[str, Any]:
        # Rollback is owned by Management release semantics; surface
        # through releases when eligible. Foundation maps to archive+note.
        _ = occurred_at
        ver = self._facade.versions.get_version(version_id)
        payload = opaque_dict(ver)
        payload["status"] = ver.publication_state
        payload["rollback_requested"] = True
        return payload

    def add_asset_ref(
        self,
        version_id: str,
        *,
        kind: str,
        reference: str,
        asset_id: str | None = None,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        self._facade.assets.add_asset(
            version_id,
            kind,
            reference,
            label=reference,
            asset_id=asset_id,
        )
        return {
            "asset_id": asset_id or reference,
            "kind": kind,
            "reference": reference,
            "version_id": version_id,
        }

    def list_assets(self, version_id: str) -> tuple[dict[str, Any], ...]:
        snap = self._facade.versions.get_version(version_id)
        kinds = getattr(snap, "asset_kinds", ()) or ()
        return tuple(
            {"version_id": version_id, "kind": k} for k in kinds
        )

    def assign_blueprint(
        self,
        version_id: str,
        *,
        section_id: str,
        blueprint_profile_id: str,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        snap = self._facade.assignments.assign(
            version_id,
            section_id,
            blueprint_profile_id,
        )
        return opaque_dict(snap)

    def validate_version(self, version_id: str) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        snap = self._facade.validation.validate(version_id)
        ids = CorrelationContext.current()
        self._events.publish(
            curriculum_validated(
                {
                    "version_id": version_id,
                    "passed": getattr(snap, "passed", None),
                },
                correlation_id=ids.correlation_id,
                causation_id=ids.causation_id,
                source=self.ADAPTER_ID,
            )
        )
        return opaque_dict(snap)

    def latest_validation(self, version_id: str) -> dict[str, Any] | None:
        ver = self.get_version_summary(version_id)
        if ver is None:
            return None
        return ver.get("latest_validation")  # type: ignore[return-value]

    def preview_version(self, version_id: str) -> dict[str, Any]:
        snap = self._facade.previews.preview(version_id)
        return opaque_dict(snap)

    def approve(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        reviewer = (actor_id or "").strip() or "system"
        snap = self._facade.approvals.approve(
            version_id,
            reviewer,
            rationale=reason,
            decided_at=occurred_at or None,
        )
        return opaque_dict(snap)

    def reject(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
        reason: str = "",
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        reviewer = (actor_id or "").strip() or "system"
        snap = self._facade.approvals.reject(
            version_id,
            reviewer,
            rationale=reason,
            decided_at=occurred_at or None,
        )
        return opaque_dict(snap)

    def publication_state(self, version_id: str) -> str | None:
        ver = self.get_version_summary(version_id)
        if ver is None:
            return None
        state = ver.get("publication_state") or ver.get("status")
        return None if state is None else str(state)

    def publish(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        snap = self._facade.publications.publish(
            version_id,
            actor_id=actor_id,
            occurred_at=occurred_at or None,
        )
        ids = CorrelationContext.current()
        payload = opaque_dict(snap)
        self._events.publish(
            curriculum_published(
                {"version_id": version_id, **payload},
                correlation_id=ids.correlation_id,
                causation_id=ids.causation_id,
                source=self.ADAPTER_ID,
            )
        )
        return payload

    def archive(
        self,
        version_id: str,
        *,
        actor_id: str | None = None,
        occurred_at: str = "",
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        snap = self._facade.publications.archive(
            version_id,
            actor_id=actor_id,
            occurred_at=occurred_at or None,
        )
        return opaque_dict(snap)

    def _subject_summary_dict(self, subject_code: str) -> dict[str, Any]:
        rows = self._facade.subjects.list_subjects()
        code = subject_code.strip().upper()
        for row in rows:
            if row.code == code:
                return opaque_dict(
                    {
                        "subject_code": row.code,
                        "title": row.title,
                        "subject_id": row.subject_id,
                        "active_version_id": row.active_version_id,
                        "version_count": row.version_count,
                        "publication_state": row.publication_state,
                        "metadata": {},
                    }
                )
        snap = self._facade.subjects.get_subject_by_code(subject_code)
        return opaque_dict(
            {
                "subject_code": snap.code,
                "title": snap.title,
                "subject_id": snap.subject_id,
                "active_version_id": snap.active_version_id,
                "version_count": snap.version_count,
                "publication_state": None,
                "metadata": {},
            }
        )

"""CurriculumIngestionAdapter — implements CurriculumIngestionPort."""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentEntryPayload,
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.ingestion_engine import (
    CurriculumIngestionEngine,
)
from app.infrastructure._opaque import opaque_dict
from app.infrastructure.diagnostics.adapter_diagnostics import AdapterDiagnostics
from app.infrastructure.diagnostics.correlation import CorrelationContext
from app.infrastructure.events.registry import EventRegistry
from app.infrastructure.events.types import curriculum_validated


class CurriculumIngestionAdapter:
    """Production adapter for CurriculumIngestionPort.

    Delegates to Curriculum Ingestion application engine.
    Never parses PDF bytes. Owns no syllabus authority.
    """

    ADAPTER_ID = "curriculum_ingestion"
    ADAPTER_VERSION = "1.0.0"

    def __init__(
        self,
        engine: CurriculumIngestionEngine | None = None,
        *,
        events: EventRegistry | None = None,
        diagnostics: AdapterDiagnostics | None = None,
        available: bool = True,
    ) -> None:
        self._engine = engine or CurriculumIngestionEngine()
        self._events = events or EventRegistry()
        self._diagnostics = diagnostics or AdapterDiagnostics()
        self._jobs: dict[str, dict[str, Any]] = {}
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

    def is_available(self) -> bool:
        return self._available

    def set_available(self, available: bool) -> None:
        self._available = available
        self._diagnostics.record_health(
            self.ADAPTER_ID,
            available=available,
            version=self.ADAPTER_VERSION,
        )

    def start_ingestion(
        self,
        *,
        subject_code: str,
        sources: tuple[dict[str, Any], ...] | list[dict[str, Any]],
        job_id: str | None = None,
    ) -> dict[str, Any]:
        self._diagnostics.record_call(self.ADAPTER_ID)
        jid = (job_id or "").strip() or f"job-{uuid4().hex[:12]}"
        documents = tuple(self._document_from_source(s) for s in sources)
        request = IngestionRequest(
            job_id=jid,
            documents=documents,
            metadata=(("subject_code", subject_code.strip().upper()),),
            require_pass=False,
        )
        snapshot = self._engine.ingest(request)
        payload = opaque_dict(snapshot)
        payload["subject_code"] = subject_code.strip().upper()
        payload["job_id"] = jid
        self._jobs[jid] = payload
        ids = CorrelationContext.current()
        report = payload.get("validation") or payload.get("report")
        if report is not None:
            self._events.publish(
                curriculum_validated(
                    {"job_id": jid, "report": report},
                    correlation_id=ids.correlation_id,
                    causation_id=ids.causation_id,
                    source=self.ADAPTER_ID,
                )
            )
        return dict(payload)

    def get_ingestion_summary(self, job_id: str) -> dict[str, Any] | None:
        item = self._jobs.get(job_id)
        return None if item is None else dict(item)

    def normalised_structure(self, job_id: str) -> dict[str, Any] | None:
        item = self._jobs.get(job_id)
        if item is None:
            return None
        structure = item.get("normalization") or item.get("package")
        return None if structure is None else opaque_dict(structure)

    def get_validation_report(self, job_id: str) -> dict[str, Any] | None:
        item = self._jobs.get(job_id)
        if item is None:
            return None
        report = item.get("validation") or item.get("report")
        return None if report is None else opaque_dict(report)

    def _document_from_source(self, source: dict[str, Any]) -> DocumentPayload:
        entries_raw = source.get("entries") or ()
        entries = tuple(
            DocumentEntryPayload(
                entry_id=str(e.get("entry_id") or f"e-{i}"),
                entry_type=str(e.get("entry_type") or "topic"),
                text=str(e.get("text") or e.get("title") or "entry"),
                number=e.get("number"),
                parent_ref=e.get("parent_ref"),
            )
            for i, e in enumerate(entries_raw)
        )
        if not entries:
            entries = (
                DocumentEntryPayload(
                    entry_id="e-1",
                    entry_type="topic",
                    text=str(source.get("title") or "Untitled"),
                ),
            )
        source_ref = str(
            source.get("source_ref") or source.get("reference") or "ref"
        )
        return DocumentPayload(
            document_id=str(source.get("document_id") or uuid4().hex[:10]),
            source_ref=source_ref,
            title=str(source.get("title") or "Document"),
            entries=entries,
            declared_kind=source.get("declared_kind"),
        )

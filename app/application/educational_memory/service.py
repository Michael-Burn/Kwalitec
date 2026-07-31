"""Educational Memory service facade (KWP-011).

Persistence and projection only — never redesigns Strategy, Diagnostics,
Difficulty, Effectiveness, Evidence, Progress, Twin, or Runtime.
"""

from __future__ import annotations

from typing import Any

from app.application.educational_memory.dto import (
    IntelligenceSnapshot,
    LearningJourneyNarrative,
)
from app.application.educational_memory.narrative import (
    build_learning_journey_narrative,
)
from app.application.educational_memory.snapshot import (
    attach_snapshot_to_package,
    capture_intelligence_snapshot,
    resolve_prior_from_packages,
    snapshot_from_package,
    student_report_metadata_pairs,
)


class EducationalMemoryService:
    """Capture sitting intelligence and project longitudinal memory."""

    def capture_for_package(
        self,
        package: dict[str, Any],
        *,
        prior_packages: list[dict[str, Any]] | tuple[dict[str, Any], ...] = (),
        metadata: dict[str, Any] | None = None,
        twin_signals: dict[str, Any] | None = None,
        cadence: dict[str, Any] | None = None,
    ) -> tuple[dict[str, Any], IntelligenceSnapshot]:
        """Capture EI outputs onto ``package`` and return (updated, snapshot).

        Auto-attaches prior intervention from the learner's last same-topic
        sitting when available (KWP-010 continuity).
        """
        prior = resolve_prior_from_packages(
            prior_packages,
            student_id=str(package.get("student_id") or ""),
            topic_title=str(package.get("topic_title") or ""),
            topic_id=str(package.get("topic_id") or ""),
            exclude_session_id=str(package.get("session_id") or ""),
        )
        snapshot = capture_intelligence_snapshot(
            package,
            prior=prior,
            metadata=metadata,
            twin_signals=twin_signals,
            cadence=cadence,
        )
        return attach_snapshot_to_package(package, snapshot), snapshot

    def persist_on_store(
        self,
        *,
        store: Any,
        session_id: str,
        package: dict[str, Any] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> IntelligenceSnapshot | None:
        """Load package from store (or use provided), capture, and re-save.

        Uses ``lsr.evidence_package`` namespace via store helpers when present.
        """
        sid = (session_id or "").strip()
        if not sid or store is None:
            return None

        pkg = package
        if pkg is None:
            pkg = _load_package(store, sid)
        if not isinstance(pkg, dict) or not pkg:
            return None

        # Idempotent: keep existing snapshot rather than rebuilding with
        # possibly different Twin enrichments.
        existing = snapshot_from_package(pkg)
        if existing is not None and existing.has_student_report:
            return existing

        prior_packages = _list_packages(store)
        updated, snapshot = self.capture_for_package(
            pkg,
            prior_packages=prior_packages,
            metadata=metadata,
        )
        _save_package(store, sid, updated)
        return snapshot

    def journey_for_student(
        self,
        *,
        store: Any = None,
        packages: list[dict[str, Any]] | tuple[dict[str, Any], ...] | None = None,
        student_id: str,
    ) -> LearningJourneyNarrative:
        """Build My Learning Journey from store packages or an explicit list."""
        rows = list(packages or ())
        if not rows and store is not None:
            rows = _list_packages(store)
        return build_learning_journey_narrative(rows, student_id=student_id)

    def snapshot_for_session(
        self, *, store: Any, session_id: str
    ) -> IntelligenceSnapshot | None:
        pkg = _load_package(store, session_id)
        return snapshot_from_package(pkg)

    @staticmethod
    def metadata_pairs_for_snapshot(
        snapshot: IntelligenceSnapshot,
    ) -> list[tuple[str, str]]:
        return student_report_metadata_pairs(snapshot)


_SERVICE: EducationalMemoryService | None = None


def get_educational_memory_service() -> EducationalMemoryService:
    global _SERVICE
    if _SERVICE is None:
        _SERVICE = EducationalMemoryService()
    return _SERVICE


def _list_packages(store: Any) -> list[dict[str, Any]]:
    from app.services.educational_yield_metrics import list_evidence_packages

    return list_evidence_packages(store)


def _load_package(store: Any, session_id: str) -> dict[str, Any] | None:
    sid = session_id.strip()
    get = getattr(store, "get", None)
    if callable(get):
        doc = get("lsr.evidence_package", sid)
        return doc if isinstance(doc, dict) else None
    docs = getattr(store, "_docs", None)
    if isinstance(docs, dict):
        doc = docs.get(("lsr.evidence_package", sid))
        return dict(doc) if isinstance(doc, dict) else None
    return None


def _save_package(store: Any, session_id: str, package: dict[str, Any]) -> None:
    save = getattr(store, "save", None)
    if callable(save):
        save("lsr.evidence_package", session_id.strip(), package)

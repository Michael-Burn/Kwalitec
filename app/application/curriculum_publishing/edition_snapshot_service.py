"""Edition snapshot capture for history and comparison (EI-003)."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from uuid import uuid4

from app.application.curriculum_publishing.edition_graph_loader import (
    EditionGraphLoader,
)
from app.extensions import db
from app.models.curriculum_knowledge_graph import CkgEditionSnapshot


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class EditionSnapshotService:
    """Capture immutable structural snapshots of CKG editions."""

    def __init__(self, loader: EditionGraphLoader | None = None) -> None:
        self._loader = loader or EditionGraphLoader()

    def capture(
        self,
        edition_id: str,
        *,
        capture_reason: str,
        captured_by: str = "",
    ) -> str:
        """Persist a structural snapshot. Returns snapshot_id."""
        edition = self._loader.require_edition(edition_id)
        payload = self._loader.structural_snapshot(edition_id)
        snapshot_id = f"ckgsnap-{uuid4().hex[:12]}"
        db.session.add(
            CkgEditionSnapshot(
                snapshot_id=snapshot_id,
                edition_id=edition_id,
                subject_code=edition.subject_code,
                capture_reason=capture_reason,
                snapshot_json=json.dumps(payload, sort_keys=True),
                node_count=len(payload.get("nodes", [])),
                edge_count=len(payload.get("edges", [])),
                captured_at=_utc_now(),
                captured_by=(captured_by or "").strip(),
            )
        )
        return snapshot_id

    def latest_for_edition(self, edition_id: str) -> CkgEditionSnapshot | None:
        return (
            CkgEditionSnapshot.query.filter_by(edition_id=edition_id)
            .order_by(CkgEditionSnapshot.captured_at.desc())
            .first()
        )

    def load_payload(self, snapshot_id: str) -> dict:
        row = CkgEditionSnapshot.query.filter_by(snapshot_id=snapshot_id).first()
        if row is None:
            return {}
        return json.loads(row.snapshot_json or "{}")

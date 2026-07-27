"""Local development vector store — SQL-backed, no external vector DB.

The remainder of the application depends only on VectorStorePort.
"""

from __future__ import annotations

import json
import math
from typing import Any

from app.application.curriculum_retrieval.ports.vector_store_port import (
    VectorHit,
    VectorStorePort,
)
from app.extensions import db
from app.infrastructure.adapters.curriculum_retrieval.hashing_embedding_model import (
    cosine_similarity,
)
from app.models.curriculum_intelligence import CipLocalVectorEntry


class LocalVectorStoreAdapter(VectorStorePort):
    """Persist vectors in ``cip_local_vector_entries`` (infrastructure table)."""

    def upsert(
        self,
        *,
        vector_id: str,
        vector: tuple[float, ...],
        metadata: dict[str, str] | None = None,
    ) -> None:
        meta = metadata or {}
        row = CipLocalVectorEntry.query.filter_by(vector_id=vector_id).first()
        payload = json.dumps(list(vector), separators=(",", ":"))
        meta_json = json.dumps(meta, sort_keys=True, separators=(",", ":"))
        if row is None:
            row = CipLocalVectorEntry(
                vector_id=vector_id,
                dimensions=len(vector),
                vector_json=payload,
                metadata_json=meta_json,
            )
            db.session.add(row)
        else:
            row.dimensions = len(vector)
            row.vector_json = payload
            row.metadata_json = meta_json
        db.session.flush()

    def delete(self, vector_id: str) -> None:
        row = CipLocalVectorEntry.query.filter_by(vector_id=vector_id).first()
        if row is not None:
            db.session.delete(row)
            db.session.flush()

    def get(self, vector_id: str) -> tuple[float, ...] | None:
        row = CipLocalVectorEntry.query.filter_by(vector_id=vector_id).first()
        if row is None:
            return None
        return _parse_vector(row.vector_json)

    def count(self, *, filter_metadata: dict[str, str] | None = None) -> int:
        rows = CipLocalVectorEntry.query.all()
        if not filter_metadata:
            return len(rows)
        return sum(1 for row in rows if _metadata_matches(row, filter_metadata))

    def search(
        self,
        *,
        query_vector: tuple[float, ...],
        limit: int = 10,
        filter_metadata: dict[str, str] | None = None,
    ) -> list[VectorHit]:
        rows = CipLocalVectorEntry.query.all()
        scored: list[tuple[float, str, dict[str, str]]] = []
        for row in rows:
            meta = _parse_metadata(row.metadata_json)
            if filter_metadata and not _metadata_matches(row, filter_metadata):
                continue
            stored = _parse_vector(row.vector_json)
            if stored is None:
                continue
            score = cosine_similarity(query_vector, stored)
            scored.append((score, row.vector_id, meta))

        # Deterministic: score desc, then vector_id asc.
        scored.sort(key=lambda item: (-item[0], item[1]))
        hits: list[VectorHit] = []
        for score, vector_id, meta in scored[: max(0, limit)]:
            hits.append(
                VectorHit(
                    vector_id=vector_id,
                    score=float(score),
                    metadata=tuple(sorted(meta.items())),
                )
            )
        return hits


def _parse_vector(raw: str) -> tuple[float, ...] | None:
    try:
        data = json.loads(raw or "[]")
    except json.JSONDecodeError:
        return None
    if not isinstance(data, list):
        return None
    return tuple(float(x) for x in data)


def _parse_metadata(raw: str) -> dict[str, str]:
    try:
        data = json.loads(raw or "{}")
    except json.JSONDecodeError:
        return {}
    if not isinstance(data, dict):
        return {}
    return {str(k): str(v) for k, v in data.items()}


def _metadata_matches(row: CipLocalVectorEntry, filters: dict[str, str]) -> bool:
    meta = _parse_metadata(row.metadata_json)
    for key, expected in filters.items():
        if meta.get(key) != expected:
            return False
    return True


def euclidean_norm(vector: tuple[float, ...]) -> float:
    """Helper for diagnostics/tests."""
    return math.sqrt(sum(v * v for v in vector))


def coerce_metadata(value: Any) -> dict[str, str]:
    if not isinstance(value, dict):
        return {}
    return {str(k): str(v) for k, v in value.items()}

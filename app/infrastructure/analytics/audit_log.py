"""In-memory audit log for privacy / retention unit tests (EP-002)."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


@dataclass
class MemoryAnalyticsAuditLog:
    """Process-local audit append/list/export for tests."""

    _entries: list[dict] = field(default_factory=list)

    def append(
        self,
        *,
        action: str,
        user_id: int | None = None,
        detail: dict | None = None,
    ) -> str:
        audit_id = uuid4().hex
        self._entries.append(
            {
                "audit_id": audit_id,
                "action": action,
                "user_id": user_id,
                "detail": dict(detail or {}),
                "created_at": datetime.now(tz=UTC).isoformat(),
            }
        )
        return audit_id

    def list_actions(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 500,
    ) -> list[dict]:
        rows = list(reversed(self._entries))
        if action:
            rows = [r for r in rows if r["action"] == action]
        if user_id is not None:
            rows = [r for r in rows if r["user_id"] == user_id]
        return rows[:limit]

    def export_jsonl(
        self,
        *,
        action: str | None = None,
        user_id: int | None = None,
        limit: int = 10_000,
    ) -> str:
        entries = self.list_actions(action=action, user_id=user_id, limit=limit)
        return "\n".join(
            json.dumps(e, separators=(",", ":"), sort_keys=True) for e in entries
        )

"""UUID identity adapter for production runtime (INF-006)."""

from __future__ import annotations

from uuid import uuid4

from application.ports.uuid_generator import UUIDGenerator


class SystemUUIDGenerator(UUIDGenerator):
    """Generate opaque UUID4 string identities."""

    def new_id(self) -> str:
        return str(uuid4())


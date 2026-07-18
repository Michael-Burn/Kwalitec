"""Version 2 production integration layer.

Wires framework-independent application ports to persistence, events,
observability, and host infrastructure (Flask / SQLAlchemy / logging).

Owns no educational rules. Owns no domain algorithm authority.
Prefer explicit imports such as
``app.infrastructure.adapters.student_twin.adapter.StudentTwinAdapter``.
"""

from __future__ import annotations

__all__ = [
    "INFRASTRUCTURE_VERSION",
]

INFRASTRUCTURE_VERSION = "v2-017-1.0.0"

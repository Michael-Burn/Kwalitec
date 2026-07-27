"""Version 2 production integration layer.

Wires framework-independent application ports to persistence, events,
observability, and host infrastructure (Flask / SQLAlchemy / logging).

Owns no educational rules. Owns no domain algorithm authority.
Prefer explicit imports such as
``app.infrastructure.adapters.student_twin.adapter.StudentTwinAdapter``.
"""

from __future__ import annotations

# Eagerly bind curriculum retrieval default ports (embedding model / vector
# store) so application services that construct without explicit injection
# resolve production adapters as soon as infrastructure is touched at all.
# Bind Educational State analytics port outside analytics/ (import-guard).
from app.application.educational_state import (  # noqa: E402
    bind_educational_state_analytics_port,
)
from app.infrastructure.adapters import (  # noqa: E402,F401
    curriculum_retrieval as _curriculum_retrieval,
)
from app.infrastructure.analytics.educational_state_events import (  # noqa: E402
    InfrastructureEducationalStateAnalyticsPort,
)

__all__ = [
    "INFRASTRUCTURE_VERSION",
]

INFRASTRUCTURE_VERSION = "v2-020a-1.0.0"

bind_educational_state_analytics_port(InfrastructureEducationalStateAnalyticsPort())

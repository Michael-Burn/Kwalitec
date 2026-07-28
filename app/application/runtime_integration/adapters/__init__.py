"""Surface adapters — Experience Models → runtime view dicts (RI-001).

Presentation mapping only. Adapters never alter educational decisions,
re-rank recommendations, or call Runtime A.
"""

from __future__ import annotations

from app.application.runtime_integration.adapters.coach_adapter import (
    map_coach_context,
)
from app.application.runtime_integration.adapters.dashboard_adapter import (
    map_dashboard_card,
    map_dashboard_recommendation,
)
from app.application.runtime_integration.adapters.mission_adapter import (
    map_daily_mission,
)
from app.application.runtime_integration.adapters.revision_adapter import (
    map_revision_entry,
)
from app.application.runtime_integration.adapters.session_adapter import (
    map_session_briefing,
)

__all__ = [
    "map_coach_context",
    "map_daily_mission",
    "map_dashboard_card",
    "map_dashboard_recommendation",
    "map_revision_entry",
    "map_session_briefing",
]

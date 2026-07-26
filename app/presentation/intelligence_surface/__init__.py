"""Runtime A intelligence-surface presentation (EP-002.8).

Presentation owns presentation. Selects communication by ``source_authority``;
never evaluates readiness, plans missions, or invents insights.
"""

from __future__ import annotations

from app.presentation.intelligence_surface.adapter import RuntimeAPresentationAdapter

__all__ = ["RuntimeAPresentationAdapter"]

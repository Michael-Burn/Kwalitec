"""HTTP blueprints for the Educational Operating System web surface."""

from __future__ import annotations

from web.blueprints.dashboard import dashboard_bp
from web.blueprints.learning import learning_bp

__all__ = ["dashboard_bp", "learning_bp"]

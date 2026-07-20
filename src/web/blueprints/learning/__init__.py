"""Learning API blueprint — thin HTTP surface over application services."""

from __future__ import annotations

from web.blueprints.learning.routes import learning_bp

__all__ = ["learning_bp"]

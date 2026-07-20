"""Application layer for the Educational Operating System.

Coordinates domain behaviour. Contains no educational intelligence.

Allowed: load repositories, invoke aggregates, commit, publish application
events, return DTOs.

Forbidden: mastery calculation, prioritisation, diagnosis, strategy selection,
Flask, SQLAlchemy, HTTP, or persistence implementations.
"""

from __future__ import annotations

__all__: list[str] = []

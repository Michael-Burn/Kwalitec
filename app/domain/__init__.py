"""Pure domain layer for Kwalitec.

Framework-independent conceptual objects. Must not import Flask, SQLAlchemy,
blueprints, HTTP, or persistence concerns.

Subpackages include ``evidence``, ``learning_events``, ``twin`` (write-path
learner state + Update Pipeline), ``readiness`` (read-side aggregation),
``decision`` (read-side next-action selection), ``recommendation``
(read-side Decision packaging), and ``mission`` (execution-layer Decision
operationalisation into Mission / MissionTask). Prefer explicit imports such
as ``app.domain.mission`` over a facade re-export.
"""

from __future__ import annotations

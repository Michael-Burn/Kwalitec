"""Pure domain layer for Kwalitec.

Framework-independent conceptual objects. Must not import Flask, SQLAlchemy,
blueprints, HTTP, or persistence concerns.

Subpackages include ``evidence``, ``learning_events``, ``twin`` (write-path
learner state + Update Pipeline), ``readiness`` (read-side aggregation),
``decision`` (read-side next-action selection), ``recommendation``
(read-side Decision packaging), ``mission`` (execution-layer Decision
operationalisation into Mission / MissionTask), ``learning_journey``
(Version 2 Learning Journey domain foundation), ``learning_activity``
(Version 2 Learning Activity domain), ``curriculum``
(Version 2 Curriculum Graph educational knowledge model), and
``instructional_blueprint`` (Version 2 pedagogical HOW-to-teach strategies),
``curriculum_management`` (Version 2 curriculum asset / publication
management), ``curriculum_studio`` (Version 2 Founder Curriculum Studio
foundation), ``student_twin`` (Version 2 Student Digital Twin),
``adaptive_learning`` (Version 2 Adaptive Decision Engine — Phase 1
revision), and ``student_experience`` (Version 2 learner product
projection / navigation). Prefer explicit imports such as
``app.domain.mission`` over a facade re-export.
"""

from __future__ import annotations

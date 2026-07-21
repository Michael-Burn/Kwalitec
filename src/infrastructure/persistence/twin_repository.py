"""Production Student Twin persistence adapter (BR-004).

Re-exports the Education OS digital-twin SQLAlchemy repository under the
BR-004 surface name. Behaviour is unchanged.
"""

from __future__ import annotations

from infrastructure.persistence.sqlalchemy.repositories.digital_twin_repository import (
    SqlAlchemyDigitalTwinRepository as SqlAlchemyTwinRepository,
)

__all__ = ["SqlAlchemyTwinRepository"]

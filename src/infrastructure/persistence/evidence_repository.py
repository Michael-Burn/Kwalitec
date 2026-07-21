"""Production Evidence persistence adapter (BR-004).

Re-exports the Education OS evidence SQLAlchemy repository under the BR-004
package surface. Behaviour is unchanged.
"""

from __future__ import annotations

from infrastructure.persistence.sqlalchemy.repositories.evidence_repository import (
    SqlAlchemyEvidenceRepository,
)

__all__ = ["SqlAlchemyEvidenceRepository"]

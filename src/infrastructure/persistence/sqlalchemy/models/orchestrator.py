"""SQLAlchemy persistence model for EducationalOrchestrator storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class OrchestratorModel(Base):
    """Persistence row for an orchestrator aggregate snapshot."""

    __tablename__ = "eos_orchestrators"

    orchestrator_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    decision_reference: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    strategy_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    plan: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    episode_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    state: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)

"""SQLAlchemy persistence model for EducationalDecision storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class DecisionModel(Base):
    """Persistence row for a decision aggregate snapshot."""

    __tablename__ = "eos_decisions"

    decision_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    priority_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    intention_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    strategy_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    indicators: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    constraints: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    reasons: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    readiness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    outcome: Mapped[str | None] = mapped_column(String(64), nullable=True)
    reconsideration_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

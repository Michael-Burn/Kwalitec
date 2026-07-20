"""SQLAlchemy persistence model for TeachingStrategy storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class TeachingStrategyModel(Base):
    """Persistence row for a teaching strategy aggregate snapshot."""

    __tablename__ = "eos_teaching_strategies"

    strategy_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    primary_strategy: Mapped[str] = mapped_column(String(64), nullable=False)
    goal: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    rationale: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    effectiveness: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    complexity: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    intention_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    diagnosis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    hypothesis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    secondary_strategies: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    constraints: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    composition_pattern: Mapped[str | None] = mapped_column(String(128), nullable=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

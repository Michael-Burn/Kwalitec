"""SQLAlchemy persistence model for EducationalPriority storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class PriorityModel(Base):
    """Persistence row for a priority aggregate snapshot."""

    __tablename__ = "eos_priorities"

    priority_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    diagnosis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    hypothesis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    factors: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    score: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    urgency: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    instructional_impact: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    constraints: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    stabilisation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

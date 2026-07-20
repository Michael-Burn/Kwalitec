"""SQLAlchemy persistence model for TeachingIntention storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class TeachingIntentionModel(Base):
    """Persistence row for a teaching intention aggregate snapshot."""

    __tablename__ = "eos_teaching_intentions"

    intention_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    intention_type: Mapped[str] = mapped_column(String(64), nullable=False)
    goal: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    expected_outcome: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    strength: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    priority_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    diagnosis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    hypothesis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    constraints: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    retire_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

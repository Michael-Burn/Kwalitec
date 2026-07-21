"""SQLAlchemy persistence model for OnboardingSession drafts (BR-004)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class OnboardingSessionModel(Base):
    """Persistence row for an onboarding draft session."""

    __tablename__ = "eos_onboarding_sessions"

    onboarding_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    current_step: Mapped[str] = mapped_column(String(64), nullable=False)
    payloads: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    saved_steps: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    row_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

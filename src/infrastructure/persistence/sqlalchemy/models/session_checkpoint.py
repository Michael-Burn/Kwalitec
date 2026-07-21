"""SQLAlchemy persistence model for Session Runtime checkpoints (BR-004)."""

from __future__ import annotations

from datetime import datetime
from typing import Any

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class SessionCheckpointModel(Base):
    """Persistence row for a serialized session event log."""

    __tablename__ = "eos_session_checkpoints"

    session_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    events: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    row_version: Mapped[int] = mapped_column(Integer, nullable=False, default=1)

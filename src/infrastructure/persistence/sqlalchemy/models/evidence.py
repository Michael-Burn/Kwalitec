"""SQLAlchemy persistence model for EvidenceRecord storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class EvidenceModel(Base):
    """Persistence row for an evidence record aggregate snapshot."""

    __tablename__ = "eos_evidence_records"

    evidence_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    items: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    source: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    context: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    strength: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    timestamp: Mapped[str] = mapped_column(String(64), nullable=False)
    known_concept_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    known_episode_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    concept_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    learning_episode_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    invalidation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

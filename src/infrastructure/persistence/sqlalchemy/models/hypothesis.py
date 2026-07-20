"""SQLAlchemy persistence model for EducationalHypothesis storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class HypothesisModel(Base):
    """Persistence row for a hypothesis aggregate snapshot."""

    __tablename__ = "eos_hypotheses"

    hypothesis_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    hypothesis_kind: Mapped[str] = mapped_column(String(64), nullable=False)
    explanation: Mapped[str] = mapped_column(Text, nullable=False)
    scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    plausibility: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    explanatory_strength: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    diagnosis_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    reasons: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    interpretation_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    evidence_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    competing_hypotheses: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    known_evidence_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    known_interpretation_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    discard_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

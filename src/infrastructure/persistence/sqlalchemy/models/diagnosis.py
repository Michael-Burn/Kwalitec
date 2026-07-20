"""SQLAlchemy persistence model for EducationalDiagnosis storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class DiagnosisModel(Base):
    """Persistence row for a diagnosis aggregate snapshot."""

    __tablename__ = "eos_diagnoses"

    diagnosis_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    diagnosis_type: Mapped[str] = mapped_column(String(64), nullable=False)
    scope: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    severity: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    indicators: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    reasons: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    known_evidence_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    known_interpretation_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    interpretation_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    invalidation_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

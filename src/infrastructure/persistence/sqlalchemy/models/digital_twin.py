"""SQLAlchemy persistence model for EducationalDigitalTwin storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class DigitalTwinModel(Base):
    """Persistence row for a digital twin aggregate snapshot."""

    __tablename__ = "eos_digital_twins"

    twin_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    learner_state: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    concept_states: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    misconception_states: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    evidence_history: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    intervention_history: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    retention: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    confidence: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    trajectory: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    status: Mapped[str] = mapped_column(String(64), nullable=False)

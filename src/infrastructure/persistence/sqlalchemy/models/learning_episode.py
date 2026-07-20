"""SQLAlchemy persistence model for LearningEpisode storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class LearningEpisodeModel(Base):
    """Persistence row for a learning episode aggregate snapshot."""

    __tablename__ = "eos_learning_episodes"

    episode_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    student_id: Mapped[str] = mapped_column(String(128), nullable=False, index=True)
    teaching_goal: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    teaching_strategy_id: Mapped[str] = mapped_column(String(128), nullable=False)
    learning_objectives: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    steps: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    concept_references: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    primary_dimension: Mapped[str] = mapped_column(String(64), nullable=False)
    duration: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    selection_rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(String(64), nullable=False)
    reflection: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    outcome: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)
    evidence_ids: Mapped[list[Any]] = mapped_column(JSON, nullable=False)

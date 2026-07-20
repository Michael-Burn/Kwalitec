"""SQLAlchemy persistence model for Concept storage."""

from __future__ import annotations

from typing import Any

from sqlalchemy import JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from infrastructure.persistence.sqlalchemy.base import Base


class ConceptModel(Base):
    """Persistence row for a subject-knowledge Concept aggregate snapshot."""

    __tablename__ = "eos_concepts"

    concept_id: Mapped[str] = mapped_column(String(128), primary_key=True)
    canonical_name: Mapped[str] = mapped_column(String(256), nullable=False)
    core_meaning: Mapped[str] = mapped_column(Text, nullable=False)
    boundary: Mapped[dict[str, Any]] = mapped_column(JSON, nullable=False)
    learning_objectives: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    representations: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    misconceptions: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    application_contexts: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    transfer_contexts: Mapped[list[Any]] = mapped_column(JSON, nullable=False)
    dependencies: Mapped[list[Any]] = mapped_column(JSON, nullable=False)

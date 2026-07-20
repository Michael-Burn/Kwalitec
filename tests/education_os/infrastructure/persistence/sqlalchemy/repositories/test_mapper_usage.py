"""Mapper usage tests — repositories must go through persistence mappers."""

from __future__ import annotations

from unittest.mock import patch

from infrastructure.persistence.sqlalchemy.repositories import (
    SqlAlchemyDigitalTwinRepository,
    SqlAlchemySubjectKnowledgeRepository,
)
from tests.education_os.infrastructure.persistence.conftest import (
    build_concept,
    build_digital_twin,
)


def test_digital_twin_save_uses_mapper(session) -> None:
    twin = build_digital_twin()
    twin.pull_events()
    repo = SqlAlchemyDigitalTwinRepository(session)

    with patch(
        "infrastructure.persistence.sqlalchemy.repositories."
        "digital_twin_repository.DigitalTwinMapper.to_persistence",
        wraps=__import__(
            "infrastructure.persistence.mappers.digital_twin_mapper",
            fromlist=["DigitalTwinMapper"],
        ).DigitalTwinMapper.to_persistence,
    ) as to_persistence:
        repo.save(twin)
        session.commit()
        assert to_persistence.called


def test_digital_twin_get_uses_mapper(session) -> None:
    twin = build_digital_twin()
    twin.pull_events()
    repo = SqlAlchemyDigitalTwinRepository(session)
    repo.save(twin)
    session.commit()

    with patch(
        "infrastructure.persistence.sqlalchemy.repositories."
        "digital_twin_repository.DigitalTwinMapper.to_domain",
        wraps=__import__(
            "infrastructure.persistence.mappers.digital_twin_mapper",
            fromlist=["DigitalTwinMapper"],
        ).DigitalTwinMapper.to_domain,
    ) as to_domain:
        loaded = repo.get(twin.twin_id)
        assert loaded is not None
        assert to_domain.called


def test_subject_knowledge_uses_mapper(session) -> None:
    concept = build_concept()
    repo = SqlAlchemySubjectKnowledgeRepository(session)

    with patch(
        "infrastructure.persistence.sqlalchemy.repositories."
        "subject_knowledge_repository.SubjectKnowledgeMapper.to_persistence",
        wraps=__import__(
            "infrastructure.persistence.mappers.subject_knowledge_mapper",
            fromlist=["SubjectKnowledgeMapper"],
        ).SubjectKnowledgeMapper.to_persistence,
    ) as to_persistence:
        repo.save_concept(concept)
        session.commit()
        assert to_persistence.called

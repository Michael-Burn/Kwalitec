"""CheckpointStore backed by SqlAlchemyProductUnitOfWork (BR-004.5)."""

from __future__ import annotations

from collections.abc import Callable

from infrastructure.persistence.sqlalchemy_uow import (
    SessionFactory,
    SqlAlchemyProductUnitOfWork,
)

ProductUnitOfWorkFactory = Callable[[], SqlAlchemyProductUnitOfWork]


class ProductCheckpointStore:
    """Persist session runtime checkpoints through the product unit of work.

    Each operation opens its own transactional unit so adapter controllers
    remain free of session lifecycle concerns.
    """

    def __init__(
        self,
        session_factory: SessionFactory | None = None,
        *,
        unit_of_work_factory: ProductUnitOfWorkFactory | None = None,
    ) -> None:
        if unit_of_work_factory is not None:
            self._uow_factory = unit_of_work_factory
        elif session_factory is not None:
            self._uow_factory = lambda: SqlAlchemyProductUnitOfWork(session_factory)
        else:
            raise TypeError(
                "provide session_factory or unit_of_work_factory"
            )

    def load(self, session_id: str) -> list[dict[str, object]] | None:
        with self._uow_factory() as uow:
            payload = uow.checkpoints.load(session_id)
            uow.commit()
            return payload

    def save(self, session_id: str, events: list[dict[str, object]]) -> None:
        with self._uow_factory() as uow:
            uow.checkpoints.save(session_id, events)
            uow.commit()

    def clear(self, session_id: str) -> None:
        with self._uow_factory() as uow:
            uow.checkpoints.clear(session_id)
            uow.commit()

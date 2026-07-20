"""Transaction manager port — low-level transaction boundary."""

from __future__ import annotations

from abc import ABC, abstractmethod


class TransactionManager(ABC):
    """Controls a persistence transaction without exposing repositories.

    Distinct from :class:`~application.ports.unit_of_work.UnitOfWork`, which
    also surfaces repository accessors. Adapters may implement both or compose
    a manager inside a unit of work.
    """

    @abstractmethod
    def begin(self) -> None:
        """Open a transaction boundary."""

    @abstractmethod
    def commit(self) -> None:
        """Persist work and close the boundary."""

    @abstractmethod
    def rollback(self) -> None:
        """Discard work and close the boundary."""

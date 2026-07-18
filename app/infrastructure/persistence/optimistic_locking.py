"""Optimistic locking helpers for mutable aggregates."""

from __future__ import annotations

from dataclasses import dataclass


class OptimisticLockError(Exception):
    """Raised when an expected version does not match the stored version."""


@dataclass(frozen=True)
class VersionToken:
    """Opaque optimistic-lock version for an aggregate instance."""

    aggregate_name: str
    aggregate_id: str
    version: int

    def next(self) -> VersionToken:
        """Return the successor token after a successful write."""
        return VersionToken(
            self.aggregate_name, self.aggregate_id, self.version + 1
        )


class OptimisticLockGuard:
    """Track aggregate versions and assert expected versions on write."""

    def __init__(self) -> None:
        self._versions: dict[tuple[str, str], int] = {}

    def current(self, aggregate_name: str, aggregate_id: str) -> int:
        """Return the current version (0 when unseen)."""
        return self._versions.get((aggregate_name, aggregate_id), 0)

    def token(self, aggregate_name: str, aggregate_id: str) -> VersionToken:
        """Build a VersionToken for the current stored version."""
        return VersionToken(
            aggregate_name,
            aggregate_id,
            self.current(aggregate_name, aggregate_id),
        )

    def assert_expected(
        self,
        aggregate_name: str,
        aggregate_id: str,
        expected: int,
    ) -> None:
        """Raise OptimisticLockError when expected version mismatches."""
        actual = self.current(aggregate_name, aggregate_id)
        if actual != expected:
            raise OptimisticLockError(
                f"{aggregate_name}:{aggregate_id} expected v{expected}, "
                f"got v{actual}"
            )

    def bump(
        self,
        aggregate_name: str,
        aggregate_id: str,
        *,
        expected: int | None = None,
    ) -> VersionToken:
        """Assert optional expected version and bump."""
        if expected is not None:
            self.assert_expected(aggregate_name, aggregate_id, expected)
        key = (aggregate_name, aggregate_id)
        self._versions[key] = self._versions.get(key, 0) + 1
        return self.token(aggregate_name, aggregate_id)

    def seed(self, aggregate_name: str, aggregate_id: str, version: int) -> None:
        """Seed a version (e.g. after load from storage)."""
        if version < 0:
            raise ValueError("version must be >= 0")
        self._versions[(aggregate_name, aggregate_id)] = version

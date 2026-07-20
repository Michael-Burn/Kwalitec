"""Educational result type for explicit success / failure outcomes.

Domain operations that can fail educationally return ``EducationalResult``
rather than mixing sentinel ``None`` values with exceptions for expected
failure modes. Construction still raises on invariant violation.
"""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from typing import Generic, TypeVar

from domain.education.foundation.errors import EducationalDomainError

T = TypeVar("T")
U = TypeVar("U")


@dataclass(frozen=True, slots=True)
class EducationalResult(Generic[T]):
    """Immutable success-or-failure wrapper for educational operations.

    Exactly one of ``value`` or ``error`` is present. Use ``ok`` / ``fail``
    factories — do not construct with both or neither.
    """

    _value: T | None
    _error: EducationalDomainError | None
    _is_success: bool

    @classmethod
    def ok(cls, value: T) -> EducationalResult[T]:
        """Build a successful educational result."""
        return cls(_value=value, _error=None, _is_success=True)

    @classmethod
    def fail(cls, error: EducationalDomainError | str) -> EducationalResult[T]:
        """Build a failed educational result.

        Args:
            error: Domain error instance or message string.
        """
        if isinstance(error, EducationalDomainError):
            domain_error = error
        else:
            domain_error = EducationalDomainError(str(error))
        return cls(_value=None, _error=domain_error, _is_success=False)

    @property
    def is_success(self) -> bool:
        """True when the result carries a value."""
        return self._is_success

    @property
    def is_failure(self) -> bool:
        """True when the result carries an educational error."""
        return not self._is_success

    @property
    def value(self) -> T:
        """Successful payload.

        Raises:
            EducationalDomainError: When the result is a failure.
        """
        if not self._is_success or self._error is not None:
            raise EducationalDomainError(
                "cannot read value from a failed EducationalResult"
            )
        return self._value  # type: ignore[return-value]

    @property
    def error(self) -> EducationalDomainError:
        """Failure payload.

        Raises:
            EducationalDomainError: When the result is a success.
        """
        if self._is_success or self._error is None:
            raise EducationalDomainError(
                "cannot read error from a successful EducationalResult"
            )
        return self._error

    def value_or(self, default: T) -> T:
        """Return the value on success, otherwise ``default``."""
        if self._is_success:
            return self._value  # type: ignore[return-value]
        return default

    def map(self, transform: Callable[[T], U]) -> EducationalResult[U]:
        """Map the success value; failures pass through unchanged."""
        if not self._is_success:
            return EducationalResult(
                _value=None, _error=self._error, _is_success=False
            )
        return EducationalResult.ok(transform(self._value))  # type: ignore[arg-type]

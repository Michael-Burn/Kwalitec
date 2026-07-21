"""Password policy — pure credential strength rules."""

from __future__ import annotations

from dataclasses import dataclass

from domain.auth.errors import AuthInvariantViolation


@dataclass(frozen=True, slots=True)
class PasswordPolicy:
    """Deterministic password strength requirements.

    Does not hash passwords. Does not persist. Does not call external services.
    """

    min_length: int = 12
    require_letter: bool = True
    require_digit: bool = True
    require_special: bool = True
    max_length: int = 128

    def validate(self, password: str) -> str:
        """Return the password when it satisfies policy; otherwise raise.

        Args:
            password: Candidate plaintext password.

        Returns:
            The same password when valid.

        Raises:
            AuthInvariantViolation: When the password fails policy checks.
        """
        if password is None:
            raise AuthInvariantViolation(
                "password is required",
                invariant="password_required",
            )
        if len(password) < self.min_length:
            raise AuthInvariantViolation(
                f"password must be at least {self.min_length} characters",
                invariant="password_min_length",
            )
        if len(password) > self.max_length:
            raise AuthInvariantViolation(
                f"password must be at most {self.max_length} characters",
                invariant="password_max_length",
            )
        if self.require_letter and not any(ch.isalpha() for ch in password):
            raise AuthInvariantViolation(
                "password must include a letter",
                invariant="password_require_letter",
            )
        if self.require_digit and not any(ch.isdigit() for ch in password):
            raise AuthInvariantViolation(
                "password must include a digit",
                invariant="password_require_digit",
            )
        if self.require_special and not any(
            not ch.isalnum() and not ch.isspace() for ch in password
        ):
            raise AuthInvariantViolation(
                "password must include a special character",
                invariant="password_require_special",
            )
        if any(ch.isspace() for ch in password):
            raise AuthInvariantViolation(
                "password must not contain whitespace",
                invariant="password_no_whitespace",
            )
        return password

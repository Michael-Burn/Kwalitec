"""Twin version — monotonic snapshot versioning."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TwinVersion:
    """Monotonic Twin snapshot version.

    Version numbers only increase. History is never rewritten.
    """

    major: int
    minor: int = 0
    patch: int = 0

    @classmethod
    def create(
        cls,
        major: int = 1,
        minor: int = 0,
        patch: int = 0,
    ) -> TwinVersion:
        """Construct a TwinVersion with non-negative components."""
        for name, value in (("major", major), ("minor", minor), ("patch", patch)):
            if not isinstance(value, int) or isinstance(value, bool):
                raise ValueError(f"{name} must be a non-negative integer")
            if value < 0:
                raise ValueError(f"{name} must be a non-negative integer")
        return cls(major=major, minor=minor, patch=patch)

    @classmethod
    def initial(cls) -> TwinVersion:
        """Return the initial Twin version (1.0.0)."""
        return cls.create(1, 0, 0)

    @property
    def label(self) -> str:
        """Dotted version label."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def bump_patch(self) -> TwinVersion:
        """Return a version with patch + 1 (evidence-driven snapshot)."""
        return TwinVersion(self.major, self.minor, self.patch + 1)

    def bump_minor(self) -> TwinVersion:
        """Return a version with minor + 1 and patch reset."""
        return TwinVersion(self.major, self.minor + 1, 0)

    def bump_major(self) -> TwinVersion:
        """Return a version with major + 1 and minor/patch reset."""
        return TwinVersion(self.major + 1, 0, 0)

    def precedes(self, other: TwinVersion) -> bool:
        """True when this version is strictly older than ``other``."""
        return (self.major, self.minor, self.patch) < (
            other.major,
            other.minor,
            other.patch,
        )

    def __str__(self) -> str:
        return self.label

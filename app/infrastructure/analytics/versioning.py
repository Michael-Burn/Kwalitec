"""Analytics event schema versions."""

from __future__ import annotations

from enum import IntEnum


class AnalyticsEventVersion(IntEnum):
    """Supported analytics event schema versions.

    Historical rows are never rewritten. Consumers upcast on read when
    later phases introduce newer schema versions.
    """

    V1 = 1

    @classmethod
    def coerce(cls, value: int | AnalyticsEventVersion) -> AnalyticsEventVersion:
        """Coerce an int or enum into a known schema version."""
        if isinstance(value, AnalyticsEventVersion):
            return value
        try:
            return cls(int(value))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"unsupported analytics schema_version: {value}") from exc

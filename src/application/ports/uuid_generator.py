"""UUID generator port — injectable identity source for application coordination."""

from __future__ import annotations

from abc import ABC, abstractmethod


class UUIDGenerator(ABC):
    """Generates opaque string identities for application workflows.

    Infrastructure may wrap ``uuid.uuid4`` or a deterministic test sequence.
    Application services must not call ``uuid.uuid4`` directly.
    """

    @abstractmethod
    def new_id(self) -> str:
        """Return a new unique identity string."""

"""Educational Policies — deterministic decision rules executed by Agents (EI-001C)."""

from __future__ import annotations

from abc import ABC, abstractmethod

from app.domain.curriculum_intelligence.policy import (
    PolicyDescriptor,
)


class EducationalPolicy(ABC):
    """Base Educational Policy — Agents execute; Policies decide."""

    @property
    @abstractmethod
    def descriptor(self) -> PolicyDescriptor:
        """Expose policy metadata."""

    @property
    def policy_id(self) -> str:
        return self.descriptor.policy_id

    @property
    def version(self) -> str:
        return self.descriptor.version

    @property
    def deterministic(self) -> bool:
        return self.descriptor.deterministic

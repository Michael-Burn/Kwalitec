"""Immutable context for one Twin Update Pipeline invocation.

Carries the current Twin snapshot, incoming Learning Evidence, and processing
metadata. Strategies read this context; they must not mutate it.
"""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass, field
from typing import Any

from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.twin.digital_twin import DigitalTwin


@dataclass(frozen=True)
class UpdateContext:
    """Immutable description of one Twin update pass.

    Attributes:
        twin: Current Digital Twin snapshot under consideration.
        evidence: Incoming Learning Evidence that may drive updates.
        metadata: Extensible processing bag (correlation ids, stage labels, …).
    """

    twin: DigitalTwin
    evidence: tuple[LearningEvidence, ...]
    metadata: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        twin: DigitalTwin,
        evidence: LearningEvidence | Sequence[LearningEvidence],
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> UpdateContext:
        """Construct an UpdateContext.

        Args:
            twin: Current Twin snapshot (not mutated).
            evidence: One Learning Evidence record or a sequence of records.
            metadata: Optional processing metadata (copied defensively).

        Returns:
            A frozen UpdateContext instance.
        """
        if isinstance(evidence, LearningEvidence):
            evidence_tuple: tuple[LearningEvidence, ...] = (evidence,)
        else:
            evidence_tuple = tuple(evidence)
        return cls(
            twin=twin,
            evidence=evidence_tuple,
            metadata=dict(metadata or {}),
        )

    def with_twin(self, twin: DigitalTwin) -> UpdateContext:
        """Return a new context with ``twin`` replaced.

        Args:
            twin: Next Twin snapshot after a strategy application.

        Returns:
            A new frozen UpdateContext sharing evidence and metadata copies.
        """
        return UpdateContext(
            twin=twin,
            evidence=self.evidence,
            metadata=dict(self.metadata),
        )

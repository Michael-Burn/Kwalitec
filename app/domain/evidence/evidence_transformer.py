"""Evidence Transformation Stage coordinator.

Receives one validated Evidence Candidate and returns one Learning Evidence
object by delegating to the first registered transformer that supports the
candidate. Performs normalization only — does not score, persist, recommend,
or update the Student Digital Twin.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.learning_evidence import LearningEvidence
from app.domain.evidence.transformers.base_transformer import BaseTransformer


class TransformationError(Exception):
    """Raised when no registered transformer supports a candidate."""


class EvidenceTransformer:
    """Registry-backed coordinator that invokes supporting transformers.

    Additional transformers are registered without modifying this class
    (open for extension). Invocation order follows registration order.
    The first transformer that reports ``supports(candidate)`` performs the
    normalization; later transformers are not consulted for that candidate.
    """

    def __init__(self, transformers: list[BaseTransformer] | None = None) -> None:
        """Initialise with an optional initial transformer list.

        Args:
            transformers: Transformers to register at construction time.
        """
        self._transformers: list[BaseTransformer] = list(transformers or [])

    def register(self, transformer: BaseTransformer) -> None:
        """Register a transformer for future invocations.

        Args:
            transformer: Strategy implementation to add to the registry.
        """
        self._transformers.append(transformer)

    @property
    def transformers(self) -> tuple[BaseTransformer, ...]:
        """Return a snapshot of registered transformers (registration order)."""
        return tuple(self._transformers)

    def transform(self, candidate: EvidenceCandidate) -> LearningEvidence:
        """Normalize ``candidate`` via the first supporting transformer.

        Args:
            candidate: Validated Evidence Candidate to normalize. Not mutated.
                Callers must only pass candidates accepted by the Validation
                Stage.

        Returns:
            One immutable LearningEvidence object.

        Raises:
            TransformationError: If no registered transformer supports the
                candidate.

        Notes:
            Does not score, persist, recommend, or mutate Twin state.
        """
        for transformer in self._transformers:
            if transformer.supports(candidate):
                return transformer.transform(candidate)
        raise TransformationError(
            f"No registered transformer supports candidate "
            f"{candidate.identifier!r} "
            f"(category={candidate.category.value!r})"
        )

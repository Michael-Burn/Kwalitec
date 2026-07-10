"""Evidence Extraction Engine coordinator.

Receives a Learning Event and returns zero or more Evidence Candidates by
delegating to registered extractors. Does not persist, score, or update the
Student Digital Twin.
"""

from __future__ import annotations

from app.domain.evidence.evidence_candidate import EvidenceCandidate
from app.domain.evidence.extractors.base_extractor import BaseExtractor
from app.domain.learning_events.learning_event import LearningEvent


class EvidenceExtractor:
    """Registry-backed coordinator that invokes supporting extractors.

    Additional extractors are registered without modifying this class
    (open for extension). Invocation order follows registration order.
    Multiple extractors may contribute candidates for the same event.
    """

    def __init__(self, extractors: list[BaseExtractor] | None = None) -> None:
        """Initialise with an optional initial extractor list.

        Args:
            extractors: Extractors to register at construction time.
        """
        self._extractors: list[BaseExtractor] = list(extractors or [])

    def register(self, extractor: BaseExtractor) -> None:
        """Register an extractor for future invocations.

        Args:
            extractor: Strategy implementation to add to the registry.
        """
        self._extractors.append(extractor)

    @property
    def extractors(self) -> tuple[BaseExtractor, ...]:
        """Return a snapshot of registered extractors (registration order)."""
        return tuple(self._extractors)

    def extract(self, event: LearningEvent) -> list[EvidenceCandidate]:
        """Run all supporting extractors against ``event``.

        Args:
            event: Learning Event to inspect for evidence.

        Returns:
            Combined list of Evidence Candidates from every extractor that
            reports ``supports(event)``. Empty when none apply. Does not
            deduplicate, score, persist, or mutate Twin state.
        """
        candidates: list[EvidenceCandidate] = []
        for extractor in self._extractors:
            if extractor.supports(event):
                candidates.extend(extractor.extract(event))
        return candidates

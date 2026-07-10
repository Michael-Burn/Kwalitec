"""Knowledge domain state for the Student Digital Twin.

Represents current knowledge structure. Structural slots only — no mastery
calculations, coverage math, or evidence weighting.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass(frozen=True)
class TopicMasteryRecord:
    """Structural mastery slot for one curriculum topic.

    Belief values are stored when supplied by later update pipelines; this
    record does not compute them.

    Attributes:
        topic_id: Canonical curriculum topic identity.
        mastery_belief: Optional stored mastery belief (not computed here).
        evidence_ids: Learning Evidence references supporting this slot.
    """

    topic_id: str
    mastery_belief: float | None = None
    evidence_ids: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        topic_id: str,
        *,
        mastery_belief: float | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
    ) -> TopicMasteryRecord:
        """Construct a TopicMasteryRecord.

        Args:
            topic_id: Non-empty canonical topic identity.
            mastery_belief: Optional stored belief value.
            evidence_ids: Optional evidence reference collection.

        Returns:
            A frozen TopicMasteryRecord.

        Raises:
            ValueError: If ``topic_id`` is empty or blank.
        """
        normalized = topic_id.strip() if isinstance(topic_id, str) else ""
        if not normalized:
            raise ValueError("topic_id must be a non-empty string")
        return cls(
            topic_id=normalized,
            mastery_belief=mastery_belief,
            evidence_ids=tuple(evidence_ids or ()),
        )


@dataclass(frozen=True)
class KnowledgeState:
    """Current knowledge structure for the learner.

    Attributes:
        topic_mastery: Collection of per-topic mastery slots.
        evidence_ids: Learning Evidence references informing this state.
        last_updated: When this knowledge snapshot was last materialised.
    """

    topic_mastery: tuple[TopicMasteryRecord, ...] = ()
    evidence_ids: tuple[str, ...] = field(default_factory=tuple)
    last_updated: datetime | None = None

    @classmethod
    def create(
        cls,
        *,
        topic_mastery: list[TopicMasteryRecord]
        | tuple[TopicMasteryRecord, ...]
        | None = None,
        evidence_ids: list[str] | tuple[str, ...] | None = None,
        last_updated: datetime | None = None,
    ) -> KnowledgeState:
        """Construct a KnowledgeState.

        Args:
            topic_mastery: Optional topic mastery collection.
            evidence_ids: Optional evidence reference collection.
            last_updated: Optional materialisation timestamp.

        Returns:
            A frozen KnowledgeState instance.
        """
        return cls(
            topic_mastery=tuple(topic_mastery or ()),
            evidence_ids=tuple(evidence_ids or ()),
            last_updated=last_updated,
        )

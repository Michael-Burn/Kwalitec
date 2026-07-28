"""Deterministic progress aggregation from node state upwards (EI-004).

Aggregates subsection → section → topic → subject from persisted node states.
No mastery calculation, forgetting, or recommendation logic.
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass

from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)
from app.domain.curriculum_knowledge_graph.value_objects.stable_curriculum_id import (
    StableCurriculumId,
    StableIdDepth,
)
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    NodeStateSnapshot,
    derive_completion_status,
    worst_revision_status,
)

_AGGREGATABLE_KINDS = frozenset(
    {
        CkgNodeKind.SUBSECTION.value,
        CkgNodeKind.SECTION.value,
        CkgNodeKind.TOPIC.value,
        CkgNodeKind.SUBJECT.value,
    }
)

_LEAF_CONTRIBUTOR_DEPTHS = frozenset(
    {
        StableIdDepth.LEARNING_OBJECTIVE,
        StableIdDepth.EDUCATIONAL_OBJECT,
        StableIdDepth.SUBSECTION,
        StableIdDepth.SECTION,
        StableIdDepth.TOPIC,
        StableIdDepth.SUBJECT,
    }
)


@dataclass(frozen=True)
class ProgressAggregate:
    """Reproducible progress roll-up for a structural curriculum node."""

    stable_id: str
    kind: str
    node_count: int
    completed_count: int
    incomplete_count: int
    in_progress_count: int
    mean_mastery: float
    mean_confidence: float
    total_attempts: int
    total_study_time_minutes: int
    total_evidence_count: int
    completion_ratio: float
    completion_status: str
    revision_status: str

    def to_dict(self) -> dict[str, object]:
        return {
            "stable_id": self.stable_id,
            "kind": self.kind,
            "node_count": self.node_count,
            "completed_count": self.completed_count,
            "incomplete_count": self.incomplete_count,
            "in_progress_count": self.in_progress_count,
            "mean_mastery": self.mean_mastery,
            "mean_confidence": self.mean_confidence,
            "total_attempts": self.total_attempts,
            "total_study_time_minutes": self.total_study_time_minutes,
            "total_evidence_count": self.total_evidence_count,
            "completion_ratio": self.completion_ratio,
            "completion_status": self.completion_status,
            "revision_status": self.revision_status,
        }


def is_descendant_or_self(candidate: str, ancestor: str) -> bool:
    """True when candidate is ancestor or a stable-id descendant of it."""
    if candidate == ancestor:
        return True
    return candidate.startswith(f"{ancestor}.")


def aggregate_progress(
    root_stable_id: str,
    root_kind: str,
    node_states: Iterable[NodeStateSnapshot],
) -> ProgressAggregate:
    """Aggregate educational state under a structural root.

    Contributors are node states whose stable ids are the root or descendants.
    Means use arithmetic average rounded to 6 decimal places for reproducibility.
    Empty contributor sets yield zeros and ``not_started``.
    """
    if root_kind not in _AGGREGATABLE_KINDS:
        raise ValueError(
            f"aggregation root kind must be one of {sorted(_AGGREGATABLE_KINDS)}; "
            f"got {root_kind!r}"
        )

    contributors = [
        s
        for s in node_states
        if is_descendant_or_self(s.node_stable_id, root_stable_id)
        and _is_contributor(s.node_stable_id)
    ]
    # Deterministic order for reproducibility of any future tie-breaking.
    contributors.sort(key=lambda s: s.node_stable_id)

    total = len(contributors)
    if total == 0:
        return ProgressAggregate(
            stable_id=root_stable_id,
            kind=root_kind,
            node_count=0,
            completed_count=0,
            incomplete_count=0,
            in_progress_count=0,
            mean_mastery=0.0,
            mean_confidence=0.0,
            total_attempts=0,
            total_study_time_minutes=0,
            total_evidence_count=0,
            completion_ratio=0.0,
            completion_status=CompletionStatus.NOT_STARTED.value,
            revision_status=worst_revision_status([]),
        )

    completed = sum(
        1
        for s in contributors
        if s.completion_status == CompletionStatus.COMPLETED.value
    )
    in_progress = sum(
        1
        for s in contributors
        if s.completion_status == CompletionStatus.IN_PROGRESS.value
    )
    incomplete = total - completed
    mean_mastery = _rounded_mean(s.mastery for s in contributors)
    mean_confidence = _rounded_mean(s.confidence for s in contributors)
    total_attempts = sum(s.attempts for s in contributors)
    total_study = sum(s.total_study_time_minutes for s in contributors)
    total_evidence = sum(s.evidence_count for s in contributors)
    ratio = _round6(completed / total)

    return ProgressAggregate(
        stable_id=root_stable_id,
        kind=root_kind,
        node_count=total,
        completed_count=completed,
        incomplete_count=incomplete,
        in_progress_count=in_progress,
        mean_mastery=mean_mastery,
        mean_confidence=mean_confidence,
        total_attempts=total_attempts,
        total_study_time_minutes=total_study,
        total_evidence_count=total_evidence,
        completion_ratio=ratio,
        completion_status=derive_completion_status(
            completed_count=completed,
            in_progress_count=in_progress,
            total_count=total,
        ),
        revision_status=worst_revision_status(
            [s.revision_status for s in contributors]
        ),
    )


def _is_contributor(stable_id: str) -> bool:
    try:
        depth = StableCurriculumId.of(stable_id).depth
    except ValueError:
        return False
    return depth in _LEAF_CONTRIBUTOR_DEPTHS


def _rounded_mean(values: Iterable[float]) -> float:
    seq = list(values)
    if not seq:
        return 0.0
    return _round6(sum(seq) / len(seq))


def _round6(value: float) -> float:
    return round(float(value), 6)

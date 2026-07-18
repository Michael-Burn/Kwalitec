"""DiffService — compare normalised curriculum structures."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.application.curriculum_studio._ports import require_ingestion
from app.application.curriculum_studio.exceptions import DiffError
from app.application.curriculum_studio.ports.curriculum_ingestion_port import (
    CurriculumIngestionPort,
)
from app.domain.curriculum_studio.curriculum_diff import (
    CurriculumDiff,
    DiffChangeKind,
    DiffEntry,
    NormalisedCurriculum,
    NormalisedTopic,
)


@dataclass(frozen=True)
class DiffEntrySnapshot:
    """Read-only diff entry projection."""

    kind: str
    path: str
    before: str | None = None
    after: str | None = None
    topic_id: str | None = None


@dataclass(frozen=True)
class DiffSnapshot:
    """Read-only curriculum diff projection."""

    diff_id: str
    left_curriculum_id: str
    right_curriculum_id: str
    change_count: int = 0
    is_identical: bool = True
    added_topic_count: int = 0
    removed_topic_count: int = 0
    updated_topic_count: int = 0
    objective_change_count: int = 0
    prerequisite_change_count: int = 0
    metadata_change_count: int = 0
    entries: tuple[DiffEntrySnapshot, ...] = field(default_factory=tuple)


class DiffService:
    """Compare normalised curriculum structures for Studio review.

    Never compares PDFs. Structure only.
    Inputs come from Ingestion-normalised structures when using job ids.
    """

    def __init__(
        self,
        *,
        ingestion: CurriculumIngestionPort | None = None,
    ) -> None:
        self._ingestion = ingestion

    def compare(
        self,
        left: NormalisedCurriculum,
        right: NormalisedCurriculum,
        *,
        diff_id: str = "diff",
    ) -> DiffSnapshot:
        """Compare two normalised curricula and return a DiffSnapshot."""
        if left.subject_code != right.subject_code:
            raise DiffError(
                f"Subject mismatch: {left.subject_code!r} vs {right.subject_code!r}"
            )
        diff = CurriculumDiff.compare(left, right, diff_id=diff_id)
        return self._to_snapshot(diff)

    def compare_dicts(
        self,
        left: dict,
        right: dict,
        *,
        diff_id: str = "diff",
    ) -> DiffSnapshot:
        """Compare dict-shaped normalised curricula (port-friendly)."""
        return self.compare(
            self._from_dict(left, default_id="left"),
            self._from_dict(right, default_id="right"),
            diff_id=diff_id,
        )

    def compare_ingestion_jobs(
        self,
        left_job_id: str,
        right_job_id: str,
        *,
        diff_id: str = "diff",
    ) -> DiffSnapshot:
        """Compare Versions — fetch normalised structures via Ingestion port."""
        port = require_ingestion(self._ingestion, action="compare_versions")
        left = port.normalised_structure(left_job_id)
        right = port.normalised_structure(right_job_id)
        if left is None or right is None:
            raise DiffError(
                f"Missing normalised structure for jobs "
                f"{left_job_id!r} / {right_job_id!r}"
            )
        return self.compare_dicts(left, right, diff_id=diff_id)

    def _to_snapshot(self, diff: CurriculumDiff) -> DiffSnapshot:
        entries = tuple(
            DiffEntrySnapshot(
                kind=e.kind.value,
                path=e.path,
                before=e.before,
                after=e.after,
                topic_id=e.topic_id,
            )
            for e in diff.entries
        )
        return DiffSnapshot(
            diff_id=diff.diff_id,
            left_curriculum_id=diff.left_curriculum_id,
            right_curriculum_id=diff.right_curriculum_id,
            change_count=diff.change_count,
            is_identical=diff.is_identical,
            added_topic_count=len(diff.added_topics),
            removed_topic_count=len(diff.removed_topics),
            updated_topic_count=len(diff.updated_topics),
            objective_change_count=len(
                diff.of_kind(DiffChangeKind.LEARNING_OBJECTIVE_CHANGE)
            ),
            prerequisite_change_count=len(
                diff.of_kind(DiffChangeKind.PREREQUISITE_CHANGE)
            ),
            metadata_change_count=len(
                diff.of_kind(DiffChangeKind.METADATA_CHANGE)
            ),
            entries=entries,
        )

    def _from_dict(
        self, payload: dict, *, default_id: str
    ) -> NormalisedCurriculum:
        try:
            topics_raw = payload.get("topics") or []
            topics = []
            for item in topics_raw:
                topics.append(
                    NormalisedTopic.create(
                        item["topic_id"],
                        item["title"],
                        section_id=item.get("section_id"),
                        objectives=item.get("objectives") or (),
                        prerequisites=item.get("prerequisites") or (),
                        metadata=item.get("metadata"),
                    )
                )
            return NormalisedCurriculum.create(
                payload.get("curriculum_id") or default_id,
                payload["subject_code"],
                version_label=payload.get("version_label") or "",
                topics=topics,
                metadata=payload.get("metadata"),
            )
        except (KeyError, TypeError, ValueError) as exc:
            raise DiffError(f"Invalid normalised curriculum payload: {exc}") from (
                exc
            )


# Re-export DiffEntry for type convenience in tests.
__all__ = [
    "DiffEntry",
    "DiffEntrySnapshot",
    "DiffService",
    "DiffSnapshot",
    "NormalisedCurriculum",
    "NormalisedTopic",
]

"""Curriculum diff — compare normalised curriculum structures.

Compares topics, objectives, prerequisites, and metadata.
Does **not** compare PDFs or binary assets.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from types import MappingProxyType


class DiffChangeKind(StrEnum):
    """Kinds of differences between normalised curriculum structures."""

    ADDED_TOPIC = "added_topic"
    REMOVED_TOPIC = "removed_topic"
    UPDATED_TOPIC = "updated_topic"
    LEARNING_OBJECTIVE_CHANGE = "learning_objective_change"
    PREREQUISITE_CHANGE = "prerequisite_change"
    METADATA_CHANGE = "metadata_change"


@dataclass(frozen=True)
class NormalisedTopic:
    """Normalised topic structure for deterministic comparison."""

    topic_id: str
    title: str
    section_id: str | None = None
    objectives: tuple[str, ...] = field(default_factory=tuple)
    prerequisites: tuple[str, ...] = field(default_factory=tuple)
    metadata: MappingProxyType | None = None

    @classmethod
    def create(
        cls,
        topic_id: str,
        title: str,
        *,
        section_id: str | None = None,
        objectives: list[str] | tuple[str, ...] | None = None,
        prerequisites: list[str] | tuple[str, ...] | None = None,
        metadata: dict[str, str] | MappingProxyType | None = None,
    ) -> NormalisedTopic:
        """Construct a NormalisedTopic after validating invariants."""
        meta = metadata
        if meta is None:
            meta_proxy: MappingProxyType = MappingProxyType({})
        elif isinstance(meta, MappingProxyType):
            meta_proxy = meta
        else:
            meta_proxy = MappingProxyType(
                {str(k): str(v) for k, v in dict(meta).items()}
            )
        return cls(
            topic_id=_require_non_empty(topic_id, "topic_id"),
            title=_require_non_empty(title, "title"),
            section_id=(
                None
                if section_id is None
                else _require_non_empty(section_id, "section_id")
            ),
            objectives=tuple(objectives or ()),
            prerequisites=tuple(prerequisites or ()),
            metadata=meta_proxy,
        )


@dataclass(frozen=True)
class NormalisedCurriculum:
    """Normalised curriculum structure used for Studio diffs.

    Not a PDF. Not a binary package. Structure only.
    """

    curriculum_id: str
    subject_code: str
    version_label: str = ""
    topics: tuple[NormalisedTopic, ...] = field(default_factory=tuple)
    metadata: MappingProxyType | None = None

    @classmethod
    def create(
        cls,
        curriculum_id: str,
        subject_code: str,
        *,
        version_label: str = "",
        topics: list[NormalisedTopic] | tuple[NormalisedTopic, ...] | None = None,
        metadata: dict[str, str] | MappingProxyType | None = None,
    ) -> NormalisedCurriculum:
        """Construct a NormalisedCurriculum after validating invariants."""
        meta = metadata
        if meta is None:
            meta_proxy: MappingProxyType = MappingProxyType({})
        elif isinstance(meta, MappingProxyType):
            meta_proxy = meta
        else:
            meta_proxy = MappingProxyType(
                {str(k): str(v) for k, v in dict(meta).items()}
            )
        topic_t = tuple(topics or ())
        seen: set[str] = set()
        for topic in topic_t:
            if topic.topic_id in seen:
                raise ValueError(f"duplicate topic_id: {topic.topic_id!r}")
            seen.add(topic.topic_id)
        return cls(
            curriculum_id=_require_non_empty(curriculum_id, "curriculum_id"),
            subject_code=_require_non_empty(subject_code, "subject_code").upper(),
            version_label=(version_label or "").strip(),
            topics=topic_t,
            metadata=meta_proxy,
        )

    def topic_map(self) -> dict[str, NormalisedTopic]:
        """Map of topic_id → NormalisedTopic."""
        return {t.topic_id: t for t in self.topics}


@dataclass(frozen=True)
class DiffEntry:
    """Single immutable difference between two normalised curricula."""

    kind: DiffChangeKind
    path: str
    before: str | None = None
    after: str | None = None
    topic_id: str | None = None

    @classmethod
    def create(
        cls,
        kind: DiffChangeKind | str,
        path: str,
        *,
        before: str | None = None,
        after: str | None = None,
        topic_id: str | None = None,
    ) -> DiffEntry:
        """Construct a DiffEntry after validating invariants."""
        resolved = (
            kind
            if isinstance(kind, DiffChangeKind)
            else DiffChangeKind(str(kind).strip().lower())
        )
        return cls(
            kind=resolved,
            path=_require_non_empty(path, "path"),
            before=before,
            after=after,
            topic_id=topic_id,
        )


@dataclass(frozen=True)
class CurriculumDiff:
    """Immutable diff between two normalised curriculum structures."""

    diff_id: str
    left_curriculum_id: str
    right_curriculum_id: str
    entries: tuple[DiffEntry, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        diff_id: str,
        left_curriculum_id: str,
        right_curriculum_id: str,
        *,
        entries: list[DiffEntry] | tuple[DiffEntry, ...] | None = None,
    ) -> CurriculumDiff:
        """Construct a CurriculumDiff."""
        return cls(
            diff_id=_require_non_empty(diff_id, "diff_id"),
            left_curriculum_id=_require_non_empty(
                left_curriculum_id, "left_curriculum_id"
            ),
            right_curriculum_id=_require_non_empty(
                right_curriculum_id, "right_curriculum_id"
            ),
            entries=tuple(entries or ()),
        )

    @classmethod
    def compare(
        cls,
        left: NormalisedCurriculum,
        right: NormalisedCurriculum,
        *,
        diff_id: str = "diff",
    ) -> CurriculumDiff:
        """Compare two normalised curricula and return a deterministic diff.

        Order of entries is stable: removed topics, added topics, updated
        topics (title/section), objective changes, prerequisite changes,
        then curriculum-level metadata changes.
        """
        entries: list[DiffEntry] = []
        left_map = left.topic_map()
        right_map = right.topic_map()
        left_ids = set(left_map)
        right_ids = set(right_map)

        for topic_id in sorted(left_ids - right_ids):
            topic = left_map[topic_id]
            entries.append(
                DiffEntry.create(
                    DiffChangeKind.REMOVED_TOPIC,
                    f"topic/{topic_id}",
                    before=topic.title,
                    after=None,
                    topic_id=topic_id,
                )
            )

        for topic_id in sorted(right_ids - left_ids):
            topic = right_map[topic_id]
            entries.append(
                DiffEntry.create(
                    DiffChangeKind.ADDED_TOPIC,
                    f"topic/{topic_id}",
                    before=None,
                    after=topic.title,
                    topic_id=topic_id,
                )
            )

        for topic_id in sorted(left_ids & right_ids):
            lt = left_map[topic_id]
            rt = right_map[topic_id]
            if lt.title != rt.title or lt.section_id != rt.section_id:
                entries.append(
                    DiffEntry.create(
                        DiffChangeKind.UPDATED_TOPIC,
                        f"topic/{topic_id}",
                        before=_topic_signature(lt),
                        after=_topic_signature(rt),
                        topic_id=topic_id,
                    )
                )
            if tuple(lt.objectives) != tuple(rt.objectives):
                entries.append(
                    DiffEntry.create(
                        DiffChangeKind.LEARNING_OBJECTIVE_CHANGE,
                        f"topic/{topic_id}/objectives",
                        before="|".join(lt.objectives),
                        after="|".join(rt.objectives),
                        topic_id=topic_id,
                    )
                )
            if tuple(lt.prerequisites) != tuple(rt.prerequisites):
                entries.append(
                    DiffEntry.create(
                        DiffChangeKind.PREREQUISITE_CHANGE,
                        f"topic/{topic_id}/prerequisites",
                        before="|".join(lt.prerequisites),
                        after="|".join(rt.prerequisites),
                        topic_id=topic_id,
                    )
                )
            left_meta = dict(lt.metadata or {})
            right_meta = dict(rt.metadata or {})
            if left_meta != right_meta:
                entries.append(
                    DiffEntry.create(
                        DiffChangeKind.METADATA_CHANGE,
                        f"topic/{topic_id}/metadata",
                        before=_meta_signature(left_meta),
                        after=_meta_signature(right_meta),
                        topic_id=topic_id,
                    )
                )

        left_root = dict(left.metadata or {})
        right_root = dict(right.metadata or {})
        if left_root != right_root:
            entries.append(
                DiffEntry.create(
                    DiffChangeKind.METADATA_CHANGE,
                    "curriculum/metadata",
                    before=_meta_signature(left_root),
                    after=_meta_signature(right_root),
                )
            )

        return cls.create(
            diff_id,
            left.curriculum_id,
            right.curriculum_id,
            entries=entries,
        )

    @property
    def change_count(self) -> int:
        """Total number of diff entries."""
        return len(self.entries)

    @property
    def is_identical(self) -> bool:
        """True when there are no differences."""
        return len(self.entries) == 0

    def of_kind(self, kind: DiffChangeKind | str) -> tuple[DiffEntry, ...]:
        """Entries matching ``kind``."""
        resolved = (
            kind
            if isinstance(kind, DiffChangeKind)
            else DiffChangeKind(str(kind).strip().lower())
        )
        return tuple(e for e in self.entries if e.kind is resolved)

    @property
    def added_topics(self) -> tuple[DiffEntry, ...]:
        """Added topic entries."""
        return self.of_kind(DiffChangeKind.ADDED_TOPIC)

    @property
    def removed_topics(self) -> tuple[DiffEntry, ...]:
        """Removed topic entries."""
        return self.of_kind(DiffChangeKind.REMOVED_TOPIC)

    @property
    def updated_topics(self) -> tuple[DiffEntry, ...]:
        """Updated topic entries."""
        return self.of_kind(DiffChangeKind.UPDATED_TOPIC)


def _topic_signature(topic: NormalisedTopic) -> str:
    section = topic.section_id or ""
    return f"{topic.title}|{section}"


def _meta_signature(meta: dict[str, str]) -> str:
    return ";".join(f"{k}={meta[k]}" for k in sorted(meta))


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized

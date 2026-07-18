"""Curriculum — educational programme structure aggregate.

Examples of programme identity (structure only): CS1, CM1, CB2.
Must not contain copyrighted educational material.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities._text import require_non_empty
from app.domain.curriculum.entities.curriculum_version import CurriculumVersion
from app.domain.curriculum.entities.dependency import Dependency
from app.domain.curriculum.entities.learning_path import LearningPath
from app.domain.curriculum.entities.prerequisite import Prerequisite
from app.domain.curriculum.entities.revision_link import RevisionLink
from app.domain.curriculum.entities.subject import Subject
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.value_objects.curriculum_id import CurriculumId
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Curriculum:
    """Educational programme aggregate: structure without proprietary content.

    Attributes:
        curriculum_id: Programme identity.
        name: Operational programme label.
        version: Edition metadata.
        subjects: Ordered subjects.
        prerequisites: Explicit required-knowledge links.
        dependencies: Directed topic relationships (all kinds).
        revision_links: Joint-revision associations.
        learning_paths: Named valid educational routes.
    """

    curriculum_id: CurriculumId
    name: str
    version: CurriculumVersion
    subjects: tuple[Subject, ...] = field(default_factory=tuple)
    prerequisites: tuple[Prerequisite, ...] = field(default_factory=tuple)
    dependencies: tuple[Dependency, ...] = field(default_factory=tuple)
    revision_links: tuple[RevisionLink, ...] = field(default_factory=tuple)
    learning_paths: tuple[LearningPath, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        curriculum_id: str | CurriculumId,
        name: str,
        version: CurriculumVersion,
        *,
        subjects: list[Subject] | tuple[Subject, ...] | None = None,
        prerequisites: list[Prerequisite] | tuple[Prerequisite, ...] | None = None,
        dependencies: list[Dependency] | tuple[Dependency, ...] | None = None,
        revision_links: list[RevisionLink] | tuple[RevisionLink, ...] | None = None,
        learning_paths: list[LearningPath] | tuple[LearningPath, ...] | None = None,
    ) -> Curriculum:
        """Construct a Curriculum after validating aggregate invariants.

        Raises:
            ValueError: On identity mismatches, duplicate ids, or empty name.
        """
        cid = CurriculumId.of(curriculum_id)
        label = require_non_empty(name, "name")
        if version.curriculum_id != cid:
            raise ValueError("version.curriculum_id must match curriculum_id")
        subjects_t = tuple(subjects or ())
        seen_subjects: set[str] = set()
        for subject in subjects_t:
            if subject.subject_id in seen_subjects:
                raise ValueError("duplicate subject_id within curriculum")
            seen_subjects.add(subject.subject_id)
            if (
                subject.curriculum_id is not None
                and subject.curriculum_id != cid.value
            ):
                raise ValueError("subject curriculum_id must match curriculum")
        topic_ids = _collect_topic_ids(subjects_t)
        if len(topic_ids) != len(set(topic_ids)):
            raise ValueError("duplicate topic_id within curriculum")
        topic_id_set = set(topic_ids)

        prerequisites_t = tuple(prerequisites or ())
        _validate_prerequisites(prerequisites_t, topic_id_set)
        dependencies_t = tuple(dependencies or ())
        _validate_dependencies(dependencies_t, topic_id_set)
        revision_links_t = tuple(revision_links or ())
        _validate_revision_links(revision_links_t, topic_id_set)
        learning_paths_t = tuple(learning_paths or ())
        _validate_learning_paths(learning_paths_t, cid, topic_id_set)

        return cls(
            curriculum_id=cid,
            name=label,
            version=version,
            subjects=subjects_t,
            prerequisites=prerequisites_t,
            dependencies=dependencies_t,
            revision_links=revision_links_t,
            learning_paths=learning_paths_t,
        )

    def ordered_subjects(self) -> tuple[Subject, ...]:
        """Subjects sorted by sequence_index, then subject_id."""
        return tuple(
            sorted(
                self.subjects,
                key=lambda s: (s.sequence_index, s.subject_id),
            )
        )

    def all_topics(self) -> tuple[Topic, ...]:
        """Flatten topics in subject → module → topic order."""
        topics: list[Topic] = []
        for subject in self.ordered_subjects():
            topics.extend(subject.all_topics())
        return tuple(topics)

    def topic_ids(self) -> tuple[TopicId, ...]:
        """All topic identities in traversal order."""
        return tuple(t.topic_id for t in self.all_topics())

    def get_topic(self, topic_id: str | TopicId) -> Topic | None:
        """Locate a topic by identity, or None."""
        tid = TopicId.of(topic_id)
        for topic in self.all_topics():
            if topic.topic_id == tid:
                return topic
        return None


def _collect_topic_ids(subjects: tuple[Subject, ...]) -> list[TopicId]:
    ids: list[TopicId] = []
    for subject in subjects:
        ids.extend(subject.topic_ids())
    return ids


def _validate_prerequisites(
    prerequisites: tuple[Prerequisite, ...],
    topic_ids: set[TopicId],
) -> None:
    seen: set[str] = set()
    for prereq in prerequisites:
        if prereq.prerequisite_id in seen:
            raise ValueError("duplicate prerequisite_id within curriculum")
        seen.add(prereq.prerequisite_id)
        if prereq.topic_id not in topic_ids:
            raise ValueError("prerequisite topic_id not in curriculum")
        if prereq.required_topic_id not in topic_ids:
            raise ValueError("prerequisite required_topic_id not in curriculum")


def _validate_dependencies(
    dependencies: tuple[Dependency, ...],
    topic_ids: set[TopicId],
) -> None:
    seen: set[str] = set()
    for dep in dependencies:
        if dep.dependency_id in seen:
            raise ValueError("duplicate dependency_id within curriculum")
        seen.add(dep.dependency_id)
        if dep.source_topic_id not in topic_ids:
            raise ValueError("dependency source_topic_id not in curriculum")
        if dep.target_topic_id not in topic_ids:
            raise ValueError("dependency target_topic_id not in curriculum")


def _validate_revision_links(
    revision_links: tuple[RevisionLink, ...],
    topic_ids: set[TopicId],
) -> None:
    seen_ids: set[str] = set()
    seen_pairs: set[tuple[TopicId, TopicId]] = set()
    for link in revision_links:
        if link.revision_link_id in seen_ids:
            raise ValueError("duplicate revision_link_id within curriculum")
        seen_ids.add(link.revision_link_id)
        if link.topic_a_id not in topic_ids or link.topic_b_id not in topic_ids:
            raise ValueError("revision link topic not in curriculum")
        pair = link.pair()
        if pair in seen_pairs:
            raise ValueError("duplicate revision link pair within curriculum")
        seen_pairs.add(pair)


def _validate_learning_paths(
    learning_paths: tuple[LearningPath, ...],
    curriculum_id: CurriculumId,
    topic_ids: set[TopicId],
) -> None:
    seen: set[str] = set()
    for path in learning_paths:
        if path.path_id in seen:
            raise ValueError("duplicate path_id within curriculum")
        seen.add(path.path_id)
        if (
            path.curriculum_id is not None
            and path.curriculum_id != curriculum_id.value
        ):
            raise ValueError("learning path curriculum_id must match curriculum")
        for tid in path.topic_ids:
            if tid not in topic_ids:
                raise ValueError("learning path topic_id not in curriculum")

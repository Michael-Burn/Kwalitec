"""Subject — ordered container of Modules within a Curriculum."""

from __future__ import annotations

from dataclasses import dataclass, field

from app.domain.curriculum.entities._text import require_non_empty
from app.domain.curriculum.entities.module import Module
from app.domain.curriculum.entities.topic import Topic
from app.domain.curriculum.value_objects.topic_id import TopicId


@dataclass(frozen=True)
class Subject:
    """Coherent examinable domain containing ordered Modules.

    Attributes:
        subject_id: Stable subject identity.
        name: Operational label (not copyrighted syllabus text).
        modules: Ordered modules belonging to this subject.
        sequence_index: Order within the owning curriculum (0-based).
        curriculum_id: Optional owning curriculum identity string.
    """

    subject_id: str
    name: str
    modules: tuple[Module, ...] = field(default_factory=tuple)
    sequence_index: int = 0
    curriculum_id: str | None = None

    @classmethod
    def create(
        cls,
        subject_id: str,
        name: str,
        *,
        modules: list[Module] | tuple[Module, ...] | None = None,
        sequence_index: int = 0,
        curriculum_id: str | None = None,
    ) -> Subject:
        """Construct a Subject after validating invariants.

        Raises:
            ValueError: On empty identities, negative index, duplicate module
                ids, or module subject_id mismatch.
        """
        sid = require_non_empty(subject_id, "subject_id")
        label = require_non_empty(name, "name")
        if sequence_index < 0:
            raise ValueError("sequence_index must be non-negative")
        cid = (
            None
            if curriculum_id is None
            else require_non_empty(curriculum_id, "curriculum_id")
        )
        modules_t = tuple(modules or ())
        seen: set[str] = set()
        for module in modules_t:
            if module.module_id in seen:
                raise ValueError("duplicate module_id within subject")
            seen.add(module.module_id)
            if module.subject_id is not None and module.subject_id != sid:
                raise ValueError("module subject_id must match subject")
        return cls(
            subject_id=sid,
            name=label,
            modules=modules_t,
            sequence_index=sequence_index,
            curriculum_id=cid,
        )

    def ordered_modules(self) -> tuple[Module, ...]:
        """Modules sorted by sequence_index ascending, then module_id."""
        return tuple(
            sorted(
                self.modules,
                key=lambda m: (m.sequence_index, m.module_id),
            )
        )

    def with_module(self, module: Module) -> Subject:
        """Return a new subject with an appended module."""
        if module.subject_id is not None and module.subject_id != self.subject_id:
            raise ValueError("module subject_id must match subject")
        if any(m.module_id == module.module_id for m in self.modules):
            raise ValueError("duplicate module_id within subject")
        return Subject(
            subject_id=self.subject_id,
            name=self.name,
            modules=(*self.modules, module),
            sequence_index=self.sequence_index,
            curriculum_id=self.curriculum_id,
        )

    def all_topics(self) -> tuple[Topic, ...]:
        """Flatten topics in module order, then topic sequence within module."""
        topics: list[Topic] = []
        for module in self.ordered_modules():
            topics.extend(module.ordered_topics())
        return tuple(topics)

    def topic_ids(self) -> tuple[TopicId, ...]:
        """Flattened topic identities in traversal order."""
        return tuple(t.topic_id for t in self.all_topics())

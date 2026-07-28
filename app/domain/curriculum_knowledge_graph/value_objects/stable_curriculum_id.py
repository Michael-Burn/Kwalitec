"""Stable curriculum identity value object (EI-001).

Edition-stable identifiers for Curriculum Knowledge Graph nodes.

Structural pattern::

    {SUBJECT}.T{tt}.S{ss}.{oo}.SS{uu}.LO{ll}

Example::

    CS1.T04.S04.02.SS01.LO03

Educational objects append typed suffixes (``.DEF03``, ``.FOR02``,
``.WE01``, ``.PE04``, ``.RR01``, ``.SO01``). Subject-level ``RR`` / ``SO``
may attach directly to the subject code (``CS1.RR01``). Edition year is
never part of the identity; it lives on ``Subject.edition_label``.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_knowledge_graph.value_objects.node_kind import (
    CkgNodeKind,
)

_SUBJECT_RE = re.compile(r"^[A-Z][A-Z0-9]{0,15}$")
_TOPIC_RE = re.compile(r"^T(\d{2,})$")
_SECTION_MAJOR_RE = re.compile(r"^S(\d{2,})$")
_ORDINAL_RE = re.compile(r"^(\d{2,})$")
_SUBSECTION_RE = re.compile(r"^SS(\d{2,})$")
_LO_RE = re.compile(r"^LO(\d{2,})$")
_OBJECT_RE = re.compile(r"^(DEF|FOR|WE|PE|RR|SO)(\d{2,})$")

_OBJECT_SUFFIX: dict[str, CkgNodeKind] = {
    "DEF": CkgNodeKind.DEFINITION,
    "FOR": CkgNodeKind.FORMULA,
    "WE": CkgNodeKind.WORKED_EXAMPLE,
    "PE": CkgNodeKind.PRACTICE_EXERCISE,
    "RR": CkgNodeKind.READING_REFERENCE,
    "SO": CkgNodeKind.SYLLABUS_OUTCOME,
}

_SUBJECT_LEVEL_OBJECT_KINDS = frozenset(
    {CkgNodeKind.READING_REFERENCE, CkgNodeKind.SYLLABUS_OUTCOME}
)


class StableIdDepth(StrEnum):
    """How deep a stable id resolves in the containment hierarchy."""

    SUBJECT = "subject"
    TOPIC = "topic"
    SECTION = "section"
    SUBSECTION = "subsection"
    LEARNING_OBJECTIVE = "learning_objective"
    EDUCATIONAL_OBJECT = "educational_object"


@dataclass(frozen=True)
class _ParsedId:
    subject_code: str
    depth: StableIdDepth
    topic_n: int | None = None
    section_n: int | None = None
    ordinal: int | None = None
    subsection_n: int | None = None
    lo_n: int | None = None
    object_kind: CkgNodeKind | None = None
    object_n: int | None = None


@dataclass(frozen=True, order=True)
class StableCurriculumId:
    """Permanent, edition-stable curriculum node identity."""

    value: str

    def __post_init__(self) -> None:
        if not isinstance(self.value, str):
            raise ValueError("StableCurriculumId value must be a non-empty string")
        normalized = self.value.strip()
        if not normalized:
            raise ValueError("StableCurriculumId value must be a non-empty string")
        _parse(normalized)
        object.__setattr__(self, "value", normalized)

    @classmethod
    def of(cls, value: str | StableCurriculumId) -> StableCurriculumId:
        """Coerce a string or StableCurriculumId."""
        if isinstance(value, StableCurriculumId):
            return value
        return cls(value)

    @classmethod
    def subject(cls, subject_code: str) -> StableCurriculumId:
        """Build a subject-level stable id (e.g. ``CS1``)."""
        return cls(_normalize_subject(subject_code))

    @classmethod
    def topic(cls, subject_code: str, topic_n: int) -> StableCurriculumId:
        """Build ``{SUBJECT}.T{tt}``."""
        return cls(f"{_normalize_subject(subject_code)}.T{_pad(topic_n)}")

    @classmethod
    def section(
        cls,
        subject_code: str,
        topic_n: int,
        section_n: int,
        ordinal: int,
    ) -> StableCurriculumId:
        """Build ``{SUBJECT}.T{tt}.S{ss}.{oo}``."""
        return cls(
            f"{_normalize_subject(subject_code)}"
            f".T{_pad(topic_n)}"
            f".S{_pad(section_n)}"
            f".{_pad(ordinal)}"
        )

    @classmethod
    def subsection(
        cls,
        subject_code: str,
        topic_n: int,
        section_n: int,
        ordinal: int,
        subsection_n: int,
    ) -> StableCurriculumId:
        """Build ``{SUBJECT}.T{tt}.S{ss}.{oo}.SS{uu}``."""
        base = cls.section(subject_code, topic_n, section_n, ordinal).value
        return cls(f"{base}.SS{_pad(subsection_n)}")

    @classmethod
    def learning_objective(
        cls,
        subject_code: str,
        topic_n: int,
        section_n: int,
        ordinal: int,
        subsection_n: int,
        lo_n: int,
    ) -> StableCurriculumId:
        """Build ``{SUBJECT}.T{tt}.S{ss}.{oo}.SS{uu}.LO{ll}``."""
        base = cls.subsection(
            subject_code, topic_n, section_n, ordinal, subsection_n
        ).value
        return cls(f"{base}.LO{_pad(lo_n)}")

    @classmethod
    def educational_object(
        cls,
        parent: str | StableCurriculumId,
        kind: CkgNodeKind | str,
        object_n: int,
    ) -> StableCurriculumId:
        """Append a typed educational-object suffix to a parent id."""
        parent_id = cls.of(parent)
        parsed = _parse(parent_id.value)
        kind_value = CkgNodeKind(kind) if isinstance(kind, str) else kind
        if parsed.depth == StableIdDepth.SUBJECT:
            if kind_value not in _SUBJECT_LEVEL_OBJECT_KINDS:
                raise ValueError(
                    "only reading_reference and syllabus_outcome may attach "
                    "directly to a subject"
                )
        elif parsed.depth not in {
            StableIdDepth.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE,
        }:
            raise ValueError(
                "educational object parent must be subject, subsection, or "
                "learning objective"
            )
        suffix = _suffix_for_kind(kind_value)
        return cls(f"{parent_id.value}.{suffix}{_pad(object_n)}")

    @property
    def depth(self) -> StableIdDepth:
        """Structural depth of this identity."""
        return _parse(self.value).depth

    @property
    def kind(self) -> CkgNodeKind:
        """Node kind implied by the identity shape."""
        parsed = _parse(self.value)
        if parsed.object_kind is not None:
            return parsed.object_kind
        return {
            StableIdDepth.SUBJECT: CkgNodeKind.SUBJECT,
            StableIdDepth.TOPIC: CkgNodeKind.TOPIC,
            StableIdDepth.SECTION: CkgNodeKind.SECTION,
            StableIdDepth.SUBSECTION: CkgNodeKind.SUBSECTION,
            StableIdDepth.LEARNING_OBJECTIVE: CkgNodeKind.LEARNING_OBJECTIVE,
        }[parsed.depth]

    @property
    def subject_code(self) -> str:
        """Subject code segment."""
        return _parse(self.value).subject_code

    def parent_id(self) -> StableCurriculumId | None:
        """Immediate structural parent identity, or None for a subject."""
        parsed = _parse(self.value)
        parts = self.value.split(".")
        if parsed.depth == StableIdDepth.SUBJECT:
            return None
        if parsed.depth == StableIdDepth.SECTION:
            return StableCurriculumId(".".join(parts[:-2]))
        return StableCurriculumId(".".join(parts[:-1]))

    def __str__(self) -> str:
        return self.value


def _pad(n: int) -> str:
    if not isinstance(n, int) or isinstance(n, bool) or n < 1:
        raise ValueError("stable id numeric segment must be a positive int")
    return f"{n:02d}" if n < 100 else str(n)


def _normalize_subject(subject_code: str) -> str:
    if not isinstance(subject_code, str):
        raise ValueError("subject_code must be a non-empty string")
    code = subject_code.strip().upper()
    if not _SUBJECT_RE.match(code):
        raise ValueError(f"invalid subject_code: {subject_code!r}")
    return code


def _suffix_for_kind(kind: CkgNodeKind) -> str:
    for suffix, node_kind in _OBJECT_SUFFIX.items():
        if node_kind is kind:
            return suffix
    raise ValueError(f"kind has no educational-object suffix: {kind}")


def _parse(value: str) -> _ParsedId:
    parts = value.split(".")
    if not parts or any(not p for p in parts):
        raise ValueError(f"invalid StableCurriculumId: {value!r}")

    subject = parts[0]
    if not _SUBJECT_RE.match(subject):
        raise ValueError(f"invalid subject segment in StableCurriculumId: {value!r}")

    if len(parts) == 1:
        return _ParsedId(subject_code=subject, depth=StableIdDepth.SUBJECT)

    # Subject-level educational object: CS1.RR01 / CS1.SO01
    obj_m = _OBJECT_RE.match(parts[1])
    if obj_m is not None:
        kind = _OBJECT_SUFFIX[obj_m.group(1)]
        if kind not in _SUBJECT_LEVEL_OBJECT_KINDS:
            raise ValueError(
                f"educational object may not attach directly to subject: {value!r}"
            )
        if len(parts) != 2:
            raise ValueError(f"invalid StableCurriculumId: {value!r}")
        return _ParsedId(
            subject_code=subject,
            depth=StableIdDepth.EDUCATIONAL_OBJECT,
            object_kind=kind,
            object_n=int(obj_m.group(2)),
        )

    topic_m = _TOPIC_RE.match(parts[1])
    if topic_m is None:
        raise ValueError(f"invalid topic segment in StableCurriculumId: {value!r}")
    topic_n = int(topic_m.group(1))

    if len(parts) == 2:
        return _ParsedId(
            subject_code=subject,
            depth=StableIdDepth.TOPIC,
            topic_n=topic_n,
        )

    section_m = _SECTION_MAJOR_RE.match(parts[2])
    if section_m is None:
        raise ValueError(f"invalid section segment in StableCurriculumId: {value!r}")
    if len(parts) < 4:
        raise ValueError(f"section id requires ordinal segment: {value!r}")
    ordinal_m = _ORDINAL_RE.match(parts[3])
    if ordinal_m is None:
        raise ValueError(f"invalid section ordinal in StableCurriculumId: {value!r}")
    section_n = int(section_m.group(1))
    ordinal = int(ordinal_m.group(1))

    if len(parts) == 4:
        return _ParsedId(
            subject_code=subject,
            depth=StableIdDepth.SECTION,
            topic_n=topic_n,
            section_n=section_n,
            ordinal=ordinal,
        )

    ss_m = _SUBSECTION_RE.match(parts[4])
    if ss_m is None:
        raise ValueError(
            f"invalid subsection segment in StableCurriculumId: {value!r}"
        )
    subsection_n = int(ss_m.group(1))

    if len(parts) == 5:
        return _ParsedId(
            subject_code=subject,
            depth=StableIdDepth.SUBSECTION,
            topic_n=topic_n,
            section_n=section_n,
            ordinal=ordinal,
            subsection_n=subsection_n,
        )

    lo_n: int | None = None
    object_kind: CkgNodeKind | None = None
    object_n: int | None = None
    depth = StableIdDepth.SUBSECTION
    idx = 5

    lo_m = _LO_RE.match(parts[idx])
    if lo_m:
        lo_n = int(lo_m.group(1))
        depth = StableIdDepth.LEARNING_OBJECTIVE
        idx += 1
    else:
        obj_m = _OBJECT_RE.match(parts[idx])
        if obj_m is None:
            raise ValueError(f"invalid segment in StableCurriculumId: {value!r}")
        object_kind = _OBJECT_SUFFIX[obj_m.group(1)]
        object_n = int(obj_m.group(2))
        depth = StableIdDepth.EDUCATIONAL_OBJECT
        idx += 1

    if idx < len(parts):
        if depth != StableIdDepth.LEARNING_OBJECTIVE:
            raise ValueError(
                f"invalid trailing segment in StableCurriculumId: {value!r}"
            )
        obj_m = _OBJECT_RE.match(parts[idx])
        if obj_m is None:
            raise ValueError(
                f"invalid trailing segment in StableCurriculumId: {value!r}"
            )
        object_kind = _OBJECT_SUFFIX[obj_m.group(1)]
        object_n = int(obj_m.group(2))
        depth = StableIdDepth.EDUCATIONAL_OBJECT
        idx += 1

    if idx != len(parts):
        raise ValueError(f"invalid StableCurriculumId: {value!r}")

    return _ParsedId(
        subject_code=subject,
        depth=depth,
        topic_n=topic_n,
        section_n=section_n,
        ordinal=ordinal,
        subsection_n=subsection_n,
        lo_n=lo_n,
        object_kind=object_kind,
        object_n=object_n,
    )

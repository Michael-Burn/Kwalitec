"""Feasibility acknowledgement types for Mission load shaping.

Goals / Constraints / sustainability shape volume and intensity — never invent
educational need or silently erase Decision authority.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum

from app.domain.decision.constraints import ConstraintClass


class FeasibilityEffect(StrEnum):
    """How execution context shaped Mission load (not educational priority)."""

    INCLUDED_AS_AUTHORISED = "included_as_authorised"
    INTENSITY_DEMOTED = "intensity_demoted"
    VOLUME_DEMOTED = "volume_demoted"
    OMITTED_TRAILING_CAPACITY = "omitted_trailing_capacity"
    EMPTY_CAPACITY_REMAINDER = "empty_capacity_remainder"
    SUSTAINABILITY_PROTECT = "sustainability_protect"
    ALREADY_COMMITTED_CAPACITY = "already_committed_capacity"


@dataclass(frozen=True)
class FeasibilityAcknowledgement:
    """Visible record that Goals / Constraints shaped Mission load.

    Attributes:
        effect: Load-shaping effect applied.
        constraint_class: Constraint class when applicable.
        omitted_task_refs: Authorised Decision refs omitted under capacity.
        note_tags: Structural notes — educational need remains visible.
    """

    effect: FeasibilityEffect
    constraint_class: ConstraintClass | None = None
    omitted_task_refs: tuple[str, ...] = ()
    note_tags: tuple[str, ...] = ()

    @classmethod
    def create(
        cls,
        effect: FeasibilityEffect | str,
        *,
        constraint_class: ConstraintClass | str | None = None,
        omitted_task_refs: list[str] | tuple[str, ...] | None = None,
        note_tags: list[str] | tuple[str, ...] | None = None,
    ) -> FeasibilityAcknowledgement:
        """Construct a FeasibilityAcknowledgement."""
        eff = (
            effect
            if isinstance(effect, FeasibilityEffect)
            else FeasibilityEffect(effect)
        )
        cclass: ConstraintClass | None = None
        if constraint_class is not None:
            cclass = (
                constraint_class
                if isinstance(constraint_class, ConstraintClass)
                else ConstraintClass(constraint_class)
            )
        return cls(
            effect=eff,
            constraint_class=cclass,
            omitted_task_refs=tuple(omitted_task_refs or ()),
            note_tags=tuple(note_tags or ()),
        )

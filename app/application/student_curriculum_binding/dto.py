"""DTOs for Student Curriculum Binding services (EI-004)."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from app.domain.student_curriculum_binding.aggregation import ProgressAggregate
from app.domain.student_curriculum_binding.node_state import NodeStateSnapshot


@dataclass(frozen=True)
class InstanceSummary:
    """Compact Student Curriculum Instance view."""

    instance_id: str
    student_id: int
    subject_code: str
    edition_id: str
    enrolled_at: str
    is_active: bool
    is_completed: bool
    completed_at: str | None = None
    node_state_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "student_id": self.student_id,
            "subject_code": self.subject_code,
            "edition_id": self.edition_id,
            "enrolled_at": self.enrolled_at,
            "is_active": self.is_active,
            "is_completed": self.is_completed,
            "completed_at": self.completed_at,
            "node_state_count": self.node_state_count,
        }


@dataclass(frozen=True)
class EducationalStateView:
    """Full educational state for one Student Curriculum Instance."""

    instance: InstanceSummary
    node_states: tuple[NodeStateSnapshot, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance": self.instance.to_dict(),
            "node_states": [s.to_dict() for s in self.node_states],
            "node_count": len(self.node_states),
        }


@dataclass(frozen=True)
class BindingResult:
    """Outcome of creating a Student Curriculum Instance."""

    instance: InstanceSummary
    created: bool
    node_states_initialised: int

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance": self.instance.to_dict(),
            "created": self.created,
            "node_states_initialised": self.node_states_initialised,
        }


@dataclass(frozen=True)
class ProgressAggregationView:
    """Aggregated progress at one or more structural levels."""

    instance_id: str
    aggregates: tuple[ProgressAggregate, ...] = ()

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "aggregates": [a.to_dict() for a in self.aggregates],
        }


@dataclass(frozen=True)
class CurriculumNodeFilterResult:
    """Filtered node states (incomplete or completed queries)."""

    instance_id: str
    completion_status: str
    nodes: tuple[NodeStateSnapshot, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return {
            "instance_id": self.instance_id,
            "completion_status": self.completion_status,
            "nodes": [n.to_dict() for n in self.nodes],
            "count": len(self.nodes),
        }


def format_dt(value: datetime | None) -> str | None:
    if value is None:
        return None
    return value.isoformat()

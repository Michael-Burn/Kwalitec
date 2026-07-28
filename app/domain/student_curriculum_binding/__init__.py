"""Student Curriculum Binding (EI-004) — learner ↔ published curriculum.

Binds a student to exactly one Published Curriculum Edition per subject and
owns mutable educational state per curriculum node. Curriculum knowledge
remains immutable; this package never modifies the CKG.

Pure domain only: no Flask, SQLAlchemy, Twin, missions, or recommendations.
"""

from __future__ import annotations

from typing import Any

__all__ = [
    "BindingInvariant",
    "BindingInvariantError",
    "CompletionStatus",
    "NodeStateSnapshot",
    "ProgressAggregate",
    "RevisionStatus",
    "aggregate_progress",
    "assert_can_bind",
    "assert_published_edition",
    "initial_node_state",
]

_EXPORT_MODULES = {
    "BindingInvariant": "app.domain.student_curriculum_binding.invariants",
    "BindingInvariantError": "app.domain.student_curriculum_binding.invariants",
    "assert_can_bind": "app.domain.student_curriculum_binding.invariants",
    "assert_published_edition": "app.domain.student_curriculum_binding.invariants",
    "CompletionStatus": "app.domain.student_curriculum_binding.node_state",
    "RevisionStatus": "app.domain.student_curriculum_binding.node_state",
    "NodeStateSnapshot": "app.domain.student_curriculum_binding.node_state",
    "initial_node_state": "app.domain.student_curriculum_binding.node_state",
    "ProgressAggregate": "app.domain.student_curriculum_binding.aggregation",
    "aggregate_progress": "app.domain.student_curriculum_binding.aggregation",
}


def __getattr__(name: str) -> Any:
    module_name = _EXPORT_MODULES.get(name)
    if module_name is None:
        raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
    from importlib import import_module

    module = import_module(module_name)
    value = getattr(module, name)
    globals()[name] = value
    return value


def __dir__() -> list[str]:
    return sorted(set(globals()) | set(__all__))

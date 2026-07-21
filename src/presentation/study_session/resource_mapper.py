"""Resource mapping — learning resources and worked examples for the runner.

Formats already-decided workspace / enrichment resource snippets into Design
System cards. Does not select curriculum resources or invent study material.
"""

from __future__ import annotations

from typing import Any

from presentation.design_system import Card, CardVariant
from presentation.mission_workspace.workspace_view_model import (
    MissionWorkspaceViewModel,
    StudyResourceView,
)
from presentation.study_session.session_view_model import (
    LearningResourceView,
    WorkedExampleView,
)

_EMPTY_RESOURCE_LABEL = "No learning resources are listed for this session yet."
_EMPTY_EXAMPLE_LABEL = "No worked example is available for this session yet."


class ResourceMapper:
    """Map workspace study resources into runner resource and example views."""

    @classmethod
    def map_resources(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> tuple[LearningResourceView, ...]:
        """Project learning resources (tasks and tips) into card views."""
        items: list[LearningResourceView] = []
        for resource in cls._workspace_resources(workspace):
            if resource.kind == "example":
                continue
            items.append(cls._to_learning_resource(resource))

        if items:
            return tuple(items)

        # Fall back to enhanced enrichment tips when workspace has none.
        enhanced = getattr(result, "enhanced_mission", None) if result else None
        for tip in _as_tuple(getattr(enhanced, "revision_tips", ())):
            text = _text(tip)
            if text:
                items.append(
                    LearningResourceView(
                        label=text,
                        detail="",
                        kind="tip",
                        card=Card(
                            title=text,
                            body="",
                            eyebrow="Tip",
                            variant=CardVariant.DEFAULT,
                        ),
                    )
                )
        return tuple(items)

    @classmethod
    def map_worked_examples(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> tuple[WorkedExampleView, ...]:
        """Project worked-example snippets into card views."""
        examples: list[WorkedExampleView] = []
        for resource in cls._workspace_resources(workspace):
            if resource.kind != "example":
                continue
            examples.append(cls._to_worked_example(resource))

        if examples:
            return tuple(examples)

        enhanced = getattr(result, "enhanced_mission", None) if result else None
        for source_attr in ("worked_examples", "examples"):
            for example in _as_tuple(getattr(enhanced, source_attr, ())):
                text = _text(example)
                if not text:
                    continue
                examples.append(
                    WorkedExampleView(
                        label=text,
                        detail="",
                        card=Card(
                            title="Worked example",
                            body=text,
                            eyebrow="Example",
                            variant=CardVariant.DEFAULT,
                        ),
                    )
                )
        return tuple(examples)

    @classmethod
    def resources_summary_body(
        cls,
        resources: tuple[LearningResourceView, ...],
    ) -> str:
        """Join resource labels into a section body string."""
        if not resources:
            return _EMPTY_RESOURCE_LABEL
        lines = []
        for resource in resources:
            line = resource.label
            if resource.estimated_minutes:
                line = f"{line} ({resource.estimated_minutes} min)"
            if resource.detail:
                line = f"{line} — {resource.detail}"
            lines.append(line)
        return "\n".join(lines)

    @classmethod
    def examples_summary_body(
        cls,
        examples: tuple[WorkedExampleView, ...],
    ) -> str:
        """Join worked-example labels into a section body string."""
        if not examples:
            return _EMPTY_EXAMPLE_LABEL
        return "\n".join(example.label for example in examples if example.label)

    @classmethod
    def study_notes_body(
        cls,
        workspace: MissionWorkspaceViewModel | None,
        *,
        result: Any = None,
    ) -> str:
        """Collect tip-style notes for the study-notes section."""
        tips: list[str] = []
        for resource in cls._workspace_resources(workspace):
            if resource.kind == "tip" and resource.label:
                tips.append(resource.label)
        if tips:
            return "\n".join(tips)

        enhanced = getattr(result, "enhanced_mission", None) if result else None
        for tip in _as_tuple(getattr(enhanced, "revision_tips", ())):
            text = _text(tip)
            if text:
                tips.append(text)
        if tips:
            return "\n".join(tips)

        if workspace is not None and workspace.mission_explanation:
            return workspace.mission_explanation
        return "Capture what you notice as you work through today's session."

    @classmethod
    def _workspace_resources(
        cls,
        workspace: MissionWorkspaceViewModel | None,
    ) -> tuple[StudyResourceView, ...]:
        if workspace is None:
            return ()
        return tuple(workspace.study_resources or ())

    @classmethod
    def _to_learning_resource(cls, resource: StudyResourceView) -> LearningResourceView:
        eyebrow = "Tip" if resource.kind == "tip" else "Task"
        detail = resource.detail
        if resource.estimated_minutes:
            minutes = f"{resource.estimated_minutes} min"
            detail = f"{detail} · {minutes}".strip(" ·") if detail else minutes
        return LearningResourceView(
            label=resource.label,
            detail=resource.detail,
            kind=resource.kind,
            estimated_minutes=resource.estimated_minutes,
            card=Card(
                title=resource.label or "Study resource",
                body=detail,
                eyebrow=eyebrow,
                variant=CardVariant.DEFAULT,
            ),
        )

    @classmethod
    def _to_worked_example(cls, resource: StudyResourceView) -> WorkedExampleView:
        return WorkedExampleView(
            label=resource.label,
            detail=resource.detail,
            card=Card(
                title="Worked example",
                body=resource.label,
                eyebrow="Example",
                variant=CardVariant.DEFAULT,
            ),
        )


def _as_tuple(value: Any) -> tuple[Any, ...]:
    if value is None:
        return ()
    if isinstance(value, tuple):
        return value
    try:
        return tuple(value)
    except TypeError:
        return ()


def _text(value: Any, *, fallback: str = "") -> str:
    if value is None:
        return fallback
    cleaned = str(value).strip()
    return cleaned if cleaned else fallback

"""ProgressCard — session / mission progress for the workspace."""

from __future__ import annotations

from dataclasses import dataclass

from application.student_experience.workspace.enums import QualityIndicatorKind
from application.student_experience.workspace.errors import WorkspaceInvariantViolation


@dataclass(frozen=True, slots=True)
class QualityIndicator:
    """One study-quality indicator projected from existing execution metrics."""

    kind: QualityIndicatorKind
    label: str
    message: str

    def __post_init__(self) -> None:
        if not isinstance(self.kind, QualityIndicatorKind):
            raise WorkspaceInvariantViolation(
                "kind must be a QualityIndicatorKind",
                invariant="QualityIndicator.kind.type",
            )
        for name in ("label", "message"):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"QualityIndicator.{name}.required",
                )
            object.__setattr__(self, name, value)


@dataclass(frozen=True, slots=True)
class ProgressCard:
    """Immutable progress projection for the current workspace session."""

    available: bool
    completion_percent: float | None
    completion_label: str
    time_invested_minutes: int | None
    time_invested_label: str
    remaining_work_minutes: int | None
    remaining_work_label: str
    quality_indicators: tuple[QualityIndicator, ...]
    summary: str

    def __post_init__(self) -> None:
        for name in (
            "completion_label",
            "time_invested_label",
            "remaining_work_label",
            "summary",
        ):
            value = (getattr(self, name) or "").strip()
            if not value:
                raise WorkspaceInvariantViolation(
                    f"{name} must be a non-empty string",
                    invariant=f"ProgressCard.{name}.required",
                )
            object.__setattr__(self, name, value)
        if self.completion_percent is not None:
            if isinstance(self.completion_percent, bool) or not isinstance(
                self.completion_percent, int | float
            ):
                raise WorkspaceInvariantViolation(
                    "completion_percent must be a real number when provided",
                    invariant="ProgressCard.completion_percent.type",
                )
            object.__setattr__(
                self, "completion_percent", round(float(self.completion_percent), 2)
            )
        for name in ("time_invested_minutes", "remaining_work_minutes"):
            value = getattr(self, name)
            if value is None:
                continue
            if isinstance(value, bool) or not isinstance(value, int):
                raise WorkspaceInvariantViolation(
                    f"{name} must be an integer when provided",
                    invariant=f"ProgressCard.{name}.type",
                )
            if value < 0:
                raise WorkspaceInvariantViolation(
                    f"{name} must be >= 0",
                    invariant=f"ProgressCard.{name}.range",
                )
        object.__setattr__(self, "quality_indicators", tuple(self.quality_indicators))
        for item in self.quality_indicators:
            if not isinstance(item, QualityIndicator):
                raise WorkspaceInvariantViolation(
                    "quality_indicators must contain QualityIndicator values",
                    invariant="ProgressCard.quality_indicators.type",
                )

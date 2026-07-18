"""Structural rule constraining Instructional Blueprint compilation.

Rules are pedagogical structure constraints — never content generators.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum


class BlueprintRuleKind(StrEnum):
    """Kinds of structural blueprint rules."""

    REQUIRE_ACTIVITY = "require_activity"
    FORBID_ACTIVITY = "forbid_activity"
    MAX_STEPS = "max_steps"
    MIN_STEPS = "min_steps"
    BOOKEND_INTRODUCTION = "bookend_introduction"
    BOOKEND_SUMMARY = "bookend_summary"
    BOOKEND_REFLECTION = "bookend_reflection"
    MIN_PRACTICE_RATIO = "min_practice_ratio"
    MAX_THEORY_RATIO = "max_theory_ratio"
    CUSTOM = "custom"

    @classmethod
    def resolve(cls, value: BlueprintRuleKind | str) -> BlueprintRuleKind:
        """Resolve a rule kind token."""
        if isinstance(value, BlueprintRuleKind):
            return value
        token = (value or "").strip().lower().replace("-", "_").replace(" ", "_")
        if not token:
            return cls.CUSTOM
        try:
            return cls(token)
        except ValueError:
            upper = token.upper()
            if upper in cls.__members__:
                return cls[upper]
            return cls.CUSTOM


@dataclass(frozen=True)
class BlueprintRule:
    """One structural compilation / validation rule.

    Attributes:
        rule_id: Stable identity within the blueprint.
        kind: Rule vocabulary member.
        parameters: Immutable structural key=value parameter tags.
        severity: soft (warn) or hard (fail validation / block compile).
        metadata: Extra structural tags.
    """

    rule_id: str
    kind: BlueprintRuleKind
    parameters: tuple[str, ...] = field(default_factory=tuple)
    severity: str = "hard"
    metadata: tuple[str, ...] = field(default_factory=tuple)

    @classmethod
    def create(
        cls,
        rule_id: str,
        kind: BlueprintRuleKind | str,
        *,
        parameters: list[str] | tuple[str, ...] | dict[str, str] | None = None,
        severity: str = "hard",
        metadata: list[str] | tuple[str, ...] | None = None,
    ) -> BlueprintRule:
        """Construct a BlueprintRule after validating invariants.

        Raises:
            ValueError: On empty identity or unsupported severity.
        """
        rid = _require_non_empty(rule_id, "rule_id")
        severity_token = (severity or "hard").strip().lower()
        if severity_token not in {"hard", "soft"}:
            raise ValueError("severity must be 'hard' or 'soft'")
        return cls(
            rule_id=rid,
            kind=BlueprintRuleKind.resolve(kind),
            parameters=_normalise_parameters(parameters),
            severity=severity_token,
            metadata=tuple(metadata or ()),
        )

    def parameter_map(self) -> dict[str, str]:
        """Parse ``key=value`` parameter tags into a dict."""
        result: dict[str, str] = {}
        for item in self.parameters:
            if "=" not in item:
                continue
            key, _, value = item.partition("=")
            key = key.strip()
            if key:
                result[key] = value.strip()
        return result

    def parameter(self, key: str, default: str | None = None) -> str | None:
        """Return a single parameter value."""
        return self.parameter_map().get(key, default)


def _require_non_empty(value: str, field_name: str) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field_name} must be a non-empty string")
    normalized = value.strip()
    if not normalized:
        raise ValueError(f"{field_name} must be a non-empty string")
    return normalized


def _normalise_parameters(
    parameters: list[str] | tuple[str, ...] | dict[str, str] | None,
) -> tuple[str, ...]:
    if parameters is None:
        return ()
    if isinstance(parameters, dict):
        return tuple(f"{k}={v}" for k, v in parameters.items())
    return tuple(str(item) for item in parameters)

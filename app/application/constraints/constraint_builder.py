"""ConstraintBuilder — Application Layer Constraints construction.

Converts authorised product context into immutable domain Constraints for
Educational Orchestrator. Owns collection, construction, lawful product
defaults, validation, and immutable emission.

Never estimates educational need, derives Readiness, ranks Recommendations,
optimises Missions, mutates Twin, interprets curriculum, or imports Flask /
routes / templates / ORM. Domains consume Constraints as feasibility bounds.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from datetime import datetime

from app.domain.decision.constraints import Constraints, IntensityPosture

# Operational note tags — feasibility packaging only, never educational claims.
_OFFLINE_TAG = "offline"
_SESSION_TYPE_PREFIX = "session_type:"
_INTENSITY_UNKNOWN_TAG = "intensity_unknown"
_PREFERENCES_ABSENT_TAG = "preferences_absent"


class ConstraintBuildError(Exception):
    """Base class for ConstraintBuilder fail-closed outcomes."""


class MissingIdentityError(ConstraintBuildError):
    """Authorised student identity is required and was not provided."""


class InvalidConstraintInputError(ConstraintBuildError):
    """Product context cannot form a lawful Constraints artefact."""


@dataclass(frozen=True)
class ConstraintProductConfiguration:
    """Lawful, non-educational product defaults for Constraints construction.

    Only fields architecture explicitly allows as product defaults — never
    invented study minutes, Mid intensity theatre, or educational scorers.
    """

    default_session_type: str | None = None


@dataclass(frozen=True)
class ConstraintProductContext:
    """Product / session facts for one Constraints construction pass.

    Sitting facts only. Unknown optional fields remain unset — never fabricated
    into educational certainty or fake study capacity.
    """

    student_id: str | None
    as_of: datetime | None = None
    available_minutes: int | None = None
    session_type: str | None = None
    preferred_intensity: IntensityPosture | str | None = None
    max_intensity_minutes: int | None = None
    burnout_risk: bool | None = None
    offline: bool = False
    preferences: Mapping[str, object] | None = None


class ConstraintBuilder:
    """Application constructor: product context → immutable Constraints.

    Called by Educational Orchestrator (or Application composition). Domains
    never import ConstraintBuilder; they receive Constraints as arguments.
    """

    def __init__(
        self,
        *,
        configuration: ConstraintProductConfiguration | None = None,
    ) -> None:
        """Wire optional product configuration for lawful defaults.

        Args:
            configuration: Named product defaults (e.g. default session type
                label). When ``None``, no configuration defaults are applied.
        """
        self._configuration = configuration or ConstraintProductConfiguration()

    def build(self, context: ConstraintProductContext) -> Constraints:
        """Construct immutable Constraints from known product facts.

        Args:
            context: Authorised product / session facts for this composition
                pass. Ownership of ``student_id`` must already be validated.

        Returns:
            Frozen domain ``Constraints`` for one composition pass. Unknown
            optional fields remain unknown (e.g. ``available_minutes=None``).

        Raises:
            MissingIdentityError: Student identity missing or blank.
            InvalidConstraintInputError: Inputs contradict structural bounds.
        """
        student_id = _normalize_student_id(context.student_id)
        if student_id is None:
            raise MissingIdentityError("authorised student identity is required")

        available_minutes = _validate_optional_minutes(
            context.available_minutes,
            field_name="available_minutes",
        )
        max_intensity_minutes = _validate_optional_minutes(
            context.max_intensity_minutes,
            field_name="max_intensity_minutes",
        )

        intensity = _resolve_intensity(context.preferred_intensity)
        burnout_risk = (
            bool(context.burnout_risk) if context.burnout_risk is not None else False
        )
        note_tags = _build_note_tags(
            context=context,
            configuration=self._configuration,
            intensity_known=intensity is not None,
        )

        try:
            if intensity is None:
                return Constraints.create(
                    available_minutes=available_minutes,
                    burnout_risk=burnout_risk,
                    max_intensity_minutes=max_intensity_minutes,
                    note_tags=note_tags,
                )
            return Constraints.create(
                available_minutes=available_minutes,
                intensity=intensity,
                burnout_risk=burnout_risk,
                max_intensity_minutes=max_intensity_minutes,
                note_tags=note_tags,
            )
        except ValueError as exc:
            raise InvalidConstraintInputError(str(exc)) from exc


def _normalize_student_id(student_id: str | None) -> str | None:
    """Require a non-blank student identity; never guess."""
    if student_id is None:
        return None
    if not isinstance(student_id, str):
        return None
    normalized = student_id.strip()
    if not normalized:
        return None
    return normalized


def _validate_optional_minutes(value: int | None, *, field_name: str) -> int | None:
    """Accept None (unknown) or a non-negative int; never invent minutes."""
    if value is None:
        return None
    if isinstance(value, bool) or not isinstance(value, int):
        raise InvalidConstraintInputError(
            f"{field_name} must be an int or None, got {type(value)!r}"
        )
    if value < 0:
        raise InvalidConstraintInputError(
            f"{field_name} must be non-negative, got {value}"
        )
    return value


def _resolve_intensity(
    preferred_intensity: IntensityPosture | str | None,
) -> IntensityPosture | None:
    """Map known preference intensity; return None when unknown.

    Does not invent Mid / High / protect intensity when preferences are absent.
    """
    if preferred_intensity is None:
        return None
    if isinstance(preferred_intensity, IntensityPosture):
        return preferred_intensity
    if isinstance(preferred_intensity, str):
        normalized = preferred_intensity.strip()
        if not normalized:
            return None
        try:
            return IntensityPosture(normalized)
        except ValueError as exc:
            raise InvalidConstraintInputError(
                f"preferred_intensity is not a lawful IntensityPosture: "
                f"{preferred_intensity!r}"
            ) from exc
    raise InvalidConstraintInputError(
        f"preferred_intensity must be IntensityPosture, str, or None, "
        f"got {type(preferred_intensity)!r}"
    )


def _build_note_tags(
    *,
    context: ConstraintProductContext,
    configuration: ConstraintProductConfiguration,
    intensity_known: bool,
) -> tuple[str, ...]:
    """Package known operational facts as Constraints note tags."""
    tags: list[str] = []

    session_type = _resolve_session_type(context, configuration)
    if session_type is not None:
        tags.append(f"{_SESSION_TYPE_PREFIX}{session_type}")

    if context.offline:
        tags.append(_OFFLINE_TAG)

    preferences_absent = context.preferences is None and not intensity_known
    if preferences_absent:
        tags.append(_PREFERENCES_ABSENT_TAG)

    if not intensity_known:
        tags.append(_INTENSITY_UNKNOWN_TAG)

    # as_of is accepted as product context; Constraints has no clock field.
    # Do not invent duration or urgency from the timestamp.
    _ = context.as_of

    return tuple(tags)


def _resolve_session_type(
    context: ConstraintProductContext,
    configuration: ConstraintProductConfiguration,
) -> str | None:
    """Use known session type, else lawful product default label only."""
    if context.session_type is not None:
        if not isinstance(context.session_type, str):
            raise InvalidConstraintInputError(
                f"session_type must be str or None, got {type(context.session_type)!r}"
            )
        normalized = context.session_type.strip()
        if normalized:
            return normalized

    default = configuration.default_session_type
    if default is None:
        return None
    if not isinstance(default, str):
        return None
    normalized_default = default.strip()
    return normalized_default or None

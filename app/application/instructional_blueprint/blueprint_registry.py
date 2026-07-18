"""In-memory registry of Instructional Blueprints.

Seeds the eight initial pedagogical strategies. Never persists. Never
loads curriculum content.
"""

from __future__ import annotations

from app.application.instructional_blueprint.exceptions import (
    BlueprintAlreadyRegistered,
    BlueprintNotFound,
    RegistryError,
)
from app.domain.instructional_blueprint.blueprint import InstructionalBlueprint
from app.domain.instructional_blueprint.blueprint_profile import BlueprintProfile
from app.domain.instructional_blueprint.blueprint_rule import BlueprintRule
from app.domain.instructional_blueprint.blueprint_step import BlueprintStep
from app.domain.instructional_blueprint.blueprint_type import BlueprintType
from app.domain.instructional_blueprint.effort_band import EffortBand


def _steps(
    *kinds: str,
    roles: tuple[str, ...] | None = None,
) -> tuple[BlueprintStep, ...]:
    role_values = roles or ()
    built: list[BlueprintStep] = []
    for index, kind in enumerate(kinds):
        role = role_values[index] if index < len(role_values) else None
        weight = 2 if kind in {"independent_practice", "knowledge_check"} else 1
        built.append(
            BlueprintStep.create(
                f"step-{index}-{kind}",
                kind,
                sequence_index=index,
                role=role,
                effort_weight=weight,
            )
        )
    return tuple(built)


def _default_catalogue() -> dict[str, InstructionalBlueprint]:
    """Build the eight initial instructional blueprints."""
    catalogue: dict[str, InstructionalBlueprint] = {}

    definitions: list[
        tuple[
            BlueprintType,
            str,
            tuple[BlueprintStep, ...],
            BlueprintProfile,
            tuple[BlueprintRule, ...],
        ]
    ] = [
        (
            BlueprintType.CONCEPT_MASTERY,
            "Concept Mastery",
            _steps(
                "introduction",
                "concept_learning",
                "worked_example",
                "guided_practice",
                "knowledge_check",
                "reflection",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "core",
                    "practice",
                    "assess",
                    "consolidate",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-concept-mastery",
                theory_weight=40,
                practice_weight=35,
                revision_weight=10,
                assessment_weight=15,
                default_effort_band=EffortBand.MEDIUM,
                intensity=3,
            ),
            (
                BlueprintRule.create(
                    "cm-require-concept",
                    "require_activity",
                    parameters={"activity_kind": "concept_learning"},
                ),
                BlueprintRule.create("cm-bookend-summary", "bookend_summary"),
            ),
        ),
        (
            BlueprintType.CALCULATION_INTENSIVE,
            "Calculation Intensive",
            _steps(
                "introduction",
                "worked_example",
                "guided_practice",
                "independent_practice",
                "independent_practice",
                "knowledge_check",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "practice",
                    "practice",
                    "practice",
                    "assess",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-calculation-intensive",
                theory_weight=15,
                practice_weight=60,
                revision_weight=5,
                assessment_weight=20,
                default_effort_band=EffortBand.HIGH,
                intensity=4,
            ),
            (
                BlueprintRule.create(
                    "ci-min-practice",
                    "min_practice_ratio",
                    parameters={"ratio": "0.5"},
                ),
                BlueprintRule.create("ci-bookend-intro", "bookend_introduction"),
            ),
        ),
        (
            BlueprintType.THEORY_HEAVY,
            "Theory Heavy",
            _steps(
                "introduction",
                "concept_learning",
                "concept_learning",
                "worked_example",
                "reflection",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "core",
                    "core",
                    "consolidate",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-theory-heavy",
                theory_weight=55,
                practice_weight=20,
                revision_weight=10,
                assessment_weight=15,
                default_effort_band=EffortBand.MEDIUM,
                intensity=3,
            ),
            (
                BlueprintRule.create(
                    "th-max-theory",
                    "max_theory_ratio",
                    parameters={"ratio": "0.85"},
                    severity="soft",
                ),
                BlueprintRule.create("th-bookend-reflection", "bookend_reflection"),
            ),
        ),
        (
            BlueprintType.REVISION,
            "Revision",
            _steps(
                "introduction",
                "spaced_recall",
                "review",
                "knowledge_check",
                "independent_practice",
                "reflection",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "core",
                    "assess",
                    "practice",
                    "consolidate",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-revision",
                theory_weight=15,
                practice_weight=25,
                revision_weight=45,
                assessment_weight=15,
                default_effort_band=EffortBand.MEDIUM,
                intensity=3,
            ),
            (
                BlueprintRule.create(
                    "rev-require-review",
                    "require_activity",
                    parameters={"activity_kind": "review"},
                ),
                BlueprintRule.create("rev-bookend-summary", "bookend_summary"),
            ),
        ),
        (
            BlueprintType.MIXED_PRACTICE,
            "Mixed Practice",
            _steps(
                "introduction",
                "concept_learning",
                "guided_practice",
                "independent_practice",
                "knowledge_check",
                "review",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "practice",
                    "practice",
                    "assess",
                    "revise",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-mixed-practice",
                theory_weight=25,
                practice_weight=40,
                revision_weight=20,
                assessment_weight=15,
                default_effort_band=EffortBand.MEDIUM,
                intensity=3,
            ),
            (
                BlueprintRule.create(
                    "mp-min-steps",
                    "min_steps",
                    parameters={"count": "5"},
                ),
            ),
        ),
        (
            BlueprintType.EXAM_PRACTICE,
            "Exam Practice",
            _steps(
                "introduction",
                "independent_practice",
                "knowledge_check",
                "independent_practice",
                "knowledge_check",
                "reflection",
                "summary",
                roles=(
                    "warm_up",
                    "practice",
                    "assess",
                    "practice",
                    "assess",
                    "consolidate",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-exam-practice",
                theory_weight=10,
                practice_weight=40,
                revision_weight=10,
                assessment_weight=40,
                default_effort_band=EffortBand.HIGH,
                intensity=4,
            ),
            (
                BlueprintRule.create(
                    "ep-require-check",
                    "require_activity",
                    parameters={"activity_kind": "knowledge_check"},
                ),
                BlueprintRule.create(
                    "ep-min-practice",
                    "min_practice_ratio",
                    parameters={"ratio": "0.4"},
                ),
            ),
        ),
        (
            BlueprintType.CASE_STUDY,
            "Case Study",
            _steps(
                "introduction",
                "concept_learning",
                "worked_example",
                "guided_practice",
                "independent_practice",
                "reflection",
                "summary",
                roles=(
                    "warm_up",
                    "core",
                    "core",
                    "practice",
                    "practice",
                    "consolidate",
                    "consolidate",
                ),
            ),
            BlueprintProfile.create(
                "profile-case-study",
                theory_weight=30,
                practice_weight=40,
                revision_weight=10,
                assessment_weight=20,
                default_effort_band=EffortBand.HIGH,
                intensity=4,
            ),
            (
                BlueprintRule.create(
                    "cs-require-worked",
                    "require_activity",
                    parameters={"activity_kind": "worked_example"},
                ),
                BlueprintRule.create("cs-bookend-reflection", "bookend_reflection"),
            ),
        ),
        (
            BlueprintType.CUSTOM,
            "Custom",
            (),
            BlueprintProfile.create(
                "profile-custom",
                theory_weight=25,
                practice_weight=25,
                revision_weight=25,
                assessment_weight=25,
                default_effort_band=EffortBand.MEDIUM,
                intensity=3,
            ),
            (
                BlueprintRule.create(
                    "custom-min-steps",
                    "min_steps",
                    parameters={"count": "1"},
                    severity="soft",
                ),
            ),
        ),
    ]

    for blueprint_type, name, steps, profile, rules in definitions:
        blueprint = InstructionalBlueprint.create(
            f"bp-{blueprint_type.value}",
            blueprint_type,
            name,
            steps=steps,
            rules=rules,
            profile=profile,
            metadata=("default_catalogue", blueprint_type.value),
            allow_empty_steps=blueprint_type == BlueprintType.CUSTOM,
        )
        catalogue[blueprint.blueprint_id] = blueprint
    return catalogue


class BlueprintRegistry:
    """Register and look up Instructional Blueprints in memory."""

    def __init__(self, *, seed_defaults: bool = True) -> None:
        self._by_id: dict[str, InstructionalBlueprint] = {}
        self._by_type: dict[BlueprintType, str] = {}
        if seed_defaults:
            for blueprint in _default_catalogue().values():
                self._store(blueprint, overwrite=True)

    def register(
        self,
        blueprint: InstructionalBlueprint,
        *,
        overwrite: bool = False,
    ) -> InstructionalBlueprint:
        """Register a blueprint.

        Raises:
            BlueprintAlreadyRegistered: When identity exists and overwrite is False.
            RegistryError: When blueprint is invalid for registration.
        """
        if not isinstance(blueprint, InstructionalBlueprint):
            raise RegistryError("register requires an InstructionalBlueprint")
        if blueprint.blueprint_id in self._by_id and not overwrite:
            raise BlueprintAlreadyRegistered(
                f"Blueprint {blueprint.blueprint_id!r} is already registered"
            )
        self._store(blueprint, overwrite=overwrite)
        return blueprint

    def get(self, blueprint_id: str) -> InstructionalBlueprint:
        """Return a blueprint by identity.

        Raises:
            BlueprintNotFound: When the identity is unknown.
        """
        bid = (blueprint_id or "").strip()
        if not bid or bid not in self._by_id:
            raise BlueprintNotFound(f"Blueprint {blueprint_id!r} not found")
        return self._by_id[bid]

    def get_by_type(
        self, blueprint_type: BlueprintType | str
    ) -> InstructionalBlueprint:
        """Return the registered blueprint for a catalogue type.

        Raises:
            BlueprintNotFound: When no blueprint is registered for the type.
        """
        resolved = BlueprintType.resolve(blueprint_type)
        blueprint_id = self._by_type.get(resolved)
        if blueprint_id is None:
            raise BlueprintNotFound(
                f"No blueprint registered for type {resolved.value!r}"
            )
        return self._by_id[blueprint_id]

    def has(self, blueprint_id: str) -> bool:
        """True when a blueprint identity is registered."""
        return (blueprint_id or "").strip() in self._by_id

    def has_type(self, blueprint_type: BlueprintType | str) -> bool:
        """True when a catalogue type has a registered blueprint."""
        return BlueprintType.resolve(blueprint_type) in self._by_type

    def list_ids(self) -> tuple[str, ...]:
        """Stable ordered registered blueprint identities."""
        return tuple(sorted(self._by_id))

    def list_types(self) -> tuple[BlueprintType, ...]:
        """Stable ordered registered blueprint types."""
        return tuple(sorted(self._by_type, key=lambda t: t.value))

    def list_blueprints(self) -> tuple[InstructionalBlueprint, ...]:
        """Stable ordered registered blueprints."""
        return tuple(self._by_id[bid] for bid in self.list_ids())

    def unregister(self, blueprint_id: str) -> InstructionalBlueprint:
        """Remove a blueprint from the registry.

        Raises:
            BlueprintNotFound: When the identity is unknown.
        """
        blueprint = self.get(blueprint_id)
        del self._by_id[blueprint.blueprint_id]
        mapped = self._by_type.get(blueprint.blueprint_type)
        if mapped == blueprint.blueprint_id:
            del self._by_type[blueprint.blueprint_type]
        return blueprint

    def clear(self) -> None:
        """Remove all registered blueprints."""
        self._by_id.clear()
        self._by_type.clear()

    def count(self) -> int:
        """Number of registered blueprints."""
        return len(self._by_id)

    def _store(self, blueprint: InstructionalBlueprint, *, overwrite: bool) -> None:
        existing_id = self._by_type.get(blueprint.blueprint_type)
        if (
            existing_id is not None
            and existing_id != blueprint.blueprint_id
            and not overwrite
        ):
            raise BlueprintAlreadyRegistered(
                f"Type {blueprint.blueprint_type.value!r} already mapped to "
                f"{existing_id!r}"
            )
        if (
            existing_id is not None
            and existing_id != blueprint.blueprint_id
            and overwrite
            and existing_id in self._by_id
        ):
            del self._by_id[existing_id]
        self._by_id[blueprint.blueprint_id] = blueprint
        self._by_type[blueprint.blueprint_type] = blueprint.blueprint_id

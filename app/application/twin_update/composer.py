"""Twin Composer — assemble Current Twin + Domain Strategy Outputs.

Capability 4.9.8 realisation of Capability 4.9.5 Strategy Composition.
Authors exactly one complete immutable Successor Twin. Assembles only —
never interprets Evidence, executes Strategies, recommends, persists, or
retrieves.

See Capability 4.9.5 Twin Update Strategy Composition architecture.
"""

from __future__ import annotations

import logging
from collections.abc import Mapping, Sequence
from typing import Any

from app.application.twin_update.outputs import DomainStrategyOutput
from app.domain.twin.behaviour_state import BehaviourState
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.goal_state import GoalState
from app.domain.twin.knowledge_state import KnowledgeState
from app.domain.twin.memory_state import MemoryState
from app.domain.twin.performance_state import PerformanceState

logger = logging.getLogger(__name__)

# Single-domain ownership map (Capability 4.9.5 §3.1). Keys are Strategy
# owned_domain identities; values are Twin attribute + expected domain type.
_COMPOSABLE_DOMAINS: Mapping[str, tuple[str, type]] = {
    "knowledge": ("knowledge", KnowledgeState),
    "performance": ("performance", PerformanceState),
    "behaviour": ("behaviour", BehaviourState),
    "memory": ("memory", MemoryState),
    "goals": ("goals", GoalState),
}

_DOMAIN_DISPLAY: Mapping[str, str] = {
    "knowledge": "Knowledge",
    "performance": "Performance",
    "behaviour": "Behaviour",
    "memory": "Memory",
    "goals": "Goals",
}

_REQUIRED_TWIN_ATTRS: tuple[str, ...] = (
    "identity",
    "goals",
    "knowledge",
    "memory",
    "behaviour",
    "performance",
    "predictions",
)


class TwinCompositionError(ValueError):
    """Structural composition failure — never an educational judgement."""


class DomainOutputCollection:
    """Validated collection of Domain Strategy Outputs for one composition cycle.

    Enforces domain uniqueness and known-domain membership. Does not interpret
    educational meaning of contributions.
    """

    def __init__(self, outputs: Sequence[DomainStrategyOutput]) -> None:
        """Validate and freeze Domain Strategy Outputs.

        Args:
            outputs: Strategy contributions for this composition cycle.

        Raises:
            TwinCompositionError: On duplicate domain, unknown domain, or
                invalid Strategy Output structure / contribution type.
        """
        validated: list[DomainStrategyOutput] = []
        seen: dict[str, str] = {}
        for index, output in enumerate(outputs):
            if not isinstance(output, DomainStrategyOutput):
                raise TwinCompositionError(
                    f"outputs[{index}] is not a DomainStrategyOutput"
                )
            domain = _normalise_domain(output.owned_domain)
            if domain not in _COMPOSABLE_DOMAINS:
                raise TwinCompositionError(
                    f"unknown domain: {output.owned_domain!r}"
                )
            if domain in seen:
                raise TwinCompositionError(
                    f"duplicate domain output: {domain!r} "
                    f"(strategies {seen[domain]!r} and "
                    f"{output.strategy_identity!r})"
                )
            _validate_contribution(domain, output.domain_contribution)
            if not output.strategy_identity.strip():
                raise TwinCompositionError(
                    f"outputs[{index}] strategy_identity must be non-empty"
                )
            # Re-bind with normalised domain so downstream replacement is stable.
            normalised = DomainStrategyOutput(
                strategy_identity=output.strategy_identity.strip(),
                owned_domain=domain,
                domain_contribution=output.domain_contribution,
                preserved=output.preserved,
            )
            seen[domain] = normalised.strategy_identity
            validated.append(normalised)
        self._outputs = tuple(validated)
        self._by_domain = {item.owned_domain: item for item in self._outputs}

    @classmethod
    def from_outputs(
        cls,
        outputs: Sequence[DomainStrategyOutput] | None,
    ) -> DomainOutputCollection:
        """Build a DomainOutputCollection from a sequence (empty allowed).

        Raises:
            TwinCompositionError: If ``outputs`` is not a sequence of outputs.
        """
        if outputs is None:
            raise TwinCompositionError("Domain Strategy Outputs are required")
        if isinstance(outputs, str | bytes):
            raise TwinCompositionError(
                "Domain Strategy Outputs must be a sequence of outputs"
            )
        if not isinstance(outputs, Sequence):
            raise TwinCompositionError(
                "Domain Strategy Outputs must be a sequence of outputs"
            )
        return cls(outputs)

    @property
    def outputs(self) -> tuple[DomainStrategyOutput, ...]:
        """Frozen Domain Strategy Outputs in invitation order."""
        return self._outputs

    def get(self, domain: str) -> DomainStrategyOutput | None:
        """Return the output for ``domain`` when present."""
        return self._by_domain.get(_normalise_domain(domain))

    def contains(self, domain: str) -> bool:
        """True when a Strategy Output covers ``domain``."""
        return _normalise_domain(domain) in self._by_domain

    def __len__(self) -> int:
        return len(self._outputs)

    def __iter__(self):
        return iter(self._outputs)


class TwinComposer:
    """Assembly authority for Strategy Composition (Capability 4.9.5 / 4.9.8).

    Receives Current Twin + Domain Strategy Outputs and authors exactly one
    complete immutable Successor Twin. Replace only supplied domains; preserve
    every other domain exactly. Never mutates Current Twin.
    """

    def compose(
        self,
        current_twin: DigitalTwin | None,
        outputs: Sequence[DomainStrategyOutput] | DomainOutputCollection | None,
    ) -> DigitalTwin:
        """Author one immutable Successor Twin from Current Twin + outputs.

        Args:
            current_twin: Lawful immutable Current Twin succession base.
            outputs: Domain Strategy Outputs for this composition cycle
                (tuple/list or validated DomainOutputCollection). Empty
                collection is lawful — all domains carry forward.

        Returns:
            Newly created complete immutable DigitalTwin Successor.

        Raises:
            TwinCompositionError: On missing/invalid Current Twin, duplicate
                or unknown domain, invalid Strategy Output, or incomplete
                successor assembly.
        """
        logger.info("Composer started")

        twin = _require_current_twin(current_twin)
        collection = (
            outputs
            if isinstance(outputs, DomainOutputCollection)
            else DomainOutputCollection.from_outputs(outputs)
        )

        domain_kwargs: dict[str, Any] = {
            "goals": twin.goals,
            "knowledge": twin.knowledge,
            "memory": twin.memory,
            "behaviour": twin.behaviour,
            "performance": twin.performance,
            "predictions": twin.predictions,
        }

        for domain_key, (attr_name, _expected_type) in _COMPOSABLE_DOMAINS.items():
            output = collection.get(domain_key)
            if output is None:
                logger.info("%s preserved", _DOMAIN_DISPLAY[domain_key])
                continue
            domain_kwargs[attr_name] = output.domain_contribution
            logger.info("%s domain replaced", _DOMAIN_DISPLAY[domain_key])

        try:
            successor = DigitalTwin.create(twin.identity, **domain_kwargs)
        except Exception as exc:  # noqa: BLE001 — structural assembly only
            raise TwinCompositionError(
                f"Successor Twin assembly failed: {exc}"
            ) from exc

        _assert_successor_complete(successor)
        _assert_identity_preserved(twin, successor)

        logger.info("Successor Twin assembled")
        logger.info("Composer completed")
        return successor


def _normalise_domain(owned_domain: object) -> str:
    if not isinstance(owned_domain, str):
        return ""
    return owned_domain.strip().lower()


def _validate_contribution(domain: str, contribution: object) -> None:
    _attr, expected_type = _COMPOSABLE_DOMAINS[domain]
    if not isinstance(contribution, expected_type):
        raise TwinCompositionError(
            f"invalid Strategy Output for {domain!r}: expected "
            f"{expected_type.__name__}, got {type(contribution).__name__}"
        )


def _require_current_twin(current_twin: DigitalTwin | None) -> DigitalTwin:
    if current_twin is None:
        raise TwinCompositionError(
            "Current Twin is required; Calibration remains birth author"
        )
    if not isinstance(current_twin, DigitalTwin):
        raise TwinCompositionError("Current Twin payload is not a DigitalTwin")

    student_id = getattr(
        getattr(current_twin, "identity", None), "student_id", None
    )
    if not isinstance(student_id, str) or not student_id.strip():
        raise TwinCompositionError(
            "Current Twin identity.student_id is missing"
        )

    for attr in _REQUIRED_TWIN_ATTRS:
        if not hasattr(current_twin, attr):
            raise TwinCompositionError(
                f"Current Twin missing domain attribute: {attr}"
            )
        if getattr(current_twin, attr) is None:
            raise TwinCompositionError(
                f"Current Twin domain attribute is None: {attr}"
            )
    return current_twin


def _assert_successor_complete(successor: DigitalTwin) -> None:
    if not isinstance(successor, DigitalTwin):
        raise TwinCompositionError("Successor is not a DigitalTwin")
    for attr in _REQUIRED_TWIN_ATTRS:
        if not hasattr(successor, attr) or getattr(successor, attr) is None:
            raise TwinCompositionError(
                f"Successor Twin incomplete: missing {attr}"
            )


def _assert_identity_preserved(
    current: DigitalTwin,
    successor: DigitalTwin,
) -> None:
    if successor.identity is not current.identity:
        # Structural equality still required when references differ.
        if successor.identity != current.identity:
            raise TwinCompositionError(
                "Successor Twin must preserve Current Twin identity"
            )
    if successor.predictions is not current.predictions:
        if successor.predictions != current.predictions:
            raise TwinCompositionError(
                "Successor Twin must preserve Current Twin predictions"
            )

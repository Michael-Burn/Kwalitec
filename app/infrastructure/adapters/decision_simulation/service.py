"""Advisory Decision Simulation Service (P2-MS011).

Parallel simulation path that evaluates how Runtime A recommendations would
differ if advisory inputs were considered. Never modifies production
recommendation outputs returned to the student.
"""

from __future__ import annotations

import hashlib
import logging
from collections.abc import Mapping, Sequence
from typing import Any

from .contracts import (
    AUTHORITY_DECISION_SIMULATION,
    AUTHORITY_RUNTIME_A,
    INVALID_STATE,
    SIMULATION_VERSION,
    UNAVAILABLE,
    DecisionComparisonRecord,
    DecisionDifference,
    DecisionSimulationContext,
    DecisionSimulationResult,
    SimulatedRecommendation,
    serialize_canonical,
    snapshot_mapping,
    snapshot_mapping_tuple,
)

logger = logging.getLogger(__name__)

SERVICE_ID = "decision_simulation_service"
SOURCE_SERVICE = "decision_simulation"

ADVISORY_SOURCE_EVIDENCE = "evidence_advisory"
ADVISORY_SOURCE_RECOVERY = "recovery_candidate"

# Structural simulation only — no ranking / schedule algorithms.
SIMULATION_MODE_STRUCTURAL = "structural_mirror_with_advisory_annotation"


def deterministic_simulation_id(
    *,
    recommendation_id: str,
    student_id: str,
    runtime_inputs: Mapping[str, Any],
    generated_at: str | None,
) -> str:
    """Deterministic simulation id from material inputs."""
    material = {
        "generated_at": generated_at,
        "recommendation_id": (recommendation_id or "").strip(),
        "runtime_inputs": dict(runtime_inputs or {}),
        "student_id": (student_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"sim-{digest}"


def deterministic_comparison_id(simulation_id: str, recommendation_id: str) -> str:
    """Deterministic comparison id."""
    material = {
        "recommendation_id": (recommendation_id or "").strip(),
        "simulation_id": (simulation_id or "").strip(),
    }
    digest = hashlib.sha256(
        serialize_canonical(material).encode("utf-8")
    ).hexdigest()[:16]
    return f"simcmp-{digest}"


def _production_snapshot(runtime_inputs: Mapping[str, Any]) -> dict[str, Any]:
    """Extract the production recommendation snapshot from runtime_inputs."""
    production = runtime_inputs.get("production_recommendation")
    if isinstance(production, Mapping):
        return dict(production)
    # Allow flattened recommendation fields at the top level.
    keys = ("title", "category", "priority", "reason", "expected_benefit")
    flat = {k: runtime_inputs[k] for k in keys if k in runtime_inputs}
    return flat


def _advisory_sources(
    context: DecisionSimulationContext,
) -> tuple[str, ...]:
    sources: list[str] = []
    if context.evidence_advisory:
        sources.append(ADVISORY_SOURCE_EVIDENCE)
        advisory_id = context.evidence_advisory.get("advisory_id")
        if advisory_id:
            sources.append(f"evidence_advisory:{advisory_id}")
    for index, candidate in enumerate(context.recovery_candidates):
        sources.append(ADVISORY_SOURCE_RECOVERY)
        candidate_id = candidate.get("candidate_id")
        if candidate_id:
            sources.append(f"recovery_candidate:{candidate_id}")
        else:
            sources.append(f"recovery_candidate:index:{index}")
    # Preserve order, drop duplicates.
    seen: set[str] = set()
    ordered: list[str] = []
    for item in sources:
        if item in seen:
            continue
        seen.add(item)
        ordered.append(item)
    return tuple(ordered)


def _build_simulated_rationale(
    *,
    production: Mapping[str, Any],
    advisory_sources: Sequence[str],
) -> str:
    base = str(production.get("reason") or production.get("rationale") or "").strip()
    if not advisory_sources:
        note = (
            "Simulation structural mirror: no advisory inputs were supplied. "
            "Production recommendation left unchanged in simulation."
        )
        return f"{base} | {note}".strip(" |") if base else note
    joined = ", ".join(advisory_sources)
    note = (
        "Simulation structural annotation only: advisory sources considered "
        f"({joined}). No ranking or schedule optimisation applied; "
        "production priority/title retained."
    )
    return f"{base} | {note}".strip(" |") if base else note


def _diff_fields(
    *,
    production: Mapping[str, Any],
    simulated: SimulatedRecommendation,
) -> tuple[DecisionDifference, ...]:
    diffs: list[DecisionDifference] = []
    prod_priority = str(production.get("priority") or "")
    if prod_priority != simulated.simulated_priority:
        diffs.append(
            DecisionDifference(
                field_name="priority",
                production_value=prod_priority,
                simulated_value=simulated.simulated_priority,
                explanation=(
                    "Simulated priority differs from production "
                    "(unexpected in structural mirror mode)."
                ),
            )
        )
    prod_title = str(production.get("title") or "")
    if prod_title != simulated.simulated_title:
        diffs.append(
            DecisionDifference(
                field_name="title",
                production_value=prod_title,
                simulated_value=simulated.simulated_title,
                explanation=(
                    "Simulated title differs from production "
                    "(unexpected in structural mirror mode)."
                ),
            )
        )
    prod_reason = str(production.get("reason") or production.get("rationale") or "")
    if prod_reason != simulated.simulated_rationale:
        diffs.append(
            DecisionDifference(
                field_name="rationale",
                production_value=prod_reason,
                simulated_value=simulated.simulated_rationale,
                explanation=(
                    "Simulated rationale annotates advisory sources considered; "
                    "production rationale remains authoritative for students."
                ),
            )
        )
    return tuple(diffs)


class DecisionSimulationService:
    """Parallel advisory decision simulation (comparison / explainability only).

    Rules:
    - MAY receive Runtime A inputs and advisory snapshots
    - MAY produce SimulatedRecommendation + DecisionComparisonRecord
    - MUST mark all simulated outputs simulation_only=True
    - MUST NEVER modify production recommendation outputs
    - MUST NOT write Runtime A / Adaptive / Strategy / Twin educational state
    """

    SERVICE_VERSION = "1.0.0-p2.ms011"

    def __init__(self, *, enabled: bool = True) -> None:
        self._enabled = bool(enabled)
        self._last_result: DecisionSimulationResult | None = None
        self._comparisons: list[DecisionComparisonRecord] = []

    @property
    def service_id(self) -> str:
        return SERVICE_ID

    @property
    def service_version(self) -> str:
        return self.SERVICE_VERSION

    def is_enabled(self) -> bool:
        return self._enabled

    @property
    def last_result(self) -> DecisionSimulationResult | None:
        return self._last_result

    @property
    def comparisons(self) -> tuple[DecisionComparisonRecord, ...]:
        """Operational comparison artefacts accumulated this process (in-memory)."""
        return tuple(self._comparisons)

    def clear_comparisons(self) -> None:
        """Clear in-memory operational comparison buffer."""
        self._comparisons.clear()

    def build_context(
        self,
        *,
        recommendation_id: str = "",
        production_recommendation: Mapping[str, Any] | None = None,
        evidence_advisory: Any | None = None,
        recovery_candidates: Sequence[Any] | None = None,
        runtime_inputs: Mapping[str, Any] | None = None,
        student_id: str = "",
        generated_at: str | None = None,
        simulation_id: str = "",
    ) -> DecisionSimulationContext:
        """Assemble an immutable DecisionSimulationContext from caller inputs."""
        inputs = dict(runtime_inputs or {})
        if production_recommendation is not None:
            inputs["production_recommendation"] = dict(production_recommendation)
        if not recommendation_id:
            production = _production_snapshot(inputs)
            recommendation_id = str(
                production.get("recommendation_id")
                or production.get("title")
                or inputs.get("recommendation_id")
                or ""
            ).strip()
        sid = simulation_id or deterministic_simulation_id(
            recommendation_id=recommendation_id,
            student_id=student_id,
            runtime_inputs=inputs,
            generated_at=generated_at,
        )
        return DecisionSimulationContext(
            simulation_id=sid,
            recommendation_id=recommendation_id,
            evidence_advisory=snapshot_mapping(evidence_advisory),
            recovery_candidates=snapshot_mapping_tuple(recovery_candidates),
            runtime_inputs=inputs,
            generated_at=generated_at,
            student_id=student_id,
        )

    def simulate(
        self,
        context: DecisionSimulationContext,
    ) -> DecisionSimulationResult:
        """Produce a simulated recommendation + comparison record.

        Never mutates ``context`` or any production recommendation mapping
        referenced by the caller.
        """
        if not self._enabled:
            result = DecisionSimulationResult(
                ok=False,
                error_code=UNAVAILABLE,
                message="ENABLE_DECISION_SIMULATION is OFF",
            )
            self._last_result = result
            return result
        if not isinstance(context, DecisionSimulationContext):
            result = DecisionSimulationResult(
                ok=False,
                error_code=INVALID_STATE,
                message="context must be a DecisionSimulationContext",
            )
            self._last_result = result
            return result
        try:
            simulated, comparison = self._run_structural_simulation(context)
        except Exception as exc:
            logger.warning(
                "decision_simulation_failed simulation_id=%s error=%s",
                getattr(context, "simulation_id", ""),
                exc,
                exc_info=True,
            )
            result = DecisionSimulationResult(
                ok=False,
                error_code=INVALID_STATE,
                message=str(exc) or "decision simulation failed",
            )
            self._last_result = result
            return result
        self._comparisons.append(comparison)
        result = DecisionSimulationResult(
            ok=True,
            simulated=simulated,
            comparison=comparison,
        )
        self._last_result = result
        logger.debug(
            "decision_simulation_completed simulation_id=%s "
            "differs_from_runtime=%s sources=%s",
            simulated.simulation_id,
            simulated.differs_from_runtime,
            list(simulated.advisory_sources),
        )
        return result

    def simulate_after_recommendations(
        self,
        *,
        student_id: str | int,
        production_recommendations: Sequence[Mapping[str, Any]],
        evidence_advisory: Any | None = None,
        recovery_candidates: Sequence[Any] | None = None,
        generated_at: str | None = None,
    ) -> tuple[DecisionComparisonRecord, ...]:
        """Run parallel simulation for each production recommendation.

        Returns comparison artefacts only. Does **not** alter
        ``production_recommendations``.
        """
        if not self._enabled:
            return ()
        records: list[DecisionComparisonRecord] = []
        sid = str(student_id).strip()
        for index, production in enumerate(production_recommendations or ()):
            if not isinstance(production, Mapping):
                continue
            recommendation_id = str(
                production.get("recommendation_id")
                or production.get("title")
                or f"index:{index}"
            ).strip()
            context = self.build_context(
                recommendation_id=recommendation_id,
                production_recommendation=production,
                evidence_advisory=evidence_advisory,
                recovery_candidates=recovery_candidates,
                student_id=sid,
                generated_at=generated_at,
            )
            result = self.simulate(context)
            if result.ok and result.comparison is not None:
                records.append(result.comparison)
        return tuple(records)

    def _run_structural_simulation(
        self,
        context: DecisionSimulationContext,
    ) -> tuple[SimulatedRecommendation, DecisionComparisonRecord]:
        production = _production_snapshot(context.runtime_inputs)
        # Copy production into a local snapshot — never mutate caller data.
        production_copy = dict(production)
        advisory_sources = _advisory_sources(context)
        simulated_rationale = _build_simulated_rationale(
            production=production_copy,
            advisory_sources=advisory_sources,
        )
        simulated_priority = str(production_copy.get("priority") or "")
        simulated_title = str(production_copy.get("title") or "")
        simulated_category = str(production_copy.get("category") or "")

        # Structural mode retains production priority/title. Rationale may
        # annotate advisory sources — that is an explainability delta only.
        differs = (
            simulated_priority != str(production_copy.get("priority") or "")
            or simulated_title != str(production_copy.get("title") or "")
            or simulated_rationale
            != str(
                production_copy.get("reason")
                or production_copy.get("rationale")
                or ""
            )
        )

        provenance = {
            "authority_chain": {
                "production": AUTHORITY_RUNTIME_A,
                "simulation": AUTHORITY_DECISION_SIMULATION,
            },
            "evidence_advisory_id": (
                (context.evidence_advisory or {}).get("advisory_id")
                if context.evidence_advisory
                else ""
            ),
            "field_provenance": {
                "advisory_sources": (
                    "Derived from evidence_advisory / recovery_candidates"
                ),
                "differs_from_runtime": (
                    "True when simulated fields diverge from production snapshot"
                ),
                "simulated_priority": "Mirrored from production priority (no ranking)",
                "simulated_rationale": (
                    "Production reason plus structural advisory annotation"
                ),
            },
            "mode": SIMULATION_MODE_STRUCTURAL,
            "recovery_candidate_ids": [
                str(item.get("candidate_id") or "")
                for item in context.recovery_candidates
            ],
            "service_id": self.service_id,
            "service_version": self.SERVICE_VERSION,
            "simulation_version": SIMULATION_VERSION,
            "source_service": SOURCE_SERVICE,
        }

        simulated = SimulatedRecommendation(
            simulation_id=context.simulation_id,
            simulated_priority=simulated_priority,
            simulated_rationale=simulated_rationale,
            advisory_sources=advisory_sources,
            differs_from_runtime=differs,
            provenance=provenance,
            simulation_only=True,
            recommendation_id=context.recommendation_id,
            simulated_title=simulated_title,
            simulated_category=simulated_category,
            student_id=context.student_id,
            generated_at=context.generated_at,
        )
        differences = _diff_fields(production=production_copy, simulated=simulated)
        comparison = DecisionComparisonRecord(
            comparison_id=deterministic_comparison_id(
                context.simulation_id, context.recommendation_id
            ),
            simulation_id=context.simulation_id,
            recommendation_id=context.recommendation_id,
            production_recommendation=production_copy,
            simulated_recommendation=simulated,
            differences=differences,
            advisory_sources_considered=advisory_sources,
            provenance={
                "mode": SIMULATION_MODE_STRUCTURAL,
                "operational_only": True,
                "service_id": self.service_id,
                "service_version": self.SERVICE_VERSION,
                "source_service": SOURCE_SERVICE,
            },
            generated_at=context.generated_at,
            student_id=context.student_id,
            operational_only=True,
        )
        return simulated, comparison


def build_decision_simulation_service(
    *,
    enabled: bool,
) -> DecisionSimulationService | None:
    """DI helper — construct service only when ENABLE_DECISION_SIMULATION is ON."""
    if not enabled:
        return None
    return DecisionSimulationService(enabled=True)


__all__ = [
    "ADVISORY_SOURCE_EVIDENCE",
    "ADVISORY_SOURCE_RECOVERY",
    "SERVICE_ID",
    "SIMULATION_MODE_STRUCTURAL",
    "SOURCE_SERVICE",
    "DecisionSimulationService",
    "build_decision_simulation_service",
    "deterministic_comparison_id",
    "deterministic_simulation_id",
]

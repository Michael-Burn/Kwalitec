"""Strategy Engine Adapter — MS-005 S0/S1/S2/S3 surface.

Implements LearningStrategyContract / StrategyAdapter. S1 wires
StrategyContextAssembler + StrategyEngine for core intervention orchestration.
S2 explainability / projection are separate DI components (not wired into
evaluate). S3 shadow validation is observational only (separate DI). No
Experience authority cutover, no Runtime A / Twin / Adaptive mutation.
"""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.infrastructure.adapters.strategy_engine.assembler import (
    StrategyContextAssembler,
    build_strategy_context_assembler,
)
from app.infrastructure.adapters.strategy_engine.contracts import (
    AUTHORITY_STRATEGY_ENGINE,
    AVAILABILITY_UNAVAILABLE,
    STRATEGY_VERSION_S0,
    STRATEGY_VERSION_S1,
    LearningIntervention,
    StrategyContext,
    StrategyExplanationPlaceholder,
    StrategyProvenancePlaceholder,
    StrategyResult,
)
from app.infrastructure.adapters.strategy_engine.engine import (
    StrategyEngine,
    build_strategy_engine,
)
from app.infrastructure.adapters.strategy_engine.validation import (
    StrategyValidationError,
)


class StrategyEngineAdapter:
    """Strategy Engine Adapter — S1 core orchestration behind feature flag.

    When constructed behind ``ENABLE_STRATEGY_ENGINE``, assembles StrategyContext
    (when inputs provided) and evaluates StrategyEngine into one
    LearningIntervention. Does not serve Experience StrategyInterventionPort or
    mutate Runtime A / Twin / Adaptive state.
    """

    ADAPTER_ID = "strategy_engine"
    ADAPTER_VERSION = "1.0.0-s2"
    STRATEGY_VERSION = STRATEGY_VERSION_S1

    def __init__(
        self,
        *,
        engine: StrategyEngine | None = None,
        assembler: StrategyContextAssembler | None = None,
    ) -> None:
        self._engine = engine or StrategyEngine()
        self._assembler = assembler or StrategyContextAssembler()
        self._available = True

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def adapter_version(self) -> str:
        return self.ADAPTER_VERSION

    @property
    def engine(self) -> StrategyEngine:
        return self._engine

    @property
    def assembler(self) -> StrategyContextAssembler:
        return self._assembler

    def is_available(self) -> bool:
        return self._available

    def assemble_context(
        self,
        student_id: str,
        *,
        as_of: str | None = None,
        runtime_a: Mapping[str, Any] | Any | None = None,
        twin: Mapping[str, Any] | Any | None = None,
        adaptive: Mapping[str, Any] | Any | None = None,
        intervention_kinds: tuple[str, ...] | list[str] | None = None,
    ) -> StrategyContext:
        """Assemble StrategyContext from consumed inputs (read-only freeze)."""
        return self._assembler.assemble(
            student_id,
            as_of=as_of,
            runtime_a=runtime_a,
            twin=twin,
            adaptive=adaptive,
            intervention_kinds=intervention_kinds,
        )

    def evaluate(self, context: StrategyContext) -> LearningIntervention:
        """Evaluate StrategyContext into LearningIntervention via StrategyEngine."""
        if not isinstance(context, StrategyContext):
            raise TypeError("context must be a StrategyContext")
        return self._engine.evaluate(context)

    def orchestrate(
        self,
        student_id: str,
        *,
        context: StrategyContext | None = None,
        runtime_a: Mapping[str, Any] | Any | None = None,
        twin: Mapping[str, Any] | Any | None = None,
        adaptive: Mapping[str, Any] | Any | None = None,
        intervention_kinds: tuple[str, ...] | None = None,
        include_explanation: bool = True,
        shadow: bool = False,
        as_of: str | None = None,
    ) -> StrategyResult:
        """Produce LearningIntervention behind the Learning Strategy contract.

        ``shadow=True`` is accepted for interface stability. S1 never writes
        Runtime A, Twin, Adaptive, or Experience state.
        """
        sid = (student_id or "").strip()
        if not sid:
            return StrategyResult(
                ok=False,
                error_code="INVALID_STATE",
                message="student_id must be a non-empty string",
            )
        if context is not None and not isinstance(context, StrategyContext):
            return StrategyResult(
                ok=False,
                error_code="INVALID_STATE",
                message="context must be a StrategyContext or None",
            )
        _ = (include_explanation, shadow)
        try:
            bundle = context
            if bundle is None:
                bundle = self._assembler.assemble(
                    sid,
                    as_of=as_of,
                    runtime_a=runtime_a,
                    twin=twin,
                    adaptive=adaptive,
                    intervention_kinds=intervention_kinds,
                )
            elif bundle.student_id != sid:
                return StrategyResult(
                    ok=False,
                    error_code="INVALID_STATE",
                    message="context.student_id must match student_id",
                )
            return StrategyResult(ok=True, value=self.evaluate(bundle))
        except StrategyValidationError as exc:
            return StrategyResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )
        except (TypeError, ValueError) as exc:
            return StrategyResult(
                ok=False,
                error_code="INVALID_STATE",
                message=str(exc),
            )


def empty_learning_intervention(
    *,
    context: StrategyContext | None = None,
    input_summary: str = "",
) -> LearningIntervention:
    """Build a structurally complete empty LearningIntervention (fallback stub)."""
    resolved = context
    return LearningIntervention(
        intervention_id="",
        strategy_version=STRATEGY_VERSION_S0,
        adaptive_recommendation_ref=(
            "" if resolved is None else resolved.adaptive_recommendation_ref
        ),
        twin_ref="" if resolved is None else resolved.twin_ref,
        runtime_a_evidence_ref=(
            "" if resolved is None else resolved.runtime_a_evidence_ref
        ),
        educational_objective="",
        explanation=StrategyExplanationPlaceholder(
            why_summary="No strategy orchestration computed.",
            input_summary=input_summary,
            limitations_codes=("empty_authentic",),
            limitations_summary="Empty authentic intervention — no primary kind.",
        ),
        provenance=StrategyProvenancePlaceholder(
            source_service="strategy_engine",
            source_entity="LearningIntervention",
            collected_at=None if resolved is None else resolved.as_of,
            availability=AVAILABILITY_UNAVAILABLE,
            unavailable_reason="empty_authentic",
            kind="strategy_derived",
        ),
        kind="",
        steps=(),
        authority=AUTHORITY_STRATEGY_ENGINE,
        limitations=("empty_authentic",),
    )


def build_strategy_engine_adapter(
    *,
    enabled: bool,
) -> StrategyEngineAdapter | None:
    """DI helper — construct StrategyEngineAdapter only when the flag is on."""
    if not enabled:
        return None
    engine = build_strategy_engine(enabled=True)
    assembler = build_strategy_context_assembler(enabled=True)
    return StrategyEngineAdapter(engine=engine, assembler=assembler)

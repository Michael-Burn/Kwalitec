"""Adaptive Engine Adapter — A0/A1/A2 contract surface.

Implements AdaptiveDecisionContract / AdaptiveEngineBridge. A2 may inject an
AdaptiveEngineExecutor for deterministic evaluate(). Shadow execution is
orchestrated separately and never wires outputs into Experience.
"""

from __future__ import annotations

from typing import Any

from app.infrastructure.adapters.adaptive_engine.contracts import (
    AUTHORITY_ADAPTIVE_ENGINE,
    AdaptiveDecisionResult,
    AdaptiveInputBundle,
    AdaptiveOutputBundle,
    ConfidencePlaceholder,
    ExplanationBundle,
    RecommendationPlaceholder,
)


class AdaptiveEngineAdapter:
    """Adaptive Engine Adapter — contracts + optional assembler / executor.

    When an executor is present, ``evaluate`` / ``decide`` produce deterministic
    AdaptiveOutputBundles. Experience AdaptiveDecisionPort cutover is handled by
    AdaptiveExperiencePortRouter (A4) behind Engine + Shadow + Authority flags.
    """

    ADAPTER_ID = "adaptive_engine"
    ADAPTER_VERSION = "0.2.0-a2"

    def __init__(
        self,
        *,
        input_assembler: Any | None = None,
        executor: Any | None = None,
    ) -> None:
        self._available = True
        self._input_assembler = input_assembler
        self._executor = executor

    @property
    def adapter_id(self) -> str:
        return self.ADAPTER_ID

    @property
    def adapter_version(self) -> str:
        return self.ADAPTER_VERSION

    @property
    def input_assembler(self) -> Any | None:
        return self._input_assembler

    @property
    def executor(self) -> Any | None:
        return self._executor

    def is_available(self) -> bool:
        return self._available

    def evaluate(self, inputs: AdaptiveInputBundle) -> AdaptiveOutputBundle:
        """Evaluate AdaptiveInputBundle via executor when wired; else empty stub."""
        if not isinstance(inputs, AdaptiveInputBundle):
            raise TypeError("inputs must be an AdaptiveInputBundle")
        if self._executor is not None:
            return self._executor.evaluate(inputs)
        return empty_adaptive_output(
            input_summary=(
                f"student_id={inputs.student_id}; contracts-only (no executor)"
            )
        )

    def decide(
        self,
        student_id: str,
        *,
        inputs: AdaptiveInputBundle | None = None,
        decision_kinds: tuple[str, ...] | None = None,
        include_explanation: bool = True,
        shadow: bool = False,
    ) -> AdaptiveDecisionResult:
        """Produce AdaptiveOutputBundle behind the Adaptive Decision contract.

        ``shadow=True`` is accepted for interface stability. A2 shadow telemetry
        and discard semantics live on AdaptiveShadowOrchestrator.execute_shadow;
        this method never writes Runtime A or Experience state.
        """
        sid = (student_id or "").strip()
        if not sid:
            return AdaptiveDecisionResult(
                ok=False,
                error_code="INVALID_STATE",
                message="student_id must be a non-empty string",
            )
        bundle = inputs
        if bundle is None and self._input_assembler is not None and shadow:
            bundle = self._input_assembler.assemble(sid)
        bundle = bundle or AdaptiveInputBundle(student_id=sid)
        if bundle.student_id != sid:
            return AdaptiveDecisionResult(
                ok=False,
                error_code="INVALID_STATE",
                message="inputs.student_id must match student_id",
            )
        _ = (decision_kinds, include_explanation, shadow)
        output = self.evaluate(bundle)
        return AdaptiveDecisionResult(ok=True, value=output)


def empty_adaptive_output(*, input_summary: str = "") -> AdaptiveOutputBundle:
    """Build a structurally complete empty AdaptiveOutputBundle."""
    return AdaptiveOutputBundle(
        recommendation=RecommendationPlaceholder(),
        confidence=ConfidencePlaceholder(),
        explanation=ExplanationBundle(
            input_summary=input_summary,
            confidence=ConfidencePlaceholder(),
            recommendation_rationale="No adaptive compute (empty contract stub).",
            why_summary="No adaptive decision computed.",
            inputs_used=(),
            inputs_unavailable=(),
        ),
        decision_id="",
        authority=AUTHORITY_ADAPTIVE_ENGINE,
    )


def build_adaptive_engine_adapter(
    *,
    enabled: bool,
    input_assembler: Any | None = None,
    executor: Any | None = None,
) -> AdaptiveEngineAdapter | None:
    """DI helper — construct AdaptiveEngineAdapter only when the flag is on."""
    if not enabled:
        return None
    return AdaptiveEngineAdapter(
        input_assembler=input_assembler,
        executor=executor,
    )

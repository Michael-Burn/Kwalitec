"""Educational Reasoning Engine — deterministic educational inference pipeline.

Observation
  → Retrieve Supporting Curriculum Evidence  (application stage)
  → Apply Educational Rules                  (this engine + registry)
  → Generate Educational Inference
  → Update Student Digital Twin              (application stage)
  → Record Reasoning History                 (application stage)

No UI, missions, tutoring, or LLM dependencies.
"""

from __future__ import annotations

import uuid
from dataclasses import replace
from datetime import UTC, datetime

from app.domain.educational_reasoning.decision import EducationalDecision
from app.domain.educational_reasoning.explanation import Explanation
from app.domain.educational_reasoning.reasoning_context import ReasoningContext
from app.domain.educational_reasoning.reasoning_result import ReasoningResult
from app.domain.educational_reasoning.rule_registry import (
    RuleRegistry,
    build_default_registry,
)
from app.domain.student_digital_twin.confidence import (
    ConfidenceState,
    confidence_band_from_score,
)
from app.domain.student_digital_twin.learning_state import LearningState
from app.domain.student_digital_twin.mastery import MasteryMap

ENGINE_VERSION = "sdt002.reasoning_engine_v1"


class EducationalReasoningEngine:
    """Apply educational rules via the registry to produce explainable inferences.

    Curriculum evidence must already be attached to ``ReasoningContext`` —
    the engine never retrieves curriculum data itself (keeps domain pure).
    """

    def __init__(self, registry: RuleRegistry | None = None) -> None:
        self._registry = registry or build_default_registry()

    @property
    def registry(self) -> RuleRegistry:
        return self._registry

    def reason(self, context: ReasoningContext) -> ReasoningResult:
        """Execute the educational rule pipeline for one reasoning cycle."""
        run_id = f"err-{uuid.uuid4().hex[:16]}"
        executions, final = self._registry.execute(context)

        mastery = final.effective_mastery
        if not isinstance(mastery, MasteryMap):
            mastery = MasteryMap.empty()

        confidence = final.confidence or ConfidenceState(
            score=0.0,
            band=confidence_band_from_score(0.0),
            evidence_count=0,
            reason="no_confidence_rule_output",
            updated_at=context.computed_at,
        )

        snapshot_id = ""
        for ex in executions:
            if ex.rule_code == "readiness_contribution":
                snapshot_id = str(ex.outputs.get("snapshot_id") or "")
                break
        if not snapshot_id:
            snapshot_id = f"lss-{uuid.uuid4().hex[:12]}"

        learning_state = LearningState(
            knowledge=final.knowledge if final.knowledge is not None else 0.0,
            confidence=confidence.score,
            retention=final.retention if final.retention is not None else 0.0,
            consistency=final.consistency if final.consistency is not None else 0.0,
            momentum=final.momentum if final.momentum is not None else 0.0,
            exam_readiness=(
                final.exam_readiness if final.exam_readiness is not None else 0.0
            ),
            snapshot_id=snapshot_id,
            computed_at=context.computed_at,
            evidence_count=len(context.observations),
            reason="educational_reasoning_engine_v1",
        )

        decisions: list[EducationalDecision] = []
        explanations: list[Explanation] = []
        for ex in executions:
            for decision in ex.decisions:
                # Namespace by run so decision_id remains unique across cycles.
                decisions.append(
                    replace(decision, decision_id=f"{run_id}:{decision.decision_id}")
                )
            explanations.append(ex.explanation)

        summary = (
            f"Engine {ENGINE_VERSION}: mastery={len(mastery.records)} "
            f"gaps={len(final.gaps)} recommendations={len(final.recommendations)} "
            f"readiness={learning_state.exam_readiness:.3f} "
            f"rules={len(executions)}"
        )

        return ReasoningResult(
            run_id=run_id,
            twin_id=context.twin_id,
            triggered_by=context.triggered_by,
            observation_ids=context.observation_ids,
            curriculum_evidence=context.curriculum_evidence,
            executions=executions,
            decisions=tuple(decisions),
            explanations=tuple(explanations),
            mastery=mastery,
            confidence=confidence,
            learning_state=learning_state,
            gaps=final.gaps,
            recommendations=final.recommendations,
            summary=summary,
            created_at=context.computed_at or datetime.now(UTC).replace(tzinfo=None),
            engine_version=ENGINE_VERSION,
            final_context=final,
        )

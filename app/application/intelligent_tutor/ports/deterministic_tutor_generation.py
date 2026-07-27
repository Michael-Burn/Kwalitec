"""Deterministic Version 1 TutorGenerationPort — no LLM."""

from __future__ import annotations

from app.application.intelligent_tutor.ports.tutor_generation_port import (
    TutorGenerationPort,
    TutorGenerationRequest,
    TutorGenerationResult,
)


class DeterministicTutorGeneration(TutorGenerationPort):
    """Placeholder generator that renders blueprint fields deterministically.

    Future LLM adapters must preserve the same contract: explain assembled
    evidence; never invent Twin / Reasoning / Graph decisions.
    """

    BACKEND = "deterministic_placeholder"
    MODEL = "tutor001.deterministic_v1"

    @property
    def backend_name(self) -> str:
        return self.BACKEND

    def generate(self, request: TutorGenerationRequest) -> TutorGenerationResult:
        bp = request.blueprint
        ctx = request.context
        q = request.question

        sections: list[str] = [
            f"You asked: {q.text.strip()}",
            "",
            bp.explanation.summary,
            bp.explanation.detail,
        ]

        if bp.evidence_summaries:
            sections.append("")
            sections.append("Supporting evidence:")
            for idx, summary in enumerate(bp.evidence_summaries[:6], start=1):
                sections.append(f"{idx}. {summary}")

        if bp.related_concepts:
            sections.append("")
            sections.append(
                "Related concepts: " + ", ".join(bp.related_concepts)
            )

        if bp.recovery_guidance:
            sections.append("")
            sections.append(f"Recovery guidance: {bp.recovery_guidance}")

        sections.append("")
        sections.append(f"Suggested next action: {bp.suggested_next_action}")
        sections.append(f"Reflection: {bp.reflection_prompt}")

        if ctx.reasoning_run_id:
            sections.append("")
            sections.append(
                f"(Grounded in educational reasoning run {ctx.reasoning_run_id})"
            )

        body = "\n".join(sections).strip()
        return TutorGenerationResult(
            body=body,
            backend=self.BACKEND,
            model_name=self.MODEL,
        )

"""TutorGenerationPort — abstract response prose generation.

The Tutor architecture depends on this port so a future LLM adapter can
replace the Version 1 deterministic placeholder without changing domain or
orchestration boundaries.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass

from app.domain.intelligent_tutor.response_builder import ResponseBlueprint
from app.domain.intelligent_tutor.tutor_context import TutorContext
from app.domain.intelligent_tutor.tutor_question import TutorQuestion


@dataclass(frozen=True)
class TutorGenerationRequest:
    """Inputs for Tutor prose generation."""

    question: TutorQuestion
    context: TutorContext
    blueprint: ResponseBlueprint


@dataclass(frozen=True)
class TutorGenerationResult:
    """Prose output from a TutorGenerationPort implementation."""

    body: str
    backend: str
    model_name: str = ""


class TutorGenerationPort(ABC):
    """Produce Tutor response prose from an evidence-backed blueprint.

    Implementations must not invent educational decisions. They may only
    render explanations already structured in the ResponseBlueprint /
    TutorContext.
    """

    @property
    @abstractmethod
    def backend_name(self) -> str:
        """Stable backend identifier (e.g. deterministic_placeholder)."""

    @abstractmethod
    def generate(self, request: TutorGenerationRequest) -> TutorGenerationResult:
        """Generate response body text from assembled educational structure."""

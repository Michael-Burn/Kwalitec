"""PB-002 F6 — Reflection accepts substance-backed published package copy."""

from __future__ import annotations

import pytest

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    reset_educational_package_cache,
)
from app.domain.session_experience.reflection_projection import (
    ReflectionProjection,
    is_reflection_safe,
)


def setup_function() -> None:
    reset_educational_package_cache()


def _runtime_shaped_copy(topic: str, lead: str = "") -> tuple[str, str, str, str]:
    insight = f"You worked through reading, examples, and practice on {topic}."
    confidence = (
        f"Growing comfort with {lead}" if lead else f"Growing comfort with {topic}"
    )
    improvement = (
        f"Revisit the learning objective that still feels unclear in {topic}."
    )
    prompt = (
        f"After reading, examples, and practice on {topic}, "
        "what still feels unclear — and what will you try next?"
    )
    return insight, confidence, improvement, prompt


@pytest.mark.parametrize(
    "pack",
    EducationalPackageLoader().all_approved(),
    ids=lambda p: p.package_id,
)
def test_published_package_reflection_projection_accepts_runtime_copy(pack) -> None:
    """Every live package topic must survive ReflectionProjection.create (F6)."""
    topic = pack.topic_title or pack.display_title or pack.topic_code
    lead = (pack.learning_objective or pack.concept_focus or topic)[:120]
    insight, confidence, improvement, prompt = _runtime_shaped_copy(topic, lead)
    pack_prompt = pack.reflection_prompt or pack.reflection_framing or prompt
    assert is_reflection_safe(insight)
    assert is_reflection_safe(confidence)
    assert is_reflection_safe(improvement)
    assert is_reflection_safe(pack_prompt)
    ReflectionProjection.create(
        "sess-pb002-f6",
        key_insight=insight,
        concept_confidence=confidence,
        suggested_improvement=improvement,
        reflection_prompt=pack_prompt,
        topic_title=topic,
    )

"""PB-002 F7 — honest withhold; no LO-shell for CS1 without package."""

from __future__ import annotations

from app.application.educational_packages.guard import (
    certified_guidance_enforced,
    reset_certified_guidance_cache,
    withhold_message,
)
from app.application.educational_packages.loader import reset_educational_package_cache
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)


def setup_function() -> None:
    reset_educational_package_cache()
    reset_certified_guidance_cache()


def test_cs1_enforces_certified_guidance() -> None:
    assert certified_guidance_enforced("CS1")
    assert not certified_guidance_enforced("SR2U1")
    assert not certified_guidance_enforced("")


def test_substance_planner_withholds_cs1_4_1() -> None:
    substance = EducationalSubstancePlanner().plan_for_topic(
        curriculum_identity="CS1:2026",
        topic_id="node-missing-4-1",
        topic_title="4.1 Explain the concepts of linear regression",
    )
    assert substance is None


def test_substance_planner_serves_cs1_4_2_package() -> None:
    substance = EducationalSubstancePlanner().plan_for_topic(
        curriculum_identity="CS1:2026",
        topic_id="node-4ca5aa5dab83f318",
        topic_title="4.2 Understand and use generalised linear models",
    )
    assert substance is not None
    assert substance.source == "educational_package"
    reading = substance.activities[0]
    assert "Learning objectives for this session:" not in reading.body
    assert "CMP" in reading.body or "GLM" in reading.body


def test_withhold_message_names_topic_and_cmp() -> None:
    msg = withhold_message(topic_code="4.1")
    assert "4.1" in msg
    assert "CMP" in msg
    assert "certified" in msg.lower()

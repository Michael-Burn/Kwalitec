"""EA-006 — Educational Package Publication tests."""

from __future__ import annotations

from app.application.educational_authoring.composition import compose_mission
from app.application.educational_authoring.dto import AuthoringContext
from app.application.educational_packages.loader import (
    find_educational_package,
    reset_educational_package_cache,
)
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.application.learning_session.substance_planner import (
    EducationalSubstancePlanner,
)


def setup_function() -> None:
    reset_educational_package_cache()


def test_golden_package_loads_and_is_approved() -> None:
    """RO-002: topic 4.2 resolves to Delta CD-D6 (EA-006 orphan superseded)."""
    pack = find_educational_package(topic_code="4.2", subject_id="CS1")
    assert pack is not None
    assert pack.is_publication_approved
    assert pack.package_id == "CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY"
    assert pack.campaign_day == "CD-D6"
    assert pack.display_title == "Place GLM responses in the exponential family"
    assert pack.reading.exit_line
    assert len(pack.knowledge_checks) == 2
    assert pack.tomorrow.next_topic_code == "4.2"
    assert "Today's topic" not in pack.reading.lead_line
    assert "placeholder" not in pack.mission_narrative.lower()


def test_package_resolves_by_title_keywords() -> None:
    """Code+subject remains the authoritative resolve path for multi-day 4.2."""
    pack = find_educational_package(topic_code="4.2", subject_id="CS1")
    assert pack is not None
    assert pack.topic_code == "4.2"
    assert pack.campaign_day == "CD-D6"
    assert "exponential" in " ".join(pack.topic_title_keywords).lower() or (
        "glm" in " ".join(pack.topic_title_keywords).lower()
    )


def test_package_resolves_by_alias() -> None:
    pack = find_educational_package(topic_id="CS1-D-T02")
    assert pack is not None
    assert pack.topic_code == "4.2"


def test_package_does_not_match_unrelated_topic() -> None:
    # Unpublished adjacent LO (6.1) — code-only control (title keywords are soft).
    pack = find_educational_package(topic_code="6.1", subject_id="CS1")
    assert pack is None


def test_topic_4_1_resolves_to_delta_entry() -> None:
    """RO-002 — CS1-003 activates 4.1 at CD-D1 (Trust Front)."""
    pack = find_educational_package(
        topic_code="4.1",
        subject_id="CS1",
    )
    assert pack is not None
    assert pack.package_id == "CS1-EP001-PKG-4.1-RESPONSE-EXPLANATORY"
    assert pack.campaign_day == "CD-D1"


def test_ep001_opening_package_is_live_approved() -> None:
    pack = find_educational_package(
        topic_code="1.1",
        topic_title="1.1 Describe the purpose and function of data analysis",
        subject_id="CS1",
    )
    assert pack is not None
    assert pack.is_publication_approved
    assert pack.package_id == "CS1-EP001-PKG-1.1-PURPOSE-FUNCTION"
    assert "Purpose of this reading" in pack.reading.lead_line
    assert "CMP" in pack.reading.exit_line


def test_shared_topic_code_prefers_campaign_day_order() -> None:
    """Shared topic_code 1.2 / 2.1: first-match follows live filename day order."""
    pack_12 = find_educational_package(topic_code="1.2", subject_id="CS1")
    assert pack_12 is not None
    assert pack_12.package_id == "CS1-EP001-PKG-1.2-EDA-SUMMARIES"
    pack_21 = find_educational_package(topic_code="2.1", subject_id="CS1")
    assert pack_21 is not None
    assert pack_21.package_id == "CS1-CS1002-PKG-2.1-DISCRETE"


def test_substance_from_package_is_complete_arc() -> None:
    pack = find_educational_package(topic_code="4.2")
    assert pack is not None
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:2026",
        topic_id="node-4ca5aa5dab83f318",
    )
    assert substance.source == "educational_package"
    assert substance.topic_title == pack.topic_title
    assert "Today's topic" not in substance.topic_title
    stages = [a.stage for a in substance.activities]
    assert EducationalStage.READ in stages
    assert EducationalStage.WORKED_EXAMPLE in stages
    assert EducationalStage.PRACTICE in stages
    assert any("CMP" in a.body or "GLM" in a.body for a in substance.activities)
    practice = [a for a in substance.activities if a.stage is EducationalStage.PRACTICE]
    assert len(practice) == 2
    assert all(a.scoreable is not None for a in practice)
    assert "exponential" in practice[0].prompt.lower() or "GLM" in practice[0].prompt


def test_substance_planner_prefers_certified_package() -> None:
    substance = EducationalSubstancePlanner().plan_for_topic(
        curriculum_identity="",
        topic_id="node-4ca5aa5dab83f318",
        topic_title="4.2 Understand and use generalised linear models",
        educational_rationale="ignored when package present",
    )
    assert substance is not None
    assert substance.source == "educational_package"
    assert substance.topic_code == "4.2"
    reading = substance.activities[0]
    assert "Today's topic" not in reading.prompt
    assert "GLM" in reading.body or "exponential" in reading.body.lower()


def test_composition_uses_package_voice_and_tomorrow() -> None:
    # RO1-R1: shared topic_code 4.2 is multi-day — bind package id (CD-D6).
    composition = compose_mission(
        AuthoringContext(
            topic_id="node-4ca5aa5dab83f318",
            topic_title="Understand and use generalised linear models",
            topic_code="4.2",
            subject_code="CS1",
            educational_package_id="CS1-EP001-PKG-4.2-EXPONENTIAL-FAMILY",
            tomorrow_topic_title="Something else",
        )
    )
    assert composition.has_composition
    narrative = composition.mission_narrative
    assert (
        "exponential" in narrative.lower()
        or "GLM" in narrative
        or "glm" in narrative.lower()
        or "family" in narrative.lower()
    )
    assert composition.tomorrow_preview is not None
    # CD-D6 multi-day: next sitting remains topic 4.2 (mean/variance 4.2.2).
    assert composition.tomorrow_preview.topic_code == "4.2"
    assert "mean" in composition.tomorrow_preview.continuity_line.lower() or (
        "4.2.2" in (composition.tomorrow_preview.topic_title or "")
    )
    reflection = composition.reflection_prompt
    assert reflection
    assert (
        "4.2.1" in reflection
        or "CMP" in reflection
        or "stickiest" in reflection.lower()
    )
    episode = composition.episodes[0]
    assert episode.learning_objective
    assert (
        "exponential" in episode.learning_objective.lower()
        or "GLM" in episode.learning_objective
        or "generalised" in episode.learning_objective.lower()
    )

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
    pack = find_educational_package(topic_code="4.2", subject_id="CS1")
    assert pack is not None
    assert pack.is_publication_approved
    assert pack.package_id == "CS1-EA005-PKG-4.2-GLM-STRUCTURE"
    assert pack.display_title == "Extend linear models into GLM structure"
    assert pack.reading.exit_line
    assert len(pack.knowledge_checks) == 2
    assert pack.tomorrow.next_topic_code == "5.1"
    assert "Today's topic" not in pack.reading.lead_line
    assert "placeholder" not in pack.mission_narrative.lower()


def test_package_resolves_by_title_keywords() -> None:
    pack = find_educational_package(
        topic_title="Study 4.2 — Understand and use generalised linear models"
    )
    assert pack is not None
    assert pack.topic_code == "4.2"


def test_package_resolves_by_alias() -> None:
    pack = find_educational_package(topic_id="CS1-D-T02")
    assert pack is not None
    assert pack.topic_code == "4.2"


def test_package_does_not_match_unrelated_topic() -> None:
    pack = find_educational_package(
        topic_code="1.1",
        topic_title="Describe the principles of actuarial modelling",
        subject_id="CS1",
    )
    assert pack is None


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
    composition = compose_mission(
        AuthoringContext(
            topic_id="node-4ca5aa5dab83f318",
            topic_title="Understand and use generalised linear models",
            topic_code="4.2",
            subject_code="CS1",
            tomorrow_topic_title="Something else",
        )
    )
    assert composition.has_composition
    assert "linear models" in composition.mission_narrative.lower()
    narrative = composition.mission_narrative
    assert (
        "GLM" in narrative
        or "glm" in narrative.lower()
        or "link" in narrative.lower()
    )
    assert composition.tomorrow_preview is not None
    assert composition.tomorrow_preview.topic_code == "5.1"
    assert "Bayesian" in composition.tomorrow_preview.topic_title or "bayesian" in (
        composition.tomorrow_preview.continuity_line.lower()
    )
    reflection = composition.reflection_prompt
    assert (
        "family" in reflection.lower()
        or "η" in reflection
        or "link" in reflection.lower()
    )
    episode = composition.episodes[0]
    assert episode.learning_objective
    assert (
        "GLM" in episode.learning_objective
        or "generalised" in episode.learning_objective.lower()
    )

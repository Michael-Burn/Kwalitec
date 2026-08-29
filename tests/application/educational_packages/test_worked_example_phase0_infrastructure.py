"""Phase 0 — Real Worked Examples infrastructure.

Proves package JSON → loader → substance → content presentation wiring.
One live pilot (Bayes screening on CS1016 Memory Front) carries the field;
remaining live inventory keeps the structure-walkthrough scaffold.
"""

from __future__ import annotations

from pathlib import Path

from app.application.educational_packages.loader import (
    EducationalPackageLoader,
    find_package_by_id,
    reset_educational_package_cache,
)
from app.application.educational_packages.models import ReadingGuidance
from app.application.educational_packages.substance import substance_from_package
from app.application.learning_session.educational_flow import EducationalStage
from app.presentation.session.content_sections import (
    parse_session_content_body,
    present_worked_example_content,
)

FIXTURE_ROOT = Path("tests/fixtures/worked_example_phase0_packages")
LIVE_PACKAGE_ROOT = Path("app/curriculum/data/educational_packages")
PILOT_PACKAGE_ID = "CS1-EP001-PKG-CP-5.1-BAYES-THEOREM"


def setup_function() -> None:
    reset_educational_package_cache()


def _load_reference_package():
    loader = EducationalPackageLoader(root=FIXTURE_ROOT)
    packs = loader.all_approved()
    assert len(packs) == 1
    pack = packs[0]
    assert pack.package_id == "CS1-RWE-PHASE0-REF"
    return pack


def test_loader_reads_worked_example_round_trip() -> None:
    pack = _load_reference_package()
    example = pack.worked_example
    assert example is not None
    assert example.title == "Screening test — Bayes update"
    assert "P(D) = 0.01" in example.problem_statement
    assert [g.symbol for g in example.given] == [
        "P(D)",
        "P(+|D)",
        "P(+|not D)",
        "P(not D)",
    ]
    assert example.given[0].value == "0.01"
    assert len(example.steps) == 2
    assert example.steps[0].id == "S1"
    assert example.steps[0].result == "0.1085"
    assert example.steps[1].id == "S2"
    assert example.steps[1].result == "≈ 0.0876"
    assert "0.1085" in example.final_answer
    assert "0.0876" in example.final_answer
    assert example.syllabus_ref == "5.1.1"
    # Dead cue must stay unloaded (ReadingGuidance has no worked_examples_cue).
    assert not hasattr(ReadingGuidance, "worked_examples_cue")
    assert not hasattr(pack.reading, "worked_examples_cue")


def test_substance_renders_genuine_numeric_walkthrough() -> None:
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:rwe-phase0",
        topic_id="RWE-PHASE0-REF",
    )
    examples = [
        a for a in substance.activities if a.stage is EducationalStage.WORKED_EXAMPLE
    ]
    assert len(examples) == 1
    example = examples[0]
    assert example.title == "Screening test — Bayes update"
    assert "0.1085" in example.body
    assert "0.0876" in example.body
    assert "Worked solution" in example.body
    assert "Confirm your structure sketch" not in example.body
    assert "Pause-point harvest" not in example.body
    assert dict(example.metadata).get("worked_example_kind") == "numeric"
    assert example.hints[0].startswith("S1:")


def test_presentation_splits_attempt_primary_from_solution_more() -> None:
    pack = _load_reference_package()
    substance = substance_from_package(
        pack,
        curriculum_identity="CS1:rwe-phase0",
        topic_id="RWE-PHASE0-REF",
    )
    example = next(
        a for a in substance.activities if a.stage is EducationalStage.WORKED_EXAMPLE
    )
    sections = parse_session_content_body(example.body)
    assert sections
    presented = present_worked_example_content(sections)
    assert "P(D) = 0.01" in presented.intro_line
    primary_labels = {s.label for s in presented.primary}
    more_labels = {s.label for s in presented.more}
    assert "Given values" in primary_labels
    assert "Attempt before reveal" in primary_labels
    assert any(label.startswith("Worked solution") for label in more_labels)
    assert "Final answer" in more_labels
    assert "Common pitfall" in more_labels
    more_text = "\n".join(
        "\n".join((*s.paragraphs, *s.bullets)) for s in presented.more
    )
    assert "0.1085" in more_text
    assert "0.0876" in more_text


def test_package_without_worked_example_keeps_structure_scaffold() -> None:
    reset_educational_package_cache()
    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    scaffold_pack = None
    for pack in loader.all_approved():
        if pack.package_id == PILOT_PACKAGE_ID:
            continue
        if pack.worked_example is None or not pack.worked_example.steps:
            scaffold_pack = pack
            break
    assert scaffold_pack is not None
    substance = substance_from_package(
        scaffold_pack,
        curriculum_identity="CS1:scaffold",
        topic_id=scaffold_pack.topic_code,
    )
    example = next(
        a for a in substance.activities if a.stage is EducationalStage.WORKED_EXAMPLE
    )
    assert example.title == "Structure walkthrough: Family → η → link"
    assert "Confirm your structure sketch" in example.body
    assert "Pause-point harvest" in example.body
    assert dict(example.metadata).get("worked_example_kind") == "scaffold"


def test_live_pilot_loads_and_inventory_gate() -> None:
    reset_educational_package_cache()
    pilot = find_package_by_id(PILOT_PACKAGE_ID)
    assert pilot is not None
    assert pilot.worked_example is not None
    assert len(pilot.worked_example.steps) == 3
    assert pilot.worked_example.steps[0].result == "P(Alert) = 0.1428"
    assert pilot.worked_example.steps[1].result == "P(Breach|Alert) ≈ 0.1849"

    substance = substance_from_package(
        pilot,
        curriculum_identity="CS1:bayes-pilot",
        topic_id=pilot.topic_code,
    )
    example = next(
        a for a in substance.activities if a.stage is EducationalStage.WORKED_EXAMPLE
    )
    assert example.title == "Bayes update for a cyber-breach alert"
    assert "0.1428" in example.body
    assert "Confirm your structure sketch" not in example.body

    loader = EducationalPackageLoader(root=LIVE_PACKAGE_ROOT)
    with_real = sorted(
        p.package_id
        for p in loader.all_approved()
        if p.worked_example is not None and p.worked_example.steps
    )
    # Phase 0 pilot slot (Bayes on CS1016, content replaced in RWE Batch 3)
    # + RWE Batch 1 (Section 3: 22) + RWE Batch 2 (Continuity: 24)
    # + RWE Batch 3 (Pi/Rho Memory-Publication: 14 new packages; pilot replaced in place)
    # + RWE Batch 4 (Delta Domain F1b / cs1003: 24).
    assert PILOT_PACKAGE_ID in with_real
    assert len(with_real) == 85

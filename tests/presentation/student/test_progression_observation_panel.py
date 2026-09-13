"""Learner observation panel: locked copy, structure, and noise discipline."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.progression_readiness import (
    CS1_A_T01_LO01,
    CS1_A_T01_LO03,
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
    InsufficientReason,
    ProgressionReadiness,
    evaluate,
)
from app.presentation.student.services.progression_observation_presenter import (
    BRAND_HEADING,
    has_meaningful_evidence,
    panels_for_topic,
    translate_result,
)


def _when(offset: int = 0) -> datetime:
    return datetime(2026, 9, 13, 8, 0, 0, tzinfo=UTC) + timedelta(seconds=offset)


def _record(
    *,
    student_id: str,
    objective_id: str,
    item_id: str,
    scored_correct: bool | None,
    offset: int = 0,
) -> AssessmentEvidenceRecord:
    return AssessmentEvidenceRecord(
        evidence_id=str(uuid4()),
        student_id=student_id,
        objective_id=objective_id,
        item_id=item_id,
        package_id="test-package",
        session_id="test-session",
        response_type="mcq",
        scored_correct=scored_correct,
        occurred_at=_when(offset),
        source="test",
    )


def _outcomes(contract, student_id: str, scores: list[bool | None]):
    rows = []
    for i, (spec, scored) in enumerate(
        zip(contract.evidence_items, scores, strict=True)
    ):
        rows.append(
            _record(
                student_id=student_id,
                objective_id=contract.objective_id,
                item_id=spec.item_id,
                scored_correct=scored,
                offset=i,
            )
        )
    return rows


class TestNoiseDiscipline:
    def test_no_panel_without_attempted_tagged_items(self):
        assert has_meaningful_evidence(CS1_A_T01_LO01, []) is False
        panels = panels_for_topic(
            topic_id="CS1-A-T01",
            student_id="s1",
            evidence=[],
        )
        assert panels == ()

    def test_no_panel_when_evidence_is_for_other_items_only(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id="CS1-A-T01-LO01",
                item_id="unrelated-item",
                scored_correct=True,
            )
        ]
        panels = panels_for_topic(
            topic_id="CS1-A-T01",
            student_id="s1",
            evidence=evidence,
        )
        assert panels == ()


class TestLockedScenarioCopy:
    def test_ready_scenario_structure_and_language(self):
        evidence = _outcomes(CS1_A_T01_LO01, "s1", [True, True, False])
        result = evaluate(
            CS1_A_T01_LO01.objective_id, "s1", CS1_A_T01_LO01, evidence
        )
        assert result.readiness is ProgressionReadiness.READY
        panel = translate_result(
            contract=CS1_A_T01_LO01,
            readiness=result.readiness,
            reason=result.reason,
            evidence=evidence,
        )
        assert panel.brand_heading == BRAND_HEADING
        assert panel.scenario_heading == "Sufficient evidence to move forward"
        assert panel.evidence_lines == ("Correct", "Correct", "Incorrect")
        assert "2 of the 3 independent questions" in panel.body_paragraphs[0]
        assert "progression requirement" in panel.meaning_paragraphs[0]
        assert "not a permanent measure of mastery" in panel.meaning_paragraphs[0]
        assert "can change" in panel.keep_in_mind
        assert "READY" not in panel.scenario_heading
        assert "READY" not in "".join(panel.body_paragraphs)
        assert "READY" not in "".join(panel.meaning_paragraphs)

    def test_insufficient_sample_scenario(self):
        # 1 of 3 correct with all items scored → INSUFFICIENT_SAMPLE
        evidence = _outcomes(CS1_A_T01_LO01, "s1", [True, False, False])
        result = evaluate(
            CS1_A_T01_LO01.objective_id, "s1", CS1_A_T01_LO01, evidence
        )
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE
        panel = translate_result(
            contract=CS1_A_T01_LO01,
            readiness=result.readiness,
            reason=result.reason,
            evidence=evidence,
        )
        assert panel.brand_heading == BRAND_HEADING
        assert panel.scenario_heading == "More evidence needed"
        assert panel.evidence_lines == ("Correct", "Incorrect", "Incorrect")
        assert "not enough to make a reliable progression judgment" in (
            panel.body_paragraphs[0]
        )
        assert "another independent assessment" in panel.next_step
        assert "INSUFFICIENT" not in panel.scenario_heading
        assert "INSUFFICIENT_SAMPLE" not in panel.body_paragraphs[0]

    def test_prerequisite_unverified_scenario(self):
        # Strong own mixed evidence, no prereq → Scenario 3
        own = [
            _record(
                student_id="s1",
                objective_id=CS1_B_T03_LO01.objective_id,
                item_id=CS1_B_T03_LO01.evidence_items[0].item_id,
                scored_correct=True,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_B_T03_LO01.objective_id,
                item_id=CS1_B_T03_LO01.evidence_items[1].item_id,
                scored_correct=True,
                offset=1,
            ),
        ]
        result = evaluate(
            CS1_B_T03_LO01.objective_id, "s1", CS1_B_T03_LO01, own
        )
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert (
            result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED
        )
        panel = translate_result(
            contract=CS1_B_T03_LO01,
            readiness=result.readiness,
            reason=result.reason,
            evidence=own,
        )
        assert panel.scenario_heading == "More evidence needed"
        assert "prerequisite concept" in panel.body_paragraphs[0]
        assert "not treating this result as confirmation" in panel.body_paragraphs[1]
        assert "REQUIRED_PREREQUISITE" not in "".join(panel.body_paragraphs)

    def test_not_ready_scenario_uses_plain_component_language(self):
        # Mixed LO02: MCQ correct, numeric incorrect → NOT_READY
        evidence = [
            _record(
                student_id="s1",
                objective_id=CS1_B_T03_LO02.objective_id,
                item_id=CS1_B_T03_LO02.evidence_items[0].item_id,
                scored_correct=True,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_B_T03_LO02.objective_id,
                item_id=CS1_B_T03_LO02.evidence_items[1].item_id,
                scored_correct=False,
                offset=1,
            ),
        ]
        result = evaluate(
            CS1_B_T03_LO02.objective_id, "s1", CS1_B_T03_LO02, evidence
        )
        assert result.readiness is ProgressionReadiness.NOT_READY
        panel = translate_result(
            contract=CS1_B_T03_LO02,
            readiness=result.readiness,
            reason=result.reason,
            evidence=evidence,
        )
        assert panel.scenario_heading == "More work recommended"
        assert "calculation component" in panel.body_paragraphs[1]
        assert "MCQ" not in "".join(panel.body_paragraphs)
        assert "numeric" not in "".join(panel.body_paragraphs).lower()
        assert "NOT_READY" not in panel.scenario_heading
        assert "Review the explanation" in panel.next_step

    def test_not_ready_conceptual_uses_conceptual_component(self):
        evidence = _outcomes(CS1_A_T01_LO03, "s1", [False, False])
        result = evaluate(
            CS1_A_T01_LO03.objective_id, "s1", CS1_A_T01_LO03, evidence
        )
        assert result.readiness is ProgressionReadiness.NOT_READY
        panel = translate_result(
            contract=CS1_A_T01_LO03,
            readiness=result.readiness,
            reason=result.reason,
            evidence=evidence,
        )
        assert "conceptual component" in panel.body_paragraphs[1]

    def test_panels_for_topic_attaches_only_when_meaningful(self):
        ready = _outcomes(CS1_A_T01_LO01, "s1", [True, True, True])
        panels = panels_for_topic(
            topic_id="CS1-A-T01", student_id="s1", evidence=ready
        )
        assert len(panels) == 1
        assert panels[0].objective_id == "CS1-A-T01-LO01"
        assert panels[0].brand_heading == BRAND_HEADING
        # Other LOs on the topic have no evidence → no panels for them
        assert all(p.objective_id == "CS1-A-T01-LO01" for p in panels)

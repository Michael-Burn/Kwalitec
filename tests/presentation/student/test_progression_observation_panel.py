"""Learner observation panel: locked copy, structure, and noise discipline."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.progression_readiness import (
    CS1_A_T01_LO01,
    CS1_A_T01_LO03,
    CS1_A_T02_LO01,
    CS1_B_T01_LO03,
    CS1_B_T01_LO04,
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
    CS1_C_T01_LO03,
    CS1_C_T02_LO01,
    CS1_D_T01_LO01,
    CS1_E_T01_LO01,
    PROGRESSION_READINESS_CONTRACTS,
    InsufficientReason,
    ProgressionReadiness,
    evaluate,
    get_contract,
)
from app.presentation.student.services.progression_observation_presenter import (
    _OBJECTIVE_LABELS,
    BRAND_HEADING,
    OBSERVATION_TOPIC_OBJECTIVES,
    _syllabus_code_label,
    has_meaningful_evidence,
    panels_by_topic_for_student,
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
        evidence = _outcomes(CS1_A_T01_LO03, "s1", [False, False, False])
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


# Catalogue-derived activation: every contracted topic, not the original 2 only.
_EXPECTED_CATALOGUE_TOPICS = (
    "CS1-A-T01",
    "CS1-A-T02",
    "CS1-B-T01",
    "CS1-B-T02",
    "CS1-B-T03",
    "CS1-B-T04",
    "CS1-B-T05",
    "CS1-B-T06",
    "CS1-C-T01",
    "CS1-C-T02",
    "CS1-C-T03",
    "CS1-D-T01",
    "CS1-D-T02",
    "CS1-E-T01",
)


class TestFullCatalogueObservationScope:
    def test_observation_scope_matches_all_catalogue_topics_and_objectives(self):
        catalogue_topics = {
            oid.rsplit("-LO", 1)[0] for oid in PROGRESSION_READINESS_CONTRACTS
        }
        assert set(OBSERVATION_TOPIC_OBJECTIVES) == catalogue_topics
        assert tuple(OBSERVATION_TOPIC_OBJECTIVES) == _EXPECTED_CATALOGUE_TOPICS
        assert len(PROGRESSION_READINESS_CONTRACTS) == 72
        activated = {
            oid
            for oids in OBSERVATION_TOPIC_OBJECTIVES.values()
            for oid in oids
        }
        assert activated == set(PROGRESSION_READINESS_CONTRACTS)
        for topic_id, oids in OBSERVATION_TOPIC_OBJECTIVES.items():
            assert oids == tuple(
                oid
                for oid in PROGRESSION_READINESS_CONTRACTS
                if oid.startswith(f"{topic_id}-LO")
            )

    def test_syllabus_labels_cover_all_contracts(self):
        assert set(_OBJECTIVE_LABELS) == set(PROGRESSION_READINESS_CONTRACTS)
        assert _OBJECTIVE_LABELS["CS1-A-T01-LO01"] == "1.1.1"
        assert _OBJECTIVE_LABELS["CS1-B-T03-LO02"] == "2.3.2"
        assert _OBJECTIVE_LABELS["CS1-A-T02-LO01"] == "1.2.1"
        assert _OBJECTIVE_LABELS["CS1-B-T01-LO03"] == "2.1.3"
        assert _OBJECTIVE_LABELS["CS1-D-T02-LO10"] == "4.2.10"
        assert _OBJECTIVE_LABELS["CS1-E-T01-LO09"] == "5.1.9"
        assert _syllabus_code_label("CS1-C-T02-LO08") == "3.2.8"

    def test_panels_render_across_previously_excluded_topics(self):
        """Seed one objective on each newly activated section/topic shape."""
        samples = (
            (CS1_A_T02_LO01, [True, True, True, False]),  # 4-item conceptual
            (CS1_B_T01_LO04, [True, True]),  # ordinary 2-item conceptual
            (CS1_C_T01_LO03, [True, True]),
            (CS1_C_T02_LO01, [True, True]),
            (CS1_D_T01_LO01, [True, True]),
            (CS1_E_T01_LO01, [True, True]),  # single-pair mixed
        )
        evidence = []
        for contract, scores in samples:
            evidence.extend(_outcomes(contract, "full-scope", scores))

        # Dual-pair conflicting demonstrations (pair A READY, pair B NOT_READY)
        dual = CS1_B_T01_LO03
        pair_a, pair_b = dual.demonstration_pairs
        evidence.extend(
            [
                _record(
                    student_id="full-scope",
                    objective_id=dual.objective_id,
                    item_id=pair_a.mcq_item_id,
                    scored_correct=True,
                    offset=100,
                ),
                _record(
                    student_id="full-scope",
                    objective_id=dual.objective_id,
                    item_id=pair_a.numeric_item_id,
                    scored_correct=True,
                    offset=101,
                ),
                _record(
                    student_id="full-scope",
                    objective_id=dual.objective_id,
                    item_id=pair_b.mcq_item_id,
                    scored_correct=True,
                    offset=102,
                ),
                _record(
                    student_id="full-scope",
                    objective_id=dual.objective_id,
                    item_id=pair_b.numeric_item_id,
                    scored_correct=False,
                    offset=103,
                ),
            ]
        )

        by_topic = {}
        for topic_id in (
            "CS1-A-T02",
            "CS1-B-T01",
            "CS1-C-T01",
            "CS1-C-T02",
            "CS1-D-T01",
            "CS1-E-T01",
        ):
            panels = panels_for_topic(
                topic_id=topic_id, student_id="full-scope", evidence=evidence
            )
            assert panels, f"expected panels for newly scoped topic {topic_id}"
            by_topic[topic_id] = panels
            for panel in panels:
                assert panel.brand_heading == BRAND_HEADING
                assert panel.scenario_heading in {
                    "Sufficient evidence to move forward",
                    "More evidence needed",
                    "More work recommended",
                }
                assert panel.objective_label == _OBJECTIVE_LABELS[panel.objective_id]
                assert panel.evidence_lines
                # Locked 4-part structure fields always present on the view
                assert isinstance(panel.body_paragraphs, tuple)
                assert isinstance(panel.meaning_paragraphs, tuple)
                assert isinstance(panel.next_step, str)
                assert isinstance(panel.keep_in_mind, str)

        four_item = next(
            p
            for p in by_topic["CS1-A-T02"]
            if p.objective_id == "CS1-A-T02-LO01"
        )
        assert four_item.scenario_heading == "Sufficient evidence to move forward"
        assert "3 of the 4 independent questions" in four_item.body_paragraphs[0]
        assert four_item.objective_label == "1.2.1"

        dual_panel = next(
            p
            for p in by_topic["CS1-B-T01"]
            if p.objective_id == "CS1-B-T01-LO03"
        )
        assert dual_panel.scenario_heading == "More evidence needed"
        assert "not enough to make a reliable progression judgment" in (
            dual_panel.body_paragraphs[0]
        )
        assert dual_panel.objective_label == "2.1.3"

        mixed = next(
            p
            for p in by_topic["CS1-E-T01"]
            if p.objective_id == "CS1-E-T01-LO01"
        )
        assert mixed.scenario_heading == "Sufficient evidence to move forward"
        assert mixed.objective_label == "5.1.1"

    def test_noise_gating_holds_across_full_catalogue_with_empty_evidence(self):
        for topic_id in OBSERVATION_TOPIC_OBJECTIVES:
            assert (
                panels_for_topic(
                    topic_id=topic_id, student_id="quiet", evidence=[]
                )
                == ()
            )
        assert panels_by_topic_for_student(student_id="quiet") == {}

    def test_noise_gating_ignores_unrelated_items_on_new_topics(self):
        evidence = [
            _record(
                student_id="s-noise",
                objective_id="CS1-A-T02-LO01",
                item_id="unrelated-item",
                scored_correct=True,
            ),
            _record(
                student_id="s-noise",
                objective_id="CS1-B-T01-LO03",
                item_id="another-unrelated",
                scored_correct=False,
            ),
        ]
        assert panels_for_topic(
            topic_id="CS1-A-T02", student_id="s-noise", evidence=evidence
        ) == ()
        assert panels_for_topic(
            topic_id="CS1-B-T01", student_id="s-noise", evidence=evidence
        ) == ()
        # Contract lookup still succeeds; gating is evidence-based only.
        assert get_contract("CS1-A-T02-LO01") is CS1_A_T02_LO01
        assert get_contract("CS1-B-T01-LO03") is CS1_B_T01_LO03

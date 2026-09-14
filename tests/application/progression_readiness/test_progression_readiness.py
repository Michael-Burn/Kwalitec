"""Golden scenarios for Progression Readiness (seventy-two real contracts).

Standalone: no live student-facing wiring. Proves locked outcome matrices,
prerequisite both states, unscored filtering, critical override capability,
and read-only OEA access.
"""

from __future__ import annotations

import ast
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

import pytest

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import ObjectiveAssessmentEvidenceStore
from app.application.progression_readiness import (
    CS1_A_T01_LO01,
    CS1_A_T01_LO02,
    CS1_A_T01_LO03,
    CS1_A_T01_LO04,
    CS1_A_T02_LO01,
    CS1_A_T02_LO02,
    CS1_A_T02_LO03,
    CS1_B_T01_LO01,
    CS1_B_T01_LO02,
    CS1_B_T01_LO03,
    CS1_B_T01_LO04,
    CS1_B_T01_LO05,
    CS1_B_T01_LO06,
    CS1_B_T02_LO01,
    CS1_B_T02_LO02,
    CS1_B_T02_LO03,
    CS1_B_T02_LO04,
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
    CS1_B_T04_LO01,
    CS1_B_T04_LO02,
    CS1_B_T05_LO01,
    CS1_B_T05_LO02,
    CS1_B_T06_LO01,
    CS1_B_T06_LO02,
    CS1_B_T06_LO03,
    CS1_B_T06_LO04,
    CS1_B_T06_LO05,
    CS1_B_T06_LO06,
    CS1_C_T01_LO01,
    CS1_C_T01_LO02,
    CS1_C_T01_LO03,
    CS1_C_T01_LO04,
    CS1_C_T01_LO05,
    CS1_C_T01_LO06,
    CS1_C_T02_LO01,
    CS1_C_T02_LO02,
    CS1_C_T02_LO03,
    CS1_C_T02_LO04,
    CS1_C_T02_LO05,
    CS1_C_T02_LO06,
    CS1_C_T02_LO07,
    CS1_C_T02_LO08,
    CS1_C_T03_LO01,
    CS1_C_T03_LO02,
    CS1_C_T03_LO03,
    CS1_C_T03_LO04,
    CS1_C_T03_LO05,
    CS1_D_T01_LO01,
    CS1_D_T01_LO02,
    CS1_D_T01_LO03,
    CS1_D_T01_LO04,
    CS1_D_T01_LO05,
    CS1_D_T02_LO01,
    CS1_D_T02_LO02,
    CS1_D_T02_LO03,
    CS1_D_T02_LO04,
    CS1_D_T02_LO05,
    CS1_D_T02_LO06,
    CS1_D_T02_LO07,
    CS1_D_T02_LO08,
    CS1_D_T02_LO09,
    CS1_D_T02_LO10,
    CS1_E_T01_LO01,
    CS1_E_T01_LO02,
    CS1_E_T01_LO03,
    CS1_E_T01_LO04,
    CS1_E_T01_LO05,
    CS1_E_T01_LO06,
    CS1_E_T01_LO07,
    CS1_E_T01_LO08,
    CS1_E_T01_LO09,
    PREREQUISITE_JOINT_DISTRIBUTION_LO,
    PROGRESSION_READINESS_CONTRACTS,
    ContractKind,
    InsufficientReason,
    ProgressionReadiness,
    ProgressionReadinessContract,
    evaluate,
    evaluate_from_store,
    get_contract,
)
from app.infrastructure.session.store import SessionDocumentStore

PKG = Path("app/application/progression_readiness")
FORBIDDEN_IMPORT_PREFIXES = (
    "app.application.student_twin",
    "app.application.student_digital_twin",
    "app.domain.student_twin",
    "app.domain.student_digital_twin",
    "app.application.spacing_scheduler",
    "app.domain.spacing_scheduler",
    "app.application.adaptive_decision",
    "app.domain.decision",
)


def _when(offset_seconds: int = 0) -> datetime:
    return datetime(2026, 9, 12, 12, 0, 0, tzinfo=UTC) + timedelta(
        seconds=offset_seconds
    )


def _record(
    *,
    student_id: str,
    objective_id: str,
    item_id: str,
    scored_correct: bool | None,
    offset: int = 0,
    misconception: str = "",
    response_type: str = "mcq",
) -> AssessmentEvidenceRecord:
    return AssessmentEvidenceRecord(
        evidence_id=str(uuid4()),
        student_id=student_id,
        objective_id=objective_id,
        item_id=item_id,
        package_id="test-package",
        session_id="test-session",
        response_type=response_type,
        scored_correct=scored_correct,
        occurred_at=_when(offset),
        source="test",
        selected_misconception_tag=misconception,
    )


def _evidence_for_items(
    student_id: str,
    objective_id: str,
    item_outcomes: list[tuple[str, bool | None]],
    *,
    response_type: str = "mcq",
) -> list[AssessmentEvidenceRecord]:
    rows: list[AssessmentEvidenceRecord] = []
    for i, (item_id, scored) in enumerate(item_outcomes):
        rows.append(
            _record(
                student_id=student_id,
                objective_id=objective_id,
                item_id=item_id,
                scored_correct=scored,
                offset=i,
                response_type=response_type,
            )
        )
    return rows


def _eval(contract: ProgressionReadinessContract, evidence, student_id="s1"):
    return evaluate(contract.objective_id, student_id, contract, evidence)


# ---------------------------------------------------------------------------
# Catalogue shape
# ---------------------------------------------------------------------------


class TestCatalogue:
    def test_seventy_two_real_contracts_present(self):
        assert set(PROGRESSION_READINESS_CONTRACTS) == {
            "CS1-A-T01-LO01",
            "CS1-A-T01-LO02",
            "CS1-A-T01-LO03",
            "CS1-A-T01-LO04",
            "CS1-A-T02-LO01",
            "CS1-A-T02-LO02",
            "CS1-A-T02-LO03",
            "CS1-B-T01-LO01",
            "CS1-B-T01-LO02",
            "CS1-B-T01-LO03",
            "CS1-B-T01-LO04",
            "CS1-B-T01-LO05",
            "CS1-B-T01-LO06",
            "CS1-B-T02-LO01",
            "CS1-B-T02-LO02",
            "CS1-B-T02-LO03",
            "CS1-B-T02-LO04",
            "CS1-B-T03-LO01",
            "CS1-B-T03-LO02",
            "CS1-B-T04-LO01",
            "CS1-B-T04-LO02",
            "CS1-B-T05-LO01",
            "CS1-B-T05-LO02",
            "CS1-B-T06-LO01",
            "CS1-B-T06-LO02",
            "CS1-B-T06-LO03",
            "CS1-B-T06-LO04",
            "CS1-B-T06-LO05",
            "CS1-B-T06-LO06",
            "CS1-C-T01-LO01",
            "CS1-C-T01-LO02",
            "CS1-C-T01-LO03",
            "CS1-C-T01-LO04",
            "CS1-C-T01-LO05",
            "CS1-C-T01-LO06",
            "CS1-C-T02-LO01",
            "CS1-C-T02-LO02",
            "CS1-C-T02-LO03",
            "CS1-C-T02-LO04",
            "CS1-C-T02-LO05",
            "CS1-C-T02-LO06",
            "CS1-C-T02-LO07",
            "CS1-C-T02-LO08",
            "CS1-C-T03-LO01",
            "CS1-C-T03-LO02",
            "CS1-C-T03-LO03",
            "CS1-C-T03-LO04",
            "CS1-C-T03-LO05",
            "CS1-D-T01-LO01",
            "CS1-D-T01-LO02",
            "CS1-D-T01-LO03",
            "CS1-D-T01-LO04",
            "CS1-D-T01-LO05",
            "CS1-D-T02-LO01",
            "CS1-D-T02-LO02",
            "CS1-D-T02-LO03",
            "CS1-D-T02-LO04",
            "CS1-D-T02-LO05",
            "CS1-D-T02-LO06",
            "CS1-D-T02-LO07",
            "CS1-D-T02-LO08",
            "CS1-D-T02-LO09",
            "CS1-D-T02-LO10",
            "CS1-E-T01-LO01",
            "CS1-E-T01-LO02",
            "CS1-E-T01-LO03",
            "CS1-E-T01-LO04",
            "CS1-E-T01-LO05",
            "CS1-E-T01-LO06",
            "CS1-E-T01-LO07",
            "CS1-E-T01-LO08",
            "CS1-E-T01-LO09",
        }

    def test_topic_1_1_item_counts_match_live_freeze(self):
        assert CS1_A_T01_LO01.item_count == 3
        assert CS1_A_T01_LO02.item_count == 3
        assert CS1_A_T01_LO03.item_count == 3
        assert CS1_A_T01_LO04.item_count == 3
        assert CS1_A_T01_LO01.ready_min_correct == 2
        assert CS1_A_T01_LO03.ready_min_correct == 2
        assert CS1_A_T01_LO04.ready_min_correct == 2

    def test_topic_1_2_item_counts_match_live_freeze(self):
        assert CS1_A_T02_LO01.item_count == 4
        assert CS1_A_T02_LO02.item_count == 4
        assert CS1_A_T02_LO03.item_count == 4
        assert CS1_A_T02_LO01.ready_min_correct == 3
        assert CS1_A_T02_LO02.ready_min_correct == 3
        assert CS1_A_T02_LO03.ready_min_correct == 3
        assert CS1_A_T02_LO01.required_prerequisite_objective_id is None
        assert CS1_A_T02_LO02.required_prerequisite_objective_id is None
        assert CS1_A_T02_LO03.required_prerequisite_objective_id is None

    def test_live_item_ids(self):
        assert CS1_A_T01_LO01.item_ids == frozenset(
            {
                "cs1017-1.1.1-ar-01",
                "cs1017-1.1.1-cp-01",
                "ep001-1.1-ar-01",
            }
        )
        assert CS1_A_T01_LO03.item_ids == frozenset(
            {
                "cs1017-1.1.3-ar-01",
                "cs1017-1.1.3-ar-02",
                "cs1017-1.1.3-cp-01",
            }
        )
        assert CS1_A_T01_LO04.item_ids == frozenset(
            {
                "cs1017-1.1.4-ar-01",
                "cs1017-1.1.4-ar-02",
                "cs1017-1.1.4-cp-01",
            }
        )
        assert CS1_A_T02_LO01.item_ids == frozenset(
            {
                "ep001-1.2a-ar-01",
                "ep001-1.2a-cp-01",
                "cs1017-1.2.1-ar-01",
                "cs1017-1.2.1-cp-01",
            }
        )
        assert CS1_A_T02_LO02.item_ids == frozenset(
            {
                "ep001-1.2b-ar-01",
                "ep001-1.2b-cp-01",
                "cs1017-1.2.2-ar-01",
                "cs1017-1.2.2-cp-01",
            }
        )
        assert CS1_A_T02_LO03.item_ids == frozenset(
            {
                "cs1002-1.2c-ar-01",
                "cs1002-1.2c-cp-01",
                "cs1017-1.2.3-ar-01",
                "cs1017-1.2.3-cp-01",
            }
        )
        assert CS1_B_T03_LO01.required_prerequisite_objective_id == (
            PREREQUISITE_JOINT_DISTRIBUTION_LO
        )
        assert PREREQUISITE_JOINT_DISTRIBUTION_LO == "CS1-B-T02-LO01"
        assert CS1_B_T03_LO02.required_prerequisite_objective_id is None

    def test_no_critical_tags_on_live_contracts(self):
        for contract in PROGRESSION_READINESS_CONTRACTS.values():
            assert contract.critical_misconception_tags == frozenset()

    def test_topic_2_1_contracts_match_approved_shapes(self):
        assert CS1_B_T01_LO01.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T01_LO01.item_count == 4
        assert CS1_B_T01_LO01.ready_min_correct == 3
        assert CS1_B_T01_LO01.required_prerequisite_objective_id is None
        assert CS1_B_T01_LO01.item_ids == frozenset(
            {
                "cs1002-2.1a-ar-01",
                "cs1002-2.1a-cp-01",
                "cs1017-2.1.1-ar-01",
                "cs1017-2.1.1-cp-01",
            }
        )

        assert CS1_B_T01_LO02.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T01_LO02.item_count == 4
        assert CS1_B_T01_LO02.ready_min_correct == 3
        assert CS1_B_T01_LO02.item_ids == frozenset(
            {
                "cs1002-2.1b-ar-01",
                "cs1002-2.1b-cp-01",
                "cs1017-2.1.2-ar-01",
                "cs1017-2.1.2-cp-01",
            }
        )

        assert CS1_B_T01_LO03.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION
        assert CS1_B_T01_LO03.item_count == 4
        assert len(CS1_B_T01_LO03.demonstration_pairs) == 2
        pair_a, pair_b = CS1_B_T01_LO03.demonstration_pairs
        assert pair_a.mcq_item_id == "cs1004-2.1c-ar-01"
        assert pair_a.numeric_item_id == "cs1004-2.1c-cp-01"
        assert pair_b.mcq_item_id == "cs1016-2.1.3-ar-01"
        assert pair_b.numeric_item_id == "cs1016-2.1.3-cp-01"
        assert CS1_B_T01_LO03.required_prerequisite_objective_id is None

        for contract in (CS1_B_T01_LO04, CS1_B_T01_LO05, CS1_B_T01_LO06):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 3
            assert contract.ready_min_correct == 2
            assert contract.required_prerequisite_objective_id is None

        assert CS1_B_T01_LO04.item_ids == frozenset(
            {
                "cs1004-2.1d-ar-01",
                "cs1004-2.1d-ar-02",
                "cs1004-2.1d-cp-01",
            }
        )
        assert CS1_B_T01_LO05.item_ids == frozenset(
            {
                "cs1004-2.1e-ar-01",
                "cs1004-2.1e-ar-02",
                "cs1004-2.1e-cp-01",
            }
        )
        assert CS1_B_T01_LO06.item_ids == frozenset(
            {
                "cs1004-2.1f-ar-01",
                "cs1004-2.1f-ar-02",
                "cs1004-2.1f-cp-01",
            }
        )

    def test_topic_2_2_contracts_match_approved_shapes(self):
        assert CS1_B_T02_LO01.kind is ContractKind.MIXED_MODALITY
        assert CS1_B_T02_LO01.item_ids == frozenset(
            {"cs1005-2.2.1-ar-01", "cs1005-2.2.1-cp-01"}
        )
        assert "cs1016-2.2.1-ar-01" not in CS1_B_T02_LO01.item_ids
        assert "cs1016-2.2.1-cp-01" not in CS1_B_T02_LO01.item_ids
        assert CS1_B_T02_LO01.required_prerequisite_objective_id is None

        assert CS1_B_T02_LO02.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T02_LO02.item_count == 3
        assert CS1_B_T02_LO02.ready_min_correct == 2
        assert CS1_B_T02_LO02.item_ids == frozenset(
            {
                "cs1005-2.2.2-ar-01",
                "cs1005-2.2.2-ar-02",
                "cs1005-2.2.2-cp-01",
            }
        )
        assert CS1_B_T02_LO02.required_prerequisite_objective_id is None

        assert CS1_B_T02_LO03.kind is ContractKind.MIXED_MODALITY
        assert CS1_B_T02_LO03.item_ids == frozenset(
            {"cs1005-2.2.3-ar-01", "cs1005-2.2.3-cp-01"}
        )
        assert CS1_B_T02_LO03.required_prerequisite_objective_id is None

        assert CS1_B_T02_LO04.kind is ContractKind.MIXED_MODALITY
        assert CS1_B_T02_LO04.item_ids == frozenset(
            {"cs1005-2.2.4-ar-01", "cs1005-2.2.4-cp-01"}
        )
        assert CS1_B_T02_LO04.required_prerequisite_objective_id is None

    def test_topic_2_4_contracts_match_approved_shapes(self):
        assert CS1_B_T04_LO01.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T04_LO01.item_count == 3
        assert CS1_B_T04_LO01.ready_min_correct == 2
        assert CS1_B_T04_LO01.item_ids == frozenset(
            {
                "cs1007-2.4.1-ar-01",
                "cs1007-2.4.1-ar-02",
                "cs1007-2.4.1-cp-01",
            }
        )
        assert CS1_B_T04_LO01.required_prerequisite_objective_id is None

        assert CS1_B_T04_LO02.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T04_LO02.item_count == 3
        assert CS1_B_T04_LO02.ready_min_correct == 2
        assert CS1_B_T04_LO02.item_ids == frozenset(
            {
                "cs1007-2.4.2-ar-01",
                "cs1007-2.4.2-ar-02",
                "cs1007-2.4.2-cp-01",
            }
        )
        assert CS1_B_T04_LO02.required_prerequisite_objective_id is None

    def test_topic_2_5_contracts_match_approved_shapes(self):
        assert CS1_B_T05_LO01.kind is ContractKind.MIXED_MODALITY
        assert CS1_B_T05_LO01.item_ids == frozenset(
            {"cs1008-2.5.1-ar-01", "cs1008-2.5.1-cp-01"}
        )
        assert "cs1016-2.5.1-ar-01" not in CS1_B_T05_LO01.item_ids
        assert "cs1016-2.5.1-cp-01" not in CS1_B_T05_LO01.item_ids
        assert CS1_B_T05_LO01.required_prerequisite_objective_id is None

        assert CS1_B_T05_LO02.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T05_LO02.item_count == 2
        assert CS1_B_T05_LO02.ready_min_correct == 2
        assert CS1_B_T05_LO02.item_ids == frozenset(
            {"cs1008-2.5.2-ar-01", "cs1008-2.5.2-cp-01"}
        )
        assert CS1_B_T05_LO02.required_prerequisite_objective_id is None

    def test_topic_2_6_contracts_match_approved_shapes(self):
        assert CS1_B_T06_LO01.kind is ContractKind.CONCEPTUAL
        assert CS1_B_T06_LO01.item_count == 2
        assert CS1_B_T06_LO01.ready_min_correct == 2
        assert CS1_B_T06_LO01.item_ids == frozenset(
            {"cs1009-2.6.1-ar-01", "cs1009-2.6.1-cp-01"}
        )
        assert "cs1016-2.6.1-ar-01" not in CS1_B_T06_LO01.item_ids
        assert "cs1016-2.6.1-cp-01" not in CS1_B_T06_LO01.item_ids
        assert CS1_B_T06_LO01.required_prerequisite_objective_id is None

        for contract, ar, cp in (
            (CS1_B_T06_LO02, "cs1009-2.6.2-ar-01", "cs1009-2.6.2-cp-01"),
            (CS1_B_T06_LO03, "cs1009-2.6.3-ar-01", "cs1009-2.6.3-cp-01"),
            (CS1_B_T06_LO04, "cs1009-2.6.4-ar-01", "cs1009-2.6.4-cp-01"),
            (CS1_B_T06_LO05, "cs1009-2.6.5-ar-01", "cs1009-2.6.5-cp-01"),
            (CS1_B_T06_LO06, "cs1009-2.6.6-ar-01", "cs1009-2.6.6-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None

    def test_topic_3_1_contracts_match_approved_shapes(self):
        assert CS1_C_T01_LO01.kind is ContractKind.MIXED_MODALITY
        assert CS1_C_T01_LO01.item_ids == frozenset(
            {"cs1010-3.1.1-ar-01", "cs1010-3.1.1-cp-01"}
        )
        assert "cs1016-3.1.1-ar-01" not in CS1_C_T01_LO01.item_ids
        assert "cs1016-3.1.1-cp-01" not in CS1_C_T01_LO01.item_ids
        assert CS1_C_T01_LO01.required_prerequisite_objective_id is None

        assert CS1_C_T01_LO02.kind is ContractKind.MIXED_MODALITY
        assert CS1_C_T01_LO02.item_ids == frozenset(
            {"cs1010-3.1.2-ar-01", "cs1010-3.1.2-cp-01"}
        )
        assert CS1_C_T01_LO02.required_prerequisite_objective_id is None

        for contract, ar, cp in (
            (CS1_C_T01_LO03, "cs1010-3.1.3-ar-01", "cs1010-3.1.3-cp-01"),
            (CS1_C_T01_LO04, "cs1010-3.1.4-ar-01", "cs1010-3.1.4-cp-01"),
            (CS1_C_T01_LO05, "cs1010-3.1.5-ar-01", "cs1010-3.1.5-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None

        assert CS1_C_T01_LO06.kind is ContractKind.MIXED_MODALITY
        assert CS1_C_T01_LO06.item_ids == frozenset(
            {"cs1010-3.1.6-ar-01", "cs1010-3.1.6-cp-01"}
        )
        assert CS1_C_T01_LO06.required_prerequisite_objective_id is None

    def test_topic_3_2_contracts_match_approved_shapes(self):
        assert "cs1016-3.2.1-ar-01" not in CS1_C_T02_LO01.item_ids
        assert "cs1016-3.2.1-cp-01" not in CS1_C_T02_LO01.item_ids
        for contract, ar, cp in (
            (CS1_C_T02_LO01, "cs1011-3.2.1-ar-01", "cs1011-3.2.1-cp-01"),
            (CS1_C_T02_LO02, "cs1011-3.2.2-ar-01", "cs1011-3.2.2-cp-01"),
            (CS1_C_T02_LO03, "cs1011-3.2.3-ar-01", "cs1011-3.2.3-cp-01"),
            (CS1_C_T02_LO04, "cs1011-3.2.4-ar-01", "cs1011-3.2.4-cp-01"),
            (CS1_C_T02_LO05, "cs1011-3.2.5-ar-01", "cs1011-3.2.5-cp-01"),
            (CS1_C_T02_LO06, "cs1011-3.2.6-ar-01", "cs1011-3.2.6-cp-01"),
            (CS1_C_T02_LO07, "cs1011-3.2.7-ar-01", "cs1011-3.2.7-cp-01"),
            (CS1_C_T02_LO08, "cs1011-3.2.8-ar-01", "cs1011-3.2.8-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None

    def test_topic_3_3_contracts_match_approved_shapes(self):
        assert "cs1016-3.3.1-ar-01" not in CS1_C_T03_LO01.item_ids
        assert "cs1016-3.3.1-cp-01" not in CS1_C_T03_LO01.item_ids
        for contract, ar, cp in (
            (CS1_C_T03_LO01, "cs1012-3.3.1-ar-01", "cs1012-3.3.1-cp-01"),
            (CS1_C_T03_LO02, "cs1012-3.3.2-ar-01", "cs1012-3.3.2-cp-01"),
            (CS1_C_T03_LO03, "cs1012-3.3.3-ar-01", "cs1012-3.3.3-cp-01"),
            (CS1_C_T03_LO04, "cs1012-3.3.4-ar-01", "cs1012-3.3.4-cp-01"),
            (CS1_C_T03_LO05, "cs1012-3.3.5-ar-01", "cs1012-3.3.5-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None

    def test_topic_4_1_contracts_match_approved_shapes(self):
        assert "cs1013-4.1.1-ar-01" not in CS1_D_T01_LO01.item_ids
        assert "cs1013-4.1.1-cp-01" not in CS1_D_T01_LO01.item_ids
        assert "cs1016-4.1.1-ar-01" not in CS1_D_T01_LO01.item_ids
        assert "cs1016-4.1.1-cp-01" not in CS1_D_T01_LO01.item_ids
        assert "cs1013-4.1.4-ar-01" not in CS1_D_T01_LO04.item_ids
        assert "cs1013-4.1.4-cp-01" not in CS1_D_T01_LO04.item_ids
        for contract, ar, cp in (
            (CS1_D_T01_LO01, "cs1003-4.1.1-ar-01", "cs1003-4.1.1-cp-01"),
            (CS1_D_T01_LO02, "cs1003-4.1.2-ar-01", "cs1003-4.1.2-cp-01"),
            (CS1_D_T01_LO03, "cs1003-4.1.3-ar-01", "cs1003-4.1.3-cp-01"),
            (CS1_D_T01_LO04, "cs1003-4.1.4-ar-01", "cs1003-4.1.4-cp-01"),
            (CS1_D_T01_LO05, "cs1003-4.1.5-ar-01", "cs1003-4.1.5-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None

    def test_topic_4_2_contracts_match_approved_shapes(self):
        for contract, ar, cp in (
            (CS1_D_T02_LO01, "cs1003-4.2.1-ar-01", "cs1003-4.2.1-cp-01"),
            (CS1_D_T02_LO02, "cs1003-4.2.2-ar-01", "cs1003-4.2.2-cp-01"),
            (CS1_D_T02_LO03, "cs1003-4.2.3-ar-01", "cs1003-4.2.3-cp-01"),
            (CS1_D_T02_LO04, "cs1003-4.2.4-ar-01", "cs1003-4.2.4-cp-01"),
            (CS1_D_T02_LO06, "cs1003-4.2.6-ar-01", "cs1003-4.2.6-cp-01"),
            (CS1_D_T02_LO07, "cs1003-4.2.7-ar-01", "cs1003-4.2.7-cp-01"),
            (CS1_D_T02_LO09, "cs1003-4.2.9-ar-01", "cs1003-4.2.9-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None
            twin_prefix = ar.replace("cs1003-", "cs1014-")
            twin_cp = cp.replace("cs1003-", "cs1014-")
            assert twin_prefix not in contract.item_ids
            assert twin_cp not in contract.item_ids

        assert CS1_D_T02_LO05.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION
        assert len(CS1_D_T02_LO05.demonstration_pairs) == 2
        assert CS1_D_T02_LO05.item_ids == frozenset(
            {
                "cs1003-4.2.5-ar-01",
                "cs1003-4.2.5-cp-01",
                "cs1014-4.2.5-ar-01",
                "cs1014-4.2.5-cp-01",
            }
        )
        assert CS1_D_T02_LO05.required_prerequisite_objective_id is None

        assert CS1_D_T02_LO10.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION
        assert len(CS1_D_T02_LO10.demonstration_pairs) == 2
        assert CS1_D_T02_LO10.item_ids == frozenset(
            {
                "cs1003-4.2.10-ar-01",
                "cs1003-4.2.10-cp-01",
                "cs1014-4.2.10-ar-01",
                "cs1014-4.2.10-cp-01",
            }
        )
        assert CS1_D_T02_LO10.required_prerequisite_objective_id is None

        assert CS1_D_T02_LO08.kind is ContractKind.MIXED_MODALITY
        assert CS1_D_T02_LO08.item_ids == frozenset(
            {"cs1003-4.2.8-ar-01", "cs1003-4.2.8-cp-01"}
        )
        assert "cs1014-4.2.8-ar-01" not in CS1_D_T02_LO08.item_ids
        assert "cs1014-4.2.8-cp-01" not in CS1_D_T02_LO08.item_ids
        assert CS1_D_T02_LO08.required_prerequisite_objective_id is None

    def test_topic_5_1_contracts_match_approved_shapes(self):
        for contract, ar, cp in (
            (CS1_E_T01_LO02, "cs1003-5.1.2-ar-01", "cs1003-5.1.2-cp-01"),
            (CS1_E_T01_LO03, "cs1003-5.1.3-ar-01", "cs1003-5.1.3-cp-01"),
            (CS1_E_T01_LO05, "cs1003-5.1.5-ar-01", "cs1003-5.1.5-cp-01"),
            (CS1_E_T01_LO09, "cs1003-5.1.9-ar-01", "cs1003-5.1.9-cp-01"),
        ):
            assert contract.kind is ContractKind.CONCEPTUAL
            assert contract.item_count == 2
            assert contract.ready_min_correct == 2
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None
            twin_ar = ar.replace("cs1003-", "cs1015-")
            twin_cp = cp.replace("cs1003-", "cs1015-")
            assert twin_ar not in contract.item_ids
            assert twin_cp not in contract.item_ids

        for contract, ar, cp in (
            (CS1_E_T01_LO04, "cs1003-5.1.4-ar-01", "cs1003-5.1.4-cp-01"),
            (CS1_E_T01_LO06, "cs1003-5.1.6-ar-01", "cs1003-5.1.6-cp-01"),
            (CS1_E_T01_LO08, "cs1003-5.1.8-ar-01", "cs1003-5.1.8-cp-01"),
        ):
            assert contract.kind is ContractKind.MIXED_MODALITY
            assert contract.item_ids == frozenset({ar, cp})
            assert contract.required_prerequisite_objective_id is None
            assert ar.replace("cs1003-", "cs1015-") not in contract.item_ids
            assert cp.replace("cs1003-", "cs1015-") not in contract.item_ids

        assert CS1_E_T01_LO01.kind is ContractKind.MIXED_MODALITY
        assert CS1_E_T01_LO01.item_ids == frozenset(
            {"cs1003-5.1.1-ar-01", "cs1016-5.1.1-cp-01"}
        )
        assert CS1_E_T01_LO01.required_prerequisite_objective_id is None
        assert "cs1003-5.1.1-cp-01" not in CS1_E_T01_LO01.item_ids
        assert "cs1015-5.1.1-ar-01" not in CS1_E_T01_LO01.item_ids
        assert "cs1015-5.1.1-cp-01" not in CS1_E_T01_LO01.item_ids
        assert "cs1016-5.1.1-ar-01" not in CS1_E_T01_LO01.item_ids

        assert CS1_E_T01_LO07.kind is ContractKind.MIXED_MODALITY_DUAL_DEMONSTRATION
        assert len(CS1_E_T01_LO07.demonstration_pairs) == 2
        assert CS1_E_T01_LO07.item_ids == frozenset(
            {
                "cs1003-5.1.7-ar-01",
                "cs1003-5.1.7-cp-01",
                "cs1015-5.1.7-ar-01",
                "cs1015-5.1.7-cp-01",
            }
        )
        assert CS1_E_T01_LO07.required_prerequisite_objective_id is None
        pair_a, pair_b = CS1_E_T01_LO07.demonstration_pairs
        assert pair_a.mcq_item_id == "cs1003-5.1.7-ar-01"
        assert pair_a.numeric_item_id == "cs1003-5.1.7-cp-01"
        assert pair_b.mcq_item_id == "cs1015-5.1.7-ar-01"
        assert pair_b.numeric_item_id == "cs1015-5.1.7-cp-01"

    def test_get_contract(self):
        assert get_contract("CS1-A-T01-LO01") is CS1_A_T01_LO01
        assert get_contract("CS1-A-T02-LO01") is CS1_A_T02_LO01
        assert get_contract("CS1-B-T01-LO03") is CS1_B_T01_LO03
        assert get_contract("CS1-B-T02-LO01") is CS1_B_T02_LO01
        assert get_contract("CS1-B-T02-LO04") is CS1_B_T02_LO04
        assert get_contract("CS1-B-T04-LO01") is CS1_B_T04_LO01
        assert get_contract("CS1-B-T04-LO02") is CS1_B_T04_LO02
        assert get_contract("CS1-B-T05-LO01") is CS1_B_T05_LO01
        assert get_contract("CS1-B-T05-LO02") is CS1_B_T05_LO02
        assert get_contract("CS1-B-T06-LO01") is CS1_B_T06_LO01
        assert get_contract("CS1-B-T06-LO06") is CS1_B_T06_LO06
        assert get_contract("CS1-C-T01-LO01") is CS1_C_T01_LO01
        assert get_contract("CS1-C-T01-LO06") is CS1_C_T01_LO06
        assert get_contract("CS1-C-T02-LO01") is CS1_C_T02_LO01
        assert get_contract("CS1-C-T02-LO08") is CS1_C_T02_LO08
        assert get_contract("CS1-C-T03-LO01") is CS1_C_T03_LO01
        assert get_contract("CS1-C-T03-LO05") is CS1_C_T03_LO05
        assert get_contract("CS1-D-T01-LO01") is CS1_D_T01_LO01
        assert get_contract("CS1-D-T01-LO05") is CS1_D_T01_LO05
        assert get_contract("CS1-D-T02-LO01") is CS1_D_T02_LO01
        assert get_contract("CS1-D-T02-LO05") is CS1_D_T02_LO05
        assert get_contract("CS1-D-T02-LO08") is CS1_D_T02_LO08
        assert get_contract("CS1-D-T02-LO10") is CS1_D_T02_LO10
        assert get_contract("CS1-E-T01-LO01") is CS1_E_T01_LO01
        assert get_contract("CS1-E-T01-LO07") is CS1_E_T01_LO07
        assert get_contract("CS1-E-T01-LO09") is CS1_E_T01_LO09
        assert get_contract("missing") is None


# ---------------------------------------------------------------------------
# Conceptual 3-item (LO01 / LO02)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_A_T01_LO01,
        CS1_A_T01_LO02,
        CS1_A_T01_LO03,
        CS1_A_T01_LO04,
        CS1_B_T01_LO04,
        CS1_B_T01_LO05,
        CS1_B_T01_LO06,
        CS1_B_T02_LO02,
        CS1_B_T04_LO01,
        CS1_B_T04_LO02,
    ],
)
class TestConceptualThreeItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_all_correct_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_two_of_three_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], True), (items[2], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY

    def test_one_of_three_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False), (items[2], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_three_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_sparse_partial_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(items[0], True)]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_empty_evidence_insufficient_sample(self, contract):
        result = _eval(contract, [])
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Fresh-second-attempt gap: miss original ar-01, still READY via ar-02 + cp-01
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract, missed_item, fresh_item, numeric_item",
    [
        (
            CS1_A_T01_LO03,
            "cs1017-1.1.3-ar-01",
            "cs1017-1.1.3-ar-02",
            "cs1017-1.1.3-cp-01",
        ),
        (
            CS1_A_T01_LO04,
            "cs1017-1.1.4-ar-01",
            "cs1017-1.1.4-ar-02",
            "cs1017-1.1.4-cp-01",
        ),
        (
            CS1_B_T01_LO04,
            "cs1004-2.1d-ar-01",
            "cs1004-2.1d-ar-02",
            "cs1004-2.1d-cp-01",
        ),
        (
            CS1_B_T01_LO06,
            "cs1004-2.1f-ar-01",
            "cs1004-2.1f-ar-02",
            "cs1004-2.1f-cp-01",
        ),
        (
            CS1_B_T02_LO02,
            "cs1005-2.2.2-ar-01",
            "cs1005-2.2.2-ar-02",
            "cs1005-2.2.2-cp-01",
        ),
        (
            CS1_B_T04_LO01,
            "cs1007-2.4.1-ar-01",
            "cs1007-2.4.1-ar-02",
            "cs1007-2.4.1-cp-01",
        ),
        (
            CS1_B_T04_LO02,
            "cs1007-2.4.2-ar-01",
            "cs1007-2.4.2-ar-02",
            "cs1007-2.4.2-cp-01",
        ),
    ],
)
class TestFreshSecondAttemptGapClosed:
    def test_ready_via_fresh_item_without_reattempting_missed_ar01(
        self, contract, missed_item, fresh_item, numeric_item
    ):
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (missed_item, False),
                (fresh_item, True),
                (numeric_item, True),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

        missed_rows = [row for row in evidence if row.item_id == missed_item]
        assert len(missed_rows) == 1
        assert missed_rows[0].scored_correct is False
        assert all(row.scored_correct is not True for row in missed_rows)
        attempted_ids = {row.item_id for row in evidence}
        assert missed_item in attempted_ids
        assert fresh_item in attempted_ids
        assert numeric_item in attempted_ids


# ---------------------------------------------------------------------------
# Conceptual 4-item (topic 1.2 LO01 / LO02 / LO03)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract", [CS1_A_T02_LO01, CS1_A_T02_LO02, CS1_A_T02_LO03]
)
class TestConceptualFourItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_all_correct_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_three_of_four_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], True),
                (items[2], True),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY

    def test_two_of_four_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], True),
                (items[2], False),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_one_of_four_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], False),
                (items[2], False),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_four_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_sparse_partial_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(items[0], True)]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_empty_evidence_insufficient_sample(self, contract):
        result = _eval(contract, [])
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Mixed modality LO02 (no prerequisite)
# ---------------------------------------------------------------------------


class TestMixedModalityLO02:
    mcq = "cs1006-2.3.2-ar-01"
    numeric = "cs1006-2.3.2-cp-01"
    contract = CS1_B_T03_LO02

    def _pair(self, mcq_ok: bool | None, numeric_ok: bool | None):
        rows = []
        if mcq_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                )
            )
        if numeric_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.numeric,
                    scored_correct=numeric_ok,
                    offset=1,
                    response_type="numeric",
                )
            )
        return rows

    def test_both_correct_ready(self):
        evidence = self._pair(True, True)
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(True, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(self):
        result = _eval(self.contract, self._pair(False, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(False, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_only_mcq_modality_not_observed(self):
        result = _eval(self.contract, self._pair(True, Ellipsis))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_only_numeric_modality_not_observed(self):
        result = _eval(self.contract, self._pair(Ellipsis, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED


# ---------------------------------------------------------------------------
# Mixed modality LO01 + prerequisite
# ---------------------------------------------------------------------------


class TestMixedModalityLO01Prerequisite:
    contract = CS1_B_T03_LO01
    mcq = "cs1006-2.3.1-ar-01"
    numeric = "cs1006-2.3.1-cp-01"

    def _own(self, mcq_ok: bool, numeric_ok: bool):
        return [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=mcq_ok,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=numeric_ok,
                offset=1,
                response_type="numeric",
            ),
        ]

    def _prereq(self, scored_correct: bool | None):
        return _record(
            student_id="s1",
            objective_id=PREREQUISITE_JOINT_DISTRIBUTION_LO,
            item_id="cs1005-2.2.1-ar-01",
            scored_correct=scored_correct,
            offset=10,
            response_type="mcq",
        )

    def test_strong_own_no_prereq_insufficient_never_ready(self):
        result = _eval(self.contract, self._own(True, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED

    def test_strong_own_prereq_incorrect_still_unverified(self):
        evidence = self._own(True, True) + [self._prereq(False)]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED

    def test_strong_own_prereq_unscored_still_unverified(self):
        evidence = self._own(True, True) + [self._prereq(None)]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED

    def test_strong_own_with_prereq_correct_ready(self):
        evidence = self._own(True, True) + [self._prereq(True)]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.READY

    def test_with_prereq_four_cells(self):
        prereq = self._prereq(True)
        cases = [
            (True, True, ProgressionReadiness.READY, None),
            (True, False, ProgressionReadiness.NOT_READY, None),
            (
                False,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
            ),
            (False, False, ProgressionReadiness.NOT_READY, None),
        ]
        for mcq_ok, num_ok, readiness, reason in cases:
            result = _eval(self.contract, self._own(mcq_ok, num_ok) + [prereq])
            assert result.readiness is readiness
            assert result.reason is reason


# ---------------------------------------------------------------------------
# Unscored filtering and critical override
# ---------------------------------------------------------------------------


class TestEvidenceFilteringAndCritical:
    def test_unscored_none_excluded_from_correct_and_incorrect(self):
        items = [spec.item_id for spec in CS1_A_T01_LO03.evidence_items]
        # One unscored, one correct → looks like sparse 1 correct, not 1/2 mix
        evidence = [
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[0],
                scored_correct=None,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[1],
                scored_correct=True,
                offset=1,
            ),
        ]
        result = _eval(CS1_A_T01_LO03, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_unscored_does_not_count_as_zero_of_two_not_ready(self):
        items = [spec.item_id for spec in CS1_A_T01_LO03.evidence_items]
        evidence = [
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[0],
                scored_correct=None,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[1],
                scored_correct=None,
                offset=1,
            ),
        ]
        result = _eval(CS1_A_T01_LO03, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_critical_misconception_forces_not_ready_despite_ready_count(self):
        items = [spec.item_id for spec in CS1_A_T01_LO01.evidence_items]
        contract = ProgressionReadinessContract(
            objective_id=CS1_A_T01_LO01.objective_id,
            kind=ContractKind.CONCEPTUAL,
            evidence_items=CS1_A_T01_LO01.evidence_items,
            ready_min_correct=2,
            critical_misconception_tags=frozenset({"critical_demo_tag"}),
        )
        evidence = [
            _record(
                student_id="s1",
                objective_id=contract.objective_id,
                item_id=items[0],
                scored_correct=True,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=contract.objective_id,
                item_id=items[1],
                scored_correct=True,
                offset=1,
            ),
            _record(
                student_id="s1",
                objective_id=contract.objective_id,
                item_id=items[2],
                scored_correct=False,
                offset=2,
                misconception="critical_demo_tag",
            ),
        ]
        # Without critical: 2/3 READY. With critical tag: NOT_READY.
        assert (
            _eval(CS1_A_T01_LO01, evidence).readiness is ProgressionReadiness.READY
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_latest_scored_per_item_wins(self):
        items = [spec.item_id for spec in CS1_A_T01_LO03.evidence_items]
        evidence = [
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[0],
                scored_correct=False,
                offset=0,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[0],
                scored_correct=True,
                offset=5,
            ),
            _record(
                student_id="s1",
                objective_id=CS1_A_T01_LO03.objective_id,
                item_id=items[1],
                scored_correct=True,
                offset=6,
            ),
        ]
        assert _eval(CS1_A_T01_LO03, evidence).readiness is ProgressionReadiness.READY


# ---------------------------------------------------------------------------
# Read-only store path + isolation
# ---------------------------------------------------------------------------


class TestReadOnlyAndIsolation:
    def test_evaluate_from_store_reads_only(self):
        store = ObjectiveAssessmentEvidenceStore(store=SessionDocumentStore())
        student = "readonly-student"
        items = [spec.item_id for spec in CS1_A_T01_LO04.evidence_items]
        for i, item_id in enumerate(items):
            store.append(
                _record(
                    student_id=student,
                    objective_id=CS1_A_T01_LO04.objective_id,
                    item_id=item_id,
                    scored_correct=True,
                    offset=i,
                )
            )
        before = store.count()

        append_calls: list[object] = []
        original_append = store.append

        def spy_append(record):
            append_calls.append(record)
            return original_append(record)

        store.append = spy_append  # type: ignore[method-assign]

        result = evaluate_from_store(
            CS1_A_T01_LO04.objective_id,
            student,
            CS1_A_T01_LO04,
            store,
        )
        assert result.readiness is ProgressionReadiness.READY
        assert append_calls == []
        assert store.count() == before

    def test_package_does_not_import_forbidden_systems(self):
        for path in PKG.rglob("*.py"):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        for prefix in FORBIDDEN_IMPORT_PREFIXES:
                            assert not alias.name.startswith(prefix), (
                                f"{path} imports {alias.name}"
                            )
                elif isinstance(node, ast.ImportFrom) and node.module:
                    for prefix in FORBIDDEN_IMPORT_PREFIXES:
                        assert not node.module.startswith(prefix), (
                            f"{path} imports from {node.module}"
                        )

    def test_insufficient_evidence_requires_reason(self):
        with pytest.raises(ValueError):
            from app.application.progression_readiness.results import (
                ProgressionReadinessResult,
            )

            ProgressionReadinessResult(
                objective_id="x",
                student_id="s",
                readiness=ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                reason=None,
            )

    def test_ready_may_carry_dual_demonstration_reason(self):
        from app.application.progression_readiness.results import (
            ProgressionReadinessResult,
        )

        result = ProgressionReadinessResult(
            objective_id="x",
            student_id="s",
            readiness=ProgressionReadiness.READY,
            reason=InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED,
        )
        assert result.reason is InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED


# ---------------------------------------------------------------------------
# Topic 2.1 LO01 / LO02: 4-item conceptual ready_min_correct=3
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("contract", [CS1_B_T01_LO01, CS1_B_T01_LO02])
class TestTopic21ConceptualFourItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_four_of_four_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_three_of_four_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], True),
                (items[2], True),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_two_of_four_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], True),
                (items[2], False),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_one_of_four_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [
                (items[0], True),
                (items[1], False),
                (items[2], False),
                (items[3], False),
            ],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_four_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 2.1 LO03: dual-pair MIXED_MODALITY_DUAL_DEMONSTRATION (9-cell matrix)
# ---------------------------------------------------------------------------


class TestTopic21DualDemonstrationLO03:
    contract = CS1_B_T01_LO03
    pair_a_mcq = "cs1004-2.1c-ar-01"
    pair_a_num = "cs1004-2.1c-cp-01"
    pair_b_mcq = "cs1016-2.1.3-ar-01"
    pair_b_num = "cs1016-2.1.3-cp-01"

    def _pair_rows(
        self,
        *,
        a_mcq: bool | None,
        a_num: bool | None,
        b_mcq: bool | None,
        b_num: bool | None,
    ) -> list[AssessmentEvidenceRecord]:
        """Build evidence for both pairs. None means modality unobserved."""
        rows: list[AssessmentEvidenceRecord] = []
        offset = 0
        for item_id, scored, response_type in (
            (self.pair_a_mcq, a_mcq, "mcq"),
            (self.pair_a_num, a_num, "numeric"),
            (self.pair_b_mcq, b_mcq, "mcq"),
            (self.pair_b_num, b_num, "numeric"),
        ):
            if scored is None:
                continue
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=item_id,
                    scored_correct=scored,
                    offset=offset,
                    response_type=response_type,
                )
            )
            offset += 1
        return rows

    @pytest.mark.parametrize(
        ("a_mcq", "a_num", "b_mcq", "b_num", "readiness", "reason"),
        [
            # READY + READY
            (
                True,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED,
            ),
            # READY + INSUFFICIENT (pair B MCQ wrong, numeric correct)
            (
                True,
                True,
                False,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            # INSUFFICIENT + READY (pair A incomplete, pair B ready)
            (
                False,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            # READY + NOT_READY (pair B MCQ correct, numeric wrong)
            (
                True,
                True,
                True,
                False,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            # NOT_READY + READY (order reversed)
            (
                True,
                False,
                True,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            # INSUFFICIENT + INSUFFICIENT
            (
                False,
                True,
                False,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.INSUFFICIENT_SAMPLE,
            ),
            # NOT_READY + INSUFFICIENT
            (
                True,
                False,
                False,
                True,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            # INSUFFICIENT + NOT_READY
            (
                False,
                True,
                True,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            # NOT_READY + NOT_READY
            (
                False,
                False,
                False,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
        ],
    )
    def test_nine_cell_combination_matrix(
        self, a_mcq, a_num, b_mcq, b_num, readiness, reason
    ):
        evidence = self._pair_rows(
            a_mcq=a_mcq, a_num=a_num, b_mcq=b_mcq, b_num=b_num
        )
        result = _eval(self.contract, evidence)
        assert result.readiness is readiness
        assert result.reason is reason

    def test_both_pairs_unobserved_insufficient_sample(self):
        result = _eval(self.contract, [])
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 2.1 LO05: every 2-of-3 pair still covers continuous and discrete halves
# ---------------------------------------------------------------------------


class TestTopic21LO05BothHalvesCoverage:
    """The combined ar-02 item exists so 2-of-3 cannot skip a half."""

    ar01 = "cs1004-2.1e-ar-01"
    ar02 = "cs1004-2.1e-ar-02"
    cp01 = "cs1004-2.1e-cp-01"
    package_name = "2.1.5-inverse-transform-cs1004.json"

    def _check(self, item_id: str):
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        root = Path("app/curriculum/data/educational_packages")
        loader = EducationalPackageLoader(root=root)
        packs = {
            Path(p.source_path).name: p for p in loader.all_approved()
        }
        pack = packs[self.package_name]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id}"
        return match

    @staticmethod
    def _blob(check) -> str:
        parts = [
            check.prompt or "",
            check.body or "",
            check.explanation or "",
            check.model_answer or "",
        ]
        parts.extend(choice.label for choice in check.choices)
        return " ".join(parts)

    def _tests_continuous(self, check) -> bool:
        text = self._blob(check)
        return "Exponential" in text or "F^{-1}" in text

    def _tests_discrete(self, check) -> bool:
        text = self._blob(check)
        lower = text.lower()
        return "discrete" in lower or "F(0)" in text or "F(1)" in text

    def test_live_items_have_the_intended_halves(self):
        ar01 = self._check(self.ar01)
        ar02 = self._check(self.ar02)
        cp01 = self._check(self.cp01)
        assert self._tests_continuous(ar01)
        assert not self._tests_discrete(ar01)
        assert self._tests_continuous(ar02)
        assert self._tests_discrete(ar02)
        assert self._tests_discrete(cp01)
        assert not self._tests_continuous(cp01)

    @pytest.mark.parametrize(
        "item_ids",
        [
            ("cs1004-2.1e-ar-01", "cs1004-2.1e-cp-01"),
            ("cs1004-2.1e-ar-01", "cs1004-2.1e-ar-02"),
            ("cs1004-2.1e-cp-01", "cs1004-2.1e-ar-02"),
        ],
    )
    def test_every_two_of_three_pair_covers_both_halves(self, item_ids):
        checks = [self._check(item_id) for item_id in item_ids]
        assert any(self._tests_continuous(check) for check in checks)
        assert any(self._tests_discrete(check) for check in checks)


# ---------------------------------------------------------------------------
# Topic 2.2 LO02: every 2-of-3 pair still covers factorisation and refuse
# ---------------------------------------------------------------------------


class TestTopic22LO02BothHalvesCoverage:
    """The combined ar-02 item exists so 2-of-3 cannot skip a half.

    Halves: (1) factorisation, including applying the product check to a
    joint table; (2) refuse zero-correlation as independence. ar-01 states
    the product condition. cp-01 refuses the zero-correlation claim.
    ar-02 applies the check to an actual table and keeps the refuse.
    """

    ar01 = "cs1005-2.2.2-ar-01"
    ar02 = "cs1005-2.2.2-ar-02"
    cp01 = "cs1005-2.2.2-cp-01"
    package_name = "2.2.2-independence-cs1005.json"

    def _check(self, item_id: str):
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        root = Path("app/curriculum/data/educational_packages")
        loader = EducationalPackageLoader(root=root)
        packs = {
            Path(p.source_path).name: p for p in loader.all_approved()
        }
        pack = packs[self.package_name]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id}"
        return match

    @staticmethod
    def _blob(check) -> str:
        parts = [
            check.prompt or "",
            check.body or "",
            check.explanation or "",
            check.model_answer or "",
        ]
        parts.extend(choice.label for choice in check.choices)
        return " ".join(parts)

    def _applies_factorisation_to_table(self, check) -> bool:
        text = self._blob(check)
        return "P(0,0)" in text and "0.45" in text and "0.36" in text

    def _covers_factorisation(self, check) -> bool:
        if self._applies_factorisation_to_table(check):
            return True
        text = self._blob(check)
        lower = text.lower()
        return (
            "product of the marginals" in lower
            or "joint factorisation" in lower
            or "joint equals the product" in lower
        )

    def _refuses_zero_correlation(self, check) -> bool:
        text = self._blob(check)
        lower = text.lower()
        return (
            "zero correlation" in lower
            or "correlation is zero" in lower
            or "uncorrelated" in lower
        )

    def test_live_items_have_the_intended_halves(self):
        ar01 = self._check(self.ar01)
        ar02 = self._check(self.ar02)
        cp01 = self._check(self.cp01)
        assert self._covers_factorisation(ar01)
        assert not self._applies_factorisation_to_table(ar01)
        assert not self._refuses_zero_correlation(ar01)
        assert self._covers_factorisation(ar02)
        assert self._applies_factorisation_to_table(ar02)
        assert self._refuses_zero_correlation(ar02)
        assert self._refuses_zero_correlation(cp01)
        assert not self._applies_factorisation_to_table(cp01)

    @pytest.mark.parametrize(
        "item_ids",
        [
            ("cs1005-2.2.2-ar-01", "cs1005-2.2.2-cp-01"),
            ("cs1005-2.2.2-ar-01", "cs1005-2.2.2-ar-02"),
            ("cs1005-2.2.2-cp-01", "cs1005-2.2.2-ar-02"),
        ],
    )
    def test_every_two_of_three_pair_covers_both_halves(self, item_ids):
        checks = [self._check(item_id) for item_id in item_ids]
        assert any(self._covers_factorisation(check) for check in checks)
        assert any(self._refuses_zero_correlation(check) for check in checks)


# ---------------------------------------------------------------------------
# Topic 2.2 LO01: single-pair mixed; cs1016 tagged but excluded from contract
# ---------------------------------------------------------------------------


class TestTopic22LO01Cs1005OnlyExcludesCs1016:
    contract = CS1_B_T02_LO01
    mcq = "cs1005-2.2.1-ar-01"
    numeric = "cs1005-2.2.1-cp-01"
    cs1016_mcq = "cs1016-2.2.1-ar-01"
    cs1016_numeric = "cs1016-2.2.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset({self.mcq, self.numeric})
        assert self.cs1016_mcq not in self.contract.item_ids
        assert self.cs1016_numeric not in self.contract.item_ids

    def test_cs1005_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=False,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1005(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_cs1005_mcq_ok_numeric_fail_not_ready_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=False,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert (
            _eval(self.contract, evidence).readiness is ProgressionReadiness.NOT_READY
        )
        cases = [
            (True, True, ProgressionReadiness.READY, None),
            (True, False, ProgressionReadiness.NOT_READY, None),
            (
                False,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED,
            ),
            (False, False, ProgressionReadiness.NOT_READY, None),
        ]
        for mcq_ok, num_ok, readiness, reason in cases:
            evidence = [
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                ),
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.numeric,
                    scored_correct=num_ok,
                    offset=1,
                    response_type="numeric",
                ),
            ]
            result = _eval(self.contract, evidence)
            assert result.readiness is readiness
            assert result.reason is reason


# ---------------------------------------------------------------------------
# Topic 2.4 LO01: every 2-of-3 pair still covers definition and named-family
# ---------------------------------------------------------------------------


class TestTopic24LO01BothHalvesCoverage:
    """The combined ar-02 item exists so 2-of-3 cannot skip a half.

    Halves: (1) MGF/CGF as functions of t, not raw moments; (2) named-family
    forms. ar-01 states the definitions. cp-01 identifies the Poisson pair.
    ar-02 forms Bernoulli MGF/CGF and keeps the mean-as-MGF refuse.
    """

    ar01 = "cs1007-2.4.1-ar-01"
    ar02 = "cs1007-2.4.1-ar-02"
    cp01 = "cs1007-2.4.1-cp-01"
    package_name = "2.4.1-mgf-cgf-cs1007.json"

    def _check(self, item_id: str):
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        root = Path("app/curriculum/data/educational_packages")
        loader = EducationalPackageLoader(root=root)
        packs = {
            Path(p.source_path).name: p for p in loader.all_approved()
        }
        pack = packs[self.package_name]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id}"
        return match

    @staticmethod
    def _blob(check) -> str:
        parts = [
            check.prompt or "",
            check.body or "",
            check.explanation or "",
            check.model_answer or "",
        ]
        parts.extend(choice.label for choice in check.choices)
        return " ".join(parts)

    def _covers_definitions(self, check) -> bool:
        text = self._blob(check)
        return r"E[e^{tX}]" in text or r"E[e^{tX}]" in text.replace(" ", "")

    def _applies_named_family(self, check) -> bool:
        text = self._blob(check)
        return "Bernoulli" in text or "Poisson" in text or r"\lambda" in text

    def _refuses_mean_as_mgf(self, check) -> bool:
        text = self._blob(check)
        lower = text.lower()
        return (
            "mean 0.4" in lower
            or "mean and variance" in lower
            or "mean alone" in lower
            or "not the mgf" in lower
        )

    def test_live_items_have_the_intended_halves(self):
        ar01 = self._check(self.ar01)
        ar02 = self._check(self.ar02)
        cp01 = self._check(self.cp01)
        assert self._covers_definitions(ar01)
        assert not self._applies_named_family(ar01) or "Bernoulli" not in self._blob(
            ar01
        )
        assert self._applies_named_family(ar02)
        assert "Bernoulli" in self._blob(ar02)
        assert self._refuses_mean_as_mgf(ar02)
        assert self._applies_named_family(cp01)
        assert "Bernoulli" not in self._blob(cp01)

    @pytest.mark.parametrize(
        "item_ids",
        [
            ("cs1007-2.4.1-ar-01", "cs1007-2.4.1-cp-01"),
            ("cs1007-2.4.1-ar-01", "cs1007-2.4.1-ar-02"),
            ("cs1007-2.4.1-cp-01", "cs1007-2.4.1-ar-02"),
        ],
    )
    def test_every_two_of_three_pair_covers_both_halves(self, item_ids):
        checks = [self._check(item_id) for item_id in item_ids]
        assert any(
            self._covers_definitions(check) or self._applies_named_family(check)
            for check in checks
        )
        assert any(
            self._refuses_mean_as_mgf(check) or self._applies_named_family(check)
            for check in checks
        )


# ---------------------------------------------------------------------------
# Topic 2.4 LO02: every 2-of-3 pair still covers the rule and extraction
# ---------------------------------------------------------------------------


class TestTopic24LO02BothHalvesCoverage:
    """The combined ar-02 item exists so 2-of-3 cannot skip a half.

    Halves: (1) Taylor / derivative-at-zero rule; (2) applied extraction.
    ar-01 states the rule. cp-01 differentiates a Poisson MGF for E[X].
    ar-02 extracts Bernoulli mean and variance and keeps the refuse.
    """

    ar01 = "cs1007-2.4.2-ar-01"
    ar02 = "cs1007-2.4.2-ar-02"
    cp01 = "cs1007-2.4.2-cp-01"
    package_name = "2.4.2-moment-via-gf-cs1007.json"

    def _check(self, item_id: str):
        from app.application.educational_packages.loader import (
            EducationalPackageLoader,
        )

        root = Path("app/curriculum/data/educational_packages")
        loader = EducationalPackageLoader(root=root)
        packs = {
            Path(p.source_path).name: p for p in loader.all_approved()
        }
        pack = packs[self.package_name]
        match = next(
            (c for c in pack.knowledge_checks if c.item_id == item_id),
            None,
        )
        assert match is not None, f"missing {item_id}"
        return match

    @staticmethod
    def _blob(check) -> str:
        parts = [
            check.prompt or "",
            check.body or "",
            check.explanation or "",
            check.model_answer or "",
        ]
        parts.extend(choice.label for choice in check.choices)
        return " ".join(parts)

    def _covers_extraction_rule(self, check) -> bool:
        text = self._blob(check)
        return (
            "Taylor" in text
            or r"M_{X}^{(r)}(0)" in text
            or "coefficient of $t$" in text
        )

    def _applies_extraction(self, check) -> bool:
        text = self._blob(check)
        return r"M_{X}'(0)" in text or r"M_{X}'(t)" in text

    def _refuses_definition_as_extraction(self, check) -> bool:
        text = self._blob(check)
        lower = text.lower()
        return (
            "without differentiating" in lower
            or "already states the mean" in lower
            or "completes moment extraction" in lower
        )

    def test_live_items_have_the_intended_halves(self):
        ar01 = self._check(self.ar01)
        ar02 = self._check(self.ar02)
        cp01 = self._check(self.cp01)
        assert self._covers_extraction_rule(ar01)
        assert self._covers_extraction_rule(ar02)
        assert self._applies_extraction(ar02)
        assert self._refuses_definition_as_extraction(ar02)
        assert self._applies_extraction(cp01)
        assert "Bernoulli" not in self._blob(cp01)

    @pytest.mark.parametrize(
        "item_ids",
        [
            ("cs1007-2.4.2-ar-01", "cs1007-2.4.2-cp-01"),
            ("cs1007-2.4.2-ar-01", "cs1007-2.4.2-ar-02"),
            ("cs1007-2.4.2-cp-01", "cs1007-2.4.2-ar-02"),
        ],
    )
    def test_every_two_of_three_pair_covers_both_halves(self, item_ids):
        checks = [self._check(item_id) for item_id in item_ids]
        assert any(self._covers_extraction_rule(check) for check in checks)
        assert any(
            self._applies_extraction(check)
            or self._refuses_definition_as_extraction(check)
            for check in checks
        )


# ---------------------------------------------------------------------------
# Topic 2.5 LO01: single-pair mixed; cs1016 tagged but excluded from contract
# ---------------------------------------------------------------------------


class TestTopic25LO01Cs1008OnlyExcludesCs1016:
    contract = CS1_B_T05_LO01
    mcq = "cs1008-2.5.1-ar-01"
    numeric = "cs1008-2.5.1-cp-01"
    cs1016_mcq = "cs1016-2.5.1-ar-01"
    cs1016_numeric = "cs1016-2.5.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset({self.mcq, self.numeric})
        assert self.cs1016_mcq not in self.contract.item_ids
        assert self.cs1016_numeric not in self.contract.item_ids

    def test_cs1008_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=False,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1008(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_cs1008_mcq_ok_numeric_fail_not_ready_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=False,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert (
            _eval(self.contract, evidence).readiness is ProgressionReadiness.NOT_READY
        )


# ---------------------------------------------------------------------------
# Topic 2.5 LO02: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


class TestTopic25LO02ConceptualTwoItem:
    contract = CS1_B_T05_LO02

    def _items(self):
        return [spec.item_id for spec in self.contract.evidence_items]

    def test_two_of_two_ready(self):
        items = self._items()
        evidence = _evidence_for_items(
            "s1", self.contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self):
        items = self._items()
        evidence = _evidence_for_items(
            "s1",
            self.contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self):
        items = self._items()
        evidence = _evidence_for_items(
            "s1", self.contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 2.2 LO03 / LO04: single-pair mixed modality (no prerequisite)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("contract", [CS1_B_T02_LO03, CS1_B_T02_LO04])
class TestTopic22MixedModalityLO03LO04:
    def _pair(self, contract, mcq_ok: bool | None, numeric_ok: bool | None):
        mcq = contract.evidence_items[0].item_id
        numeric = contract.evidence_items[1].item_id
        rows = []
        if mcq_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                )
            )
        if numeric_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=numeric,
                    scored_correct=numeric_ok,
                    offset=1,
                    response_type="numeric",
                )
            )
        return rows

    def test_both_correct_ready(self, contract):
        evidence = self._pair(contract, True, True)
        assert _eval(contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(self, contract):
        result = _eval(contract, self._pair(contract, True, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(self, contract):
        result = _eval(contract, self._pair(contract, False, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(self, contract):
        result = _eval(contract, self._pair(contract, False, False))
        assert result.readiness is ProgressionReadiness.NOT_READY


# ---------------------------------------------------------------------------
# Cross-topic: CS1-B-T03-LO01 prerequisite now verified by live T02-LO01 items
# ---------------------------------------------------------------------------


class TestCrossTopicPrerequisiteT03DependsOnT02:
    """End-to-end proof: T03-LO01 gate uses real CS1-B-T02-LO01 evidence both ways."""

    t03 = CS1_B_T03_LO01
    t02 = CS1_B_T02_LO01

    def _t03_own(self, mcq_ok: bool, numeric_ok: bool):
        return [
            _record(
                student_id="s1",
                objective_id=self.t03.objective_id,
                item_id=self.t03.evidence_items[0].item_id,
                scored_correct=mcq_ok,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.t03.objective_id,
                item_id=self.t03.evidence_items[1].item_id,
                scored_correct=numeric_ok,
                offset=1,
                response_type="numeric",
            ),
        ]

    def _t02_scored_correct(self):
        return [
            _record(
                student_id="s1",
                objective_id=self.t02.objective_id,
                item_id="cs1005-2.2.1-ar-01",
                scored_correct=True,
                offset=10,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.t02.objective_id,
                item_id="cs1005-2.2.1-cp-01",
                scored_correct=True,
                offset=11,
                response_type="numeric",
            ),
        ]

    def test_no_t02_evidence_still_prerequisite_unverified(self):
        result = _eval(self.t03, self._t03_own(True, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED

    def test_t02_incorrect_only_still_prerequisite_unverified(self):
        t02_fail = [
            _record(
                student_id="s1",
                objective_id=self.t02.objective_id,
                item_id="cs1005-2.2.1-ar-01",
                scored_correct=False,
                offset=10,
                response_type="mcq",
            ),
        ]
        result = _eval(self.t03, self._t03_own(True, True) + t02_fail)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_PREREQUISITE_UNVERIFIED

    def test_genuine_t02_scored_correct_unlocks_t03_ready(self):
        evidence = self._t03_own(True, True) + self._t02_scored_correct()
        result = _eval(self.t03, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_cs1016_only_scored_correct_also_verifies_prerequisite(self):
        """Prerequisite check is objective-scoped (any scored-correct T02-LO01)."""
        t02_cs1016 = [
            _record(
                student_id="s1",
                objective_id=self.t02.objective_id,
                item_id="cs1016-2.2.1-ar-01",
                scored_correct=True,
                offset=10,
                response_type="mcq",
            ),
        ]
        result = _eval(self.t03, self._t03_own(True, True) + t02_cs1016)
        assert result.readiness is ProgressionReadiness.READY


# ---------------------------------------------------------------------------
# Topic 2.6 LO01: 2-item conceptual; cs1016 tagged but excluded from contract
# ---------------------------------------------------------------------------


class TestTopic26LO01Cs1009OnlyExcludesCs1016:
    contract = CS1_B_T06_LO01
    primary_ar = "cs1009-2.6.1-ar-01"
    primary_cp = "cs1009-2.6.1-cp-01"
    cs1016_ar = "cs1016-2.6.1-ar-01"
    cs1016_cp = "cs1016-2.6.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        assert self.cs1016_ar not in self.contract.item_ids
        assert self.cs1016_cp not in self.contract.item_ids

    def test_cs1009_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=False,
                offset=3,
                response_type="mcq",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1009(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_cs1009_one_of_two_insufficient_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=False,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=3,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 2.6 LO01-LO06: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_B_T06_LO01,
        CS1_B_T06_LO02,
        CS1_B_T06_LO03,
        CS1_B_T06_LO04,
        CS1_B_T06_LO05,
        CS1_B_T06_LO06,
    ],
)
class TestTopic26ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 3.1 LO01: single-pair mixed; cs1016 tagged but excluded from contract
# ---------------------------------------------------------------------------


class TestTopic31LO01Cs1010OnlyExcludesCs1016:
    contract = CS1_C_T01_LO01
    mcq = "cs1010-3.1.1-ar-01"
    numeric = "cs1010-3.1.1-cp-01"
    cs1016_mcq = "cs1016-3.1.1-ar-01"
    cs1016_numeric = "cs1016-3.1.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset({self.mcq, self.numeric})
        assert self.cs1016_mcq not in self.contract.item_ids
        assert self.cs1016_numeric not in self.contract.item_ids

    def test_cs1010_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=False,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1010(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_cs1010_mcq_ok_numeric_fail_not_ready_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=False,
                offset=1,
                response_type="numeric",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_mcq,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_numeric,
                scored_correct=True,
                offset=3,
                response_type="numeric",
            ),
        ]
        assert (
            _eval(self.contract, evidence).readiness is ProgressionReadiness.NOT_READY
        )


# ---------------------------------------------------------------------------
# Topic 3.1 LO02 / LO06: single-pair mixed-modality four-cell matrix
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract,mcq,numeric",
    [
        (CS1_C_T01_LO02, "cs1010-3.1.2-ar-01", "cs1010-3.1.2-cp-01"),
        (CS1_C_T01_LO06, "cs1010-3.1.6-ar-01", "cs1010-3.1.6-cp-01"),
    ],
)
class TestTopic31MixedModalityLO02LO06:
    def _pair(
        self,
        contract,
        mcq,
        numeric,
        mcq_ok: bool | None,
        numeric_ok: bool | None,
    ):
        rows = []
        if mcq_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                )
            )
        if numeric_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=numeric,
                    scored_correct=numeric_ok,
                    offset=1,
                    response_type="numeric",
                )
            )
        return rows

    def test_both_correct_ready(self, contract, mcq, numeric):
        evidence = self._pair(contract, mcq, numeric, True, True)
        assert _eval(contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(self, contract, mcq, numeric):
        result = _eval(contract, self._pair(contract, mcq, numeric, True, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(
        self, contract, mcq, numeric
    ):
        result = _eval(contract, self._pair(contract, mcq, numeric, False, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(self, contract, mcq, numeric):
        result = _eval(contract, self._pair(contract, mcq, numeric, False, False))
        assert result.readiness is ProgressionReadiness.NOT_READY


# ---------------------------------------------------------------------------
# Topic 3.1 LO03-LO05: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_C_T01_LO03,
        CS1_C_T01_LO04,
        CS1_C_T01_LO05,
    ],
)
class TestTopic31ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 3.2 LO01: conceptual pair; cs1016 tagged but excluded from contract
# ---------------------------------------------------------------------------


class TestTopic32LO01Cs1011OnlyExcludesCs1016:
    contract = CS1_C_T02_LO01
    primary_ar = "cs1011-3.2.1-ar-01"
    primary_cp = "cs1011-3.2.1-cp-01"
    cs1016_ar = "cs1016-3.2.1-ar-01"
    cs1016_cp = "cs1016-3.2.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        assert self.cs1016_ar not in self.contract.item_ids
        assert self.cs1016_cp not in self.contract.item_ids

    def test_cs1011_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=False,
                offset=3,
                response_type="mcq",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1011(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_cs1011_one_of_two_insufficient_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=False,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=3,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 3.2 LO01-LO08: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_C_T02_LO01,
        CS1_C_T02_LO02,
        CS1_C_T02_LO03,
        CS1_C_T02_LO04,
        CS1_C_T02_LO05,
        CS1_C_T02_LO06,
        CS1_C_T02_LO07,
        CS1_C_T02_LO08,
    ],
)
class TestTopic32ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 3.3 LO01: cs1012 only; cs1016 twin OEA-tagged but excluded
# ---------------------------------------------------------------------------


class TestTopic33LO01Cs1012OnlyExcludesCs1016:
    contract = CS1_C_T03_LO01
    primary_ar = "cs1012-3.3.1-ar-01"
    primary_cp = "cs1012-3.3.1-cp-01"
    cs1016_ar = "cs1016-3.3.1-ar-01"
    cs1016_cp = "cs1016-3.3.1-cp-01"

    def test_contract_item_ids_exclude_cs1016(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        assert self.cs1016_ar not in self.contract.item_ids
        assert self.cs1016_cp not in self.contract.item_ids

    def test_cs1012_both_correct_ready_even_with_cs1016_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=False,
                offset=3,
                response_type="mcq",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1016_both_correct_does_not_make_ready_without_cs1012(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_cs1012_one_of_two_insufficient_despite_cs1016_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=False,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_ar,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.cs1016_cp,
                scored_correct=True,
                offset=3,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 3.3 LO01-LO05: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_C_T03_LO01,
        CS1_C_T03_LO02,
        CS1_C_T03_LO03,
        CS1_C_T03_LO04,
        CS1_C_T03_LO05,
    ],
)
class TestTopic33ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 4.1 LO01: cs1003 only; Continuity + Memory twins OEA-tagged but excluded
# ---------------------------------------------------------------------------


class TestTopic41LO01Cs1003OnlyExcludesTwins:
    contract = CS1_D_T01_LO01
    primary_ar = "cs1003-4.1.1-ar-01"
    primary_cp = "cs1003-4.1.1-cp-01"
    twin_ids = (
        "cs1013-4.1.1-ar-01",
        "cs1013-4.1.1-cp-01",
        "cs1016-4.1.1-ar-01",
        "cs1016-4.1.1-cp-01",
    )

    def test_contract_item_ids_exclude_twins(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        for twin_id in self.twin_ids:
            assert twin_id not in self.contract.item_ids

    def test_cs1003_both_correct_ready_even_with_twins_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        for i, twin_id in enumerate(self.twin_ids, start=2):
            evidence.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=twin_id,
                    scored_correct=False,
                    offset=i,
                    response_type="mcq",
                )
            )
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_twins_both_correct_do_not_make_ready_without_cs1003(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=twin_id,
                scored_correct=True,
                offset=i,
                response_type="mcq",
            )
            for i, twin_id in enumerate(self.twin_ids)
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_cs1003_one_of_two_insufficient_despite_twins_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=False,
                offset=1,
                response_type="mcq",
            ),
        ]
        for i, twin_id in enumerate(self.twin_ids, start=2):
            evidence.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=twin_id,
                    scored_correct=True,
                    offset=i,
                    response_type="mcq",
                )
            )
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 4.1 LO04: cs1003 only; Continuity twin OEA-tagged but excluded
# ---------------------------------------------------------------------------


class TestTopic41LO04Cs1003OnlyExcludesCs1013:
    contract = CS1_D_T01_LO04
    primary_ar = "cs1003-4.1.4-ar-01"
    primary_cp = "cs1003-4.1.4-cp-01"
    twin_ar = "cs1013-4.1.4-ar-01"
    twin_cp = "cs1013-4.1.4-cp-01"

    def test_contract_item_ids_exclude_cs1013(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        assert self.twin_ar not in self.contract.item_ids
        assert self.twin_cp not in self.contract.item_ids

    def test_cs1003_both_correct_ready_even_with_cs1013_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_ar,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_cp,
                scored_correct=False,
                offset=3,
                response_type="mcq",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1013_both_correct_does_not_make_ready_without_cs1003(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_cs1003_one_of_two_insufficient_despite_cs1013_correct(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=False,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_ar,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_cp,
                scored_correct=True,
                offset=3,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 4.1 LO01-LO05: 2-item conceptual ready_min_correct=2
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_D_T01_LO01,
        CS1_D_T01_LO02,
        CS1_D_T01_LO03,
        CS1_D_T01_LO04,
        CS1_D_T01_LO05,
    ],
)
class TestTopic41ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 4.2 LO01/LO02/LO03/LO04/LO06/LO07/LO09: 2-item conceptual
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_D_T02_LO01,
        CS1_D_T02_LO02,
        CS1_D_T02_LO03,
        CS1_D_T02_LO04,
        CS1_D_T02_LO06,
        CS1_D_T02_LO07,
        CS1_D_T02_LO09,
    ],
)
class TestTopic42ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 4.2 LO01: cs1003 only; Continuity twins OEA-tagged but excluded
# ---------------------------------------------------------------------------


class TestTopic42LO01Cs1003OnlyExcludesCs1014:
    contract = CS1_D_T02_LO01
    primary_ar = "cs1003-4.2.1-ar-01"
    primary_cp = "cs1003-4.2.1-cp-01"
    twin_ar = "cs1014-4.2.1-ar-01"
    twin_cp = "cs1014-4.2.1-cp-01"

    def test_contract_item_ids_exclude_cs1014(self):
        assert self.contract.item_ids == frozenset(
            {self.primary_ar, self.primary_cp}
        )
        assert self.twin_ar not in self.contract.item_ids
        assert self.twin_cp not in self.contract.item_ids

    def test_cs1003_both_correct_ready_even_with_cs1014_incorrect(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.primary_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_ar,
                scored_correct=False,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_cp,
                scored_correct=False,
                offset=3,
                response_type="mcq",
            ),
        ]
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_cs1014_both_correct_do_not_make_ready_without_cs1003(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_ar,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_cp,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE


# ---------------------------------------------------------------------------
# Topic 4.2 LO05 / LO10: dual-pair MIXED_MODALITY_DUAL_DEMONSTRATION
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract,pair_a_mcq,pair_a_num,pair_b_mcq,pair_b_num",
    [
        (
            CS1_D_T02_LO05,
            "cs1003-4.2.5-ar-01",
            "cs1003-4.2.5-cp-01",
            "cs1014-4.2.5-ar-01",
            "cs1014-4.2.5-cp-01",
        ),
        (
            CS1_D_T02_LO10,
            "cs1003-4.2.10-ar-01",
            "cs1003-4.2.10-cp-01",
            "cs1014-4.2.10-ar-01",
            "cs1014-4.2.10-cp-01",
        ),
    ],
)
class TestTopic42DualDemonstrationLO05LO10:
    def _pair_rows(
        self,
        contract,
        pair_a_mcq,
        pair_a_num,
        pair_b_mcq,
        pair_b_num,
        *,
        a_mcq: bool | None,
        a_num: bool | None,
        b_mcq: bool | None,
        b_num: bool | None,
    ) -> list[AssessmentEvidenceRecord]:
        rows: list[AssessmentEvidenceRecord] = []
        offset = 0
        for item_id, scored, response_type in (
            (pair_a_mcq, a_mcq, "mcq"),
            (pair_a_num, a_num, "numeric"),
            (pair_b_mcq, b_mcq, "mcq"),
            (pair_b_num, b_num, "numeric"),
        ):
            if scored is None:
                continue
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=item_id,
                    scored_correct=scored,
                    offset=offset,
                    response_type=response_type,
                )
            )
            offset += 1
        return rows

    @pytest.mark.parametrize(
        ("a_mcq", "a_num", "b_mcq", "b_num", "readiness", "reason"),
        [
            (
                True,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED,
            ),
            (
                True,
                True,
                False,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            (
                False,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            (
                True,
                True,
                True,
                False,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            (
                True,
                False,
                True,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            (
                False,
                True,
                False,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.INSUFFICIENT_SAMPLE,
            ),
            (
                True,
                False,
                False,
                True,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            (
                False,
                True,
                True,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            (
                False,
                False,
                False,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
        ],
    )
    def test_nine_cell_combination_matrix(
        self,
        contract,
        pair_a_mcq,
        pair_a_num,
        pair_b_mcq,
        pair_b_num,
        a_mcq,
        a_num,
        b_mcq,
        b_num,
        readiness,
        reason,
    ):
        evidence = self._pair_rows(
            contract,
            pair_a_mcq,
            pair_a_num,
            pair_b_mcq,
            pair_b_num,
            a_mcq=a_mcq,
            a_num=a_num,
            b_mcq=b_mcq,
            b_num=b_num,
        )
        result = _eval(contract, evidence)
        assert result.readiness is readiness
        assert result.reason is reason


# ---------------------------------------------------------------------------
# Topic 4.2 LO08: single-pair mixed; cs1014 OEA-tagged but excluded
# ---------------------------------------------------------------------------


class TestTopic42LO08MixedModalityCs1003Only:
    contract = CS1_D_T02_LO08
    mcq = "cs1003-4.2.8-ar-01"
    numeric = "cs1003-4.2.8-cp-01"
    twin_mcq = "cs1014-4.2.8-ar-01"
    twin_numeric = "cs1014-4.2.8-cp-01"

    def _pair(self, mcq_ok: bool | None, numeric_ok: bool | None):
        rows = []
        if mcq_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                )
            )
        if numeric_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=self.numeric,
                    scored_correct=numeric_ok,
                    offset=1,
                    response_type="numeric",
                )
            )
        return rows

    def test_both_correct_ready(self):
        evidence = self._pair(True, True)
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(True, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(self):
        result = _eval(self.contract, self._pair(False, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(False, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_cs1014_evidence_does_not_affect_result(self):
        """Independent twin numeric (and identical AR) never enter LO08 evaluation."""
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.twin_numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

        evidence_with_primary_partial = evidence + [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=False,
                offset=3,
                response_type="numeric",
            ),
        ]
        result2 = _eval(self.contract, evidence_with_primary_partial)
        assert result2.readiness is ProgressionReadiness.NOT_READY


# ---------------------------------------------------------------------------
# Topic 5.1 LO02/LO03/LO05/LO09: 2-item conceptual
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract",
    [
        CS1_E_T01_LO02,
        CS1_E_T01_LO03,
        CS1_E_T01_LO05,
        CS1_E_T01_LO09,
    ],
)
class TestTopic51ConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_two_of_two_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert result.reason is None

    def test_one_of_two_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1",
            contract.objective_id,
            [(items[0], True), (items[1], False)],
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.INSUFFICIENT_SAMPLE

    def test_zero_of_two_not_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, False) for i in items]
        )
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.NOT_READY
        assert result.reason is None


# ---------------------------------------------------------------------------
# Topic 5.1 LO04/LO06/LO08: single-pair mixed; cs1015 OEA-tagged but excluded
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "contract,mcq,numeric,twin_mcq,twin_numeric",
    [
        (
            CS1_E_T01_LO04,
            "cs1003-5.1.4-ar-01",
            "cs1003-5.1.4-cp-01",
            "cs1015-5.1.4-ar-01",
            "cs1015-5.1.4-cp-01",
        ),
        (
            CS1_E_T01_LO06,
            "cs1003-5.1.6-ar-01",
            "cs1003-5.1.6-cp-01",
            "cs1015-5.1.6-ar-01",
            "cs1015-5.1.6-cp-01",
        ),
        (
            CS1_E_T01_LO08,
            "cs1003-5.1.8-ar-01",
            "cs1003-5.1.8-cp-01",
            "cs1015-5.1.8-ar-01",
            "cs1015-5.1.8-cp-01",
        ),
    ],
)
class TestTopic51MixedModalitySinglePair:
    def _pair(
        self,
        contract,
        mcq,
        numeric,
        twin_mcq,
        twin_numeric,
        mcq_ok: bool | None,
        numeric_ok: bool | None,
    ):
        rows = []
        if mcq_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=mcq,
                    scored_correct=mcq_ok,
                    offset=0,
                    response_type="mcq",
                )
            )
        if numeric_ok is not Ellipsis:
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=contract.objective_id,
                    item_id=numeric,
                    scored_correct=numeric_ok,
                    offset=1,
                    response_type="numeric",
                )
            )
        return rows

    def test_both_correct_ready(
        self, contract, mcq, numeric, twin_mcq, twin_numeric
    ):
        evidence = self._pair(
            contract, mcq, numeric, twin_mcq, twin_numeric, True, True
        )
        assert _eval(contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(
        self, contract, mcq, numeric, twin_mcq, twin_numeric
    ):
        result = _eval(
            contract,
            self._pair(contract, mcq, numeric, twin_mcq, twin_numeric, True, False),
        )
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(
        self, contract, mcq, numeric, twin_mcq, twin_numeric
    ):
        result = _eval(
            contract,
            self._pair(contract, mcq, numeric, twin_mcq, twin_numeric, False, True),
        )
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(
        self, contract, mcq, numeric, twin_mcq, twin_numeric
    ):
        result = _eval(
            contract,
            self._pair(contract, mcq, numeric, twin_mcq, twin_numeric, False, False),
        )
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_cs1015_evidence_does_not_affect_result(
        self, contract, mcq, numeric, twin_mcq, twin_numeric
    ):
        evidence = [
            _record(
                student_id="s1",
                objective_id=contract.objective_id,
                item_id=twin_mcq,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=contract.objective_id,
                item_id=twin_numeric,
                scored_correct=True,
                offset=1,
                response_type="numeric",
            ),
        ]
        result = _eval(contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED


# ---------------------------------------------------------------------------
# Topic 5.1 LO07: dual-pair MIXED_MODALITY_DUAL_DEMONSTRATION
# ---------------------------------------------------------------------------


class TestTopic51DualDemonstrationLO07:
    contract = CS1_E_T01_LO07
    pair_a_mcq = "cs1003-5.1.7-ar-01"
    pair_a_num = "cs1003-5.1.7-cp-01"
    pair_b_mcq = "cs1015-5.1.7-ar-01"
    pair_b_num = "cs1015-5.1.7-cp-01"

    def _pair_rows(
        self,
        *,
        a_mcq: bool | None,
        a_num: bool | None,
        b_mcq: bool | None,
        b_num: bool | None,
    ) -> list[AssessmentEvidenceRecord]:
        rows: list[AssessmentEvidenceRecord] = []
        offset = 0
        for item_id, scored, response_type in (
            (self.pair_a_mcq, a_mcq, "mcq"),
            (self.pair_a_num, a_num, "numeric"),
            (self.pair_b_mcq, b_mcq, "mcq"),
            (self.pair_b_num, b_num, "numeric"),
        ):
            if scored is None:
                continue
            rows.append(
                _record(
                    student_id="s1",
                    objective_id=self.contract.objective_id,
                    item_id=item_id,
                    scored_correct=scored,
                    offset=offset,
                    response_type=response_type,
                )
            )
            offset += 1
        return rows

    @pytest.mark.parametrize(
        ("a_mcq", "a_num", "b_mcq", "b_num", "readiness", "reason"),
        [
            (
                True,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.ALL_REQUIRED_MODALITIES_DEMONSTRATED,
            ),
            (
                True,
                True,
                False,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            (
                False,
                True,
                True,
                True,
                ProgressionReadiness.READY,
                InsufficientReason.SECOND_DEMONSTRATION_INCOMPLETE,
            ),
            (
                True,
                True,
                True,
                False,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            (
                True,
                False,
                True,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.CONFLICTING_DEMONSTRATIONS,
            ),
            (
                False,
                True,
                False,
                True,
                ProgressionReadiness.INSUFFICIENT_EVIDENCE,
                InsufficientReason.INSUFFICIENT_SAMPLE,
            ),
            (
                True,
                False,
                False,
                True,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            (
                False,
                True,
                True,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
            (
                False,
                False,
                False,
                False,
                ProgressionReadiness.NOT_READY,
                InsufficientReason.NEGATIVE_DEMONSTRATION,
            ),
        ],
    )
    def test_nine_cell_combination_matrix(
        self,
        a_mcq,
        a_num,
        b_mcq,
        b_num,
        readiness,
        reason,
    ):
        evidence = self._pair_rows(
            a_mcq=a_mcq,
            a_num=a_num,
            b_mcq=b_mcq,
            b_num=b_num,
        )
        result = _eval(self.contract, evidence)
        assert result.readiness is readiness
        assert result.reason is reason


# ---------------------------------------------------------------------------
# Topic 5.1 LO01: cross-package mixed (cs1003 MCQ + cs1016 numeric)
# ---------------------------------------------------------------------------


class TestTopic51LO01CrossPackageMixedModality:
    """Prove LO01 evaluates across packages with no evaluator changes."""

    contract = CS1_E_T01_LO01
    mcq = "cs1003-5.1.1-ar-01"
    numeric = "cs1016-5.1.1-cp-01"
    oe_only_mcq_cp = "cs1003-5.1.1-cp-01"
    oe_only_cs1015_ar = "cs1015-5.1.1-ar-01"
    oe_only_cs1015_cp = "cs1015-5.1.1-cp-01"
    oe_only_cs1016_ar = "cs1016-5.1.1-ar-01"

    def _pair(self, mcq_ok: bool, numeric_ok: bool):
        return [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                scored_correct=mcq_ok,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                scored_correct=numeric_ok,
                offset=1,
                response_type="numeric",
            ),
        ]

    def test_both_correct_ready_across_packages(self):
        evidence = self._pair(True, True)
        assert _eval(self.contract, evidence).readiness is ProgressionReadiness.READY

    def test_mcq_correct_numeric_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(True, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_mcq_incorrect_numeric_correct_modality_not_observed(self):
        result = _eval(self.contract, self._pair(False, True))
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_both_incorrect_not_ready(self):
        result = _eval(self.contract, self._pair(False, False))
        assert result.readiness is ProgressionReadiness.NOT_READY

    def test_oea_only_items_do_not_satisfy_contract(self):
        evidence = [
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.oe_only_mcq_cp,
                scored_correct=True,
                offset=0,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.oe_only_cs1015_ar,
                scored_correct=True,
                offset=1,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.oe_only_cs1015_cp,
                scored_correct=True,
                offset=2,
                response_type="mcq",
            ),
            _record(
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.oe_only_cs1016_ar,
                scored_correct=True,
                offset=3,
                response_type="mcq",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.INSUFFICIENT_EVIDENCE
        assert result.reason is InsufficientReason.REQUIRED_MODALITY_NOT_OBSERVED

    def test_cross_package_pairing_requires_no_evaluator_changes(self):
        """Contract item_ids alone drive matching; package_id is unused."""
        assert self.contract.item_ids == frozenset({self.mcq, self.numeric})
        evidence = [
            AssessmentEvidenceRecord(
                evidence_id=str(uuid4()),
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.mcq,
                package_id="CS1-EP001-PKG-5.1-BAYES-THEOREM",
                session_id="test-session",
                response_type="mcq",
                scored_correct=True,
                occurred_at=_when(0),
                source="test",
                selected_misconception_tag="",
            ),
            AssessmentEvidenceRecord(
                evidence_id=str(uuid4()),
                student_id="s1",
                objective_id=self.contract.objective_id,
                item_id=self.numeric,
                package_id="CS1-EP001-PKG-CP-5.1-BAYES-THEOREM",
                session_id="test-session",
                response_type="numeric",
                scored_correct=True,
                occurred_at=_when(1),
                source="test",
                selected_misconception_tag="",
            ),
        ]
        result = _eval(self.contract, evidence)
        assert result.readiness is ProgressionReadiness.READY
        assert evidence[0].package_id != evidence[1].package_id

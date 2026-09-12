"""Golden scenarios for Progression Readiness (six real contracts).

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
    CS1_B_T03_LO01,
    CS1_B_T03_LO02,
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
    def test_six_real_contracts_present(self):
        assert set(PROGRESSION_READINESS_CONTRACTS) == {
            "CS1-A-T01-LO01",
            "CS1-A-T01-LO02",
            "CS1-A-T01-LO03",
            "CS1-A-T01-LO04",
            "CS1-B-T03-LO01",
            "CS1-B-T03-LO02",
        }

    def test_topic_1_1_item_counts_match_live_freeze(self):
        assert CS1_A_T01_LO01.item_count == 3
        assert CS1_A_T01_LO02.item_count == 3
        assert CS1_A_T01_LO03.item_count == 2
        assert CS1_A_T01_LO04.item_count == 2
        assert CS1_A_T01_LO01.ready_min_correct == 2
        assert CS1_A_T01_LO03.ready_min_correct == 2

    def test_live_item_ids(self):
        assert CS1_A_T01_LO01.item_ids == frozenset(
            {
                "cs1017-1.1.1-ar-01",
                "cs1017-1.1.1-cp-01",
                "ep001-1.1-ar-01",
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

    def test_get_contract(self):
        assert get_contract("CS1-A-T01-LO01") is CS1_A_T01_LO01
        assert get_contract("missing") is None


# ---------------------------------------------------------------------------
# Conceptual 3-item (LO01 / LO02)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("contract", [CS1_A_T01_LO01, CS1_A_T01_LO02])
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
# Conceptual 2-item (LO03 / LO04)
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("contract", [CS1_A_T01_LO03, CS1_A_T01_LO04])
class TestConceptualTwoItem:
    def _items(self, contract):
        return [spec.item_id for spec in contract.evidence_items]

    def test_all_correct_ready(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(i, True) for i in items]
        )
        assert _eval(contract, evidence).readiness is ProgressionReadiness.READY

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
        assert _eval(contract, evidence).readiness is ProgressionReadiness.NOT_READY

    def test_sparse_one_correct_insufficient_sample(self, contract):
        items = self._items(contract)
        evidence = _evidence_for_items(
            "s1", contract.objective_id, [(items[0], True)]
        )
        result = _eval(contract, evidence)
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
            item_id="seeded-2.2.1-item",
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

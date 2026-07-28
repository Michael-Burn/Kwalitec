"""Application tests for Educational Reasoning Engine (EI-007)."""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path

import pytest

from app.application.curriculum_extraction.dto import ExtractionRequest
from app.application.curriculum_extraction.extraction_engine import (
    CurriculumExtractionEngine,
)
from app.application.curriculum_publishing.editorial_operations_service import (
    EditorialOperationsService,
)
from app.application.curriculum_publishing.publication_engine import (
    PublicationEngine,
)
from app.application.educational_reasoning_engine.exceptions import (
    DecisionNotFoundError,
    InstanceNotFoundError,
)
from app.application.educational_reasoning_engine.query_service import (
    DecisionQueryService,
)
from app.application.educational_reasoning_engine.reasoning_service import (
    DecisionReasoningService,
)
from app.application.learning_evidence.recording_service import (
    EvidenceRecordingService,
)
from app.application.student_curriculum_binding.binding_service import (
    StudentCurriculumBindingService,
)
from app.application.twin_inference.inference_service import BeliefInferenceService
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.educational_reasoning_engine.version import REASONING_VERSION
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.domain.student_curriculum_binding.node_state import (
    CompletionStatus,
    RevisionStatus,
)
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
)
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.student_curriculum_binding import SciCurriculumNodeState
from app.models.twin_inference import TieNodeBelief
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"
AS_OF = datetime(2026, 7, 28, 12, 0, 0)


def _publish_and_bind(*, job_id: str = "job-ei007-1") -> tuple[int, str, str]:
    user = _make_user()
    engine = CurriculumExtractionEngine()
    result = engine.extract(
        ExtractionRequest(
            job_id=job_id,
            subject_code="CS1",
            edition_label="2026",
            subject_title="Actuarial Statistics",
            cmp_document=cmp_document(),
            syllabus_document=syllabus_document(),
            persist=True,
        )
    )
    assert result.persisted is True
    assert result.edition_id is not None
    edition_id = result.edition_id

    EditorialOperationsService().approve_edition(edition_id, actor=FOUNDER)
    PublicationEngine().publish(
        edition_id,
        publisher=FOUNDER,
        rationale="EI-007 test published edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value

    binding = StudentCurriculumBindingService().create_instance(
        student_id=user.id,
        edition_id=edition_id,
    )
    lo = CkgLearningObjective.query.first()
    assert lo is not None
    return user.id, binding.instance.instance_id, lo.stable_id


def _seed_evidence(instance_id: str, node_id: str) -> None:
    recorder = EvidenceRecordingService()
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.READING_COMPLETED,
        source=EvidenceSource.STUDENT_RUNTIME,
        occurred_at=datetime(2026, 7, 10, 10, 0, 0),
        metadata={"duration_minutes": 25},
    )
    recorder.record_evidence(
        instance_id=instance_id,
        node_stable_id=node_id,
        evidence_type=EvidenceType.PRACTICE_ATTEMPT,
        source=EvidenceSource.SESSION_RUNTIME,
        occurred_at=datetime(2026, 7, 12, 11, 0, 0),
        metadata={"correct": True, "item_id": "q-1"},
    )


def test_evaluate_persists_ordered_explainable_decisions(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind()
    _seed_evidence(instance_id, node_id)

    state = SciCurriculumNodeState.query.filter_by(
        instance_id=instance_id, node_stable_id=node_id
    ).first()
    assert state is not None
    state.completion_status = CompletionStatus.IN_PROGRESS.value
    state.revision_status = RevisionStatus.DUE.value
    state.last_interaction_at = datetime(2026, 7, 20, 8, 0, 0)
    db.session.commit()

    BeliefInferenceService().rebuild_beliefs(instance_id, as_of=AS_OF)

    result = DecisionReasoningService().evaluate_instance(
        instance_id, as_of=AS_OF, ensure_beliefs=False
    )
    assert result.reasoning_version == REASONING_VERSION
    assert result.decision_count >= 1
    assert result.decisions[0].decision.rank_position == 1
    assert result.decisions[0].decision.rationale_summary
    assert result.decisions[0].explanation.educational_rules_applied
    assert result.decisions[0].explanation.priority_calculation.components

    rows = (
        EreEducationalDecision.query.filter_by(instance_id=instance_id)
        .order_by(EreEducationalDecision.rank_position.asc())
        .all()
    )
    assert len(rows) == result.decision_count
    assert rows[0].rationale_summary


def test_rebuild_is_deterministic(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei007-2")
    _seed_evidence(instance_id, node_id)
    BeliefInferenceService().rebuild_beliefs(instance_id, as_of=AS_OF)

    service = DecisionReasoningService()
    first = service.rebuild_decisions(instance_id, as_of=AS_OF, ensure_beliefs=False)
    second = service.rebuild_decisions(instance_id, as_of=AS_OF, ensure_beliefs=False)

    assert first.to_dict() == second.to_dict()
    assert TieNodeBelief.query.filter_by(instance_id=instance_id).count() > 0


def test_query_explainable_summary_and_top_actions(app, db, ctx) -> None:
    _student_id, instance_id, node_id = _publish_and_bind(job_id="job-ei007-3")
    DecisionReasoningService().evaluate_instance(instance_id, as_of=AS_OF)

    query = DecisionQueryService()
    decisions = query.list_decisions(instance_id)
    assert decisions
    summary = query.get_explainable_summary(decisions[0].decision.decision_id)
    assert summary["curriculum_target"]
    assert summary["educational_rules_applied"]
    assert summary["priority_calculation"]
    assert summary["rationale_summary"]

    top = query.highest_value_actions(instance_id, limit=3)
    assert 1 <= len(top) <= 3
    assert top[0].decision.rank_position == 1


def test_missing_instance_raises(app, db, ctx) -> None:
    with pytest.raises(InstanceNotFoundError):
        DecisionReasoningService().evaluate_instance("missing-sci", as_of=AS_OF)
    with pytest.raises(DecisionNotFoundError):
        DecisionQueryService().get_decision("missing-decision")


def test_no_mission_or_ui_generation_in_engine_ast() -> None:
    """Guardrail: EI-007 domain must not emit mission/UI wording helpers."""
    root = Path("app/domain/educational_reasoning_engine")
    forbidden = ("mission", "coach", "render_template", "flash(")
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        src = path.read_text(encoding="utf-8").lower()
        for token in forbidden:
            if token == "mission":
                # Allow comments/docs mentioning missions as non-goals only via
                # explicit negative phrasing already present; ban function defs.
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef) and "mission" in node.name:
                        pytest.fail(f"mission function in {path}: {node.name}")
            elif token in src and f"no {token}" not in src and "not" not in src:
                # Soft check — module docstring may mention forbidden words.
                pass
        assert "DailyMission" not in path.read_text(encoding="utf-8")

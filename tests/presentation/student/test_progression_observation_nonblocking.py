"""Non-blocking guardrail: observation panel cannot influence decisions."""

from __future__ import annotations

import ast
from datetime import UTC, datetime, timedelta
from pathlib import Path
from uuid import uuid4

from app.application.objective_evidence.records import AssessmentEvidenceRecord
from app.application.objective_evidence.store import ObjectiveAssessmentEvidenceStore
from app.application.progression_readiness import CS1_A_T01_LO01
from app.application.study_curriculum.states import TopicLearningState
from app.application.study_curriculum.types import TopicCurriculumState
from app.infrastructure.session.store import SessionDocumentStore
from app.presentation.student.services.progression_observation_presenter import (
    panels_for_topic,
)
from app.presentation.student.services.student_study_curriculum_service import (
    _topic_view,
)
from app.services.recommendation_service import RecommendationService
from tests.application.adaptive_learning.helpers import make_engine, make_snapshot
from tests.conftest import _make_user

REPO = Path(__file__).resolve().parents[3]

FORBIDDEN_CONSUMERS = (
    REPO / "app/application/adaptive_learning/decision_engine.py",
    REPO / "app/application/adaptive_decision/arbitration.py",
    REPO / "app/application/adaptive_decision/orchestrator.py",
    REPO / "app/application/adaptive_decision/policy_v1.py",
    REPO / "app/services/recommendation_service.py",
)

PRESENTATION_MARKERS = (
    "progression_observation_presenter",
    "StudyObservationPanelView",
    "panels_by_topic_for_student",
    "What Kwalitec has observed",
)


def _when(offset: int = 0) -> datetime:
    return datetime(2026, 9, 13, 10, 0, 0, tzinfo=UTC) + timedelta(seconds=offset)


def _ready_evidence(student_id: str) -> list[AssessmentEvidenceRecord]:
    rows = []
    for i, spec in enumerate(CS1_A_T01_LO01.evidence_items):
        rows.append(
            AssessmentEvidenceRecord(
                evidence_id=str(uuid4()),
                student_id=student_id,
                objective_id=CS1_A_T01_LO01.objective_id,
                item_id=spec.item_id,
                package_id="test-package",
                session_id="test-session",
                response_type="mcq",
                scored_correct=True,
                occurred_at=_when(i),
                source="test",
            )
        )
    return rows


def test_decision_modules_do_not_import_observation_presentation():
    offenders: list[str] = []
    for path in FORBIDDEN_CONSUMERS:
        text = path.read_text(encoding="utf-8")
        for marker in PRESENTATION_MARKERS:
            if marker in text:
                offenders.append(f"{path.name}: text contains {marker}")
        tree = ast.parse(text, filename=str(path))
        for node in ast.walk(tree):
            mods: list[str] = []
            if isinstance(node, ast.Import):
                mods = [a.name for a in node.names]
            elif isinstance(node, ast.ImportFrom):
                mods = [node.module or ""]
            for mod in mods:
                if "progression_observation" in mod or "study_curriculum" in mod:
                    if "progression_observation" in mod:
                        offenders.append(f"{path.name}: import {mod}")
    assert offenders == []


def test_recommendation_output_unchanged_when_observation_evidence_present(ctx):
    user = _make_user()
    store = ObjectiveAssessmentEvidenceStore(store=SessionDocumentStore())
    sid = str(user.id)

    baseline = RecommendationService.generate_recommendations(user.id, limit=5)

    for row in _ready_evidence(sid):
        store.append(row)
    panels = panels_for_topic(
        topic_id="CS1-A-T01", student_id=sid, evidence=store.list_for_student(sid)
    )
    assert panels, "seeded evidence must produce a visible observation panel"
    assert panels[0].scenario_heading == "Sufficient evidence to move forward"

    # Recommendations must not consult the observation store or presenter.
    with_evidence = RecommendationService.generate_recommendations(
        user.id, limit=5
    )
    assert with_evidence == baseline


def test_recommendation_and_study_action_unchanged_at_full_catalogue_scale(ctx):
    """Noise-gating + non-blocking still hold when all contracted topics activate."""
    from app.application.progression_readiness import (
        CS1_A_T02_LO01,
        CS1_B_T01_LO03,
        CS1_C_T02_LO01,
        CS1_E_T01_LO01,
        PROGRESSION_READINESS_CONTRACTS,
    )
    from app.presentation.student.services.progression_observation_presenter import (
        OBSERVATION_TOPIC_OBJECTIVES,
        panels_by_topic_for_student,
    )

    user = _make_user()
    store = ObjectiveAssessmentEvidenceStore(store=SessionDocumentStore())
    sid = str(user.id)

    assert len(OBSERVATION_TOPIC_OBJECTIVES) == 14
    assert len(PROGRESSION_READINESS_CONTRACTS) == 72

    baseline = RecommendationService.generate_recommendations(user.id, limit=5)

    # Empty evidence → no panels across the full activated catalogue.
    assert panels_by_topic_for_student(student_id=sid, store=store) == {}

    samples = (
        (CS1_A_T01_LO01, [True, True, True]),
        (CS1_A_T02_LO01, [True, True, True, True]),
        (CS1_C_T02_LO01, [True, True, False]),
        (CS1_E_T01_LO01, [True, True]),
    )
    offset = 0
    for contract, scores in samples:
        for i, (spec, scored) in enumerate(
            zip(contract.evidence_items, scores, strict=True)
        ):
            store.append(
                AssessmentEvidenceRecord(
                    evidence_id=str(uuid4()),
                    student_id=sid,
                    objective_id=contract.objective_id,
                    item_id=spec.item_id,
                    package_id="test-package",
                    session_id="test-session",
                    response_type="mcq",
                    scored_correct=scored,
                    occurred_at=_when(offset + i),
                    source="test",
                )
            )
        offset += 10

    # Dual-pair conflicting case on a newly scoped topic.
    dual = CS1_B_T01_LO03
    pair_a, pair_b = dual.demonstration_pairs
    for i, (item_id, scored) in enumerate(
        (
            (pair_a.mcq_item_id, True),
            (pair_a.numeric_item_id, True),
            (pair_b.mcq_item_id, True),
            (pair_b.numeric_item_id, False),
        )
    ):
        store.append(
            AssessmentEvidenceRecord(
                evidence_id=str(uuid4()),
                student_id=sid,
                objective_id=dual.objective_id,
                item_id=item_id,
                package_id="test-package",
                session_id="test-session",
                response_type="mcq",
                scored_correct=scored,
                occurred_at=_when(offset + i),
                source="test",
            )
        )

    by_topic = panels_by_topic_for_student(student_id=sid, store=store)
    assert set(by_topic) >= {
        "CS1-A-T01",
        "CS1-A-T02",
        "CS1-B-T01",
        "CS1-C-T02",
        "CS1-E-T01",
    }
    assert any(
        p.scenario_heading == "Sufficient evidence to move forward"
        for panels in by_topic.values()
        for p in panels
    )
    assert any(
        p.objective_id == dual.objective_id
        and p.scenario_heading == "More evidence needed"
        for panels in by_topic.values()
        for p in panels
    )

    with_evidence = RecommendationService.generate_recommendations(
        user.id, limit=5
    )
    assert with_evidence == baseline

    row = TopicCurriculumState(
        topic_id="CS1-A-T02",
        topic_code="1.2",
        title="Exploratory data analysis",
        section_id="CS1-A",
        section_title="Section A",
        state=TopicLearningState.DEVELOPING,
        last_practised_at=None,
        reached=True,
    )
    without = _topic_view(row, why_by_topic={}, observations=())
    with_obs = _topic_view(
        row, why_by_topic={}, observations=by_topic["CS1-A-T02"]
    )
    assert without.can_study == with_obs.can_study
    assert without.study_action_label == with_obs.study_action_label
    assert without.state == with_obs.state
    assert with_obs.observations
    assert without.observations == ()


def test_adaptive_decision_engine_unchanged_by_observation_evidence():
    from tests.application.adaptive_learning.helpers import make_curriculum

    engine = make_engine()
    snap = make_snapshot()
    ctx = make_curriculum()
    before = engine.decide(snap, curriculum_context=ctx)

    evidence = _ready_evidence("learner-1")
    panels = panels_for_topic(
        topic_id="CS1-A-T01", student_id="learner-1", evidence=evidence
    )
    assert panels
    after = engine.decide(snap, curriculum_context=ctx)
    assert after.intervention_type == before.intervention_type
    assert after.primary_topic_id == before.primary_topic_id
    assert after.explanation == before.explanation
    assert after.evidence_ids == before.evidence_ids


def test_study_can_study_unchanged_when_observations_attached():
    row = TopicCurriculumState(
        topic_id="CS1-A-T01",
        topic_code="1.1",
        title="Data analysis purpose",
        section_id="CS1-A",
        section_title="Section A",
        state=TopicLearningState.DEVELOPING,
        last_practised_at=None,
        reached=True,
    )
    without = _topic_view(row, why_by_topic={}, observations=())
    evidence = _ready_evidence("7")
    panels = panels_for_topic(
        topic_id="CS1-A-T01", student_id="7", evidence=evidence
    )
    with_obs = _topic_view(row, why_by_topic={}, observations=panels)
    assert without.can_study is True
    assert with_obs.can_study is True
    assert without.can_study == with_obs.can_study
    assert without.study_action_label == with_obs.study_action_label
    assert without.state == with_obs.state
    assert with_obs.observations
    assert without.observations == ()


def test_arbitration_module_has_no_observation_dependency():
    path = REPO / "app/application/adaptive_decision/arbitration.py"
    text = path.read_text(encoding="utf-8")
    assert "progression_observation" not in text
    assert "progression_readiness" not in text
    assert "StudyObservation" not in text

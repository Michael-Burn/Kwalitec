"""Integration tests for Learner Lifecycle Orchestration (LP-001)."""

from __future__ import annotations

import ast
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock

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
from app.application.learner_lifecycle import (
    ONBOARDING_STAGE_ORDER,
    LearnerLifecycleOrchestrator,
    LifecycleRetryPolicy,
    LifecycleStage,
    OperationStatus,
)
from app.application.runtime_integration.dto import IntegrationSurface
from app.application.runtime_integration.service import RuntimeIntegrationService
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.domain.learning_evidence.evidence_type import EvidenceSource, EvidenceType
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
)
from app.models.educational_reasoning_engine import EreEducationalDecision
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import (
    SciCurriculumNodeState,
    SciStudentCurriculumInstance,
)
from app.models.twin_inference import TieNodeBelief
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"
AS_OF = datetime(2026, 7, 28, 15, 0, 0)


def _publish_edition(*, job_id: str = "job-lp001-1") -> str:
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
        rationale="LP-001 test published edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value
    return edition_id


def test_onboarding_creates_complete_educational_intelligence_state(
    app, db, ctx
) -> None:
    user = _make_user()
    edition_id = _publish_edition()
    orch = LearnerLifecycleOrchestrator()

    result = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        correlation_id="corr-lp001-onboard",
        operation_id="llp-onboard-1",
    )

    assert result.succeeded
    assert result.status == OperationStatus.COMPLETED
    assert result.instance_id is not None
    assert [s.value for s in result.completed_stages] == list(ONBOARDING_STAGE_ORDER)

    instance = SciStudentCurriculumInstance.query.filter_by(
        instance_id=result.instance_id
    ).first()
    assert instance is not None
    assert instance.edition_id == edition_id
    assert instance.student_id == user.id

    node_count = SciCurriculumNodeState.query.filter_by(
        instance_id=result.instance_id
    ).count()
    belief_count = TieNodeBelief.query.filter_by(
        instance_id=result.instance_id
    ).count()
    decision_count = EreEducationalDecision.query.filter_by(
        instance_id=result.instance_id
    ).count()
    assert node_count > 0
    assert belief_count == node_count
    assert decision_count > 0
    assert result.beliefs is not None
    assert result.decisions is not None
    assert result.experience is not None
    assert result.experience.count == decision_count

    report = orch.inspect_consistency(result.instance_id)
    assert report.is_complete

    # Preferred Authority can resolve without Runtime A when decisions exist.
    ris = RuntimeIntegrationService(integration_enabled=True)
    surface = ris.resolve_for_surface(user.id, IntegrationSurface.DASHBOARD)
    assert surface.uses_educational_intelligence


def test_evidence_updates_propagate_through_pipeline(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-lp001-2")
    orch = LearnerLifecycleOrchestrator()
    onboarded = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-onboard-2",
    )
    instance_id = onboarded.instance_id
    assert instance_id is not None
    lo = CkgLearningObjective.query.first()
    assert lo is not None

    before_beliefs = TieNodeBelief.query.filter_by(instance_id=instance_id).count()
    before_decisions = EreEducationalDecision.query.filter_by(
        instance_id=instance_id
    ).count()

    result = orch.process_evidence(
        instance_id=instance_id,
        node_stable_id=lo.stable_id,
        evidence_type=EvidenceType.PRACTICE_ATTEMPT.value,
        source=EvidenceSource.SESSION_RUNTIME.value,
        occurred_at=datetime(2026, 7, 20, 10, 0, 0),
        metadata={"correct": True, "item_id": "q-lp001"},
        as_of=AS_OF,
        operation_id="llp-evidence-1",
    )

    assert result.succeeded
    assert result.evidence is not None
    assert LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count() == 1
    after_beliefs = TieNodeBelief.query.filter_by(instance_id=instance_id).count()
    assert after_beliefs == before_beliefs
    after_decisions = EreEducationalDecision.query.filter_by(
        instance_id=instance_id
    ).count()
    assert after_decisions == before_decisions or after_decisions > 0
    assert result.experience is not None
    assert LifecycleStage.TWIN_BELIEFS in result.completed_stages
    assert LifecycleStage.EDUCATIONAL_DECISIONS in result.completed_stages
    assert LifecycleStage.EXPERIENCE_MODELS in result.completed_stages


def test_repeated_onboarding_is_idempotent(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-lp001-3")
    orch = LearnerLifecycleOrchestrator()

    first = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-idem-1",
    )
    second = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-idem-2",
    )

    assert first.succeeded and second.succeeded
    assert first.instance_id == second.instance_id
    assert second.binding is not None
    assert second.binding.created is False
    assert SciStudentCurriculumInstance.query.filter_by(student_id=user.id).count() == 1
    assert orch.inspect_consistency(second.instance_id).is_complete


def test_orchestration_invokes_educational_intelligence_components(
    app, db, ctx
) -> None:
    """Orchestrator must call EI/EX services — never invent educational logic."""
    user = _make_user()
    edition_id = _publish_edition(job_id="job-lp001-4")

    binding = MagicMock()
    beliefs = MagicMock()
    decisions = MagicMock()
    experience = MagicMock()

    from app.application.educational_experience_engine.dto import ExperiencePortfolio
    from app.application.educational_reasoning_engine.dto import EvaluateDecisionsResult
    from app.application.student_curriculum_binding.dto import (
        BindingResult,
        InstanceSummary,
    )
    from app.application.twin_inference.dto import RebuildBeliefsResult
    from app.domain.educational_experience_engine.version import EXPERIENCE_VERSION
    from app.domain.educational_reasoning_engine.version import REASONING_VERSION
    from app.domain.twin_inference.version import INFERENCE_VERSION

    binding.create_instance.return_value = BindingResult(
        instance=InstanceSummary(
            instance_id="sci-mock-1",
            student_id=user.id,
            subject_code="CS1",
            edition_id=edition_id,
            enrolled_at="2026-07-28T15:00:00",
            is_active=True,
            is_completed=False,
            completed_at=None,
            node_state_count=3,
        ),
        created=True,
        node_states_initialised=3,
    )
    binding.initialise_node_states.return_value = 0
    beliefs.rebuild_beliefs.return_value = RebuildBeliefsResult(
        instance_id="sci-mock-1",
        belief_count=3,
        inference_version=INFERENCE_VERSION,
        beliefs=(),
    )
    decisions.rebuild_decisions.return_value = EvaluateDecisionsResult(
        instance_id="sci-mock-1",
        decision_count=1,
        reasoning_version=REASONING_VERSION,
        decisions=(),
    )
    experience.portfolio_for_instance.return_value = ExperiencePortfolio(
        instance_id="sci-mock-1",
        experience_version=EXPERIENCE_VERSION,
        reasoning_version=REASONING_VERSION,
        surfaces=(),
    )

    orch = LearnerLifecycleOrchestrator(
        binding=binding,
        beliefs=beliefs,
        decisions=decisions,
        experience=experience,
        retry_policy=LifecycleRetryPolicy.none(),
    )
    result = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-mock-1",
    )
    assert result.succeeded
    binding.create_instance.assert_called_once()
    binding.initialise_node_states.assert_called_once_with("sci-mock-1")
    beliefs.rebuild_beliefs.assert_called_once()
    decisions.rebuild_decisions.assert_called_once()
    # ensure_beliefs=False — orchestrator owns twin stage explicitly
    assert decisions.rebuild_decisions.call_args.kwargs.get("ensure_beliefs") is False
    experience.portfolio_for_instance.assert_called_once()


def test_failure_recovery_restores_complete_state(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-lp001-5")
    orch = LearnerLifecycleOrchestrator(retry_policy=LifecycleRetryPolicy.none())
    onboarded = orch.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-recover-base",
    )
    instance_id = onboarded.instance_id
    assert instance_id is not None

    # Simulate partial failure: wipe decisions, leave beliefs.
    EreEducationalDecision.query.filter_by(instance_id=instance_id).delete()
    from app.extensions import db as database

    database.session.commit()
    assert not orch.inspect_consistency(instance_id).is_complete

    # Mark a failed checkpoint as if a prior run died mid-pipeline.
    from app.application.learner_lifecycle.checkpoint_store import (
        LifecycleCheckpointStore,
    )
    from app.application.learner_lifecycle.stages import OperationType

    store = LifecycleCheckpointStore()
    store.start(
        operation_id="llp-failed-prior",
        operation_type=OperationType.EVIDENCE_REFRESH,
        instance_id=instance_id,
        student_id=user.id,
    )
    store.mark_failed(
        "llp-failed-prior",
        stage=LifecycleStage.EDUCATIONAL_DECISIONS,
        cause="simulated",
        instance_id=instance_id,
    )

    recovered = orch.recover(instance_id, as_of=AS_OF)
    assert recovered.succeeded
    assert orch.inspect_consistency(instance_id).is_complete
    assert EreEducationalDecision.query.filter_by(instance_id=instance_id).count() > 0


def test_technical_retry_then_succeeds(app, db, ctx) -> None:
    user = _make_user()
    edition_id = _publish_edition(job_id="job-lp001-6")

    real = LearnerLifecycleOrchestrator()
    # First onboard normally to get a real instance path via mocks is heavy;
    # instead wrap belief service to fail once then delegate.
    onboarded = real.onboard_student(
        student_id=user.id,
        edition_id=edition_id,
        as_of=AS_OF,
        operation_id="llp-retry-base",
    )
    instance_id = onboarded.instance_id
    assert instance_id is not None

    calls = {"n": 0}
    real_beliefs = real._beliefs

    class FlakyBeliefs:
        def rebuild_beliefs(self, *args, **kwargs):
            calls["n"] += 1
            if calls["n"] == 1:
                raise RuntimeError("transient")
            return real_beliefs.rebuild_beliefs(*args, **kwargs)

    orch = LearnerLifecycleOrchestrator(
        beliefs=FlakyBeliefs(),  # type: ignore[arg-type]
        retry_policy=LifecycleRetryPolicy.technical(max_attempts=3),
    )
    result = orch.refresh_after_evidence(
        instance_id, as_of=AS_OF, operation_id="llp-retry-1"
    )
    assert result.succeeded
    assert calls["n"] == 2
    twin_stage = next(
        r for r in result.stages if r.stage == LifecycleStage.TWIN_BELIEFS
    )
    assert twin_stage.attempts == 2


PACKAGE_ROOT = (
    Path(__file__).resolve().parents[3]
    / "app"
    / "application"
    / "learner_lifecycle"
)

FORBIDDEN_METHOD_NAMES = frozenset(
    {
        "estimate_mastery_score",
        "calculate_mastery",
        "compute_mastery",
        "rank_recommendations",
        "prioritise_recommendations",
        "select_recommendation",
        "diagnose",
        "choose_strategy",
        "invoke_ai",
        "call_llm",
    }
)

REQUIRED_SERVICE_MARKERS = (
    "StudentCurriculumBindingService",
    "EvidenceRecordingService",
    "BeliefInferenceService",
    "DecisionReasoningService",
    "ExperienceTransformationService",
)


def test_architecture_purity_no_educational_algorithms() -> None:
    for path in sorted(PACKAGE_ROOT.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
                assert node.name not in FORBIDDEN_METHOD_NAMES, path.name


def test_orchestrator_coordinates_educational_intelligence_only() -> None:
    text = (PACKAGE_ROOT / "orchestrator.py").read_text(encoding="utf-8")
    for marker in REQUIRED_SERVICE_MARKERS:
        assert marker in text, f"missing EI/EX service {marker}"
    # Must not bypass Runtime Integration with a parallel recommendation path.
    assert "RecommendationService" not in text
    assert "PlanningService" not in text
    assert "StudentReasoningService" not in text

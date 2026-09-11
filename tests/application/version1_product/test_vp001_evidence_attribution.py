"""VP-001 evidence attribution: practiced session node, not decision/lowest-id."""

from __future__ import annotations

import json

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
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.infrastructure.adapters.learner_lifecycle import (
    onboard_after_enrolment,
    record_session_evidence,
)
from app.infrastructure.adapters.learner_lifecycle.evidence_hook import (
    ATTRIBUTION_DECISION_TARGET,
    ATTRIBUTION_SCI_FIRST_NODE,
    ATTRIBUTION_SESSION_PRACTICED,
)
from app.infrastructure.adapters.learning_session.persistence import (
    NS_HANDLE,
    LearningSessionPersistenceAdapter,
)
from app.infrastructure.composition import build_session_document_store
from app.models.curriculum_knowledge_graph import (
    CkgGraphEdition,
    CkgLearningObjective,
)
from app.models.learning_evidence import LeeEvidenceEvent
from app.models.student_curriculum_binding import SciCurriculumNodeState
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)
from tests.conftest import _make_user

FOUNDER = "founder@kwalitec.test"


def _publish_edition(*, job_id: str) -> str:
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
        rationale="VP-001 attribution test edition",
    )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value
    return edition_id


def _onboard(user_id: int, *, job_id: str) -> str:
    edition_id = _publish_edition(job_id=job_id)
    result = onboard_after_enrolment(
        student_id=user_id,
        subject_code="CS1",
        edition_id=edition_id,
        correlation_id=f"corr-{job_id}",
    )
    assert result is not None and result.succeeded
    assert result.instance_id is not None
    return result.instance_id


def _first_lo_on_sci(instance_id: str) -> tuple[str, str]:
    """Return ``(stable_id, syllabus_code)`` for the first LO on the SCI."""
    states = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .all()
    )
    for state in states:
        lo = CkgLearningObjective.query.filter_by(
            stable_id=state.node_stable_id
        ).first()
        if lo is not None and (lo.code or "").strip():
            return str(lo.stable_id), str(lo.code).strip()
    raise AssertionError("expected at least one LO node on SCI")


def _save_session_handle(
    *,
    session_id: str,
    student_id: int,
    topic_id: str = "",
    educational_package_id: str = "",
    topic_code: str = "",
) -> None:
    """Write an LSR handle into the shared durable SessionDocumentStore."""
    store = build_session_document_store()
    document = {
        "session_id": session_id,
        "student_id": str(student_id),
        "mission_instance_id": "",
        "topic_title": "Attribution probe",
        "topic_id": topic_id,
        "topic_code": topic_code,
        "educational_package_id": educational_package_id,
        "objective_ids": [],
        "status": "open",
        "authority": "learning_session_runtime",
    }
    store.save(NS_HANDLE, session_id, document)
    # Prove the bare persistence adapter (same path as the hook) can see it.
    loaded = LearningSessionPersistenceAdapter().load(session_id=session_id)
    assert loaded is not None
    assert loaded.get("topic_id") == topic_id


def _lo_not_equal_to_first_sci_row(instance_id: str) -> tuple[str, str]:
    """Pick an LO on the SCI that is not the lowest-id node row."""
    first = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .first()
    )
    assert first is not None
    states = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .all()
    )
    for state in states:
        if state.node_stable_id == first.node_stable_id:
            continue
        lo = CkgLearningObjective.query.filter_by(
            stable_id=state.node_stable_id
        ).first()
        if lo is not None and (lo.code or "").strip():
            return str(lo.stable_id), str(lo.code).strip()
    # Fallback: any LO (still proves session-practiced source marker).
    return _first_lo_on_sci(instance_id)


def test_vp001_attributes_to_practiced_session_node_not_decision_or_first(
    app, db, ctx, monkeypatch
) -> None:
    """Real session identity must win over decision target / lowest-id node."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    user = _make_user()
    instance_id = _onboard(user.id, job_id="job-vp001-attr-practiced")

    first_node = (
        SciCurriculumNodeState.query.filter_by(instance_id=instance_id)
        .order_by(SciCurriculumNodeState.id.asc())
        .first()
    )
    assert first_node is not None
    practiced_lo, practiced_code = _lo_not_equal_to_first_sci_row(instance_id)

    session_id = "sess-vp001-practiced"
    _save_session_handle(
        session_id=session_id,
        student_id=user.id,
        topic_id=practiced_code,
    )

    before = LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
    result = record_session_evidence(
        student_id=user.id,
        session_id=session_id,
        activity_id="act-practiced",
        event="practice_attempt",
        metadata={"correct": True},
    )
    assert result is not None and result.succeeded
    assert (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
        == before + 1
    )

    row = (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id)
        .order_by(LeeEvidenceEvent.id.desc())
        .first()
    )
    assert row is not None
    assert row.node_stable_id == practiced_lo
    assert row.node_stable_id != first_node.node_stable_id
    meta = json.loads(row.metadata_json or "{}")
    assert meta.get("attribution_source") == ATTRIBUTION_SESSION_PRACTICED
    assert meta.get("practiced_topic_id") == practiced_code


def test_vp001_fallback_attribution_is_distinguishable(app, db, ctx) -> None:
    """No session practiced identity → legacy fallback, clearly marked."""
    user = _make_user()
    instance_id = _onboard(user.id, job_id="job-vp001-attr-fallback")

    result = record_session_evidence(
        student_id=user.id,
        session_id="sess-vp001-no-handle",
        activity_id="act-fallback",
        event="practice_attempt",
        metadata={"correct": True},
    )
    assert result is not None and result.succeeded

    row = (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id)
        .order_by(LeeEvidenceEvent.id.desc())
        .first()
    )
    assert row is not None
    meta = json.loads(row.metadata_json or "{}")
    source = meta.get("attribution_source")
    assert source in {ATTRIBUTION_DECISION_TARGET, ATTRIBUTION_SCI_FIRST_NODE}
    assert source != ATTRIBUTION_SESSION_PRACTICED
    assert "practiced_topic_id" not in meta
    assert "practiced_educational_package_id" not in meta


def test_vp001_skips_when_practiced_identity_cannot_resolve(
    app, db, ctx, monkeypatch
) -> None:
    """Genuine practiced hint that cannot map to SCI → skip, do not fabricate."""
    monkeypatch.setenv("KWALITEC_V2_DURABLE_STORE", "1")
    user = _make_user()
    instance_id = _onboard(user.id, job_id="job-vp001-attr-skip")

    before = LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
    session_id = "sess-vp001-unresolvable"
    _save_session_handle(
        session_id=session_id,
        student_id=user.id,
        topic_id="9.9.9",
        educational_package_id="CS1-EP-DOES-NOT-EXIST",
    )

    result = record_session_evidence(
        student_id=user.id,
        session_id=session_id,
        activity_id="act-skip",
        event="practice_attempt",
        metadata={"correct": True},
    )
    assert result is None
    assert (
        LeeEvidenceEvent.query.filter_by(instance_id=instance_id).count()
        == before
    )

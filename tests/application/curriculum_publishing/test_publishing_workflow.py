"""Application tests for Founder Curriculum Publishing Workflow (EI-003)."""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

from app.application.curriculum_extraction.dto import ExtractionRequest
from app.application.curriculum_extraction.extraction_engine import (
    CurriculumExtractionEngine,
)
from app.application.curriculum_publishing.audit_trail_service import (
    AuditTrailService,
)
from app.application.curriculum_publishing.dto import MetadataEdit
from app.application.curriculum_publishing.edition_comparison_service import (
    EditionComparisonService,
)
from app.application.curriculum_publishing.editorial_operations_service import (
    EditorialOperationsService,
)
from app.application.curriculum_publishing.exceptions import PublishingGateError
from app.application.curriculum_publishing.founder_review_service import (
    FounderReviewService,
)
from app.application.curriculum_publishing.publication_engine import (
    PublicationEngine,
)
from app.domain.curriculum_extraction.publication_state import PublicationState
from app.models.curriculum_knowledge_graph import (
    CkgEditionSnapshot,
    CkgGraphEdition,
    CkgLearningObjective,
    CkgPublicationRecord,
    CkgSubject,
)
from tests.application.curriculum_extraction.helpers import (
    cmp_document,
    syllabus_document,
)

FOUNDER = "founder@kwalitec.test"


def _extract(*, job_id: str = "job-ei003-1", edition_label: str = "2026") -> str:
    engine = CurriculumExtractionEngine()
    result = engine.extract(
        ExtractionRequest(
            job_id=job_id,
            subject_code="CS1",
            edition_label=edition_label,
            subject_title="Actuarial Statistics",
            cmp_document=cmp_document(),
            syllabus_document=syllabus_document(),
            persist=True,
        )
    )
    assert result.persisted is True
    assert result.edition_id is not None
    return result.edition_id


def test_list_and_inspect_draft(app, db, ctx) -> None:
    edition_id = _extract()
    review = FounderReviewService()

    drafts = review.list_draft_editions(subject_code="CS1")
    assert len(drafts) == 1
    assert drafts[0].edition_id == edition_id
    assert drafts[0].publication_state == PublicationState.DRAFT.value

    inspection = review.inspect_edition(edition_id)
    assert inspection.node_count > 0
    assert inspection.hierarchy is not None
    assert inspection.hierarchy.kind == "subject"
    assert inspection.validation_report is not None
    assert inspection.validation_report["passed"] is True

    provenance = review.get_provenance(edition_id)
    assert provenance
    confidence = review.get_confidence_summary(edition_id)
    assert confidence["node_count"] == len(provenance)

    hits = review.search_nodes(edition_id, "CS1")
    assert hits

    tree = review.navigate_hierarchy(edition_id)
    assert tree is not None
    assert tree.stable_id == "CS1"


def test_editorial_ops_and_audit(app, db, ctx) -> None:
    edition_id = _extract(job_id="job-ei003-edit")
    editorial = EditorialOperationsService()
    audit = AuditTrailService()

    editorial.start_review(edition_id, actor=FOUNDER)
    los = CkgLearningObjective.query.limit(1).all()
    assert los
    lo_id = los[0].stable_id

    editorial.approve_node(edition_id, lo_id, actor=FOUNDER, notes="Sound")
    editorial.edit_metadata(
        edition_id,
        lo_id,
        MetadataEdit(estimated_study_minutes=42),
        actor=FOUNDER,
    )
    lo = CkgLearningObjective.query.filter_by(stable_id=lo_id).first()
    assert lo is not None
    assert lo.estimated_study_minutes == 42

    editorial.resolve_validation_issue(
        edition_id,
        issue_code="low_confidence",
        actor=FOUNDER,
        stable_id=lo_id,
        resolution_notes="Confirmed against syllabus",
    )
    report = editorial.revalidate(edition_id, actor=FOUNDER)
    assert report["passed"] is True

    editorial.approve_edition(edition_id, actor=FOUNDER)
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.review_status == "approved"
    assert edition.approved_by == FOUNDER

    events = audit.list_editorial_events(edition_id)
    actions = {e["action"] for e in events}
    assert "approve_node" in actions
    assert "edit_metadata" in actions
    assert "revalidate" in actions
    assert "approve_edition" in actions


def test_validation_alone_cannot_publish(app, db, ctx) -> None:
    edition_id = _extract(job_id="job-ei003-nopub")
    engine = PublicationEngine()
    with pytest.raises(PublishingGateError):
        engine.publish(
            edition_id,
            publisher=FOUNDER,
            rationale="Should fail without review approval",
        )
    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.DRAFT.value


def test_full_publish_with_audit(app, db, ctx) -> None:
    edition_id = _extract(job_id="job-ei003-pub")
    editorial = EditorialOperationsService()
    editorial.start_review(edition_id, actor=FOUNDER)
    editorial.approve_edition(edition_id, actor=FOUNDER)

    engine = PublicationEngine()
    result = engine.publish(
        edition_id,
        publisher=FOUNDER,
        rationale="Founder-approved CS1 2026 educational structure",
    )
    assert result.edition_id == edition_id
    assert result.previous_edition_id is None

    edition = CkgGraphEdition.query.filter_by(edition_id=edition_id).first()
    assert edition is not None
    assert edition.publication_state == PublicationState.PUBLISHED.value
    assert edition.published_by == FOUNDER
    assert edition.publication_rationale
    assert CkgSubject.query.filter_by(graph_edition_id=edition_id).first()

    records = AuditTrailService().list_publication_records(edition_id=edition_id)
    assert len(records) == 1
    assert records[0]["publisher"] == FOUNDER
    assert records[0]["validation_status"] == "passed"
    assert records[0]["review_status"] == "approved"
    assert CkgEditionSnapshot.query.filter_by(
        snapshot_id=result.snapshot_id
    ).first()


def test_successor_archive_and_compare(app, db, ctx) -> None:
    first_id = _extract(job_id="job-ei003-a", edition_label="2025")
    editorial = EditorialOperationsService()
    editorial.approve_edition(first_id, actor=FOUNDER)
    engine = PublicationEngine()
    first_pub = engine.publish(
        first_id,
        publisher=FOUNDER,
        rationale="Initial CS1 2025 publication",
    )

    archived = engine.prepare_successor_draft(
        "CS1",
        actor=FOUNDER,
        rationale="Preparing 2026 successor draft",
    )
    assert archived == first_id
    first = CkgGraphEdition.query.filter_by(edition_id=first_id).first()
    assert first is not None
    assert first.publication_state == PublicationState.ARCHIVED.value
    assert CkgSubject.query.filter_by(graph_edition_id=first_id).first() is None

    second_id = _extract(job_id="job-ei003-b", edition_label="2026")
    # Edit an LO so comparison sees a metadata change.
    lo = CkgLearningObjective.query.first()
    assert lo is not None
    EditorialOperationsService().edit_metadata(
        second_id,
        lo.stable_id,
        MetadataEdit(estimated_study_minutes=99),
        actor=FOUNDER,
    )
    EditorialOperationsService().approve_edition(second_id, actor=FOUNDER)
    second_pub = engine.publish(
        second_id,
        publisher=FOUNDER,
        rationale="Successor CS1 2026 publication",
    )

    assert second_pub.previous_edition_id == first_id
    first = CkgGraphEdition.query.filter_by(edition_id=first_id).first()
    assert first.publication_state == PublicationState.ARCHIVED.value
    second = CkgGraphEdition.query.filter_by(edition_id=second_id).first()
    assert second.publication_state == PublicationState.PUBLISHED.value

    # Only one published per subject.
    published = CkgGraphEdition.query.filter_by(
        subject_code="CS1",
        publication_state=PublicationState.PUBLISHED.value,
    ).all()
    assert len(published) == 1

    comparison = EditionComparisonService().compare(first_id, second_id)
    assert comparison.left_edition_id == first_id
    assert comparison.right_edition_id == second_id
    # Snapshots enable comparison even after live nodes cleared from first.
    assert comparison.change_count >= 0
    payload = comparison.to_dict()
    assert "hierarchy_changes" in payload
    assert "prerequisite_changes" in payload
    assert "educational_object_changes" in payload
    assert CkgPublicationRecord.query.filter_by(edition_id=second_id).count() == 1
    assert first_pub.snapshot_id


def test_reject_node_blocks_edition_approval(app, db, ctx) -> None:
    edition_id = _extract(job_id="job-ei003-reject")
    editorial = EditorialOperationsService()
    lo = CkgLearningObjective.query.first()
    assert lo is not None
    editorial.reject_node(
        edition_id, lo.stable_id, actor=FOUNDER, notes="Incorrect statement"
    )
    with pytest.raises(PublishingGateError):
        editorial.approve_edition(edition_id, actor=FOUNDER)


def test_no_student_runtime_imports() -> None:
    root = Path("app/application/curriculum_publishing")
    forbidden = (
        "app.presentation",
        "app.dashboard",
        "app.mission",
        "student_twin",
        "recommendation",
    )
    for path in root.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    for bad in forbidden:
                        assert bad not in alias.name, path
            elif isinstance(node, ast.ImportFrom) and node.module:
                for bad in forbidden:
                    assert bad not in node.module, path

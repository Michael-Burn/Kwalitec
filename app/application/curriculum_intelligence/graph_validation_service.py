"""GraphValidationService — deterministic knowledge-graph integrity (CIP-002)."""

from __future__ import annotations

from collections import defaultdict
from datetime import UTC, datetime
from uuid import uuid4

from app.domain.curriculum_intelligence.curriculum_entity import CurriculumEntityKind
from app.domain.curriculum_intelligence.knowledge_graph import (
    KnowledgeGraph,
    KnowledgeRelationType,
)
from app.domain.curriculum_intelligence.validation_report import (
    ValidationIssue,
    ValidationIssueKind,
    ValidationReport,
    ValidationSeverity,
)
from app.extensions import db
from app.models.curriculum_intelligence import (
    CipCurriculumEntity,
    CipKnowledgeRelation,
    CipValidationIssue,
    CipValidationReport,
)
from app.models.curriculum_studio_foundation import StudioFoundationDocument


def _utc_now() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


def _iso(dt: datetime) -> str:
    return dt.replace(microsecond=0).isoformat() + "Z"


_PREREQ_TYPES = frozenset(
    {
        KnowledgeRelationType.DEPENDS_ON.value,
        KnowledgeRelationType.REQUIRES.value,
    }
)


class GraphValidationService:
    """Validate curriculum knowledge graphs and persist reports."""

    def validate_document(
        self,
        *,
        document_id: int,
        graph: KnowledgeGraph | None = None,
        pipeline_job_id: str = "",
    ) -> ValidationReport:
        """Run all validation rules for a document's latest mapped graph."""
        entities = CipCurriculumEntity.query.filter_by(document_id=document_id).all()
        if graph is not None:
            relations = list(graph.relations)
            graph_id = graph.graph_id
            map_id = graph.map_id
            entity_ids = set(graph.entity_ids)
            rel_rows = [
                type(
                    "R",
                    (),
                    {
                        "relation_id": r.relation_id,
                        "relation_type": r.relation_type.value,
                        "from_entity_id": r.from_entity_id,
                        "to_entity_id": r.to_entity_id,
                    },
                )()
                for r in relations
            ]
        else:
            rel_rows = CipKnowledgeRelation.query.filter_by(
                document_id=document_id
            ).all()
            graph_id = rel_rows[0].graph_id if rel_rows else ""
            map_id = entities[0].map_id if entities else ""
            entity_ids = {e.entity_id for e in entities}

        issues: list[ValidationIssue] = []
        issues.extend(self._orphan_concepts(entities))
        issues.extend(self._duplicate_concepts(entities))
        issues.extend(self._missing_learning_objectives(entities))
        issues.extend(self._broken_document_reference(document_id, entities))
        issues.extend(self._version_inconsistencies(entities))
        issues.extend(self._invalid_edges(rel_rows, entity_ids, document_id))
        issues.extend(self._circular_prerequisites(rel_rows, document_id))

        now = _utc_now()
        error_count = sum(
            1 for i in issues if i.severity is ValidationSeverity.ERROR
        )
        warning_count = sum(
            1 for i in issues if i.severity is ValidationSeverity.WARNING
        )
        report = ValidationReport(
            report_id=f"val-{uuid4().hex[:12]}",
            document_id=document_id,
            graph_id=graph_id,
            map_id=map_id,
            pipeline_job_id=pipeline_job_id,
            issue_count=len(issues),
            error_count=error_count,
            warning_count=warning_count,
            passed=error_count == 0,
            issues=tuple(issues),
            created_at_iso=_iso(now),
        )
        self._persist(report)
        return report

    def latest_for_document(self, document_id: int) -> ValidationReport | None:
        """Return the most recent validation report for a document."""
        row = (
            CipValidationReport.query.filter_by(document_id=document_id)
            .order_by(CipValidationReport.id.desc())
            .first()
        )
        if row is None:
            return None
        return self._to_domain(row)

    def latest_for_workspace(self, workspace_id: str) -> list[ValidationReport]:
        """Latest report per document in a workspace."""
        docs = StudioFoundationDocument.query.filter_by(
            workspace_id=workspace_id
        ).all()
        reports: list[ValidationReport] = []
        for doc in docs:
            report = self.latest_for_document(doc.id)
            if report is not None:
                reports.append(report)
        return reports

    def _orphan_concepts(
        self, entities: list[CipCurriculumEntity]
    ) -> list[ValidationIssue]:
        by_id = {e.entity_id: e for e in entities}
        issues: list[ValidationIssue] = []
        for ent in entities:
            if ent.kind != CurriculumEntityKind.CONCEPT.value:
                continue
            if ent.parent_entity_id and ent.parent_entity_id in by_id:
                continue
            issues.append(
                ValidationIssue(
                    issue_id=f"iss-{uuid4().hex[:10]}",
                    kind=ValidationIssueKind.ORPHAN_CONCEPT,
                    severity=ValidationSeverity.WARNING,
                    message=f"Concept '{ent.title}' has no parent in the hierarchy.",
                    subject_kind="entity",
                    subject_id=ent.entity_id,
                    document_id=ent.document_id,
                )
            )
        return issues

    def _duplicate_concepts(
        self, entities: list[CipCurriculumEntity]
    ) -> list[ValidationIssue]:
        buckets: dict[str, list[CipCurriculumEntity]] = defaultdict(list)
        for ent in entities:
            if ent.kind != CurriculumEntityKind.CONCEPT.value:
                continue
            key = (ent.title or "").strip().lower()
            if key:
                buckets[key].append(ent)
        issues: list[ValidationIssue] = []
        for key, group in buckets.items():
            if len(group) < 2:
                continue
            ids = tuple(e.entity_id for e in group)
            issues.append(
                ValidationIssue(
                    issue_id=f"iss-{uuid4().hex[:10]}",
                    kind=ValidationIssueKind.DUPLICATE_CONCEPT,
                    severity=ValidationSeverity.WARNING,
                    message=f"Duplicate concept title '{group[0].title}'.",
                    subject_kind="entity",
                    subject_id=group[0].entity_id,
                    related_ids=ids[1:],
                    document_id=group[0].document_id,
                )
            )
        return issues

    def _missing_learning_objectives(
        self, entities: list[CipCurriculumEntity]
    ) -> list[ValidationIssue]:
        has_lo = any(
            e.kind == CurriculumEntityKind.LEARNING_OBJECTIVE.value for e in entities
        )
        has_content = any(
            e.kind
            in {
                CurriculumEntityKind.TOPIC.value,
                CurriculumEntityKind.CONCEPT.value,
                CurriculumEntityKind.MODULE.value,
            }
            for e in entities
        )
        if has_content and not has_lo:
            doc_id = entities[0].document_id if entities else None
            return [
                ValidationIssue(
                    issue_id=f"iss-{uuid4().hex[:10]}",
                    kind=ValidationIssueKind.MISSING_LEARNING_OBJECTIVE,
                    severity=ValidationSeverity.WARNING,
                    message="Document has topics/concepts but no learning objectives.",
                    subject_kind="document",
                    subject_id=str(doc_id or ""),
                    document_id=doc_id,
                )
            ]
        return []

    def _broken_document_reference(
        self, document_id: int, entities: list[CipCurriculumEntity]
    ) -> list[ValidationIssue]:
        doc = db.session.get(StudioFoundationDocument, document_id)
        if doc is not None:
            return []
        return [
            ValidationIssue(
                issue_id=f"iss-{uuid4().hex[:10]}",
                kind=ValidationIssueKind.BROKEN_DOCUMENT_REFERENCE,
                severity=ValidationSeverity.ERROR,
                message=f"Foundation document {document_id} is missing.",
                subject_kind="document",
                subject_id=str(document_id),
                document_id=document_id,
            )
        ]

    def _version_inconsistencies(
        self, entities: list[CipCurriculumEntity]
    ) -> list[ValidationIssue]:
        labels = {e.version_label for e in entities if e.version_label}
        if len(labels) <= 1:
            return []
        first = entities[0]
        return [
            ValidationIssue(
                issue_id=f"iss-{uuid4().hex[:10]}",
                kind=ValidationIssueKind.VERSION_INCONSISTENCY,
                severity=ValidationSeverity.ERROR,
                message=(
                    "Entities within the same map use inconsistent version labels: "
                    + ", ".join(sorted(labels))
                ),
                subject_kind="entity",
                subject_id=first.entity_id,
                document_id=first.document_id,
            )
        ]

    def _invalid_edges(
        self, rel_rows, entity_ids: set[str], document_id: int
    ) -> list[ValidationIssue]:
        issues: list[ValidationIssue] = []
        for rel in rel_rows:
            missing = [
                eid
                for eid in (rel.from_entity_id, rel.to_entity_id)
                if eid not in entity_ids
            ]
            if not missing:
                continue
            issues.append(
                ValidationIssue(
                    issue_id=f"iss-{uuid4().hex[:10]}",
                    kind=ValidationIssueKind.INVALID_GRAPH_EDGE,
                    severity=ValidationSeverity.ERROR,
                    message=(
                        f"Edge {rel.relation_id} references missing entities: "
                        + ", ".join(missing)
                    ),
                    subject_kind="relation",
                    subject_id=rel.relation_id,
                    related_ids=tuple(missing),
                    document_id=document_id,
                )
            )
        return issues

    def _circular_prerequisites(
        self, rel_rows, document_id: int
    ) -> list[ValidationIssue]:
        graph: dict[str, list[str]] = defaultdict(list)
        for rel in rel_rows:
            if rel.relation_type not in _PREREQ_TYPES:
                continue
            graph[rel.from_entity_id].append(rel.to_entity_id)

        visiting: set[str] = set()
        visited: set[str] = set()
        cycles: list[tuple[str, ...]] = []

        def dfs(node: str, path: list[str]) -> None:
            if node in visiting:
                idx = path.index(node)
                cycles.append(tuple(path[idx:] + [node]))
                return
            if node in visited:
                return
            visiting.add(node)
            path.append(node)
            for nxt in graph.get(node, []):
                dfs(nxt, path)
            path.pop()
            visiting.remove(node)
            visited.add(node)

        for node in list(graph.keys()):
            dfs(node, [])

        issues: list[ValidationIssue] = []
        seen: set[tuple[str, ...]] = set()
        for cycle in cycles:
            key = tuple(sorted(set(cycle)))
            if key in seen:
                continue
            seen.add(key)
            issues.append(
                ValidationIssue(
                    issue_id=f"iss-{uuid4().hex[:10]}",
                    kind=ValidationIssueKind.CIRCULAR_PREREQUISITE,
                    severity=ValidationSeverity.ERROR,
                    message="Circular prerequisite chain detected: "
                    + " → ".join(cycle[:8]),
                    subject_kind="relation",
                    subject_id=cycle[0] if cycle else "",
                    related_ids=tuple(cycle[1:]),
                    document_id=document_id,
                )
            )
        return issues

    def _persist(self, report: ValidationReport) -> None:
        # Keep prior reports for history; always insert new snapshot.
        root = CipValidationReport(
            report_id=report.report_id,
            document_id=report.document_id,
            graph_id=report.graph_id,
            map_id=report.map_id,
            pipeline_job_id=report.pipeline_job_id,
            issue_count=report.issue_count,
            error_count=report.error_count,
            warning_count=report.warning_count,
            passed=report.passed,
        )
        db.session.add(root)
        db.session.flush()
        for issue in report.issues:
            db.session.add(
                CipValidationIssue(
                    issue_id=issue.issue_id,
                    report_id=report.report_id,
                    kind=issue.kind.value,
                    severity=issue.severity.value,
                    message=issue.message[:512],
                    subject_kind=issue.subject_kind,
                    subject_id=issue.subject_id,
                    related_ids_csv=",".join(issue.related_ids),
                    document_id=issue.document_id,
                )
            )

    @staticmethod
    def _to_domain(row: CipValidationReport) -> ValidationReport:
        issues = tuple(
            ValidationIssue(
                issue_id=i.issue_id,
                kind=ValidationIssueKind(i.kind),
                severity=ValidationSeverity(i.severity),
                message=i.message,
                subject_kind=i.subject_kind,
                subject_id=i.subject_id,
                related_ids=tuple(
                    p for p in (i.related_ids_csv or "").split(",") if p
                ),
                document_id=i.document_id,
            )
            for i in row.issues
        )
        return ValidationReport(
            report_id=row.report_id,
            document_id=row.document_id,
            graph_id=row.graph_id,
            map_id=row.map_id,
            pipeline_job_id=row.pipeline_job_id,
            issue_count=row.issue_count,
            error_count=row.error_count,
            warning_count=row.warning_count,
            passed=row.passed,
            issues=issues,
            created_at_iso=_iso(row.created_at) if row.created_at else "",
        )

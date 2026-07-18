"""Stateless validation policy for normalised curriculum structures."""

from __future__ import annotations

from app.application.curriculum_ingestion.policies.normalization_policy import (
    NormalizationPolicy,
)
from app.domain.curriculum_ingestion.ingestion_report import (
    IngestionIssue,
    IngestionIssueCode,
    IngestionIssueSeverity,
)
from app.domain.curriculum_ingestion.normalization_result import NormalizationResult


class ValidationPolicy:
    """Deterministic structural checks over normalised ingestion output."""

    REQUIRED_METADATA_KEYS = frozenset({"subject_code"})

    @staticmethod
    def collect_issues(
        normalization: NormalizationResult,
        *,
        document_empty: bool = False,
        has_unknown_kind: bool = False,
    ) -> tuple[IngestionIssue, ...]:
        """Inspect normalised structures; return immutable findings."""
        issues: list[IngestionIssue] = []

        if document_empty:
            issues.append(
                IngestionIssue.create(
                    IngestionIssueCode.EMPTY_DOCUMENT,
                    "Source documents produced no structural entries",
                    severity=IngestionIssueSeverity.BLOCKING,
                )
            )

        if has_unknown_kind:
            issues.append(
                IngestionIssue.create(
                    IngestionIssueCode.UNKNOWN_DOCUMENT_KIND,
                    "One or more documents could not be classified",
                    severity=IngestionIssueSeverity.WARNING,
                )
            )

        issues.extend(ValidationPolicy._section_issues(normalization))
        issues.extend(ValidationPolicy._topic_issues(normalization))
        issues.extend(ValidationPolicy._objective_issues(normalization))
        issues.extend(ValidationPolicy._prerequisite_issues(normalization))
        issues.extend(ValidationPolicy._metadata_issues(normalization))
        issues.extend(ValidationPolicy._numbering_issues(normalization))
        return tuple(issues)

    @staticmethod
    def _section_issues(
        normalization: NormalizationResult,
    ) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        seen: set[str] = set()
        section_ids = {s.section_id for s in normalization.sections}
        for section in normalization.sections:
            key = section.section_id.lower()
            if key in seen:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.DUPLICATE_SECTION,
                        f"Duplicate section id: {section.section_id}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"section:{section.section_id}",
                    )
                )
            seen.add(key)
            if (
                section.parent_section_id is not None
                and section.parent_section_id not in section_ids
            ):
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.MALFORMED_HIERARCHY,
                        f"Section {section.section_id} references unknown "
                        f"parent {section.parent_section_id}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"section:{section.section_id}",
                    )
                )
            if section.parent_section_id == section.section_id:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.MALFORMED_HIERARCHY,
                        f"Section {section.section_id} is its own parent",
                        severity=IngestionIssueSeverity.BLOCKING,
                        path=f"section:{section.section_id}",
                    )
                )
        return issues

    @staticmethod
    def _topic_issues(normalization: NormalizationResult) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        seen: set[str] = set()
        seen_titles: dict[str, str] = {}
        section_ids = {s.section_id for s in normalization.sections}
        for topic in normalization.topics:
            key = topic.topic_id.lower()
            if key in seen:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.DUPLICATE_TOPIC,
                        f"Duplicate topic id: {topic.topic_id}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"topic:{topic.topic_id}",
                    )
                )
            seen.add(key)
            title_key = topic.title.strip().lower()
            if title_key in seen_titles:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.DUPLICATE_TOPIC,
                        f"Duplicate topic title: {topic.title}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"topic:{topic.topic_id}",
                    )
                )
            else:
                seen_titles[title_key] = topic.topic_id
            if topic.section_id not in section_ids:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.UNKNOWN_SECTION,
                        f"Topic {topic.topic_id} references unknown "
                        f"section {topic.section_id}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"topic:{topic.topic_id}",
                    )
                )
        return issues

    @staticmethod
    def _objective_issues(
        normalization: NormalizationResult,
    ) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        topic_ids = {t.topic_id for t in normalization.topics}
        objectives_by_topic: dict[str, int] = {t: 0 for t in topic_ids}
        seen: set[str] = set()
        for objective in normalization.objectives:
            key = objective.objective_id.lower()
            if key in seen:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.DUPLICATE_OBJECTIVE,
                        f"Duplicate objective id: {objective.objective_id}",
                        severity=IngestionIssueSeverity.WARNING,
                        path=f"objective:{objective.objective_id}",
                    )
                )
            seen.add(key)
            if objective.topic_id not in topic_ids:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.ORPHAN_OBJECTIVE,
                        f"Objective {objective.objective_id} references "
                        f"unknown topic {objective.topic_id}",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"objective:{objective.objective_id}",
                    )
                )
            else:
                objectives_by_topic[objective.topic_id] = (
                    objectives_by_topic.get(objective.topic_id, 0) + 1
                )

        if normalization.topics:
            for topic in normalization.topics:
                if objectives_by_topic.get(topic.topic_id, 0) == 0:
                    issues.append(
                        IngestionIssue.create(
                            IngestionIssueCode.MISSING_OBJECTIVES,
                            f"Topic {topic.topic_id} has no learning objectives",
                            severity=IngestionIssueSeverity.ERROR,
                            path=f"topic:{topic.topic_id}",
                        )
                    )
        return issues

    @staticmethod
    def _prerequisite_issues(
        normalization: NormalizationResult,
    ) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        topic_ids = {t.topic_id for t in normalization.topics}
        for source, target in normalization.prerequisite_edges:
            if source not in topic_ids or target not in topic_ids:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.DANGLING_PREREQUISITE,
                        f"Prerequisite edge {source} → {target} is dangling",
                        severity=IngestionIssueSeverity.WARNING,
                        path=f"prerequisite:{source}->{target}",
                    )
                )
            if source == target:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.MALFORMED_HIERARCHY,
                        f"Topic {source} lists itself as prerequisite",
                        severity=IngestionIssueSeverity.ERROR,
                        path=f"prerequisite:{source}",
                    )
                )
        for topic in normalization.topics:
            for prereq in topic.prerequisite_ids:
                if prereq not in topic_ids:
                    issues.append(
                        IngestionIssue.create(
                            IngestionIssueCode.DANGLING_PREREQUISITE,
                            f"Topic {topic.topic_id} references unknown "
                            f"prerequisite {prereq}",
                            severity=IngestionIssueSeverity.WARNING,
                            path=f"topic:{topic.topic_id}",
                        )
                    )
        return issues

    @staticmethod
    def _metadata_issues(
        normalization: NormalizationResult,
    ) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        keys = {k.strip().lower() for k, _ in normalization.metadata}
        for required in ValidationPolicy.REQUIRED_METADATA_KEYS:
            if required not in keys:
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.MISSING_METADATA,
                        f"Missing required metadata key: {required}",
                        severity=IngestionIssueSeverity.WARNING,
                        path=f"metadata:{required}",
                    )
                )
        return issues

    @staticmethod
    def _numbering_issues(
        normalization: NormalizationResult,
    ) -> list[IngestionIssue]:
        issues: list[IngestionIssue] = []
        section_numbers = [s.number for s in normalization.sections]
        if not NormalizationPolicy.numbers_are_consistent(section_numbers):
            issues.append(
                IngestionIssue.create(
                    IngestionIssueCode.INCONSISTENT_NUMBERING,
                    "Section numbering is not strictly increasing",
                    severity=IngestionIssueSeverity.WARNING,
                    path="sections",
                )
            )
        by_section: dict[str, list[str]] = {}
        for topic in normalization.topics:
            by_section.setdefault(topic.section_id, []).append(topic.number)
        for section_id, numbers in by_section.items():
            if not NormalizationPolicy.numbers_are_consistent(numbers):
                issues.append(
                    IngestionIssue.create(
                        IngestionIssueCode.INCONSISTENT_NUMBERING,
                        f"Topic numbering inconsistent under section "
                        f"{section_id}",
                        severity=IngestionIssueSeverity.WARNING,
                        path=f"section:{section_id}",
                    )
                )
        return issues

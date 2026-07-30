"""CoveragePolicy — educational reconciliation rules (Generation 6)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from app.application.curriculum_intelligence.policies.base import EducationalPolicy
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.generation import EducationalNode
from app.domain.curriculum_intelligence.policy import (
    EducationalDecision,
    PolicyDescriptor,
)

_NUM = re.compile(r"(\d+(?:\.\d+)*)")
_TOKEN = re.compile(r"[a-z0-9]+")

_DESCRIPTOR = PolicyDescriptor(
    policy_id="coverage_policy",
    name="CoveragePolicy",
    purpose="Compare syllabus / CMP / generation history for educational completeness",
    version="1.0.0",
    deterministic=True,
    generation_index=6,
)


class CoverageFindingKind(StrEnum):
    COVERED = "covered"
    MISSING_CONCEPT = "missing_concept"
    UNEXPECTED_CONCEPT = "unexpected_concept"
    HIERARCHY_INCONSISTENT = "hierarchy_inconsistent"
    COMPLETE = "educationally_complete"


@dataclass(frozen=True)
class CoverageFinding:
    """One reconciliation finding with evidence grade."""

    finding_id: str
    kind: CoverageFindingKind
    syllabus_ref: str | None
    title: str
    matched_node_id: str | None
    score: float
    evidence_grade: EvidenceGrade
    reason: str


@dataclass(frozen=True)
class CoverageMatrixResult:
    """Coverage matrix + completeness for Generation 6."""

    findings: tuple[CoverageFinding, ...]
    decisions: tuple[EducationalDecision, ...]
    covered: int
    missing: int
    unexpected: int
    hierarchy_issues: int
    syllabus_objective_count: int
    completeness: float
    hierarchy_consistent: bool


class CoveragePolicy(EducationalPolicy):
    """Deterministic coverage / completeness reconciliation policy."""

    COVERED_THRESHOLD = 0.55

    @property
    def descriptor(self) -> PolicyDescriptor:
        return _DESCRIPTOR

    def reconcile(
        self,
        *,
        working_nodes: tuple[EducationalNode, ...] | list[EducationalNode],
        syllabus_objectives: tuple[tuple[str, str], ...],
        decision_prefix: str = "cov",
    ) -> CoverageMatrixResult:
        """Compare working curriculum against official syllabus objectives.

        Args:
            working_nodes: Active (+ inactive) nodes from Gen 5.
            syllabus_objectives: ``(number, title)`` pairs from syllabus authority.
        """
        active = [n for n in working_nodes if n.active]
        pool = [
            n
            for n in active
            if n.kind
            in {
                "topic",
                "subtopic",
                "concept",
                "learning_objective",
                "objective",
                "section",
                "chapter",
            }
        ]
        pool_tokens = [(n, _tokens(n.title)) for n in pool]
        used: set[str] = set()
        findings: list[CoverageFinding] = []
        decisions: list[EducationalDecision] = []
        covered = missing = 0
        seq = 0

        for number, title in syllabus_objectives:
            seq += 1
            target = _tokens(f"{number} {title}")
            best: EducationalNode | None = None
            best_score = 0.0
            for node, tokens in pool_tokens:
                score = _similarity(target, tokens, number, _node_number(node))
                if score > best_score:
                    best_score = score
                    best = node
            if best is not None and best_score >= self.COVERED_THRESHOLD:
                covered += 1
                used.add(best.node_id)
                finding = CoverageFinding(
                    finding_id=f"{decision_prefix}-f-{seq}",
                    kind=CoverageFindingKind.COVERED,
                    syllabus_ref=number,
                    title=title,
                    matched_node_id=best.node_id,
                    score=round(best_score, 3),
                    evidence_grade=EvidenceGrade.A,
                    reason="Syllabus objective matched in working curriculum",
                )
                action = "cover:matched"
                conf = 0.92
            else:
                missing += 1
                finding = CoverageFinding(
                    finding_id=f"{decision_prefix}-f-{seq}",
                    kind=CoverageFindingKind.MISSING_CONCEPT,
                    syllabus_ref=number,
                    title=title,
                    matched_node_id=None,
                    score=round(best_score, 3),
                    evidence_grade=EvidenceGrade.A,
                    reason="Official syllabus concept not found in working curriculum",
                )
                action = "cover:missing"
                conf = 0.9
            matched_ids = (
                (best.node_id,)
                if best is not None and best_score >= self.COVERED_THRESHOLD
                else ()
            )
            findings.append(finding)
            decisions.append(
                EducationalDecision(
                    decision_id=f"{decision_prefix}-d-{seq}",
                    action=action,
                    subject_node_ids=matched_ids,
                    reason=finding.reason,
                    evidence_refs=(number,),
                    confidence=conf,
                    policy_id=self.policy_id,
                    evidence_grade=EvidenceGrade.A,
                    related_node_ids=(),
                    detail=title[:200],
                    syllabus_ref=number,
                )
            )

        unexpected = 0
        for node in pool:
            if node.node_id in used:
                continue
            if node.kind not in {"topic", "concept", "learning_objective", "objective"}:
                continue
            # Hierarchy nodes with syllabus refs are expected authority — skip.
            if node.lineage.syllabus_refs:
                continue
            unexpected += 1
            seq += 1
            finding = CoverageFinding(
                finding_id=f"{decision_prefix}-f-{seq}",
                kind=CoverageFindingKind.UNEXPECTED_CONCEPT,
                syllabus_ref=None,
                title=node.title,
                matched_node_id=node.node_id,
                score=0.0,
                evidence_grade=node.evidence_grade or EvidenceGrade.B,
                reason="Working concept has no syllabus counterpart",
            )
            findings.append(finding)
            decisions.append(
                EducationalDecision(
                    decision_id=f"{decision_prefix}-d-{seq}",
                    action="cover:unexpected",
                    subject_node_ids=(node.node_id,),
                    reason=finding.reason,
                    evidence_refs=_evidence_refs(node),
                    confidence=0.7,
                    policy_id=self.policy_id,
                    evidence_grade=finding.evidence_grade,
                    detail=node.title[:200],
                )
            )

        hierarchy_issues = _hierarchy_issues(active)
        for index, issue in enumerate(hierarchy_issues, start=1):
            seq += 1
            node_id, reason = issue
            findings.append(
                CoverageFinding(
                    finding_id=f"{decision_prefix}-h-{index}",
                    kind=CoverageFindingKind.HIERARCHY_INCONSISTENT,
                    syllabus_ref=None,
                    title=reason,
                    matched_node_id=node_id,
                    score=0.0,
                    evidence_grade=EvidenceGrade.C,
                    reason=reason,
                )
            )

        total = max(len(syllabus_objectives), 1)
        completeness = round(covered / total, 4) if syllabus_objectives else 1.0
        hierarchy_ok = len(hierarchy_issues) == 0
        if (
            syllabus_objectives
            and completeness >= 0.85
            and hierarchy_ok
            and missing == 0
        ):
            seq += 1
            findings.append(
                CoverageFinding(
                    finding_id=f"{decision_prefix}-complete",
                    kind=CoverageFindingKind.COMPLETE,
                    syllabus_ref=None,
                    title="Educational completeness",
                    matched_node_id=None,
                    score=completeness,
                    evidence_grade=EvidenceGrade.A,
                    reason=(
                        "Working curriculum covers syllabus objectives "
                        "with consistent hierarchy"
                    ),
                )
            )

        return CoverageMatrixResult(
            findings=tuple(findings),
            decisions=tuple(decisions),
            covered=covered,
            missing=missing,
            unexpected=unexpected,
            hierarchy_issues=len(hierarchy_issues),
            syllabus_objective_count=len(syllabus_objectives),
            completeness=completeness,
            hierarchy_consistent=hierarchy_ok,
        )


def _evidence_refs(node: EducationalNode) -> tuple[str, ...]:
    refs: list[str] = []
    if node.provenance_id:
        refs.append(node.provenance_id)
    refs.extend(node.lineage.syllabus_refs)
    return tuple(refs)


def _tokens(text: str) -> frozenset[str]:
    return frozenset(_TOKEN.findall(text.lower()))


def _node_number(node: EducationalNode) -> str:
    if node.lineage.syllabus_refs:
        return node.lineage.syllabus_refs[0]
    match = _NUM.search(node.title)
    return match.group(1) if match else ""


def _similarity(
    target: frozenset[str],
    candidate: frozenset[str],
    target_num: str,
    candidate_num: str,
) -> float:
    if not target or not candidate:
        token_score = 0.0
    else:
        token_score = len(target & candidate) / len(target | candidate)
    num_score = 0.0
    if target_num and candidate_num:
        if target_num == candidate_num:
            num_score = 1.0
        elif candidate_num.startswith(target_num + ".") or target_num.startswith(
            candidate_num + "."
        ):
            num_score = 0.7
    return 0.55 * token_score + 0.45 * num_score


def _hierarchy_issues(active: list[EducationalNode]) -> list[tuple[str, str]]:
    by_id = {n.node_id: n for n in active}
    issues: list[tuple[str, str]] = []
    allowed = {
        "chapter": frozenset({"subject"}),
        "section": frozenset({"chapter", "module", "subject"}),
        "topic": frozenset({"section", "chapter", "module", "subject"}),
        "concept": frozenset({"section", "chapter", "module", "subject", "topic"}),
        "learning_objective": frozenset(
            {"topic", "subtopic", "concept", "section", "chapter", "module"}
        ),
        "objective": frozenset(
            {"topic", "subtopic", "concept", "section", "chapter", "module"}
        ),
    }
    for node in active:
        if not node.parent_node_id:
            continue
        parent = by_id.get(node.parent_node_id)
        if parent is None:
            issues.append((node.node_id, f"Orphan parent ref on {node.title[:80]}"))
            continue
        parents = allowed.get(node.kind)
        if parents is not None and parent.kind not in parents:
            issues.append(
                (
                    node.node_id,
                    f"Invalid parent kind {parent.kind} for {node.kind}",
                )
            )
    return issues

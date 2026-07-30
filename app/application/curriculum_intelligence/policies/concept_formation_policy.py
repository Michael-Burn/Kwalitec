"""ConceptFormationPolicy — coherent learning-unit decisions (Generation 4).

Optimises for educational coherence, not topic count.
Decisions: merge · split · retain — each with reason, evidence, confidence,
policy id, and Evidence Grade.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

from app.application.curriculum_intelligence.policies.base import EducationalPolicy
from app.domain.curriculum_intelligence.evidence import EvidenceGrade
from app.domain.curriculum_intelligence.generation import EducationalNode
from app.domain.curriculum_intelligence.policy import (
    ConceptAction,
    EducationalDecision,
    PolicyDescriptor,
)

_NUM = re.compile(r"(\d+(?:\.\d+)*)")
_TOKEN = re.compile(r"[a-z0-9]+")
_MULTI_LO = re.compile(r"\d+\.\d+\.\d+")

_DESCRIPTOR = PolicyDescriptor(
    policy_id="concept_formation_policy",
    name="ConceptFormationPolicy",
    purpose="Discover coherent learning units (merge / split / retain)",
    version="1.0.0",
    deterministic=True,
    generation_index=4,
)

# Near-duplicate sibling merge threshold (token Jaccard).
_MERGE_JACCARD = 0.72
# Title containment merge (fragment absorbed into fuller sibling).
_CONTAINMENT_MIN_LEN = 12


@dataclass(frozen=True)
class ConceptFormationPlan:
    """Deterministic plan of concept decisions for one snapshot."""

    decisions: tuple[EducationalDecision, ...]
    # survivor_id → absorbed node ids
    merges: tuple[tuple[str, tuple[str, ...]], ...]
    # source_id → new concept titles to create
    splits: tuple[tuple[str, tuple[str, ...]], ...]
    retained_ids: tuple[str, ...]


class ConceptFormationPolicy(EducationalPolicy):
    """Decide merge / split / retain for topic-level learning units."""

    @property
    def descriptor(self) -> PolicyDescriptor:
        return _DESCRIPTOR

    def plan(
        self,
        nodes: tuple[EducationalNode, ...] | list[EducationalNode],
        *,
        decision_prefix: str = "cf",
    ) -> ConceptFormationPlan:
        """Produce a deterministic Concept Formation plan.

        Rules (educational coherence):
        1. Split a topic whose title embeds multiple numbered LOs.
        2. Merge sibling topics that are near-duplicates or title fragments.
        3. Otherwise retain.
        """
        active = [n for n in nodes if n.active and n.kind in {"topic", "subtopic"}]
        by_parent: dict[str | None, list[EducationalNode]] = {}
        for node in active:
            by_parent.setdefault(node.parent_node_id, []).append(node)

        decisions: list[EducationalDecision] = []
        merges: list[tuple[str, tuple[str, ...]]] = []
        splits: list[tuple[str, tuple[str, ...]]] = []
        absorbed: set[str] = set()
        split_sources: set[str] = set()
        seq = 0

        # Pass 1 — splits (do not optimise for count; fix compound units).
        for node in sorted(active, key=lambda n: n.node_id):
            parts = _split_titles(node.title)
            if len(parts) < 2:
                continue
            seq += 1
            decision = EducationalDecision(
                decision_id=f"{decision_prefix}-split-{seq}",
                action=ConceptAction.SPLIT.value,
                subject_node_ids=(node.node_id,),
                reason=(
                    "Topic embeds multiple numbered learning units; "
                    "separating them improves understanding"
                ),
                evidence_refs=_evidence_refs(node),
                confidence=0.88,
                policy_id=self.policy_id,
                evidence_grade=_grade_for_node(node, default=EvidenceGrade.A),
                related_node_ids=(),
                detail=f"split_into={len(parts)}",
                syllabus_ref=_primary_number(node),
            )
            decisions.append(decision)
            splits.append((node.node_id, tuple(parts)))
            split_sources.add(node.node_id)

        # Pass 2 — sibling merges (coherence, not count targets).
        for _parent, siblings in sorted(
            by_parent.items(), key=lambda item: item[0] or ""
        ):
            ordered = sorted(
                [s for s in siblings if s.node_id not in split_sources],
                key=lambda n: (_sort_key(n), n.node_id),
            )
            i = 0
            while i < len(ordered):
                survivor = ordered[i]
                if survivor.node_id in absorbed:
                    i += 1
                    continue
                group: list[EducationalNode] = []
                for other in ordered[i + 1 :]:
                    if other.node_id in absorbed:
                        continue
                    if _should_merge(survivor, other):
                        group.append(other)
                if group:
                    seq += 1
                    absorbed_ids = tuple(n.node_id for n in group)
                    for n in group:
                        absorbed.add(n.node_id)
                    grade = _grade_for_node(survivor, default=EvidenceGrade.A)
                    decision = EducationalDecision(
                        decision_id=f"{decision_prefix}-merge-{seq}",
                        action=ConceptAction.MERGE.value,
                        subject_node_ids=(survivor.node_id, *absorbed_ids),
                        reason=(
                            "Sibling topics form one coherent learning unit; "
                            "an IFoA student would naturally study them together"
                        ),
                        evidence_refs=_evidence_refs(survivor)
                        + tuple(
                            ref
                            for n in group
                            for ref in _evidence_refs(n)
                            if ref
                        ),
                        confidence=0.9,
                        policy_id=self.policy_id,
                        evidence_grade=grade,
                        related_node_ids=absorbed_ids,
                        detail=f"merged_count={len(group)}",
                        syllabus_ref=_primary_number(survivor),
                    )
                    decisions.append(decision)
                    merges.append((survivor.node_id, absorbed_ids))
                i += 1

        retained = tuple(
            n.node_id
            for n in active
            if n.node_id not in absorbed and n.node_id not in split_sources
        )
        for node_id in retained:
            node = next(n for n in active if n.node_id == node_id)
            seq += 1
            decisions.append(
                EducationalDecision(
                    decision_id=f"{decision_prefix}-retain-{seq}",
                    action=ConceptAction.RETAIN.value,
                    subject_node_ids=(node_id,),
                    reason="Topic already forms a coherent learning unit",
                    evidence_refs=_evidence_refs(node),
                    confidence=0.92,
                    policy_id=self.policy_id,
                    evidence_grade=_grade_for_node(node, default=EvidenceGrade.A),
                    syllabus_ref=_primary_number(node),
                )
            )

        return ConceptFormationPlan(
            decisions=tuple(decisions),
            merges=tuple(merges),
            splits=tuple(splits),
            retained_ids=retained,
        )


def _evidence_refs(node: EducationalNode) -> tuple[str, ...]:
    refs: list[str] = []
    if node.provenance_id:
        refs.append(node.provenance_id)
    refs.extend(node.lineage.syllabus_refs)
    return tuple(refs)


def _grade_for_node(
    node: EducationalNode, *, default: EvidenceGrade
) -> EvidenceGrade:
    if node.evidence_grade is not None:
        return node.evidence_grade
    if node.lineage.syllabus_refs:
        return EvidenceGrade.A
    return default


def _tokens(text: str) -> frozenset[str]:
    return frozenset(_TOKEN.findall(text.lower()))


def _jaccard(a: frozenset[str], b: frozenset[str]) -> float:
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _primary_number(node: EducationalNode) -> str | None:
    if node.lineage.syllabus_refs:
        return node.lineage.syllabus_refs[0]
    match = _NUM.search(node.title)
    return match.group(1) if match else None


def _sort_key(node: EducationalNode) -> tuple:
    num = _primary_number(node) or "999"
    parts = tuple(int(p) for p in num.split(".") if p.isdigit())
    return parts or (999,)


def _should_merge(a: EducationalNode, b: EducationalNode) -> bool:
    """True when siblings are educationally the same unit."""
    if a.parent_node_id != b.parent_node_id:
        return False
    ta = a.title.strip().lower()
    tb = b.title.strip().lower()
    if not ta or not tb:
        return False
    # Same syllabus number prefix with near-duplicate wording.
    na = _primary_number(a)
    nb = _primary_number(b)
    tokens_a = _tokens(_strip_number(a.title))
    tokens_b = _tokens(_strip_number(b.title))
    sim = _jaccard(tokens_a, tokens_b)
    if na and nb and na == nb and sim >= 0.5:
        return True
    if sim >= _MERGE_JACCARD:
        return True
    # Fragment containment: short title fully inside longer sibling.
    short, long = (ta, tb) if len(ta) <= len(tb) else (tb, ta)
    if (
        len(short) >= _CONTAINMENT_MIN_LEN
        and short in long
        and short != long
        and sim >= 0.4
    ):
        return True
    return False


def _strip_number(title: str) -> str:
    return _NUM.sub("", title, count=1).strip(" -–—:\t")


def _split_titles(title: str) -> tuple[str, ...]:
    """Split compound numbered titles into separate learning-unit titles."""
    matches = list(_MULTI_LO.finditer(title))
    if len(matches) < 2:
        return ()
    parts: list[str] = []
    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(title)
        chunk = title[start:end].strip(" ;,/|")
        if chunk:
            parts.append(chunk)
    # Only treat as a real split when chunks look like distinct units.
    if len(parts) < 2:
        return ()
    return tuple(parts)

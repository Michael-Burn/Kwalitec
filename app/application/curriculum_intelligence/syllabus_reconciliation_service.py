"""Syllabus-first coverage reconciliation (EQ-001).

The official syllabus defines WHAT must be learned. CMP content explains HOW.
This service measures CMP coverage of syllabus objectives without inventing
curriculum.
"""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import StrEnum

from app.domain.curriculum_intelligence.curriculum_entity import (
    CurriculumEntityKind,
    CurriculumKnowledgeEntity,
    CurriculumMap,
)

_NUM_PREFIX = re.compile(r"^(?P<num>\d+(?:\.\d+)*)\s+")
_TOKEN = re.compile(r"[a-z0-9]+")


class CoverageStatus(StrEnum):
    COVERED = "covered"
    PARTIALLY_COVERED = "partially_covered"
    NOT_FOUND = "not_found"
    EXTRA_CMP = "extra_cmp_material"


@dataclass(frozen=True)
class CoverageRow:
    syllabus_id: str
    syllabus_number: str
    syllabus_title: str
    status: CoverageStatus
    cmp_match_title: str | None
    score: float


@dataclass(frozen=True)
class CoverageMatrix:
    rows: tuple[CoverageRow, ...]
    covered: int
    partially_covered: int
    not_found: int
    extra_cmp: int
    syllabus_objective_count: int
    completeness: float


class SyllabusReconciliationService:
    """Reconcile syllabus objectives against CMP-mapped entities."""

    PARTIAL_THRESHOLD = 0.35
    COVERED_THRESHOLD = 0.62

    def reconcile(
        self,
        syllabus_map: CurriculumMap,
        cmp_map: CurriculumMap,
    ) -> CoverageMatrix:
        syllabus_objs = [
            e
            for e in syllabus_map.entities
            if e.kind
            in {
                CurriculumEntityKind.LEARNING_OBJECTIVE,
                CurriculumEntityKind.TOPIC,
                CurriculumEntityKind.MODULE,
            }
            and self._number_of(e)
        ]
        # Prefer finest grain: depth ≥2 numbers as objectives; depth 1 as topics.
        objectives = [
            e for e in syllabus_objs if self._number_of(e).count(".") >= 2
        ] or [
            e for e in syllabus_objs if self._number_of(e).count(".") >= 1
        ]
        cmp_pool = [
            e
            for e in cmp_map.entities
            if e.kind
            in {
                CurriculumEntityKind.LEARNING_OBJECTIVE,
                CurriculumEntityKind.TOPIC,
                CurriculumEntityKind.SUBTOPIC,
                CurriculumEntityKind.MODULE,
                CurriculumEntityKind.CONCEPT,
            }
        ]
        cmp_tokens = [(e, self._tokens(e.title)) for e in cmp_pool]
        used_cmp: set[str] = set()
        rows: list[CoverageRow] = []
        covered = partial = missing = 0

        for obj in objectives:
            num = self._number_of(obj)
            target = self._tokens(obj.title)
            best: CurriculumKnowledgeEntity | None = None
            best_score = 0.0
            for ent, tokens in cmp_tokens:
                score = self._similarity(target, tokens, num, self._number_of(ent))
                if score > best_score:
                    best_score = score
                    best = ent
            if best is not None and best_score >= self.COVERED_THRESHOLD:
                status = CoverageStatus.COVERED
                covered += 1
                used_cmp.add(best.entity_id)
            elif best is not None and best_score >= self.PARTIAL_THRESHOLD:
                status = CoverageStatus.PARTIALLY_COVERED
                partial += 1
                used_cmp.add(best.entity_id)
            else:
                status = CoverageStatus.NOT_FOUND
                missing += 1
                best = None
                best_score = 0.0
            rows.append(
                CoverageRow(
                    syllabus_id=obj.entity_id,
                    syllabus_number=num,
                    syllabus_title=obj.title,
                    status=status,
                    cmp_match_title=best.title if best else None,
                    score=round(best_score, 3),
                )
            )

        extras = 0
        for ent in cmp_pool:
            if ent.entity_id in used_cmp:
                continue
            if ent.kind not in {
                CurriculumEntityKind.MODULE,
                CurriculumEntityKind.TOPIC,
                CurriculumEntityKind.LEARNING_OBJECTIVE,
            }:
                continue
            # Flag CMP-only chapters/topics as extra instructional material.
            extras += 1
            rows.append(
                CoverageRow(
                    syllabus_id="",
                    syllabus_number=self._number_of(ent),
                    syllabus_title=ent.title,
                    status=CoverageStatus.EXTRA_CMP,
                    cmp_match_title=ent.title,
                    score=0.0,
                )
            )

        total = len(objectives) or 1
        completeness = (covered + 0.5 * partial) / total
        return CoverageMatrix(
            rows=tuple(rows),
            covered=covered,
            partially_covered=partial,
            not_found=missing,
            extra_cmp=extras,
            syllabus_objective_count=len(objectives),
            completeness=round(completeness, 4),
        )

    @staticmethod
    def _number_of(entity: CurriculumKnowledgeEntity) -> str:
        for k, v in entity.attributes:
            if k == "section_number":
                return v
        m = _NUM_PREFIX.match(entity.title or "")
        return m.group("num") if m else ""

    @staticmethod
    def _tokens(text: str) -> frozenset[str]:
        stop = {
            "the",
            "a",
            "an",
            "of",
            "and",
            "or",
            "to",
            "for",
            "in",
            "on",
            "with",
            "using",
            "from",
            "that",
            "this",
            "as",
            "be",
            "is",
            "are",
            "their",
            "these",
            "those",
        }
        return frozenset(
            t
            for t in _TOKEN.findall((text or "").lower())
            if t not in stop and len(t) > 1
        )

    @staticmethod
    def _similarity(
        a: frozenset[str],
        b: frozenset[str],
        num_a: str,
        num_b: str,
    ) -> float:
        if not a or not b:
            # Exact number match alone is a weak signal.
            if num_a and num_a == num_b:
                return 0.55
            return 0.0
        inter = len(a & b)
        union = len(a | b) or 1
        jaccard = inter / union
        if num_a and num_b and num_a == num_b:
            jaccard = max(jaccard, 0.7)
        elif num_a and num_b and (
            num_b.startswith(num_a + ".") or num_a.startswith(num_b + ".")
        ):
            jaccard = max(jaccard, 0.45)
        return jaccard

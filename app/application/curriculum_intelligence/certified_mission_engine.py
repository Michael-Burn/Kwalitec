"""EI-002B — Daily Missions from certified Learning Objectives only.

Selection reuses EducationalArtefactDeriver mission templates and applies
deterministic filters for coverage, dependencies, difficulty, progress, and
calibration bias. No new educational reasoning architecture.

MISSION-002 / SR-001A P0: Learning Mode selects the next incomplete eligible
topic in published syllabus order (aligned with ``derive_progress``). LO density
is a weak tie-break only and must not jump ahead in the syllabus.
"""

from __future__ import annotations

from typing import Any
from uuid import uuid4

from app.application.curriculum_intelligence.learner_knowledge_graph_service import (
    LearnerKnowledgeGraphBuilder,
    assert_certified_package,
    extract_provenance,
)
from app.domain.curriculum_intelligence.certified_learning import (
    CertifiedMissionSpec,
    MissionSelectionReason,
)
from app.domain.educational_engine_foundation.derivation import (
    EducationalArtefactDeriver,
)

_DIFFICULTY_RANK = {
    "foundational": 0,
    "easy": 0,
    "introductory": 0,
    "intermediate": 1,
    "standard": 1,
    "balanced": 1,
    "advanced": 2,
    "hard": 2,
    "challenging": 2,
}


class CertifiedMissionEngine:
    """Generate Daily Missions exclusively from certified Learning Objectives."""

    def __init__(
        self,
        *,
        deriver: EducationalArtefactDeriver | None = None,
        graph_builder: LearnerKnowledgeGraphBuilder | None = None,
    ) -> None:
        self._deriver = deriver or EducationalArtefactDeriver()
        self._graph = graph_builder or LearnerKnowledgeGraphBuilder(
            deriver=self._deriver
        )

    def generate(
        self,
        package: dict[str, Any],
        *,
        completed_node_ids: tuple[str, ...] | list[str] = (),
        mastered_objective_ids: tuple[str, ...] | list[str] = (),
        preferred_difficulty: str = "",
        preferred_topic_id: str | None = None,
        calibration: dict[str, Any] | None = None,
        mission_id: str | None = None,
    ) -> CertifiedMissionSpec:
        """Select the next Daily Mission from certified LOs.

        Args:
            package: Published curriculum package (must be certified / legacy).
            completed_node_ids: Topics / chapters already covered.
            mastered_objective_ids: Learning objectives already mastered.
            preferred_difficulty: Optional learner difficulty preference.
            preferred_topic_id: When eligible, force this topic (progress current).
            calibration: Optional Founder calibration outputs
                (``difficulty_bias``, ``topic_density``, ``granularity``).
            mission_id: Optional stable id (tests); otherwise generated.

        Returns:
            CertifiedMissionSpec bound to certified node identifiers.

        Raises:
            ValueError: if package is non-certified or no eligible LO remains.
        """
        provenance = assert_certified_package(package)
        bundle = self._deriver.derive(package)
        graph = self._graph.build(package)
        completed = {str(x).strip() for x in completed_node_ids if str(x).strip()}
        mastered = {
            str(x).strip() for x in mastered_objective_ids if str(x).strip()
        }
        preferred = (preferred_topic_id or "").strip()
        cal = dict(calibration or {})
        # Prefer calibration block embedded in package metadata when present.
        structure = package.get("structure") if isinstance(package, dict) else {}
        if isinstance(structure, dict) and not cal:
            embedded = structure.get("calibration") or package.get("calibration")
            if isinstance(embedded, dict):
                cal = dict(embedded)

        coverage_before = (
            len(mastered) / max(1, len(bundle.objectives))
            if bundle.objectives
            else 0.0
        )

        candidates = []
        for template in bundle.mission_templates:
            if template.topic_id in completed:
                continue
            # Prerequisites must be satisfied (topic-level).
            missing_prereq = [
                p for p in template.prerequisite_ids if p not in completed
            ]
            if missing_prereq:
                continue
            uncovered = [
                oid for oid in template.objective_ids if oid not in mastered
            ]
            if not uncovered and template.objective_ids:
                continue
            # Missions must carry at least one certified Learning Objective.
            if not template.objective_ids:
                continue
            topic = next(
                (t for t in bundle.topics if t.topic_id == template.topic_id),
                None,
            )
            difficulty = (topic.difficulty if topic else "") or "intermediate"
            reasons: list[MissionSelectionReason] = [
                MissionSelectionReason.NEXT_UNCOVERED_OBJECTIVE,
                MissionSelectionReason.PREREQUISITE_READY,
                MissionSelectionReason.PROGRESS_ADVANCE,
            ]
            order = topic.display_order if topic else 999
            # Learning Mode: syllabus order dominates. Soft signals stay below
            # one display-order step so LO density cannot skip ahead.
            score = 0.0
            score -= float(order) * 1000.0
            score += float(len(uncovered)) * 0.01
            # Difficulty match (soft).
            pref = (preferred_difficulty or "").strip().lower()
            bias = str(cal.get("difficulty_bias") or "").strip().lower()
            target = pref or _bias_to_difficulty(bias) or ""
            if target:
                gap = abs(
                    _DIFFICULTY_RANK.get(difficulty.lower(), 1)
                    - _DIFFICULTY_RANK.get(target, 1)
                )
                score += max(0.0, 5.0 - gap * 2.0)
                reasons.append(MissionSelectionReason.DIFFICULTY_MATCH)
                if bias:
                    reasons.append(MissionSelectionReason.CALIBRATION_BIAS)
            # Topic density calibration: consolidated prefers fewer parallel LOs.
            density = str(cal.get("topic_density") or "").strip().lower()
            if density == "consolidated":
                score += max(0.0, 4.0 - float(len(template.objective_ids)))
            elif density == "detailed":
                score += float(len(template.objective_ids)) * 0.5

            obj_titles = tuple(
                next(
                    (
                        o.text
                        for o in bundle.objectives
                        if o.objective_id == oid
                    ),
                    "",
                )
                for oid in (uncovered or template.objective_ids)
            )
            # Drop empty titles (never surface raw objective ids to students).
            obj_titles = tuple(t for t in obj_titles if t) or tuple(
                next(
                    (
                        o.text
                        for o in bundle.objectives
                        if o.objective_id == oid
                    ),
                    "Learning objective",
                )
                for oid in (uncovered or template.objective_ids)
            )
            candidates.append(
                (
                    score,
                    order,
                    template,
                    topic,
                    uncovered or list(template.objective_ids),
                    obj_titles,
                    difficulty,
                    tuple(dict.fromkeys(reasons)),
                )
            )

        if not candidates:
            raise ValueError(
                "no certified Learning Objective remains eligible for a Daily Mission"
            )

        if preferred:
            preferred_rows = [
                row for row in candidates if row[2].topic_id == preferred
            ]
            if preferred_rows:
                candidates = preferred_rows

        candidates.sort(key=lambda row: (-row[0], row[1], row[2].topic_id))
        (
            _score,
            _order,
            template,
            topic,
            objective_ids,
            obj_titles,
            difficulty,
            reasons,
        ) = candidates[0]

        cal_notes: list[str] = []
        if cal.get("difficulty_bias"):
            cal_notes.append(f"difficulty_bias={cal['difficulty_bias']}")
        if cal.get("topic_density"):
            cal_notes.append(f"topic_density={cal['topic_density']}")
        if cal.get("granularity"):
            cal_notes.append(f"granularity={cal['granularity']}")

        mid = (mission_id or "").strip() or f"cm_{uuid4().hex[:12]}"
        # Ensure objective ids exist in the learner graph (integrity).
        graph_obj_ids = {n.node_id for n in graph.objectives()}
        for oid in objective_ids:
            if oid not in graph_obj_ids:
                raise ValueError(
                    f"mission references unknown certified objective {oid}"
                )

        return CertifiedMissionSpec(
            mission_id=mid,
            curriculum_identity=bundle.curriculum_identity,
            topic_id=template.topic_id,
            topic_title=(topic.title if topic else template.title),
            objective_ids=tuple(objective_ids),
            objective_titles=obj_titles,
            prerequisite_ids=template.prerequisite_ids,
            estimated_minutes=int(template.estimated_duration_minutes or 0),
            difficulty=difficulty,
            selection_reasons=reasons,
            provenance=provenance or extract_provenance(package),
            task_descriptions=template.task_descriptions,
            calibration_notes=tuple(cal_notes),
            coverage_ratio_before=round(coverage_before, 4),
        )


def _bias_to_difficulty(bias: str) -> str:
    mapping = {
        "foundational": "foundational",
        "easier": "foundational",
        "supportive": "foundational",
        "balanced": "intermediate",
        "challenging": "advanced",
        "advanced": "advanced",
    }
    return mapping.get(bias, "")

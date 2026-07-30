"""EI-001 Curriculum Intelligence Agents (Phases B–D)."""

from __future__ import annotations

from app.application.curriculum_intelligence.mock_generation_runners import (
    GenerationRunner,
    MockPassThroughRunner,
    default_mock_runners,
)

from .base import (
    AgentRunResult,
    CurriculumIntelligenceAgent,
    record_educational_decisions,
)
from .concept_formation_agent import ConceptFormationAgent
from .educational_certification_agent import EducationalCertificationAgent
from .educational_reconciliation_agent import EducationalReconciliationAgent
from .hierarchy_construction_agent import HierarchyConstructionAgent
from .noise_elimination_agent import NoiseEliminationAgent
from .objective_intelligence_agent import ObjectiveIntelligenceAgent
from .raw_graph_agent import RawGraphAgent

__all__ = [
    "AgentRunResult",
    "ConceptFormationAgent",
    "CurriculumIntelligenceAgent",
    "EducationalCertificationAgent",
    "EducationalReconciliationAgent",
    "HierarchyConstructionAgent",
    "NoiseEliminationAgent",
    "ObjectiveIntelligenceAgent",
    "RawGraphAgent",
    "default_phase_b_runners",
    "default_phase_c_runners",
    "default_phase_d_runners",
    "record_educational_decisions",
]


def default_phase_b_runners(
    *,
    through: int = 3,
    include_mock_tail: bool = True,
) -> dict[int, GenerationRunner]:
    """Wire Gen 1–3 Agents; optionally keep mock runners for Gen 4–7."""
    runners: dict[int, GenerationRunner] = {
        1: RawGraphAgent(),
        2: NoiseEliminationAgent(),
        3: HierarchyConstructionAgent(),
    }
    if include_mock_tail and through > 3:
        mocks = default_mock_runners()
        for index in range(4, through + 1):
            runners[index] = mocks[index]
    elif include_mock_tail:
        # Keep registry complete for orchestrator ranges that extend past B.
        for index in range(4, 8):
            runners[index] = MockPassThroughRunner(index)
    return runners


def default_phase_c_runners(
    *,
    through: int = 6,
    include_mock_tail: bool = True,
) -> dict[int, GenerationRunner]:
    """Wire Gen 1–6 Agents; optionally keep mock Certification (Gen 7)."""
    runners: dict[int, GenerationRunner] = {
        1: RawGraphAgent(),
        2: NoiseEliminationAgent(),
        3: HierarchyConstructionAgent(),
        4: ConceptFormationAgent(),
        5: ObjectiveIntelligenceAgent(),
        6: EducationalReconciliationAgent(),
    }
    if include_mock_tail and through >= 7:
        runners[7] = default_mock_runners()[7]
    elif include_mock_tail:
        runners[7] = MockPassThroughRunner(7)
    return runners


def default_phase_d_runners(
    *,
    through: int = 7,
) -> dict[int, GenerationRunner]:
    """Wire Gen 1–7 Agents including Educational Certification."""
    runners: dict[int, GenerationRunner] = {
        1: RawGraphAgent(),
        2: NoiseEliminationAgent(),
        3: HierarchyConstructionAgent(),
        4: ConceptFormationAgent(),
        5: ObjectiveIntelligenceAgent(),
        6: EducationalReconciliationAgent(),
        7: EducationalCertificationAgent(),
    }
    if through < 7:
        return {k: v for k, v in runners.items() if k <= through}
    return runners

"""SQLAlchemy repository adapters for Education OS application ports (INF-003).

Repositories translate between domain aggregates and storage only.
"""

from __future__ import annotations

from .decision_repository import (
    SqlAlchemyDecisionRepository,
)
from .diagnosis_repository import (
    SqlAlchemyDiagnosisRepository,
)
from .digital_twin_repository import (
    SqlAlchemyDigitalTwinRepository,
)
from .evidence_repository import (
    SqlAlchemyEvidenceRepository,
)
from .hypothesis_repository import (
    SqlAlchemyHypothesisRepository,
)
from .learning_episode_repository import (
    SqlAlchemyLearningEpisodeRepository,
)
from .orchestrator_repository import (
    SqlAlchemyOrchestratorRepository,
)
from .priority_repository import (
    SqlAlchemyPriorityRepository,
)
from .subject_knowledge_repository import (
    SqlAlchemySubjectKnowledgeRepository,
)
from .teaching_intention_repository import (
    SqlAlchemyTeachingIntentionRepository,
)
from .teaching_plan_repository import (
    SqlAlchemyTeachingPlanRepository,
)
from .teaching_strategy_repository import (
    SqlAlchemyTeachingStrategyRepository,
)

__all__ = [
    "SqlAlchemyDigitalTwinRepository",
    "SqlAlchemyLearningEpisodeRepository",
    "SqlAlchemyEvidenceRepository",
    "SqlAlchemySubjectKnowledgeRepository",
    "SqlAlchemyTeachingPlanRepository",
    "SqlAlchemyDiagnosisRepository",
    "SqlAlchemyHypothesisRepository",
    "SqlAlchemyPriorityRepository",
    "SqlAlchemyTeachingIntentionRepository",
    "SqlAlchemyTeachingStrategyRepository",
    "SqlAlchemyDecisionRepository",
    "SqlAlchemyOrchestratorRepository",
]

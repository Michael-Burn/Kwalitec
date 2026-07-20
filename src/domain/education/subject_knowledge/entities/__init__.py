"""Subject Knowledge entities."""

from __future__ import annotations

from domain.education.subject_knowledge.entities.application_context import (
    ApplicationContext,
    ApplicationContextId,
)
from domain.education.subject_knowledge.entities.learning_objective import (
    LearningObjective,
)
from domain.education.subject_knowledge.entities.misconception import Misconception
from domain.education.subject_knowledge.entities.representation import (
    Representation,
    RepresentationId,
)
from domain.education.subject_knowledge.entities.transfer_context import (
    TransferContext,
    TransferContextId,
)

__all__ = [
    "ApplicationContext",
    "ApplicationContextId",
    "LearningObjective",
    "Misconception",
    "Representation",
    "RepresentationId",
    "TransferContext",
    "TransferContextId",
]

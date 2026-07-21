"""Student Twin Initialization — CompletedOnboarding → Twin + first pipeline.

Converts sealed onboarding declarations into the first persistent Educational
Digital Twin, seeds the observational evidence catalogue, and immediately
executes the Educational Pipeline for the student's first educational result.

Allowed: validation, Twin creation, evidence seeding, transactional
persistence through repository ports, Educational Pipeline execution.

Forbidden: recommendations outside the Educational Pipeline, Flask,
presentation, HTML, AI, SQLAlchemy.
"""

from __future__ import annotations

from application.student_initialization.availability_mapper import (
    build_availability,
)
from application.student_initialization.errors import (
    OnboardingValidationError,
    StudentInitializationError,
)
from application.student_initialization.evidence_seeder import (
    EvidenceCatalogueSeeder,
    evidence_id_for_onboarding,
)
from application.student_initialization.onboarding_adapter import (
    StudentTwinInitializerAdapter,
)
from application.student_initialization.ports import (
    Clock,
    EducationalPipelinePort,
    PipelineSessionContextFactory,
    TwinIdGenerator,
)
from application.student_initialization.results import (
    InitialEvidence,
    InitializationResult,
    StudentTwin,
)
from application.student_initialization.session_context_factory import (
    FirstRunSessionContextFactory,
)
from application.student_initialization.student_initialization_service import (
    DeterministicTwinIdGenerator,
    EducationalPipelineAdapter,
    StudentInitializationService,
)
from application.student_initialization.twin_builder import (
    build_student_twin,
    map_confidence_profile,
)

__all__ = [
    "Clock",
    "DeterministicTwinIdGenerator",
    "EducationalPipelineAdapter",
    "EducationalPipelinePort",
    "EvidenceCatalogueSeeder",
    "FirstRunSessionContextFactory",
    "InitialEvidence",
    "InitializationResult",
    "OnboardingValidationError",
    "PipelineSessionContextFactory",
    "StudentInitializationError",
    "StudentInitializationService",
    "StudentTwin",
    "StudentTwinInitializerAdapter",
    "TwinIdGenerator",
    "build_availability",
    "build_student_twin",
    "evidence_id_for_onboarding",
    "map_confidence_profile",
]

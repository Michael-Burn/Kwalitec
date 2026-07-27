"""Curriculum Intelligence infrastructure adapters."""

from app.infrastructure.adapters.curriculum_intelligence.pipeline_processing import (
    CurriculumIntelligenceProcessingAdapter,
)
from app.infrastructure.adapters.curriculum_intelligence.pypdf_extractor import (
    PyPdfExtractionAdapter,
)

__all__ = [
    "CurriculumIntelligenceProcessingAdapter",
    "PyPdfExtractionAdapter",
]

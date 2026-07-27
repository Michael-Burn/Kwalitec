"""CIP application exceptions."""

from __future__ import annotations


class CurriculumIntelligenceError(Exception):
    """Base CIP application error."""

    def __init__(self, message: str, *, code: str = "cip_error") -> None:
        super().__init__(message)
        self.code = code


class PipelineTransitionError(CurriculumIntelligenceError):
    """Illegal or blocked pipeline transition."""

    def __init__(self, message: str, *, code: str = "illegal_transition") -> None:
        super().__init__(message, code=code)


class PipelineCancelledError(CurriculumIntelligenceError):
    """Job was cancelled before completion."""

    def __init__(self, message: str = "Processing was cancelled.") -> None:
        super().__init__(message, code="cancelled")


class ExtractionError(CurriculumIntelligenceError):
    """Deterministic extraction failed."""

    def __init__(self, message: str, *, code: str = "extraction_failed") -> None:
        super().__init__(message, code=code)


class ParseError(CurriculumIntelligenceError):
    """Structural parse failed."""

    def __init__(self, message: str, *, code: str = "parse_failed") -> None:
        super().__init__(message, code=code)


class MappingError(CurriculumIntelligenceError):
    """Curriculum mapping failed."""

    def __init__(self, message: str, *, code: str = "mapping_failed") -> None:
        super().__init__(message, code=code)


class GraphBuildError(CurriculumIntelligenceError):
    """Knowledge graph build failed."""

    def __init__(self, message: str, *, code: str = "graph_failed") -> None:
        super().__init__(message, code=code)


class JobNotFoundError(CurriculumIntelligenceError):
    """Processing job not found."""

    def __init__(self, message: str = "Processing job not found.") -> None:
        super().__init__(message, code="job_not_found")

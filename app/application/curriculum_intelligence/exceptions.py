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


class SnapshotImmutableError(CurriculumIntelligenceError):
    """Attempted to mutate an immutable generation snapshot."""

    def __init__(
        self, message: str = "Generation snapshots are immutable after creation."
    ) -> None:
        super().__init__(message, code="snapshot_immutable")


class SnapshotNotFoundError(CurriculumIntelligenceError):
    """Requested generation snapshot was not found."""

    def __init__(self, message: str = "Generation snapshot not found.") -> None:
        super().__init__(message, code="snapshot_not_found")


class GenerationOrderError(CurriculumIntelligenceError):
    """Generations must execute in index order without skipping."""

    def __init__(self, message: str, *, code: str = "generation_order") -> None:
        super().__init__(message, code=code)


class LineageAppendError(CurriculumIntelligenceError):
    """Illegal lineage mutation (history rewrite attempted)."""

    def __init__(self, message: str, *, code: str = "lineage_append_only") -> None:
        super().__init__(message, code=code)

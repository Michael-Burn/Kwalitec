"""Application-layer exceptions for the Instructional Blueprint Engine.

Framework-independent. Raised when registration, selection, validation,
compilation, or sequence generation rules are violated.
"""

from __future__ import annotations


class InstructionalBlueprintEngineError(Exception):
    """Base exception for Instructional Blueprint Engine failures."""


class BlueprintNotFound(InstructionalBlueprintEngineError):  # noqa: N818
    """No Instructional Blueprint exists for the requested identity or type."""


class BlueprintAlreadyRegistered(InstructionalBlueprintEngineError):  # noqa: N818
    """A blueprint with the same identity is already registered."""


class BlueprintSelectionError(InstructionalBlueprintEngineError):  # noqa: N818
    """A blueprint could not be selected from the supplied structural signals."""


class BlueprintValidationError(InstructionalBlueprintEngineError):  # noqa: N818
    """Blueprint structural validation failed."""


class BlueprintCompilationError(InstructionalBlueprintEngineError):  # noqa: N818
    """Blueprint could not be compiled into an instructional structure."""


class SequenceGenerationError(InstructionalBlueprintEngineError):  # noqa: N818
    """Activity sequence / session skeleton could not be generated."""


class RegistryError(InstructionalBlueprintEngineError):  # noqa: N818
    """Blueprint registry operation failed."""

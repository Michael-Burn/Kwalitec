"""Exceptions for document upload orchestration."""

from __future__ import annotations


class DocumentUploadError(Exception):
    """Base class for Founder-facing document upload failures."""

    def __init__(self, message: str, *, code: str = "upload_error") -> None:
        super().__init__(message)
        self.message = message
        self.code = code


class DocumentValidationError(DocumentUploadError):
    """Invalid file type, size, or corrupted PDF."""

    def __init__(self, message: str, *, code: str = "validation_error") -> None:
        super().__init__(message, code=code)


class DuplicateDocumentError(DocumentUploadError):
    """Active document with the same checksum already exists."""

    def __init__(self, message: str, *, code: str = "duplicate") -> None:
        super().__init__(message, code=code)


class DocumentNotFoundError(DocumentUploadError):
    """Requested document metadata or blob is missing."""

    def __init__(self, message: str, *, code: str = "not_found") -> None:
        super().__init__(message, code=code)

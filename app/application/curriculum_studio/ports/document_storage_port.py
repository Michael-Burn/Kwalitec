"""DocumentStoragePort — opaque blob storage for curriculum PDFs.

Implementations must never store PDF bytes in SQL. Domain layers receive
only storage keys / opaque references after a successful put.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import BinaryIO


@dataclass(frozen=True)
class StoredDocument:
    """Result of persisting document bytes."""

    storage_key: str
    byte_size: int
    checksum_sha256: str
    content_type: str


class DocumentStoragePort(ABC):
    """Abstract curriculum document blob store (local / S3 / Azure / GCS)."""

    @abstractmethod
    def put(
        self,
        *,
        storage_key: str,
        data: bytes | BinaryIO,
        content_type: str = "application/pdf",
    ) -> StoredDocument:
        """Persist bytes under storage_key. Overwrites if the key exists."""

    @abstractmethod
    def get(self, storage_key: str) -> bytes:
        """Return raw bytes for a storage key."""

    @abstractmethod
    def exists(self, storage_key: str) -> bool:
        """Return True when the key is present."""

    @abstractmethod
    def delete(self, storage_key: str) -> None:
        """Remove bytes for a key. No-op if missing."""

    @abstractmethod
    def open_stream(self, storage_key: str) -> BinaryIO:
        """Open a readable binary stream for download."""

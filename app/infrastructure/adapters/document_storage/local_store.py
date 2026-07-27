"""Local filesystem DocumentStoragePort adapter.

Production can swap this for S3/Azure/GCS without changing Founder code.
"""

from __future__ import annotations

import hashlib
import logging
from pathlib import Path
from typing import BinaryIO

from app.application.curriculum_studio.ports.document_storage_port import (
    DocumentStoragePort,
    StoredDocument,
)

logger = logging.getLogger(__name__)


class LocalDocumentStorageAdapter(DocumentStoragePort):
    """Store curriculum PDFs under a local root directory."""

    def __init__(self, root: Path | str) -> None:
        self._root = Path(root).resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    @property
    def root(self) -> Path:
        return self._root

    def put(
        self,
        *,
        storage_key: str,
        data: bytes | BinaryIO,
        content_type: str = "application/pdf",
    ) -> StoredDocument:
        key = self._safe_key(storage_key)
        path = self._path_for(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        payload = data.read() if hasattr(data, "read") else bytes(data)
        digest = hashlib.sha256(payload).hexdigest()
        path.write_bytes(payload)
        logger.info(
            "Stored curriculum document key=%s bytes=%s",
            key,
            len(payload),
        )
        return StoredDocument(
            storage_key=key,
            byte_size=len(payload),
            checksum_sha256=digest,
            content_type=content_type or "application/pdf",
        )

    def get(self, storage_key: str) -> bytes:
        path = self._require_path(storage_key)
        return path.read_bytes()

    def exists(self, storage_key: str) -> bool:
        try:
            return self._path_for(self._safe_key(storage_key)).is_file()
        except ValueError:
            return False

    def delete(self, storage_key: str) -> None:
        try:
            path = self._path_for(self._safe_key(storage_key))
        except ValueError:
            return
        if path.is_file():
            path.unlink()
            logger.info("Deleted curriculum document key=%s", storage_key)

    def open_stream(self, storage_key: str) -> BinaryIO:
        path = self._require_path(storage_key)
        return path.open("rb")

    def _require_path(self, storage_key: str) -> Path:
        path = self._path_for(self._safe_key(storage_key))
        if not path.is_file():
            raise FileNotFoundError(f"Document not found: {storage_key}")
        return path

    def _path_for(self, storage_key: str) -> Path:
        return self._root / storage_key

    @staticmethod
    def _safe_key(storage_key: str) -> str:
        key = (storage_key or "").strip().lstrip("/")
        if not key:
            raise ValueError("storage_key is required")
        if ".." in key.split("/"):
            raise ValueError("storage_key must not contain path traversal")
        return key

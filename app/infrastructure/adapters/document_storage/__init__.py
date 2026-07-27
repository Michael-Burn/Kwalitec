"""Document storage adapters package."""

from app.infrastructure.adapters.document_storage.local_store import (
    LocalDocumentStorageAdapter,
)
from app.infrastructure.adapters.document_storage.metadata import (
    SqlAlchemyDocumentMetadataAdapter,
)
from app.infrastructure.adapters.document_storage.queued_processing import (
    QueuedDocumentProcessingAdapter,
)

__all__ = [
    "LocalDocumentStorageAdapter",
    "QueuedDocumentProcessingAdapter",
    "SqlAlchemyDocumentMetadataAdapter",
]

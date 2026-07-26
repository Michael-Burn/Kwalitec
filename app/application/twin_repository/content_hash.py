"""Deterministic snapshot hash for persisted Twin codec payloads.

Hashing is performed at the Twin persist authority so analytics never
receives Twin aggregates — only the resulting SHA-256 hex digest.

The hash input is the canonical codec JSON string already produced by
``encode_twin`` (sort_keys + compact separators). Analytics never imports
Twin domain modules.
"""

from __future__ import annotations

import hashlib


def compute_twin_snapshot_hash(encoded_twin_payload: str) -> str:
    """Return SHA-256 hex of a Twin codec JSON string.

    Args:
        encoded_twin_payload: Output of ``encode_twin`` (canonical JSON text).

    Returns:
        Lowercase 64-character SHA-256 hex digest.

    Raises:
        ValueError: When ``encoded_twin_payload`` is empty or not a string.
    """
    if not isinstance(encoded_twin_payload, str) or not encoded_twin_payload.strip():
        raise ValueError("encoded_twin_payload must be a non-empty string")
    return hashlib.sha256(encoded_twin_payload.encode("utf-8")).hexdigest()

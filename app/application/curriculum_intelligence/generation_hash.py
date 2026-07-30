"""Deterministic generation hash for Curriculum Intelligence snapshots."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from app.domain.curriculum_intelligence.generation import EducationalNode


def stable_id(prefix: str, *parts: str, length: int = 16) -> str:
    """Derive a short deterministic id from stable parts."""
    material = "\0".join(parts)
    digest = hashlib.sha256(material.encode("utf-8")).hexdigest()
    return f"{prefix}-{digest[:length]}"


def node_fingerprint(node: EducationalNode) -> dict[str, Any]:
    """Stable serialisable fingerprint of one educational node."""
    return {
        "node_id": node.node_id,
        "title": node.title,
        "kind": node.kind,
        "role": node.role,
        "parent_node_id": node.parent_node_id,
        "active": node.active,
        "body": node.body,
        "confidence": round(node.confidence.score, 6),
        "attributes": list(node.attributes),
        "evidence_grade": (
            node.evidence_grade.value if node.evidence_grade is not None else ""
        ),
        "policy_id": node.policy_id or "",
    }


def compute_generation_hash(
    *,
    source_document_ids: tuple[int, ...],
    parent_snapshot_hash: str,
    calibration_profile_id: str | None,
    agent_id: str,
    agent_version: str,
    generation_index: int,
    nodes: tuple[EducationalNode, ...],
) -> str:
    """Compute a deterministic Generation Hash.

    Derived from:
    - source documents
    - parent snapshot hash
    - calibration profile
    - agent versions
    - generation outputs (nodes)
    """
    payload = {
        "source_document_ids": list(source_document_ids),
        "parent_snapshot_hash": parent_snapshot_hash or "",
        "calibration_profile_id": calibration_profile_id or "",
        "agent_id": agent_id,
        "agent_version": agent_version,
        "generation_index": generation_index,
        "nodes": [node_fingerprint(n) for n in sorted(nodes, key=lambda n: n.node_id)],
    }
    encoded = json.dumps(
        payload, sort_keys=True, separators=(",", ":"), ensure_ascii=True
    )
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest()

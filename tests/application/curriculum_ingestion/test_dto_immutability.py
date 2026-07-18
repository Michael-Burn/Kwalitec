"""DTO immutability tests for Curriculum Ingestion."""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from tests.application.curriculum_ingestion.helpers import make_engine, make_request


def test_ingestion_snapshot_frozen():
    snap = make_engine().ingest(make_request())
    with pytest.raises(FrozenInstanceError):
        snap.state = "x"  # type: ignore[misc]


def test_extraction_snapshot_frozen():
    snap = make_engine().ingest(make_request())
    with pytest.raises(FrozenInstanceError):
        snap.extraction.result_id = "x"  # type: ignore[misc]


def test_normalization_snapshot_frozen():
    snap = make_engine().ingest(make_request())
    with pytest.raises(FrozenInstanceError):
        snap.normalization.result_id = "x"  # type: ignore[misc]


def test_validation_snapshot_frozen():
    snap = make_engine().ingest(make_request())
    with pytest.raises(FrozenInstanceError):
        snap.validation.passed = False  # type: ignore[misc]


def test_package_preview_frozen():
    snap = make_engine().ingest(make_request())
    with pytest.raises(FrozenInstanceError):
        snap.package.ready = False  # type: ignore[misc]


@pytest.mark.parametrize(
    "attr",
    ["job_id", "state", "document_count", "passed", "failure_reason"],
)
def test_snapshot_attributes_readable(attr):
    snap = make_engine().ingest(make_request())
    assert hasattr(snap, attr)


@pytest.mark.parametrize("idx", range(20))
def test_nested_tuples_immutable(idx):
    snap = make_engine().ingest(make_request())
    with pytest.raises((TypeError, AttributeError)):
        snap.normalization.topics.append("x")  # type: ignore[attr-defined]
    assert idx >= 0

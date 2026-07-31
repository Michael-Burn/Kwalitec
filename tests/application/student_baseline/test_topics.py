"""Unit tests for SB-001A Baseline topic catalogue helpers."""

from __future__ import annotations

from app.application.student_baseline.topics import (
    list_topic_choices,
    ordered_topic_codes,
)


def test_published_version_returns_empty_without_active_package(ctx):
    choices = list_topic_choices(
        category_code="Published",
        subject_code="NOSUCH",
        curriculum_version="published",
    )
    assert choices == []
    assert (
        ordered_topic_codes(
            category_code="Published",
            subject_code="NOSUCH",
            curriculum_version="published",
        )
        == []
    )


def test_published_topic_choices_from_artefacts(ctx, monkeypatch):
    class FakeSnapshot:
        topics = (
            {
                "topic_id": "node-a",
                "code": "1.1",
                "title": "First topic",
                "display_order": 1,
            },
            {
                "topic_id": "node-b",
                "code": "1.2",
                "title": "Second topic",
                "display_order": 2,
            },
        )

    class FakeService:
        def derive_active(self, subject_code: str):
            assert subject_code == "CS1"
            return FakeSnapshot()

    monkeypatch.setattr(
        "app.application.educational_engine_foundation.service."
        "EducationalEngineFoundationService",
        FakeService,
    )
    choices = list_topic_choices(
        category_code="Published",
        subject_code="CS1",
        curriculum_version="published",
    )
    assert choices == [
        ("1.1", "1.1 — First topic"),
        ("1.2", "1.2 — Second topic"),
    ]
    assert ordered_topic_codes(
        category_code="Published",
        subject_code="CS1",
        curriculum_version="published",
    ) == ["1.1", "1.2"]


def test_missing_subject_returns_empty():
    assert (
        list_topic_choices(
            category_code="Published",
            subject_code="",
            curriculum_version="published",
        )
        == []
    )

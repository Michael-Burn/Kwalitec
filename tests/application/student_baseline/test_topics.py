"""Unit tests for SB-001A Baseline topic catalogue helpers."""

from __future__ import annotations

from app.application.student_baseline.topics import (
    format_baseline_topic_choice,
    list_topic_choices,
    ordered_topic_codes,
)
from app.domain.educational_runtime_engine.student_facing_identity import (
    student_syllabus_code,
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


def test_published_topic_choices_clean_labels(ctx, monkeypatch):
    class FakeSnapshot:
        topics = (
            {
                "topic_id": "node-a",
                "code": "1.1",
                "title": "1.1 Describe the purpose and function of data analysis",
                "display_order": 1,
                "number": "1",
            },
            {
                "topic_id": "node-b",
                "code": "2",
                "title": "1.2 Complete exploratory data analysis",
                "display_order": 2,
                "number": "2",
            },
            {
                "topic_id": "node-junk",
                "code": "15",
                "title": "1 Jln Kilang Timor #06-01 · Singapore 159303",
                "display_order": 15,
                "number": "15",
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
        ("1.1", "1.1 — Describe the purpose and function of data analysis"),
        ("1.2", "1.2 — Complete exploratory data analysis"),
    ]
    assert ordered_topic_codes(
        category_code="Published",
        subject_code="CS1",
        curriculum_version="published",
    ) == ["1.1", "1.2"]


def test_format_rejects_address_noise():
    assert (
        format_baseline_topic_choice(
            code="15",
            title="1 Jln Kilang Timor #06-01 · Singapore 159303",
            number="15",
        )
        is None
    )


def test_student_syllabus_code_prefers_title_over_sequence_index():
    assert (
        student_syllabus_code(
            code="2",
            title="1.2 Complete exploratory data analysis",
            number="2",
        )
        == "1.2"
    )


def test_missing_subject_returns_empty():
    assert (
        list_topic_choices(
            category_code="Published",
            subject_code="",
            curriculum_version="published",
        )
        == []
    )

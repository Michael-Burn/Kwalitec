"""Parametrized matrix coverage for Curriculum Ingestion."""

from __future__ import annotations

import pytest

from app.application.curriculum_ingestion.dto.ingestion_request import (
    DocumentEntryPayload,
    DocumentPayload,
    IngestionRequest,
)
from app.application.curriculum_ingestion.exceptions import ValidationFailed
from app.domain.curriculum_ingestion.curriculum_document import DocumentKind
from app.domain.curriculum_ingestion.ingestion_state import (
    IngestionState,
    IngestionTransitionEvent,
    next_ingestion_state,
)
from tests.application.curriculum_ingestion.helpers import (
    entry,
    make_engine,
    make_request,
    multi_topic_payload,
    syllabus_payload,
)

DOCUMENT_KINDS = [
    DocumentKind.CMP,
    DocumentKind.SYLLABUS,
    DocumentKind.LEARNING_OBJECTIVES,
    DocumentKind.FORMULA_SHEET,
    DocumentKind.SUPPORTING_DOCUMENT,
]

TOPIC_TITLES = [
    "Probability",
    "Random Variables",
    "Expectation",
    "Variance",
    "Discrete Distributions",
    "Continuous Distributions",
    "Hypothesis Testing",
    "Confidence Intervals",
    "Correlation",
    "Regression",
    "Bayes Theorem",
    "Sampling",
    "Estimation",
    "Likelihood",
    "Goodness of Fit",
    "Contingency Tables",
    "Nonparametric Methods",
    "Time Series Intro",
    "Markov Chains Intro",
    "Simulation",
]


@pytest.mark.parametrize("kind", DOCUMENT_KINDS)
def test_classify_declared_kinds(kind):
    payload = DocumentPayload(
        document_id=f"doc-{kind.value}",
        source_ref=f"s3://x/{kind.value}",
        title=f"Doc {kind.value}",
        declared_kind=kind.value,
        entries=(entry("n1", "note", "note text"),),
        metadata=(("subject_code", "CS1"),),
    )
    # formula/supporting may not produce topics — require_pass False
    snap = make_engine().classify_only(
        IngestionRequest(job_id=f"c-{kind.value}", documents=(payload,))
    )
    assert snap.classified_kinds[0][1] == kind.value


@pytest.mark.parametrize("title", TOPIC_TITLES)
def test_ingest_each_topic_title(title):
    payload = syllabus_payload(topic_title=title)
    snap = make_engine().ingest(
        make_request(job_id=f"t-{title[:12]}", documents=(payload,))
    )
    assert snap.passed
    assert any(title in t.title for t in snap.normalization.topics)


@pytest.mark.parametrize("n", range(1, 26))
def test_ingest_topic_counts(n):
    snap = make_engine().ingest(
        make_request(
            job_id=f"count-{n}",
            documents=(multi_topic_payload(n),),
        )
    )
    assert snap.normalization.topic_count == n


@pytest.mark.parametrize(
    "label",
    [f"2026.{n}" for n in range(1, 13)] + [f"2027.{n}" for n in range(1, 6)],
)
def test_metadata_year_labels(label):
    payload = syllabus_payload()
    # rebuild with year metadata
    payload = DocumentPayload(
        document_id=payload.document_id,
        source_ref=payload.source_ref,
        title=payload.title,
        entries=payload.entries,
        declared_kind=payload.declared_kind,
        metadata=(("subject_code", "CS1"), ("version_label", label)),
    )
    snap = make_engine().ingest(
        make_request(job_id=f"y-{label}", documents=(payload,))
    )
    assert ("version_label", label) in snap.normalization.metadata


@pytest.mark.parametrize(
    "event,start,end",
    [
        (
            IngestionTransitionEvent.MARK_CLASSIFIED,
            IngestionState.RECEIVED,
            IngestionState.CLASSIFIED,
        ),
        (
            IngestionTransitionEvent.MARK_EXTRACTED,
            IngestionState.CLASSIFIED,
            IngestionState.EXTRACTED,
        ),
        (
            IngestionTransitionEvent.MARK_NORMALIZED,
            IngestionState.EXTRACTED,
            IngestionState.NORMALIZED,
        ),
        (
            IngestionTransitionEvent.MARK_VALIDATED,
            IngestionState.NORMALIZED,
            IngestionState.VALIDATED,
        ),
        (
            IngestionTransitionEvent.MARK_PREVIEW_READY,
            IngestionState.VALIDATED,
            IngestionState.PREVIEW_READY,
        ),
        (
            IngestionTransitionEvent.MARK_COMPLETED,
            IngestionState.PREVIEW_READY,
            IngestionState.COMPLETED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.CLASSIFIED,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.EXTRACTED,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.NORMALIZED,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.VALIDATED,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.MARK_FAILED,
            IngestionState.PREVIEW_READY,
            IngestionState.FAILED,
        ),
        (
            IngestionTransitionEvent.RESET_TO_RECEIVED,
            IngestionState.FAILED,
            IngestionState.RECEIVED,
        ),
    ],
)
def test_state_transition_matrix(event, start, end):
    assert next_ingestion_state(start, event) is end


@pytest.mark.parametrize(
    "section_number",
    [str(i) for i in range(1, 21)],
)
def test_section_numbers(section_number):
    payload = DocumentPayload(
        document_id="doc-sec",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=(
            entry(
                "s1",
                "section",
                f"Chapter {section_number}",
                number=section_number,
            ),
            entry(
                "t1",
                "topic",
                "Topic",
                number=f"{section_number}.1",
                parent_ref="s1",
            ),
            entry("o1", "objective", "Obj", number="1", parent_ref="t1"),
        ),
    )
    snap = make_engine().ingest(
        make_request(job_id=f"sec-{section_number}", documents=(payload,))
    )
    assert snap.normalization.sections[0].number == section_number


@pytest.mark.parametrize(
    "prereq_count",
    range(0, 8),
)
def test_prerequisite_attributes(prereq_count):
    prereqs = ",".join(f"t{i}" for i in range(prereq_count))
    entries = [
        entry("s1", "section", "Ch1", number="1"),
    ]
    for i in range(max(prereq_count, 1)):
        entries.append(
            entry(f"t{i}", "topic", f"Topic {i}", number=f"1.{i+1}", parent_ref="s1")
        )
        entries.append(
            entry(
                f"o{i}",
                "objective",
                f"Obj {i}",
                number="1",
                parent_ref=f"t{i}",
            )
        )
    # attach prereqs on last topic if any
    if prereq_count:
        last = entries[-2]
        entries[-2] = DocumentEntryPayload(
            entry_id=last.entry_id,
            entry_type=last.entry_type,
            text=last.text,
            number=last.number,
            parent_ref=last.parent_ref,
            attributes=(("prerequisites", prereqs),),
        )
    payload = DocumentPayload(
        document_id="doc-pr",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        metadata=(("subject_code", "CS1"),),
        entries=tuple(entries),
    )
    snap = make_engine().ingest(
        make_request(
            job_id=f"pr-{prereq_count}",
            documents=(payload,),
            require_pass=False,
        )
    )
    assert snap.normalization is not None


@pytest.mark.parametrize(
    "bad_kind",
    ["mission", "session", "activity", "quiz", "lesson"],
)
def test_invalid_declared_kind_rejected_at_document_build(bad_kind):
    from app.application.curriculum_ingestion.exceptions import CurriculumIngestionError

    payload = DocumentPayload(
        document_id="bad",
        source_ref="s3://x",
        title="X",
        declared_kind=bad_kind,
        entries=(entry("n1", "note", "n"),),
    )
    with pytest.raises((CurriculumIngestionError, ValueError)):
        make_engine().ingest(
            IngestionRequest(job_id="bad", documents=(payload,), require_pass=False)
        )


@pytest.mark.parametrize("idx", range(30))
def test_deterministic_repeat(idx):
    engine = make_engine()
    request = make_request(job_id="det-job")
    a = engine.ingest(request)
    b = engine.ingest(request)
    assert a.normalization.topics == b.normalization.topics
    assert a.normalization.sections == b.normalization.sections
    assert a.validation.issue_count == b.validation.issue_count
    assert idx >= 0


def test_require_pass_raises():
    payload = DocumentPayload(
        document_id="lonely",
        source_ref="s3://x",
        title="Syllabus",
        declared_kind="syllabus",
        entries=(
            entry("s1", "section", "Ch1", number="1"),
            entry("t1", "topic", "Lonely", number="1.1", parent_ref="s1"),
        ),
    )
    with pytest.raises(ValidationFailed):
        make_engine().ingest(
            IngestionRequest(job_id="fail", documents=(payload,), require_pass=True)
        )

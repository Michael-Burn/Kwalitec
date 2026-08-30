"""Drift detector D1-D5 tests (ADR-027 Phase 2 Stage 1)."""

from __future__ import annotations

from pathlib import Path

from app.application.student_twin.daily_loop_codec import encode_daily_loop_twin
from app.application.student_twin.drift_detector import (
    CODEC_DECIMAL_PLACES,
    KNOWN_BASELINE_A_WRITER_FRAGMENTS,
    KNOWN_BASELINE_C_WRITER_FRAGMENTS,
    DriftDetector,
)
from app.application.student_twin.query import MapStudyProgress, TopicKnowledgeFact
from app.infrastructure.adapters.student_twin.query_adapter import (
    DailyLoopLearnerTwinQueryAdapter,
)
from tests.application.student_twin.helpers import make_engine, success_events


def _document_with_evidence(topic_id: str = "CS1-A-T01") -> dict:
    engine = make_engine()
    twin = engine.create_twin("learner-d1", twin_id="twin-d1", subject_code="CS1")
    twin = engine.ingest_many(
        twin, success_events(4, topic_id=topic_id, prefix="d1")
    )
    return encode_daily_loop_twin(twin)


# --- D1 ----------------------------------------------------------------------


def test_d1_replay_determinism_matches_persisted_document():
    document = _document_with_evidence()
    report = DriftDetector(engine=make_engine()).check_replay_determinism(document)
    assert report.ok, report.findings
    assert report.findings == ()


def test_d1_detects_corrupted_persisted_map():
    document = _document_with_evidence()
    corrupted = dict(document)
    knowledge = dict(corrupted["estimated_knowledge"])
    topic = next(iter(knowledge))
    knowledge[topic] = round(min(1.0, knowledge[topic] + 0.5), CODEC_DECIMAL_PLACES)
    corrupted["estimated_knowledge"] = knowledge
    report = DriftDetector(engine=make_engine()).check_replay_determinism(corrupted)
    assert not report.ok
    assert any("estimated_knowledge" in f.field for f in report.findings)


# --- D2 ----------------------------------------------------------------------


def test_d2_baseline_detects_existing_a_and_c_writers():
    """Stage 1: existing writers must be reported, not treated as CI failure."""
    inventory = DriftDetector().scan_ek_writers()
    paths = " ".join(h.path for h in inventory.hits)

    for frag in KNOWN_BASELINE_A_WRITER_FRAGMENTS:
        assert frag in paths, f"expected baseline A writer fragment {frag} in {paths}"
    for frag in KNOWN_BASELINE_C_WRITER_FRAGMENTS:
        assert frag in paths, f"expected baseline C writer fragment {frag} in {paths}"

    assert inventory.baseline_writers_present()
    assert inventory.stack_a_hits
    assert inventory.stack_c_hits
    # Explicit Stage 1 posture: presence is inventory, not a fail-closed gate.
    assert len(inventory.hits) > 0


def test_d2_scan_skips_stage1_query_modules():
    inventory = DriftDetector().scan_ek_writers()
    for hit in inventory.hits:
        assert "application/student_twin/query" not in hit.path
        assert "application/student_twin/drift_detector" not in hit.path


# --- D3 ----------------------------------------------------------------------


def test_d3_identity_hygiene_accepts_published_ids():
    report = DriftDetector().check_identity_hygiene(["CS1-A-T01", "CS1-B-T03"])
    assert report.ok
    assert report.violations == ()


def test_d3_identity_hygiene_flags_blank_int_and_node():
    report = DriftDetector().check_identity_hygiene(
        ["", "42", "node-internal", "CS1-A-T01"]
    )
    assert not report.ok
    assert "" in report.violations
    assert "42" in report.violations
    assert "node-internal" in report.violations
    assert "CS1-A-T01" not in report.violations


def test_d3_document_hygiene():
    document = _document_with_evidence(topic_id="CS1-A-T01")
    assert DriftDetector().check_identity_hygiene_in_document(document).ok
    bad = dict(document)
    knowledge = dict(bad["estimated_knowledge"])
    knowledge["node-x"] = 0.5
    bad["estimated_knowledge"] = knowledge
    assert not DriftDetector().check_identity_hygiene_in_document(bad).ok


# --- D4 ----------------------------------------------------------------------


def test_d4_study_progress_not_ek_invariant():
    class _Persist:
        def load_twin(self, *, learner_id: str, subject_code: str | None = None):
            return None

    adapter = DailyLoopLearnerTwinQueryAdapter(
        persistence=_Persist(),
        study_progress=MapStudyProgress({"CS1-A-T01"}),
    )
    fact = adapter.topic_knowledge(
        user_id=1, subject_code="CS1", topic_id="CS1-A-T01"
    )
    covered = adapter.topic_covered(
        user_id=1, subject_code="CS1", topic_id="CS1-A-T01"
    )
    assert covered is True
    assert fact.has_estimated_knowledge is False
    assert DriftDetector.check_study_progress_not_ek(
        topic_covered=covered,
        fact=fact,
        twin_has_topic_evidence=False,
    )


def test_d4_invariant_fails_if_fact_claims_ek_without_evidence():
    dishonest = TopicKnowledgeFact(
        topic_id="CS1-A-T01",
        has_estimated_knowledge=True,
        estimated_knowledge=0.5,
        estimated_mastery=0.5,
        evidence_count=0,
        last_practised_at=None,
    )
    assert not DriftDetector.check_study_progress_not_ek(
        topic_covered=True,
        fact=dishonest,
        twin_has_topic_evidence=False,
    )


# --- D5 ----------------------------------------------------------------------


def test_d5_scale_accepts_unit_interval_document():
    document = _document_with_evidence()
    report = DriftDetector().check_scale(document)
    assert report.ok, report.violations


def test_d5_scale_rejects_out_of_range():
    document = _document_with_evidence()
    bad = dict(document)
    knowledge = dict(bad["estimated_knowledge"])
    topic = next(iter(knowledge))
    knowledge[topic] = 1.5
    bad["estimated_knowledge"] = knowledge
    report = DriftDetector().check_scale(bad)
    assert not report.ok
    assert report.violations


def test_d5_scale_rejects_negative_overall():
    document = _document_with_evidence()
    bad = dict(document)
    bad["overall_knowledge"] = -0.01
    report = DriftDetector().check_scale(bad)
    assert not report.ok


def test_codec_decimal_places_is_six():
    assert CODEC_DECIMAL_PLACES == 6
    assert Path(__file__).name == "test_drift_detector.py"

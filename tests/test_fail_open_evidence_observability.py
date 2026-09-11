"""Fail-open evidence writers: honest observability without changing UX.

Covers Twin consume, mission-complete under the evidence gate, SQL companion
write-through, and the VP-001 outer wrapper. Student requests still succeed;
failures must be distinguishable from benign skips and countable.
"""

from __future__ import annotations

from unittest.mock import MagicMock, patch

import pytest

from app.application.educational_runtime_engine.exceptions import (
    MissionAlreadyCompleted,
)
from app.application.founder_validation.telemetry import DEFAULT_FV_TELEMETRY
from app.application.learning_session.dto.candidate_observation import (
    RuntimeEvidenceType,
)
from app.application.learning_session.dto.evidence_package import (
    EvidenceDisposition,
)
from app.infrastructure.adapters.learning_session.runtime_engine import (
    LearningSessionRuntimeEngine,
    MissionCompleteResult,
)
from app.presentation.session.sitting_report import build_sitting_report
from app.services.educational_yield_metrics import EducationalYieldMetrics


@pytest.fixture(autouse=True)
def _clear_fv_telemetry():
    DEFAULT_FV_TELEMETRY.clear()
    yield
    DEFAULT_FV_TELEMETRY.clear()


def _fv_kinds() -> list[str]:
    # Events are not listed in snapshot; inspect via private store for tests.
    with DEFAULT_FV_TELEMETRY._lock:
        return [e.kind for e in DEFAULT_FV_TELEMETRY._events]


# ---------------------------------------------------------------------------
# Location A: Twin yield metric honesty + fail-open signal
# ---------------------------------------------------------------------------


class TestTwinYieldMetricHonesty:
    def test_authorized_but_failed_consume_is_not_twin_updated(self):
        packages = [
            {
                "validation": {
                    "disposition": EvidenceDisposition.ACCEPTED.value,
                    "may_update_twin": True,
                },
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                ],
                "twin_updated": False,
                "twin_status": "active",
                "twin_consumption": {
                    "twin_updated": False,
                    "reason": "twin_consume_failed_open",
                    "twin_status": None,
                },
            }
        ]
        snap = EducationalYieldMetrics.from_packages(packages)
        assert snap.twin_updated_sittings == 0
        assert snap.twin_consume_failed_open == 1

    def test_genuine_twin_update_counts(self):
        packages = [
            {
                "validation": {"may_update_twin": True},
                "twin_updated": True,
                "twin_consumption": {
                    "twin_updated": True,
                    "reason": "accepted_educational_plus_consumed",
                    "twin_status": "active",
                },
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                ],
            }
        ]
        snap = EducationalYieldMetrics.from_packages(packages)
        assert snap.twin_updated_sittings == 1
        assert snap.twin_consume_failed_open == 0

    def test_ignored_reason_does_not_count_as_failed_open(self):
        packages = [
            {
                "validation": {"may_update_twin": False},
                "twin_updated": False,
                "twin_consumption": {
                    "twin_updated": False,
                    "reason": "twin_daily_loop_flag_off",
                },
            }
        ]
        snap = EducationalYieldMetrics.from_packages(packages)
        assert snap.twin_updated_sittings == 0
        assert snap.twin_consume_failed_open == 0


class TestTwinConsumeFailOpenSignal:
    def test_consume_exception_emits_distinct_signal_and_exc_info(self):
        consumer = MagicMock()
        consumer.consume.side_effect = RuntimeError("twin store down")
        engine = LearningSessionRuntimeEngine(twin_consumer=consumer)

        with patch(
            "app.infrastructure.adapters.learning_session.runtime_engine.logger"
        ) as log:
            result = engine._consume_twin_evidence({"package_id": "pkg-1"})

        assert result["twin_updated"] is False
        assert result["reason"] == "twin_consume_failed_open"
        assert "twin_consume_failed_open" in _fv_kinds()
        log.warning.assert_called()
        kwargs = log.warning.call_args.kwargs
        assert kwargs.get("exc_info") is True


# ---------------------------------------------------------------------------
# Location B: Mission-complete result distinction + Sitting Report honesty
# ---------------------------------------------------------------------------


class TestMissionCompleteResultDistinction:
    def test_already_completed_is_benign_not_failed_open(self):
        completer = MagicMock()
        completer.complete_mission.side_effect = MissionAlreadyCompleted("mid-1")
        engine = LearningSessionRuntimeEngine(mission_completer=completer)

        result = engine._complete_mission_if_authorised(
            student_id="4",
            mission_instance_id="mid-1",
            advance_progress=True,
            package_id="pkg-1",
        )
        assert isinstance(result, MissionCompleteResult)
        assert result.status == "already_completed"
        assert result.mission_completed is True
        assert result.failed_open is False
        assert "evidence_gate_mission_complete_failed" not in _fv_kinds()

    def test_genuine_write_failure_is_failed_open_with_signal(self):
        completer = MagicMock()
        completer.complete_mission.side_effect = RuntimeError("db unavailable")
        engine = LearningSessionRuntimeEngine(mission_completer=completer)

        with patch(
            "app.infrastructure.adapters.learning_session.runtime_engine.logger"
        ) as log:
            result = engine._complete_mission_if_authorised(
                student_id="4",
                mission_instance_id="mid-1",
                advance_progress=True,
                package_id="pkg-1",
            )

        assert result.status == "failed_open"
        assert result.mission_completed is False
        assert result.failed_open is True
        assert "evidence_gate_mission_complete_failed" in _fv_kinds()
        kwargs = log.warning.call_args.kwargs
        assert kwargs.get("exc_info") is True

    def test_skipped_no_mission_is_benign(self):
        engine = LearningSessionRuntimeEngine(mission_completer=MagicMock())
        result = engine._complete_mission_if_authorised(
            student_id="4",
            mission_instance_id="",
            advance_progress=True,
            package_id="pkg-1",
        )
        assert result.status == "skipped_no_mission"
        assert result.failed_open is False
        assert "evidence_gate_mission_complete_failed" not in _fv_kinds()


class TestSittingReportMissionFailOpenCopy:
    def test_failed_open_does_not_use_policy_journey_language(self):
        report = build_sitting_report(
            topic_title="Cash flows",
            opaque_summary={
                "finish_review": {"verdict": "yes"},
                "substance": "package",
                "mission_complete_status": "failed_open",
                "observations": [
                    {"type_id": RuntimeEvidenceType.PRACTICE_CORRECT.value},
                ],
            },
            metadata={
                "progress_advanced": "false",
                "mission_completed": "false",
                "mission_complete_status": "failed_open",
                "evidence_disposition": "accepted",
            },
        )
        explanation = report.progress_explanation.lower()
        assert (
            "could not be recorded" in explanation
            or "could not be updated" in explanation
        )
        assert "study is accepted" not in explanation
        assert "progress stayed" not in explanation
        assert "honest finish" not in explanation


# ---------------------------------------------------------------------------
# Location C: SQL companion distinct failure signal
# ---------------------------------------------------------------------------


class TestSqlEvidenceFailOpenSignal:
    def test_unexpected_failure_emits_distinct_signal(self):
        from app.application.student_runtime.evidence_write_through import (
            maybe_write_sql_evidence_from_sitting,
        )

        with patch(
            "app.application.student_runtime.evidence_write_through."
            "_write_sql_evidence_from_sitting",
            side_effect=RuntimeError("flush failed"),
        ):
            result = maybe_write_sql_evidence_from_sitting(
                user_id=4,
                session_id="sess-sql-fail",
                mission_instance_id="mid-sql",
                store=MagicMock(),
            )
        assert result is None
        assert "sql_evidence_write_through_failed" in _fv_kinds()

    def test_benign_flag_off_does_not_emit_failure_signal(self, app, ctx):
        from app.application.student_runtime.evidence_write_through import (
            maybe_write_sql_evidence_from_sitting,
        )

        with patch(
            "app.application.student_runtime.evidence_write_through."
            "resolve_v2_feature_flags",
            return_value=MagicMock(SR_SESSION_SQL_EVIDENCE_COMPANION=False),
        ):
            result = maybe_write_sql_evidence_from_sitting(
                user_id=4,
                session_id="sess-sql-skip",
                mission_instance_id="mid-sql",
                store=MagicMock(),
            )
        assert result is None
        assert "sql_evidence_write_through_failed" not in _fv_kinds()


# ---------------------------------------------------------------------------
# Location D: VP-001 outer wrapper no longer swallows at debug
# ---------------------------------------------------------------------------


class TestVp001OuterWrapperObservability:
    def test_outer_wrapper_records_system_failure_not_debug(self, app, ctx, user):
        from app.presentation.session import views

        with app.test_request_context():
            from flask_login import login_user

            login_user(user)
            with patch(
                "app.infrastructure.adapters.learner_lifecycle.record_session_evidence",
                side_effect=RuntimeError("import-path boom"),
            ), patch(
                "app.presentation.session.views.logger"
            ) as log:
                views._vp001_record_evidence(
                    session_id="sess-vp001-outer",
                    event="practice_attempt",
                )

        assert "evidence" in _fv_kinds()
        assert DEFAULT_FV_TELEMETRY.snapshot()["system_failures"] >= 1
        log.exception.assert_called()
        log.debug.assert_not_called()

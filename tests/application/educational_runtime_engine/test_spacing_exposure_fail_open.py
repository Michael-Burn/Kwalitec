"""QG item 4 Finding 2 residual: spacing write must not fail the completed mission."""

from __future__ import annotations

import logging
from datetime import date

from app.application.educational_runtime_engine.service import (
    EducationalRuntimeEngineService,
)


def test_spacing_write_failure_is_logged_not_raised(ctx, monkeypatch, caplog):
    class _BrokenScheduler:
        def record_completed_exposure(self, **kwargs):
            raise RuntimeError("spacing store down")

    monkeypatch.setattr(
        "app.application.spacing_scheduler.get_spacing_scheduler",
        lambda: _BrokenScheduler(),
    )
    monkeypatch.setattr(
        "app.application.educational_runtime_engine.confidence_ladder_adapter."
        "ladder_step_delta_for_completed_sitting",
        lambda **kwargs: 0,
    )
    runtime = EducationalRuntimeEngineService()
    with caplog.at_level(logging.ERROR):
        runtime._record_spacing_exposure_for_completion(
            user_id=1,
            package_id="PACK-1",
            completed_on=date(2026, 9, 15),
            mission_instance_id="mid-1",
        )
    assert "spacing_exposure_write_failed" in caplog.text
    assert "PACK-1" in caplog.text

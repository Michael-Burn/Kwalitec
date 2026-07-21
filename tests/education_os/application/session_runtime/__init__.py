"""Shared helpers for Study Session Runtime tests (V3-004)."""

from __future__ import annotations

from presentation.study_session import SessionPresenter, StudySessionViewModel


def make_view_model() -> StudySessionViewModel:
    """Return a deterministic null-safe study session view model."""
    return SessionPresenter.present(None)

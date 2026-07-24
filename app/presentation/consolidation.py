"""Legacy presentation redirects for sole-runtime Education OS.

READY FOR MIGRATION shells stay registered but send learners to the
canonical Student Experience when ``KWALITEC_V2_SOLE_RUNTIME`` is set.
Protected educational engines and V1 data paths are not deleted.
"""

from __future__ import annotations

from flask import redirect, url_for

from app.application.config.v2_flags import resolve_v2_feature_flags


def redirect_if_sole_runtime(endpoint: str = "student.home", **values):
    """Return a redirect to the canonical surface when sole runtime is on.

    Returns None when dual-run / legacy default is active so callers continue.
    """
    if resolve_v2_feature_flags().SOLE_RUNTIME:
        return redirect(url_for(endpoint, **values))
    return None

"""PX-003 Phase 1 — student session path declaration (PX-B-014).

Authoritative happy path under sole runtime (``KWALITEC_V2_SOLE_RUNTIME``):

    Home → Start Today's Session / Continue → ``/session/<id>/*``
    Overview → Activity → Reflection → Summary → Finish (confirm)
    → Sitting Report (Complete surface) → Home

Legacy ``/missions/<id>/session`` remains registered for rollback only and
redirects to Student Home when sole runtime is on. Do not teach both paths
as product. Selection, Twin, and educational package bodies are unchanged.
"""

from __future__ import annotations

AUTHORITATIVE_SESSION_PREFIX = "/session"
LEGACY_MISSION_SESSION_PREFIX = "/missions"
SOLE_RUNTIME_DECLARES_SESSION_PRIMARY = True

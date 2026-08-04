"""Ops expected-day labels vs student chrome (PX-B-003).

Ops / PB verification harnesses may carry scripted ``expected_day`` /
``ops_expected_day`` sequences that run ahead or behind the package-path
``campaign_day`` detected from LIVE HTML. Those labels are **ops tooling
only**.

Rules:
1. Never render ``expected_day`` / ``ops_expected_day`` on student Home,
   Finish, Mission, Session, Profile, or Journey chrome.
2. Student chrome identity comes from ``educational_package_id`` /
   ``resolve_package_for_tomorrow_chrome`` / Runtime mission payload.
3. Package-path Progressive Confidence PASS must not be failed solely
   because an ops detector label desynced (offset class).

Related residuals: RO6-R1 … RO15-R2 · PB15-R2 · PB14-R3.
"""

from __future__ import annotations

# Detector field names that must stay out of student DTOs / templates.
OPS_ONLY_DAY_LABEL_KEYS = frozenset(
    {
        "expected_day",
        "ops_expected_day",
        "detected_campaign_day",
    }
)

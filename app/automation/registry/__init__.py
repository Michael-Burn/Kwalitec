"""AutomationRegistry — register and look up automation workflows."""

from __future__ import annotations

from app.automation.registry.bootstrap import build_default_registry
from app.automation.registry.registry import AutomationRegistry

__all__ = [
    "AutomationRegistry",
    "build_default_registry",
]

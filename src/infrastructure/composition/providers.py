"""Concrete infrastructure providers used by the composition root."""

from __future__ import annotations

from infrastructure.runtime.clock import SystemClock
from infrastructure.runtime.event_publisher import (
    ApplicationEventHandler,
    SynchronousApplicationEventPublisher,
)
from infrastructure.runtime.uuid_generator import SystemUUIDGenerator

# Backwards-compatible alias; milestone expects `SystemUUIDGenerator`.
UUID4Generator = SystemUUIDGenerator

__all__ = [
    "ApplicationEventHandler",
    "SynchronousApplicationEventPublisher",
    "SystemClock",
    "SystemUUIDGenerator",
    "UUID4Generator",
]


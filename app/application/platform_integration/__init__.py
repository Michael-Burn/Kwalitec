"""PI-002A — Platform Integration: Founder → Student Bridge.

Connects founder-published curriculum packages to student discovery and
enrolment while preserving Runtime A as the default production path.
Runtime C is reachable only through controlled, auditable routing.
"""

from app.application.platform_integration.discovery import (
    PUBLISHED_CATEGORY_CODE,
    PublishedSubjectDiscoveryService,
)
from app.application.platform_integration.dto import (
    EnrolmentBridgeResult,
    PublishedSubjectOffer,
    RoutingDecision,
)
from app.application.platform_integration.enrolment_bridge import (
    FounderStudentEnrolmentBridge,
)
from app.application.platform_integration.flags import (
    FounderStudentBridgeFlags,
    resolve_founder_student_bridge_flags,
)
from app.application.platform_integration.routing import RuntimeRoutingService

__all__ = [
    "PUBLISHED_CATEGORY_CODE",
    "EnrolmentBridgeResult",
    "FounderStudentBridgeFlags",
    "FounderStudentEnrolmentBridge",
    "PublishedSubjectDiscoveryService",
    "PublishedSubjectOffer",
    "RoutingDecision",
    "RuntimeRoutingService",
    "resolve_founder_student_bridge_flags",
]

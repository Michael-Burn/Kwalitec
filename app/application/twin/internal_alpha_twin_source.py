"""Internal Alpha TwinSource — interim cold-start Twin for developer daily use.

Provides a structural Digital Twin (identity + empty belief domains) so
Educational Orchestrator can compose a truthful cold-start Experience.

This is the TwinProvider architecture "interim source" — not TwinRepository,
not Mid preparedness theatre, and not legacy mastery converted into Twin
beliefs. Empty domains keep Decision / Readiness on the honest cold-start
path until durable Twin persistence lands.
"""

from __future__ import annotations

from app.application.twin.twin_provider import TwinRetrievalContext
from app.domain.twin.digital_twin import DigitalTwin
from app.domain.twin.identity_state import IdentityState


class InternalAlphaTwinSource:
    """Interim TwinSource for Educational Intelligence Internal Alpha.

    ``load`` always returns a structural cold-start Twin for the authorised
    student identity. Never invents Knowledge / Memory / Performance beliefs.
    """

    def load(
        self,
        student_id: str,
        *,
        context: TwinRetrievalContext | None = None,
    ) -> DigitalTwin | None:
        """Return a structural cold-start Twin for the requested student.

        Args:
            student_id: Authorised learner identity (already ownership-validated).
            context: Optional retrieval scope; ``curriculum_id`` anchors Identity.

        Returns:
            A frozen ``DigitalTwin`` with identity only and empty domains.
        """
        curriculum_id = None
        if context is not None and context.curriculum_id:
            curriculum_id = context.curriculum_id.strip() or None

        identity = IdentityState.create(
            student_id,
            curriculum_id=curriculum_id,
        )
        return DigitalTwin.create(identity)

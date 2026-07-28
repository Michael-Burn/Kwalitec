"""Decision Journal invariants (ILE-002).

Educational memory rules: append-only evidence, lawful lifecycle moves,
and student-safe language (no engineering leakage, no shame).
"""

from __future__ import annotations

from app.domain.decision_journal.enums import JournalLifecycleStatus

# Lawful status transitions. Evidence may append at several stages without
# forcing a status change; explicit ``evidence_evolving`` is optional.
_ALLOWED: dict[JournalLifecycleStatus, frozenset[JournalLifecycleStatus]] = {
    JournalLifecycleStatus.RECOMMENDED: frozenset(
        {
            JournalLifecycleStatus.ACCEPTED,
            JournalLifecycleStatus.DEFERRED,
            JournalLifecycleStatus.EVIDENCE_EVOLVING,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.ACCEPTED: frozenset(
        {
            JournalLifecycleStatus.EVIDENCE_EVOLVING,
            JournalLifecycleStatus.REFLECTED,
            JournalLifecycleStatus.OUTCOME_RECORDED,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.DEFERRED: frozenset(
        {
            JournalLifecycleStatus.ACCEPTED,
            JournalLifecycleStatus.EVIDENCE_EVOLVING,
            JournalLifecycleStatus.REFLECTED,
            JournalLifecycleStatus.OUTCOME_RECORDED,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.EVIDENCE_EVOLVING: frozenset(
        {
            JournalLifecycleStatus.REFLECTED,
            JournalLifecycleStatus.OUTCOME_RECORDED,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.REFLECTED: frozenset(
        {
            JournalLifecycleStatus.OUTCOME_RECORDED,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.OUTCOME_RECORDED: frozenset(
        {
            # ILE-005: optional reflection may follow an educational outcome.
            # Outcome summary remains; history is never rewritten.
            JournalLifecycleStatus.REFLECTED,
            JournalLifecycleStatus.ARCHIVED,
        }
    ),
    JournalLifecycleStatus.ARCHIVED: frozenset(),
}


def can_transition(
    current: JournalLifecycleStatus | str,
    target: JournalLifecycleStatus | str,
) -> bool:
    """Return True when ``current`` → ``target`` is a lawful lifecycle move."""
    cur = JournalLifecycleStatus(str(current))
    nxt = JournalLifecycleStatus(str(target))
    if cur == nxt:
        return True
    return nxt in _ALLOWED.get(cur, frozenset())


# Terms that must never appear in student-visible journal fields.
FORBIDDEN_STUDENT_TERMS: tuple[str, ...] = (
    "digital twin",
    "student twin",
    "twin state",
    "adaptive decision",
    "learning orchestrator",
    "mission engine",
    "curriculum graph",
    "warrant id",
    "ranking algorithm",
    "mastery score",
    "entity_id",
    "pipeline",
)


def assert_student_safe_text(text: str, *, field: str = "text") -> None:
    """Raise ValueError if ``text`` leaks implementation detail to learners."""
    lowered = (text or "").lower()
    for term in FORBIDDEN_STUDENT_TERMS:
        if term in lowered:
            raise ValueError(
                f"Decision Journal {field} must not expose '{term}'"
            )

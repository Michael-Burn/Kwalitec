"""Educational growth milestones from sitting memory (KWP-011).

Milestones represent educational growth — never points, badges, or
leaderboards.
"""

from __future__ import annotations

from typing import Any

from app.application.educational_memory.dto import (
    MILESTONE_TITLES,
    LearningMilestone,
    MilestoneKind,
)
from app.application.educational_memory.snapshot import snapshot_from_package
from app.application.learning_strategy.dto import StrategyEvidenceInput


def detect_learning_milestones(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> tuple[LearningMilestone, ...]:
    """Detect educational milestones from Evidence Packages + snapshots."""
    ordered = _chronological(packages, student_id=student_id)
    if not ordered:
        return ()

    milestones: list[LearningMilestone] = []
    recovery_done = False
    mastery_done = False
    forgotten_done = False
    difficult_done = False
    alignment_done = False
    best_streak = 0
    current_streak = 0
    streak_session = ""
    streak_topic = ""
    streak_at = ""

    for pkg_index, package in enumerate(ordered):
        snap = snapshot_from_package(package)
        practice = StrategyEvidenceInput.from_opaque(package)
        topic = str(package.get("topic_title") or "").strip() or "a topic"
        stamp = str(
            (snap.captured_at if snap else "")
            or package.get("created_at")
            or ""
        )
        session_id = str(package.get("session_id") or "")
        strategy_action = str((snap.strategy if snap else {}).get("action") or "")
        calibration = str((snap.strategy if snap else {}).get("calibration") or "")
        observed = str(
            (snap.difficulty if snap else {}).get("observed_difficulty") or ""
        )
        eff_verdict = str(
            (snap.effectiveness if snap else {}).get("verdict") or ""
        )
        prior_kind = str(
            (snap.prior_intervention if snap else {}).get("kind") or ""
        )

        if _is_strong(practice) and practice.finish_verdict == "yes":
            current_streak += 1
            if current_streak > best_streak:
                best_streak = current_streak
                streak_session = session_id
                streak_topic = topic
                streak_at = stamp
        else:
            current_streak = 0

        if not recovery_done and (
            (prior_kind == "recovery" and eff_verdict == "effective")
            or (
                strategy_action == "recover_prior_knowledge"
                and _is_strong(practice)
            )
        ):
            recovery_done = True
            milestones.append(
                LearningMilestone(
                    kind=MilestoneKind.FIRST_SUCCESSFUL_RECOVERY,
                    title=MILESTONE_TITLES[
                        MilestoneKind.FIRST_SUCCESSFUL_RECOVERY
                    ],
                    narrative=(
                        f"You recovered understanding of {topic} after "
                        "difficulty — an important educational moment."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    recorded_at=stamp,
                    evidence_codes=("first_recovery",),
                )
            )

        if (
            not mastery_done
            and _is_strong(practice)
            and practice.progress_advanced
            and best_streak >= 2
        ):
            mastery_done = True
            milestones.append(
                LearningMilestone(
                    kind=MilestoneKind.FIRST_SUSTAINED_MASTERY,
                    title=MILESTONE_TITLES[
                        MilestoneKind.FIRST_SUSTAINED_MASTERY
                    ],
                    narrative=(
                        f"Sustained strong practice on {topic} supports "
                        "your first mastery signals."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    recorded_at=stamp,
                    evidence_codes=("sustained_mastery",),
                )
            )

        if (
            not forgotten_done
            and (
                practice.retention_risk
                or strategy_action == "recover_prior_knowledge"
            )
            and _is_strong(practice)
        ):
            forgotten_done = True
            milestones.append(
                LearningMilestone(
                    kind=MilestoneKind.RECOVERED_FORGOTTEN_KNOWLEDGE,
                    title=MILESTONE_TITLES[
                        MilestoneKind.RECOVERED_FORGOTTEN_KNOWLEDGE
                    ],
                    narrative=(
                        f"You recovered knowledge of {topic} that had begun "
                        "to fade."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    recorded_at=stamp,
                    evidence_codes=("forgotten_recovered",),
                )
            )

        if (
            not difficult_done
            and observed in {"demanding", "very_demanding"}
            and (_is_strong(practice) or practice.progress_advanced)
        ):
            difficult_done = True
            milestones.append(
                LearningMilestone(
                    kind=MilestoneKind.COMPLETED_DIFFICULT_TOPIC,
                    title=MILESTONE_TITLES[
                        MilestoneKind.COMPLETED_DIFFICULT_TOPIC
                    ],
                    narrative=(
                        f"You completed demanding work on {topic} with "
                        "honest evidence of progress."
                    ),
                    topic_title=topic,
                    session_id=session_id,
                    recorded_at=stamp,
                    evidence_codes=("difficult_completed",),
                )
            )

        if (
            not alignment_done
            and calibration == "healthy"
            and _is_strong(practice)
        ):
            # Prefer when prior mismatch existed somewhere earlier.
            prior_mismatch = any(
                str(
                    (
                        snapshot_from_package(p).strategy
                        if snapshot_from_package(p)
                        else {}
                    ).get("calibration")
                    or ""
                )
                in {"over_confident", "under_confident"}
                for p in ordered[:pkg_index]
            )
            if prior_mismatch:
                alignment_done = True
                milestones.append(
                    LearningMilestone(
                        kind=MilestoneKind.IMPROVED_CONFIDENCE_ALIGNMENT,
                        title=MILESTONE_TITLES[
                            MilestoneKind.IMPROVED_CONFIDENCE_ALIGNMENT
                        ],
                        narrative=(
                            "Your confidence and performance are better "
                            "aligned than earlier sittings suggested."
                        ),
                        topic_title=topic,
                        session_id=session_id,
                        recorded_at=stamp,
                        evidence_codes=("confidence_aligned",),
                    )
                )

    if best_streak >= 3:
        milestones.append(
            LearningMilestone(
                kind=MilestoneKind.LONGEST_CONSISTENCY_STREAK,
                title=MILESTONE_TITLES[
                    MilestoneKind.LONGEST_CONSISTENCY_STREAK
                ],
                narrative=(
                    f"Your longest stretch of strong, completed sittings "
                    f"reached {best_streak} in a row"
                    + (f" (through {streak_topic})." if streak_topic else ".")
                ),
                topic_title=streak_topic,
                session_id=streak_session,
                recorded_at=streak_at,
                evidence_codes=("consistency_streak", str(best_streak)),
            )
        )

    return tuple(milestones)


def _chronological(
    packages: list[dict[str, Any]] | tuple[dict[str, Any], ...],
    *,
    student_id: str = "",
) -> list[dict[str, Any]]:
    sid = (student_id or "").strip()
    rows = [
        p
        for p in packages
        if isinstance(p, dict)
        and (not sid or str(p.get("student_id") or "").strip() == sid)
    ]
    rows.sort(key=lambda p: str(p.get("created_at") or ""))
    return rows


def _is_strong(practice: StrategyEvidenceInput) -> bool:
    scored = practice.practice_correct + practice.practice_incorrect
    if scored <= 0:
        return False
    return practice.practice_correct >= practice.practice_incorrect and scored >= 2

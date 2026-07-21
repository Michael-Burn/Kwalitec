"""OnboardingPresenter — OnboardingSnapshot → OnboardingViewModel.

Presentation orchestration only. Assembles Design System chrome for first-run
collection. Never diagnoses, recommends, persists, plans missions, or calls AI.
"""

from __future__ import annotations

from application.onboarding.results import CompletedOnboarding, OnboardingSnapshot
from presentation.design_system import ContainerWidth, PageHeader
from presentation.onboarding.onboarding_mapper import OnboardingMapper
from presentation.onboarding.onboarding_view_model import OnboardingViewModel

_EMPTY_HEADER = PageHeader(
    title="Student Onboarding",
    description=(
        "Gather structured educational evidence so your Student Twin can begin "
        "honestly. No diagnosis or recommendations in this flow."
    ),
    eyebrow="First run",
)


class OnboardingPresenter:
    """Present the immutable first-run onboarding surface."""

    @classmethod
    def present(
        cls,
        snapshot: OnboardingSnapshot | None = None,
        *,
        completed: CompletedOnboarding | None = None,
    ) -> OnboardingViewModel:
        if completed is not None:
            return cls._completed(completed)
        if snapshot is None:
            return cls._empty()
        step_key = snapshot.current_step.value
        current = OnboardingMapper.map_current_step(
            step_key=step_key,
            payloads=snapshot.payloads,
        )
        review_lines = (
            OnboardingMapper.map_review_lines(snapshot.payloads)
            if step_key == "review"
            else ()
        )
        primary_key = "complete" if step_key == "review" else "advance"
        return OnboardingViewModel(
            header=PageHeader(
                title="Student Onboarding",
                description=current.description,
                eyebrow=current.title,
            ),
            stepper=OnboardingMapper.map_stepper(
                current_step=step_key,
                saved_steps=snapshot.saved_steps,
            ),
            progress_bar=OnboardingMapper.map_progress(snapshot.progress_percent),
            current_step=current,
            primary_button=OnboardingMapper.primary_action(step_key=step_key),
            secondary_button=OnboardingMapper.secondary_action(step_key=step_key),
            skip_button=OnboardingMapper.skip_action(step_key=step_key),
            primary_action_key=primary_key,
            review_lines=review_lines,
            container_width=ContainerWidth.CONTENT,
            onboarding_id=snapshot.onboarding_id,
            student_id=snapshot.student_id,
            status_label=snapshot.status.value,
            progress_percent=snapshot.progress_percent,
            is_complete=False,
        )

    @classmethod
    def _empty(cls) -> OnboardingViewModel:
        current = OnboardingMapper.map_current_step(step_key="welcome", payloads={})
        return OnboardingViewModel(
            header=_EMPTY_HEADER,
            stepper=OnboardingMapper.map_stepper(
                current_step="welcome",
                saved_steps=(),
            ),
            progress_bar=OnboardingMapper.map_progress(0.0),
            current_step=current,
            primary_button=OnboardingMapper.primary_action(step_key="welcome"),
            container_width=ContainerWidth.CONTENT,
            status_label="not_started",
        )

    @classmethod
    def _completed(cls, completed: CompletedOnboarding) -> OnboardingViewModel:
        current = OnboardingMapper.map_current_step(step_key="review", payloads={})
        return OnboardingViewModel(
            header=PageHeader(
                title="Student Twin ready",
                description=(
                    "Your declarations are sealed. Continuing to the dashboard."
                ),
                eyebrow="Complete",
            ),
            stepper=OnboardingMapper.map_stepper(
                current_step="review",
                saved_steps=(
                    "welcome",
                    "ifoa_profile",
                    "exam_history",
                    "weekly_availability",
                    "confidence",
                    "study_habits",
                    "optional_diagnostic",
                    "review",
                ),
            ),
            progress_bar=OnboardingMapper.map_progress(100.0),
            current_step=current,
            primary_button=None,
            container_width=ContainerWidth.CONTENT,
            onboarding_id=completed.onboarding_id,
            student_id=completed.student_id,
            status_label="completed",
            progress_percent=100.0,
            is_complete=True,
            redirect_path=completed.redirect_path,
        )

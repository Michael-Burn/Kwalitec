"""Operator-facing validation guidance for Curriculum Studio (PR-001A).

Maps finding codes to issue / why-it-matters / recovery copy. Presentation
projects these fields; routes do not invent educational rules.
"""

from __future__ import annotations

from dataclasses import dataclass

from app.domain.curriculum_studio.validation_summary import ValidationFinding


@dataclass(frozen=True)
class FindingGuidance:
    """Operator guidance for one validation finding code."""

    issue: str
    why_it_matters: str
    recovery_action: str


VALIDATION_FINDING_GUIDANCE: dict[str, FindingGuidance] = {
    "missing_cmp": FindingGuidance(
        issue="CMP source is not present.",
        why_it_matters=(
            "Without a Curriculum Master Pack reference the Studio cannot "
            "derive sections, topics, or learning objectives for students."
        ),
        recovery_action=(
            "Assign a version label, enter a CMP reference "
            "(for example ref://cmp/subject-2026), then upload sources "
            "and run Validate Curriculum again."
        ),
    ),
    "missing_syllabus": FindingGuidance(
        issue="Official syllabus source is not present.",
        why_it_matters=(
            "Publication must stay grounded in the official syllabus so "
            "student journeys follow authorised curriculum order."
        ),
        recovery_action=(
            "Enter a syllabus reference (for example "
            "ref://syllabus/subject-2026), upload sources, then run "
            "Validate Curriculum again."
        ),
    ),
    "ingestion_error": FindingGuidance(
        issue="Curriculum ingestion reported a blocking problem.",
        why_it_matters=(
            "Parsing or structural failures mean the extracted curriculum "
            "is unsafe to preview or publish."
        ),
        recovery_action=(
            "Check CMP and syllabus references, re-upload corrected "
            "sources, then run Validate Curriculum again."
        ),
    ),
    "ingestion_warning": FindingGuidance(
        issue="Curriculum ingestion reported a warning.",
        why_it_matters=(
            "Warnings do not always block publication, but they can hide "
            "gaps students will feel later."
        ),
        recovery_action=(
            "Review the warning detail, correct sources if needed, then "
            "re-validate before preview."
        ),
    ),
}

_DEFAULT_WHY = (
    "Unresolved validation findings can block a safe publication "
    "or leave students with an incomplete curriculum."
)
_DEFAULT_RECOVERY = (
    "Review the finding detail, correct CMP/syllabus sources or "
    "structure, then run Validate Curriculum again."
)


def enrich_finding(finding: ValidationFinding) -> ValidationFinding:
    """Fill why/recovery from the catalog when the finding omits them."""
    guide = VALIDATION_FINDING_GUIDANCE.get(finding.code)
    if guide is None:
        if finding.why_it_matters and finding.recovery_action:
            return finding
        return ValidationFinding.create(
            finding.code,
            finding.message,
            severity=finding.severity,
            section_id=finding.section_id,
            topic_id=finding.topic_id,
            why_it_matters=finding.why_it_matters or _DEFAULT_WHY,
            recovery_action=finding.recovery_action or _DEFAULT_RECOVERY,
        )
    return ValidationFinding.create(
        finding.code,
        finding.message if finding.message else guide.issue,
        severity=finding.severity,
        section_id=finding.section_id,
        topic_id=finding.topic_id,
        why_it_matters=finding.why_it_matters or guide.why_it_matters,
        recovery_action=finding.recovery_action or guide.recovery_action,
    )


def guided_finding(
    code: str,
    *,
    severity: str = "blocking",
    message: str | None = None,
) -> ValidationFinding:
    """Build a ValidationFinding with catalog guidance applied."""
    guide = VALIDATION_FINDING_GUIDANCE.get(code)
    issue = (message or (guide.issue if guide else code)).strip()
    finding = ValidationFinding.create(
        code,
        issue,
        severity=severity,
        why_it_matters=guide.why_it_matters if guide else "",
        recovery_action=guide.recovery_action if guide else "",
    )
    return enrich_finding(finding)

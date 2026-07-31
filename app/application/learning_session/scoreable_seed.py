"""CS1 commercial seed corpus of scoreable practice items (KWP-004).

Syllabus-faithful assessable items for high-traffic commercial topics.
Used by EducationalSubstancePlanner when matching topic / LO context.
"""

from __future__ import annotations

from app.application.learning_session.scoreable_practice import (
    AnswerKey,
    MarkScheme,
    PracticeResponseType,
    ScoreablePracticeItem,
)

# Seed items for commercial CS1-style topics. Matched by topic keywords /
# title fragments — never invents mastery or Twin grades.
CS1_SCOREABLE_SEED: tuple[ScoreablePracticeItem, ...] = (
    ScoreablePracticeItem(
        item_id="cs1-cash-mcq-1",
        prompt=(
            "Which cash-flow classification typically includes interest paid "
            "under IFRS when presented as an operating item?"
        ),
        response_type=PracticeResponseType.MCQ,
        answer_key=AnswerKey(
            accepted=("operating", "operating activities", "a"),
            correct_choice_id="a",
        ),
        mark_scheme=MarkScheme(
            points=("Identify the IFRS classification choice for interest paid.",),
            max_marks=1,
        ),
        explanation=(
            "Under IFRS, interest paid may be classified as operating or financing. "
            "When presented as an operating item, it belongs with operating activities."
        ),
        model_answer="Operating activities (choice A).",
        common_mistake=(
            "Assuming interest paid is always financing — IFRS allows operating "
            "presentation when that policy is chosen."
        ),
        next_action="Continue to the next cash-flow practice item.",
        topic_keywords=("cash flow", "cash flows", "cashflow"),
        choices=(
            ("a", "Operating activities"),
            ("b", "Investing activities only"),
            ("c", "Equity activities"),
            ("d", "Never disclosed"),
        ),
        emit_structured=True,
        body="Choose the best classification.",
        hints=("Recall IFRS vs US GAAP presentation choices for interest.",),
        supporting_material="IAS 7 permits operating or financing classification.",
    ),
    ScoreablePracticeItem(
        item_id="cs1-cash-short-1",
        prompt=(
            "In one sentence, define operating cash flow for a non-financial "
            "company."
        ),
        response_type=PracticeResponseType.SHORT_STRUCTURED,
        answer_key=AnswerKey(
            accepted=(
                "cash generated from core trading operations",
                "cash from operating activities",
                "cash from day to day operations",
                "cash from principal revenue-producing activities",
            )
        ),
        mark_scheme=MarkScheme(
            points=(
                "Link cash flow to principal revenue-producing / core operations.",
            ),
            max_marks=1,
        ),
        explanation=(
            "Operating cash flow is cash generated or used by the entity's "
            "principal revenue-producing activities — not investing or financing."
        ),
        model_answer=(
            "Cash generated from the company's principal revenue-producing "
            "(day-to-day trading) activities."
        ),
        common_mistake=(
            "Confusing operating cash flow with profit, or including investing "
            "cash such as asset purchases."
        ),
        next_action="Compare your wording with the model answer, then continue.",
        topic_keywords=("cash flow", "cash flows", "cashflow", "operating cash"),
        body="Use precise study language — one clear sentence is enough.",
        hints=("Start from 'principal revenue-producing activities'.",),
    ),
    ScoreablePracticeItem(
        item_id="cs1-discount-numeric-1",
        prompt=(
            "A payment of 100 is due in exactly one year. At an effective annual "
            "rate of 5%, what is the present value to the nearest whole number?"
        ),
        response_type=PracticeResponseType.NUMERIC,
        answer_key=AnswerKey(accepted=("95", "95.24"), numeric_tolerance=0.6),
        mark_scheme=MarkScheme(
            points=("Apply PV = 100 / 1.05 and round sensibly.",),
            max_marks=1,
        ),
        explanation=(
            "Present value = 100 / 1.05 ≈ 95.24, which rounds to 95 to the "
            "nearest whole number."
        ),
        model_answer="95 (from 100 / 1.05 ≈ 95.24).",
        common_mistake=(
            "Multiplying by 1.05 instead of dividing, or using a continuous "
            "force of interest when the question specifies an effective rate."
        ),
        next_action="Review the discounting step, then continue practice.",
        topic_keywords=(
            "discount",
            "discounting",
            "present value",
            "time value",
            "interest",
        ),
        emit_structured=True,
        body="Enter a numeric answer (nearest whole number).",
        hints=("PV = future payment ÷ (1 + i).",),
    ),
    ScoreablePracticeItem(
        item_id="cs1-discount-short-1",
        prompt=(
            "State the relationship between an effective annual rate i and the "
            "one-year discount factor v."
        ),
        response_type=PracticeResponseType.SHORT_STRUCTURED,
        answer_key=AnswerKey(
            accepted=(
                "v = 1/(1+i)",
                "v=1/(1+i)",
                "v equals 1 over 1 plus i",
                "discount factor is 1/(1+i)",
            )
        ),
        mark_scheme=MarkScheme(
            points=("State v = 1 / (1 + i).",),
            max_marks=1,
        ),
        explanation=(
            "The one-year discount factor is the present value of 1 due in one "
            "year: v = 1 / (1 + i)."
        ),
        model_answer="v = 1 / (1 + i).",
        common_mistake="Writing v = 1 + i or confusing v with the force of interest.",
        next_action="Keep the identity v = 1/(1+i) ready for the next item.",
        topic_keywords=(
            "discount",
            "discounting",
            "present value",
            "time value",
            "interest",
        ),
        body="Give the standard actuarial identity.",
        hints=("Discount factor converts a payment due in one year to today.",),
    ),
    ScoreablePracticeItem(
        item_id="cs1-equity-mcq-1",
        prompt=(
            "Under the equity method, an investor typically recognises its share "
            "of an associate's profit by:"
        ),
        response_type=PracticeResponseType.MCQ,
        answer_key=AnswerKey(
            accepted=("increasing the investment carrying amount", "a"),
            correct_choice_id="a",
        ),
        mark_scheme=MarkScheme(
            points=("Identify the equity-method carrying-amount update.",),
            max_marks=1,
        ),
        explanation=(
            "The equity method increases the investment's carrying amount for "
            "the investor's share of profit (and reduces it for dividends)."
        ),
        model_answer=(
            "Increasing the investment carrying amount by the investor's share "
            "of profit (choice A)."
        ),
        common_mistake=(
            "Treating the associate like a subsidiary consolidation, or booking "
            "only dividend income."
        ),
        next_action="Continue with the next equity-method check.",
        topic_keywords=("equity method", "associate", "associates", "influence"),
        choices=(
            ("a", "Increasing the investment carrying amount"),
            ("b", "Recognising the full associate revenue line-by-line"),
            ("c", "Ignoring profit until dividends are paid"),
            ("d", "Fair-valuing only through OCI each period"),
        ),
        emit_structured=True,
        body="Select the equity-method treatment.",
        hints=("Think about carrying amount vs dividend cash.",),
    ),
    ScoreablePracticeItem(
        item_id="cs1-general-short-1",
        prompt=(
            "In your own words, state one syllabus idea from today's topic and "
            "how you would check it against a worked example."
        ),
        response_type=PracticeResponseType.SHORT_STRUCTURED,
        answer_key=AnswerKey(
            accepted=(
                "worked example",
                "compare",
                "check",
                "definition",
                "method",
                "objective",
            )
        ),
        mark_scheme=MarkScheme(
            points=("Name a syllabus idea and a concrete check against the example.",),
            max_marks=1,
        ),
        explanation=(
            "Strong practice names a concrete syllabus idea and describes how "
            "the worked example would confirm or correct it."
        ),
        model_answer=(
            "Name the idea (for example a definition or method step), then say "
            "you would compare your reasoning with the corresponding step in "
            "the worked example."
        ),
        common_mistake=(
            "Restating the topic title without saying how you would verify it."
        ),
        next_action="Continue to reflection when practice feels complete.",
        topic_keywords=(),  # fallback catch-all when no topic-specific items match
        body="Be specific — one idea and one check.",
        hints=("Reuse a method step from the worked example.",),
    ),
)


def items_for_topic(
    *,
    topic_title: str = "",
    topic_id: str = "",
    limit: int = 3,
) -> tuple[ScoreablePracticeItem, ...]:
    """Return seed items matching the topic, capped for one sitting."""
    haystack = f"{topic_title} {topic_id}".strip().lower()
    matched: list[ScoreablePracticeItem] = []
    for item in CS1_SCOREABLE_SEED:
        if item.item_id == "cs1-general-short-1":
            continue
        if item.topic_id and topic_id and item.topic_id == topic_id:
            matched.append(item)
            continue
        if any(keyword in haystack for keyword in item.topic_keywords):
            matched.append(item)
    if not matched:
        general = next(
            (i for i in CS1_SCOREABLE_SEED if i.item_id == "cs1-general-short-1"),
            None,
        )
        if general is not None:
            matched.append(general)
    return tuple(matched[: max(1, limit)])

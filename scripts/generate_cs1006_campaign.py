#!/usr/bin/env python3
"""Generate CS1-006 / Campaign Zeta educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-zeta-cs1006"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1006-campaign-zeta-1.0.0",
    "publication_version": "cs1006-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-ZETA",
    "volume_id": "CS1-006",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1006_EDUCATIONAL_VOLUME.md",
        "CS1006_CERTIFICATION_REPORT.md",
        "EP004_WAVE4_PLAN.md",
    ],
    "author_id": "cs1006-educational-author",
    "authored_at": "2026-08-01",
}

TOPIC = {
    "topic_code": "2.3",
    "topic_title": "Evaluate expectations and conditional expectations",
    "topic_id": "CS1-B-T03",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "2.3", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1006-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1006-cs1-{d['slug']}",
            "display_title": d["title"],
            "mission_purpose": d["purpose"],
            "tutor_intent": d["tutor"],
            "educational_intent": d["edu"],
            "learning_objective": d["lo_text"],
            "concept_focus": d["focus"],
            "prior_bridge": d["prior"],
            "why_now": d["why"],
            "expected_benefit": d["benefit"],
            "explainability": d["explain"],
            "success_criteria": d["criteria"],
            "task_descriptions": d["tasks"],
            "estimated_study_time_minutes": {"min": 55, "max": 75},
        },
        "session": {
            "session_id": f"ssn-cs1006-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Mission for Syllabus {lo} — not the next LO as primary."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo}, exit to CMP, retrieve today's hinge, refuse swallowed next LO."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo}. This is Study Progress for today's block — not Topic Complete "
                f"for later 2.3 LOs, Chapter 2, or generating functions."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} hinge closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to extract Syllabus {lo} — "
                f"{d['title'].lower()}. Stop before out-of-scope later LOs."
            ),
            "focus_questions": [
                f"What is the core move of Syllabus {lo}?",
                "What warrant separates today's skill from yesterday's?",
                "What claim must you refuse today?",
                "What will you practise in Knowledge Checks after the CMP?",
            ],
            "misconception_watch": d["misconceptions"],
            "open_point": d["open"],
            "stop_condition": d["stop"],
            "out_of_scope_today": d["oos"],
            "annotation_task": "Before deep reading: sketch today's concept chain in notes",
            "attempt_before_reveal": (
                "At the first worked example, cover the answer and attempt the middle step"
            ),
            "exit_line": (
                f"Open your CMP (IFoA CS1 Core Reading / CMP · 2026 syllabus alignment) at "
                f"{d['open']}. Kwalitec is the guide; the CMP is the authoritative material — "
                "do not treat this activity body as a substitute textbook. Hunt with the focus "
                "questions; watch the misconception list. Ignore items in out_of_scope_today. "
                f"Stop when: {d['stop']}. Then close the CMP and return here — next in-app "
                "activity: Worked-example re-entry (CMP closed), then Knowledge Checks."
            ),
            "return_cue": (
                f"You are finished with Guided Reading when the CMP {lo} block meets the stop "
                "condition and you can answer today's focus questions from your notes. Close the "
                "CMP and return to Kwalitec. Immediate next activity: Worked-example re-entry, "
                "then Knowledge Checks (Active Recall → Checkpoint)."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause — write today's core move in one sentence.",
                    "student_action": "Annotate",
                },
                {
                    "id": "PP2",
                    "cue": "Attempt the next worked step before uncovering the solution.",
                    "student_action": "Attempt",
                },
            ],
            "reentry_line": (
                "Welcome back. Keep your CMP closed. Immediate next activity: "
                "Worked-example re-entry, then Knowledge Checks."
            ),
        },
        "knowledge_checks": [
            {
                "episode_id": f"lep-cs1006-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1006-{lo}-ar-01",
                "title": f"Active Recall: {lo}",
                "prompt": d["ar_prompt"],
                "response_type": "short_structured",
                "body": f"Retrieve {lo} closed-book.",
                "hints": ["Use CMP language from today's notes.", "Stay inside today's LO."],
                "accepted_keywords": d["ar_kw"],
                "explanation": f"Active recall for {lo}.",
                "model_answer": d["ar_model"],
                "common_mistake": "Skipping the LO hinge or swallowing the next LO.",
                "success_criteria": ["Addresses the prompt structure.", "Stays inside today's LO."],
            },
            {
                "episode_id": f"lep-cs1006-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1006-{lo}-cp-01",
                "title": f"Checkpoint: {lo}",
                "prompt": d["cp_prompt"],
                "response_type": "short_structured",
                "body": f"Checkpoint refuse/warrant for {lo}.",
                "hints": ["Name the refusal clearly.", "Give a positive warrant."],
                "accepted_keywords": d["cp_kw"],
                "explanation": f"Checkpoint for {lo}.",
                "model_answer": d["cp_model"],
                "common_mistake": "Accepting the forbidden claim.",
                "success_criteria": ["Refusal present.", "Positive warrant present."],
            },
        ],
        "reflection": {
            "framing": d["reflect"],
            "prompt": (
                f"Which part of today's {lo} move is stickiest and why? Quote or paraphrase "
                "the single CMP cue still unclear. If you had five minutes tomorrow, what one "
                "move would you rework?"
            ),
            "prompts": [
                f"Which part of {lo} is stickiest and why?",
                "Quote or paraphrase the single CMP cue still unclear.",
                "If you had five minutes tomorrow, what one move would you rework?",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": d["next_code"],
            "next_topic_title": d["next_title"],
            "continuity_line": d["cont"],
            "light_prep_cue": d["prep"],
            "student_facing": d["student"],
        },
    }


def revision_pkg() -> dict:
    day = "CZ-R1"
    pid = "CS1-EP001-PKG-REV-CONDITIONAL-EXPECTATIONS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Zeta revision — expectations and conditional expectations",
        "return_targets": ["2.3.1", "2.3.2"],
        "topic_aliases": [day, "campaign-zeta-revision"],
        "topic_title_keywords": [
            "revision",
            "conditional",
            "expectation",
            "tower",
            "variance",
            "conditioning",
        ],
        "golden_id": "GOLDEN-CS1006-CS1-CZ-R1-CONDITIONAL-EXPECTATIONS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1006-cs1-cz-r1-conditional-expectations",
            "display_title": "Retrieve conditional-expectation hinges (2.3)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Zeta — retrieving "
                "conditional expectation of one RV given another, and mean/variance via "
                "conditioning — so 2.3 does not evaporate before generating functions (2.4)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Zeta's Learning hinges — "
                "not a passive CMP re-read and not a first-pass 2.4 lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: "
                "conditional expectation → mean/variance as expectations of conditional values."
            ),
            "learning_objective": (
                "Retrieve and connect (1) conditional expectation E[Y|X=x] (or equivalent), "
                "and (2) mean and variance obtained via conditioning (tower / law of total "
                "expectation and related variance decomposition)."
            ),
            "concept_focus": (
                "Campaign chain retrieval: E[Y|X] → E[E[Y|X]] / Var via conditioning."
            ),
            "prior_bridge": (
                "Yesterday you finished mean and variance via conditioning (2.3.2). "
                "Today is Revision mode: return to 2.3.1–2.3.2 under closed-book retrieval — "
                "no new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 2.4 work."
            ),
            "expected_benefit": (
                "Evidence that the 2.3 chain retrieves — revision Study Progress, not a claim "
                "that Chapter 2 or the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, outline conditional expectation of one RV given another.",
                "State how mean (and variance) arise as expectations of conditional values.",
                "Refuse Chapter 2 complete / spine / until-exam / MGF-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Zeta's chain: E[Y|X] → mean/variance via "
                "conditioning.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 40, "max": 55},
        },
        "session": {
            "session_id": "ssn-cs1006-cs1-cz-r1-conditional-expectations",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Zeta skills — not to teach 2.4."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link — Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 40, "max": 55},
            "wrap_up": (
                "Revision Session complete. You stress-tested 2.3.1–2.3.2 return targets. "
                "This is revision Study Progress — not Topic Complete for 2.4, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that conditional expectation → mean/variance via "
                "conditioning will still retrieve in three days? Rate 1–5 and name the "
                "weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Zeta "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you form or interpret E[Y|X=x] (or equivalent)?",
                "Can you obtain mean (and variance) via conditioning?",
                "What claim must you refuse (Chapter 2 complete / spine / until-exam / 2.4 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 2 / 2.4 complete.",
                "Watch for dropping Epsilon joint-distribution memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection — do not begin Syllabus 2.4 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass generating functions (2.4)",
                "CLT / sampling (2.5–2.6)",
                "Inference Chapter 3",
                "First-pass spine PASS",
                "Until-exam educational trust",
            ],
            "annotation_task": "Before checks: sketch return-target chain from memory",
            "attempt_before_reveal": "Attempt each check before any targeted CMP reopen",
            "exit_line": (
                "Begin closed-book retrieval. Reopen CMP only at a failed locus. After checks, "
                "complete Reflection."
            ),
            "return_cue": (
                "Revision reading stage is complete when checks are attempted and any failed "
                "locus has a targeted reopen plan."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause — mark the weakest link before checks.",
                    "student_action": "Annotate",
                }
            ],
            "reentry_line": "Stay closed-book unless a check failed. Continue retrieval.",
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1006-cz-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1006-cz-r1-ar-01",
                "title": "Active Recall: CZ-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) conditional "
                    "expectation of one RV given another; (2) mean and/or variance obtained as "
                    "an expectation of conditional expected values."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 2.3.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "conditional",
                    "expectation",
                    "given",
                    "tower",
                    "total",
                    "mean",
                    "variance",
                    "conditioning",
                    "E[Y|X]",
                ],
                "explanation": "Revision retrieves the 2.3 arc.",
                "model_answer": (
                    "Example: (1) E[Y|X=x] is the expected value of Y given X=x (function of x). "
                    "(2) E[Y]=E[E[Y|X]]; variance can use conditioning / law of total variance "
                    "as in the CMP."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Two hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1006-cz-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1006-cz-r1-cp-01",
                "title": "Checkpoint: CZ-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest conditioning link and one concrete "
                    "rework. (2) Refuse: 'E[Y|X] is just ordinary expectation, so Chapter 2 is "
                    "done.' (3) Name the honest next topic (generating functions, 2.4) or "
                    "confirm you are stopping here."
                ),
                "response_type": "short_structured",
                "body": "Weakest link + honest next.",
                "hints": ["Name a concrete rework.", "Refuse forbidden claims."],
                "accepted_keywords": [
                    "weak",
                    "rework",
                    "refuse",
                    "spine",
                    "chapter",
                    "2.4",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. Var via conditioning — five-minute rework. (2) Refuse Chapter 2 "
                    "complete / spine / until-exam. (3) Honest next is 2.4 (successor Volume) "
                    "or declared stop — not claimed finished here."
                ),
                "common_mistake": "Spine / Chapter 2 / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which link retrieved least cleanly today and what one concrete rework will "
                "you schedule? Do not claim the rest of Chapter 2 is finished from one retrieval sitting."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Do not claim the rest of Chapter 2 is finished from one retrieval sitting.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "2.4",
            "next_topic_title": (
                "Honest next — generating functions (2.4) under a successor Volume "
                "(or declared stop)"
            ),
            "continuity_line": (
                "Campaign Zeta / Volume CS1-006 completes after this Revision. Honest stop: "
                "2.3 Pilot Arc closed — not Chapter 2 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 2.4 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight — rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Zeta / CS1-006 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 2.4 successor Volume. Optional: schedule your "
                "weakest 2.3 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CZ-D1",
        stem="2.3.1-conditional-expectation-cs1006",
        pid="CS1-EP001-PKG-2.3-CONDITIONAL-EXPECTATION",
        lo="2.3.1",
        slug="2.3-conditional-expectation",
        keywords=["conditional", "expectation", "given", "random", "variable"],
        title="Form the conditional expectation of one RV given another",
        purpose=(
            "Today's Mission exists to obtain the conditional expectation of one random "
            "variable given the value of another — so E[Y|X=x] (or equivalent) is a usable "
            "object — without pretending the tower / total-expectation mean-variance LO is finished."
        ),
        tutor=(
            "Today I will force the candidate to form or interpret E[Y|X=x] from a joint or "
            "conditional setup — and refuse treating 'I can compute an ordinary expectation' "
            "as having conditional expectation."
        ),
        edu=(
            "Produce a cognitive move from joint/conditional structure to lawful conditional "
            "expectation of one RV given another."
        ),
        lo_text=(
            "Obtain and interpret the conditional expectation of one random variable given "
            "the value of another random variable."
        ),
        focus=(
            "Joint/conditional → E[Y|X=x] as a function of x → refuse ordinary-E-as-conditional."
        ),
        prior=(
            "Campaign Epsilon closed joint distributions through linear combinations (2.2) "
            "with Revision. Today opens topic 2.3 at LO 2.3.1 — the named Continuity Front "
            "after CS1-005."
        ),
        why=(
            "2.3.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at conditional expectation, keeping mean/variance-via-conditioning for the following session."
        ),
        benefit="Study Progress for conditional expectation — not Topic Complete for 2.3.2.",
        explain=(
            "Day 1 opens 2.3 at the named learning objective — "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, outline what E[Y|X=x] means (or equivalent CMP form).",
            "Sketch how to obtain it from a joint or conditional distribution.",
            "Refuse one 'ordinary expectation finished conditional expectation' claim.",
        ],
        tasks=[
            "Sketch conditional expectation as a function of the conditioning value before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.3.1.",
            "Closed-book Knowledge Checks: E[Y|X] + refuse ordinary-E collapse.",
        ],
        next_code="2.3",
        next_title="Mean and variance via conditioning (2.3.2)",
        cont=(
            "Today you formed conditional expectation of one RV given another; tomorrow "
            "continues 2.3 at mean and variance as expectations of conditional expected values."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.3.2 — titles only tonight",
        student=(
            "Tomorrow: mean and variance via conditioning (2.3.2). Optional light prep: "
            "skim 2.3.2 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.3.1 conditional expectation",
        stop=(
            "Through the CMP treatment of Syllabus 2.3.1 "
            "(stop before mean/variance via conditioning 2.3.2)"
        ),
        oos=[
            "Mean and variance via conditioning as primary (2.3.2)",
            "Generating functions (2.4)",
            "CLT / sampling (2.5–2.6)",
            "Inference Chapter 3",
            "CS1B coding marathon",
        ],
        misconceptions=[
            "Watch for equating E[Y] with E[Y|X=x].",
            "Watch for starting tower/total-expectation drills (2.3.2) inside this sitting.",
            "Watch for MGF work (2.4) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) In words, what is E[Y|X=x]? (2) How does it differ from E[Y]? "
            "(3) Name one operation or setup that produces it from a joint/conditional."
        ),
        ar_kw=[
            "conditional",
            "expectation",
            "given",
            "E[Y|X]",
            "function",
            "x",
            "joint",
            "average",
        ],
        ar_model=(
            "E[Y|X=x] is the expected value of Y when X is fixed at x — a function of x. "
            "It is not the same as the unconditional E[Y]. Obtain it from the conditional "
            "distribution of Y|X=x (or equivalent joint setup in the CMP)."
        ),
        cp_prompt=(
            "Closed-book. A colleague says 'we already know how to take expectations, so "
            "conditional expectation is just the same skill.' Refuse in one sentence and "
            "restate what today's LO adds."
        ),
        cp_kw=["refuse", "conditional", "expectation", "given", "not same", "function"],
        cp_model=(
            "Refuse: ordinary expectation is not conditional expectation. Today's skill is "
            "E[Y|X=x] (or equivalent) — expectation under the conditioned world, as a "
            "function of the conditioning value."
        ),
        reflect=(
            "Harvest wobble on E[Y|X=x] vs E[Y] — mean/variance via conditioning comes tomorrow."
        ),
    ),
    dict(
        day="CZ-D2",
        stem="2.3.2-mean-variance-conditioning-cs1006",
        pid="CS1-EP001-PKG-2.3-MEAN-VARIANCE-CONDITIONING",
        lo="2.3.2",
        slug="2.3-mean-variance-conditioning",
        keywords=["mean", "variance", "conditional", "expectation", "tower", "total"],
        title="Obtain mean and variance via conditioning",
        purpose=(
            "Today's Mission exists to obtain the mean and variance of a random variable as "
            "expectations of conditional expected values — so the tower / law of total "
            "expectation (and related variance decomposition) is usable — without claiming "
            "Chapter 2 or generating functions complete."
        ),
        tutor=(
            "Today I will force the candidate through mean (and variance) via conditioning — "
            "refuse treating yesterday's E[Y|X] as having finished the tower, and refuse "
            "Chapter-2-complete claims."
        ),
        edu=(
            "Produce executable warrants for mean and variance obtained via conditioning."
        ),
        lo_text=(
            "Obtain the mean and variance of a random variable as an expectation of "
            "conditional expected values."
        ),
        focus=(
            "E[Y]=E[E[Y|X]] → variance via conditioning → refuse E[Y|X]-as-done / Ch2-done."
        ),
        prior=(
            "Yesterday you formed conditional expectation of one RV given another (2.3.1). "
            "Today uses that object to recover mean and variance."
        ),
        why=(
            "2.3.2 completes topic 2.3 Learning; Revision follows before any 2.4 commission."
        ),
        benefit=(
            "Study Progress for mean/variance via conditioning — not 2.4; not Chapter 2 trophy."
        ),
        explain="Campaign Zeta Day 2 focuses LO 2.3.2 — terminal Learning day of CS1-006.",
        criteria=[
            "Closed-book, state how E[Y] arises from E[E[Y|X]] (or equivalent).",
            "Outline how variance uses conditioning (CMP form).",
            "Refuse Chapter 2 complete / treating 2.3.1 as having finished 2.3.2.",
        ],
        tasks=[
            "Sketch tower / total-expectation and variance-via-conditioning before CMP.",
            "Guided Reading through CMP 2.3.2.",
            "Knowledge Checks: mean/variance via conditioning + refuse Ch2-complete.",
        ],
        next_code="CZ-R1",
        next_title="Campaign Zeta Revision — retrieve 2.3.1–2.3.2",
        cont=(
            "Today you finished mean and variance via conditioning; tomorrow is Revision "
            "mode — retrieve the 2.3 chain closed-book before any 2.4 first-pass work."
        ),
        prep="Optional: list the two 2.3 LO hinges from memory — titles only tonight",
        student=(
            "Tomorrow: Campaign Zeta Revision (retrieve 2.3.1–2.3.2). Optional light prep: "
            "list the two hinges from memory — titles only tonight."
        ),
        open="CMP · Syllabus 2.3.2 mean and variance via conditioning",
        stop="Through CMP 2.3.2 (stop before generating functions 2.4)",
        oos=[
            "Generating functions / MGF / CGF (2.4)",
            "CLT / sampling (2.5–2.6)",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "First-pass spine PASS",
        ],
        misconceptions=[
            "Watch for stopping at E[Y|X] without the tower / total step.",
            "Watch for claiming Chapter 2 / 2.4 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. (1) Write or state E[Y] in terms of conditional expectation. "
            "(2) In one sentence, how can variance use conditioning (CMP idea)?"
        ),
        ar_kw=[
            "expectation",
            "conditional",
            "tower",
            "total",
            "variance",
            "E[E[Y|X]]",
            "conditioning",
            "mean",
        ],
        ar_model=(
            "E[Y] = E[E[Y|X]] (law of total / tower expectation). Variance can be recovered "
            "via conditioning (e.g. law of total variance / related CMP decomposition)."
        ),
        cp_prompt=(
            "Closed-book. (1) Refuse 'Yesterday's E[Y|X] already finished mean/variance via "
            "conditioning.' (2) Refuse 'Finishing 2.3.2 means all of Chapter 2 is done.' Name "
            "what still sits ahead before generating functions."
        ),
        cp_kw=["refuse", "tower", "variance", "chapter", "complete", "2.4", "revision", "stop"],
        cp_model=(
            "(1) Refuse: forming E[Y|X] is not the same as recovering mean/variance via "
            "conditioning. (2) Refuse: 2.3.2 closes topic 2.3 Learning, not Chapter 2; next "
            "is Revision then honest 2.4 successor — not spine/until-exam claims."
        ),
        reflect="Harvest conditioning-mean/variance wobble — Revision protects the 2.3 chain tomorrow.",
    ),
]


def main() -> None:
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    inventory: list[str] = []
    span: list[str] = []

    for d in LEARNING:
        pkg = learning_pkg(d)
        path = PKG_DIR / f"{d['stem']}.json"
        path.write_text(json.dumps(pkg, indent=2) + "\n")
        inventory.append(d["pid"])
        span.append(d["lo"])

    rev = revision_pkg()
    (PKG_DIR / "revision-conditional-expectations-cs1006.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-ZETA",
        "campaign_version": "cs1006-1.0.0",
        "display_title": "Campaign Zeta — Expectations and conditional expectations (2.3)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-006",
        "prior_volume_id": "CS1-005",
        "day_count": {"learning": 2, "revision": 1, "total": 3},
        "syllabus_span": span,
        "out_of_scope": [
            "2.4+",
            "Chapter 2 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 5 / Chapter 3 inference authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

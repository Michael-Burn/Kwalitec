#!/usr/bin/env python3
"""Generate CS1-011 / Campaign Lambda educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

from _mcq_batch1_section3_payload import apply_mcq_overlay
from _mcq_batch6b_revision_payload import apply_mcq_overlay as apply_batch6b_mcq_overlay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-lambda-cs1011"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1011-campaign-lambda-1.0.0",
    "publication_version": "cs1011-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-LAMBDA",
    "volume_id": "CS1-011",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1011_EDUCATIONAL_VOLUME.md",
        "CS1011_CERTIFICATION_REPORT.md",
        "EP009_WAVE9_PLAN.md",
    ],
    "author_id": "cs1011-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "3.2",
    "topic_title": "Calculate confidence intervals and prediction intervals",
    "topic_id": "CS1-C-T02",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "3.2", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1011-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1011-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1011-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Mission for Syllabus {lo}. Not the next LO as primary."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo}, exit to CMP, retrieve today's hinge, refuse swallowed next LO."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo}. This is Study Progress for today's block. Not Topic Complete "
                f"for later 3.2 LOs, Chapter 3 trophy, hypothesis testing (3.3), or until-exam "
                "trust."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} hinge closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to extract Syllabus {lo}–"
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
                f"{d['open']}. Kwalitec is the guide; the CMP is the authoritative material. "
                "do not treat this activity body as a substitute textbook. Hunt with the focus "
                "questions; watch the misconception list. Ignore items in out_of_scope_today. "
                f"Stop when: {d['stop']}. Then close the CMP and return here. Next in-app "
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
                    "cue": "Pause. Write today's core move in one sentence.",
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
                "episode_id": f"lep-cs1011-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1011-{lo}-ar-01",
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
                "episode_id": f"lep-cs1011-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1011-{lo}-cp-01",
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
    day = "CL-R1"
    pid = "CS1-EP001-PKG-REV-CONFIDENCE-INTERVALS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Lambda revision: confidence and prediction intervals",
        "return_targets": [
            "3.2.1",
            "3.2.2",
            "3.2.3",
            "3.2.4",
            "3.2.5",
            "3.2.6",
            "3.2.7",
            "3.2.8",
        ],
        "topic_aliases": [day, "campaign-lambda-revision"],
        "topic_title_keywords": [
            "revision",
            "confidence",
            "prediction",
            "interval",
            "normal",
            "binomial",
            "Poisson",
            "paired",
            "bootstrap",
            "two-sample",
        ],
        "golden_id": "GOLDEN-CS1011-CS1-CL-R1-INTERVALS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1011-cs1-cl-r1-intervals",
            "display_title": "Retrieve interval hinges (3.2)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Lambda. Retrieving "
                "parameter CI, prediction interval, given-sampling-distribution CI, Normal "
                "mean/variance CIs, binomial/Poisson CIs, two-sample CIs, paired-mean CI, and "
                "bootstrap CIs. So 3.2 does not evaporate before hypothesis testing (3.3)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Lambda's Learning hinges. "
                "not a passive CMP re-read and not a first-pass 3.3 hypothesis-testing lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: parameter CI "
                "→ prediction → given sampling distribution → Normal mean/var → binomial/"
                "Poisson → two-sample → paired → bootstrap CI."
            ),
            "learning_objective": (
                "Retrieve and connect (1) parameter CI from a random sample, (2) prediction "
                "interval, (3) CI given a sampling distribution, (4) Normal mean and variance "
                "CIs, (5) binomial/Poisson CIs with Normal approximation, (6) two-sample CIs, "
                "(7) paired mean-difference CI, and (8) bootstrap confidence intervals."
            ),
            "concept_focus": (
                "Campaign chain retrieval: parameter CI → prediction → given distribution → "
                "Normal → binomial/Poisson → two-sample → paired → bootstrap CI."
            ),
            "prior_bridge": (
                "Yesterday you finished bootstrap confidence intervals (3.2.8). Today is "
                "Revision mode: return to 3.2.1–3.2.8 under closed-book retrieval. No new "
                "first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 3.3 work."
            ),
            "expected_benefit": (
                "Evidence that the 3.2 chain retrieves. Revision Study Progress, not a claim "
                "that Chapter 3 / the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the eight 3.2 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse Chapter 3 complete / spine / until-exam / 3.3-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Lambda's chain: parameter CI → prediction → "
                "given sampling distribution → Normal mean/var → binomial/Poisson → two-sample "
                "→ paired → bootstrap CI.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 45, "max": 65},
        },
        "session": {
            "session_id": "ssn-cs1011-cs1-cl-r1-intervals",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Lambda skills. Not to teach 3.3."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 45, "max": 65},
            "wrap_up": (
                "Revision Session complete. You stress-tested 3.2.1–3.2.8 return targets. "
                "This is revision Study Progress. Not Topic Complete for 3.3, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that interval hinges will still retrieve in three "
                "days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Lambda "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the eight 3.2 Learning hinges in order?",
                "Can you state CI vs prediction interval and when bootstrap CI enters?",
                "What claim must you refuse (Chapter 3 complete / spine / until-exam / 3.3 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 3 / spine / until-exam complete.",
                "Watch for dropping Kappa estimator memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not begin Syllabus 3.3 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass hypothesis testing / goodness of fit (3.3)",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Chapter 3 complete trophy claim",
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
                    "cue": "Pause. Mark the weakest link before checks.",
                    "student_action": "Annotate",
                }
            ],
            "reentry_line": "Stay closed-book unless a check failed. Continue retrieval.",
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1011-cl-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1011-cl-r1-ar-01",
                "title": "Active Recall: CL-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) parameter CI "
                    "from a random sample; (2) prediction interval; (3) CI given a sampling "
                    "distribution; (4) Normal mean and variance CIs; (5) binomial/Poisson CIs "
                    "(Normal approx); (6) two-sample CIs; (7) paired mean-difference CI; "
                    "(8) bootstrap confidence intervals."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 3.2.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "confidence",
                    "prediction",
                    "sampling",
                    "normal",
                    "binomial",
                    "Poisson",
                    "two-sample",
                    "paired",
                    "bootstrap",
                    "interval",
                ],
                "explanation": "Revision retrieves the 3.2 arc.",
                "model_answer": (
                    "Example: (1) CI for a parameter from a random sample; (2) prediction "
                    "interval for a future observation; (3) CI using a given sampling "
                    "distribution; (4) Normal mean and variance intervals; (5) binomial/"
                    "Poisson intervals with Normal approximation; (6) two-sample intervals; "
                    "(7) paired mean-difference interval; (8) bootstrap CIs."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Eight hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1011-cl-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1011-cl-r1-cp-01",
                "title": "Checkpoint: CL-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest interval-estimation link and one "
                    "concrete rework. (2) Refuse: 'A confidence interval is the same as a "
                    "prediction interval, so Chapter 3 is done.' (3) Name the honest next "
                    "topic (hypothesis testing, 3.3) or confirm you are stopping here."
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
                    "3.3",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. two-sample Normal-approx CI. Five-minute rework. (2) Refuse "
                    "Chapter 3 complete / spine / until-exam. (3) Honest next is 3.3 "
                    "(successor Volume) or declared stop. Not claimed finished here."
                ),
                "common_mistake": "Spine / Chapter 3 / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which link retrieved least cleanly today and what one concrete rework will "
                "you schedule? Do not claim the rest of Chapter 3 is finished from one retrieval sitting."
            ),
            "prompts": [
                "Which link retrieved least cleanly today?",
                "What one concrete rework will you schedule?",
                "Do not claim the rest of Chapter 3 is finished from one retrieval sitting.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "3.3",
            "next_topic_title": (
                "Honest next: hypothesis testing and goodness of fit (3.3) under a successor "
                "Volume (or declared stop)"
            ),
            "continuity_line": (
                "Campaign Lambda / Volume CS1-011 completes after this Revision. Honest stop: "
                "3.2 Pilot Arc closed. Not Chapter 3 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 3.3 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Lambda / CS1-011 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 3.3 successor Volume. Optional: schedule your "
                "weakest 3.2 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CL-D1",
        stem="3.2.1-confidence-interval-parameter-cs1011",
        pid="CS1-EP001-PKG-3.2-CONFIDENCE-INTERVAL-PARAMETER",
        lo="3.2.1",
        slug="3.2-confidence-interval-parameter",
        keywords=["confidence", "interval", "parameter", "random", "sample", "coverage"],
        title="Construct a confidence interval for an unknown parameter from a random sample",
        purpose=(
            "Today's Mission exists to construct a confidence interval for an unknown "
            "parameter of a distribution based on a random sample. So the CI coverage "
            "reading is usable. Without pretending prediction intervals (3.2.2) are finished."
        ),
        tutor=(
            "Today I will force the candidate to state a CI for a parameter from sample "
            "evidence and refuse treating a prediction interval as today's LO."
        ),
        edu=(
            "Produce a cognitive move from random-sample evidence to a parameter confidence "
            "interval under CMP language."
        ),
        lo_text=(
            "Confidence interval for an unknown parameter of a distribution based on a "
            "random sample."
        ),
        focus="Random sample → estimator / pivotal idea → parameter CI → refuse prediction-as-done.",
        prior=(
            "Campaign Kappa closed estimators (3.1) with Revision. Today opens topic 3.2 at "
            "LO 3.2.1. The named Continuity Front after CS1-010."
        ),
        why=(
            "3.2.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at intervals, keeping prediction intervals for the following session."
        ),
        benefit=(
            "You will be able to construct and correctly interpret a confidence "
            "interval for an unknown parameter. And refuse prediction-interval "
            "readings."
        ),
        explain=(
            "Day 1 opens 3.2 at the named learning objective. "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, state what a confidence interval claims about a parameter.",
            "Name the sample-to-interval move in CMP-usable form.",
            "Refuse one 'prediction interval finished today's LO' claim.",
        ],
        tasks=[
            "Sketch sample → parameter CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.1.",
            "Closed-book Knowledge Checks: parameter CI + refuse prediction swallow.",
        ],
        next_code="3.2",
        next_title="Prediction interval for a future observation (3.2.2)",
        cont=(
            "Today you constructed a parameter confidence interval from a random sample; "
            "tomorrow continues 3.2 at prediction intervals."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.2. Titles only tonight",
        student=(
            "Tomorrow: prediction interval (3.2.2). Optional light prep: skim 3.2.2 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.2.1 confidence interval for a parameter",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.1 "
            "(stop before prediction interval 3.2.2)"
        ),
        oos=[
            "Prediction interval as primary (3.2.2)",
            "Given-sampling-distribution CI primary (3.2.3)",
            "Normal mean/variance CIs primary (3.2.4)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating any interval with a confidence interval for a parameter.",
            "Watch for starting prediction-interval drills (3.2.2) inside this sitting.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does a confidence interval claim about an unknown "
            "parameter? (2) What sample ingredient enters the construction? (3) Name one "
            "reason a prediction interval is not today's LO."
        ),
        ar_kw=[
            "confidence",
            "parameter",
            "sample",
            "interval",
            "coverage",
            "prediction",
        ],
        ar_model=(
            "A confidence interval uses random-sample evidence to give an interval for an "
            "unknown parameter with a stated frequentist coverage reading. A prediction "
            "interval targets a future observation. That is tomorrow's LO, not today's."
        ),
        cp_prompt=(
            "Closed-book. From a large sample you obtain a 95% CI for mean claim "
            "size μ as (120, 140). (1) What does this interval claim about the "
            "unknown parameter μ? (2) Refuse: 'There is a 95% probability that the "
            "next claim falls between 120 and 140.'"
        ),
        cp_kw=["parameter", "coverage", "confidence", "refuse", "prediction", "future"],
        cp_model=(
            "(1) The interval was produced by a procedure that covers the unknown "
            "parameter μ in 95% of repeated samples (frequentist coverage for μ). "
            "(2) Refuse: that reading is a prediction claim about a future "
            "observation, not a confidence interval for a parameter."
        ),
        reflect="Harvest CI coverage-reading wobble. Keep prediction out of tonight's claim.",
    ),
    dict(
        day="CL-D2",
        stem="3.2.2-prediction-interval-cs1011",
        pid="CS1-EP001-PKG-3.2-PREDICTION-INTERVAL",
        lo="3.2.2",
        slug="3.2-prediction-interval",
        keywords=["prediction", "interval", "future", "observation", "model", "sample"],
        title="Construct a prediction interval for a future observation",
        purpose=(
            "Today's Mission exists to construct a prediction interval for a future "
            "observation based on a model fitted to a random sample. So prediction is "
            "distinct from parameter CI. Without pretending given-sampling-distribution "
            "CIs (3.2.3) are finished."
        ),
        tutor=(
            "Today I will force the candidate to target a future observation with a "
            "prediction interval and refuse collapsing it into yesterday's parameter CI."
        ),
        edu=(
            "Produce a cognitive move from a fitted model on a random sample to a prediction "
            "interval for a future observation."
        ),
        lo_text=(
            "Prediction interval for a future observation based on a model fitted to a "
            "random sample."
        ),
        focus=(
            "Fitted model → future observation → prediction interval → refuse "
            "given-distribution CI-as-done."
        ),
        prior=(
            "Yesterday you constructed a parameter confidence interval (3.2.1). Today "
            "continues topic 3.2 at LO 3.2.2: prediction intervals."
        ),
        why=(
            "3.2.2 is contiguous after parameter CI. Closing it prevents a cliff at "
            "prediction while keeping given-sampling-distribution CI as day three."
        ),
        benefit=(
            "You will be able to construct a prediction interval for a future "
            "observation and distinguish it from a parameter CI."
        ),
        explain=(
            "Day 2 continues at the named learning objective. Prediction immediately after parameter CI."
        ),
        criteria=[
            "Closed-book, state what a prediction interval targets.",
            "Name how a fitted model from a random sample enters.",
            "Refuse one 'parameter CI finished prediction' claim.",
        ],
        tasks=[
            "Sketch fitted model → future observation interval before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.2.",
            "Closed-book Knowledge Checks: prediction interval + refuse CI collapse.",
        ],
        next_code="3.2",
        next_title="CI using a given sampling distribution (3.2.3)",
        cont=(
            "Today you constructed a prediction interval; tomorrow continues 3.2 at "
            "confidence intervals that use a given sampling distribution."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.3. Titles only tonight",
        student=(
            "Tomorrow: CI given a sampling distribution (3.2.3). Optional light prep: skim "
            "3.2.3 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.2.2 prediction interval",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.2 "
            "(stop before given-sampling-distribution CI 3.2.3)"
        ),
        oos=[
            "Given-sampling-distribution CI as primary (3.2.3)",
            "Normal mean/variance CIs primary (3.2.4)",
            "Bootstrap CI primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating parameter CI and prediction interval as interchangeable.",
            "Watch for starting given-distribution CI drills (3.2.3) today.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does a prediction interval claim about a future "
            "observation? (2) What role does a model fitted to a random sample play? "
            "(3) Name one difference from a parameter confidence interval."
        ),
        ar_kw=[
            "prediction",
            "future",
            "observation",
            "model",
            "sample",
            "parameter",
        ],
        ar_model=(
            "A prediction interval targets a future observation (not the parameter itself), "
            "using a model fitted to a random sample. A parameter CI targets the unknown "
            "parameter: different object."
        ),
        cp_prompt=(
            "Closed-book. You fit a model to historical annual losses and need an "
            "interval for next year's loss Y_new. (1) What does a prediction "
            "interval cover that a parameter CI for E[Y] does not? (2) Refuse: 'My "
            "confidence interval for the mean loss already finished the "
            "prediction-interval LO.'"
        ),
        cp_kw=["prediction", "future", "observation", "parameter", "refuse", "mean", "wider"],
        cp_model=(
            "(1) A prediction interval aims to cover a future observation Y_new "
            "(parameter uncertainty plus process/residual variation); a parameter CI "
            "covers only a fixed unknown parameter such as E[Y]. (2) Refuse: a "
            "parameter CI is not a prediction interval. Different target, typically "
            "wider for prediction."
        ),
        reflect="Harvest prediction-vs-CI wobble. Keep given-distribution CI out of tonight's claim.",
    ),
    dict(
        day="CL-D3",
        stem="3.2.3-ci-given-sampling-distribution-cs1011",
        pid="CS1-EP001-PKG-3.2-CI-GIVEN-SAMPLING-DISTRIBUTION",
        lo="3.2.3",
        slug="3.2-ci-given-sampling-distribution",
        keywords=["confidence", "interval", "sampling", "distribution", "pivotal", "given"],
        title="Construct a confidence interval using a given sampling distribution",
        purpose=(
            "Today's Mission exists to construct a confidence interval for an unknown "
            "parameter using a given sampling distribution. So the given-distribution "
            "route is usable. Without pretending Normal mean/variance recipes (3.2.4) "
            "are finished."
        ),
        tutor=(
            "Today I will force the candidate to use a stated sampling distribution to form "
            "a CI and refuse treating Normal mean/variance cookbook as today's LO."
        ),
        edu=(
            "Produce a cognitive move from a given sampling distribution to a parameter "
            "confidence interval under CMP language."
        ),
        lo_text=(
            "Confidence interval for an unknown parameter using a given sampling distribution."
        ),
        focus="Given sampling distribution → invert / pivot → CI → refuse Normal cookbook-as-done.",
        prior=(
            "Yesterday you constructed a prediction interval (3.2.2). Today continues topic "
            "3.2 at LO 3.2.3: CI using a given sampling distribution."
        ),
        why=(
            "3.2.3 is contiguous after prediction. Closing it prevents a cliff at the "
            "given-distribution method while keeping Normal mean/variance CIs as day four."
        ),
        benefit=(
            "You will be able to form a CI by inverting a given sampling "
            "distribution, not only by recalling Normal-mean formulae."
        ),
        explain=(
            "Day 3 continues at the named learning objective. Given-sampling-distribution CI after prediction."
        ),
        criteria=[
            "Closed-book, state how a given sampling distribution yields a CI.",
            "Name the invert / pivotal move in CMP-usable form.",
            "Refuse one 'Normal mean/variance recipes finished today' claim.",
        ],
        tasks=[
            "Sketch given sampling distribution → CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.3.",
            "Closed-book Knowledge Checks: given-distribution CI + refuse Normal swallow.",
        ],
        next_code="3.2",
        next_title="Normal mean and variance confidence intervals (3.2.4)",
        cont=(
            "Today you formed a CI from a given sampling distribution; tomorrow continues "
            "3.2 at Normal mean and variance intervals."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.4. Titles only tonight",
        student=(
            "Tomorrow: Normal mean and variance CIs (3.2.4). Optional light prep: skim 3.2.4 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.2.3 CI using a given sampling distribution",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.3 "
            "(stop before Normal mean/variance CIs 3.2.4)"
        ),
        oos=[
            "Normal mean/variance CIs as primary (3.2.4)",
            "Binomial/Poisson CIs primary (3.2.5)",
            "Bootstrap CI primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for jumping straight to Normal mean/variance formulae as today's LO.",
            "Watch for treating any CI template as 'given sampling distribution' without using it.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the given-sampling-distribution CI move? (2) What is "
            "inverted or pivoted? (3) Name one reason Normal mean/variance recipes are not "
            "automatically today's LO."
        ),
        ar_kw=[
            "sampling",
            "distribution",
            "confidence",
            "interval",
            "pivot",
            "invert",
        ],
        ar_model=(
            "Given a sampling distribution for an estimator or pivotal quantity, invert that "
            "distribution to obtain a confidence interval for the parameter. Specific Normal "
            "mean/variance recipes are tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. For an Exponential mean-θ model you are told that 2n X̄ / "
            "θ ~ χ²_{2n}. (1) Outline how you invert this sampling distribution to "
            "form a CI for θ. (2) Refuse: 'I memorised the Normal-mean CI cookbook, "
            "so any sampling-distribution CI is done.'"
        ),
        cp_kw=["invert", "sampling distribution", "pivot", "chi-square", "refuse", "Normal"],
        cp_model=(
            "(1) Choose χ² critical values so P(χ²_L < 2n X̄ / θ < χ²_U) = 1−α, then "
            "rearrange the inequality to isolate θ (bounds involve 2n X̄ / χ²). (2) "
            "Refuse: cookbook Normal-mean formulae do not replace inverting the "
            "given sampling distribution for this model."
        ),
        reflect="Harvest given-distribution inversion wobble. Keep Normal cookbook out of tonight's claim.",
    ),
    dict(
        day="CL-D4",
        stem="3.2.4-ci-normal-mean-variance-cs1011",
        pid="CS1-EP001-PKG-3.2-CI-NORMAL-MEAN-VARIANCE",
        lo="3.2.4",
        slug="3.2-ci-normal-mean-variance",
        keywords=["normal", "mean", "variance", "confidence", "interval", "chi-square", "t"],
        title="Construct confidence intervals for the mean and variance of a Normal distribution",
        purpose=(
            "Today's Mission exists to construct confidence intervals for the mean and the "
            "variance of a Normal distribution. So both Normal interval recipes are usable "
            ". Without pretending binomial/Poisson CIs (3.2.5) are finished."
        ),
        tutor=(
            "Today I will force the candidate to form Normal mean and variance CIs and refuse "
            "treating binomial/Poisson approximation as today's LO."
        ),
        edu=(
            "Produce cognitive moves for Normal mean and Normal variance confidence intervals "
            "under CMP language."
        ),
        lo_text=(
            "Confidence intervals for the mean and the variance of a normal distribution."
        ),
        focus="Normal sample → mean CI → variance CI → refuse binomial/Poisson-as-done.",
        prior=(
            "Yesterday you formed a CI from a given sampling distribution (3.2.3). Today "
            "continues topic 3.2 at LO 3.2.4: Normal mean and variance intervals."
        ),
        why=(
            "3.2.4 is contiguous after the given-distribution method. Closing it prevents a "
            "cliff at Normal recipes while keeping binomial/Poisson as day five."
        ),
        benefit=(
            "You will be able to construct confidence intervals for both the mean "
            "and the variance of a Normal sample."
        ),
        explain=(
            "Day 4 continues at the named learning objective. Normal mean/variance CIs after given-sampling-distribution CI."
        ),
        criteria=[
            "Closed-book, state the Normal mean CI hinge.",
            "State the Normal variance CI hinge.",
            "Refuse one 'binomial/Poisson finished today' claim.",
        ],
        tasks=[
            "Sketch Normal mean CI and Normal variance CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.4.",
            "Closed-book Knowledge Checks: both Normal recipes + refuse binomial swallow.",
        ],
        next_code="3.2",
        next_title="Binomial and Poisson confidence intervals (3.2.5)",
        cont=(
            "Today you formed Normal mean and variance CIs; tomorrow continues 3.2 at "
            "binomial and Poisson intervals (including Normal approximation)."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.5. Titles only tonight",
        student=(
            "Tomorrow: binomial/Poisson CIs (3.2.5). Optional light prep: skim 3.2.5 headings "
            ". Titles only tonight."
        ),
        open="CMP · Syllabus 3.2.4 Normal mean and variance confidence intervals",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.4 "
            "(stop before binomial/Poisson CIs 3.2.5)"
        ),
        oos=[
            "Binomial/Poisson CIs as primary (3.2.5)",
            "Two-sample CIs primary (3.2.6)",
            "Bootstrap CI primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for covering only the mean CI and calling variance done.",
            "Watch for starting binomial/Poisson drills (3.2.5) today.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) State the hinge for a CI for a Normal mean. (2) State the "
            "hinge for a CI for a Normal variance. (3) Name one reason binomial/Poisson "
            "intervals are not today's LO."
        ),
        ar_kw=["normal", "mean", "variance", "confidence", "interval", "t", "chi"],
        ar_model=(
            "For a Normal sample, form a CI for the mean (typically via Normal/t pivotal "
            "structure under CMP conditions) and a CI for the variance (typically via "
            "chi-square structure under CMP conditions). Binomial/Poisson intervals are "
            "tomorrow."
        ),
        cp_prompt=(
            "Closed-book. IID Normal sample, n=16, x̄=10, s²=4 (σ unknown). (1) "
            "State the form of a CI for μ and the form of a CI for σ². (2) Refuse: "
            "'The mean CI alone finishes today. Variance can wait, and binomial is "
            "the same LO.'"
        ),
        cp_kw=["Normal", "mean", "variance", "t", "chi-square", "refuse", "both"],
        cp_model=(
            "(1) For μ: x̄ ± t_{n−1, 1−α/2} · s/√n. For σ²: ((n−1)s² / χ²_{n−1, "
            "1−α/2}, (n−1)s² / χ²_{n−1, α/2}). (2) Refuse: both Normal mean and "
            "Normal variance CIs are required; binomial/Poisson intervals are a "
            "different LO."
        ),
        reflect="Harvest mean-vs-variance CI wobble. Keep binomial out of tonight's claim.",
    ),
    dict(
        day="CL-D5",
        stem="3.2.5-ci-binomial-poisson-cs1011",
        pid="CS1-EP001-PKG-3.2-CI-BINOMIAL-POISSON",
        lo="3.2.5",
        slug="3.2-ci-binomial-poisson",
        keywords=["binomial", "Poisson", "probability", "mean", "normal", "approximation", "CI"],
        title="Construct confidence intervals for a binomial probability and a Poisson mean",
        purpose=(
            "Today's Mission exists to construct confidence intervals for a binomial "
            "probability and a Poisson mean, including Normal approximation in both cases "
            " (so discrete-parameter CIs are usable) without pretending two-sample CIs "
            "(3.2.6) are finished."
        ),
        tutor=(
            "Today I will force binomial-probability and Poisson-mean CI construction "
            "(including Normal approximation) and refuse treating two-sample intervals as "
            "today's LO."
        ),
        edu=(
            "Produce cognitive moves for binomial-probability and Poisson-mean confidence "
            "intervals, including Normal approximation under CMP conditions."
        ),
        lo_text=(
            "Confidence intervals for a binomial probability and a Poisson mean, including "
            "the use of the normal approximation in both cases."
        ),
        focus="Binomial p CI → Poisson mean CI → Normal approx → refuse two-sample-as-done.",
        prior=(
            "Yesterday you formed Normal mean and variance CIs (3.2.4). Today continues "
            "topic 3.2 at LO 3.2.5: binomial and Poisson intervals."
        ),
        why=(
            "3.2.5 is contiguous after Normal recipes. Closing it prevents a cliff at "
            "discrete-parameter intervals while keeping two-sample CIs as day six."
        ),
        benefit=(
            "You will be able to form Normal-approximation confidence intervals for "
            "both a binomial probability and a Poisson mean."
        ),
        explain=(
            "Day 5 continues at the named learning objective. Binomial/Poisson CIs after Normal mean/variance."
        ),
        criteria=[
            "Closed-book, state the binomial-probability CI hinge (incl. Normal approx).",
            "State the Poisson-mean CI hinge (incl. Normal approx).",
            "Refuse one 'two-sample finished today' claim.",
        ],
        tasks=[
            "Sketch binomial p CI and Poisson mean CI (with Normal approx) before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.5.",
            "Closed-book Knowledge Checks: both discrete CIs + refuse two-sample swallow.",
        ],
        next_code="3.2",
        next_title="Two-sample confidence intervals (3.2.6)",
        cont=(
            "Today you formed binomial and Poisson CIs; tomorrow continues 3.2 at "
            "two-sample situations."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.6. Titles only tonight",
        student=(
            "Tomorrow: two-sample CIs (3.2.6). Optional light prep: skim 3.2.6 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.2.5 binomial and Poisson confidence intervals",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.5 "
            "(stop before two-sample CIs 3.2.6)"
        ),
        oos=[
            "Two-sample CIs as primary (3.2.6)",
            "Paired-means CI primary (3.2.7)",
            "Bootstrap CI primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for covering only binomial and calling Poisson done (or vice versa).",
            "Watch for skipping Normal approximation when the syllabus includes it.",
            "Watch for starting two-sample drills (3.2.6) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) State the hinge for a CI for a binomial probability, noting "
            "Normal approximation. (2) State the hinge for a CI for a Poisson mean, noting "
            "Normal approximation. (3) Name one reason two-sample CIs are not today's LO."
        ),
        ar_kw=[
            "binomial",
            "Poisson",
            "probability",
            "mean",
            "normal",
            "approximation",
            "confidence",
        ],
        ar_model=(
            "Form a CI for a binomial probability and for a Poisson mean, using Normal "
            "approximation under CMP conditions where appropriate. Two-sample intervals are "
            "tomorrow."
        ),
        cp_prompt=(
            "Closed-book. (1) State a Normal-approximation CI form for a binomial "
            "probability p and for a Poisson mean λ (single sample). (2) Refuse: 'A "
            "binomial CI alone finishes the LO. Poisson is the same formula with a "
            "different letter.'"
        ),
        cp_kw=["binomial", "Poisson", "Normal", "approximation", "refuse", "both"],
        cp_model=(
            "(1) Binomial: p̂ ± z_{1−α/2} √(p̂(1−p̂)/n). Poisson: λ̂ ± z_{1−α/2} "
            "√(λ̂/n) (or equivalent for a total count with matching variance). (2) "
            "Refuse: both binomial-p and Poisson-mean CIs with Normal approximation "
            "are required. One does not stand in for the other."
        ),
        reflect="Harvest discrete-parameter CI wobble. Keep two-sample out of tonight's claim.",
    ),
    dict(
        day="CL-D6",
        stem="3.2.6-ci-two-sample-cs1011",
        pid="CS1-EP001-PKG-3.2-CI-TWO-SAMPLE",
        lo="3.2.6",
        slug="3.2-ci-two-sample",
        keywords=["two-sample", "normal", "binomial", "Poisson", "difference", "confidence"],
        title="Construct confidence intervals for two-sample situations",
        purpose=(
            "Today's Mission exists to construct confidence intervals for two-sample "
            "situations involving the Normal distribution and the binomial and Poisson "
            "distributions using the Normal approximation. So two-sample interval literacy "
            "is usable. Without pretending paired-means CI (3.2.7) is finished."
        ),
        tutor=(
            "Today I will force two-sample CI construction across Normal / binomial / "
            "Poisson (Normal approx) settings and refuse treating paired data as today's LO."
        ),
        edu=(
            "Produce cognitive moves for two-sample confidence intervals under Normal, "
            "binomial, and Poisson (Normal approximation) settings."
        ),
        lo_text=(
            "Confidence intervals for two-sample situations involving the normal "
            "distribution and the binomial and Poisson distributions using the normal "
            "approximation."
        ),
        focus="Two independent samples → difference / contrast CI → refuse paired-as-done.",
        prior=(
            "Yesterday you formed binomial and Poisson single-sample CIs (3.2.5). Today "
            "continues topic 3.2 at LO 3.2.6: two-sample situations."
        ),
        why=(
            "3.2.6 is contiguous after single-sample discrete CIs. Closing it prevents a "
            "cliff at two-sample intervals while keeping paired means as day seven."
        ),
        benefit=(
            "You will be able to construct independent two-sample CIs and refuse "
            "misapplying them to paired data."
        ),
        explain=(
            "Day 6 continues at the named learning objective. Two-sample CIs after binomial/Poisson single-sample work."
        ),
        criteria=[
            "Closed-book, state the two-sample CI hinge for a Normal setting.",
            "Name how binomial/Poisson two-sample CIs use Normal approximation.",
            "Refuse one 'paired data finished today' claim.",
        ],
        tasks=[
            "Sketch two-sample contrast CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.6.",
            "Closed-book Knowledge Checks: two-sample CI + refuse paired swallow.",
        ],
        next_code="3.2",
        next_title="Paired-data mean-difference confidence interval (3.2.7)",
        cont=(
            "Today you formed two-sample CIs; tomorrow continues 3.2 at paired-data "
            "mean-difference intervals."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.7. Titles only tonight",
        student=(
            "Tomorrow: paired mean-difference CI (3.2.7). Optional light prep: skim 3.2.7 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.2.6 two-sample confidence intervals",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.6 "
            "(stop before paired-means CI 3.2.7)"
        ),
        oos=[
            "Paired-means CI as primary (3.2.7)",
            "Bootstrap CI primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating paired differences as two independent samples today.",
            "Watch for covering only Normal two-sample and calling binomial/Poisson done.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the two-sample CI move for a Normal setting? "
            "(2) How do binomial/Poisson two-sample CIs use Normal approximation? "
            "(3) Name one reason paired data is not today's LO."
        ),
        ar_kw=[
            "two-sample",
            "difference",
            "normal",
            "binomial",
            "Poisson",
            "approximation",
            "paired",
        ],
        ar_model=(
            "Form CIs for contrasts between two independent samples (Normal; binomial/"
            "Poisson via Normal approximation under CMP conditions). Paired mean-difference "
            "is tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Independent samples of claim amounts from portfolio A and "
            "portfolio B (Normal model). (1) What parameter contrast does a "
            "two-sample CI target, and what independence assumption is required? (2) "
            "Refuse: 'Paired before/after rows with equal n are just two-sample with "
            "n₁ = n₂.'"
        ),
        cp_kw=["two-sample", "independent", "difference", "paired", "refuse", "Normal"],
        cp_model=(
            "(1) Typically μ_A − μ_B (or an analogous contrast for binomial/Poisson "
            "with Normal approx), under independent samples from the two groups. (2) "
            "Refuse: paired data shares observational units; equal sample sizes do "
            "not make paired rows an independent two-sample problem. Use the "
            "paired-difference construction instead."
        ),
        reflect="Harvest two-sample contrast wobble. Keep paired out of tonight's claim.",
    ),
    dict(
        day="CL-D7",
        stem="3.2.7-ci-paired-means-cs1011",
        pid="CS1-EP001-PKG-3.2-CI-PAIRED-MEANS",
        lo="3.2.7",
        slug="3.2-ci-paired-means",
        keywords=["paired", "difference", "means", "confidence", "interval", "matched"],
        title="Construct a confidence interval for a difference between two means from paired data",
        purpose=(
            "Today's Mission exists to construct a confidence interval for a difference "
            "between two means from paired data. So paired-difference literacy is usable "
            ". Without pretending bootstrap CIs (3.2.8) are finished."
        ),
        tutor=(
            "Today I will force a paired mean-difference CI and refuse treating independent "
            "two-sample or bootstrap CI as today's LO."
        ),
        edu=(
            "Produce a cognitive move from paired observations to a CI for the mean "
            "difference under CMP language."
        ),
        lo_text=(
            "Confidence intervals for a difference between two means from paired data."
        ),
        focus="Paired observations → differences → mean-difference CI → refuse bootstrap-as-done.",
        prior=(
            "Yesterday you formed two-sample CIs (3.2.6). Today continues topic 3.2 at LO "
            "3.2.7: paired mean-difference intervals."
        ),
        why=(
            "3.2.7 is contiguous after independent two-sample work. Closing it prevents a "
            "cliff at paired data while keeping bootstrap CI as day eight."
        ),
        benefit=(
            "You will be able to form a paired mean-difference CI by analysing "
            "within-pair differences."
        ),
        explain=(
            "Day 7 continues at the named learning objective. Paired-means CI after two-sample situations."
        ),
        criteria=[
            "Closed-book, state the paired mean-difference CI hinge.",
            "Name why pairing differs from independent two-sample.",
            "Refuse one 'bootstrap CI finished today' claim.",
        ],
        tasks=[
            "Sketch paired differences → CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.7.",
            "Closed-book Knowledge Checks: paired CI + refuse bootstrap swallow.",
        ],
        next_code="3.2",
        next_title="Bootstrap confidence intervals (3.2.8)",
        cont=(
            "Today you formed a paired mean-difference CI; tomorrow continues 3.2 at "
            "bootstrap confidence intervals."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.2.8. Titles only tonight",
        student=(
            "Tomorrow: bootstrap CIs (3.2.8). Optional light prep: skim 3.2.8 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.2.7 paired mean-difference confidence interval",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.7 "
            "(stop before bootstrap CI 3.2.8)"
        ),
        oos=[
            "Bootstrap CI as primary (3.2.8)",
            "Hypothesis testing (3.3)",
            "Independent two-sample re-teach as primary",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for analysing paired data as independent two-sample without warrant.",
            "Watch for starting bootstrap CI drills (3.2.8) today.",
            "Watch for hypothesis testing (3.3) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the paired mean-difference CI move? (2) Why is pairing "
            "not the same as independent two-sample? (3) Name one reason bootstrap CI is not "
            "today's LO."
        ),
        ar_kw=["paired", "difference", "means", "confidence", "interval", "bootstrap"],
        ar_model=(
            "Form differences within pairs and construct a CI for the mean difference. "
            "Pairing exploits dependence. Not the same as independent two-sample. Bootstrap "
            "CI is tomorrow."
        ),
        cp_prompt=(
            "Closed-book. Each policyholder has a before/after loss pair (Xᵢ, Yᵢ). "
            "(1) What do you analyse to form a CI for the mean difference? (2) "
            "Refuse: 'Apply the independent two-sample CI to the before column and "
            "the after column.'"
        ),
        cp_kw=["paired", "difference", "one-sample", "refuse", "independent", "two-sample"],
        cp_model=(
            "(1) Form paired differences Dᵢ = Yᵢ − Xᵢ (or Xᵢ − Yᵢ), then build a "
            "one-sample CI for μ_D. (2) Refuse: the independent two-sample formula "
            "ignores pairing and uses the wrong variance structure for matched pairs."
        ),
        reflect="Harvest pairing wobble. Keep bootstrap out of tonight's claim.",
    ),
    dict(
        day="CL-D8",
        stem="3.2.8-bootstrap-confidence-interval-cs1011",
        pid="CS1-EP001-PKG-3.2-BOOTSTRAP-CONFIDENCE-INTERVAL",
        lo="3.2.8",
        slug="3.2-bootstrap-confidence-interval",
        keywords=["bootstrap", "confidence", "interval", "resample", "percentile", "estimator"],
        title="Obtain confidence intervals by the bootstrap method",
        purpose=(
            "Today's Mission exists to obtain confidence intervals by the bootstrap method "
            " (so bootstrap interval construction is usable) without pretending hypothesis "
            "testing (3.3) or Chapter 3 complete are finished."
        ),
        tutor=(
            "Today I will force bootstrap CI construction and refuse treating Kappa's "
            "bootstrap-for-estimator-properties or 3.3 hypothesis testing as today's LO."
        ),
        edu=(
            "Produce a cognitive move from resampling to a bootstrap confidence interval "
            "under CMP language."
        ),
        lo_text="Bootstrap method to obtain confidence intervals.",
        focus=(
            "Resample → bootstrap replicates of the statistic → bootstrap CI → "
            "refuse properties-bootstrap-as-CI."
        ),
        prior=(
            "Yesterday you formed a paired mean-difference CI (3.2.7). Today completes the "
            "3.2 Learning span at LO 3.2.8: bootstrap confidence intervals."
        ),
        why=(
            "3.2.8 completes topic 3.2 Learning. Closing it prevents a cliff at bootstrap "
            "intervals while keeping hypothesis testing as a later Volume."
        ),
        benefit=(
            "You will be able to obtain a confidence interval by the bootstrap "
            "method and distinguish it from bootstrap SE estimation."
        ),
        explain=(
            "Day 8 continues at the named learning objective. Bootstrap CI as the terminal Learning day of 3.2."
        ),
        criteria=[
            "Closed-book, state the bootstrap CI construction move.",
            "Distinguish bootstrap CI from Kappa's bootstrap-for-estimator-properties if asked.",
            "Refuse one 'Chapter 3 / 3.3 finished' claim.",
        ],
        tasks=[
            "Sketch resample → bootstrap CI before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.2.8.",
            "Closed-book Knowledge Checks: bootstrap CI + refuse 3.3 / Chapter 3 swallow.",
        ],
        next_code="CL-R1",
        next_title="Campaign Lambda Revision: retrieve 3.2 hinges",
        cont=(
            "Today you obtained bootstrap confidence intervals; tomorrow is Revision. "
            "retrieve the 3.2 chain closed-book (not first-pass 3.3)."
        ),
        prep="Optional: list the eight 3.2 LO codes from memory. Titles only tonight",
        student=(
            "Tomorrow: CL-R1 Revision (retrieve 3.2.1–3.2.8). Optional light prep: list the "
            "eight LO codes from memory. Titles only tonight."
        ),
        open="CMP · Syllabus 3.2.8 bootstrap confidence intervals",
        stop=(
            "Through the CMP treatment of Syllabus 3.2.8 "
            "(stop before hypothesis testing 3.3)"
        ),
        oos=[
            "Hypothesis testing / goodness of fit as primary (3.3)",
            "Chapter 3 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Treating Kappa estimator-bootstrap as finishing this LO without CI construction",
        ],
        misconceptions=[
            "Watch for equating bootstrap-for-estimator-properties (3.1.6) with bootstrap CI.",
            "Watch for starting hypothesis testing (3.3) inside this sitting.",
            "Watch for Chapter 3 / spine / until-exam claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is the bootstrap method move for obtaining a confidence "
            "interval? (2) What is resampled? (3) Name one reason this is not the same as "
            "finishing hypothesis testing (3.3)."
        ),
        ar_kw=[
            "bootstrap",
            "resample",
            "confidence",
            "interval",
            "percentile",
            "hypothesis",
        ],
        ar_model=(
            "Resample from the sample (or an appropriate bootstrap mechanism under CMP), "
            "form the interval statistic on replicates, and obtain a bootstrap confidence "
            "interval. Hypothesis testing is topic 3.3. Not today's LO."
        ),
        cp_prompt=(
            "Closed-book. (1) Outline the bootstrap move to obtain a confidence "
            "interval for a parameter (percentile idea is enough). (2) Refuse: "
            "'Bootstrap for an estimator standard error is the same as a bootstrap "
            "confidence interval' and 'finishing a bootstrap CI finishes hypothesis "
            "testing.'"
        ),
        cp_kw=["bootstrap", "resample", "percentile", "confidence", "interval", "refuse", "hypothesis"],
        cp_model=(
            "(1) Resample with replacement, recompute the statistic on each "
            "resample, then form an interval from the bootstrap distribution of that "
            "statistic (e.g. percentile interval from the α/2 and 1−α/2 quantiles of "
            "the replicates). (2) Refuse: estimating an estimator property is not "
            "the same as constructing a CI; hypothesis testing is a different LO."
        ),
        reflect=(
            "Harvest bootstrap CI procedure wobble. Revision protects the 3.2 chain tomorrow."
        ),
    ),
]


def main() -> None:
    PKG_DIR.mkdir(parents=True, exist_ok=True)
    inventory: list[str] = []
    span: list[str] = []

    for d in LEARNING:
        pkg = apply_mcq_overlay(learning_pkg(d), d["stem"])
        path = PKG_DIR / f"{d['stem']}.json"
        path.write_text(json.dumps(pkg, indent=2, ensure_ascii=False) + "\n")
        inventory.append(d["pid"])
        span.append(d["lo"])

    rev = apply_batch6b_mcq_overlay(revision_pkg(), "revision-confidence-intervals-cs1011")
    (PKG_DIR / "revision-confidence-intervals-cs1011.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-LAMBDA",
        "campaign_version": "cs1011-1.0.0",
        "display_title": "Campaign Lambda: Confidence and prediction intervals (3.2)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-011",
        "prior_volume_id": "CS1-010",
        "day_count": {"learning": 8, "revision": 1, "total": 9},
        "syllabus_span": span,
        "out_of_scope": [
            "3.3+",
            "Chapter 3 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 10 / remainder / spine re-audit authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

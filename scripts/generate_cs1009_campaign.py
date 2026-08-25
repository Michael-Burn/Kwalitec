#!/usr/bin/env python3
"""Generate CS1-009 / Campaign Iota educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-iota-cs1009"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1009-campaign-iota-1.0.0",
    "publication_version": "cs1009-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-IOTA",
    "volume_id": "CS1-009",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1009_EDUCATIONAL_VOLUME.md",
        "CS1009_CERTIFICATION_REPORT.md",
        "EP007_WAVE7_PLAN.md",
    ],
    "author_id": "cs1009-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "2.6",
    "topic_title": (
        "Describe random sampling and the sampling distributions of statistics "
        "commonly used in statistical inference"
    ),
    "topic_id": "CS1-B-T06",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "2.6", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1009-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1009-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1009-cs1-{d['slug']}",
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
                f"for later 2.6 LOs, Chapter 2 trophy, Chapter 3 inference, or until-exam trust."
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
                "episode_id": f"lep-cs1009-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1009-{lo}-ar-01",
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
                "episode_id": f"lep-cs1009-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1009-{lo}-cp-01",
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
    day = "CI-R1"
    pid = "CS1-EP001-PKG-REV-SAMPLING-DISTRIBUTIONS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Iota revision — random sampling and sampling distributions",
        "return_targets": ["2.6.1", "2.6.2", "2.6.3", "2.6.4", "2.6.5", "2.6.6"],
        "topic_aliases": [day, "campaign-iota-revision"],
        "topic_title_keywords": [
            "revision",
            "sampling",
            "distribution",
            "sample",
            "mean",
            "variance",
            "t-statistic",
            "F",
            "Normal",
        ],
        "golden_id": "GOLDEN-CS1009-CS1-CI-R1-SAMPLING-DISTRIBUTIONS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1009-cs1-ci-r1-sampling-distributions",
            "display_title": "Retrieve sampling-distribution hinges (2.6)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Iota — retrieving random "
                "samples, sampling distributions of statistics, mean/variance of sample mean "
                "and mean of sample variance, Normal-sample mean/variance laws, the t-statistic, "
                "and the F ratio — so 2.6 does not evaporate before Chapter 3 inference."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Iota's Learning hinges — "
                "not a passive CMP re-read and not a first-pass 3.1 estimators lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: random "
                "sampling → sampling distribution of a statistic → mean/variance results → "
                "Normal sampling laws → t → F."
            ),
            "learning_objective": (
                "Retrieve and connect (1) random samples, (2) the sampling distribution of a "
                "statistic, (3) mean/variance of a sample mean and mean of a sample variance, "
                "(4) basic Normal sampling distributions for mean and variance, (5) the "
                "t-statistic, and (6) the F distribution for a variance ratio."
            ),
            "concept_focus": (
                "Campaign chain retrieval: random sample → sampling dist → E/Var results → "
                "Normal laws → t → F."
            ),
            "prior_bridge": (
                "Yesterday you finished the F distribution for a variance ratio (2.6.6). "
                "Today is Revision mode: return to 2.6.1–2.6.6 under closed-book retrieval — "
                "no new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 3.1 work."
            ),
            "expected_benefit": (
                "Evidence that the 2.6 chain retrieves — revision Study Progress, not a claim "
                "that Chapter 2 / Chapter 3 / the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the six 2.6 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse Chapter 2 complete / spine / until-exam / 3.1-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Iota's chain: sample → statistic → mean/var "
                "laws → Normal → t → F.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 45, "max": 60},
        },
        "session": {
            "session_id": "ssn-cs1009-cs1-ci-r1-sampling-distributions",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Iota skills — not to teach 3.1."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link — Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 45, "max": 60},
            "wrap_up": (
                "Revision Session complete. You stress-tested 2.6.1–2.6.6 return targets. "
                "This is revision Study Progress — not Topic Complete for Chapter 3, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that sampling-distribution hinges will still retrieve "
                "in three days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Iota "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the six 2.6 Learning hinges in order?",
                "Can you state when t vs Normal and when F enters?",
                "What claim must you refuse (Chapter 2 complete / spine / until-exam / 3.1 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 2 / Chapter 3 / spine complete.",
                "Watch for dropping Theta CLT memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection — do not begin Syllabus 3.1 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass estimators / inference (3.1)",
                "Confidence intervals / hypothesis testing primary",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Chapter 2 complete trophy claim",
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
                "episode_id": "lep-cs1009-ci-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1009-ci-r1-ar-01",
                "title": "Active Recall: CI-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) random sample; "
                    "(2) sampling distribution of a statistic; (3) mean/variance of sample mean "
                    "and mean of sample variance; (4) Normal sampling laws for mean/variance; "
                    "(5) t-statistic; (6) F variance ratio."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 2.6.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "sample",
                    "sampling",
                    "distribution",
                    "mean",
                    "variance",
                    "Normal",
                    "t",
                    "F",
                    "statistic",
                ],
                "explanation": "Revision retrieves the 2.6 arc.",
                "model_answer": (
                    "Example: (1) iid draws from a population; (2) distribution of a statistic "
                    "over repeated samples; (3) E/Var of X̄ and E[S²] in population terms; "
                    "(4) Normal-sample laws for X̄ and S² (χ² form as CMP); (5) t when σ unknown; "
                    "(6) F for ratio of independent sample variances."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Six hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1009-ci-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1009-ci-r1-cp-01",
                "title": "Checkpoint: CI-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest sampling-distribution link and one "
                    "concrete rework. (2) Refuse: 'My sample mean is the sampling "
                    "distribution, so Chapter 2 is done.' (3) Name the honest next topic "
                    "(estimators, 3.1) or confirm you are stopping here."
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
                    "3.1",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. F degrees of freedom — five-minute rework. (2) Refuse Chapter 2 "
                    "complete / spine / until-exam. (3) Honest next is 3.1 (successor Volume) "
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
            "next_topic_code": "3.1",
            "next_topic_title": (
                "Honest next — estimators and properties (3.1) under a successor Volume "
                "(or declared stop)"
            ),
            "continuity_line": (
                "Campaign Iota / Volume CS1-009 completes after this Revision. Honest stop: "
                "2.6 Pilot Arc closed — not Chapter 2 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 3.1 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight — rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Iota / CS1-009 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 3.1 successor Volume. Optional: schedule your "
                "weakest 2.6 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CI-D1",
        stem="2.6.1-random-samples-cs1009",
        pid="CS1-EP001-PKG-2.6-RANDOM-SAMPLES",
        lo="2.6.1",
        slug="2.6-random-samples",
        keywords=["random", "sample", "population", "iid", "sampling"],
        title="Describe random samples from a population",
        purpose=(
            "Today's Mission exists to describe random samples from a population — so the "
            "sampling model is usable — without pretending the sampling distribution of a "
            "statistic (2.6.2) is finished."
        ),
        tutor=(
            "Today I will force the candidate to state what a random sample means under CMP "
            "language — and refuse treating 'I drew some numbers' as having the LO."
        ),
        edu=(
            "Produce a cognitive move from population concept to a random sample as "
            "iid (or CMP-equivalent) draws."
        ),
        lo_text="Describe random samples from a population.",
        focus=(
            "Population → random sample (iid / CMP conditions) → refuse convenience-sample "
            "as-done."
        ),
        prior=(
            "Campaign Theta closed the central limit theorem (2.5) with Revision. Today opens "
            "topic 2.6 at LO 2.6.1 — the named Continuity Front after CS1-008."
        ),
        why=(
            "2.6.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at random sampling, keeping sampling-distribution of a statistic for the following session."
        ),
        benefit="Study Progress for random samples — not Topic Complete for 2.6.2.",
        explain=(
            "Day 1 opens 2.6 at the named learning objective — "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, define a random sample from a population in CMP-usable form.",
            "Name the independence / identical-distribution (or CMP-equivalent) warrant.",
            "Refuse one 'any collection of observed values is a random sample' claim.",
        ],
        tasks=[
            "Sketch population → random sample before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.6.1.",
            "Closed-book Knowledge Checks: random-sample definition + refuse convenience collapse.",
        ],
        next_code="2.6",
        next_title="Sampling distribution of a statistic (2.6.2)",
        cont=(
            "Today you described random samples from a population; tomorrow continues 2.6 "
            "at the sampling distribution of a statistic."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.6.2 — titles only tonight",
        student=(
            "Tomorrow: sampling distribution of a statistic (2.6.2). Optional light prep: "
            "skim 2.6.2 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.1 random samples from a population",
        stop=(
            "Through the CMP treatment of Syllabus 2.6.1 "
            "(stop before sampling distribution of a statistic 2.6.2)"
        ),
        oos=[
            "Sampling distribution of a statistic as primary (2.6.2)",
            "Mean/variance of sample mean primary (2.6.3)",
            "t / F / Normal sampling laws primary",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating any dataset with a random sample.",
            "Watch for starting sampling-distribution drills (2.6.2) inside this sitting.",
            "Watch for estimator / CI work (3.x) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a random sample from a population (CMP form)? "
            "(2) What independence / identical-distribution warrant matters? (3) Name one "
            "reason a convenience collection is not automatically a random sample."
        ),
        ar_kw=[
            "random",
            "sample",
            "population",
            "iid",
            "independent",
            "identical",
            "distribution",
        ],
        ar_model=(
            "A random sample is a set of observations drawn from a population under CMP "
            "sampling conditions (typically modelled as iid). Convenience collections need not "
            "satisfy those conditions."
        ),
        cp_prompt=(
            "Closed-book. A colleague says 'I have twenty observations, so I have a random "
            "sample.' Refuse in one sentence and restate what today's LO requires."
        ),
        cp_kw=["refuse", "random", "sample", "population", "iid", "not same", "conditions"],
        cp_model=(
            "Refuse: having observations is not the same as a random sample under CMP "
            "conditions. Today's skill is describing a random sample from a population with "
            "the lawful sampling warrant."
        ),
        reflect=(
            "Harvest wobble on population vs sample language — sampling distribution of a "
            "statistic comes tomorrow."
        ),
    ),
    dict(
        day="CI-D2",
        stem="2.6.2-sampling-distribution-statistic-cs1009",
        pid="CS1-EP001-PKG-2.6-SAMPLING-DISTRIBUTION-STATISTIC",
        lo="2.6.2",
        slug="2.6-sampling-distribution-statistic",
        keywords=["sampling", "distribution", "statistic", "sample", "repeated"],
        title="Describe the sampling distribution of a statistic",
        purpose=(
            "Today's Mission exists to describe the sampling distribution of a statistic — "
            "so the repeated-sample behaviour of a statistic is usable — without claiming "
            "mean/variance formulas (2.6.3) finished."
        ),
        tutor=(
            "Today I will force the candidate through sampling-distribution language for a "
            "statistic — refuse treating yesterday's random-sample definition as finishing "
            "2.6.2."
        ),
        edu=(
            "Produce executable warrants for the sampling distribution of a statistic over "
            "repeated random samples."
        ),
        lo_text="Describe the sampling distribution of a statistic.",
        focus=(
            "Statistic as function of sample → distribution over repeated samples → refuse "
            "single-sample-as-distribution."
        ),
        prior=(
            "Yesterday you described random samples from a population (2.6.1). Today names "
            "the sampling distribution of a statistic."
        ),
        why=(
            "2.6.2 continues after random samples; mean/variance "
            "results wait for day three."
        ),
        benefit="Study Progress for sampling distribution of a statistic — not 2.6.3.",
        explain="Campaign Iota Day 2 focuses LO 2.6.2.",
        criteria=[
            "Closed-book, define the sampling distribution of a statistic.",
            "Distinguish a statistic's realised value from its sampling distribution.",
            "Refuse treating one sample's statistic as the sampling distribution.",
        ],
        tasks=[
            "Sketch statistic → repeated samples → distribution before CMP.",
            "Guided Reading through CMP 2.6.2.",
            "Knowledge Checks: sampling distribution + refuse single-sample collapse.",
        ],
        next_code="2.6",
        next_title="Mean and variance of sample mean / mean of sample variance (2.6.3)",
        cont=(
            "Today you described the sampling distribution of a statistic; tomorrow continues "
            "2.6 at mean/variance results for sample mean and mean of sample variance."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.6.3 — titles only tonight",
        student=(
            "Tomorrow: mean/variance of sample mean and mean of sample variance (2.6.3). "
            "Optional light prep: skim 2.6.3 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.2 sampling distribution of a statistic",
        stop="Through CMP 2.6.2 (stop before mean/variance formulas 2.6.3)",
        oos=[
            "Mean/variance of sample mean primary (2.6.3)",
            "Normal sampling laws / t / F primary",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for confusing a statistic with a parameter.",
            "Watch for treating one realised statistic as its sampling distribution.",
            "Watch for jumping to Var(X̄)=σ²/n as today's only content without the concept.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a statistic in this LO? (2) What is its sampling "
            "distribution? (3) How does that differ from one realised value from one sample?"
        ),
        ar_kw=[
            "statistic",
            "sampling",
            "distribution",
            "sample",
            "repeated",
            "function",
            "parameter",
        ],
        ar_model=(
            "A statistic is a function of the sample. Its sampling distribution is the "
            "distribution of that statistic over repeated random samples. One realised value "
            "is a single draw from that distribution, not the distribution itself."
        ),
        cp_prompt=(
            "Closed-book. A colleague says 'my sample mean is 12, so the sampling distribution "
            "is 12.' Refuse and restate today's LO."
        ),
        cp_kw=["refuse", "sampling", "distribution", "statistic", "realised", "repeated"],
        cp_model=(
            "Refuse: a realised statistic is not its sampling distribution. Today's skill is "
            "describing the distribution of the statistic over repeated samples."
        ),
        reflect="Harvest statistic-vs-distribution wobble — mean/variance formulas tomorrow.",
    ),
    dict(
        day="CI-D3",
        stem="2.6.3-mean-var-sample-cs1009",
        pid="CS1-EP001-PKG-2.6-MEAN-VAR-SAMPLE",
        lo="2.6.3",
        slug="2.6-mean-var-sample",
        keywords=["mean", "variance", "sample", "mean", "population", "n"],
        title="Relate sample-mean and sample-variance moments to the population",
        purpose=(
            "Today's Mission exists to express the mean and variance of a sample mean and "
            "the mean of a sample variance in terms of population mean, variance and sample "
            "size — without claiming Normal-sample distributional laws (2.6.4) finished."
        ),
        tutor=(
            "Today I will force the candidate through E[X̄], Var(X̄), and E[S²] warrants — "
            "refuse treating sampling-distribution vocabulary alone as having the formulas."
        ),
        edu=(
            "Produce executable population-parameter expressions for E/Var of the sample mean "
            "and E of the sample variance."
        ),
        lo_text=(
            "Express the mean and variance of a sample mean and the mean of a sample variance "
            "in terms of the population mean, variance and sample size."
        ),
        focus=(
            "Population μ, σ², n → E[X̄], Var(X̄), E[S²] → refuse Normal-law / t jump today."
        ),
        prior=(
            "Yesterday you described the sampling distribution of a statistic (2.6.2). Today "
            "gives the key moment results for sample mean and sample variance."
        ),
        why=(
            "2.6.3 supplies the moment hinge before Normal-sample distributional results."
        ),
        benefit="Study Progress for sample-mean/variance moments — not 2.6.4.",
        explain="Campaign Iota Day 3 focuses LO 2.6.3.",
        criteria=[
            "Closed-book, state E[X̄] and Var(X̄) in population terms (CMP form).",
            "State E[S²] (or CMP-equivalent mean of sample variance) warrant.",
            "Refuse treating these moment results as finishing Normal sampling laws / t / F.",
        ],
        tasks=[
            "Sketch μ,σ²,n → E/Var of X̄ and E[S²] before CMP.",
            "Guided Reading through CMP 2.6.3.",
            "Knowledge Checks: moment results + refuse Normal-law swallow.",
        ],
        next_code="2.6",
        next_title="Normal sampling distributions for mean and variance (2.6.4)",
        cont=(
            "Today you related sample-mean and sample-variance moments to the population; "
            "tomorrow continues 2.6 at basic sampling distributions under Normal samples."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.6.4 — titles only tonight",
        student=(
            "Tomorrow: basic Normal sampling distributions for mean and variance (2.6.4). "
            "Optional light prep: skim 2.6.4 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.3 mean/variance of sample mean and mean of sample variance",
        stop="Through CMP 2.6.3 (stop before Normal sampling laws 2.6.4)",
        oos=[
            "Normal sampling distributions as primary (2.6.4)",
            "t-statistic / F primary",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for writing Var(X̄)=σ² without /n.",
            "Watch for confusing E[S²] with σ² without CMP degrees-of-freedom care.",
            "Watch for jumping to t / F as today's primary.",
        ],
        ar_prompt=(
            "Closed-book. (1) State E[X̄] and Var(X̄) for a random sample (CMP form). "
            "(2) State what E[S²] equals (or CMP-equivalent). (3) Which quantities are "
            "population parameters vs sample size?"
        ),
        ar_kw=["mean", "variance", "sample", "mu", "sigma", "n", "E", "Var", "S"],
        ar_model=(
            "Under CMP random-sample conditions: E[X̄]=μ, Var(X̄)=σ²/n (finite variance), and "
            "E[S²]=σ² for the usual unbiased sample variance (as CMP states). μ,σ² are "
            "population; n is sample size."
        ),
        cp_prompt=(
            "Closed-book. Refuse 'I know Var(X̄)=σ²/n so Normal sampling laws and t are done "
            "today.' Restate today's stop."
        ),
        cp_kw=["refuse", "moment", "Normal", "t", "stop", "2.6.3", "2.6.4"],
        cp_model=(
            "Refuse: moment results are not the Normal sampling laws or t/F. Today's stop is "
            "2.6.3; distributional laws under Normal samples come next."
        ),
        reflect="Harvest /n and E[S²] wobble — Normal sampling laws tomorrow.",
    ),
    dict(
        day="CI-D4",
        stem="2.6.4-normal-sample-mean-var-cs1009",
        pid="CS1-EP001-PKG-2.6-NORMAL-SAMPLE-MEAN-VAR",
        lo="2.6.4",
        slug="2.6-normal-sample-mean-var",
        keywords=["Normal", "sampling", "mean", "variance", "chi-square", "distribution"],
        title="State basic Normal sampling distributions for mean and variance",
        purpose=(
            "Today's Mission exists to state basic sampling distributions for the sample mean "
            "and variance for random samples from a Normal distribution — without claiming "
            "the t-statistic (2.6.5) finished."
        ),
        tutor=(
            "Today I will force Normal-sample laws for X̄ and S² (χ² form as CMP) — refuse "
            "treating moment results alone as the distributional laws."
        ),
        edu=(
            "Produce distributional warrants for sample mean and sample variance under "
            "Normal random samples."
        ),
        lo_text=(
            "State basic sampling distributions for the sample mean and variance for random "
            "samples from a normal distribution."
        ),
        focus=(
            "Normal population sample → X̄ Normal · S² related χ² (CMP) → refuse t as today."
        ),
        prior=(
            "Yesterday you expressed E/Var of the sample mean and E of sample variance "
            "(2.6.3). Today specialises to Normal-sample distributional laws."
        ),
        why=(
            "2.6.4 is the distributional hinge before student-t when σ is unknown."
        ),
        benefit="Study Progress for Normal sampling laws — not t; not F.",
        explain="Campaign Iota Day 4 focuses LO 2.6.4.",
        criteria=[
            "Closed-book, state the sampling distribution of X̄ for Normal samples (CMP form).",
            "State the sampling result for sample variance / χ² form as CMP directs.",
            "Refuse treating this LO as having finished the t-statistic.",
        ],
        tasks=[
            "Sketch Normal sample → X̄ / S² laws before CMP.",
            "Guided Reading through CMP 2.6.4.",
            "Knowledge Checks: Normal laws + refuse t swallow.",
        ],
        next_code="2.6",
        next_title="t-statistic for Normal samples (2.6.5)",
        cont=(
            "Today you stated basic Normal sampling distributions for mean and variance; "
            "tomorrow continues 2.6 at the t-statistic."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.6.5 — titles only tonight",
        student=(
            "Tomorrow: t-statistic for random samples from a Normal (2.6.5). Optional light "
            "prep: skim 2.6.5 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.4 Normal sampling distributions for mean and variance",
        stop="Through CMP 2.6.4 (stop before t-statistic 2.6.5)",
        oos=[
            "t-statistic as primary (2.6.5)",
            "F distribution as primary (2.6.6)",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for using t when σ is known / when today only asks Normal laws.",
            "Watch for skipping χ² / variance result the CMP requires.",
            "Watch for CI construction as today's primary.",
        ],
        ar_prompt=(
            "Closed-book. For iid Normal samples (CMP): (1) What is the distribution of X̄? "
            "(2) What sampling result applies to the sample variance (χ² form as CMP)? "
            "(3) Why is this not yet the t-statistic LO?"
        ),
        ar_kw=["Normal", "mean", "variance", "chi", "square", "distribution", "sample"],
        ar_model=(
            "For Normal samples, X̄ is Normal with mean μ and variance σ²/n (CMP). Sample "
            "variance follows a χ²-related law as CMP states. The t-statistic is a separate "
            "LO when σ is replaced by S."
        ),
        cp_prompt=(
            "Closed-book. Refuse 'Normal sampling laws finished the t-statistic.' State "
            "what still sits ahead before the next syllabus topic."
        ),
        cp_kw=["refuse", "t", "Normal", "stop", "2.6.4", "2.6.5"],
        cp_model=(
            "Refuse: Normal X̄/S² laws are not the t-statistic. Stop after 2.6.4; t is tomorrow."
        ),
        reflect="Harvest Normal X̄ vs S² wobble — t-statistic tomorrow.",
    ),
    dict(
        day="CI-D5",
        stem="2.6.5-t-statistic-cs1009",
        pid="CS1-EP001-PKG-2.6-T-STATISTIC",
        lo="2.6.5",
        slug="2.6-t-statistic",
        keywords=["t", "statistic", "Student", "Normal", "sample", "sigma"],
        title="Describe the distribution of the t-statistic for Normal samples",
        purpose=(
            "Today's Mission exists to describe the distribution of the t-statistic for "
            "random samples from a Normal distribution — without claiming the F distribution "
            "(2.6.6) finished."
        ),
        tutor=(
            "Today I will force the candidate through the t construction (unknown σ) — refuse "
            "treating Normal X̄ laws with known σ as having finished t."
        ),
        edu=(
            "Produce the cognitive move from Normal sample with unknown σ to the t-statistic "
            "and its sampling distribution (CMP)."
        ),
        lo_text=(
            "Describe the distribution of the t-statistic for random samples from a normal "
            "distribution."
        ),
        focus=(
            "Normal sample · unknown σ → t = (X̄−μ)/(S/√n) → t distribution (df) → refuse F."
        ),
        prior=(
            "Yesterday you stated Normal sampling distributions for mean and variance "
            "(2.6.4). Today forms the t-statistic when σ is unknown."
        ),
        why=(
            "2.6.5 is contiguous after Normal laws; F for variance ratios waits for day six."
        ),
        benefit="Study Progress for t-statistic — not F; not CI construction as primary.",
        explain="Campaign Iota Day 5 focuses LO 2.6.5.",
        criteria=[
            "Closed-book, write the t-statistic for Normal samples (CMP form).",
            "Name its distribution / degrees of freedom warrant as CMP states.",
            "Refuse treating this as finishing F / Chapter 3 intervals.",
        ],
        tasks=[
            "Sketch unknown-σ → t before CMP.",
            "Guided Reading through CMP 2.6.5.",
            "Knowledge Checks: t construction + refuse F / CI swallow.",
        ],
        next_code="2.6",
        next_title="F distribution for a variance ratio (2.6.6)",
        cont=(
            "Today you described the t-statistic for Normal samples; tomorrow continues 2.6 "
            "at the F distribution for a ratio of sample variances."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.6.6 — titles only tonight",
        student=(
            "Tomorrow: F distribution for the ratio of two sample variances (2.6.6). "
            "Optional light prep: skim 2.6.6 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.5 t-statistic for Normal samples",
        stop="Through CMP 2.6.5 (stop before F distribution 2.6.6)",
        oos=[
            "F distribution as primary (2.6.6)",
            "Confidence intervals / hypothesis tests as primary (3.x)",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for using z when S replaces σ without naming t.",
            "Watch for wrong df.",
            "Watch for jumping to F or CI construction as today's primary.",
        ],
        ar_prompt=(
            "Closed-book. (1) Write the t-statistic for a Normal random sample (CMP). "
            "(2) When do you use t rather than a Normal/z form? (3) What df warrant applies?"
        ),
        ar_kw=["t", "statistic", "S", "sigma", "normal", "df", "n", "mean"],
        ar_model=(
            "t=(X̄−μ)/(S/√n) for Normal samples (CMP). Use t when σ is unknown and estimated "
            "by S. Degrees of freedom follow CMP (typically n−1 for one-sample)."
        ),
        cp_prompt=(
            "Closed-book. Refuse 'The t-statistic finished the F variance-ratio LO "
            "and Chapter 3.' State today's stop."
        ),
        cp_kw=["refuse", "F", "t", "stop", "2.6.5", "3.1", "chapter"],
        cp_model=(
            "Refuse: t is not F and not Chapter 3. Stop after 2.6.5; F is tomorrow; inference "
            "Volumes come later."
        ),
        reflect="Harvest t-vs-z / df wobble — F ratio tomorrow.",
    ),
    dict(
        day="CI-D6",
        stem="2.6.6-f-distribution-cs1009",
        pid="CS1-EP001-PKG-2.6-F-DISTRIBUTION",
        lo="2.6.6",
        slug="2.6-f-distribution",
        keywords=["F", "distribution", "variance", "ratio", "Normal", "independent"],
        title="Describe the F distribution for a ratio of sample variances",
        purpose=(
            "Today's Mission exists to describe the F distribution for the ratio of two "
            "sample variances from independent Normal samples — without claiming Chapter 2 "
            "complete, Chapter 3 inference, or until-exam trust."
        ),
        tutor=(
            "Today I will force the F variance-ratio construction — refuse treating t as "
            "having finished 2.6.6, and refuse Chapter-2-complete claims."
        ),
        edu=(
            "Produce executable warrants for an F ratio of independent sample variances from "
            "Normal populations (CMP)."
        ),
        lo_text=(
            "Describe the F distribution for the ratio of two sample variances from "
            "independent samples taken from normal distributions."
        ),
        focus=(
            "Two independent Normal samples → variance ratio → F (df1, df2) → refuse "
            "Ch2-done / 3.1-done."
        ),
        prior=(
            "Yesterday you described the t-statistic (2.6.5). Today closes topic 2.6 Learning "
            "with the F distribution for a variance ratio."
        ),
        why=(
            "2.6.6 completes topic 2.6 Learning; Revision follows before any 3.1 commission."
        ),
        benefit=(
            "Study Progress for F variance ratio — not 3.1; not Chapter 2 trophy."
        ),
        explain="Campaign Iota Day 6 focuses LO 2.6.6 — terminal Learning day of CS1-009.",
        criteria=[
            "Closed-book, state the F construction for a ratio of sample variances (CMP).",
            "Name independence / Normal-sample conditions and df warrants as CMP states.",
            "Refuse Chapter 2 complete / treating t as having finished 2.6.6.",
        ],
        tasks=[
            "Sketch two-sample variance ratio → F before CMP.",
            "Guided Reading through CMP 2.6.6.",
            "Knowledge Checks: F ratio + refuse Ch2-complete.",
        ],
        next_code="CI-R1",
        next_title="Campaign Iota Revision — retrieve 2.6.1–2.6.6",
        cont=(
            "Today you finished the F distribution for a variance ratio; tomorrow is "
            "Revision mode — retrieve the 2.6 chain closed-book before any 3.1 first-pass work."
        ),
        prep="Optional: list the six 2.6 LO hinges from memory — titles only tonight",
        student=(
            "Tomorrow: Campaign Iota Revision (retrieve 2.6.1–2.6.6). Optional light prep: "
            "list the six hinges from memory — titles only tonight."
        ),
        open="CMP · Syllabus 2.6.6 F distribution for a ratio of sample variances",
        stop="Through CMP 2.6.6 (stop before estimators / inference 3.1)",
        oos=[
            "Estimators and properties (3.1)",
            "Confidence intervals / hypothesis testing primary",
            "Chapter 2 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating t as the variance-ratio tool.",
            "Watch for claiming Chapter 2 / 3.1 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. (1) What ratio has an F distribution in this LO? (2) What sample "
            "conditions are required (independence / Normal as CMP)? (3) What do the two "
            "degrees of freedom refer to?"
        ),
        ar_kw=[
            "F",
            "variance",
            "ratio",
            "independent",
            "Normal",
            "df",
            "sample",
        ],
        ar_model=(
            "Under CMP conditions, a suitably scaled ratio of two independent sample "
            "variances from Normal populations follows an F distribution with two df "
            "parameters tied to the two sample sizes / variance estimators."
        ),
        cp_prompt=(
            "Closed-book. (1) Refuse 'Yesterday's t-statistic already finished the F ratio of "
            "sample variances.' (2) Refuse 'Finishing 2.6.6 means all of Chapter 2 is done.' "
            "Name what still sits ahead before estimators."
        ),
        cp_kw=[
            "refuse",
            "F",
            "t",
            "chapter",
            "complete",
            "3.1",
            "revision",
            "stop",
        ],
        cp_model=(
            "(1) Refuse: t is not the F variance-ratio LO. (2) Refuse: 2.6.6 closes topic 2.6 "
            "Learning, not Chapter 2; next is Revision then honest 3.1 successor — not "
            "spine/until-exam claims."
        ),
        reflect=(
            "Harvest F / df wobble — Revision protects the 2.6 chain tomorrow."
        ),
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
    (PKG_DIR / "revision-sampling-distributions-cs1009.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-IOTA",
        "campaign_version": "cs1009-1.0.0",
        "display_title": "Campaign Iota — Random sampling and sampling distributions (2.6)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-009",
        "prior_volume_id": "CS1-008",
        "day_count": {"learning": 6, "revision": 1, "total": 7},
        "syllabus_span": span,
        "out_of_scope": [
            "3.1+",
            "Chapter 2 complete",
            "Chapter 3 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 8 / remainder / spine re-audit authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

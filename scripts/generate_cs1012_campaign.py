#!/usr/bin/env python3
"""Generate CS1-012 / Campaign Mu educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-mu-cs1012"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1012-campaign-mu-1.0.0",
    "publication_version": "cs1012-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-MU",
    "volume_id": "CS1-012",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1012_EDUCATIONAL_VOLUME.md",
        "CS1012_CERTIFICATION_REPORT.md",
        "EP010_WAVE10_PLAN.md",
    ],
    "author_id": "cs1012-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "3.3",
    "topic_title": "Apply the concepts of hypothesis testing and goodness of fit",
    "topic_id": "CS1-C-T03",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "3.3", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1012-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1012-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1012-cs1-{d['slug']}",
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
                f"for later 3.3 LOs, Chapter 3 trophy, first-pass spine PASS, or until-exam "
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
                "episode_id": f"lep-cs1012-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1012-{lo}-ar-01",
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
                "episode_id": f"lep-cs1012-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1012-{lo}-cp-01",
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
    day = "CM-R1"
    pid = "CS1-EP001-PKG-REV-HYPOTHESIS-TESTING"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Mu revision: hypothesis testing and goodness of fit",
        "return_targets": [
            "3.3.1",
            "3.3.2",
            "3.3.3",
            "3.3.4",
            "3.3.5",
        ],
        "topic_aliases": [day, "campaign-mu-revision"],
        "topic_title_keywords": [
            "revision",
            "hypothesis",
            "null",
            "p-value",
            "power",
            "permutation",
            "chi-square",
            "goodness of fit",
            "contingency",
            "independence",
        ],
        "golden_id": "GOLDEN-CS1012-CS1-CM-R1-HYPOTHESIS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1012-cs1-cm-r1-hypothesis",
            "display_title": "Retrieve hypothesis-testing hinges (3.3)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Mu. Retrieving HT "
                "concepts, basic one-/two-sample and paired tests, permutation tests, "
                "chi-square goodness of fit, and contingency independence. So 3.3 does not "
                "evaporate before an honest stop or remainder-spine successor."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Mu's Learning hinges. "
                "not a passive CMP re-read and not a Chapter 3 trophy or until-exam claim."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: HT concepts "
                "→ basic tests → permutation → chi-square GOF → contingency independence."
            ),
            "learning_objective": (
                "Retrieve and connect (1) HT vocabulary and decision concepts, (2) basic "
                "one-/two-sample and paired tests, (3) permutation non-parametric tests, "
                "(4) chi-square goodness of fit (incl. unknown parameters), and "
                "(5) contingency-table independence tests."
            ),
            "concept_focus": (
                "Campaign chain retrieval: HT concepts → basic tests → permutation → "
                "chi-square GOF → contingency independence."
            ),
            "prior_bridge": (
                "Yesterday you finished contingency independence (3.3.5). Today is Revision "
                "mode: return to 3.3.1–3.3.5 under closed-book retrieval. No new first-pass LO."
            ),
            "why_now": (
                "You've just finished hypothesis testing; spaced retrieval now protects that chain "
                "before you stop."
            ),
            "expected_benefit": (
                "Evidence that the 3.3 chain retrieves. Revision Study Progress, not a claim "
                "that Chapter 3 / the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the five 3.3 Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse Chapter 3 complete / spine / until-exam claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Mu's chain: HT concepts → basic tests → "
                "permutation → chi-square GOF → contingency independence.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 45, "max": 65},
        },
        "session": {
            "session_id": "ssn-cs1012-cs1-cm-r1-hypothesis",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Mu skills. Not to claim Chapter 3 complete."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 45, "max": 65},
            "wrap_up": (
                "Revision Session complete. You stress-tested 3.3.1–3.3.5 return targets. "
                "This is revision Study Progress. Not Topic Complete for Chapter 3, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that hypothesis-testing hinges will still retrieve in "
                "three days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Mu "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the five 3.3 Learning hinges in order?",
                "Can you state type I/II vs p-value vs power, and when chi-square GOF enters?",
                "What claim must you refuse (Chapter 3 complete / spine / until-exam)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 3 / spine / until-exam complete.",
                "Watch for dropping Lambda interval memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not claim Chapter 3 complete, "
                "spine PASS, or until-exam trust in this sitting"
            ),
            "out_of_scope_today": [
                "Chapter 3 complete trophy claim",
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Trust Front absorb (4.x/5.x already LIVE)",
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
                "episode_id": "lep-cs1012-cm-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1012-cm-r1-ar-01",
                "title": "Active Recall: CM-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) HT concepts "
                    "(null/alternative, errors, p-value, power); (2) basic one-/two-sample and "
                    "paired tests; (3) permutation non-parametric tests; (4) chi-square "
                    "goodness of fit; (5) contingency independence."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 3.3.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "hypothesis",
                    "null",
                    "p-value",
                    "power",
                    "test",
                    "permutation",
                    "chi-square",
                    "goodness",
                    "contingency",
                    "independence",
                ],
                "explanation": "Revision retrieves the 3.3 arc.",
                "model_answer": (
                    "Example: (1) HT vocabulary: null/alternative, type I/II, critical "
                    "region, p-value, power; (2) basic Normal/binomial/Poisson and paired "
                    "tests; (3) permutation approach; (4) chi-square GOF incl. unknown "
                    "parameters; (5) contingency table independence test."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Five hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1012-cm-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1012-cm-r1-cp-01",
                "title": "Checkpoint: CM-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest hypothesis-testing link and one "
                    "concrete rework. (2) Refuse: 'A small p-value proves the alternative, so "
                    "Chapter 3 is done.' (3) Name whether you stop here or what syllabus "
                    "topic honestly comes next. Not 'exam ready.'"
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
                    "stop",
                    "remainder",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. permutation test construction. Five-minute rework. (2) Refuse "
                    "Chapter 3 complete / spine / until-exam. (3) Honest next is declared stop "
                    "or remainder-spine successor Volume. Not claimed finished here."
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
            "next_topic_code": "stop",
            "next_topic_title": (
                "Honest next: declared stop / remainder-spine successor (or Wave 0 honesty) "
                ". Not Chapter 3 trophy"
            ),
            "continuity_line": (
                "Campaign Mu / Volume CS1-012 completes after this Revision. Honest stop: "
                "3.3 Pilot Arc closed. Not Chapter 3 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is remainder / spine re-audit under a "
                "later commission (or declared stop)."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight: rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Mu / CS1-012 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await remainder-spine successor Volume. Optional: "
                "schedule your weakest 3.3 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CM-D1",
        stem="3.3.1-hypothesis-concepts-cs1012",
        pid="CS1-EP001-PKG-3.3-HYPOTHESIS-CONCEPTS",
        lo="3.3.1",
        slug="3.3-hypothesis-concepts",
        keywords=[
            "hypothesis",
            "null",
            "alternative",
            "type I",
            "type II",
            "p-value",
            "power",
            "critical region",
        ],
        title="Understand hypothesis-testing concepts (null/alternative, errors, p-value, power)",
        purpose=(
            "Today's Mission exists to establish the conceptual toolkit of hypothesis testing "
            ": null and alternative hypotheses, simple and composite forms, type I and type II "
            "errors, sensitivity and specificity, test statistic, likelihood ratio, critical "
            "region, significance level, p-value, and power. Without pretending basic applied "
            "tests (3.3.2) are finished."
        ),
        tutor=(
            "Today I will force the candidate to name HT decision concepts in CMP language "
            "and refuse treating a cookbook one-sample test as today's LO."
        ),
        edu=(
            "Produce a cognitive move from interval-thinking (3.2) to the hypothesis-testing "
            "decision framework under CMP vocabulary."
        ),
        lo_text=(
            "Understand the concepts of Null and alternative hypotheses, simple and composite "
            "hypotheses, type I and type II errors, sensitivity, specificity, test statistic, "
            "likelihood ratio, critical region, level of significance, probability value and "
            "power of a test."
        ),
        focus=(
            "Null/alternative → errors & operating characteristics → critical region "
            "/ p-value / power → refuse applied-test-as-done."
        ),
        prior=(
            "Campaign Lambda closed confidence and prediction intervals (3.2) with Revision. "
            "Today opens topic 3.3 at LO 3.3.1. The named Continuity Front after CS1-011."
        ),
        why=(
            "3.3.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at hypothesis testing, keeping basic applied tests for the following session."
        ),
        benefit=(
            "You will be able to use HT vocabulary (errors, p-value, power, critical "
            "region) correctly on a concrete vignette."
        ),
        explain=(
            "Day 1 opens 3.3 at the named learning objective. "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, distinguish null vs alternative and type I vs type II errors.",
            "State what a p-value and power claim in CMP-usable form.",
            "Refuse one 'I ran a Normal mean test, so I finished today's LO' claim.",
        ],
        tasks=[
            "Sketch HT decision vocabulary before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.3.1.",
            "Closed-book Knowledge Checks: HT concepts + refuse applied-test swallow.",
        ],
        next_code="3.3",
        next_title="Basic one-/two-sample and paired hypothesis tests (3.3.2)",
        cont=(
            "Today you established hypothesis-testing concepts; tomorrow continues 3.3 at "
            "basic applied tests."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.3.2. Titles only tonight",
        student=(
            "Tomorrow: basic tests (3.3.2). Optional light prep: skim 3.3.2 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.3.1 hypothesis-testing concepts",
        stop=(
            "Through the CMP treatment of Syllabus 3.3.1 "
            "(stop before basic applied tests 3.3.2)"
        ),
        oos=[
            "Basic one-/two-sample / paired tests as primary (3.3.2)",
            "Permutation tests as primary (3.3.3)",
            "Chi-square GOF as primary (3.3.4)",
            "Contingency independence as primary (3.3.5)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating a confidence interval with a hypothesis test.",
            "Watch for starting cookbook Normal/binomial tests (3.3.2) inside this sitting.",
            "Watch for Chapter 3 / spine / until-exam claims.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is a null hypothesis vs an alternative? (2) What is a "
            "type I error vs a type II error? (3) What does a p-value measure, and what is "
            "power? (4) Name one reason a basic applied test is not today's LO."
        ),
        ar_kw=[
            "null",
            "alternative",
            "type I",
            "type II",
            "p-value",
            "power",
            "critical",
            "significance",
        ],
        ar_model=(
            "Null is the statement under test; alternative is the competing claim. Type I is "
            "rejecting a true null; type II is failing to reject a false null. A p-value is "
            "the probability, under the null, of a result at least as extreme as observed; "
            "power is the probability of rejecting a false null. Applied cookbook tests are "
            "tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Disease screening: H₀ = no disease, H₁ = disease present. "
            "(1) Define Type I and Type II errors in this vignette. (2) What does a "
            "p-value measure, and what is power? (3) Refuse: 'I ran a one-sample "
            "Normal mean test in software, so the concepts LO is done.'"
        ),
        cp_kw=["Type I", "Type II", "p-value", "power", "null", "refuse", "critical"],
        cp_model=(
            "(1) Type I: false positive. Declare disease when healthy (reject H₀ "
            "wrongly). Type II: false negative. Miss disease when present (fail to "
            "reject H₀ wrongly). (2) p-value: under H₀, the probability of a result "
            "at least as extreme as observed. Power: P(reject H₀ | H₁ true) = 1 − β. "
            "(3) Refuse: running a cookbook test is not the same as mastering HT "
            "vocabulary (errors, critical region, p-value, power)."
        ),
        reflect="Harvest HT vocabulary wobble. Keep applied tests out of tonight's claim.",
    ),
    dict(
        day="CM-D2",
        stem="3.3.2-basic-tests-cs1012",
        pid="CS1-EP001-PKG-3.3-BASIC-TESTS",
        lo="3.3.2",
        slug="3.3-basic-tests",
        keywords=[
            "test",
            "one-sample",
            "two-sample",
            "paired",
            "normal",
            "binomial",
            "Poisson",
        ],
        title="Apply basic one-sample, two-sample, and paired hypothesis tests",
        purpose=(
            "Today's Mission exists to apply basic hypothesis tests for one-sample and "
            "two-sample situations involving the Normal, binomial, and Poisson distributions, "
            "and basic tests for paired data. Without pretending permutation tests (3.3.3) "
            "are finished."
        ),
        tutor=(
            "Today I will force the candidate to select and apply a basic parametric test "
            "setting and refuse collapsing today's LO into yesterday's vocabulary-only day "
            "or tomorrow's permutation approach."
        ),
        edu=(
            "Produce a cognitive move from HT concepts to executable one-/two-sample and "
            "paired tests under CMP procedures."
        ),
        lo_text=(
            "Use of basic tests for the one-sample and two-sample situations involving the "
            "normal, binomial and Poisson distributions, and apply basic tests for paired data."
        ),
        focus=(
            "Choose setting → apply basic Normal/binomial/Poisson or paired test → "
            "refuse permutation-as-done."
        ),
        prior=(
            "Yesterday you established HT concepts (3.3.1). Today continues topic 3.3 at "
            "LO 3.3.2: basic applied tests."
        ),
        why=(
            "3.3.2 is the contiguous next LO after concepts. Closing it builds usable test "
            "skill before non-parametric permutation methods."
        ),
        benefit=(
            "You will be able to choose and apply a basic Normal, binomial, Poisson, "
            "or paired test for a stated setting."
        ),
        explain=(
            "Day 2 focuses the named learning objective. Contiguity inside topic 3.3."
        ),
        criteria=[
            "Closed-book, name when one-sample vs two-sample vs paired applies.",
            "Sketch a basic Normal or discrete-test move in CMP-usable form.",
            "Refuse one 'permutation finished today's LO' claim.",
        ],
        tasks=[
            "Sketch one-/two-sample/paired decision before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.3.2.",
            "Closed-book Knowledge Checks: basic tests + refuse permutation swallow.",
        ],
        next_code="3.3",
        next_title="Permutation approach to non-parametric hypothesis tests (3.3.3)",
        cont=(
            "Today you applied basic one-/two-sample and paired tests; tomorrow continues "
            "3.3 at permutation tests."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.3.3. Titles only tonight",
        student=(
            "Tomorrow: permutation tests (3.3.3). Optional light prep: skim 3.3.3 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.3.2 basic hypothesis tests",
        stop=(
            "Through the CMP treatment of Syllabus 3.3.2 "
            "(stop before permutation tests 3.3.3)"
        ),
        oos=[
            "Permutation non-parametric tests as primary (3.3.3)",
            "Chi-square GOF as primary (3.3.4)",
            "Contingency independence as primary (3.3.5)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for treating vocabulary-only (3.3.1) as finishing applied tests.",
            "Watch for starting permutation drills (3.3.3) inside this sitting.",
            "Watch for equating paired tests with two-sample independent tests.",
        ],
        ar_prompt=(
            "Closed-book. (1) When do you use a one-sample vs two-sample vs paired test? "
            "(2) Name one Normal and one discrete (binomial or Poisson) basic-test setting. "
            "(3) Name one reason a permutation test is not today's LO."
        ),
        ar_kw=[
            "one-sample",
            "two-sample",
            "paired",
            "normal",
            "binomial",
            "Poisson",
            "test",
            "permutation",
        ],
        ar_model=(
            "One-sample tests a single population parameter; two-sample compares independent "
            "groups; paired uses matched differences. Normal mean tests and binomial/Poisson "
            "tests appear under CMP basic procedures. Permutation is tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. (1) For each setting, name the appropriate basic test "
            "family: (a) one Normal mean with σ known; (b) two independent binomial "
            "proportions; (c) paired Normal differences. (2) Refuse: 'Shuffling "
            "labels for a permutation test finishes the applied basic-tests "
            "requirement.'"
        ),
        cp_kw=["z-test", "proportion", "paired", "Normal", "binomial", "refuse", "permutation"],
        cp_model=(
            "(1) (a) one-sample Normal/z-test for a mean; (b) two-sample proportion "
            "test with Normal approximation; (c) paired test on differences (paired "
            "t/z). (2) Refuse: permutation tests are a different LO; today is basic "
            "parametric tests for Normal / binomial / Poisson / paired settings."
        ),
        reflect="Harvest basic-test selection wobble. Keep permutation out of tonight's claim.",
    ),
    dict(
        day="CM-D3",
        stem="3.3.3-permutation-tests-cs1012",
        pid="CS1-EP001-PKG-3.3-PERMUTATION-TESTS",
        lo="3.3.3",
        slug="3.3-permutation-tests",
        keywords=["permutation", "non-parametric", "shuffle", "null", "test", "resampling"],
        title="Apply the permutation approach to non-parametric hypothesis tests",
        purpose=(
            "Today's Mission exists to apply the permutation approach to non-parametric "
            "hypothesis tests. So exchangeability under the null becomes a usable test "
            "construction. Without pretending chi-square goodness of fit (3.3.4) is finished."
        ),
        tutor=(
            "Today I will force the candidate to state the permutation null mechanism and "
            "refuse treating yesterday's parametric cookbook as finishing today's LO."
        ),
        edu=(
            "Produce a cognitive move from parametric basic tests to permutation "
            "non-parametric hypothesis testing under CMP language."
        ),
        lo_text="The permutation approach to non-parametric hypothesis tests.",
        focus=(
            "Exchangeability under null → permute / reshuffle → reference "
            "distribution → refuse GOF-as-done."
        ),
        prior=(
            "Yesterday you applied basic parametric / paired tests (3.3.2). Today continues "
            "topic 3.3 at LO 3.3.3: permutation."
        ),
        why=(
            "3.3.3 is the contiguous next LO after basic tests. Closing it adds the "
            "non-parametric permutation hinge before chi-square GOF."
        ),
        benefit=(
            "You will be able to outline a permutation test from exchangeability "
            "under H₀ to a reference distribution."
        ),
        explain=(
            "Day 3 focuses the named learning objective. Contiguity inside topic 3.3."
        ),
        criteria=[
            "Closed-book, state what is permuted under the null and why.",
            "Name how a permutation reference distribution supports a decision.",
            "Refuse one 'chi-square GOF finished today's LO' claim.",
        ],
        tasks=[
            "Sketch permute-under-null before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.3.3.",
            "Closed-book Knowledge Checks: permutation + refuse GOF swallow.",
        ],
        next_code="3.3",
        next_title="Chi-square goodness-of-fit test (3.3.4)",
        cont=(
            "Today you applied permutation non-parametric tests; tomorrow continues 3.3 at "
            "chi-square goodness of fit."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.3.4. Titles only tonight",
        student=(
            "Tomorrow: chi-square GOF (3.3.4). Optional light prep: skim 3.3.4 headings. "
            "titles only tonight."
        ),
        open="CMP · Syllabus 3.3.3 permutation hypothesis tests",
        stop=(
            "Through the CMP treatment of Syllabus 3.3.3 "
            "(stop before chi-square GOF 3.3.4)"
        ),
        oos=[
            "Chi-square goodness of fit as primary (3.3.4)",
            "Contingency independence as primary (3.3.5)",
            "Chapter 3 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating bootstrap CI (3.2.8) with permutation HT.",
            "Watch for starting chi-square GOF drills (3.3.4) inside this sitting.",
            "Watch for treating permutation as optional flavour of yesterday's Normal test.",
        ],
        ar_prompt=(
            "Closed-book. (1) What is reshuffled or reassigned under a permutation null? "
            "(2) How does the permutation reference distribution enter the decision? "
            "(3) Name one reason chi-square GOF is not today's LO."
        ),
        ar_kw=[
            "permutation",
            "shuffle",
            "null",
            "reference",
            "non-parametric",
            "exchangeability",
            "chi-square",
        ],
        ar_model=(
            "Under an exchangeability null, labels or assignments are permuted to build a "
            "reference distribution for the test statistic; the observed statistic is compared "
            "to that distribution. Chi-square GOF is tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. Under H₀ of no treatment effect, treatment labels are "
            "exchangeable across units. (1) Outline the permutation test move from "
            "that exchangeability to a decision. (2) Refuse: 'This is just a Normal "
            "two-sample z-test' and 'a chi-square GOF finishes permutation.'"
        ),
        cp_kw=["permutation", "exchangeability", "shuffle", "reference", "null", "refuse", "Normal", "GOF"],
        cp_model=(
            "(1) Shuffle/reassign labels under H₀, recompute the test statistic many "
            "times, and compare the observed statistic to that permutation reference "
            "distribution (tail probability / critical value). (2) Refuse: "
            "permutation builds a null reference from exchangeability, not from a "
            "parametric Normal cookbook; chi-square GOF is a different LO."
        ),
        reflect="Harvest permutation-mechanism wobble. Keep GOF out of tonight's claim.",
    ),
    dict(
        day="CM-D4",
        stem="3.3.4-chi-square-gof-cs1012",
        pid="CS1-EP001-PKG-3.3-CHI-SQUARE-GOF",
        lo="3.3.4",
        slug="3.3-chi-square-gof",
        keywords=[
            "chi-square",
            "goodness of fit",
            "distribution",
            "unknown parameters",
            "degrees of freedom",
        ],
        title="Perform a chi-square goodness-of-fit test (including unknown parameters)",
        purpose=(
            "Today's Mission exists to perform a chi-square test that a random sample is from "
            "a particular distribution, including cases where parameters are unknown. Without "
            "pretending contingency independence (3.3.5) is finished."
        ),
        tutor=(
            "Today I will force the candidate to construct expected frequencies and adjust "
            "degrees of freedom when parameters are estimated, and refuse treating "
            "independence tests as today's LO."
        ),
        edu=(
            "Produce a cognitive move from permutation HT to chi-square goodness-of-fit "
            "assessment under CMP procedures."
        ),
        lo_text=(
            "Chi-square test to test the hypothesis that a random sample is from a particular "
            "distribution, including cases where parameters are unknown."
        ),
        focus=(
            "Hypothesised distribution → expected frequencies → chi-square GOF → DF "
            "adjust if parameters estimated → refuse independence-as-done."
        ),
        prior=(
            "Yesterday you applied permutation tests (3.3.3). Today continues topic 3.3 at "
            "LO 3.3.4: chi-square GOF."
        ),
        why=(
            "3.3.4 is the contiguous next LO after permutation. Closing it adds distributional "
            "GOF before contingency independence."
        ),
        benefit=(
            "You will be able to run a chi-square GOF test, including DF adjustment "
            "when parameters are estimated."
        ),
        explain=(
            "Day 4 focuses the named learning objective. Contiguity inside topic 3.3."
        ),
        criteria=[
            "Closed-book, state the GOF hypothesis and how expected counts arise.",
            "Name what changes when parameters are unknown / estimated.",
            "Refuse one 'contingency independence finished today's LO' claim.",
        ],
        tasks=[
            "Sketch observed vs expected → chi-square GOF before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.3.4.",
            "Closed-book Knowledge Checks: GOF + refuse independence swallow.",
        ],
        next_code="3.3",
        next_title="Contingency tables and chi-square independence (3.3.5)",
        cont=(
            "Today you performed chi-square goodness of fit; tomorrow continues 3.3 at "
            "contingency independence."
        ),
        prep="Optional: glance at CMP headings for Syllabus 3.3.5. Titles only tonight",
        student=(
            "Tomorrow: contingency independence (3.3.5). Optional light prep: skim 3.3.5 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 3.3.4 chi-square goodness of fit",
        stop=(
            "Through the CMP treatment of Syllabus 3.3.4 "
            "(stop before contingency independence 3.3.5)"
        ),
        oos=[
            "Contingency independence as primary (3.3.5)",
            "Chapter 3 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating GOF with a two-way independence test.",
            "Watch for forgetting DF adjustment when parameters are estimated.",
            "Watch for starting contingency drills (3.3.5) inside this sitting.",
        ],
        ar_prompt=(
            "Closed-book. (1) What hypothesis does a chi-square GOF test? (2) How do expected "
            "frequencies arise? (3) What changes when parameters are unknown? (4) Name one "
            "reason contingency independence is not today's LO."
        ),
        ar_kw=[
            "chi-square",
            "goodness",
            "fit",
            "expected",
            "parameters",
            "degrees",
            "contingency",
        ],
        ar_model=(
            "GOF tests whether a sample is consistent with a stated distribution. Expected "
            "counts come from the hypothesised probabilities (and sample size). Unknown "
            "parameters are estimated and DF adjusted under CMP rules. Independence is "
            "tomorrow's LO."
        ),
        cp_prompt=(
            "Closed-book. You test whether claim counts follow a Poisson "
            "distribution; λ is estimated from the same sample. (1) How are expected "
            "frequencies formed, and what happens to degrees of freedom when λ is "
            "estimated? (2) Refuse: 'A chi-square test of independence in a two-way "
            "table finishes GOF.'"
        ),
        cp_kw=["GOF", "expected", "degrees of freedom", "estimated", "Poisson", "refuse", "independence"],
        cp_model=(
            "(1) Expected frequencies = n × fitted Poisson probabilities using λ̂; "
            "DF = (number of bins − 1 − number of estimated parameters), so subtract "
            "1 for λ̂. (2) Refuse: independence in a contingency table is a "
            "different LO from one-sample GOF to a named distribution."
        ),
        reflect="Harvest GOF / DF wobble. Keep contingency out of tonight's claim.",
    ),
    dict(
        day="CM-D5",
        stem="3.3.5-contingency-independence-cs1012",
        pid="CS1-EP001-PKG-3.3-CONTINGENCY-INDEPENDENCE",
        lo="3.3.5",
        slug="3.3-contingency-independence",
        keywords=[
            "contingency",
            "two-way",
            "independence",
            "chi-square",
            "classification",
        ],
        title="Use contingency tables and chi-square tests of independence",
        purpose=(
            "Today's Mission exists to use a contingency (two-way) table and a chi-square "
            "test of independence for two classification criteria. Completing the 3.3 "
            "Learning span. Without pretending Chapter 3 / spine / until-exam trust are done."
        ),
        tutor=(
            "Today I will force the candidate to form a two-way table and test independence, "
            "and refuse Chapter 3 complete / spine / until-exam claims."
        ),
        edu=(
            "Produce a cognitive move from distributional GOF to contingency-table "
            "independence testing under CMP procedures."
        ),
        lo_text=(
            "A contingency (or two-way) table, and use of a chi-square test to test the "
            "independence of two classification criteria."
        ),
        focus=(
            "Two-way table → independence null → chi-square independence → refuse "
            "GOF-as-independence."
        ),
        prior=(
            "Yesterday you performed chi-square GOF (3.3.4). Today completes topic 3.3 "
            "Learning at LO 3.3.5: contingency independence."
        ),
        why=(
            "Finish topic 3.3 with contingency tables and chi-square independence tests. Then revise the hypothesis-testing chain."
        ),
        benefit=(
            "You'll be able to read a contingency table and run a chi-square test of "
            "independence with the right hypotheses."
        ),
        explain=(
            "Day 5 focuses the named learning objective. Finishes 3.3 "
            "Learning LOs before Revision."
        ),
        criteria=[
            "Closed-book, state the independence null for two classification criteria.",
            "Sketch how expected cell counts arise in a two-way table.",
            "Refuse one 'Chapter 3 / spine / until-exam finished' claim.",
        ],
        tasks=[
            "Sketch two-way table → independence test before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 3.3.5.",
            "Closed-book Knowledge Checks: independence + refuse Chapter 3 / spine swallow.",
        ],
        next_code="CM-R1",
        next_title="Campaign Mu Revision: retrieve 3.3 hinges",
        cont=(
            "Today you used contingency independence tests; tomorrow is Revision. Retrieve "
            "the 3.3 chain closed-book (not Chapter 3 trophy)."
        ),
        prep="Optional: list the five 3.3 LO codes from memory. Titles only tonight",
        student=(
            "Tomorrow: CM-R1 Revision (retrieve 3.3.1–3.3.5). Optional light prep: list the "
            "five LO codes from memory. Titles only tonight."
        ),
        open="CMP · Syllabus 3.3.5 contingency tables and independence",
        stop=(
            "Through the CMP treatment of Syllabus 3.3.5 "
            "(stop before Chapter 3 trophy / remainder / spine claims)"
        ),
        oos=[
            "Chapter 3 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Trust Front absorb (4.x/5.x already LIVE)",
            "Remainder / spine re-audit authoring",
        ],
        misconceptions=[
            "Watch for equating GOF (3.3.4) with independence in a two-way table.",
            "Watch for claiming Chapter 3 / spine / until-exam complete after one LO.",
            "Watch for absorbing Trust Front regression/Bayesian credit as Continuity Front.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does a contingency table classify? (2) What is the "
            "independence null? (3) How do expected cell counts arise? (4) Name one reason "
            "this does not finish Chapter 3 or the first-pass spine."
        ),
        ar_kw=[
            "contingency",
            "two-way",
            "independence",
            "chi-square",
            "expected",
            "classification",
            "chapter",
        ],
        ar_model=(
            "A two-way table cross-classifies two criteria. Independence says row and column "
            "factors do not associate; expected counts use marginal structure under CMP. "
            "One LO does not finish Chapter 3 or first-pass spine PASS."
        ),
        cp_prompt=(
            "Closed-book. Two-way table: rating class × claim/no-claim. (1) State "
            "the independence null and how expected cell counts are formed. (2) "
            "Refuse: 'This is the same as a chi-square GOF to a named distribution.'"
        ),
        cp_kw=["independence", "contingency", "expected", "row", "column", "refuse", "GOF"],
        cp_model=(
            "(1) H₀: row and column classifications are independent; E_{ij} = (row i "
            "total × column j total) / n. (2) Refuse: GOF tests whether one sample "
            "follows a named distribution; independence tests association between "
            "two classification criteria in a two-way table."
        ),
        reflect=(
            "Harvest independence / expected-count wobble. Revision protects the 3.3 chain "
            "tomorrow."
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
    (PKG_DIR / "revision-hypothesis-testing-cs1012.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-MU",
        "campaign_version": "cs1012-1.0.0",
        "display_title": "Campaign Mu: Hypothesis testing and goodness of fit (3.3)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-012",
        "prior_volume_id": "CS1-011",
        "day_count": {"learning": 5, "revision": 1, "total": 6},
        "syllabus_span": span,
        "out_of_scope": [
            "Chapter 3 complete trophy",
            "first-pass spine",
            "until-examination educational trust",
            "Trust Front absorb (4.x/5.x already LIVE)",
            "Wave 11 / remainder / spine re-audit authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

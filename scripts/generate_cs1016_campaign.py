#!/usr/bin/env python3
"""Generate CS1-016 / Campaign Pi educational packages (catalogue only).

Memory Front / spine re-audit Pilot Arc after Topic 5.1 Continuity Front tip close.
Hinge Learning LOs are already Published via Gamma→Omicron — Pi uses distinct
CP-prefixed package IDs and must not be copied to educational_packages/ in this cycle.
Published Coverage and Student Reliance are unchanged by catalogue authoring.
Wave 0 Alpha/Beta Approver honesty gap is scheduled residual — not cleared.
"""
from __future__ import annotations

import json
from pathlib import Path

from _mcq_batch1_section3_payload import apply_mcq_overlay

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-pi-cs1016"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1016-campaign-pi-1.0.0",
    "publication_version": "cs1016-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-PI",
    "volume_id": "CS1-016",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1016_EDUCATIONAL_VOLUME.md",
        "CS1016_CERTIFICATION_REPORT.md",
        "EP014_WAVE14_PLAN.md",
    ],
    "author_id": "cs1016-educational-author",
    "authored_at": "2026-08-04",
    "front_class": "memory_front_spine_reaudit",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_code": d["topic_code"],
        "topic_title": d["topic_title"],
        "topic_focus_lo": lo,
        "topic_aliases": [d["topic_code"], lo, "memory-front-pi"],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1016-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1016-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1016-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Memory Front Mission for Syllabus {lo}: retrieval under "
                "spine re-audit discipline, not a new first-pass LO discovery claim."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo} retrieval, exit to CMP, retrieve today's hinge, refuse "
                "spine PASS / until-exam / Wave 0 clearance swallow."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo} under Memory Front discipline. This is Study Progress for "
                "today's hinge. Not first-pass spine PASS, until-exam trust, or Wave 0 "
                "Approver honesty clearance."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} hinge closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to retrieve Syllabus {lo}–"
                f"{d['title'].lower()}: under Memory Front / spine re-audit discipline. "
                "Stop before out-of-scope later hinges as primary."
            ),
            "focus_questions": [
                f"What is the core retrieval move of Syllabus {lo}?",
                "What warrant separates today's hinge from the next Memory Front day?",
                "What claim must you refuse today (spine / until-exam / Wave 0)?",
                "What will you practise in Knowledge Checks after the CMP?",
            ],
            "misconception_watch": d["misconceptions"],
            "open_point": d["open"],
            "stop_condition": d["stop"],
            "out_of_scope_today": d["oos"],
            "annotation_task": "Before deep reading: sketch today's hinge chain in notes",
            "attempt_before_reveal": (
                "At the first worked example, cover the answer and attempt the middle step"
            ),
            "worked_examples_cue": (
                "Worked-example re-entry (CMP closed): attempt the hinge step before uncovering "
                f"the solution: stay inside {lo}."
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
                    "cue": "Pause. Write today's core retrieval move in one sentence.",
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
                "episode_id": f"lep-cs1016-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1016-{lo}-ar-01",
                "title": f"Active Recall: {lo}",
                "prompt": d["ar_prompt"],
                "response_type": "short_structured",
                "body": f"Retrieve {lo} closed-book under Memory Front discipline.",
                "hints": ["Use CMP language from today's notes.", "Stay inside today's LO."],
                "accepted_keywords": d["ar_kw"],
                "explanation": f"Active recall for {lo}.",
                "model_answer": d["ar_model"],
                "common_mistake": "Skipping the LO hinge or claiming spine / until-exam complete.",
                "success_criteria": ["Addresses the prompt structure.", "Stays inside today's LO."],
            },
            {
                "episode_id": f"lep-cs1016-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1016-{lo}-cp-01",
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
                f"Which part of today's {lo} retrieval is stickiest and why? Quote or paraphrase "
                "the single CMP cue still unclear. If you had five minutes tomorrow, what one "
                "move would you rework?"
            ),
            "prompts": [
                f"Which part of {lo} retrieval is stickiest and why?",
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
        "revision_linkage": {
            "returns_on": "CP-R1",
            "campaign_revision_package": "CS1-EP001-PKG-REV-SPINE-MEMORY-PI",
            "note": f"Syllabus {lo} is a CP-R1 return target after Memory Front Learning span closes.",
        },
    }


def revision_pkg() -> dict:
    day = "CP-R1"
    pid = "CS1-EP001-PKG-REV-SPINE-MEMORY-PI"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Pi revision: Memory Front spine hinges",
        "return_targets": [
            "2.1.3",
            "2.2.1",
            "2.5.1",
            "2.6.1",
            "3.1.1",
            "3.2.1",
            "3.3.1",
            "4.1.1",
            "5.1.1",
        ],
        "topic_aliases": [day, "campaign-pi-revision", "memory-front"],
        "topic_title_keywords": [
            "revision",
            "memory",
            "spine",
            "continuity",
            "retrieval",
        ],
        "golden_id": "GOLDEN-CS1016-CS1-CP-R1-SPINE-MEMORY",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1016-cs1-cp-r1-spine-memory",
            "display_title": "Retrieve Memory Front spine hinges",
            "mission_purpose": (
                "Today's Mission exists to protect memory across Campaign Pi. Retrieving "
                "2.1.3 through 5.1.1 hinges. So Continuity Front tip closure does not "
                "evaporate into until-exam theatre or Wave 0 clearance claims."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Pi's Learning hinges. "
                "not a passive CMP re-read and not a first-pass spine PASS or until-exam claim."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: "
                "2.1.3 → 2.2.1 → 2.5.1 → 2.6.1 → 3.1.1 → 3.2.1 → 3.3.1 → 4.1.1 → 5.1.1."
            ),
            "learning_objective": (
                "Retrieve and connect Memory Front hinges (1) probabilities/quantiles, "
                "(2) marginal/conditional, (3) CLT, (4) random samples, (5) estimators, "
                "(6) CI from sample, (7) hypothesis testing, (8) linear regression entry, "
                "and (9) Bayes' theorem tip."
            ),
            "concept_focus": (
                "Quantiles → joints → CLT → sampling → estimators → intervals → tests → regression → Bayes tip retrieval."
            ),
            "prior_bridge": (
                "Yesterday you finished Bayes' theorem tip retrieval (5.1.1). Today is Revision "
                "mode: return to CP hinges under closed-book retrieval. No new first-pass LO."
            ),
            "why_now": (
                "Space a closed-book retrieval across the memory chain (quantiles through Bayes tip)"
                "before you stop."
            ),
            "expected_benefit": (
                "You'll confirm the memory chain still retrieves closed-book. From quantiles through Bayes tip."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, name the nine CP Learning hinges in order (short phrases).",
                "State at least one concrete weakest link with a rework plan.",
                "Refuse treating one retrieval sitting as Topic mastery.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Pi's hinge chain from 2.1.3 to 5.1.1.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 50, "max": 75},
        },
        "session": {
            "session_id": "ssn-cs1016-cs1-cp-r1-spine-memory",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Pi Memory Front skills. Not to claim spine PASS."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link. Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 50, "max": 75},
            "wrap_up": (
                "Revision Session complete. You stress-tested CP hinge return targets. "
                "This is revision Study Progress. Not first-pass spine PASS, not until-exam "
                "trust, and not Wave 0 Approver honesty clearance."
            ),
            "confidence_prompt": (
                "How confident are you that Memory Front hinges will still retrieve in three days? "
                "Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Pi "
                "Memory Front chain without opening a new CMP chapter first. Attempt "
                "closed-book retrieval; only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you name the nine CP Learning hinges in order?",
                "Can you state 2.1.3 → 2.2.1 → 2.5.1 → 2.6.1 → 3.1.1 → 3.2.1 → 3.3.1 → 4.1.1 → 5.1.1?",
                "What claim must you refuse (spine / until-exam / Wave 0 clearance)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming spine / until-exam / Wave 0 complete.",
                "Watch for inventing Topic 5.2 as Continuity Front geography.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection. Do not claim spine PASS, "
                "until-exam trust, or Wave 0 clearance in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Wave 0 Approver honesty clearance",
                "Certified Educational Coverage increase from catalogue alone",
                "Topic 5.2 invention",
                "New first-pass LO beyond Memory Front hinges",
            ],
            "annotation_task": "Before checks: sketch return-target chain from memory",
            "attempt_before_reveal": "Attempt each check before any targeted CMP reopen",
            "worked_examples_cue": (
                "Revision worked re-entry: attempt the failed hinge closed-book before "
                "targeted CMP reopen."
            ),
            "exit_line": (
                "Keep the CMP closed to begin. Attempt closed-book retrieval of the Campaign Pi "
                "hinge chain. Only after a failed check may you reopen the exact failed locus "
                "in the CMP. Stop after checks and Reflection. Refuse spine PASS, until-exam "
                "trust, and Wave 0 clearance claims."
            ),
            "return_cue": (
                "You are finished when return-target checks and Reflection are complete. "
                "Immediate next: honest stop / Wave 0 Approver residual. Not until-exam trust."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause. List the nine hinges from memory before any CMP reopen.",
                    "student_action": "Retrieve",
                },
                {
                    "id": "PP2",
                    "cue": "Name one claim you must refuse today.",
                    "student_action": "Refuse",
                },
            ],
            "reentry_line": (
                "Welcome back. Keep CMP closed unless a targeted failed-locus reopen is required."
            ),
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1016-cp-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1016-cp-r1-ar-01",
                "title": "Active Recall: Memory Front hinges",
                "prompt": (
                    "Closed-book. (1) Name the nine CP Learning hinges in order. "
                    "(2) Name your weakest link. (3) Name one reason this does not finish "
                    "first-pass spine PASS or until-exam trust."
                ),
                "response_type": "short_structured",
                "body": "Retrieve the Memory Front hinge chain.",
                "hints": ["2.1.3 starts the chain.", "5.1.1 is the tip hinge."],
                "accepted_keywords": [
                    "2.1.3",
                    "2.2.1",
                    "2.5.1",
                    "2.6.1",
                    "3.1.1",
                    "3.2.1",
                    "3.3.1",
                    "4.1.1",
                    "5.1.1",
                ],
                "explanation": "Active recall for CP-R1.",
                "model_answer": (
                    "Hinges: 2.1.3 → 2.2.1 → 2.5.1 → 2.6.1 → 3.1.1 → 3.2.1 → 3.3.1 → 4.1.1 → "
                    "5.1.1. Weakest link is personal. Spine PASS / until-exam remain out of scope."
                ),
                "common_mistake": "Claiming spine or until-exam complete from Revision day.",
                "success_criteria": ["Nine hinges named.", "Weakest link named.", "Refusal present."],
            },
            {
                "episode_id": "lep-cs1016-cp-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1016-cp-r1-cp-01",
                "title": "Checkpoint: memory-chain revision honesty",
                "prompt": (
                    "Closed-book. A colleague says 'If I can recite Bayes' theorem, the whole "
                    "chain from quantiles through regression is secure.' Refuse; name the "
                    "weakest link on today's retrieval chain; name one concrete residual to "
                    "rework."
                ),
                "response_type": "short_structured",
                "body": "Checkpoint refuse for CP-R1.",
                "hints": ["Name Wave 0 Approver residual.", "Refuse until-exam."],
                "accepted_keywords": ["refuse", "spine", "Wave 0", "until-exam"],
                "explanation": "Checkpoint for CP-R1.",
                "model_answer": (
                    "Refuse: Memory Front Revision ≠ first-pass spine PASS, ≠ Wave 0 Approver "
                    "clearance, ≠ until-exam trust. Honest residual: Wave 0 Approver ownership "
                    "remains scheduled; until-exam blocked."
                ),
                "common_mistake": "Accepting the forbidden claim.",
                "success_criteria": ["Refusal present.", "Honest residual named."],
            },
        ],
        "reflection": {
            "framing": "Harvest Memory Front wobble: Wave 0 Approver residual remains open.",
            "prompt": (
                "Which hinge retrieved least cleanly today. Quantiles, joints, CLT, sampling, "
                "estimators, intervals, tests, regression roles, or Bayes tip. And why? "
                "What one concrete rework will you schedule? Do not claim the full syllabus "
                "stretch is finished because one retrieval sitting went well."
            ),
            "prompts": [
                "Which Memory Front hinge is stickiest and why?",
                "What one rework plan will you keep?",
                "What claim must you refuse after Revision?",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "WAVE0",
            "next_topic_title": "Honest stop / Wave 0 Approver residual (not cleared)",
            "continuity_line": (
                "Today you closed Campaign Pi Revision; next is an honest stop with Wave 0 "
                "Approver ownership still scheduled. Not until-exam trust."
            ),
            "light_prep_cue": "No new LO tonight: rest or jot the stickiest Memory Front hinge",
            "student_facing": (
                "Honest next: stop / Wave 0 Approver residual. Do not claim first-pass spine "
                "PASS or until-exam trust from Pi catalogue alone."
            ),
        },
        "revision_linkage": {
            "returns_on": "CP-R1",
            "campaign_revision_package": pid,
            "note": "Terminal Revision for Campaign Pi Memory Front hinge chain.",
        },
    }


LEARNING = [
    dict(
        day="CP-D1",
        stem="2.1.3-prob-quantiles-cs1016",
        pid="CS1-EP001-PKG-CP-2.1-PROB-QUANTILES",
        lo="2.1.3",
        topic_code="2.1",
        topic_title="Understand the characteristics of basic univariate distributions and how to generate samples from them",
        slug="2.1-prob-quantiles",
        keywords=["probability", "quantile", "univariate", "memory"],
        title="Retrieve probabilities and quantiles (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 2.1.3 probability/quantile skill under Memory Front discipline after Continuity Front tip close. Without pretending joint distributions (2.2.1) are finished.",
        tutor="Today I will force closed-book probability/quantile retrieval and refuse 'Memory Front finished joint distributions / spine PASS'.",
        edu="Produce Memory Front retrieval of probabilities and quantiles as the lawful first hinge after Topic 5.1 tip close.",
        lo_text="Evaluate probabilities and quantiles associated with univariate distributions (by calculation or using statistical software as appropriate).",
        focus=(
            """Named univariate family → probability or quantile evaluation (tables/software/calculation) → refuse recognition-as-evaluation."""
        ),
        prior="Yesterday you closed Campaign Omicron Revision at the Continuity Front tip (5.1). Today opens Memory Front / spine re-audit at the historical Opening Continuity Front hinge 2.1.3.",
        why="Topic 5.1 is closed and there is no 5.2 next. Retrieve probability and quantile evaluation from earlier distribution work.",
        benefit=(
            """You'll retrieve how to evaluate a probability and a quantile for a placed univariate family from memory."""
        ),
        explain="Day 1 focuses the named learning objective. After tip close begins at the Opening hinge already Published via Gamma.",
        criteria=["Closed-book, outline one probability and one quantile move for a named univariate distribution.", "State why this is retrieval not new first-pass discovery theatre.", "Refuse one joint-distributions / spine swallow."],
        tasks=["Sketch probability/quantile path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 2.1.3.", "Closed-book Knowledge Checks: retrieval + refuse swallow."],
        next_code="2.2",
        next_title="Marginal and conditional distributions (2.2.1)",
        cont="Today you retrieved 2.1.3; tomorrow continues Memory Front at 2.2.1.",
        prep="Optional: glance at CMP headings for Syllabus 2.2.1. Titles only tonight",
        student="Tomorrow: marginal/conditional Memory Front hinge (2.2.1). Optional light prep: skim 2.2.1 headings. Titles only tonight.",
        open="CMP · Syllabus 2.1.3 probabilities and quantiles",
        stop="Through the CMP treatment of Syllabus 2.1.3 (stop before joint distributions primary 2.2.1)",
        oos=["Joint distributions as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for treating Memory Front as rewriting first-pass discovery.", "Watch for swallowing 2.2.1 today.", "Watch for claiming spine PASS from one hinge."],
        ar_prompt="Closed-book. (1) What probability object do you evaluate for a univariate distribution? (2) What is a quantile move? (3) Why is 2.2.1 not today's primary?",
        ar_kw=["probability", "quantile", "univariate", "distribution"],
        ar_model="Evaluate probabilities and quantiles for named univariate distributions. Joint distributions open tomorrow under Memory Front.",
        cp_prompt=(
            """Closed-book. Claim sizes ~ Exponential with mean θ = 1000. (1) Compute P(X > 2000). (2) Compute the 90th percentile of X (leave exact form or a one-decimal numerical value). (3) Refuse: 'I recognise it is Exponential, so evaluation is finished without computing.'"""
        ),
        cp_kw=["probability", "quantile", "exponential", "percentile", "refuse", "evaluate"],
        cp_model=(
            """(1) P(X > 2000) = e^{-2000/1000} = e^{-2} ≈ 0.135. (2) Solve 1 − e^{-x/1000} = 0.9 ⇒ x = 1000 ln(10) ≈ 2302.6. (3) Refuse: naming the family is not the evaluation. You still must compute the probability or quantile."""
        ),
        reflect="Harvest probability/quantile wobble: joint distributions continue Memory Front tomorrow.",
    ),
    dict(
        day="CP-D2",
        stem="2.2.1-marginal-conditional-cs1016",
        pid="CS1-EP001-PKG-CP-2.2-MARGINAL-CONDITIONAL",
        lo="2.2.1",
        topic_code="2.2",
        topic_title="Understand jointly distributed random variables",
        slug="2.2-marginal-conditional",
        keywords=["marginal", "conditional", "joint", "memory"],
        title="Retrieve marginal and conditional distributions (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 2.2.1 marginal/conditional skill under Memory Front discipline. Without pretending CLT (2.5.1) is finished.",
        tutor="Today I will force marginal/conditional retrieval and refuse 'Memory Front finished CLT / spine PASS'.",
        edu="Produce Memory Front retrieval of marginal and conditional distributions contiguous after 2.1.3.",
        lo_text="Obtain the probability function or density function for marginal and conditional distributions of jointly distributed random variables.",
        focus="Joint \u2192 marginal (sum/integrate) \u2192 conditional (normalise) \u2192 refuse joint-as-margins-done.",
        prior="Yesterday you retrieved probabilities/quantiles (2.1.3). Today continues Memory Front at joint entry.",
        why="Keep Chapter 2 alive: retrieve how to form marginals and conditionals from a joint distribution.",
        benefit=(
            """You'll retrieve how to obtain a marginal and a conditional from a joint distribution by actual extraction, not by recognition alone."""
        ),
        explain="Day 2 focuses the named learning objective. Preserves joint-entry hinge after retrieval.",
        criteria=["Closed-book, distinguish marginal vs conditional in one sentence each.", "State one joint-to-marginal move.", "Refuse one CLT / spine swallow."],
        tasks=["Sketch marginal/conditional path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 2.2.1.", "Closed-book Knowledge Checks."],
        next_code="2.5",
        next_title="Central limit theorem (2.5.1)",
        cont="Today you retrieved 2.2.1; tomorrow continues Memory Front at 2.5.1.",
        prep="Optional: glance at CMP headings for Syllabus 2.5.1. Titles only tonight",
        student="Tomorrow: CLT Memory Front hinge (2.5.1). Optional light prep: skim 2.5.1 headings. Titles only tonight.",
        open="CMP · Syllabus 2.2.1 marginal and conditional distributions",
        stop="Through the CMP treatment of Syllabus 2.2.1 (stop before CLT primary 2.5.1)",
        oos=["CLT as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for equating marginal with conditional.", "Watch for swallowing CLT today.", "Watch for claiming Chapter 2 complete."],
        ar_prompt="Closed-book. (1) How do you obtain a marginal from a joint? (2) What changes for a conditional? (3) Why is CLT not today's primary?",
        ar_kw=["marginal", "conditional", "joint", "density"],
        ar_model="Marginals integrate/sum out other variables; conditionals renormalise on a condition. CLT is tomorrow.",
        cp_prompt=(
            """Closed-book. Joint PMF of (X, Y):
  P(0,0)=0.10, P(0,1)=0.20, P(1,0)=0.30, P(1,1)=0.40.
(1) Compute the marginal P(X=1). (2) Compute P(Y=1 | X=1). (3) Refuse: 'We have the joint table, so marginals and conditionals are optional decoration.'"""
        ),
        cp_kw=["marginal", "conditional", "joint", "sum", "normalise", "refuse"],
        cp_model=(
            """(1) P(X=1) = 0.30 + 0.40 = 0.70. (2) P(Y=1 | X=1) = 0.40 / 0.70 ≈ 0.571. (3) Refuse: the joint is not the same as its margins or conditionals. You must sum for the marginal and divide by that marginal for the conditional."""
        ),
        reflect="Harvest joint-entry wobble. CLT continues Memory Front tomorrow.",
    ),
    dict(
        day="CP-D3",
        stem="2.5.1-clt-cs1016",
        pid="CS1-EP001-PKG-CP-2.5-CLT",
        lo="2.5.1",
        topic_code="2.5",
        topic_title="Central limit theorem",
        slug="2.5-clt",
        keywords=["CLT", "central", "limit", "memory"],
        title="Retrieve the central limit theorem (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 2.5.1 CLT under Memory Front discipline. Without pretending random-sample foundations (2.6.1) are finished.",
        tutor="Today I will force CLT retrieval and refuse 'Memory Front finished sampling / spine PASS'.",
        edu="Produce Memory Front retrieval of CLT contiguous in the hinge chain.",
        lo_text="Apply the central limit theorem for a sequence of independent, identically distributed random variables.",
        focus=(
            """IID sequence → standardised sample mean → Normal limit under CLT conditions → refuse Normal-everywhere-without-CLT."""
        ),
        prior="Yesterday you retrieved marginal/conditional (2.2.1). Today continues Memory Front at CLT.",
        why="CLT is a high-decay hinge between distributions and sampling/inference.",
        benefit=(
            """You'll retrieve how to apply the CLT to approximate a probability for a sample mean from an iid sequence."""
        ),
        explain="Day 3 focuses the named learning objective. Protects CLT before sampling foundations.",
        criteria=["Closed-book, state CLT for an IID sequence in one careful sentence.", "Name one condition you must not drop.", "Refuse one sampling / spine swallow."],
        tasks=["Sketch CLT path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 2.5.1.", "Closed-book Knowledge Checks."],
        next_code="2.6",
        next_title="Random samples (2.6.1)",
        cont="Today you retrieved 2.5.1; tomorrow continues Memory Front at 2.6.1.",
        prep="Optional: glance at CMP headings for Syllabus 2.6.1. Titles only tonight",
        student="Tomorrow: random samples Memory Front hinge (2.6.1). Optional light prep: skim 2.6.1 headings. Titles only tonight.",
        open="CMP · Syllabus 2.5.1 central limit theorem",
        stop="Through the CMP treatment of Syllabus 2.5.1 (stop before random samples primary 2.6.1)",
        oos=["Random samples as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for dropping IID conditions.", "Watch for swallowing sampling foundations today.", "Watch for claiming inference complete."],
        ar_prompt="Closed-book. (1) State CLT for an IID sequence. (2) What does it approximate? (3) Why is 2.6.1 not today's primary?",
        ar_kw=["CLT", "IID", "approximate", "normal"],
        ar_model="For IID with finite mean/variance, sample-mean distributions approach Normal under CLT conditions. Sampling foundations open tomorrow.",
        cp_prompt=(
            """Closed-book. Claim sizes are iid with mean μ = 500 and sd σ = 200; n = 100. Using the CLT, approximate P(X̄ > 540). (1) State the approximate distribution of X̄. (2) Compute the standardised z and the approximate probability (use Φ(2) ≈ 0.977). (3) Refuse: 'We already use the Normal all the time, so the CLT is just common sense and needs no statement.'"""
        ),
        cp_kw=["CLT", "iid", "sample mean", "Normal", "standardise", "refuse"],
        cp_model=(
            """(1) X̄ ≈ Normal(μ=500, sd=σ/√n=20). (2) z = (540 − 500) / 20 = 2; P(X̄ > 540) ≈ 1 − Φ(2) ≈ 0.023. (3) Refuse: casual Normal habit is not the CLT. Today's skill is stating and applying the theorem for iid sequences under the stated conditions."""
        ),
        reflect="Harvest CLT wobble: random samples continue Memory Front tomorrow.",
    ),
    dict(
        day="CP-D4",
        stem="2.6.1-random-samples-cs1016",
        pid="CS1-EP001-PKG-CP-2.6-RANDOM-SAMPLES",
        lo="2.6.1",
        topic_code="2.6",
        topic_title="Random sampling and sampling distributions",
        slug="2.6-random-samples",
        keywords=["sample", "population", "sampling", "memory"],
        title="Retrieve random samples foundations (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 2.6.1 random-sample foundations under Memory Front discipline. Without pretending estimators (3.1.1) are finished.",
        tutor="Today I will force random-sample retrieval and refuse 'Memory Front finished estimators / spine PASS'.",
        edu="Produce Memory Front retrieval of random samples as the bridge into inference hinges.",
        lo_text="Explain random samples from a population and the role of sampling as the bridge into inference.",
        focus="Population \u2192 random sample (iid / CMP sampling warrant) \u2192 refuse n-observations-as-random-sample.",
        prior="Yesterday you retrieved CLT (2.5.1). Today continues Memory Front at sampling foundations.",
        why="Sampling vocabulary must retrieve before estimator and CI hinges.",
        benefit=(
            """You'll retrieve what a random sample from a population requires and why a pile of observations is not automatically one."""
        ),
        explain="Day 4 focuses the named learning objective. Places sampling before inference hinges.",
        criteria=["Closed-book, define a random sample from a population.", "State why sampling precedes estimators in the hinge chain.", "Refuse one estimators / spine swallow."],
        tasks=["Sketch sample/population path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 2.6.1.", "Closed-book Knowledge Checks."],
        next_code="3.1",
        next_title="Estimators: method of moments (3.1.1)",
        cont="Today you retrieved 2.6.1; tomorrow continues Memory Front at 3.1.1.",
        prep="Optional: glance at CMP headings for Syllabus 3.1.1. Titles only tonight",
        student="Tomorrow: estimators Memory Front hinge (3.1.1). Optional light prep: skim 3.1.1 headings. Titles only tonight.",
        open="CMP · Syllabus 2.6.1 random samples from a population",
        stop="Through the CMP treatment of Syllabus 2.6.1 (stop before estimators primary 3.1.1)",
        oos=["Estimators as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for equating sample with population.", "Watch for swallowing estimators today.", "Watch for claiming Chapter 2 complete."],
        ar_prompt="Closed-book. (1) What is a random sample from a population? (2) Why does sampling precede estimators? (3) Why is 3.1.1 not today's primary?",
        ar_kw=["sample", "population", "random", "inference"],
        ar_model="A random sample is drawn from a population under a sampling model. Estimators open tomorrow.",
        cp_prompt=(
            """Closed-book. An analyst takes the 40 most recent claims from one large commercial client and treats them as a random sample from the whole motor book. (1) In one sentence, why this may fail as a random sample of the portfolio population. (2) State what a random sample from a population requires. (3) Refuse: 'I have n = 40 observations, so I already have a random sample.'"""
        ),
        cp_kw=["random sample", "population", "iid", "sampling", "refuse", "observations"],
        cp_model=(
            """(1) Consecutive claims from one client are clustered and not an iid draw from the whole book. Dependence and selection bias break the portfolio sampling warrant. (2) A random sample is drawn so that each observation follows the population distribution under CMP/iid (or stated sampling) conditions. (3) Refuse: having observations is not the same as a random sample with a lawful sampling warrant."""
        ),
        reflect="Harvest sampling wobble: estimators continue Memory Front tomorrow.",
    ),
    dict(
        day="CP-D5",
        stem="3.1.1-estimators-cs1016",
        pid="CS1-EP001-PKG-CP-3.1-ESTIMATORS",
        lo="3.1.1",
        topic_code="3.1",
        topic_title="Estimators and their properties",
        slug="3.1-estimators",
        keywords=["estimator", "moments", "parameter", "memory"],
        title="Retrieve method-of-moments estimators (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 3.1.1 method-of-moments estimators under Memory Front discipline. Without pretending CI-from-sample (3.2.1) is finished.",
        tutor="Today I will force estimator retrieval and refuse 'Memory Front finished CIs / spine PASS'.",
        edu="Produce Memory Front retrieval of method-of-moments estimators as inference entry.",
        lo_text="Use the method of moments for constructing estimators of population parameters.",
        focus="Moments → equate → estimator → refuse MLE-as-MoM / estimator-as-CI.",
        prior="Yesterday you retrieved random samples (2.6.1). Today continues Memory Front at estimators.",
        why="Estimator construction is the first inference hinge after sampling foundations.",
        benefit=(
            "You'll retrieve how to construct a method-of-moments estimator from "
            "population moment equations."
        ),
        explain="Day 5 focuses the named learning objective. Opens Chapter 3 at method of moments.",
        criteria=["Closed-book, outline method-of-moments construction in one careful chain.", "Name one population parameter you could target.", "Refuse one CI / spine swallow."],
        tasks=["Sketch moments→estimator path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 3.1.1.", "Closed-book Knowledge Checks."],
        next_code="3.2",
        next_title="Confidence interval from a random sample (3.2.1)",
        cont="Today you retrieved 3.1.1; tomorrow continues Memory Front at 3.2.1.",
        prep="Optional: glance at CMP headings for Syllabus 3.2.1. Titles only tonight",
        student="Tomorrow: CI-from-sample Memory Front hinge (3.2.1). Optional light prep: skim 3.2.1 headings. Titles only tonight.",
        open="CMP · Syllabus 3.1.1 method of moments estimators",
        stop="Through the CMP treatment of Syllabus 3.1.1 (stop before CI-from-sample primary 3.2.1)",
        oos=["CI from sample as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for equating estimator with confidence interval.", "Watch for swallowing 3.2.1 today.", "Watch for claiming Chapter 3 complete."],
        ar_prompt="Closed-book. (1) What is the method-of-moments move? (2) What object do you construct? (3) Why is 3.2.1 not today's primary?",
        ar_kw=["moments", "estimator", "parameter", "population"],
        ar_model="Match sample moments to population moments to construct estimators. CIs open tomorrow.",
        cp_prompt=(
            "Closed-book. Exponential claim sizes with mean θ; sample mean x̄ = 5. "
            "(1) Write the method-of-moments estimator for θ. (2) Refuse: 'I "
            "maximised the likelihood, so I already have the MoM estimator' and 'an "
            "estimator is the same object as a confidence interval.'"
        ),
        cp_kw=["moments", "equate", "mean", "refuse", "likelihood", "confidence", "estimator"],
        cp_model=(
            "(1) Equate E[X]=θ to x̄, so θ̂_MoM = x̄ = 5. (2) Refuse: MLE maximises "
            "the likelihood: different construction from MoM. An estimator is a "
            "point estimate of a parameter; a CI is an interval procedure for a "
            "parameter."
        ),
        reflect="Harvest estimator wobble. CI-from-sample continues Memory Front tomorrow.",
    ),
    dict(
        day="CP-D6",
        stem="3.2.1-ci-sample-cs1016",
        pid="CS1-EP001-PKG-CP-3.2-CI-SAMPLE",
        lo="3.2.1",
        topic_code="3.2",
        topic_title="Confidence and prediction intervals",
        slug="3.2-ci-sample",
        keywords=["confidence", "interval", "sample", "memory"],
        title="Retrieve CI from a random sample (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 3.2.1 confidence-interval-from-sample skill under Memory Front discipline. Without pretending hypothesis testing (3.3.1) is finished.",
        tutor="Today I will force CI-from-sample retrieval and refuse 'Memory Front finished HT / spine PASS'.",
        edu="Produce Memory Front retrieval of parameter CI based on a random sample.",
        lo_text="Construct a confidence interval for an unknown parameter of a distribution based on a random sample.",
        focus="Sample → parameter CI → coverage reading → refuse prediction-as-CI / HT-as-CI.",
        prior="Yesterday you retrieved estimators (3.1.1). Today continues Memory Front at CI-from-sample.",
        why="CI construction is a high-stakes inference hinge before hypothesis testing.",
        benefit="You'll retrieve how to build a confidence interval for a parameter from a random sample.",
        explain="Day 6 focuses the named learning objective. Places CI-from-sample before HT.",
        criteria=["Closed-book, outline CI construction from a random sample.", "State what 'confidence' does and does not mean in one careful sentence.", "Refuse one HT / spine swallow."],
        tasks=["Sketch CI path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 3.2.1.", "Closed-book Knowledge Checks."],
        next_code="3.3",
        next_title="Hypothesis testing foundations (3.3.1)",
        cont="Today you retrieved 3.2.1; tomorrow continues Memory Front at 3.3.1.",
        prep="Optional: glance at CMP headings for Syllabus 3.3.1. Titles only tonight",
        student="Tomorrow: hypothesis-testing Memory Front hinge (3.3.1). Optional light prep: skim 3.3.1 headings. Titles only tonight.",
        open="CMP · Syllabus 3.2.1 confidence interval based on a random sample",
        stop="Through the CMP treatment of Syllabus 3.2.1 (stop before hypothesis testing primary 3.3.1)",
        oos=["Hypothesis testing as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for treating CI as a probability on the parameter after seeing data without care.", "Watch for swallowing HT today.", "Watch for claiming Chapter 3 complete."],
        ar_prompt="Closed-book. (1) What inputs enter a CI from a random sample? (2) What claim does the interval support? (3) Why is 3.3.1 not today's primary?",
        ar_kw=["confidence", "interval", "sample", "parameter"],
        ar_model="A CI uses sample information to construct an interval for an unknown parameter under stated assumptions. HT opens tomorrow.",
        cp_prompt=(
            "Closed-book. A 95% CI for mean claim size μ is (80, 100). (1) What does "
            "this interval claim about μ? (2) Refuse: 'There is a 95% chance the "
            "next claim falls in (80, 100)' and 'a CI is the same as a hypothesis "
            "test.'"
        ),
        cp_kw=["coverage", "parameter", "refuse", "prediction", "hypothesis", "confidence"],
        cp_model=(
            "(1) The interval comes from a procedure with 95% coverage for the "
            "unknown parameter μ under repeated sampling. (2) Refuse: that is a "
            "prediction reading of a future observation, not a parameter CI. A CI "
            "estimates a parameter with coverage; a hypothesis test decides between "
            "hypotheses."
        ),
        reflect="Harvest CI wobble: hypothesis testing continues Memory Front tomorrow.",
    ),
    dict(
        day="CP-D7",
        stem="3.3.1-hypothesis-testing-cs1016",
        pid="CS1-EP001-PKG-CP-3.3-HYPOTHESIS-TESTING",
        lo="3.3.1",
        topic_code="3.3",
        topic_title="Hypothesis testing and goodness of fit",
        slug="3.3-hypothesis-testing",
        keywords=["hypothesis", "null", "power", "memory"],
        title="Retrieve hypothesis-testing foundations (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 3.3.1 hypothesis-testing foundations under Memory Front discipline. Without pretending linear regression (4.1.1) is finished.",
        tutor="Today I will force HT vocabulary retrieval and refuse 'Memory Front finished regression / spine PASS'.",
        edu="Produce Memory Front retrieval of HT foundations as Chapter 3 close hinge.",
        lo_text="Understand null/alternative hypotheses, error types, test statistics, critical regions, significance, p-values, and power at foundation level.",
        focus="Null/alternative → Type I/II → p-value / power → refuse cookbook-as-concepts.",
        prior="Yesterday you retrieved CI-from-sample (3.2.1). Today continues Memory Front at HT foundations.",
        why="Refresh hypothesis-testing foundations before you revisit regression and GLM.",
        benefit="You'll retrieve null/alternative, error types, p-values, and power at foundation level.",
        explain="Day 7 focuses the named learning objective. Closes Chapter 3 at HT foundations before CF-join regression.",
        criteria=["Closed-book, name null vs alternative and type I vs type II in careful pairs.", "Name test statistic / critical region / significance at foundation level.", "Refuse one regression / spine swallow."],
        tasks=["Sketch HT vocabulary map before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 3.3.1.", "Closed-book Knowledge Checks."],
        next_code="4.1",
        next_title="Linear regression entry (4.1.1)",
        cont="Today you retrieved 3.3.1; tomorrow continues Memory Front at 4.1.1.",
        prep="Optional: glance at CMP headings for Syllabus 4.1.1. Titles only tonight",
        student="Tomorrow: linear-regression Memory Front hinge (4.1.1). Optional light prep: skim 4.1.1 headings. Titles only tonight.",
        open="CMP · Syllabus 3.3.1 hypothesis testing foundations",
        stop="Through the CMP treatment of Syllabus 3.3.1 (stop before linear regression primary 4.1.1)",
        oos=["Linear regression as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance"],
        misconceptions=["Watch for confusing type I and type II errors.", "Watch for swallowing regression today.", "Watch for claiming Chapter 3 complete as spine PASS."],
        ar_prompt="Closed-book. (1) Distinguish null and alternative. (2) Distinguish type I and type II. (3) Why is 4.1.1 not today's primary?",
        ar_kw=["null", "alternative", "type I", "type II", "power"],
        ar_model="Null vs alternative frame the test; type I/II name error directions; power is related. Regression opens tomorrow.",
        cp_prompt=(
            "Closed-book. Fraud flag: H₀ = genuine claim, H₁ = fraudulent. (1) "
            "Define Type I and Type II errors here. (2) In one sentence each, what "
            "are a p-value and power? (3) Refuse: 'I clicked a software z-test, so "
            "HT concepts are done' and 'HT foundations are the same skill as fitting "
            "a linear regression.'"
        ),
        cp_kw=["Type I", "Type II", "p-value", "power", "refuse", "regression", "null"],
        cp_model=(
            "(1) Type I: flag fraud when the claim is genuine. Type II: miss fraud "
            "when it is present. (2) p-value: probability under H₀ of data at least "
            "as extreme as observed. Power: probability of rejecting H₀ when H₁ is "
            "true. (3) Refuse: a cookbook software test does not replace HT "
            "vocabulary; linear regression is a different topic."
        ),
        reflect="Harvest HT wobble: linear regression continues Memory Front tomorrow.",
    ),
    dict(
        day="CP-D8",
        stem="4.1.1-linear-regression-cs1016",
        pid="CS1-EP001-PKG-CP-4.1-LINEAR-REGRESSION",
        lo="4.1.1",
        topic_code="4.1",
        topic_title="Linear regression models",
        slug="4.1-linear-regression",
        keywords=["response", "explanatory", "regression", "memory"],
        title="Retrieve linear-regression entry (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 4.1.1 response/explanatory entry under Memory Front discipline. Without pretending Bayes' theorem tip (5.1.1) is finished.",
        tutor="Today I will force regression-entry retrieval and refuse 'Memory Front finished Bayes / spine PASS'.",
        edu="Produce Memory Front retrieval of linear-regression entry as Continuity Front join hinge.",
        lo_text="Distinguish response and explanatory variables in a linear regression setting.",
        focus="Data sketch \u2192 name response Y \u2192 name explanatory X's with warrants \u2192 refuse column-soup / role-swap.",
        prior="Yesterday you retrieved HT foundations (3.3.1). Today continues Memory Front at Continuity Front join regression entry.",
        why="Refresh response vs explanatory roles. The entry point into linear modelling.",
        benefit=(
            """You'll retrieve how to name response and explanatory variables with modelling warrants in a linear regression setting."""
        ),
        explain="Day 8 focuses the named learning objective. Returns to Nu CF-join entry before Bayes tip.",
        criteria=["Closed-book, distinguish response vs explanatory with one actuarial-flavoured example.", "State why this is entry not full 4.1 mastery.", "Refuse one Bayes / spine swallow."],
        tasks=["Sketch response/explanatory map before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 4.1.1.", "Closed-book Knowledge Checks."],
        next_code="5.1",
        next_title="Bayes' theorem tip (5.1.1)",
        cont="Today you retrieved 4.1.1; tomorrow continues Memory Front at 5.1.1 tip hinge.",
        prep="Optional: glance at CMP headings for Syllabus 5.1.1. Titles only tonight",
        student="Tomorrow: Bayes' theorem Memory Front tip hinge (5.1.1). Optional light prep: skim 5.1.1 headings. Titles only tonight.",
        open="CMP · Syllabus 4.1.1 response and explanatory variables",
        stop="Through the CMP treatment of Syllabus 4.1.1 (stop before Bayes tip primary 5.1.1)",
        oos=["Bayes' theorem as primary", "First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance", "Whole-Delta Trust Front absorb"],
        misconceptions=["Watch for swapping response and explanatory.", "Watch for swallowing Bayes tip today.", "Watch for claiming mid-spine complete as spine PASS."],
        ar_prompt="Closed-book. (1) What is a response variable? (2) What is an explanatory variable? (3) Why is 5.1.1 not today's primary?",
        ar_kw=["response", "explanatory", "regression", "variable"],
        ar_model="Response is modelled outcome; explanatory variables explain variation in the response. Bayes tip opens tomorrow.",
        cp_prompt=(
            """Closed-book. Household contents book: you want to model renewal premium. Columns include renewal premium, sum insured, number of bedrooms, previous claims count, and postcode band. (1) Name the response and two explanatory variables with a one-sentence warrant each. (2) Refuse: 'Put every numeric column on the right-hand side. That finishes variable-role modelling' and 'Treat renewal premium as an explanatory variable for sum insured.'"""
        ),
        cp_kw=["response", "explanatory", "regression", "warrant", "refuse", "column-soup"],
        cp_model=(
            """(1) Response Y = renewal premium (the outcome to explain/predict). Explanatory examples: sum insured and bedrooms (predictors of premium level); previous claims count may also warrant as an X. (2) Refuse: column-soup is not modelling. Choose Y for the modelling question, then choose X's with warrants. Swapping so that premium explains sum insured answers a different question."""
        ),
        reflect="Harvest regression-entry wobble. Bayes tip continues Memory Front tomorrow.",
    ),
    dict(
        day="CP-D9",
        stem="5.1.1-bayes-theorem-cs1016",
        pid="CS1-EP001-PKG-CP-5.1-BAYES-THEOREM",
        lo="5.1.1",
        topic_code="5.1",
        topic_title="Explain fundamental concepts of Bayesian statistics and use these concepts to calculate Bayesian estimators",
        slug="5.1-bayes-theorem",
        keywords=["Bayes", "theorem", "conditional", "memory"],
        title="Retrieve Bayes' theorem tip (Memory Front)",
        purpose="Today's Mission exists to retrieve Syllabus 5.1.1 Bayes' theorem under Memory Front discipline. Without pretending first-pass spine PASS, until-exam trust, or Wave 0 clearance.",
        tutor="Today I will force Bayes' theorem tip retrieval and refuse 'Memory Front finished the exam journey / first-pass spine / Wave 0'.",
        edu="Produce Memory Front retrieval of Bayes' theorem as the Continuity Front tip hinge before Revision.",
        lo_text="Use Bayes’ theorem to calculate simple conditional probabilities.",
        focus=(
            """Prior / base rate → likelihood of data → Bayes update → posterior → refuse inverse-probability confusion."""
        ),
        prior="Yesterday you retrieved linear-regression entry (4.1.1). Today closes Memory Front Learning at the Continuity Front tip hinge.",
        why="Retrieve Bayes' theorem at the tip of Topic 5.1 before revision. Without inventing a Topic 5.2.",
        benefit=(
            """You'll retrieve how to apply Bayes' theorem to compute a simple posterior probability and refuse inverse-probability errors."""
        ),
        explain="Day 9 retrieves Bayes' theorem at the tip of Topic 5.1 before revision.",
        criteria=["Closed-book, state Bayes' theorem for a simple conditional probability case.", "Compute or outline one simple application.", "Refuse one spine / until-exam / Wave 0 clearance claim."],
        tasks=["Sketch Bayes path before CMP.", "Complete Guided Reading through CMP treatment of Syllabus 5.1.1.", "Closed-book Knowledge Checks: theorem + refuse spine swallow."],
        next_code="CP-R1",
        next_title="Campaign Pi Revision: retrieve Memory Front hinges",
        cont="Today you closed Memory Front Learning at Bayes tip; tomorrow is Campaign Pi Revision returning to the hinge chain.",
        prep="No new LO tonight: rest or jot the stickiest Memory Front hinge for Revision",
        student="Tomorrow: CP-R1 Revision of Memory Front hinges. Optional: note your weakest hinge. Titles only tonight.",
        open="CMP · Syllabus 5.1.1 Bayes’ theorem for simple conditional probabilities",
        stop="Through the CMP treatment of Syllabus 5.1.1 (stop before terminal Revision as Learning; no spine / until-exam / Wave 0 claim)",
        oos=["First-pass spine PASS", "Until-exam educational trust", "Wave 0 Approver honesty clearance", "Topic 5.2 invention", "Certified Educational Coverage increase from catalogue alone", "New first-pass LO beyond Memory Front"],
        misconceptions=["Watch for claiming spine / until-exam from tip retrieval day.", "Watch for inventing Topic 5.2.", "Watch for skipping Revision."],
        ar_prompt="Closed-book. (1) State Bayes' theorem for a simple case. (2) What probability do you update? (3) Name one reason this does not finish first-pass spine or until-exam trust.",
        ar_kw=["Bayes", "conditional", "prior", "posterior"],
        ar_model="Bayes updates probabilities using prior and likelihood information in simple cases. Spine PASS and until-exam remain out of scope.",
        cp_prompt=(
            """Closed-book. Screening: P(D) = 0.01, P(+|D) = 0.95, P(+|not D) = 0.10. A case tests positive. (1) Compute P(D|+) via Bayes (show the normalising P(+)). (2) Refuse: 'P(D|+) equals P(+|D) = 0.95.'"""
        ),
        cp_kw=["Bayes", "posterior", "prior", "likelihood", "base rate", "refuse"],
        cp_model=(
            """(1) P(+) = 0.95·0.01 + 0.10·0.99 = 0.0095 + 0.099 = 0.1085. P(D|+) = 0.0095 / 0.1085 ≈ 0.0876. (2) Refuse: that equates posterior with likelihood and ignores the base rate. Bayes multiplies prior × likelihood and normalises."""
        ),
        reflect="Harvest Bayes-tip wobble. Revision protects the Memory Front chain tomorrow.",
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

    rev = revision_pkg()
    (PKG_DIR / "revision-spine-memory-cs1016.json").write_text(json.dumps(rev, indent=2) + "\n")
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-PI",
        "campaign_version": "cs1016-1.0.0",
        "display_title": (
            "Campaign Pi. Memory Front spine re-audit after Topic 5.1 tip close"
        ),
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-016",
        "prior_volume_id": "CS1-015",
        "day_count": {"learning": 9, "revision": 1, "total": 10},
        "syllabus_span": span,
        "front_class": "memory_front_spine_reaudit",
        "out_of_scope": [
            "first-pass spine PASS",
            "until-examination educational trust",
            "Wave 0 Approver honesty clearance",
            "Topic 5.2 invention / remainder theatre",
            "Trust Front whole-Delta absorb into Continuity Front credit",
            "Wave 15 authoring",
            "coverage mirage / Student Reliance increase from catalogue alone",
            "LIVE copies in educational_packages/",
        ],
        "inventory": inventory,
        "wave0_note": (
            "Publication Front / Wave 0 Alpha/Beta Approver honesty gap remains open. "
            "Approver ownership is scheduled; Pi catalogue must not claim clearance."
        ),
        "trust_front_note": (
            "CS1-003 / Campaign Delta remains independent Trust Front LIVE inventory for "
            "4.1–5.1. Pi package IDs are CP-prefixed Memory Front catalogue. "
            "not LIVE this cycle; Published Coverage unchanged (hinges already counted)."
        ),
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

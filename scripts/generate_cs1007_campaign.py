#!/usr/bin/env python3
"""Generate CS1-007 / Campaign Eta educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-eta-cs1007"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1007-campaign-eta-1.0.0",
    "publication_version": "cs1007-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-ETA",
    "volume_id": "CS1-007",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1007_EDUCATIONAL_VOLUME.md",
        "CS1007_CERTIFICATION_REPORT.md",
        "EP005_WAVE5_PLAN.md",
    ],
    "author_id": "cs1007-educational-author",
    "authored_at": "2026-08-01",
}

TOPIC = {
    "topic_code": "2.4",
    "topic_title": "Evaluate and apply generating functions",
    "topic_id": "CS1-B-T04",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "2.4", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1007-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1007-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1007-cs1-{d['slug']}",
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
                f"for later 2.4 LOs, Chapter 2, or the central limit theorem."
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
                "episode_id": f"lep-cs1007-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1007-{lo}-ar-01",
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
                "episode_id": f"lep-cs1007-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1007-{lo}-cp-01",
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
    day = "CH-R1"
    pid = "CS1-EP001-PKG-REV-GENERATING-FUNCTIONS"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Eta revision — generating functions",
        "return_targets": ["2.4.1", "2.4.2"],
        "topic_aliases": [day, "campaign-eta-revision"],
        "topic_title_keywords": [
            "revision",
            "generating",
            "moment",
            "cumulant",
            "MGF",
            "CGF",
            "series",
            "differentiation",
        ],
        "golden_id": "GOLDEN-CS1007-CS1-CH-R1-GENERATING-FUNCTIONS",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1007-cs1-ch-r1-generating-functions",
            "display_title": "Retrieve generating-function hinges (2.4)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Eta — retrieving moment "
                "and cumulant generating functions, and moment calculation via series or "
                "differentiation — so 2.4 does not evaporate before the central limit theorem (2.5)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Eta's Learning hinges — "
                "not a passive CMP re-read and not a first-pass 2.5 lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: "
                "MGF/CGF definition → moments via expansion or differentiation."
            ),
            "learning_objective": (
                "Retrieve and connect (1) moment and cumulant generating functions of a random "
                "variable, and (2) moment calculation via series expansion or differentiation "
                "of a generating function."
            ),
            "concept_focus": (
                "Campaign chain retrieval: MGF/CGF → moments via series or differentiation."
            ),
            "prior_bridge": (
                "Yesterday you finished moment calculation via generating functions (2.4.2). "
                "Today is Revision mode: return to 2.4.1–2.4.2 under closed-book retrieval — "
                "no new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 2.5 work."
            ),
            "expected_benefit": (
                "Evidence that the 2.4 chain retrieves — revision Study Progress, not a claim "
                "that Chapter 2 or the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, outline what an MGF (and CGF) is for a random variable.",
                "State how moments arise via series expansion or differentiation of a GF.",
                "Refuse Chapter 2 complete / spine / until-exam / CLT-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Eta's chain: MGF/CGF → moments via GF.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 40, "max": 55},
        },
        "session": {
            "session_id": "ssn-cs1007-cs1-ch-r1-generating-functions",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Eta skills — not to teach 2.5."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link — Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 40, "max": 55},
            "wrap_up": (
                "Revision Session complete. You stress-tested 2.4.1–2.4.2 return targets. "
                "This is revision Study Progress — not Topic Complete for 2.5, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that MGF/CGF → moments via GF will still retrieve in "
                "three days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Eta "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you define or interpret the MGF and CGF of a random variable?",
                "Can you obtain moments via series expansion or differentiation of a GF?",
                "What claim must you refuse (Chapter 2 complete / spine / until-exam / 2.5 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 2 / 2.5 complete.",
                "Watch for dropping Zeta conditional-expectation memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection — do not begin Syllabus 2.5 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass central limit theorem (2.5)",
                "Sampling distributions (2.6)",
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
                "episode_id": "lep-cs1007-ch-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1007-ch-r1-ar-01",
                "title": "Active Recall: CH-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) moment and "
                    "cumulant generating functions of a random variable; (2) moment calculation "
                    "via series expansion or differentiation of a generating function."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 2.4.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "MGF",
                    "CGF",
                    "moment",
                    "cumulant",
                    "generating",
                    "series",
                    "differentiation",
                    "expand",
                    "derivative",
                ],
                "explanation": "Revision retrieves the 2.4 arc.",
                "model_answer": (
                    "Example: (1) MGF M_X(t)=E[e^{tX}] (or CMP form); CGF is log M (or CMP "
                    "cumulant form). (2) Moments from Taylor coefficients / derivatives of the "
                    "MGF (or related GF operations in the CMP)."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Two hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1007-ch-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1007-ch-r1-cp-01",
                "title": "Checkpoint: CH-R1",
                "prompt": (
                    "Closed-book. (1) Weakest 2.4 link + one concrete rework. (2) Refuse "
                    "Chapter 2 complete and first-pass spine PASS. (3) Name the honest next "
                    "geography (2.5) or confirm declared stop."
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
                    "2.5",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. CGF vs MGF — five-minute rework. (2) Refuse Chapter 2 complete / "
                    "spine / until-exam. (3) Honest next is 2.5 (successor Volume) or declared "
                    "stop — not claimed finished here."
                ),
                "common_mistake": "Spine / Chapter 2 / until-exam claim.",
                "success_criteria": ["Rework named.", "Forbidden claim refused."],
            },
        ],
        "reflection": {
            "framing": "Revision Reflection names the weakest Campaign link for spaced return.",
            "prompt": (
                "Which return target retrieved least cleanly and what one concrete rework will "
                "you schedule? Confirm Chapter 2 complete / spine / until-exam stayed out of scope."
            ),
            "prompts": [
                "Which return target retrieved least cleanly?",
                "What one concrete rework will you schedule?",
                "Confirm: Chapter 2 complete / spine PASS / until-exam trust were out of scope.",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "2.5",
            "next_topic_title": (
                "Honest next — central limit theorem (2.5) under a successor Volume "
                "(or declared stop)"
            ),
            "continuity_line": (
                "Campaign Eta / Volume CS1-007 completes after this Revision. Honest stop: "
                "2.4 Pilot Arc closed — not Chapter 2 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 2.5 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight — rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Eta / CS1-007 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 2.5 successor Volume. Optional: schedule your "
                "weakest 2.4 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CH-D1",
        stem="2.4.1-mgf-cgf-cs1007",
        pid="CS1-EP001-PKG-2.4-MGF-CGF",
        lo="2.4.1",
        slug="2.4-mgf-cgf",
        keywords=["moment", "cumulant", "generating", "function", "MGF", "CGF"],
        title="Form the moment and cumulant generating functions of an RV",
        purpose=(
            "Today's Mission exists to obtain the moment and cumulant generating functions of "
            "a random variable — so M_X(t) and K_X(t) (or CMP equivalents) are usable objects — "
            "without pretending moment-via-GF calculation is finished."
        ),
        tutor=(
            "Today I will force the candidate to define or interpret the MGF and CGF — and "
            "refuse treating 'I can compute ordinary moments by hand' as having generating "
            "functions."
        ),
        edu=(
            "Produce a cognitive move from the distribution of an RV to lawful MGF and CGF "
            "objects under CMP definitions."
        ),
        lo_text=(
            "Obtain and interpret the moment and cumulant generating functions of a random "
            "variable."
        ),
        focus=(
            "Distribution → MGF M_X(t)=E[e^{tX}] → CGF (log M or CMP form) → refuse "
            "ordinary-moments-as-GF."
        ),
        prior=(
            "Campaign Zeta closed expectations and conditional expectations (2.3) with "
            "Revision. Today opens topic 2.4 at LO 2.4.1 — the named Continuity Front after "
            "CS1-006."
        ),
        why=(
            "2.4.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at generating functions, keeping moment-via-GF for the following session."
        ),
        benefit="Study Progress for MGF/CGF — not Topic Complete for 2.4.2.",
        explain=(
            "Day 1 opens 2.4 at the named learning objective — "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, outline what the MGF is (CMP form).",
            "State how the CGF relates to the MGF (or CMP cumulant definition).",
            "Refuse one 'ordinary moments finished generating functions' claim.",
        ],
        tasks=[
            "Sketch MGF and CGF definitions before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.4.1.",
            "Closed-book Knowledge Checks: MGF/CGF + refuse ordinary-moments collapse.",
        ],
        next_code="2.4",
        next_title="Moment calculation via generating functions (2.4.2)",
        cont=(
            "Today you formed moment and cumulant generating functions; tomorrow continues "
            "2.4 at moment calculation via series expansion or differentiation of a GF."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.4.2 — titles only tonight",
        student=(
            "Tomorrow: moment calculation via generating functions (2.4.2). Optional light "
            "prep: skim 2.4.2 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.4.1 moment and cumulant generating functions",
        stop=(
            "Through the CMP treatment of Syllabus 2.4.1 "
            "(stop before moment calculation via GF 2.4.2)"
        ),
        oos=[
            "Moment calculation via series/differentiation as primary (2.4.2)",
            "Central limit theorem (2.5)",
            "Sampling distributions (2.6)",
            "Inference Chapter 3",
            "CS1B coding marathon",
        ],
        misconceptions=[
            "Watch for equating 'I know E[X] and Var(X)' with having an MGF/CGF.",
            "Watch for starting moment-via-differentiation drills (2.4.2) inside this sitting.",
            "Watch for CLT work (2.5) today.",
        ],
        ar_prompt=(
            "Closed-book. (1) Write or state the MGF of a random variable X. (2) What is the "
            "CGF in relation to the MGF (or CMP form)? (3) Name one reason these objects are "
            "not the same as listing a few raw moments."
        ),
        ar_kw=[
            "MGF",
            "CGF",
            "moment",
            "cumulant",
            "generating",
            "E[e",
            "log",
            "function",
            "t",
        ],
        ar_model=(
            "MGF is M_X(t)=E[e^{tX}] (or CMP equivalent). CGF is typically K_X(t)=log M_X(t) "
            "(or CMP cumulant form). Knowing a few moments is not the same as possessing the "
            "generating-function object that encodes the moment sequence."
        ),
        cp_prompt=(
            "Closed-book. A colleague says 'we already know how to get means and variances, "
            "so generating functions are just the same skill.' Refuse in one sentence and "
            "restate what today's LO adds."
        ),
        cp_kw=["refuse", "MGF", "CGF", "generating", "not same", "function", "moments"],
        cp_model=(
            "Refuse: raw moments are not the MGF/CGF. Today's skill is forming and interpreting "
            "the generating-function objects (MGF and CGF) for a random variable."
        ),
        reflect=(
            "Harvest wobble on MGF vs CGF vs raw moments — moment-via-GF calculation comes tomorrow."
        ),
    ),
    dict(
        day="CH-D2",
        stem="2.4.2-moment-via-gf-cs1007",
        pid="CS1-EP001-PKG-2.4-MOMENT-VIA-GF",
        lo="2.4.2",
        slug="2.4-moment-via-gf",
        keywords=["moment", "series", "expansion", "differentiation", "generating", "MGF"],
        title="Obtain moments via series expansion or differentiation of a GF",
        purpose=(
            "Today's Mission exists to obtain moments via series expansion or differentiation "
            "of a generating function — so the GF → moment pipeline is usable — without "
            "claiming Chapter 2 or the central limit theorem complete."
        ),
        tutor=(
            "Today I will force the candidate through moment extraction from a GF — refuse "
            "treating yesterday's MGF/CGF definitions as having finished moment calculation, "
            "and refuse Chapter-2-complete claims."
        ),
        edu=(
            "Produce executable warrants for moments obtained via series expansion or "
            "differentiation of a generating function."
        ),
        lo_text=(
            "Obtain moments of a random variable via series expansion or differentiation of "
            "a generating function."
        ),
        focus=(
            "MGF/CGF → Taylor / derivatives → moments → refuse definition-as-done / Ch2-done."
        ),
        prior=(
            "Yesterday you formed moment and cumulant generating functions (2.4.1). Today uses "
            "those objects to recover moments."
        ),
        why=(
            "2.4.2 completes topic 2.4 Learning; Revision follows before any 2.5 commission."
        ),
        benefit=(
            "Study Progress for moment-via-GF — not 2.5; not Chapter 2 trophy."
        ),
        explain="Campaign Eta Day 2 focuses LO 2.4.2 — terminal Learning day of CS1-007.",
        criteria=[
            "Closed-book, outline how a moment arises from series coefficients of an MGF.",
            "Outline how differentiation of an MGF (or related GF) yields moments (CMP form).",
            "Refuse Chapter 2 complete / treating 2.4.1 as having finished 2.4.2.",
        ],
        tasks=[
            "Sketch series-expansion and differentiation routes to moments before CMP.",
            "Guided Reading through CMP 2.4.2.",
            "Knowledge Checks: moment-via-GF + refuse Ch2-complete.",
        ],
        next_code="CH-R1",
        next_title="Campaign Eta Revision — retrieve 2.4.1–2.4.2",
        cont=(
            "Today you finished moment calculation via generating functions; tomorrow is "
            "Revision mode — retrieve the 2.4 chain closed-book before any 2.5 first-pass work."
        ),
        prep="Optional: list the two 2.4 LO hinges from memory — titles only tonight",
        student=(
            "Tomorrow: Campaign Eta Revision (retrieve 2.4.1–2.4.2). Optional light prep: "
            "list the two hinges from memory — titles only tonight."
        ),
        open="CMP · Syllabus 2.4.2 moment calculation via generating functions",
        stop="Through CMP 2.4.2 (stop before central limit theorem 2.5)",
        oos=[
            "Central limit theorem (2.5)",
            "Sampling distributions (2.6)",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "First-pass spine PASS",
        ],
        misconceptions=[
            "Watch for stopping at MGF/CGF definition without extracting moments.",
            "Watch for claiming Chapter 2 / 2.5 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. (1) How does a series expansion of an MGF yield moments? "
            "(2) In one sentence, how can differentiation of a GF produce a moment (CMP idea)?"
        ),
        ar_kw=[
            "series",
            "expansion",
            "Taylor",
            "coefficient",
            "derivative",
            "differentiation",
            "moment",
            "MGF",
            "t=0",
        ],
        ar_model=(
            "Moments appear as coefficients in the Taylor series of the MGF (scaled as in the "
            "CMP). Differentiating the MGF and evaluating at t=0 (or equivalent CMP operation) "
            "recovers moments."
        ),
        cp_prompt=(
            "Closed-book. (1) Refuse 'yesterday's MGF/CGF finished today's LO'. (2) Refuse "
            "'Chapter 2 is complete because I finished 2.4.2'. State the honest stop."
        ),
        cp_kw=["refuse", "series", "derivative", "chapter", "complete", "2.5", "revision", "stop"],
        cp_model=(
            "(1) Refuse: defining MGF/CGF is not the same as extracting moments via series or "
            "differentiation. (2) Refuse: 2.4.2 closes topic 2.4 Learning, not Chapter 2; next "
            "is Revision then honest 2.5 successor — not spine/until-exam claims."
        ),
        reflect="Harvest moment-via-GF wobble — Revision protects the 2.4 chain tomorrow.",
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
    (PKG_DIR / "revision-generating-functions-cs1007.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-ETA",
        "campaign_version": "cs1007-1.0.0",
        "display_title": "Campaign Eta — Generating functions (2.4)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-007",
        "prior_volume_id": "CS1-006",
        "day_count": {"learning": 2, "revision": 1, "total": 3},
        "syllabus_span": span,
        "out_of_scope": [
            "2.5+",
            "Chapter 2 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 6 / Chapter 3 inference authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

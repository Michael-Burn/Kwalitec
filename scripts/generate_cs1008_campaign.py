#!/usr/bin/env python3
"""Generate CS1-008 / Campaign Theta educational packages (catalogue only)."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-theta-cs1008"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1008-campaign-theta-1.0.0",
    "publication_version": "cs1008-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-THETA",
    "volume_id": "CS1-008",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1008_EDUCATIONAL_VOLUME.md",
        "CS1008_CERTIFICATION_REPORT.md",
        "EP006_WAVE6_PLAN.md",
    ],
    "author_id": "cs1008-educational-author",
    "authored_at": "2026-08-02",
}

TOPIC = {
    "topic_code": "2.5",
    "topic_title": "State and apply the central limit theorem",
    "topic_id": "CS1-B-T05",
}


def learning_pkg(d: dict) -> dict:
    lo = d["lo"]
    return {
        **COMMON,
        **TOPIC,
        "package_id": d["pid"],
        "campaign_day": d["day"],
        "topic_focus_lo": lo,
        "topic_aliases": [TOPIC["topic_id"], "2.5", lo],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1008-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1008-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1008-cs1-{d['slug']}",
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
                f"for later 2.5 LOs, Chapter 2, sampling distributions, or until-exam trust."
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
                "episode_id": f"lep-cs1008-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1008-{lo}-ar-01",
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
                "episode_id": f"lep-cs1008-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1008-{lo}-cp-01",
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
    day = "CT-R1"
    pid = "CS1-EP001-PKG-REV-CENTRAL-LIMIT-THEOREM"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Theta revision — central limit theorem",
        "return_targets": ["2.5.1", "2.5.2"],
        "topic_aliases": [day, "campaign-theta-revision"],
        "topic_title_keywords": [
            "revision",
            "central",
            "limit",
            "theorem",
            "CLT",
            "Normal",
            "simulation",
            "iid",
        ],
        "golden_id": "GOLDEN-CS1008-CS1-CT-R1-CENTRAL-LIMIT-THEOREM",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1008-cs1-ct-r1-central-limit-theorem",
            "display_title": "Retrieve central-limit hinges (2.5)",
            "mission_purpose": (
                "Today's Mission exists to protect memory of Campaign Theta — retrieving the "
                "central limit theorem for iid sequences, and comparison of simulated samples "
                "with the Normal — so 2.5 does not evaporate before sampling distributions (2.6)."
            ),
            "tutor_intent": (
                "Today I will run closed-book retrieval across Theta's Learning hinges — "
                "not a passive CMP re-read and not a first-pass 2.6 lesson."
            ),
            "educational_intent": (
                "Produce retrieval strength on the Campaign Educational Objective: "
                "CLT for iid sequences → simulated-sample comparison with the Normal."
            ),
            "learning_objective": (
                "Retrieve and connect (1) the central limit theorem for a sequence of "
                "independent, identically distributed random variables, and (2) comparison of "
                "simulated samples from a given distribution with the Normal distribution."
            ),
            "concept_focus": (
                "Campaign chain retrieval: CLT (iid) → simulated samples vs Normal."
            ),
            "prior_bridge": (
                "Yesterday you finished simulated-sample comparison with the Normal (2.5.2). "
                "Today is Revision mode: return to 2.5.1–2.5.2 under closed-book retrieval — "
                "no new first-pass LO."
            ),
            "why_now": (
                "You've just finished this topic's learning stretch; spaced retrieval now "
                "protects it before 2.6 work."
            ),
            "expected_benefit": (
                "Evidence that the 2.5 chain retrieves — revision Study Progress, not a claim "
                "that Chapter 2 or the exam journey is complete."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of this topic's chain before moving on."
            ),
            "success_criteria": [
                "Closed-book, state the CLT for an iid sequence (CMP conditions / conclusion).",
                "State what simulated-sample comparison with the Normal is testing (2.5.2).",
                "Refuse Chapter 2 complete / spine / until-exam / 2.6-as-done claims.",
            ],
            "task_descriptions": [
                "Without opening the CMP, sketch Theta's chain: CLT → simulated vs Normal.",
                "Complete Revision Knowledge Checks under closed-book rules.",
                "Author a revision Reflection naming the weakest link.",
            ],
            "estimated_study_time_minutes": {"min": 40, "max": 55},
        },
        "session": {
            "session_id": "ssn-cs1008-cs1-ct-r1-central-limit-theorem",
            "session_educational_purpose": (
                "Retrieve and connect Campaign Theta skills — not to teach 2.6."
            ),
            "session_tutor_purpose": (
                "Keep CMP closed for checks; harvest weakest link — Gate RV substance."
            ),
            "duration_budget_minutes": {"min": 40, "max": 55},
            "wrap_up": (
                "Revision Session complete. You stress-tested 2.5.1–2.5.2 return targets. "
                "This is revision Study Progress — not Topic Complete for 2.6, and not "
                "first-pass spine PASS."
            ),
            "confidence_prompt": (
                "How confident are you that CLT → simulated-vs-Normal will still retrieve in "
                "three days? Rate 1–5 and name the weakest link."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this revision stage: strengthen retrieval of the Campaign Theta "
                "chain without opening a new CMP chapter first. Attempt closed-book retrieval; "
                "only then reopen the exact failed locus."
            ),
            "focus_questions": [
                "Can you state the CLT for an iid sequence (conditions and conclusion)?",
                "Can you explain simulated-sample comparison with the Normal (2.5.2)?",
                "What claim must you refuse (Chapter 2 complete / spine / until-exam / 2.6 done)?",
            ],
            "misconception_watch": [
                "Watch for turning revision into a passive re-read.",
                "Watch for claiming Chapter 2 / 2.6 complete.",
                "Watch for dropping Eta generating-function memory as irrelevant.",
            ],
            "open_point": (
                "No new CMP open required to begin. Targeted re-open only after failed "
                "retrieval on the failed LO block."
            ),
            "stop_condition": (
                "After revision checks and Reflection — do not begin Syllabus 2.6 in this sitting"
            ),
            "out_of_scope_today": [
                "First-pass sampling distributions (2.6)",
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
                "episode_id": "lep-cs1008-ct-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1008-ct-r1-ar-01",
                "title": "Active Recall: CT-R1",
                "prompt": (
                    "Closed-book. Retrieve in order, one short phrase each: (1) central limit "
                    "theorem for an iid sequence; (2) comparison of simulated samples with the "
                    "Normal distribution."
                ),
                "response_type": "short_structured",
                "body": "Revision chain recall for 2.5.",
                "hints": ["Name each hinge briefly.", "Stay retrieval-first."],
                "accepted_keywords": [
                    "CLT",
                    "central",
                    "limit",
                    "iid",
                    "independent",
                    "identical",
                    "Normal",
                    "simulate",
                    "sample",
                    "distribution",
                ],
                "explanation": "Revision retrieves the 2.5 arc.",
                "model_answer": (
                    "Example: (1) For iid RVs with finite mean/variance (CMP conditions), "
                    "standardised sample means → Normal as n grows. (2) Simulate samples from a "
                    "stated distribution and compare behaviour / shape to the Normal (CMP)."
                ),
                "common_mistake": "Passive summary without retrieval.",
                "success_criteria": ["Two hinges named.", "Weakest link candid."],
            },
            {
                "episode_id": "lep-cs1008-ct-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1008-ct-r1-cp-01",
                "title": "Checkpoint: CT-R1",
                "prompt": (
                    "Closed-book. (1) Name today's weakest CLT link and one concrete rework. "
                    "(2) Refuse: 'The CLT means every sample mean is already Normal, so "
                    "Chapter 2 is done.' (3) Name the honest next topic (sampling "
                    "distributions, 2.6) or confirm you are stopping here."
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
                    "2.6",
                    "stop",
                    "until-exam",
                ],
                "explanation": "RV harvests memory debt and honest next.",
                "model_answer": (
                    "(1) e.g. rate of Normal approximation — five-minute rework. (2) Refuse "
                    "Chapter 2 complete / spine / until-exam. (3) Honest next is 2.6 (successor "
                    "Volume) or declared stop — not claimed finished here."
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
            "next_topic_code": "2.6",
            "next_topic_title": (
                "Honest next — sampling distributions (2.6) under a successor Volume "
                "(or declared stop)"
            ),
            "continuity_line": (
                "Campaign Theta / Volume CS1-008 completes after this Revision. Honest stop: "
                "2.5 Pilot Arc closed — not Chapter 2 complete; not first-pass spine; not "
                "until-exam trust. Successor geography is 2.6 under a later commission."
            ),
            "light_prep_cue": (
                "No new first-pass LO tonight — rest or schedule weakest-link rework only"
            ),
            "student_facing": (
                "Campaign Theta / CS1-008 complete after today (pending human Approver + LIVE). "
                "Honest next: stop or await 2.6 successor Volume. Optional: schedule your "
                "weakest 2.5 rework only."
            ),
        },
    }


LEARNING = [
    dict(
        day="CT-D1",
        stem="2.5.1-clt-cs1008",
        pid="CS1-EP001-PKG-2.5-CLT",
        lo="2.5.1",
        slug="2.5-clt",
        keywords=["central", "limit", "theorem", "CLT", "iid", "Normal", "mean"],
        title="State and apply the CLT for an iid sequence",
        purpose=(
            "Today's Mission exists to state and apply the central limit theorem for a "
            "sequence of independent, identically distributed random variables — so the "
            "standardised-mean → Normal conclusion is usable — without pretending simulated "
            "sample comparison (2.5.2) is finished."
        ),
        tutor=(
            "Today I will force the candidate to state CLT conditions and conclusion for iid "
            "sequences — and refuse treating 'the Normal is everywhere' as having the theorem."
        ),
        edu=(
            "Produce a cognitive move from iid sum/mean behaviour to the lawful CLT statement "
            "under CMP conditions."
        ),
        lo_text=(
            "State and apply the central limit theorem for a sequence of independent, "
            "identically distributed random variables."
        ),
        focus=(
            "IID with finite mean/variance → standardised sample mean → Normal limit ",
            "under CLT → refuse Normal-everywhere-without-CLT."
        ),
        prior=(
            "Campaign Eta closed generating functions (2.4) with Revision. Today opens topic "
            "2.5 at LO 2.5.1 — the named Continuity Front after CS1-007."
        ),
        why=(
            "2.5.1 opens this stretch at the natural next learning objective. Close it to avoid "
            "a cliff at the CLT, keeping simulated-sample comparison for the following session."
        ),
        benefit=(
            "You will be able to state and apply the CLT to approximate a ",
            "probability for an iid sample mean."
        ),
        explain=(
            "Day 1 opens 2.5 at the named learning objective — "
            "the natural next step after the previous topic."
        ),
        criteria=[
            "Closed-book, state the CLT conclusion for iid sample means (CMP form).",
            "Name the key conditions the CMP requires (independence, identical distribution, "
            "moment conditions as stated).",
            "Refuse one 'everything is Normal so CLT is done' claim.",
        ],
        tasks=[
            "Sketch iid → standardised mean → Normal before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.5.1.",
            "Closed-book Knowledge Checks: CLT statement + refuse Normal-everywhere collapse.",
        ],
        next_code="2.5",
        next_title="Simulated samples vs Normal (2.5.2)",
        cont=(
            "Today you stated and applied the CLT for iid sequences; tomorrow continues 2.5 "
            "at comparison of simulated samples with the Normal distribution."
        ),
        prep="Optional: glance at CMP headings for Syllabus 2.5.2 — titles only tonight",
        student=(
            "Tomorrow: comparison of simulated samples with the Normal (2.5.2). Optional light "
            "prep: skim 2.5.2 headings — titles only tonight."
        ),
        open="CMP · Syllabus 2.5.1 central limit theorem (iid)",
        stop=(
            "Through the CMP treatment of Syllabus 2.5.1 "
            "(stop before simulated-sample comparison 2.5.2)"
        ),
        oos=[
            "Simulated sample comparison with Normal as primary (2.5.2)",
            "Sampling distributions (2.6)",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for equating 'I know the Normal density' with having the CLT.",
            "Watch for starting simulation-vs-Normal drills (2.5.2) inside this sitting.",
            "Watch for sampling-distribution / 2.6 work today.",
        ],
        ar_prompt=(
            "Closed-book. (1) State the CLT for an iid sequence in one or two sentences "
            "(conditions + conclusion). (2) What random quantity is becoming approximately "
            "Normal? (3) Name one reason 'the Normal is common' is not the same as stating "
            "the CLT."
        ),
        ar_kw=[
            "CLT",
            "central",
            "limit",
            "iid",
            "independent",
            "identical",
            "mean",
            "Normal",
            "standardis",
            "n",
        ],
        ar_model=(
            "Under CMP conditions (iid; finite mean/variance as stated), the standardised "
            "sample mean (or sum) converges in distribution to Normal as n increases. Knowing "
            "the Normal shape is not the same as stating this limit theorem for iid sequences."
        ),
        cp_prompt=(
            "Closed-book. Claim sizes are iid with mean μ=500 and sd σ=200; n=100. ",
            "Using the CLT, approximate P(X̄>540). (1) State the approximate ",
            "distribution of X̄. (2) Compute the standardised z and the approximate ",
            "probability (use Φ(2)≈0.977). (3) Refuse: 'We already use the Normal ",
            "all the time, so the CLT is just common sense and needs no statement.'"
        ),
        cp_kw=["CLT", "iid", "z=2", "0.023", "Normal", "refuse"],
        cp_model=(
            "(1) X̄ ≈ Normal(μ=500, sd=σ/√n=20). (2) z=(540−500)/20=2; ",
            "P(X̄>540)≈1−Φ(2)≈0.023. (3) Refuse: casual Normal habit is not the CLT ",
            "— today's skill is stating and applying the theorem for iid sequences ",
            "under the stated conditions."
        ),
        reflect=(
            "Harvest wobble on conditions vs conclusion — simulated-sample comparison comes "
            "tomorrow."
        ),
    ),
    dict(
        day="CT-D2",
        stem="2.5.2-simulated-sample-normal-cs1008",
        pid="CS1-EP001-PKG-2.5-SIMULATED-SAMPLE-NORMAL",
        lo="2.5.2",
        slug="2.5-simulated-sample-normal",
        keywords=["simulate", "sample", "Normal", "comparison", "distribution", "CLT"],
        title="Compare simulated samples with the Normal distribution",
        purpose=(
            "Today's Mission exists to compare simulated samples from a given distribution "
            "with the Normal distribution — so the simulation check on CLT intuition is "
            "usable — without claiming Chapter 2 or sampling distributions (2.6) complete."
        ),
        tutor=(
            "Today I will force the candidate through simulated-sample vs Normal comparison — "
            "refuse treating yesterday's CLT statement as having finished 2.5.2, and refuse "
            "Chapter-2-complete claims."
        ),
        edu=(
            "Produce executable warrants for comparing simulated samples from a stated "
            "distribution with the Normal (CMP method)."
        ),
        lo_text=(
            "Compare simulated samples from a given distribution with the Normal distribution."
        ),
        focus=(
            "Stated (possibly skewed) parent → simulate samples of size n → compare ",
            "to Normal → judge when Normal approx is poor."
        ),
        prior=(
            "Yesterday you stated and applied the CLT for iid sequences (2.5.1). Today uses "
            "simulation to compare sample behaviour with the Normal."
        ),
        why=(
            "2.5.2 completes topic 2.5 Learning; Revision follows before any 2.6 commission."
        ),
        benefit=(
            "You will be able to say what a simulation-vs-Normal comparison would ",
            "show for a skewed parent and when the Normal approximation is poor."
        ),
        explain="Campaign Theta Day 2 focuses LO 2.5.2 — terminal Learning day of CS1-008.",
        criteria=[
            "Closed-book, outline how to simulate samples from a given distribution for this LO.",
            "State what you compare against the Normal (and what a mismatch might mean).",
            "Refuse Chapter 2 complete / treating 2.5.1 as having finished 2.5.2.",
        ],
        tasks=[
            "Sketch simulate → compare-to-Normal plan before CMP.",
            "Guided Reading through CMP 2.5.2.",
            "Knowledge Checks: simulated-vs-Normal + refuse Ch2-complete.",
        ],
        next_code="CT-R1",
        next_title="Campaign Theta Revision — retrieve 2.5.1–2.5.2",
        cont=(
            "Today you finished simulated-sample comparison with the Normal; tomorrow is "
            "Revision mode — retrieve the 2.5 chain closed-book before any 2.6 first-pass work."
        ),
        prep="Optional: list the two 2.5 LO hinges from memory — titles only tonight",
        student=(
            "Tomorrow: Campaign Theta Revision (retrieve 2.5.1–2.5.2). Optional light prep: "
            "list the two hinges from memory — titles only tonight."
        ),
        open="CMP · Syllabus 2.5.2 simulated samples compared with the Normal",
        stop="Through CMP 2.5.2 (stop before sampling distributions 2.6)",
        oos=[
            "Sampling distributions (2.6)",
            "Inference Chapter 3",
            "Chapter 2 complete claim",
            "First-pass spine PASS",
            "Until-exam educational trust",
        ],
        misconceptions=[
            "Watch for stopping at CLT statement without the simulation comparison.",
            "Watch for claiming Chapter 2 / 2.6 finished.",
            "Watch for treating Revision as optional.",
        ],
        ar_prompt=(
            "Closed-book. (1) What do you simulate for Syllabus 2.5.2? (2) What do you compare "
            "those samples against, and why does that check the CLT intuition?"
        ),
        ar_kw=[
            "simulate",
            "sample",
            "Normal",
            "distribution",
            "compare",
            "CLT",
            "shape",
            "histogram",
        ],
        ar_model=(
            "Simulate samples (or sample means / related quantities as the CMP directs) from a "
            "given distribution; compare their behaviour or shape to the Normal. The comparison "
            "stress-tests when Normal approximation looks reasonable versus when it does not."
        ),
        cp_prompt=(
            "Closed-book. Parent distribution: Exp(mean=1), heavily right-skewed. ",
            "You simulate many samples of size n=5 and of size n=100, each time ",
            "plotting the histogram of the sample mean against a Normal with ",
            "matching mean/variance. (1) What qualitative difference do you expect ",
            "between n=5 and n=100, and why (CLT intuition)? (2) Refuse: 'Stating ",
            "the CLT already finished comparing simulated samples with the Normal' ",
            "and 'a skewed parent means the sample mean is never approximately ",
            "Normal.'"
        ),
        cp_kw=["simulate", "skewed", "n=5", "n=100", "Normal", "refuse", "CLT"],
        cp_model=(
            "(1) At n=5 the histogram of X̄ should still look skewed (poor Normal ",
            "match); at n=100 it should be much closer to Normal as the CLT kicks in ",
            "for the mean. (2) Refuse: stating the theorem is not the same as ",
            "checking simulated samples against Normal; skewness of the parent does ",
            "not forbid approximate Normality of the mean for large n under CLT ",
            "conditions."
        ),
        reflect=(
            "Harvest simulated-vs-Normal wobble — Revision protects the 2.5 chain tomorrow."
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
    (PKG_DIR / "revision-central-limit-theorem-cs1008.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-THETA",
        "campaign_version": "cs1008-1.0.0",
        "display_title": "Campaign Theta — Central limit theorem (2.5)",
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-008",
        "prior_volume_id": "CS1-007",
        "day_count": {"learning": 2, "revision": 1, "total": 3},
        "syllabus_span": span,
        "out_of_scope": [
            "2.6+",
            "Chapter 2 complete",
            "first-pass spine",
            "until-examination educational trust",
            "Wave 7 / Chapter 3 inference authoring",
            "coverage mirage from drafts",
        ],
        "inventory": inventory,
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

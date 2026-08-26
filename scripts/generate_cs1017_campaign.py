#!/usr/bin/env python3
"""Generate CS1-017 / Campaign Rho educational packages (catalogue only).

Publication Front / Wave 0 residual Pilot Arc after Memory Front LIVE (Campaign Pi).
Learning LOs 1.1.1–2.1.2 remain Awaiting Approval — Rho uses distinct CR-prefixed
package IDs and must not be copied to educational_packages/ in this cycle.
Existing Alpha/Beta packages are not modified.
Published Coverage and Student Reliance are unchanged by catalogue authoring.
Approver seals remain required — catalogue must not claim Wave 0 clearance.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "app/curriculum/data/educational_campaigns/cs1/campaign-rho-cs1017"
PKG_DIR = OUT / "packages"

COMMON = {
    "package_version": "cs1017-campaign-rho-1.0.0",
    "publication_version": "cs1017-catalogue-1.0.0",
    "status": "campaign_member_certified",
    "campaign_id": "CS1-EP001-CAMPAIGN-RHO",
    "volume_id": "CS1-017",
    "subject_id": "CS1",
    "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
    "certification_refs": [
        "CS1017_EDUCATIONAL_VOLUME.md",
        "CS1017_CERTIFICATION_REPORT.md",
        "EP015_WAVE15_PLAN.md",
    ],
    "author_id": "cs1017-educational-author",
    "authored_at": "2026-08-04",
    "front_class": "publication_front_wave0_residual",
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
        "topic_aliases": [d["topic_code"], lo, "publication-front-rho"],
        "topic_title_keywords": d["keywords"],
        "golden_id": f"GOLDEN-CS1017-CS1-{d['slug'].upper()}",
        "mode": "learning",
        "mission": {
            "mission_id": f"msn-cs1017-cs1-{d['slug']}",
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
            "session_id": f"ssn-cs1017-cs1-{d['slug']}",
            "session_educational_purpose": (
                f"Execute today's Publication Front Mission for Syllabus {lo}: LO-per-day "
                "Wave 0 residual catalogue under EP Production Era, not Approver clearance."
            ),
            "session_tutor_purpose": (
                f"Set focus on {lo}, exit to CMP, practise today's LO, refuse spine PASS / "
                "until-exam / Approver clearance swallow."
            ),
            "duration_budget_minutes": {"min": 55, "max": 75},
            "wrap_up": (
                f"Session complete for {d['title']}. You practised selective CMP reading on "
                f"Syllabus {lo} under Publication Front discipline. This is Study Progress for "
                "today's LO. Not first-pass spine PASS, until-exam trust, or Approver honesty "
                "clearance."
            ),
            "confidence_prompt": (
                f"How confident are you that you could retrieve today's {lo} closed-book "
                "tomorrow? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                f"Purpose of this reading: use the CMP to study Syllabus {lo}–"
                f"{d['title'].lower()}: under Publication Front / Wave 0 residual discipline. "
                "Stop before out-of-scope later LOs as primary."
            ),
            "focus_questions": [
                f"What is the core move of Syllabus {lo}?",
                "What warrant separates today's LO from the next Publication Front day?",
                "What claim must you refuse today (spine / until-exam / Approver clearance)?",
                "What will you practise in Knowledge Checks after the CMP?",
            ],
            "misconception_watch": d["misconceptions"],
            "open_point": d["open"],
            "stop_condition": d["stop"],
            "out_of_scope_today": d["oos"],
            "annotation_task": "Before deep reading: sketch today's LO chain in notes",
            "attempt_before_reveal": (
                "At the first worked example, cover the answer and attempt the middle step"
            ),
            "worked_examples_cue": (
                "Worked-example re-entry (CMP closed): attempt the LO step before uncovering "
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
                    "cue": "Pause. Write today's core LO move in one sentence.",
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
                "episode_id": f"lep-cs1017-{lo}-ar-01",
                "kind": "active_recall",
                "item_id": f"cs1017-{lo}-ar-01",
                "title": f"Active Recall: {lo}",
                "prompt": d["ar_prompt"],
                "response_type": "short_structured",
                "body": f"Retrieve {lo} closed-book under Publication Front discipline.",
                "hints": ["Use CMP language from today's notes.", "Stay inside today's LO."],
                "accepted_keywords": d["ar_kw"],
                "explanation": f"Active recall for {lo}.",
                "model_answer": d["ar_model"],
                "common_mistake": (
                    "Skipping the LO or claiming Approver clearance / spine / until-exam complete."
                ),
                "success_criteria": ["Addresses the prompt structure.", "Stays inside today's LO."],
            },
            {
                "episode_id": f"lep-cs1017-{lo}-cp-01",
                "kind": "checkpoint",
                "item_id": f"cs1017-{lo}-cp-01",
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
                f"Which part of today's {lo} work is stickiest and why? Quote or paraphrase "
                "the single CMP cue still unclear. If you had five minutes tomorrow, what one "
                "move would you rework?"
            ),
            "prompts": [
                f"Which part of {lo} work is stickiest and why?",
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
            "returns_on": "CR-R1",
            "campaign_revision_package": "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO",
            "note": (
                f"Syllabus {lo} is a CR-R1 return target after Publication Front Learning "
                "span closes."
            ),
        },
    }


def revision_pkg() -> dict:
    day = "CR-R1"
    pid = "CS1-EP001-PKG-REV-PUBLICATION-FRONT-RHO"
    return {
        **COMMON,
        "package_id": pid,
        "campaign_day": day,
        "topic_code": day,
        "topic_title": "Campaign Rho revision: Publication Front Wave 0 residual",
        "return_targets": [
            "1.1.1",
            "1.1.2",
            "1.1.3",
            "1.1.4",
            "1.2.1",
            "1.2.2",
            "1.2.3",
            "2.1.1",
            "2.1.2",
        ],
        "topic_aliases": [day, "campaign-rho-revision", "publication-front"],
        "topic_title_keywords": [
            "revision",
            "publication",
            "wave0",
            "opening",
            "retrieval",
        ],
        "golden_id": "GOLDEN-CS1017-CS1-CR-R1-PUBLICATION-FRONT",
        "mode": "revision",
        "mission": {
            "mission_id": "msn-cs1017-cs1-cr-r1-publication-front",
            "display_title": "Retrieve Publication Front Wave 0 residual chain",
            "mission_purpose": (
                "Today's Mission exists to protect memory across Campaign Rho. Retrieving "
                "1.1.1 through 2.1.2. So Publication Front catalogue completion does not "
                "evaporate into until-exam theatre or Approver clearance claims."
            ),
            "tutor_intent": (
                "Today I will force closed-book retrieval across the Publication Front chain "
                "and refuse 'Rho finished Approver honesty / spine / until-exam'."
            ),
            "educational_intent": (
                "Produce Revision retrieval of Publication Front LO-per-day chain under one "
                "Sensei before an honest stop awaiting human Approver seals."
            ),
            "learning_objective": (
                "Retrieve Campaign Rho Learning LOs 1.1.1–2.1.2 closed-book; reopen CMP only "
                "at failed locus."
            ),
            "concept_focus": (
                "Aims → reproducibility → EDA/PCA → discrete → continuous family retrieval → "
                "refuse claiming the opening analysis arc is finished."
            ),
            "prior_bridge": (
                "Yesterday you closed Publication Front Learning at continuous distributions "
                "(2.1.2). Today is Campaign Rho Revision."
            ),
            "why_now": (
                "Closed-book retrieval of the opening analysis-to-distributions chain before you stop."
            ),
            "expected_benefit": (
                "You'll confirm the opening analysis-to-distributions chain still retrieves closed-book."
            ),
            "explainability": (
                "Revision day: closed-book retrieval of the opening analysis-to-distributions chain before you stop."
            ),
            "success_criteria": [
                "Closed-book, retrieve each CR Learning LO at foundation warrant level.",
                "Reopen CMP only at a failed locus.",
                "Refuse claiming the opening analysis arc is finished from one retrieval sitting.",
            ],
            "task_descriptions": [
                "List CR Learning LOs before opening any CMP.",
                "Retrieve each target closed-book; note failures.",
                "Targeted CMP reopen only at failed locus; then refuse forbidden claims.",
            ],
            "estimated_study_time_minutes": {"min": 55, "max": 80},
        },
        "session": {
            "session_id": "ssn-cs1017-cs1-cr-r1-publication-front",
            "session_educational_purpose": (
                "Execute Campaign Rho Revision: retrieve Publication Front chain without "
                "Approver clearance theatre."
            ),
            "session_tutor_purpose": (
                "Force retrieval across 1.1.1–2.1.2; refuse Approver / spine / until-exam swallow."
            ),
            "duration_budget_minutes": {"min": 55, "max": 80},
            "wrap_up": (
                "Session complete for Publication Front Revision. You retrieved the CR chain "
                "under Wave 0 residual discipline. This is Study Progress for Revision. Not "
                "Approver honesty clearance, first-pass spine PASS, or until-exam trust."
            ),
            "confidence_prompt": (
                "How confident are you that you could retrieve the Publication Front chain "
                "closed-book next week? Rate 1–5 and give one honest warrant."
            ),
        },
        "reading_guidance": {
            "lead_line": (
                "Purpose of this reading: Revision is retrieval-first. Open the CMP only at a "
                "failed locus on the Publication Front chain. Not as a re-teach of all of "
                "Chapter 1–2.1."
            ),
            "focus_questions": [
                "Which CR Learning LO is stickiest closed-book?",
                "Where will you reopen the CMP (failed locus only)?",
                "What claim must you refuse (spine / until-exam / Approver clearance)?",
            ],
            "misconception_watch": [
                "Watch for re-teaching the whole opening arc as Learning.",
                "Watch for claiming Approver clearance from Revision.",
                "Watch for claiming spine / until-exam complete.",
            ],
            "open_point": "CMP · only at failed Publication Front locus",
            "stop_condition": (
                "After closed-book retrieval of CR chain and targeted CMP reopen at failures. "
                "stop before claiming Approver clearance, until-exam trust, or spine PASS"
            ),
            "out_of_scope_today": [
                "First-pass spine PASS",
                "Until-exam educational trust",
                "Approver honesty clearance from catalogue",
                "Topic 5.2 invention",
                "Certified Educational Coverage increase from catalogue alone",
                "Modifying Alpha/Beta packages",
            ],
            "annotation_task": "List stickiest CR LO before any CMP reopen",
            "attempt_before_reveal": "Attempt closed-book retrieval before any CMP reopen",
            "worked_examples_cue": (
                "If a locus fails, reopen CMP only there. Attempt the failed step before "
                "uncovering."
            ),
            "exit_line": (
                "Keep CMP closed for first-pass retrieval. Reopen only at failed loci. "
                "Kwalitec is the guide; the CMP is authoritative. Stop when retrieval + "
                "targeted reopen are done: refuse Approver clearance, spine PASS, and "
                "until-exam claims."
            ),
            "return_cue": (
                "You are finished when CR Learning LOs are retrieved closed-book (with "
                "targeted reopen only where needed) and forbidden claims are refused."
            ),
            "pause_points": [
                {
                    "id": "PP1",
                    "cue": "Pause. Name the stickiest Publication Front LO before reopen.",
                    "student_action": "Annotate",
                },
                {
                    "id": "PP2",
                    "cue": "Attempt closed-book retrieval before uncovering CMP text.",
                    "student_action": "Attempt",
                },
            ],
            "reentry_line": (
                "Welcome back. Keep your CMP closed unless returning to a failed locus. "
                "Immediate next: Knowledge Checks."
            ),
        },
        "knowledge_checks": [
            {
                "episode_id": "lep-cs1017-cr-r1-ar-01",
                "kind": "active_recall",
                "item_id": "cs1017-cr-r1-ar-01",
                "title": "Active Recall: Publication Front chain",
                "prompt": (
                    "Closed-book. List the nine CR Learning LOs in order and give one warrant "
                    "sentence for your stickiest LO."
                ),
                "response_type": "short_structured",
                "body": "Retrieve Publication Front chain closed-book.",
                "hints": ["Order: 1.1.1→2.1.2.", "One sticky warrant."],
                "accepted_keywords": [
                    "1.1.1",
                    "1.2.1",
                    "2.1.1",
                    "2.1.2",
                    "retrieval",
                ],
                "explanation": "Active recall for CR-R1.",
                "model_answer": (
                    "Chain: 1.1.1–1.1.4, 1.2.1–1.2.3, 2.1.1–2.1.2. Name the stickiest LO with "
                    "one warrant."
                ),
                "common_mistake": "Skipping order or claiming Approver clearance.",
                "success_criteria": ["Order present.", "Sticky warrant present."],
            },
            {
                "episode_id": "lep-cs1017-cr-r1-cp-01",
                "kind": "checkpoint",
                "item_id": "cs1017-cr-r1-cp-01",
                "title": "Checkpoint: opening-arc revision honesty",
                "prompt": (
                    "Closed-book. A colleague says 'Placing continuous families means aims, "
                    "reproducibility, EDA, and discrete matching are all solid.' Refuse; name "
                    "the weakest link on today's retrieval chain; name one concrete residual "
                    "to rework."
                ),
                "response_type": "short_structured",
                "body": "Refuse Approver / spine / until-exam swallow after Revision.",
                "hints": ["Name Approver residual.", "Refuse until-exam."],
                "accepted_keywords": ["refuse", "Approver", "spine", "until-exam"],
                "explanation": "Checkpoint for CR-R1.",
                "model_answer": (
                    "Refuse: Publication Front Revision ≠ Approver honesty clearance, ≠ "
                    "first-pass spine PASS, ≠ until-exam trust. Honest residual: human "
                    "Publication Approver seals remain required; Coverage stays 63/72 until "
                    "sealed."
                ),
                "common_mistake": "Accepting Approver clearance from catalogue.",
                "success_criteria": ["Refusal present.", "Approver residual named."],
            },
        ],
        "reflection": {
            "framing": "Harvest Publication Front wobble: Approver residual remains open.",
            "prompt": (
                "Which link retrieved least cleanly today. Analysis aims, reproducibility, "
                "EDA summaries/association, PCA limits, discrete families, or continuous "
                "placement. And why? What one concrete rework will you schedule? Do not "
                "claim probability/quantile evaluation or later chapters are finished."
            ),
            "prompts": [
                "Which Publication Front LO is stickiest and why?",
                "What one rework plan will you keep?",
                "What claim must you refuse after Revision?",
            ],
        },
        "tomorrow_preview": {
            "next_topic_code": "APPROVER",
            "next_topic_title": "Honest stop / Publication Approver residual (not cleared)",
            "continuity_line": (
                "Today you closed Campaign Rho Revision; next is an honest stop with "
                "Publication Approver ownership still required. Not until-exam trust."
            ),
            "light_prep_cue": (
                "No new LO tonight: rest or jot the stickiest Publication Front LO"
            ),
            "student_facing": (
                "Honest next: stop / Publication Approver residual. Do not claim first-pass "
                "spine PASS, until-exam trust, or Approver clearance from Rho catalogue alone."
            ),
        },
        "revision_linkage": {
            "returns_on": "CR-R1",
            "campaign_revision_package": pid,
            "note": "Terminal Revision for Campaign Rho Publication Front chain.",
        },
    }


LEARNING = [
    dict(
        day="CR-D1",
        stem="1.1.1-aims-analysis-cs1017",
        pid="CS1-EP001-PKG-CR-1.1-AIMS-ANALYSIS",
        lo="1.1.1",
        topic_code="1.1",
        topic_title="Purpose and function of data analysis",
        slug="1.1-aims-analysis",
        keywords=["aims", "descriptive", "inferential", "predictive", "publication"],
        title="Aims of a data analysis (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.1.1 aims of data analysis under "
            "Publication Front / Wave 0 residual discipline after Memory Front LIVE. Without "
            "pretending stages/tools (1.1.2) are finished or Approver honesty is cleared."
        ),
        tutor=(
            "Today I will force aims classification (descriptive / inferential / predictive) "
            "and refuse 'Publication Front finished stages/tools / Approver clearance'."
        ),
        edu=(
            "Produce Publication Front LO-per-day study of analysis aims as the lawful first "
            "day after Memory Front close."
        ),
        lo_text="Aims of a data analysis (e.g. descriptive, inferential and predictive)",
        focus=(
            """Stated task → classify aim (descriptive / inferential / predictive) → refuse collapsing all aims into EDA."""
        ),
        prior=(
            "Yesterday you closed Campaign Pi Revision (Memory Front). Today opens Publication "
            "Front / Wave 0 residual at Syllabus 1.1.1."
        ),
        why=(
            "Start the opening analysis arc at aims: descriptive, inferential, and predictive intents."
        ),
        benefit=(
            """You will be able to classify actuarial analysis aims as descriptive, inferential, or predictive and refuse EDA-as-everything."""
        ),
        explain=(
            "Day 1 opens the analysis arc at aims. The natural start for opening syllabus work."
        ),
        criteria=[
            "Closed-book, distinguish descriptive, inferential, and predictive aims in one "
            "careful trio.",
            "State why this is Publication Front catalogue work not Approver clearance.",
            "Refuse one stages/tools / Approver swallow.",
        ],
        tasks=[
            "Sketch aims map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.1.1.",
            "Closed-book Knowledge Checks: aims + refuse swallow.",
        ],
        next_code="1.1",
        next_title="Stages and tools (1.1.2)",
        cont="Today you studied 1.1.1; tomorrow continues Publication Front at 1.1.2.",
        prep="Optional: glance at CMP headings for Syllabus 1.1.2. Titles only tonight",
        student=(
            "Tomorrow: stages and tools Publication Front day (1.1.2). Optional light prep: "
            "skim 1.1.2 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.1.1 aims of a data analysis",
        stop="Through the CMP treatment of Syllabus 1.1.1 (stop before stages/tools primary 1.1.2)",
        oos=[
            "Stages and tools as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for collapsing all aims into 'EDA'.",
            "Watch for swallowing 1.1.2 today.",
            "Watch for claiming Approver clearance from one LO.",
        ],
        ar_prompt=(
            "Closed-book. (1) Name three analysis aims. (2) Give one warrant that separates "
            "inferential from predictive. (3) Why is 1.1.2 not today's primary?"
        ),
        ar_kw=["descriptive", "inferential", "predictive", "aims"],
        ar_model=(
            "Descriptive summarises; inferential generalises from sample evidence; predictive "
            "forecasts. Stages/tools open tomorrow."
        ),
        cp_prompt=(
            """Closed-book. Motor pricing review tasks: (A) histogram of last year's claim severities; (B) a confidence interval for mean severity; (C) a model that forecasts next year's severity. (1) Classify each as descriptive, inferential, or predictive. (2) Refuse: 'All three are just EDA, so aims are done.'"""
        ),
        cp_kw=["descriptive", "inferential", "predictive", "aims", "refuse", "EDA"],
        cp_model=(
            """(1) A descriptive (summarise observed severities); B inferential (generalise from sample evidence to a parameter); C predictive (forecast future severity). (2) Refuse: EDA is exploratory summarising. It does not replace naming distinct descriptive, inferential, and predictive aims."""
        ),
        reflect="Harvest aims wobble: stages/tools continue Publication Front tomorrow.",
    ),
    dict(
        day="CR-D2",
        stem="1.1.2-stages-tools-cs1017",
        pid="CS1-EP001-PKG-CR-1.1-STAGES-TOOLS",
        lo="1.1.2",
        topic_code="1.1",
        topic_title="Purpose and function of data analysis",
        slug="1.1-stages-tools",
        keywords=["stages", "tools", "workflow", "publication"],
        title="Stages and tools for data analysis (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.1.2 stages and tools under Publication "
            "Front discipline. Without pretending data sources (1.1.3) are finished."
        ),
        tutor=(
            "Today I will force stages/tools warrant and refuse 'Publication Front finished "
            "data sources / Approver clearance'."
        ),
        edu="Produce contiguous Publication Front study of analysis stages and suitable tools.",
        lo_text=(
            "Stages and suitable tools used to conduct a data analysis to solve real-world "
            "problems"
        ),
        focus="Analysis stages in order \u2192 suitable tool class per stage \u2192 refuse tool-shopping-without-stages.",
        prior="Yesterday you studied analysis aims (1.1.1). Today continues Publication Front.",
        why="Stages/tools convert aims into an executable analysis path.",
        benefit=(
            """You will be able to list analysis stages in a sensible order and pair a stage with a suitable tool class."""
        ),
        explain=(
            "Day 2 focuses preserves opening."
            "contiguity after aims."
        ),
        criteria=[
            "Closed-book, outline analysis stages in order.",
            "Name one suitable tool class for a named stage.",
            "Refuse one data-sources / Approver swallow.",
        ],
        tasks=[
            "Sketch stages map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.1.2.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="1.1",
        next_title="Data sources (1.1.3)",
        cont="Today you studied 1.1.2; tomorrow continues Publication Front at 1.1.3.",
        prep="Optional: glance at CMP headings for Syllabus 1.1.3. Titles only tonight",
        student=(
            "Tomorrow: data sources Publication Front day (1.1.3). Optional light prep: skim "
            "1.1.3 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.1.2 stages and suitable tools",
        stop="Through the CMP treatment of Syllabus 1.1.2 (stop before data sources primary 1.1.3)",
        oos=[
            "Data sources as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for tool-shopping without stages.",
            "Watch for swallowing data sources today.",
            "Watch for claiming Section 1 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) List analysis stages. (2) Pair one stage with a suitable tool "
            "class. (3) Why is 1.1.3 not today's primary?"
        ),
        ar_kw=["stages", "tools", "workflow", "analysis"],
        ar_model=(
            "Stages structure the analysis path; tools serve stages. Data sources open tomorrow."
        ),
        cp_prompt=(
            """Closed-book. You are running a reserves data analysis. (1) List the main stages in a sensible order and mark which stage exploratory work sits in. (2) Pair the clean/explore stage with one suitable tool class. (3) Refuse: 'I opened a notebook and loaded packages, so the analysis stages are finished.'"""
        ),
        cp_kw=["stages", "tools", "explore", "EDA", "refuse", "order"],
        cp_model=(
            """(1) Define aim → obtain data → clean/explore → analyse (infer or predict) → communicate; EDA sits in clean/explore. (2) Clean/explore pairs with summary statistics and exploratory visualisations (or data-wrangling scripts). (3) Refuse: opening tools is not completing the staged analysis path."""
        ),
        reflect="Harvest stages/tools wobble: data sources continue Publication Front tomorrow.",
    ),
    dict(
        day="CR-D3",
        stem="1.1.3-data-sources-cs1017",
        pid="CS1-EP001-PKG-CR-1.1-DATA-SOURCES",
        lo="1.1.3",
        topic_code="1.1",
        topic_title="Purpose and function of data analysis",
        slug="1.1-data-sources",
        keywords=["sources", "characteristics", "large", "publication"],
        title="Data sources and large data sets (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.1.3 data sources under Publication "
            "Front discipline. Without pretending reproducible research (1.1.4) is finished."
        ),
        tutor=(
            "Today I will force source characteristics warrant and refuse 'Publication Front "
            "finished reproducibility / Approver clearance'."
        ),
        edu="Produce contiguous Publication Front study of data sources including large sets.",
        lo_text=(
            "Sources of data and their characteristics, including extremely large data sets"
        ),
        focus="Source type \u2192 trust/quality characteristics (incl. scale) \u2192 refuse bigger-equals-better.",
        prior="Yesterday you studied stages/tools (1.1.2). Today continues Publication Front.",
        why="Source honesty precedes reproducible analysis claims.",
        benefit=(
            """You will be able to name source characteristics that change how you trust results, including constraints from large data sets."""
        ),
        explain=(
            "Day 3 focuses places source."
            "characteristics before reproducibility."
        ),
        criteria=[
            "Closed-book, name source types and one scale characteristic.",
            "State one risk of ignoring source characteristics.",
            "Refuse one reproducibility / Approver swallow.",
        ],
        tasks=[
            "Sketch sources map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.1.3.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="1.1",
        next_title="Reproducible research (1.1.4)",
        cont="Today you studied 1.1.3; tomorrow continues Publication Front at 1.1.4.",
        prep="Optional: glance at CMP headings for Syllabus 1.1.4. Titles only tonight",
        student=(
            "Tomorrow: reproducible research Publication Front day (1.1.4). Optional light "
            "prep: skim 1.1.4 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.1.3 sources of data and large data sets",
        stop=(
            "Through the CMP treatment of Syllabus 1.1.3 (stop before reproducible research "
            "primary 1.1.4)"
        ),
        oos=[
            "Reproducible research as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for treating 'big data' as automatically better data.",
            "Watch for swallowing reproducibility today.",
            "Watch for claiming Section 1 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) Name source types. (2) Name one large-set characteristic. "
            "(3) Why is 1.1.4 not today's primary?"
        ),
        ar_kw=["sources", "characteristics", "large", "data"],
        ar_model=(
            "Sources differ in origin and quality; large sets add scale constraints. "
            "Reproducibility opens tomorrow."
        ),
        cp_prompt=(
            """Closed-book. Compare an administrative claims extract with a voluntary customer survey, both used for the same pricing question. (1) Name two source characteristics that change how you trust results. (2) Name one characteristic of an extremely large data set that constrains analysis. (3) Refuse: 'The bigger file is automatically better data.'"""
        ),
        cp_kw=["sources", "bias", "granularity", "large data", "refuse", "quality"],
        cp_model=(
            """(1) Examples: selection/response bias (voluntary survey vs administrative coverage); granularity or completeness of fields; measurement error. (2) Scale constraints: storage/compute limits, need for sampling or distributed tooling, or quality issues that volume does not fix. (3) Refuse: volume alone does not imply representativeness or fitness for the analysis aim."""
        ),
        reflect=(
            "Harvest sources wobble: reproducible research continues Publication Front tomorrow."
        ),
    ),
    dict(
        day="CR-D4",
        stem="1.1.4-reproducible-cs1017",
        pid="CS1-EP001-PKG-CR-1.1-REPRODUCIBLE",
        lo="1.1.4",
        topic_code="1.1",
        topic_title="Purpose and function of data analysis",
        slug="1.1-reproducible",
        keywords=["reproducible", "research", "elements", "publication"],
        title="Reproducible research (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.1.4 reproducible research under "
            "Publication Front discipline. Without pretending EDA summaries (1.2.1) are finished."
        ),
        tutor=(
            "Today I will force reproducibility elements warrant and refuse 'Publication "
            "Front finished EDA / Approver clearance'."
        ),
        edu="Produce contiguous Publication Front study of reproducibility elements.",
        lo_text=(
            "Meaning and value of reproducible research and the elements required to ensure "
            "a data analysis is reproducible"
        ),
        focus=(
            """Reproducibility meaning → required elements (data, code, docs) → refuse one-off-rerun-as-reproducible."""
        ),
        prior="Yesterday you studied data sources (1.1.3). Today continues Publication Front.",
        why="Reproducibility closes Topic 1.1 before EDA entry.",
        benefit=(
            """You will be able to state what reproducible research means and name elements required to keep a data analysis reproducible."""
        ),
        explain=(
            "Day 4 focuses the named learning objective. Closes Topic 1.1 at "
            "reproducibility before EDA."
        ),
        criteria=[
            "Closed-book, state meaning/value of reproducible research.",
            "List required elements at foundation level.",
            "Refuse one EDA / Approver swallow.",
        ],
        tasks=[
            "Sketch reproducibility checklist before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.1.4.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="1.2",
        next_title="EDA summaries and visuals (1.2.1)",
        cont="Today you studied 1.1.4; tomorrow continues Publication Front at 1.2.1.",
        prep="Optional: glance at CMP headings for Syllabus 1.2.1. Titles only tonight",
        student=(
            "Tomorrow: EDA summaries Publication Front day (1.2.1). Optional light prep: skim "
            "1.2.1 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.1.4 reproducible research",
        stop="Through the CMP treatment of Syllabus 1.1.4 (stop before EDA primary 1.2.1)",
        oos=[
            "EDA summaries as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for equating reproducibility with 'rerun the notebook once'.",
            "Watch for swallowing EDA today.",
            "Watch for claiming Section 1 complete as Approver clearance.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does reproducible research mean? (2) Name required "
            "elements. (3) Why is 1.2.1 not today's primary?"
        ),
        ar_kw=["reproducible", "elements", "analysis", "research"],
        ar_model=(
            "Reproducible research lets others reconstruct the analysis; elements include "
            "data, code, and documentation warrants. EDA opens tomorrow."
        ),
        cp_prompt=(
            """Closed-book. A colleague says their pricing analysis is reproducible because they can re-run one notebook cell on their laptop. (1) In one sentence, what does reproducible research mean? (2) Name two elements required to keep an analysis reproducible. (3) Refuse the colleague's claim in one sentence."""
        ),
        cp_kw=["reproducible", "versioned", "scripted", "documentation", "refuse", "reconstruct"],
        cp_model=(
            """(1) Others (or a future you) can reconstruct the same analysis results from the stated inputs and steps. (2) Examples: versioned data (or clear extract identity); scripted code path; documented environment/parameters and decisions. (3) Refuse: a one-off local re-run without shared data, code, and documentation is not reproducibility."""
        ),
        reflect="Harvest reproducibility wobble. EDA continues Publication Front tomorrow.",
    ),
    dict(
        day="CR-D5",
        stem="1.2.1-eda-summaries-cs1017",
        pid="CS1-EP001-PKG-CR-1.2-EDA-SUMMARIES",
        lo="1.2.1",
        topic_code="1.2",
        topic_title="Complete exploratory data analysis",
        slug="1.2-eda-summaries",
        keywords=["EDA", "summary", "visualisation", "publication"],
        title="EDA summaries and visualisations (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.2.1 EDA summaries/visuals under "
            "Publication Front discipline. Without pretending correlation (1.2.2) is finished."
        ),
        tutor=(
            "Today I will force summary/visual tool warrant and refuse 'Publication Front "
            "finished correlation / Approver clearance'."
        ),
        edu="Produce Publication Front study of EDA summary statistics and visualisations.",
        lo_text=(
            "Appropriate tools to calculate suitable summary statistics and undertake "
            "exploratory data visualisations"
        ),
        focus=(
            """Variable type → suitable summary → suitable visualisation → aim alignment → refuse mean-only / pie misuse."""
        ),
        prior="Yesterday you studied reproducibility (1.1.4). Today opens Topic 1.2 on Publication Front.",
        why="EDA entry is the next contiguous opening honesty LO after Topic 1.1 close.",
        benefit=(
            """You will be able to choose a summary-and-plot pair for a named EDA aim and refuse a visualisation misuse."""
        ),
        explain=(
            "Day 5 focuses opens EDA at summaries."
            "before association measures."
        ),
        criteria=[
            "Closed-book, name suitable summary tools and one visualisation class.",
            "State why tool choice depends on the analysis aim.",
            "Refuse one correlation / Approver swallow.",
        ],
        tasks=[
            "Sketch EDA tool map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.2.1.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="1.2",
        next_title="Correlation measures (1.2.2)",
        cont="Today you studied 1.2.1; tomorrow continues Publication Front at 1.2.2.",
        prep="Optional: glance at CMP headings for Syllabus 1.2.2. Titles only tonight",
        student=(
            "Tomorrow: correlation Publication Front day (1.2.2). Optional light prep: skim "
            "1.2.2 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.2.1 summary statistics and exploratory visualisations",
        stop="Through the CMP treatment of Syllabus 1.2.1 (stop before correlation primary 1.2.2)",
        oos=[
            "Correlation measures as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for plotting without a question.",
            "Watch for swallowing correlation today.",
            "Watch for claiming Topic 1.2 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) Name summary tools. (2) Name one visualisation class. (3) Why "
            "is 1.2.2 not today's primary?"
        ),
        ar_kw=["summary", "visualisation", "EDA", "tools"],
        ar_model=(
            "Summaries and visuals explore structure before formal association measures. "
            "Correlation opens tomorrow."
        ),
        cp_prompt=(
            """Closed-book. Claim counts per policy-year: many zeros, a long right tail of large counts. Aim: explore the frequency shape before modelling. (1) Name one exploratory visualisation you would use and what pattern it should reveal. (2) Name one visualisation or summary misuse you would refuse for this aim."""
        ),
        cp_kw=["EDA", "summary", "visualisation", "histogram", "refuse", "zero"],
        cp_model=(
            """(1) A bar/histogram of counts (or a zero-aware frequency plot) to reveal the mass at zero and the right tail. (2) Refuse a pie chart of policies or a mean-only table that hides zero-inflation and the tail."""
        ),
        reflect="Harvest EDA wobble: correlation continues Publication Front tomorrow.",
    ),
    dict(
        day="CR-D6",
        stem="1.2.2-correlation-cs1017",
        pid="CS1-EP001-PKG-CR-1.2-CORRELATION",
        lo="1.2.2",
        topic_code="1.2",
        topic_title="Complete exploratory data analysis",
        slug="1.2-correlation",
        keywords=["Pearson", "Spearman", "Kendall", "correlation", "publication"],
        title="Correlation measures (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.2.2 correlation measures under "
            "Publication Front discipline. Without pretending PCA (1.2.3) is finished."
        ),
        tutor=(
            "Today I will force Pearson/Spearman/Kendall warrant and refuse 'Publication "
            "Front finished PCA / Approver clearance'."
        ),
        edu="Produce Publication Front study of bivariate correlation measures and inference.",
        lo_text=(
            "Interpret and make statistical inferences using Pearson’s, Spearman’s and "
            "Kendall’s measures of correlation for bivariate data"
        ),
        focus=(
            """Measure choice (Pearson / Spearman / Kendall) → what association means → refuse causation / linearity overclaim."""
        ),
        prior="Yesterday you studied EDA summaries (1.2.1). Today continues Publication Front.",
        why="Association measures sit between summaries and dimensionality reduction.",
        benefit=(
            """You will be able to justify a correlation measure for bivariate data and state one inferential limit of a large coefficient."""
        ),
        explain=(
            "Day 6 focuses places correlation."
            "before PCA."
        ),
        criteria=[
            "Closed-book, distinguish Pearson, Spearman, and Kendall at foundation level.",
            "State one inference caution for bivariate correlation.",
            "Refuse one PCA / Approver swallow.",
        ],
        tasks=[
            "Sketch correlation measure map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.2.2.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="1.2",
        next_title="Principal component analysis (1.2.3)",
        cont="Today you studied 1.2.2; tomorrow continues Publication Front at 1.2.3.",
        prep="Optional: glance at CMP headings for Syllabus 1.2.3. Titles only tonight",
        student=(
            "Tomorrow: PCA Publication Front day (1.2.3). Optional light prep: skim 1.2.3 "
            "headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.2.2 correlation measures for bivariate data",
        stop="Through the CMP treatment of Syllabus 1.2.2 (stop before PCA primary 1.2.3)",
        oos=[
            "PCA as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for equating correlation with causation.",
            "Watch for swallowing PCA today.",
            "Watch for claiming Topic 1.2 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) Distinguish Pearson, Spearman, Kendall. (2) Name one inference "
            "caution. (3) Why is 1.2.3 not today's primary?"
        ),
        ar_kw=["Pearson", "Spearman", "Kendall", "correlation"],
        ar_model=(
            "Pearson is linear association; Spearman/Kendall are rank-based. PCA opens tomorrow."
        ),
        cp_prompt=(
            """Closed-book. Years licensed vs claim frequency: frequency is skewed with visible outliers; the scatter looks roughly decreasing but nonlinear. (1) Which correlation measure would you prefer and why? (2) State one claim a large coefficient still does not justify."""
        ),
        cp_kw=["Spearman", "Pearson", "Kendall", "correlation", "causation", "refuse"],
        cp_model=(
            """(1) Prefer Spearman (or Kendall) because the relationship looks monotone but nonlinear and outliers can distort Pearson. (2) A large coefficient still does not prove that changing years licensed causes frequency to change."""
        ),
        reflect="Harvest correlation wobble. PCA continues Publication Front tomorrow.",
    ),
    dict(
        day="CR-D7",
        stem="1.2.3-pca-cs1017",
        pid="CS1-EP001-PKG-CR-1.2-PCA",
        lo="1.2.3",
        topic_code="1.2",
        topic_title="Complete exploratory data analysis",
        slug="1.2-pca",
        keywords=["PCA", "dimensionality", "components", "publication"],
        title="Principal component analysis (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 1.2.3 PCA under Publication Front "
            "discipline. Without pretending discrete distributions (2.1.1) are finished."
        ),
        tutor=(
            "Today I will force PCA dimensionality-reduction warrant and refuse 'Publication "
            "Front finished discrete distributions / Approver clearance'."
        ),
        edu="Produce Publication Front study of PCA to reduce dimensionality.",
        lo_text=(
            "Principal component analysis to reduce the dimensionality of a complex data set"
        ),
        focus="Why reduce dimensions \u2192 what PCs capture \u2192 refuse PC-as-causal-driver theatre.",
        prior="Yesterday you studied correlation (1.2.2). Today closes Topic 1.2 on Publication Front.",
        why="PCA closes EDA before univariate distribution entry.",
        benefit=(
            """You will be able to state a lawful exploratory use of PCA and refuse treating a principal component as a proven causal factor."""
        ),
        explain=(
            "Day 7 focuses the named learning objective. Closes Topic 1.2 at PCA "
            "before discrete distributions."
        ),
        criteria=[
            "Closed-book, state PCA purpose for dimensionality reduction.",
            "Name what a principal component represents at foundation level.",
            "Refuse one discrete-distributions / Approver swallow.",
        ],
        tasks=[
            "Sketch PCA purpose map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 1.2.3.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="2.1",
        next_title="Discrete distributions (2.1.1)",
        cont="Today you studied 1.2.3; tomorrow continues Publication Front at 2.1.1.",
        prep="Optional: glance at CMP headings for Syllabus 2.1.1. Titles only tonight",
        student=(
            "Tomorrow: discrete distributions Publication Front day (2.1.1). Optional light "
            "prep: skim 2.1.1 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 1.2.3 principal component analysis",
        stop=(
            "Through the CMP treatment of Syllabus 1.2.3 (stop before discrete distributions "
            "primary 2.1.1)"
        ),
        oos=[
            "Discrete distributions as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
        ],
        misconceptions=[
            "Watch for treating PCA as automatic feature selection without warrant.",
            "Watch for swallowing discrete distributions today.",
            "Watch for claiming Section 1 complete as Approver clearance.",
        ],
        ar_prompt=(
            "Closed-book. (1) What does PCA reduce? (2) What is a principal component at "
            "foundation level? (3) Why is 2.1.1 not today's primary?"
        ),
        ar_kw=["PCA", "dimensionality", "component", "variance"],
        ar_model=(
            "PCA reduces dimensionality via components capturing variation structure. Discrete "
            "distributions open tomorrow."
        ),
        cp_prompt=(
            """Closed-book. A colleague says: 'PC1 from our rating factors is the true underlying risk score, so we can treat it as a causal driver and auto-decline on PC1 alone.' (1) What one useful thing might PC1 still be doing exploratorily? (2) State one claim this statement overreaches."""
        ),
        cp_kw=["PCA", "dimension", "variation", "causal", "refuse", "exploratory"],
        cp_model=(
            """(1) PC1 may usefully summarise major shared variation among correlated rating factors for exploration or visualisation. (2) It does not by itself prove a causal risk driver or justify auto-decline without external subject-matter and decision warrants."""
        ),
        reflect=(
            "Harvest PCA wobble: discrete distributions continue Publication Front tomorrow."
        ),
    ),
    dict(
        day="CR-D8",
        stem="2.1.1-discrete-cs1017",
        pid="CS1-EP001-PKG-CR-2.1-DISCRETE",
        lo="2.1.1",
        topic_code="2.1",
        topic_title=(
            "Understand the characteristics of basic univariate distributions and how to "
            "generate samples from them"
        ),
        slug="2.1-discrete",
        keywords=["discrete", "binomial", "Poisson", "geometric", "publication"],
        title="Discrete distributions (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 2.1.1 discrete distributions under "
            "Publication Front discipline. Without pretending continuous distributions "
            "(2.1.2) are finished."
        ),
        tutor=(
            "Today I will force discrete family recognition and refuse 'Publication Front "
            "finished continuous distributions / Approver clearance'."
        ),
        edu="Produce Publication Front study of named discrete distributions on a finite set.",
        lo_text=(
            "Geometric, binomial, negative binomial, hypergeometric, Poisson and uniform "
            "discrete distributions on a finite set"
        ),
        focus=(
            """Counting / selection situation → discrete family → defining characteristic → refuse mismatched family."""
        ),
        prior="Yesterday you studied PCA (1.2.3). Today opens Topic 2.1 on Publication Front.",
        why="Discrete families are the first univariate distribution honesty LO still AA.",
        benefit=(
            """You will be able to match a discrete data-generating situation to a syllabus family and refuse a habitual mismatch."""
        ),
        explain=(
            "Day 8 focuses places discrete."
            "families before continuous families."
        ),
        criteria=[
            "Closed-book, name the discrete families in scope.",
            "State one distinguishing warrant between two named families.",
            "Refuse one continuous / Approver swallow.",
        ],
        tasks=[
            "Sketch discrete family map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.1.1.",
            "Closed-book Knowledge Checks.",
        ],
        next_code="2.1",
        next_title="Continuous distributions (2.1.2)",
        cont="Today you studied 2.1.1; tomorrow continues Publication Front at 2.1.2.",
        prep="Optional: glance at CMP headings for Syllabus 2.1.2. Titles only tonight",
        student=(
            "Tomorrow: continuous distributions Publication Front day (2.1.2). Optional light "
            "prep: skim 2.1.2 headings. Titles only tonight."
        ),
        open="CMP · Syllabus 2.1.1 discrete distributions",
        stop=(
            "Through the CMP treatment of Syllabus 2.1.1 (stop before continuous distributions "
            "primary 2.1.2)"
        ),
        oos=[
            "Continuous distributions as primary",
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
            "Probabilities/quantiles (2.1.3) as primary",
        ],
        misconceptions=[
            "Watch for mixing discrete support with continuous density language.",
            "Watch for swallowing continuous families today.",
            "Watch for claiming Topic 2.1 complete.",
        ],
        ar_prompt=(
            "Closed-book. (1) List discrete families in scope. (2) Give one distinguishing "
            "warrant. (3) Why is 2.1.2 not today's primary?"
        ),
        ar_kw=["geometric", "binomial", "Poisson", "discrete"],
        ar_model=(
            "Named discrete families share discrete support with distinct generative stories. "
            "Continuous families open tomorrow."
        ),
        cp_prompt=(
            """Closed-book. (1) For a single policy, you model the number of claims in a fixed year with a constant rare-event rate and independent increments. Which discrete family fits, and why? (2) Name one family that would be a habitual mismatch here, and refuse it in one sentence."""
        ),
        cp_kw=["Poisson", "discrete", "count", "rate", "refuse", "family"],
        cp_model=(
            """(1) Poisson: counts of rare events in a fixed interval under a constant rate / independent-increments story. (2) Refuse continuous Normal for a non-negative integer count, or refuse hypergeometric if there is no without-replacement draw from a finite success/failure population."""
        ),
        reflect=(
            "Harvest discrete wobble: continuous distributions continue Publication Front "
            "tomorrow."
        ),
    ),
    dict(
        day="CR-D9",
        stem="2.1.2-continuous-cs1017",
        pid="CS1-EP001-PKG-CR-2.1-CONTINUOUS",
        lo="2.1.2",
        topic_code="2.1",
        topic_title=(
            "Understand the characteristics of basic univariate distributions and how to "
            "generate samples from them"
        ),
        slug="2.1-continuous",
        keywords=["continuous", "normal", "gamma", "exponential", "publication"],
        title="Continuous distributions (Publication Front)",
        purpose=(
            "Today's Mission exists to study Syllabus 2.1.2 continuous distributions under "
            "Publication Front discipline. Without pretending Approver clearance, first-pass "
            "spine PASS, or until-exam trust."
        ),
        tutor=(
            "Today I will force continuous family recognition and refuse 'Publication Front "
            "cleared Approver honesty / finished spine / unlocked until-exam'."
        ),
        edu=(
            "Produce Publication Front study of named continuous distributions as the Learning "
            "close before Revision."
        ),
        lo_text=(
            "Normal, lognormal, exponential, gamma, chi-square, t, F, beta and uniform "
            "continuous distributions on an interval"
        ),
        focus="Support / shape story \u2192 continuous family \u2192 refuse Normal-by-default for mismatched response.",
        prior=(
            "Yesterday you studied discrete distributions (2.1.1). Today closes Publication "
            "Front Learning."
        ),
        why=(
            "Place continuous families to close this opening stretch. Then revise the "
            "analysis-to-distributions chain."
        ),
        benefit=(
            """You will be able to place a continuous family from support and shape and refuse Normal-by-default for a mismatched quantity."""
        ),
        explain=(
            "Day 9 closes the opening stretch at continuous families. Then revise the chain."
        ),
        criteria=[
            "Closed-book, name continuous families in scope.",
            "State one distinguishing warrant between two named families.",
            "Refuse one Approver / spine / until-exam clearance claim.",
        ],
        tasks=[
            "Sketch continuous family map before CMP.",
            "Complete Guided Reading through CMP treatment of Syllabus 2.1.2.",
            "Closed-book Knowledge Checks: families + refuse Approver swallow.",
        ],
        next_code="CR-R1",
        next_title="Campaign Rho Revision: retrieve Publication Front chain",
        cont=(
            "Today you closed Publication Front Learning at continuous distributions; tomorrow "
            "is Campaign Rho Revision returning to the CR chain."
        ),
        prep=(
            "No new LO tonight: rest or jot the stickiest Publication Front LO for Revision"
        ),
        student=(
            "Tomorrow: CR-R1 Revision of Publication Front LOs. Optional: note your weakest "
            "LO. Titles only tonight."
        ),
        open="CMP · Syllabus 2.1.2 continuous distributions",
        stop=(
            "Through the CMP treatment of Syllabus 2.1.2 (stop before terminal Revision as "
            "Learning; no Approver / spine / until-exam claim)"
        ),
        oos=[
            "First-pass spine PASS",
            "Until-exam educational trust",
            "Approver honesty clearance",
            "Probabilities/quantiles (2.1.3) as primary Learning today",
            "Topic 5.2 invention",
            "Certified Educational Coverage increase from catalogue alone",
            "Modifying Alpha/Beta packages",
        ],
        misconceptions=[
            "Watch for claiming Approver clearance from Learning close.",
            "Watch for swallowing 2.1.3 as Rho Learning.",
            "Watch for skipping Revision.",
        ],
        ar_prompt=(
            "Closed-book. (1) List continuous families in scope. (2) Give one distinguishing "
            "warrant. (3) Name one reason this does not clear Approver honesty or finish "
            "first-pass spine."
        ),
        ar_kw=["normal", "gamma", "exponential", "continuous"],
        ar_model=(
            "Named continuous families share continuous support with distinct shape/scale "
            "stories. Approver seals and spine PASS remain out of scope."
        ),
        cp_prompt=(
            """Closed-book. Inter-claim waiting times are strictly positive and, under a constant hazard story, memoryless. (1) Which continuous family would you place first, and why? (2) Refuse Normal-by-default for this quantity in one sentence."""
        ),
        cp_kw=["exponential", "continuous", "waiting", "Normal", "refuse", "support"],
        cp_model=(
            """(1) Exponential: positive support and memoryless waiting times under a constant hazard. (2) Refuse Normal-by-default because a symmetric all-real support model mismatches strictly positive waiting times."""
        ),
        reflect=(
            "Harvest continuous-family wobble. Revision protects the Publication Front chain "
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
    (PKG_DIR / "revision-publication-front-cs1017.json").write_text(
        json.dumps(rev, indent=2) + "\n"
    )
    inventory.append(rev["package_id"])

    campaign = {
        "campaign_id": "CS1-EP001-CAMPAIGN-RHO",
        "campaign_version": "cs1017-1.0.0",
        "display_title": (
            "Campaign Rho. Publication Front Wave 0 residual after Memory Front LIVE"
        ),
        "subject_id": "CS1",
        "package_version_pin": "IFoA CS1 2026",
        "scope_class": "Pilot Arc",
        "cmp_edition": "IFoA CS1 Core Reading / CMP · 2026 syllabus alignment",
        "status": "authored_pending_gate_cg",
        "volume_id": "CS1-017",
        "prior_volume_id": "CS1-016",
        "day_count": {"learning": 9, "revision": 1, "total": 10},
        "syllabus_span": span,
        "front_class": "publication_front_wave0_residual",
        "out_of_scope": [
            "first-pass spine PASS",
            "until-examination educational trust",
            "Approver honesty clearance from catalogue alone",
            "Topic 5.2 invention / remainder theatre",
            "Trust Front whole-Delta absorb into Continuity Front credit",
            "Wave 16 authoring",
            "coverage mirage / Student Reliance increase from catalogue alone",
            "modifying existing Alpha/Beta packages",
            "LIVE copies in educational_packages/",
        ],
        "inventory": inventory,
        "wave0_note": (
            "Publication Front / Wave 0 Approver honesty gap remains open until human "
            "Publication Approver seals. Rho catalogue prepares LO-per-day Approver-path "
            "inventory; it must not claim clearance. Existing Alpha/Beta packages remain "
            "untouched honesty-gap loader inventory."
        ),
        "memory_front_note": (
            "CS1-016 / Campaign Pi remains independent Memory Front LIVE inventory. Rho "
            "package IDs are CR-prefixed Publication Front catalogue. Not LIVE this cycle; "
            "Published Coverage unchanged until Approver seals."
        ),
        "trust_front_note": (
            "CS1-003 / Campaign Delta remains independent Trust Front LIVE inventory for "
            "4.1–5.1. Rho does not absorb whole-Delta credit."
        ),
    }
    (OUT / "campaign.json").write_text(json.dumps(campaign, indent=2) + "\n")
    print(f"Wrote campaign + {len(list(PKG_DIR.glob('*.json')))} packages to {OUT}")


if __name__ == "__main__":
    main()

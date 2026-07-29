# FV-001A — Founder Blind Acceptance Review

**Programme:** Founder Validation Programme  
**Sub-programme:** FV-001A — Founder Blind Acceptance Review  
**Date:** 2026-07-28  
**Status:** Complete (independent acceptance report)  
**Reviewer persona:** First-time founder preparing CS1; actuarial exams known; Kwalitec terminology unknown  
**Method:** Visible product only (Playwright walkthrough of a clean instance). No architecture defence. No code fixes.

**Companion artefacts:** [`SCREEN_REVIEW_LOG.md`](SCREEN_REVIEW_LOG.md) · [`FIRST_IMPRESSIONS.md`](FIRST_IMPRESSIONS.md) · [`JOURNEY_TIMELINE.md`](JOURNEY_TIMELINE.md) · [`TERMINOLOGY_AUDIT.md`](TERMINOLOGY_AUDIT.md) · [`UX_FINDINGS.md`](UX_FINDINGS.md) · [`LAUNCH_BLOCKERS.md`](LAUNCH_BLOCKERS.md) · [`PRIORITISED_ACTIONS.md`](PRIORITISED_ACTIONS.md) · [`FINAL_VERDICT.md`](FINAL_VERDICT.md)

**Evidence:** [`_evidence/phases.json`](_evidence/phases.json) · [`_evidence/focus2.json`](_evidence/focus2.json) · [`_evidence/precise.json`](_evidence/precise.json)

---

## 1. Executive Summary

A first-time founder opening Kwalitec today meets a polished **invite-only student study OS** (Study Sensei, Mission, Session) and a separate **Kwalitec Console / Curriculum Studio** for content operations. The product does **not** successfully carry a founder from zero setup (new subject → syllabus/CMP upload → trusted curriculum → publish → enrolment → completed study session) using only what appears on screen.

Registration is impossible without a coordinator. After a provisioned sign-in (methodological exception), Create Subject and Open Workspace are achievable via Content → Curriculum Studio. Dummy PDF uploads are accepted into slots but show **STATUS Failed**, extraction yields **0 nodes**, and Publish correctly refuses incomplete material. The student Home shows a Mission and Start Session, but the mission/topic language is generic (“this topic”, “your topic”, “Core methods”), so the founder cannot answer *what* to study with confidence. There is no conversational Coach surface—only Help & Support.

**Recommendation: NO-GO** against the stated Version 1 zero-to-session founder journey success criteria. Constrained Internal Alpha dogfood on the student path remains a separate, narrower question (see Final Verdict).

---

## 2. Journey Success Rate

| Phase | Journey step | Outcome | Score /10 |
|---|---|---|---|
| 1 | Landing page | Partial — student value clear; founder “create CS1” path not | 6 |
| 2 | Registration | Fail — invite-only; no self-serve account | 2 |
| 3 | Founder dashboard (Console) | Partial — dense ops pulse; Content is findable | 4 |
| 4 | Create Subject | Pass — CS1X created with clear confirmation | 8 |
| 5 | Upload Syllabus | Partial — upload UI clear; file status Failed | 4 |
| 6 | Upload CMP | Partial — same; slot confusion risk | 4 |
| 7 | Curriculum Review | Fail — 0 nodes; nothing trustworthy to edit | 2 |
| 8 | Publish Curriculum | Fail — blocked (correctly); journey cannot finish | 3 |
| 9 | Student Enrolment / Study Plan | Partial — wizard clear for IFoA/CS1; not fully completed | 5 |
| 10 | Dashboard / Home | Partial — Mission hierarchy good; topic clarity poor | 5 |
| 11 | Mission | Partial — startable; content feels generic | 4 |
| 12 | Study Session | Partial — session opens; activities feel hollow | 4 |
| 13 | Session Completion | Fail — summary/accomplishment not reached | 1 |
| 14 | Revision Planner | Pass (empty-state) — honest and directional | 7 |
| 15 | Coach | Fail — no ask/answer Coach; Help only | 2 |
| 16 | Return Journey | Partial — sign-in works; continuity of study weak | 5 |

**Phases passed (Pass only):** 2 / 16 (Create Subject; Revision empty-state)  
**Phases partial:** 10 / 16  
**Phases failed:** 4 / 16  

**Weighted journey completion (Pass=1, Partial=0.5, Fail=0):** **≈ 44%**

---

## 3. Screen-by-Screen Scores

| Screen | Confidence | Launch blocker? |
|---|---|---|
| Sign-in / landing | 6/10 | No (for invite-only alpha messaging) |
| Registration (absent) | 2/10 | **Yes** for self-serve founder onboarding |
| Console Home | 4/10 | **Yes** for “what do I do first to prepare CS1?” |
| Curriculum Studio index | 7/10 | No |
| Create Subject confirmation | 8/10 | No |
| Workspace (Content Sources) | 5/10 | **Yes** if zero-setup publish is required |
| Upload result (Failed) | 3/10 | **Yes** |
| Validation / Preview (0 nodes) | 2/10 | **Yes** |
| Publish blocked | 6/10 (message quality) / 2/10 (journey) | **Yes** for end-to-end publish |
| Student onboarding | 7/10 | No |
| Study Plan wizard (IFoA/CS1) | 7/10 | No |
| Student Home | 5/10 | **Yes** for trust (“what topic?”) |
| Learning Activity session | 4/10 | **Yes** for “worth studying” |
| Revision empty state | 7/10 | No |
| Help & Support (Coach proxy) | 3/10 as Coach | **Yes** for Coach journey step |

Detail: [`SCREEN_REVIEW_LOG.md`](SCREEN_REVIEW_LOG.md)

---

## 4. Critical Issues

1. **No self-serve registration** — journey stops unless credentials are pre-provisioned.  
2. **Zero-setup curriculum path incomplete** — uploads Fail; 0 nodes; cannot publish a usable CS1 from dummy/official docs in this walkthrough.  
3. **Student Mission/topic opacity** — Home and Session do not name a real CS1 topic the founder recognises; confidence to study collapses.  
4. **No Coach to ask questions** — Phase 15 cannot be completed as specified.  
5. **Console Home first impression** — ops metrics (“Platform Health 0%”, Product Check-ins) do not answer “create CS1 / start studying”; founder must invent the path.

---

## 5. Major Issues

1. Workspace exposes **PIPELINE / KNOWLEDGE GRAPH / EVIDENCE EXPLORER / ENTITY DETAILS** — feels like an internal tools console, not a founder curriculum setup wizard.  
2. After Create Subject, founder must separately **Open Workspace** with the same code — easy to stall on “No workspaces yet”.  
3. Upload **STATUS Failed** without a plain-language recovery that restores trust.  
4. Session activities are generic free-text (“explain one key idea from Core methods”) with vague supporting material — does not feel like actuarial exam preparation.  
5. Dual surfaces (Console vs Student) without an explicit “I am setting up content” vs “I am studying” mode switch for a founder dogfooding both roles.  
6. Copy defects: double period in readiness sentence; “UPLOADED BY 1” (user id) on documents.

---

## 6. Minor Improvements

1. Distinguish landing hero for founders vs students (or a single clear “Get started” that branches).  
2. After subject create, primary CTA should be “Open workspace for CS1X” pre-filled.  
3. Soften or hide intelligence pipeline tabs until documents validate.  
4. Name the Mission topic in the Home card title.  
5. Help search alone is not a Coach—label it as Help, not mentor chat.  
6. Wizard radio cards: click targets should be large/stable (automation and humans both hesitate).

---

## 7. Terminology Problems

Observed on-screen terms that force mental translation (full audit: [`TERMINOLOGY_AUDIT.md`](TERMINOLOGY_AUDIT.md)):

| Term | Where | Severity |
|---|---|---|
| Education Operating System | Landing | Major (abstract) |
| Study Sensei | Student surfaces / Help | Observation → Major if mistaken for a chat Coach |
| Estimated Knowledge | Home readiness | Major |
| Decision Journal / Educational Timeline | Help, History | Major |
| Curriculum Intelligence Pipeline | Workspace | Critical for founder calm |
| Knowledge Graph / Evidence Explorer / Entity Details | Workspace tabs | Critical UX terminology |
| Platform Intelligence / Product Check-in | Console | Major |
| Official CMP | Workspace upload | Observation (actuarial founders may know CMP; still jargon for others) |

**Forbidden internal terms SCI / Runtime / Twin / Educational Decision:** not observed as primary student labels in this walkthrough. **Knowledge Graph / Pipeline / Estimated Knowledge / Decision Journal** still violate the spirit of “application explains itself.”

---

## 8. UX Strengths

1. Landing value props are concrete for a student (“what to study next”, exam-date plans, focused sessions).  
2. Invite-only copy is honest about how to get access.  
3. Curriculum Studio next-step hints and blocking validation findings explain *why* CMP/syllabus matter.  
4. Create Subject success flash and activity line (`subject_created: Created subject CS1X`) are clear.  
5. Publish refusal message protects students and tells the founder what is missing.  
6. Student Home hierarchy (Mission → Start Session → Readiness) is scannable within ten seconds for *action*, if not for *topic identity*.  
7. Revision empty state refuses to invent fake work and points back to Mission.  
8. Session step rail (Overview → Activity → Reflection → Summary) sets expectations.

---

## 9. Version 1 Launch Blockers

See [`LAUNCH_BLOCKERS.md`](LAUNCH_BLOCKERS.md). Summary:

| ID | Blocker |
|---|---|
| LB-01 | Self-serve account creation absent |
| LB-02 | Document upload → Failed; no trusted curriculum extraction |
| LB-03 | Cannot publish a founder-created subject to a student-ready state |
| LB-04 | Mission/session topic identity insufficient for trust |
| LB-05 | Coach journey step unavailable |
| LB-06 | Console Home does not orient a founder to “prepare CS1” |

---

## 10. Overall Product Score

**42 / 100**

Breakdown (approximate weights): discoverability 8/20 · setup completion 6/25 · study clarity 10/25 · trust & completion 8/20 · coach/continuity 10/10 → scaled to 42.

---

## 11. Recommendation

### **NO-GO**

Against the FV-001A success criterion: *complete the entire Version 1 founder journey from zero setup to a completed study session using only the visible product.*

Conditions that would reopen a later review (not granted now):

1. Provisioned-login path documented as the only onboarding (if intentional) **and** zero-setup Studio path produces a reviewable, editable curriculum from real PDFs.  
2. Mission and Session name real syllabus topics a CS1 candidate recognises.  
3. A visible Coach/ask surface exists, or Phase 15 is formally descopeed from Version 1.  
4. Session completion feedback shows what changed in plain language.

---

## Method notes (transparency)

- Clean local instance; Playwright headless Chromium; screenshots/JSON under `_evidence/`.  
- **Methodological exception:** after documenting registration failure, review continued with a provisioned founder account (simulating coordinator invite) so later phases could be observed. This does **not** convert Phase 2 to Pass.  
- Dummy PDFs were used for upload phases as specified; Failed status is recorded as observed, not excused.  
- No engineering changes were made during this review.

---

**End of Founder Blind Acceptance Review**

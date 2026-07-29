# FV-001A — Screen Review Log

**Date:** 2026-07-28  
**Template:** Screen · Objective · First Impression · Positives · Confusing · Mental model · Critical / Major / Minor · Launch blocker · Confidence  

---

## PHASE 1 — Landing / Sign-in

------------------------------------------------
**Screen:** `/auth/login` (root `/` redirects here)  
**Objective:** Understand what Kwalitec is and what to do first.  
**First Impression:** Polished split landing: “Education Operating System” / “Know exactly what to study next.” Feels like a student study product, not a “create a new IFoA subject” product.  
**Positive Observations:** Concrete feature bullets; Internal Alpha badge; honest invite-only note.  
**Confusing Elements:** No path labeled for founders creating curricula; “Education Operating System” is abstract.  
**Expected User Mental Model:** “This is an exam study app I sign into.”  
**Critical Issues:** None on this screen alone for invite-only alpha.  
**Major Issues:** Founder goal (create CS1) not represented.  
**Minor Improvements:** Hero could acknowledge operators/founders or offer “I have an invite.”  
**Launch Blocker:** No  
**Confidence Score:** 6/10  
------------------------------------------------

---

## PHASE 2 — Registration

------------------------------------------------
**Screen:** No registration UI. Tried `/auth/register`, `/register`, `/signup`, `/auth/signup`, `/join` → 404.  
**Objective:** Create an account.  
**First Impression:** Dead ends. Only “contact your coordinator.”  
**Positive Observations:** Invite-only messaging is explicit on login.  
**Confusing Elements:** A founder expecting Sign up finds nothing.  
**Expected User Mental Model:** “I should be able to create an account.”  
**Critical Issues:** Journey cannot start without external credentials.  
**Major Issues:** Password reset also “contact coordinator” only.  
**Minor Improvements:** Link to a public waitlist/contact form.  
**Launch Blocker:** Yes (for self-serve)  
**Confidence Score:** 2/10  
------------------------------------------------

*Method note: continued with provisioned credentials to observe later phases.*

---

## PHASE 3 — Founder Dashboard (Console Home)

------------------------------------------------
**Screen:** `/console/` — “Console Home”  
**Objective:** Know where I am and what to click to prepare CS1.  
**First Impression:** Operations centre: Attention Required, Platform Health 0%, Product Check-ins, Support inbox. Not a study desk and not an obvious “New subject” wizard.  
**Positive Observations:** Nav includes Content; Quick Action “Manage content” → Studio.  
**Confusing Elements:** Platform Health 0% / “Needs attention” with empty product; dual identity Console vs Student unclear.  
**Expected User Mental Model:** “I run a platform; something is wrong; I should open Attention Center.”  
**Critical Issues:** First ten seconds do not answer “create CS1 / start studying.”  
**Major Issues:** Ops language dominates educational intent.  
**Minor Improvements:** Empty-state next step: “Create your first subject.”  
**Launch Blocker:** Yes (orientation)  
**Confidence Score:** 4/10  
------------------------------------------------

---

## PHASE 4 — Create Subject

------------------------------------------------
**Screen:** `/console/studio/` — Curriculum Studio  
**Objective:** Create CS1 (tested as CS1X).  
**First Impression:** Clear “Next step” empty-state; Create Subject card with Subject code + Title.  
**Positive Observations:** Hint “Use a short syllabus code such as CS1.” Success: “We've created your subject successfully.” Activity: `subject_created: Created subject CS1X`.  
**Confusing Elements:** After create, still “No workspaces yet” — subject ≠ workspace. Two cards both ask for Subject code.  
**Expected User Mental Model:** “I created CS1; I should now upload papers.”  
**Critical Issues:** None for create itself.  
**Major Issues:** Extra Open Workspace step not auto-started.  
**Minor Improvements:** Auto-open workspace after create.  
**Launch Blocker:** No  
**Confidence Score:** 8/10  
------------------------------------------------

---

## PHASE 5 — Upload Syllabus

------------------------------------------------
**Screen:** Workspace Content Sources — Official Syllabus slot  
**Objective:** Upload a syllabus PDF and know what happens next.  
**First Impression:** Clear REQUIRED slots; drag/select PDF; explains grounding in authorised order.  
**Positive Observations:** Plain-language “Why it matters” on missing docs before upload.  
**Confusing Elements:** First file input is Official CMP; easy to put syllabus in wrong slot. After upload: STATUS **Failed**, tiny file size, “UPLOADED BY 1”. Next step still says upload PDFs.  
**Expected User Mental Model:** “Upload → system reads syllabus → I review topics.”  
**Critical Issues:** Failed status without recovery that restores trust.  
**Major Issues:** Slot order/mistake risk; no progress narrative after failure.  
**Minor Improvements:** Show human error text (“PDF unreadable / too small”).  
**Launch Blocker:** Yes  
**Confidence Score:** 4/10  
------------------------------------------------

---

## PHASE 6 — Upload CMP

------------------------------------------------
**Screen:** Official CMP slot  
**Objective:** Upload CMP; trust the system understood it.  
**First Impression:** CMP described as “Curriculum Master Pack — authoritative source for sections, topics, and learning objectives.” Actuarial founder may recognise CMP; others need that sentence.  
**Positive Observations:** Blocking validation findings before upload set expectations.  
**Confusing Elements:** Same Failed status after upload; tabs PIPELINE / KNOWLEDGE GRAPH / etc.  
**Expected User Mental Model:** “CMP feeds the topic list.”  
**Critical Issues:** No confidence the system understood documents.  
**Major Issues:** Intelligence tooling visible too early.  
**Minor Improvements:** Hide advanced tabs until validation passes.  
**Launch Blocker:** Yes  
**Confidence Score:** 4/10  
------------------------------------------------

---

## PHASE 7 — Curriculum Review

------------------------------------------------
**Screen:** Workspace Validation / Preview  
**Objective:** Review extracted curriculum; spot mistakes; edit.  
**First Impression:** Preview “not_ready · 0 nodes.” Checklist 0–3 of 8. No topic tree to trust or edit.  
**Positive Observations:** Findings explain missing CMP/syllabus in human language.  
**Confusing Elements:** “Curriculum Intelligence Pipeline” / “Evidence Explorer” while there is nothing to review.  
**Expected User Mental Model:** “I should see CS1 chapters and fix errors.”  
**Critical Issues:** Nothing reviewable; cannot identify mistakes in extraction.  
**Major Issues:** Editing not reachable.  
**Minor Improvements:** Empty review state with single CTA “Fix uploads.”  
**Launch Blocker:** Yes  
**Confidence Score:** 2/10  
------------------------------------------------

---

## PHASE 8 — Publish Curriculum

------------------------------------------------
**Screen:** Workspace Publish action  
**Objective:** Understand publishing; confirm safely.  
**First Impression:** Publish available early; refusal flash: cannot publish without approval and version — protects students.  
**Positive Observations:** Warning explains student risk.  
**Confusing Elements:** Can attempt publish while still on Content Sources; workflow stages feel out of sync with clicks.  
**Expected User Mental Model:** “Publish means students can study this subject.”  
**Critical Issues:** Cannot complete publish journey from zero uploads.  
**Major Issues:** Stage vs action mismatch.  
**Minor Improvements:** Disable Publish until checklist green.  
**Launch Blocker:** Yes (for zero-setup completion)  
**Confidence Score:** 3/10 (journey) / 6/10 (warning quality)  
------------------------------------------------

---

## PHASE 9 — Student Enrolment / Study Plan

------------------------------------------------
**Screen:** `/study-plan/wizard/1` … `/wizard/2`  
**Objective:** Create a study plan for CS1.  
**First Impression:** Clear examining-body cards; IFoA “Partially Supported”; CS1 “Supported — Actuarial Statistics 1.”  
**Positive Observations:** Honest “Coming Soon / Not Supported” labels.  
**Confusing Elements:** Founder already had Student Home with Mission before finishing wizard (dual path). Option cards can feel fiddly to select.  
**Expected User Mental Model:** “Pick IFoA → CS1 → exam date → plan.”  
**Critical Issues:** None blocking discovery of CS1 support.  
**Major Issues:** Full wizard not stably completed in this review (session drop observed mid-wizard in one pass).  
**Minor Improvements:** Larger click targets on option cards.  
**Launch Blocker:** No  
**Confidence Score:** 5/10  
------------------------------------------------

---

## PHASE 10 — Dashboard / Student Home

------------------------------------------------
**Screen:** `/student/`  
**Objective:** Within ten seconds: What / Why / How much / When.  
**First Impression:** Study Sensei · Today's Mission · 30 minutes · Start Session — strong action hierarchy.  
**Positive Observations:** Readiness empty-state honesty (“Not enough history”); “Why this estimate?” link.  
**Confusing Elements:** Mission title is “Today's Mission,” not a CS1 topic. WHY: “highest-value next step for **this topic**.” Expected readiness sentence ends with double period. “Estimated Knowledge (~0%).”  
**Expected User Mental Model:** “Tell me which CS1 chapter to do for 30 minutes today.”  
**Critical Issues:** Cannot answer *what* to study with confidence.  
**Major Issues:** Generic why/copy; Estimated Knowledge jargon.  
**Minor Improvements:** Fix typo; put topic name in H1.  
**Launch Blocker:** Yes (trust)  
**Confidence Score:** 5/10  
------------------------------------------------

---

## PHASE 11 — Mission

------------------------------------------------
**Screen:** Mission card on Home (mission list redirected through onboarding/home)  
**Objective:** Does today's work feel clear, achievable, worth doing?  
**First Impression:** 30 minutes feels achievable; Start Session is obvious. Worth-doing is weak because topic is unnamed.  
**Positive Observations:** Single primary CTA.  
**Confusing Elements:** “Explain today's mission” present but topic still abstract.  
**Expected User Mental Model:** “Today I revise topic X for exam Y.”  
**Critical Issues:** Worth-doing undermined by generic topic.  
**Major Issues:** None beyond topic opacity.  
**Minor Improvements:** Show exam paper code (CS1) on card.  
**Launch Blocker:** No (if topic fixed) / Yes (as observed)  
**Confidence Score:** 4/10  
------------------------------------------------

---

## PHASE 12 — Study Session

------------------------------------------------
**Screen:** `/session/sess-1/activity`  
**Objective:** Complete a study session with clear instructions.  
**First Impression:** Step rail 1–4 clear. Activity: “In your own words, explain one key idea from Core methods.” Topic label: “today's topic.” Flash: “Session started: your topic.”  
**Positive Observations:** Progress 0% / 0 of 3; hints present; supporting material section exists.  
**Confusing Elements:** Free-text “exam practice” feels like a journal prompt, not actuarial CMP work. Supporting material: “Review the core definition… and one worked example” with no actual content.  
**Expected User Mental Model:** “I practice real CS1 questions.”  
**Critical Issues:** Surprise hollowness — may abandon.  
**Major Issues:** Missing exam-grade artefacts on screen.  
**Minor Improvements:** If scaffolded, label as “reflection prompt,” not silent substitute for CMP practice.  
**Launch Blocker:** Yes (quality)  
**Confidence Score:** 4/10  
------------------------------------------------

---

## PHASE 13 — Session Completion

------------------------------------------------
**Screen:** Not reached (remained on Learning Activity).  
**Objective:** Feel accomplishment; know what changed.  
**First Impression:** N/A — incomplete.  
**Positive Observations:** Reflection and Summary appear in step rail as future steps.  
**Confusing Elements:** Leaving session and returning Home still shows Start Session — continuity unclear.  
**Expected User Mental Model:** “I finished; readiness / plan updated.”  
**Critical Issues:** Completion feedback absent in this walkthrough.  
**Major Issues:** Resume/continue not obvious after abandon.  
**Minor Improvements:** Persist “Resume session” on Home.  
**Launch Blocker:** Yes  
**Confidence Score:** 1/10  
------------------------------------------------

---

## PHASE 14 — Revision Planner

------------------------------------------------
**Screen:** `/student/revision`  
**Objective:** See personalised recommendations; trust them.  
**First Impression:** Honest empty state — “No revision support yet… Follow today's Mission.”  
**Positive Observations:** Explicitly not a second Mission; CTA back to Mission.  
**Confusing Elements:** None material.  
**Expected User Mental Model:** “Revision appears when I have gaps.”  
**Critical Issues:** None.  
**Major Issues:** Cannot judge personalisation yet (empty).  
**Minor Improvements:** Optional one-line “why empty.”  
**Launch Blocker:** No  
**Confidence Score:** 7/10  
------------------------------------------------

---

## PHASE 15 — Coach

------------------------------------------------
**Screen:** Help nav → `/alpha/help` ( `/student/coach`, `/coach` → 404)  
**Objective:** Ask questions; rely on a coach.  
**First Impression:** Help & Support / Study Sensei orientation essay — not a chat. Report a problem / Suggest improvement.  
**Positive Observations:** Distinguishes Kwalitec vs Study Sensei in prose.  
**Confusing Elements:** “Study Sensei” sounds like a coach but there is no ask box. Decision Journal / Educational Timeline jargon heavy.  
**Expected User Mental Model:** “I can ask ‘why this mission?’ and get an answer.”  
**Critical Issues:** Coach journey step missing.  
**Major Issues:** Terminology overload on Help.  
**Minor Improvements:** Rename nav if only Help.  
**Launch Blocker:** Yes (for Phase 15 scope)  
**Confidence Score:** 2/10  
------------------------------------------------

---

## PHASE 16 — Return Journey

------------------------------------------------
**Screen:** Sign out → Sign in → Student Home / Console  
**Objective:** Continuity; know next step.  
**First Impression:** Sign-in remembers product identity. Founder account returns to Console. Student Home still offers Start Session.  
**Positive Observations:** Session auth works; Welcome back.  
**Confusing Elements:** Unfinished session not clearly resumed; Console vs Student still split.  
**Expected User Mental Model:** “Pick up yesterday’s mission.”  
**Critical Issues:** None alone.  
**Major Issues:** Continuity of in-progress session weak.  
**Minor Improvements:** “Resume” language on Home.  
**Launch Blocker:** No  
**Confidence Score:** 5/10  
------------------------------------------------

---

**End of Screen Review Log**

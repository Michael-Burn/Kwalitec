# FV-001B Re-run — Screen-by-Screen Review

Evidence screenshots under [`_evidence/screenshots/`](_evidence/screenshots/). JSON captures: `phases.json`, `focus.json`, `final.json`, `complete.json`, `probe.json`.

---

## Login

### Purpose
Authenticate into the Founder Console.

### First Impression (5 seconds)
Standard email/password login; product context arrives after submit.

### Positive Observations
- Clean form; works without assistance.

### Confusing Elements
- Pre-login page does not yet signal curriculum authority.

### Critical Issues
- None.

### Major Issues
- None.

### Minor Improvements
- Optional Founder/curriculum cue on login chrome.

### Terminology Review
- Neutral.

### Navigation Review
- Submit is obvious.

### Confidence Score (0–10)
8

---

## Console Home

### Purpose
Operational landing after login.

### First Impression (5 seconds)
“Kwalitec Console” + **CURRICULUM AUTHORITY** sidebar; attention metrics dominate the main pane.

### Positive Observations
- Sidebar clearly lists Subjects and Curriculum Studio.
- INTERNAL ALPHA badge sets environment expectation.

### Confusing Elements
- Home is support/ops pulse, not curriculum publishing.

### Critical Issues
- None for recognition.

### Major Issues
- Primary curriculum next action is not the hero of the first viewport.

### Minor Improvements
- Quick action “Open Curriculum Studio” / “Subjects” on home.

### Terminology Review
- “Platform Intelligence” appears under Quick Actions (secondary).

### Navigation Review
- Sidebar is sufficient.

### Confidence Score
7

**Evidence:** `phase1_console_home.png`

---

## Subjects catalogue

### Purpose
List subjects/workspaces; create or open curriculum work.

### First Impression (5 seconds)
Clear Subjects heading; workflow strip; Create / Open controls.

### Positive Observations
- Explains Ready = after publish.
- Create Subject is visible.
- Workspace rows show stage labels after work begins.

### Confusing Elements
- Ready / Draft / Coming Soon as a formal triad is only partly visible; rows use stage names (Subject, Validation, Content Sources).

### Critical Issues
- After full attempt, no row reaches Ready (see Phase 9).

### Major Issues
- Published date not shown on rows in the observed list.

### Minor Improvements
- Explicit Ready / Draft / Coming Soon badges with published date when Ready.

### Terminology Review
- Founder-aligned.

### Navigation Review
- Open Curriculum Studio link present.

### Confidence Score
7

**Evidence:** `phase2_subjects.png`, `phase9_subjects_not_ready.png`

---

## Curriculum Studio index

### Purpose
Hub for create/open and workspace list.

### First Impression (5 seconds)
“Review, validate, preview, approve, and publish” — purpose is clear.

### Positive Observations
- NEXT STEP guidance.
- Counts for Published / Drafts.
- Create Subject + Open Workspace cards.

### Confusing Elements
- Recent activity uses machine-ish event names (`sources_uploaded`, `subject_created`).

### Critical Issues
- None on index alone.

### Major Issues
- None.

### Minor Improvements
- Humanise activity feed.

### Terminology Review
- Good primary copy.

### Navigation Review
- Strong.

### Confidence Score
8

**Evidence:** `phase2_studio.png`

---

## Create Subject (form / success)

### Purpose
Register a new subject code and title.

### First Impression (5 seconds)
Short form; required subject code.

### Positive Observations
- Success flash is clear.
- Empty create refused with plain language.

### Confusing Elements
- Title optional visually vs code required — acceptable.

### Critical Issues
- None.

### Major Issues
- None.

### Minor Improvements
- Inline field errors in addition to flash.

### Terminology Review
- Good.

### Navigation Review
- Returns to Studio with subject listed.

### Confidence Score
9

**Evidence:** `phase3_created.png`

---

## Workspace — Content Sources / Overview

### Purpose
Upload CMP + Syllabus; run validate → preview → approve → publish.

### First Impression (5 seconds)
Dense: workflow strip, status cards, two upload slots, processing tracker, review tabs, actions far down the page.

### Positive Observations
- Slot labels and rationale are excellent.
- Document Ready status and version metadata visible.
- Structure tab shows real chapter/topic content after extraction.

### Confusing Elements
- NEXT STEP often stale (“Confirm the subject…” / “Run validation after both…”) while docs already Ready and topics exist.
- Status cards vs overview metrics disagree.
- Action controls are `input[type=submit]` far below the fold.
- “Uploaded by 38” is opaque.
- Structure uses “entities · relationships”.

### Critical Issues
- Validate fails with “blocking findings” while showing **0 validation errors** and **no findings list** (`phase5_validate_blocked.png`).
- Preview success flash vs `not_ready` (`phase6_preview_contradiction.png`).
- Approve returns Publish refusal copy (`phase7_approve_confused.png`).
- Publish never succeeds on dual-Ready path (`phase8_publish_refused.png`).

### Major Issues
- Topic counts disagree (Overview 23 vs Preview line 2).
- Approve / Publish / Validate remain clickable while gates fail — Founder must learn by flash errors.

### Minor Improvements
- Collapse processing log detail; promote Actions nearer NEXT STEP.

### Terminology Review
- Primary labels Founder-friendly; secondary “entities/relationships” and numeric uploader id are not.

### Navigation Review
- Workflow strip suggests order, but stage dot lags reality; NEXT STEP unreliable.

### Confidence Score
2

**Evidence:** `phase4_both_docs_ready.png`, `phase5_validate_blocked.png`, `phase6_*.png`, `phase7_approve_confused.png`, `phase8_publish_refused.png`

---

## Workspace — Incomplete (no documents)

### Purpose
Regression: gates when nothing uploaded.

### First Impression (5 seconds)
Blocking findings for missing CMP and Syllabus are clear.

### Positive Observations
- Findings explain why and what to do.
- Empty preview refused without success flash.
- Publish refused.

### Confusing Elements
- Approve click can surface Publish refusal wording.

### Critical Issues
- None for safety intent.

### Major Issues
- Wrong action attribution in flashes (Approve → publish message).

### Minor Improvements
- Disable Approve/Publish until prerequisites met, with tooltip.

### Terminology Review
- Good on findings.

### Navigation Review
- NEXT STEP still generic.

### Confidence Score
6 (for incomplete path honesty)

**Evidence:** `regression_empty_preview.png`, `regression_incomplete_publish.png`

---

## Student orientation / catalogue cue

### Purpose
Confirm student-facing Ready discoverability after publish.

### First Impression (5 seconds)
Orientation explains Ready vs Coming Soon.

### Positive Observations
- Language matches Founder catalogue promise.

### Confusing Elements
- N/A for this re-run — publish never completed, so Ready subject not observed.

### Critical Issues
- Acceptance criterion “subject discoverable as Ready” unmet because publish failed.

### Major Issues
- —

### Minor Improvements
- —

### Terminology Review
- Student-friendly.

### Navigation Review
- Orientation gate before Home.

### Confidence Score
3 (for end-to-end Ready claim)

**Evidence:** `phase9_student_orientation.png`

---

## Review Queue / Publishing / Versions / Quality

### Purpose
Authority secondary surfaces (visited for completeness).

### First Impression (5 seconds)
Console sections exist under CURRICULUM AUTHORITY.

### Positive Observations
- Navigation items present and reachable.

### Confusing Elements
- Relationship to the single workspace Actions strip is not always obvious mid-journey.

### Critical Issues
- None blocking recognition.

### Major Issues
- Founder mid-publish does not need these if workspace Actions worked — they did not.

### Minor Improvements
- Cross-link “open active workspace” from Publishing when drafts pending.

### Terminology Review
- Acceptable.

### Navigation Review
- Sidebar consistent.

### Confidence Score
6

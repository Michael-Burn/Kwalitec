# FV-001B — Screen-by-Screen Review

**Date:** 2026-07-28  
**Template:** Programme Screen Evaluation Template  
**Evidence:** `_evidence/precise.json`, `_evidence/focus.json`, screenshots under `_evidence/screenshots/`

---

## Screen

Sign in

---

### Purpose

Authenticate into Kwalitec (invite-only Internal Alpha).

### First Impression

Polished education OS marketing; feels like a **student** product, not a curriculum-authority console.

### Positive Observations

- Clear invite-only messaging; coordinator contact path.
- Sign-in form simple (Email, Password, Remember me).

### Confusing Elements

- Headline *Know exactly what to study next* does not match Founder job (upload CMP/syllabus, publish).
- No cue that credentials open Curriculum Authority vs Student.

### Critical Issues

None for invite-only alpha (account provisioning assumed).

### Major Issues

None for authentication itself.

### Minor Improvements

Role-aware post-login promise (“Continue to Curriculum Authority” when founder).

### Terminology Review

Student study language dominant; acceptable only if Founder expects dual-role product.

### Navigation Review

Sign in is obvious.

### Confidence Score

**6 / 10**

---

## Screen

Console Home (Overview)

---

### Purpose

Operational pulse — what needs attention today.

### First Impression

Ops dashboard: Platform Health 0%, check-ins, support — not “prepare official curriculum.”

### Positive Observations

- Sidebar **CURRICULUM AUTHORITY** + Subjects / Curriculum Studio immediately visible.
- Welcome flash on first landing.

### Confusing Elements

- Platform Health 0% / “Waiting for first Product Check-in” reads as system failure on day zero.
- Quick Actions emphasise support inbox and “Platform Intelligence,” not Create Subject.

### Critical Issues

None that block login, but **delays** curriculum work.

### Major Issues

First screen does not answer “what should I do next to publish CS1?”

### Minor Improvements

Founder-first next-step card: Create Subject / Open Curriculum Studio.

### Terminology Review

“Platform Intelligence” is opaque for curriculum prep.

### Navigation Review

Subjects / Curriculum Studio are findable in sidebar — next action requires ignoring the pulse cards.

### Confidence Score

**4 / 10**

---

## Screen

Subjects

---

### Purpose

Create subjects / open workspaces; explain Ready gating for students.

### First Impression

Clear Founder job statement + workflow strip. Feels aligned with curriculum authority.

### Positive Observations

- Copy: *Students only see a subject as Ready after you publish a verified curriculum.*
- Workflow: New Subject → CMP → Syllabus → Extraction → Review → Publish → Ready.
- Create Subject / Open Workspace forms present.

### Confusing Elements

- Empty state repeats “No workspaces yet” twice.
- After work exists, status is stage label (`Content Sources` / `Validation`), not Ready/Draft/Coming Soon.
- “Open Curriculum Studio” CTA when already inside Subjects under Studio routes.

### Critical Issues

None for locating/creating entry points.

### Major Issues

Catalogue does not distinguish published vs draft subjects in Founder-facing Ready language.

### Minor Improvements

Show Ready / Draft / Coming Soon legend; list title + code + status badge.

### Terminology Review

Strong match to Founder role (Official CMP, Official Syllabus, Verified Curriculum).

### Navigation Review

Create Subject is obvious; continuing an existing subject requires knowing to click the workspace row or Open Workspace.

### Confidence Score

**6 / 10**

---

## Screen

Curriculum Studio (index)

---

### Purpose

Single Console workflow to review, validate, preview, approve, publish.

### First Impression

Command centre with counters (Published / Drafts / Pending validation / Pending approval) and create/open cards.

### Positive Observations

- NEXT STEP guidance when empty.
- Recent activity feed after actions.
- Create Subject success is clear.

### Confusing Elements

- Open Workspace after subject exists tries to **create** another workspace and errors.
- Activity uses developer-ish keys (`sources_uploaded:`, `version_assigned:`).

### Critical Issues

None on index alone.

### Major Issues

Open Workspace affordance vs “open existing from dashboard” error.

### Minor Improvements

Rename Open Workspace to “Open or create workspace”; auto-open existing.

### Terminology Review

Mostly Founder-appropriate; counters use Drafts/Published language (good).

### Navigation Review

After create, NEXT STEP still says create subject then open workspace — correct but must re-enter code.

### Confidence Score

**6 / 10**

---

## Screen

Review Queue / Publishing / Versions / Quality (hubs)

---

### Purpose

(As labelled) Review corrections; approve/publish; manage versions; quality-check.

### First Impression

Same curriculum workflow strip + workspace list; little unique content.

### Positive Observations

- Page titles and blurbs match Founder vocabulary (especially Publishing → Ready).

### Confusing Elements

- Hubs do not host the actual review/publish UI — must open workspace anyway.
- Before any workspace: identical empty states across four nav items.

### Critical Issues

None individually; collectively inflate nav without payload.

### Major Issues

Review Queue does not show extractable structure to correct (journey Phase 5 fails here).

### Minor Improvements

Deep-link hub CTAs into the relevant workspace stage, or collapse hubs until content exists.

### Terminology Review

Good Founder language on page chrome.

### Navigation Review

Primary CTA is “Open Curriculum Studio” / workspace link — next action exists but hubs feel redundant.

### Confidence Score

**4 / 10**

---

## Screen

Workspace — Content Sources / workflow

---

### Purpose

Upload official PDFs; advance Subject → Content Sources → Validation → Preview → Approval → Publish.

### First Impression

Dense engineering console: workflow stages plus PIPELINE / KNOWLEDGE GRAPH / ENTITY DETAILS tabs. Upload WHY copy is excellent.

### Positive Observations

- Official CMP / Syllabus REQUIRED with plain-language purpose.
- Blocking findings before upload explain what to do.
- Document STATUS Ready with version/size/time.
- Safety flashes on failed validate/approve/publish are readable.

### Confusing Elements

- Files appear under the wrong slot labels after sequential file pick.
- “Preview ready · not_ready · 0 nodes” is self-contradictory.
- NEXT STEP can say validation looks ready while flash says validation failed.
- “0 awaiting review · 0 validation errors” vs blocking validation flash.
- `UPLOADED BY 1`.
- Pipeline ms timings and “Knowledge Graph Built” feel internal.

### Critical Issues

- Cannot obtain a reviewable curriculum (0 nodes).
- Cannot approve/publish to Ready.
- Slot swap undermines trust in document identity.

### Major Issues

- EI/engineering tab labels on primary Founder surface.
- Checklist 3/8 without clear list of remaining items in the captured viewport narrative.

### Minor Improvements

- Collapse Pipeline/Knowledge Graph behind “Advanced”.
- Deduplicate stacked flash messages.

### Terminology Review

**Fails** Founder-plain language: Knowledge Graph, Pipeline, Entity Details, Curriculum Intelligence, Inference (Pipeline audit).

### Navigation Review

Actions (Advance, Validate, Build Preview, Approve, Publish) are visible; which to trust when contradictory is not.

### Confidence Score

**3 / 10**

---

## Screen

Workspace — Validation / Pipeline tabs (detail)

---

### Purpose

Inspect validation issues and pipeline history.

### First Impression

Technical audit trail; some topic names appear in entity_created lines (e.g. Chapter 1 — Random variables) but not as an editable curriculum tree.

### Positive Observations

- Issues like “no learning objectives” are somewhat understandable.
- Pipeline history shows completed stages.

### Confusing Elements

- Graph rebuilt with “32 relations” while preview has 0 nodes.
- Encoding glitches in topic titles (`Chapter 3 â Regression`).

### Critical Issues

No Founder-facing correction UI for extracted structure.

### Major Issues

Inference / graph language unnecessary for publication confidence.

### Minor Improvements

Present issues as “Fix before students can study” checklist with document+slot context.

### Terminology Review

Poor match — intelligence/pipeline/entity vocabulary.

### Navigation Review

Tabs discoverable; purpose for a Founder unclear.

### Confidence Score

**3 / 10**

---

## Screen

Subjects / Studio after failed publish (verification)

---

### Purpose

Confirm Ready subject for students.

### First Impression

CS1B exists but is not Ready; counters show Drafts 1, Published 0.

### Positive Observations

- System did not falsely mark Ready.
- Version crumb `2026.1` visible on workspace list.

### Confusing Elements

- No explicit “Draft” badge vs “Ready” badge.
- Open Workspace error when re-entering code.

### Critical Issues

Acceptance criterion “Confirm subject is Ready” fails.

### Major Issues

Catalogue does not communicate confidence for student use.

### Minor Improvements

Show blocking reason on catalogue row (“Validation incomplete — 0 nodes”).

### Terminology Review

Adequate.

### Navigation Review

Return to Subjects is easy via sidebar.

### Confidence Score

**3 / 10**

---

## Score summary

| Screen | Confidence | Blocks launch? |
|---|---|---|
| Sign in | 6 | No |
| Console Home | 4 | Major (first-action clarity) |
| Subjects | 6 | Major (status model) |
| Curriculum Studio index | 6 | Major (open existing) |
| Hub pages | 4 | Major (hollow review) |
| Workspace | 3 | **Critical** |
| Validation/Pipeline detail | 3 | **Critical** |
| Post-publish verification | 3 | **Critical** |

# PR-001A — Founder Workflow Specification

**Programme:** PR-001A — Founder Operations Certification  
**Audience:** Product / engineering (operator contract)  
**Scope:** Curriculum Studio founder publishing workflows only  

---

## Purpose

Define the intended behaviour of every founder-facing publishing workflow so a founder can operate Kwalitec without developer assistance.

## Actors

| Actor | Access |
|---|---|
| Founder | Admin / `FOUNDER_EMAILS` Console access |
| Student | Consumes **published** curriculum only |
| Developer | Out of band — not required for the happy path |

## Workflow overview

```
Login → Curriculum Studio → Create Subject → Open Workspace
  → Assign Version → Upload CMP + Syllabus → Validate
  → Preview / Review → Approve → Publish → Verify availability
```

Stages (UI labels): **Subject → Content Sources → Validation → Preview → Approval → Publish**.

---

## WF-01 Login & Console access

| Item | Specification |
|---|---|
| Intended behaviour | Founder signs in at `/auth/login`, opens Command Centre, navigates to Curriculum Studio (`/console/studio/`). |
| Operator decisions | Confirm correct founder account. |
| Failure modes | Non-founder blocked (403); wrong credentials. |
| Recovery | Use authorised founder email; contact platform admin if access missing. |
| Guidance | Studio is under Command Centre → Curriculum Studio. |

## WF-02 Subject creation

| Item | Specification |
|---|---|
| Intended behaviour | From Studio dashboard, enter subject code (+ optional title), submit **Create Subject**. Subject appears for workspace binding. |
| Operator decisions | Choose a stable syllabus code (e.g. `CS1`, `LAW1`). |
| Failure modes | Empty code; duplicate code; port unavailable. |
| Recovery | Fix fields; choose a new code or open existing workspace; retry. |
| Guidance | Flash explains issue, why duplicates hurt enrolment/history, and next action. |

## WF-03 Open workspace

| Item | Specification |
|---|---|
| Intended behaviour | Enter subject code → **Open Workspace** → land on workspace page with stage strip and next-step hint. |
| Operator decisions | Confirm correct subject. |
| Failure modes | Unknown subject; workspace already exists; missing workspace URL. |
| Recovery | Create subject first; open existing workspace from dashboard. |
| Guidance | Next-step panel drives the primary CTA. |

## WF-04 Version assignment

| Item | Specification |
|---|---|
| Intended behaviour | Assign an immutable version label (e.g. `2027.1`) before validation/publication gates. |
| Operator decisions | Label scheme (calendar or semantic). |
| Failure modes | Empty label; duplicate version id/label. |
| Recovery | Choose a new label; do not reuse published labels. |
| Guidance | Version history panel lists prior labels/status. |

## WF-05 CMP & syllabus upload

| Item | Specification |
|---|---|
| Intended behaviour | Enter CMP and syllabus **references** (not raw PDF bytes) → **Upload Sources**. Checklist facts update. |
| Operator decisions | Correct reference URIs for the version. |
| Failure modes | Empty refs; no version; ingestion/port failure; parse failure downstream. |
| Recovery | Assign version; supply at least one reference; re-upload corrected refs; re-validate. |
| Guidance | Help text: “Reference only — do not paste PDF bytes.” |

## WF-06 Validation

| Item | Specification |
|---|---|
| Intended behaviour | **Validate Curriculum** runs ingestion + management gates; readiness card updates; findings list shows issue / why / recovery. |
| Operator decisions | Whether warnings are acceptable; fix blocking errors before preview. |
| Failure modes | Missing sources; no version; blocking findings; service unavailable. |
| Recovery | Follow each finding’s **What to do**; re-run Validate. |
| Guidance | Blocking findings prevent safe publication. |

## WF-07 Review (preview)

| Item | Specification |
|---|---|
| Intended behaviour | **Build Preview** after validation; founder reviews extracted structure before approval. |
| Operator decisions | Approve structure as student-visible curriculum. |
| Failure modes | Preview before validation; empty structure. |
| Recovery | Validate first; fix sources; rebuild preview. |
| Guidance | Next-step copy mentions version + approve. |

## WF-08 Approval

| Item | Specification |
|---|---|
| Intended behaviour | Optional approval note → **Approve Curriculum**. |
| Operator decisions | Confirm readiness to publish. |
| Failure modes | Missing version/preview. |
| Recovery | Assign version; complete preview; retry. |

## WF-09 Publication

| Item | Specification |
|---|---|
| Intended behaviour | **Publish Curriculum**; package becomes student-available authority for that subject/version. |
| Operator decisions | Timing of release. |
| Failure modes | Incomplete checklist; missing approval/version. |
| Recovery | Complete checklist items shown on workspace; retry. |
| Guidance | Success flash confirms publication. |

## WF-10 Subject management & availability

| Item | Specification |
|---|---|
| Intended behaviour | Dashboard metrics show published / drafts / pending validation / pending approval; workspace list remains the management surface. |
| Operator decisions | Which draft to continue; when to publish. |
| Failure modes | Stale browser tab; missing workspace. |
| Recovery | Return to Studio index; reopen workspace. |

## WF-11 Version history

| Item | Specification |
|---|---|
| Intended behaviour | Workspace shows assigned labels and status; history grows as versions are assigned/published. |
| Operator decisions | New label for each material curriculum change. |
| Failure modes | Conflicts / duplicates. |
| Recovery | New label; never overwrite published history. |

## WF-12 Error handling (cross-cutting)

All founder POST actions:

1. Validate CSRF/forms.
2. Call Studio application service.
3. On success → success flash.
4. On failure → exception-mapped recovery flash (`recover_flash`) and redirect back to a safe page (dashboard or workspace).

No stack traces are shown to founders.

---

## Non-goals (PR-001A)

- Runtime A cutover, Twin activation, premium UI redesign, educational algorithm changes.

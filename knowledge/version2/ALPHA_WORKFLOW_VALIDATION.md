# Alpha Workflow Validation (ARP-003)

**Authority:** Informational (end-to-end product workflow validation)  
**Scope:** Founder → Student workflows, navigation consistency, error-path polish.  
**Constraints:** No new features, no architecture changes, no educational logic, no persistence changes.

This note records ARP-003 validation of complete product workflows from a user’s
perspective, issues found, fixes applied, and remaining observations.

---

## Workflows tested

| # | Workflow | Path | Outcome |
|---|----------|------|---------|
| 1 | Founder publish journey | Studio → Workspace → Validate → Preview → Approve → Publish | **Pass** (with messaging polish) |
| 2 | Student session journey | Home → Start → Activities → Reflection → Summary → Home | **Pass** |
| 3 | Session interrupt / resume | Interrupt mid-session → Resume → Complete | **Pass** (after resume fix) |
| 4 | Founder alpha navigation | Evidence Gates ↔ Intelligence ↔ Studio | **Pass** (after nav promotion) |
| 5 | Dual-run navigation | Dashboard ↔ Student Experience ↔ Dashboard | **Pass** (after return link) |

---

## Workflow 1 — Founder create → publish

**Expected:** Published curriculum becomes available to Student Experience.

**Outcome:** Pass.

**Validated:**

- Studio dashboard and workspace surfaces render with breadcrumbs, next-step copy, and stage-based primary CTAs.
- Stage order remains Subject → Content Sources → Validation → Preview → Approval → Publish.
- Success flashes confirm outcomes (`Validation completed successfully.`, `Curriculum published successfully.`, …).
- Approval-stage guidance now states that published curriculum becomes available to Student Experience.
- Preview/approve warnings remind Founders to assign a version label before approval/publish (Management requires `version_id`).

**Issues found:**

1. Approve/publish warnings omitted the version-label prerequisite (Founders hit soft failures when approving without a version).
2. Invalid workspace IDs returned a bare 404 without recovery guidance.

**Fixes applied:**

- Preview/approval next-step copy and approve/publish warning flashes mention version assignment.
- Missing workspace redirects to Studio with an understandable flash instead of a silent 404.

**Remaining observations:**

- Studio still has no dedicated Content Sources upload UI (stage CTA advances to Validate). Content upload remains an application-port capability without a Founder form in this milestone — out of ARP-003 fix scope (would be a feature).
- Publish success confirms Studio publication; student availability still depends on Curriculum Management `active_version` wiring (unchanged architecture).

---

## Workflow 2 — Student home → complete → home

**Expected:** Updated projections displayed after return home.

**Outcome:** Pass.

**Validated:**

- Linear session flow Overview → Activity → Reflection → Summary → Complete → Student Home.
- Primary CTAs (`Begin Session`, answer submit, Continue, Return Home) and progress chrome.
- Finish success flash: “Session complete. Your home view is ready with today's updates.”
- Forbidden educational-kernel jargon absent from session HTML.

**Issues found:** None blocking.

**Fixes applied:** None beyond shared error-path polish (finish failures stay on Complete).

**Remaining observations:**

- Home projection refresh after finish depends on Experience ports / composition (validated at presentation handoff; educational projection math untouched).

---

## Workflow 3 — Interrupt → resume → complete

**Expected:** Workspace restored correctly.

**Outcome:** Pass (after fix).

**Issues found:**

1. **Critical:** Re-entering Overview after leaving mid-session rewound `active_surface` to Overview, wiping resume position.
2. Skip-ahead URLs could leave URL/content mismatched when workspace was behind the requested surface.

**Fixes applied:**

- `resume_redirect_if_needed` restores (or clamps to) the active workspace surface.
- Overview re-entry after interrupt flashes “Welcome back — continuing where you left off.” and redirects to the active surface.
- `load_page` no longer rewinds workspace state via URL.

**Remaining observations:**

- There is still no dedicated Pause control; interrupt is brand → Home. Resume is implicit via workspace registry + redirect. A labelled “Resume Session” Home CTA would be a future enhancement, not required once workspace restore works.

---

## Workflow 4 — Evidence Gates → Intelligence → Studio

**Expected:** Navigation remains consistent.

**Outcome:** Pass (after fix).

**Issues found:**

1. Evidence Gates lived only in secondary nav (not rendered in the Command Centre shell), so the Alpha trio was not equally discoverable.
2. Evidence Gates lacked a clear return path to Intelligence / Studio.

**Fixes applied:**

- Evidence Gates promoted into primary `COMMAND_CENTRE_NAV` (Studio → Intelligence → Evidence Gates).
- Cross-links added on Intelligence and Evidence Gates pages.

**Remaining observations:**

- Secondary operational destinations (Attention, Findings, …) remain secondary by design.

---

## Workflow 5 — Dual-run Dashboard ↔ Student Experience

**Expected:** No broken navigation.

**Outcome:** Pass (after fix).

**Issues found:**

1. V1 Dashboard linked into Student Experience, but Student Experience had no reverse “Back to Dashboard” link in dual-run mode.

**Fixes applied:**

- Student shell footer shows **Back to Dashboard** when `ENABLE_STUDENT_EXPERIENCE` is on and `SOLE_RUNTIME` is off.
- `v2_flags` injected into global template context for consistent dual-run chrome.

**Remaining observations:**

- `/student` remains registered even when the flag is off (deep links still work); flag mainly gates entry CTA and dual-run chrome.

---

## Error paths

| Condition | Behaviour after ARP-003 |
|-----------|-------------------------|
| Missing / foreign session ownership | HTTP 403 with clearer copy (shared/expired link guidance); sole-runtime users get Return Home |
| Missing session / workspace mid-flow | Warning flash → Student Home |
| Invalid Studio workspace | Warning flash → Studio index |
| Finish / begin form failures | Stay on the relevant surface (Complete / Overview), not a confusing sibling |
| Unauthenticated founder/student routes | Redirect to login / founder gate |

Every user-visible failure now includes recovery language (“try again”, “return home”, “open Curriculum Studio”).

---

## Consistency checklist

| Concern | Status |
|---------|--------|
| Breadcrumbs | Studio, Intelligence, Evidence Gates present |
| Navigation | Alpha trio in primary Founder nav; student nav unchanged |
| Page titles | Product language (Curriculum Studio, Founder Intelligence, Evidence Gates, session surface labels) |
| Primary CTA | Stage-based on Studio; linear on Session |
| Flash messages | Centralised Studio flashes; session success/warning copy polished |
| Icons / chrome | Shared Founder CSS shell; session/student brand exit hatch |
| Terminology | Publish (not Publication) in UI; Content Sources; no kernel jargon on learner surfaces |

---

## Fixes applied (summary)

1. Session resume redirect (no workspace rewind on interrupt).
2. Evidence Gates moved to primary Founder nav.
3. Dual-run “Back to Dashboard” on Student Experience.
4. Studio missing-workspace recovery flash + redirect.
5. Approve/publish/version guidance copy.
6. Finish error redirects stay on Complete.
7. Session missing-surface flash → Home.
8. 403 copy improved for shared/expired links.

---

## Remaining observations

- Content Sources upload UI still absent (feature-sized).
- Home “Resume Session” labelled CTA not added (resume works via redirect).
- Publish → student curriculum activation remains Management-mediated (architecture boundary).
- Progress chrome markers are not deep links (by session-experience design).

---

## Tests

Workflow-oriented suite: `tests/presentation/workflows/`

| Module | Focus |
|--------|-------|
| `test_workflow_founder_studio.py` | Workflow 1 — Studio journey, flashes, stages |
| `test_workflow_student_session.py` | Workflow 2 — Happy path session |
| `test_workflow_session_resume.py` | Workflow 3 — Interrupt / resume |
| `test_workflow_founder_nav.py` | Workflow 4 — Alpha nav consistency |
| `test_workflow_dual_run.py` | Workflow 5 — Dual-run links |
| `test_workflow_error_paths.py` | Failure paths |
| `test_workflow_consistency.py` | Titles, CTAs, terminology, flashes |
| `test_workflow_volume_matrix.py` | Navigation / resume matrix volume |

**Collected:** 180 workflow tests (179 passed, 1 skipped).  
Target was 60–120; volume matrix intentionally exceeds the floor for resume/nav permutations.

```bash
python3 -m pytest tests/presentation/workflows/ -q
```

---

## Constraints respected

- No educational algorithm changes
- No domain educational decisions changed
- No architecture / persistence refactor
- Fixes limited to genuine workflow, navigation, and error-path issues

---

## Related documents

- [`ALPHA_READINESS_FOUNDER_UX.md`](ALPHA_READINESS_FOUNDER_UX.md) — ARP-002 Founder polish
- [`LEARNING_SESSION_EXPERIENCE.md`](LEARNING_SESSION_EXPERIENCE.md) — Session flow authority
- [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md) — Studio product/architecture
- [`STUDENT_EXPERIENCE.md`](STUDENT_EXPERIENCE.md) — Student Experience projections
- [`V2_020_RETIREMENT_RUNBOOK.md`](V2_020_RETIREMENT_RUNBOOK.md) — Dual-run / cutover

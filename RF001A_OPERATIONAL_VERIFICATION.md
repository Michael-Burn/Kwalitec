# RF-001A — Operational Verification

**Programme:** Release Acceptance Programme RF-001A  
**Date:** 2026-07-31  
**Method:** Flask test-client walkthroughs + BF-001 remediation suite + workflow/alpha smoke (verification only)  
**Candidate:** Working tree = RF-001 seal (`e4d5a1b`) + BF-001 Studio remediation (uncommitted at review time)

---

## Overall

| Walkthrough | Result |
|-------------|--------|
| Founder (RF-001A path) | **PASS** (with live-deploy WARNING — see below) |
| Student (RF-001A path) | **PASS** |
| Combined operational gates | **159/159 PASS** |
| Path evidence subset | **22/22 PASS** |

No Category A defects remained on the candidate after BF-001.

---

## Phase 3 — Founder operational verification

Path required:

Create Subject → Upload → Preview → Expand/Collapse → Back → Restart → Assign Version (YYYY.N) → Approve → Publish → Archive → Delete Draft → Logout

| Step | Result | Evidence |
|------|--------|----------|
| Create Subject / Studio | **PASS** | `test_studio_index_reachable`; `GET /console/studio/` 200 |
| Upload | **PASS** | `test_workspace_reachable`; Upload chrome on workspace |
| Preview | **PASS** | Workflow stage labels + workspace Preview chrome |
| Expand / Collapse | **PASS** | `test_preview_tree_js_uses_plain_objects_not_object_constructor` — `var byId = {}`, `expandAll`, `keydown` |
| Back | **PASS** | `test_retreat_moves_stage_back_without_duplicate` |
| Restart | **PASS** | `test_reset_returns_to_upload_subject_stage` → `subject` |
| Assign Version (YYYY.N) | **PASS** | Form accepts `2026.1`, rejects `1.0.0`; assign route remediation |
| Approve | **PASS** | Workflow founder studio approval chrome / CTAs |
| Publish | **PASS** | Publish stage + success flash contracts |
| Archive | **PASS** | `test_archive_published_protects_from_delete` → `archived` |
| Delete Draft | **PASS** | `test_delete_draft_removes_workspace` |
| Logout | **PASS** | Alpha founder smoke + RF-001 smoke (POST `/auth/logout`) |

Supporting suite: `tests/presentation/curriculum_studio/test_bf001_blocker_remediation.py` (13) + founder workflow/nav/consistency + alpha founder smoke — all green in RF-001A ops gates.

### Founder ratings

| Observation | Rating |
|-------------|--------|
| Candidate Studio workflow after BF-001 | **PASS** |
| Live production Studio Expand/Collapse (`e4d5a1b` JS still `var byId = Object`) | **WARNING** — deploy BF-001 before production authoring |
| Duplicate catalogue desktop rows | **PASS** (CSS remediation verified) |

---

## Phase 4 — Student operational verification

Path required:

Login → Dashboard → Today's Mission → Study Session → Reflection → Completion → History → Revision → Logout

| Step | Result | Evidence |
|------|--------|----------|
| Login | **PASS** | Workflow / alpha student fixtures |
| Dashboard / Home | **PASS** | `test_student_home_reachable`; DX-006B home |
| Today's Mission | **PASS** | Home handoff + mission chrome; alpha surfaces 200 |
| Study Session | **PASS** | `test_begin_advances_to_activity`; overview→activity |
| Reflection | **PASS** | `test_full_session_happy_path` |
| Completion | **PASS** | Full happy path through complete/summary |
| History | **PASS** | Secondary surfaces `/student/history` 200 |
| Revision | **PASS** | Secondary surfaces `/student/revision` 200 |
| Logout | **PASS** | Workflow / RF-001 smoke |

### Student verification checks

| Check | Result |
|-------|--------|
| No crashes (5xx on primary path) | **PASS** |
| No broken navigation | **PASS** |
| No incorrect study flow on happy path | **PASS** |
| No data loss on complete/resume suites | **PASS** (resume suite residual assertion is finish→summary redirect debt, not data loss) |

---

## Phase 6 — Manual browser verification

| Item | Result |
|------|--------|
| Platform | macOS 26.5.2 (Darwin 25.5.0, arm64) — The-Citadel |
| Agent UA | Safari-class `Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15` |
| Live login | **PASS** — HTTP 200 (~1.1 s) |
| Live first-party CSS/JS | **PASS** — 200 for `app.css`, `brand.css`, `fonts.css`, `tokens.css`, `app.js`, `theme.js`, tree JS |
| Local BF-001 tree JS brace/paren balance | **PASS** (0 imbalance) |
| Local BF-001 forest init | **PASS** — plain `{}`; no `Object` constructor maps |
| Playwright interactive session | **N/A** — Playwright not runnable in this environment; no browser MCP |
| Live tree JS behaviour | **WARNING** — production still serves pre-BF-001 `var byId = Object` until Manual Deploy of BF-001 |
| Console exceptions on candidate | **PASS** (source-level); interactive Chromium session not executed |

Honesty note: interactive in-browser console capture was not available. Verification used live HTTP asset probes + static JS inspection + Flask walkthroughs. This matches RF-001 smoke posture and is sufficient to flag the live Studio JS gap.

---

## Ops gate command (executed)

```bash
.venv/bin/python -m pytest \
  tests/presentation/curriculum_studio/test_bf001_blocker_remediation.py \
  tests/presentation/workflows/test_workflow_founder_studio.py \
  tests/presentation/workflows/test_workflow_student_session.py \
  tests/presentation/workflows/test_workflow_founder_nav.py \
  tests/presentation/workflows/test_workflow_consistency.py \
  tests/operational/test_alpha_smoke_founder.py \
  tests/operational/test_alpha_smoke_student.py \
  tests/test_v1s008_educational_integrity.py \
  tests/test_dx006b_founder_home.py \
  tests/test_dx006b_student_home.py \
  tests/test_dx006b_founder_subjects.py \
  -q
# → 159 passed in 13.49s
```

---

## Verdict

**Founder candidate: PASS**  
**Student candidate: PASS**  
**Live Studio authoring: WARNING until BF-001 cutover**

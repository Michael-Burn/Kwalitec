# APPLICATION_IDENTITY.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Base URL:** `http://127.0.0.1:5201`  
**Captured at (UTC):** `2026-07-28T23:04:31Z` (health) / screenshots immediately after

---

## Recorded identity

| Field | Value | Source |
|---|---|---|
| Application version | `2.0.0` | `/health` → `version`; Settings “Application Information”; Console banner `V2.0.0`; `VERSION` file |
| Build identifier (RC freeze) | `5e8e92256cbd1e728e5ddb8f8ec40b1f9f26ccf1ac84ddb0addd36d02593915e` | Source worktree digest ([SOURCE_CERTIFICATION.md](SOURCE_CERTIFICATION.md)) |
| Build number (runtime health) | `local` | `/health` → `build_number` (`KWALITEC_BUILD_NUMBER` unset) |
| Product UI build label | `Build RC2` | Login / Settings footer (`INTERNAL_ALPHA_BUILD_LABEL`) — **product chrome**, not the RC programme ID |
| Release Candidate ID | `RC-2026.07.29-01` | This certification programme |
| Environment label | Internal Alpha · Founding Cohort | Login / Settings / Console |

Note: UI “Build RC2” is **not** the Release Candidate ID. Programmes must cite **`RC-2026.07.29-01`**, not “RC2”.

---

## Screenshots

All under `_evidence/screenshots/`.

| Capture | File | URL | Observation |
|---|---|---|---|
| Login | `01_login.png` | `/auth/login` | Kwalitec sign-in; footer `v2.0.0 · INTERNAL ALPHA · Build RC2` |
| Founder Console | `02_founder_console.png` | `/console/` | Console Home; banner `INTERNAL ALPHA · V2.0.0`; pulse `2026-07-28 23:04 UTC`; System card `Build local` |
| Subjects | `03_subjects.png` | `/console/studio/subjects` | **No workspaces yet**; no CS1* rows |
| Studio hub | `03b_studio_hub.png` | `/console/studio/` | Drafts 0 / Published 0 |
| System Operations | `04_system_operations.png` | `/console/operations` | Operations snapshot present |
| Settings / About | `04b_settings_about.png` | `/settings/` | Version `2.0.0`; About Kwalitec |
| Alpha Help | `04c_alpha_help_release.png` | `/alpha/help` | Help & Support |
| Health | `05_health.png` | `/health` | JSON identity payload |
| Health details | `05b_health_details.png` | `/health/details` | Migrations `202607280080` |

Machine-readable capture: `_evidence/screenshots/identity_capture.json`

---

## Subjects emptiness check

`identity_capture.json` → Subjects `mentions_cs1: false`  
Consistent with fresh RC database (no historical Founder subjects).

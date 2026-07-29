# UX-004 — Settings Information Architecture Report

**Programme:** UX Architecture  
**Status:** Review complete — **no implementation in this milestone**  
**Date:** 2026-07-29  
**Scope:** Audit Settings as a configuration centre; separate analytics/KPIs from account control. Align with DX-002 product architecture and the Student EOS surface model.  
**Predecessor context:** UX-001 (Founder routing), UX-002 / UX-002A (production data lifecycle), DX-002 (IA / KPI audits)

---

## Summary

Kwalitec currently presents **Settings** as the nav label for `/student/profile`, while a second product Settings surface still exists at `/settings/*`. The Student Settings page mixes genuine configuration (preferences, account) with **read-only learning KPIs** (study time, sessions, topics mastered, exam readiness) and a **Current Examination** identity card that belongs to Study Plan / exam configuration — not to Settings.

Verdict: Settings is not yet a true configuration centre. Analytics already have a home on **History** (practice archive) and readiness context on **Journey**. Relocating KPI clusters out of Settings, and treating examination identity as Study Plan configuration with quiet status elsewhere, restores the premium exam-OS split: **Settings configures the system; dashboards and archives report progress.**

**No code or template changes were made in UX-004.** Implementation should follow this review as a later programme.

---

## Audit method

| Source | Role |
|--------|------|
| `app/templates/student/profile.html` | Canonical Student Settings content (nav label **Settings**) |
| `app/templates/settings/index.html` + `app/settings/routes.py` | Product Settings sections (Preferences, Data, Account Status, …) |
| `app/presentation/student/navigation.py` + `experience_workspace.py` | Nav labels and surface mapping |
| `app/templates/student/history.html`, `home.html`, `journey.html` | Candidate destinations for analytics / identity |
| DX-002 `PRODUCT_ARCHITECTURE.md`, `KPI_AUDIT.md`, `INFORMATION_HIERARCHY_AUDIT.md` | Prior one-question and KPI policy |
| Help copy (`alpha/help.html`) | Student mental model for History vs Settings |

---

## Current structure

### Dual Settings surfaces

| Surface | Route | Nav treatment | Role today |
|---------|-------|---------------|------------|
| **Student Settings (canonical)** | `/student/profile` | Primary nav item **Settings** (`ExperienceSurface.PROFILE`) | Examination card, preferences summary, goals, learning statistics, account summary, CTA into product Settings |
| **Product Settings** | `/settings/*` | Nested under same nav highlight when opened | General, Profile, Preferences, Data, Account Status, Product Check-in |
| Sole-runtime bridge | `GET /settings/` | Redirects to `student.profile` | Avoids duplicate “General” landing (PX-003 B9) |

Help still teaches **Settings → Preferences** and **Settings → Data**, which correctly point at product Settings — while the nav pill **Settings** lands on the Student Profile page. That label collision is part of the IA debt (also noted in DX-002 FP-18).

### Student Settings — component inventory

Rendered by `student/profile.html` under page title **Settings**:

| # | Component (as shown) | What it shows | Editable? |
|---|----------------------|---------------|-----------|
| 1 | **Current examination** | Active exam / paper label (`examination_label`) | No — display only; authoritative source is active study plan |
| 2 | **Learning preferences** | Session length, study days, reminders, quiet hours | No on this page — summary only |
| 3 | **Goals** | Goal titles + progress bars | No edit controls |
| 4 | **Learning statistics / Progress summary** | Total study time, sessions completed, topics mastered, exam readiness | No — pure KPIs |
| 5 | **Account settings** | Email, notifications, locale, timezone | No — summary only |
| 6 | Primary CTA | “Open account settings” → `settings.preferences` | Navigates to product Settings |

### Product Settings — section inventory

| Section | Route | Contents |
|---------|-------|----------|
| General | `/settings/` (redirect under sole runtime) | Version, support, account email, diagnostics, About |
| Profile | `/settings/profile` | Email (readonly), Research Journey contribution KPIs / badges |
| Preferences | `/settings/preferences` | Appearance (Light/Dark/System), daily study goal hours |
| Data | `/settings/data` | Weekly report export, JSON backup + restore, record counts |
| Account Status | `/settings/internal-alpha` | Curriculum / study plan labels, personalised-recommendations status, appearance duplicate, diagnostics |
| Product Check-in | `/settings/share-feedback` | Redirect to research check-in |

### Adjacent surfaces that already own analytics

| Surface | Already shows |
|---------|---------------|
| **History** | Study time, session count, readiness trend, recent sessions, completed topics |
| **Journey** | Syllabus progress, current/completed/upcoming topics |
| **Home** | Today’s Mission (operational decision — not a KPI wall) |
| **Choose Exam / Study Plan** | Examination selection and plan configuration |

---

## Categorisation

Categories used for this audit: **Configuration · Analytics · Profile · Learning · Security · Operational**.

### Student Settings components

| Component | Category | Belongs in Settings? | Rationale |
|-----------|----------|----------------------|-----------|
| Current examination | Learning (identity) + Operational (plan binding) | **No** as KPI/status card | Exam identity is configured via **Choose Exam / Study Plan**. Settings may deep-link to change it; it must not present as a Settings “dashboard” tile. |
| Learning preferences (summary) | Configuration | **Yes** (summary + edit path) | Session length, days, reminders, quiet hours are system behaviour controls. |
| Goals (progress bars) | Learning / Analytics | **No** unless editable | Progress without edit is a KPI. Goals that are preferences belong under Configuration once editable. |
| Progress summary — study time | Analytics | **No** | Already on History; DX-002 KPI policy: remove decorative stats from Profile. |
| Progress summary — sessions completed | Analytics | **No** | History owns session archive counts. |
| Progress summary — topics mastered | Analytics / Learning | **No** | History (completed topics) + Journey (syllabus map). |
| Progress summary — exam readiness | Analytics | **No** | Journey / History context; never a Settings KPI. |
| Account summary | Profile / Configuration | **Yes** | Identity and account controls belong in Settings. |
| Open account settings CTA | Configuration | **Yes** | Correct bridge into editable product Settings. |

### Product Settings sections

| Section / block | Category | Belongs in Settings? | Rationale |
|-----------------|----------|----------------------|-----------|
| Appearance | Configuration | **Yes** | Browser/system behaviour. |
| Daily study goal | Configuration / Learning | **Yes** | Preference that drives tracking — keep under Preferences. |
| Email / account identity | Profile / Security | **Yes** | Account centre. |
| Data export / backup / restore | Operational / Security | **Yes** | Data control is classic Settings. Record-count badges are operational summary for export, not learning KPIs — keep quiet. |
| Weekly report export | Operational (export of Analytics) | **Yes** (action) | Export *action* stays in Settings; the report *content* is analytics produced elsewhere. |
| Account Status (curriculum / plan / personalisation) | Operational | **Partial** | Quiet “system posture” is acceptable; duplicate Current Examination / plan labels should not compete with Study Plan. Prefer diagnostics disclosure. |
| Diagnostic build metadata | Operational | **Yes** (disclosed) | Already behind disclosure — correct. |
| General / About / Help links | Operational | **Prefer Help** | Sole-runtime redirect already acknowledges duplication with Help. |
| Research Journey badges | Analytics (research) | **No** on Profile tab | Move to Product Check-in / research surface; Settings keeps only the Check-in entry. |
| Product Check-in entry | Operational | **Yes** | Configuration of participation / feedback channel. |

---

## Specific review (mission checklist)

| Item | Verdict | Recommended home |
|------|---------|-------------------|
| **Current Examination** | Does **not** belong in Settings as a hero status card | **Study Plan / Choose Exam** for change; optional quiet identity line on **Home** or **Journey** if orientation requires it. Settings may offer “Change examination” → Study Plan. |
| **Study Statistics** | Does **not** belong in Settings | **History** (canonical practice analytics archive) |
| **Progress Summary** | Does **not** belong in Settings | **History** for cumulative stats; **Journey** for syllabus/readiness narrative |
| **Study Time** | Does **not** belong in Settings | **History** (already present) |
| **Topics Mastered** | Does **not** belong in Settings | **History** (completed topics) + **Journey** (map) |
| **Sessions** | Does **not** belong in Settings | **History** (recent sessions); session *start* remains **Home** (Mission / Session — Mission Centre analogue) |

**Not recommended as primary destinations for these KPIs**

| Destination | Why not primary for Settings leftovers |
|-------------|----------------------------------------|
| Student Dashboard (legacy `/dashboard`) | Dual-runtime / legacy Learning Workspace; not the sole-runtime EOS home. Do not reintroduce KPI walls there. |
| Learning Dashboard | Same — avoid resurrecting multi-metric dashboards as the analytics home. |
| Analytics (legacy blueprint) | Label retired in favour of **History** for student practice stats (PX-002A). Prefer History. |
| Mission Centre | No separate nav surface; **Home** is the mission decision surface. Sessions *to do* stay on Home; sessions *done* stay on History. |

---

## Recommended structure

### Principle

> **Settings** answers: *How do I configure my account and how Kwalitec behaves for me?*  
> **History / Journey / Home** answer: *What have I practiced, where am I, what should I do next?*

### Target Student Settings (configuration centre)

```
Settings
├── Examination & plan          ← links only: “Change exam / plan” → Study Plan
├── Study preferences           ← editable (or deep-link to Preferences)
├── Appearance                  ← Light / Dark / System
├── Account                     ← email, notifications, locale, timezone
├── Data & privacy              ← weekly report export, backup, restore
├── Security (future)           ← password / sessions when shipped
└── Product participation       ← Product Check-in entry (no badge KPI wall)
```

Remove from this page:

- Learning statistics / Progress summary cluster  
- Goal progress bars (until goals are editable configuration)  
- Hero “Current examination” status card (replace with configuration link)  
- Research Journey contribution scoreboard  

### Target analytics / KPI homes

| Content | Home surface | Notes |
|---------|--------------|-------|
| Study time, sessions, completed topics | **History** | Already owns these; strengthen as single archive, not duplicate on Settings |
| Exam readiness / syllabus position | **Journey** | Progress map; avoid KPI mosaic |
| Today’s session / mission | **Home** | Decision surface only — no decorative KPI strip |
| Examination selection | **Study Plan (Choose Exam)** | Authoritative configuration |

### Target product Settings IA (sidebar)

| Keep | Demote / merge | Remove or relocate |
|------|----------------|--------------------|
| Preferences (Appearance + study goal) | Account Status → “System status” under Data or General diagnostics | Research Journey KPI block → Check-in / research |
| Data (export / backup / restore) | Duplicate Appearance on Account Status | General landing (already redirected under sole runtime) |
| Profile → Account (email + future identity fields) | — | — |
| Product Check-in entry | — | — |

### Recommended information architecture diagram

```text
                    Student EOS
┌──────────────────────────────────────────────────────────┐
│  Home          Journey       Revision      History       │
│  (Mission)     (Progress)    (Support)     (Analytics    │
│                                             archive)     │
└──────────────────────────────────────────────────────────┘
         │              │                         │
         │              │                         └── Study time, Sessions,
         │              └── Topics map / readiness        Topics mastered
         └── Start session

  Study Plan ──────────────── Examination & availability (Learning config)

  Settings ─────────────────── Configuration centre only
         ├── Preferences / Appearance / Account
         ├── Data & privacy
         └── Links → Study Plan (change exam), History (view progress)
```

---

## Components to relocate

| Component | From | To | Mode |
|-----------|------|----|------|
| Progress summary (study time, sessions, topics mastered, readiness) | Student Settings | **History** (primary); readiness cue on **Journey** if needed | Remove duplicate; do not invent a third Analytics nav item |
| Current Examination hero | Student Settings | **Study Plan**; optional quiet identity on Home/Journey | Replace with “Manage examination” link in Settings |
| Goals progress bars | Student Settings | **Journey** or omit until editable | Remove decorative bars from Settings |
| Research Journey badges | Settings → Profile | Product Check-in / research journey surface | Keep Check-in entry in Settings |
| Account Status curriculum/plan labels | Settings → Account Status | Study Plan (canonical); quiet diagnostics only in Settings | Demote |
| Application General / About | Settings → General | **Help** (already mirrored) | Keep sole-runtime redirect |

**Stay in Settings (do not relocate)**

- Appearance  
- Daily study goal / study preferences (when editable)  
- Account identity fields  
- Data export, backup, restore  
- Product Check-in *entry*  
- Disclosed diagnostics  

---

## Navigation impact

| Change | Impact | Risk mitigation |
|--------|--------|-----------------|
| Settings page loses KPI cluster | Students seeking “my stats” must use **History** | Help already documents History for sessions/study time; add a quiet “View progress” link from Settings → History during migration |
| Current Examination leaves Settings | Exam identity discovered via Study Plan / Home | Keep one-line “Exam: …” only where orientation needs it; never as Settings hero |
| Nav label **Settings** still maps to `/student/profile` | No new primary nav item required | Optionally rename page H1 to **Settings** consistently and retire “Profile” language in descriptions |
| Product Settings remains nested | Preferences / Data stay reachable | Preserve Help paths `Settings → Preferences` / `Settings → Data` |
| No new “Analytics” primary nav | Avoids PX-002A collision | History remains the student analytics archive |
| Mission Centre | No new destination | Home continues as mission/session start |

**Primary nav (feature mode) — unchanged count**

`Home · Journey · Revision · History · Settings · Choose Exam · Help`

IA success does **not** require adding Analytics or Mission Centre to chrome. It requires clarifying what each existing destination owns.

---

## Migration strategy

Phased — **review first (this report), implement later**. Do not ship a big-bang Settings rewrite without Help and deep-link updates.

### Phase 0 — Alignment (docs / acceptance)

1. Treat this report as the Settings IA contract for subsequent UX programmes.  
2. Confirm with DX-002: Profile KPI cards remain **Remove**; History remains practice archive.  
3. Freeze new KPI additions on `/student/profile`.

### Phase 1 — Subtract analytics from Settings (low risk)

1. Remove the **Learning statistics / Progress summary** section from `student/profile.html`.  
2. Add a single secondary link: “View study progress” → `student.history`.  
3. Update page description from “Examination, preferences, goals, and account” to configuration-first copy.  
4. Regression: profile presentation tests + Help smoke for Settings → Data / Preferences.

### Phase 2 — Examination identity

1. Replace Current Examination hero with **Manage examination** → Study Plan (or quiet label + link).  
2. Ensure Home/Journey still surface exam identity where orientation requires it (already partially true via countdown / plan).  
3. Preserve B2 invariant: examination label must not contradict active plan (`_authoritative_examination_label`).

### Phase 3 — Goals & Research Journey

1. Hide goal progress bars until goals are editable configuration.  
2. Move Research Journey scoreboard off Settings → Profile; retain Check-in CTA.  

### Phase 4 — Consolidate Settings shells

1. Fold remaining Student Settings summaries into a single configuration hub that hosts or deep-links product Settings sections (Preferences, Data, Account).  
2. Retire duplicate Appearance on Account Status.  
3. Demote Account Status plan/curriculum rows to diagnostics or Study Plan links.  
4. Keep sole-runtime `/settings/` → profile (or final Settings hub) redirect.

### Phase 5 — Validate

1. Dogfood: can a student change appearance, export data, and find study time without seeing KPIs on Settings?  
2. Navigation: History remains discoverable for stats; Study Plan for exam change.  
3. No new primary nav destinations; Help copy updated only where paths change.

**Out of scope for migration**

- Redesigning History into a KPI dashboard (forbidden by DX-001/DX-002)  
- Restoring legacy Analytics / Student Dashboard as the analytics home  
- Schema or readiness-engine changes  
- Founder Console Settings IA (separate surface)

---

## Success criteria (acceptance for later implementation)

| Criterion | Measure |
|-----------|---------|
| Settings is configuration-only | No study-time / sessions / topics-mastered / readiness KPI cluster on Settings |
| Analytics have a clear home | History (and Journey for syllabus/readiness) own those numbers |
| Examination is configurable elsewhere | Change path lives on Study Plan; Settings only links |
| Navigation stays intuitive | Same primary destinations; Help paths still resolve |
| Premium exam OS posture | Configuration centre ≠ progress dashboard |

---

## Architecture compliance

| Concern | Assessment |
|---------|------------|
| Layering | IA-only; no blueprint/service changes in UX-004 |
| Curriculum V1/V2 | N/A — no traversal or import changes |
| Sole runtime | Reinforces Student EOS Settings as config; product Settings as nested controls |
| DX-002 alignment | Extends Profile KPI removal and Settings-as-configuration type |

---

## Migration impact

**None** (documentation / IA review only). No Alembic or schema effects.

---

## Technical debt

| Debt | Note |
|------|------|
| Dual Settings shells | Student Profile vs `/settings/*` still dual; Phase 4 consolidation pending |
| Preferences partially session-only | Daily goal hours stored in session — persistence is separate from IA |
| Label collision Settings vs Profile | Nav says Settings; routes/docs still say Profile in places |
| Account Status URL slug | `/settings/internal-alpha` is legacy; student-visible label already cleaned |

---

## Known limitations

- This programme **does not implement** UI moves.  
- Does not redesign History layout (separate DX backlog item B-004 / History P1).  
- Does not invent a Mission Centre product surface.  
- Does not audit Founder Console Settings beyond noting it is out of scope.  
- Goals may still appear empty or stubbed depending on Twin/projection data — IA treats them as non-configuration until editable.

---

## Files created

- `knowledge/product/ux004_settings_information_architecture/UX004_INFORMATION_ARCHITECTURE_REPORT.md`

## Files modified

- None (review-only)

## Tests executed

- None (documentation-only)

## Commit

- Not requested / not created for this milestone

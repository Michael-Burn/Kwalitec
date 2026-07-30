# VISUAL ARCHIVE — Screenshots Catalogue

**Release:** `2.0.0-beta.1`  
**Policy:** Binary screenshots are **indexed**, not mass-duplicated into this archive (avoids archive bloat). Paths below are the authoritative source collections at archival time.

See also: `SOURCE_COLLECTIONS.md`, `RC001_PRODUCT_SCREENSHOT_INDEX.md`.

---

## Existing collections

| Collection | Path | Approx. files | Content |
|---|---|---:|---|
| Product RC-001 multi-breakpoint set | `knowledge/product/rc001/screens/` | 162 | Student Home, Journey, Revision, History, Profile, Study Plan, Settings, Help, Session flow, empty/error/dark/light — 9 breakpoints |
| Product RC-001 index | `knowledge/product/rc001/SCREENSHOT_INDEX.md` | — | Catalogue of the 162 set (copied here as `RC001_PRODUCT_SCREENSHOT_INDEX.md`) |
| FV-002 Founder/Student dogfood | `knowledge/evidence/releases/FV002/screenshots/` | ~80 | Login, Founder Console, Studio create/upload/process/preview/approve, student home/enrol/exam flows |
| RC release-candidate evidence | `knowledge/release/rc001_release_candidate/_evidence/screenshots/` | ~11 | Login, Founder console/overview, subjects, studio hub, system ops, health, help/release |
| Login polish evidence | `knowledge/engineering/rc20260729_02_login_experience_polish/_evidence/screenshots/` | (present) | Login experience polish captures |

---

## Required screens (AR-001 Workstream 9)

Status relative to **deployed Private Beta surfaces**. “Catalogue” = existing archives cover the screen. “Capture after deploy” = recommended manual production capture for museum completeness of beta.1 chrome (Private Beta badge, version identity).

| Screen | Route (canonical) | Status | Notes |
|---|---|---|---|
| **Student Home** | `/student/` | **Catalogued** | Full 9-breakpoint set in product RC-001 screens; FV-002 student home samples |
| **Mission** | Home mission panel + `/session/...` | **Catalogued** | Session overview/activity/reflection/summary in product RC-001; mission is session-backed under sole runtime |
| **Tutor** | `/student/tutor` | **Capture after deploy** | UX-001 introduced dedicated Tutor UI; not listed in the older 162-screen product RC-001 index — capture production Tutor (empty + explained states) |
| **Knowledge Map** | `/student/knowledge_graph` | **Capture after deploy** | UX-001 dedicated KG; capture production hierarchy with certified CS1 |
| **Journey** | `/student/journey` | **Catalogued** | Product RC-001 9-breakpoint + empty state |
| **Study Session** | `/session/<id>/…` | **Catalogued** | Overview, activity, reflection, summary across breakpoints |
| **Founder Dashboard** | `/console/` | **Catalogued** | FV-002 + RC release-candidate evidence (`01_founder_console`, overview) |
| **Curriculum Studio** | `/console/studio/…` | **Catalogued** | FV-002 extensive Studio pipeline screenshots; RC evidence studio hub / subjects |
| **Curriculum Health** | `/console/curriculum-health` | **Capture after deploy** | UX-001 surface; recommend production capture with certified CS1 health strip |
| **Private Beta Dashboard** | `/console/beta` | **Capture after deploy** | PB-001 surface; capture empty cohort and first-enrol states when available |

---

## Recommended manual capture checklist (post-deploy)

Capture at desktop (~1440px) and one mobile width (~390px), signed-in as Founder (dual capability) and as a pure student account where relevant:

1. Student Home — Today’s Mission focal, Private Beta badge visible  
2. Mission / Session — in-progress Focus mode  
3. Tutor — grounded explanation with citations  
4. Knowledge Map — expanded chapter/topic/LO  
5. Journey — overall mastery + next focus  
6. Study Session summary after completion  
7. Founder Console home  
8. Curriculum Studio subject workspace (certified CS1)  
9. Curriculum Health  
10. Private Beta Dashboard  

Store new captures under:

`knowledge/archive/releases/v2_0_0_beta_1/screenshots/manual_production/`

(create on first capture; keep filenames `YYYYMMDD_<role>_<screen>.png`).

---

## Integrity note

Screenshots from earlier programmes (product RC-001 screen set, FV-002) may predate final UX-001 / PB-001 chrome. They remain historically valid as **evolution evidence**. Production manual captures close the gap for Tutor, Knowledge Map, Curriculum Health, and Private Beta Dashboard at the true `2.0.0-beta.1` deploy.

---

*AR-001 visual archive catalogue.*

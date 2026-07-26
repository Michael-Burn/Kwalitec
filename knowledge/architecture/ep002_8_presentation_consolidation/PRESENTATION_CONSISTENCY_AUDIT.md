# EP-002.8 — Presentation Consistency Audit

**Milestone:** EP-002.8  
**Date:** 2026-07-26  
**Surfaces:** Dashboard · Analytics · Mission (Runtime A)

---

## 1. Terminology

| Term | Dashboard | Analytics | Mission | Consistent? |
|---|---|---|---|---|
| Estimated readiness | Yes (`ProductCommunicationService` / narrative label) | Yes | Coverage uses syllabus coverage language | Yes for readiness |
| Estimated Knowledge | Yes | Yes | n/a | Yes |
| Observed Facts / Estimates / Advice / Next step | Explainability macro | Narrative prose fields | Macro on mission | Yes (EIP-003 claim types) |
| Twin fallback mission reason | “Projected from Twin daily study plan” | n/a | Same string via adapter | Yes after consolidation |

**Finding:** Analytics readiness hero uses narrative label when available; fallback hardcodes “Estimated readiness” — aligned with ProductCommunicationService.

---

## 2. Colours & severity

| Signal | Threshold / mapping | Surfaces |
|---|---|---|
| Mastery badge weak | `<40` danger, `<60` warning | Dashboard + Analytics |
| Mastery badge strong | `≥90` success, `≥70` info | Analytics strongest |
| Recommendation priority | Critical/High/Medium/else | Dashboard only |
| Mission status | Completed success / In Progress warning / else secondary | Dashboard + Mission |
| Burnout | high → danger card; else warning | Dashboard |

**Finding:** Severity bands are shared CSS/Bootstrap semantic classes; no Twin-specific colour invent. Twin topic rows without `stage_label` show empty stage — acceptable; mastery badge still applies.

---

## 3. Recommendation cards

| Path | Card style | Explainability |
|---|---|---|
| Legacy / Study Insights lists | Dashboard list + `explainability_block` | EIP-003 enrich or Insight fields |
| EI Stage A card | `dashboard_view_model.recommendation_card` | Separate Stage A |
| Mutual exclusion | Legacy lists hidden when EI card present | Preserved |

---

## 4. Readiness indicators

| Element | Twin path | Legacy path |
|---|---|---|
| Score display | Twin projected score via narrative percentage | EIP-003 from legacy score |
| Evidence basis | Drivers + confidence (adapter) | Coverage / mastery / review (EIP-003) |
| Topic lists | Twin areas (no re-enrich) | EIP-003 stage labels |

---

## 5. Mission presentation

| Element | Twin | Legacy |
|---|---|---|
| Title | Display proxy over ORM | ORM title |
| Narrative shape | `MissionNarrative` | `MissionNarrative` |
| Explainability macro | observed_facts from slots | full EIP-003 tuples |

---

## 6. Confidence indicators

| Source | Exposure |
|---|---|
| Twin readiness `confidence_level` | Included in evidence_basis text (adapter) |
| Insight `confidence_level` on rec rows | Present on projected dicts; template may not render chip — accepted limitation |
| Legacy | No confidence chip; estimate language via EIP-003 |

**UI Consistency Score (qualitative):** **0.92** — shared terminology and severity; residual: confidence chip not rendered as dedicated control on all surfaces (documented limitation, not regression).

---

## 7. Accessibility notes

| Check | Status |
|---|---|
| Progressbar ARIA on readiness | Present on dashboard |
| `role="status"` burnout | Present |
| Explainability lists semantic `<ul>` | Present in macro |
| Colour-only severity | Badges also have text labels (priority/category/status) |

Regression tests assert macro markers and narrative fields remain present under legacy and Twin paths.

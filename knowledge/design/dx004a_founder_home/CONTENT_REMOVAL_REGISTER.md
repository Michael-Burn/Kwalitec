# Content Removal Register

**Programme:** DX-004A  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Source of legacy inventory:** `app/founder/dashboard/templates/founder_dashboard/overview.html` + DX-002/DX-003 audits  
**Rule:** Zero Legacy — do not rearrange; remove and replace with L0–L3 only.

---

## Method

Each legacy element is classified:

| Class | Meaning |
|---|---|
| **Delete** | Never on Founder Home |
| **Relocate** | Belongs on another surface |
| **Replace** | Intent survives as L0/L1/L2 structure |
| **Keep** | Survives with rewrite (rare) |

---

## Legacy → target map

| # | Legacy element | Class | Destination / replacement | Authority |
|---|---|---|---|---|
| 1 | Eyebrow: Console · Alpha · version | **Delete** | Omit; Alpha once in shell if required | DX-001 L3 leak; DX-003 inventory |
| 2 | Page title “Console Home” / Overview label | **Replace** | Title **Home** | DX-004A; terminology update |
| 3 | “Operational pulse — what needs attention… timestamp · timezone” | **Delete** | — | DX-003 Delete; FP pulse essay |
| 4 | Header Primary “Review attention queue (N)” | **Replace** | L0 Primary = publication Resume / Continue (not Attention Center) | DX-004A publication-first |
| 5 | Section “Attention Required” | **Replace** | L1 Publication Queue (publication gates only) | DX-002 B-001; DX-004A L1 |
| 6 | Attention KPI card: Pending content reviews | **Relocate** | Support inbox / queue | DX-002 KPI Audit |
| 7 | Attention KPI card: Platform Health % | **Relocate** | Settings → Operations / Platform Intelligence | KPI Audit |
| 8 | Attention KPI card: High-severity findings | **Relocate** | Findings (via Support / Settings) | KPI Audit |
| 9 | Attention KPI card: Needs intervention | **Relocate** | Attention queue (nested) | KPI Audit |
| 10 | Alerts list under Attention | **Relocate** | Operations / Attention — not Home L0 | DX-004A |
| 11 | Section “Platform Summary” (entire) | **Delete** | — | DX-001 KPI policy; FP-07 |
| 12 | KPI: Active participants | **Delete** from Home | Students catalogue / Research | KPI Audit |
| 13 | KPI: Check-ins today | **Delete** from Home | Research | KPI Audit |
| 14 | KPI: Avg experience / would open tomorrow | **Delete** from Home | Research | KPI Audit |
| 15 | KPI: Alpha health + Build number | **Delete** from Home | Operations | KPI Audit; L3 |
| 16 | Section “Quick Actions” (entire) | **Delete** | Shell nav + L0 Primary | FP-03; Nav audit |
| 17 | QA: Review support inbox (Primary weight) | **Relocate** | Support nav | — |
| 18 | QA: Open operations | **Relocate** | Settings → Operations | — |
| 19 | QA: Manage content | **Relocate** | Subjects / Curriculum Studio nav | — |
| 20 | QA: Platform Intelligence | **Relocate** | Settings nested | — |
| 21 | Section “Operational detail” | **Delete** from Home | — | DX-003 inventory |
| 22 | Card: Recent support | **Relocate** | Support | — |
| 23 | Card: Attention queue list | **Relocate** / selective **Replace** | Publication rows → L1; student interventions → Attention | DX-004A |
| 24 | Card: Vision Journal | **Relocate** | Settings / Vision (nested) | Wrong job on Home |
| 25 | “Open Attention Center” section link | **Delete** | Not Home chrome | Duplicate nav |
| 26 | Decorative card chrome as default | **Delete** | Lists | DX-001 cards policy |
| 27 | Multiple Primary-weight buttons | **Delete** | Exactly one Primary | DX-001 / DX-004A |
| 28 | Welcome / motivational patterns | **Delete** | — | Explicit forbid |
| 29 | Charts / usage metrics / insights widgets | **Delete** | — | Explicit forbid |
| 30 | Large hero / feature promotion | **Delete** | — | Explicit forbid |

---

## Explicit forbid list (DX-004A) — confirmation

| Forbidden content | Present in legacy? | Status |
|---|---|---|
| Welcome messages | No (elsewhere Welcome modal) | Keep off Home; kill modal in DX-004 nav work |
| Platform summaries | Yes | Removed |
| Quick statistics / decorative KPIs | Yes | Removed |
| Pulse widgets | Yes (copy + health) | Removed |
| Insights | No on Overview | Stay off |
| Health scores | Yes | Removed |
| Charts | No | Stay off |
| Usage metrics | Yes (check-ins, participants) | Removed |
| Motivational text | Pulse essay adjacent | Removed |
| Large hero sections | Header stack | Flattened to title + L0 |
| Feature promotion | Quick Actions theatre | Removed |
| Multiple CTAs | Yes | One Primary |
| Space-filling widgets | Detail grid | Removed |

---

## Estimated visual reduction

| Measure | Legacy Overview | Target Founder Home | Δ |
|---|---|---|---|
| Distinct content sections | 5 (header + attention + summary + QA + detail) | 3 page sections (L0–L2) + shell | **~40%** fewer sections |
| Metric / KPI tiles | 8 | 0 | **−100%** KPI tiles |
| Primary-weight buttons | 2–5 competing | **1** | **~80%** fewer Primaries |
| Card containers | ~10+ | 0–1 (optional L0) | **~90%** fewer cards |
| Visible interactive destinations in-page | ~15–20 | Primary + queue/recent rows | **~60–70%** fewer in-page destinations |
| Independent decisions (DX-003) | 4–6 | **1** | **~75%** |

---

## What is *not* removed from the product

Removal from **Founder Home** is not deletion from Kwalitec.

| Capability | Lives at |
|---|---|
| Support reviews | Support |
| Platform / Alpha health | Settings → Operations / Intelligence |
| Findings | Findings (nested) |
| Vision Journal | Nested under Settings / Research |
| Attention interventions | Attention (nested) or Support |
| Subject create / browse | Subjects |
| Workspace open | Curriculum Studio / Subjects |

---

## Implementation note

Replace `overview.html` content model with a publication-centred view-model (current workspace, queue rows, recent published). Do not CSS-hide legacy sections — **delete** markup and dead view-model fields from the Home path.

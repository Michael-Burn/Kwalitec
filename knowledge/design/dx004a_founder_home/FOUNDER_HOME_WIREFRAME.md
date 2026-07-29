# Founder Home Wireframe

**Programme:** DX-004A  
**Status:** Binding layout intent (not Figma; not CSS)  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001 typography/spacing; DX-002 Home type; DX-003 reading flow  
**Companion:** `FOUNDER_HOME_ARCHITECTURE.md`

---

## Design posture

Empty canvas. Zero legacy layout. Operational Elegance.

One column. Whitespace carries hierarchy. Exactly one Primary.

---

## Primary viewport (desktop ≥1024)

All content below the shell nav fits **above the fold** at 900–1080px height without requiring scroll to find the Primary.

```
╔══════════════════════════════════════════════════════════════════╗
║  CONSOLE SHELL                                                   ║
║  [Mark]  Home  Subjects  Curriculum Studio  Students  Support    ║
║          Settings ▾                                              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Home                                              ← 24px        ║
║                                                                  ║
║                                                                  ║
║  Current Work                                      ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  CS1 Financial Reporting                           ← 16px sb     ║
║  Stage · Validation                                ← 14px        ║
║                                                                  ║
║  [ Resume Publication ]                            ← ONE Primary ║
║                                                                  ║
║                                                                  ║
║  Publication Queue                                 ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  CS1 Valuation          Awaiting Approval          ← row         ║
║  CS2 Audit              Ready to Publish                         ║
║  CS1 FR (v2)            Awaiting Validation                      ║
║                                                                  ║
║                                                                  ║
║  Recent Publications                               ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  CS0 Foundations        Published 22 Jul           ← 14/12px     ║
║  … (max 5)                                                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Notes**

- No eyebrow with version / Alpha / build.  
- No executive summary / pulse sentence.  
- No KPI grids.  
- No Quick Actions strip.  
- No Operational detail card mosaic.  
- Section rules are optional hairlines (`brand-divider` / neutral) — not card chrome.

---

## Typography map

| Element | Token | Size |
|---|---|---|
| Page title “Home” | `type-page` | 24px / 600 |
| “Current Work” / “Publication Queue” / “Recent Publications” | `type-section` | 18px / 600 |
| Subject name (L0) | `type-body` semibold | 16px / 600 |
| Stage line | `type-support` | 14px / 400 |
| Queue subject | `type-body` | 16px / 400 |
| Queue status | `type-support` | 14px / 400 |
| Recent subject | `type-support` | 14px / 400 |
| Recent date | `type-caption` | 12px / 500 |
| Primary button label | `type-body` | 16px / 600 |

---

## Spacing map (DX-001)

| Region | Token |
|---|---|
| Page top padding | `space-7` (64) or `space-6` (48) |
| Title → L0 | `space-6` (48) |
| L0 label → subject | `space-3` (16) |
| Subject → stage | `space-1` (4) |
| Stage → Primary | `space-4` (24) |
| L0 → L1 | `space-6` (48) |
| L1 → L2 | `space-6` (48) |
| Queue row gap | `space-2`–`space-3` (8–16) |
| Content max width | Prefer ~720–800px primary column (calm); full content width of Console content well is acceptable if density stays list-like |

---

## L0 detail wireframe

```
Current Work
────────────

{subject_name}
Stage · {stage_name}
{optional: Blocking · N}     ← only if actionable

[ {primary_label} ]
```

Primary variants (mutually exclusive — one shown):

| State | Button |
|---|---|
| In progress | Resume Publication |
| Mid-stage continue | Continue |
| Gate awaiting human | Review Subject |
| Ready to publish | Publish |
| Empty product | Create Subject |

---

## L1 detail wireframe

```
Publication Queue
─────────────────

{subject}     {status}
{subject}     {status}
{subject}     {status}

View all in Subjects          ← text link only if truncated
```

Row interaction: entire row is a quiet link (cursor + focus ring). **No** `btn-primary` in the list.

Status vocabulary (DX-003): Awaiting Validation · Awaiting Approval · Ready to Publish · Incomplete.

---

## L2 detail wireframe

```
Recent Publications
───────────────────

{subject}     Published {date}
{subject}     Published {date}
…
```

Omit section when count = 0. No “No publications yet” essay on Home if L0 empty state already covers Create Subject.

---

## Empty state wireframe

```
Home

Current Work
────────────

No publication work in progress.

[ Create Subject ]
```

Omit L1 and L2 when empty (or L1 one muted line only — prefer omit).

---

## Mobile / narrow (<768)

```
Home

Current Work
{subject}
{stage}
[ Primary ]          ← full-width Primary OK

Publication Queue
{rows stacked}

Recent Publications
{rows stacked}
```

Single column preserved. Primary remains first interactive control after title + L0 identity. Touch targets ≥44px height. Keyboard: tab order Title (skip) → Primary → queue rows → recent rows.

---

## Accessibility

| Requirement | Spec |
|---|---|
| Landmark | `<main>` / page `article` with `aria-labelledby` on Home title |
| Primary | One visible Primary; accessible name = button label |
| Focus | Visible focus ring on Primary and list rows |
| Contrast | Body/Support AA on surface (DX-001 / Brand neutrals) |
| Status | Not colour-alone; text status labels |
| Motion | None required; if any, ≤250ms |

---

## Explicit non-wireframes

Do **not** implement:

```
[KPI][KPI][KPI][KPI]
[KPI][KPI][KPI][KPI]
[Primary][Primary][Secondary][Tertiary]
[Card][Card][Card]
```

That is the legacy Overview — rejected under Zero Legacy Rule.

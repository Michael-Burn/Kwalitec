# Student Home Wireframe

**Programme:** DX-005A  
**Status:** Binding layout intent (not Figma; not CSS)  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001 typography/spacing; DX-002 Home type; DX-003 reading flow  
**Companion:** `STUDENT_HOME_ARCHITECTURE.md`

---

## Design posture

Empty canvas. Zero legacy layout. Mastery First.

One column. Whitespace carries hierarchy. Exactly one Primary.

---

## Primary viewport (desktop ≥1024)

All content below the shell nav fits **above the fold** at 900–1080px height without requiring scroll to find the Primary.

```
╔══════════════════════════════════════════════════════════════════╗
║  STUDENT SHELL                                                   ║
║  [Mark]  Home  Choose Exam  History  Settings  Help              ║
╠══════════════════════════════════════════════════════════════════╣
║                                                                  ║
║  Home                                              ← 24px        ║
║                                                                  ║
║                                                                  ║
║  Current Mission                                   ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  CS1 Financial Reporting                           ← 16px sb     ║
║  Objective · Lease liability — initial recognition ← 16/14px     ║
║  In progress · ~25 min                             ← 14px        ║
║                                                                  ║
║  Why now · Open session — continue question 4      ← 14px        ║
║  After · Short check on this objective             ← 14px        ║
║                                                                  ║
║  [ Continue Session ]                              ← ONE Primary ║
║                                                                  ║
║                                                                  ║
║  Learning Queue                                    ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  Assessment Ready     CS1 FR · Topic 2.1           ← row         ║
║  Revision Due         Deferred tax — recognition                 ║
║                                                                  ║
║                                                                  ║
║  Recent Progress                                   ← 18px        ║
║  ─────────────────────────────────────────────                   ║
║                                                                  ║
║  Session · Lease classification        Yesterday   ← 14/12px     ║
║  … (max 5)                                                       ║
║                                                                  ║
╚══════════════════════════════════════════════════════════════════╝
```

**Notes**

- No greeting / welcome / “Good morning”.  
- No Study Sensei narrator block.  
- No readiness % / countdown cards.  
- No Journey / Guidance / Coach panels.  
- No Quick Actions / milestones disclosure.  
- No welcome modal.  
- Section rules are optional hairlines — not card chrome.

---

## Typography map

| Element | Token | Size |
|---|---|---|
| Page title “Home” | `type-page` | 24px / 600 |
| “Current Mission” / “Learning Queue” / “Recent Progress” | `type-section` | 18px / 600 |
| Subject name (L0) | `type-body` semibold | 16px / 600 |
| Objective line | `type-body` or `type-support` | 16px / 400 or 14px |
| Status · duration | `type-support` | 14px / 400 |
| Why now / After | `type-support` | 14px / 400 |
| Queue title | `type-body` | 16px / 400 |
| Queue meta | `type-support` | 14px / 400 |
| Recent activity | `type-support` | 14px / 400 |
| Recent time | `type-caption` | 12px / 500 |
| Primary button label | `type-body` | 16px / 600 |

---

## Spacing map (DX-001)

| Region | Token |
|---|---|
| Page top padding | `space-7` (64) or `space-6` (48) |
| Title → L0 | `space-6` (48) |
| L0 label → subject | `space-3` (16) |
| Subject → objective | `space-1` (4) |
| Objective → status | `space-1` (4) |
| Status → why/after | `space-3` (16) |
| Why/after → Primary | `space-4` (24) |
| L0 → L1 | `space-6` (48) |
| L1 → L2 | `space-6` (48) |
| Queue row gap | `space-2`–`space-3` (8–16) |
| Content max width | Prefer ~720–800px primary column |

---

## L0 detail wireframe

```
Current Mission
───────────────

{subject_name}
Objective · {objective_label}
{status_label} · {optional_duration}

Why now · {why_now}
After · {after_completion}

[ {primary_label} ]
```

Primary variants (mutually exclusive — one shown):

| State | Button |
|---|---|
| Open session | Continue Session |
| Mission ready | Start Session / Resume Mission |
| Assessment due | Start Assessment |
| Findings waiting | Review Findings |
| Revision ack / due | Continue / Begin Revision |
| No plan | Choose Exam |
| Day complete | *(no button — quiet copy)* |

---

## L1 row wireframe

```
{attention_label}     {subject} · {short_focus}
```

Examples:

```
Resume Session        CS1 FR · Lease liability
Assessment Ready      CS1 FR · Topic 2.1
Revision Due          Deferred tax — recognition
Findings Ready        CS1 FR · Topic 2.1 results
```

No icons required. If icons used: Lucide only, muted, not decorative clusters.

---

## L2 row wireframe

```
{activity_type} · {short_title}          {relative_time}
```

Example:

```
Session · Lease classification          Yesterday
Assessment · Topic 2.1                  Mon
```

Omit entire L2 section when empty.

---

## Mobile (≤640)

```
╔════════════════════════════╗
║  Home                      ║
║                            ║
║  Current Mission           ║
║  {subject}                 ║
║  {objective}               ║
║  {status}                  ║
║  Why now · …               ║
║  [ Continue Session ]      ║
║                            ║
║  Learning Queue            ║
║  …                         ║
║                            ║
║  Recent Progress           ║
║  …                         ║
╚════════════════════════════╝
```

- Primary remains first actionable control after heading.  
- Shell may be top or bottom tabs — still L3 only; no in-page Quick Actions.  
- Why/After may collapse to Why only on very small heights; After remains in Mission DTO for Session.

---

## Empty state wireframe

```
Home

No exam selected yet.
Choose an exam to begin studying.

[ Choose Exam ]
```

---

## Day-complete wireframe

```
Current Mission
───────────────

{subject_name}
Complete for today

Today’s mission is finished. Return tomorrow to continue.

(Learning Queue omitted if empty)
(Recent Progress ≤5 if available)
```

No congratulations banner. No confetti. No streak.

---

## Reading flow (target)

```
Enter shell
  → Recognise “Home”
  → Recognise Current Mission (subject + objective)
  → Find Primary
  → Act (one click)
  → Session / Assessment loads with continuity
```

Legacy failure (do not recreate): Greeting → Sensei → eyebrow → title → status → multi-why → educational panel → alternatives → readiness cards → Primary buried → Quick Actions.

---

## Motion

- None required for architecture.  
- If used: ≤250ms; Primary appear / focus only.  
- No celebration animations on Home.

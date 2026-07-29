# Discovery Wireframe

**Programme:** DX-005B  
**Status:** Binding layout authority (ASCII)  
**Release Candidate:** `RC-2026.07.29-01`  
**Companion:** `DISCOVERY_ARCHITECTURE.md`  
**Note:** No Figma in this programme — this file is the layout authority.

---

## 1. Default — Ready offerings present

```
┌──────────────────────────────────────────────────────────────────┐
│  Kwalitec                                              [avatar]  │
│  Home · Choose Exam · History · Settings · Help         ← L3    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Choose Exam                                                     │
│                                                                  │
│  ┌────────────────────────────┐  Family ▾   Status ▾   A–Z ▾    │
│  │ Search exams…              │                         ← L1    │
│  └────────────────────────────┘                                  │
│                                                                  │
│  Ready to begin                                         ← L0    │
│  ────────────────────────────────────────────────────────────    │
│                                                                  │
│  (●)  CS1 Valuation                                              │
│       Short factual description of the exam.                     │
│       Scope · ~N topics          Updated 12 Jul 2026   ← L2    │
│                                                                  │
│  ( )  CS1 Financial                                              │
│       Short factual description of the exam.                     │
│       Scope · ~N topics          Updated 08 Jul 2026             │
│                                                                  │
│                                                                  │
│                         [ Begin Learning ]              ← Primary│
│                                                                  │
│  Coming soon                                            ← sec.  │
│  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    │
│                                                                  │
│       CM2 …                                                      │
│       Under preparation.                                         │
│                         [ Notify when available ]       ← quiet │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Notes

- Selected Ready row uses single-select (radio or equivalent).  
- **Begin Learning** is the only filled Primary; sits with Ready band / after selection — not duplicated in Coming Soon.  
- Coming Soon uses quieter type, lighter rules, no radio.  
- **Notify when available** is Secondary / text — never filled Primary weight.  
- Optional quiet Recommended marker on one Ready row only — no essay.

---

## 2. Confirm step (commitment)

Shown after Ready selection when additional confirmation is required (or as a dedicated review beat before POST).

```
┌──────────────────────────────────────────────────────────────────┐
│  Choose Exam                                                     │
│                                                                  │
│  Confirm                                                         │
│                                                                  │
│  CS1 Valuation                                                   │
│  Exam date · 15 Sep 2026                                         │
│  Availability · as set                                           │
│  Defaults applied · quietly (one line) or omitted                │
│                                                                  │
│  [ Begin Learning ]                                              │
│  Change selection                                                │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

| Element | Rule |
|---|---|
| Filled Primary | **Begin Learning** only |
| Change selection | Text / ghost Secondary — returns to L0 |
| Forbidden | Twin filled Yes/No; feature list; marketing; surprise multi-section defaults |

If exam date / availability are collected before confirm, those steps use quiet **Continue** chrome — not a second “Primary of the product.”

---

## 3. Empty — no Ready subjects

```
┌──────────────────────────────────────────────────────────────────┐
│  Choose Exam                                                     │
│                                                                  │
│                                                                  │
│           No Ready subjects yet.                                 │
│                                                                  │
│           Return later                                           │
│                                                                  │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Exactly Reason → Next Action. No tips, illustrations essays, or second CTA.

If Coming Soon items exist while Ready is empty: Coming Soon may appear **below** the empty Ready reason as the secondary band — still no Begin Learning; empty Ready Reason remains L0.

---

## 4. Search / filter zero results

```
┌──────────────────────────────────────────────────────────────────┐
│  Choose Exam                                                     │
│                                                                  │
│  [ actuarial xyz________ ]  Family ▾  Status ▾  A–Z ▾           │
│                                                                  │
│           No matches.                                            │
│           Clear query                                            │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

Clear query / Clear filters is Secondary. Do not invent Begin Learning when nothing is selectable.

---

## 5. Coming Soon only (no Ready)

```
┌──────────────────────────────────────────────────────────────────┐
│  Choose Exam                                                     │
│                                                                  │
│           No Ready subjects yet.                                 │
│           Return later                                           │
│                                                                  │
│  Coming soon                                                     │
│  - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -    │
│       Subject A …          [ Notify when available ]             │
│       Subject B …          [ Notify when available ]             │
└──────────────────────────────────────────────────────────────────┘
```

Ready emptiness owns the message. Coming Soon does not pretend to be Ready.

---

## 6. Enrolment gated (visible, not selectable)

```
│  ( )  CS1 Valuation                                    Ready*    │
│       Enrolment opens when student access is enabled.            │
│       Scope · …                  Updated …                       │
```

\*Badge may say Ready for publication honesty, but row is **not selectable** and **Begin Learning** stays disabled. Prefer one quiet prep line — not a support essay wall. See `READY_STATE_SPEC.md`.

---

## 7. Mobile (first principles)

```
┌────────────────────────────┐
│ Choose Exam                │
│ [ Search…            ]     │
│ Family · Status · Sort     │
│                            │
│ Ready to begin             │
│ (●) Title                  │
│     Description            │
│     Scope · Updated        │
│                            │
│ ( ) Title …                │
│                            │
│ [ Begin Learning ]         │
│                            │
│ Coming soon                │
│   Title · Notify…          │
└────────────────────────────┘
```

Primary remains full-width and singular. Coming Soon collapses further (title + notify only).

---

## 8. Reading flow (DX-003)

```
Enter Choose Exam
  → Recognise page purpose (title)
  → Find Ready list (L0)
  → Confirm Ready vs Coming Soon by band
  → Select one
  → Begin Learning
  → Home
```

Do not insert marketing or KPI before selection.

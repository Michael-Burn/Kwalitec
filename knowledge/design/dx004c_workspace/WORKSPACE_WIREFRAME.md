# Workspace Wireframe

**Programme:** DX-004C  
**Status:** Binding layout authority (ASCII)  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** `WORKSPACE_ARCHITECTURE.md`, DX-001 spacing/type  

---

## 1. Desktop — Validate stage (reference)

```
┌─ Console shell ─────────────────────────────────────────────────────────┐
│ Home   Subjects   Curriculum Studio   Students   Support   Settings     │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                         │
│  CS1 · Probability                                                      │
│  Version 2026.1 · Current stage: Validate                               │
│                                                                         │
│  ┌─ Stage ────────────────────────────────────────────────────────────┐ │
│  │ Upload ✓  ·  Validate (here)  ·  Review  ·  Approve  ·  Publish    │ │
│  │                                                                    │ │
│  │ Next step for this subject                                         │ │
│  │ [ Resolve findings ]                          Blocking: 2          │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Findings (blocking)                                                    │
│  · Missing topic mapping in Section 3 — Re-run structure after fix      │
│  · Syllabus node orphaned — Attach or remove                            │
│                                                                         │
│  Stage content                                                          │
│  [ Re-run validation ]   (secondary if Primary is Resolve)              │
│                                                                         │
│  ─ Supporting ──────────────────────────────────────────────────────── │
│  Last validation: today 14:02 · Passed checks: 18 · Warnings: 1         │
│                                                                         │
│  ▶ Technical details                                                    │
│                                                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## 2. Desktop — Upload stage (clean)

```
│  CS1 · Probability                                                      │
│  Version 2026.1 · Current stage: Upload                                 │
│                                                                         │
│  ┌─ Stage ────────────────────────────────────────────────────────────┐ │
│  │ Upload (here)  ·  Validate  ·  Review  ·  Approve  ·  Publish      │ │
│  │                                                                    │ │
│  │ [ Upload documents ]                                               │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  Required sources                                                       │
│  · CMP        — not uploaded                                            │
│  · Syllabus   — not uploaded                                            │
│                                                                         │
│  (dropzone / file pickers — L1 only)                                    │
```

---

## 3. Desktop — Publish stage (ready)

```
│  CS1 · Probability                                                      │
│  Version 2026.1 · Current stage: Publish                                │
│                                                                         │
│  ┌─ Stage ────────────────────────────────────────────────────────────┐ │
│  │ Upload ✓ · Validate ✓ · Review ✓ · Approve ✓ · Publish (here)      │ │
│  │                                                                    │ │
│  │ [ Publish ]                                                        │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                         │
│  This version will become Ready for students.                           │
│  (one short sentence — no marketing essay)                              │
```

---

## 4. After Publish (not a workspace celebration page)

```
Home
  L0 Current Work → next item (or empty Create Subject)
  L2 Recent Publications
     · Probability · Published just now
```

Workspace does not retain a “Published successfully” dashboard.

---

## 5. Mobile / narrow

```
┌──────────────────────┐
│ Shell (collapsed)    │
├──────────────────────┤
│ CS1 · Probability    │
│ v2026.1 · Validate   │
├──────────────────────┤
│ Upload✓ · Validate●  │
│ (horizontal scroll   │
│  ok for stage strip) │
├──────────────────────┤
│ [ Resolve findings ] │
│ Blocking: 2          │
├──────────────────────┤
│ Finding 1 …          │
│ Finding 2 …          │
├──────────────────────┤
│ Supporting (muted)   │
│ ▶ Technical          │
└──────────────────────┘
```

Primary remains full-width and above the fold when possible. Time-to-Primary <5s still applies.

---

## 6. Layout rules

| Rule | Detail |
|---|---|
| One composition | Workspace is one operational composition, not a card dashboard |
| No KPI row | Forbidden three-up Validation/Preview/Checklist cards |
| Cards | Only if they wrap a necessary interaction (e.g. upload group); prefer plain sections |
| Stage strip | Orientation; steps are not five Primaries |
| Persistent header | Always above L0; never scrolls away on desktop if feasible (sticky allowed) |
| L3 | `<details>` or equivalent; closed by default |
| Exit | Shell nav / optional quiet “Back to Subjects” text — not a second Primary |

---

## 7. Focus order (keyboard)

1. Skip to content (if present)  
2. Persistent context (landmarks only)  
3. **Primary**  
4. Blocking findings list  
5. L1 stage controls  
6. L2 supporting  
7. L3 disclosure  

---

## 8. States to wire

| State | Wireframe note |
|---|---|
| Empty Upload | Primary = Upload documents; L1 lists required sources |
| Processing | Primary may be disabled with brief “Processing…” status — not a spinner essay |
| Blocking Validate | Primary = Resolve findings; findings at L0+L1 |
| Clear Review | Primary = Confirm structure |
| Approve | Primary = Approve |
| Publish ready | Primary = Publish |
| Publish error | Inline error + Primary becomes Retry publish |
| L2 empty | Omit section entirely |
| L3 | Always available; collapsed |

---

## 9. Explicit non-wireframes

Do not design:

- Side-by-side “Studio dashboard” + workspace  
- Floating tip badges on the stage strip  
- Confetti / celebration full-page after publish  
- Wizard step numbers as a separate route per step  

ASCII herein is the layout authority until a later visual polish programme; DX-001 tokens apply at implementation.

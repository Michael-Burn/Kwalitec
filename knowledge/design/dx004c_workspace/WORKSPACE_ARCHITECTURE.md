# Workspace Architecture

**Programme:** DX-004C  
**Status:** Binding for Publication Workspace redesign  
**Release Candidate:** `RC-2026.07.29-01`  
**Authorities:** DX-001, DX-002, DX-003, DX-004A, DX-004B  
**Implementation:** Architecture only (UI in later execution)

---

## 1. Surface identity

| Attribute | Value |
|---|---|
| **Surface name** | Publication Workspace |
| **Shell** | Console |
| **Type (DX-002)** | Workspace — stage-driven work on one object |
| **Page title** | Subject name (not “Workspace” as hero) |
| **Nav entry** | Opened from Home Resume or Subjects Open — not a catalogue itself |
| **One question** | What is the next step for this subject? |
| **One sentence (DX-003)** | Complete the next publication stage. |
| **Design target** | Execution First |

**Forbidden labels as page identity:** Dashboard, Hub, Studio Home, Pipeline Overview, Command Centre.

Curriculum Studio may remain a shell/tooling entry that lists workspaces; it must not compete with Subjects as the catalogue of record (DX-004B). The **workspace page** is the execution surface for one Subject.

---

## 2. Product philosophy

The Workspace owns **execution**. Nothing else.

| It is | It is not |
|---|---|
| Where the Founder completes publication | A catalogue of subjects |
| Stage-based operational environment | A wizard of disconnected steps |
| One decision → one Primary → feedback | An analytics or reporting wall |
| Continuity of one Subject | A navigation hub |

```
Nothing on this page exists unless it helps answer:
“What is the next step for this subject?”
```

---

## 3. Decision → Action → Feedback

Per DX-003, every stage follows:

```
Decision:  What is the next step for this subject?
    ↓
Action:    Exactly one Primary (stage-specific)
    ↓
Feedback:  Inline status update, stage advance, or return Home (after Publish)
```

| Beat | Workspace manifestation |
|---|---|
| **Decision** | Persistent context + stage header + (if any) blocking findings |
| **Action** | One Primary control in L0 |
| **Feedback** | Immediate inline result; stage transition without leaving the workspace URL family |

No loops. No dead ends. No unnecessary confirmations (Publish may keep a single confirm only if irreversible — see DX-004D for refinement).

Secondary controls (upload another file, open L2 history, expand L3 diagnostics) must never look equal-weight to the Primary.

---

## 4. Information hierarchy (L0–L3)

| Layer | Name | Purpose | Visual weight |
|---|---|---|---|
| **Persistent** | Subject context | Identity anchor — always visible | Stable header (above stage chrome) |
| **L0** | Stage decision strip | Current stage · Primary · Blocking findings | Dominant |
| **L1** | Stage content | Exactly what is needed to complete the current stage | Primary work area |
| **L2** | Supporting information | Prior validation, history, versions — only when useful | Secondary / muted |
| **L3** | Technical metadata | IDs, timestamps, diagnostics | Collapsed by default |

```
┌─────────────────────────────────────────────────────────────┐
│ [Shell: Console · Home · Subjects · Studio · …]             │
├─────────────────────────────────────────────────────────────┤
│ PERSISTENT CONTEXT                                          │
│   CS1 · Probability · Version 2026.1 · Stage: Validate      │
├─────────────────────────────────────────────────────────────┤
│ L0  Stage: Validate                                         │
│     [ Resolve findings ]  ← exactly one Primary             │
│     Blocking: 2 findings                                    │
├─────────────────────────────────────────────────────────────┤
│ L1  Stage content (documents / findings / preview / …)      │
├─────────────────────────────────────────────────────────────┤
│ L2  History / prior results (omit if empty / not useful)    │
├─────────────────────────────────────────────────────────────┤
│ L3  ▶ Technical details (collapsed)                         │
└─────────────────────────────────────────────────────────────┘
```

Shell navigation is escape, not page content. Do not duplicate Home / Subjects / Studio as in-page destination cards.

---

## 5. Stage-based architecture (not page-based)

Replace competing destinations with **modes of one workspace**.

```
Upload → Validate → Review → Approve → Publish
```

| Rule | Detail |
|---|---|
| One URL family | Prefer `/studio/workspaces/<id>` (or equivalent) with stage as state, not five peer routes as peer nav |
| Review | Stage — not a Review Queue page |
| Publish | Final stage — not a Publishing hub |
| Stage strip | Orientation only (where / done / next) — not five Primaries |

Never present Upload, Validate, Review, Approve, Publish as competing top-level destinations that feel like separate products.

---

## 6. Persistent context

Documented in `PERSISTENT_CONTEXT_SPEC.md`.

Minimum always-visible fields:

- Subject code (e.g. CS1)  
- Subject name (e.g. Probability)  
- Version label (e.g. 2026.1)  
- Current stage name  

This header **never changes role**. Content updates when stage/version changes; the slot remains.

Object permanence (DX-004B): name, code, and status vocabulary must match Subjects and Home.

---

## 7. Stage header

Answers only:

1. Where am I?  
2. What has been completed?  
3. What is next?  

Nothing more — no essays, no KPI tiles, no “tips for Founders.”

---

## 8. Findings at L0

Only **blocking** findings appear in L0.

Warnings and informational notes remain in L1/L2. Severity drives prominence — see `FINDINGS_PRESENTATION.md`.

When blocking findings exist, the Primary typically becomes **Resolve findings** (or the recovery action that unblocks the stage), not a premature Advance/Approve/Publish.

---

## 9. Workspace continuity

| Event | Behaviour |
|---|---|
| Leave workspace | Persist current stage on the workspace object |
| Return (Home Resume / Subjects Open / deep link) | Restore exact stage; Primary ready without manual stage pick |
| Browser refresh | Same stage; no wizard reset |
| Publish success | Exit to Home; item appears in Recent Publications |

No manual “return to step 3” navigation required.

---

## 10. Navigation boundaries

| From | To | Rule |
|---|---|---|
| Home Primary | Workspace at current stage | Direct |
| Subjects Open | Workspace at current stage | Direct; no interstitial |
| Workspace | Subjects / Home | Shell nav or explicit Exit — never forced mid-stage |
| Workspace | Review hub / Publish hub | **Forbidden** — those hubs do not exist |

Navigation must never interrupt execution. Exit only when the Founder chooses (or after successful Publish completion path).

---

## 11. Error recovery

Documented in `ERROR_RECOVERY_SPEC.md`.

- Errors appear **inline** in context.  
- Recovery is **immediate** (retry, re-upload, re-validate).  
- Never redirect to another page for recoverable issues.  

---

## 12. Completion path

```
Publish (Primary succeeds)
    ↓
Immediate confirmation (inline or flash)
    ↓
Return to Home
    ↓
Published item in Recent Publications (L2)
```

Home remains the continuation surface; Workspace does not keep the Founder in a “celebration dashboard.”

---

## 13. Accessibility & performance

| Requirement | Target |
|---|---|
| Keyboard | Full Primary and stage content operable; focus order Persistent → L0 Primary → L1 |
| Responsive | Single column stacks; Primary remains visible without horizontal scroll |
| Time-to-Primary | **<5 seconds** after workspace loads |
| Stage transitions | Instant where possible (same page state update) |
| Publication confirmation | Immediate |

No accessibility regressions vs current Console workspace patterns.

---

## 14. Removal register (legacy workspace chrome)

Do not include / remove on implementation:

| Remove | Why |
|---|---|
| Validation / Preview / Checklist **KPI card row** | Decorative readiness theatre; stage content owns truth |
| Platform / Studio summaries on workspace | Wrong surface |
| Welcome / tutorial essays | DX-003 density |
| Progress wheels / decorative rings | Not decision aids |
| Multi-Primary action clusters (Advance + Approve + Publish equal weight) | Violates one Primary |
| Competing panel destinations that feel like separate apps | Stage modes only |
| In-page duplicate nav to Review Queue / Publishing hubs | Hubs eliminated (DX-004B) |
| Feature promotion / “what’s new” | Not execution |

---

## 15. Relationship to domain workflow

Founder-facing stages (this programme) map to domain `WorkflowStage` — see `STAGE_MODEL.md`. Design does not rename domain enums in this documentation-only programme; UI labels and stage chrome follow the Founder-facing model.

---

## 16. Success tests

1. **3-second test:** Founder opens workspace and can name the next step and find the Primary.  
2. **One Primary test:** At any stage, only one control has Primary visual weight.  
3. **Continuity test:** Leave mid-Validate; return; still on Validate with same blocking findings.  
4. **Boundary test:** Ask “Where do I Review?” → Workspace Review stage — not a peer catalogue.  
5. **Completion test:** Publish lands on Home with the subject in Recent Publications.

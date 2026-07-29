# Card Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**DX-001 rule:** Cards are optional grouping only — not the primary information container. Prefer section, table, list, timeline, or plain content.

---

## Evaluation questions

Could this become a section / table / list / timeline / plain content? If yes → recommend removal of card chrome.

---

## Console

| Card / pattern | Location | Better as | Verdict |
|---|---|---|---|
| Attention metric cards (×4) | Overview | Ranked list with counts | **Remove cards** |
| Platform Summary cards (×4) | Overview | Remove or report table | **Remove** |
| Recent support / activity cards | Overview | Compact list | **Demote** |
| Curriculum Authority shortcut cards | Overview | Quiet links | **Demote** |
| command-card wrappers | Studio hubs | Section + table | **Remove chrome** |
| Create Subject / Open Workspace cards | Subjects | Single form section | **Merge; less card** |
| Workspaces list in command-card | Hubs | Table | **Table** |
| Workflow essay card | Hubs | Delete | **Remove** |

---

## Curriculum Workspace

| Card / pattern | Location | Better as | Verdict |
|---|---|---|---|
| Workflow stepper card | Workspace | Compact stage strip | **Demote** |
| Validation / Preview / Checklist cards | Workspace | Status line | **Remove cards** |
| Validation findings card | Workspace | Plain list (keep structure) | Grouping OK if borderless |
| Content Sources card | Workspace | Section with upload slots | Section |
| Document upload cards | Slots | File rows / dropzones | Prefer list rows |
| Pipeline job articles | Processing | Compact list | Demote |
| Curriculum review card + tabs | Workspace | Stage panels | Keep container minimal |
| Actions card with button grid | Workspace | One Primary + menu | **Remove grid card** |
| CIP metric mini-cards | Overview/Quality/Evidence | Remove / Advanced table | **Remove** |

---

## Student

| Card / pattern | Location | Better as | Verdict |
|---|---|---|---|
| explanation_card | Home, Revision, etc. | Inline L1 text + disclosure | Reduce usage |
| readiness_card / countdown_card | Home | Journey section | **Relocate / remove from Home** |
| progress_card | Journey | Plain progress + list | Demote |
| history_card | History | List row | Prefer list |
| History stats cards | History | Captions | **Remove** |
| Profile multi-cards | Profile | Grouped sections | Demote |
| recommendation_card | Home | Hero is enough | Avoid second card hero |
| Session question_card / timer_card | Session | Practice layout | Acceptable grouping if quiet |
| Subject catalogue radio cards | Wizard step 1 | List with radio | Consider list |
| Landing sign-in card | Login | Form section | OK for interaction container |
| Welcome modal | Modal | Delete | **Remove** |

---

## When cards are justified

DX-001 allows cards when they are the **container for a user interaction** and removing chrome would hurt understanding.

| Justified | Reason |
|---|---|
| Login form panel | Interaction container |
| Confirm modal | Interaction container |
| Upload dropzone | Interaction affordance |
| Feedback form panels | Interaction |

| Not justified | Reason |
|---|---|
| KPI metric tiles | Decoration |
| Workflow tutorial boxes | Content not interaction |
| Stats grids | Analytics theatre |
| Duplicate explanation cards | Density |

---

## Estimated card reduction

| Area | Cards/chrome blocks (est.) | Target |
|---|---|---|
| Console Overview | ~12 | ≤2 list sections |
| Workspace | ~10+ | ≤3 sections |
| History | ~4+ | 1 list |
| Home | Multiple explanation/context cards | 0–1 disclosure |

**Overall:** Prefer **~60% fewer card containers** on P0 surfaces.

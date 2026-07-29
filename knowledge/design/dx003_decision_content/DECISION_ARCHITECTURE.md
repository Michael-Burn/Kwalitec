# Decision Architecture

**Programme:** DX-003  
**Status:** Binding  
**Release Candidate:** `RC-2026.07.29-01`  
**Depends on:** DX-002 `PRODUCT_ARCHITECTURE.md` one-question map  

---

## Model

Every screen follows exactly:

```
Decision
    ↓
Action
    ↓
Feedback
```

| Beat | Definition | UI manifestation |
|---|---|---|
| **Decision** | The one question the user must resolve now | Page sentence + primary options |
| **Action** | The single Primary control that resolves it | Exactly one Primary button / select |
| **Feedback** | Confirmation of outcome, or next Decision | Flash, inline status change, or next screen |

If a screen asks a second independent decision before the first Feedback, it fails — split or sequence it.

---

## One-sentence rule

Every page is summarised by a single sentence (≤ one line).

| Surface | One sentence |
|---|---|
| Login | Sign in. |
| Alpha onboarding | Confirm you understand Alpha scope. |
| Choose Exam | Select a published curriculum. |
| Exam date | Set your exam date. |
| Availability | Set weekly study time. |
| Begin Learning | Confirm and start. |
| Calibration | Set prior coverage. |
| Student Home | Continue today’s study. |
| Session overview | Begin this session. |
| Session activity | Answer the next item. |
| Session reflection | Record what you noticed. |
| Session summary / complete | Review outcome, then return. |
| Journey | See syllabus position. |
| Revision | Revise to support today’s Mission. |
| History | Browse practice archive. |
| Decision Journal | Review guidance memory. |
| Educational Timeline | Read the learning story. |
| Profile / Settings | Configure account. |
| Help | Get unblocked. |
| Console Overview | Continue curriculum publication. |
| Subjects | Open or create a subject. |
| Curriculum Studio | Open the workspace that needs work. |
| Curriculum Workspace | Complete the next publication stage. |
| Attention | Intervene on the top item. |
| Support | Review the next submission. |
| Findings | Open an open finding. |
| Students | View a participant. |
| Console Search | Open the matched object. |
| Console Settings | Configure Console. |
| Secondary reports | Inspect the selected metric set. |
| Confirm modal | Confirm or cancel. |
| Subject support gate | Resolve the blocking condition. |
| Errors 403/404/500 | Understand the block, then act. |

If the sentence exceeds one line, the screen contains too much.

---

## Decision → Action → Feedback (primary screens)

### Auth

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Login | Enter credentials? | Sign in | Home or Console loads; or field error |

### Student — planning

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Choose Exam | Which Ready subject? | Select → Next | Step 2 |
| Exam date | Which date? | Next | Step 3 |
| Availability | How much time? | Next | Review |
| Begin Learning | Accept plan? | Begin Learning | Home with Mission |
| Calibration | Prior coverage level? | Continue | Home / plan ready |

### Student — daily

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Home | Start today’s Mission? | Start / Continue | Session overview |
| Journey | (Scan only) Need Home? | Return Home / Continue | Home |
| Revision | Revise this topic? | Begin revision | Session / practice |
| History | Open which session? | Open detail | Detail / Journal link |
| Journal | Reflect / continue? | Reflect (optional) | Entry saved |
| Timeline | Done scanning? | Return | Prior screen |
| Profile | Change which setting? | Save / open section | Saved |

### Student — session

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Overview | Ready to begin? | Begin Session | Activity |
| Activity | What is the answer? | Submit / Advance | Next item or reflection |
| Reflection | What do I notice? | Continue | Summary |
| Summary / Complete | Where next? | Return Home | Home |

### Console — authority path

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Overview | Which item needs attention? | Open / Resume | Workspace or queue |
| Subjects | Open or create? | Create / Open | Workspace |
| Studio list | Which workspace? | Open Workspace | Workspace |
| Workspace | What is the next stage task? | Stage Primary | Stage advances; status updates |
| Attention | Which intervention? | Open item | Item workspace |
| Support | Which submission? | Review | Disposition saved |
| Findings | Which finding? | Open | Detail updated |
| Students | Which participant? | View | Detail |
| Search | Which result? | Open | Destination |

### Shared

| Screen | Decision | Action | Feedback |
|---|---|---|---|
| Confirm | Proceed with destructive action? | Confirm / Cancel | Action completes or cancelled |
| Support gate | Can I continue with this subject? | Choose another / wait | Catalogue resumes |
| Welcome modal | *(forbidden)* | — | **Delete** |

---

## Multi-decision screens (fail today)

| Screen | Independent decisions today | Target | Fix |
|---|---|---|---|
| Curriculum Workspace | Stage task + upload + validate + preview + approve + publish + tab browse + diagnostics | 1 | Stage-gated Primary only |
| Console Overview | Which KPI? + Quick Action? + Attention item? + Curriculum shortcut? | 1 | One attention Primary |
| Student Home | Start Mission? + Why? + Defer? + Tutor? + Mark complete? + Readiness? | 1 | One Primary; rest disclose |
| Studio hubs | Create? + Open? + Jump Studio? + Read workflow? | 1 | Catalogue only |
| History | Browse? + Learn epistemology? + Open Journal? + Open Timeline? | 1 | Archive list only |
| Help | Orient ontology? + Search? + Contact? | 1–2 | Search/contact; cut ontology |

See `DECISION_DENSITY_AUDIT.md` for counts.

---

## Feedback rules

| Outcome | Feedback form | Length |
|---|---|---|
| Success | Short flash or inline label | 1–4 words preferred; max one short sentence |
| Progress | Stage / status change only | No essay |
| Error | Problem → Reason → Action | Three beats; see `SUCCESS_ERROR_COPY_GUIDE.md` |
| Empty | Reason → Next Action | See `EMPTY_STATE_STANDARDS.md` |

Permanent decorative “status essays” on idle screens are not Feedback — they are noise. Remove them (`STATUS_SYSTEM.md`).

---

## Relationship to DX-002

| DX-002 | DX-003 |
|---|---|
| One question | Decision |
| Primary action | Action |
| (implicit outcome) | Feedback |

DX-003 does not change IA trees. It specifies the **verbal contract** of each screen under that IA.

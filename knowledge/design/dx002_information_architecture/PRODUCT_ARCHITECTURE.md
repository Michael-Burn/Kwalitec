# Product Architecture

**Programme:** DX-002  
**Status:** Binding Information Architecture  
**Release Candidate:** `RC-2026.07.29-01`  
**Authority:** Supplements DX-001; constrains future redesign programmes. No UI implementation in this programme.

---

## 1. Product mission

Kwalitec helps highly educated professionals **know what to study next** for a real exam — with curriculum authority owned by the Founder, not by opaque ranking.

Two user roles, two product jobs:

| Role | Job |
|---|---|
| **Student** | Choose exam → receive today’s focus → complete a session → trust progress |
| **Founder / operator** | Author subjects → verify curriculum → publish Ready subjects → monitor Alpha health |

---

## 2. Shell model

```
┌─────────────────────────────────────────────────────────────┐
│ Public entry                                                │
│   Login (auth shell)                                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
          ┌─────────────────┴─────────────────┐
          ▼                                   ▼
┌─────────────────────┐             ┌─────────────────────┐
│ STUDENT SHELL       │             │ CONSOLE SHELL       │
│ Education OS        │             │ Curriculum Authority│
│ eos_student layout  │             │ console_base layout │
└─────────────────────┘             └─────────────────────┘
```

**Rules**

- One primary navigation per shell.  
- No competing “homes.” Student Home ≠ Console Overview ≠ legacy Dashboard.  
- Cross-shell links are rare and quiet (Console Account → student settings; never equal-weight peer nav).  
- Legacy Learning Workspace (`legacy_workspace.html`) is dual-run rollback only — not a third product.

---

## 3. Surface taxonomy

Every screen must declare exactly one type. Rename “dashboard” when the type is wrong.

| Type | Definition | Examples (target) |
|---|---|---|
| **Home** | Daily decision surface; one next action | Student Home; Console Overview |
| **Workspace** | Stage-driven work on one object | Curriculum Workspace; Session flow |
| **Wizard** | Linear capture of decisions | Choose Exam (4 steps) |
| **Catalogue** | Browse / select / open items | Subject Catalogue (student); Subjects list (Console) |
| **Queue** | Work items awaiting human action | Attention; Support inbox; Review queue (in-workspace) |
| **Report** | Analytical monitoring | Research / Analytics; Runtime Health |
| **Archive** | Historical record | History (practice archive); Findings list |
| **Settings** | Account / preference configuration | Student Profile; Settings sections; Console Settings |
| **Help** | Orientation + support actions | Help & Support |
| **Auth** | Identity gate | Login |

### Current mislabels (must rename in redesign)

| Current label | Actual type | Target name |
|---|---|---|
| Console “dashboard” / Console Home as KPI wall | Report + Queue mashup | **Console Overview** (decision surface) |
| Curriculum Studio “dashboard” | Catalogue | **Curriculum Studio** (workspace list) |
| Student “Dashboard” (legacy) | Home | **Home** (already redirected) |
| “Participants” page | Catalogue | **Students** (match nav) |
| History (with KPI cards) | Report + Archive | **Practice Archive** or keep History as archive only |
| Platform Summary cards | Decorative report | Remove from Overview |

---

## 4. Canonical one-question map

| Surface | Type | One question | Primary action |
|---|---|---|---|
| Login | Auth | How do I enter? | Sign in |
| Alpha onboarding | Help (orientation) | What must I know before I start? | Continue |
| Choose Exam (step 1) | Catalogue / Wizard | What can I begin studying? | Select subject → Next |
| Exam date (step 2) | Wizard | When is my exam? | Next |
| Availability (step 3) | Wizard | How much time can I study? | Next |
| Begin Learning (review) | Wizard | Confirm and start? | Begin Learning |
| Calibration | Wizard | What prior coverage should guide me? | Continue |
| Student Home | Home | What should I study next? | Start / Continue session |
| Session overview | Workspace | Am I ready to begin this session? | Begin Session |
| Session activity | Workspace | What is the next practice step? | Submit / Advance |
| Session reflection | Workspace | What do I notice about this practice? | Continue |
| Session summary / complete | Workspace | What happened — and where next? | Return Home |
| Journey | Report (progress map) | Where am I in the syllabus? | Return to Home / continue |
| Revision | Workspace | What should I revise to support today’s focus? | Begin revision |
| History | Archive | What have I practiced? | Open session detail / Journal |
| Decision Journal | Archive | What guidance and choices shaped my path? | Reflect / open Timeline |
| Educational Timeline | Archive | How does my learning story read over time? | Return |
| Profile / Settings | Settings | How do I configure my account? | Save / open section |
| Help | Help | How do I get unblocked? | Search topic / contact |
| Console Overview | Home | What should I publish or fix next? | Open top attention item |
| Subjects | Catalogue | Which subject do I open or create? | Create / Open workspace |
| Curriculum Studio list | Catalogue | Which workspace needs work? | Open workspace |
| Curriculum Workspace | Workspace | What is the next publication task? | Stage Primary (upload / advance / validate / approve / publish) |
| Review / Publishing hubs | Queue / Catalogue | *(target: fold into Studio filters)* | Open workspace |
| Attention | Queue | What needs intervention? | Open item |
| Support | Queue | Which feedback needs review? | Review submission |
| Findings | Archive / Queue | Which product findings are open? | Open finding |
| Students | Catalogue | Who is participating? | View / award |
| Console Search | Catalogue | Where is this operational object? | Open result |
| Console Settings | Settings | How is Console configured? | Open product settings |

If a screen cannot state one question in one sentence, it fails IA and must be split or cut.

---

## 5. Target information architecture (trees)

### 5.1 Student

```
Home                    ← daily decision
├── Session/*           ← guided practice loop (not in primary nav)
Journey                 ← syllabus position
Revision                ← supporting practice (not a second Home)
History                 ← practice archive
│   └── Decision Journal / Timeline   ← progressive disclosure (not peer heroes)
Study Plan              ← exam + availability configuration
Settings                ← account
Help                    ← orientation + support
```

**Nav rule:** ≤6 primary destinations in feature mode. Unified-journey mode must not introduce a second Home personality — stage labels map to the same destinations.

### 5.2 Console

```
Overview                ← what to publish/fix next
Subjects                ← catalogue (create + open)
Curriculum Studio       ← workspaces + open Workspace
Students                ← participants
Support                 ← feedback queue
Settings                ← includes Search, ops reports as nested destinations
```

**Demote from primary chrome (into Settings → Operations / Intelligence):**

Operations, Learning (Founder Intelligence), Assessments (Evidence Gates), Analytics/Research, Platform Intelligence, Attention (or merge into Overview), Runtime Health, Findings (link from Support), Internal Alpha, System Operations, Releases, Vision Journal, Search.

**Remove as peer hubs:** Review Queue, Publishing, Versions, Quality — become **filters or stages inside Curriculum Studio / Workspace**, not separate primary nav items.

---

## 6. Publication object model (operator)

```
Subject
  └── Workspace (draft → … → published)
        ├── Content Sources (CMP + Syllabus)
        ├── Extraction / Structure
        ├── Validation & Review
        ├── Preview
        ├── Approve
        └── Publish → Subject Ready for students
```

Student Subject Catalogue shows only **Ready** subjects. Coming Soon is catalogue metadata, not a workspace.

---

## 7. Learning loop object model (student)

```
Study Plan (exam + date + availability)
  └── Daily Focus (Home recommendation / mission)
        └── Guided Session
              ├── Overview
              ├── Activity
              ├── Reflection
              └── Summary → Complete → Home
        └── Optional Revision (supports focus; never a second Mission)
```

Educational memory:

| Store | Job |
|---|---|
| Practice History | What was practiced (archive) |
| Decision Journal | Why guidance changed / choices made |
| Educational Timeline | Chronological narrative view of Journal |

**IA target:** One “Progress” or “Memory” entry point with internal views — not three peer nav items requiring Help to disambiguate.

---

## 8. Global capabilities

| Capability | Status | IA rule |
|---|---|---|
| Console Search | Present | Operator-only; keep in topbar; not a student feature |
| Student Help search | Present (topic filter) | Keep local to Help |
| Notifications centre | Absent | Do not invent for Alpha; flash messages suffice |
| Confirm modal | Present | Destructive actions only |
| Welcome modal | Present | **Remove or one-shot** — violates DX-001 welcome-message policy |

---

## 9. Relationship to DX-001

| DX-001 rule | DX-002 application |
|---|---|
| One screen, one purpose | Canonical question table (§4) |
| L0–L3 hierarchy | Per-screen layers in `INFORMATION_HIERARCHY_AUDIT.md` |
| Default no KPI cards | KPI audit + Console/Workspace removals |
| Cards only for grouping | Card audit |
| Dashboards are decision surfaces | Taxonomy rename + Overview redesign |
| Navigation calm | Nav audit + target trees |

---

## 10. Non-goals

- Visual redesign, CSS tokens, new components  
- Engineering deletion of dual-run routes in this programme  
- Changing educational recommendation algorithms  

Architecture first; DX-003 owns content density; later DX programmes own visual execution.

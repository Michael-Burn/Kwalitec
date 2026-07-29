# Information Hierarchy Audit

**Programme:** DX-002  
**Release Candidate:** `RC-2026.07.29-01`  
**Layers:** L0 Mission Critical · L1 Primary Context · L2 Supporting · L3 Metadata  

For each screen: Purpose, Primary Question, Primary Action, Layers, Problems, Removals, Consolidations, Relocations, Cognitive Load, Premium Score.

---

## Scoring

Premium Score estimates readiness against DX-001 (≥9 required to ship a redesign). Cognitive Load: Low / Moderate / High / Very High.

---

## Student surfaces

### D1 — Student Home

| Field | Assessment |
|---|---|
| **Purpose** | Present today’s single study decision and start it |
| **Primary Question** | What should I study next? |
| **Primary Action** | Start / Continue session (exactly one) |
| **L0** | Mission title; Primary CTA |
| **L1** | Duration; one-line why; blocking status (resume / reflection / day complete) |
| **L2** | Expected benefit; alternatives (collapsed); Study Sensei attribution |
| **L3** | Trust-state attributes; journey-stage data attrs; coherence badges |
| **Current Problems** | Greeting + narrator + eyebrow + title + status + duration + purpose + educational panel + alternatives + readiness/countdown cards compete; multiple secondary CTAs (tutor explain, defer, mark complete) visually near Primary |
| **Removals** | Duplicate duration; redundant “Today's Focus” when title already states focus; decorative trust chrome in L0 |
| **Consolidations** | One explanation block (why); move benefit/alts behind “Why this?” disclosure |
| **Relocations** | Readiness/countdown → Journey; defer reasons → compact menu |
| **Cognitive Load** | High |
| **Premium Score** | **5/10** |

### D2 — Journey

| Field | Assessment |
|---|---|
| **Purpose** | Show syllabus position |
| **Primary Question** | Where am I in the syllabus? |
| **Primary Action** | Quiet link back to Home / continue |
| **L0** | Current topic + progress |
| **L1** | Completed / upcoming lists |
| **L2** | Progress % |
| **L3** | — |
| **Problems** | Card framing; CTA may compete with Home’s job |
| **Removals** | Card chrome if list/timeline suffices |
| **Load** | Moderate · **Premium** 6/10 |

### D3 — Revision

| Field | Assessment |
|---|---|
| **Purpose** | Offer revision that supports today’s Mission |
| **Primary Question** | What should I revise to support today? |
| **Primary Action** | Begin revision |
| **L0** | Topic + Begin |
| **L1** | Priority + time estimate; one-line “supports Mission” |
| **L2** | Alternative options |
| **L3** | — |
| **Problems** | Explanation cards stack; must never read as second Home |
| **Load** | Moderate · **Premium** 6/10 |

### D4 — History

| Field | Assessment |
|---|---|
| **Purpose** | Practice archive |
| **Primary Question** | What have I practiced? *(fails today — also explains epistemology)* |
| **Primary Action** | Browse sessions *(today: Open Journal / Timeline)* |
| **L0** | Recent sessions list |
| **L1** | Study time total (if decision-relevant — usually L2) |
| **L2** | Recommendation narrative |
| **L3** | Timestamps |
| **Problems** | Opens with tutorial “What History shows”; KPI cards; repeatedly pushes Journal/Timeline — screen answers three questions |
| **Removals** | Epistemology essay; readiness-trend KPI card; duplicate Journal CTAs |
| **Consolidations** | Merge Journal + Timeline under one Progress/Memory surface |
| **Load** | High · **Premium** 3/10 |

### D5 / D6 — Decision Journal & Educational Timeline

| Field | Assessment |
|---|---|
| **Purpose** | Educational memory / narrative |
| **Primary Question** | Journal: What guidance shaped my path? Timeline: How does the story read? |
| **Primary Action** | Reflect / scan |
| **Problems** | Peer nav + Help essays prove IA overlap; students must learn product ontology |
| **Consolidations** | Single **Progress** or **Memory** entry with Journal / Timeline tabs |
| **Load** | Moderate–High · **Premium** 5/10 |

### D7 — Profile

| Field | Assessment |
|---|---|
| **Purpose** | Account configuration summary |
| **Primary Question** | How do I configure my account? |
| **Primary Action** | Open account settings / edit prefs |
| **Problems** | Multiple cards (exam, prefs, goals, stats, account); learning statistics are KPIs without decisions |
| **Removals** | Decorative stats; goal progress bars unless editable here |
| **Load** | Moderate · **Premium** 5/10 |

### C1 — Choose Exam

| Field | Assessment |
|---|---|
| **Purpose** | Select Ready subject |
| **Primary Question** | What can I begin studying? |
| **Primary Action** | Select → Next |
| **L0** | Subject list / radios |
| **L1** | Ready vs Coming Soon |
| **L2** | Support gate message when blocked |
| **L3** | Subject codes (quiet) |
| **Problems** | Card radio pattern OK if list alternative considered; Coming Soon must not dominate |
| **Load** | Low–Moderate · **Premium** 7/10 |

### C4 — Begin Learning (Review)

| Field | Assessment |
|---|---|
| **Purpose** | Confirm plan and start |
| **Primary Question** | Confirm and start? |
| **Primary Action** | Begin Learning |
| **Problems** | Shows defaults for position/style/target the user never chose — surprise density; multi-section review |
| **Removals** | Sections user did not set (or mark “defaulted” quietly) |
| **Load** | Moderate · **Premium** 5/10 |

### E2 — Session activity

| Field | Assessment |
|---|---|
| **Purpose** | Execute practice step |
| **Primary Question** | What is the next practice step? |
| **Primary Action** | Submit / Advance |
| **L0** | Question + answer controls + Primary |
| **L1** | Progress; timer if needed |
| **L2** | Explanation after answer |
| **L3** | Session ids |
| **Problems** | Relatively focused; card wrappers still present |
| **Load** | Low–Moderate · **Premium** 8/10 |

### B1 — Onboarding

| Field | Assessment |
|---|---|
| **Purpose** | Orientation before first use |
| **Primary Question** | What must I know before I start? |
| **Primary Action** | Continue |
| **Problems** | Welcome heading; three CTAs (Continue / Skip / Help) |
| **Removals** | Extra secondary when Skip exists |
| **Load** | Moderate · **Premium** 6/10 |

### B2 — Help

| Field | Assessment |
|---|---|
| **Purpose** | Unblock + contact support |
| **Primary Question** | How do I get unblocked? |
| **Primary Action** | Find topic / report problem |
| **Problems** | Long orientation essays compensating for IA failures elsewhere; implementation of memory model as student content |
| **Removals** | Journey ontology tutorials once Progress is unified |
| **Load** | High · **Premium** 4/10 |

### A1 — Login

| Field | Assessment |
|---|---|
| **Purpose** | Authenticate |
| **Primary Question** | How do I enter? |
| **Primary Action** | Sign in |
| **Problems** | Six feature bullets + decorative illustration shapes + alpha badge — landing mashup; two H1-weight zones |
| **Removals** | Feature list → 1 sentence; decorative shapes |
| **Load** | Moderate · **Premium** 5/10 |

---

## Console surfaces

### G1 — Console Home

| Field | Assessment |
|---|---|
| **Purpose** | Direct founder to highest-leverage next work |
| **Primary Question** | What should I publish or fix next? |
| **Primary Action** | Open top attention / publication blocker |
| **L0** | Single next work item + Primary CTA |
| **L1** | Short attention list (3–5) |
| **L2** | Curriculum shortcuts (quiet) |
| **L3** | Version, timezone, refreshed_at, build number |
| **Current Problems** | Eyebrow with version; executive summary with timestamp/timezone; 4 attention KPI cards; 4 platform summary KPI cards; Quick Actions with **multiple primary-weight buttons**; operational detail cards |
| **Removals** | Platform Summary grid; build number in L0; vanity participant/check-in KPIs |
| **Consolidations** | Attention queue as list not metric cards; one Primary only |
| **Relocations** | Analytics → Research report; Platform health → Operations |
| **Load** | Very High · **Premium** 3/10 |

### H2 — Subjects hub (representative of H3–H6)

| Field | Assessment |
|---|---|
| **Purpose** | Create/open subjects |
| **Primary Question** | Which subject do I open or create? |
| **Primary Action** | Create Subject or Open Workspace |
| **Problems** | Same workflow essay on every hub; two Primary forms side-by-side; “Open Curriculum Studio” CTA unrelated to Subjects job; hubs H3–H6 are filtered duplicates |
| **Removals** | Workflow tutorial list; non-Subjects hubs as pages |
| **Consolidations** | One Subjects catalogue + Studio list with filters |
| **Load** | High · **Premium** 4/10 |

### H7 — Curriculum Workspace

| Field | Assessment |
|---|---|
| **Purpose** | Complete next publication stage for one subject |
| **Primary Question** | What is the next publication task? |
| **Primary Action** | Stage Primary only (upload / advance / validate / preview / approve / publish) |
| **L0** | Subject title; Next step; stage Primary button |
| **L1** | Blocking validation findings; content sources for current stage |
| **L2** | Workflow stage list (compact); structure/review panels behind disclosure |
| **L3** | Workspace id, entity ids, embedding model, ms timings, retrieval profiles |
| **Current Problems** | Next step + full workflow card + 3 readiness KPI cards + findings + upload + 7 processing stages + pipeline jobs with ms + **9 CIP tabs** including Entity id + Actions grid with many buttons |
| **Removals** | Always-visible readiness KPI triad; Documents tab that only points upward; Entity id entry in L0 path; embedding KPI row; Mission Engine / Tutor retrieval profiles in Founder default path |
| **Consolidations** | Tabs → stage-appropriate panels (≤3 visible); Actions → one Primary + overflow |
| **Relocations** | Diagnostics → Advanced / Quality drawer; pipeline ms → L3 |
| **Load** | Very High · **Premium** 2/10 |

### G3 / G4 — Attention / Support

| Field | Assessment |
|---|---|
| **Purpose** | Work a queue |
| **Primary Question** | What needs intervention? / Which feedback needs review? |
| **Primary Action** | Open next item |
| **Problems** | Overlap with Console Home attention cards; Support filters dense |
| **Consolidations** | Overview leads into these queues; avoid duplicating metrics |
| **Load** | Moderate · **Premium** 6/10 |

### I* — Secondary reports

| Field | Assessment |
|---|---|
| **Purpose** | Analytical monitoring |
| **Primary Question** | Varies (health / research / gates) |
| **Primary Action** | Inspect (rarely act) |
| **Problems** | Peers in secondary nav inflate product surface; engineering terminology |
| **Relocations** | Nest under Settings → Operations / Intelligence |
| **Load** | Moderate–High · **Premium** 4–5/10 |

---

## Shared chrome

### J2 — Welcome modal

| Field | Assessment |
|---|---|
| **Purpose** | Post-calibration celebration |
| **Primary Question** | *(none valid — Home already answers)* |
| **Primary Action** | Start Today's Session *(duplicates Home)* |
| **Verdict** | Remove; forbidden welcome pattern |
| **Premium** | 2/10 |

### Navigation shells

Documented in `NAVIGATION_AUDIT.md`. Hierarchy failure: duplicate destinations across sidebar, Quick Actions, and hub CTAs.

---

## Cross-cutting hierarchy failures

| Failure | Where | Fix direction |
|---|---|---|
| L3 in L0 | Console eyebrow version; Workspace entity ids; pipeline ms | Demote / hide |
| Multiple Primaries | Console Quick Actions; Workspace Actions; Onboarding | One Primary |
| Tutorial as L0 | History, Help, Studio hubs | Delete after IA fix |
| Analytics above action | Console Platform Summary | Remove |
| Equal-weight peer archives | History / Journal / Timeline | Consolidate |

---

## Summary table (priority screens)

| ID | Screen | Load | Premium | One-purpose? |
|---|---|---|---|---|
| H7 | Curriculum Workspace | Very High | 2 | No |
| G1 | Console Home | Very High | 3 | No |
| H3–H6 | Studio hubs | High | 3 | No |
| D4 | History | High | 3 | No |
| B2 | Help | High | 4 | Weak |
| H1–H2 | Studio / Subjects | High | 4 | Weak |
| D1 | Student Home | High | 5 | Yes (question) / No (execution) |
| A1 | Login | Moderate | 5 | Weak |
| C4 | Review | Moderate | 5 | Yes |
| E2 | Session activity | Low–Mod | 8 | Yes |

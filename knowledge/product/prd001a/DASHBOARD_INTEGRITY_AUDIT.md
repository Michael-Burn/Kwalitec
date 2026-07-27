# PRD-001A — Dashboard Integrity Audit

**Surface:** EOS Home (`/student/`) under sole runtime — the student’s primary dashboard.  
**Rule:** Flag components that exist only because data is available; elevate components that improve study decisions.

---

## Component inventory

| Component | Purpose | Input data | Educational value | Decision value | Student value | Prominence | Integrity call |
|---|---|---|---|---|---|---|---|
| Greeting | Orientation | Time/name | Low | None | Low-medium | High (hero) | Keep — cheap |
| Today’s Mission title | Name the action | Mission / recommendation title | High | **Critical** | High | Highest | **Elevate** — ensure always curriculum-bound |
| Duration label | Timebox | Plan minutes / unified journey estimate | Medium | Medium | High | High | Keep — explain source |
| Why / Why now / Next / Benefit | Explain recommendation | MES explanation | High | High | High | High | **Elevate honesty** of selection rule |
| Commitment / defer | Capture intent | Commitment service | Medium | High (behaviour) | High | Medium | Keep |
| L2 explanation_card | Deep why + alts | Explanation DTO | High | Medium | Medium | Medium (disclosure) | Keep |
| Today’s journey timeline | Day phases | Unified journey flag | Low-medium | Low | Medium | Medium | Keep only if flag ON and accurate; else noise |
| Experience feedback facts | Period stats | Feedback facts | Low-medium | Low | Medium | Medium | **Demote** if not decision-linked |
| Readiness panel | Exam posture | Readiness surface | High | Medium (not mission picker) | High | Secondary | Keep; link to what it does **not** change |
| Journey story panel | Narrative progress | Journey story string | Medium | Low | Medium | Secondary | **Elevate → link/embed syllabus position** or demote vs Journey page |
| Coach panel | Guidance | Coach trust / placeholder | Medium | Low when duplicate | Medium-low | Secondary | **Demote or differentiate** — avoid paraphrase |
| Primary Start CTA | Begin session | Mission/session ids | High | **Critical** | High | Highest | Keep |
| Reflection preview (presentation-only) | Tease reflection | Reflection prompts | Low if unsaved | Misleading if thought saved | Low | Conditional | **Fix contract** — placeholder honesty already noted; still integrity risk |
| Empty states | Cold start | Missing ports/plan | Medium | Direct to wizard/session | High | Full page | Keep |

---

## Components that risk “data because we have it”

1. **Coach panel when it restates Mission MES** — PX-002A already tries to dedupe; residual paraphrase still costs trust.  
2. **Experience feedback / journey stats on Home** — informative, rarely changes today’s action.  
3. **Readiness “Next” alongside Mission “Next”** — two next-actions dilute the Blueprint’s single daily expression.  
4. **Presentation-only reflection controls** — look interactive; copy admits nothing saved.

---

## Elevate (decision-critical)

1. **Curriculum position** — current topic code + section name + “X of Y topics complete” on Home first viewport.  
2. **Explicit selection contract** — one line: “Today follows your syllabus order” (Learning Mode) or “Today interrupts for review/weak topic” (when true).  
3. **Estimated Knowledge when evidence exists** — beside topic, with “does not change today’s syllabus slot until …” honesty.  
4. **Mission title always topic-bound** — eliminate generic `Daily Study — Day` when curriculum exists.

---

## Demote / relocate

| Item | Recommendation |
|---|---|
| Duplicate Coach MES | Show only unique coach content or collapse into Mission disclosure |
| Dual “Next” lines | One primary next; readiness next as subordinate |
| Experience feedback strip | Move to History |
| Alpha Settings twin status | Keep out of student decision chrome (PX-003) |

---

## Dashboard integrity verdict

Home correctly prioritises **Today’s Mission** as the north-star expression. Secondary panels partially recreate Blueprint nouns (Readiness, Journey, Coach) but **under-deliver syllabus mapping and understanding gauges**, which is why the dashboard can feel “disconnected from syllabus progression” despite Journey existing one click away.

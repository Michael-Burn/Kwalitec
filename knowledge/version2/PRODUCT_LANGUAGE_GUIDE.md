# Product Language Guide

**Authority:** Normative for learner-facing and Founder-facing product copy  
**Milestone:** ARP-004 — Copy, Language & Product Communication Audit  
**Scope:** Presentation templates, flash messages, navigation labels, empty states, and CTAs.  
Does **not** govern internal package names, domain type names, or architecture docs.

Kwalitec speaks in one voice: clear, professional, encouraging, and concise.

---

## 1. Approved terminology

Use **one** product term everywhere in the UI. Prefer consistency over variety.

| Approved term | Use for | Do not use |
|---------------|---------|------------|
| **Session** | The focused study workflow | Study Session, Learning Session, Mission (as UI label) |
| **Today's Session** | The session recommended for today | Today's Mission (learner UI), Daily Mission |
| **Publish** | Making curriculum available to learners | Release, Go Live, Ship, Deploy (as curriculum CTA) |
| **Journey** | Progress through topics toward exam readiness | Roadmap, Progress Path, Learning Path, Curriculum Graph |
| **Learning Insights** | Explainable readiness / progress summaries | Twin Insights, Student Analysis, Digital Twin, Mastery Score |
| **Revision** | Highest-value review work | Remediation, Intervention (learner UI) |
| **Exam Readiness** | Readiness toward the examination | Mastery score, Twin score |
| **Curriculum Studio** | Founder curriculum readiness workspace | Curriculum Manager, CMS, Pipeline |
| **Evidence Gates** | Cutover evidence checklist | Gates checklist, Cutover blockers (as page title) |
| **Home** | Student landing surface | Dashboard (learner UI) |

### Internal terms — never show to learners

These may appear in architecture docs and code, never in Student UI copy:

- Digital Twin / Student Twin
- Adaptive Decision
- Learning Orchestrator
- Mission Engine
- Curriculum Graph / graph node / graph edge
- Evidence Spine
- Mastery score (as a raw score label)

Founder-facing surfaces may use operational product language (Studio, Evidence Gates, Intelligence) but should still avoid engine jargon in primary CTAs and empty states.

---

## 2. Writing principles

1. **Clear** — Say what happened and what to do next.
2. **Professional** — Product-ready tone; no slang, no developer jokes.
3. **Encouraging** — Support focus and progress without empty cheerleading.
4. **Concise** — Prefer one short sentence; add a second only for recovery guidance.
5. **Human** — Prefer “we” / “your” over system or stack language.
6. **Consistent** — Reuse approved terms and CTA verbs; do not invent synonyms for variety.

### Avoid

- Developer terminology (`execute`, `payload`, `endpoint`, `null`, `stack trace`)
- Internal implementation language (`port unavailable`, `facade`, `aggregate`)
- Technical jargon in learner flashes (`runtime`, `orchestrator`, `dual-run` on Student Home)
- Inconsistent verbs for the same action (`Open` / `Launch` / `Start` / `Begin` mixed without intent)

---

## 3. Preferred button labels

Primary CTAs should be Title Case and verb-led.

### Student

| Surface | Preferred label |
|---------|-----------------|
| Home | **Start Today's Session** |
| Session Overview | **Begin Session** |
| Activity (next step) | **Continue** |
| Activity (submit) | **Submit Answer** |
| Reflection | **Continue to Summary** |
| Summary / Complete | **Return Home** |
| History / Revision empty recovery | **Return Home** |

Resume copy (flash, not button): “Welcome back — continuing where you left off.”

### Founder — Curriculum Studio

| Action | Preferred label |
|--------|-----------------|
| Create subject | **Create Subject** |
| Open workspace | **Open Workspace** |
| Advance workflow | **Advance to Next Stage** |
| Validate | **Validate Curriculum** |
| Preview | **Build Preview** |
| Approve | **Approve Curriculum** |
| Publish | **Publish Curriculum** |
| Version | **Assign Version** |

Stage rail label for publication remains **Publish** (not “Publication” or “Go Live”).

### Founder — Intelligence & Evidence

| Action | Preferred label |
|--------|-----------------|
| Evidence checklist | **Review Evidence** |
| Studio entry from advisory | **Curriculum Studio** |
| Back to intelligence | **Founder Intelligence** |

Avoid **Open**, **Launch**, **Execute**, and **Proceed** on primary CTAs unless the product intentionally needs a distinct verb (document the exception here when that happens).

---

## 4. Navigation labels

### Student primary nav

Home · Journey · Revision · History · Profile

### Founder Command Centre (primary)

Overview · Operational Health · Studio · Intelligence · Evidence Gates · Feedback · Research · Vision Journal · Releases · Settings

Do not rename Studio to “Curriculum Studio” in the compact nav; page titles and breadcrumbs may say **Curriculum Studio**.

---

## 5. Messaging patterns

### Success

Pattern: confirm the outcome in one sentence. Optional “we” voice.

Examples:

- “We've published your curriculum successfully.”
- “We've completed validation successfully.”
- “Session complete. Your home view is ready with today's updates.”
- “Welcome back — continuing where you left off.”

### Error / warning

Pattern: what failed + how to recover.

Examples:

- “We couldn't publish this curriculum. Assign a version label, complete approval, and try again.”
- “We couldn't start this session. Please try again.”
- “Learning insights are temporarily unavailable. Please try again shortly.”
- “That session could not be found. Return home and start today's session again.”

Recovery guidance should always be present where the user can act (retry, complete a prior step, or return home).

### Empty states

Pattern: name what is missing + give the next constructive step.

Examples:

- “No workspaces yet. Create a subject, then open a workspace to begin the validate → preview → approve → publish journey.”
- “No completed sessions yet.”
- “Your home view will appear when learning insights are available.”

Never leave a blank list without guidance.

---

## 6. Session chrome

| Element | Approved copy |
|---------|---------------|
| Eyebrow | `Session · Step N of M` |
| Overview title | Session Overview |
| Activity title | Learning Activity |
| Reflection title | Reflection |
| Summary title | Session Summary |
| Complete title | Complete |

Do not prefix chrome with “Learning Session” or “Study Session”.

---

## 7. Future naming conventions

When introducing a new user-visible concept:

1. Check this guide for an existing approved term.
2. Prefer a short noun learners already understand (Session, Journey, Revision).
3. Add the term to the table in §1 in the same pull request as the UI copy.
4. Add a presentation test that asserts the approved label and forbids the rejected synonyms.
5. Keep architecture / package names unchanged when they differ from product language (e.g. code may say `StudentTwinPort`; UI says **Learning Insights**).

### Naming checklist

- [ ] One term only (no synonym drift across screens)
- [ ] No engine jargon in learner copy
- [ ] Primary CTA uses an approved verb
- [ ] Success / error / empty states follow §5
- [ ] Presentation tests cover the new strings

---

## 9. Legacy V1 surfaces

Older Mission / Dashboard templates may still show **Study Session** in places
owned by pre-V2 flows. New and V2 presentation work (Student Experience,
Session Experience, Curriculum Studio, Founder Intelligence / Evidence Gates)
must use **Session** / **Today's Session** per §1. Shared chrome (sidebar,
welcome modal) uses the approved Session terminology.
---

## 10. Related documents

- [`DESIGN_SYSTEM.md`](DESIGN_SYSTEM.md) — visual and layout rules
- [`STUDENT_EXPERIENCE.md`](STUDENT_EXPERIENCE.md) — learner surfaces and vocabulary mapping
- [`LEARNING_SESSION_EXPERIENCE.md`](LEARNING_SESSION_EXPERIENCE.md) — session flow
- [`ALPHA_READINESS_FOUNDER_UX.md`](ALPHA_READINESS_FOUNDER_UX.md) — Founder UX polish (ARP-002)
- [`CURRICULUM_STUDIO.md`](CURRICULUM_STUDIO.md) — Studio workflow authority

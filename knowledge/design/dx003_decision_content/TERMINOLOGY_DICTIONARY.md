# Terminology Dictionary

**Programme:** DX-003  
**Status:** Binding canonical names for product UI  
**Release Candidate:** `RC-2026.07.29-01`  
**Extends:** `CANONICAL_EDUCATIONAL_LEXICON.md`, `product_language.py`  
**Rule:** Each concept has exactly one name. Never mix synonyms for variety.

---

## 1. Publication & curriculum authority

| Concept | Canonical term | Forbidden synonyms in UI |
|---|---|---|
| Make curriculum available to students | **Publish** | Release, Deploy, Activate, Go Live, Ship, Launch (as publish CTA) |
| Human sign-off before publish | **Approve** | Sign off, Clear, Greenlight |
| Check package against rules | **Validate** | Run checks, QA pass (as CTA) |
| Build reviewable structure view | **Build Preview** / **Preview** | Generate structure, Render |
| Move workflow forward | **Advance** | Progress stage, Next gate (as primary label when stage-specific CTA exists) |
| Official subject offering | **Subject** | Course, Module (as top-level), Exam product (as catalogue noun) |
| Draft publication work object | **Workspace** | Project, Pipeline instance |
| Student-selectable Ready offering | **Subject** (catalogue) | Curriculum (as radio label — use Subject title) |
| Authoritative syllabus package | **Curriculum** | Content pack, Graph |
| Studio product surface | **Curriculum Studio** | CMS, Curriculum Manager, Pipeline UI |
| CMP source document | **Official CMP** | CMP PDF (ok secondary), Content map file |
| Syllabus source document | **Official Syllabus** | Syllabus PDF (ok secondary) |
| Student-visible availability | **Ready** | Live, Active, Published (as catalogue badge — use Ready) |
| Not yet selectable | **Coming Soon** | Unavailable, Draft (in student catalogue) |
| Console home decision surface | **Overview** | Dashboard, Console Home (as page title) |
| Participant catalogue | **Students** | Participants (page title → Students) |

**Publish vs Ready:** Operators **Publish**; students see **Ready**. Do not badge student catalogue “Published”.

---

## 2. Student learning

| Concept | Canonical term | Forbidden synonyms in UI |
|---|---|---|
| Daily educational focus | **Mission** / **Today's Mission** | Focus card (as noun), Daily goal |
| Practice workflow instance | **Session** / **Today's Session** | Study session, Learning session, Mission (as CTA label) |
| Start practice CTA | **Start Today's Session** / **Start Session** / **Continue** | Begin Mission, Launch, Go |
| Syllabus progress map | **Journey** | Roadmap, Progress path, Learning path, Curriculum graph |
| Supporting review work | **Revision** | Remediation, Intervention |
| Practice archive | **History** | Analytics (student), Practice log (ok secondary) |
| Guidance memory store | **Decision Journal** | Feedback log, Coach diary |
| Chronological narrative | **Educational Timeline** | Story view, Second journal |
| Mentor attribution (once) | **Study Sensei** | Coach, AI tutor (as product name) |
| Recommendation panel noun | **Guidance** | Tip, Coach insight |
| Readiness toward exam | **Exam Readiness** | Mastery score, Twin score |
| Explainable summaries | **Learning Insights** | Twin insights, Student analysis |
| Plan configuration | **Study Plan** | Curriculum plan |
| Subject selection step | **Choose Exam** | Pick course, Select module |
| Prior-knowledge capture | **Calibration** | Baseline quiz (unless product renames later) |
| Post-session notice | **Session reflection** | Daily reflection, Feedback loop |
| Optional Journal form | **Sensei reflection** | Feedback Loop (never student-facing) |
| Product research form | **Product Check-in** | NPS survey (as title) |
| Student landing | **Home** | Dashboard |

**Mission vs Session:** Mission = what to focus on; Session = the practice vehicle. CTAs use Session verbs; Mission is the focus noun.

---

## 3. Shells & navigation

| Concept | Canonical term | Forbidden |
|---|---|---|
| Student shell | **Home** (entry) | Education OS (user-facing) |
| Operator shell | **Console** | Founder OS, FOS (L0) |
| Account configuration | **Settings** | Preferences (ok nested) |
| Orientation / unblock | **Help** | FAQ homepage essay |
| Destructive confirm | **Confirm** | Are you sure? (prefer specific verb) |

---

## 4. Status vocabulary (see also STATUS_SYSTEM.md)

| Concept | Canonical | Do not mix with |
|---|---|---|
| Blocking validation | **Blocking** | Error (when severity is gate), Critical (unless same meaning) |
| Non-blocking finding | **Warning** / **Advisory** | pick one family; prefer Warning |
| Workflow incomplete | **Incomplete** | Pending (ambiguous) |
| Awaiting operator | **Needs attention** | Action required (duplicate) |
| Successful publish outcome | **Published** (flash) | Released, Deployed |
| Student catalogue state | **Ready** | Published |

---

## 5. Implementation terms — never in L0 UI

| Internal | User-facing substitute |
|---|---|
| workspace_id / entity id | Subject code / Version label |
| Pipeline stage enum | Stage name (“Validation”) |
| Port unavailable | Studio service unavailable |
| Retrieval profile / embedding ms | (Advanced only or omit) |
| Feedback Loop | Sensei reflection |
| Dual-run / SOLE_RUNTIME | (omit) |
| Mission Engine | (omit) |

---

## 6. Verb consistency

| Action family | Canonical verbs | Avoid mixing |
|---|---|---|
| Enter practice | Start, Continue, Begin Session | Launch, Open Session, Go |
| Leave | Return Home | Back to Dashboard |
| Catalogue open | Open Workspace, Open | Launch, Enter |
| Create | Create Subject | New, Add Subject (ok if space) |
| Persist settings | Save | Update, Apply (unless form pattern requires) |
| Queue work | Review, Open | Disposition (internal) |

---

## 7. One-name enforcement checklist

Before shipping any screen:

1. Search for Release / Deploy / Activate / Go Live → replace with **Publish** where meaning is publication.  
2. Search for Dashboard (student) → **Home**.  
3. Search for Participants (title) → **Students**.  
4. Search for Course / Module as top-level catalogue noun → **Subject**.  
5. Search for Feedback Loop (student) → **Sensei reflection**.  
6. Ensure Ready (student) ≠ Published (operator flash) confusion in the same viewport.

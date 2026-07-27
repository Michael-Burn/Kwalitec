# Student Journey Specification — PR-001B

**Programme:** PR-001B — Student Pilot Journey  
**Audience:** Product, ops, and certification  
**Runtime:** Runtime C (published curriculum) via founder → student bridge  
**Non-goals:** Runtime A cutover, Twin activation, premium UI redesign, educational algorithm changes  

---

## Purpose

Define the certified end-to-end first-time student experience so a new Runtime C student can independently discover, enrol, understand, complete, and return for study using only the product and student documentation.

---

## Journey steps

For each step: expected user goal, educational information, potential confusion, recovery path, completion criteria.

### 1. Account creation / sign-in

| Aspect | Detail |
|---|---|
| **User goal** | Access Kwalitec with a provisioned invite account |
| **Educational information** | Login states invite-only Internal Alpha; no public self-registration |
| **Potential confusion** | Expecting a “Sign up” button |
| **Recovery** | Ask ops to provision via `flask create-test-user` / Stage 1 pilot script; then sign in |
| **Completion** | Authenticated session; alpha onboarding shown once if required |

### 2. Subject discovery

| Aspect | Detail |
|---|---|
| **User goal** | Find a published subject they can enrol in |
| **Educational information** | Study Plan wizard Step 1 shows **Published Curriculum** when discovery flags are on |
| **Potential confusion** | Legacy catalogue papers vs Published Curriculum; Coming Soon / Not Supported badges |
| **Recovery** | Choose a subject marked Supported under Published Curriculum; if none, contact founder/ops |
| **Completion** | A supported published subject is selected |

### 3. Subject selection

| Aspect | Detail |
|---|---|
| **User goal** | Confirm the subject and exam context |
| **Educational information** | Subject title/code; exam date preference in later wizard steps |
| **Potential confusion** | Selecting a legacy Runtime A paper by mistake |
| **Recovery** | Restart wizard; pick Published Curriculum category again |
| **Completion** | Wizard review shows the published subject ready to enrol |

### 4. Enrolment

| Aspect | Detail |
|---|---|
| **User goal** | Start studying the published syllabus |
| **Educational information** | Bridge routes to Runtime C (`published_curriculum`); no Runtime A StudyPlan row is created |
| **Potential confusion** | Expecting calibration after enrol (Runtime A habit) |
| **Recovery** | Docs explain Runtime C skips calibration and lands on Home; if enrol blocked, flash explains support/flag/duplicate |
| **Completion** | Active Runtime C enrolment; redirect to Student Home |

### 5. Dashboard arrival

| Aspect | Detail |
|---|---|
| **User goal** | Know what to do today |
| **Educational information** | Home hero: mission title, Why, Why now, You’ll work toward, Next; Educational context panel |
| **Potential confusion** | No Guided Session chrome (by design for pilot write-back) |
| **Recovery** | Read Educational context; open Journey for syllabus map |
| **Completion** | Home shows Runtime C educational panel and today’s mission |

### 6. Educational context

| Aspect | Detail |
|---|---|
| **User goal** | Understand syllabus position and rationale |
| **Educational information** | Today’s topic, curriculum position, learning objectives, why this mission, duration, Done when, prerequisites, journey (why today / previous / unlocks next), progress, exam pacing, What comes next |
| **Potential confusion** | Dense explainability disclosure |
| **Recovery** | Focus on Why / Why now / Done when / What comes next; expand “Why the system chose this” only if curious |
| **Completion** | Student can answer the four clarity questions (see Educational Clarity Review) |

### 7. First mission

| Aspect | Detail |
|---|---|
| **User goal** | Study the assigned topic using their materials |
| **Educational information** | Mission title, objectives, estimated duration, Done when criteria |
| **Potential confusion** | CTA is **Mark mission complete** (not Start Guided Session) |
| **Recovery** | Pilot Guide explains study-offline-then-confirm model |
| **Completion** | Student has studied against Done when criteria |

### 8. Mission completion

| Aspect | Detail |
|---|---|
| **User goal** | Record that today’s learning is done |
| **Educational information** | Success flash with topic; Home shows day complete + next guidance |
| **Potential confusion** | Clicking complete twice |
| **Recovery** | Duplicate complete shows recoverable info flash; progress already saved |
| **Completion** | Mission status `completed`; progress events written |

### 9. Progress update

| Aspect | Detail |
|---|---|
| **User goal** | See that the syllabus advanced |
| **Educational information** | Coverage %, completed topics on Journey, unlocks next |
| **Potential confusion** | Expecting a second mission the same calendar day |
| **Recovery** | Docs: one mission per day; return tomorrow |
| **Completion** | Journey lists completed topic; coverage increased |

### 10. Journey advancement

| Aspect | Detail |
|---|---|
| **User goal** | Know what topic comes next |
| **Educational information** | Journey current/upcoming; unlocks_next / What comes next |
| **Potential confusion** | Revision/History still Runtime A-framed |
| **Recovery** | Use Home + Journey for Runtime C authority during pilot |
| **Completion** | Student can name the next syllabus topic |

### 11. Returning for the next study session

| Aspect | Detail |
|---|---|
| **User goal** | Sign in again and continue without re-enrolment |
| **Educational information** | Login routes Runtime C enrollees (no StudyPlan) to Home; new day’s mission for next topic |
| **Potential confusion** | Being sent to the wizard again (fixed in PR-001B) |
| **Recovery** | If wizard appears unexpectedly, confirm enrolment still exists; contact ops |
| **Completion** | Home shows next topic mission with clarity fields |

---

## Certified scenarios

| Scenario | Intent |
|---|---|
| **First-day experience** | Discover → enrol → understand → complete one mission |
| **Consecutive study sessions** | Complete day N; day N+1 shows next topic |
| **Interrupted session recovery** | Leave without completing; same mission still open |
| **Missed-day return** | Gap of days; current topic unchanged until completed |
| **Multiple missions** | Complete missions across days; coverage advances |

---

## Coexistence invariants

- Runtime A students without Runtime C enrolment keep prior Home behaviour.
- Runtime C Home/Journey use educational experience projection.
- No Twin / Adaptive interruption.
- Feature flags for discovery/enrolment remain the rollout control.

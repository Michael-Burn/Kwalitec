# Common Issues Guide — Student Pilot

**Programme:** PR-001B  
**Audience:** Students and pilot ops supporting students  

---

## Sign-in and landing

| Symptom | Likely cause | What to do |
|---|---|---|
| No Sign up button | Invite-only alpha | Ask organiser for an account |
| Invalid email or password | Typo or wrong env | Retry; confirm which environment URL; reset via ops |
| Sent to study plan wizard after already enrolling | Missing Runtime C enrolment or wrong account | Confirm email; ops verifies `RuntimeEnrolment`; do not create a second enrolment unless told |
| Alpha onboarding every time | Onboarding not marked complete | Finish or skip onboarding once |

## Discovery and enrolment

| Symptom | Likely cause | What to do |
|---|---|---|
| No Published Curriculum category | Discovery flag off | Ops enables `KWALITEC_PUBLISHED_SUBJECT_DISCOVERY` / bridge umbrella |
| Subject Coming Soon / Not Supported | Enrolment flag or support gate | Choose another subject; founder publishes/support; ops enables Runtime C enrolment |
| Enrolment flash / blocked | Duplicate enrolment, missing package, or support failure | Read flash; open wizard step 2; contact founder if subject unpublished |
| Expected calibration | Runtime A habit | Ignore — Runtime C lands on Home |

## Home and mission clarity

| Symptom | Likely cause | What to do |
|---|---|---|
| No Educational context panel | Not on Runtime C enrolment | Confirm published-subject enrol; refresh |
| CTA says Mark mission complete | Expected pilot behaviour | Study materials, then confirm |
| “Session will be ready…” with no CTA | Mission not generated / syllabus complete / error | Refresh; check Journey; if syllabus complete, no further missions |
| Don’t understand the mission | Skipped Educational context | Read Why, Why now, Done when, What comes next |

## Completion and progress

| Symptom | Likely cause | What to do |
|---|---|---|
| Complete button errors | Transient failure or stale page | Refresh Home; retry once |
| “Already complete” | Double submit | Safe — progress saved; return tomorrow |
| No second mission today | One mission per day | Return next calendar day |
| Journey doesn’t show progress | Looking at wrong surface / not completed | Complete from Home; reopen Journey |
| Progress vanished after finishing syllabus | Enrolment completed | Home/Journey should still show syllabus complete; contact ops if Home looks empty |

## Return sessions

| Symptom | Likely cause | What to do |
|---|---|---|
| Different topic after incomplete day | Unexpected | Should stay on current topic until complete — report to ops with date/subject |
| Same topic after complete + next day | Generation/date issue | Confirm local date; refresh; ops checks mission instances |
| Revision/History confusing | Not Runtime C projected yet | Use Home + Journey for pilot authority |

## Ops quick checks

1. Feature flags: discovery + Runtime C enrolment (+ allowlist if used).  
2. Subject has an active published package.  
3. User has `RuntimeEnrolment` (active or completed).  
4. Home HTML includes `data-educational-experience="runtime-c"`.  
5. Acceptance suite: `pytest tests/certification/test_pr001b_student_pilot.py`.

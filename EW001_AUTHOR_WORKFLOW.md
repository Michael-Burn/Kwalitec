# EW-001 — Author Workflow

**Programme:** Editorial Production Infrastructure EW-001 — Editorial Authoring Workspace  
**Status:** Binding — author-facing production journey  
**Effective:** 2026-08-01  
**Parent:** `EW001_EDITORIAL_WORKSPACE_SPEC.md`  
**Companion:** `EW001_AUTHOR_CHECKLIST.md`  
**Authority:** Educational Excellence Framework (Frozen) · Educational Operations (Frozen) · TV-001 PASS · EJ-001 PASS  
**Nature:** Process guidance for Educational Authors — **not** application code, **not** educational content generation, **not** framework redesign  

---

## 1. Purpose

Guide an Educational Author from blank workfile to Approver-ready dossier through **one ordered journey** of ten stages.

You do **not** need to read the full EA / EO / EJ / TV document set as your primary guide.  
Those frameworks are already built into the stage prompts below. Open the frozen documents only when a stage’s “Why this matters” drawer or a reviewer cites a gate ID.

> **Follow the stages in order.**  
> **Finish each stage’s exit criteria before treating the next as complete.**  
> **If defence fails, revise the Mission — do not decorate a weak design with polished Justification.**

---

## 2. Before you start

### 2.1 Preconditions (Commission)

Confirm EO-001 Stage 0 Commission exists for the Volume (or you are working under an approved series charter):

- Subject + provisional volume / package scope known  
- Curriculum package + CMP edition pin available  
- Author of Record named  
- Anti-mirage claims forbidden at commission acknowledged  

If Commission is missing, **stop**. Do not invent a commercial Mission outside the ops spine.

### 2.2 Open the Editorial Workfile

Create or open one Workfile per Mission (see Spec §6.1). Record:

| Field | Example |
|-------|---------|
| `mission_id` | *(house ID)* |
| `subject_id` | e.g. CS1 |
| `package_version` | target package version |
| `mode` | `learning` / `revision` |
| `author_of_record` | you |
| `cmp_edition` | pinned edition |
| `volume_id` | Volume dossier membership |

Set stage statuses: S1 = `active`; S2–S10 = `locked` (preview allowed).

### 2.3 Author stance (30 seconds)

Answer privately before Stage 1:

1. What is the **one** skill or conceptual move of the day?  
2. If an IFoA-aware tutor challenged this Mission, could I defend placement, load, CMP locus, revision timing, stop, and tomorrow?  
3. What misconception am I hunting?

If (1) is empty, you are not ready to author. If (2) will clearly fail, redesign before writing student prose.

---

## 3. The ten-stage journey

```text
S1  Mission objective
S2  Syllabus objectives
S3  CMP references
S4  Educational Justification (J1–J10)
S5  Tutor Voice mission
S6  Knowledge checks
S7  Reflection
S8  Tomorrow bridge
S9  Certification evidence
S10 Publication dossier
```

---

## Stage S1 — Mission objective

### What you are collecting

The day’s educational centre: objective, concept focus, success criterion, and private Tutor Intent.

### Prompts (answer in the Workfile)

1. **Tutor Intent (internal):** What coaching move are you making today that another tutor would recognise as specific?  
2. **Concept focus:** What single idea or skill defines the day?  
3. **Learning objective:** One actionable verb + outcome — **not** a paste of the syllabus heading.  
4. **Success criterion:** What must the candidate be able to explain or do when the Session ends? (countable, assessable)

### Do / Don’t

| Do | Don’t |
|----|-------|
| Write Intent first, student title later | Start from a syllabus heading as the Mission |
| Keep one centre of gravity | Pack three topics into one evening |
| Use assessable verbs (explain, derive, justify, compare) | Use “understand,” “cover,” “strengthen today’s focus” |

### Exit criteria

- [ ] Tutor Intent drafted  
- [ ] Concept focus named  
- [ ] Learning objective distinct from syllabus heading  
- [ ] Success criterion assessable  

**Mark S1 `complete` → unlock S2.**

### Behind the glass (reference only)

EA-001 M2/M5/M6 · EA-003 Steps 1–2 · Mission Philosophy Tutor Brief test.

---

## Stage S2 — Syllabus objectives

### What you are collecting

Lawful identity: official topic, syllabus learning outcomes served, mode, continuity context.

### Prompts

1. **Topic code + official title** (from curriculum package — never invent).  
2. **Syllabus learning outcomes / objectives** this Mission serves (cite codes or exact LO text pointers).  
3. **Mode:** Learning or Revision — labelled honestly.  
4. **Prior context:** Prior Mission/topic ID, or lawful cold-start (enrolment goal / chapter purpose).  
5. **Why this topic is on-path now** (one sentence — full defence comes in S4/J1).

### Do / Don’t

| Do | Don’t |
|----|-------|
| Copy identity from authoritative curriculum JSON/syllabus | Use placeholders or contaminant publisher strings |
| Separate *syllabus LO* (S2) from *Mission objective* (S1) | Collapse Mission objective into the syllabus heading |
| Disclose Revision focus when not Learning-order | Pretend Revision is “next Learning topic” |

### Exit criteria

- [ ] Official topic code + title recorded  
- [ ] Syllabus LO pointers recorded  
- [ ] Mode set  
- [ ] Prior / cold-start context recorded  
- [ ] No placeholder identity  

**Mark S2 `complete` → unlock S3.**

### Behind the glass

Constitution Article VI · EA-001 M1/M3/M4 · EA-003 Inputs table.

---

## Stage S3 — CMP references

### What you are collecting

Authorised material locus and reading craft (Guidance-Over-Content).

### Prompts

1. **CMP edition** (must match Volume pin).  
2. **Open point:** Exact TOC / section locus where the candidate starts.  
3. **Aim:** What they hunt or extract at that locus (one clear aim).  
4. **Stop condition:** Where they stop — and why stopping there is educationally correct.  
5. **Out of scope:** What adjacent CMP material they must not chase tonight.  
6. **Return path:** How Episode/knowledge-check work uses what they read (pointer — detail in S6).

### Do / Don’t

| Do | Don’t |
|----|-------|
| Point into the authorised CMP | Invent a second textbook in Mission narrative |
| Defend stop as craft | Select a locus because it “looks important” without LO fit |
| Keep Mission body free of raw CMP paste | Dump paragraphs of CMP into student-facing Mission |

### Exit criteria

- [ ] Edition + open + stop + out-of-scope complete  
- [ ] Aim stated  
- [ ] No raw CMP paste planned as Mission body  

**Mark S3 `complete` → unlock S4.**

### Behind the glass

EP-01 · EP-04 · EA-001 M8 · EA-003 Step 4 · TV-001 T3 corroboration target.

---

## Stage S4 — Educational Justification (J1–J10)

### What you are collecting

The **editorial** Justification pack — not student copy. Duplicate `EJ001_MISSION_JUSTIFICATION_TEMPLATE.md` into the Workfile (or Volume dossier path) and fill it.

### Authoring order (recommended inside this stage)

```text
J8 → J1 → J6 → J3 → J5 → J2 → J4 → J9 → J7 → J10 → Expert-defence paragraph
```

| ID | You answer |
|----|------------|
| **J8** | Syllabus/CMP support — identity + locus truth |
| **J1** | Why this topic at this point |
| **J6** | Tomorrow continuity rationale |
| **J3** | Why this CMP reading |
| **J5** | Why this stopping point |
| **J2** | Why this workload |
| **J4** | Revision timing (including honest “not today”) |
| **J9** | Misconception prevention design |
| **J7** | Educational science actually applied |
| **J10** | Expected outcome + explicit non-claims |

Then write the **Expert-defence** paragraph (Template §D): how you would defend this Mission to an IFoA-aware tutor.

### Do / Don’t

| Do | Don’t |
|----|-------|
| Defend the Mission as authored | Decorate a weak Mission with Justification theatre |
| Cite concrete IDs, loci, EP moves | Reusable boilerplate across Missions |
| Keep this artefact internal | Paste Justification onto student surfaces |

### Exit criteria

- [ ] All J1–J10 present and Mission-unique  
- [ ] Expert-defence written  
- [ ] Status set to `complete`  
- [ ] Cross-check: Justification does not contradict S1–S3 decisions  
- [ ] EJ-R01–EJ-R13 self-scan recorded (see Checklist)  

**Mark S4 `complete` → unlock S5.**  
If later stages change educational decisions, return here and update Justification before resubmitting review.

### Behind the glass

EJ-001 Standard · Template · Authoring Guidelines · TV-001 T1–T7 evidence targets.

---

## Stage S5 — Tutor Voice mission

### What you are collecting

Student-facing Mission brief (AF-MS / EA-003 schema fields) in Study Sensei voice.

### Prompts (write after S1–S4 foundations)

1. Continuity lines: `prior_bridge` (and ensure tomorrow will be honest in S8).  
2. Student prose: `display_title`, `mission_purpose`, `why_now`, `explainability`, `expected_benefit`.  
3. Pack fields: misconceptions (1–3), study strategy, load + minutes, revision signals, session intent, linked Session/Episode IDs (draft-link allowed until S6 completes).  
4. Self-deny prohibited patterns P1–P12.  
5. Style Guide + Tutor Voice Guide self-check.

### Fit test (mandatory)

Read the brief aloud as an IFoA tutor’s night-before note.  
If you would not send it to a candidate, **rewrite** — do not polish placeholders.

### Do / Don’t

| Do | Don’t |
|----|-------|
| Calm, specific, exam-serious voice | Platform meta, milestone IDs, runtime names on hero |
| Unique explainability | Identical boilerplate across Missions |
| Match session intent to real Episodes | Advertise stages with no authored substance |

### Exit criteria

- [ ] All mandatory Mission elements M1–M12 addressable from pack  
- [ ] P1–P12 denied  
- [ ] Style + Voice self-check recorded  
- [ ] Fit test PASS (author judgement)  
- [ ] Linked Session intent present  

**Mark S5 `complete` → unlock S6.**

### Behind the glass

EA-002 Tutor Voice + Style · EA-003 Steps 8–10 · Gate MG · EA-001 Mission Philosophy.

---

## Stage S6 — Knowledge checks

### What you are collecting

Episode-level **active cognitive demands** (knowledge checks): the moments that force retrieval, justification, comparison, or diagnosis — including misconception hunt.

### Prompts

1. List Episodes that realise the Session intent (order + purpose).  
2. For each Episode: what the candidate **does** (not only reads).  
3. Mark ≥1 **knowledge check** with active demand (retrieve / justify / derive / diagnose / compare).  
4. Tie each check to Mission success criterion and/or a listed misconception.  
5. Confirm Guided Reading (if used) names locus, hunt, action, stop, return — consistent with S3.

### Do / Don’t

| Do | Don’t |
|----|-------|
| Force misconceptions into the open | Passive “read and proceed” only |
| Align checks with success criterion | Invent checks that the Mission never prepared |
| Keep demand proportional to load (J2) | Exam theatre: five unrelated mini-tests |

### Exit criteria

- [ ] Episode set authored / linked  
- [ ] ≥1 active knowledge check  
- [ ] Misconception(s) addressed by design  
- [ ] Session intent matches Episode count/roles  
- [ ] Gate LE self-check recorded  

**Mark S6 `complete` → unlock S7.**

### Behind the glass

EA-004 Study Session Flow / Episode law · Gate LE · SS-03 · EP active demand.

---

## Stage S7 — Reflection

### What you are collecting

Topic-specific Reflection that harvests residual uncertainty (student-authored path).

### Prompts

1. `reflection_goal` — what residual you intend to harvest.  
2. Reflection prompt triad (topic-bound): what clicked / what remains shaky / what you’ll need tomorrow.  
3. Confirm Reflection is **not** generic wellness or platform meta.  
4. Confirm completion language does not claim mastery.

### Do / Don’t

| Do | Don’t |
|----|-------|
| Bind prompts to concept focus / misconceptions | Reuse identical Reflection across unrelated topics |
| Leave a student-authored path | Auto-fill fake residual text as if student-written |
| Align with Session close | Skip Reflection because “time is short” in authoring |

### Exit criteria

- [ ] Reflection prompts topic-specific  
- [ ] Student-authored path exists  
- [ ] `reflection_goal` aligns to concept or misconceptions  
- [ ] SS-04 self-check recorded  

**Mark S7 `complete` → unlock S8.**

### Behind the glass

EP-07 · Gate SS-04 · AF-RF · EA-004 Session close.

---

## Stage S8 — Tomorrow bridge

### What you are collecting

Honest continuity handoff (`tomorrow_bridge` / Tomorrow Preview fields).

### Prompts

1. Is the next lawful focus **known**? If yes: topic + continuity line. If no: honest empty / deferred note.  
2. Continuity line agrees with Mission handoff used on Summary / Home.  
3. No heavy new teaching assigned after today’s Reflection.  
4. Align with J6 — if J6 promised a bridge, S8 must realise it (or update J6).

### Do / Don’t

| Do | Don’t |
|----|-------|
| Prefer educational continuity | Vague “keep going” cheerleading |
| Allow honest unknown | Invent a next topic to look complete |
| Keep load for tomorrow proportionate | Dump tonight’s overflow as “tomorrow’s Mission” without design |

### Exit criteria

- [ ] `tomorrow_bridge` complete (known or honest empty)  
- [ ] Continuity line consistent with Mission handoff  
- [ ] Gate TP self-check recorded  
- [ ] J6 still consistent (else return to S4)  

**Mark S8 `complete` → unlock S9.**

### Behind the glass

EA-001 M10 · Gate TP · AF-TP · EA-004 Session Philosophy §9.

---

## Stage S9 — Certification evidence

### What you are collecting

The evidence pack for EA-002 multi-stage certification — assembled from work already done.

### Assemble

| Evidence item | Source stages |
|---------------|---------------|
| Mission pack + Gate MG self-evidence | S1–S5 |
| Episode / Session Gate LE + SS self-evidence | S6–S8 |
| Style + Tutor Voice self-checks | S5 |
| Educational Justification (`complete`) | S4 |
| Defect log (empty or resolved) | Workfile |
| Joint composition confirmation | Mission ⇄ Session ⇄ Episodes ⇄ Reflection ⇄ Tomorrow |
| Universal preconditions U1–U7 self-scan | Checklist |
| Principle citations (EP IDs) | Mission pack |

### Author actions

1. Run `EW001_AUTHOR_CHECKLIST.md` end-to-end.  
2. Set Workfile status to **ready for Educational Review**.  
3. Do **not** self-certify commercial packs alone.  
4. Do **not** request Publication Approval from this stage — that is S10 + EO Approver.

### Exit criteria

- [ ] Checklist complete  
- [ ] Evidence URIs / paths recorded in Workfile  
- [ ] Justification attached and current  
- [ ] Joint composition confirmed  
- [ ] Ready for EA-002 stages ① Educational Review → ② Tutor Review → ③ Curriculum Review → ④ Quality Gate Review  

**Mark S9 `complete` → unlock S10.**

### Behind the glass

EA-002 Certification Workflow · EA-001 Quality Gates · EJ-001 publication hard rule.

---

## Stage S10 — Publication dossier

### What you are collecting

EO-001 / EA-002 Publication dossier fields so Approvers receive a deterministic inventory — not a scavenger hunt.

### Prompts / fields

1. Subject ID + package version.  
2. Artefact inventory (Mission, Session, Episode IDs, Reflection, Tomorrow Preview).  
3. Certification evidence reference (from S9).  
4. Justification ID + status (will become `locked` at Approval).  
5. Campaign / Volume membership pointers (if Campaign-scoped: EA-008 / Volume dossier).  
6. FP / anti-mirage denials (AU-04 spirit).  
7. Author statement: no student-pathway release performed from Authoring.

### Author actions

1. Update Volume Dossier worklist membership.  
2. Submit Publication **Request** only after Certification stages PASS (reviewers own those PASS marks).  
3. Stop. Approver signs under EO-001 Stage 5 — not the author.

### Exit criteria

- [ ] Inventory complete  
- [ ] Evidence + Justification pointers present  
- [ ] Volume dossier slot updated  
- [ ] Authoring release prohibition affirmed  
- [ ] Workfile status `authoring_complete` / awaiting review outcomes  

**Mark S10 `complete`.** Authoring journey ends. Review and Approval continue under frozen EO/EA law outside this workflow’s authorship loop.

### Behind the glass

EO-001 Stages 1–5 · EA-002 Publication Workflow · EJ-001 §4 hard rule · PR-001 ops registers (when in use).

---

## 4. Rework loops

| Trigger | Return to |
|---------|-----------|
| Educational Review FAIL on substance | Earliest failing stage (often S5–S8); update S4 if decisions change |
| Tutor Review FAIL on voice/continuity | S5 and/or S8 |
| Curriculum Review FAIL on locus/identity | S2–S3; then S4 J8/J3 |
| Justification review_fail | S4 only (unless Mission must change) |
| Gate HOLD (missing locus, etc.) | Blocking stage; HOLD is not PASS |
| Edition bump / CMP pin change | S3 → S4 (minimum); re-run S9–S10 |

Never skip to Approver because the calendar is tight (EO-001 design posture).

---

## 5. What “framework invisible” means in practice

| You open | You usually do not open first |
|----------|-------------------------------|
| This workflow | Full EA-001–EA-008 suite |
| Author Checklist | EO-001 full lifecycle essay |
| EJ Template (inside S4) | TV-001 philosophy paper |
| Mission / Session pack fields | Scattered implementation reports |

When a reviewer cites `MG-07` or `EJ-R13`, open the cited law. Until then, stay in the journey.

---

## 6. Closing discipline

> **One journey. Ten stages. Every required decision explicit.**  
> **Excellence runs underneath — almost invisible, never optional.**  
> **Publish only when Justification, craft, checks, Reflection, tomorrow, evidence, and dossier are complete — and human certification has PASSed.**

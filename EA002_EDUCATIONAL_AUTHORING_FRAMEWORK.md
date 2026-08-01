# EA-002 — Educational Authoring Framework

**Programme:** Educational Excellence Programme EA-002  
**Phase:** Educational Production Framework  
**Status:** Binding — permanent educational production system for Version 1 onward  
**Effective:** 2026-08-01  
**Nature:** Authoring, review, certification, publication, and maintenance law — not content generation, not application code  

**Authority cited:** EA-001 PASS · EV-001 · `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` · `PRODUCT_BLUEPRINT.md` · Vision 2030 · Study Sensei Philosophy · Guidance Over Content · Canonical Educational Lexicon  

**Companion deliverables:** `EA002_TUTOR_VOICE_GUIDE.md` · `EA002_EDUCATIONAL_STYLE_GUIDE.md` · `EA002_PUBLICATION_WORKFLOW.md` · `EA002_CERTIFICATION_WORKFLOW.md` · `EA002_IMPLEMENTATION_REPORT.md`

**Does not:** rewrite CS1 · generate educational content · modify application code · amend EA-001 principles · declare EV-001 FAIL resolved  

---

## 1. Purpose

This framework defines **how** premium educational artefacts are authored, reviewed, certified, published, and maintained so that different authors produce Kwalitec content that feels like it was written by one exceptional tutor.

EA-001 established *what* teaching is and *what must pass*.  
EA-002 establishes the **production system** that makes that law operational.

> **Nothing educational is authored without inputs.**  
> **Nothing educational is published without certification.**  
> **Nothing educational is maintained without continuity of truth.**

---

## 2. Position in the authority stack

| Rank | Authority | EA-002 relationship |
|-----:|-----------|---------------------|
| 1 | Vision 2030 | Superior — purpose, north star |
| 2 | Product Blueprint / experience guidelines | Superior — product strategy and feel |
| 3 | Educational Constitution | Superior — truth, mastery, evidence, modes |
| 3a | EA-001 teaching constitution | Superior — principles, philosophies, quality gates |
| **3b** | **EA-002 Educational Authoring Framework (this family)** | Binding production process under EA-001 |
| 4 | EVF / EV-001 and successors | Consume EA-002 packs when judging authored artefacts |
| — | Implementation, templates, generators | Must comply; never redefine authoring by behaviour |

If production practice would contradict EA-001 or higher law, **stop**. Amend the superior document first.

---

## 3. Artefact catalogue

Every educational artefact that reaches students belongs to one class below. Each class has a full lifecycle: Inputs → Authoring → Review → Certification → Publication → Maintenance.

| Class | Code | Gate (EA-001) | Primary student moment |
|-------|------|---------------|------------------------|
| Mission | AF-MS | Gate MG | Home / Today’s focus |
| Learning Episode | AF-LE | Gate LE | Session stages |
| Session (arc + Overview) | AF-SS | Gate SS | Overview → close |
| Revision plan / activity | AF-RV | Gate RV | Revision workspace / revision Session |
| Tomorrow Preview | AF-TP | Gate TP | Summary / Home continuity |
| Reflection | AF-RF | Gate SS (SS-04) + EP-07 | Post-study close |

**Joint publication rule:** A Mission may not publish alone. Linked Session and Episodes must be certified together (or the Mission must be honestly unavailable). See `EA002_PUBLICATION_WORKFLOW.md`.

---

## 4. Universal lifecycle (all artefacts)

```text
REQUIRED INPUTS
      ↓
AUTHORING WORKFLOW          (draft under this Framework + Style + Voice)
      ↓
EDUCATIONAL REVIEW          (substance vs EP-01–EP-10)
      ↓
TUTOR REVIEW                (Tutor Voice + IFoA-tutor brief test)
      ↓
CURRICULUM REVIEW           (syllabus / CMP locus / contaminant check)
      ↓
QUALITY GATE REVIEW         (EA-001 MG/LE/SS/RV/TP + universal U1–U7)
      ↓
PUBLICATION APPROVAL        (human sign-off; package version stamp)
      ↓
MAINTENANCE WORKFLOW        (drift, Twin truth, CMP edition, sitting changes)
```

**Hard rule:** A single failed stage blocks publication. There is no parallel “ship then fix voice” path.

Detail for stages 3–6: `EA002_CERTIFICATION_WORKFLOW.md`.  
Detail for publication and maintenance: `EA002_PUBLICATION_WORKFLOW.md`.

---

## 5. Universal authoring requirements

Every artefact draft must declare:

| Field | Requirement |
|-------|-------------|
| **Artefact ID** | Stable identifier within subject package version |
| **Subject / package version** | Official curriculum package identity |
| **Syllabus node** | Lawful topic code + human title (U1) |
| **CMP locus** | Where content lives (section/LO/example) when reading or practice depends on CMP |
| **Principle citations** | EP-01–EP-10 IDs that the artefact is designed to satisfy |
| **Twin / evidence inputs** | Which learner-state facts (if any) the artefact assumes or may consume |
| **Voice check** | Conforms to `EA002_TUTOR_VOICE_GUIDE.md` |
| **Style check** | Conforms to `EA002_EDUCATIONAL_STYLE_GUIDE.md` |
| **Prohibited-pattern scan** | Explicit denial of EA-001 Mission P1–P12 / EV-001 TB classes as applicable |

**Prohibited shortcuts (universal):**

- Shipping placeholders (“Today’s topic”, TODO, TBD, unfilled tokens)  
- Syllabus-heading paste as the teaching body  
- Raw CMP dump as Kwalitec prose  
- Identical explainability boilerplate across artefacts  
- Platform / engineering jargon on primary study surfaces  
- Claiming mastery from first-pass completion  
- Publishing a brief over empty or unreachable stages  
- Silent dual-truth across Home / History / Revision / Journey  

---

## 6. Mission authoring (AF-MS)

### 6.1 Purpose

Author the day’s authorised educational focus as a **tutor brief**: what, why now, expected benefit, and how it will be executed — never a syllabus checkbox.

### 6.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Official topic code + title | Syllabus / curriculum package | Yes |
| Prior topic / Mission (or cold-start context) | Twin / History / plan | Yes |
| Mode | Learning / Revision (Constitution Article VI) | Yes |
| Exam sitting date + weight cues (when known) | Twin / syllabus weights | Preferred |
| Linked Session intent + Episode IDs | Session authoring pack | Yes before publish |
| CMP locus for today’s work | CMP TOC / LO map | Yes |
| Residual uncertainties from prior Reflection | Soft evidence | When available |

### 6.3 Required outputs

Complete M1–M12 fields per `EA001_MISSION_PHILOSOPHY.md`: Topic · Distinct objective · Bridge · Why now · Concept focus · Success criterion · Session intent · Material locus · Expected benefit · Handoff · Explainability · Tutor Voice.

### 6.4 Mandatory educational elements

Bridge from prior learning · one actionable objective · one concept focus · countable success criterion · CMP locus · Session structure that exists · specific why-now · tomorrow handoff or honest absence.

### 6.5 Mandatory CMP references

Named open point in CMP (chapter/section/example). Never “the material” alone.

### 6.6 Mandatory syllabus references

Topic code + accurate title. Objective must **not** equal the syllabus heading string.

### 6.7 Educational reasoning

A Mission multiplies CMP value by deciding *today’s* focus and success check (EP-01, EP-08). Continuity and explainability protect trust (EP-02, EP-09, EP-10).

### 6.8 Prohibited shortcuts

EA-001 Mission P1–P12 in full. Especially: title = objective = narrative; boilerplate why-now; platform meta as hero copy; beautiful brief over empty episodes.

### 6.9 Premium quality (illustrative pattern — not live CS1 content)

> Bridge from yesterday’s completed unit → today’s skill in tutor language → specific exam-relevant why-now → CMP locus through a named example → success the student can demonstrate closed-book → lawful tomorrow handoff.

### 6.10 Unacceptable quality

> “Study 4.2 — Understand and use generalised linear models” as title, objective, and narrative; why = “highest-value next step toward exam readiness”; no CMP locus; no bridge.

---

## 7. Learning Episode authoring (AF-LE)

### 7.1 Purpose

Author one bounded, teachable stage inside a Session (Guided Reading, Worked Example, Practice, Checkpoint, or equivalent) with one objective and real cognitive work.

### 7.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Parent Mission ID + topic | Mission pack | Yes |
| Episode type | Authoring taxonomy | Yes |
| Learning objective (distinct from topic title) | Author | Yes |
| CMP locus (for reading / example types) | CMP | Yes for Guided Reading / Worked Example |
| Position in Session (N of M) | Session arc | Yes |
| Duration budget | Session Philosophy honesty | Yes |
| Success criteria (2–4) | Author | Yes |

### 7.3 Required outputs

Teachable student instruction · focus prompts or practice stem · active cognitive demand · success criteria · return / advance cue · accurate feedback path where answers are objective.

### 7.4 Mandatory educational elements

One clear objective · educational coherence with Mission · CMP vs Kwalitec roles correct · active demand (note / recall / solve / justify) · no empty free-text-only reading shell.

### 7.5 Mandatory CMP references

For Guided Reading / Worked Example: section or example identity + stop condition.  
For Practice: optional formula reference **after** attempt only.

### 7.6 Mandatory syllabus references

Parent topic code; objective language aligned to lawful learning outcomes without pasting the outcome title as the whole episode.

### 7.7 Educational reasoning

Episodes implement Deliberate Study and Guided Reading (EP-03, EP-04) and convert exposure into recall/evidence candidates (EP-05) without republishing the textbook (EP-01).

### 7.8 Prohibited shortcuts

Empty “read the material for Today’s topic” · CMP paste · mechanical template concatenation · advertising N of M when stages missing · false mathematical claims · duration theatre without depth.

### 7.9 Premium quality

> “In CMP §X.Y, find the definition of [concept]. Write it in your own words. After Example N, pause before the solution and attempt the middle step. Return here for a one-minute closed-book recall.”

### 7.10 Unacceptable quality

> “Read the material.” + free-text box + “Answer recorded” with no feedback and no Continue.

---

## 8. Session authoring (AF-SS)

### 8.1 Purpose

Author the full study arc so an IFoA tutor would assign it as the student’s primary block for the hour: Overview → Before / During / After Reading → Reflection → Summary / Tomorrow.

### 8.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Certified or co-drafted Mission | AF-MS | Yes |
| Ordered Episode set implementing Session intent | AF-LE | Yes |
| Reflection pack | AF-RF | Yes |
| Tomorrow Preview pack | AF-TP | Yes (or honest empty) |
| Duration claim | Authoring | Yes |
| Evidence effect notes | Constitution VIII | Yes (completion ≠ mastery) |

### 8.3 Required outputs

Session Overview that answers “Am I ready to begin?” · Before Reading briefing · reachable stages matching advertised count · After Reading active demand · topic-specific Reflection · Summary language that does not invent mastery · Tomorrow Preview aligned with Mission handoff.

### 8.4 Mandatory educational elements

Real topic data on Overview · focus questions before CMP opens · Guided Reading alive prompts · at least one Active Recall or Practice demand · Reflection required before educational close · stage advance integrity.

### 8.5 Mandatory CMP references

Material locus inherited from Mission; stop conditions in During Reading; no chapter dump inside Overview.

### 8.6 Mandatory syllabus references

Topic code + title on Overview and throughout; no placeholder lexicon.

### 8.7 Educational reasoning

The Session is where Guidance Over Content becomes lived behaviour: Kwalitec structures study; CMP holds exposition (Foundation §4–5; Session Philosophy).

### 8.8 Prohibited shortcuts

Opening Overview without bound topic · restacking Home as a wall · skipping Reflection · stuck Continue · duration claims that contradict depth · Summary mastery theatre.

### 8.9 Premium quality

> Overview names real topic and success · Before Reading primes 2–4 hunt questions · During Reading guides into CMP with annotation task · After Reading closed-book check · Reflection names the fuzzy idea · Tomorrow preview connects skill bridge.

### 8.10 Unacceptable quality

> Overview/Activity/Reflection all say “Today’s topic”; reading stage is an empty shell; continue broken after answer.

---

## 9. Revision authoring (AF-RV)

### 9.1 Purpose

Author deliberate rework of previously studied material for retention and exam consolidation — labelled as revision, triggered from evidence (or disclosed student choice), never as first-pass mastery theatre.

### 9.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Prior study identity (topic / Mission / evidence) | Twin / History | Yes |
| Trigger | Decay, gap, weight, sitting pressure, or student choice | Yes |
| Mode label | Revision (not Current Learning Topic first-pass) | Yes |
| CMP locus for rework | CMP | Yes |
| Weak-point cues from Reflection / practice | Soft / hard evidence | Preferred |

### 9.3 Required outputs

Revision label · explainable why-revise · deliberate activity (re-work example, spaced recall, exam-skill drill) · completion language that does not narrate first-pass Topic Complete / mastery · continuity to prior learning identity.

### 9.4 Mandatory educational elements

Evidence-backed or disclosed trigger · rework not empty first-pass shell · Tutor Voice · One Educational Truth with Home/History/Revision.

### 9.5 Mandatory CMP references

Named rework locus (often narrower than first-pass chapter span).

### 9.6 Mandatory syllabus references

Lawful topic node previously studied or warranted; never contaminant nodes.

### 9.7 Educational reasoning

Progressive Mastery and Exam Focus require return to weak, high-weight material (EP-06, EP-08). Empty “Nothing to revise” against high coverage is a trust break (EV-001 TB-005).

### 9.8 Prohibited shortcuts

Re-pasting empty first-pass shells · celebrating coverage while denying revisable material without reason · mastery language on revision completion · comfort-topic preference over weight/decay.

### 9.9 Premium quality

> “Revise yesterday’s weak link-function justification — re-attempt Example 3 closed-book, then check against CMP. Trigger: soft evidence named link as fuzzy; topic has exam weight.”

### 9.10 Unacceptable quality

> “Nothing to revise yet” while Home shows high coverage and History shows completed study, with no disclosed cold-start reason.

---

## 10. Tomorrow Preview authoring (AF-TP)

### 10.1 Purpose

Author the continuity bridge that answers **What happens next?** without inventing syllabus nodes or assigning heavy new teaching after Reflection.

### 10.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Today’s topic + objective | Mission / Session | Yes |
| Next lawful focus (when known) | Syllabus order / plan / Twin | Yes when known |
| Continuity skill bridge | Author | Yes when next known |
| Optional light prep CMP locus | CMP | Optional |

### 10.3 Required outputs

When known: next topic title + educational continuity line + agreement with Mission M10 and next Home assignment.  
When unknown: honest empty state (heading · one sentence · one action) only.

### 10.4 Mandatory educational elements

Lawful node · skill/bridge continuity (not unlock theatre alone) · no heavy teaching · optional prep cue names light CMP locus only.

### 10.5 Mandatory CMP references

Only for optional light prep skim; never dump tomorrow’s chapter tonight.

### 10.6 Mandatory syllabus references

Next node must be lawful syllabus topic — never address/metadata contaminants (TB-003).

### 10.7 Educational reasoning

Educational Continuity (EP-02) closes anxiety and sets tomorrow’s Mission brief; Exam Focus keeps the bridge skill-relevant (EP-08).

### 10.8 Prohibited shortcuts

Fabricated next topics · contaminant strings · unlock copy that contradicts Twin · heavy teaching after Reflection · disagreeing with Mission handoff.

### 10.9 Premium quality

> “Next: Bayesian foundations — likelihood thinking from today’s GLM work carries forward. Tonight (optional): skim CMP headings for Bayesian notation only.”

### 10.10 Unacceptable quality

> Tomorrow = postal address string; or invented topic; or “unlock next module!” with no educational bridge.

---

## 11. Reflection authoring (AF-RF)

### 11.1 Purpose

Author topic-specific metacognitive close prompts so the student names clarity, uncertainty, and carry-forward — producing soft evidence and continuity fuel without fabricating the student’s words.

### 11.2 Required educational inputs

| Input | Source | Mandatory |
|-------|--------|-----------|
| Today’s topic + objective + concept focus | Mission / Session | Yes |
| Episode skills exercised | AF-LE set | Yes |
| Known fuzzy zones (if prior soft evidence) | Twin / prior Reflection | Preferred |

### 11.3 Required outputs

At least three student-decision prompts: what is clearer · what remains uncertain · what to carry forward — each bound to **this** topic/objective. Capture path that is student-authored (free text and/or structured choices that are still student decisions).

### 11.4 Mandatory educational elements

Topic specificity · completion required before Session educational close · soft-evidence only · no platform jargon in prompts.

### 11.5 Mandatory CMP references

Optional: “Which CMP example still feels shaky?” when examples were in today’s locus — never requiring CMP paste into the reflection field.

### 11.6 Mandatory syllabus references

Real topic title in prompt stems; never “Today’s topic.”

### 11.7 Educational reasoning

Reflection (EP-07) converts experience into metacognition and feeds tomorrow’s bridge (EP-02) without false mastery (EP-06).

### 11.8 Prohibited shortcuts

Generic reusable prompts with no substitution · system-written reflection attributed to the student · skipping Reflection while marking Session complete · engineering terms in student copy.

### 11.9 Premium quality

> “Which GLM idea is still fuzzy: mean function, link, or variance function? What will you re-check before tomorrow’s Bayesian work?”

### 11.10 Unacceptable quality

> “What is clearer about Today’s topic?” as the sole prompt for every Session in the subject.

---

## 12. Cross-artefact composition rules

1. **One story:** Mission objective, Session Overview, Episodes, Reflection, and Tomorrow Preview must narrate the same educational day (EP-10).  
2. **CMP partnership:** Kwalitec guides; CMP teaches subject depth (EP-01, EP-04).  
3. **Advertised = reachable:** Session intent stages must exist as certified Episodes (TB-008).  
4. **Generation allowed, shortcuts forbidden:** Human, template, or composition-engine output must still satisfy this Framework and EA-001 gates. Failed field resolution → block, never placeholder degrade.  
5. **AI polish only behind ports:** Wording may be polished; syllabus order, mastery, and rankings may not be invented (Study Sensei / Vision AI philosophy).  
6. **No CS1 rewrite in EA-002:** This programme defines process only. Live subject packages are rewritten only under explicit successor programmes that submit packs through this Framework.

---

## 13. Author roles

| Role | Responsibility |
|------|----------------|
| **Educational Author** | Drafts artefacts against this Framework + Style + Voice |
| **Educational Reviewer** | Substance vs EP-01–EP-10; educational fitness |
| **Tutor Reviewer** | Voice, brief test, continuity feel |
| **Curriculum Reviewer** | Syllabus lawfulness, CMP locus accuracy, contaminant quarantine |
| **Quality Gate Owner** | EA-001 checklist PASS/FAIL/HOLD |
| **Publication Approver** | Final human sign-off for package version |
| **Maintenance Owner** | Post-publish drift, CMP edition, sitting, truth audits |

One person may hold multiple roles only when independence is not required; Quality Gate PASS and Publication Approval for Version 1 commercial cohorts should not be the sole Author without a second reviewer.

---

## 14. Relationship to EA-001 gates

| Framework class | Must pass |
|-----------------|-----------|
| AF-MS | Gate MG (+ linked SS/LE or unavailable state) |
| AF-LE | Gate LE |
| AF-SS | Gate SS (implies LE + MG joint rules) |
| AF-RV | Gate RV |
| AF-TP | Gate TP |
| AF-RF | SS-04 + EP-07 (reviewed inside Gate SS) |

Certification evidence package: `EA002_CERTIFICATION_WORKFLOW.md` § Certification package.  
Publication: `EA002_PUBLICATION_WORKFLOW.md`.

---

## 15. Closing rule

> Different authors. One tutor.

If two authors following this Framework, the Tutor Voice Guide, and the Educational Style Guide produce artefacts that feel like different products, the Framework was not followed — or the guides need amendment by Board decision, not silent local exception.

**EA-002 is the permanent educational production system.**  
Content programmes execute it. They do not invent parallel processes.

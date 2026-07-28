# RP-001.3 — Terminology Register

**Programme:** RP-001 — Alpha Readiness Certification  
**Work Package:** RP-001.3 — Study Sensei Identity & Voice Certification  
**Date:** 2026-07-28  
**Status:** Observed lexicon (certification) — no renames in this package  
**Related:** `knowledge/product/px002a/TERMINOLOGY_STANDARD.md`, `knowledge/version2/PRODUCT_LANGUAGE_GUIDE.md`, `knowledge/product/ILE-001/TERMINOLOGY_STANDARD.md`, `knowledge/product/MICROCOPY_LIBRARY.md`

---

## Purpose

Register **student-facing educational terms** as they appear in Alpha-relevant code, and mark where the same concept has multiple names. This register explains identity drift; it does not choose a final rename set (out of scope for RP-001.3).

---

## 1. Narrator / brand terms

| Term | Observed role | Where it appears | Status |
|------|---------------|------------------|--------|
| **Study Sensei** | Educational mentor narrator | Decision Journal eyebrow/empty; Educational Timeline; Mission Intelligence empty/skip; Feedback Loop intro | **Canonical for Sensei surfaces** |
| **Kwalitec** | Product / company brand | Auth welcome; onboarding bodies; Help; assessment flash “helps Kwalitec support you” | **Canonical for product brand** |
| **Your learning** | EOS page shell eyebrow | Student educational view models | Neutral chrome — not Sensei |
| **Internal Alpha** | Release posture | Onboarding/Help eyebrows; badge | Release honesty |
| **the system** | Robotic agent | Runtime C panel summary “Why the system chose this” | **Rejected for Sensei voice** (surface OFF) |

**Finding:** Two narrators (Study Sensei vs Kwalitec) coexist. Students may not know they are the same guide.

---

## 2. Today’s focus (highest-impact conflict)

| Term | Authority / source | Surfaces | Notes |
|------|--------------------|----------|-------|
| **Today's Mission** | ILE-004 / Home hero / microcopy | Home eyebrow, Mission Intelligence, compose defaults, educational context | Dominant educational noun on EOS Home |
| **Today's Session** | PX-002A / product_language | CTA labels, forms, some flashes | Approved OS workflow name; **rejects** “Today's Mission” as synonym in PX standard |
| **Today's Recommendation** | Recommendation card macro | `recommendation_card.html` | Third synonym for same daily focus |
| **Mission tip** | Journal empty; Timeline narrative | Decision Journal, Educational Timeline | Softens Mission to “tip” |
| **tip** | Explanation disclosure | “Why this tip?” | Fourth register |
| **guidance** | Journal / Feedback Loop | Broad Sensei noun | Good umbrella when specific noun conflicts |
| **recommendation** | MES / commitment / ILE-005 prompts | Home, Journal reflection | Accurate for decision object; overlaps Mission |

**Certification status:** **Conflict — Fail for noun unity.** Educational meaning is mostly shared; labels are not.

**Recommended future convergence (not implemented):** Board chooses either Mission-led Sensei lexicon *or* Session-led PX lexicon, then aliases the other in Help/onboarding. Do not keep “tip” as a primary noun for authorised daily guidance.

---

## 3. Reflection family (duplicate concepts)

| Term / system | Purpose | Location | Distinct? |
|---------------|---------|----------|-----------|
| **Guided Reflection** (Home preview) | UJ/session reflection chrome | `home.html` | Presentation-only risk |
| **Commitment reflection** | Post-complete five-beat ack | Home commitment block | Educational close-loop |
| **ILE-005 student reflection** | Optional usefulness judgement | Decision Journal | Sensei calibration |
| **Session reflection** | In-session reflection step | Session routes / flashes | Workflow step |
| **Help “Reflection”** | FAQ about closing the loop | `help.html` | Explains session reflection |
| **Product Check-in** | Research survey | Alpha / research | **Not** educational reflection |

**Status:** Multiple legitimate concepts + one false affordance. Needs student-facing map (improvement — not this package).

---

## 4. Memory / archive terms

| Term | Meaning | Consistency |
|------|---------|-------------|
| **Decision Journal** | Chronology of guidance, choice, outcome | Strong; Sensei-branded |
| **Educational Timeline** | Narrative interpretation of journal | Strong; Sensei-branded |
| **History** | Accomplished sessions + stats + bridges | PX-canonical; good links to Journal/Timeline |
| **Archive** | Unified Journey nav label (flag OFF) | Alternate name for History-class surface |
| **Recent study choices** | History narrative list | Aligns with Journal story |

---

## 5. Assessment / check terms

| Term | Scope | Notes |
|------|-------|-------|
| **Quick Check** | AA session type + framing | Anxiety-safe; flag OFF in Alpha |
| **Deep / Recovery / Confidence / Revision / Readiness Check** | AA registry | Canonical AA names |
| **learning check** | `/assessment` flashes | Parallel secondary path |
| **Contextual Framing / Context Card / Educational Summary** | ILE-001C | Sensei arcs; flag OFF |

**ILE-001A forbidden (AA registry):** Exam, Test, Pass, Fail, Weak, Strong student, Poor performance (enforced in AA resources).

**Out-of-AA residual:** Help FAQ “closest to being tested on”; Exam Readiness nav/card; syllabus “exam date” — allowed as planning vocabulary but can feel like test anxiety if overused in Sensei speech.

---

## 6. Readiness / progress terms

| Term | Status |
|------|--------|
| **Exam Readiness** | PX-canonical readiness label; card eyebrow |
| **Estimated readiness (provisional)** | Microcopy library preferred framing |
| **Readiness trend** | History |
| **Journey** | Syllabus progress surface |
| **mastered / Completed topics** | History — prefer “completed” in new copy |
| **Progress** | Runtime C / Journey labels |

---

## 7. Action / control terms

| Term | Surfaces | Notes |
|------|----------|-------|
| **Start Today's Session** | Home CTA | PX |
| **Continue Mission / Start Mission** | Microcopy library | ILE |
| **I’m doing this next** | Commitment confirm | Strong agency |
| **Not today** / defer reasons | Commitment | Non-shaming |
| **Got it** | Reflection ack | Calm close |
| **Save reflection** / **Skip for now** | ILE-005 | Optional |
| **Done reflecting** / **Skip for today** | Home preview | **Non-functional** — trust risk |
| **Pause for now** | AA | Good |

---

## 8. Explainability labels (convergent — keep)

These appear consistently and should remain shared Sensei grammar:

- Why  
- Why now  
- Why this Mission / Why this recommendation?  
- Why not something else  
- Supporting evidence / Supporting evidence  
- Expected benefit / You’ll work toward  
- Confidence / Mission confidence  
- Uncertainty  
- After you finish / What happens next  
- Optional reflection  

**Divergent label to retire later:** “Why this tip?” → prefer “Why this guidance?” or “Why this Mission?”  
**Divergent label to retire if Runtime C enabled:** “Why the system chose this” → “Why this Mission” / “Why this focus”.

---

## 9. Uncertainty / confidence terms (aligned)

| Band / phrase | Sources |
|---------------|---------|
| Not enough evidence yet | Mission Intelligence; microcopy |
| Emerging confidence | Mission defaults |
| Some uncertainty remains — guidance stays provisional | compose |
| Prefer not to say | ILE-005 answer |
| Evidence insufficient / Limited / Adequate / Strong | Feedback loop labels (mostly internal review; student sees reflection, not Sensei score) |
| Inconclusive / Requires future observation | Review states |

---

## 10. Terms that must not enter Sensei speech

| Forbidden class | Examples observed / guarded |
|-----------------|----------------------------|
| Engagement theatre | streak (guarded in commitment/feedback; still in legacy analytics/settings export) |
| Engine names | Twin, Adaptive Decision Engine (translated in MES) |
| Shame / identity | weak/fail (AA); “broke your streak” (forbidden list) |
| Certainty theatre | guarantee pass; unlabelled high % confidence |
| Robotic agent | “the system chose” |

---

## 11. Register decision

| Question | Answer |
|----------|--------|
| Is terminology documented? | **Yes** |
| Is terminology unified? | **No** |
| Blocking for Alpha educational calmness? | **No** (Conditional) |
| Blocking for “one Study Sensei” identity claim? | **Yes** — narrator + daily-focus noun conflicts |

---

**End of TERMINOLOGY_REGISTER**

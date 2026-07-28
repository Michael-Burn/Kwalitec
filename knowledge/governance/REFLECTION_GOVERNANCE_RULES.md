# Reflection Governance Rules

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.3 — Reflection Architecture  
**Status:** Active — Board educational law  
**Effective:** 2026-07-28  
**Companions:** `REFLECTION_ARCHITECTURE.md`, `REFLECTION_LIFECYCLE.md`, `REFLECTION_RELATIONSHIP_MATRIX.md`  
**Constraint:** Governance only.

---

## 1. Purpose

Permanent rules governing every reflection interaction in Kwalitec.  
These rules bind future copy, product, and engineering programmes. They do not themselves change runtime behaviour.

Authority chain: Educational Constitution → Educational Philosophy → DG-001 lexicon/authority → **these rules**.

---

## 2. Foundational rules (Board mandate)

| ID | Rule |
|----|------|
| **RG-01** | Reflection must never become engagement theatre. |
| **RG-02** | Reflection must always remain optional unless educationally justified. |
| **RG-03** | Reflection must explain its educational purpose. |
| **RG-04** | Reflection must never imply surveillance. |
| **RG-05** | Reflection must support student autonomy. |
| **RG-06** | Reflection must strengthen professional judgement. |
| **RG-07** | Reflection must contribute to one coherent learning narrative. |

The following sections operationalise RG-01–RG-07 and add structural permanence rules.

---

## 3. Operational definitions

### RG-01 — No engagement theatre

**Forbidden:**

- Guilt, FOMO, streak pressure, or “keep your reflection streak” framing  
- Fake interactive controls that look like reflection decisions but save nothing (unless explicitly labelled preview/orientation)  
- Points, badges, or vanity scores for reflecting  
- Dark patterns that make skip feel like failure  

**Required:**

- Calm, professional close of practice or judgement  
- Honest affordances (preview vs capture)  

### RG-02 — Optional unless educationally justified

**Default:** Optional (skip / prefer not to say / empty note lawful).

**Educationally justified required workflow steps** (continue the Session) may exist **only** when:

1. the step is a calm close of practice (not a scored essay), and  
2. free-text and judgement questions remain optional inside that step, and  
3. Help / chrome explain why the pause exists.

Commitment acknowledgement may advance state without free-text. It must not score the learner.

**Never required:** Sensei reflection, Timeline reflection, Product Check-in, Guided preview interaction.

### RG-03 — Explain educational purpose

Every student-visible reflection surface must make clear **why** the pause or question exists, in Study Sensei voice where educational:

| Surface | Purpose line (intent) |
|---------|----------------------|
| Session reflection | Notice what practice taught; close the loop |
| Commitment reflection | Confirm completion of what you chose |
| Sensei reflection | Help the Sensei learn whether guidance was useful — optional |
| Timeline reflection | Think about how your learning story changed |
| Guided preview | Orientation only — not saved |

Product Check-in must state it is **product research**, not educational reflection.

### RG-04 — Never imply surveillance

**Forbidden:**

- Language suggesting monitoring of private thoughts  
- Silent exfiltration of reflection free-text into marketing, Twin mastery, or third parties  
- Analytics payloads that store reflection body text (metadata-only events remain lawful)  

**Required:**

- Prefer-not-to-say / skip without penalty  
- Clear boundary: research surveys ≠ Sensei memory  

### RG-05 — Support student autonomy

**Required:**

- Accept, defer, skip, and prefer-not-to-say remain first-class  
- No punishment path for declining reflection  
- Deferral of Mission must not be framed as moral failure  

**Forbidden:**

- Reflection as gate to “earn” tomorrow’s Mission  
- Forced essays as proof of diligence  

### RG-06 — Strengthen professional judgement

Reflection exists to improve **future judgement**, not to collect sentiment for its own sake.

**Lawful outcomes of reflection:**

- Student notices learning and uncertainty  
- Student evaluates whether guidance helped  
- Student interprets long-term story on Timeline  
- Sensei improves **honesty of guidance reviews** internally  

**Unlawful outcomes:**

- Reflection as mastery certificate  
- Reflection as ranking feature  
- Reflection as engagement KPI primary  

### RG-07 — One coherent learning narrative

All educational reflections must map to:

```
Experience → Evidence → Reflection → Learning → Professional judgement → Long-term mastery
```

and to the student narrative:

Mission → Commitment → Session → Session/Commitment reflection → Decision Journal → (optional) Sensei reflection → Educational Timeline → Future Mission.

**Forbidden:** Teaching disconnected reflection “apps” without the student map.  
**Required:** New reflection surfaces need Board taxonomy update before Alpha claims.

---

## 4. Structural permanence rules

| ID | Rule |
|----|------|
| **RG-08** | Decision Journal is the sole durable educational memory for Sensei-visible, memory-grade reflection. |
| **RG-09** | Study Sensei is the sole primary authority for educational reflection meaning (DG-001.2). |
| **RG-10** | Educational Feedback Loop must never re-rank recommendations from student reflection. |
| **RG-11** | Product Check-in is never educational reflection (DEP-15 / ED-18). |
| **RG-12** | Calibration is never educational reflection. |
| **RG-13** | System-authored session feedback (explainability) is not student reflection. |
| **RG-14** | No orphan reflections — every interaction named, owned, staged, stored-or-declared-non-storing, and narratively placed (`REFLECTION_LIFECYCLE.md`). |
| **RG-15** | Parallel stacks (Unified Journey, EOS, JourneyReflection domain) must not create a second student mental model; consolidate or keep residual and out of Help map until converged. |
| **RG-16** | Session-local notes must not be presented as Decision Journal persistence unless mirrored under Board-authorised wiring. |
| **RG-17** | Timeline reflection questions must cite narrative evidence and must not write new educational state. |
| **RG-18** | Reflection free-text is educationally sensitive — minimum retention, no body in analytics events, no silent Twin writes. |
| **RG-19** | The student map sentence in `REFLECTION_ARCHITECTURE.md` / vocabulary map is the canonical Help teaching until Board revises it. |
| **RG-20** | Naming: UI may say “reflection” only with qualifier or via the published map; “Daily Reflection” as Product Check-in title is deprecated educationally. |

---

## 5. Authority and voice

| Situation | Authority | Voice rule |
|-----------|-----------|------------|
| Educational reflection prompts and meaning | Study Sensei | Mentor; calm; uncertain when evidence thin |
| Product Check-in | Kwalitec / Research | Product research — never mentor memory |
| Mechanical save/load errors | System | Factual; no mentor warmth as theatre |
| Optional reflection labels | Study Sensei | Always mark optional |

Identity ≠ Authority ≠ Voice (DG-001.1 / DG-001.2) remain separate.

---

## 6. Recommendation and Twin boundaries

| Boundary | Rule |
|----------|------|
| Ranking | Reflection must never become an input that silently re-ranks Missions or tips |
| Twin mastery | Reflection free-text / usefulness answers must not declare mastery |
| Twin birth | Calibration declarations only — not reflection |
| Evidence | Lawful practice evidence may flow through constitutionally authorised paths; reflection remains soft / reflective signal when used at all |
| Explainability | If guidance changes, explain from authorised evidence — not “because you reflected poorly” |

---

## 7. Compliance checklist (for future programmes)

Before shipping or claiming a reflection change:

- [ ] Named in taxonomy or filed as non-reflection / residual  
- [ ] Owner assigned  
- [ ] Lifecycle stage mapped  
- [ ] Storage declared  
- [ ] Contribution to coherent narrative stated  
- [ ] RG-01–RG-07 satisfied in copy and UX  
- [ ] No re-rank / no surveillance implication  
- [ ] Optional posture clear (or educational justification documented)  
- [ ] Help / map impact considered (ED-03)  
- [ ] Authority is Study Sensei for educational meaning  

---

## 8. Enforcement

| Layer | Mechanism |
|-------|-----------|
| Board | These rules + DG-001.3 architecture docs |
| Product programmes | Cite RG IDs in completion reports when touching reflection |
| Copy / PX | Obey map sentence; fix RIP-001 naming collision in copy programmes |
| Engineering | Fail-open Journal mirrors; never wire Check-in → Twin/Journal; no reflection body in analytics |
| Release / Alpha | Do not claim ED-03 closed until Help student map published |

Violations are educational governance defects (same class as ED-03 / ED-18), not mere style nits.

---

## 9. Certification

These rules are sufficient to recreate reflection **policy** even if all UI disappeared: purpose, optionality, anti-theatre, anti-surveillance, autonomy, judgement, narrative unity, storage authority, and forbidden sinks.

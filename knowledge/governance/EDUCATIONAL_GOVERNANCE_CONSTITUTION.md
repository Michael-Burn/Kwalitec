# Educational Governance Constitution

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.4 — Educational Governance Constitution  
**Version:** 1.0  
**Status:** Active — Board-approved educational governance constitution  
**Effective:** 2026-07-28  
**Constraint:** Governance only — does not change product behaviour, templates, copy, recommendations, Mission Intelligence, architecture, feature flags, or curriculum.

---

## 1. Authority and scope

### 1.1 What this Constitution is

This Constitution is the **highest educational governance authority** for Kwalitec’s DG-001 corpus and for all future educational governance instruments that define:

- educational vocabulary and naming law;
- educational speech authority and narrator ownership;
- reflection system architecture and reflection governance rules;
- how those instruments interact, take precedence, are amended, and are complied with.

It consolidates Board decisions from **DG-001.1**, **DG-001.2**, and **DG-001.3** into one constitutional framework so every future educational capability can be evaluated against a single governance spine.

### 1.2 What this Constitution is not

This Constitution does **not**:

- replace Vision 2030 (product philosophy apex);
- replace or amend the Educational Constitution (`knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md`, EGI-001) — which remains the highest authority for educational *meaning, truth, and integrity*;
- replace Architecture Constitution, EVF, P-002.1, or meta-governance in `knowledge/GOVERNANCE.md`;
- invent educational algorithms, recommendations, or UI behaviour;
- close Alpha educational drift by itself — implementation programmes remain required.

### 1.3 Dual educational apex (resolved)

| Apex | Owns | Path |
|------|------|------|
| **Educational Constitution (EGI-001)** | Educational *meaning* — what learning, evidence, mastery, and integrity mean | `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` |
| **Educational Governance Constitution (this document)** | Educational *governance procedure* — how vocabulary, authority, and reflection law interact; amendment; compliance; review | `knowledge/governance/EDUCATIONAL_GOVERNANCE_CONSTITUTION.md` |

**Conflict rule:** On conflict between EGI-001 educational meaning and this Constitution’s governance procedure, **EGI-001 and Vision 2030 win**. Amend this Constitution or the subordinate DG-001 instrument — do not silently reinterpret educational meaning.

**Within educational governance instruments** (lexicon, authority model, reflection architecture, and companions), **this Constitution is supreme**. Lower documents must not contradict it.

### 1.4 Success criterion

The Board can answer:

1. Which governance document is authoritative for a given educational decision?
2. How are governance conflicts resolved?
3. How are governance decisions amended?
4. How does future implementation demonstrate compliance?
5. Can every future educational capability be evaluated against one constitutional framework?

If yes for all five — this Constitution is operating as designed.

---

## 2. Preamble

Kwalitec’s Alpha certification and RP-001 programmes showed that educational *intelligence* can be coherent while educational *governance* remains fragmented: multiple names for one concept, dual narrators, and reflection-like surfaces without one student mental model.

DG-001.1 established one vocabulary.  
DG-001.2 established one authority model.  
DG-001.3 established one reflection architecture.

This Constitution binds those decisions so they cannot drift apart, so remediation cannot invent a fourth speaker or a second reflection system, and so educational honesty remains enforceable before engagement optimisation.

**Governance precedes remediation.  
Philosophy precedes implementation.  
Evidence overrides certainty.**

---

## 3. Constitutional principles

These principles are permanent. Subordinate governance and all educational implementation must comply. Amendment requires the process in `GOVERNANCE_AMENDMENT_PROCESS.md`.

| ID | Principle | Meaning |
|----|-----------|---------|
| **CP-01** | Educational philosophy precedes implementation | No educational feature may ship against Educational Philosophy, Study Sensei Philosophy, or EGI-001 beliefs without amending the higher authority first. |
| **CP-02** | Governance precedes remediation | Copy, UX, and engineering programmes remediate *against* published governance law. They do not invent competing educational definitions mid-delivery. |
| **CP-03** | One educational concept has one canonical definition | DG-001.1 lexicon is naming law. Synonyms require explicit approval or deprecation — never silent equivalence. |
| **CP-04** | One educational interaction has one primary authority | DG-001.2: Study Sensei, Kwalitec, or System — exactly one primary speaker per interaction. |
| **CP-05** | Reflection is one coherent educational system | DG-001.3: reflection is a family in one narrative, not a bag of unrelated forms. |
| **CP-06** | Student trust takes precedence over engagement | Engagement theatre, streak pressure, and survey fatigue that undermine trust are forbidden even if metrics rise. |
| **CP-07** | Educational honesty overrides marketing convenience | Claims about mastery, readiness, memory, and guidance must match evidence and storage reality. |
| **CP-08** | Evidence overrides certainty | Where evidence is thin, speak of estimates and uncertainty — never false validated truth. |
| **CP-09** | Professional judgement is the educational objective | Guidance, reflection, and memory exist to improve long-term professional judgement — not activity volume. |
| **CP-10** | Study Sensei remains the sole educational mentor | Kwalitec is never a second tutor. System never exercises educational judgement. No fourth educational speaker is authorised. |

### 3.1 Supporting invariants (from DG-001.1–3)

| ID | Invariant | Source |
|----|-----------|--------|
| **CI-01** | Mission ≠ Session ≠ Recommendation; tip is deprecated as primary educational noun | DG-001.1-D02 |
| **CI-02** | Decision Journal is sole durable Sensei memory for memory-grade reflection | DG-001.3-D02 |
| **CI-03** | Product Check-in, Calibration, and system session feedback are not educational reflection | DG-001.3-D05 |
| **CI-04** | Reflection remains optional unless educationally justified; never scores or re-ranks | DG-001.3-D06 / RG rules |
| **CI-05** | Mandatory Study Sensei handoff exists in law (onboarding KW → SS) | DG-001.1-D01 / DG-001.2-D04 |
| **CI-06** | Identity / Authority / Voice remain separate concepts | DG-001.2 |

---

## 4. Document precedence

Authority flows **downward**. Lower documents must not contradict higher ones. On conflict within educational governance: **STOP**, document, amend the higher authority first.

```
Vision 2030
    ↓
Educational Constitution (EGI-001) — educational meaning & integrity
    ↓
Educational Governance Constitution (this document) — governance procedure apex
    ↓
Educational Philosophy · Study Sensei Philosophy
    ↓
Canonical Educational Lexicon (+ map, deprecation, style)
    ↓
Educational Authority Model (+ transitions, matrix, conflicts)
    ↓
Reflection Architecture (+ lifecycle, relationships, RG rules)
    ↓
EGI review / EVF / P-001.2 / P-001.3 / implementation standards
    ↓
Application code · templates · copy
```

Full ranked table, ownership, and conflict examples: `GOVERNANCE_HIERARCHY.md`.

### 4.1 Precedence among DG-001 packages

| Rank (within DG-001) | Package | Owns |
|----------------------|---------|------|
| Apex | DG-001.4 Constitution | Hierarchy, principles, amendment, compliance |
| 1 | DG-001.1 Lexicon | What educational words mean |
| 2 | DG-001.2 Authority | Who may speak and about what |
| 3 | DG-001.3 Reflection | How reflection exists as one system |

**Interaction rule:** Lexicon names; Authority permits speech; Reflection architectures storage and narrative; Constitution governs how those three stay coherent.

---

## 5. Governance hierarchy (summary)

See `GOVERNANCE_HIERARCHY.md` for the full hierarchy, including:

- relationship to `knowledge/GOVERNANCE.md` repository ranks;
- ownership of each educational governance instrument;
- ILE, PX, Voice Guide, Ubiquitous Language, release, and Alpha certification positions;
- conflict-resolution procedure.

---

## 6. Amendment process (summary)

Amendments to this Constitution or to DG-001.1–3 instruments follow `GOVERNANCE_AMENDMENT_PROCESS.md`:

- who may propose;
- required evidence;
- review and approval;
- versioning and supersession;
- STOP rule when higher law is implicated.

No educational implementation may treat a PR, tip copy, or local README as amending Board educational governance law.

---

## 7. Compliance process (summary)

Every educational work package that affects student-facing vocabulary, authority, reflection, recommendations framing, Mission Intelligence presentation, Help educational map, or related speech must demonstrate compliance using `GOVERNANCE_COMPLIANCE_CHECKLIST.md`.

Minimum compliance statement:

1. Affected governance documents  
2. Affected constitutional principles (CP-01–CP-10)  
3. Compliance statement (Pass / Conditional / Fail)  
4. Exceptions (if any) with rationale and expiry  
5. Explicit non-claims (what this package does *not* close)

---

## 8. Governance review process

### 8.1 When review is required

| Trigger | Review type |
|---------|-------------|
| New student-facing educational capability | Full educational governance review |
| Material copy / narrator / reflection change | Targeted review (vocabulary + authority ± reflection) |
| Claim that ED-01–ED-18 or DG-001 residuals are closed | Full review + evidence of implementation |
| Proposed amendment to DG-001 law | Amendment review per `GOVERNANCE_AMENDMENT_PROCESS.md` |
| End of major release / Alpha certification refresh | Periodic constitutional review |

### 8.2 Review dimensions

Every educational governance review must evaluate at least:

1. **Vocabulary compliance** — DG-001.1  
2. **Authority compliance** — DG-001.2  
3. **Reflection compliance** — DG-001.3 (when reflection or memory-adjacent)  
4. **Philosophy compliance** — Educational Philosophy + Study Sensei Philosophy + EGI-001  
5. **Explainability** — P-001.2 / EIP-003 as applicable  
6. **Educational honesty** — CP-07 / CP-08  
7. **Student autonomy** — optional reflection, silence, Decision Framework as applicable  
8. **Long-term mastery alignment** — CP-09; no engagement-over-trust

Checklist: `GOVERNANCE_COMPLIANCE_CHECKLIST.md`.

### 8.3 Review outcomes

| Outcome | Meaning |
|---------|---------|
| **Pass** | Compliant; may proceed (implementation still needs its own engineering gates) |
| **Conditional Pass** | Compliant as governance; named residuals block unqualified student-facing claims |
| **Fail** | Must amend design or amend higher law before proceeding |
| **Hold** | Insufficient evidence; do not claim closure |

---

## 9. Consolidated Board decisions (DG-001.1–3)

This Constitution incorporates the following Board decisions by reference. Detail remains in the named package documents.

### 9.1 Vocabulary (DG-001.1)

| ID | Decision |
|----|----------|
| DG-001.1-D01 | Study Sensei educational mentor; Kwalitec product brand |
| DG-001.1-D02 | Mission-led focus; Session ≠ Mission; tip deprecated |
| DG-001.1-D03 | Reflection family with explicit map; Check-in excluded |
| DG-001.1-D04 | First-introduction ownership for Journal / Timeline / MI |

### 9.2 Authority (DG-001.2)

| ID | Decision |
|----|----------|
| DG-001.2-D01–D03 | Three authorities only: Study Sensei / Kwalitec / System |
| DG-001.2-D04 | Mandatory onboarding handoff KW → SS |
| DG-001.2-D05 | Exactly one primary authority per interaction |
| DG-001.2-D06–D10 | History, flags, notifications, Session framing, Help teaching |

### 9.3 Reflection (DG-001.3)

| ID | Decision |
|----|----------|
| DG-001.3-D01–D08 | One reflection system; Journal sole durable memory; no orphans; non-reflections named; residuals named |

Permanent reflection rules **RG-01–RG-20** remain binding subordinate law.

---

## 10. Relationship to related corpora

| Corpus | Relationship to this Constitution |
|--------|-----------------------------------|
| Educational Philosophy | Subordinate philosophy filter; must not contradict CP-01–CP-10 |
| Study Sensei Philosophy | Subordinate mentor filter; affirms CP-10 |
| EGI-002 / EGI-003 | Educational logic registry and review standard — complementary; EGI-003 remains mandatory for educational *meaning* review; this Constitution adds DG-001 compliance |
| EVF / Educational Release Gate | Release *quality/trust* — complementary; does not amend DG-001 law |
| Product Language Guide / PX | UI naming — subordinate for educational meaning; must reconcile to lexicon (OQ-01) |
| Voice Guide (RP-001) | Voice *how* — does not reassign authority domains |
| Ubiquitous Language | Engineering UL — educational student-facing terms defer to DG-001.1 |
| Release / Alpha certification | Consume this Constitution as educational governance law; do not invent parallel vocabulary/authority/reflection apexes |
| ILE programme docs | Permanent strategic filters under Vision + EGI-001; educational naming/authority/reflection must cite DG-001 |

---

## 11. Hard prohibitions

Under this Constitution it is forbidden to:

1. Create a fourth student-facing educational speaker.  
2. Treat Kwalitec brand speech as educational mentoring.  
3. Present System status as educational judgement.  
4. Invent a second durable Sensei memory store alongside Decision Journal.  
5. Call Product Check-in, Calibration, or system feedback “educational reflection.”  
6. Close ED-01–ED-18 or DG-001 residuals by governance claim alone without implementation evidence.  
7. Amend DG-001 law via feature PR description without Board amendment process.  
8. Optimise engagement metrics in ways that violate CP-06–CP-08.

---

## 12. Companions

| Document | Role |
|----------|------|
| `GOVERNANCE_HIERARCHY.md` | Full hierarchy, ownership, precedence |
| `GOVERNANCE_AMENDMENT_PROCESS.md` | How law changes |
| `GOVERNANCE_COMPLIANCE_CHECKLIST.md` | How programmes demonstrate compliance |
| `CANONICAL_EDUCATIONAL_LEXICON.md` | Vocabulary law (DG-001.1) |
| `EDUCATIONAL_AUTHORITY_MODEL.md` | Authority law (DG-001.2) |
| `REFLECTION_ARCHITECTURE.md` | Reflection law (DG-001.3) |
| `knowledge/GOVERNANCE.md` | Repository-wide meta-governance ranks |
| `knowledge/educational/KWALITEC_EDUCATIONAL_CONSTITUTION.md` | Educational meaning apex (EGI-001) |

---

## 13. Certification statement

**DG-001.4 Educational Governance Constitution is established as Board law.**

Educational meaning remains governed by EGI-001.  
Educational vocabulary, authority, and reflection remain governed by DG-001.1–3 under this Constitution.  
Student-facing remediation remains future work.

---

**End of EDUCATIONAL_GOVERNANCE_CONSTITUTION**

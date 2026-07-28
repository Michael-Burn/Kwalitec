# Educational Authority Model

**Programme:** DG-001 — Educational Governance  
**Work Package:** DG-001.2 — Educational Authority Model  
**Version:** 1.0  
**Status:** Active — Board-approved educational authority law  
**Effective:** 2026-07-28  
**Authority:** Educational Governance (DG-001); subordinate to Vision 2030, Educational Constitution, Study Sensei Philosophy (ILE-010)  
**Upstream:** DG-001.1 Canonical Educational Lexicon; RP-001.5 Educational Drift Register (ED-01, ED-05, ED-11); RP-001 Educational Consistency Audit  
**Companions:** `AUTHORITY_TRANSITION_MAP.md`, `AUTHORITY_DECISION_MATRIX.md`, `AUTHORITY_CONFLICT_REGISTER.md`

---

## Purpose

Define the **single authoritative educational authority model** for Kwalitec.

This model establishes:

- **who speaks**
- **when they speak**
- **why they speak**
- **what authority they possess**
- **what authority they do not possess**

Its purpose is to eliminate educational ambiguity, narrator drift, competing authority, and inconsistent ownership across the product.

This document is governance law for educational *authority*. It does **not** change application behaviour, templates, copy, recommendations, Mission Intelligence, architecture, feature flags, or curriculum.

**Success criterion:** The Board can answer without ambiguity — Who is speaking? Why? What may they say? What must they never say? Every educational interaction has exactly one primary authority.

---

## Educational principle

Professional learners should always understand:

- who is teaching them,
- who is explaining recommendations,
- who remembers their learning,
- who is presenting product information,
- and when the system is merely reporting facts.

Educational authority should feel **singular, intentional, and trustworthy**.

---

## Identity, Authority, and Voice

Educational identity, authority, and voice are separate governance concepts.

| Concept | Question answered | Owned by |
|---------|-------------------|----------|
| **Identity** | Who am I interacting with? | DG-001.1 lexicon (Study Sensei / Kwalitec / neutral) |
| **Authority** | What is this entity permitted to communicate? | **This document (DG-001.2)** |
| **Voice** | How should this entity communicate? | DG-001.1 Style Guide; ILE-001C0; RP-001.3 Voice Guide |

DG-001.1 named the speakers. DG-001.2 assigns their permitted speech domains. Future voice programmes refine *how*; they must not invent a fourth educational speaker or reassign domains without Board amendment of this model.

---

## The three educational authorities

Exactly three student-facing authorities exist. No other named educational speaker is authorised.

```
Educational speech domain
├── Study Sensei — educational mentor
├── Kwalitec — product / company
└── System — pure factual layer (unnamed chrome)
```

---

### 1. Study Sensei

**Role:** Educational mentor.

**Speaks when:** The student needs educational judgement, guidance, explanation of learning decisions, memory of those decisions, reflection on guidance usefulness, uncertainty honesty, or long-term learning interpretation.

**Why:** One calm professional relationship for learning decisions — observe → guide → explain → remember → adapt.

#### Permitted responsibilities

| Domain | Examples |
|--------|----------|
| Educational judgement | What deserves attention today; when to wait |
| Recommendations | Authorised next-action suggestions and their educational meaning |
| Evidence interpretation | What evidence supports / weakens guidance |
| Uncertainty | Provisional honesty when evidence is thin |
| Encouragement | Process- and evidence-based support (not engagement theatre) |
| Educational memory | Decision Journal continuity; what we decided and why |
| Reflection | Sensei / Timeline reflection; calibration of guidance usefulness |
| Long-term learning | Educational Timeline narrative; professional development framing |
| Mission briefs | Daily Mission Intelligence composition speech |
| Mission explanations | Why this Mission? / Why this guidance? / Why this recommendation? |

#### Forbidden responsibilities

Study Sensei must **never**:

- discuss infrastructure, deployments, or outages
- discuss subscriptions, billing, or commercial offers
- discuss authentication, passwords, or account recovery
- explain feature flags, rollout state, or engineering toggles
- present operational / maintenance notices
- speak as the company on legal, privacy, or support tickets
- claim to be a human teacher, tutor, or AI chatbot product identity

**Board rule DG-001.2-D01:** Study Sensei is the sole primary authority for educational judgement, recommendations, evidence interpretation, educational memory, and guidance reflection.

---

### 2. Kwalitec

**Role:** The product and company.

**Speaks when:** The student needs product orientation, account control, legal clarity, operational honesty, or support — not educational mentoring.

**Why:** Separate the software platform from the mentor relationship so learners never confuse company speech with teaching authority.

#### Permitted responsibilities

| Domain | Examples |
|--------|----------|
| Authentication | Login, logout, session expiry product messages |
| Accounts | Profile identity fields that are product/account scoped |
| Settings | Preferences, notifications prefs, account controls |
| Billing / subscriptions | Commercial and access messages (when present) |
| Privacy / legal | Policies, consent, Alpha disclosures |
| Maintenance | Planned downtime, Alpha stage notices |
| Operational notices | Product-level status that is not educational guidance |
| Support | Help FAQ product orientation; how to get help |
| Release information | What Alpha includes; gated capability honesty |
| Product orientation | What Kwalitec *is* as a product (before Sensei handoff) |

#### Forbidden responsibilities

Kwalitec must **never**:

- make educational judgements (what to study next as mentor speech)
- interpret learning evidence as a second tutor
- replace Study Sensei on Journal, Timeline, Mission Intelligence, Feedback Loop, or Mission explanation surfaces
- recommend learning actions in mentor voice
- own Decision Journal / Educational Timeline narrative authority
- use “we prepared this Mission for you” without the Sensei handoff when speaking as product onboarding (must introduce Study Sensei)

**Board rule DG-001.2-D02:** Kwalitec is primary authority for product, account, legal, and operational speech. Kwalitec is never a second tutor.

---

### 3. System

**Role:** Pure factual layer.

**Speaks when:** The UI must report status, time, calculation results, loading, storage, or synchronisation without teaching or motivating.

**Why:** Facts must remain facts. Factual chrome must not impersonate the mentor or the brand's product promises.

#### Permitted responsibilities

| Domain | Examples |
|--------|----------|
| Timestamps | Last updated, session duration clock |
| Calculations | Displayed counts, percentages as raw figures |
| Synchronisation | Saved / syncing indicators |
| Loading | Spinners, “Loading…” |
| Processing | “Saving…”, “Processing…” |
| Storage | Local persistence confirmations that are mechanical |
| Status | HTTP/session-not-found, CSRF failure, unavailable resource |

#### Forbidden responsibilities

System must **never**:

- encourage or motivate
- recommend learning actions
- interpret evidence educationally
- teach syllabus content or learning strategy
- speak as Study Sensei
- speak as Kwalitec marketing or mentor substitute

**Attribution:** System speech is typically **unnamed** (neutral chrome). Do not brand mechanical status as Study Sensei warmth or Kwalitec mentoring.

**Board rule DG-001.2-D03:** System is the sole primary authority for pure factual / mechanical status. It has zero educational judgement authority.

---

## Primary authority rule

> **Every student-facing interaction has exactly one primary authority.**

Secondary authority is allowed only when:

1. the secondary role is explicitly bounded (e.g. System timestamps on a Sensei surface), and  
2. the secondary never overrides primary judgement or product law.

| Pattern | Allowed? |
|---------|----------|
| Study Sensei primary + System secondary (timestamp) | Yes |
| Kwalitec primary + System secondary (loading) | Yes |
| Study Sensei primary + Kwalitec secondary (Help glossary defining Sensei terms) | Yes — Kwalitec teaches vocabulary; Sensei owns educational meaning once guidance starts |
| Two primaries for the same educational judgement | **Never** |
| Unnamed “the system chose this Mission” as mentor substitute | **Never** (DEP-04 / ED-11) |

---

## Authority by speech type

| Speech type | Primary | Secondary | Forbidden |
|-------------|---------|-----------|-----------|
| Educational judgement | Study Sensei | — | Kwalitec, System |
| Recommendation explanation | Study Sensei | System (facts cited) | Kwalitec-as-mentor |
| Educational memory / reflection | Study Sensei | — | Kwalitec-as-mentor |
| Uncertainty / silence | Study Sensei | — | Fake certainty; System-as-mentor |
| Product / account / legal | Kwalitec | System | Study Sensei |
| Operational notice | Kwalitec | System | Study Sensei |
| Mechanical status | System | — | Mentor theatre; product marketing |
| Feature-flag honesty | Kwalitec | System | Study Sensei explaining engineering toggles |

---

## Relationship to decision engines

Educational *decision* authority (what Mission / recommendation cores compute) remains singular under Educational Constitution, Runtime A, and ILE programmes. This model governs *who may narrate* those decisions to the student.

| Layer | Owner | Note |
|-------|-------|------|
| Decision computation | Deterministic educational cores | Not a student-facing speaker |
| Decision narration | Study Sensei | Explains authorised decisions |
| Product framing | Kwalitec | Does not re-rank learning actions |
| Fact display | System | Does not interpret |

Narrating engines as “the system / algorithm / engine chose this” is **forbidden** (DEP-04). Sensei speech cites evidence and educational reasons, not infrastructure.

---

## Capability authority index (summary)

Full rows: `AUTHORITY_DECISION_MATRIX.md`. Transition journey: `AUTHORITY_TRANSITION_MAP.md`. Conflicts: `AUTHORITY_CONFLICT_REGISTER.md`.

| Capability | Primary | Secondary |
|------------|---------|-----------|
| Authentication | Kwalitec | System |
| Onboarding | Kwalitec → Study Sensei (handoff) | System |
| Home (educational hero) | Study Sensei | System; Kwalitec product chrome |
| Mission Intelligence | Study Sensei | System |
| Mission Commitment | Study Sensei | System |
| Mission explanations | Study Sensei | System |
| Study Session | Study Sensei (guidance) / System (workflow status) | Kwalitec product chrome |
| Decision Journal | Study Sensei | System |
| Educational Timeline | Study Sensei | System |
| Educational Feedback Loop | Study Sensei | System |
| Study Plan | Kwalitec (structure) / Study Sensei (when advising pacing educationally) | System |
| Revision | Study Sensei | System |
| History | System (stats) / Kwalitec (archive framing) | Study Sensei bridges only |
| Calibration | Kwalitec (intake product) | System; Sensei after handoff for educational meaning |
| Help | Kwalitec | Study Sensei terms via glossary |
| Profile | Kwalitec | System |
| Settings | Kwalitec | System |
| Notifications | Kwalitec (delivery) / Study Sensei (if educational content) | System |
| Success states | By domain of the completed action | System |
| Empty states | By surface owner (Sensei memory vs Kwalitec product) | System |
| Error states | System (mechanical) / Kwalitec (product recovery) | Never Sensei theatre |
| Feature-flag messaging | Kwalitec | System |

---

## How to use this model

1. Before writing or reviewing student-facing copy, identify the capability.  
2. Assign primary authority from the matrix — do not invent a speaker.  
3. If tempted to let Kwalitec interpret evidence or Sensei discuss billing, **STOP** — amend via Board process.  
4. Implementation / copy programmes remediating ED-01 must cite this model and the transition map.  
5. Identity labels come from DG-001.1; permitted speech domains come from DG-001.2; tone from the Style Guide.

---

**End of EDUCATIONAL_AUTHORITY_MODEL**

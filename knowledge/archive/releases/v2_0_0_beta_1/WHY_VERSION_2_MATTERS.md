# WHY VERSION 2 MATTERS

**Subject:** Historical importance of Kwalitec `2.0.0-beta.1`  
**Audience:** Future contributors comparing later versions to this baseline  
**Tone:** Reasoning for the archive — not a marketing brief and not a roadmap.

---

## First production deployment of the Private Beta product

Earlier tags and dogfoods proved pieces of the system. **`2.0.0-beta.1` is the first versioned identity that RC-001 deployed to production** (`https://kwalitec.onrender.com`) under feature freeze, with migrations at head `202607300005`, health checks green, and Founder + Student surfaces smoke-verified.

It is therefore the first **shipping** Private Beta baseline — not a lab branch, not a design freeze tag alone.

---

## First Founder workflow as an operational product path

At this release, a Founder can (and did, in dogfood programmes) run:

**create subject → upload sources → process → validate → preview → approve → publish → observe health / beta**

Curriculum Studio, Curriculum Health, and the Private Beta Dashboard are part of the deployed console. That Founder workflow is no longer a sketch; it is the operational spine of how curricula enter Student Runtime.

---

## First Student Runtime on certified catalogue authority

The Education Operating System (Home, Mission/Session, Journey, Tutor, Knowledge Map) runs as the **sole student runtime**. After RR-001, the active published CS1 path carries **certified-snapshot authority** (5 chapters · 15 topics · 73 LOs), not the earlier noisy FV-002 extract.

EI-002B wires certified node identity into missions, tutor grounding, knowledge map, and progress. This is the first release where “student intelligence” is explicitly bound to **certified educational artefacts**.

---

## First certified curriculum path

EI-001D introduced Generation 7 certification, Decision Ledger, and Review Packs. EQ-001 forced syllabus-first educational coherence. RR-001 made certification stick through publish and calibration.

`2.0.0-beta.1` is the first Private Beta production release that stands on that certification story end-to-end.

---

## First Private Beta

PB-001 shipped participant / feedback / observation / metrics infrastructure. RC-001 packaged invite-only beta operations (`PRIVATE_BETA_GUIDE.md`). Even though the validation report recorded an empty cohort at generation time, the **platform for Private Beta** exists and is deployed — historically marking the start of external learning evidence collection.

---

## First commercial-ready architecture shape

“Commercial-ready” here means architectural readiness for a controlled commercial learning product — not a claim of market validation or CRI/KSI thresholds.

At beta.1 the architecture exhibits:

- Layered Flask product (blueprints → services → engine/models)
- Invite-only auth and Founder authorization boundaries
- Deterministic curriculum engine + Alembic schema discipline
- Publication pipeline with certification gates
- Student EOS with explainability-oriented certified integrations
- Production deploy topology on Render + Postgres
- Version identity (`VERSION`, `/health`, changelog, release notes)

Future versions should treat this as the **architecture museum piece** against which regressions and expansions are judged.

---

## Why archive it immutably

Without a sealed baseline, “Version 2” becomes a moving target in folklore. AR-001 freezes:

- What was deployed
- What was certified
- What was knowingly incomplete
- What future releases must measure against

Contributors should not rewrite this story to flatter later work. Compare forward; do not revise the past.

---

*AR-001 release philosophy — for future contributors.*

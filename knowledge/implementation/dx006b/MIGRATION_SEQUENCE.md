# Migration Sequence

**Programme:** DX-006B  
**Status:** Binding — mandatory order  
**Release Candidate:** `RC-2026.07.29-01`  

---

## Law

```text
No later phase may begin until the previous phase is certified.
```

Certification requires every gate in `DX006B_EXECUTION_PLAN.md` §7 to PASS, including Architectural Fidelity ≥95% and Premium ≥9/10 on all dimensions.

---

## Sequence diagram

```text
┌─────────────────────────────────────────┐
│  Foundation Gate                        │
│  DX-006A Phases 1–5 in code             │
│  Tokens → L1 → L2 → L3 → Guardian       │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 1 — Founder Home                 │
│  Authority: DX-004A                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 2 — Founder Subjects             │
│  Authority: DX-004B                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 3 — Founder Workspace            │
│  Authority: DX-004C                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 4 — Student Home                 │
│  Authority: DX-005A                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 5 — Choose Exam                  │
│  Authority: DX-005B                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  Phase 6 — Study Session                │
│  Authority: DX-005C                     │
└────────────────────┬────────────────────┘
                     │ CERTIFIED
                     ▼
┌─────────────────────────────────────────┐
│  DX-006B Programme Exit                 │
│  → CQ-008 Premium Product Certification │
└─────────────────────────────────────────┘
```

---

## Why this order

| Step | Rationale |
|---|---|
| Foundation first | Pages compose catalogue components; migrating onto unfinished L0–L3 creates drift |
| Founder Home first | Establishes Current Work / Queue / Recent patterns and nav label Home |
| Subjects before Workspace | Catalogue Open → Workspace; object permanence shared helpers |
| Workspace completes Founder OS | Stages replace Review/Publish hubs; continuity from Home Resume |
| Student Home next | Parallel OS entry; Mission / Queue / Progress mirror Founder patterns |
| Choose Exam after Home | Empty Primary → Choose Exam; Begin Learning → Home handoff |
| Session last | Continue Session from Home; practice-first after discovery exists |

---

## Parallelism rules

| Allowed | Forbidden |
|---|---|
| Read next phase authority docs while current phase codes | Start next phase templates before current CERTIFIED |
| Extract shared L3 partials used by *current* phase | Invent components “for later phases” without catalogue entry |
| Fix bugs on already-certified surfaces | Reopen architecture (DX-001…005) to fit code |
| Foundation Gate work as opening of Phase 1 | Skip Foundation Gate and “token later” |

---

## Per-phase replace targets (canonical)

| Phase | Replace (canonical after cert) | Do not keep as peer |
|---|---|---|
| 1 | Founder Console Home body | Overview KPI / Quick Actions chrome |
| 2 | Subjects catalogue | Review / Publishing / Versions / Quality hubs as catalogues |
| 3 | Single Curriculum Workspace | Standalone Review page; standalone Publish page |
| 4 | `student/home.html` | Sensei / readiness / Journey Home mashup |
| 5 | Choose Exam discovery | Wizard marketing / multi-Primary commit theatre |
| 6 | Session practice surface | Coach walls / stats / gamification chrome |

Exact template paths may evolve; the **job** of each surface must remain singular per DX-002 / DX-004 / DX-005.

---

## Hand-off contracts between phases

| From → To | Contract |
|---|---|
| Foundation → P1 | Token-only styles; L1–L3 available for composition |
| P1 → P2 | Home “View all” / Create Subject targets Subjects; terminology Home |
| P2 → P3 | Row Open lands Workspace at persisted stage |
| P3 → P4 | Founder OS complete; no student dependency |
| P4 → P5 | Empty Home Primary = Choose Exam |
| P5 → P6 | Begin Learning → Home Mission; Continue Session → Session |
| P6 → Exit | Full Student OS loop: Home ↔ Choose Exam ↔ Session |

---

## Stop conditions

Halt the sequence if:

1. Architecture documents are edited to match imperfect code.  
2. A phase ships with Fidelity &lt;95% or any Premium dimension &lt;9.  
3. Legacy chrome is CSS-hidden rather than removed.  
4. A second Primary appears “for mobile.”  
5. A new dashboard / KPI pattern is introduced.

Resume only after Guard remediation (`IMPLEMENTATION_GUARD.md`).

---

*Release Candidate: RC-2026.07.29-01*

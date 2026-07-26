# Calendar Allocation

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Mapping specification from blueprint structure to calendar units  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how Planning Blueprint phases and components are mapped onto calendar time**.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `SCHEDULING_ENGINE.md`
3. `SCHEDULING_RULES.md`
4. `../planning_blueprint/PLANNING_BLUEPRINT_MODEL.md`
5. `../planning_blueprint/BLUEPRINT_PHASES.md`
6. `../planning_blueprint/BLUEPRINT_COMPONENTS.md`

This document concerns **allocation geometry** — weeks, days, sessions, study blocks, flexible capacity, and overflow. It introduces **no new educational reasoning**.

---

## 1. Purpose

A blueprint is date-independent journey structure. A timetable is that structure seated in real time.

This document records the mapping units and placement mechanics so packing code allocates *authorised structure*, rather than inventing educational shape while filling a calendar grid.

---

## 2. Calendar Unit Model

| Unit | Definition | Typical use |
|------|------------|-------------|
| **Horizon** | Contiguous capacity from timetable start reference to sitting / exam date | Bounds all placement |
| **Week** | Seven-day planning bucket used for weekly load checks against availability and BC-12 | Weekly allocation |
| **Day** | Calendar date with a capacity profile (available / reduced / zero) | Session placement host |
| **Session** | Contiguous study appointment within a day’s available window | Student-facing study slot |
| **Study block** | One placed fragment of a blueprint component inside a session (or spanning a short session) | Traceable BC-XX instance fragment |
| **Region** | Multi-day/week span reserved for a phase or protection (revision, buffer, recovery, final approach) | Protect-regions-first placement |
| **Flexible capacity** | Unallocated residual minutes inside a week/day after mandatory placements | Slip absorption; not rewrite authority |

Identifiers for implementation may vary; educational and allocation meanings above are binding.

---

## 3. Capacity Map Construction

Before placing components, build a **capacity map**:

1. **Anchor** sitting / exam date (hard end).
2. **Mark leave periods** as zero or reduced capacity (SR-17).
3. **Mark holidays** per declared unavailability (SR-18).
4. **Apply study availability** — which weekdays/times exist, and how many minutes each day offers (SR-06, SR-07).
5. **Reserve rest / freshness days** required by BC-11 / declared non-study pattern (SR-16).
6. **Compute residual usable minutes** per day and per week inside BC-12 envelopes.

The capacity map is a practical artefact. It does not diagnose the student or change blueprint missions.

### 3.1 Study availability inputs

| Input | Allocation use |
|-------|----------------|
| Weekly available hours | Caps weekly placed load |
| Study-day pattern | Restricts which days may receive sessions |
| Preferred session windows | Soft preference inside available windows |
| Preferred session length | Soft preference inside envelope-safe bands |
| Declared leave | Zero/reduced capacity regions |
| Declared holidays / unavailable dates | Zero/reduced capacity regions |

Missing availability inputs: do not invent generous free time. Prefer cautious defaults already settled upstream in capacity decisions (PD-12 family), or refuse complete timetable publication until capacity truth exists.

---

## 4. Weekly Allocation

### 4.1 Purpose of the week

The week is the primary **load-balancing unit**. It answers: *how much blueprint work lands in this week without breaching availability or intensity?*

### 4.2 Weekly allocation procedure

For each week from start toward the sitting (after protection regions are reserved — SR-20):

1. Read residual available minutes after leave/holiday/rest.
2. Cap by BC-12 weekly envelope.
3. Draw the next unplaced fragments from the active phase region’s component queue (blueprint order).
4. Assign fragments until the weekly cap is reached or the region’s work for that span is satisfied.
5. Leave unallocated residual as **flexible capacity** when intentional slack remains (buffers, preference headroom).
6. If the week’s residual cannot accept the next mandatory fragment under rules, either shift that fragment to the next lawful week inside its region, or record overflow if no lawful week remains.

### 4.3 Interleaved phases within a week

When the blueprint authorises interleaving (e.g. practice after studied topics; consolidation windows during first-pass):

- A week may contain multiple component types.
- Ordering *inside* the week still respects SR-01 / SR-02 (foundations before dependent units; practice only on studied scope).
- Interleave ratios follow blueprint / package posture — they are not invented weekly by the allocator.

### 4.4 Protected weeks

Weeks that fall inside reserved revision, final-approach, mock+recovery, or buffer regions inherit those region missions. Weekly allocation must not treat them as generic first-pass dumping grounds.

---

## 5. Day Allocation

### 5.1 Day capacity profiles

| Profile | Meaning | Placement |
|---------|---------|-----------|
| **Full available** | Declared study day with normal minutes | May host working sessions inside envelope |
| **Reduced** | Partial availability (short day, travel, light leave) | Shorter sessions only; no heroic catch-up |
| **Rest / freshness** | Planned non-study or light-only (BC-11) | No dense working load |
| **Leave** | Declared unavailable | Empty (unless ultra-light continuity explicitly authorised upstream) |
| **Holiday unavailable** | Declared closed | Treat as leave |
| **Holiday available** | Student declared study possible | Treat as available day |

### 5.2 Day load rule

Sum of study-block minutes on a day ≤ min(declared day capacity, BC-12 daily envelope remainder).

Stacking multiple dense high-demand new topics on one day beyond envelope or without blueprint-authorised recovery allowance is forbidden (aligns with C4).

---

## 6. Session Placement

### 6.1 What a session is

A **session** is a contiguous appointment the student can recognise: e.g. “Tuesday 19:00–21:00 — CM1 learning block (topics …)”.

Sessions exist to make blueprint work actionable. They do not create educational meaning beyond the blocks they contain.

### 6.2 Placement algorithm (deterministic)

For each study day with residual capacity:

1. Identify available windows on that day.
2. Choose window via SR-24 tie-breaks (preference → earlier → contiguous → earlier day already applied at higher levels).
3. Size the session to the lesser of: preferred length, remaining day capacity, remaining envelope, remaining component fragment size.
4. Attach one or more study blocks (usually one primary block per session for clarity).
5. Attach explainability stub (component + why this day/window).

### 6.3 Multi-block sessions

A session may contain a short secondary block (e.g. light consolidation after a learning block) **only** when the blueprint authorises that interleave and envelopes allow. Do not invent mixed missions for packing density.

### 6.4 Empty available days

Leaving an available day empty is lawful when:

- weekly envelope is already met;
- rest pattern requires it;
- flexible capacity / buffer policy prefers slack;
- next component belongs to a later protected region not yet open.

Filling every empty day by default is not a goal.

---

## 7. Study Blocks

### 7.1 Block as blueprint fragment

Each **study block** is a dated fragment of a blueprint component instance:

| Field | Requirement |
|-------|-------------|
| Blueprint component ID | BC-XX (+ instance identity) |
| Phase home | BP-XX |
| Educational scope | Topics/units already authorised by the component |
| Duration | Minutes ≤ remaining envelopes |
| Calendar coordinates | Week, day, session window |
| Trace links | Blueprint → package → strategy/profile as inherited |

### 7.2 Splitting

Large components split across days/sessions under SR-22:

- Preserve internal order of topics/units.
- Do not place later prerequisite-dependent units earlier than foundations across the split.
- Keep split fragments recognisable as one educational component for explainability (“continued learning block”).

### 7.3 Component-specific placement notes

| Component | Calendar placement notes |
|-----------|--------------------------|
| BC-01 Learning | Place in BP-01 region; sequential; never into protected revision by default |
| BC-02 Practice | After studied scope; density from blueprint; may interleave in same week as related learning |
| BC-03 Consolidation | Interleaved windows during first-pass per blueprint — not premature full revision |
| BC-04 Revision | Only inside protected revision (and authorised final-approach subset) |
| BC-05 Mock | Inside authorised mock window; pair recovery capacity when blueprint requires |
| BC-06 Recovery | Lighter/zero working load cells after disruption or mocks |
| BC-07 Buffer | Reserved unallocated or lightly held capacity until slip consumes it |
| BC-08 / BC-09 | Place near educational events they mark; dates serve legibility, not mastery fiat |
| BC-10 Transition | Visible calendar marker at PD-04 / mission-change boundary |
| BC-11 Rest | Explicit empty or light days |
| BC-12 Envelope | Constraint on other blocks — not a student-facing “task” |
| BC-13 / BC-14 | Colour placement caution / completable pacing — do not invent new cells beyond blueprint |

---

## 8. Phase → Calendar Region Mapping

| Phase | Typical calendar geometry |
|-------|---------------------------|
| BP-00 Intake | Usually pre-timetable; published timetable assumes intake complete |
| BP-01 Foundation & Knowledge Building | Early-to-mid horizon residual after protections reserved; sequential learning weeks |
| BP-02 Reinforcement & Practice | Interleaved or concentrated weeks per blueprint practice posture |
| BP-03 Consolidation Windows | Interleaved light returns inside/beside BP-01 weeks |
| BP-04 Protected Revision | Reserved late-horizon region sized by blueprint reservation — placed first among protections |
| BP-05 Mock Examinations | Discrete window(s) adjacent to revision / before final approach, with recovery |
| BP-06 Final Preparation | Terminal region before sitting; freeze expansion; freshness capacity |
| BP-07 Recovery / Replan | Inserted spans when authorised — often consuming buffer or replacing dense weeks temporarily |

Phase meanings remain those of MS005. Calendar geometry realises them; it does not redefine them.

---

## 9. Flexible Capacity

### 9.1 Definition

**Flexible capacity** is residual available time inside a week or day that is intentionally unallocated after placing mandatory region work and honouring envelopes.

### 9.2 Lawful uses

- Absorb small session slips without touching protected revision
- Honour preference moves (Tuesday → Wednesday) inside the same educational component queue
- Provide breathing room consistent with sustainability
- Host optional light review only if the blueprint already authorised such lightness in that span

### 9.3 Unlawful uses

- Invent new educational missions to “use the gap”
- Quietly extend first-pass into the revision region because flexible minutes appeared there
- Justify exceeding BC-12 because flexible capacity “looked free”
- Hide infeasibility by labelling impossible work as flexible

Flexible capacity is packing slack under blueprint law — not a second planning engine.

---

## 10. Overflow Handling

### 10.1 What overflow is

**Overflow** exists when one or more blueprint components (or fragments) cannot be placed inside the horizon under SR-01…SR-24 and scheduling constraints.

### 10.2 Lawful overflow responses (allocation layer)

1. **Record** which components remain unplaced and why (capacity, protection conflict, leave collision).
2. **Do not** steal protected revision, delete buffers, or breach envelopes to clear the queue.
3. **Offer** only blueprint-authorised slack consumption already structured (e.g. remaining BC-07) if still unused and educationally lawful for this slip type.
4. **Escalate** upstream for re-package / re-blueprint / triage when overflow persists.

### 10.3 Overflow vs infeasibility theatre

Publishing a “complete” timetable while material mandatory components remain in overflow is allocation-invalid.

A triage timetable may be published when the blueprint itself is triage-reduced — still honest about what was placed and what was deferred or removed upstream.

---

## 11. Worked Allocation Sketch (Non-normative)

Illustrative only — not a numeric optimiser:

```
1. Capacity map: Mon–Thu evenings available; Fri rest; weekends light;
   leave week 12; sitting date S.
2. Reserve: last N weeks → BP-04 revision region (sized by blueprint);
            final days → BP-06; mock weekend + recovery → BP-05/BC-06;
            buffer pockets → BC-07.
3. Fill residual earlier weeks with BC-01 queue in order;
   weave BC-02/BC-03 per blueprint interleave.
4. Split long learning components across Mon/Tue sessions.
5. Leave some Thursday minutes flexible in early weeks.
6. If BC-01 queue remains when revision region begins → overflow / escalate;
   do not borrow revision weeks by default.
```

---

## 12. Cross References

- `SCHEDULING_RULES.md` — SR-01…SR-27
- `SCHEDULING_CONSTRAINTS.md` — hard constraint catalogue
- `RESCHEDULING_POLICY.md` — moving blocks after divergence
- `SCHEDULING_EXPLAINABILITY.md` — explaining placement geometry
- `../planning_blueprint/BLUEPRINT_PHASES.md` — phase missions
- `../planning_blueprint/BLUEPRINT_COMPONENTS.md` — placeable blocks

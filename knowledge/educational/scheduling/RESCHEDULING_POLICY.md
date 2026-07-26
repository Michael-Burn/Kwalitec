# Rescheduling Policy

**Programme:** VI — Master Planner  
**Milestone:** MS006 — Scheduling Engine Specification  
**Classification:** Adaptation policy for Study Timetables when reality diverges  
**Status:** APPROVED — governing  
**Version:** 1.0  
**Date:** 2026-07-25  

---

## Authority

This document defines **how a Study Timetable adapts** when lived reality diverges from the allocated plan — while preserving the educational intent of the Planning Blueprint wherever possible.

Subordinate to:

1. `KWALITEC_EDUCATIONAL_CONSTITUTION.md`
2. `SCHEDULING_ENGINE.md`
3. `SCHEDULING_RULES.md` (especially SR-25…SR-27)
4. `SCHEDULING_CONSTRAINTS.md`
5. `../planning_blueprint/BLUEPRINT_PROGRESSION.md`
6. `../planning_engine/DECISION_CONFLICT_RESOLUTION.md`
7. `../planning_engine/DECISION_PIPELINE.md` (PD-16 / re-run triggers)

Rescheduling is **allocation adaptation**. It introduces **no new educational reasoning**. When educational envelopes must change, escalate upstream.

> **Move placement. Preserve mission.  
> Escalate when mission itself must change.**

---

## 1. Purpose

Real candidates miss sessions, fall ill, take unexpected leave, find extra evenings, or discover that declared availability was optimistic.

An expert IFoA tutor does not pretend the old diary still holds, and does not invent a new educational philosophy to “catch up.” The tutor:

1. tells the truth about what changed;
2. uses reserved buffers and recovery capacity first;
3. shifts remaining authorised work later (or earlier, for extra time) without breaking order or protections;
4. refuses punishment compression;
5. returns to planning decisions when the blueprint no longer fits.

This policy records that posture for algorithms.

---

## 2. Governing Principles

1. **Preserve blueprint intent.** Phase order, component meanings, sequencing, revision protection, and intensity envelopes remain law unless upstream changes them.
2. **Capacity truth first.** Update the capacity map before moving cells.
3. **Buffer before heroics.** Consume BC-07 / authorised PD-16 options before breaching envelopes.
4. **Recovery before punishment.** After illness or dense shock, prefer BC-06 lighter load over impossible make-up.
5. **Deterministic moves.** Same divergence event + same remaining blueprint + same capacity map → same reschedule posture.
6. **Explain every material change.** Students must understand why the timetable moved (`SCHEDULING_EXPLAINABILITY.md`).
7. **Escalate, don’t invent.** If remaining work cannot fit under constraints, stop silent adaptation and request re-package / re-blueprint.
8. **Continuity.** Moving or replacing timetable cells must not erase learner history (SC-23).
9. **No new educational reasoning.** Extra time does not authorise inventing new first-pass ambition beyond the blueprint; missed time does not authorise inventing weakness theatre.

---

## 3. Divergence Event Catalogue

Identifiers (RD-XX) name observed practical events. They are not educational diagnoses.

| ID | Event | Typical capacity effect |
|----|-------|-------------------------|
| RD-01 | Missed session(s) | Planned minutes unused; backlog of placed fragments becomes unplaced residual |
| RD-02 | Missed week / adherence collapse | Large capacity loss; may threaten envelopes and feasibility |
| RD-03 | Reduced availability (ongoing) | Capacity map shrinks; weekly caps fall |
| RD-04 | Extra study time (one-off) | Temporary surplus minutes |
| RD-05 | Extra study time (ongoing) | Capacity map expands |
| RD-06 | Unexpected leave | New zero/reduced region |
| RD-07 | Illness | Leave-like capacity loss; recovery expectation |
| RD-08 | Holiday newly recognised | Capacity map correction |
| RD-09 | Sitting / exam date change | Horizon re-anchor — usually requires upstream replan |
| RD-10 | Blueprint superseded | New blueprint published upstream — full re-allocation |

---

## 4. Rescheduling Pipeline

For any material divergence:

```
1. DETECT   — record the divergence event (RD-XX) with dates/minutes affected
2. UPDATE   — rebuild capacity map (availability, leave, holidays, rest)
3. CLASSIFY — local adaptation vs upstream escalation (see §5)
4. ADAPT    — apply lawful move / consume buffer / insert recovery cells
5. VALIDATE — re-check SC-01…SC-25 and SR-01…SR-27
6. EXPLAIN  — attach change explainability
7. PUBLISH  — replace affected timetable region; preserve history
```

Do not skip VALIDATE. A “helpful” move that steals revision is invalid.

---

## 5. Local Adaptation vs Upstream Escalation

### 5.1 Local adaptation (stays in Scheduling Engine)

Lawful when **all** hold:

- The Planning Blueprint remains the correct educational structure.
- Remaining work can still fit inside residual capacity after using authorised buffer/recovery options.
- Order, prerequisites, revision protection, and intensity envelopes can be preserved.
- Feasibility posture does not flip from “fits” to hidden impossibility.

Examples: move two missed evening sessions into buffer pockets next week; shorten sessions after reduced availability while keeping the same component queue; place an unexpected free Saturday session onto the next authorised learning fragment.

### 5.2 Upstream escalation (Decision Engine / Blueprint rebuild)

Required when **any** hold:

- Protected revision would need to be consumed to clear first-pass backlog (unless an upstream trade-off was already decided and disclosed).
- Intensity envelopes must be breached to finish.
- Feasibility is threatened or broken (PD-13 territory).
- Sitting date changes (RD-09).
- Strategy / profile / package decisions are obsolete (blueprint superseded — RD-10).
- Chronic adherence collapse needs recovery *educational* posture change, not endless cell shuffling.
- Overflow persists after lawful buffer use.

Escalation outputs a new package and/or blueprint; Scheduling then **re-allocates** — it does not invent the educational compromise itself.

---

## 6. Policies by Event

### 6.1 Missed sessions (RD-01)

| Step | Action |
|------|--------|
| 1 | Mark missed session cells as not completed; do not erase the educational component identity |
| 2 | Return unfinished fragments to the unplaced queue in original order |
| 3 | Prefer placement into flexible capacity and BC-07 buffer pockets inside the same phase region |
| 4 | Shift later non-protected work later within the region if needed |
| 5 | Do not accelerate by exceeding BC-12 or by stealing BP-04 |
| 6 | If backlog cannot be re-placed lawfully → escalate |

**Forbidden:** punishment double-sessions that breach envelopes; silent relabel of missed first-pass as “revision.”

### 6.2 Missed week / adherence collapse (RD-02)

| Step | Action |
|------|--------|
| 1 | Update capacity truth; pause dense placement if burnout signals warrant lighter near-term load (using blueprint BC-06 / rest capacity — not inventing diagnosis) |
| 2 | Consume buffer proportionally to the shock |
| 3 | Re-pack remaining region work into residual weeks under protect-regions-first |
| 4 | If revision region start would be breached by first-pass spill → escalate (triage / intensity / sitting counsel upstream) |

Aligns with blueprint progression pause / recovery insertion and PD-16 options — allocator executes calendar consequences of options already authorised; it does not invent a new option catalogue.

### 6.3 Reduced availability (RD-03)

| Step | Action |
|------|--------|
| 1 | Rebuild capacity map with lower weekly/daily caps |
| 2 | Shrink session lengths and/or session count inside envelopes |
| 3 | Preserve component order; accept later completion dates inside regions |
| 4 | If mandatory regions no longer fit → escalate |

Do not keep the old ambitious session pattern on fewer days by overloading remaining evenings.

### 6.4 Extra study time — one-off (RD-04)

| Step | Action |
|------|--------|
| 1 | Confirm the extra window is truly available and envelope-safe |
| 2 | Pull the **next** authorised unplaced fragment (or bring forward a fragment already queued for soon) |
| 3 | Optionally reduce near-term pressure by leaving later flexible capacity |
| 4 | Do **not** invent additional first-pass topics beyond the blueprint queue |
| 5 | Do **not** invade rest days required by BC-11 unless the student explicitly converts rest and envelopes still hold |

Extra time is surplus packing capacity — not a licence for educational expansion.

### 6.5 Extra study time — ongoing (RD-05)

| Step | Action |
|------|--------|
| 1 | Rebuild capacity map |
| 2 | Re-pack with higher weekly caps still inside BC-12 (envelope may already assume max sustainable — do not exceed it merely because more hours exist) |
| 3 | May finish regions earlier; must still honour revision start intent and final freeze |
| 4 | If sustained surplus suggests intensity or ambition could lawfully rise, **escalate upstream** — do not silently widen educational ambition in packing |

### 6.6 Unexpected leave (RD-06)

| Step | Action |
|------|--------|
| 1 | Punch a zero/reduced region into the capacity map |
| 2 | Evict any previously placed sessions from that span back to the queue |
| 3 | Re-place using buffer / later residual capacity |
| 4 | Escalate if leave duration breaks feasibility |

### 6.7 Illness (RD-07)

| Step | Action |
|------|--------|
| 1 | Treat as leave for the illness window |
| 2 | Prefer inserting BC-06 recovery cells on return before restoring full envelope intensity |
| 3 | Use buffer for displaced work |
| 4 | Forbid immediate punishment catch-up as default |
| 5 | Escalate if prolonged illness breaks remaining horizon maths |

### 6.8 Holiday newly recognised (RD-08)

Treat as capacity-map correction akin to leave; re-place displaced sessions under the same rules as RD-06.

### 6.9 Sitting / exam date change (RD-09)

**Local adaptation is insufficient.** Horizon maths, revision reservation, and feasibility must be recomputed upstream. Scheduling waits for a new blueprint (or explicit package confirming structure still holds), then re-allocates from scratch against the new horizon.

### 6.10 Blueprint superseded (RD-10)

Discard placement derived from the old blueprint (preserve learner history). Allocate the new blueprint cleanly. Do not merge conflicting phase missions cell-by-cell.

---

## 7. Buffer Utilisation

### 7.1 Purpose on the calendar

BC-07 appears as reserved spare capacity so slip has somewhere lawful to go.

### 7.2 Consumption order

When absorbing divergence:

1. Flexible capacity inside the current week/region  
2. BC-07 buffer pockets designated for slip  
3. Blueprint-authorised deferral of non-critical consolidation (only if PD-16 / blueprint already allows shrinking BC-03)  
4. Escalate — do not proceed to envelope breach or revision theft  

### 7.3 Partial consumption

Buffers may be partially used. Remaining buffer stays visible. Exhausting buffer without escalation when overflow remains is incomplete handling — either the queue fits after consumption or escalation is required.

### 7.4 Refill

Buffers do not magically refill because a good week occurred, unless upstream replan restores buffer policy. Local rescheduling must not invent new buffer educational policy.

---

## 8. Recovery Insertion on the Calendar

### 8.1 When to insert recovery cells

Insert or emphasise BC-06 / lighter days when:

- the blueprint already pairs recovery after mocks;
- illness / leave return requires lighter re-entry;
- divergence handling selects an authorised PD-16 recovery option already reflected in blueprint structure;
- intensity was at envelope ceiling and adherence collapsed.

### 8.2 What recovery cells look like

- Reduced minutes vs normal working band  
- Lighter component types only if blueprint allows (e.g. light consolidation — not new dense first-pass)  
- Explicit empty rest days when BC-11 warrants  

### 8.3 Re-entry

Restore normal BC-01…BC-05 placement only when capacity and envelopes again support it, sequencing remains honest, and revision protection remains intact. If capacity truth changed materially, prefer upstream re-check.

---

## 9. Preservation Invariants During Reschedule

| Invariant | Must remain true |
|-----------|------------------|
| **Order** | Component queue order and prerequisites |
| **Revision region** | Not consumed by default for first-pass spill |
| **Final freeze** | Not reopened for unbounded expansion |
| **Envelope** | BC-12 respected |
| **Feasibility speech** | No new complete theatre over broken fit |
| **History** | Progress/evidence not erased by cell moves |
| **Mode authority** | Learning Mode not silently hijacked |

Violation of any invariant → invalid reschedule or mandatory escalation.

---

## 10. Worked Sketches (Non-normative)

### Missed two evening sessions

```
Missed: Tue/Wed learning fragments
→ Return fragments to queue
→ Place into Thursday flexible slot + weekend buffer pocket
→ Later weeks shift by one fragment each
→ Revision region untouched
→ Explain: “We used spare capacity so your syllabus order stays intact.”
```

### Two-week illness near mid-horizon

```
Illness leave punched into map
→ Evict displaced sessions
→ On return: one recovery week (lighter load)
→ Consume buffer for displaced learning
→ If revision start would slip into first-pass theft → escalate for triage/replan
→ Explain: “Recovery first; we will not punish-pace the illness weeks.”
```

### Ongoing extra weeknight

```
Capacity map +1 evening
→ Repack: same blueprint queue, earlier completion of BP-01 region possible
→ Keep revision region size/intent
→ Do not add topics the blueprint never authorised
→ If student wants higher ambition → upstream decision, not packing invention
```

---

## 11. Cross References

- `SCHEDULING_ENGINE.md` — allocation-only constitution
- `SCHEDULING_RULES.md` — SR-25…SR-27
- `CALENDAR_ALLOCATION.md` — capacity map, flexible capacity, overflow
- `SCHEDULING_CONSTRAINTS.md` — SC publication gate
- `SCHEDULING_EXPLAINABILITY.md` — explaining timetable changes
- `../planning_blueprint/BLUEPRINT_PROGRESSION.md` — pause / recovery educational criteria
- `../planning_engine/DECISION_CONFLICT_RESOLUTION.md` — life and adherence conflicts upstream

# Twin Stack Quarantine

**Programme:** EP-002 Student Intelligence Surface  
**Milestone:** EP-002.1 — Consumer-Chain Observability & Twin Quarantine  
**Addresses:** EP-001.5 **TD-ARCH-01** (operator confusion across Twin stacks)  
**Date:** 2026-07-26  
**Status:** Binding operator narrative for Runtime A

---

## Purpose

Kwalitec has several artefacts named “Twin”. Only one path is the Runtime A product substrate for EP-001 / EP-002. This note quarantines the others so operators and engineers do not promote, merge, or extend the wrong stack.

---

## Authority matrix (speakable)

| Stack | Location | Role | Authoritative for Runtime A student product? | Extend? |
|---|---|---|---|---|
| **MS-004 Foundation + EP-001.1** | `app/infrastructure/adapters/digital_twin/` (`foundation.py`, facets, snapshot, shadow, authority) | Canonical learner-state **read model** for EP-001.2–4 `build_*` | **Yes** | **Yes — extend this** |
| **ExperienceTwinAdapter** | `app/infrastructure/adapters/student_twin/experience_adapter.py` | Default Experience `StudentTwinPort` UX adapter | Default UX until Authority soak | Keep; do not fork a fourth stack |
| **Foundation Authority port** | `digital_twin/authority.py` | Optional Experience TwinPort serving Foundation when `KWALITEC_DIGITAL_TWIN_AUTHORITY` ON | Gated; requires Twin ON | Extend only via soak evidence (EP-002.3 complete for non-prod) |
| **Epic Twin** | `app/domain/twin/` | Constitutional aggregate **vocabulary** / domain shapes | **No** — reference only | Do not promote to production writer |
| **V2 Student Twin** | `app/domain/student_twin/`, `app/application/student_twin/` | Parallel bounded context (historical / experimental) | **No** | Do **not** extend for EP-002; eventual docs-only quarantine |
| **EOS Educational Digital Twin** | `src/domain/education/digital_twin/` | Education OS stack | **No** for Flask Runtime A | Keep isolated; no merge into MS-004 |

---

## Which implementation is which

### Authoritative (Runtime A product path)

**MS-004 Student Digital Twin (T0–T6) + EP-001.1 Foundation** is the only Twin substrate EP-001.2–4 and EP-002 may consume.

- Flag: `KWALITEC_DIGITAL_TWIN` → `ENABLE_DIGITAL_TWIN` (default **OFF**)
- Authority cutover (Experience TwinPort): `KWALITEC_DIGITAL_TWIN_AUTHORITY` (default **OFF**, requires Twin ON)
- Shadow validation and Adaptive TwinInput are **bundled under Twin ON** (no separate env flags in code)

### Historical / reference

- **Epic Twin** (`app/domain/twin`) — domain vocabulary for facet names and constitutional aggregate language. Not a production educational writer.
- Architecture vision docs under `STUDENT_DIGITAL_TWIN.md` — reinterpreted under MS-004; not a second implementation.

### Experimental / non-authority

- **V2 student_twin** packages — parallel context; must not become SoT for planner / readiness / insight.
- **EOS digital twin** — Education OS only; never Flask Runtime A source of truth.

### Currently used in production defaults

| Concern | Production default |
|---|---|
| Learner-state Foundation / `build_*` | Twin **OFF** → `build_*` return `None`; legacy HTTP APIs authoritative |
| Experience TwinPort | `ExperienceTwinAdapter` (Authority **OFF**) |
| Adaptive TwinInput attachment | Wired only when Twin ON; fail-open when absent |

### Which should be extended

| Extend | Do not extend for EP-002 |
|---|---|
| `digital_twin/` Foundation + MS-004 | Epic Twin as a new runtime writer |
| Runtime A `PlanningService` / `ReadinessService` / `RecommendationService` hosts | V2 `student_twin` engine |
| Existing `consumer_chain` observability | EOS twin merged into Flask |
| Experience Authority soak path | A fourth Twin package “for UX” |

---

## Operator rules (binding)

1. **Never introduce a fourth Twin stack** for EP-002 surface cutover.  
2. When docs say “Twin,” assume **MS-004 + Foundation** unless they explicitly name Epic / V2 / EOS.  
3. Fail-open remains: Twin OFF restores legacy Runtime A behaviour immediately.  
4. Authority ON is **not** implied by Twin ON.  
5. EP-002 does **not** declare MS-004 Twin Ready (T7).

---

## Related artefacts

- `knowledge/architecture/STUDENT_DIGITAL_TWIN_ARCHITECTURE.md`
- `knowledge/architecture/ep001_5_architectural_integration_review/PARALLEL_PATH_ANALYSIS.md`
- `knowledge/architecture/ep002_student_intelligence_surface/PROGRAMME_BRIEF.md`
- `knowledge/architecture/ep002_1_consumer_chain_observability/`
- `knowledge/architecture/ep002_9_programme_exit_certification/` — programme exit; Twin Ready (T7) still **not** declared

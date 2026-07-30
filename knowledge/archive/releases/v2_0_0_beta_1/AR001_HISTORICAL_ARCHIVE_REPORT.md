# AR-001 — Historical Archive Report

**Programme:** AR-001 · Historical Release Archive  
**Subject:** Kwalitec Version `2.0.0-beta.1`  
**Date:** 2026-07-30  
**Constraint:** No features · No architecture · No UI · No educational reasoning · No refactoring · No deployment changes · No source-code modification  

---

## Summary

AR-001 created a permanent, immutable historical archive for the first production release that entered Private Beta. The archive lives at `knowledge/archive/releases/v2_0_0_beta_1/` and preserves release identity (manifest + certificate), product timeline, architecture snapshot, indexed programme reports (EI-001/002, EQ-001, RR-001, UX-001, PB-001, RC-001), version statistics, known limitations, release philosophy, visual catalogue, and a V3 comparison baseline. Application source, database schema, and deployment configuration were **not** modified by this programme.

---

## FINAL DECISION

# VERSION 2.0.0-BETA.1
# PERMANENTLY ARCHIVED

**Evidence:** Complete folder structure; all eleven workstreams delivered; primary reports copied and indexed; release identity pinned to git tag `v2.0.0-beta.1`, deploy commit `7302bb7…`, Alembic `202607300005`, and URL `https://kwalitec.onrender.com`; quality gates below all pass.

---

## Archive contents

```
knowledge/archive/releases/v2_0_0_beta_1/
├── README.md
├── RELEASE_CERTIFICATE.md
├── WHY_VERSION_2_MATTERS.md
├── PRODUCT_TIMELINE.md
├── KNOWN_LIMITATIONS.md
├── BASELINE_FOR_V3.md
├── AR001_HISTORICAL_ARCHIVE_REPORT.md
├── release/          # manifest, VERSION, changelog, notes, guides, pins, render.yaml
├── reports/          # EI/EQ/RR/UX/PB/RC copies + REPORT_INDEX.md
├── screenshots/      # visual catalogue + indexes (binaries referenced, not duplicated)
├── architecture/     # ARCHITECTURE_AT_V2.md + ARCHITECTURE.md copy
├── metrics/          # VERSION_STATISTICS.md
└── documentation/    # PROJECT_CONTEXT, PRODUCT_BLUEPRINT, README copies
```

---

## Files generated

### New narrative / index documents

| File |
|---|
| `knowledge/archive/releases/v2_0_0_beta_1/README.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/RELEASE_CERTIFICATE.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/WHY_VERSION_2_MATTERS.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/PRODUCT_TIMELINE.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/KNOWN_LIMITATIONS.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/BASELINE_FOR_V3.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/AR001_HISTORICAL_ARCHIVE_REPORT.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/release/RELEASE_MANIFEST.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/architecture/ARCHITECTURE_AT_V2.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/reports/REPORT_INDEX.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/metrics/VERSION_STATISTICS.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/screenshots/VISUAL_ARCHIVE.md` |
| `knowledge/archive/releases/v2_0_0_beta_1/screenshots/SOURCE_COLLECTIONS.md` |
| `knowledge/archive/releases/README.md` |

### Copied artefacts (release-bound)

- Release: `VERSION`, `CHANGELOG.md`, `RELEASE_NOTES.md`, `PRIVATE_BETA_GUIDE.md`, `FOUNDER_DEPLOYMENT_GUIDE.md`, `requirements.txt`, `render.yaml`, `pyproject.toml`, SHA/revision pin files  
- Architecture: `ARCHITECTURE.md`  
- Documentation: `PROJECT_CONTEXT.md`, `PRODUCT_BLUEPRINT.md`, `README.md`  
- Reports: EI-001A–D, EI-002A–B, EQ-001, RR-001, UX-001, PB-001 (×2), RC-001, supporting PL-001A + FV-002  
- Screenshots index: `RC001_PRODUCT_SCREENSHOT_INDEX.md`

---

## Historical significance

This archive seals the moment Kwalitec became a **versioned, production-deployed Private Beta product** with:

- Certified curriculum path (EI / EQ / RR lineage)  
- Founder Console operational workflow  
- Student EOS on certified catalogue authority  
- Private Beta instrumentation  
- Explicit known limitations and empty-cohort honesty (PB-001)

Future development should compare against this museum snapshot rather than rewriting it.

---

## Completeness review

| Workstream | Deliverable | Status |
|---|---|---|
| 1 Release archive folder | `knowledge/archive/releases/v2_0_0_beta_1/{release,reports,screenshots,architecture,metrics,documentation}/` | **Complete** |
| 2 Historical manifest | `release/RELEASE_MANIFEST.md` | **Complete** |
| 3 Historical timeline | `PRODUCT_TIMELINE.md` | **Complete** |
| 4 Architecture snapshot | `architecture/ARCHITECTURE_AT_V2.md` | **Complete** |
| 5 Evidence preservation | Report copies + `reports/REPORT_INDEX.md` | **Complete** |
| 6 Release statistics | `metrics/VERSION_STATISTICS.md` | **Complete** |
| 7 Known limitations | `KNOWN_LIMITATIONS.md` | **Complete** |
| 8 Release philosophy | `WHY_VERSION_2_MATTERS.md` | **Complete** |
| 9 Visual archive | `screenshots/VISUAL_ARCHIVE.md` (+ indexes) | **Complete** (4 screens flagged for optional post-deploy manual capture) |
| 10 Future comparison baseline | `BASELINE_FOR_V3.md` | **Complete** |
| 11 Release certificate | `RELEASE_CERTIFICATE.md` | **Complete** |
| Output report | This document | **Complete** |

### Quality gates

| Gate | Result |
|---|---|
| No source code modified (by AR-001) | **PASS** — archive under `knowledge/archive/` only |
| No database changes | **PASS** |
| No deployment changes | **PASS** |
| Archive complete | **PASS** |
| Reports indexed | **PASS** |
| Version documented | **PASS** |
| Architecture preserved | **PASS** |
| Historical record complete | **PASS** |

---

## Recommendations

1. **Do not mutate** identity fields in `RELEASE_CERTIFICATE.md` / `RELEASE_MANIFEST.md` after seal; add errata only via new dated notes if facts were wrong.  
2. Optionally complete the four **manual production screenshots** listed in `screenshots/VISUAL_ARCHIVE.md` (Tutor, Knowledge Map, Curriculum Health, Private Beta Dashboard) into `screenshots/manual_production/` — enhancement, not a blocker for archival seal.  
3. When tagging a later major release, create a sibling folder under `knowledge/archive/releases/` and run the `BASELINE_FOR_V3.md` comparison protocol.  
4. Keep living engineering reports under `knowledge/engineering/`; treat copies here as the release-bound set.

---

## Migration Impact

**None.**

## Architecture Compliance

Documentation-only. Application layering and curriculum V1/V2 invariants untouched. Traversal/import compatibility preserved (N/A — no code change).

## Technical Debt

None introduced. Archive honestly records pre-existing debt in `KNOWN_LIMITATIONS.md`.

## Known Limitations (of this archive programme)

- Binary screenshot libraries were catalogued by path rather than duplicated (intentional).  
- Four UX-001/PB-001 surfaces lack dedicated production captures in-archive (checklist provided).  
- Repository LOC/statistics measured on the archival working tree contemporaneous with AR-001; tag commit `f6245f4` is one docs commit after deploy tip `7302bb7` — both documented in the manifest.

---

*AR-001 preserves history. It does not change it.*

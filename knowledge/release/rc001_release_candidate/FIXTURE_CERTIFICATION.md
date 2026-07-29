# FIXTURE_CERTIFICATION.md

**Programme:** RC-001  
**Release Candidate ID:** `RC-2026.07.29-01`  
**Fixture pack:** EV-001 CS1V official pack (approved)

---

## Approved fixture set

Canonical copies live under:

`knowledge/release/rc001_release_candidate/_evidence/fixtures/`

Hash record: `_evidence/fixtures/FIXTURE_HASHES.txt`

### Official CMP

| Field | Value |
|---|---|
| Filename | `official_cmp.pdf` |
| Size (bytes) | `1844` |
| SHA-256 | `b7b33a78a7635089e56fb152b94aafb79ed4f527ea4ab517400c919545110091` |

### Official Syllabus

| Field | Value |
|---|---|
| Filename | `official_syllabus.pdf` |
| Size (bytes) | `1731` |
| SHA-256 | `68b4204d62b21513324b5ab88b96f97b546028aa2a1446b91b6fa675bbcf6a60` |

### Provenance

| Field | Value |
|---|---|
| Source pack | EV-001 capture `/tmp/ev001_capture/` |
| Byte-identical to EV-001 CS1V instance store | Yes — matches `instance/curriculum_documents/cs1v/cmp/v1/b7b33a78a7635089-f868d522.pdf` and `…/syllabus/v1/68b4204d62b21513-90ebca36.pdf` |

---

## Subject / workspace binding (prescribed)

At RC certification the database is empty (no workspace rows). The following identity is **approved for all subsequent validation programmes** using this RC:

| Field | Prescribed value | Notes |
|---|---|---|
| Subject Code | `CS1V` | Same code used in EV-001 lifecycle verification |
| Workspace ID | Created during programme (`ws-cs1v` if Studio assigns that id) | Must be recorded in each programme’s evidence after create; must not swap fixture packs mid-programme |

**Do not** silently substitute CS1F / CS1R / other PDF packs while claiming this Release Candidate.

---

## Verification

| Check | Result | Notes |
|---|---|---|
| Fixtures approved | **PASS** | EV-001 CS1V pack frozen under `_evidence/fixtures/` with SHA-256 |
| Same fixtures used throughout all validation programmes | **BINDING RULE** | Every programme must hash-upload these exact files and cite this document |

---

## Operator instruction

Before upload in any validation walk:

```bash
shasum -a 256 knowledge/release/rc001_release_candidate/_evidence/fixtures/official_cmp.pdf
shasum -a 256 knowledge/release/rc001_release_candidate/_evidence/fixtures/official_syllabus.pdf
```

Hashes must match the table above. Mismatch → stop; do not continue under `RC-2026.07.29-01`.

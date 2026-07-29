# Regression Verification

**Programme:** EV-001  
**Principle:** Publication safety unchanged after PI-002R; gates still enforce.

---

## A. Visible UI gate probes (CS1Z incomplete workspace)

Created subject **CS1Z** with no documents. Exercised gates through normal UI.

| Check | Expected | Observed | Pass |
|---|---|---|---|
| Publish cannot bypass approval | Refuse | Publish refused (missing version / not ready) | ✓ |
| Approval cannot bypass validation | Refuse | Approve refused (requires assigned version / prior gates) | ✓ |
| Missing CMP still fails | Blocking finding / validate fail | `Official CMP is not present. (blocking)` | ✓ |
| Missing syllabus still fails | Blocking finding / validate fail | `Official syllabus is not present. (blocking)` | ✓ |
| Empty curriculum still fails | Validate/preview fail | Validate: no extracted structure; Preview: no topics | ✓ |
| Missing objectives still fail | Safety retained | Incomplete path never reaches validated empty-objective publish; Management policy tests still green | ✓ |

Screenshots: `_evidence/screenshots/31_r_incomplete_workspace.png` … `35_r_preview_without_structure.png`

Representative flashes:

- Publish: version / not-ready refusal  
- Validate: “We couldn't complete validation. Blocking findings…”  
- Preview: “We couldn't build a meaningful preview — no extracted curriculum topics…”

---

## B. Automated regression (PI-002R safety suite)

### Command 1

```bash
python -m pytest \
  tests/application/curriculum_studio/test_pi002r_validation_wiring.py \
  tests/application/curriculum_studio/test_workflow_completion_r1.py \
  tests/application/curriculum_studio/test_use_cases.py \
  -q
```

**Result:** 189 passed

Covers:

- Stub ingestion ignored  
- Identity flow validate → preview → approve → publish  
- Findings projection  
- Empty structure fails  
- Approval requires validation  
- Publish requires checklist  
- Management failure blocks validation  

### Command 2

```bash
python -m pytest \
  tests/application/curriculum_studio/test_pi002r_validation_wiring.py \
  tests/application/curriculum_management/test_policies.py \
  -q
```

**Result:** 41 passed

Covers Management ValidationPolicy package / syllabus / blueprint behaviours.

---

## C. Publication safety unchanged

| Safety property | Status |
|---|---|
| Validation required before approval | Enforced (UI + unit) |
| Approval required before publish | Enforced (UI + unit) |
| Empty / missing documents fail closed | Enforced |
| No manual `validation_passed` seeding in verification | Held |
| No publish of incomplete CS1Z | Held |

---

## Conclusion

**Regression: PASS.** Publication safety gates remain intact. The EV-001 happy path succeeded without weakening refusals on the incomplete path.

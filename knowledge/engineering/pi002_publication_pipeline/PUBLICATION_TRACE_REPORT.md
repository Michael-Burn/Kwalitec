# Publication Trace Report

**Programme:** PI-002  
**Stage:** Publication → Ready bridge

---

## 1. Trace: request → completion

Founder `POST /workspaces/<id>/publish` → `PublicationService.publish`:

```text
1. require Management port
2. _ensure_rollback_snapshot (creates rollback fact if missing)
3. assert_ready → PublicationChecklist.ready_to_publish
4. require version_id
5. mgmt.publish(version_id)
6. assert Management publication_state == published
7. mirror Studio version status PUBLISHED; workspace status PUBLISHED
8. PublicationBridgeService.publish_to_catalogue (Foundation Ready package)
9. record activity "published"
```

---

## 2. Checkpoint results (Founder happy path after FV re-run failure)

| Checkpoint | Expected | Actual | Notes |
|---|---|---|---|
| Publication command received | Yes | Yes | Route invoked (`C5_publish`) |
| Validation satisfied | Yes | **No** | `validation_passed` false |
| Approval satisfied | Yes | **No** | `preview_approved` false |
| Version assigned | Yes | Yes | `2026.1` present in evidence |
| Rollback snapshot created | On publish attempt | May set during `_ensure_rollback_snapshot` before assert_ready | Order: rollback ensured **before** assert_ready |
| Ready package generated | Yes | No | Never reaches bridge |
| Subject Catalogue updated | Yes | No | Subjects stay non-Ready |

---

## 3. First failed transition on publish path

`assert_ready` raises:

```text
PublicationError(
  "Not ready to publish {workspace_id}: "
  "blocking=['validation_passed', 'preview_approved', ...]"
)
```

Observed flash (FV re-run): generic publish incomplete copy via `recover_flash` (`not ready` / `blocking` → `FLASH_WARNING["publish"]`).

**Important:** This is **not** the earliest pipeline failure. Publish fails because Validation (and therefore Approval) never completed. Publish’s refusal is correct safety behaviour.

---

## 4. Rollback ordering note

`_ensure_rollback_snapshot` runs **before** `assert_ready`. A refused publish can still create a rollback snapshot fact. That can move checklist from e.g. 5/8 toward 6/8 without making the curriculum publishable — another subtle consistency quirk (not the root cause).

---

## 5. Foundation bridge (only after Management publish)

`PublicationBridgeService.publish_to_catalogue`:

1. Resolve Foundation version for subject/label  
2. Ensure parsed structure JSON (from CIP/structure service if empty)  
3. Foundation `founder_review(approve=True)` if needed  
4. Foundation `publish_curriculum(activate=True)` → `PublishedCurriculumPackage`  
5. Subject Catalogue reads active packages for Ready

If Foundation missing: PublicationError (or soft-skip only for “no foundation” unit paths).

---

## 6. Management publish prerequisites

Management publication requires version in `approved` state (lawful `approved → published`). Without Studio/Management approval, publish cannot succeed even if checklist were forced.

---

## 7. Evidence

- `C5_publish` / `C5_publish_reload` in complete.json  
- `phase8_publish_refused.png` / LB-R4  
- `publication_service.py`, `publication_bridge.py`, `subject_catalogue.py`

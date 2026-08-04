# REL-001 smoke operator notes

1. Confirm `/health`, `/health/live`, `/health/ready` commit = `95a82b04ae50d32003add3a2f5e6789005a4c962`.
2. Create throwaway user via Render one-off `flask create-test-user` (do not commit plaintext password).
3. Login → alpha onboarding → CS1 enrol wizard + baseline → Student Home.
4. `POST /student/session/start` → session overview → activity (package body) → reflection → summary → complete surface.
5. History / Journey / Profile / Settings → logout.

Reuse harness patterns from `/tmp/pb001a/run_verification.py` (`Client`, `login`, `enrol`).

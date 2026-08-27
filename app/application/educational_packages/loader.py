"""Load and resolve certified educational packages from on-disk JSON (EA-006)."""

from __future__ import annotations

import json
import logging
from functools import lru_cache
from pathlib import Path
from typing import Any

from app.application.educational_packages.models import (
    CertifiedEducationalPackage,
    KnowledgeCheck,
    KnowledgeCheckChoice,
    ReadingGuidance,
    TomorrowPreviewPack,
)

logger = logging.getLogger(__name__)

_PACKAGE_REL = Path("curriculum") / "data" / "educational_packages"


def package_data_root() -> Path:
    """Absolute path to educational package JSON roots."""
    # app/application/educational_packages/loader.py → app/
    app_root = Path(__file__).resolve().parents[2]
    return app_root / _PACKAGE_REL


def find_educational_package(
    *,
    topic_id: str = "",
    topic_code: str = "",
    topic_title: str = "",
    subject_id: str = "",
) -> CertifiedEducationalPackage | None:
    """Resolve a publication-approved package for a topic, if one exists."""
    return EducationalPackageLoader().find(
        topic_id=topic_id,
        topic_code=topic_code,
        topic_title=topic_title,
        subject_id=subject_id,
    )


def find_package_by_id(package_id: str) -> CertifiedEducationalPackage | None:
    """Resolve a publication-approved package by exact package_id."""
    pid = (package_id or "").strip()
    if not pid:
        return None
    for pack in EducationalPackageLoader().all_approved():
        if pack.package_id == pid:
            return pack
    return None


def packages_for_subject(
    subject_id: str,
) -> tuple[CertifiedEducationalPackage, ...]:
    """All publication-approved packages for a subject (stable load order)."""
    sid = (subject_id or "").strip().upper()
    if not sid:
        return ()
    return tuple(
        p
        for p in EducationalPackageLoader().all_approved()
        if p.subject_id.upper() == sid
    )


def reset_educational_package_cache() -> None:
    """Clear cached package inventory (tests)."""
    EducationalPackageLoader._load_all.cache_clear()
    try:
        from app.application.educational_packages.guard import (
            reset_certified_guidance_cache,
        )

        reset_certified_guidance_cache()
    except ImportError:
        pass


class EducationalPackageLoader:
    """Deterministic loader over certified educational package JSON files."""

    def __init__(self, *, root: Path | None = None) -> None:
        self._root = root or package_data_root()

    def find(
        self,
        *,
        topic_id: str = "",
        topic_code: str = "",
        topic_title: str = "",
        subject_id: str = "",
    ) -> CertifiedEducationalPackage | None:
        tid = (topic_id or "").strip()
        code = _normalize_code(topic_code)
        title = (topic_title or "").strip().lower()
        subject = (subject_id or "").strip().upper()

        # Prefer exact identity matches, then code, then title keywords.
        for pack in self.all_approved():
            if subject and pack.subject_id.upper() != subject:
                # Soft filter — unknown subject still allows code/title match.
                if code and pack.topic_code != code and tid not in pack.topic_aliases:
                    if not any(k in title for k in pack.topic_title_keywords):
                        continue
            if tid and (
                tid == pack.topic_code
                or tid in pack.topic_aliases
                or tid.lower() == pack.topic_title.lower()
            ):
                return pack
            if code and pack.topic_code == code:
                return pack
        for pack in self.all_approved():
            if title and any(k in title for k in pack.topic_title_keywords):
                return pack
        return None

    def all_approved(self) -> tuple[CertifiedEducationalPackage, ...]:
        return tuple(
            p for p in self._load_all(str(self._root)) if p.is_publication_approved
        )

    @staticmethod
    @lru_cache(maxsize=4)
    def _load_all(root_str: str) -> tuple[CertifiedEducationalPackage, ...]:
        root = Path(root_str)
        if not root.is_dir():
            return ()
        packs: list[CertifiedEducationalPackage] = []
        for path in sorted(root.rglob("*.json")):
            try:
                raw = json.loads(path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError) as exc:
                logger.warning(
                    "educational_package_load_failed path=%s err=%s",
                    path,
                    exc,
                )
                continue
            if not isinstance(raw, dict):
                continue
            try:
                packs.append(_parse_package(raw, source_path=str(path)))
            except (KeyError, TypeError, ValueError) as exc:
                logger.warning(
                    "educational_package_parse_failed path=%s err=%s", path, exc
                )
                continue
        return tuple(packs)


def _normalize_code(code: str) -> str:
    text = (code or "").strip()
    if not text:
        return ""
    # Titles like "4.2 Understand…" → "4.2"
    head = text.split()[0] if text else ""
    if head and head[0].isdigit():
        return head
    return text


def _parse_package(
    raw: dict[str, Any], *, source_path: str
) -> CertifiedEducationalPackage:
    mission = dict(raw.get("mission") or {})
    session = dict(raw.get("session") or {})
    reading_raw = dict(raw.get("reading_guidance") or {})
    reflection = dict(raw.get("reflection") or {})
    tomorrow_raw = dict(raw.get("tomorrow_preview") or {})
    checks_raw = list(raw.get("knowledge_checks") or [])

    pause_points: list[dict[str, str]] = []
    for pp in reading_raw.get("pause_points") or ():
        if isinstance(pp, dict):
            pause_points.append({str(k): str(v) for k, v in pp.items()})

    reading = ReadingGuidance(
        lead_line=str(reading_raw.get("lead_line") or "").strip(),
        focus_questions=tuple(
            str(q).strip()
            for q in (reading_raw.get("focus_questions") or ())
            if str(q).strip()
        ),
        misconception_watch=tuple(
            str(m).strip()
            for m in (reading_raw.get("misconception_watch") or ())
            if str(m).strip()
        ),
        open_point=str(reading_raw.get("open_point") or "").strip(),
        stop_condition=str(reading_raw.get("stop_condition") or "").strip(),
        out_of_scope_today=tuple(
            str(x).strip()
            for x in (reading_raw.get("out_of_scope_today") or ())
            if str(x).strip()
        ),
        annotation_task=str(reading_raw.get("annotation_task") or "").strip(),
        attempt_before_reveal=str(
            reading_raw.get("attempt_before_reveal") or ""
        ).strip(),
        exit_line=str(reading_raw.get("exit_line") or "").strip(),
        return_cue=str(reading_raw.get("return_cue") or "").strip(),
        pause_points=tuple(pause_points),
        reentry_line=str(reading_raw.get("reentry_line") or "").strip(),
    )

    checks: list[KnowledgeCheck] = []
    for item in checks_raw:
        if not isinstance(item, dict):
            continue
        choices: list[KnowledgeCheckChoice] = []
        for raw_choice in item.get("choices") or ():
            if not isinstance(raw_choice, dict):
                continue
            cid = str(raw_choice.get("id") or "").strip()
            label = str(raw_choice.get("label") or "").strip()
            if not cid or not label:
                continue
            choices.append(
                KnowledgeCheckChoice(
                    id=cid,
                    label=label,
                    misconception_tag=str(
                        raw_choice.get("misconception_tag") or ""
                    ).strip(),
                )
            )
        checks.append(
            KnowledgeCheck(
                episode_id=str(item.get("episode_id") or "").strip(),
                kind=str(item.get("kind") or "").strip(),
                item_id=str(item.get("item_id") or "").strip(),
                title=str(item.get("title") or "").strip(),
                prompt=str(item.get("prompt") or "").strip(),
                response_type=str(
                    item.get("response_type") or "short_structured"
                ).strip(),
                body=str(item.get("body") or "").strip(),
                hints=tuple(
                    str(h).strip() for h in (item.get("hints") or ()) if str(h).strip()
                ),
                accepted_keywords=tuple(
                    str(k).strip()
                    for k in (item.get("accepted_keywords") or ())
                    if str(k).strip()
                ),
                explanation=str(item.get("explanation") or "").strip(),
                model_answer=str(item.get("model_answer") or "").strip(),
                common_mistake=str(item.get("common_mistake") or "").strip(),
                success_criteria=tuple(
                    str(c).strip()
                    for c in (item.get("success_criteria") or ())
                    if str(c).strip()
                ),
                choices=tuple(choices),
                correct_choice_id=str(item.get("correct_choice_id") or "").strip(),
            )
        )

    time_raw = mission.get("estimated_study_time_minutes") or {}
    if not isinstance(time_raw, dict):
        time_raw = {}
    session_time = session.get("duration_budget_minutes") or {}
    if not isinstance(session_time, dict):
        session_time = {}

    return CertifiedEducationalPackage(
        package_id=str(raw.get("package_id") or "").strip(),
        package_version=str(raw.get("package_version") or "").strip(),
        publication_version=str(raw.get("publication_version") or "").strip(),
        status=str(raw.get("status") or "").strip(),
        subject_id=str(raw.get("subject_id") or "").strip(),
        topic_code=str(raw.get("topic_code") or "").strip(),
        topic_title=str(raw.get("topic_title") or "").strip(),
        topic_aliases=tuple(
            str(a).strip() for a in (raw.get("topic_aliases") or ()) if str(a).strip()
        ),
        topic_title_keywords=tuple(
            str(k).strip().lower()
            for k in (raw.get("topic_title_keywords") or ())
            if str(k).strip()
        ),
        golden_id=str(raw.get("golden_id") or "").strip(),
        mode=str(raw.get("mode") or "learning").strip(),
        display_title=str(mission.get("display_title") or "").strip(),
        mission_purpose=str(mission.get("mission_purpose") or "").strip(),
        learning_objective=str(mission.get("learning_objective") or "").strip(),
        concept_focus=str(mission.get("concept_focus") or "").strip(),
        prior_bridge=str(mission.get("prior_bridge") or "").strip(),
        why_now=str(mission.get("why_now") or "").strip(),
        expected_benefit=str(mission.get("expected_benefit") or "").strip(),
        explainability=str(mission.get("explainability") or "").strip(),
        success_criteria=tuple(
            str(c).strip()
            for c in (mission.get("success_criteria") or ())
            if str(c).strip()
        ),
        task_descriptions=tuple(
            str(t).strip()
            for t in (mission.get("task_descriptions") or ())
            if str(t).strip()
        ),
        student_brief=str(mission.get("student_brief") or "").strip(),
        session_purpose=str(session.get("session_educational_purpose") or "").strip(),
        wrap_up=str(session.get("wrap_up") or "").strip(),
        confidence_prompt=str(session.get("confidence_prompt") or "").strip(),
        reading=reading,
        knowledge_checks=tuple(checks),
        reflection_framing=str(reflection.get("framing") or "").strip(),
        reflection_prompt=str(reflection.get("prompt") or "").strip(),
        reflection_prompts=tuple(
            str(p).strip() for p in (reflection.get("prompts") or ()) if str(p).strip()
        ),
        tomorrow=TomorrowPreviewPack(
            next_topic_code=str(tomorrow_raw.get("next_topic_code") or "").strip(),
            next_topic_title=str(tomorrow_raw.get("next_topic_title") or "").strip(),
            continuity_line=str(tomorrow_raw.get("continuity_line") or "").strip(),
            light_prep_cue=str(tomorrow_raw.get("light_prep_cue") or "").strip(),
            student_facing=str(tomorrow_raw.get("student_facing") or "").strip(),
        ),
        campaign_id=str(raw.get("campaign_id") or "").strip(),
        campaign_day=str(raw.get("campaign_day") or "").strip(),
        estimated_minutes_min=int(
            time_raw.get("min") or session_time.get("min") or 50
        ),
        estimated_minutes_max=int(
            time_raw.get("max") or session_time.get("max") or 70
        ),
        source_path=source_path,
        certification_refs=tuple(
            str(r).strip()
            for r in (raw.get("certification_refs") or ())
            if str(r).strip()
        ),
        metadata={
            "cmp_edition": str(raw.get("cmp_edition") or "").strip(),
            "published_at": str(raw.get("published_at") or "").strip(),
        },
    )

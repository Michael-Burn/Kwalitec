"""Classify extracted text into educational vs non-curriculum roles (EQ-001)."""

from __future__ import annotations

import re

from app.domain.curriculum_intelligence.content_role import ContentRole

# Recurring ActEd / IFoA page chrome.
_HEADER_FOOTER = re.compile(
    r"^(?:"
    r"AGOGO\s+CDO|"
    r"©\s*IFE\b|"
    r"©\s*Institute and Faculty of Actuaries|"
    r"The Actuarial Education Company(?:\s*©.*)?"
    r")\s*$",
    re.IGNORECASE,
)
_PAGE_RUNNING = re.compile(
    r"^(?:"
    r"Page\s+\d+\s+CS1-\d|"
    r"Syllabus\s+Actuarial Statistics\s*\(CS1\)\s*\d{4}|"
    r"CS1:\s*Study Guide\s+Page\s+\d+"
    r")",
    re.IGNORECASE,
)
# Running headers that still carry a chapter identity — keep for hierarchy,
# do not strip in normalisation.
_CHAPTER_RUNNING = re.compile(
    r"^(?:Page\s+\d+\s+)?CS1-\d+[a-z]?\s*[:\-].+",
    re.IGNORECASE,
)
_COPYRIGHT = re.compile(
    r"(?:copyright|all rights reserved|\bisbn\b|legal action will be)",
    re.IGNORECASE,
)
_TOC = re.compile(
    r"^(?:contents|table of contents|index of chapters)\b|"
    r"\bpage\s+\d+\s*$|"
    r"part\s+\d+\s+section\s+\d+.+page\s+\d+",
    re.IGNORECASE,
)
_QUALIFICATION = re.compile(
    r"^(?:"
    r"associateship qualification|"
    r"core principles|"
    r"syllabus for the \d{4} examinations|"
    r"links across the qualifications|"
    r"how this subject links|"
    r"aim of the subject|"
    r"aim|"
    r"topics and topic weightings|"
    r"subject topics and topic weightings"
    r")\s*$",
    re.IGNORECASE,
)
_ASSESSMENT = re.compile(
    r"^(?:"
    r"assessment information|"
    r"topic weighting|"
    r"the examination|"
    r"paper\s*[ab]\b|"
    r"mock exam|"
    r"permitted calculators?"
    r")|"
    r"\bcs1[ab]\b.*candidates|"
    r"combined mark of a pass",
    re.IGNORECASE,
)
_APPENDIX = re.compile(
    r"^(?:appendix|appendices|annex)\b",
    re.IGNORECASE,
)
_INDEX = re.compile(r"^(?:index|subject index)\b", re.IGNORECASE)
_REFERENCES = re.compile(
    r"^(?:references|bibliography|further reading)\s*$",
    re.IGNORECASE,
)
_FRONT_MATTER_TITLES = re.compile(
    r"^(?:"
    r"combined materials pack|"
    r"the actuarial education company|"
    r"study guide|"
    r"introduction|"
    r"before you start|"
    r"core study material|"
    r"acted study support|"
    r"study skills|"
    r"queries and feedback|"
    r"frequently asked questions|"
    r"revision notes|"
    r"preface|"
    r"acknowledgements?|"
    r"edition information|"
    r"syllabus objectives\s*$"
    r")\s*$",
    re.IGNORECASE,
)
_PUBLISHER = re.compile(
    r"^(?:"
    r"april\s+\d{4}|"
    r"for exams in \d{4}|"
    r"beijing|edinburgh|london|oxford|singapore|malaysia|"
    r"institute and faculty education limited"
    r")|"
    r"www\.acted\.co\.uk|"
    r"staple inn|woodstock road|lochrin square",
    re.IGNORECASE,
)
_CHAPTER = re.compile(r"^(?:Page\s+\d+\s+)?CS1-\d+[a-z]?\b", re.IGNORECASE)
_WEIGHTED_TOPIC = re.compile(r"^\d+\s+.+\{\s*\d+\s*%\s*\}|^\d+\s+.+\[\s*\d+\s*%\s*\]")
_NUMBERED = re.compile(r"^(?P<num>\d+(?:\.\d+){0,5})\s+(?P<title>\S.+)$")
_ACTION_VERBS = re.compile(
    r"^(?:"
    r"describe|define|explain|understand|apply|evaluate|calculate|construct|"
    r"discuss|compare|state|use|complete|produce|interpret|determine|"
    r"generate|derive|identify|analyse|analyze|assess|perform|fit|"
    r"select|demonstrate|summarise|summarize|outline|list|show|"
    r"compute|estimate|test|prove|solve|recognise|recognize"
    r")\b",
    re.IGNORECASE,
)
_EDUCATIONAL_START = re.compile(
    r"(?:^CS1-\d+[a-z]?\b)|(?:^\d+\s+\S.+(?:\[\s*\d+\s*%\s*\]|\{\s*\d+\s*%\s*\}))",
    re.IGNORECASE,
)


class ContentClassificationService:
    """Deterministic semantic classifier for CMP / syllabus text lines."""

    def classify_line(self, text: str) -> ContentRole:
        """Classify a single line or short title."""
        line = (text or "").strip()
        if not line or len(line) < 2:
            return ContentRole.BLANK_ARTEFACT
        # Chapter running headers are educational anchors, not disposable chrome.
        if _CHAPTER_RUNNING.match(line) or _CHAPTER.match(line):
            return ContentRole.EDUCATIONAL
        if _HEADER_FOOTER.match(line) or _PAGE_RUNNING.match(line):
            return ContentRole.NAVIGATION
        if _COPYRIGHT.search(line) and len(line) < 200:
            return ContentRole.COPYRIGHT
        if _TOC.search(line) and (
            "page" in line.lower() or line.lower() in {"contents", "table of contents"}
        ):
            return ContentRole.TABLE_OF_CONTENTS
        if _QUALIFICATION.match(line):
            return ContentRole.QUALIFICATION_INFORMATION
        if _ASSESSMENT.search(line) and len(line) < 160:
            return ContentRole.ASSESSMENT_LOGISTICS
        if _APPENDIX.match(line):
            return ContentRole.APPENDIX
        if _INDEX.match(line):
            return ContentRole.INDEX
        if _REFERENCES.match(line):
            return ContentRole.REFERENCES
        if _FRONT_MATTER_TITLES.match(line):
            return ContentRole.FRONT_MATTER
        if _PUBLISHER.search(line) and len(line) < 120:
            return ContentRole.PUBLISHER_METADATA
        if line.lower() in {
            "objectives",
            "subject cs1",
            "actuarial statistics",
            "actuarial statistics (cs1)",
            "syllabus for the 2026 examinations",
            "syllabus for the 2019 examinations",
        }:
            return ContentRole.FRONT_MATTER
        # Educational signals
        if _CHAPTER.match(line) or _WEIGHTED_TOPIC.match(line):
            return ContentRole.EDUCATIONAL
        m = _NUMBERED.match(line)
        if m:
            depth = m.group("num").count(".")
            # Depth-1 action verbs are topic-level outcomes, not leaf objectives.
            if depth >= 2:
                return ContentRole.LEARNING_OBJECTIVE
            return ContentRole.EDUCATIONAL
        if line.lower().startswith(("definition", "define ")):
            return ContentRole.DEFINITION
        if line.lower().startswith("worked example"):
            return ContentRole.WORKED_EXAMPLE
        if line.lower().startswith("example"):
            return ContentRole.EXAMPLE
        if re.match(r"^(?:question|exercise|practice)\b", line, re.IGNORECASE):
            return ContentRole.EXERCISE
        if re.match(r"^(?:exam tip|tip:|hint:)\b", line, re.IGNORECASE):
            return ContentRole.EXAM_TIP
        return ContentRole.EDUCATIONAL

    def is_boilerplate_line(self, text: str) -> bool:
        """True when the line is page chrome and should be dropped early."""
        line = (text or "").strip()
        if _CHAPTER_RUNNING.match(line) or _CHAPTER.match(line):
            return False
        role = self.classify_line(text)
        return role in {
            ContentRole.NAVIGATION,
            ContentRole.BLANK_ARTEFACT,
            ContentRole.COPYRIGHT,
        } and (
            _HEADER_FOOTER.match(line) is not None
            or _PAGE_RUNNING.match(line) is not None
            or not line
        )

    def marks_educational_start(self, text: str) -> bool:
        """True when this line begins the educational body of a document."""
        line = (text or "").strip()
        if _EDUCATIONAL_START.match(line):
            return True
        # Syllabus chapter without weight on same line still counts when numbered
        # topic title after "Objectives" — handled by weighted pattern primarily.
        if _CHAPTER.match(line):
            return True
        if _WEIGHTED_TOPIC.match(line):
            return True
        return False

    def looks_like_learning_objective(self, text: str) -> bool:
        """Numbered knowledge/skill statement suitable as a learning objective."""
        line = (text or "").strip()
        m = _NUMBERED.match(line)
        if not m:
            lower = line.lower()
            return any(
                h in lower
                for h in (
                    "objective",
                    "learning outcome",
                    "by the end",
                    "students will",
                    "candidates will",
                )
            )
        title = m.group("title").strip()
        depth = m.group("num").count(".")
        if depth >= 2:
            return True
        if depth == 1 and _ACTION_VERBS.match(title):
            # Depth-1 with verb is a topic-level objective (e.g. "1.1 Describe…")
            # Prefer topic mapping for depth-1; LO for depth ≥2.
            return False
        return bool(_ACTION_VERBS.match(title) and depth >= 2)

    def section_number(self, text: str) -> str | None:
        m = _NUMBERED.match((text or "").strip())
        return m.group("num") if m else None

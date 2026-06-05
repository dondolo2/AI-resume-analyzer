"""Skill extraction from resumes and job descriptions."""

from __future__ import annotations

import json
import logging
import re
from pathlib import Path
from typing import Optional, Set

import spacy

from app.core.text_cleaner import clean_resume_text
from app.exceptions import SkillDictionaryError

logger = logging.getLogger(__name__)

_nlp = None


def _get_nlp():
    """Load spaCy model once (lazy).

    Returns:
        Loaded spaCy language pipeline.
    """
    global _nlp
    if _nlp is None:
        from app import SPACY_MODEL

        _nlp = spacy.load(SPACY_MODEL)
    return _nlp


def load_skill_dict(path: Path | str) -> Set[str]:
    """Load skill dictionary from JSON file.

    Args:
        path: Path to skills_list.json.

    Returns:
        Set of lowercase skill strings.

    Raises:
        SkillDictionaryError: If file is missing or invalid.
    """
    skill_path = Path(path)
    if not skill_path.is_file():
        raise SkillDictionaryError(f"Skill dictionary not found: {skill_path}")
    try:
        with skill_path.open(encoding="utf-8") as handle:
            data = json.load(handle)
    except (json.JSONDecodeError, OSError) as exc:
        raise SkillDictionaryError(f"Failed to load skill dictionary: {exc}") from exc

    if not isinstance(data, list):
        raise SkillDictionaryError("Skill dictionary must be a JSON array")

    return {str(skill).lower().strip() for skill in data if str(skill).strip()}


def extract_job_skills(job_description: str) -> list[str]:
    """Extract meaningful keywords from a job description.

    Args:
        job_description: Raw job description text.

    Returns:
        Sorted list of unique keyword strings.
    """
    if not job_description or not job_description.strip():
        return []

    doc = _get_nlp()(job_description)
    keywords: list[str] = []

    for token in doc:
        if token.is_stop or token.is_punct:
            continue
        if token.pos_ == "PROPN":
            keywords.append(token.text.lower())
        elif token.pos_ in ("NOUN", "ADJ", "VERB"):
            keywords.append(token.lemma_.lower())

    return sorted(set(keywords))


def extract_resume_skills(
    resume_text: str,
    skill_dict: Optional[Set[str]] = None,
) -> list[str]:
    """Extract known skills from resume text using a skill dictionary.

    Args:
        resume_text: Raw or cleaned resume text.
        skill_dict: Known skills (lowercase). Uses default inline set if None.

    Returns:
        Sorted list of matched skills.
    """
    if skill_dict is None:
        from app import DEFAULT_SKILL_DICT_PATH

        skill_dict = load_skill_dict(DEFAULT_SKILL_DICT_PATH)

    cleaned = clean_resume_text(resume_text)
    found: list[str] = []
    for skill in skill_dict:
        pattern = r"\b" + re.escape(skill) + r"\b"
        if re.search(pattern, cleaned):
            found.append(skill)
    return sorted(found)

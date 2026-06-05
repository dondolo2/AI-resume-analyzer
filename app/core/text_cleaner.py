"""Text normalization utilities for resumes and job descriptions."""

import re


def clean_job_description(text: str) -> str:
    """Clean raw job description text.

    Args:
        text: Raw job description.

    Returns:
        Lowercased text with punctuation removed and whitespace normalized.
    """
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def clean_resume_text(text: str) -> str:
    """Clean and normalize resume text.

    Args:
        text: Raw resume text.

    Returns:
        Lowercased text with extra whitespace and unwanted characters removed.
    """
    if text is None:
        return ""
    text = text.lower()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"[^a-zA-Z0-9\s\.\,\-\:]", "", text)
    return text.strip()

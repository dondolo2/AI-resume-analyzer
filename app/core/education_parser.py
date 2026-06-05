"""Education level detection from resume text."""

from typing import Final

EDUCATION_LEVELS: Final[dict[str, list[str]]] = {
    "PhD": ["phd", "ph.d", "doctorate", "doctoral"],
    "Master": ["master", "msc", "m.sc", "mba", "m.eng", "honours"],
    "Bachelor": [
        "bachelor",
        "bsc",
        "b.sc",
        "btech",
        "b.tech",
        "undergraduate",
        "degree",
    ],
    "High School": ["matric", "high school", "grade 12", "secondary school"],
}


def detect_education_level(resume_text: str) -> str:
    """Detect the highest education level mentioned in a resume.

    Args:
        resume_text: Raw or cleaned resume text.

    Returns:
        One of PhD, Master, Bachelor, High School, or Unknown.
    """
    if not resume_text:
        return "Unknown"

    text_lower = resume_text.lower()
    for level, keywords in EDUCATION_LEVELS.items():
        if any(kw in text_lower for kw in keywords):
            return level
    return "Unknown"

"""Resume section parsing."""

from typing import Dict


def extract_resume_sections(resume_text: str) -> Dict[str, str]:
    """Split resume into structured sections using heading keyword detection.

    Args:
        resume_text: Raw or cleaned resume text.

    Returns:
        Dict with keys education, experience, skills, projects.
    """
    sections: Dict[str, str] = {
        "education": "",
        "experience": "",
        "skills": "",
        "projects": "",
    }

    if not resume_text:
        return sections

    section_keywords = {
        "education": ["education", "academic background", "qualifications"],
        "experience": ["experience", "work experience", "employment", "work history"],
        "skills": ["skills", "technical skills", "core competencies"],
        "projects": ["projects", "personal projects", "academic projects"],
    }

    lines = resume_text.split("\n")
    current_section = None

    for line in lines:
        stripped = line.strip()
        line_lower = stripped.lower()
        matched_heading = False
        for sec, keywords in section_keywords.items():
            if any(kw in line_lower for kw in keywords):
                current_section = sec
                matched_heading = True
                break
        if not matched_heading and current_section and stripped:
            sections[current_section] += stripped + "\n"

    for sec in sections:
        sections[sec] = sections[sec].strip()
    return sections

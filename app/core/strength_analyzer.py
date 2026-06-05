"""Overall resume strength scoring across four dimensions."""

import re
from typing import Any, Dict, List

from app.core.education_parser import detect_education_level
from app.core.experience_analyzer import estimate_experience_years
from app.core.skill_extractor import extract_resume_skills


def analyze_resume_strength(resume_text: str) -> Dict[str, Any]:
    """Score resume strength across skill, experience, education, and projects.

    Args:
        resume_text: Raw resume text.

    Returns:
        Dict with strength_score (0-100) and feedback message list.
    """
    feedback: List[str] = []
    score = 0

    skills = extract_resume_skills(resume_text)
    skill_pts = min(len(skills), 10) * 4
    score += skill_pts
    if len(skills) < 5:
        feedback.append("Add more technical skills to strengthen your profile.")
    else:
        feedback.append(f"Good skill diversity — {len(skills)} skills detected.")

    years = estimate_experience_years(resume_text)
    exp_pts = min(years, 6) * 5
    score += exp_pts
    if years == 0:
        feedback.append("Quantify your experience (e.g. '2 years of Python').")
    else:
        feedback.append(f"Experience detected: ~{years} year(s).")

    edu = detect_education_level(resume_text)
    edu_points = {
        "PhD": 20,
        "Master": 16,
        "Bachelor": 12,
        "High School": 6,
        "Unknown": 0,
    }
    score += edu_points[edu]
    feedback.append(f"Education level detected: {edu}.")

    project_entries = len(re.findall(r"—|–", resume_text))
    if project_entries >= 2:
        score += 10
        feedback.append("Multiple projects found - great for showcasing work.")
    elif project_entries >= 1:
        score += 5
        feedback.append("Consider adding more projects to your resume.")
    else:
        feedback.append("No projects section detected - consider adding one.")

    return {"strength_score": min(score, 100), "feedback": feedback}

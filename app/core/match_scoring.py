"""Match scoring and skill gap analysis."""

from typing import Dict, List


def calculate_match_score(matched_skills: List[str], job_skills: List[str]) -> float:
    """Calculate match percentage between resume and job skills.

    Args:
        matched_skills: Skills present in both resume and job.
        job_skills: Skills required by the job.

    Returns:
        Match percentage from 0.0 to 100.0.
    """
    if not job_skills:
        return 0.0
    score = (len(matched_skills) / len(job_skills)) * 100
    return round(score, 2)


def match_resume_to_job(
    resume_skills: List[str],
    job_skills: List[str],
) -> Dict[str, List[str]]:
    """Compare resume skills with job skills.

    Args:
        resume_skills: Skills extracted from resume.
        job_skills: Skills required by job.

    Returns:
        Dict with matched_skills and missing_skills lists.
    """
    resume_set = {skill.lower() for skill in resume_skills}
    job_set = {skill.lower() for skill in job_skills}
    return {
        "matched_skills": sorted(resume_set & job_set),
        "missing_skills": sorted(job_set - resume_set),
    }


def identify_skill_gap(
    candidate_skills: List[str],
    job_skills: List[str],
) -> Dict[str, List[str]]:
    """Identify matched and missing skills between candidate and job.

    Args:
        candidate_skills: Skills the candidate has.
        job_skills: Skills the job requires.

    Returns:
        Dict with matched and missing skill lists.
    """
    candidate_set = {s.lower() for s in candidate_skills}
    job_set = {s.lower() for s in job_skills}
    return {
        "matched": sorted(candidate_set & job_set),
        "missing": sorted(job_set - candidate_set),
    }

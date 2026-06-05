"""Experience duration estimation from resume text."""

import re
from datetime import datetime


def estimate_experience_years(resume_text: str) -> int:
    """Estimate total years of experience mentioned in a resume.

    Args:
        resume_text: Raw or cleaned resume text.

    Returns:
        Estimated years of experience (0 if none detected).
    """
    if not resume_text:
        return 0

    text_lower = resume_text.lower()
    word_to_num = {
        "one": 1,
        "two": 2,
        "three": 3,
        "four": 4,
        "five": 5,
        "six": 6,
        "seven": 7,
        "eight": 8,
        "nine": 9,
        "ten": 10,
    }
    explicit_years: list[int] = []

    digit_matches = re.findall(r"(\d+)\s+year", text_lower)
    explicit_years.extend(int(y) for y in digit_matches)

    for word, num in word_to_num.items():
        if re.search(rf"\b{word}\s+year", text_lower):
            explicit_years.append(num)

    current_year = datetime.now().year
    range_total = 0
    range_matches = re.findall(
        r"(20\d{2}|19\d{2})\s*[-–—to]+\s*(20\d{2}|19\d{2}|present)",
        text_lower,
    )
    for start, end in range_matches:
        end_year = current_year if end == "present" else int(end)
        duration = end_year - int(start)
        if 0 < duration <= 50:
            range_total += duration

    all_estimates = explicit_years + ([range_total] if range_total > 0 else [])
    return max(all_estimates) if all_estimates else 0

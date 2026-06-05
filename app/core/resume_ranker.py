"""Resume candidate ranking utilities."""

from typing import Any, Dict, List


def rank_resumes(resume_scores: Dict[str, float]) -> List[Dict[str, Any]]:
    """Rank candidates from highest to lowest score.

    Args:
        resume_scores: Mapping of candidate name to score.

    Returns:
        Sorted list of dicts with rank, candidate, and score keys.
    """
    sorted_candidates = sorted(
        resume_scores.items(),
        key=lambda item: item[1],
        reverse=True,
    )
    return [
        {"rank": index + 1, "candidate": name, "score": score}
        for index, (name, score) in enumerate(sorted_candidates)
    ]

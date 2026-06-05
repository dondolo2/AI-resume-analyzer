"""Skill list vectorization for comparison."""

from typing import List, Optional

from sklearn.feature_extraction.text import CountVectorizer


def vectorize_skills(
    skill_list: List[str],
    vocabulary: Optional[List[str]] = None,
) -> List[int]:
    """Convert a list of skills into a binary vector.

    Args:
        skill_list: Skills to vectorize.
        vocabulary: Optional fixed vocabulary for consistent vectors.

    Returns:
        Binary vector (1 = present, 0 = absent). Empty list if no skills.
    """
    if not skill_list:
        return []

    text = " ".join(skill_list)
    if vocabulary:
        vectorizer = CountVectorizer(vocabulary=vocabulary)
    else:
        vectorizer = CountVectorizer()

    matrix = vectorizer.fit_transform([text])
    return matrix.toarray()[0].tolist()

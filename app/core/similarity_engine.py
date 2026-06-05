"""TF-IDF cosine similarity between resume texts."""

import logging

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


def calculate_resume_similarity(resume1: str, resume2: str) -> float:
    """Calculate cosine similarity between two resume texts using TF-IDF.

    Args:
        resume1: First resume text.
        resume2: Second resume text.

    Returns:
        Similarity score between 0.0 and 1.0.
    """
    if not (resume1 and resume1.strip()) or not (resume2 and resume2.strip()):
        return 0.0

    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform([resume1, resume2])
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])
    result = round(float(score[0][0]), 4)
    logger.debug("Resume similarity score: %s", result)
    return result

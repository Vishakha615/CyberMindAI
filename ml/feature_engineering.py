import numpy as np


def calculate_performance_features(
    quiz_scores,
    learning_progress,
    quiz_attempts
):

    if not quiz_scores:
        average_score = 0
    else:
        average_score = np.mean(
            quiz_scores
        )

    if not learning_progress:
        average_progress = 0
    else:
        average_progress = np.mean(
            learning_progress
        )

    return np.array([
        average_score,
        average_progress,
        quiz_attempts
    ]).reshape(1, -1)
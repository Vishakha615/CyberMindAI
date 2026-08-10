import joblib
import numpy as np


MODEL_PATH = (
    "ml/models/performance_model.pkl"
)

ENCODER_PATH = (
    "ml/models/performance_encoder.pkl"
)


model = joblib.load(
    MODEL_PATH
)

encoder = joblib.load(
    ENCODER_PATH
)


def predict_performance(
    quiz_score,
    learning_progress,
    quiz_attempts
):

    features = np.array([
        [
            quiz_score,
            learning_progress,
            quiz_attempts
        ]
    ])


    prediction = model.predict(
        features
    )[0]


    performance = encoder.inverse_transform(
        [prediction]
    )[0]


    probabilities = model.predict_proba(
        features
    )[0]


    confidence = max(
        probabilities
    ) * 100


    return (
        performance,
        confidence
    )
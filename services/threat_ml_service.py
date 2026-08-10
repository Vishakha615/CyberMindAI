import joblib
from services.threat_ml_service import (
    predict_threat
)


prediction, confidence = predict_threat(
    text
)


st.metric(
    "AI Classification",
    prediction.upper()
)

st.metric(
    "Confidence",
    f"{confidence:.1f}%"
)




MODEL_PATH = (
    "ml/models/threat_classifier.pkl"
)


model = joblib.load(
    MODEL_PATH
)


def predict_threat(text):

    prediction = model.predict(
        [text]
    )[0]

    probabilities = model.predict_proba(
        [text]
    )[0]

    confidence = max(
        probabilities
    ) * 100

    return (
        prediction,
        confidence
    )
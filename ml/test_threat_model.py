from services.threat_ml_service import (
    predict_threat
)


texts = [

    "Your account will be suspended. "
    "Verify your password immediately.",

    "Congratulations, you won a free prize!",

    "Your project submission deadline "
    "is tomorrow."

]


for text in texts:

    prediction, confidence = (
        predict_threat(text)
    )

    print("\nText:")
    print(text)

    print(
        "Prediction:",
        prediction
    )

    print(
        f"Confidence: {confidence:.2f}%"
    )
from services.performance_service import (predict_performance)


performance, confidence = predict_performance(
    quiz_score=82,
    learning_progress=75,
    quiz_attempts=8
)


print(
    "Predicted Performance:",
    performance
)


print(
    f"Confidence: {confidence:.2f}%"
)
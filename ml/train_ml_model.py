import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(
    "ml/training_data.csv"
)


X = df[
    [
        "quiz_score",
        "learning_progress",
        "quiz_attempts"
    ]
]


y = df["performance"]


# ---------------------------------------------------------
# ENCODE TARGET
# ---------------------------------------------------------

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)


# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y_encoded,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=150,
    random_state=42
)


model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# EVALUATION
# ---------------------------------------------------------

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    f"Model Accuracy: {accuracy * 100:.2f}%"
)


# ---------------------------------------------------------
# SAVE MODEL
# ---------------------------------------------------------

os.makedirs(
    "ml/models",
    exist_ok=True
)


joblib.dump(
    model,
    "ml/models/performance_model.pkl"
)


joblib.dump(
    encoder,
    "ml/models/performance_encoder.pkl"
)


print(
    "✅ ML model saved!"
)
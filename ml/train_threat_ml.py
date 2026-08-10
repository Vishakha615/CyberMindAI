import os
import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

DATA_PATH = "ml/datasets/threat_dataset.csv"

df = pd.read_csv(DATA_PATH)

print("Dataset size:", len(df))

print("\nClass distribution:")
print(df["label"].value_counts())


# ---------------------------------------------------------
# FEATURES / LABEL
# ---------------------------------------------------------

X = df["text"]

y = df["label"]


# ---------------------------------------------------------
# TRAIN / TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ---------------------------------------------------------
# MODEL PIPELINE
# ---------------------------------------------------------

model = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            ngram_range=(1, 2)
        )
    ),

    (
        "classifier",
        LogisticRegression(
            max_iter=1000
        )
    )
])


# ---------------------------------------------------------
# TRAIN
# ---------------------------------------------------------

model.fit(
    X_train,
    y_train
)


# ---------------------------------------------------------
# EVALUATE
# ---------------------------------------------------------

predictions = model.predict(
    X_test
)

accuracy = accuracy_score(
    y_test,
    predictions
)

print(
    f"\nAccuracy: {accuracy * 100:.2f}%"
)

print(
    "\nClassification Report:"
)

print(
    classification_report(
        y_test,
        predictions
    )
)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

os.makedirs(
    "ml/models",
    exist_ok=True
)

joblib.dump(
    model,
    "ml/models/threat_classifier.pkl"
)

print(
    "\n✅ Threat ML model saved!"
)
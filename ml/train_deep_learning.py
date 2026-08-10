import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.utils import to_categorical


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
].values


y = df["performance"].values


# ---------------------------------------------------------
# ENCODE LABELS
# ---------------------------------------------------------

encoder = LabelEncoder()

y_encoded = encoder.fit_transform(y)

y_categorical = to_categorical(
    y_encoded
)


# ---------------------------------------------------------
# SCALE FEATURES
# ---------------------------------------------------------

scaler = StandardScaler()

X_scaled = scaler.fit_transform(
    X
)


# ---------------------------------------------------------
# TRAIN / TEST
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y_categorical,
    test_size=0.2,
    random_state=42,
    stratify=y_encoded
)


# ---------------------------------------------------------
# NEURAL NETWORK
# ---------------------------------------------------------

model = Sequential([

    Dense(
        32,
        activation="relu",
        input_shape=(3,)
    ),

    Dropout(0.2),

    Dense(
        16,
        activation="relu"
    ),

    Dense(
        3,
        activation="softmax"
    )
])


model.compile(
    optimizer="adam",
    loss="categorical_crossentropy",
    metrics=["accuracy"]
)


# ---------------------------------------------------------
# TRAIN
# ---------------------------------------------------------

model.fit(
    X_train,
    y_train,
    epochs=30,
    batch_size=32,
    validation_split=0.2,
    verbose=1
)


# ---------------------------------------------------------
# EVALUATE
# ---------------------------------------------------------

loss, accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=0
)


print(
    f"Deep Learning Accuracy: "
    f"{accuracy * 100:.2f}%"
)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

os.makedirs(
    "ml/models",
    exist_ok=True
)


model.save(
    "ml/models/performance_nn.keras"
)


joblib.dump(
    scaler,
    "ml/models/performance_scaler.pkl"
)


joblib.dump(
    encoder,
    "ml/models/performance_dl_encoder.pkl"
)


print(
    "✅ Deep Learning model saved!"
)
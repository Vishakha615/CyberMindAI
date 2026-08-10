import os
import joblib
import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (
    Embedding,
    GlobalAveragePooling1D,
    Dense,
    Dropout
)


# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

df = pd.read_csv(
    "ml/datasets/threat_dataset.csv"
)


texts = df["text"].values

labels = df["label"].values


# ---------------------------------------------------------
# LABEL ENCODING
# ---------------------------------------------------------

encoder = LabelEncoder()

y = encoder.fit_transform(
    labels
)


# ---------------------------------------------------------
# TOKENIZATION
# ---------------------------------------------------------

tokenizer = Tokenizer(
    num_words=5000,
    oov_token="<OOV>"
)

tokenizer.fit_on_texts(
    texts
)


sequences = tokenizer.texts_to_sequences(
    texts
)


X = pad_sequences(
    sequences,
    maxlen=50,
    padding="post"
)


# ---------------------------------------------------------
# TRAIN TEST SPLIT
# ---------------------------------------------------------

X_train, X_test, y_train, y_test = (
    train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )
)


# ---------------------------------------------------------
# MODEL
# ---------------------------------------------------------

model = Sequential([

    Embedding(
        input_dim=5000,
        output_dim=32,
        input_length=50
    ),

    GlobalAveragePooling1D(),

    Dense(
        32,
        activation="relu"
    ),

    Dropout(0.2),

    Dense(
        16,
        activation="relu"
    ),

    Dense(
        len(encoder.classes_),
        activation="softmax"
    )
])


model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


# ---------------------------------------------------------
# TRAIN
# ---------------------------------------------------------

model.fit(
    X_train,
    y_train,
    epochs=20,
    batch_size=8,
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
    f"\nDeep Learning Accuracy: "
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
    "ml/models/threat_classifier_dl.keras"
)


joblib.dump(
    tokenizer,
    "ml/models/threat_tokenizer.pkl"
)


joblib.dump(
    encoder,
    "ml/models/threat_label_encoder.pkl"
)


print(
    "\n✅ Deep Learning model saved!"
)
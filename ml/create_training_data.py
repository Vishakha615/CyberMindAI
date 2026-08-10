import random
import pandas as pd


data = []


for _ in range(1000):

    quiz_score = random.randint(
        20,
        100
    )

    learning_progress = random.randint(
        10,
        100
    )

    quiz_attempts = random.randint(
        1,
        20
    )


    # Determine performance level

    if (
        quiz_score >= 75
        and learning_progress >= 70
    ):

        performance = "Advanced"

    elif (
        quiz_score >= 50
        and learning_progress >= 40
    ):

        performance = "Intermediate"

    else:

        performance = "Beginner"


    data.append([
        quiz_score,
        learning_progress,
        quiz_attempts,
        performance
    ])


df = pd.DataFrame(
    data,
    columns=[
        "quiz_score",
        "learning_progress",
        "quiz_attempts",
        "performance"
    ]
)


df.to_csv(
    "ml/training_data.csv",
    index=False
)


print(
    "✅ Training dataset created!"
)

print(
    df.head()
)
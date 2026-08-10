import json
import streamlit as st

from services.rag_service import (
    get_relevant_context
)

from services.content_generator import (
    generate_quiz
)


st.set_page_config(
    page_title="AI Quiz Generator | CyberMind AI",
    page_icon="🧠",
    layout="wide"
)


# ---------------------------------------------------------
# LOGIN
# ---------------------------------------------------------

if not st.session_state.get(
    "logged_in",
    False
):

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page(
            "pages/1_Login.py"
        )

    st.stop()


# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------

st.title("🧠 AI Quiz Generator")

st.write(
    "Generate cybersecurity questions "
    "using RAG + Generative AI."
)


col1, col2, col3 = st.columns(3)


with col1:

    topic = st.selectbox(
        "Topic",
        [
            "Cybersecurity Fundamentals",
            "Networking",
            "Cryptography",
            "Web Security",
            "Authentication",
            "Threat Detection"
        ]
    )


with col2:

    difficulty = st.selectbox(
        "Difficulty",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


with col3:

    number_of_questions = st.selectbox(
        "Questions",
        [3, 5, 10]
    )


if st.button(
    "✨ Generate Quiz",
    use_container_width=True
):

    with st.spinner(
        "Generating AI quiz..."
    ):

        try:

            context = get_relevant_context(
                topic,
                top_k=5
            )

            if not context:

                st.warning(
                    "No relevant knowledge found."
                )

                st.stop()


            raw_quiz = generate_quiz(
                topic,
                difficulty,
                number_of_questions,
                context
            )


            # Remove markdown code fences
            raw_quiz = raw_quiz.strip()

            if raw_quiz.startswith(
                "```json"
            ):

                raw_quiz = raw_quiz[
                    7:-3
                ]

            elif raw_quiz.startswith(
                "```"
            ):

                raw_quiz = raw_quiz[
                    3:-3
                ]


            quiz = json.loads(
                raw_quiz
            )


            st.session_state.ai_quiz = quiz


        except json.JSONDecodeError:

            st.error(
                "The AI returned an invalid "
                "quiz format. Please try again."
            )

        except Exception as e:

            st.error(
                "Unable to generate quiz."
            )

            st.exception(e)


# ---------------------------------------------------------
# DISPLAY GENERATED QUIZ
# ---------------------------------------------------------

if "ai_quiz" in st.session_state:

    st.divider()

    st.subheader(
        f"🧠 {topic} Quiz"
    )


    for index, question in enumerate(
        st.session_state.ai_quiz,
        start=1
    ):

        st.markdown(
            f"### Question {index}"
        )

        st.write(
            question["question"]
        )

        st.radio(
            "Choose your answer:",
            [
                f"A. {question['option_a']}",
                f"B. {question['option_b']}",
                f"C. {question['option_c']}",
                f"D. {question['option_d']}"
            ],
            key=f"ai_q_{index}"
        )

        st.divider()
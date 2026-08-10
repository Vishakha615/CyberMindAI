import streamlit as st

from services.quiz_service import (
    get_quiz_questions,
    save_quiz_result
)


st.set_page_config(
    page_title="Quiz | CyberMind AI",
    page_icon="🧠",
    layout="wide"
)


# ---------------------------------------------------------
# LOGIN CHECK
# ---------------------------------------------------------

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page("pages/1_Login.py")

    st.stop()


user_id = st.session_state.user_id


# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------

st.title("🧠 Cybersecurity Quiz")

st.write(
    "Test your cybersecurity knowledge and track "
    "your learning progress."
)


# ---------------------------------------------------------
# QUIZ SETTINGS
# ---------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:

    topic = st.selectbox(
        "Select Topic",
        [
            "Cybersecurity Fundamentals",
            "Networking",
            "Cryptography",
            "Web Security"
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


# ---------------------------------------------------------
# START QUIZ
# ---------------------------------------------------------

if st.button(
    "🚀 Start Quiz",
    use_container_width=True
):

    questions = get_quiz_questions(
        topic,
        difficulty,
        number_of_questions
    )

    if not questions:

        st.error(
            "No questions available for this topic "
            "and difficulty."
        )

    else:

        st.session_state.quiz_questions = questions
        st.session_state.quiz_started = True
        st.session_state.quiz_submitted = False

        st.rerun()


# ---------------------------------------------------------
# DISPLAY QUIZ
# ---------------------------------------------------------

if st.session_state.get(
    "quiz_started",
    False
):

    questions = st.session_state.quiz_questions

    st.divider()

    st.subheader(
        f"📚 {topic}"
    )

    answers = {}

    for index, question in enumerate(
        questions,
        start=1
    ):

        st.markdown(
            f"### Question {index}"
        )

        st.write(
            question["question_text"]
        )

        options = {
            "A": question["option_a"],
            "B": question["option_b"],
            "C": question["option_c"],
            "D": question["option_d"]
        }

        selected = st.radio(
            "Select your answer:",
            options.keys(),
            format_func=lambda x: (
                f"{x}. {options[x]}"
            ),
            key=f"question_{question['question_id']}"
        )

        answers[
            question["question_id"]
        ] = selected

        st.divider()


    # -----------------------------------------------------
    # SUBMIT
    # -----------------------------------------------------

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        correct_answers = 0

        for question in questions:

            user_answer = answers.get(
                question["question_id"]
            )

            correct_answer = question[
                "correct_option"
            ]

            if user_answer == correct_answer:

                correct_answers += 1


        total_questions = len(questions)

        score = (
            correct_answers /
            total_questions
        ) * 100


        # Save result

        saved = save_quiz_result(
            user_id,
            topic,
            total_questions,
            correct_answers
        )


        if saved:

            st.session_state.quiz_submitted = True

            st.success(
                "Quiz result saved successfully!"
            )


            # -------------------------------------------------
            # RESULT
            # -------------------------------------------------

            st.divider()

            st.subheader("🎉 Quiz Result")

            col1, col2, col3 = st.columns(3)

            with col1:

                st.metric(
                    "Score",
                    f"{score:.1f}%"
                )

            with col2:

                st.metric(
                    "Correct",
                    correct_answers
                )

            with col3:

                st.metric(
                    "Total",
                    total_questions
                )


            if score >= 80:

                st.success(
                    "🔥 Excellent! You have a strong "
                    "understanding of this topic."
                )

            elif score >= 50:

                st.warning(
                    "👍 Good attempt! Review the topic "
                    "and try the quiz again."
                )

            else:

                st.error(
                    "📚 You should revise this topic "
                    "before attempting the quiz again."
                )


            # Clear quiz

            st.session_state.quiz_started = False
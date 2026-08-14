'''import json
import streamlit as st
from services.rag_service import get_relevant_context
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

        st.divider()'''











import json
import streamlit as st

from services.rag_service import get_relevant_context
from services.content_generator import generate_quiz


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

    st.warning(
        "Please login first."
    )

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


# ---------------------------------------------------------
# QUIZ SETTINGS
# ---------------------------------------------------------

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


# ---------------------------------------------------------
# GENERATE QUIZ
# ---------------------------------------------------------

if st.button(
    "✨ Generate Quiz",
    use_container_width=True
):

    with st.spinner(
        "Generating AI quiz..."
    ):

        try:

            # Get RAG context

            context = get_relevant_context(
                topic,
                top_k=5
            )

            if not context:

                st.warning(
                    "No relevant knowledge found."
                )

                st.stop()


            # Generate quiz

            raw_quiz = generate_quiz(
                topic,
                difficulty,
                number_of_questions,
                context
            )


            raw_quiz = raw_quiz.strip()


            # Remove code fences if AI adds them

            if raw_quiz.startswith(
                "```json"
            ):

                raw_quiz = raw_quiz[7:-3]

            elif raw_quiz.startswith(
                "```"
            ):

                raw_quiz = raw_quiz[3:-3]


            # Convert JSON to Python

            quiz = json.loads(
                raw_quiz
            )


            # Save quiz

            st.session_state.ai_quiz = quiz

            # Reset previous answers

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = None


        except json.JSONDecodeError:

            st.error(
                "The AI returned an invalid quiz format. Please try again."
            )


        except Exception as e:

            st.error(
                "Unable to generate quiz."
            )

            st.exception(e)


# ---------------------------------------------------------
# DISPLAY QUIZ
# ---------------------------------------------------------

if "ai_quiz" in st.session_state:

    st.divider()

    st.subheader(
        f"🧠 {topic} Quiz"
    )

    st.info(
        "Choose one answer for each question, "
        "then click Submit Quiz."
    )


    # -----------------------------------------------------
    # QUESTIONS
    # -----------------------------------------------------

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


    # -----------------------------------------------------
    # SUBMIT
    # -----------------------------------------------------

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        correct = 0
        wrong = 0


        # Check answers

        for index, question in enumerate(
            st.session_state.ai_quiz,
            start=1
        ):

            selected = st.session_state.get(
                f"ai_q_{index}"
            )


            if selected is None:

                continue


            # Get selected option letter

            selected_answer = selected[0]


            correct_answer = (
                question["correct_answer"]
                .upper()
            )


            if selected_answer == correct_answer:

                correct += 1

            else:

                wrong += 1


        total = len(
            st.session_state.ai_quiz
        )

        unanswered = (
            total - correct - wrong
        )


        # Save result

        st.session_state.quiz_score = {
            "correct": correct,
            "wrong": wrong,
            "unanswered": unanswered,
            "total": total
        }

        st.session_state.quiz_submitted = True


# ---------------------------------------------------------
# RESULT
# ---------------------------------------------------------

if st.session_state.get(
    "quiz_submitted",
    False
):

    score = st.session_state.quiz_score


    st.divider()

    st.subheader(
        "🎉 Quiz Result"
    )


    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total",
            score["total"]
        )


    with col2:

        st.metric(
            "Correct",
            score["correct"]
        )


    with col3:

        st.metric(
            "Wrong",
            score["wrong"]
        )


    with col4:

        st.metric(
            "Unanswered",
            score["unanswered"]
        )


    # Percentage

    percentage = (
        score["correct"]
        / score["total"]
    ) * 100


    st.progress(
        percentage / 100
    )


    st.write(
        f"### Score: {score['correct']} / {score['total']} "
        f"({percentage:.0f}%)"
    )


    # -----------------------------------------------------
    # ANSWER REVIEW
    # -----------------------------------------------------

    st.subheader(
        "📖 Answer Review"
    )


    for index, question in enumerate(
        st.session_state.ai_quiz,
        start=1
    ):

        selected = st.session_state.get(
            f"ai_q_{index}"
        )


        selected_answer = (
            selected[0]
            if selected
            else "Not answered"
        )


        correct_answer = (
            question["correct_answer"]
            .upper()
        )


        st.markdown(
            f"### Question {index}"
        )


        st.write(
            question["question"]
        )


        if selected_answer == correct_answer:

            st.success(
                f"✅ Your answer: {selected_answer} — Correct!"
            )

        elif selected_answer == "Not answered":

            st.warning(
                f"⚠️ Not answered"
            )

        else:

            st.error(
                f"❌ Your answer: {selected_answer} — Wrong"
            )


        st.info(
            f"✅ Correct answer: {correct_answer}"
        )


        st.write(
            f"💡 **Explanation:** "
            f"{question['explanation']}"
        )


        st.divider()

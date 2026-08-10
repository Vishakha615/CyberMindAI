import re
import streamlit as st

from services.interview_service import (
    generate_interview_question,
    evaluate_answer,
    save_interview_result
)


st.set_page_config(
    page_title="AI Interview | CyberMind AI",
    page_icon="🎤",
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


user_id = st.session_state.user_id


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title(
    "🎤 AI Cybersecurity Interview"
)

st.write(
    "Practice cybersecurity interview "
    "questions and receive AI-powered feedback."
)


# ---------------------------------------------------------
# SETTINGS
# ---------------------------------------------------------

col1, col2 = st.columns(2)


with col1:

    topic = st.selectbox(
        "Interview Topic",
        [
            "Cybersecurity Fundamentals",
            "Networking",
            "Cryptography",
            "Web Security",
            "Authentication",
            "Threat Detection",
            "Cloud Security"
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


# ---------------------------------------------------------
# GENERATE QUESTION
# ---------------------------------------------------------

if st.button(
    "🎯 Generate Question",
    use_container_width=True
):

    with st.spinner(
        "Preparing your interview question..."
    ):

        try:

            question = (
                generate_interview_question(
                    topic,
                    difficulty
                )
            )

            st.session_state.interview_question = (
                question
            )

            
            st.session_state.interview_feedback = None
            
            st.session_state.interview_saved = False

        except Exception as e:

            st.error(
                "Unable to generate question."
            )

            st.exception(e)


# ---------------------------------------------------------
# QUESTION
# ---------------------------------------------------------

if "interview_question" in st.session_state:

    st.divider()

    st.subheader(
        "💬 Interview Question"
    )

    st.info(
        st.session_state.interview_question
    )


    answer = st.text_area(
        "Your Answer",
        height=200,
        placeholder=(
            "Write your answer as if you "
            "were answering an interviewer..."
        )
    )


    if st.button(
        "🤖 Evaluate My Answer",
        use_container_width=True
    ):

        if not answer.strip():

            st.warning(
                "Please write your answer first."
            )

            st.stop()


        with st.spinner(
            "AI is evaluating your answer..."
        ):

            try:

                feedback = evaluate_answer(
                    topic,
                    st.session_state.interview_question,
                    answer
                )

                st.session_state.interview_feedback = (
                    feedback
                )


            except Exception as e:

                st.error(
                    "Unable to evaluate answer."
                )

                st.exception(e)


# ---------------------------------------------------------
# FEEDBACK
# ---------------------------------------------------------

if st.session_state.get(
    "interview_feedback"
):

    st.divider()

    st.subheader(
        "📊 AI Interview Feedback"
    )

    feedback = (
        st.session_state.interview_feedback
    )

    st.markdown(
        feedback
    )


    # ---------------------------------------------
    # Extract score
    # ---------------------------------------------

    score_match = re.search(
        r"SCORE:\s*(\d+(?:\.\d+)?)",
        feedback,
        re.IGNORECASE
    )


    if score_match:

        score = float(
            score_match.group(1)
        )

        st.metric(
            "Interview Score",
            f"{score:.0f}/100"
        )


        # ---------------------------------------------
        # Save result
        # ---------------------------------------------

        if not st.session_state.get(
            "interview_saved",
            False
        ):

            saved = save_interview_result(
                user_id,
                topic,
                st.session_state.interview_question,
                answer,
                score,
                feedback
            )

            if saved:

                st.session_state.interview_saved = True

                st.success(
                    "Interview result saved successfully."
                )
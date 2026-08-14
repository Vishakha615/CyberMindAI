import json
import streamlit as st
from services.quiz_service import save_quiz
from services.rag_service import get_relevant_context
from services.content_generator import generate_quiz


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Quiz Generator | CyberMind AI",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# LOGIN
# =========================================================

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page(
            "pages/1_Login.py"
        )

    st.stop()


# =========================================================
# SESSION STATE
# =========================================================

if "ai_quiz" not in st.session_state:
    st.session_state.ai_quiz = None

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_score" not in st.session_state:
    st.session_state.quiz_score = {
        "total": 0,
        "correct": 0,
        "wrong": 0,
        "unanswered": 0,
        "percentage": 0
    }


# =========================================================
# HEADER
# =========================================================

st.title("🧠 AI Quiz Generator")

st.write(
    "Generate cybersecurity quizzes using "
    "RAG + Generative AI."
)

st.caption(
    "Questions are generated from the CyberMind "
    "cybersecurity knowledge base."
)

st.divider()


# =========================================================
# QUIZ SETTINGS
# =========================================================

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


# =========================================================
# GENERATE QUIZ
# =========================================================

if st.button(
    "✨ Generate Quiz",
    use_container_width=True
):

    with st.spinner(
        "Generating AI quiz..."
    ):

        try:

            # ---------------------------------------------
            # GET KNOWLEDGE FROM RAG
            # ---------------------------------------------

            context = get_relevant_context(
                topic,
                top_k=5
            )


            if not context.strip():

                st.warning(
                    "No relevant knowledge found "
                    "for this topic."
                )

                st.stop()


            # ---------------------------------------------
            # GENERATE QUIZ
            # ---------------------------------------------

            raw_quiz = generate_quiz(
                topic,
                difficulty,
                number_of_questions,
                context
            )


            if not raw_quiz:

                raise ValueError(
                    "AI returned an empty quiz."
                )


            # ---------------------------------------------
            # CLEAN RESPONSE
            # ---------------------------------------------

            raw_quiz = raw_quiz.strip()


            if raw_quiz.startswith(
                "```json"
            ):

                raw_quiz = raw_quiz[7:]


            elif raw_quiz.startswith(
                "```"
            ):

                raw_quiz = raw_quiz[3:]


            if raw_quiz.endswith(
                "```"
            ):

                raw_quiz = raw_quiz[:-3]


            raw_quiz = raw_quiz.strip()


            # ---------------------------------------------
            # PARSE JSON
            # ---------------------------------------------

            quiz = json.loads(
                raw_quiz
            )


            # ---------------------------------------------
            # CHECK LIST
            # ---------------------------------------------

            if not isinstance(
                quiz,
                list
            ):

                raise ValueError(
                    "AI did not return a JSON list."
                )


            # ---------------------------------------------
            # CHECK QUESTION COUNT
            # ---------------------------------------------

            if len(quiz) == 0:

                raise ValueError(
                    "AI returned no questions."
                )


            # =================================================
            # VALIDATE EVERY QUESTION
            # =================================================

            required_fields = [
                "question",
                "option_a",
                "option_b",
                "option_c",
                "option_d",
                "correct_answer",
                "explanation"
            ]


            for index, question in enumerate(
                quiz,
                start=1
            ):

                # -----------------------------------------
                # Check fields
                # -----------------------------------------

                for field in required_fields:

                    if field not in question:

                        raise ValueError(
                            f"Question {index} is missing "
                            f"'{field}'."
                        )


                # -----------------------------------------
                # Check question text
                # -----------------------------------------

                if not str(
                    question["question"]
                ).strip():

                    raise ValueError(
                        f"Question {index} is empty."
                    )


                # -----------------------------------------
                # Check options
                # -----------------------------------------

                for option in [
                    "option_a",
                    "option_b",
                    "option_c",
                    "option_d"
                ]:

                    if not str(
                        question[option]
                    ).strip():

                        raise ValueError(
                            f"Question {index} has "
                            f"an empty {option}."
                        )


                # -----------------------------------------
                # Normalize correct answer
                # -----------------------------------------

                correct_answer = str(
                    question["correct_answer"]
                ).strip().upper()


                # Remove common formatting

                correct_answer = (
                    correct_answer
                    .replace(".", "")
                    .replace(")", "")
                    .replace(":", "")
                    .strip()
                )


                # -----------------------------------------
                # Check correct answer
                # -----------------------------------------

                if correct_answer not in [
                    "A",
                    "B",
                    "C",
                    "D"
                ]:

                    raise ValueError(
                        f"Question {index} has invalid "
                        f"correct_answer: "
                        f"'{correct_answer}'. "
                        f"AI must return A, B, C or D."
                    )


                question[
                    "correct_answer"
                ] = correct_answer


                # -----------------------------------------
                # Check explanation
                # -----------------------------------------

                explanation = str(
                    question["explanation"]
                ).strip()


                if not explanation:

                    raise ValueError(
                        f"Question {index} has "
                        "an empty explanation."
                    )


                question[
                    "explanation"
                ] = explanation


            # =================================================
            # SAVE QUIZ
            # =================================================

            st.session_state.ai_quiz = quiz

            st.session_state.quiz_submitted = False

            st.session_state.quiz_score = {
                "total": 0,
                "correct": 0,
                "wrong": 0,
                "unanswered": 0,
                "percentage": 0
            }


            # ---------------------------------------------
            # Clear previous answers
            # ---------------------------------------------

            for index in range(
                1,
                11
            ):

                key = f"ai_q_{index}"

                if key in st.session_state:

                    del st.session_state[key]


            st.success(
                "🎉 Quiz generated successfully!"
            )


        except json.JSONDecodeError:

            st.error(
                "❌ AI returned an invalid quiz format."
            )

            st.info(
                "Please click Generate Quiz again."
            )


        except Exception as e:

            st.error(
                "❌ Unable to generate quiz."
            )

            st.error(
                str(e)
            )


# =========================================================
# DISPLAY QUIZ
# =========================================================

if st.session_state.ai_quiz:

    st.divider()

    st.subheader(
        f"🧠 {topic} Quiz"
    )

    st.info(
        "Select one answer for every question "
        "and then click Submit Quiz."
    )


    # =====================================================
    # QUESTIONS
    # =====================================================

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


        options = [
            f"A. {question['option_a']}",
            f"B. {question['option_b']}",
            f"C. {question['option_c']}",
            f"D. {question['option_d']}"
        ]


        st.radio(
            "Choose your answer:",
            options,
            key=f"ai_q_{index}"
        )


        st.divider()


    # =====================================================
    # SUBMIT QUIZ
    # =====================================================

    if st.button(
        "✅ Submit Quiz",
        use_container_width=True
    ):

        total = len(
            st.session_state.ai_quiz
        )

        correct = 0

        wrong = 0

        unanswered = 0


        # =================================================
        # CHECK ANSWERS
        # =================================================

        for index, question in enumerate(
            st.session_state.ai_quiz,
            start=1
        ):

            selected = st.session_state.get(
                f"ai_q_{index}"
            )


            # ---------------------------------------------
            # Unanswered
            # ---------------------------------------------

            if not selected:

                unanswered += 1

                continue


            # ---------------------------------------------
            # Extract selected letter
            # ---------------------------------------------

            selected_answer = (
                selected[0]
                .upper()
            )


            # ---------------------------------------------
            # Correct answer
            # ---------------------------------------------

            correct_answer = str(
                question.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()


            # ---------------------------------------------
            # Compare
            # ---------------------------------------------

            if (
                selected_answer
                == correct_answer
            ):

                correct += 1

            else:

                wrong += 1


        # =================================================
        # CALCULATE PERCENTAGE
        # =================================================

        if total > 0:

            percentage = (
                correct / total
            ) * 100

        else:

            percentage = 0


        # =================================================
        # SAVE SCORE
        # =================================================

        st.session_state.quiz_score = {

            "total": total,

            "correct": correct,

            "wrong": wrong,

            "unanswered": unanswered,

            "percentage": percentage
        }


        st.session_state.quiz_submitted = True


        st.rerun()


# =========================================================
# RESULTS
# =========================================================

if (
    st.session_state.quiz_submitted
    and st.session_state.ai_quiz
):

    score = st.session_state.get(
        "quiz_score",
        {}
    )


    total = score.get(
        "total",
        0
    )

    correct = score.get(
        "correct",
        0
    )

    wrong = score.get(
        "wrong",
        0
    )

    unanswered = score.get(
        "unanswered",
        0
    )

    percentage = score.get(
        "percentage",
        0
    )


    st.divider()

    st.subheader(
        "🎉 Quiz Result"
    )


    # =====================================================
    # SCORE CARDS
    # =====================================================

    col1, col2, col3, col4 = st.columns(4)


    with col1:

        st.metric(
            "Total",
            total
        )


    with col2:

        st.metric(
            "✅ Correct",
            correct
        )


    with col3:

        st.metric(
            "❌ Wrong",
            wrong
        )


    with col4:

        st.metric(
            "⚪ Unanswered",
            unanswered
        )


    # =====================================================
    # SCORE
    # =====================================================

    st.write(
        f"### 🏆 Score: {correct} / {total}"
    )

    st.write(
        f"**Percentage: {percentage:.0f}%**"
    )


    st.progress(
        min(
            max(
                percentage / 100,
                0
            ),
            1
        )
    )


    # =====================================================
    # PERFORMANCE
    # =====================================================

    if percentage >= 80:

        st.success(
            "🌟 Excellent! You have a strong "
            "understanding of this topic."
        )

    elif percentage >= 60:

        st.info(
            "👍 Good job! Keep practicing "
            "to improve your knowledge."
        )

    else:

        st.warning(
            "📚 Keep learning and try again "
            "to improve your score."
        )


    # =====================================================
    # ANSWER REVIEW
    # =====================================================

    st.divider()

    st.subheader(
        "📖 Answer Review"
    )


    for index, question in enumerate(
        st.session_state.ai_quiz,
        start=1
    ):

        st.markdown(
            f"## Question {index}"
        )


        st.write(
            question["question"]
        )


        # ---------------------------------------------
        # User answer
        # ---------------------------------------------

        selected = st.session_state.get(
            f"ai_q_{index}"
        )


        if selected:

            selected_answer = (
                selected[0]
                .upper()
            )

        else:

            selected_answer = None


        # ---------------------------------------------
        # Correct answer
        # ---------------------------------------------

        correct_answer = str(
            question.get(
                "correct_answer",
                ""
            )
        ).strip().upper()


        # ---------------------------------------------
        # Show result
        # ---------------------------------------------

        if (
            selected_answer
            == correct_answer
        ):

            st.success(
                f"✅ Your answer: "
                f"{selected_answer} — Correct!"
            )


        elif selected_answer is None:

            st.warning(
                "⚪ You did not answer this question."
            )


        else:

            st.error(
                f"❌ Your answer: "
                f"{selected_answer} — Wrong"
            )


        # =================================================
        # GET CORRECT ANSWER TEXT
        # =================================================

        if correct_answer == "A":

            correct_text = (
                question["option_a"]
            )

        elif correct_answer == "B":

            correct_text = (
                question["option_b"]
            )

        elif correct_answer == "C":

            correct_text = (
                question["option_c"]
            )

        elif correct_answer == "D":

            correct_text = (
                question["option_d"]
            )

        else:

            correct_text = (
                "Correct answer unavailable."
            )


        # =================================================
        # CORRECT ANSWER
        # =================================================

        st.info(
            f"✅ **Correct answer:** "
            f"{correct_answer}. "
            f"{correct_text}"
        )


        # =================================================
        # EXPLANATION
        # =================================================

        explanation = str(
            question.get(
                "explanation",
                ""
            )
        ).strip()


        if explanation:

            st.markdown(
                f"💡 **Explanation:** "
                f"{explanation}"
            )

        else:

            st.warning(
                "💡 Explanation is not available."
            )


        st.divider()


    # =====================================================
    # NEW QUIZ
    # =====================================================

    if st.button(
        "🔄 Generate New Quiz",
        use_container_width=True
    ):

        st.session_state.ai_quiz = None

        st.session_state.quiz_submitted = False

        st.session_state.quiz_score = {
            "total": 0,
            "correct": 0,
            "wrong": 0,
            "unanswered": 0,
            "percentage": 0
        }


        # Clear answers

        for index in range(
            1,
            11
        ):

            key = f"ai_q_{index}"

            if key in st.session_state:

                del st.session_state[key]


        st.rerun()

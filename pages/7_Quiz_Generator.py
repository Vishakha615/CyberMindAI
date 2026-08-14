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











'''import json
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


            # Validate quiz format

            for question in quiz:
                required_keys = [
                    "question",
                    "option_a",
                    "option_b",
                    "option_c",
                    "option_d",
                    "correct_answer",
                    "explanation"
                    ]

            for key in required_keys:

                if key not in question:

                    raise ValueError(
                        f"Quiz question is missing required field: {key}"
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
    unanswered = 0

    for index, question in enumerate(
        st.session_state.ai_quiz,
        start=1
    ):

        selected = st.session_state.get(
            f"ai_q_{index}"
        )

        # No answer selected
        if not selected:

            unanswered += 1
            continue

        # Get A/B/C/D from user's selected option
        selected_answer = selected.split(".")[0].strip().upper()

        # Get correct answer safely
        correct_answer = str(
            question.get("correct_answer", "")
        ).strip().upper()

        # Compare
        if selected_answer == correct_answer:

            correct += 1

        else:

            wrong += 1


    total = len(
        st.session_state.ai_quiz
    )

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
st.subheader("📖 Answer Review")

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

    selected = st.session_state.get(
        f"ai_q_{index}"
    )

    if selected:

        selected_answer = (
            selected.split(".")[0]
            .strip()
            .upper()
        )

    else:

        selected_answer = "Not answered"


    correct_answer = str(
        question.get(
            "correct_answer",
            ""
        )
    ).strip().upper()


    explanation = question.get(
        "explanation",
        "No explanation was provided."
    )


    # -------------------------------------------------
    # RESULT
    # -------------------------------------------------

    if selected_answer == correct_answer:

        st.success(
            f"✅ Your answer: {selected_answer} — Correct!"
        )

    elif selected_answer == "Not answered":

        st.warning(
            "⚠️ You did not answer this question."
        )

    else:

        st.error(
            f"❌ Your answer: {selected_answer} — Wrong"
        )


    st.info(
        f"✅ Correct answer: {correct_answer}"
    )


    st.write(
        f"💡 **Explanation:** {explanation}"
    )


    st.divider()

        st.divider()'''






import json
import streamlit as st

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
# LOGIN CHECK
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

    with st.spinner("Generating AI quiz..."):

        try:

            # ---------------------------------------------
            # GET RAG CONTEXT
            # ---------------------------------------------

            context = get_relevant_context(
                topic,
                top_k=5
            )


            if not context:

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


            # ---------------------------------------------
            # CLEAN GEMINI RESPONSE
            # ---------------------------------------------

            raw_quiz = raw_quiz.strip()


            if raw_quiz.startswith("```json"):

                raw_quiz = raw_quiz[7:]

                if raw_quiz.endswith("```"):
                    raw_quiz = raw_quiz[:-3]


            elif raw_quiz.startswith("```"):

                raw_quiz = raw_quiz[3:]

                if raw_quiz.endswith("```"):
                    raw_quiz = raw_quiz[:-3]


            raw_quiz = raw_quiz.strip()


            # ---------------------------------------------
            # CONVERT JSON
            # ---------------------------------------------

            quiz = json.loads(raw_quiz)


            # ---------------------------------------------
            # VALIDATE QUIZ
            # ---------------------------------------------

            if not isinstance(quiz, list):

                raise ValueError(
                    "Invalid quiz format."
                )


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

                for field in required_fields:

                    if field not in question:

                        raise ValueError(
                            f"Question {index} is missing "
                            f"'{field}'."
                        )


                # Normalize correct answer

                correct_answer = str(
                    question["correct_answer"]
                ).strip().upper()


                # Accept formats such as:
                # A
                # A.
                # A) Answer

                if correct_answer.startswith("A"):
                    correct_answer = "A"

                elif correct_answer.startswith("B"):
                    correct_answer = "B"

                elif correct_answer.startswith("C"):
                    correct_answer = "C"

                elif correct_answer.startswith("D"):
                    correct_answer = "D"

                else:

                    raise ValueError(
                        f"Question {index} has an "
                        f"invalid correct answer."
                    )


                question["correct_answer"] = (
                    correct_answer
                )


                # Make sure explanation exists

                if not str(
                    question["explanation"]
                ).strip():

                    question["explanation"] = (
                        "No explanation was provided."
                    )


            # ---------------------------------------------
            # SAVE QUIZ
            # ---------------------------------------------

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
            # REMOVE OLD ANSWERS
            # ---------------------------------------------

            for index in range(1, 11):

                key = f"ai_q_{index}"

                if key in st.session_state:

                    del st.session_state[key]


            st.success(
                "🎉 Quiz generated successfully!"
            )


        except json.JSONDecodeError:

            st.error(
                "Gemini returned an invalid quiz format."
            )


        except Exception as e:

            st.error(
                "Unable to generate quiz."
            )

            st.exception(e)


# =========================================================
# DISPLAY QUIZ
# =========================================================

if st.session_state.ai_quiz:

    st.divider()

    st.subheader(
        f"🧠 {topic} Quiz"
    )

    st.info(
        "Select one answer for each question "
        "and click Submit Quiz."
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
    # SUBMIT BUTTON
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


        # ---------------------------------------------
        # CHECK ANSWERS
        # ---------------------------------------------

        for index, question in enumerate(
            st.session_state.ai_quiz,
            start=1
        ):

            selected = st.session_state.get(
                f"ai_q_{index}"
            )


            # No answer

            if not selected:

                unanswered += 1

                continue


            # -----------------------------------------
            # Extract selected letter
            # -----------------------------------------

            selected_answer = (
                selected
                .split(".", 1)[0]
                .strip()
                .upper()
            )


            # -----------------------------------------
            # Get correct answer
            # -----------------------------------------

            correct_answer = str(
                question.get(
                    "correct_answer",
                    ""
                )
            ).strip().upper()


            # -----------------------------------------
            # Compare
            # -----------------------------------------

            if selected_answer == correct_answer:

                correct += 1

            else:

                wrong += 1


        # =================================================
        # CALCULATE PERCENTAGE
        # =================================================

        percentage = 0

        if total > 0:

            percentage = (
                correct / total
            ) * 100


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


        # Force Streamlit to rerun and show result

        st.rerun()


# =========================================================
# RESULT SECTION
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


    # Progress bar

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
    # PERFORMANCE MESSAGE
    # =====================================================

    if percentage >= 80:

        st.success(
            "🌟 Excellent! You have a strong "
            "understanding of this topic."
        )

    elif percentage >= 60:

        st.info(
            "👍 Good job! Keep practicing "
            "to improve your score."
        )

    else:

        st.warning(
            "📚 Keep learning and try the quiz "
            "again to improve your understanding."
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
            f"### Question {index}"
        )


        st.write(
            question["question"]
        )


        # ---------------------------------------------
        # USER ANSWER
        # ---------------------------------------------

        selected = st.session_state.get(
            f"ai_q_{index}"
        )


        if selected:

            selected_answer = (
                selected
                .split(".", 1)[0]
                .strip()
                .upper()
            )

        else:

            selected_answer = None


        # ---------------------------------------------
        # CORRECT ANSWER
        # ---------------------------------------------

        correct_answer = str(
            question.get(
                "correct_answer",
                ""
            )
        ).strip().upper()


        # ---------------------------------------------
        # SHOW RESULT
        # ---------------------------------------------

        if selected_answer == correct_answer:

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


        # ---------------------------------------------
        # CORRECT ANSWER
        # ---------------------------------------------

        correct_text = ""

        if correct_answer == "A":

            correct_text = question["option_a"]

        elif correct_answer == "B":

            correct_text = question["option_b"]

        elif correct_answer == "C":

            correct_text = question["option_c"]

        elif correct_answer == "D":

            correct_text = question["option_d"]


        st.info(
            f"✅ Correct answer: "
            f"{correct_answer}. {correct_text}"
        )


        # ---------------------------------------------
        # EXPLANATION
        # ---------------------------------------------

        explanation = question.get(
            "explanation",
            "No explanation was provided."
        )


        st.markdown(
            f"💡 **Explanation:** {explanation}"
        )


        st.divider()


    # =====================================================
    # RETAKE QUIZ
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


        for index in range(1, 11):

            key = f"ai_q_{index}"

            if key in st.session_state:

                del st.session_state[key]


        st.rerun()

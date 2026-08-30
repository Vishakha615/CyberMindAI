'''import streamlit as st

from services.quiz_service import (
    get_quiz_questions,
    save_quiz_result
)
import streamlit as st

st.markdown(
    """
    <style>
    /* Hide Streamlit default page navigation */
    [data-testid="stSidebarNav"] {
        display: none;
    }
    </style>
    """,
    unsafe_allow_html=True
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

            st.session_state.quiz_started = False'''








import streamlit as st
from ui.styles import apply_custom_css
from ui.components import (
    show_header,
    show_card,
    show_section_title
)
from services.quiz_service import (
    get_quiz_questions,
    save_quiz_result
)


st.set_page_config(
    page_title="Quiz | CyberMind AI",
    page_icon="🧠",
    layout="wide"
)


# =========================================================
# LOGIN
# =========================================================

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


# =========================================================
# SESSION STATE
# =========================================================

if "quiz_started" not in st.session_state:
    st.session_state.quiz_started = False

if "quiz_submitted" not in st.session_state:
    st.session_state.quiz_submitted = False

if "quiz_questions" not in st.session_state:
    st.session_state.quiz_questions = []

if "quiz_answers" not in st.session_state:
    st.session_state.quiz_answers = {}


st.markdown(
        """
        <style>

        /* =========================
           SIDEBAR
           ========================= */

        [data-testid="stSidebar"] {

             background:
                linear-gradient(
                    180deg,
                    #0C1430,
                    #070E29
                );

            border-right:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.08
                );
        }

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #050816 0%,
                    #0b1026 50%,
                    #111936 100%
                );
        }
        </style>
        """,
        unsafe_allow_html=True
    )




# =========================================================
# HEADER
# =========================================================

st.title("🧠 Cybersecurity Quiz")

st.write(
    "Test your cybersecurity knowledge and "
    "track your learning progress."
)

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.markdown(
        "## 🛡️ CyberMind AI"
    )

    st.caption(
        "AI-Powered Cybersecurity Learning"
    )

    st.divider()

    st.markdown(
        "### 🧭 Navigation"
    )

    st.page_link(
        "app.py",
        label="🏠 Dashboard"
    )

    st.page_link(
        "pages/5_AI_Mentor.py",
        label="🤖 AI Mentor"
    )

    st.page_link(
        "pages/6_Notes_Generator.py",
        label="📚 Notes Generator"
    )

    st.page_link(
        "pages/7_Quiz_Generator.py",
        label="📝 Quiz Generator"
    )

    st.page_link(
        "pages/8_Roadmap.py",
        label="🗺️ Learning Roadmap"
    )

    st.page_link(
        "pages/9_Threat_Analyzer.py",
        label="🛡️ Threat Analyzer"
    )

    st.page_link(
        "pages/10_Cyber_Labs.py",
        label="🧪 Cyber Labs"
    )

    st.page_link(
        "pages/11_Interview.py",
        label="🎤 AI Interview"
    )

    st.divider()

    st.page_link(
        "pages/3_Profile.py",
        label="👤 Profile"
    )



# =========================================================
# QUIZ SETTINGS
# =========================================================

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


# =========================================================
# START QUIZ
# =========================================================

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
            "No questions available for this "
            "topic and difficulty."
        )

    else:

        st.session_state.quiz_questions = questions

        st.session_state.quiz_started = True

        st.session_state.quiz_submitted = False

        st.session_state.quiz_answers = {}

        # Clear old radio answers
        for question in questions:

            key = f"question_{question['question_id']}"

            if key in st.session_state:

                del st.session_state[key]

        st.rerun()


# =========================================================
# DISPLAY QUIZ
# =========================================================

if st.session_state.quiz_started:

    questions = st.session_state.quiz_questions

    st.divider()

    st.subheader(
        f"📚 {topic}"
    )


    # =====================================================
    # QUESTIONS
    # =====================================================

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
            list(options.keys()),
            format_func=lambda x:
                f"{x}. {options[x]}",
            key=f"question_{question['question_id']}"
        )


        st.session_state.quiz_answers[
            question["question_id"]
        ] = selected


        st.divider()


    # =====================================================
    # SUBMIT QUIZ
    # =====================================================

    if not st.session_state.quiz_submitted:

        if st.button(
            "✅ Submit Quiz",
            use_container_width=True
        ):

            correct_answers = 0

            total_questions = len(
                questions
            )


            # -------------------------------------------------
            # CHECK ANSWERS
            # -------------------------------------------------

            for question in questions:

                question_id = question[
                    "question_id"
                ]

                user_answer = (
                    st.session_state.quiz_answers
                    .get(question_id)
                )


                correct_answer = (
                    question["correct_option"]
                    .strip()
                    .upper()
                )


                if (
                    user_answer
                    and
                    user_answer.upper()
                    == correct_answer
                ):

                    correct_answers += 1


            # -------------------------------------------------
            # SAVE RESULT
            # -------------------------------------------------

            saved = save_quiz_result(
                user_id,
                topic,
                total_questions,
                correct_answers
            )


            if saved:

                st.session_state.quiz_submitted = True

                st.session_state.quiz_score = {
                    "correct": correct_answers,
                    "total": total_questions
                }

                st.rerun()

            else:

                st.error(
                    "❌ Quiz result could not be saved."
                )


# =========================================================
# RESULT
# =========================================================

if (
    st.session_state.quiz_submitted
    and st.session_state.quiz_questions
):

    questions = st.session_state.quiz_questions

    score = st.session_state.quiz_score

    correct_answers = score["correct"]

    total_questions = score["total"]

    percentage = (
        correct_answers /
        total_questions
    ) * 100


    st.divider()

    st.subheader(
        "🎉 Quiz Result"
    )


    # =====================================================
    # SCORE
    # =====================================================

    col1, col2, col3 = st.columns(3)


    with col1:

        st.metric(
            "Score",
            f"{percentage:.1f}%"
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


    if percentage >= 80:

        st.success(
            "🔥 Excellent! You have a strong "
            "understanding of this topic."
        )

    elif percentage >= 50:

        st.warning(
            "👍 Good attempt! Review the topic "
            "and keep practicing."
        )

    else:

        st.error(
            "📚 You should revise this topic "
            "before trying again."
        )


    # =====================================================
    # ANSWER REVIEW
    # =====================================================

    st.divider()

    st.subheader(
        "📖 Answer Review"
    )


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


        question_id = question[
            "question_id"
        ]


        user_answer = (
            st.session_state.quiz_answers
            .get(question_id)
        )


        correct_answer = (
            question["correct_option"]
            .strip()
            .upper()
        )


        options = {
            "A": question["option_a"],
            "B": question["option_b"],
            "C": question["option_c"],
            "D": question["option_d"]
        }


        # =================================================
        # CORRECT
        # =================================================

        if (
            user_answer
            and
            user_answer.upper()
            == correct_answer
        ):

            st.success(
                f"✅ Correct! "
                f"You selected {user_answer}. "
                f"The correct answer is "
                f"{correct_answer}."
            )


        # =================================================
        # WRONG
        # =================================================

        else:

            st.error(
                f"❌ Wrong! "
                f"You selected "
                f"{user_answer if user_answer else 'No answer'}."
            )


            st.info(
                f"✅ Correct answer: "
                f"{correct_answer}. "
                f"{options[correct_answer]}"
            )


        # =================================================
        # SHOW CORRECT ANSWER FOR CORRECT TOO
        # =================================================

        if (
            user_answer
            and
            user_answer.upper()
            == correct_answer
        ):

            st.info(
                f"💡 Correct answer: "
                f"{correct_answer}. "
                f"{options[correct_answer]}"
            )


        st.divider()


    # =====================================================
    # NEW QUIZ
    # =====================================================

    if st.button(
        "🔄 Take Another Quiz",
        use_container_width=True
    ):

        st.session_state.quiz_started = False

        st.session_state.quiz_submitted = False

        st.session_state.quiz_questions = []

        st.session_state.quiz_answers = {}

        st.session_state.quiz_score = {
            "correct": 0,
            "total": 0
        }

        st.rerun()

import streamlit as st

from services.recommendation_service import (
    get_topic_performance,
    get_recommendation_message
)


st.set_page_config(
    page_title="Learning Roadmap | CyberMind AI",
    page_icon="🗺️",
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
    "🗺️ Personalized Learning Roadmap"
)

st.write(
    "CyberMind AI analyzes your quiz "
    "performance and recommends what "
    "you should study next."
)


# ---------------------------------------------------------
# PERFORMANCE
# ---------------------------------------------------------

performance = get_topic_performance(
    user_id
)


if not performance:

    st.info(
        "📚 Complete some quizzes first. "
        "Your personalized roadmap will "
        "appear here."
    )

    st.stop()


# ---------------------------------------------------------
# RECOMMENDATION
# ---------------------------------------------------------

st.subheader(
    "🤖 AI Learning Recommendation"
)

st.markdown(
    get_recommendation_message(
        user_id
    )
)


# ---------------------------------------------------------
# TOPIC PERFORMANCE
# ---------------------------------------------------------

st.divider()

st.subheader(
    "📊 Your Topic Performance"
)


for item in performance:

    topic = item["topic"]

    score = float(
        item["average_score"]
    )

    attempts = item["attempts"]


    st.write(
        f"**{topic}**"
    )

    st.progress(
        min(score / 100, 1.0)
    )

    st.caption(
        f"Average Score: {score:.1f}% "
        f"| Attempts: {attempts}"
    )
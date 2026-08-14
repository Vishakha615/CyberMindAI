'''import streamlit as st

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
    )'''





'''import streamlit as st

from services.recommendation_service import (
    get_topic_performance,
    get_recommendation_message
)


st.set_page_config(
    page_title="Learning Roadmap | CyberMind AI",
    page_icon="🗺️",
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


user_id = st.session_state.user_id


# =========================================================
# HEADER
# =========================================================

st.title("🗺️ Personalized Learning Roadmap")

st.write(
    "CyberMind AI analyzes your quiz performance "
    "and recommends what you should study next."
)


st.divider()


# =========================================================
# GET PERFORMANCE
# =========================================================

performance = get_topic_performance(user_id)


if not performance:

    st.info(
        "📚 Complete some quizzes first. "
        "Your personalized roadmap will appear here."
    )

    st.stop()


# =========================================================
# CALCULATE OVERALL SCORE
# =========================================================

total_score = 0

for item in performance:

    total_score += float(
        item["average_score"]
    )


overall_score = total_score / len(performance)


# =========================================================
# OVERVIEW CARDS
# =========================================================

st.subheader("📊 Learning Overview")

col1, col2, col3 = st.columns(3)


with col1:

    st.metric(
        "Overall Score",
        f"{overall_score:.1f}%"
    )


with col2:

    st.metric(
        "Topics Studied",
        len(performance)
    )


with col3:

    total_attempts = sum(
        item["attempts"]
        for item in performance
    )

    st.metric(
        "Quiz Attempts",
        total_attempts
    )


st.divider()


# =========================================================
# CLASSIFY TOPICS
# =========================================================

weak_topics = []
practice_topics = []
strong_topics = []


for item in performance:

    topic = item["topic"]

    score = float(
        item["average_score"]
    )

    if score < 50:

        weak_topics.append(
            (topic, score)
        )

    elif score < 75:

        practice_topics.append(
            (topic, score)
        )

    else:

        strong_topics.append(
            (topic, score)
        )


# =========================================================
# AI RECOMMENDATION
# =========================================================

st.subheader("🤖 AI Learning Recommendation")

recommendation = get_recommendation_message(
    user_id
)

st.info(
    recommendation
)


st.divider()


# =========================================================
# PERSONALIZED ROADMAP
# =========================================================

st.subheader("🗺️ Your Learning Path")

st.write(
    "Follow this roadmap based on your quiz performance."
)


# ---------------------------------------------------------
# STEP 1 — WEAK TOPICS
# ---------------------------------------------------------

if weak_topics:

    st.markdown(
        "### 🔴 Step 1 — Focus on These Topics"
    )

    st.caption(
        "These topics need the most improvement."
    )

    for topic, score in weak_topics:

        with st.container(border=True):

            st.markdown(
                f"### 📕 {topic}"
            )

            st.progress(
                min(score / 100, 1.0)
            )

            st.write(
                f"Current average: **{score:.1f}%**"
            )

            st.write(
                "📚 Recommended action: "
                "Review your notes and practice "
                "more questions on this topic."
            )


# ---------------------------------------------------------
# STEP 2 — PRACTICE TOPICS
# ---------------------------------------------------------

if practice_topics:

    st.markdown(
        "### 🟡 Step 2 — Practice More"
    )

    st.caption(
        "You understand these topics but need more practice."
    )

    for topic, score in practice_topics:

        with st.container(border=True):

            st.markdown(
                f"### 📘 {topic}"
            )

            st.progress(
                min(score / 100, 1.0)
            )

            st.write(
                f"Current average: **{score:.1f}%**"
            )

            st.write(
                "🧠 Recommended action: "
                "Practice quizzes and revise key concepts."
            )


# ---------------------------------------------------------
# STEP 3 — STRONG TOPICS
# ---------------------------------------------------------

if strong_topics:

    st.markdown(
        "### 🟢 Step 3 — Strong Topics"
    )

    st.caption(
        "Great work! You are performing well here."
    )

    for topic, score in strong_topics:

        with st.container(border=True):

            st.markdown(
                f"### 📗 {topic}"
            )

            st.progress(
                min(score / 100, 1.0)
            )

            st.write(
                f"Average score: **{score:.1f}%**"
            )

            st.write(
                "⭐ Recommended action: "
                "Maintain your knowledge and move "
                "to more advanced concepts."
            )


st.divider()


# =========================================================
# TOPIC PERFORMANCE
# =========================================================

st.subheader("📈 Detailed Topic Performance")


for item in performance:

    topic = item["topic"]

    score = float(
        item["average_score"]
    )

    attempts = item["attempts"]


    st.markdown(
        f"**{topic}**"
    )

    st.progress(
        min(score / 100, 1.0)
    )

    st.caption(
        f"Average Score: {score:.1f}% "
        f"| Attempts: {attempts}"
    )'''




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
# HEADER
# =========================================================

st.title(
    "🗺️ Personalized Learning Roadmap"
)

st.write(
    "CyberMind AI analyzes your quiz performance "
    "and recommends what you should study next."
)

st.divider()


# =========================================================
# GET PERFORMANCE
# =========================================================

performance = get_topic_performance(
    user_id
)


# =========================================================
# NO QUIZ DATA
# =========================================================

if not performance:

    st.info(
        "📚 Complete some quizzes first. "
        "Your personalized roadmap will appear here."
    )

    st.stop()


# =========================================================
# OVERALL STATISTICS
# =========================================================

total_attempts = sum(
    int(item["attempts"])
    for item in performance
)


average_score = sum(
    float(item["average_score"])
    for item in performance
) / len(performance)


strongest = max(
    performance,
    key=lambda x:
    float(x["average_score"])
)


weakest = min(
    performance,
    key=lambda x:
    float(x["average_score"])
)


# =========================================================
# DASHBOARD
# =========================================================

st.subheader(
    "📊 Your Learning Progress"
)


col1, col2, col3, col4 = st.columns(4)


with col1:

    st.metric(
        "Topics Practiced",
        len(performance)
    )


with col2:

    st.metric(
        "Quiz Attempts",
        total_attempts
    )


with col3:

    st.metric(
        "Average Score",
        f"{average_score:.1f}%"
    )


with col4:

    st.metric(
        "Strongest Topic",
        strongest["topic"]
    )


st.divider()


# =========================================================
# AI RECOMMENDATION
# =========================================================

st.subheader(
    "🤖 AI Learning Recommendation"
)


recommendation = get_recommendation_message(
    user_id
)


st.markdown(
    recommendation
)


st.divider()


# =========================================================
# TOPIC PERFORMANCE
# =========================================================

st.subheader(
    "📚 Topic Performance"
)


for item in performance:

    topic = item["topic"]

    score = float(
        item["average_score"]
    )

    attempts = int(
        item["attempts"]
    )


    if score >= 80:

        status = "🟢 Strong"

    elif score >= 50:

        status = "🟡 Needs Practice"

    else:

        status = "🔴 Needs Improvement"


    st.markdown(
        f"### {topic}"
    )


    st.progress(
        min(
            max(
                score / 100,
                0
            ),
            1
        )
    )


    st.write(
        f"**{score:.1f}%** — {status}"
    )


    st.caption(
        f"Quiz attempts: {attempts}"
    )


    st.divider()


# =========================================================
# NEXT LEARNING STEP
# =========================================================

st.subheader(
    "🎯 What Should You Study Next?"
)


weakest_topic = weakest["topic"]

weakest_score = float(
    weakest["average_score"]
)


if weakest_score < 50:

    st.error(
        f"📖 Focus on **{weakest_topic}** first."
    )

    st.write(
        "Your current performance is below 50%. "
        "Review the fundamentals and practice "
        "more beginner questions."
    )


elif weakest_score < 75:

    st.warning(
        f"📖 Practice **{weakest_topic}** next."
    )

    st.write(
        "You have a basic understanding, but "
        "more practice will improve your score."
    )


else:

    st.success(
        "🚀 You're doing well across your topics!"
    )

    st.write(
        "You can start exploring more advanced "
        "cybersecurity concepts."
    )

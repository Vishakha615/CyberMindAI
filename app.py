import streamlit as st

from ui.styles import apply_custom_css
from ui.components import (
    show_header,
    
    show_section_title
)


import streamlit as st
import base64
from pathlib import Path
from textwrap import dedent


def image_to_base64(image_path):

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


def show_card(title, value, image_path, card_class):

    image_base64 = image_to_base64(image_path)

    html = dedent(f"""
    <div class="dashboard-card {card_class}"
         style="background-image:
         linear-gradient(
             rgba(5, 12, 35, 0.30),
             rgba(5, 12, 35, 0.90)
         ),
         url('data:image/png;base64,{image_base64}');">

        

    </div>
    """)

    st.markdown(
        html,
        unsafe_allow_html=True
    )
st.markdown(
    """
    <style>

    .dashboard-card {
        height: 100%;
        width: 100%;
        border-radius: 20px;

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;

        position: relative;
        overflow: hidden;

        border: 1px solid rgba(100, 150, 255, 0.4);

        transition: all 0.35s ease;

        box-shadow:
            0 8px 25px rgba(0, 0, 0, 0.35);
    }


    .dashboard-card:hover {
        transform: translateY(-8px) scale(1.02);

        border-color: #4da6ff;

        box-shadow:
            0 18px 45px rgba(40, 120, 255, 0.45);
    }


    .quiz-card:hover {
        box-shadow:
            0 18px 45px rgba(0, 120, 255, 0.55);
    }


    .labs-card:hover {
        box-shadow:
            0 18px 45px rgba(130, 70, 255, 0.55);
    }


    .interview-card:hover {
        box-shadow:
            0 18px 45px rgba(255, 120, 30, 0.55);
    }


    .streak-card:hover {
        box-shadow:
            0 18px 45px rgba(0, 200, 255, 0.55);
    }


    .card-content {
        position: absolute;

        left: 0;
        right: 0;
        bottom: 0;

        padding: 25px;

        background: linear-gradient(
            transparent,
            rgba(2, 7, 25, 0.95)
        );
    }


    .card-title {
        color: white;

        font-size: 20px;

        font-weight: 700;

        margin-bottom: 10px;
    }


    .card-value {
        color: white;

        font-size: 45px;

        font-weight: 800;

        line-height: 1.1;
    }

    </style>
    """,
    unsafe_allow_html=True
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


st.markdown("""
<style>

div.stButton > button {
    width: 100%;
    background-color: #232C5C;
    color: white;
    border: 1px solid #3C457A;
    border-radius: 8px;
    padding: 12px 20px;
    font-size: 16px;
    font-weight: 600;
    transition: all 0.3s ease;
}

div.stButton > button:hover {
    background-color: #3C457A;
    color: #06111f;
    border-color: #3C457A;
}

div.stButton > button:active {
    transform: scale(0.98);
}

</style>
""", unsafe_allow_html=True)


st.set_page_config(
    page_title="CyberMind AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page("pages/1_Login.py")

    st.stop()


user_id = st.session_state.user_id

# ---------------------------------------------------------
# CSS
# ---------------------------------------------------------

apply_custom_css()


# ---------------------------------------------------------
# SESSION
# ---------------------------------------------------------

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


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
    st.page_link(
        "pages/1_Login.py",
        label="🚪 Logout"
    )

# ---------------------------------------------------------
# DASHBOARD
# ---------------------------------------------------------

show_header()

st.success(f"Welcome, {st.session_state.get('full_name', '')} 👋")

st.divider()

show_section_title(
    "📊 Your Learning Overview",
    "Track your cybersecurity learning journey."
)




col1, col2, col3, col4 = st.columns(4)

with col1:
    show_card(
        "Quiz Score",
        "85%",
        "assets/quiz.png",
        "quiz-card"
    )

with col2:
    show_card(
        "Labs Completed",
        "4",
        "assets/labs.png",
        "labs-card"
    )

with col3:
    show_card(
        "Interview Score",
        "78%",
        "assets/interview.png",
        "interview-card"
    )

with col4:
    show_card(
        "Learning Streak",
        "7 Days",
        "assets/streak.png",
        "streak-card"
    )




# ---------------------------------------------------------
# AI RECOMMENDATION
# ---------------------------------------------------------

st.divider()


show_section_title(
    "🎯 AI Recommendation",
    "Personalized guidance based on your learning activity."
)


st.markdown(
    """
    <div class="cyber-card">

    <h3>🧠 Focus on Network Security</h3>

    <p style="color:#a8b2d1;">
    Your recent quiz and lab performance suggests
    that Network Security is a good topic to revise next.
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# QUICK ACTIONS
# ---------------------------------------------------------

st.divider()
show_section_title(
    "⚡ Quick Actions"
)


col1, col2, col3 = st.columns(3)


with col1:

    if st.button(
        "🤖 Ask AI Mentor",
        use_container_width=True
    ):

        st.switch_page(
            "pages/5_AI_Mentor.py"
        )


with col2:

    if st.button(
        "🛡️ Analyze Threat",
        use_container_width=True
    ):

        st.switch_page(
            "pages/9_Threat_Analyzer.py"
        )


with col3:

    if st.button(
        "🧪 Start Cyber Lab",
        use_container_width=True
    ):

        st.switch_page(
            "pages/10_Cyber_Labs.py"
        )

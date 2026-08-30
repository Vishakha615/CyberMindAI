import streamlit as st

from services.profile_service import (
    get_student_profile,
    update_student_profile
)


st.set_page_config(
    page_title="Profile | CyberMind AI",
    page_icon="👤",
    layout="wide"
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



div.stButton > button:active {
    transform: scale(0.98);
}

</style>
""", unsafe_allow_html=True)



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


# ---------------------------------------------------------
# CHECK LOGIN
# ---------------------------------------------------------

if not st.session_state.get("logged_in", False):

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page("pages/1_Login.py")

    st.stop()


# ---------------------------------------------------------
# GET USER
# ---------------------------------------------------------

user_id = st.session_state.user_id

profile = get_student_profile(user_id)


if profile is None:

    st.error("Unable to load your profile.")
    st.stop()


# ---------------------------------------------------------
# PAGE
# ---------------------------------------------------------

st.title("👤 My Profile")

st.caption(
    "Complete your profile to receive personalized "
    "CyberMind AI recommendations."
)

st.divider()


# ---------------------------------------------------------
# BASIC INFORMATION
# ---------------------------------------------------------

st.subheader("👋 Personal Information")

col1, col2 = st.columns(2)

with col1:

    st.text_input(
        "Full Name",
        value=profile["full_name"],
        disabled=True
    )

with col2:

    st.text_input(
        "Email",
        value=profile["email"],
        disabled=True
    )


st.divider()


# ---------------------------------------------------------
# LEARNING INFORMATION
# ---------------------------------------------------------

st.subheader("🎓 Learning Information")

education_options = [
    "Diploma",
    "Undergraduate",
    "Postgraduate",
    "Other"
]

experience_options = [
    "Beginner",
    "Intermediate",
    "Advanced"
]

career_options = [
    "Cybersecurity Analyst",
    "SOC Analyst",
    "Security Engineer",
    "Ethical Hacking",
    "Digital Forensics",
    "Cloud Security",
    "General Cybersecurity"
]


current_education = profile["education_level"]

if current_education not in education_options:
    current_education = education_options[0]


current_experience = profile["experience_level"]

if current_experience not in experience_options:
    current_experience = experience_options[0]


current_goal = profile["career_goal"]

if current_goal not in career_options:
    current_goal = career_options[0]


col1, col2 = st.columns(2)

with col1:

    education = st.selectbox(
        "Education Level",
        education_options,
        index=education_options.index(
            current_education
        )
    )

with col2:

    experience = st.selectbox(
        "Cybersecurity Experience",
        experience_options,
        index=experience_options.index(
            current_experience
        )
    )


career_goal = st.selectbox(
    "Career Goal",
    career_options,
    index=career_options.index(
        current_goal
    )
)


# ---------------------------------------------------------
# SAVE
# ---------------------------------------------------------

if st.button(
    "💾 Save Profile",
    use_container_width=True
):

    success, message = update_student_profile(
        user_id,
        education,
        experience,
        career_goal
    )

    if success:

        st.success(message)

        st.rerun()

    else:

        st.error(message)

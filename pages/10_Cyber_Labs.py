import streamlit as st
from ui.styles import apply_custom_css
from ui.components import (
    show_header,
    show_card,
    show_section_title
)
from services.lab_service import (
    get_labs,
    save_lab_result,
    get_completed_labs
)


st.set_page_config(
    page_title="Cyber Labs | CyberMind AI",
    page_icon="🧪",
    layout="wide"
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
    "🧪 Cybersecurity Labs"
)

st.divider()

st.write(
    "Practice cybersecurity concepts through "
    "safe, educational scenarios."
)


completed = get_completed_labs(
    user_id
)

st.metric(
    "Labs Completed",
    completed
)


# ---------------------------------------------------------
# LOAD LABS
# ---------------------------------------------------------

labs = get_labs()


if not labs:

    st.info(
        "No labs are available yet."
    )

    st.stop()


# ---------------------------------------------------------
# SELECT LAB
# ---------------------------------------------------------

lab_names = [
    lab["title"]
    for lab in labs
]


selected_name = st.selectbox(
    "Select a Lab",
    lab_names
)


selected_lab = next(
    lab
    for lab in labs
    if lab["title"] == selected_name
)




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
# LAB DETAILS
# ---------------------------------------------------------

st.divider()

st.subheader(
    selected_lab["title"]
)

st.caption(
    f"Topic: {selected_lab['topic']} "
    f"| Difficulty: {selected_lab['difficulty']}"
)

st.write(
    selected_lab["description"]
)


st.info(
    selected_lab["question"]
)


options = {
    "A": selected_lab["option_a"],
    "B": selected_lab["option_b"],
    "C": selected_lab["option_c"],
    "D": selected_lab["option_d"]
}


answer = st.radio(
    "Choose your answer:",
    list(options.keys()),
    format_func=lambda key:
        f"{key}. {options[key]}"
)


# ---------------------------------------------------------
# SUBMIT
# ---------------------------------------------------------

if st.button(
    "✅ Submit Lab",
    use_container_width=True
):

    if answer == selected_lab[
        "correct_option"
    ]:

        score = 100

        st.success(
            "🎉 Correct! Great work."
        )

    else:

        score = 0

        st.error(
            "❌ Incorrect. Review the concept "
            "and try again."
        )


    saved = save_lab_result(
        user_id,
        selected_lab["lab_id"],
        score
    )


    if saved:

        st.info(
            "Your lab result has been saved."
        )

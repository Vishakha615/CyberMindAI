import streamlit as st

from services.rag_service import (
    get_relevant_context
)
from ui.styles import apply_custom_css
from ui.components import (
    show_header,
    show_card,
    show_section_title
)
from services.content_generator import (
    generate_notes
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
    page_title="AI Notes | CyberMind AI",
    page_icon="📚",
    layout="wide"
)




st.markdown(
    """
    <style>

    h1 {
        background: linear-gradient(
            90deg,
            #4B549C,
            #565C8C
        );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;

        font-weight: 800;
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

    st.warning("Please login first.")

    if st.button("Go to Login"):

        st.switch_page(
            "pages/1_Login.py"
        )

    st.stop()

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
# PAGE
# ---------------------------------------------------------

st.title("📚 AI Notes Generator")
st.divider()

st.write(
    "Generate personalized cybersecurity "
    "study notes using RAG + Generative AI."
)


col1, col2 = st.columns(2)


with col1:

    topic = st.selectbox(
        "Select Topic",
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
        "Student Level",
        [
            "Beginner",
            "Intermediate",
            "Advanced"
        ]
    )


if st.button(
    "✨ Generate Notes",
    use_container_width=True
):

    with st.spinner(
        "Retrieving knowledge and generating notes..."
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


            notes = generate_notes(
                topic,
                difficulty,
                context
            )


            st.session_state.generated_notes = notes


        except Exception as e:

            st.error(
                "Unable to generate notes."
            )

            st.exception(e)


# ---------------------------------------------------------
# DISPLAY NOTES
# ---------------------------------------------------------

if "generated_notes" in st.session_state:

    st.divider()

    st.markdown(
        st.session_state.generated_notes
    )

    st.divider()

    st.success(
        "📚 Notes generated successfully "
        "using your cybersecurity knowledge base."
    )

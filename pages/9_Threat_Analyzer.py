import streamlit as st
from ui.styles import apply_custom_css
from ui.components import (
    show_header,
    show_card,
    show_section_title
)

from services.threat_analyzer import (
    analyze_text
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

from services.threat_ai_service import (
    generate_threat_explanation
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

st.set_page_config(
    page_title="Threat Analyzer | CyberMind AI",
    page_icon="🛡️",
    layout="wide"
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
# HEADER
# ---------------------------------------------------------

st.title(
    "🛡️ AI Threat Analyzer"
)

st.divider()

st.write(
    "Analyze suspicious messages and "
    "learn about common cybersecurity "
    "warning signs."
)

st.info(
    "💡 This tool is designed for "
    "cybersecurity education and awareness."
)


# ---------------------------------------------------------
# INPUT
# ---------------------------------------------------------

text = st.text_area(
    "Enter a message, email or security alert:",
    height=220,
    placeholder=(
        "Paste a suspicious message here..."
    )
)


# ---------------------------------------------------------
# ANALYZE
# ---------------------------------------------------------

if st.button(
    "🔍 Analyze Threat",
    use_container_width=True
):

    if not text.strip():

        st.warning(
            "Please enter some text first."
        )

        st.stop()


    with st.spinner(
        "Analyzing..."
    ):

        try:

            analysis = analyze_text(
                text
            )

            explanation = (
                generate_threat_explanation(
                    text,
                    analysis
                )
            )


            # ---------------------------------------------
            # RESULT
            # ---------------------------------------------

            st.divider()

            st.subheader(
                "🚨 Threat Assessment"
            )


            col1, col2 = st.columns(2)


            with col1:

                level = analysis[
                    "threat_level"
                ]

                if level == "HIGH":

                    st.error(
                        f"🚨 Threat Level: {level}"
                    )

                elif level == "MEDIUM":

                    st.warning(
                        f"⚠️ Threat Level: {level}"
                    )

                else:

                    st.success(
                        f"✅ Threat Level: {level}"
                    )


            with col2:

                st.metric(
                    "Threat Score",
                    f"{analysis['score']}/100"
                )


            # ---------------------------------------------
            # FEATURES
            # ---------------------------------------------

            st.subheader(
                "🔎 Detected Indicators"
            )

            features = analysis[
                "features"
            ]


            feature_labels = {
                "urgent_words":
                    "Urgent language",

                "credential_words":
                    "Credential-related terms",

                "link_present":
                    "Link detected",

                "suspicious_words":
                    "Suspicious wording",

                "financial_words":
                    "Financial terms"
            }


            for key, label in feature_labels.items():

                value = features[key]

                if value:

                    st.warning(
                        f"⚠️ {label}"
                    )


            # ---------------------------------------------
            # AI EXPLANATION
            # ---------------------------------------------

            st.divider()

            st.subheader(
                "🤖 CyberMind AI Explanation"
            )

            st.markdown(
                explanation
            )


        except Exception as e:

            st.error(
                "Unable to analyze the text."
            )

            st.exception(e)

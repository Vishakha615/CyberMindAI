import streamlit as st

from services.threat_analyzer import (
    analyze_text
)

from services.threat_ai_service import (
    generate_threat_explanation
)


st.set_page_config(
    page_title="Threat Analyzer | CyberMind AI",
    page_icon="🛡️",
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
# HEADER
# ---------------------------------------------------------

st.title(
    "🛡️ AI Threat Analyzer"
)

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
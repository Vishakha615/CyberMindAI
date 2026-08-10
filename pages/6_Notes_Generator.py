import streamlit as st

from services.rag_service import (
    get_relevant_context
)

from services.content_generator import (
    generate_notes
)


st.set_page_config(
    page_title="AI Notes | CyberMind AI",
    page_icon="📚",
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

st.title("📚 AI Notes Generator")

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
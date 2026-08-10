import streamlit as st

from services.rag_service import ask_cybermind


st.set_page_config(
    page_title="AI Mentor | CyberMind AI",
    page_icon="🤖",
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
        "Please login to use AI Mentor."
    )

    if st.button("Go to Login"):

        st.switch_page(
            "pages/1_Login.py"
        )

    st.stop()


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🤖 CyberMind AI Mentor")

st.write(
    "Your AI-powered cybersecurity learning assistant."
)

st.caption(
    "Powered by RAG + Embeddings + LLM"
)

st.divider()


# ---------------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------------

if "mentor_messages" not in st.session_state:

    st.session_state.mentor_messages = []


# Display previous messages

for message in st.session_state.mentor_messages:

    with st.chat_message(
        message["role"]
    ):

        st.markdown(
            message["content"]
        )


# ---------------------------------------------------------
# USER QUESTION
# ---------------------------------------------------------

question = st.chat_input(
    "Ask a cybersecurity question..."
)


if question:

    # Show user message

    with st.chat_message("user"):

        st.markdown(question)


    st.session_state.mentor_messages.append(
        {
            "role": "user",
            "content": question
        }
    )


    # Generate response

    with st.chat_message("assistant"):

        with st.spinner(
            "CyberMind is thinking..."
        ):

            try:

                answer, sources = ask_cybermind(
                    question
                )

                st.markdown(answer)


                # Sources

                if sources:

                    st.caption(
                        "📚 Knowledge sources:"
                    )

                    for source in set(
                        sources
                    ):

                        st.caption(
                            f"• {source}"
                        )


                st.session_state.mentor_messages.append(
                    {
                        "role": "assistant",
                        "content": answer
                    }
                )


            except Exception as e:

                st.error(
                    "Unable to generate a response."
                )

                st.caption(
                    f"Error: {e}"
                )
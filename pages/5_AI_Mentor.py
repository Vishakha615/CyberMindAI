import streamlit as st

from services.rag_service import ask_cybermind
from rag.knowledge_base import initialize_knowledge_base

import streamlit as st

from services.rag_service import ask_cybermind


st.set_page_config(
    page_title="AI Mentor | CyberMind AI",
    page_icon="🤖",
    layout="wide"
)
initialize_knowledge_base()

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

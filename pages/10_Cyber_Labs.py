import streamlit as st

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
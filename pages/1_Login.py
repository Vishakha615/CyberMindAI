import streamlit as st

from services.auth_service import login_user


st.set_page_config(
    page_title="Login | CyberMind AI",
    page_icon="🛡️",
    layout="centered"
)


st.title("🛡️ CyberMind AI")

st.subheader("Login")

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)


if st.button(
    "Login",
    use_container_width=True
):

    if not email or not password:

        st.warning(
            "Please enter email and password."
        )

    else:

        success, user, message = login_user(
            email,
            password
        )

        if success:

            st.session_state.logged_in = True
            st.session_state.user_id = user["user_id"]
            st.session_state.username = user["full_name"]
            st.session_state.email = user["email"]

            st.success(message)

            st.switch_page("app.py")

        else:

            st.error(message)


st.divider()

st.write("Don't have an account?")

if st.button(
    "Create Account",
    use_container_width=True
):

    st.switch_page("pages/2_Register.py")
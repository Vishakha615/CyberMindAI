import streamlit as st

from services.auth_service import register_user
from database.mysql_connection import get_connection

connection = get_connection()

st.set_page_config(
    page_title="Register | CyberMind AI",
    page_icon="🛡️",
    layout="centered"
)


st.title("🛡️ CyberMind AI")
st.subheader("Create Your Account")

full_name = st.text_input(
    "Full Name",
    placeholder="Enter username"
)

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)

password = st.text_input(
    "Password",
    type="password",
    placeholder="Create a password"
)

confirm_password = st.text_input(
    "Confirm Password",
    type="password",
    placeholder="Confirm your password"
)


if st.button(
    "Create Account",
    use_container_width=True
):

    if not full_name or not email or not password:

        st.warning("Please fill all required fields.")

    elif password != confirm_password:

        st.error("Passwords do not match.")

    elif len(password) < 6:

        st.error("Password must contain at least 6 characters.")

    else:

        success, message = register_user(
            full_name,
            email,
            password
        )

        if success:

            st.success(message)

            st.info(
                "Account created successfully. "
                "Please login to continue."
            )

        else:

            st.error(message)


st.divider()

if st.button(
    "Already have an account? Login",
    use_container_width=True
):

    st.switch_page("pages/1_Login.py")

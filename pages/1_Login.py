'''import streamlit as st

from services.auth_service import login_user


st.set_page_config(
    page_title="Login | CyberMind AI",
    page_icon="🛡️",
    layout="centered"
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


st.markdown(
        """
        <style>

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

    st.switch_page("pages/2_Register.py")'''






import streamlit as st

from services.auth_service import login_user


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Login | CyberMind AI",
    page_icon="🛡️",
    layout="centered"
)


# =========================================================
# HIDE DEFAULT NAVIGATION
# =========================================================

st.markdown(
    """
    <style>

    [data-testid="stSidebarNav"] {
        display: none;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# BACKGROUND
# =========================================================

st.markdown(
    """
    <style>

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


# =========================================================
# BUTTON STYLE
# =========================================================

st.markdown(
    """
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


    div.stButton > button:hover {

        background-color: #303B78;

        border-color: #5968B5;

        transform: translateY(-2px);
    }


    div.stButton > button:active {

        transform: scale(0.98);
    }

    </style>
    """,
    unsafe_allow_html=True
)


# =========================================================
# TITLE
# =========================================================

st.title("🛡️ CyberMind AI")

st.subheader("Login")


# =========================================================
# LOGIN INPUT
# =========================================================

email = st.text_input(
    "Email",
    placeholder="Enter your email"
)


password = st.text_input(
    "Password",
    type="password",
    placeholder="Enter your password"
)


# =========================================================
# LOGIN BUTTON
# =========================================================

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


        # =================================================
        # SUCCESSFUL LOGIN
        # =================================================

        if success:

            # Save login information
            st.session_state.logged_in = True

            st.session_state.user_id = (
                user["user_id"]
            )

            # IMPORTANT:
            # Save full_name with this exact key
            st.session_state.full_name = (
                user["full_name"]
            )

            st.session_state.email = (
                user["email"]
            )


            st.success(
                "Login Succuessful"
            )


            # Go to dashboard
            st.switch_page(
                "app.py"
            )


        # =================================================
        # LOGIN FAILED
        # =================================================

        else:

            st.error(message)


# =========================================================
# REGISTER
# =========================================================

st.divider()

st.write(
    "Don't have an account?"
)


if st.button(
    "Create Account",
    use_container_width=True
):

    st.switch_page(
        "pages/2_Register.py"
    )

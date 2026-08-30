import streamlit as st


def show_header():

    st.markdown(
        """
        <div class="main-title">
            🛡️ CyberMind AI
        </div>

        <div class="subtitle">
            Your Intelligent Cybersecurity
            Learning Companion
        </div>
        """,
        unsafe_allow_html=True
    )





'''
def show_card(title, value, icon):

    html = f"""
    <div class="dashboard-card">
        <div class="card-title">
            {icon} {title}
        </div>

        <div class="card-value">
            {value}
        </div>
    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )'''

'''
import streamlit as st
import base64
from pathlib import Path


def get_image_base64(image_path):

    image_path = Path(image_path)

    with open(image_path, "rb") as image_file:
        return base64.b64encode(
            image_file.read()
        ).decode()


def show_card(title, value, image_path):

    image_base64 = get_image_base64(
        image_path
    )

    html = f"""
    <div class="dashboard-card">

        <img
            src="data:image/png;base64,{image_base64}"
            class="card-image"
        >

        <div class="card-title">
            {title}
        </div>

        <div class="card-value">
            {value}
        </div>

    </div>
    """

    st.markdown(
        html,
        unsafe_allow_html=True
    )'''



import streamlit as st

import streamlit as st


def show_card(title, value, image_path):

    with st.container(border=True):

        st.image(
            image_path,
            width=80
        )

        st.markdown(
            f"**{title}**"
        )

        st.markdown(
            f"## {value}"
        )







def show_section_title(
    title,
    description=""
):

    st.markdown(
        f"""
        <h2 style="margin-bottom:5px;">
            {title}
        </h2>

        <p style="
            color:#a8b2d1;
            margin-bottom:20px;
        ">
            {description}
        </p>
        """,
        unsafe_allow_html=True
    )

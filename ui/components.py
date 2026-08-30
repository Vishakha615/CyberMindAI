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


'''def show_card(
    title,
    value,
    icon
):

    st.markdown(
        f"""
        <div class="cyber-card">

            <div class="card-title">
                {icon} {title}
            </div>

            <div class="card-value">
                {value}
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )'''



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

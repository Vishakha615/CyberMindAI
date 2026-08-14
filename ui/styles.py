import streamlit as st


def apply_custom_css():

    st.markdown(
        """
        <style>

        /* ------------------------------
           GLOBAL
        ------------------------------ */

        .stApp {
            background:
                linear-gradient(
                    135deg,
                    #050816 0%,
                    #0b1026 50%,
                    #111936 100%
                );
        }


        /* ------------------------------
           MAIN CONTENT
        ------------------------------ */

        .main-title {

            font-size: 42px;

            font-weight: 800;

            margin-bottom: 5px;

            background:
                linear-gradient(
                    90deg,
                    #00f5d4,
                    #00bbf9,
                    #9b5de5
                );

            -webkit-background-clip: text;

            -webkit-text-fill-color: transparent;
        }


        .subtitle {

            color: #a8b2d1;

            font-size: 17px;

            margin-bottom: 30px;
        }


        /* ------------------------------
           CARDS
        ------------------------------ */

        .cyber-card {

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.05
                );

            border:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.08
                );

            border-radius: 18px;

            padding: 24px;

            margin-bottom: 20px;

            backdrop-filter: blur(10px);

            box-shadow:
                0 8px 30px
                rgba(
                    0,
                    0,
                    0,
                    0.25
                );
        }


        .card-title {

            font-size: 16px;

            color: #a8b2d1;

            margin-bottom: 8px;
        }


        .card-value {

            font-size: 30px;

            font-weight: 700;

            color: white;
        }


        /* ------------------------------
           SIDEBAR
        ------------------------------ */

        section[data-testid="stSidebar"] {

            background:
                linear-gradient(
                    180deg,
                    #060B24,
                    #0B1442
                );

            border-right:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.08
                );
        }


        /* ------------------------------
           BUTTON
        ------------------------------ */

        .stButton > button {

            border-radius: 12px;

            border: none;

            padding: 10px 20px;

            font-weight: 600;

            transition:
                0.2s ease;
        }


        .stButton > button:hover {

            transform:
                translateY(-2px);

            box-shadow:
                0 8px 20px
                rgba(
                    0,
                    187,
                    249,
                    0.25
                );
        }


        /* ------------------------------
           METRICS
        ------------------------------ */

        div[data-testid="stMetric"] {

            background:
                rgba(
                    255,
                    255,
                    255,
                    0.04
                );

            padding: 18px;

            border-radius: 16px;

            border:
                1px solid
                rgba(
                    255,
                    255,
                    255,
                    0.07
                );
        }

        </style>
        """,
        unsafe_allow_html=True
    )

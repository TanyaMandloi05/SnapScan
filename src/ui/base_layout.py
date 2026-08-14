import streamlit as st

def style_home_layout():
    st.markdown("""
        <style>
            .stApp {
            background: #5865F2 !important;
            }
            /* overriding streamlit column property*/
            .stApp div[data-testid="stColumn"]{
                background: #E0E3FF !important;
                padding: 2.5rem !important;
                border-radius: 5rem !important;
            }
        </style>

        """, unsafe_allow_html=True)

def style_dashboard_layout():
    st.markdown("""
        <style>
            .stApp {
            background: #E0E3FF !important;
            }
        </style>

        """, unsafe_allow_html=True)

def style_base_layout():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Lilita+One&display=swap');
        @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');

           /*removed extra gap of streamlit*/
            #MainMenu, header, footer {
            visibility: hidden;
            }

            .block-container{
            padding-top: 1.5rem;
            }

            h1{
            font-family: 'Lilita One', cursive !important;
            font-size: 2.5rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            /* color: #E0E3FF !important; */
            }

            h2{
            font-family: 'Lilita One', cursive !important;
            font-size: 2rem !important;
            line-height: 1.1 !important;
            margin-bottom: 0rem !important;
            
            color: #454545 !important;
            }

            h3, h4, p {
            font-family: 'Outfit', sans-serif !important;
            }

            button[kind="primary"]{
            border-radius: 1.5rem !important;
            background: #5865F2 !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
            }

            button[kind="secondary"]{
            border-radius: 1.5rem !important;
            Background : Transparent;
            Border     : 2px solid #5865F2 !important;
            color       : #5865F2 !important;
            padding: 10px 20px !important;
            transition: transform 0.25s ease-in-out !important;
            }

            button[kind="secondary"]:hover {
            transform: scale(1.05)!important;
            Background : #5865F2;
            color : White !important;
            }

            button[kind="tertiary"]{
            border-radius: 1.5rem !important;
            background: black !important;
            color: white !important;
            padding: 10px 20px !important;
            border: none !important;
            transition: transform 0.25s ease-in-out !important;
            }

            button[kind="primary"]:hover{
            transform: scale(1.05)!important;
            Background : Transparent !important;
            Border     : 2px solid #5865F2 !important;
            color       : #5865F2 !important;
            }
        </style>

        """, unsafe_allow_html=True)
import streamlit as st

def header_home():
    # logo_url = "src/images/logo.png"
    logo_url = "https://i.ibb.co/YTYGn5qV/logo.png"
    st.markdown(f"""
    <div style="display:flex; justify-content:center; align-items:center; flex-direction:column; margin-top:30px; margin-bottom:30px"> 
    <img src="{logo_url}" style="height:100px">
    <h1 style="color:#EB459E; text-align:center;">SNAP</br>  SCAN</h1>
    </div>
    """, unsafe_allow_html=True)
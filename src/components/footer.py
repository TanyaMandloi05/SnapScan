import streamlit as st
def footer_home():
    st.markdown("""
    <div style="display:flex; justify-content:center; margin-top:2rem;">
    <p style="font-weight:bold; color:white;">Create with ❤️ by <span style="color: #FFDD00">Tanya</span></p>
    </div>
""", unsafe_allow_html=True)

def footer_dashboard():
    st.markdown("""
    <div style="display:flex; justify-content:center; margin-top:2rem;">
    <p style="font-weight:bold; color:black;">Create with ❤️ by <span style="color: #0080FE">Tanya</span></p>
    </div>
""", unsafe_allow_html=True)

import streamlit as st
import recflix
import login

st.set_page_config(page_title="Recflix", layout="wide", initial_sidebar_state="collapsed")

if "page" not in st.session_state:
    st.session_state.page = "login"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if st.session_state.page == "login":
    login.render_login()
elif st.session_state.page == "recflix":
    recflix.render_app()

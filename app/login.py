import streamlit as st
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.auth import store_user, validate_user

def render_login():
    st.title("Recflix")

    tab1, tab2 = st.tabs(["Log In", "Sign Up"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Log In"):
            user_info = validate_user(username, password)
            if user_info:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.session_state.is_admin = user_info.get("admin", False)
                st.session_state.page = "recflix"
                st.rerun()
            else:
                st.error("Invalid credentials")

    with tab2:
        new_user = st.text_input("New Username", key="signup_user")
        new_pass = st.text_input("New Password", type="password", key="signup_pass")

        if st.button("Sign Up"):
            success = store_user(new_user, new_pass)
            if success:
                st.session_state.logged_in = True
                st.session_state.username = new_user
                st.session_state.is_admin = False
                st.session_state.page = "recflix"
                st.rerun()
            else:
                st.error("Username already taken")
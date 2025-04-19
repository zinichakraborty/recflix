import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app.user_profile as user_profile
import app.user_analytics as user_analytics
import app.recommender as recommender

def render_app():
    if "username" not in st.session_state:
        st.warning("You must log in.")
        return

    st.title(f"Hi {st.session_state.username}!")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    if st.session_state.get("is_admin", False):
        tabs = st.tabs(["Recommendations", "Profile", "User Analytics"])
    else:
        tabs = st.tabs(["Recommendations", "Profile"])

    with tabs[0]:
        recommender.render()

    with tabs[1]:
        user_profile.render()
    
    if st.session_state.get("is_admin", False):
        with tabs[2]:
            user_analytics.render()
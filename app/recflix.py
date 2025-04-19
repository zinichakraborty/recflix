import streamlit as st
from streamlit_option_menu import option_menu
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import app.recommender as recommender
import app.user_profile as user_profile
import app.user_analytics as user_analytics

def render_app():
    if "username" not in st.session_state:
        st.warning("You must log in.")
        return

    st.title(f"Hi {st.session_state.username}!")

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    tabs = ["Recommendations", "Profile"]
    if st.session_state.get("is_admin", False):
        tabs.append("User Analytics")

    choice = option_menu(
        menu_title=None,
        options=tabs,
        icons=["list", "person", "bar-chart"][: len(tabs)],
        orientation="horizontal",
        styles={"nav-link": {"padding": "0.5rem 1rem", "font-size": "1rem"}},
    )

    if choice == "Recommendations":
        recommender.render()
    elif choice == "Profile":
        user_profile.render()
    else:
        user_analytics.render()
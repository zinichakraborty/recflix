import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.store.users as users

def render():
    st.title(f"{st.session_state.username}'s Profile")

    st.subheader("Watch History")
    watch_history = users.get_watch_history(st.session_state.username)
    if watch_history:
        st.write("### Movies You've Watched:")
        for movie in watch_history:
            st.markdown(f"- {movie}")
    else:
        st.write("No watch history yet.")

    #TODO: Add or delete movies from the watched list cleanly with API

    new_history_input = st.text_area("Update your watch history (comma-separated)")
    if st.button("Update Watch History"):
        history_list = [x.strip() for x in new_history_input.split(",") if x.strip()]
        success = users.add_watch_history(st.session_state.username, history_list)
        st.rerun()

    
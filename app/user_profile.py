import streamlit as st
import sys
import os
import requests

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db.store.users as users
import db.actions.user_stats as user_stats
import db.actions.imdb_search as imdb_search

def render():
    st.title(f"{st.session_state.username}'s Profile")

    st.subheader("Watch History")
    watch_history = users.get_watch_history(st.session_state.username) or []
    st.session_state.watched_movies = watch_history

    if watch_history:
        st.markdown("### Movies You've Watched:")
        for movie in watch_history:
            st.markdown(f"{movie}")
    else:
        st.info("No watch history yet.")

    st.markdown("### Add Movies to Watch History")
    if "profile_search_results" not in st.session_state:
        st.session_state.profile_search_results = []

    search_query = st.text_input("Search for a movie to add:")
    if search_query:
        st.session_state.profile_search_results = imdb_search.search_movies(search_query)

    if st.session_state.profile_search_results:
        selected_movie = st.selectbox("Suggestions:", st.session_state.profile_search_results)
        if st.button("Add Movie to Watch History"):
            if selected_movie not in watch_history:
                updated_history = watch_history + [selected_movie]
                user_stats.save_user_data(st.session_state.username, updated_history)
                users.add_watch_history(st.session_state.username, updated_history)
                st.success(f"Added {selected_movie} to watch history.")
                st.session_state.profile_search_results = []
                st.rerun()

    selected_to_remove = st.multiselect(
        "Select movies to remove from watch history:",
        options=watch_history
    )
    if st.button("Remove Selected"):
        updated_history = [m for m in watch_history if m not in selected_to_remove]
        user_stats.save_user_data(st.session_state.username, updated_history)
        users.add_watch_history(st.session_state.username, updated_history)
        st.rerun()
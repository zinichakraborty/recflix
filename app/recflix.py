import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.actions.user_data as user_data
import db.actions.recommend as recommend
import app.user_profile as user_profile
import app.user_analytics as user_analytics

#TODO: Display user's watched movies
#TODO: Make an API call with a search bar to get a list of movies
#TODO: Add or delete movies from the watched list
#TODO: Get the tags of top watched movies and add them to the query
#TODO: Redis caches watch history and preferences
#TODO: Possibly add a movie rating system

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
        watched = st.multiselect("Movies you’ve watched:", [
            "Inception", "The Matrix", "Parasite", "Spirited Away"
        ])
        genres = st.multiselect("Select favorite genres:", ["Drama", "Sci-Fi", "Comedy", "Action"])
        prefs = st.text_area("Tell us more about your taste")
        min_rating = st.slider("Minimum Movie Rating (out of 5)", 0.0, 5.0, 3.5, step=0.1)

        if st.button("Save Preferences"):
            user_data.save_user_data(
                st.session_state.username,
                watched,
                genres,
                prefs
            )
            st.success("Preferences saved!")
            st.subheader("Recommendations based on your preferences:")
        if st.button("Recommend"):
            results = recommend.recommend_movies(watched, genres, prefs, min_rating)
            for i, result in enumerate(results):
                movie = result['movie'] 
                st.markdown(f"**{i+1}. {movie['title']}** (Similarity Score: {result['score']*100:.2f})")
                st.markdown(f"• Rating: {movie['avgRating']:.2f}")
                st.markdown(f"• Directed by: {movie['directedBy']}")
                st.markdown(f"• Starring: {movie['starring']}")
                st.markdown(f"• IMDb ID: {movie['imdbId']}")
                st.markdown("---")

    with tabs[1]:
        user_profile.render()
    
    if st.session_state.get("is_admin", False):
        with tabs[2]:
            user_analytics.render()
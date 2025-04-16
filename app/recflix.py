import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.actions.user_stats as user_stats
import db.actions.recommend as recommend
import app.user_profile as user_profile
import app.user_analytics as user_analytics
import db.store.users as users
import db.actions.imdb_search as imdb_search

def render_app():
    if "username" not in st.session_state:
        st.warning("You must log in.")
        return

    st.title(f"Hi {st.session_state.username}!")
    watch_history = users.get_watch_history(st.session_state.username)

    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state.page = "login"
        st.rerun()

    if st.session_state.get("is_admin", False):
        tabs = st.tabs(["Recommendations", "Profile", "User Analytics"])
    else:
        tabs = st.tabs(["Recommendations", "Profile"])

    with tabs[0]:
        st.subheader("Select movies you’ve watched:")

        if "watched_movies" not in st.session_state:
            st.session_state.watched_movies = watch_history or []

        if "search_results" not in st.session_state:
            st.session_state.search_results = []

        query_input = st.text_input("Search for a movie:")

        if query_input:
            st.session_state.search_results = imdb_search.search_movies(query_input)

        if st.session_state.search_results:
            selected_movie = st.selectbox(
                "Suggestions:",
                options=st.session_state.search_results,
                key="suggest_box"
            )

            if st.button("Add to Watched"):
                if selected_movie and selected_movie not in st.session_state.watched_movies:
                    st.session_state.watched_movies.append(selected_movie)
                    user_stats.save_user_data(st.session_state.username, st.session_state.watched_movies)
                st.session_state.search_results = []
                st.rerun()

        watched = st.multiselect(
            "Your watched movies:",
            options=st.session_state.watched_movies,
            default=st.session_state.watched_movies,
            key="watched_movies_select"
        )
        print(watched)
        if watched:
            include_watch_history = st.radio(
                "Include your watch history in the recommendation?",
                ["Yes", "No"],
                horizontal=True
            ) == "Yes"
        else:
            include_watch_history = False

        genres = st.multiselect(
            "What genre are you looking for right now:",
            [
                "Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Documentary",
                "Drama", "Family", "Fantasy", "Film-Noir", "History", "Horror", "Music", "Musical",
                "Mystery", "Romance", "Sci-Fi", "Short", "Sport", "Superhero", "Thriller", "War", "Western"
            ]
        )

        prefs = st.text_area("What general preferences do you have for the movie?")
        min_rating = st.slider("Minimum Movie Rating (out of 5)", 0.0, 5.0, 3.5, step=0.1)
        if st.button("Recommend"):
            if not genres:
                st.error("Please select at least one genre before getting recommendations.")
                st.stop()

            if not prefs.strip():
                st.error("Please enter your general movie preferences.")
                st.stop()
            st.subheader("Recommendations based on your history and current preferences:")
            user_stats.save_user_data(st.session_state.username, watched)
            users.add_watch_history(st.session_state.username, watched)
            results = recommend.recommend_movies(watched, genres, prefs, min_rating, include_watch_history)
            for i, result in enumerate(results):
                movie = result['movie'] 
                st.markdown(f"**{i+1}. {movie['title']}** (Similarity Score: {result['score']*100:.2f})")
                st.markdown(f"Rating: {movie['avgRating']:.2f}")
                st.markdown(f"Directed by: {movie['directedBy']}")
                st.markdown(f"Starring: {movie['starring']}")
                st.markdown(f"IMDb ID: {movie['imdbId']}")
                st.markdown("---")

    with tabs[1]:
        user_profile.render()
    
    if st.session_state.get("is_admin", False):
        with tabs[2]:
            user_analytics.render()
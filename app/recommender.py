import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import db.store.users as users
import db.actions.user_stats as user_stats
import db.actions.imdb_search as imdb_search
import db.actions.user_stats as user_stats
import db.actions.recommend as recommend

def render():
    watch_history = users.get_watch_history(st.session_state.username)
    
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
    if watched:
        include_watch_history = st.radio("Include your watch history in the recommendation?", ["Yes", "No"], horizontal=True) == "Yes"
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
    min_rating = st.slider("Minimum Movie Rating (out of 5)", 0.0, 5.0, 3.0, step=0.1)
    
    if st.button("Recommend"):
        user_stats.save_user_data(st.session_state.username, watched)
        users.add_watch_history(st.session_state.username, watched)
        st.success(f"Getting your recommendations...")
        results = recommend.recommend_movies(watched, genres, prefs, min_rating, include_watch_history)
        for i, result in enumerate(results):
            movie = result['movie']
            header = f"**{i+1}. {movie['title']}** | Similarity Score: {result['score']*100:.2f}%"
            with st.expander(header):
                st.markdown(f"**Rating:** {movie['avgRating']:.2f}")
                st.markdown(f"**Directed by:** {movie['directedBy']}")
                st.markdown(f"**Starring:** {movie['starring']}")
                st.markdown(f"**IMDb ID:** {movie['imdbId']}")

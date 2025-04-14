import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.user_profile as user_profile
import db.recommend as recommend
import app.user_analytics as user_analytics

#TODO: User registration/login
#TODO: Display user's watched movies
#TODO: Make an API call with a search bar to get a list of movies
#TODO: Add or delete movies from the watched list
#TODO: Possibly add a movie rating system
#TODO: Possibly create a graph database for movie recommendations OR get the tags of top watched movies and add them to the query

st.title("🎬 Recflix")

tab1, tab2 = st.tabs(["Recommendation Form", "User Analytics"])

with tab1:
    st.write("Tell us a bit about what you like to watch and we will give you recommendations!")

    user_name = st.text_input("👤 Your Name")

    genre_list = [
        "Action", "Adventure", "Animation", "Comedy", "Crime", "Documentary", "Drama", "Fantasy",
        "Historical", "Horror", "LGBTQ+", "Musical", "Mystery", "Romance", "Sci-Fi", "Thriller", "War", "Western"
    ]

    watched_movies = []

    selected_genres = st.multiselect("Select your favorite genres:", genre_list)

    user_preferences = st.text_area("Write about your favorite genres, themes, directors, etc.")

    min_rating = st.slider("Minimum Movie Rating (out of 5)", 0.0, 5.0, 3.5, step=0.1)

    if st.button("Submit"):
        st.success(f"Thanks, {user_name}! Getting your recommendations...")
        user_profile.save_user_data(user_name, watched_movies, selected_genres, user_preferences)
        st.subheader("Recommendations based on your preferences:")
        results = recommend.recommend_movies(user_preferences, min_rating)
        for i, result in enumerate(results):
            movie = result['movie'] 
            st.markdown(f"**{i+1}. {movie['title']}** (Similarity Score: {result['score']*100:.2f})")
            st.markdown(f"• Rating: {movie['avgRating']:.2f}")
            st.markdown(f"• Directed by: {movie['directedBy']}")
            st.markdown(f"• Starring: {movie['starring']}")
            st.markdown(f"• IMDb ID: {movie['imdbId']}")
            st.markdown("---")

with tab2:
    user_analytics.render()
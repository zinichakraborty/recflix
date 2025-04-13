import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import db.user_profile as user_profile
import app.user_analytics as user_analytics

st.title("🎬 Recflix")

tab1, tab2 = st.tabs(["Recommendation Form", "User Analytics"])

with tab1:
    st.write("Tell us a bit about what you like to watch and we will give you recommendations!")

    user_name = st.text_input("👤 Your Name")

    movie_list = [
        "Inception", "The Matrix", "Interstellar", "The Godfather",
        "The Dark Knight", "Pulp Fiction", "Parasite", "The Shawshank Redemption"
    ]

    watched_movies = st.multiselect("Select movies you have seen:", movie_list)

    user_preferences = st.text_area("Write about your favorite genres, themes, directors, etc.")

    if st.button("Submit"):
        st.success(f"Thanks, {user_name}! Getting your recommendations...")
        user_profile.save_user_data(user_name, watched_movies, user_preferences)
        user_data = user_profile.get_user_data(user_name)

with tab2:
    user_analytics.render()
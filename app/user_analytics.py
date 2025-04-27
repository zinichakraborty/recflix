import plotly.graph_objects as go
import streamlit as st
import sys
import os
from collections import Counter

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.actions.user_stats import get_all_user_data

def render():
    st.title("User Analytics")

    user_data = get_all_user_data()

    if user_data:
        num_users = len(user_data)

        all_movies = []

        for user in user_data.values():
            all_movies.extend(user.get("watched_movies", []))

        top_movies = Counter(all_movies).most_common(5)

        if top_movies:
            movie_titles, movie_counts = zip(*top_movies)
            movie_fig = go.Figure([go.Bar(x=movie_titles, y=movie_counts)])
            movie_fig.update_layout(title="Top Watched Movies", xaxis_title="Movie", yaxis_title="Watch Count")
            st.plotly_chart(movie_fig, use_container_width=True)

        fig = go.Figure(go.Indicator(
            mode="number",
            value=num_users,
            title={"text": "Active Users"},
            number={"font": {"size": 48}}
        ))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No user data found in Redis yet.")
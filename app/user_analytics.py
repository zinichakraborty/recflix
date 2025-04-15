import plotly.graph_objects as go
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.actions.user_data import get_all_user_data

def render():
    st.title("User Analytics")

    user_data = get_all_user_data()

    if user_data:
        num_users = len(user_data)

        fig = go.Figure(go.Indicator(
            mode="number",
            value=num_users,
            title={"text": "Total Users"},
            number={"font": {"size": 48}}
        ))

        #TODO: Plot most watched movies and prefered genres

        st.plotly_chart(fig, use_container_width=True)

        for name, data in user_data.items():
            with st.expander(f"{name}"):
                st.json(data)
    else:
        st.info("No user data found in Redis.")
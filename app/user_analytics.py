import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.user_profile import get_all_user_data

def render():
    st.title("User Analytics")

    user_data = get_all_user_data()

    if user_data:
        for name, data in user_data.items():
            with st.expander(f"User: {name}"):
                st.json(data)
    else:
        st.info("No user data found in Redis.")
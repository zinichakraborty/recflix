import plotly.graph_objects as go
import streamlit as st
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def render():
    st.title(f"{st.session_state.username}'s Profile")



    
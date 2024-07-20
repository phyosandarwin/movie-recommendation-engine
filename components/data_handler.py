import os
import gzip
import pickle
import streamlit as st

@st.cache_data
def load_movie_data(file_name):
    file_path = os.path.join("data", "pkl_files", file_name)
    with gzip.open(file_path, "rb") as file:
        return pickle.load(file)
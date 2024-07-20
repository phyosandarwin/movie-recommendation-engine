import os
import pickle

def load_movie_data(file_name):
    file_path = os.path.join("data", "pkl_files", file_name)
    with open(file_path, "rb") as file:
        return pickle.load(file)
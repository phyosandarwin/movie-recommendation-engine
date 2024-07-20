import streamlit as st
import pandas as pd
import re
import gzip
from sklearn.metrics.pairwise import cosine_similarity
from fuzzywuzzy import fuzz
from .data_handler import load_movie_data



# preprocessing title
def clean_title(title):
    title = re.sub("[^a-zA-Z0-9 ]","", title)
    title = title.lower()
    return title

#---------Operation 1: Search movie title and return exact/similar search ----------
@st.cache_data
def search_movie_title(df, movie_title, k=15):
    # Clean the input title
    cleaned_title = clean_title(movie_title)
    
    # Calculate cosine similarity between cleaned_title and movie titles
    vectorizer_title = load_movie_data("tfidf_vectorizer_title.pkl.gz")
    tfidf_matrix_title = load_movie_data("tfidf_matrix_title.pkl.gz")
    query_vect_title = vectorizer_title.transform([cleaned_title])
    similarity_title = cosine_similarity(query_vect_title, tfidf_matrix_title).flatten()
    
    # Fuzzy matching to account for minor title variations
    fuzzy_scores = [fuzz.ratio(cleaned_title, t) for t in df['title_processed']]
    combined_similarity = similarity_title * (0.8 + 0.2 * (pd.Series(fuzzy_scores) / 100))
    
    # Get the indices of top 10 similar movies
    top_indices = combined_similarity.argsort()[-k:][::-1]
    
    # Retrieve the top 10 search results
    search_movie_results = df.iloc[top_indices]
    search_movie_results = search_movie_results.sort_values(by='release_date', ascending=False)
    
    return search_movie_results[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]


#----------Operation 2: Recommendations based on dropdown criteria options-------
@st.cache_data
def recommend_movies_by_genres(df, user_genres, k=30):
    # Create a filter mask for all specified genres
    genre_mask = df['genres'].apply(lambda genres: any(genre.lower() in genres.lower() for genre in user_genres))
    filtered_movies = df[genre_mask]
    
    # Sort by vote_count then vote_average in descending order
    sorted_movies = filtered_movies.sort_values(by=['vote_count', 'vote_average'], ascending=[False, False])
    
    # Get top k movies
    top_movies = sorted_movies.head(k)
    
    # sort by release date
    top_movies = top_movies.sort_values(by='release_date', ascending=False)

    return top_movies[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]

@st.cache_data
def recommend_movies_by_language(df, language, k=30):
    # Get the movies that belong to the specified genre
    lang_movies = df[df['original_language'].str.contains(language)]

    sorted_lang_movies = lang_movies.sort_values(by=['vote_count', 'vote_average'], ascending=[False, False])

    top_lang_movies = sorted_lang_movies.head(k)

    top_lang_movies = top_lang_movies.sort_values(by='release_date', ascending=False)

    return top_lang_movies[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]

@st.cache_data
def search_movie_overview(df, movie_title, k=30):
    similar_movie = search_movie_title(df, movie_title, k=1)
    idx = similar_movie.index[0]  # Get the index of the most similar movie

    tfidf_matrix_overview = load_movie_data("tfidf_matrix_overview.pkl.gz")

    query_vect_overview = tfidf_matrix_overview[idx]
    similarity_overview = cosine_similarity(query_vect_overview.reshape(1, -1), tfidf_matrix_overview).flatten()
    top_indices = similarity_overview.argsort()[-(k+1):][::-1]
    top_indices = top_indices[top_indices != idx]  # Exclude the original movie
    top_indices = top_indices[:k]
    search_movie_results = df.iloc[top_indices]
    search_movie_results = search_movie_results.sort_values(by='release_date', ascending=False)
    return search_movie_results[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]
    


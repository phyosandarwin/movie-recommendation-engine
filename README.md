# Cinematic Seeker
This movie recommendation system is built upon **content-based filtering technique**.

## Preprocessing
Dataset is collected from [Kaggle](https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies/).
It has been cleaned and preprocessed as seen in the `tmdb_movie_dataset_cleaning` notebook.

## App Features
1. Search movie - returns top 10 movies that are closest in title name as the user's input
2. Give Recommendations based on genre, language and similar overview as input title

### Recommendation functions (see `guide` page of the app to refer to code explanations)
- recommend by genre
  ```
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
  ```
- recommend by language
  ```
  def recommend_movies_by_language(df, language, k=30):
      lang_movies = df[df['original_language'].str.contains(language)]
      sorted_lang_movies = lang_movies.sort_values(by=['vote_count', 'vote_average'], ascending=[False, False])
      top_lang_movies = sorted_lang_movies.head(k)
      top_lang_movies = top_lang_movies.sort_values(by='release_date', ascending=False)
  
      return top_lang_movies[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]
    ```

- recommend by similar overview
  ```
  def search_movie_overview(df, movie_title, k=30):
      similar_movie = search_movie_title(df, movie_title, k=1)
      idx = similar_movie.index[0]  
      tfidf_matrix_overview = load_movie_data("tfidf_matrix_overview.pkl.gz")
      query_vect_overview = tfidf_matrix_overview[idx]
      similarity_overview = cosine_similarity(query_vect_overview.reshape(1, -1), tfidf_matrix_overview).flatten()
      top_indices = similarity_overview.argsort()[-(k+1):][::-1]
      top_indices = top_indices[top_indices != idx]  # Exclude the original movie
      top_indices = top_indices[:k]
      search_movie_results = df.iloc[top_indices]
      search_movie_results = search_movie_results.sort_values(by='release_date', ascending=False)
  
      return search_movie_results[['title', 'overview', 'runtime', 'vote_average', 'release_date', 'poster_path']]
    ```


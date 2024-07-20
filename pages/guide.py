import streamlit as st

st.set_page_config(page_title="Recommendation Functions", page_icon="🤔", 
                   initial_sidebar_state='collapsed', layout='wide')
with st.sidebar:
    st.link_button("See Github repository💡", 
                   url="https://github.com/phyosandarwin/movie-recommender-chatbot", type='primary', use_container_width=True)
    st.write("Made by Phyo Sandar Win 💙")
    
st.title("Recommendation Functions")

st.markdown(f'''**:green-background[:red[1. Recommending by genre]]**''')
with st.container(border=True):
    genre_code = '''def recommend_movies_by_genres(df, user_genres, k=30):
        genre_mask = df['genres'].apply(lambda genres: any(genre.lower() in 
                                        genres.lower() for genre in user_genres))
        filtered_movies = df[genre_mask]
        sorted_movies = filtered_movies.sort_values(by=['vote_count', 'vote_average'], 
                                                    ascending=[False, False])
        top_movies = sorted_movies.head(k)
        top_movies = top_movies.sort_values(by='release_date', ascending=False)
        return top_movies[['title', 'overview', 'runtime', 'vote_average', 'release_date', 
                            'poster_path']]
    '''
    st.code(
        genre_code, language='python'
    )
    with st.expander(label="Explain code",):
        st.write("After selecting the genre(s), we find the movies that are of at least one of the selected genres.\
                30 (by default) of these movies that are ranked the highest in total vote count and average votes\
                are fetched and sorted by their release date from latest to earliest.")

st.markdown(f'''**:blue-background[:blue[2. Recommending by language]]**''')
with st.container(border=True):
    lang_code = '''def recommend_movies_by_language(df, language, k=30):
        lang_movies = df[df['original_language'].str.contains(language)]
        sorted_lang_movies = lang_movies.sort_values(by=['vote_count', 'vote_average'], 
                                                    ascending=[False, False])
        top_lang_movies = sorted_lang_movies.head(k)
        top_lang_movies = top_lang_movies.sort_values(by='release_date', ascending=False)

        return top_lang_movies[['title', 'overview', 'runtime', 'vote_average', 'release_date',
                                'poster_path']]

    '''
    st.code(lang_code, language='python')
    with st.expander(label="Explain code",):
        st.write("After selecting the language,\
                the top 30 movies ranked the highest in total vote count and average votes are fetched\
                and sorted by their release date from latest to earliest.")

st.markdown(f'''**:blue-background[:green[3. Recommending by similar movie plot]]**''')
with st.container(border=True):
    overview_code = '''def search_movie_overview(df, movie_title, k=30):
        similar_movie = search_movie_title(df, movie_title, k=1)
        idx = similar_movie.index[0]  
        tfidf_matrix_overview = load_movie_data("tfidf_matrix_overview.pkl")
        query_vect_overview = tfidf_matrix_overview[idx]
        similarity_overview = cosine_similarity(query_vect_overview.reshape(1, -1), tfidf_matrix_overview).flatten()
        top_indices = similarity_overview.argsort()[-(k+1):][::-1]
        top_indices = top_indices[top_indices != idx]
        top_indices = top_indices[:k]
        search_movie_results = df.iloc[top_indices]
        search_movie_results = search_movie_results.sort_values(by='release_date', ascending=False)
        return search_movie_results[['title', 'overview', 'runtime', 'vote_average', 
                                    'release_date', 'poster_path']]

    '''
    st.code(overview_code, language='python')
    with st.expander(label="Explain code"):
        st.write("This function finds the most similar movie to the user's input.\
                The cosine similarity between the overview of the input movie and all other movies\
                using a precomputed TF-IDF matrix is calculated.\
                The top 30 similar movies are then fetched and sorted by their release date from latest to earliest.")

st.subheader("Try out the movie recommendation engine!")
st.page_link("app.py", label="Go to the movie recommendation engine!", icon="👉")
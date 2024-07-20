import streamlit as st
import os
from components.data_handler import load_movie_data
from components.recommendation_engine import *
from components.ui_components import display_search_results
st.set_page_config(page_title="Cinematic Seeker", page_icon="🍿", 
                   initial_sidebar_state='collapsed', layout='wide')


# load pickle files
movie_overall_data = load_movie_data("movie_overall_data.pkl.gz")
movie_genre_data = load_movie_data("movie_genres_rec_data.pkl.gz")
movie_lang_data = load_movie_data("movie_language_rec_data.pkl.gz")

st.title("Cinematic Seeker 🍿")
st.markdown(f'''<i>Search for movie title or get movie title recommendations!</i>''', unsafe_allow_html=True)
st.page_link("pages/guide.py", label="Learn how the recommendation engine works", icon="👉", )

with st.sidebar:
    st.link_button("See Github repository💡", 
                   url="https://github.com/phyosandarwin/movie-recommendation-engine", type='primary', use_container_width=True)
    st.write("Made by Phyo Sandar Win 💙")

tab1, tab2, tab3, tab4 = st.tabs(["Movie Title Search", "Recommend by Genre", 
                                  "Recommend by Language", "Recommend by Similar Plot"])

with tab1:
    movie_title = st.text_input(label="Input Movie Title", placeholder="Inside out...", key="title_input")
    
    if st.button("Search 🔍", key="title_search_btn"):
        search_results = search_movie_title(movie_overall_data, movie_title)
        if not search_results.empty:
            display_search_results(search_results)
        else:
            st.info("No movies found.")

with tab2:
    genre_list = ['Action', 'Adventure', 'Animation', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family', 
                  'Fantasy', 'History', 'Horror', 'Music', 'Mystery', 'Romance', 'Science Fiction', 
                  'TV Movie', 'Thriller', 'War', 'Western']
    
    selected_genres = st.multiselect(label="Select movie genres", options= genre_list)
    
    if st.button("Get Recommendations!", type='primary', key="genre_search_btn"):
        search_results = recommend_movies_by_genres(movie_genre_data, selected_genres)
        if not search_results.empty:
            display_search_results(search_results)
        else:
            st.info("No movies found.")

with tab3:
    language_list = ['Abkhazian', 'Afrikaans', 'Akan', 'Albanian', 'Amharic', 'Arabic', 'Armenian', 
                     'Assamese', 'Aymara', 'Azerbaijani', 'Bambara', 'Bangla', 'Basque', 'Belarusian', 
                     'Bislama', 'Bosnian', 'Bulgarian', 'Burmese', 'Catalan', 'Chinese', 'Cornish', 'Cree',
                     'Croatian', 'Czech', 'Danish', 'Divehi', 'Dutch', 'Dzongkha', 'English', 'Esperanto',
                     'Estonian', 'Faroese', 'Filipino', 'Finnish', 'French', 'Fula', 'Galician', 'Georgian', 
                     'German', 'Greek', 'Guarani', 'Gujarati', 'Haitian Creole', 'Hausa', 'Hebrew', 'Hindi',
                     'Hungarian', 'Icelandic', 'Igbo', 'Indonesian', 'Interlingue', 'Inuktitut', 'Inupiaq',
                     'Irish', 'Italian', 'Japanese', 'Javanese', 'Kalaallisut', 'Kannada', 'Kashmiri', 'Kazakh', 
                     'Khmer', 'Kinyarwanda', 'Korean', 'Kurdish', 'Kyrgyz', 'Lao', 'Latin', 'Latvian', 'Limburgish',
                     'Lingala', 'Lithuanian', 'Luxembourgish', 'Macedonian', 'Malagasy', 'Malay', 'Malayalam', 'Maltese',
                     'Marathi', 'Mongolian', 'Māori', 'Navajo', 'Nepali', 'North Ndebele', 'Northern Sami', 'Norwegian',
                     'Norwegian Bokmål', 'Norwegian Nynorsk', 'Nyanja', 'Odia', 'Oromo', 'Ossetic', 'Pashto', 'Persian',
                     'Polish', 'Portuguese', 'Punjabi', 'Quechua', 'Romanian', 'Romansh', 'Russian', 'Samoan', 'Sango',
                     'Sanskrit', 'Sardinian', 'Scottish Gaelic', 'Serbian', 'Serbian (Latin)', 'Shona', 'Sinhala',
                     'Slovak', 'Slovenian', 'Somali', 'Southern Sotho', 'Spanish', 'Sundanese', 'Swahili', 'Swedish',
                     'Tajik', 'Tamil', 'Tatar', 'Telugu', 'Thai', 'Tibetan', 'Tswana', 'Turkish', 'Turkmen', 'Twi',
                     'Ukrainian', 'Urdu', 'Uyghur', 'Uzbek', 'Vietnamese', 'Welsh', 'Western Frisian', 'Wolof', 'Xhosa',
                     'Yiddish', 'Yoruba', 'Zulu']
    
    selected_language = st.selectbox(label="Select language", options = language_list, index= 28)

    if st.button("Get Recommendations!", type='primary',key="lang_search_btn"):
        search_results = recommend_movies_by_language(movie_lang_data, selected_language)
        if not search_results.empty:
            display_search_results(search_results)
        else:
            st.info("No movies found.")

with tab4:
    movie_title = st.text_input(label="Input Movie Title", placeholder="Inside out...", key="overview_movie_input")
    
    if st.button("Get Recommendations!", type='primary', key="overview_search_btn"):
        search_results = search_movie_overview(movie_overall_data, movie_title)
        if not search_results.empty:
            display_search_results(search_results)
        else:
            st.info("No movies found.")
    

              







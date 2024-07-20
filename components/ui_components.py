import streamlit as st

def display_search_results(search_results):
    num_cols = 3
    num_rows = (len(search_results) + num_cols - 1) // num_cols

    for row_index in range(num_rows):
        cols = st.columns(num_cols)
        for col_index in range(num_cols):
            data_index = row_index * num_cols + col_index
            if data_index < len(search_results):
                row = search_results.iloc[data_index]
                with cols[col_index]:
                    image = row['poster_path']
                    title = row['title']
                    overview = row['overview']
                    release_date = row['release_date'].strftime('%Y-%m-%d')
                    runtime = row['runtime']
                    vote_average = row['vote_average']

                    st.markdown(
                        f"""
                        <div style="display: flex; flex-direction: column; border: 2px solid gray; background-color: #dbdbdb; border-radius: 10px; padding: 1.25rem; margin-bottom: 10px;">
                            {'<img src="' + image + '" style="width:100%; border-radius: 8px;" />' if image else ''}
                            <h4>{title}</h4>
                            <p><b>Rating:</b> {vote_average}</p>
                            <p><b>Runtime:</b> {runtime} mins</p>
                            <p><b>Release Date:</b> {release_date}</p>
                            <div style="max-height: 200px; overflow-y: auto;">
                                <p style="margin-bottom: 0;"><b>Overview:</b> {overview}</p>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
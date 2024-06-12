import streamlit as st
from PIL import Image
import json
from Classifier import KNearestNeighbours

with open('./Data/movie_data.json', 'r+', encoding='utf-8') as f:
    data = json.load(f)
with open('./Data/movie_titles.json', 'r+', encoding='utf-8') as f:
    movie_titles = json.load(f)
hdr = {'User-Agent': 'Mozilla/5.0'}

def KNN_Movie_Recommender(test_point, k):
    # Create dummy target variable for the KNN Classifier
    target = [0 for item in movie_titles]
    # Instantiate object for the Classifier
    model = KNearestNeighbours(data, target, test_point, k=k)
    # Run the algorithm
    model.fit()
    # Print list of recommendations
    table = []
    for i in model.indices:
        # Returns movie title, IMDb link, and rating
        table.append([movie_titles[i][0], movie_titles[i][2], data[i][-1]])
    return table

st.set_page_config(page_title="CineScribe")

# Add custom CSS for the gradient background
st.markdown(
    """
    <style>
/* Custom CSS for CineScribe */
body {
    background: linear-gradient(to right, #3a6186, #89253e);
    color: white;
}
.main .block-container {
    background: linear-gradient(to bottom, #1c1c1c, #0d0d0d);  /* Blackish tones */
    border-radius: 10px;
    padding: 20px;
}
h1 {
    color: #FFFFFF;
}
.stButton>button {
    background-color: #1E3C72;
    color: white;
}
.stSlider>div>div>div>div {
    background: #1E3C72;
}
.movie-container {
    background: #2a5298;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 10px;
}
.movie-container:nth-child(even) {
    background: #3a6186;
}
a {
    color: white; /* Change link color to white */
    text-decoration: none; /* Remove underline */
}
/* Change recommendation type box color */
.css-1k5bxof select {
    background-color: #504C4E !important;
    color: white !important;
}
footer {
    background: linear-gradient(to bottom, #1c1c1c, #0d0d0d);
    color: #FFFFFF;
    text-align: center;
    font-size: large;
    padding: 10px;
}
</style>



    """,
    unsafe_allow_html=True
)

def run():
    st.markdown('''<h1 style='text-align:center;'>CineScribe</h1>''', unsafe_allow_html=True)
    
    img1 = Image.open('./meta/logo.png')
    img1 = img1.resize((650, 250))
    st.image(img1, use_column_width=False)

    genres = ['Action', 'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Family',
              'Fantasy', 'Film-Noir', 'Game-Show', 'History', 'Horror', 'Music', 'Musical', 'Mystery', 'News',
              'Reality-TV', 'Romance', 'Sci-Fi', 'Short', 'Sport', 'Thriller', 'War', 'Western']
    movies = [title[0] for title in movie_titles]
    category = ['--Select--', 'Movie based', 'Genre based']
    cat_op = st.selectbox('Select Recommendation Type', category)
    if cat_op == category[0]:
        st.warning('Please select Recommendation Type!!')
    elif cat_op == category[1]:
        select_movie = st.selectbox('Select movie: (Recommendation will be based on this selection)',
                                    ['--Select--'] + movies)
        if select_movie == '--Select--':
            st.warning('Please select Movie!!')
        else:
            no_of_reco = st.slider('Number of movies you want Recommended:', min_value=5, max_value=20, step=1)
            genres = data[movies.index(select_movie)]
            test_points = genres
            table = KNN_Movie_Recommender(test_points, no_of_reco + 1)
            table.pop(0)
            c = 0
            st.success('Some of the movies from our Recommendation, have a look below')
            for movie, link, ratings in table:
                c += 1
                st.markdown(f"<div class='movie-container'>"
                            f"<p>({c}) <a href='{link}' target='_blank'>{movie}</a></p>"
                            f"<p>IMDB Rating: {ratings} ⭐</p>"
                            "</div>", unsafe_allow_html=True)
    elif cat_op == category[2]:
        sel_gen = st.multiselect('Select Genres:', genres)
        if sel_gen:
            imdb_score = st.slider('Choose IMDb score:', 1, 10, 8)
            no_of_reco = st.number_input('Number of movies:', min_value=5, max_value=20, step=1)
            test_point = [1 if genre in sel_gen else 0 for genre in genres]
            test_point.append(imdb_score)
            table = KNN_Movie_Recommender(test_point, no_of_reco)
            c = 0
            st.success('Some of the movies from our Recommendation, have a look below')
            for movie, link, ratings in table:
                c += 1
                st.markdown(f"<div class='movie-container'>"
                            f"<p>({c}) <a href='{link}' target='_blank'>{movie}</a></p>"
                            f"<p>IMDB Rating: {ratings} ⭐</p>"
                            "</div>", unsafe_allow_html=True)

    st.text(" ")
    st.markdown(
        """
        <footer>Handcrafted by Anish(Machine Learning Enthusiast)</footer>
        """,
        unsafe_allow_html=True
    )

run()

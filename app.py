import pickle
import streamlit as st
import requests

st.header("Movie Recommender System using ML")

# Load Data
movies = pickle.load(open('artifacts/movies.pkl', 'rb'))
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))

# Dropdown for movie selection
movie_list = movies['title'].values
selected_movie = st.selectbox(
    'Type or select a movie',
    movie_list
)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=292d13212bbaf0d5533dbcf9908d3257".format(movie_id)
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/original" + data['poster_path']
    else:
        return "https://via.placeholder.com/300"  # Placeholder if no poster

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies_name = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id  # Ensure movie_id exists
        recommended_movies_poster.append(fetch_poster(movie_id))
        recommended_movies_name.append(movies.iloc[i[0]].title)
    
    return recommended_movies_name, recommended_movies_poster

if st.button('Show Recommendation'):
    recommended_movies_name, recommended_movies_poster = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movies_name[0])
        st.image(recommended_movies_poster[0])
    with col2:
        st.text(recommended_movies_name[1])
        st.image(recommended_movies_poster[1])
    with col3:
        st.text(recommended_movies_name[2])
        st.image(recommended_movies_poster[2])
    with col4:
        st.text(recommended_movies_name[3])
        st.image(recommended_movies_poster[3])
    with col5:
        st.text(recommended_movies_name[4])
        st.image(recommended_movies_poster[4])

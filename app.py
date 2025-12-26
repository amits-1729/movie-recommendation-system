import streamlit as st
import pickle
import pandas as pd
import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("TMDB_API_KEY")

@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": API_KEY,
        "language": "en-US"
    }

    try:
        response = requests.get(url, params=params, timeout=7)
        response.raise_for_status()

        data = response.json()
        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster"

    except requests.exceptions.RequestException as e:
        print("Poster fetch error:", e)
        return "https://via.placeholder.com/300x450?text=Error"


def recommend(movie):
    if movie not in movies['title'].values:
        return [], []

    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_movies_posters = []

    for idx, _ in movies_list:
        movie_title = movies.iloc[idx].title
        movie_id = movies.iloc[idx].movie_id

        recommend_movies.append(movie_title)
        recommend_movies_posters.append(fetch_poster(movie_id))

    return recommend_movies, recommend_movies_posters


movies_dict = pickle.load(open('movies_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

st.title("Movie Recommender System")

selected_movie_name = st.selectbox('Select the movie',movies['title'].values)

if st.button('Recommend'):
    name,posters = recommend(selected_movie_name)


    col1, col2, col3 = st.columns(3)

    with col1:
        st.text(name[0])
        st.image(posters[0])

    with col2:
        st.text(name[1])
        st.image(posters[1])

    with col3:
        st.text(name[2])
        st.image(posters[2])


    col4, col5, col6 = st.columns(3)
    with col4:
        st.text(name[3])
        st.image(posters[3])

    with col5:
        st.text(name[4])
        st.image(posters[4])
import streamlit as st
import pickle
import pandas as pd
import requests

def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=ee312f5b66b54a6f9bf71979ae620ad1&language=en-US'.format(
            movie_id))
    data = response.json()
    print(data)
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommend_movies.append(movies.iloc[i[0]].title)
        # fetch poster from API
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters  # Ensure this line returns both lists


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
st.title('Movie Recommender System')
selected_movie_name = st.selectbox(
    "How would you like to be contacted?",
    movies['title'].values)

if st.button("Recommend"):
    recommend_movie_names, recommend_movie_posters = recommend(selected_movie_name)
    cols = st.columns(5)
    for j in range(5):  # Use 'j' here to iterate over the columns
        with cols[j]:  # Use 'j' here to match the column index
            st.text(recommend_movie_names[j])  # Use 'j' here to access the movie name
            st.image(recommend_movie_posters[j])  # Use 'j' here to access the poster URL

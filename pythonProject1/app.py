import streamlit as st
import pickle
import pandas as pd


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(movies.iloc[i[0]].poster)
    return recommended_movies, recommended_posters

# load the data
movies_dict = pickle.load(open('movie_dict_with_posters.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

movie_list = movies['title'].values
selected_movie = st.selectbox("Select a movie", movie_list)

if st.button('Recommend'):
    names, posters = recommend(selected_movie)
    cols = st.columns(5)   # create 5 columns (side by side)
    for i in range(5):     # Loops through all 5 movies.
        with cols[i]:      # Puts each movie inside its own column.
            st.image(posters[i], width=120)
            st.write(names[i])

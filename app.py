import pickle
import streamlit as st
import requests

# ----------------------
# 1. Load movie data first
# ----------------------
movies = pickle.load(open('movie_list.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
movie_list = movies['title'].values

# ----------------------
# 2. Fetch poster from OMDb
# ----------------------
def fetch_poster(movie_title):
    api_key = "835f4b15"  # Your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    data = requests.get(url).json()
    if "Poster" in data and data["Poster"] != "N/A":
        return data["Poster"]
    else:
        # Placeholder if no poster found
        return "https://via.placeholder.com/300x450?text=No+Image"

# ----------------------
# 3. Recommendation function
# ----------------------
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:  # top 5 recommendations
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].title))

    return recommended_movie_names, recommended_movie_posters

# ----------------------
# 4. Streamlit UI
# ----------------------
st.header('Movie Recommender System')

# Dropdown to select movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

# Button to show recommendations
if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display recommendations in columns
    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movie_names, recommended_movie_posters):
        with col:
            st.text(name)
            st.image(poster)

import pickle
import pandas as pd
import streamlit as st
import requests
import random
import os
import gdown
from concurrent.futures import ThreadPoolExecutor

# 🔑 TMDB API Key
API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# 📥 Download similarity.pkl from Google Drive if not present
@st.cache_resource
def download_similarity_file():
    file_id = "1N01JBtIScxb9ppqJFbJV2SNUnUoOtIo_"  # 🔁 Replace this with your Google Drive file ID
    url = f"https://drive.google.com/uc?id={file_id}"
    output = "similarity.pkl"
    if not os.path.exists(output):
        gdown.download(url, output, quiet=False)

download_similarity_file()

# 📦 Load movie_dict and similarity matrix
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# 🖼️ Fetch poster image from TMDB
@st.cache_data(show_spinner=False)
def fetch_movie_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500{poster_path}"
        else:
            return "https://via.placeholder.com/300x450.png?text=No+Image"
    except:
        return "https://via.placeholder.com/300x450.png?text=Error"

# 🎯 Recommend similar movies
@st.cache_data(show_spinner=False)
def recommend(movie):
    if movie not in movies['title'].values:
        return [], [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    titles, ids, links = [], [], []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        titles.append(movies.iloc[i[0]].title)
        ids.append(movie_id)
        links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        posters = list(executor.map(fetch_movie_poster, ids))

    return titles, posters, links

# 🌐 Streamlit UI
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie", movie_list, key="movie_selector")

if st.button("🎲 Surprise Me"):
    selected_movie = random.choice(movie_list)
    st.success(f"🎉 Randomly selected: **{selected_movie}**")

if st.button("🎯 Show Recommendation"):
    with st.spinner("🔎 Fetching recommendations..."):
        names, posters, links = recommend(selected_movie)

    if not names:
        st.warning("No recommendations found.")
    else:
        st.subheader("🎞️ Recommended Movies")
        for i in range(len(names)):
            st.markdown(f"- [{names[i]}]({links[i]})")

        st.divider()
        st.subheader("🖼️ Posters")
        cols = st.columns(5)
        for i in range(min(5, len(posters))):
            with cols[i]:
                st.image(posters[i], caption=names[i], use_container_width=True)

import pickle
import pandas as pd
import streamlit as st
import requests
import random
from concurrent.futures import ThreadPoolExecutor

API_KEY = "8265bd1679663a7ea12ac168da84d2e8"

# --- Load model files ---
try:
    movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movie_dict)
    similarity = pickle.load(open('similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"❌ Failed to load data: {e}")
    st.stop()

# --- Cached poster fetch (without year) ---
@st.cache_data(show_spinner=False)
def fetch_movie_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=2)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get("poster_path")
            return (
                f"https://image.tmdb.org/t/p/w342/{poster_path}"
                if poster_path else
                "https://via.placeholder.com/342x513.png?text=No+Image"
            )
    except:
        pass
    return "https://via.placeholder.com/342x513.png?text=No+Image"

# --- Cached movie recommendation logic ---
@st.cache_data(show_spinner=False)
def recommend(movie):
    if movie not in movies['title'].values:
        return [], [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    titles = []
    ids = []
    links = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        titles.append(movies.iloc[i[0]].title)
        ids.append(movie_id)
        links.append(f"https://www.themoviedb.org/movie/{movie_id}")

    with ThreadPoolExecutor(max_workers=2) as executor:
        posters = list(executor.map(fetch_movie_poster, ids))

    return titles, posters, links

# --- Streamlit UI ---
st.set_page_config(layout="wide")
st.title("🎬 Movie Recommender System")

# --- Movie selector ---
movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Select a movie", movie_list, key="movie_selector")

# --- Surprise Me button ---
if st.button("🎲 Surprise Me"):
    selected_movie = random.choice(movie_list)
    st.success(f"🎉 Randomly selected: **{selected_movie}**")

# --- Show Recommendations button ---
if st.button("🎯 Show Recommendation"):
    with st.spinner("🔎 Fetching recommendations..."):
        names, posters, links = recommend(selected_movie)

    if not names:
        st.warning("No recommendations found.")
    else:
        # Vertical list of recommended movies
        st.subheader("🎞️ Recommended Movies")
        for i in range(len(names)):
            st.markdown(f"- [{names[i]}]({links[i]})")

        st.divider()

        # Poster grid
        st.subheader("🖼️ Posters")
        cols = st.columns(5)
        for i in range(5):
            with cols[i]:
                st.image(posters[i], caption=names[i], use_container_width=True)

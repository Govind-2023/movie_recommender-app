import pickle
import streamlit as st
import requests
import pandas as pd
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Movie Recommender", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }

    /* FIX: Make Selectbox and Input labels visible */
    .stSelectbox label, .stMultiSelect label, div[data-testid="stText"] p {
        color: #ffffff !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
    }

    /* Header styling */
    h1 {
        color: #E50914 !important; 
        font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif;
        font-weight: bold;
        text-align: center;
    }

    /* Movie Poster Styling */
    div[data-testid="stImage"] img {
        border-radius: 15px;
        transition: transform .3s ease;
        box-shadow: 0 4px 15px rgba(0,0,0,0.5);
    }
    div[data-testid="stImage"] img:hover {
        transform: scale(1.05);
    }

    /* Centered Movie Titles */
    .movie-card-title {
        color: #ffffff;
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        margin-top: 10px;
        height: 40px;
        overflow: hidden;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #E50914;
        color: white;
        border: none;
        border-radius: 5px;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #ff1e2b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)


def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=733330b25ad948f31c84d81b2b35ed17&language=en-US"
    try:
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

    names, posters = [], []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        posters.append(fetch_poster(movie_id))
        names.append(movies.iloc[i[0]].title)
    return names, posters


# Load data
current_path = os.path.dirname(__file__)
movies_dict = pickle.load(open(os.path.join(current_path, 'movie_dict.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(os.path.join(current_path, 'similarity.pkl'), 'rb'))

st.title('🎬 Movie Recommender System')

# --- UI LAYOUT ---
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    selected_movie = st.selectbox(
        "What would you like to watch?",  # This label is now white!
        movies['title'].values
    )
    recommend_btn = st.button('Recommend Now', use_container_width=True)

if recommend_btn:
    names, posters = recommend(selected_movie)
    st.write("### Recommended for You:")

    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.markdown(f"<div class='movie-card-title'>{names[i]}</div>", unsafe_allow_html=True)
            st.image(posters[i])
            # Added a direct link to YouTube search for the trailer
            yt_link = f"https://www.youtube.com/results?search_query={names[i].replace(' ', '+')}+trailer"
            st.link_button("🎥 Trailer", yt_link, use_container_width=True)
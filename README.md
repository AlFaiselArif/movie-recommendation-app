# 🎬 Movie Recommendation System

This project is a simple content-based movie recommender system that suggests movies similar to the one selected by the user. It uses a precomputed cosine similarity matrix for fast recommendations.

Built with:
- Python
- Pandas
- scikit-learn
- Streamlit


## 🚀 Live Demo
Try it here: [Movie Recommender App](https://movie-recommendation-app-yknvhu6yzbhapsewhq7sew.streamlit.app/)


## 📂 Dataset Used

- 📄 **movies.csv** – Contains cleaned metadata for over 4,800 movies
- ❌ **credits.csv** – *Not included due to file size limitations (>25MB)*

If you'd like to recreate the full dataset locally, you can download both from Kaggle:

👉 [TMDB Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_movies.csv)

Or, download the original `credits.csv` here:  
📥 [credits.csv – [TMDB Movie Dataset on Kaggle](https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata?select=tmdb_5000_credits.csv)



## 🧠 How It Works

- The system uses movie metadata such as genres, keywords, cast, and crew.
- Text features are vectorized using `CountVectorizer`.
- Cosine similarity is calculated between all movie vectors.
- The top 5 similar movies are shown when a user selects one.

## 🗂️ Files Included

- `app.py` – Streamlit UI code
- `movies.csv` – Cleaned dataset with metadata
- `similarity.pkl` – Precomputed similarity matrix (⚠️ not included due to file size)
- `requirements.txt` – Python dependencies

## ⚠️ similarity.pkl Not Included

Due to GitHub's file size limit (100 MB), the `similarity.pkl` file is **not included** in this repository.

You can generate it by running the `generate_similarity.py` script (see below), or download it from this link:

📥 https://drive.google.com/file/d/1N01JBtIScxb9ppqJFbJV2SNUnUoOtIo_/view?usp=drivesdk

> Note: You must place the `similarity.pkl` file in the root folder to run the app locally.


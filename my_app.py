
import streamlit as st
import pandas as pd

# Load the dataset
df = pd.read_csv("https://raw.githubusercontent.com/krishna-koly/IMDB_TOP_1000/main/imdb_top_1000.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Function to get top movies by genre
def top_movies_by_genre(genre, df, top_n=5):
    df['genre'] = df['genre'].str.lower()
    filtered = df[df['genre'].str.split(', ').apply(lambda x: any(genre.lower() in g for g in x))]
    if filtered.empty:
        return None
    top_movies = filtered.sort_values(by='imdb_rating', ascending=False).head(top_n)
    return top_movies[['series_title', 'genre', 'imdb_rating']]

# Streamlit app
st.title("Top IMDb Movies by Genre")

# Genre selection
genre_options = df['genre'].str.split(', ').explode().unique()
selected_genre = st.selectbox("Select a genre:", genre_options)

# Number of top movies
top_n = st.slider("Number of top movies:", min_value=1, max_value=20, value=5)

# Get top movies
top_movies = top_movies_by_genre(selected_genre, df, top_n)

# Display results
if top_movies is not None:
    st.table(top_movies)
else:
    st.write(f"No movies found for the genre '{selected_genre}'. Please try again.")
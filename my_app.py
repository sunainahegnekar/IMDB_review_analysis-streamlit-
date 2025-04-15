
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

#sorting and rating
sort_by_rating = st.checkbox("Sort by Rating (Descending)")

if top_movies is not None:
    if sort_by_rating:
        top_movies = top_movies.sort_values(by='imdb_rating', ascending=False)
    st.table(top_movies)    


#search for movies
search_term = st.text_input("Search for a movie:")

if search_term:
    filtered_movies = df[df['series_title'].str.contains(search_term, case=False)]
    st.table(filtered_movies)

#Display movie details

# ... (other code)
if top_movies is not None:  # Check if top_movies DataFrame is not empty
    # ... (sorting and filtering logic)  # Apply any sorting or filtering based on user input

    # Create a selectbox to choose a movie for details
    selected_movie = st.selectbox("Select a movie for details:", top_movies['series_title']) 
    
    if selected_movie:  # Check if a movie has been selected
        # Get details for the selected movie
        movie_details = df[df['series_title'] == selected_movie].iloc[0]  
        
        # Display movie details
        st.write(f"**Director:** {movie_details['director']}")  
        st.write(f"**Actors:** {movie_details['star1']}, {movie_details['star2']}, {movie_details['star3']}, {movie_details['star4']}") 
        # ... (display other details)  # You can add more details here

#downloading

# ... (other code)
if top_movies is not None:
    # ... (sorting and filtering logic)
    st.download_button(
        label="Download data as CSV",
        data=top_movies.to_csv(index=False).encode('utf-8'),
        file_name='top_movies.csv',
        mime='text/csv',
    )


#graphs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#runtime distribution
fig, ax = plt.subplots()
sns.histplot(df['runtime'], bins=30, kde=True, ax=ax)
ax.set_title("Runtime Distribution")
ax.set_xlabel("Runtime (minutes)")
ax.set_ylabel("Count")
st.pyplot(fig)

#Rating Distribution:
fig, ax = plt.subplots()
sns.histplot(df['imdb_rating'], bins=20, kde=True, ax=ax)
ax.set_xlabel("IMDb Rating")
ax.set_ylabel("Count")
st.pyplot(fig)
ax.set_title("Rating Distribution")


#piecharts
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ... (load and clean data, other app code)

# 1. Pie Chart of Rating Categories:

# Create rating categories (e.g., Excellent, Good, Average)
def rating_category(rating):
    if rating >= 8.5:
        return 'Excellent'
    elif rating >= 7.0:
        return 'Good'
    else:
        return 'Average'
df['rating_category'] = df['imdb_rating'].apply(rating_category)

# Count movies in each rating category
rating_counts = df['rating_category'].value_counts()

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(rating_counts, labels=rating_counts.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title("Distribution of Movies by Rating Category")
st.pyplot(fig)


# 2. Pie Chart of Top Genres:

# Get the top 5 genres
top_genres = df['genre'].str.split(', ').explode().value_counts().head(5)

# Create the pie chart
fig, ax = plt.subplots()
ax.pie(top_genres, labels=top_genres.index, autopct='%1.1f%%', startangle=90)
ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax.set_title("Top 5 Genres")
st.pyplot(fig)

#bargraph
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ... (load and clean data, other app code)

# Get the number of movies per genre
genre_counts = df['genre'].str.split(', ').explode().value_counts()

# Create the vertical bar graph
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
ax.barh(genre_counts.index, genre_counts.values)  # Create horizontal bar plot
ax.set_title("Number of Movies by Genre")  # Set title
ax.set_xlabel("Number of Movies")  # Set x-axis label
ax.set_ylabel("Genre")  # Set y-axis label
st.pyplot(fig)  # Display the plot in Streamlit


# Runtime vs Rating
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ... (load and clean data, other app code)

# Create the scatterplot
fig, ax = plt.subplots(figsize=(10, 6))  # Adjust figure size as needed
ax.scatter(df['runtime'], df['imdb_rating'])  # Create scatter plot
ax.set_title("Runtime vs. IMDb Rating")  # Set title
ax.set_xlabel("Runtime (minutes)")  # Set x-axis label
ax.set_ylabel("IMDb Rating")  # Set y-axis label
st.pyplot(fig)  # Display the plot in Streamlit


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ... (load and clean data, other app code)

# Top Actors Analysis
all_actors = pd.concat([df['star1'], df['star2'], df['star3'], df['star4']])
top_actors = all_actors.value_counts().head(10)

fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(x=top_actors.values, y=top_actors.index, palette="viridis", ax=ax)
ax.set_title("Top 10 Most Frequent Actors in Top 1000 IMDB Movies")
ax.set_xlabel("Number of Appearances")
ax.set_ylabel("Actor")
st.pyplot(fig)  # Display using Streamlit


import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ... (load and clean data, other app code)

# Correlation Heatmap
numeric_cols = df.select_dtypes(include=['float64', 'int64'])
fig, ax = plt.subplots(figsize=(10, 8))  # Create a Matplotlib figure and axes
sns.heatmap(numeric_cols.corr(), annot=True, cmap='coolwarm', center=0, ax=ax)  # Plot on the axes
ax.set_title("Correlation Heatmap of Numerical Features")  # Set title on the axes
st.pyplot(fig)  # Display using Streamlit


import streamlit as st
import pandas as pd

# ... (load and clean data, other app code)

# Advanced Filtering and Search
st.sidebar.title("Filters")

# Multi-Select Genre Filtering
genre_options = df['genre'].str.split(', ').explode().unique()
selected_genres = st.sidebar.multiselect("Select Genres:", genre_options, default=genre_options)

# Actor/Director Filtering
actor_options = pd.concat([df['star1'], df['star2'], df['star3'], df['star4']]).unique()
selected_actors = st.sidebar.multiselect("Select Actors:", actor_options)

director_options = df['director'].unique()
selected_directors = st.sidebar.multiselect("Select Directors:", director_options)

# Keyword Search
search_term = st.sidebar.text_input("Search by Keyword:")


# Function to filter movies based on selected criteria
def filter_movies(df, genres, actors, directors, search_term):
    filtered_df = df.copy()

    # Filter by genres
    if genres:
        filtered_df = filtered_df[filtered_df['genre'].str.contains('|'.join(genres))]

    # Filter by actors
    if actors:
        filtered_df = filtered_df[filtered_df[['star1', 'star2', 'star3', 'star4']].apply(lambda row: any(actor in row.values for actor in actors), axis=1)]
    
    # Filter by directors
    if directors:
        filtered_df = filtered_df[filtered_df['director'].isin(directors)]

    # Filter by search term
    if search_term:
        filtered_df = filtered_df[filtered_df['series_title'].str.contains(search_term, case=False)]

    return filtered_df


# Filter the movies
filtered_movies = filter_movies(df, selected_genres, selected_actors, selected_directors, search_term)

# ... (rest of your app code to display filtered movies)


import pandas as pd

# ... (load and clean data, other app code)

def top_movies_by_rating(min_rating, df, top_n=5):
    # 1. Filter movies with rating >= min_rating:
    filtered = df[df['imdb_rating'] >= min_rating]

    # 2. Handle empty results:
    if filtered.empty:
        print(f"No movies found with a rating of {min_rating} or higher. Please try again.")
        return None

    # 3. Sort and select top movies:
    top_movies = filtered.sort_values(by='imdb_rating', ascending=False).head(top_n)

    # 4. Print results:
    print(f"\n🎬 Top {top_n} movies with a rating of {min_rating} or higher:\n")
    return top_movies[['series_title', 'genre', 'imdb_rating']]


# Clean column names
df.columns = df.columns.str.strip().str.lower()

# Take input for rating
min_rating_input = float(input("Enter a minimum rating (e.g., 8.0): "))
top_n = int(input("How many top movies do you want to see? (e.g., 5): "))

# Recommend
top_movies_rating = top_movies_by_rating(min_rating_input, df, top_n)

# Show
if top_movies_rating is not None:
    print(top_movies_rating.to_string(index=False))
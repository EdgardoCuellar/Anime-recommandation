import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the dataset
data = pd.read_csv("data/features.csv", skipinitialspace=True)

# Preprocess the data
data['genre'] = data['genre'].apply(lambda x: ' '.join(eval(x)))
data['favorites_anime'] = data['favorites_anime'].apply(lambda x: ' '.join(eval(x)))

# Create the TF-IDF vectorizer
vectorizer = TfidfVectorizer()

# Fit and transform the vectorizer to the genre and favorite_anime columns
genre_tfidf = vectorizer.fit_transform(data['genre'])
fav_tfidf = vectorizer.fit_transform(data['favorites_anime'])

# Compute the cosine similarity matrix for the genre and favorite_anime columns
genre_sim = cosine_similarity(genre_tfidf)
fav_sim = cosine_similarity(fav_tfidf)

# Define the recommendation function
def recommend_anime(anime_id):
    # Get the row index of the anime in the data
    idx = data[data['anime_uid'] == anime_id].index[0]

    # Compute the average similarity score for each anime based on genre and favorite_anime
    sim_scores = (genre_sim[idx] + fav_sim[idx]) / 2.0

    # Get the indices of the top 10 similar animes
    similar_indices = sim_scores.argsort()[:-11:-1]

    # Return the titles of the top 10 similar animes
    return data.iloc[similar_indices]['title']

# Test the recommendation function with an example anime id
recommend_anime(1535)

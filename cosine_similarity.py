import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("------------------")
print('Recommandation par la similarité du cosinus .......')
print("------------------")
dataset = pd.read_csv("data/animes_scored.csv", skipinitialspace=True) 

# Traiter la colonne "genre"
dataset['genre'] = dataset['genre'].apply(lambda x: x.join("") if isinstance(x, list) else x.replace("[", "").replace("]", "").replace("',", "").replace("'", ""))

# Remplir les valeurs manquantes dans la colonne "episodes" par la 1
dataset['episodes'] = dataset['episodes'].fillna(value=1)

# Convertir les scores en nombres décimaux
dataset["score"] = pd.to_numeric(dataset["score"], errors="coerce")

# Remplir les valeurs manquantes dans la colonne "score" par la moyenne
dataset["score"].fillna(dataset["score"].mean(), inplace=True)

# Créer une représentation vectorielle pour chaque anime en utilisant les colonnes "genre", "episodes"
anime_features = pd.concat([dataset["genre"].str.get_dummies(sep=" "), dataset[["episodes"]]], axis=1)

# Normaliser les caractéristiques
anime_features = (anime_features - anime_features.mean()) / anime_features.std()

# Définir la fonction de recommandation basée sur la similarité cosinus
def get_anime_recommendations(user_preferences, anime_features, anime_df, top_n=10):
    # Normaliser les préférences de l'utilisateur
    user_preferences_norm = (user_preferences - anime_features.mean()) / anime_features.std()

    # Calculer la similarité cosinus entre les préférences de l'utilisateur et les caractéristiques de chaque anime
    similarities = cosine_similarity(user_preferences_norm.values.reshape(1, -1), anime_features)[0]
    print(similarities)

    # # Trier les similarités dans l'ordre décroissant et récupérer les indices des animes correspondants
    # anime_indices = similarities.argsort()[::-1][:top_n]
   
    # # si anime_indices est un tableau vide alors on retourne un message d'erreur
    # if len(anime_indices) == 0:
    #     return "Aucun anime ne correspond à vos préférences"
    # else:
    #     # Récupérer les informations des animes correspondants
    #     anime_recommendations = anime_df.iloc[anime_indices].copy()

    #     # Ajouter une colonne "similarity" pour afficher la similarité entre chaque anime et les préférences de l'utilisateur
    #     anime_recommendations["similarity"] = similarities[anime_indices]

    #     return anime_recommendations[["title", "genre", "episodes", "score", "similarity"]]

# Exemple d'utilisation
user_preferences = pd.DataFrame({
    "Comedy": 1,
    "Sports": 1,
    "Drama": 0,
    "School": 1,
    "Shounen": 1,
    "episodes": 25}
    , index=[0])

recommendations = get_anime_recommendations(user_preferences, anime_features, dataset, top_n=10)
print(recommendations)








# # Vectoriser les données textuelles pour la similarité cosinus
# dataset["text_data"] = dataset["genre"].apply(lambda x: " ".join(x))
# count = CountVectorizer()
# count_matrix = count.fit_transform(dataset["text_data"])

# # Calculer la similarité cosinus entre les animes
# cosine_sim = cosine_similarity(count_matrix, count_matrix)

# # Fonction pour recommander des animes similaires en fonction de l'indice de l'anime
# def recommend_animes(anime_index, cosine_sim=cosine_sim):
#     # Récupérer les scores de similarité des animes
#     sim_scores = list(enumerate(cosine_sim[anime_index]))

#     # Trier les animes en fonction des scores de similarité
#     sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

#     # Sélectionner les 10 animes les plus similaires (en excluant l'anime lui-même)
#     sim_scores = sim_scores[1:11]

#     # Récupérer les indices des 10 animes les plus similaires
#     anime_indices = [i[0] for i in sim_scores]

#     # Renvoyer les titres des 10 animes les plus similaires
#     return anime_data["name"].iloc[anime_indices]

# # Exemple d'utilisation : recommander des animes similaires à l'anime d'indice 0
# print(recommend_animes(0))





# animes = pd.read_csv("data/animes.csv", skipinitialspace=True) 

# vectorizer = CountVectorizer()
# vectorized_bag_of_words = vectorizer.fit_transform(dataset['genre'])
# vectorized_bag_of_words = vectorized_bag_of_words.toarray()

# genre = dataset['genre']
# title = dataset['title']

# def recommender(show_title, n_recom):
#     similarity_matrix = cosine_similarity(vectorized_bag_of_words, vectorized_bag_of_words[list(np.where(title == show_title)[0]), :])
#     similarity_dataframe = pd.DataFrame(similarity_matrix)
#     similarity_dataframe.index = title 
#     similarity_dataframe =  similarity_dataframe.iloc[:,0]
#     similarity_dataframe = similarity_dataframe.sort_values(ascending = False)
#     similarity_dataframe = similarity_dataframe.drop_duplicates()
#     return list(similarity_dataframe.index)[1:n_recom + 1]

# print(recommender('Naruto', 10))
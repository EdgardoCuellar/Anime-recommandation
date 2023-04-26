import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import users_test


print("------------------------------------------------------------------------------------------------------------------------------------------------")
print("----Recommandation par la similarité du cosinus en considérant le genre d'animé de l'utilisateur, l'année de sortie et le nombre d'épisode .....")
print("------------------------------------------------------------------------------------------------------------------------------------------------")

dataset = pd.read_csv("data/animes_for_cs.csv", skipinitialspace=True) 

# # les differentes valeurs de la colonne "genre"
# print(dataset["genre"].unique())

# Traiter la colonne "genre"
dataset['genre'] = dataset['genre'].apply(lambda x: x.join("") if isinstance(x, list) else x.replace("[", "").replace("]", "").replace("',", "").replace("'", ""))

# Convertir les scores en nombres décimaux
dataset["score"] = pd.to_numeric(dataset["score"], errors="coerce")

# Remplir les valeurs manquantes dans la colonne "score" par la moyenne
dataset["score"].fillna(dataset["score"].mean(), inplace=True)

# Créer une représentation vectorielle pour chaque anime en utilisant les colonnes "genre", "episodes" et release_year
anime_features = pd.concat([dataset["genre"].str.get_dummies(sep=" "), dataset[["episodes"]], dataset[["release_year"]]], axis=1)

# Normaliser les caractéristiques
anime_features = (anime_features - anime_features.mean()) / anime_features.std()

# Définir la fonction de recommandation basée sur la similarité cosinus
def get_anime_recommendations(user_preferences, anime_features, anime_df, top_n=10):

    # Remplir les valeurs manquantes dans les préférences de l'utilisateur par 0
    user_preferences = user_preferences.fillna(0)

    # Normaliser les préférences de l'utilisateur
    user_preferences_norm = (user_preferences - anime_features.mean()) / anime_features.std()

    # supprimer les nan de la matrice
    user_preferences_norm = np.nan_to_num(user_preferences_norm)

    # Calculer la similarité cosinus entre les préférences de l'utilisateur et les caractéristiques de chaque anime
    similarities = cosine_similarity(user_preferences_norm.reshape(1, -1), anime_features)[0]
    # print(similarities)

    # Trier les similarités dans l'ordre décroissant et récupérer les indices des animes correspondants
    anime_indices = similarities.argsort()[::-1][:top_n]
   
    # si anime_indices est un tableau vide alors on retourne un message d'erreur
    if len(anime_indices) == 0:
        return "Aucun anime ne correspond à vos préférences"
    else:
        # Récupérer les informations des animes correspondants
        anime_recommendations = anime_df.iloc[anime_indices].copy()

        # Ajouter une colonne "similarity" pour afficher la similarité
        # entre chaque anime et les préférences de l'utilisateur
        anime_recommendations["similarity"] = similarities[anime_indices]

        return anime_recommendations[["title", "genre", "episodes", "release_year", "similarity"]]

# Exemple d'utilisation
user_preferences = pd.DataFrame(users_test.USER_8['user_genre_preference'], index=[0])

recommendations = get_anime_recommendations(user_preferences, anime_features, dataset, top_n=10)
print(recommendations)





print("---------------------------------------------------------------------------------------------")
print(".............................................................................................")
print("---------------------------------------------------------------------------------------------")

# Vectoriser les données textuelles pour la similarité cosinus
count = CountVectorizer()
count_matrix = count.fit_transform(dataset["genre"])

# Calculer la similarité cosinus entre les animes
cosine_sim = cosine_similarity(count_matrix, count_matrix)

# Fonction pour recommander des animes similaires en fonction de l'indice de l'anime
def recommend_animes(anime_index, cosine_sim=cosine_sim):

    # Récupérer les scores de similarité des animes
    sim_scores = list(enumerate(cosine_sim[anime_index]))

    # Trier les animes en fonction des scores de similarité
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Sélectionner les 10 animes les plus similaires (en excluant l'anime lui-même)
    sim_scores = sim_scores[1:11]

    # Récupérer les indices des 10 animes les plus similaires
    anime_indices = [i[0] for i in sim_scores]

    # Renvoyer les titres des 10 animes les plus similaires
    return dataset["title"].iloc[anime_indices]

anime_index = 100 

# récuperer le titre de l'anime
anime_title = dataset["title"][anime_index]

# récupérer les genre de l'anime
anime_genre = dataset["genre"][anime_index] 

print("Recommandation par la similarité du cosinus en considérant seulement le genre de : ", anime_title)
print("Les genres sont : ", anime_genre)
print("........................................................................................................ ")
# Exemple d'utilisation : recommander des animes similaires à l'anime d'indice 0
print(recommend_animes(anime_index))
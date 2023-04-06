# la librairie principale pour la gestion des données
import pandas as pd

# l'emplacement des données sur le disque
data_path = "donnees/"

# chargement des données
animes = pd.read_csv(data_path + "animes.csv", skipinitialspace=True)
profiles = pd.read_csv(data_path + "profiles.csv", skipinitialspace=True)
reviews = pd.read_csv(data_path + "reviews.csv", skipinitialspace=True)


# Imprimer la taille de chaque table de données
print("Taille des données:")
print("------------------")
print("animes:\t", len(animes))
print("profiles:\t\t\t", len(profiles))
print("reviews:\t\t", len(reviews))
print("------------------")


# Initialisation du Dataframe "features" qui va contenir l'ensemble de données d'entrainement
features = animes[['uid', 'title', 'genre', 'episodes', 'aired']].copy()
features = features.rename(columns={'uid': 'anime_uid'}) 

reviews_columns = reviews[['profile', 'anime_uid','score','scores']].copy()
features = features.merge(reviews_columns, on='anime_uid', how='left')

profiles_columns = profiles[['profile', 'gender', 'favorites_anime']].copy()
features = features.merge(profiles_columns, on='profile', how='left')


# Remplacement des valeurs manquantes de la colonne gender, episodes, score et scores par des valeurs par défaut
features[['gender']] = features[['gender']].fillna(value='Undefined')
features[['episodes']] = features[['episodes']].fillna(value=1)
# features[['score']] = features[['score']].fillna(value=0)
scores_specs = {'Overall': '1', 'Story': '1', 'Animation': '1', 'Sound': '1', 'Character': '1', 'Enjoyment': '1'}
# features[['scores']] = features[['scores']].fillna(value=scores_specs)
print(features.isnull().sum())

print(features['score'].unique())
print(features['profile'].unique())

# réorganisation des colonnes
features.reindex(columns = ['anime_uid', 'title', 'genre', 'episodes', 'aired', 'score', 'scores', 'profile', 'gender', 'favorites_anime'])

# Sauvegarde des données dans un fichier csv
features.to_csv(data_path + "features.csv", index=False)
print('preprocessing file created .......')
# print(features)



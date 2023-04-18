# la librairie principale pour la gestion des données
import pandas as pd
from datetime import datetime
from dateutil import parser
import re

# l'emplacement des données sur le disque
data_path = "data/"

# chargement des données
animes = pd.read_csv(data_path + "animes.csv", skipinitialspace=True)
profiles = pd.read_csv(data_path + "profiles.csv", skipinitialspace=True)
reviews = pd.read_csv(data_path + "reviews.csv", skipinitialspace=True)

# quelques fonctions utiles pour le prétraitement des données
def convert_to_list(lst):
    lst = lst.strip("[]")
    if lst == "":
        return []
    else:
        return list(map(int, lst.split(", ")))
    


# Convertit une chaîne de caractères représentant une date en un objet datetime

    
def convert_to_date(date_str):
    if date_str == "Unknown":
        return None
    else:
        if 'to' in date_str:
            split_date_str = date_str.split(' to ')
            start_date = datetime.strptime(split_date_str[0], '%b %d, %Y')
            return start_date.year

        elif ',' in date_str:
            try:
                date = datetime.strptime(date_str, "%b %d, %Y")
            except ValueError:
                date = datetime.strptime(date_str, "%b, %Y")
            return date.year
        else:
            try:
                date = parser.parse(date_str)
                return date.year
            except ValueError:
                try:
                    date_str = date_str.split()[0]
                    return datetime.strptime(date_str, "%b %d, %Y").year
                except ValueError:
                    match = re.search(r'(\w{3} \d{2}, \d{4}) to (\w{3} \d{2}, \d{4})', date_str)
                    if match:
                        date_str = match.group(0)
                        date = datetime.strptime(date_str, "%b %d, %Y")
                        return date.year
                    else:
                        return date_str


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

# Remplacement des valeurs manquantes de la colonne gender par Not Specified
features['gender'] = features['gender'].fillna(value='Not Specified')

# Remplir les valeurs manquantes dans la colonne "episodes" par la 1
features['episodes'] = features['episodes'].fillna(value=1)

# supprimer la ligne si la colonne score et la colonne scores sont vides 
features = features.dropna(subset=['score', 'scores'], how='all')

# supprimer les doublons dans le dataset
features = features.drop_duplicates()

# Convertir la colonne "aired" en un objet datetime et en une colonne de date
# features["aired"] = features["aired"].apply(convert_to_date)

# transformer la colonne favorites_anime en liste
features["favorites_anime"] = features["favorites_anime"].str.replace("'", "")   
features["favorites_anime"] = features["favorites_anime"].apply(convert_to_list)


print(features.isnull().sum())


# réorganisation des colonnes
features.reindex(columns = ['anime_uid', 'title', 'genre', 'episodes', 'aired', 'score', 'scores', 'profile', 'gender', 'favorites_anime'])

# Sauvegarde des données dans un fichier csv
features.to_csv(data_path + "features.csv", index=False)
print("------------------")
print('preprocessing file created .......')
print("------------------")
print("Taille du dataset:\t", len(features))
print("------------------")
# print(features)
import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
vectorizer = CountVectorizer()

dataset = pd.read_csv("data/features.csv", skipinitialspace=True) 
# vectorized_bag_of_words = vectorizer.fit_transform(dataset['genre'])
# vectorized_bag_of_words = vectorized_bag_of_words.toarray()

# genre = dataset['genre']
# title = dataset['title']


# def cosine_similarity(show_title, n_recom):
#     similarity_matrix = cosine_similarity(vectorized_bag_of_words, vectorized_bag_of_words[list(np.where(title == show_title)[0]), :])
#     similarity_dataframe = pd.DataFrame(similarity_matrix)
#     similarity_dataframe.index = title 
#     similarity_dataframe =  similarity_dataframe.iloc[:,0]
#     similarity_dataframe = similarity_dataframe.sort_values(ascending = False)
#     similarity_dataframe = similarity_dataframe.drop_duplicates()
#     return list(similarity_dataframe.index)[1:n_recom + 1]

# print(cosine_similarity('Naruto', 10))





favorites_count = {}

def count_favs(x):

    # ne pas compter les animes qui ont la colonne favorites_anime un array vide 
   
  
    for anime_uid in x:
        if len(x["favorites_anime"]) == 0:
            favorites_count[anime_uid] = 0
    
        if anime_uid not in favorites_count:
            favorites_count[anime_uid] = 0
        favorites_count[anime_uid] +=1 
        
dataset[["anime_uid", "favorites_anime"]].apply(count_favs)   

fav_counts = pd.DataFrame.from_dict(favorites_count, orient="index").rename(columns={0:"Count"})
df_fav = fav_counts.sort_values(by="Count", ascending=False).head(10)
df_fav["anime_uid"] = dataset.loc[df_fav.index]["anime_uid"]
df_fav[["anime_uid", "Count"]]
print(df_fav)

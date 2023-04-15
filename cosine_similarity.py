import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("------------------")
print('Recommandation par la similarité du cosinus .......')
print("------------------")
dataset = pd.read_csv("data/features.csv", skipinitialspace=True) 
animes = pd.read_csv("data/animes.csv", skipinitialspace=True) 


# vectorizer = CountVectorizer()
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

import pandas as pd
import pickle
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori
from mlxtend.frequent_patterns import association_rules

print("------------------")
print("Recommandation par l'algorithme a priori.......")
print("------------------")

# importation des données
data = pd.read_csv("./data/features.csv", usecols=['profile', 'anime_uid', 'score'])

# Filter out anime with less than 10 ratings
anime_counts = data.groupby('anime_uid').count()['score']
valid_anime_uids = anime_counts[anime_counts >= 10].index.tolist()
data = data[data['anime_uid'].isin(valid_anime_uids)]

# Filtre les utilisateur avec moins de 10 notes
data = data.groupby('profile').filter(lambda x: len(x) >= 10)

# Ne garder que les profils qui ont au moins une note > 5
data['score'] = (data['score'] > 5).astype(int)
items = data[data['score'] == 1].groupby('profile')['anime_uid'].apply(list).tolist()

te = TransactionEncoder()
te_ary = te.fit(items).transform(items)
df = pd.DataFrame(te_ary, columns=te.columns_)

# Trouver les ensembles d'articles fréquents avec l'algorithme Apriori
frequent_itemsets = apriori(df, min_support=0.0033, use_colnames=True)

# Générer les règles d'association à partir des ensembles fréquents
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=2)
# Trier les règles d'association par le score de lift et les afficher
rules = rules.sort_values(by='lift', ascending=False)

print("Nombre de règles d'association: {}".format(len(rules)))
print("Affichage des 10 premières règles d'association:")
print(rules.head(10))
# save the rules to a file
with open('./apriori_rules/rules.pickle', 'wb') as f:
    pickle.dump(rules, f)
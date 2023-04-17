import pandas as pd
import pickle
from mlxtend.frequent_patterns import association_rules

# load the rules from a file
with open('./apriori_rules/rules.pickle', 'rb') as f:
    rules = pickle.load(f)

# create a function to recommend anime for a given user profile
def recommend_anime(profile):
    # get the rules for the given user profile
    profile_rules = rules[rules['antecedents'] == {profile}]
    # sort the rules by lift
    profile_rules = profile_rules.sort_values(by='lift', ascending=False)
    # get the recommended anime
    recommendations = list(profile_rules['consequents'].values.flatten())
    return recommendations

# test the recommend_anime function
data = pd.read_csv("./data/features.csv", usecols=['profile', 'anime_uid', 'score'])
# Changer valeur de score, si score > 5 alors score = 1 sinon score = 0
data['score'] = data['score'].apply(lambda x: 1 if x > 5 else 0)

# pivot the dataframe
data_pivoted = data.pivot_table(index='profile', columns='anime_uid', values='score', aggfunc='sum', fill_value=0)
bool_df = data_pivoted.astype(bool)

# transform into TransactionEncoder format
te = TransactionEncoder()
te_data = te.fit_transform(bool_df.values)

# create a new dataframe with the TransactionEncoder data
df_te = pd.DataFrame(te_data, columns=te.columns_, index=bool_df.index)

# Trouver les ensembles d'articles fréquents avec l'algorithme Apriori
frequent_itemsets = apriori(df_te, min_support=0.01, use_colnames=True)

# Générer les règles d'association à partir des ensembles fréquents
rules = association_rules(frequent_itemsets, metric='lift', min_threshold=1)

# recommend anime for a given profile
profile = 'user_1'
recommendations = recommend_anime(profile)
print("Recommended anime for {}: {}".format(profile, recommendations))

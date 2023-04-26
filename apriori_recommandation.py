import pandas as pd
import pickle
import users_test

# load the rules from a file
with open('./apriori_rules/rules.pickle', 'rb') as f:
    rules = pickle.load(f)

def recommend_anime(watched_anime, N=3):
    relevant_rules = rules[rules['antecedents'].apply(lambda x: len(set(x).intersection(watched_anime)) > 0)]
    relevant_rules = relevant_rules.sort_values(by='lift', ascending=False)
    top_n_rules = relevant_rules.head(N)
    recommended_items = set()
    for rule in top_n_rules.itertuples():
        recommended_items.update(rule.consequents)
    recommended_items.difference_update(watched_anime)
    recommended_items.discard(0)
    return recommended_items

if __name__ == '__main__':
    # Test the recommendation function
    watched_anime = users_test.USER_2
    watched_anime_uids = users_test.get_anime_uids(watched_anime)
    recommended_anime = recommend_anime(watched_anime_uids, N=10)
    
    for anime in recommended_anime:
        print(users_test.get_anime_title(anime))
    
    #users_test.display_anime_info(recommended_anime)

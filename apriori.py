import pandas as pd
from apyori import apriori


data = pd.read_csv("donnees/features.csv", skipinitialspace=True)

# Group data by profile and anime
grouped_data = data.groupby(['profile', 'anime_uid'])['score'].sum().unstack().reset_index().fillna(0).set_index('profile')

# Convert data to a list of lists
records = []
for _, row in grouped_data.iterrows():
    records.append([str(anime) for anime in row.index if row[anime] > 0])

# Use Apriori algorithm to generate association rules
association_rules = apriori(records, min_support=0.01, min_confidence=0.5, min_lift=1)

# Convert association rules to a list of lists
rules_list = list(association_rules)

# Print the association rules
for rule in rules_list:
    antecedent = ', '.join(list(rule.ordered_statistics[0].items_base))
    consequent = ', '.join(list(rule.ordered_statistics[0].items_add))
    lift = rule.ordered_statistics[0].lift
    print(f'{antecedent} -> {consequent} (lift={lift:.2f})')

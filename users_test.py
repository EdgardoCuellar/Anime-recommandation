import pandas as pd

anime = pd.read_csv("./data/animes.csv", usecols=['uid', 'title', 'synopsis', 'genre', 'episodes', 'score'])

USER_1 = ['Naruto']
USER_2 = ['Naruto', 'Death Note', 'Shingeki no Kyojin']
USER_3 = ['One Piece', 'Bleach', 'Fairy Tail']
USER_4 = ['Death Note', 'Shingeki no Kyojin']
USER_5 = ['Saiki Kusuo no Î¨-nan: Kanketsu-hen']

def get_anime_title(uid):
    return anime[anime['uid'] == uid]['title'].values[0]

def get_anime_uid(anime_title):
    return anime[anime['title'] == anime_title]['uid'].values[0]

def get_anime_uids(anime_titles):
    return [get_anime_uid(anime_name) for anime_name in anime_titles]

def display_anime_info(uid):
    print("*********************************")
    print("Anime: {}".format(get_anime_title(uid)))
    print("Synopsis: {}".format(anime[anime['uid'] == uid]['synopsis'].values[0]))
    print("Genre: {}".format(anime[anime['uid'] == uid]['genre'].values[0]))
    print("Episodes: {}".format(anime[anime['uid'] == uid]['episodes'].values[0]))
    print("Rating: {}".format(anime[anime['uid'] == uid]['score'].values[0]))
    print("*********************************")
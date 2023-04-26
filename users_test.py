import pandas as pd

anime = pd.read_csv("./data/animes.csv", usecols=['uid', 'title', 'synopsis', 'genre', 'episodes', 'score'])

USER_1 = ['Naruto']
USER_2 = ['Naruto', 'Death Note', 'Shingeki no Kyojin']
USER_3 = ['One Piece', 'Bleach', 'Fairy Tail']
USER_4 = ['Death Note', 'Shingeki no Kyojin']


# ***************************************************************************************************

user1_genre_preference = {
        "Comedy": 2,
        "Sports": 1,
        "Drama": 2,
        "School": 1,
        "Action": 5,
        "Sci-Fi": 2,
        "episodes": 10, 
        "release_year": 2021
    }

user2_genre_preference = {
        "Comedy": 2,
        "Sports": 1,
        "Drama": 2,
        "School": 1,
        "Action": 5,
        "Sci-Fi": 2,
        "episodes": 20, 
        "release_year": 2019
    }


user3_genre_preference = {
        "Comedy": 2,
        "Sports": 1,
        "Drama": 2,
        "School": 1,
        "Action": 5,
        "Adventure": 2,
        "episodes": 20, 
        "release_year": 2019
    }

USER_6 = {
    "user_genre_preference" : user2_genre_preference, 
    "user_anime_watched" : USER_2
}

USER_7 = {
    "user_genre_preference" : user1_genre_preference, 
    "user_anime_watched" : USER_3
}

USER_8 = {
    "user_genre_preference" : user3_genre_preference, 
    "user_anime_watched" : USER_4
}

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







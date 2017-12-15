from imdb import IMDb
import pickle
import pandas as pd

pickle_in = open("imdb_dict_set.pickle", "rb")
imdb_dict = pickle.load(pickle_in)
item_profile_dict = {}

pickle_in2 = open("feature_list.pickle", "rb")
feature_list = pickle.load(pickle_in2)

"""
ia = IMDb()
movie = ia.get_movie(114709)
print movie.get("long imdb title")
print movie.get("title")
print movie.get("genre")
"""

for l in open("C:/Users/Jonas/Desktop/ml-20m/movies.csv").readlines()[1:]:
    movie_id = l.strip().split(',')[0]
    item_profile_dict[movie_id] = []
    for each_feature in feature_list:
        if each_feature[0] != "rating":
            if each_feature[1] in imdb_dict[movie_id][each_feature[0]]:
                item_profile_dict[movie_id].append(1)
                print imdb_dict[movie_id]["title"], each_feature
            else:
                item_profile_dict[movie_id].append(0)
        else:
            item_profile_dict[movie_id].append((imdb_dict[movie_id]["rating"])/10)

for id in item_profile_dict:
    print item_profile_dict[id]

print len(item_profile_dict)

pickle_in.close()
pickle_in2.close()

pickle_out = open("item_profiles.pickle", "wb")
pickle.dump(item_profile_dict, pickle_out)
pickle_out.close()
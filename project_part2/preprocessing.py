import pickle

pickle_in = open("imdb_dict.pickle", "rb")
imdb_dict = pickle.load(pickle_in)
genre_set = set()
feature_list = []

for id in imdb_dict:
    for feature_category in imdb_dict[id]:
        #print feature_category
        if feature_category not in {"rating", "title"}:
            imdb_dict[id][feature_category] = set(imdb_dict[id][feature_category])
            #print feature_category, imdb_dict[id][feature_category]
        if feature_category == "genre":
            for each_genre in imdb_dict[id]["genre"]:
                genre_set.add(each_genre)

print genre_set
genre_list = list(genre_set)
print genre_list

pickle_out = open("imdb_dict_set.pickle", "wb")
pickle.dump(imdb_dict, pickle_out)
pickle_out.close()

pickle_out2 = open("genre_list.pickle", "wb")
pickle.dump(genre_list, pickle_out2)
pickle_out2.close()

for genre in genre_list:
    feature_list.append(("genre", genre))

for l in open("top_actors_list.csv").readlines()[1:]:
    actor = l.strip().split(',')[1]
    feature_list.append(("actor", actor))

for l in open("top_directors_list.csv").readlines()[1:]:
    director = l.strip().split(',')[1]
    feature_list.append(("director", director))

feature_list.append(("rating", "rating"))

for feature in feature_list:
    print feature

pickle_out3 = open("feature_list.pickle", "wb")
pickle.dump(feature_list, pickle_out3)
pickle_out3.close()
import pickle
pickle_in = open("item_profiles.pickle", "rb")
old_item_profiles = pickle.load(pickle_in)
pickle_out2 = open("new_item_profiles.pickle", "wb")
pickle_in2 = open("index_map.dat", "rb")
movie_id_map = pickle.load(pickle_in2)

new_item_profiles = {}

for old_ids in old_item_profiles:
    if int(old_ids) in movie_id_map:
        new_ids = movie_id_map[int(old_ids)]
        new_item_profiles[new_ids] = old_item_profiles[old_ids]

for key in new_item_profiles:
    print key, new_item_profiles[key]

print len(new_item_profiles)

pickle.dump(new_item_profiles, pickle_out2)
pickle_in.close()
pickle_out2.close()
pickle_in2.close()
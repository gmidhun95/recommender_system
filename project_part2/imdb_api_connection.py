from imdb import IMDb
import pickle
import pandas as pd

ia = IMDb()
imdb_dict = {}

for l in open("C:/Users/Jonas/Desktop/ml-20m/links.csv").readlines()[1:]:
    movieID, imdbID, tmdbID = l.strip().split(',')
    print int(imdbID)
    movie = ia.get_movie(int(imdbID))

    try:
        title = movie.get("long imdb title").encode("UTF8")
    except AttributeError:
        title = movie.get("long imdb title")

    rating = movie.get("rating", 0.0)

    genre, cast, director, producer, writer = [], [], [], [], []

    try:
        for each_genre in movie.get("genre"):
            genre.append(each_genre.encode("UTF8"))
    except TypeError:
        pass

    try:
        for person in movie.get("cast"):
            cast.append(person.get("name").encode("UTF8"))
    except TypeError:
        pass

    try:
        for person in movie.get("director"):
            director.append(person.get("name").encode("UTF8"))
    except TypeError:
        pass
    try:
        for person in movie.get("producer"):
            producer.append(person.get("name").encode("UTF8"))
    except TypeError:
        pass

    try:
        for person in movie.get("writer"):
            writer.append(person.get("name").encode("UTF8"))
    except TypeError:
        pass

    imdb_dict[movieID] = {"title": title, "rating": rating, "genre": genre, "cast": cast,
                          "director": director, "producer": producer, "writer": writer}


for id in imdb_dict:
    for feature in imdb_dict[id]:
        print feature, ":", imdb_dict[id][feature]

print "number of items in imdb_dict:", len(imdb_dict)

pickle_out = open("imdb_dict.pickle", "wb")
pickle.dump(imdb_dict, pickle_out)
pickle_out.close()

"""
movie = ia.get_movie(388473)
print movie.get("long imdb title")
print movie.get("title")
"""
from imdb import IMDb
import pickle
import pandas as pd

ia = IMDb()
movie = ia.get_movie(114709)
print movie.get("long imdb title")
print movie.get("title")
print movie.get("genre")
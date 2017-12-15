Authors: Midhun Gundapuneni, Jonas Han, Chin-Wen Chang, Sithal Nimmagadda

Overview
--------
In this project, our goal was to utilize the 20M MovieLens dataset to build a system that recommended movies to users based on the users' behaviors(previous ratings).
We wanted a system that both gives a great considered the as well as the specific tastes and preferences of the user.
In order to achieve this, we devised two separate approaches to recommend items: a collaborative filtering approach and a content-based approach.

Content-based Approach
The content-based approach attempts to dissect each item into a list of features that best describes that given item.
Then, we try to describe each user using these same features by analyzing the previous rating history of that user.
For example, if a given user consistently gives romance films high ratings, then we can deduce that the user is a fan of romance films and the user's model will reflect that.
Finally, we can then recommend an item to a user by determining how similar that candidate item's features are to the user's features.

After building the content-based model, we . All
-Similarity Metric (Pearson Correlation vs. Cosine Similarity)  
-Category Weight (i.e. 1-1-1-1, 2-1-1-2, etc.)  


LSH w/ Cosine Similarity



### ***Please note all files below are within the "recommender_system\project_part2" directory.**

Documentation
-------------
Notebook: Report.ipynb  

Content-Based Model
-------------------
BoxOfficeMojoScraper.py: A web scraper written to extract a list of top grossing actors and directors to create our item/user feature space.

imdb_api_connection.py: IMDbPY API to extract genre, cast, director, and rating information for each movie in our dataset.

preprocessing.py: Source code to create a mapping between each feature category (i.e. Genre) and the specific feature (i.e. Action).
The feature space for each user/item is a 1757 dimensional vector which corresponds to the genre, cast, director, and IMDB rating that the user/item belongs to.

item_profiles.py: The source code used to create the feature space for each item in the dataset.

user_profiles.ipynb: The source code to create the feature space for each user in the dataset.

test_content_model.py: The source code to test the content-based model on tune or holdout datasets.


LSH w/ Cosine Similarity
------------------------



Datasets
--------

Movielens 20M: https://grouplens.org/datasets/movielens/20m/


Results
-------

Content_Model_Testing_Results.csv: A file detailing the RMSE, Precision, and Recall for each iteration of tests we conducted.




Plots
-----

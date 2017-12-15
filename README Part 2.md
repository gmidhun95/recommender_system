Authors: Midhun Gundapuneni, Jonas Han, Chin-Wen Chang, Sithal Nimmagadda

Overview
--------
Our goal is to build a system that recommends highly relevant movies to users.
In order to achieve this, our system must accurately predict the rating that a user will give to an unseen item 
as well as display items of high interest to the user.
Therefore, we will be monitoring two key metrics throughout our analyses: root-mean-squared error (RMSE) and precision.
RMSE allows us to measure the accuracy of each prediction and precision allows us to measure 
the quality of our recommender system as a whole.
We will be developing a two-model mixed hybrid system, where one model will have a content-based approach and the other
model will have an approximate nearest neighbors approach.
A mixed hybrid system is a system where recommendations from both models are served simultaneously to a user.
Our benchmarks for each model will be the baseline algorithms found in the Python Surprise package.
We will also be monitoring recall as a metric for serendipity in the content-based approach.

Content-based Approach:
The content-based approach attempts to dissect each item into a list of features that best describes that given item. 
Then, we try to describe each user using these same features by analyzing the previous rating history of that user. 
For example, if a given user consistently gives romance films high ratings, then we can deduce that the user is 
a fan of romance films and the user's model will reflect that.
Next, we compute a predicted rating for a given user and a given item by examining how closely their features
are aligned. That is, the fan of romance of films and  romance films that the user has not already consumed will 
likely have a high similarity value.
We will compute a predicted rating for every user and item pair that the user has not already consumed.
Finally, we can sort these predicted ratings from greatest to least and recommend the top k items to a user.


LSH w/ Cosine Similarity:



### ***Please note the files mentioned below are within the "recommender_system\project_part2" directory.**

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

user_profiles.ipynb: The source code used to create the feature space for each user in the dataset.

test_content_model.py: The source code to test the content-based model on tune or holdout datasets.


LSH w/ Cosine Similarity
------------------------



Datasets
--------

Movielens 20M: https://grouplens.org/datasets/movielens/20m/

All data sets, source code, and files are in the link below:
https://drive.google.com/drive/folders/1dQsyB3lVi2yp9pMlef4qzG4H41EtaVGb?usp=sharing


Results
-------

Content_Model_Testing_Results.csv: A file detailing the RMSE, Precision, and Recall for each iteration of tests we conducted.

Plots
-----


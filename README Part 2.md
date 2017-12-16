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

Here we implement the KNN based models, but using only the approximate nearest neighbors.
We used two different variations of KNN i.e., KNN Basic, KNN Baseline. We refer to the following paper for cosine similarity hashing
(http://www.cs.princeton.edu/courses/archive/spr04/cos598B/bib/CharikarEstim.pdf) and
implimentation from the github repository (https://github.com/marufaytekin/lsh-spark).
We implemented the Sim Hash for the users using pyspark as demonstrated below.
1) create a random vector of size number of movies having values -1,1 (using a normal distribution)
2) calculate dot product of the random vector and the item rating vector of the user, if the dot product is >0 output 1 else output 0
3) repeat steps 1 and 2 for b bands and r rows


### ***Please note the files mentioned below are within the "recommender_system\project_part2" directory.**

Documentation
-------------
Notebook: Report.ipynb

Content-Based Model
-------------------

crawler.ipynb: IMDB data crawler for all the movies in the data

BoxOfficeMojoScraper.py: A web scraper written to extract a list of top grossing actors and directors to create our item/user feature space.

imdb_api_connection.py: IMDbPY API to extract genre, cast, director, and rating information for each movie in our dataset.

preprocessing.py: Source code to create a mapping between each feature category (i.e. Genre) and the specific feature (i.e. Action).
The feature space for each user/item is a 1757 dimensional vector which corresponds to the genre, cast, director, and IMDB rating that the user/item belongs to.

item_profiles.py: The source code used to create the feature space for each item in the dataset.

user_profiles.ipynb: The source code used to create the feature space for each user in the dataset.

test_content_model.py: The source code to test the content-based model on tune or holdout datasets.


LSH w/ Cosine Similarity
------------------------

index matching.ipynb: The source code to modify the movie indices from the movie lens data to new linear indices
data_split.ipynb: The source code to split the data into folds
data_with_bias.ipynb: The source code to convert the data to be used for the knnbaseline model

bias_values.ipynb: The source code for the baseline only approach

complete_run.py: The source code to run the data for all band(b) and row(r) values and calculate similarities
read_br_results.ipynb: The source code to read the output from the complete_run.py

cross_validate.py: The source code to vary the k nearest neighbors in knn models and run 4 fold cross validation on the data for given b and r values

final_run.py: The source code to run the model on the final train set and test set for the knnbasic model

final_run_baseline.py: The source code to run the model on the final train set and test set for the knnbaseline model

Datasets
--------

Movielens 20M: https://grouplens.org/datasets/movielens/20m/

All data sets, source code, and files are in the link below:
https://drive.google.com/drive/folders/1dQsyB3lVi2yp9pMlef4qzG4H41EtaVGb?usp=sharing


Results
-------

Content_Model_Testing_Results.csv: A file detailing the RMSE, Precision, and Recall for each iteration of tests we conducted.

final_test.csv: Final testing data in csv containg the true ratings
test_prediction.csv: A csv file of the prediction from the baseline-only model
final_predictions.dat: A pickle dump file of the final predictions from the knnbasic model
final_predictions_baseline.dat: A pickle dump file of the final predictions from the knnbaseline model

Plots
-----

user_data_plot.ipynb : Code to generate the distribuition of user data for sample 10 users
rmse.ipynb : Code to generate all the plots for the baseline model, knnbasic model and knnbaseline model

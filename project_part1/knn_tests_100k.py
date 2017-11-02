import pandas as pd
from surprise import prediction_algorithms as pa
from surprise import Dataset, Reader, GridSearch, accuracy
import datetime
import random

data = pd.read_csv('./ml-100k/data.csv')
df = pd.DataFrame(data)
df.drop('timestamp', axis=1, inplace=True)
reader = Reader(rating_scale=(1, 5))
dataset = Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader)
raw_ratings = dataset.raw_ratings
random.shuffle(raw_ratings)
threshold = int(.8 * len(raw_ratings))
A_raw_ratings = raw_ratings[:threshold]
B_raw_ratings = raw_ratings[threshold:]
dataset.raw_ratings = A_raw_ratings
dataset.split(n_folds=5)

#Grid search to find optimal parameters.
similarities = ['cosine', 'msd', 'pearson', 'pearson_baseline']
user_based = [True, False]
start_time = ('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))
sim_options = {'name': similarities, 'user_based': user_based}
param_grid = {'k': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 'min_k': [5], 'sim_options': sim_options}
grid_search = GridSearch(pa.KNNBaseline, param_grid=param_grid, measures=['MAE', 'RMSE', 'FCP'])
grid_search.evaluate(dataset)
end_time = ('Timestamp: {:%Y-%b-%d %H:%M:%S}'.format(datetime.datetime.now()))


algo = grid_search.best_estimator["RMSE"]
best_score = grid_search.best_score["RMSE"]
best_params = grid_search.best_params["RMSE"]
results_df = pd.DataFrame.from_dict(grid_search.cv_results)
results_df.to_csv("100k_KNNBaseline_Results.csv")
print "Start Time: ", start_time
print "End Time: ", end_time


print "size of A: ", len(A_raw_ratings)
print "size of B: ", len(B_raw_ratings)
print "Best score: ", best_score
print "Best parameters: ", best_params
trainset = dataset.build_full_trainset()
algo.train(trainset)
testset = dataset.construct_testset(B_raw_ratings)
predictions = algo.test(testset)
print('Unbiased accuracy on B,', accuracy.rmse(predictions))
accuracy.rmse(predictions)
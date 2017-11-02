import pandas as pd
from surprise import prediction_algorithms as pa
from surprise import Dataset, Reader, GridSearch, accuracy
from surprise import evaluate, print_perf
import datetime
from collections import defaultdict


def precision_recall_at_k(predictions, k=10, threshold=3.5):
    '''Return precision and recall at k metrics for each user.'''
    # First map the predictions to each user.
    user_est_true = defaultdict(list)
    for uid, _, true_r, est, _ in predictions:
        user_est_true[uid].append((est, true_r))
    precisions = dict()
    recalls = dict()
    for uid, user_ratings in user_est_true.items():
        # Sort user ratings by estimated value
        user_ratings.sort(key=lambda x: x[0], reverse=True)
        # Number of relevant items
        n_rel = sum((true_r >= threshold) for (_, true_r) in user_ratings)
        # Number of recommended items in top k
        n_rec_k = sum((est >= threshold) for (est, _) in user_ratings[:k])
        # Number of relevant and recommended items in top k
        n_rel_and_rec_k = sum(((true_r >= threshold) and (est >= threshold))
                              for (est, true_r) in user_ratings[:k])
        # Precision@K: Proportion of recommended items that are relevant
        precisions[uid] = n_rel_and_rec_k / n_rec_k if n_rec_k != 0 else 1
        # Recall@K: Proportion of relevant items that are recommended
        recalls[uid] = n_rel_and_rec_k / n_rel if n_rel != 0 else 1
    return precisions, recalls

one_hundred_k_data = pd.read_csv('./ml-100k/data.csv')
two_hundred_fifty_data = pd.read_csv("ratingsNew_250k.csv")
five_hundred_data = pd.read_csv("ratingsNew_500k.csv")
seven_hundred_fifty_data = pd.read_csv("ratingsNew_750k.csv")
one_million_data = pd.read_csv("./movielens_1M/ratings.csv")

datasets = [one_hundred_k_data, two_hundred_fifty_data, five_hundred_data, seven_hundred_fifty_data, one_million_data]
datasets_names = ["100k", "250k", "500k", "750k", "1M"]
surprise_datasets = []

for each_dataset in datasets:
    df = pd.DataFrame(each_dataset)
    df.drop('timestamp', axis=1, inplace=True)
    print df.head()
    reader = Reader(rating_scale=(1, 5))
    surprise_datasets.append(Dataset.load_from_df(df[['userId', 'movieId', 'rating']], reader))


user_based = [True, False]
sim_options = {'name': "pearson_baseline", 'user_based': user_based}
list_of_k = [30, 40, 50, 60, 70]
param_grid = {'k': [30, 40, 50, 60, 70], 'min_k': [5], 'sim_options': sim_options}
grid_search = GridSearch(pa.KNNBaseline, param_grid=param_grid, measures=['MAE', 'RMSE', 'FCP'])

"""
for i in range(len(surprise_datasets)):
    surprise_datasets[i].split(n_folds=5)
    grid_search.evaluate(surprise_datasets[i])
    results_df = pd.DataFrame.from_dict(grid_search.cv_results)
    results_df.to_csv(results[i])
"""

results_dict = {"Dataset": [], "User-based?": [], "k": [], "RMSE": [], "MAE": [], "Precision": [], "Recall": [], "Running_Time": []}

for i in range(len(surprise_datasets)):
    for each_option in user_based:
        for each_k in list_of_k:
            surprise_datasets[i].split(n_folds=5)
            sim_options = {'name': "pearson_baseline", 'user_based': each_option}
            algo = pa.KNNBaseline(k=each_k, min_k=5, sim_options=sim_options)
            RMSEs, MAEs, precision_percents, recall_percents = [], [], [], []
            start_time = datetime.datetime.now()
            for train_set, test_set in surprise_datasets[i].folds():
                print "User-based: ", each_option
                print "k: ", each_k
                algo.train(train_set)
                predictions = algo.test(test_set)
                rmse = accuracy.rmse(predictions, verbose=True)
                RMSEs.append(rmse)
                mae = accuracy.mae(predictions, verbose=True)
                MAEs.append(mae)
                precisions, recalls = precision_recall_at_k(predictions=predictions, k=10, threshold=3)
                precision_percent = (sum(prec for prec in precisions.values()) / float(len(precisions)))
                precision_percents.append(precision_percent)
                recall_percent = (sum(rec for rec in recalls.values()) / float(len(recalls)))
                recall_percents.append(recall_percent)
                print "Precision, Recall: ", precision_percent, recall_percent
            end_time = datetime.datetime.now()
            average_RMSE = (sum(x for x in RMSEs) / len(RMSEs))
            average_MAE = (sum(x for x in MAEs) / len(MAEs))
            average_precision = (sum(x for x in precision_percents) / len(precision_percents))
            average_recall = (sum(x for x in recall_percents) / len(recall_percents))
            results_dict["Dataset"].append(datasets_names[i])
            results_dict["User-based?"].append(each_option)
            results_dict["k"].append(each_k)
            results_dict["RMSE"].append(average_RMSE)
            results_dict["MAE"].append(average_MAE)
            results_dict["Precision"].append(average_precision)
            results_dict["Recall"].append(average_recall)
            results_dict["Running_Time"].append(end_time-start_time)
            print "Average RMSE: ", average_RMSE
            print "Average MAE: ", average_MAE
            print "Average Precision: ", average_precision
            print "Average Recall: ", average_recall
            print "Time Difference: ", (end_time-start_time)

results_df = pd.DataFrame(results_dict)
results_df.to_csv("250k_to_1M_Results.csv")

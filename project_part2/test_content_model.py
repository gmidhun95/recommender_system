import pickle
from scipy import spatial
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.metrics import mean_squared_error
from math import sqrt
from collections import defaultdict
import datetime
import numpy as np
from scipy.stats.stats import pearsonr
import random


def test_content_model(user_profiles_pickle, item_profiles_pickle, ratings_file, k=10, threshold=3.5):
    pickle_out = open("predicted_vs_actual.pickle", "wb")
    pickle_in = open(user_profiles_pickle, "rb")
    user_profiles_dict = pickle.load(pickle_in)
    print "done reading in item profiles."
    pickle_in2 = open(item_profiles_pickle, "rb")
    item_profiles_dict = pickle.load(pickle_in2)
    print "done reading in user profiles."
    predicted_ratings_list, actual_ratings_list = [], []
    user_est_true = defaultdict(list)
    precisions = dict()
    recalls = dict()
    metrics_dict = dict()

    for line in open(ratings_file).readlines():
        print line
        user_id, item_id, actual_rating = line.strip().split(",")
        user_id = int(user_id)
        item_id = int(item_id)
        actual_rating = float(actual_rating)
        user_vector = user_profiles_dict[user_id]
        item_vector = item_profiles_dict[item_id]
        user_vector_common, item_vector_common = [], []
        print "found user and item vectors."
        # for i in range(0, len(user_vector)):
        #     if user_vector[i] != 0 or item_vector[i] != 0:
        #         user_vector_common.append(user_vector[i])
        #         item_vector_common.append(item_vector[i])
        # pearson_corr = pearsonr(user_vector, item_vector)[0]
        # if np.isnan(pearson_corr):
        #     pearson_corr = 0.5
        # predicted_rating = (((pearson_corr - (-1)) * 4.5) / 2) + 0.5
        cosine_sim = 1 - spatial.distance.cosine(user_vector, item_vector)
        if np.isnan(cosine_sim):
            cosine_sim = 0
        print "finished computing cosine similarity."
        predicted_rating = (((cosine_sim - (-1)) * 4.5) / 2) + 0.5
        #predicted_rating = random.uniform(0.5, 5.0)
        print "actual rating:", actual_rating, "predicted rating:", predicted_rating
        predicted_ratings_list.append(predicted_rating)
        actual_ratings_list.append(actual_rating)
        user_est_true[user_id].append((predicted_rating, actual_rating))

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

    pickle.dump(user_est_true, pickle_out)

    rmse = sqrt(mean_squared_error(actual_ratings_list, predicted_ratings_list))
    precision = (sum(prec for prec in precisions.values()) / float(len(precisions)))
    recall = (sum(rec for rec in recalls.values()) / float(len(recalls)))

    pickle_in.close()
    pickle_in2.close()
    pickle_out.close()
    metrics_dict["RMSE"] = rmse
    metrics_dict["Precision"] = precision
    metrics_dict["Recall"] = recall
    return metrics_dict


print test_content_model("user_profile_small.pickle", "new_item_profiles.pickle",
                         "C:/Users/Jonas/Desktop/recommender_system/project_part2/Splits/split_4.csv")

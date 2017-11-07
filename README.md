# recommender_system
basics of recommendation systems

In this project, our goal was to utilize the Movielens datasets and build a system that recommended movies to users' behaviors.
We achieved this by implementing two collaborative filtering recommender systems (one memory-based & one model-based) using the scikit-surprise library in Python.


Authors: Midhun Gundapuneni, Jonas Han, Chi-Wen Chang, Sithal Nimmagadda


Write-up: 



**Please note all paths below are within the "recommender_system\project_part1" directory.**

Memory-based Algorithms + Tests
-------------------------------
knn_tests_100k.py: The source code to implement the KNN algorithms in Surprise (using 100k dataset) and 
run the grid search tests to find optimal hyperparameters for each algorithm.
KNNBaselineTests.py: The source code used to analyze performance of our chosen memory-based algorithm (KNN Baseline) against
larger datasets. 


Model-based Algorithms + Tests
------------------------------



Datasets
--------
100k: ml-100k/data.csv
250k: ratingsNew_250k.csv
500k: ratingsNew_500k.csv
750k: ratingsNew_750k.csv
1M: movielens_1M/ratings.csv


Results
-------
100k_KNNBaseline_Results.csv - Results for the grid search using the KNN Baseline algorithm.
100k_KNNBasic_Results.csv - Results for the grid search using the KNN Basic algorithm.
100k_KNNWithMeans_Results.csv - Results for the grid search using the KNN With Means algorithm.
100k_KNNWithZScore_Results.csv - Results for the grid search using the KNN With Z-Score algorithm.
100k_to_1M_Results.csv - Results for testing performance of our chosen memory-based algorithm (KNN Basline) against larger datasets.
100k_Best_Algo_Results.txt - Best parameters and error for each algorithm (from grid search) and the results using the same parameters on the unbiased test dataset.


Plots
-----
KNN_Performance_Plots_Revised.ipynb - All plots associated with analyzing performance of KNN algorithms.

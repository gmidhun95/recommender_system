Authors: Midhun Gundapuneni, Jonas Han, Chin-Wen Chang, Sithal Nimmagadda

Overview
--------
In this project, our goal was to utilize the MovieLens datasets and build a system that recommended movies based on users' behaviors.
We achieved this by implementing two popular collaborative filtering models (one memory-based & one model-based) using the scikit-surprise library in Python.
We chose the optimal memory-based and model-based systems by systematically testing the following combinations:

Memory-based  
-Algorithm (i.e. KNN Basic, KNN With Means, etc.)  
-Item-based vs. User-based  
-Similarity Metric (i.e. Pearson Correlation, Cosine Similarity, etc.)  
-Neighborhood Size (i.e. k=10, 20, 30, etc.)  

Model-based  
-Algorithm (i.e. SVD, NMF)  
-Parameters (i.e. number of latent factors, etc.)  

From these combinations, we were able to determine a single best memory-based and a single best model-based algorithm.
Note: Performance of each model variation was primarily gauged by the root-mean-squred error (RMSE) accuracy metric. However, we also considered other accuracy metrics (i.e. MAE, precision, recall) when we made our final decision.

After finding the optimal combination of parameters for each model, we ran our models again on the larger datasets to evaluate how performance changed as a function of data size.
We were able to determine that the SVD (model-based) algorithm outperformed the KNN (memory-based) algorithm in terms of RMSE, MAE, precision, and run-time.
Therefore, we would recommend utilizing the SVD algorithm during actual implementation.


Write-up :
--------
documentatiom: Personalization-mini-project_v1.docx
markup/notebook: project_part1/Report.ipynb



**Please note all paths below are within the "recommender_system\project_part1" directory.**

Memory-based Algorithms + Tests
-------------------------------
knn_tests_100k.py: The source code to implement the KNN algorithms in Surprise (using 100k dataset) and run the grid search tests to find optimal hyperparameters for each algorithm.

KNNBaselineTests.py: The source code used to analyze performance of our chosen memory-based algorithm (KNN Baseline) against larger datasets. 


Model-based Algorithms + Tests
------------------------------

NMF.ipynb: The source code to vary various hyperparamenters and run the grid search to find the optimal hyperparameters for the NMF algorithms.

SVD.ipynb: The source code to vary hyperparameters and run the grid search to find the optimal hyperparamets for the SVD algorithm.

plot_data.ipynb: The source code to observe the comparision plot of NMF and SVD with respect to the number of latent factors. Results are dumped into the pickle file "nmf_svd_factor_plot.dat".

scale_data.ipynb: The source code to run the SVD algorithm on different datasets to see the results as the scale grows. Results are dumped into the csv file "scale_svd_results.csv".


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

100k_to_1M_Results.csv - Results for evaluating performance of our chosen memory-based algorithm (KNN Basline) on larger datasets.

100k_Best_Algo_Results.txt - Best parameters and error for each algorithm (from grid search) and the results using the same parameters on the unbiased test dataset.

nmf_svd_factor_plot.dat - Pickle file with results for performance comparison between NMF and SVD algorithms.

scale_svd_results.csv - Results for evaluating performance of our chosen model-based algorithm (SVD) on larger datasets.

Plots
-----
KNN_Performance_Plots_Revised.ipynb - All plots associated with analyzing performance of KNN algorithms.

revised_plot.ipynb: The source code to compare the model-based SVD algo and memory-based algorithms with respect to performance and time

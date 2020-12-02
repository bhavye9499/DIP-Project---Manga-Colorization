from sklearn.cluster import DBSCAN
from sklearn.mixture import GaussianMixture

from src.visualizer import *


def get_pixel_neighbourhood(mat, location, shape):
    x, y = location
    P, Q = shape
    x_max = min(x + P // 2, mat.shape[0])
    y_max = min(y + Q // 2, mat.shape[1])
    x_min = max(x - P // 2, 0)
    y_min = max(y - Q // 2, 0)
    return mat[x_min:x_max, y_min:y_max]


def get_major_cluster(feature_vectors, eps=1, min_samples=20):
    model = DBSCAN(eps=eps, min_samples=min_samples, n_jobs=-1)
    yhat = model.fit_predict(feature_vectors)
    clusters, cluster_counts = np.unique(yhat, return_counts=True)
    print(f'clusters = {list(zip(clusters, cluster_counts))}')
    visualize_clustered_feature_vectors(feature_vectors, yhat)
    M_cluster = clusters[np.where(cluster_counts == max(cluster_counts[1:]))[0][0]]
    row_ix = np.where(yhat == M_cluster)
    major_cluster = np.asarray(feature_vectors)[row_ix]
    return major_cluster

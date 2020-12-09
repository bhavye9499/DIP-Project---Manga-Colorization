import numpy as np
from matplotlib import pyplot as plt
from skimage.color import label2rgb
from sklearn.cluster import KMeans
from sklearn.decomposition import TruncatedSVD
from PIL import Image


def visualize_clustered_feature_vectors(feature_vectors, cluster_ids):
    model = TruncatedSVD(n_components=2)
    yhat = model.fit_transform(feature_vectors)
    clusters = np.unique(cluster_ids)
    for cluster in clusters:
        row_ix = np.where(cluster_ids == cluster)
        plt.scatter(yhat[row_ix, 0], yhat[row_ix, 1])
    plt.legend(labels=[f'Cluster_{cluster}' for cluster in clusters])
    plt.show()


def visualize_distance_map(distance_map, cmap=None):
    plt.imshow(distance_map, cmap=cmap)
    plt.colorbar()
    plt.show()


def visualize_feature_vectors(feature_vectors):
    model = TruncatedSVD(n_components=2)
    yhat = model.fit_transform(feature_vectors)
    plt.scatter(yhat[:, 0], yhat[:, 1])
    plt.show()


def visualize_feature_vector_set_of_image(img_feature_vector_set, n_clusters, cmap=None):
    P, Q, R = img_feature_vector_set.shape
    model = KMeans(n_clusters=n_clusters, max_iter=10)
    X = np.reshape(img_feature_vector_set, (P * Q, R))
    yhat = model.fit_predict(X)
    L = label2rgb(yhat)
    output = np.reshape(L, (P, Q, 3))
    plt.imshow(output, cmap=cmap)
    plt.show()


def visualize_filter_bank(filter_bank, m, n):
    fig, axs = plt.subplots(m, n)
    for i in range(m):
        for j in range(n):
            if m == 1:
                axs[j].imshow(np.real(filter_bank[i * m + j]), cmap='gray')
            else:
                axs[i, j].imshow(np.real(filter_bank[i * n + j]), cmap='gray')
    plt.show()


def visualize_image(img_arr, mode=None):
    Image.fromarray(img_arr, mode=mode).show()


def visualize_scribbled_pixels(img, scribbled_pixels):
    output = img
    for x, y in scribbled_pixels:
        output[x, y] = 0
    plt.imshow(output, cmap='gray')
    plt.show()
